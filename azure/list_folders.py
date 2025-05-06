from azure.identity import ClientSecretCredential
from azure.storage.blob import BlobServiceClient
import os
import logging
from collections import defaultdict

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def load_environment_variables():
    """Load environment variables from .env file if available."""
    try:
        from dotenv import load_dotenv
        load_dotenv()
        logger.info("Environment variables loaded from .env file")
    except ImportError:
        logger.warning("python-dotenv package not found. Using environment variables directly.")

def get_blob_service_client():
    """Create and return an authenticated BlobServiceClient using service principal."""
    try:
        tenant_id = os.getenv("AZURE_TENANT_ID")
        client_id = os.getenv("AZURE_CLIENT_ID")
        client_secret = os.getenv("AZURE_CLIENT_SECRET")
        storage_account = os.getenv("AZURE_STORAGE_ACCOUNT_NAME")
        
        credential = ClientSecretCredential(tenant_id, client_id, client_secret)
        blob_service_client = BlobServiceClient(
            f"https://{storage_account}.blob.core.windows.net", 
            credential=credential
        )
        
        logger.info(f"Successfully connected to storage account: {storage_account}")
        return blob_service_client
    except Exception as e:
        logger.error(f"Authentication failed: {str(e)}")
        raise

def create_directory(path):
    """Create a directory if it doesn't exist."""
    if not os.path.exists(path):
        os.makedirs(path)
        logger.info(f"Created directory at: {path}")
    else:
        logger.info(f"Using existing directory at: {path}")

def create_output_directory(directory_name="container_contents"):
    """Create a directory for storing results if it doesn't exist."""
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_dir = os.path.join(project_root, directory_name)
    create_directory(output_dir)
    return output_dir

def list_folders_in_container(container_name):
    """List all folders (prefixes) in the specified container."""
    try:
        blob_service_client = get_blob_service_client()
        container_client = blob_service_client.get_container_client(container_name)
        
        logger.info(f"Listing folders in container '{container_name}':")
        blobs = list(container_client.list_blobs())
        
        if not blobs:
            logger.info("No blobs found in the container.")
            return []
        
        folders = defaultdict(set)
        for blob in blobs:
            parts = blob.name.split('/')
            current_path = ""
            for i, part in enumerate(parts[:-1]):
                current_path = f"{current_path}/{part}" if current_path else part
                folders[current_path].add(parts[i+1] if i+1 < len(parts) else "")
        
        log_folder_structure(folders)
        return dict(folders)
    except Exception as e:
        logger.error(f"Error listing folders: {str(e)}")
        raise

def log_folder_structure(folders):
    """Log the folder structure."""
    if not folders:
        logger.info("No folders found in the container (flat structure).")
    else:
        logger.info("Folder structure:")
        for folder_path, contents in sorted(folders.items()):
            logger.info(f"- {folder_path}/")
            for item in sorted(contents):
                if item:
                    logger.info(f"  -- {item}")

def save_to_file(output_path, content):
    """Save content to a file with UTF-8 encoding."""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)
    logger.info(f"Content saved to {output_path}")

def save_folder_structure(container_name, output_file="folder_structure.txt"):
    """Save the folder structure to a file."""
    try:
        folders = list_folders_in_container(container_name)
        output_dir = create_output_directory()
        output_path = os.path.join(output_dir, output_file)
        
        content = f"Folder structure for container '{container_name}':\n\n"
        if not folders:
            content += "No folders found (flat structure).\n"
        else:
            for folder_path, contents in sorted(folders.items()):
                content += f"- {folder_path}/\n"
                for item in sorted(contents):
                    if item:
                        content += f"  -- {item}\n"
        
        save_to_file(output_path, content)
        return output_path
    except Exception as e:
        logger.error(f"Error saving folder structure: {str(e)}")
        raise

def save_blob_contents(container_name, output_file="blob_contents.txt"):
    """Saves all blob names to a file and download the actual blob content."""
    try:
        blob_service_client = get_blob_service_client()
        container_client = blob_service_client.get_container_client(container_name)
        blobs = list(container_client.list_blobs())
        
        output_dir = create_output_directory()
        blobs_dir = os.path.join(output_dir, "blobs")
        create_directory(blobs_dir)
        
        output_path = os.path.join(output_dir, output_file)
        content = f"Blob contents for container '{container_name}':\n\n"
        
        if not blobs:
            content += "No blobs found in the container.\n"
        else:
            for blob in sorted(blobs, key=lambda x: x.name):
                content += f"- {blob.name}\n  Size: {blob.size} bytes\n  Last Modified: {blob.last_modified}\n  Content Type: {blob.content_settings.content_type}\n\n"
                download_blob(container_client, blob, blobs_dir)
        
        save_to_file(output_path, content)
        return output_path
    except Exception as e:
        logger.error(f"Error saving blob contents: {str(e)}")
        raise

def download_blob(container_client, blob, blobs_dir):
    """Download blob while preserving its directory structure."""
    blob_path_parts = blob.name.split('/')
    download_path = os.path.join(blobs_dir, *blob_path_parts)
    create_directory(os.path.dirname(download_path))
    
    try:
        blob_client = container_client.get_blob_client(blob.name)
        with open(download_path, "wb") as download_file:
            download_file.write(blob_client.download_blob().readall())
        logger.info(f"Downloaded blob content: {blob.name} -> {download_path}")
    except Exception as download_error:
        logger.error(f"Error downloading blob {blob.name}: {str(download_error)}")

def download_folder_contents(container_name, folder_prefix, output_dir=None):
    """Download all blobs from a specific folder in the container."""
    try:
        blob_service_client = get_blob_service_client()
        container_client = blob_service_client.get_container_client(container_name)
        
        folder_prefix = f"{folder_prefix}/" if folder_prefix and not folder_prefix.endswith('/') else folder_prefix
        output_dir = output_dir or os.path.join(create_output_directory(), folder_prefix.rstrip('/').replace('/', '_'))
        create_directory(output_dir)
        
        blobs = list(container_client.list_blobs(name_starts_with=folder_prefix))
        
        if not blobs:
            logger.info(f"No blobs found in folder '{folder_prefix}'")
            return []
        
        downloaded_files = []
        for blob in blobs:
            relative_path = blob.name[len(folder_prefix):]
            if not relative_path:
                continue
            
            download_path = os.path.join(output_dir, relative_path)
            download_blob(container_client, blob, output_dir)
            downloaded_files.append(download_path)
        
        logger.info(f"Downloaded {len(downloaded_files)} files from folder '{folder_prefix}' to {output_dir}")
        return downloaded_files
    except Exception as e:
        logger.error(f"Error downloading folder contents: {str(e)}")
        raise

if __name__ == "__main__":
    load_environment_variables()
    container_name = os.getenv("AZURE_STORAGE_CONTAINER_NAME")
    output_dir = create_output_directory()
    
    save_folder_structure(container_name)
    save_blob_contents(container_name)
    
    container_dir = os.path.join(output_dir, container_name)
    logger.info(f"Downloading entire container '{container_name}' with exact folder structure to {container_dir}...")
    download_folder_contents(container_name, "", container_dir)
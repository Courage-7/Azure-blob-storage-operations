from log_config import setup_logging
from list_folders import (
    load_environment_variables,
    create_output_directory,
    save_folder_structure,
    save_blob_contents,
    download_folder_contents
)
import os

def main():
    logger = setup_logging()
    try:
        # Load environment variables
        load_environment_variables()
        
        # Validate required Azure credentials
        required_vars = [
            "AZURE_TENANT_ID", 
            "AZURE_CLIENT_ID", 
            "AZURE_CLIENT_SECRET",
            "AZURE_STORAGE_ACCOUNT_NAME",
            "AZURE_STORAGE_CONTAINER_NAME"
        ]
        
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        if missing_vars:
            logger.error(f"Missing required environment variables: {', '.join(missing_vars)}")
            logger.info("Please ensure you have a .env file with these variables or they are set in your environment")
            return
        
        container_name = os.getenv("AZURE_STORAGE_CONTAINER_NAME")
        
        output_dir = create_output_directory()
        
        # List and save folder structure
        logger.info("Starting folder structure analysis...")
        save_folder_structure(container_name)
        
        # Save blob contents and metadata
        logger.info("Starting blob content analysis and download...")
        save_blob_contents(container_name)
        
        # Download entire container
        container_dir = os.path.join(output_dir, container_name)
        logger.info(f"Downloading entire container '{container_name}'...")
        download_folder_contents(container_name, "", container_dir)
        
        logger.info("All operations completed successfully")
        
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        raise

if __name__ == "__main__":
    main()
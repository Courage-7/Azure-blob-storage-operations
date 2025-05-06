import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Azure Storage Account Configuration
AZURE_CONFIG = {
    'tenant_id': os.getenv('AZURE_TENANT_ID'),
    'client_id': os.getenv('AZURE_CLIENT_ID'),
    'client_secret': os.getenv('AZURE_CLIENT_SECRET'),
    'storage_account': os.getenv('AZURE_STORAGE_ACCOUNT_NAME'),
    'container_name': os.getenv('AZURE_STORAGE_CONTAINER_NAME')
}

# Output Directory Configuration
OUTPUT_CONFIG = {
    'base_dir': 'container_contents',
    'blobs_dir': 'blobs',
    'folder_structure_file': 'folder_structure.txt',
    'blob_contents_file': 'blob_contents.txt'
}

# Logging Configuration
LOGGING_CONFIG = {
    'format': '%(asctime)s - %(levelname)s - %(message)s',
    'level': 'INFO'
}
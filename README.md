# Azure Blob Storage Utility

This project provides a set of Python utilities for interacting with Azure Blob Storage, allowing you to list, download, and manage blob content while preserving folder structures.

## Features

- Connect to Azure Blob Storage using service principal authentication
- List all folders and blobs in a container
- Download entire containers or specific folders while preserving folder structure
- Save metadata about blobs including size, last modified date, and content type
- Comprehensive logging for all operations
- Support for environment variables through .env files

## Project Structure

```plaintext
azure-blob/
├── azure/                      # Main package directory
│   ├── __init__.py             # Package initialization
│   ├── config.py               # Configuration settings
│   ├── list_folders.py         # Core functionality for listing and downloading blobs
│   ├── log_config.py           # Logging configuration
│   └── main.py                 # Main entry point
├── container_contents/         # Output directory (created at runtime)
│   ├── blobs/                  # Downloaded blob contents
│   ├── folder_structure.txt    # Text file with folder structure
│   └── blob_contents.txt       # Text file with blob metadata
├── logs/                       # Log directory (created at runtime)
├── .env                        # Environment variables (not in repo)
├── .gitignore                  # Git ignore file
├── README.md                   # Project documentation
└── requirements.txt            # Python dependencies
```

## Getting Started

### Prerequisites

- Python 3.6+
- Azure Storage account with blob containers
- Service principal with appropriate permissions

### Installation

1. Clone this repository:
```bash
git clone https://github.com/courage-7/azure-blob.git
cd azure-blob
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. Create a .env file in the root directory with your Azure credentials:
```plaintext
AZURE_TENANT_ID=your_tenant_id
AZURE_CLIENT_ID=your_client_id
AZURE_CLIENT_SECRET=your_client_secret
AZURE_STORAGE_ACCOUNT_NAME=your_storage_account_name
AZURE_STORAGE_CONTAINER_NAME=your_container_name
```

## Usage

Run the main script to download and analyze a container:
```bash
python -m azure.main
```

This will:
1. Connect to your Azure Blob Storage account
2. List and save the folder structure of the specified container
3. Save metadata about all blobs in the container
4. Download all blob contents while preserving folder structure

## Output

The script creates the following output:
- container_contents/folder_structure.txt : Text file showing the folder hierarchy
- container_contents/blob_contents.txt : Text file with metadata for each blob
- container_contents/blobs/ : Directory containing all downloaded blobs with their original folder structure
- logs/azure_blob_[timestamp].log : Log file with detailed operation information

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
from azure.storage.blob import BlobServiceClient

def upload_to_blob(local_path: str, blob_name: str, storage_conn: str, container_name:str):
    
    """     
    Uploads a local file to Azure Blob Storage.
    Creates the container if it does not already exist.
    """
    
    if not storage_conn:
        raise Exception("STORAGE_CONNECTION_STRING is missing")
    if not container_name:
        raise Exception("CONTAINER_NAME is missing")
    blob_service_client = BlobServiceClient.from_connection_string(storage_conn)
    container_client = blob_service_client.get_container_client(container_name)

    # Create container if not exists
    try:
        container_client.create_container()
    except:
        pass

    with open(local_path, "rb") as f:
        container_client.upload_blob(blob_name, f, overwrite=True)
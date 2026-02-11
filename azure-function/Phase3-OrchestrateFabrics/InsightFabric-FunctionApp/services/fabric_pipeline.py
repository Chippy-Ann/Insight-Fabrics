import requests
import os
import logging
import json
from azure.identity import ClientSecretCredential
from services.Keyvault_reader import get_secret
from urllib.parse import urlparse
def get_fabric_token():

    tenant_id = os.environ["TENANT_ID"]     #sp-fabric-orchestrator

    client_id = os.environ["CLIENT_ID"]
    client_secret = os.environ["CLIENT_SECRET"]

    

    credential = ClientSecretCredential(
        tenant_id=tenant_id,
        client_id=client_id,
        client_secret=client_secret
    )

    # Fabric resource scope
    token = credential.get_token("https://api.fabric.microsoft.com/.default")

    return token.token
def trigger_fabric_pipeline(blob_url: str):

    workspace_id = os.environ["FABRIC_WORKSPACE_ID"]
    master_pipeline_id = os.environ["FABRIC_PIPELINE_ID"]



    token =get_fabric_token()

    url_template=os.environ["FABRICS_PIPELINE_URL"] 
    url = url_template.format(
        workspace_id=workspace_id,
        pipeline_id=os.environ["FABRIC_PIPELINE_ID"]
    )
    # url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/pipelines/{tobronze_pipeline_id}/jobs"
    list_workspace_items(workspace_id)
    #https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/items/{pipeline_id}/jobs/instances?jobType=Pipeline
    # url=f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/items/{tobronze_pipeline_id}/jobs"
    logging.info(f"starting pipleneid {master_pipeline_id} ")
    logging.info(f"url: {url} ")

    parsed=urlparse(blob_url)
    path_parts = parsed.path.lstrip("/").split("/")  # remove leading slash
    
    container_name = path_parts[0]
    folder_path = "/".join(path_parts[1:-1])
    file_name = path_parts[-1]
    
    payload_template = os.environ["FABRIC_PIPELINE_PAYLOAD"]
    logging.info(f"Payload: {payload_template}")

    payload = json.loads(payload_template)
    payload["executionData"]["parameters"]["containername"] = container_name
    payload["executionData"]["parameters"]["foldername"] = folder_path
    payload["executionData"]["parameters"]["filename"] = file_name
    logging.info(f"Payload: {payload}")



    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 202:
        # Fabric returns the job tracking URL in the 'Location' header
        operation_url = response.headers.get("Location")
        job_instance_id = operation_url.split("/")[-1] if operation_url else None
        logging.info(f"Pipeline triggered successfully. Job Instance ID: {job_instance_id}")
        return f"Success: {job_instance_id}"

    elif response.status_code in [429, 500, 502, 503, 504]:
        # These are "Retryable" errors (Throttling or Server issues)
        msg = f"Fabric Server Error {response.status_code}. Retrying via Azure Policy..."
        logging.warning(msg)
        raise Exception(msg) # This triggers your 5-run retry policy

    else:
        # Only parse JSON if there's actually content (for errors)
        try:
            error_details = response.json()
            logging.error(f"Failed to trigger pipeline: {error_details}")
            return f"Failed with status {error_details}" # We return instead of raise to stop pointless retries

        except ValueError:
            logging.error(f"Failed with status {response.status_code}: {response.text}")
            return f"Failed with status {response.status_code}: {response.text}" # We return instead of raise to stop pointless retries




def list_workspace_items(workspace_id):
    token = get_fabric_token()
    logging.info(f"calling workspaceid {workspace_id} info")
    url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/items"

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(url, headers=headers)
    logging.info(response.status_code)
    logging.info(response.text)

    return response.json()
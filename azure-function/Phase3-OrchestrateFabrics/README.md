# Phase 3 – Fabric Orchestration Azure Function

This **Python 3.10 Azure Function** orchestrates the Insight Fabrics data pipelines.  
It is **event-driven**, triggered by **BlobCreated events** in Azure Storage, and calls the **Fabric Master Pipeline** with parameters extracted from the blob URL.  

The function is fully integrated with **Key Vault for secrets** and deployed via **Azure DevOps CI/CD pipelines**.

---

## Purpose

- Automate triggering of **Fabric master pipeline** on new data arrival
- Extract and pass **blob metadata** to pipeline parameters
- Handle **authentication securely** using a service principal and Fabric API
- Support **retryable and robust execution** in production
- Enable orchestration for **Raw → Silver → Gold transformations** and downstream analytics

---

## Event Trigger

- Triggered by **Azure Event Grid** when a new blob is created
- Function signature:

```python
def BlobCreatedEvent(event: func.EventGridEvent):
```

- Extracts blob URL from event.get_json()["url"]
- Logs the event and triggers Fabric pipeline

## Fabric Pipeline Trigger Workflow

1. Authenticate with Fabric API
    - Uses ClientSecretCredential (service principal)
    - Retrieves tenant ID, client ID, client secret from environment variables or Key Vault
    - Requests token from https://api.fabric.microsoft.com/.default
2. Parse Blob URL
    - Extracts:
        - Container name
        - Folder path
        - File name

3. Prepare Payload
    - Loads JSON payload from environment variable FABRIC_PIPELINE_PAYLOAD
    - Updates parameters for:
        - containername
        - foldername
        - filename

4. Call Fabric API
    - POST to Fabric pipeline endpoint
    - Handles HTTP status codes:
    - 202 → success, returns job instance ID
    - 429, 500, 502, 503, 504 → retryable errors
    - Other errors → log and raise exception if needed

5. Logging
  - Logs pipeline trigger details
  - Logs workspace items for auditing and debugging

## Environment Variables

| Variable                  | Purpose                               |
|---------------------------|---------------------------------------|
| `TENANT_ID`               | Azure tenant ID for service principal |
| `CLIENT_ID`               | Service principal client ID           |
| `CLIENT_SECRET`           | Service principal secret              |
| `FABRIC_WORKSPACE_ID`     | Target Fabric workspace ID            |
| `FABRIC_PIPELINE_ID`      | Master pipeline ID                    |
| `FABRICS_PIPELINE_URL`    | Fabric REST API URL template          |
| `FABRIC_PIPELINE_PAYLOAD` | JSON template for pipeline parameters |

## CI/CD Deployment
- Deployed via Azure DevOps YAML pipeline
- CI/CD steps include:
- Python dependency installation (requirements.txt)
- Packaging Azure Function
- Deployment to Azure Function App
- Secrets stored securely in Azure Key Vault
- Supports automated redeployments without manual intervention
## How This Supports the Project
- Orchestrates full project flow from raw data ingestion to Gold layer
- Connects Blob events → Fabric master pipeline → downstream Lakehouse transformations
- Supports parameterized execution, allowing multiple pipelines or files to be handled automatically
- Works with Phase 1 and Phase 2 infrastructure (Blob Storage, SQL, Functions, Key Vault)
- Enables Power BI dashboards and semantic models to reflect real-time data
## Tech Stack

- Python 3.10
- Azure Functions (Event Grid Trigger)
- Microsoft Fabric REST API
- Azure Key Vault for secrets
- Azure DevOps for CI/CD automation
- Requests library for API calls

## Notes
- Robust error handling with retryable logic for throttling or server errors
- Logs all steps for auditing and debugging
- Fully reusable for any future Fabric pipelines or blob-based triggers

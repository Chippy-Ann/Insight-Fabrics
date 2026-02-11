# Phase 1 – Azure Function: GenerateEmotionData

This **Python 3.10 Azure Function** generates synthetic emotional event data for the Insight Fabrics project.  
It simulates user-submitted emotions and uploads the resulting dataset as a CSV file to **Azure Blob Storage**.  
The function is fully automated and deployed using **Azure DevOps CI/CD pipelines**.

---

## Purpose

- Generate **synthetic emotional event records** for testing and learning purposes
- Provide consistent **input datasets** for downstream pipelines (ADF learning pipelines and later Fabric pipelines)
- Support **event-driven execution** and automated data ingestion into Azure Blob Storage

---

## Function Details

### Function Name & Route

```python
@app.function_name(name="GenerateEmotionData")
@app.route(route="GenerateEmotionData")

```
### Function URL: /GenerateEmotionData

### HTTP Method: GET or POST

### Optional Parameter: count – number of records to generate (default: 10,000)


### Input

- Query parameter: ?count=<number>
- POST body JSON: { "count": <number> }
- If no count is provided, defaults to 10,000 records
### Output

Returns a JSON response:

```Json
{
  "status": "Success",
  "recordsUploaded": 10000,
  "FileName": "emotion_data_20260211123456_10000.csv",
  "FolderName": "emotion_data",
  "blobUri": "https://<storageaccount>.blob.core.windows.net/<container>/emotion_data/filename.csv"
}
```
or an error Json
```json
{
  "status": "Error",
  "message": "<error message>"
}

```
### Function Workflow

- Retrieve Azure Blob Storage connection string and container name from Key Vault
- Read count parameter from HTTP request
- Generate synthetic emotional event data (generate_month_records(count))
- Convert the data to pandas DataFrame and write a temporary CSV
- Upload the CSV to Azure Blob Storage under emotion_data/ folder
- Return JSON with upload details or error information

### Storage Integration

- Uses Azure Blob Storage to store generated CSVs
- Connection string and container name are retrieved securely via Key Vault
- Supports event-driven workflows for downstream ingestion

### CI/CD Deployment

- Function is deployed using Azure DevOps YAML pipeline
- CI/CD includes:
  -   1. Python dependency installation (requirements.txt)
  -   2. Function package creation
  -  3. Deployment to Azure Function App
- Secrets are never hardcoded; retrieved at runtime from Key Vault

### How This Supports the Project

- Provides synthetic datasets for:
- Phase 2 ADF learning pipelines (Raw → Silver)
- Phase 3 Fabric pipelines (Raw → Silver → Gold)
- Enables repeatable, automated testing and data generation
- Demonstrates Python serverless function development, secure integration, and CI/CD automation

### Tech Stack

- **Language**: Python 3.10
- **Serverless Framework**: Azure Functions
- **Data Handling**: pandas
- **Storage**: Azure Blob Storage
- **Secrets**: Azure Key Vault
- **Automation**: Azure DevOps CI/CD pipelines




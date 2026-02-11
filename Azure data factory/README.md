# Phase 2 – Azure Data Factory Pipelines

This project contains **Azure Data Factory (ADF) pipelines** for the Insight Fabrics platform.  
The pipelines automate **data ingestion, validation, normalization, and lineage tracking** of emotional event data.  

**Version control is integrated via Azure DevOps**, enabling CI/CD for repeatable deployments and controlled releases.

---

## Pipelines Overview

### 1. `pl_EmotionDataValidation` – Data Transformation for Emotions

This pipeline handles:

- **Blob-triggered execution** when new raw CSVs are uploaded to the Bronze/Raw layer  
- Validation of raw emotion data  
- Normalization of valid records  
- Separation of invalid data to **Quarantine Blob folder**  
- Deduplication and writing of clean data to **Silver Blob folder**  
- **Lineage tracking** via stored procedure `[dbo].[SpInsertLineage]` in Azure SQL Database  

#### Pipeline Flow

1. **Set Silver Destination File Name**  
   - Expression:  
     ```text
     @concat('silver_Validated_', formatDateTime(pipeline().TriggerTime,'yyyyMMdd_HHmmss'),'.parquet')
     ```

2. **Set Normalized File Name**  
   - Expression:  
     ```text
     @concat('silver_Normalised_', formatDateTime(pipeline().TriggerTime,'yyyyMMdd_HHmmss'),'.parquet')
     ```

3. **Dataflow Task: `SchemaValidation`**  
   - Validates column formats, data types, and required fields  
   - Separates **valid vs invalid records**  
   - Invalid records → **Quarantine Blob folder**  
   - Valid records → written temporarily and then deduplicated  
   - Calls `[dbo].[SpInsertLineage]` to log processing metadata:
     - Run ID, file name, row counts, status, blob URIs, timestamps

4. **Dataflow Task: `Normalization`**  
   - Standardizes data values (e.g., Emotion types, intensity scores)  
   - Writes normalized dataset to **Silver Blob folder**  

> **Screenshot Placeholder:**  
<img width="1865" height="818" alt="image" src="https://github.com/user-attachments/assets/b4a9261e-43b8-44f5-af79-3efc8a87b492" />
<img width="1498" height="435" alt="image" src="https://github.com/user-attachments/assets/4cac768a-a6bb-479e-8bc5-e2da1a9ac8a8" />
<img width="1413" height="516" alt="image" src="https://github.com/user-attachments/assets/3eafbeee-850b-4e25-b6d0-847d3e5a0a6b" />
<img width="1232" height="545" alt="image" src="https://github.com/user-attachments/assets/9cd870ae-8648-4db0-962f-52a1ce37a11e" />
<img width="1918" height="846" alt="image" src="https://github.com/user-attachments/assets/b74d1344-3bd8-4bcd-882a-6f478536419f" />




---

### 2. `pl_Ingest_Event_Bronze` – Trigger Azure Function for Data Generation

This pipeline handles:

- Triggering the **Phase 1 Azure Function** to generate synthetic emotion data  
- Saving the generated CSVs to **Raw/Bronze Blob folder**  
- Logging the ingestion metadata via `[dbo].[SpInsertLineage]` stored procedure  
- Supports automated, repeatable **data ingestion workflows**

> **Screenshot Placeholder:**  
> <img width="1862" height="817" alt="image" src="https://github.com/user-attachments/assets/15b8a79a-d14d-4e8f-b505-9ed8907d9291" />


---

## Linked Services / Connections

These pipelines leverage multiple linked services:

| Service Type       | Name / Purpose                                      |
|------------------|---------------------------------------------------|
| Azure Blob Storage | Raw/Bronze, Silver, Quarantine layers            |
| Azure SQL Database | `[dbo].[SpInsertLineage]` for lineage tracking   |
| Azure Function     | Phase 1 data generator                            |
| Key Vault          | Secrets for storage, SQL connections, and function credentials |

---

## Key Features

- **Blob-triggered pipelines** for real-time or event-driven execution  
- **Parameterization**: File paths and names are dynamically generated using pipeline trigger time  
- **Data Quality Checks**: Invalid records quarantined, valid data deduplicated and normalized  
- **Lineage Logging**: Stored procedure `[dbo].[SpInsertLineage]` tracks run metadata, blob details, and row counts  
- **CI/CD Ready**: Version control via Azure DevOps ensures consistent deployment across environments  
- **Integration with Phase 1 & Phase 3**: Supports downstream Fabric pipelines and SQL-based reporting  

---

## Future Enhancements / Notes

- Add **pipeline monitoring dashboards** to visualize run statistics  
- Expand **normalization rules** for additional emotion attributes  
- Include **sample output files** for reference  

---

## Tech Stack

- **Azure Data Factory** – Pipelines & Dataflows  
- **Azure Blob Storage** – Raw / Silver / Quarantine layers  
- **Azure SQL Database** – Lineage tracking  
- **Azure Functions** – Data generation (Phase 1)  
- **Azure Key Vault** – Secrets management  
- **Azure DevOps** – CI/CD & version control  

---


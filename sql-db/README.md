# Insight Fabrics – SQL Database Project

This SQL project is part of the **Insight Fabrics platform**.  
It provides the **data storage foundation** for both the **web app** and the **pipeline orchestration / lineage tracking**.

---

## Purpose

- Store emotional events submitted from the **web application**
- Track **pipeline execution lineage and status**
- Provide a **central source of truth** for downstream processing in Azure Functions, ADF (learning), and Microsoft Fabric pipelines
- Enable **repeatable, version-controlled deployments** via CI/CD


---

## Tables

### 1. `EmoionChoices`
- Stores emotional events captured from the **web application**
- Columns include:
  - `UserName` – Name of the user
  - `Emotion` – Type of emotion (`Joy`, `Sadness`, `Anger`, etc.)
  - `Reason` – Trigger/reason for the emotion
  - `Intensity` – Numerical intensity score
  - `CreatedOn` – Timestamp of submission

### 2. `tblInsightFabricPipelineLineage`
- Tracks **pipeline execution metadata and status**
- Columns include:
  - `RunId` – Unique execution identifier
  - `PipeLineName` – Name of the pipeline
  - `CurrentStage` – Stage of execution (`Raw`, `Silver`, `Gold`)
  - `BlobName` / `BlobUri` – Source blob details
  - `SizeBytes` – File size
  - `RowCountRaw`, `RowCountSilver`, `RowCountQuarrentine` – Row counts at different stages
  - `SilverModifiedOn` – Timestamp when Silver layer was updated
  - `Status` – Execution status (`Success`, `Failed`, etc.)
  - `ErrorMessage` – Error details (if any)
  - `CreatedOn` – Timestamp of pipeline run

---

## Stored Procedures

### `SpInsertLineage`
- Inserts or updates **pipeline execution metadata** in `tblInsightFabricPipelineLineage`
- Checks if a record with the same `BlobName` and `BlobUri` exists:
  - **If exists:** updates counts, status, error message, and stage
  - **If not exists:** inserts a new record
- Parameters:
  - `@RunId`, `@PipeLineName`, `@CurrentStage`, `@BlobName`, `@BlobUri`
  - `@SizeBytes`, `@CreatedOn`, `@RowCountRaw`, `@RowCountSilver`
  - `@RowCountQuarrentine`, `@SilverModifiedOn`, `@Status`, `@ErrorMessage`

---
<img width="386" height="532" alt="image" src="https://github.com/user-attachments/assets/4d61c56e-29c7-4ea7-892e-1cf2cdb05f44" />


## CI/CD Automation

- **Azure DevOps YAML pipelines** used to automate:

  1. Database creation (if not exists)
  2. Table deployment (`tblInsightFabricEmotions`, `tblInsightFabricPipelineLineage`)
  3. Stored procedure deployment (`SpInsertLineage`)
  4. Schema updates and version control

- Benefits:
  - Repeatable, reliable deployments across environments
  - Version control for database schema
  - Supports automated testing and integration
  - Eliminates manual SQL script execution

---

## How This Supports the Project

- Ensures **production-grade deployment** of database objects
- Provides the **foundation for Azure Functions and Fabric pipelines**
- Enables **pipeline status automation and monitoring**
- Works seamlessly with Phase 1 infrastructure and Phase 3 analytics

---

## Notes

- The database is designed for **scalability and CI/CD integration**
- Secrets (connection strings) are retrieved securely via **Azure Key Vault**
- This approach demonstrates **modern DevOps practices applied to databases**

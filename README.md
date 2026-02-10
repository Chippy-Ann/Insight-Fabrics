# Insight Fabrics – Event-Driven Emotional Insights Platform

An end-to-end **Azure + Microsoft Fabric data platform** that captures emotional events, processes them through layered pipelines, and delivers analytics-ready insights using **Direct Lake semantic models and Power BI dashboards**.

---

## Project Theme

**Emotions as events.**

This project treats human emotions as structured events and processes them through a modern data architecture — from capture to transformation to insight.

The solution is built incrementally across **three phases**, reflecting real-world learning, evaluation, and architectural evolution.

---

## High-Level Architecture

> ⚠️ **Note**  
> Azure Data Factory pipelines were implemented in **Phase 2 strictly for learning purposes**.  
> The **final project flow is fully implemented using Microsoft Fabric pipelines** in Phase 3.

### Final Execution Flow


| Step | Component | Purpose |
|------|-----------|---------|
| 1 | User | Submits emotion via web app |
| 2 | .NET Web App | Captures emotion, intensity, reason, user, timestamp |
| 3 | SQL Database | Stores structured emotional events |
| 4 | Azure Function (Python – Data Generation) | Dumps data to Blob Storage (Raw) |
| 5 | Azure Blob Storage (Raw) | Stores raw CSV files |
| 6 | Azure Function (Event Trigger) | Triggers Fabric master pipeline on blob arrival |
| 7 | Microsoft Fabric Master Pipeline | Orchestrates ingestion and transformations |
| 8 | Fabric Pipelines / Dataflows | Handles data ingestion, transformations, and storage |
| 9 | Fabric Lakehouse | Raw → Silver → Gold layers |
| 10 | Spark Notebooks | Transformations: Raw→Silver, Silver→Gold |
| 11 | Direct Lake Semantic Model | Analytics-ready layer |
| 12 | Power BI Dashboards | Visualizes emotional trends and insights |


---

## Phase 1 – Azure Foundation, App & Automation

### Goal
Build a **cost-efficient, fully automated Azure foundation** to capture emotional events and extract them as raw data.

### What Was Built

- **Infrastructure as Code (Terraform)**
  - Azure resources provisioned using Terraform
  - Remote Terraform state stored in a separate Azure resource group
  - Designed for reproducibility and cost control

- **Web Application**
  - .NET 9.0 single-page application
  - Captures:
    - Emotion
    - Intensity
    - Reason
    - User
    - Timestamp

- **SQL Database Project**
  - Structured storage for emotional events
  - Schema and scripts version-controlled
  - Deployed via CI/CD

- **Azure Function (Python)**
  - Extracts data from SQL
  - Dumps CSV files into Azure Blob Storage

- **CI/CD (Azure DevOps – YAML)**
  - Pipelines for:
    - Terraform infrastructure
    - Web app deployment
    - SQL database project
    - Azure Function deployment

### Outcome

- Fully automated deployment of infra, app, database, and functions
- Emotional events captured and exported as raw CSV data
- Strong foundation for downstream data engineering

---

## Phase 2 – Data Engineering with Azure Data Factory (Learning Phase)

### Goal
Learn and apply **data ingestion, transformation, and orchestration** concepts using Azure Data Factory.

### What Was Built

- **ADF Pipelines**
  - Trigger Azure Function to generate data
  - Read raw CSV data from Blob Storage
  - Apply transformations:
    - Normalization
    - Standardization
    - Deduplication
  - Store clean data in **Silver layer (Blob Storage)**

- **Triggers**
  - Blob-based triggers for pipeline execution

- **Terraform Enhancements**
  - Added:
    - Silver blob containers
    - Azure Function resources
    - ADF-related infrastructure

### Outcome

- Automated Raw → Silver transformation pipeline
- Hands-on experience with ADF orchestration and transformations

> ℹ️ These pipelines are **not part of the final project execution**.  
> The production data flow is fully implemented in **Microsoft Fabric (Phase 3)**.

---

## Phase 3 – Microsoft Fabric End-to-End Platform

### Goal
Build a **modern, event-driven analytics platform** using Microsoft Fabric, Spark, and Direct Lake.

### What Was Built

- **Microsoft Fabric Setup**
  - Fabric subscription and workspace
  - Lakehouse with Raw, Silver, and Gold layers
  - Access control and permissions configured

- **Fabric Pipelines & Dataflows**
  - Ingest data from Azure Blob Storage into Lakehouse
  - Orchestrated via a **master pipeline**

- **Spark Notebooks**
  - Raw → Silver transformations
  - Silver → Gold transformations

- **Event-Driven Orchestration**
  - Python-based Azure Function triggers the Fabric master pipeline
  - Automatically executes when a new blob arrives
  - Passes dynamic parameters to the pipeline

- **Semantic Modeling (Direct Lake)**
  - Direct Lake semantic model built on Gold layer
  - Optimized for performance and minimal data duplication

- **Power BI Dashboards**
  - Interactive dashboards built on the Direct Lake model
  - Visualizes emotional trends, intensity patterns, and insights

### Outcome

- Fully automated **event → insight** pipeline
- Analytics-ready Gold data in Fabric Lakehouse
- High-performance Power BI dashboards using Direct Lake
- End-to-end Fabric-first architecture

---

## Skills Demonstrated

- Infrastructure as Code (**Terraform**)
- CI/CD with **Azure DevOps (YAML)**
- Full-stack development (**.NET 9.0**)
- SQL database design and deployment
- Serverless computing (**Azure Functions – Python**)
- Data engineering with **Azure Data Factory**
- Microsoft Fabric pipelines and orchestration
- Spark notebook transformations
- Direct Lake semantic modeling
- Power BI dashboard development
- Event-driven data architecture

---

## Why This Project Matters

This project mirrors **real enterprise data platforms**:

- Incremental, phase-based architecture
- Clear separation of Raw / Silver / Gold layers
- Event-driven automation
- Fabric-first analytics design
- CI/CD-driven, reproducible deployments

Built entirely as **self-learning**, with production-style discipline and architectural intent.

---

## License

MIT License — free to use for learning and experimentation.

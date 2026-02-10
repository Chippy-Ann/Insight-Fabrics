# Phase 2 – Data Engineering Infrastructure (Terraform)

This module extends the Phase 1 Azure foundation by provisioning **data engineering–specific resources** required for learning and experimenting with **Azure Data Factory–based pipelines**.

The focus of this phase is **data ingestion, transformation, and orchestration**, while maintaining the same security and CI/CD standards established in Phase 1.

---

## Purpose of Phase 2

- Provision infrastructure required for Azure Data Factory pipelines
- Enable automated data generation for pipeline testing
- Securely manage secrets for Azure Functions using Azure Key Vault
- Prepare Silver-layer storage for cleansed data

---

## Key Terraform Additions

### `datafactory.tf`
A dedicated Terraform file introduced to logically separate **data engineering resources** from core infrastructure.

---

## Resources Provisioned

### Azure Data Factory
- Azure Data Factory instance created for learning and experimentation
- Used to orchestrate data ingestion and transformation pipelines

> ⚠️ Note  
> ADF pipelines were implemented for learning purposes only and are **not part of the final production data flow**, which is implemented using Microsoft Fabric in Phase 3.

---

### Azure Function – Data Generation
- Python-based Azure Function provisioned to generate emotional event data
- Produces CSV files used as input for ADF pipelines
- Deployed and managed via CI/CD

---

### Storage Enhancements
- Additional Blob containers created for:
  - **Silver layer** data
- Used to store normalized, standardized, and deduplicated datasets

---

### Azure Key Vault – Secret Management
- New secrets added to Azure Key Vault for:
  - Azure Function connection strings
  - Storage access credentials
- Secrets written via Terraform
- Azure Functions granted RBAC-based access to retrieve secrets at runtime

---

## Security Model

- Secrets are **never hardcoded**
- Azure Functions read secrets securely from Key Vault
- RBAC used consistently across all services
- Aligns with enterprise-grade security patterns

---

## CI/CD Integration

- All Phase 2 resources deployed via **Azure DevOps YAML pipelines**
- Supports repeatable deployments and safe infrastructure changes

---

## How This Phase Fits in the Overall Architecture

- Introduces data engineering tooling (ADF) for learning purposes
- Produces clean Silver-layer datasets
- Informs architectural decisions that led to a Fabric-first approach in Phase 3

---

## Notes

- This phase focuses on **learning and evaluation**, not final architecture
- Design intentionally evolves in Phase 3 based on insights gained here

# Phase 1 – Azure Infrastructure (Terraform)

This module provisions the **core Azure infrastructure** required for the Insight Fabrics platform.  
All resources are created using **Terraform** with a strong focus on **security, cost awareness, and reproducibility**.

---

## Purpose of Phase 1

- Establish a secure Azure foundation for the application and data platform
- Enable automated deployments via CI/CD
- Centralize secrets using Azure Key Vault
- Prepare storage and database layers for downstream data pipelines

---

## Resources Provisioned

### Resource Groups
- **Primary resource group** for application and data resources
- **Separate resource group** for Terraform remote state backup  
  (ensures isolation and recoverability)

---

### SQL Resources
- Azure SQL Server
- Azure SQL Database
- Used to store structured emotional event data captured by the web application

---

### Storage Account
- Azure Blob Storage
- Containers created for:
  - Raw data exports (CSV)
- Acts as the landing zone for data extracted by Azure Functions

---

### Azure Key Vault
- Centralized secret management
- Stores:
  - SQL connection strings
  - Storage account connection strings
  - Application secrets

#### RBAC Configuration
- Role-based access control (RBAC) used instead of access policies
- Web App and Azure Functions granted:
  - Read access to secrets
  - Write access where required

---

### Web Application Infrastructure
- Azure App Service
- App Service Plan
- Configured to:
  - Read secrets securely from Azure Key Vault
  - Avoid hardcoded credentials in code or pipelines

---

## Security Considerations

- No secrets stored in:
  - Terraform code
  - CI/CD pipeline YAML files
  - Application configuration files
- All sensitive values are retrieved at runtime from **Azure Key Vault**
- RBAC ensures least-privilege access

---

## Terraform State Management

- Remote backend configured
- Terraform state stored in a **dedicated resource group**
- Prevents accidental deletion and enables safe collaboration

---

## CI/CD Integration

This Terraform module is deployed using **Azure DevOps YAML pipelines**:
- Supports repeatable deployments across environments
- Enables infrastructure changes to be version-controlled

---

## How This Supports Later Phases

- Provides secure storage and database layers for data pipelines
- Enables Azure Functions and Fabric pipelines to operate without embedded secrets
- Establishes a scalable foundation for ADF and Microsoft Fabric workloads

---

## Notes

- This module is designed for **learning and portfolio demonstration**
- Emphasis is placed on **real-world patterns** rather than minimal setup

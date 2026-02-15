# Self-Hosted Azure DevOps Agent Setup Checklist

This checklist covers everything needed to ensure a self-hosted agent can **build SQL projects**, **deploy DACPACs**, and run Azure DevOps pipelines reliably.

---

## 1. Agent Installation

- [ ] Provision a **Windows Server / VM** for the agent (Windows 10/11 or Windows Server 2016+)
- [ ] Ensure the agent has **internet access** to Azure and NuGet feeds
- [ ] Download the latest **Azure DevOps agent** from:
  [https://dev.azure.com/{your-org}/_settings/agents](https://dev.azure.com)
- [ ] Extract and configure the agent:
  ```powershell
  .\config.cmd
  ```
- [ ] Run the agent as Windows Service (recommended)
- [ ] Verify the agent is online in the SelfHosted agent pool
## 2. Required Software / Tools
### .NET SDK

- [ ] Install .NET SDK 8.0 or 9.0 (matching your SQL project SDK)
- [ ] Verify with:
 ```powershell
dotnet --list-sdks
```
### Visual Studio Build Tools

 - [ ] Install Visual Studio Build Tools 2019/2022
 - [ ] Include workloads:
  - MSBuild
  - .NET desktop build tools
  - SQL Server Data Tools (SSDT)
 - [ ] Verify msbuild is available in PATH:
 ```powershell
msbuild -version
```
### SQL Tools

- [ ] Install SQL Server DAC Framework / SqlPackage
- [ ] Typically installed from: Microsoft SQL Server 2019/2022 Feature Pack
- [ ] Verify installation:
 ```powershell
SqlPackage.exe /?
```
- [ ] Ensure sqlpackage.exe is in PATH for the agent
- [ ] NuGet
- [ ] Install latest NuGet CLI
- [ ] Verify:
 ```powershell
nuget help
```
### Azure CLI

- [ ] Install latest Azure CLI
- [ ]  Verify login with service principal:
 ```powershell
az login --service-principal -u <app-id> -p <secret> --tenant <tenant-id>
```
- [ ] Ensure PowerShell scripts can run az commands

## 3. Agent Capabilities Verification

Go to Organization Settings → Agent Pools → SelfHosted → Agents → Capabilities
- [ ] Verify system capabilities:
 - msbuild
 - visualstudio
 - sqlpackage
 - dotnet

- [ ] Add user capabilities if custom paths are used

## 4. Networking / Firewall

 - [ ] Ensure agent can reach Azure SQL Server:
  - [ ] Port 1433 TCP open
- [ ] Ensure agent’s public IP is allowed in Azure SQL firewall:
  - [ ] Either via dynamic detection script in pipeline
  - [ ] Or via static firewall rule / IP range
  - [ ] Optional: enable “Allow Azure services” in SQL Server

## 5. Pipeline Readiness Checks

- [ ] Test dotnet restore & build for SQL project
- [ ] Test CopyFiles task to staging directory
- [ ] Test Azure KeyVault retrieval for secrets
- [ ] Test Azure CLI firewall rule creation
- [ ] Test DACPAC deployment to Azure SQL Database

## 6. Optional / Recommended
- [ ] Set agent as service account with non-admin login
- [ ] Schedule agent restart policy for long-running VMs
- [ ] Enable TLS 1.2 support (Azure CLI and SQL connections)
- [ ] Add cleanup scripts to remove firewall rule after deployment

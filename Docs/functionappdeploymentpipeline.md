# InsightFabric functonapp Pipeline Issues & Fixes

This document summarizes the errors we encountered while setting up the InsightFabric CI/CD pipeline on a Windows self‑hosted agent, and how each was resolved.

---

## 1. Python Not Recognized
**Error:**
'python' is not recognized as an internal or external command

**Cause:**  
Python was installed only for the current user, so the Azure DevOps agent service could not resolve it from PATH.

**Fix:**  
Reinstalled Python **for all users** → placed in `C:\Program Files\Python310\`, accessible to the agent service.

---

## 2. Access Denied Running Python
**Error:**
Access is denied.


**Cause:**  
Agent service account lacked permission to run executables from the user profile directory.

**Fix:**  
Installing Python for all users solved this too, since `C:\Program Files` is accessible to system services.

---

## 3. Missing `zip` Command
**Error:**
'zip' is not recognized as an internal or external command

**Cause:**  
Windows does not ship with a `zip` CLI tool.

**Fix:**  
Replaced with the **ArchiveFiles@2** task (or PowerShell `Compress-Archive`) to package the Function App.

---

## 4. WSL Not Installed
**Error:**
Windows Subsystem for Linux has no installed distributions

**Cause:**  
AzureCLI@2 task was set to `scriptType: bash` on Windows, which requires WSL.

**Fix:**  
Switched to `scriptType: ps` (PowerShell) so Azure CLI runs natively on Windows.

---

## 5. FileNotFoundError for Zip
**Error:**
FileNotFoundError: [WinError 3] The system cannot find the path specified: '...drop/functionapp_package.zip'

**Cause:**  
Artifact was published but not downloaded into the workspace before deploy.

**Fix:**  
Added **DownloadPipelineArtifact@2** step to pull the `drop` artifact into `$(Pipeline.Workspace)` before deployment.

---

## ✅ Outcome
- Pipeline now **packages, publishes, downloads, and deploys** the Function App zip cleanly.  
- Self‑hosted agent is stable with Python, pip, and Azure CLI accessible.  
- Deployment to Azure Functions works end‑to‑end.

---

## 📌 Lessons Learned
- Always install developer tools **for all users** on self‑hosted agents.  
- Use built‑in tasks (`ArchiveFiles`, `PublishBuildArtifacts`, `DownloadPipelineArtifact`) instead of relying on missing OS commands.  
- Match script type (`ps` vs `bash`) to the agent OS.  
- Add debug steps (`where python`, `dir drop`) to confirm environment consistency.  



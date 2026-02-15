# 🛠️ InsightFabric Function App Troubleshooting & Resolution

## Problem
After deploying our Function App with:
```powershell
az functionapp deployment source config-zip --resource-group rg-dev-insightfabric --name fn-dev-insightfabric --src "functionapp_package.zip"
```
the Functions blade in Azure Portal showed no functions. Log Stream revealed the host was entering DrainMode immediately:
Received request to drain the host
DrainMode mode enabled
StopAsync on the registered listeners

Root Causes Considered
DrainMode can be triggered by several issues:

Runtime mismatch → Function App set to unsupported Python version.

Missing/invalid app settings → e.g. FUNCTIONS_WORKER_RUNTIME not set to python.

Extension bundle issue → host.json bundle range not resolving.

Package structure mismatch → host.json not at root, dependencies not packaged correctly.

Scaling event → Linux Consumption plan drains idle workers.

In our case, the manual zip deployment lacked the correct dependency packaging and metadata,
so the runtime drained before indexing.

Solution
1. Deploying from VS Code with Core Tools
We switched to Azure Functions Core Tools (func) for publishing:
```powershell
cd C:\Users\chipp\Azure\chippyannlearningstuff\InsightFabric-FunctionApp
func azure functionapp publish fn-dev-insightfabric --python
```
Core Tools fixed the issue by:

Building .python_packages/lib/site-packages with dependencies

Ensuring host.json was at the root

Adding correct metadata for the Python v2 programming model

Deploying via ZipDeploy with proper structure

Result: Functions (GenerateEmotionData) appeared in the Azure Portal and logs streamed correctly.

## Installing Core Tools on the Agent
To make CI/CD reproducible, we installed Core Tools globally on the self‑hosted agent:
from msi 
https://learn.microsoft.com/en-us/azure/azure-functions/functions-run-local?tabs=windows%2Cisolated-process%2Cnode-v4%2Cpython-v2%2Chttp-trigger%2Ccontainer-apps&pivots=programming-language-csharp

then add <img width="1366" height="292" alt="image" src="https://github.com/user-attachments/assets/f710d577-fa60-4866-966f-08357da8f5e1" />



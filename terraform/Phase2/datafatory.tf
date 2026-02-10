# create Log analatics workspace

resource "azurerm_log_analytics_workspace" "law" {
  name                = var.log_analytics_workspace_name
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  sku                 = "PerGB2018"
}

# Application Insights

resource "azurerm_application_insights" "appi" {
  name                = var.application_insights_name
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  workspace_id        = azurerm_log_analytics_workspace.law.id
  application_type     = "web"     
  retention_in_days    = 90
  daily_data_cap_in_gb = 5
}



# Function App Plan To generate data

resource "azurerm_service_plan" "function_plan" {
  name                = "fnappserviceplan-insightfabric"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  os_type             = "Linux"
  sku_name            = "Y1"  # Consumption plan
}
# Function App To generate data
resource "azurerm_function_app" "function_app" {
  name                       = var.function_app_name
  location                   = azurerm_resource_group.rg.location
  resource_group_name        = azurerm_resource_group.rg.name
  app_service_plan_id        = azurerm_service_plan.function_plan.id
  storage_account_name       = azurerm_storage_account.datalake.name
  storage_account_access_key = azurerm_storage_account.datalake.primary_access_key
  version                    = "~4"
  os_type                    = "linux"
  identity {
    type = "SystemAssigned"
  }
  site_config {
    linux_fx_version = "PYTHON|3.10"
  }
 
  app_settings = {
    "FUNCTIONS_WORKER_RUNTIME" = "python"
    "AzureWebJobsFeatureFlags" = "EnableWorkerIndexing"
    "WEBSITE_RUN_FROM_PACKAGE" = "1"
    "KEY_VAULT_URL"            =  azurerm_key_vault.kv.vault_uri
    "APPINSIGHTS_INSTRUMENTATIONKEY"        = azurerm_application_insights.appi.instrumentation_key
    "APPLICATIONINSIGHTS_CONNECTION_STRING" = azurerm_application_insights.appi.connection_string


  }
}


# Assign RBAC role to fuctionapp identity
resource "azurerm_role_assignment" "fnapp_kv_rbac" {
  scope                = azurerm_key_vault.kv.id
  role_definition_name = "Key Vault Secrets User"
  principal_id         = azurerm_function_app.function_app.identity[0].principal_id
}

data "azurerm_function_app_host_keys" "fnkeys" {
  name                = azurerm_function_app.function_app.name
  resource_group_name = azurerm_resource_group.rg.name
}

resource "azurerm_key_vault_secret" "fnkey" {
  name         = "fn-key"
  value        = data.azurerm_function_app_host_keys.fnkeys.default_function_key
  key_vault_id = azurerm_key_vault.kv.id
}

resource "azurerm_key_vault_secret" "fnurl" {
  name         = "fn-url"
  value        = "https://${azurerm_function_app.function_app.default_hostname}/api/"
  key_vault_id = azurerm_key_vault.kv.id
}


# Event Grid System Topic for bronze

resource "azurerm_eventgrid_system_topic" "bronze_topic" {
  name                = "insightfabric-bronze-topic"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  source_arm_resource_id = azurerm_storage_account.datalake.id
  topic_type             = "Microsoft.Storage.StorageAccounts"
}


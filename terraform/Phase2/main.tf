# Configure the Azure provider
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0.2"
    }
  }

  required_version = ">= 1.1.0"

  backend "azurerm" {
    resource_group_name  = "rg-backend-insightfabric"
    storage_account_name = "tfstateinsightfabric"
    container_name       = "tfstate"
    key                  = "terraform.tfstate"
  }
}

provider "azurerm" {
  features {}
}
# 1 creating resource group
resource "azurerm_resource_group" "rg" {
  name     = var.resource_group_name
  location = "australiasoutheast"
}

# 2 Storage Account (Data Lake Gen2)
resource "azurerm_storage_account" "datalake" {
  name                     = "stginsightfabricdatalake"
  resource_group_name      = azurerm_resource_group.rg.name
  location                 = azurerm_resource_group.rg.location
  account_tier             = "Standard"
  account_replication_type = "LRS"

  # this enables Data Lake (Hierarchical Namespace)
  is_hns_enabled = true

  # allow public access or secure transfer
  # allow_blob_public_access = false
  enable_https_traffic_only = true

  tags = {
    environment = "dev"
    project     = "data-lake"
  }
}

# 3 Create a Container (like a folder)
resource "azurerm_storage_container" "bronze" {
  name                  = "bronze-emotion-data"
  storage_account_name  = azurerm_storage_account.datalake.name
  container_access_type = "private"
}

resource "azurerm_storage_container" "silver" {
  name                  = "silver-emotion-data"
  storage_account_name  = azurerm_storage_account.datalake.name
  container_access_type = "private"
}
resource "azurerm_storage_container" "gold" {
  name                  = "gold-emotion-data"
  storage_account_name  = azurerm_storage_account.datalake.name
  container_access_type = "private"
}
# 4 Key Vault
resource "azurerm_key_vault" "kv" {
  name                = var.keyvault_name
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  tenant_id           = data.azurerm_client_config.current.tenant_id
  sku_name            = "standard"

  # Access Policies – simplest way  we used it first but now we are trying RBAC for that below line is required
  enable_rbac_authorization = true

  # soft_delete_enabled         = true
  purge_protection_enabled = false # change to true in production

  # Optional network restrictions (remove if you want public access)
  # public_network_access_enabled = true
}

# 5 Data to get your tenant id
data "azurerm_client_config" "current" {}

/* we are commenting below block so that we can enable RBAC instead of access policies

# 6 Grant terraform Access to Key Vault

resource "azurerm_key_vault_access_policy" "user_policy" {
  key_vault_id = azurerm_key_vault.kv.id
  tenant_id    = data.azurerm_client_config.current.tenant_id
  object_id    = data.azurerm_client_config.current.object_id

  secret_permissions = ["Get", "Set", "List", "Delete", "Recover", "Purge"]
}
*/

# 6.Grant terraform Access to Key Vault
 resource "azurerm_role_assignment" "kv_rbac" {
  scope                = azurerm_key_vault.kv.id
  role_definition_name = "Key Vault Secrets Officer" # or "Secrets User"
  principal_id         = data.azurerm_client_config.current.object_id
}


# 7 Azure SQL Server
resource "azurerm_mssql_server" "sqlserver" {
  name                         = var.sqlserver-name # must be globally unique
  resource_group_name          = azurerm_resource_group.rg.name
  location                     = azurerm_resource_group.rg.location
  version                      = "12.0"         # required version
  administrator_login          = "sqladminuser" # choose your admin username
  administrator_login_password = "Chippy@123!"  # use a secure password
  minimum_tls_version          = "1.2"
}

# 8 Azure SQL Database (Basic Tier)
resource "azurerm_mssql_database" "sqldb" {
  name      = "sqlemotiondb"
  server_id = azurerm_mssql_server.sqlserver.id

  sku_name    = "Basic" # Basic, S0, S1, P1, etc.
  max_size_gb = 2       # Basic max size is 2 GB
}


# 9 Store Connection string in keyvault

resource "azurerm_key_vault_secret" "sql_conn" {
  name         = "EmotionDbConnectionString"
  value        = "Server=tcp:${azurerm_mssql_server.sqlserver.fully_qualified_domain_name},1433;Database=${azurerm_mssql_database.sqldb.name};User ID=${azurerm_mssql_server.sqlserver.administrator_login};Password=${azurerm_mssql_server.sqlserver.administrator_login_password};Encrypt=True;TrustServerCertificate=False;Connection Timeout=30;"
  key_vault_id = azurerm_key_vault.kv.id
    depends_on = [
    # azurerm_key_vault_access_policy.user_policy #replacing this so that it supports RBAC
     azurerm_role_assignment.kv_rbac
  ]
}

# 9b Store Connection string in keyvault

resource "azurerm_key_vault_secret" "sql_psw" {
  name         = "EmotionDbPassword"
  value        = azurerm_mssql_server.sqlserver.administrator_login_password
  key_vault_id = azurerm_key_vault.kv.id
    depends_on = [
    # azurerm_key_vault_access_policy.user_policy #replacing this so that it supports RBAC
     azurerm_role_assignment.kv_rbac
  ]
}


# 10 Create App service plan for appservice
resource "azurerm_service_plan" "appserviceplan" {
  name                = "appserviceplan-azdatapltfrm"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  os_type             = "Windows"
  sku_name            = "B1" # Basic tier 
}


# 11 create appservice
resource "azurerm_windows_web_app" "dotnetapp" {
  name                = var.dotnetapp-name
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  service_plan_id     = azurerm_service_plan.appserviceplan.id

  identity {
    type = "SystemAssigned" # Enables Managed Identity
  }

  site_config {
    always_on = false
    application_stack {
      current_stack  = "dotnet"
      dotnet_version = "v6.0"
    }
  }

  app_settings = {
    "WEBSITE_RUN_FROM_PACKAGE" = "1"
    # Connection string will be Key Vault reference
    "DefaultConnection" = "@Microsoft.KeyVault(SecretUri=${azurerm_key_vault_secret.sql_conn.id})"

  }

}

/* removing below to enable RBAC 
# 12 Grant App Service Access to Key Vault

resource "azurerm_key_vault_access_policy" "appservice" {
  key_vault_id = azurerm_key_vault.kv.id
  tenant_id    = data.azurerm_client_config.current.tenant_id
  object_id    = azurerm_windows_web_app.dotnetapp.identity[0].principal_id

  secret_permissions = [
    "Get"
  ]
}

*/

# 12 Grant App Service Access to Key Vault
resource "azurerm_role_assignment" "appservice_kv_access" {
  scope                = azurerm_key_vault.kv.id
  role_definition_name = "Key Vault Secrets User"
  principal_id         = azurerm_windows_web_app.dotnetapp.identity[0].principal_id
}

#13 allow firewall 
resource "azurerm_mssql_firewall_rule" "allow_my_ip" {
  name             = "AllowMyIP"
  server_id        = azurerm_mssql_server.sqlserver.id
  start_ip_address = "122.150.165.169" # your current public IP
  end_ip_address   = "122.150.165.169"
}
# 14  allow all azure services to contact sql
resource "azurerm_mssql_firewall_rule" "allow_azure_services" {
  name       = "AllowAzureServices"
  server_id  = azurerm_mssql_server.sqlserver.id
  start_ip_address = "0.0.0.0"
  end_ip_address   = "0.0.0.0"
}
/* migrating below block as well for RBAC
resource "azurerm_key_vault_access_policy" "devops_access" {
  key_vault_id = azurerm_key_vault.kv.id
  tenant_id    = var.tenantid-devops
  object_id    = var.objectid-devops  # This is the ID of your service connection

  secret_permissions = [
    "Get",
    "List"
  ]
}
*/
# 14 Enabling access to devops to keyvault
resource "azurerm_role_assignment" "devops_kv_access" {
  scope                = azurerm_key_vault.kv.id
  role_definition_name = "Key Vault Secrets Officer"
  principal_id         = var.principalid-devops
}

# 15 Data Factory with system-assigned identity
resource "azurerm_data_factory" "df" {
  name                = var.azure-data-factory
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  identity {
    type = "SystemAssigned"
  }
}

# 16 Assign RBAC role to Data Factory identity
resource "azurerm_role_assignment" "df_kv_rbac" {
  scope                = azurerm_key_vault.kv.id
  role_definition_name = "Key Vault Secrets User"
  principal_id         = azurerm_data_factory.df.identity[0].principal_id
}

# 17 Storage Acount conn string add to keyvault
resource "azurerm_key_vault_secret" "storage_conn" {
  name         = "storage-connstring"
  value        = azurerm_storage_account.datalake.primary_connection_string
  key_vault_id = azurerm_key_vault.kv.id
   depends_on = [
     azurerm_role_assignment.kv_rbac
  ]
}
#18 adding container name for row emotion data
resource "azurerm_key_vault_secret" "container_name" {
  name         = "emotion-container"                         # Secret name in Key Vault
  value        = "bronze-emotion-data"                          # Name of your blob container
  key_vault_id = azurerm_key_vault.kv.id
   depends_on = [
     azurerm_role_assignment.kv_rbac
  ]
}

# 19 Assign RBAC role to Data Factory identity FOR STORAGE Account
resource "azurerm_role_assignment" "df_st_rbac" {
  scope                = azurerm_storage_account.datalake.id
  role_definition_name = "Storage Blob Data Contributor"
  principal_id         = azurerm_data_factory.df.identity[0].principal_id
}


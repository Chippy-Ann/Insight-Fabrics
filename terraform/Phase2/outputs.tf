output "resource_group_id" {
  value = azurerm_resource_group.rg.id
}


output "keyvault_uri" {
  value       = azurerm_key_vault.kv.vault_uri
  description = "The URI endpoint for the created Key Vault"
}

output "sql_connection_string" {
  value     = "Server=tcp:${azurerm_mssql_server.sqlserver.fully_qualified_domain_name},1433;Database=${azurerm_mssql_database.sqldb.name};User ID=${azurerm_mssql_server.sqlserver.administrator_login};Password=${azurerm_mssql_server.sqlserver.administrator_login_password};Encrypt=true;Connection Timeout=30;"
  sensitive = true
}

output "app_service_url" {
  value = azurerm_windows_web_app.dotnetapp.default_hostname
}

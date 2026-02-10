variable "environment" {
  description = "Environment name (dev/test)"
  type        = string
}

variable "resource_group_name" {
  description = "Resource group name"
  type        = string
}


variable "keyvault_name" {
  description = "Key Vault name"
  type        = string
}

variable "sqlserver-name" {
  description = "SQL Server name"
  type        = string
}

variable "dotnetapp-name" {
  description = "App Service name"
  type        = string
}

variable "tenantid-devops" {
  description = "devops tenantid"
  type        = string
}
variable "principalid-devops" {
  description = "devops principalid"
  type        = string
}

variable "azure-data-factory" {
  description = "Azure data factory"
  type        = string
}

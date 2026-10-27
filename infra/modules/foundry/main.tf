# Microsoft Foundry: one account (kind AIServices) + one project + one model
# deployment. Everything in this package calls models through this account.
#
# What it creates, and why:
#   - the account: where your model deployments live. API keys are switched OFF
#     (local_auth_enabled = false), so the only way in is Microsoft Entra ID.
#   - the project: Agent Framework and Foundry Agent Service work inside one.
#   - the "chat" deployment: gpt-5.4-mini, GlobalStandard (pay per token, $0 idle).
#   - two role assignments for YOU, so your `az login` can call models and use
#     the project — and nothing more.

terraform {
  required_providers {
    azurerm = { source = "hashicorp/azurerm" }
    random  = { source = "hashicorp/random" }
  }
}

variable "resource_group_name" { type = string }
variable "location" { type = string }
variable "deployer_object_id" { type = string }
variable "chat_model" {
  type = object({ model = string, version = string, capacity = number })
}
variable "ci_principal_id" {
  description = "Lab 9: the service principal your CI signs in as, to run the evaluation gate. Empty = none."
  type        = string
  default     = ""
}

# A random suffix keeps names globally unique. Its keepers give a NEW name when
# the SKU or region changes: Azure keeps a deleted account's name reserved for
# a while, and reusing it fails for minutes.
resource "random_string" "suffix" {
  length  = 6
  upper   = false
  special = false
  keepers = { sku = "S0", location = var.location }
}

resource "azurerm_cognitive_account" "foundry" {
  name                       = "fdy-fieldnotes-${random_string.suffix.result}"
  location                   = var.location
  resource_group_name        = var.resource_group_name
  kind                       = "AIServices"
  sku_name                   = "S0"
  custom_subdomain_name      = "fdy-fieldnotes-${random_string.suffix.result}"
  project_management_enabled = true  # allows projects (Agent Service needs one)
  local_auth_enabled         = false # keyless only: API keys are refused
  identity { type = "SystemAssigned" }
}

resource "azurerm_cognitive_account_project" "fieldnotes" {
  name                 = "fieldnotes"
  cognitive_account_id = azurerm_cognitive_account.foundry.id
  location             = var.location
  identity { type = "SystemAssigned" }
}

resource "azurerm_cognitive_deployment" "chat" {
  name                 = "chat" # the name your code uses, whatever the model behind it
  cognitive_account_id = azurerm_cognitive_account.foundry.id
  model {
    format  = "OpenAI"
    name    = var.chat_model.model
    version = var.chat_model.version
  }
  sku {
    name     = "GlobalStandard" # current models require it; plain Standard is refused
    capacity = var.chat_model.capacity
  }
}

# Call models (inference) — nothing else.
resource "azurerm_role_assignment" "openai_user" {
  scope                = azurerm_cognitive_account.foundry.id
  role_definition_name = "Cognitive Services OpenAI User"
  principal_id         = var.deployer_object_id
}

# Lab 9: the evaluation gate in CI calls the model too. Granted here, so it
# survives every tear-down and bring-up (the account, and its roles, are new each time).
resource "azurerm_role_assignment" "ci_openai_user" {
  count                = var.ci_principal_id == "" ? 0 : 1
  scope                = azurerm_cognitive_account.foundry.id
  role_definition_name = "Cognitive Services OpenAI User"
  principal_id         = var.ci_principal_id
  principal_type       = "ServicePrincipal"
}

# Use the project: create and run agents (labs 5 and 8). Named "Azure AI User"
# until 2026; "Foundry User" as of October 2026.
resource "azurerm_role_assignment" "foundry_user" {
  scope                = azurerm_cognitive_account.foundry.id
  role_definition_name = "Foundry User"
  principal_id         = var.deployer_object_id
}

output "openai_v1_endpoint" {
  value = "https://${azurerm_cognitive_account.foundry.custom_subdomain_name}.openai.azure.com/openai/v1/"
}
output "project_endpoint" {
  value = "https://${azurerm_cognitive_account.foundry.custom_subdomain_name}.services.ai.azure.com/api/projects/${azurerm_cognitive_account_project.fieldnotes.name}"
}
output "account_endpoint" { value = azurerm_cognitive_account.foundry.endpoint }
output "chat_deployment" { value = azurerm_cognitive_deployment.chat.name }
output "project_principal_id" { value = azurerm_cognitive_account_project.fieldnotes.identity[0].principal_id }

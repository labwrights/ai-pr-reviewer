# Root module: one resource group with one Microsoft Foundry account, project and
# chat model. Nothing here bills by the hour: you pay per token the reviewer uses.
#
#     az resource list -g rg-fieldnotes-reviewer -o table

# Who is running terraform right now (your `az login` identity). It gets the role
# to call the model: keyless sign-in, no API keys anywhere.
data "azurerm_client_config" "me" {}

resource "azurerm_resource_group" "lab" {
  name     = var.resource_group_name
  location = var.location
  tags = {
    project = "fieldnotes-pr-reviewer"
    purpose = "learning"
  }
}

module "foundry" {
  source = "../../modules/foundry"

  resource_group_name = azurerm_resource_group.lab.name
  location            = azurerm_resource_group.lab.location
  deployer_object_id  = data.azurerm_client_config.me.object_id
  chat_model          = var.chat_model
  ci_principal_id     = var.ci_principal_id
}

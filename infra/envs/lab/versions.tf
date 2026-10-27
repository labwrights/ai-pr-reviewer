# Tool and provider versions these labs were verified with (as of October 2026).
terraform {
  required_version = ">= 1.9"
  required_providers {
    azurerm = { source = "hashicorp/azurerm", version = "~> 5.11" }
    random  = { source = "hashicorp/random", version = "~> 3.6" }
  }
}

provider "azurerm" {
  features {
    cognitive_account {
      # Deleted Foundry accounts are kept for 48 hours by default, holding their
      # name and quota. Purge on destroy so tear-down really means gone.
      purge_soft_delete_on_destroy = true
    }
  }
}


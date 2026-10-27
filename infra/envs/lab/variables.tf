# scripts/bring-up.sh sets what you need; you never edit this file during the labs.

variable "location" {
  description = "Azure region. eastus2 offers the chat model; change it only if START-HERE's region check tells you to."
  type        = string
  default     = "eastus2"
}

variable "resource_group_name" {
  description = "One resource group for everything: one place to look, one thing to delete."
  type        = string
  default     = "rg-fieldnotes-reviewer"
}

variable "chat_model" {
  description = "The model behind the 'chat' deployment. Small and cheap on purpose."
  type = object({
    model    = string
    version  = string
    capacity = number
  })
  default = {
    model    = "gpt-5.4-mini"
    version  = "2026-03-17"
    capacity = 30 # thousands of tokens per minute
  }
}

variable "ci_principal_id" {
  description = "Lab 2: object id of the service principal GitHub Actions signs in as (CI_PRINCIPAL_ID). Empty = none."
  type        = string
  default     = ""
}

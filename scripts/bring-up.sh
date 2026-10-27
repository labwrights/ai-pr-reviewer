#!/usr/bin/env bash
# Stands up the one thing the reviewer needs on Azure: a Microsoft Foundry
# account with a small chat model. Safe to re-run: Terraform never duplicates.
#
#   scripts/bring-up.sh                           # lab 1
#   CI_PRINCIPAL_ID=<id> scripts/bring-up.sh      # lab 2: also let GitHub Actions call the model
#   scripts/bring-up.sh --location swedencentral  # if your region lacks the model
#
# It ends by printing the export lines the reviewer needs, and what it costs.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT/infra/envs/lab"

LOCATION=""
while [ $# -gt 0 ]; do
  case "$1" in
    --location) LOCATION="$2"; shift 2 ;;
    *) echo "unknown argument: $1"; echo "usage: scripts/bring-up.sh [--location REGION]"; exit 2 ;;
  esac
done

if ! az account show >/dev/null 2>&1; then
  echo "❌ You are not logged in to Azure. Run: az login"
  exit 1
fi
export ARM_SUBSCRIPTION_ID="$(az account show --query id -o tsv)"
echo "Azure subscription: $(az account show --query name -o tsv)"

VARS=()
[ -n "$LOCATION" ] && VARS+=(-var "location=$LOCATION")
# Lab 2: GitHub Actions' identity gets the same "call the model" role you have.
# Terraform grants it on every bring-up, because tear-down deletes the account.
[ -n "${CI_PRINCIPAL_ID:-}" ] && VARS+=(-var "ci_principal_id=$CI_PRINCIPAL_ID")

terraform init -input=false -upgrade >/dev/null
terraform apply -auto-approve -input=false "${VARS[@]}"

echo
echo "── what is now running, and what it costs ─────────────────────────────"
echo "  Microsoft Foundry + chat model → \$0 idle; you pay per token used (cents for these labs)"
echo
echo "── environment for the reviewer (paste into your shell) ───────────────"
echo "export AZURE_OPENAI_ENDPOINT=\"$(terraform output -raw openai_endpoint)\""
echo "export AZURE_OPENAI_CHAT_DEPLOYMENT=\"$(terraform output -raw chat_deployment)\""
echo "────────────────────────────────────────────────────────────────────────"
echo "Done. When you stop for the day: scripts/tear-down.sh"

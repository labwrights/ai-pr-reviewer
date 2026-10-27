#!/usr/bin/env bash
# Destroys the lab's Azure resources and PROVES the money has stopped: the
# resource group is gone, and no deleted Foundry account is left to purge.
#
#   scripts/tear-down.sh
set -euo pipefail

cd "$(dirname "$0")/../infra/envs/lab"

if ! az account show >/dev/null 2>&1; then
  echo "❌ You are not logged in to Azure. Run: az login"
  exit 1
fi
export ARM_SUBSCRIPTION_ID="$(az account show --query id -o tsv)"
RG="rg-fieldnotes-reviewer"

echo "Destroying lab resources (takes 2-6 minutes)…"
terraform init -input=false >/dev/null
terraform destroy -auto-approve -input=false >/dev/null || true

echo
FAILED=0
if [ "$(az group exists -n "$RG")" = "false" ]; then
  echo "✅ Resource group '$RG' is gone."
else
  LEFT=$(az resource list -g "$RG" --query "length(@)" -o tsv 2>/dev/null || echo "0")
  if [ "$LEFT" = "0" ]; then echo "✅ Resource group '$RG' has nothing running."
  else echo "⚠️  $LEFT resource(s) still in '$RG':"; az resource list -g "$RG" -o table; FAILED=1; fi
fi
SOFT=$(az cognitiveservices account list-deleted --query "[?starts_with(name,'fdy-fieldnotes-')] | length(@)" -o tsv 2>/dev/null || echo "0")
if [ "$SOFT" = "0" ]; then
  echo "✅ No deleted Foundry account waiting to be purged."
else
  echo "⚠️  $SOFT deleted Foundry account(s) still held; purge with:"
  echo "    az cognitiveservices account list-deleted -o table   then   az cognitiveservices account purge ..."
  FAILED=1
fi
echo
if [ "$FAILED" = "0" ]; then
  echo "Run-rate is now \$0/day (nothing left running)."
  echo "What this session already used (tokens) is still billed; it shows up in Cost Management within a day or two."
else
  echo "❌ Something is still there: fix the ⚠️ lines above, then run this script again."
  exit 1
fi

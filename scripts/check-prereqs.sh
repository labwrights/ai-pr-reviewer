#!/usr/bin/env bash
# Verifies everything START-HERE requires, one check at a time.
# Prints a ✅ or ❌ per item with the exact fix. Exits 0 only when all pass.
set -u

PASS=0
FAIL=0
ok()   { echo "✅ $1"; PASS=$((PASS+1)); }
bad()  { echo "❌ $1"; echo "   fix → $2"; FAIL=$((FAIL+1)); }
info() { echo "ℹ️  $1"; }

echo "AI PR Reviewer prerequisite check"
echo "---------------------------------"

if command -v git >/dev/null 2>&1; then ok "Git is installed"; else bad "Git" "https://git-scm.com/downloads"; fi

if command -v uv >/dev/null 2>&1 || [ -x "$HOME/.local/bin/uv" ]; then
  ok "uv is installed (it creates the Python 3.12 environment)"
else
  bad "uv" "curl -LsSf https://astral.sh/uv/install.sh | sh"
fi

if command -v az >/dev/null 2>&1; then
  ok "Azure CLI is installed ($(az version --query '"azure-cli"' -o tsv 2>/dev/null))"
  if az account show >/dev/null 2>&1; then
    ok "Azure CLI is logged in (subscription: $(az account show --query name -o tsv))"
    if az ad signed-in-user show --query id -o tsv >/dev/null 2>&1; then
      ok "You can read your Entra ID profile (lab 2 registers an app in your tenant)"
    else
      info "Couldn't read your Entra ID profile. Lab 2 needs permission to register an app; see START-HERE"
    fi
  else
    bad "Azure CLI login" "run: az login"
  fi
else
  bad "Azure CLI" "https://learn.microsoft.com/cli/azure/install-azure-cli"
fi

if command -v terraform >/dev/null 2>&1; then
  TFV=$(terraform version -json 2>/dev/null | python3 -c 'import json,sys; print(json.load(sys.stdin)["terraform_version"])' 2>/dev/null || terraform version | head -1)
  ok "Terraform is installed ($TFV; 1.9 or newer is needed)"
else
  bad "Terraform 1.9+" "https://developer.hashicorp.com/terraform/install"
fi

if command -v gh >/dev/null 2>&1; then
  if gh auth status >/dev/null 2>&1; then ok "GitHub CLI is installed and logged in"
  else bad "GitHub CLI login" "run: gh auth login   (lab 2 uses it)"; fi
else
  bad "GitHub CLI" "https://cli.github.com   (lab 2 uses it)"
fi

echo "---------------------------------"
echo "$PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ]

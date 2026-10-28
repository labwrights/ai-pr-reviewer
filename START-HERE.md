# Start here

Welcome. In about 4 hours you'll build an AI reviewer for pull requests, measure how good it is, and run it on every pull request in your own repository. This page gets you ready: the tools you need, your Azure subscription, and a first run.

## 1. What you need

- **Python basics**: you can read a function and run a script.
- **git and a GitHub account**: you'll make your own copy of this repository, because GitHub Actions runs there.
- **An Azure subscription with billing enabled** (section 2).
- **These tools** on Linux, macOS, or Windows with WSL2: git, [uv](https://docs.astral.sh/uv/) (it brings Python 3.12), the [Azure CLI](https://learn.microsoft.com/cli/azure/install-azure-cli), [Terraform](https://developer.hashicorp.com/terraform/install) 1.9 or newer, and the [GitHub CLI](https://cli.github.com).

Check them all at once:

Run

```bash
scripts/check-prereqs.sh
```

**Expected result:** one ✅ per tool, then `7 passed, 0 failed`. Each ❌ prints the exact fix.

## 2. Set up your Azure subscription (once)

A personal pay-as-you-go subscription is exactly right. If you don't have one, sign up at azure.microsoft.com and choose pay-as-you-go.

**It's your own subscription.** Everything the labs create goes into the Azure subscription you sign in with, and Azure bills you for it directly. Labwrights never sees your subscription, your resources or your bill.

1. **Sign in** so the labs can act as you:

   Run

   ```bash
   az login
   ```

   If you have more than one subscription, make sure the labs use the right one. Check it, and change it if needed:

   Run

   ```bash
   az account show --query name -o tsv                       # the subscription the labs will use
   az account set --subscription "<your lab subscription>"   # only if it's the wrong one
   ```

   Use a subscription you're allowed to spend on: a work subscription only if your company agrees. Every bring-up script prints the subscription's name first, so you can check before anything is created.

2. **Protect your wallet.** A budget alert means a forgotten resource can never surprise you:

   Run

   ```bash
   az consumption budget create --budget-name labs-cap \
     --amount 25 --time-grain Monthly --category Cost \
     --start-date $(date +%Y-%m-01) --end-date 2030-01-01
   ```

   You can also do this in the portal: Cost Management → Budgets. Add your email as the alert recipient there.

3. **Check you can register an app.** Lab 2 lets GitHub Actions sign in to Azure, which means registering an app in your Azure tenant. A personal Azure account can always do this; company tenants often block it. If lab 2 fails with "Insufficient privileges", use a personal subscription.

4. **Cost expectations.** Both labs together cost **under $0.25** in our runs, if you tear down when each lab tells you to. The model bills per token and costs nothing while idle. All cost figures are **estimates**. Your actual costs depend on your use: how much you call the model, how long you keep resources up, your region, and Azure's current prices. **They're entirely yours:** Azure bills you directly, and Labwrights doesn't pay or refund them.

5. **Region note.** The labs default to `eastus2`, which offers the model. If yours doesn't, `scripts/bring-up.sh --location swedencentral` uses another region.

## 3. First run

Run

```bash
uv venv --python 3.12 .venv && uv pip install -p .venv -e ".[dev]" -c constraints.txt
.venv/bin/python -m pytest
```

**Expected result:** `11 passed`. You're ready for [lab 1](labs/lab-01/README.md).

## 4. How the labs work

- **Each lab opens with a TL;DR**: what you build, how long it takes, what it costs, and the new words it introduces. [GLOSSARY.md](GLOSSARY.md) collects them.
- **Every step shows the real output** to expect, captured from a run in October 2026. Model answers vary in wording; each lab says what must hold.
- **You write the reviewer's core**; the diff reader, the model client, the GitHub helper, the Terraform and the scripts are pre-built and commented.
- **Stuck?** `scripts/catch-up.sh 1` puts your reviewer exactly at the end of lab 1. `solutions/` holds every reference file.
- **Every lab ends with a teardown** that brings your Azure run-rate back to $0/day.

## 5. Getting help

Open an issue on [labwrights/ai-pr-reviewer](https://github.com/labwrights/ai-pr-reviewer) with the lab, the step, and the exact output you got.

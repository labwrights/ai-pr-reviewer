# AI PR Reviewer on Azure

**Build an AI reviewer for your pull requests, measure it, and run it on every PR.** A free Labwrights package.

> **TL;DR**
> - **What you do:** build a reviewer that reads a pull request's changes, reports real problems with the exact file, line and reason, and refuses anything it can't back up. Measure it on pull requests with planted bugs. Then put it on every pull request in GitHub Actions, signed in to Azure without a stored secret.
> - **Format:** 2 hands-on labs, text and code, in your own copy of this repository. Every command and expected output was captured from a real run.
> - **Time:** about 4 hours.
> - **Azure cost:** **under $0.25 in total**, if you tear down when each lab says so. *Costs are estimates from our runs. Yours depend on your use, your region and Azure's current prices, and they're entirely yours: Azure bills you directly.*
> - **You need:** Python basics, git and a GitHub account, and an Azure subscription with billing enabled.
> - **Price:** free.

**Start here → [START-HERE.md](START-HERE.md)**

---

## What you'll build

```
 a pull request ──→ GitHub Actions (signed in to Azure with OIDC: no secret stored)
                       │ the diff, with every line numbered
                       ▼
                 your reviewer ──→ gpt-5.4-mini on Azure, strict output schema
                       │ findings: file, line, severity, why
                       ▼
                 validated against the lines the PR changed
                       │
                       ▼
 inline comments on the PR · a cost line · never an approval
```

Most AI-review demos stop when the bot posts a comment. This one keeps going: it checks every finding against the diff, splits changes too big for one call, measures itself on known bugs, and treats the pull request's own text as untrusted.

## The labs

| # | Lab | What you build | Time | Azure cost |
|---|---|---|---|---|
| 1 | [A reviewer that tells the truth](labs/lab-01/README.md) | structured findings, validation against the diff, splitting, a measured catch rate | 2 h | ≈ $0.01–0.05 |
| 2 | [On every pull request](labs/lab-02/README.md) | the reviewer in GitHub Actions: OIDC, inline comments, a cost line, an injection that fails | 2 h | ≈ $0.01–0.05 |
| | **Total** | | **≈ 4 h** | **≈ $0.02–0.10** |

## Who it's for

- Developers who open and review pull requests, and want an AI reviewer they can trust and explain.
- Anyone curious how Labwrights teaches, before choosing a full package.

## Where to go next

This free package is a taste of the full Labwrights packages, which go much deeper:

- **[AI Agents & MCP on Azure](https://labwrights.io/agents-mcp-on-azure/)**: an agent with tools and approvals, your own MCP server behind Entra ID, an evaluation gate, monitoring, and layered defences against prompt injection.
- **[RAG on Azure](https://labwrights.io/rag-on-azure/)**: a production RAG system with ingestion, hybrid search, cited answers, evaluation and monitoring.

## How this repository is organized

```
START-HERE.md   setup: prerequisites, your Azure subscription, first run
GLOSSARY.md     every technical term the labs introduce
labs/           the 2 labs: start at lab-01
reviewer/       the reviewer: you write the parts the labs show; the helpers are pre-built
fieldnotes/     a small slice of the Fieldnotes team app: the code under review
data/prs/       nine prepared pull requests: six planted bugs, two clean, one injection attempt
tests/          the reviewer's tests (no Azure needed)
infra/          pre-built, commented Terraform: one Microsoft Foundry account and model
scripts/        bring-up, tear-down, prerequisite check, catch-up
solutions/      the reviewer at the start, and at the end of each lab
.github/        the review workflow, ready after lab 2's setup
```

---

Code: MIT licence. Lab text and docs: © Labwrights. See [LICENSE.md](LICENSE.md). Not affiliated with or endorsed by Microsoft or GitHub. Azure is a trademark of Microsoft Corporation; GitHub is a trademark of GitHub, Inc.

# Changelog

What changed in this package, newest first. Before every release, both labs are run again on live Azure and in GitHub Actions.

## [2027 Edition]

First release.

- **2 labs** that build an AI reviewer for pull requests: structured findings validated against the diff, splitting large changes, a measured catch rate on planted bugs, then GitHub Actions with OIDC (no stored secret), inline comments, a cost line, and a pull request that tries to talk the reviewer into approving.
- **Every command and expected output was captured from a real run** on live Azure and GitHub Actions in October 2026.
- **Pinned dependencies** through `constraints.txt`: `openai` 3.39.0, `azure-identity` 1.27.0.
- **Model version:** `gpt-5.4-mini` (2026-03-17). Azure's catalog lists its retirement as 2027-09-21.

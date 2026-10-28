# Changelog

What changed in this package, newest first. Before every release, both labs are run again on live Azure and in GitHub Actions.

## [2027 Edition, update 1] — 2026-10-27

A documentation-only update; no lab content changed.

- **[START-HERE.md](START-HERE.md), section 2,** now says plainly that the labs run on your own Azure subscription and bill you directly. It also shows how to check which subscription the labs will use, and change it, if you have more than one.
- **Azure costs:** START-HERE and the README now say that your costs depend on your use, and that they're entirely yours: Azure bills you directly.

## [2027 Edition]

First release.

- **2 labs** that build an AI reviewer for pull requests: structured findings validated against the diff, splitting large changes, a measured catch rate on planted bugs, then GitHub Actions with OIDC (no stored secret), inline comments, a cost line, and a pull request that tries to talk the reviewer into approving.
- **Every command and expected output was captured from a real run** on live Azure and GitHub Actions in October 2026.
- **Pinned dependencies** through `constraints.txt`: `openai` 3.39.0, `azure-identity` 1.27.0.
- **Model version:** `gpt-5.4-mini` (2026-03-17). Azure's catalog lists its retirement as 2027-09-21.

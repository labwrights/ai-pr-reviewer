# Glossary

Every technical term the labs introduce, in the order you meet them.

## Lab 1 — A reviewer that tells the truth

- **diff** (lab 1): the lines a change adds and removes, as `git diff` prints them; `+` lines are added, `-` lines removed.
- **hunk** (lab 1): one block of a diff, starting with an `@@` line, with a few unchanged lines around the change.
- **structured output** (lab 1): a model reply that must fit a schema you send, so your code can always read it.
- **false alarm** (lab 1): a finding on code that has nothing wrong with it; on a clean change, any serious finding is one.

## Lab 2 — On every pull request

- **workflow** (lab 2): a file in `.github/workflows/` that tells GitHub Actions what to run, and on which events.
- **OIDC federation** (lab 2): a way for GitHub Actions to sign in to Azure with a short-lived token for one repository and event, so no secret is stored anywhere.
- **least privilege** (lab 2): giving a program only the permissions its job needs, so a mistake or a misuse can do little harm.
- **prompt injection** (lab 2): text written to give a model orders its owner never gave, such as a pull request description telling the reviewer to approve.

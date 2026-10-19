# Secrets

*Last updated: 2026-10-19*

> What never enters a repository — credentials, secrets and private infrastructure identifiers — and where they live.
> Applies to every repository, public or private.

## Repository content

- must not commit passwords, tokens, API keys, private keys, OAuth client secrets or connection strings.
- must not commit real host addresses, provider hostnames, or account and customer IDs.
- may commit placeholders (`<actual-host>`), example values and generated test-only credentials.
- may commit generic provider portal URLs and runbook steps.

---

## Storage

- must keep credentials and private identifiers in NordPass.
- must place runtime secrets as protected files on the host they serve, never in images or bundles: mode `0600`,
  or `0444` inside a `0700` folder when a container reads the file.
- must keep CI secrets in GitHub environment secrets, never in workflow files or logs.

---

## Agents

- must not print or copy a secret value into chat, logs, tool input or files.
- must hand credential entry to the developer; an agent never types a password or token.
- must reference a secret by its NordPass item or host file path, never by value.

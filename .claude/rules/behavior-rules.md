# Behavior Rules

## Lookup

- `.claude/repo-registry.md` maps every wow-two repo to its org, purpose and status -- consult it before answering about a repo
- Read a repo's own `CLAUDE.md` before changing that repo

## Cross-repo workflow

Updating a library other repos depend on: identify its consumers (the registry, or a search for the package reference) → check their use of the API being changed → update the lib first, then the consumers → note breaking changes in the commit message.

## Dependency awareness

- `wow-two-sdk` packages reach apps and external users -- a breaking change needs a major version bump
- `wow-two-sdk-beta` packages and products may break whenever it improves something, while products have no external users; `wow-two-platform` packages are internal -- break more freely, still coordinate consumer updates -> `conventions/development/breaking-changes.md`

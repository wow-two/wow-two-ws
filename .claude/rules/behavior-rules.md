# Behavior Rules

## Lookup

- `repo-registry.md` maps every wow-two repo to its org, purpose, and status — consult it before answering about a repo.
- Each repo may have its own `CLAUDE.md` — read it before changing that repo.
- Touching *how we build*? `conventions/conventions.md` is the index to every convention.

## Cross-repo workflow

Updating a library other repos depend on:

1. Identify consumers (the registry, or search for the package reference).
2. Check the consumer's usage of the API being changed.
3. Update the lib first, then the consumers.
4. Note breaking changes in the commit message.

## Dependency awareness

- `wow-two-sdk` / `wow-two-sdk-beta` packages → consumed by apps + external users; a breaking change needs a major version bump.
- `wow-two-platform` packages → internal only; can break more freely, but still coordinate consumer updates.

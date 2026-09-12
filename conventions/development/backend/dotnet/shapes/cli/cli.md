# CLI

*Last updated: 2026-09-10*

> Recognized command-line shape; generic CLI architecture is not yet selected.

## Activation

- must inherit [core](../../core/core.md) rules.
- must define process lifetime, command boundaries, exit codes and test strategy when starting a standalone CLI.
- must declare its concrete dependencies rather than automatically copy the service project split.
- must use [SDK delivery](../sdk/delivery/delivery.md) for a CLI published in the SDK package family.
- must use [migration tooling](../../core/mla/domains/persistence/migrations/sql/migration-tooling.md)
  for the existing SDK migration command; its domain behavior is already owned there.

---

## Open

- generic CLI architecture and testing remain unwritten until a CLI outside the existing migration-tool scope is active.

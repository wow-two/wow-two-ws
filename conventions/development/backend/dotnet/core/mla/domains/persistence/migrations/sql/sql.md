# Sql

*Last updated: 2026-10-28*

> Ordered SQL scripts and their migration hosts.

## Files

- [bespoke migrations](bespoke-migrations.md) — layout, lifecycle, integrity and registration.
- [migration dialects](migration-dialects.md) — dialect-correct Apply and Rollback SQL.
- [migration tooling](migration-tooling.md) — the `migrate` tree's hosts, exit mapping, guards and configuration.

---

## Boundary

- must follow the selected runner's file contract, including any required rollback file.
- must preserve applied scripts under the [migration lifecycle](../migrations.md#lifecycle).

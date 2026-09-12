# Sql

*Last updated: 2026-09-10*

> Ordered SQL scripts and their migration hosts.

## Files

- [bespoke migrations](bespoke-migrations.md) — layout, lifecycle, integrity and registration.
- [migration dialects](migration-dialects.md) — dialect-correct Apply and Rollback SQL.
- [migration tooling](migration-tooling.md) — CLI composition, exit codes and target guards.

---

## Boundary

- must follow the selected runner's file contract, including any required rollback file.
- must preserve applied scripts under the [migration lifecycle](../migrations.md#lifecycle).

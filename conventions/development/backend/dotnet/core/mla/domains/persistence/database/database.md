# Database

*Last updated: 2026-09-10*

> The engine the schema lives in — its types, its enum forms, its column conventions.
> Purpose — an engine fact travels with the engine, so swapping one does not rewrite the model.
> Use case — choosing a column type, or reading what a given engine fixes.

## Engines

| Engine | Docs |
|---|---|
| Postgres | [postgres](postgres/postgres.md) |

- must keep a mapping API out of here — how EF or Dapper reaches a column is [access](../access/access.md).
- must inherit [schema ownership](../persistence.md#contract); engine facts do not choose the migration strategy.

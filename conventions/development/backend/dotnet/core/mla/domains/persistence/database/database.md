# Database

*Last updated: 2026-10-27*

> The engine the schema lives in — its types, its enum forms, its column conventions.
> Purpose — an engine fact travels with the engine, so swapping one does not rewrite the model.
> Use case — choosing a column type, or reading what a given engine fixes.

## Engines

| Engine | Docs |
|---|---|
| Postgres | [postgres](postgres/postgres.md) |

- must run every product and platform service on PostgreSQL, Identity included; SQLite is banned for them
  (developer, 2026-10-27).
- may use SQLite only for a very small service whose data can be lost without harm, and only by the owner's choice;
  no current product qualifies. Tests keep their SQLite speed lane ([test databases](../testing/test-databases.md)).
- must keep a mapping API out of here — how EF or Dapper reaches a column is [access](../access/access.md).
- must inherit [schema ownership](../persistence.md#contract); engine facts do not choose the migration strategy.

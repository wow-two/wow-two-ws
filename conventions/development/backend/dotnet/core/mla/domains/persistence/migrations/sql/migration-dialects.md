# Migration dialects

*Last updated: 2026-09-10*

> Authoring PostgreSQL and SQLite migration SQL; runner lifecycle belongs to [bespoke migrations](bespoke-migrations.md).

## Quoting

- must quote reserved identifiers consistently in creation, queries, indexes and rollback.
- must use SQL double quotes for identifiers in both PostgreSQL and SQLite.
- may rename a reserved identifier while the schema is still fluid.

---

## Rollback

- must follow the [rollback contract](bespoke-migrations.md#rollback).
- must remove dependent objects before the objects they depend on.
- must use `IF EXISTS` where recovery can encounter partial state.
- must inspect `CASCADE` dependencies before using it; do not remove unrelated objects as collateral recovery.
- must invert added columns and indexes explicitly when an inverse exists.
- must not promise removal of an enum label through `ALTER TYPE`; PostgreSQL has no direct drop-label operation.

---

## Transactions

- must follow the [transaction contract](bespoke-migrations.md#transactions).
- must use `-- @no-transaction` for `CREATE INDEX CONCURRENTLY`, `REINDEX CONCURRENTLY`, or maintenance that forbids a transaction.
- must keep nontransactional files single-statement where possible.
- must make recovery correct after partial execution, not merely suppress duplicate-object errors.
- must not assume PostgreSQL supports `IF NOT EXISTS` on every `ALTER` form.

---

## Concurrent indexes

- must check a same-name index's definition and validity before treating it as applied.
- must recover an invalid concurrent build by an intentional drop/rebuild or reindex strategy.
- must not use `CREATE INDEX CONCURRENTLY IF NOT EXISTS` alone as interrupted-build recovery.
- must verify recovery from an interrupted build before declaring the migration restart-safe.
- engine behavior → [PostgreSQL concurrent index creation](https://www.postgresql.org/docs/current/sql-createindex.html).

---

## Native enum changes

- must add a PostgreSQL enum label through a migration.
- may add a label inside a transaction, but must commit before using that label.
- must split add-label and use-label work across the commit boundary.
- must use `IF NOT EXISTS` when a nontransactional add-label operation can be retried.
- must follow [stored enum names](../../database/postgres/postgres.md#enums).

```sql
ALTER TYPE code_status ADD VALUE IF NOT EXISTS 'archived';
```

- transaction behavior → [PostgreSQL ALTER TYPE](https://www.postgresql.org/docs/current/sql-altertype.html).

---

## Schema mapping

- must mirror the [selected schema owner](../../persistence.md#contract) in runtime mappings.
- must name constraints explicitly when later migrations or rollback reference them.
- must use the [Postgres type rules](../../database/postgres/postgres.md#types) for PostgreSQL columns.

---

## SQLite storage

- must match the stored shape consumed by the product's access provider.
- must use the [portable enum policy](../../database/postgres/postgres.md#enums) for new enum storage.
- must preserve an existing ordinal mapping until an explicit data migration changes it.
- must update any enum `CHECK` constraint when a new accepted value lies outside its set.
- must not describe that constrained case as a code-only enum change.
- must verify timestamp and UUID converters against stored values; SQLite affinity alone does not define those contracts.
- must use a GUID-compatible storage representation rather than `INTEGER PRIMARY KEY` for a GUID key.

---

## SQLite alterations

- must use a table rebuild for a type or constraint change not supported by `ALTER TABLE`.
- must preserve rows, indexes, triggers and foreign-key relationships through the rebuild.
- must verify both Apply and Rollback against the declared SQLite version.
- must not mark an ordinary SQLite index build nontransactional.
- must place connection pragmas outside a transaction when SQLite requires it.
- must enable `PRAGMA foreign_keys = ON` on every connection relying on foreign-key enforcement.
- must verify integrity after a table rebuild, not only successful SQL execution.
- supported changes → [SQLite ALTER TABLE](https://www.sqlite.org/lang_altertable.html).

# Migration dialects

*Last updated: 2026-10-28*

> Authoring PostgreSQL and SQLite migration SQL; runner lifecycle belongs to [bespoke migrations](bespoke-migrations.md).
> Point ids cite the [migrations analysis](../../../../../../../../../../ideas/migrations-analysis-2026-10/migrations-analysis-2026-10.md).

## Naming

- must write identifiers unquoted, in [snake_case](../../database/postgres/postgres.md#naming) (M64).
- must rename an identifier that would need quotes, such as a reserved word, rather than quote it (M64).
- must reference an identifier with one spelling and quoting in creation, queries, indexes and rollback.

---

## Idempotency

- the rule → [rollback contract](bespoke-migrations.md#rollback) (M2); its idioms follow.
- must guard creation and removal with `IF NOT EXISTS` and `IF EXISTS` where the statement accepts them.
- must write a reference-data upsert as `INSERT … ON CONFLICT (…) DO UPDATE` (M26).
- must bound a backfill to the rows it has not filled yet, as `WHERE new_column IS NULL` (M23).

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

## Lock safety

The `Testing.Data` lint flags each risk below (M22); the runner's lock bounds → [execution](../migrations.md#execution).

- must build an index on an existing table `CONCURRENTLY`, in a `-- @no-transaction` file (M22).
- must add a constraint to an existing table `NOT VALID`, then `VALIDATE CONSTRAINT` it (M22).
- must not run an `ALTER COLUMN … TYPE` that rewrites a populated table; widening a `varchar(n)` does not (M22, M73).
- must not add a column with a volatile default to an existing table (M22).

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

- applies only to a SQLite set the [model](../migrations.md#model) still allows (M40, M49).
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

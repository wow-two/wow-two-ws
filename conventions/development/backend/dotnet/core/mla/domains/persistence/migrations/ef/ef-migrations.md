# EF migrations

*Last updated: 2026-10-28*

> Banned in wow2 (owner 2026-10-28): no set evolves through EF migrations, `EnsureCreated` or `Database.Migrate()`.
> EF Core maps a SQL-owned schema only → [EF mapping](../../access/ef/ef-mapping.md); every set is
> [bespoke SQL](../sql/bespoke-migrations.md).
> Point ids cite the [migrations analysis](../../../../../../../../../../ideas/migrations-analysis-2026-10/migrations-analysis-2026-10.md).

## Why

- EF decides the SQL at generation time; no reviewed script in the repository says what runs.
- A generated rename or type change may drop and re-add a column, losing its data.
- `Down` is generated and seldom run, so a rollback stays unproven (M2, M59).
- It carries no migration kinds, `-- @contract since=`, lock timeout or no-transaction header (M16, M21, M50).
- The model snapshot and designer files drift and conflict between branches.
- `Database.Migrate()` invites an apply at boot, which deployed boots forbid (M47).

---

## Converting an EF set

- must convert at the product's sweep: script the current model once (`dotnet ef dbcontext script`) into
  `001-<name>/Apply.sql`, hand-write its `Rollback.sql`, then delete `Migrations/`, the snapshot and the designer files.
- must conform the scripted schema to the [PostgreSQL rules](../../database/postgres/postgres.md) while converting.
- may drop and recreate the set's database instead of a `baseline`, while products have no external users
  (owner 2026-10-28).
- must answer the `migrate` verbs through `AddEfMigrationsRunner<TContext>` only until the conversion lands (M11).

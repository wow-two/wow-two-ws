# EF migrations

*Last updated: 2026-10-28*

> EF-owned schema evolution for a code-first set.
> Point ids cite the [migrations analysis](../../../../../../../../../../ideas/migrations-analysis-2026-10/migrations-analysis-2026-10.md).

## Selection

- may select EF migrations when one model owns schema evolution.
- must not combine this strategy with SQL-owned migrations over the same schema.
- must follow the shared [migration lifecycle](../migrations.md#lifecycle).
- must answer the same `migrate` verbs and exits as every set (M11) → [actions](../migrations.md#actions).

---

## Registration

- may register `AddEfMigrationsRunner<TContext>()` for a local run's boot apply only, when `IsLocalRun` (M16).
- must not let it apply on any deployed boot, dev included; the step runs `app migrate` (M16, M47).
- must validate configured connection retry counts and delays through the agreed [options recipe](../../../../components/options.md#registration).
- actual registration and defaults → [EF migration registration](../../../../../../../../../../workbench/wow-two-sdk-beta/wow-two-sdk-beta.be/engineering/codebase/wow-two-sdk-beta-be/src/Data/Migrations/Ef/EfMigrationsServiceCollectionExtensions.cs).

---

## Authoring

- must edit the model and generate its migration rather than hand-edit the database.
- must review generated operations for data preservation before applying them.
- may use migration SQL for an operation the EF model cannot express.
- must not remove an applied migration to rewrite shared history.
- must keep each migration's `Down` a real inverse, or an explicit no-op where none exists (M2).
- must put a contract in a migration of its own (M21) → [compatibility](../migrations.md#compatibility).
- must keep the model snapshot and migration files in the owning repository.

```bash
dotnet ef migrations add AddServiceColumn
```

---

## Execution

- must verify the runner/provider's locking before allowing concurrent application → [execution](../migrations.md#execution).
- must distinguish a transient connection failure from a failing migration statement when configuring retries.
- must verify both model mapping and migration behavior on the target engine.
- must keep migration-only mapping configuration when EF generates the schema.
- runtime mapping → [EF mapping](../../access/ef/ef-mapping.md).

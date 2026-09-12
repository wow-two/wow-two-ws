# EF migrations

*Last updated: 2026-09-10*

> EF-owned schema evolution for a code-first product database.

## Selection

- may select EF migrations when one model owns schema evolution.
- must not combine this strategy with SQL-owned migrations over the same schema.
- must follow the shared [migration lifecycle](../migrations.md#lifecycle).

---

## Registration

- must register the startup runner through `AddEfMigrationsRunner<TContext>()` when the host applies development migrations.
- must disable that runner on a production application host using an explicit deployment migration action.
- must validate configured connection retry counts and delays through the agreed [options recipe](../../../../components/options.md#registration).
- actual registration and defaults → [EF migration registration](../../../../../../../../../../workbench/wow-two-sdk-beta/wow-two-sdk.backend.beta/engineering/codebase/wow-two-back-beta-sdk/src/Data/Migrations/Ef/EfMigrationsServiceCollectionExtensions.cs).

---

## Authoring

- must edit the model and generate its migration rather than hand-edit the database.
- must review generated operations for data preservation before applying them.
- may use migration SQL for an operation the EF model cannot express.
- must not remove an applied migration to rewrite shared history.
- must keep the model snapshot and migration files in the owning repository.

```bash
dotnet ef migrations add AddServiceColumn
```

---

## Execution

- must verify the runner/provider's locking before allowing concurrent application → [coordination](../migrations.md#coordination).
- must distinguish a transient connection failure from a failing migration statement when configuring retries.
- must verify both model mapping and migration behavior on the target engine.
- must keep migration-only mapping configuration when EF generates the schema.
- runtime mapping → [EF mapping](../../access/ef/ef-mapping.md).

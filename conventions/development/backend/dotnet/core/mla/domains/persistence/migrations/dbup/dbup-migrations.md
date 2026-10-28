# DbUp migrations

*Last updated: 2026-10-28*

> Forward-only embedded SQL with DbUp's journal and an explicit provider choice.
> Point ids cite the [migrations analysis](../../../../../../../../../../ideas/migrations-analysis-2026-10/migrations-analysis-2026-10.md).

## Selection

- must not start a new set on DbUp: every set keeps a rollback (M2), and DbUp journals forward scripts only.
- must let a DbUp set answer the same `migrate` verbs and exits as every set (M11).
- must follow shared [lifecycle and execution](../migrations.md).
- must not treat journaled repeat execution as protection against simultaneous applicants.

---

## Registration

- must pass the connection string explicitly to `AddDbUpRunner(connectionString, configure)`.
- must choose PostgreSQL through `UsePostgres()` on the configured options (M40).
- must specify the scripts assembly and a resource-prefix filter when the assembly contains unrelated SQL.
- must not mutate registered options after composition.

```csharp
services.AddDbUpRunner(connectionString, options =>
{
    options.UsePostgres();
    options.ScriptsAssembly = typeof(SomePersistenceMarker).Assembly;
    options.ScriptsNamespacePrefix = "App.Migrations.Scripts.";
});
```

- current registration → [DbUp registration source](../../../../../../../../../../workbench/wow-two-sdk-beta/wow-two-sdk-beta.be/engineering/codebase/wow-two-sdk-beta-be/src/Data/Migrations/DbUp/DbUpServiceCollectionExtensions.cs).
- provider selectors → [DbUp extensions](../../../../../../../../../../workbench/wow-two-sdk-beta/wow-two-sdk-beta.be/engineering/codebase/wow-two-sdk-beta-be/src/Data/Migrations/DbUp/Extensions/DbUpExtensions.cs).

---

## Execution

- must abort host startup when a local run's boot migration fails.
- must enable the startup runner only when `IsLocalRun`; a deployed boot never applies (M16, M47).
- must apply on deploy through the step's `app migrate` (M11) → [actions](../migrations.md#actions).
- must verify runner options against the [options source](../../../../../../../../../../workbench/wow-two-sdk-beta/wow-two-sdk-beta.be/engineering/codebase/wow-two-sdk-beta-be/src/Data/Migrations/DbUp/DbUpOptions.cs).

---

## Scripts

- must embed scripts as assembly resources.
- must name scripts so lexical order equals apply order, using zero-padded ordinals.
- must not rename an applied script; its name is its journal identity.
- must undo a change through a new forward script.
- must not expect DbUp's journal to detect changed contents in a previously applied script.

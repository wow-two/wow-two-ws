# DbUp migrations

*Last updated: 2026-09-10*

> Forward-only embedded SQL with DbUp's journal and an explicit provider choice.

## Selection

- may select DbUp for an existing forward-only script set or an additive schema with no in-place rollback.
- must select another runner when checksum drift detection or paired rollback is required.
- must follow shared [lifecycle and coordination](../migrations.md).
- must not treat journaled repeat execution as protection against simultaneous applicants.

---

## Registration

- must pass the connection string explicitly to `AddDbUpRunner(connectionString, configure)`.
- must choose the provider through `UsePostgres()`, `UseSqlServer()` or `UseMySql()` on the configured options.
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

- current registration → [DbUp registration source](../../../../../../../../../../workbench/wow-two-sdk-beta/wow-two-sdk.backend.beta/engineering/codebase/wow-two-back-beta-sdk/src/Data/Migrations/DbUp/DbUpServiceCollectionExtensions.cs).
- provider selectors → [DbUp extensions](../../../../../../../../../../workbench/wow-two-sdk-beta/wow-two-sdk.backend.beta/engineering/codebase/wow-two-back-beta-sdk/src/Data/Migrations/DbUp/Extensions/DbUpExtensions.cs).

---

## Execution

- must abort host startup when a development boot migration fails.
- must run production migration application as an explicit deployment action.
- must not register the enabled startup runner on a production application host that should never mutate schema at boot.
- must verify runner options against the [options source](../../../../../../../../../../workbench/wow-two-sdk-beta/wow-two-sdk.backend.beta/engineering/codebase/wow-two-back-beta-sdk/src/Data/Migrations/DbUp/DbUpOptions.cs).

---

## Scripts

- must embed scripts as assembly resources.
- must name scripts so lexical order equals apply order, using zero-padded ordinals.
- must not rename an applied script; its name is its journal identity.
- must undo a change through a new forward script.
- must not expect DbUp's journal to detect changed contents in a previously applied script.

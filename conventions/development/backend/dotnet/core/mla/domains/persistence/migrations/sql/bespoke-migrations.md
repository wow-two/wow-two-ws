# Bespoke migrations

*Last updated: 2026-09-10*

> SQL-owned schema evolution through ordered Apply/Rollback pairs and a checksum journal.

## Layout

- must place each promoted migration in `Migrations/NNN-name/`.
- must give it `Apply.sql` and `Rollback.sql`.
- must keep in-flight drafts flat under `Migrations/Dev/`, named with a UTC timestamp and slug.
- must allocate the ordinal at promotion on the integration branch: highest ordinal plus one.
- must not allocate competing ordinals on feature branches.
- must not embed drafts or read them as numbered migrations.
- layout constants → [migration constants](../../../../../../../../../../workbench/wow-two-sdk-beta/wow-two-sdk.backend.beta/engineering/codebase/wow-two-back-beta-sdk/src/Data/Migrations/Bespoke/MigrationConstants.cs).

---

## Schema

- must treat applied SQL as the owned schema and map entities over it.
- must verify it before changing a model, query or EF mapping.
- must follow the [migration lifecycle](../migrations.md#lifecycle).
- must execute scripts as authored; dialect correctness belongs to the author.
- SQL idioms → [migration dialects](migration-dialects.md).

---

## Rollback

- must retain a `Rollback.sql` file even for an irreversible operation.
- must make that file an explicit no-op with an explanation when no inverse exists.
- must not describe a no-op as restoring the original schema or data.
- must enable rollback or repair only for the guarded operation.
- must use the resolved target confirmation in [tooling](migration-tooling.md#destructive-operations).
- may use guarded rollback in any environment when a forward correction is not viable.

---

## Transactions

- must use the runner's per-file transaction unless SQL genuinely needs execution outside it.
- must mark an outside-transaction Apply with a leading `-- @no-transaction`.
- must make that Apply recoverable from a partially applied and unjournaled state.
- must inspect validity as well as object existence during recovery → [concurrent indexes](migration-dialects.md#concurrent-indexes).
- must not assume multiple SQL statements sent in one command each autocommit independently.
- transaction and result behavior → [runner source](../../../../../../../../../../workbench/wow-two-sdk-beta/wow-two-sdk.backend.beta/engineering/codebase/wow-two-back-beta-sdk/src/Data/Migrations/Bespoke/MigrationRunnerService.cs).

---

## Integrity

- must stop when an applied migration's source checksum changes or source history is unexpectedly absent.
- must resolve drift by an intentional forward correction or guarded rollback/repair.
- must tolerate orphaned history only for an intentional older binary through `AllowOrphanedHistory`.
- must not treat a clean Apply checksum as verification of Rollback content.
- must preserve source files even when the deployed binary no longer needs to apply them.
- must consume the runner's `Result` failures explicitly; a malformed source may still throw at the broker seam.
- checksum normalization and flags → [checksum source](../../../../../../../../../../workbench/wow-two-sdk-beta/wow-two-sdk.backend.beta/engineering/codebase/wow-two-back-beta-sdk/src/Data/Migrations/Bespoke/MigrationChecksumHasher.cs).

---

## Registration

- must register through `AddDatabaseBespokeMigrations(assembly)` for embedded runtime SQL.
- must use `AddDatabaseBespokeMigrations(migrationsRoot)` for filesystem CLI/development SQL.
- must supply the connection factory required by that registration.
- must use the same lock identity for applicants sharing one PostgreSQL database.
- must inherit [coordination](../migrations.md#coordination) for another provider.
- current overloads and options → [registration source](../../../../../../../../../../workbench/wow-two-sdk-beta/wow-two-sdk.backend.beta/engineering/codebase/wow-two-back-beta-sdk/src/Data/Migrations/Bespoke/MigrationServiceCollectionExtensions.cs).

---

## Embedding

- must keep resource names in the slash-separated shape expected by the embedded broker.
- must exclude `Dev/` from the binary.

```xml
<EmbeddedResource Include="Migrations\**\*.sql" Exclude="Migrations\Dev\**\*.sql">
    <LogicalName>Migrations/%(RecursiveDir)%(Filename)%(Extension)</LogicalName>
</EmbeddedResource>
```

- parser contract → [embedded broker](../../../../../../../../../../workbench/wow-two-sdk-beta/wow-two-sdk.backend.beta/engineering/codebase/wow-two-back-beta-sdk/src/Data/Migrations/Bespoke/EmbeddedResourceMigrationBroker.cs).

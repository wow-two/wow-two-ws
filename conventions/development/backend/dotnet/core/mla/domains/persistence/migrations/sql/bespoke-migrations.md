# Bespoke migrations

*Last updated: 2026-10-28*

> SQL-owned schema evolution through ordered Apply/Rollback pairs and a checksum journal, one per set.
> Point ids cite the [migrations analysis](../../../../../../../../../../ideas/migrations-analysis-2026-10/migrations-analysis-2026-10.md).

## Layout

- must place each promoted migration in `Migrations/NNN-name/` (M10).
- must give it `Apply.sql` and `Rollback.sql` (M2).
- must keep in-flight drafts flat under `Migrations/Dev/`, named with a UTC timestamp and slug.
- must promote a draft into the set only by `wow-migrate promote` (M56).
- must allocate the ordinal at promotion on the integration branch: highest ordinal plus one.
- must allocate an ordinal once and never reuse it; gaps stay (M56).
- must not allocate competing ordinals on feature branches.
- must not embed drafts or read them as numbered migrations.
- must ship a template's baseline without a sample table (M56).
- must place seed files in the set's `Seeds/NNN-name.json`: a `mode` and rows per table (M51).
- layout constants → [migration constants](../../../../../../../../../../workbench/wow-two-sdk-beta/wow-two-sdk-beta.be/engineering/codebase/wow-two-sdk-beta-be/src/Data/Migrations/Bespoke/MigrationConstants.cs).

---

## Markers

A file's leading comment lines carry its markers, one per line.

| Marker | Means |
|---|---|
| `-- @contract since=vX.Y` | a contract; `since` is the oldest owner release that no longer reads or writes it (M21) |
| `-- @requires <name>` | `apply` refuses the file until that background migration finished (M25) |
| `-- @lock-timeout <s>` | the file's own `lock_timeout` per batch, instead of 5 s (M17) |
| `-- @no-transaction` | the file runs outside the batch transaction ([transactions](#transactions)) |

- must mark every contract `-- @contract since=vX.Y`; an unmarked file is an expand (M21).
- kinds and the compatibility rule → [migrations](../migrations.md#compatibility).

---

## Schema

- must treat applied SQL as the owned schema and map entities over it.
- must verify it before changing a model, query or EF mapping.
- must follow the [migration lifecycle](../migrations.md#lifecycle).
- must execute scripts as authored; dialect correctness belongs to the author.
- must name a dependency's schema in SQL by `{{schema:<set>}}`, as `{{schema}}` names the set's own (M79).
- SQL idioms → [migration dialects](migration-dialects.md).

---

## Rollback

- must retain a `Rollback.sql` file even for an irreversible operation (M2).
- must make every `Apply.sql` and `Rollback.sql` idempotent: rerun where it took effect, it succeeds and changes
  nothing (M2).
- must write a real inverse in every `Rollback.sql` that has one.
- must split a data-destroying step into its own migration, so only that migration lacks an inverse.
- must make that file an explicit no-op with an explanation when no inverse exists.
- must not describe a no-op as restoring the original schema or data.
- must run `Rollback.sql` only locally, in tests or by the guarded `rollback` verb; a deploy never runs it (M2).
- may run guarded `rollback` on prod only when a forward correction fails (M2).
- verb and guard → [actions](../migrations.md#actions); idempotency proof → [testing](../migrations.md#testing).

---

## Transactions

- must use the runner's per-file transaction unless SQL genuinely needs execution outside it.
- must mark an outside-transaction Apply with a leading `-- @no-transaction`.
- must make that Apply recoverable from a partially applied and unjournaled state.
- must inspect validity as well as object existence during recovery → [concurrent indexes](migration-dialects.md#concurrent-indexes).
- must not assume multiple SQL statements sent in one command each autocommit independently.
- transaction and result behavior → [runner source](../../../../../../../../../../workbench/wow-two-sdk-beta/wow-two-sdk-beta.be/engineering/codebase/wow-two-sdk-beta-be/src/Data/Migrations/Bespoke/MigrationRunnerService.cs).

---

## Integrity

- must stop when an applied migration's source checksum changes or source history is unexpectedly absent.
- must resolve drift by an intentional forward correction or guarded `rollback` or `repair`.
- must refuse orphaned history below the level; a compatible `Ahead` boots per
  [compatibility](../migrations.md#compatibility) (M16).
- must not treat a clean Apply checksum as verification of Rollback content.
- must preserve source files even when the deployed binary no longer needs to apply them.
- must consume the runner's `Result` failures explicitly; a malformed source may still throw at the broker seam.
- checksum normalization and flags → [checksum source](../../../../../../../../../../workbench/wow-two-sdk-beta/wow-two-sdk-beta.be/engineering/codebase/wow-two-sdk-beta-be/src/Data/Migrations/Bespoke/MigrationChecksumHasher.cs).

---

## History

| Table | Holds |
|---|---|
| `migration_history` · `{set}_migration_history` | each applied migration, with `kind` and `contract_since` (M21) |
| `{history}_events` | append-only: verb, ordinals, by, job, at, detail (M61) |
| `{set}_seed_history` | one row per applied seed file (M51) |
| `{set}_background_migrations` | each background migration's state and cursor (M24) |

- must change history only through the verbs; never by hand SQL (M60, M61).

---

## Registration

- must register the default set through `AddDatabaseBespokeMigrations(assembly)` for embedded runtime SQL.
- must register every further set through `AddDatabaseBespokeMigrationSet(name, …)` (M4).
- must use `AddDatabaseBespokeMigrations(migrationsRoot)` for filesystem CLI/development SQL.
- must supply the connection factory required by that registration.
- must declare on the set's registration its dependencies (`DependsOn`), its referenceable tables and its required
  extensions (M41, M79).
- must keep one lock key per set, shared by every host of it, in the migrator's reserved class (M50).
- must inherit [execution](../migrations.md#execution) for another provider.
- current overloads and options → [registration source](../../../../../../../../../../workbench/wow-two-sdk-beta/wow-two-sdk-beta.be/engineering/codebase/wow-two-sdk-beta-be/src/Data/Migrations/Bespoke/MigrationServiceCollectionExtensions.cs).

---

## Embedding

- must keep resource names in the slash-separated shape expected by the embedded broker.
- must exclude `Dev/` from the binary.
- must embed `Seeds/` beside `Migrations/` (M51).

```xml
<EmbeddedResource Include="Migrations\**\*.sql" Exclude="Migrations\Dev\**\*.sql">
    <LogicalName>Migrations/%(RecursiveDir)%(Filename)%(Extension)</LogicalName>
</EmbeddedResource>
```

- parser contract → [embedded broker](../../../../../../../../../../workbench/wow-two-sdk-beta/wow-two-sdk-beta.be/engineering/codebase/wow-two-sdk-beta-be/src/Data/Migrations/Bespoke/EmbeddedResourceMigrationBroker.cs).

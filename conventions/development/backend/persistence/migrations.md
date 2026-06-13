# Migrations

*Last updated: 2026-06-13*

How product authors write and ship SQL migrations for the bespoke migrator (`AddSqlMigrations`). Engine internals (advisory lock, checksum, host model) live in the SDK `Sql/README.md`; this doc is the product-facing contract.

## Canonical layout

Raw `.sql` pairs, one folder per migration, ordinal-prefixed:

```
{Repo}.Persistence/Migrations/
├── 001-baseline/
│   ├── Apply.sql
│   └── Rollback.sql
├── 002-add-users-table/
│   ├── Apply.sql
│   └── Rollback.sql
└── Dev/                     ← flat in-flight drafts, never embedded, never ordinal-named
    ├── .gitkeep
    └── 20260611T1030_add-service-column.sql
```

- Folder name is `NNN-name` (three-digit ordinal + `-` + slug). Matched by `MigrationConventions.FolderPattern()`; parsed into `MigrationDescriptor.Ordinal` / `.Name`.
- File names are fixed: `Apply.sql`, `Rollback.sql` (`MigrationConventions.ApplyFileName` / `.RollbackFileName`). Both required — a folder missing `Rollback.sql` throws at scan (`FileSystemMigrationSource.Read` / `EmbeddedResourceMigrationSource.Read`).
- `Dev/` is reserved (`MigrationConventions.DevFolderName`): flat, editable drafts that carry both Apply + Rollback sections in one file. Promoted to a numbered pair at merge. Never read as a numbered migration; never shipped (csproj excludes it — see below).

> **This IS the schema-first canonical schema.** `Migrations/*/Apply.sql` is the owned `CREATE TABLE` truth — read it before writing any model / query / EF config (the schema-first rule in [database.md](database.md)). EF maps **over** this; it does not generate it. Supersedes the bare `migrations/*.sql` pointer in [database.md](database.md).

## Authoring rules

### Rollback symmetry

Every `Apply.sql` ships a paired `Rollback.sql` that inverts it — reverse dependency order, `IF EXISTS` + `CASCADE` so it is safe on partial state. The baseline pair (`001-baseline/{Apply,Rollback}.sql`) is the reference: `Apply.sql` creates `codes` → `routing_rules` → `scan_events`; `Rollback.sql` drops them in reverse with `DROP TABLE IF EXISTS … CASCADE`.

Rollback is a **dev/test affordance only** — it is never run in prod. It is still mandatory authoring (a missing rollback fails the scan), but see *Drift & orphans* for the prod stance.

### Reserved-word quoting

The migrator does **not** auto-quote identifiers (EF does; raw SQL does not). Hand-quote reserved words with double quotes:

```sql
"order"          integer     NOT NULL,
...
CREATE INDEX ix_routing_rules_code_id_order ON routing_rules (code_id, "order");
```

`routing_rules."order"` in the baseline is the canonical example.

### Ordinals are allocated at merge, never hand-authored

There is **one** authoring path and it never picks an ordinal:

1. New work lands as a flat `Dev/<utc-ts>_<slug>.sql` draft (no ordinal).
2. The ordinal is allocated **only** at promote/merge time, on the integration branch — `next = max(existing NNN) + 1`.

Two feature branches each adding a `Dev/` draft merge cleanly; neither computes an `NNN`, so they cannot collide. **Do not** hand-author a `Migrations/NNN-name/` folder on a feature branch — that is the exact collision `Dev/` exists to dodge.

### Idempotency mandate for `-- @no-transaction`

By default each migration runs inside a per-file transaction (Postgres transactional DDL) — a failed file leaves zero partial schema. For statements that forbid running in a transaction (`CREATE INDEX CONCURRENTLY`, `VACUUM`, native enum `ALTER TYPE … ADD VALUE`), opt out with the leading directive:

```sql
-- @no-transaction
CREATE INDEX CONCURRENTLY IF NOT EXISTS ix_codes_user_id ON codes (user_id);
```

The directive is `MigrationConventions.NoTransactionDirective` (`-- @no-transaction`), parsed into `MigrationDescriptor.NoTransaction`. A `@no-transaction` migration is recorded **separately** from its apply, so a crash between the DDL and the history insert **re-runs** the file on the next pass. Therefore `@no-transaction` Apply SQL **MUST be idempotent** — `IF NOT EXISTS`, guarded `DO $$ … $$` blocks. This is non-negotiable; the transactional path gives the crash-safety guarantee that `@no-transaction` forfeits.

### Native PG enums

Adding a value to a native Postgres enum is a migration: `ALTER TYPE foo_status ADD VALUE 'archived'`. `ADD VALUE` cannot run inside a transaction, so it is always a `-- @no-transaction` migration. (Enum **string**-mapping vs native-enum choice is in [enums.md](enums.md); this is only the migration mechanics.)

## Drift & orphans

| Term | What it is | Reaction |
|---|---|---|
| **Drift** | An already-applied migration's `Apply.sql` was edited after apply (disk checksum ≠ recorded `migration_history.checksum`). | Apply throws `MigrationDriftException`. **Prod: roll forward** — write a new migration. **Dev/test only: rollback the migration and re-apply, or `repair` to re-record the checksum.** |
| **Orphan** | `migration_history` has an applied row whose source file is gone (running binary older than the DB, or a folder was deleted). | Apply **fails closed** with `MigrationOrphanException`. Opt out with `MigrationOptions.AllowOrphanedHistory = true` only when intentionally running an older binary. |

Checksum is normalized (LF-only, trimmed) so whitespace/line-ending edits do not trip false drift; only real SQL edits do. Repair (`IMigrationRunnerService.RepairAsync`) and rollback (`RollbackAsync`) are gated by `MigrationOptions.AllowRollback` — keep it `false` in prod hosts; the engine throws if a destructive op is called while disabled.

> **Never edit an applied migration in prod.** Editing `Apply.sql` after it has run is drift by definition. Roll forward with a new ordinal.

## Registration & dual-ship

### `AddSqlMigrations(assembly)` — embed SQL in the PRODUCT assembly

Runtime hosts register the embedded source — the schema ships inside the binary, no filesystem dependency at deploy:

```csharp
// Pass the product assembly that embeds Migrations/NNN-name/*.sql
services.AddSqlMigrations(typeof(SomePersistenceMarker).Assembly);
```

The CLI / dev path registers the on-disk source instead (edit + apply live, no rebuild):

```csharp
services.AddSqlMigrations(migrationsRoot);   // "{Repo}.Persistence/Migrations"
```

Both overloads take an optional `Action<MigrationOptions>` to flip per-host flags (`AllowRollback`, `AllowOrphanedHistory`, `SchemaName`, `TableName`, `AdvisoryLockId`). Wired services: `IMigrationSource` (`EmbeddedResourceMigrationSource` or `FileSystemMigrationSource`), `IMigrationScanner` (`MigrationScannerService`), `IMigrationHistoryRepository`, `IMigrationRunnerService`.

### Dual-ship csproj

The same files ship two ways from one folder — embedded for runtime, on-disk for the CLI — with `Dev/` excluded from the binary:

```xml
<ItemGroup>
    <!-- Exclude Dev/ drafts: unpromoted SQL must never ship in the binary. -->
    <EmbeddedResource Include="Migrations\**\*.sql" Exclude="Migrations\Dev\**\*.sql">
        <LogicalName>Migrations/%(RecursiveDir)%(Filename)%(Extension)</LogicalName>
    </EmbeddedResource>
</ItemGroup>
```

- The `<LogicalName>` glob yields resource names like `Migrations/001-baseline/Apply.sql` — exactly what `EmbeddedResourceMigrationSource` parses (`folderPrefix = "Migrations/"`).
- The on-disk files stay in the repo for `FileSystemMigrationSource` (CLI + dev).
- The `Exclude` on `Migrations\Dev\**` is mandatory — drafts are runtime-ignored anyway, but must not be embedded.

## Apply triggers — dev auto vs prod explicit

| Host | When apply runs | `AllowRollback` |
|---|---|---|
| Dev (startup auto-apply) | On boot, **gated** to `IsDevelopment()` in the hosted-service adapter. | `false` (roll-forward even in dev hosts; rollback is a CLI op) |
| Prod | **Never auto on startup.** Explicit only — the CLI, or an init step / HTTP endpoint. | `false` (hard) |

`IMigrationRunnerService.ApplyPendingAsync(appliedBy, ct)` stamps each row's `applied_by` (`"startup"`, `"cli"`, `"endpoint"`). Apply is idempotent under the advisory lock — whichever host boots first applies; the rest no-op. Prod gates apply behind an explicit action so a deploy never silently mutates schema on boot.

## See also

- [database.md](database.md) — schema-first rule (this folder is its canonical schema) + EF-as-pure-mapper waste-rule
- [enums.md](enums.md) — native-PG-enum vs string mapping; `ALTER TYPE … ADD VALUE` becomes a `@no-transaction` migration here
- [data-access.md](data-access.md) — Dapper conventions for raw-SQL read paths over the migrated schema
- [tooling-cli.md](tooling-cli.md) — the `wow-migrate` CLI (`status` / `apply` / `rollback` / `new` / `promote` / `repair`) that drives `FileSystemMigrationSource`
- [testing.md](../testing/testing.md) — Testcontainers schema-conformance: apply → assert EF round-trips every entity; Respawn resets excluding `migration_history`
- SDK `wow-two-sdk.backend.beta` → `src/Data/Migrations/Sql/README.md` — engine internals (advisory lock, normalized checksum, host model, build-then-extract plan)

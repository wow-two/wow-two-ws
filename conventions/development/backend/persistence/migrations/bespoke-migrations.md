# SQL Migrator

*Last updated: 2026-06-16*

> Components, file layout, lifecycle of the bespoke-SQL migrator — the provider-agnostic engine that runs your `Apply.sql` / `Rollback.sql` verbatim.
> Purpose — own the schema as raw SQL the engine never rewrites, so per-provider correctness is explicit and EF maps over a schema it never generates.
> Use case — authoring migrations; reasoning over apply order, drift, rollback. SQL idioms → [migration-dialects.md](migration-dialects.md).

> Engine internals (advisory-lock id, normalized-checksum algorithm, `DbConnection`→`NpgsqlConnection` cast point, the three-host model) → SDK
> `src/Data/Migrations/Bespoke/bespoke.md`. This doc is the product-facing engine contract. SQL idioms (quoting, rollback, `@no-transaction`, native enums) →
> [migration-dialects.md](migration-dialects.md).

---

## File layout

One folder per migration, ordinal-prefixed, a raw `.sql` pair, under `{Repo}.Persistence/Migrations/`:

```
Migrations/
├── 001-baseline/{Apply,Rollback}.sql
├── 002-add-users-table/{Apply,Rollback}.sql
└── Dev/                       ← flat in-flight drafts, never embedded, never ordinal-named
    ├── .gitkeep
    └── 20260611T1030_add-service-column.sql
```

- Folder `NNN-name` → `MigrationConventions.FolderPattern()` (`^(\d{3})-(.+)$`) → `MigrationDescriptor.Ordinal` + `.Name`; `.Label` renders
  `NNN-name`.
- Fixed file names `Apply.sql` + `Rollback.sql` (`MigrationConventions.ApplyFileName` / `.RollbackFileName`).
- `Dev/` (`MigrationConventions.DevFolderName`) — flat editable drafts, both sections in one file; promoted at merge; never embedded, never read as a
  numbered migration.
- **`Migrations/*/Apply.sql` IS the schema-first canonical schema** — the owned `CREATE TABLE` truth, read before any model / query / EF config
  ([database.md](../database.md)). EF maps over it, never generates it.

---

## Ordinals — allocated at merge

Engine/file-layout concern, **not** dialect. Ordinals order the apply loop and gate what's applied.

- New work → flat `Dev/<utc-ts>_<slug>.sql`, **no ordinal**.
- Ordinal assigned **only** at promote/merge on the integration branch — `next = max(NNN) + 1` (or `001`).
- Two `Dev/` drafts on different branches merge cleanly. **Never** hand-create a `Migrations/NNN-name/` folder on a feature branch — that is the
  collision `Dev/` exists to dodge.
- `MigrationScannerService.Scan()` throws on a malformed folder or a duplicate ordinal.

---

## Components

The engine source depends only on a connection seam + `Npgsql` + `Dapper` + `ILogger` — zero domain / web / Hosting / CLI deps. All registered by
`AddDatabaseBespokeMigrations`.

- `IMigrationSource` / `FileSystemMigrationSource` · `EmbeddedResourceMigrationSource` — read the raw `.sql` pairs from disk (CLI/dev) or embedded
  resources (runtime); both return `RawMigration` and throw if a `Rollback.sql` is missing.
- `IMigrationScanner` / `MigrationScannerService` — parses `NNN-name`, computes the normalized checksum, returns `MigrationDescriptor`s ordered by
  ordinal.
- `MigrationDescriptor` — one validated migration: `Ordinal`, `Name`, `ApplySql`, `RollbackSql`, `Checksum`, `NoTransaction`, `Label`.
- `IMigrationHistoryRepository` / `MigrationHistoryRepository` — owns `migration_history`: `EnsureTableAsync`, `GetAppliedAsync`, `RecordAsync`,
  `RemoveAsync` (rollback), `UpdateChecksumAsync` (repair) + `AcquireLockAsync` / `ReleaseLockAsync`.
- `MigrationHistoryEntry` — one applied row: `Ordinal` (PK) · `Version` · `Name` · `Checksum` · `AppliedAt` · `AppliedBy` · `ExecutionMs`.
- `IMigrationRunnerService` / `MigrationRunnerService` — the host-facing engine: `ApplyPendingAsync`, `GetStatusAsync`, `RollbackAsync`,
  `RepairAsync`.
- `MigrationStatus` — snapshot: `Applied` · `Pending` · `Drifted` · `Orphaned`.
- `MigrationOptions` — per-host flags (below).
- `MigrationConventions` — file names, the `-- @no-transaction` directive, `Dev` folder name, `FolderPattern()`.

- `IMigrationRunnerService.ApplyPendingAsync(appliedBy, ct)` stamps `MigrationHistoryEntry.AppliedBy` with the host string (`"startup"` / `"cli"` /
  `"endpoint"`).
- `IMigrationDialect` / `PostgresMigrationDialect` is the engine's **internal** SQL seam (history DDL, advisory lock, `EnsureDatabaseExistsAsync`),
  selected by `MigrationOptions.Provider` (`DatabaseProvider`). It is **NOT author-facing** — authors write Apply/Rollback SQL
  ([migration-dialects.md](migration-dialects.md)); the dialect lives in the SDK `Bespoke/bespoke.md`.

---

## `MigrationOptions`

Set in code via the `AddDatabaseBespokeMigrations` configure hook; shared by every host.

- `AllowRollback` (default `false`) — gates `RollbackAsync` + `RepairAsync`. Off by default; enable **per-operation** for a guarded rollback/repair —
  **prod included** (recovery), paired with the CLI's target-DB confirm. Not an environment gate.
- `AllowOrphanedHistory` (default `false`) — tolerate applied rows with no source migration; keep `false` to fail closed when the binary predates the
  DB.
- `Provider` (default `Postgres`) — selects the `IMigrationDialect` (`DatabaseProvider`).
- `SchemaName` / `TableName` (default `public` / `migration_history`) — history-table location.
- `AdvisoryLockId` (default `4_855_178_001`) — canonical lock id; every host of one DB **must** share it or apply loops won't serialize.
- `Version` (default `v1.0`) — free label stamped onto applied rows; `Ordinal` is the gate.

---

## Engine-level rules

- **Verbatim SQL.** The engine runs your `Apply.sql` / `Rollback.sql` as written — no auto-quoting, no statement rewriting (unlike EF). Per-provider
  correctness is the author's job → [migration-dialects.md](migration-dialects.md).
- **`Rollback.sql` mandatory.** Every migration ships one — `FileSystemMigrationSource` / `EmbeddedResourceMigrationSource` throw at scan if it's
  missing. Rollback is a **guarded recovery op** (`RollbackAsync`, gated by `MigrationOptions.AllowRollback` + the CLI target-DB confirm): roll
  forward by default, but usable in **prod** when a forward-fix isn't viable (e.g. apply succeeded but the deploy is broken and reverting is fastest).
- **`-- @no-transaction` directive.** A leading `MigrationConventions.NoTransactionDirective` sets `MigrationDescriptor.NoTransaction` → the file runs
  outside a transaction and is **recorded separately** from its apply, so a crash mid-apply **re-runs the file** (its Apply SQL must therefore be
  idempotent). Default (no directive) = per-file transaction → a failed file leaves zero partial schema. Which statements force `@no-transaction` +
  the idempotency idioms → [migration-dialects.md](migration-dialects.md).

---

## Drift, orphans, checksum

- **Drift** — applied `Apply.sql` edited after apply (disk checksum ≠ `MigrationHistoryEntry.Checksum`). Reaction: `MigrationDriftException` (carries
  drifted `Label`s). Prod → roll forward (new migration). Dev → rollback+re-apply, or `RepairAsync` to re-record.
- **Orphan** — `migration_history` row whose source file is gone (older binary / deleted folder). Reaction: fails closed — `MigrationOrphanException`
  (carries the ordinals); opt out via `MigrationOptions.AllowOrphanedHistory` only for an intentional older binary.

- Checksum is SHA-256 over the **normalized** `Apply.sql` (CR/CRLF → LF, trailing whitespace trimmed) → whitespace/line-ending edits don't false-trip;
  only real SQL edits do. `Rollback.sql` and the `@no-transaction` flag are **excluded** (documented blind spot — see SDK `Bespoke/bespoke.md`).
- `RepairAsync` re-records drifted checksums to the disk value; `RollbackAsync` removes the latest row (or every row above `targetOrdinal`). Both
  gated by `MigrationOptions.AllowRollback` — the engine throws if either runs while disabled. **Never edit an applied migration in prod** — roll
  forward with a new ordinal.

---

## Apply triggers — dev auto vs prod explicit

| Host | When apply runs | `AllowRollback` |
|---|---|---|
| Dev | on boot, gated to `IsDevelopment()` in the hosted-service adapter | `false` |
| Prod | **never auto on boot** — CLI / init step / HTTP endpoint only | `false` for apply (rollback is separately, explicitly enabled) |

- Idempotent under the advisory lock — the first host applies, the rest no-op. Prod gates apply behind an explicit action so a deploy never silently
  mutates schema on boot.
- The CLI is the build-now host — `ApplyPendingAsync("cli", ct)` from its composition root ([migration-tooling.md](migration-tooling.md)).

---

## Registration & dual-ship

Two `AddDatabaseBespokeMigrations` overloads (`MigrationServiceCollectionExtensions`) wire the whole graph — source + dialect + `IMigrationScanner` +
`IMigrationHistoryRepository` + `IMigrationRunnerService`; an optional `Action<MigrationOptions>` flips per-host flags.

- **Runtime hosts** embed SQL in the product assembly (ships in the binary, no deploy-time filesystem):

```csharp
services.AddDatabaseBespokeMigrations(typeof(SomePersistenceMarker).Assembly);
```

- **CLI / dev** reads on-disk (edit + apply live, no rebuild):

```csharp
services.AddDatabaseBespokeMigrations(migrationsRoot);   // "{Repo}.Persistence/Migrations"
```

One folder ships **two ways** — embedded for runtime, on-disk for the CLI; `Dev/` excluded from the binary:

```xml
<EmbeddedResource Include="Migrations\**\*.sql" Exclude="Migrations\Dev\**\*.sql">
    <LogicalName>Migrations/%(RecursiveDir)%(Filename)%(Extension)</LogicalName>
</EmbeddedResource>
```

- `<LogicalName>` yields `Migrations/001-baseline/Apply.sql` — what `EmbeddedResourceMigrationSource` parses (`folderPrefix` defaults to
  `"Migrations/"`).
- The `Exclude` on `Migrations\Dev\**` is mandatory — drafts are runtime-ignored anyway; never embed them.

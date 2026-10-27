# Migrations — wow2 analysis

*Last updated: 2026-10-27 03:10 PM*

> How the wow2 ecosystem changes persistent state across releases: schema and data migrations, who owns, declares
> and runs them, and how products, standalone platform services and Wheelhouse itself share one model. Written before
> Wheelhouse builds its migrate rollout step, to find what the [migrate step spec](../wheelhouse-migrate-step-spec.md)
> misses; the spec is read, not edited. Analysis pool: settled points move to the conventions
> ([migrations](../../conventions/development/backend/dotnet/core/mla/domains/persistence/migrations/migrations.md),
> [deploy descriptor](../../conventions/deployment/descriptor/deploy-descriptor.md),
> [capability forms](../../conventions/development/capability-forms.md)), the be sdk backlog and Wheelhouse's backlog.

## Sources

| Short | Path under the hub |
|---|---|
| be sdk | `workbench/wow-two-sdk-beta/wow-two-sdk-beta.be/engineering/codebase/wow-two-sdk-beta-be/` |
| Wheelhouse | `workbench/wow-two-platform/wow-two-platform.wheelhouse/engineering/` |
| runner | Wheelhouse `codebase/wheelhouse.runner-services/` |
| Identity | `workbench/wow-two-sdk-beta/wow-two-sdk-beta.identity/engineering/` |
| Files | `workbench/wow-two-sdk-beta/wow-two-sdk-beta.files/engineering/` |
| ForeverPin | `workbench/maxs-projects/ventures/saas/10x-venture-forever-pin/engineering/` |
| Ocharo | `workbench/mfts-projects/ventures/ocharo-hq/ocharo-ws/workbench/` |
| ventures | `workbench/maxs-projects/ventures/` (`saas/`, `consumer/`, `labs/`) |
| Haven | ventures `saas/10x-ven-haven/engineering/codebase/haven.backend-services/` |
| clients | `workbench/maxs-projects/clients/` |
| pipelines | `workbench/wow-two-platform/wow-two-platform.pipelines/` |
| migration conventions | `conventions/development/backend/dotnet/core/mla/domains/persistence/migrations/` |

- read 2026-10-27; line numbers as of that read; `(U)` = read in code, not run.
- [Use cases](#use-cases) merge two read-only sweeps of 2026-10-27: every registry repository and the owner folders,
  47 with server-side state and 3 with browser storage only; the claims corrected below were re-read in the cited files.
- verified 2026-10-27 by a second read: about 80 claims re-read in the repositories and corrected in place; a real
  Wheelhouse rollback run of the same day is recorded under [Wheelhouse as an app](#wheelhouse-as-an-app) and S5.
- external practice is linked inline and collected in [Prior art](#prior-art).

---

## Developer questions (2026-10-27)

| # | Question | Short answer | Section | Points |
|---|---|---|---|---|
| 1 | What is a migration | a journaled change in one set: schema, reference data or a bounded backfill; up runs on deploy, down is a guarded tool; expand before contract | [Definitions](#definitions) | M1, M2, M20, M23 |
| 2 | How wow2 does it today | authoring, sets, local apply and tests are solid; deploy-time execution, data migrations, lock safety, compatibility and visibility are missing | [Current state](#current-state) | M10, M13 |
| 3 | Data migrations | small: a SQL file in the set; large or code-bound: a resumable SDK background migration that a later contract waits on | [Data migrations](#data-migrations) | M23–M26 |
| 4 | Several services | one database per product environment, one owner per set, every set migrated before any service restarts; B failing leaves A's expand harmless | [Multi-service products](#multi-service-products) | M6–M9, M14, M27, M28 |
| 5 | Standalone services | the instance product owns, versions and runs its sets; consumers depend on its contract version, never its tables | [Platform services and instances](#platform-services-and-instances) | M29–M34 |
| 6 | Platform apps vs products | one mechanism, stricter policy for platform apps | [One model](#one-model) | M12, M19 |
| 7 | Which cases occur in practice | 74 distinct cases across 50 repositories; most fit the model, and the misses are legacy mechanisms, package-owned DDL, seeds, imports, SQLite and the SDK spread | [Use cases](#use-cases) | M39–M56 |

---

## Verdict

- **The set is the unit of ownership.** A migration set (ordered SQL, one history table, one lock, optionally one
  schema) has exactly one owner; databases host sets and services host sets, and neither owns them.
- **One path for every deployed app.** Wheelhouse runs each release image's `migrate` in a one-off container after the
  pull and before the first wave, for products, Identity, Files and Wheelhouse itself; only a local run applies at boot.
  A product deployed by compose runs the same command as a one-shot service.
- **A set with history is the entry ticket.** `EnsureCreated`, hand DDL and tables a package creates for itself adopt
  into sets before their product takes the step; seeds join the step file by file, while imports, file stores and
  browser storage stay outside it.
- **Schemas stay one release backward compatible.** Migrations expand; a contract lands a release later in its own
  marked file that history records, so an older image boots on a newer schema and Wheelhouse checks a rollback before
  it runs. Down scripts never run on deploy; prod recovers forward or from the snapshot. Today an older image refuses
  any newer history, expand or not: a real Wheelhouse rollback failed on it on 2026-10-27 (S5).
- **Data by size.** Small backfills are SQL files in the set; large or code-bound ones are resumable SDK background
  migrations a later contract waits on; transfers across systems (Files imports, tenant and server moves, Identity
  takeover) are Wheelhouse "move" jobs, not migrations.
- **Platform services own their state.** An instance product (an Identity instance, a Files host) migrates its own sets
  in its own rollout; consumers depend on its contract version, never its tables; a Form 1 module's set rides the
  consumer's step.

---

## Current state

### SDK

| Piece | State | Evidence |
|---|---|---|
| bespoke engine: `NNN-name/{Apply,Rollback}.sql`, normalized checksum, drift and orphan refusal | stable since 2026-06 | be sdk `src/Data/Migrations/Bespoke/bespoke.md:7-22` |
| batch atomicity: consecutive transactional files commit as one unit; `-- @no-transaction` splits | shipped 2026-10-15 | `bespoke.md:24-42` |
| dry run: rehearses pending files under the lock, always rolls back | shipped; takes the same DDL locks | `bespoke.md:44-69` |
| named sets: own history, advisory lock, schema, `{{schema}}`, owner marker naming the instance | 10.0.81–10.0.82 | `bespoke.md:78-139` |
| level check: `Current` · `Behind` · `Ahead` · `Orphaned` · `Drifted` · `OwnerConflict` | shipped; anything but `Current` fails unless the set is `Warn` | `bespoke.md:141-155`, `MigrationSetServiceProviderExtensions.cs:107-108` |
| boot gate: a deployed boot verifies read-only, a local run applies, `ApplyWhenDeployed` opts back in | 10.0.82 | `src/Data/PostgresPersistenceStartupExtensions.cs:53-76` |
| `MigrateBespokeForDeployAsync`: creates databases, applies every set, returns a `Result` | shipped | `PostgresPersistenceStartupExtensions.cs:94-112` |
| baseline (mark as applied) | 10.0.82 | `bespoke.md:174-190` |
| `wow-migrate`: apply, check, baseline, rollback, repair; a sets manifest; PostgreSQL only | shipped | `bespoke.md:192-215` |
| `MigratorHarness`: one or several sets, PostgreSQL and SQLite | shipped | `src/Testing.Data/Migrations/MigratorHarness.cs:119-143` |
| EF and DbUp runners | shipped; startup hosted services | `src/Data/Migrations/migrations.md:9-17` |

Gaps:

- no lock safety: no `lock_timeout` or `statement_timeout` in the SDK, Wheelhouse or the conventions; the advisory lock
  waits without bound (`bespoke.md:826`, item 5 parked).
- apply refuses newer history: `ApplyPendingAsync` fails on any applied ordinal the source lacks
  (`MigrationRunnerService.cs:72`, `:721-741`) unless `AllowOrphanedHistory`; the level check calls the same case
  `Ahead` and fails too (`MigrationLevelReport.cs:73-74`), and its only relief, `LevelMismatch = Warn`, lets `Behind`
  and `Drifted` boot as well (`MigrationSetServiceProviderExtensions.cs:107-108`). Both refusals confirmed on a real
  Wheelhouse rollback, 2026-10-27 ([Wheelhouse as an app](#wheelhouse-as-an-app)).
- no migration kind: history records nothing about expand vs contract, so neither an older image nor Wheelhouse can
  tell a safe `Ahead` from an unsafe one.
- no data-migration primitive: no batched or background migration, no progress journal, no gate a contract can wait on.
- no exit-code helper: each image maps the `Result` to `0`/`1`/`2` itself (Identity
  `service/Identity.Api/Configurations/HostConfiguration.cs:59-80`).
- stale doc: `bespoke.md:411-426` shows an `applied_by` CHECK of `startup|endpoint|cli`; the code has `varchar(60)` and
  no CHECK (`PostgresMigrationDialect.cs:54-63`) and writes `deploy` and `baseline`.
- adoption: 35 of 37 backend solutions pin 10.0.71–10.0.81, before the boot gate — 10.0.71: Ocharo's 7, the canary,
  the product template; 10.0.72: ForeverPin, Pose Coach; 10.0.74: 20 ventures; 10.0.75: Matinee; 10.0.77: the domain
  template; 10.0.80: Wheelhouse; 10.0.81: Harvest. Only Files (10.0.84, back to boot apply through
  `ApplyWhenDeployed`) and Identity (10.0.86) are past 10.0.82; core is at 10.0.87. 5 more solutions stay on the
  pre-rename `WoW2.Sdk.Backend.Beta` (TBS 10.0.45, tnis-mintrans 10.0.21, HomeAtlas and med-text-fab 10.0.63,
  secrets-vault 10.0.56) and reach the gate only through the rename. Each bump turns a bespoke boot that applied into
  one that refuses a pending set, whatever deploys the product; EF-run and `EnsureCreated` boots sit outside the gate
  (U) (M48).

### Conventions

| Rule | Where |
|---|---|
| one strategy per owned database; bespoke by default, EF or DbUp allowed | `migrations.md:9-13` |
| production applies through an explicit deployment action, not at startup | `migrations.md:22` |
| one applicant per database unless the runner's lock is verified | `migrations.md:31-35` |
| `Rollback.sql` always; a real inverse or an explicit no-op; Apply → Rollback → Apply tested | `sql/bespoke-migrations.md:29-39` |
| exits `0` · `1` refused · `2` failed or guard; destructive operations need `--i-understand-this-is` | `sql/migration-tooling.md:39-59` |
| applied rows stamped with the product version | `development/repo/versioning/versioning.md:31` |
| a Form 1 consumer owns module tables; a Form 2/3 service owns its database | `development/capability-forms.md:71-72` |
| one role and one database per product environment | `deployment/servers/server-lifecycle.md:80` |
| a failed schema change recovers forward or by restore; an image rollback never undoes a migration | `server-lifecycle.md:99` |
| no shim or data-preserving migration for users who do not exist | `development/breaking-changes.md:14`, `:21` |
| changed services restart in dependency waves; a failure stops later waves | `deployment/descriptor/deploy-descriptor.md:281-285` |
| Wheelhouse fills the connection key from the target's database for `needs: [postgres]` | `deploy-descriptor.md:298` |

Gaps:

- no rule for data migrations, expand and contract, lock timeouts or the deploy step's image contract.
- the bespoke convention predates sets: nothing on set naming, schema ownership, owner instance, level check or baseline.
- `capability-forms.md:71-72` still says per database; Identity Q54 confirmed ownership per schema
  (Identity `research/identity-analysis-2026-10/t10-schema-migrations.md:302`).
- the descriptor has no migrate key; `dependsOn` is the only ordering, and Ocharo uses it to sequence a boot migration.
- nothing says which of several services sharing a set runs it; in practice Haven gives the job to a dedicated
  `database` service (M44), and Desk applies at boot while `jobs` waits.

### Pipelines

- the release manifest carries `rollbackCompatible`, false by default (pipelines `generator/release.py:713`, `:754`); no
  `migrations` or `migrate` key.
- Wheelhouse already reads an optional `migrations: bool` from a bundle (runner `transport.py:264-270`,
  `release_sets.py:208-211`) and flags changed `Migrations/` paths in changelogs (`artifacts.py:468`); the generator
  never sets it, so it reads null.

### Wheelhouse as deployer

| Piece | State | Evidence |
|---|---|---|
| steps: render, check, snapshot (prod), pull, waves, verify, publish, probe, dev check | built | Wheelhouse `deployment/deployment.md:703-723` |
| prod snapshot before the pull: `pg_dump` per database, volume tars, newest 5 kept; restore by hand | built | `deployment.md:956-975` |
| one-off container from a release image (`verify_release`) | built; no settings, no secrets, 512 MB | runner `runner.py:2006-2045` |
| roll back to the previous release when the bundle or the target promises compatibility | built; fails across a migration today (S5) | `runner.py:1970-1973` |
| one deployment per target | built | `runner.py:1493` |
| migrate rollout step | v0.7 Iteration 6, spec only | `planning/version-track/v0.7/v0.7.md:32-37` |
| dry run before a rollout; dry run without long locks | backlog | `planning/backlog.md:108`, `:113` |
| recover migrations across services when a later one fails | open decision | `backlog.md:134` |
| contract migrations under decision 65; extract the expand-only lint to the be sdk | backlog | `backlog.md:94`, `:223`, `:237` |
| refresh dev's database from a redacted prod copy | backlog | `backlog.md:123` |

### Wheelhouse as an app

- applies its own set at every boot (`codebase/wheelhouse.backend-services/Wheelhouse.Api/Program.cs:16`) on be sdk
  10.0.80 (`Directory.Packages.props:4`), before the boot gate.
- decision 65: migrations only expand, a contract takes two releases (`research/platform-ideation.md:77`); enforced
  from ordinal 031 by a regex lint with a `-- contract:` exemption (`Wheelhouse.Tests.Migrations/Tests/ExpandOnlyTests.cs`).
- the runner rolls a failed self-promotion back on that promise (`deployment.md:149`, `:184-185`).
- gap, confirmed by a run on 2026-10-27: the previous image refuses the newer release's ordinals, so a rollback across
  a migration fails to boot, and both `deployment.md` lines are false today.
  - v0.7.2 (be sdk 10.0.80) booted on a throwaway database v0.7.3 had migrated (`033`, an `ADD COLUMN IF NOT EXISTS …
    NOT NULL DEFAULT`) and aborted in `MigrateBespokeOnStartupAsync` before any SQL: "History holds applied migrations
    absent from the source: 033." (`MigrationRunnerService.cs:72`; `AllowOrphanedHistory` is unset).
  - the schema did not block v0.7.2; only the history check did.
  - on be sdk 10.0.87 the same apply call fails alike; `VerifyMigrationLevelsOnStartupAsync` fails by default
    ("database at 033 is newer than the code (032)") and boots only with `LevelMismatch = Warn`.
  - the runner's automatic restore after a failed probe hits the same refusal.
  - workarounds that worked: deleting `033`'s history row (v0.7.2 boots; the re-upgrade re-applies the idempotent
    `033`), or building with `AllowOrphanedHistory = true`, a code-only option in 10.0.80 (M16, M19).
- gap: a bump past 10.0.82 makes its deployed boot verify-only; its self-deploy and `deployment/vps/self-deploy.py` then
  need the step, or the first release with a migration fails to boot.
- the built-in vault (decision 59) lives in Wheelhouse's own set, schema `vault` beside `public`
  (`Wheelhouse.Persistence/Migrations/030-built-in-vault/Apply.sql`).

### Products

| Product | Shape | Today |
|---|---|---|
| ForeverPin | `management` and `redirect` over one set (`ForeverPin.Persistence/Migrations`) and one database (`deployment/deploy.yml:36-80`) | both hosts apply the set at boot (`ForeverPin.Api/Configurations/HostConfiguration.cs:56`, `ForeverPin.Redirect.Api/Configurations/HostConfiguration.cs:41`), be sdk 10.0.72; the advisory lock serializes two applicants |
| Ocharo | one product `ocharo` of 4 repositories and 9 services: `desk`, `jobs`, `image-worker`, `brand`, `catalogue` (platform) · `marketing`, `blog` · `studio` · `motion` (assets); only Desk and `jobs` share a database (PostgreSQL, 7 schemas); 6 more services keep SQLite on their own volumes; 4 mechanisms; all 7 solutions on be sdk 10.0.71 | Desk: a bespoke set applied at boot by its own loop (`ocharo-platform/…/BrandWorkspace.Api/Configurations/HostConfiguration.Extensions.cs:452-470`) plus `--migrate` (`:480`); `jobs` waits through `dependsOn: [desk]` (`ocharo-platform/engineering/deployment/deploy.yml:64`). Marketing: the EF runner at boot (`ocharo-marketing/…/OcharoMarketing.Api/Configurations/HostConfiguration.Extensions.cs:90-91`). Brand, Catalogue, Blog, Motion: `EnsureCreated`; Catalogue, Blog and Studio add hand `CREATE TABLE IF NOT EXISTS` and `pragma_table_info` guards |
| Haven | 5 .NET services (`auth`, `supply`, `location`, `settings`, `database`) with 5 `DbContext`s over one PostgreSQL database and one set; compose on a VPS, no `deploy.yml` | only `database` applies, when `Schema:ApplyOnStartup` (`Haven.Database.Infrastructure/Startup/BackgroundServices/SchemaStartupService.cs:18`), then applies 12 JSON seeds; it also serves apply, rollback (behind `AllowRollback`), status and seed endpoints; v1.1 converted v1.0's `migration_history` (`LegacyJournalRepository.cs`); be sdk 10.0.74 |
| Hijinx | one service, SQLite rooms database | the EF runner runs only in Development (`Hijinx.Api/Configurations/HostConfiguration.Extensions.cs:39-43`); production has no apply step ("backlog", `engineering/deployment/deployment.md:30`) |
| templates | product and domain templates | boot only (`Sample.Api/Configurations/HostConfiguration.cs:40` and `:35`); no `migrate` command |

- gap: a deploy-time command exists only in Identity (`migrate`), Desk (`--migrate`) and TNIS
  (`Tnis.Ingestion.Cli migrate`); Haven applies from one service behind a flag, every other product applies at boot,
  and Hijinx applies nowhere in production. TNIS's command calls the boot helper (`MigrateCommand.cs:34`), so past
  10.0.82 it verifies instead of applying.
- gap: Ocharo runs four mechanisms in one product — bespoke on PostgreSQL, EF on SQLite, `EnsureCreated`, hand additive
  DDL; the last two keep no history, so neither a bespoke step nor `--check` sees them. 8 swept services have no
  history at all ([Use cases](#use-cases), M46).
- facts: no Ocharo `deploy.yml` declares an Identity instance or a Files host. Desk hosts ASP.NET Identity's tables in
  its own schema `access` (`Migrations/002-access`, EF-generated DDL frozen into its set) beside Telegram and SSO
  tables (`009`, `010`); media sits in Desk's `bytea` columns and in SQLite `MediaStore` copies in Brand, Catalogue and
  Blog. The Identity instance (2026-10-21) and the shared Files host (2026-10-26) are decisions
  ([platform apps](../../docs/platform-apps.md) § Decisions), not declarations.

### Platform services

- Identity: a SQL set in `Identity.Module`, embedded per dialect, own schema, owner `module` or `service`
  (`codebase/identity.backend-services/packages/Module/Core/IdentityDatabaseServiceCollectionExtensions.cs:63-75`);
  the image's `migrate` maps exits `0`/`1`/`2` (`service/Identity.Api/Program.cs:16-17`, `HostConfiguration.cs:59-80`).
  Decided: SQL set (Q47), sets per host (Q48), never one schema for two instances (Q53), ownership per schema (Q54),
  explicit migrate step (Q57) (`research/identity-analysis-2026-10/identity-analysis-2026-10.md:129-139`); one
  Wheelhouse product per instance with its own database (Q5 · B,
  [identity instances](../identity-instances-2026-10/identity-instances-2026-10.md) § Two owners' instances).
- Files: one image; instance A per owner, shared host B with tenants as rows (Files
  `research/files-analysis-2026-10/t1-services-tenancy.md:34-55`). Its "Wheelhouse migration module" moves bytes and
  metadata between stores and instances, and the product's own migration writes `file_id` from an id map
  (`t9-wheelhouse-migration.md:32-41`, `:84-99`; [platform apps](../../docs/platform-apps.md) § Decisions, 2026-10-26).
- gap: Files' set is a default set in SQLite only, registered by the service host
  (`service/Files.Api/Configurations/HostConfiguration.Extensions.cs:35`), not by the Module; a Form 1 consumer on
  PostgreSQL has no Files schema path, and the set would share `migration_history` with the consumer's own default set
  (M40). Its deployed boot applies through `ApplyWhenDeployed` (`HostConfiguration.cs:40`).
- Harvest: a named set `harvest` in PostgreSQL only, tables prefixed rather than schema'd; its own boot helper
  (`service/Harvest.Api/Configurations/HostConfiguration.cs:38`) probes encoding and `pg_trgm`, applies, probes again,
  and is not deploy-gated; `001` creates the extension and monthly partitions that a job must extend; `002` drops
  columns and deletes rows, a contract (M41).
- Secrets Vault: merged into Wheelhouse (decision 59); its schema rides Wheelhouse's set.
- gap: nothing says who runs an instance's migrations across many instances, or how a consumer states the service
  version it needs.

---

## Model

### Definitions

| Term | Means | Lives in | Runs |
|---|---|---|---|
| set | ordered SQL + one history table + one advisory lock, optionally one owned schema | the owner's assembly, embedded | the migrate step |
| schema migration | DDL in a set | `Migrations/NNN-name/Apply.sql` | the migrate step |
| reference-data migration | rows the code needs in every environment: lookup values, enum tables | the set, as idempotent upserts | the migrate step |
| backfill | DML over existing rows, bounded: seconds on prod-size data | its own file in the set | the migrate step |
| background migration | batched, resumable DML or code over large data | the owner's code; its journal in the set's schema | the new release's job worker |
| move | data crossing a system boundary: Files import, tenant or server move, takeover | the owning service's CLI + a Wheelhouse job | an operator job, never inside a rollout |
| seed | per-environment data: first admin, OIDC clients, test personas | configuration or a host CLI | boot or operator |
| seed file | rows the repository ships with an owner per file: `upsert` (the file wins) or `insert` (the runtime owns the row once it exists) | the owner's assembly, journalled | the migrate step, after the sets (M51) |
| import | data from outside the release: a bundle, a private folder, another store; derived tables rebuilt from sources | the owning image's CLI, with `--dry-run` | an operator job (M52) |

- up is `Apply.sql`; down is `Rollback.sql`.
- expand: a change the previous release survives — a new table, a nullable column, a column with a constant default,
  an index built `CONCURRENTLY`, an enum label the previous release can read, a constraint `NOT VALID` that its writes
  already satisfy (new rows are still checked,
  [ALTER TABLE](https://www.postgresql.org/docs/current/sql-altertable.html)), a widened type.
- contract: a change the previous release may not survive — a drop, a rename, a narrowed type, `SET NOT NULL`, rows
  deleted or rewritten that old code reads.
- level: a set's highest applied ordinal. Rollback floor: the oldest release that can run on the current level.

Rules:

- must express every persistent-state change the code depends on as a migration in exactly one set.
- must keep `Rollback.sql` and run it only locally, in tests, or as a guarded operator action; a deploy never runs it
  (M2).
- must not put a seed, an import or a move in a set (M26, M33, M52).
- out of scope: files on volumes and keys (M42), and browser or device storage (M54).

---

### Ownership

| Owner | Example | Set | Schema | Marker |
|---|---|---|---|---|
| product | ForeverPin | the default set | `public` | none |
| module (Form 1) | `Identity.Module` inside a product | a named set | `identity` | `module`, the product's instance |
| service instance (Forms 2/3) | the wow2 Identity instance, Files host B | named sets | its own | `service`, the instance |

- must give every set exactly one owner: one repository and the assembly that embeds it (M3).
- must give module and service sets a named PostgreSQL schema; a product's default set may stay in `public` (M4).
- must not reach another set's tables by foreign key, view or query; reference by id, such as `sub` or a file id (M5).
- must keep one database per product environment (`<product>_{env}`), holding the product's sets and its Form 1
  modules' sets; an instance product gets its own (M6).
- may share a set's Persistence assembly and `DbContext` across the services of one repository; must not map a set
  another repository owns (M7).
- should give the step its own connection key, so an owner role (DDL) and a runtime role (DML) can split later without
  a contract change (M8); EF's guidance is the same
  ([applying migrations](https://learn.microsoft.com/en-us/ef/core/managing-schemas/migrations/applying)).
- tenants stay rows inside the owner's set; a schema or database per tenant waits for the SDK (M55).
- why the set: a service may host several sets (a product with `Identity.Module`), and a set may be hosted by several
  services (ForeverPin's two images), so only the set has one owner.

---

### Declaration

A repository declares three things:

1. its sets, in code — `AddDatabaseBespokeMigrations` / `AddDatabaseBespokeMigrationSet`, or the EF or DbUp runner —
   with SQL under `Migrations/NNN-name/`, embedded in the image.
2. a `migrate` command in every image that hosts a set: the be sdk helper, so `app migrate` applies every registered
   set and `app migrate --check` reports levels and compatibility read-only (M10).
3. in `deploy.yml`, a product-level `migrate:` list: which service's image runs the step, its command and timeout
   (M9).

```yaml
migrate:                                      # sketch for the decision, not a spec
  - service: management                       # its release image hosts every set this repository owns
    command: [dotnet, ForeverPin.Api.dll, migrate]
    timeout: 10m
```

- must declare one item per hosting image, normally one per repository, even when several services read the set.
- must keep one exit contract for bespoke, EF and DbUp sets (M11).
- must allocate an ordinal once and never reuse it; a pending ordinal below the applied level refuses on deploy (M56).
- should let the generator derive the bundle's existing `migrations` fact from the key, so changelogs and release facts
  read one source.

---

### Execution

| Situation | What runs | Where | Connects as |
|---|---|---|---|
| local run (`Development`, no `DEPLOY_ENVIRONMENT`) | boot applies every set | the app process | the local default |
| tests | `MigratorHarness`, `RelationalTestDb` | the test process | Testcontainers or SQLite |
| forward deploy, dev and prod | `migrate` from the new image | a one-off container after the pull, before the first wave | the migrate key |
| rollback, or an older release | `migrate --check` from the older image; refuse when incompatible | a one-off container, read-only | the migrate key |
| deployed boot | the level check, read-only; a compatible `Ahead` warns | the service | the service's settings |
| background migration | the new release's job worker, in batches | the service owning the job | the service's settings |
| move, takeover, baseline, down script | the owning image's CLI | an operator job: typed confirmation, audited | the migrate key or a move token |

- must run every declared step on every forward deploy; a current set exits `0` in seconds (M13).
- must run all steps after the pull and before the first wave: repository order, then descriptor order; any failure
  stops the job before any restart (M14).
- must gate a rollback with the older image's `--check`: proceed on current or a compatible `Ahead`, refuse otherwise
  and name the snapshot (M15).
- must keep a deployed boot read-only (M16).
- must bound waiting: the migrator sets `lock_timeout` per batch (a few seconds), retries the batch a bounded number
  of times, bounds the advisory-lock wait, and exits `3` "busy" when it gives up; the runner may retry once (M17).
- must take the prod snapshot before the step (exists) and trust the dev run for rehearsal in v1 (M18).
- must hold the target's deployment lock for the whole job and each set's advisory lock for its run (both exist).
- the container facts in the spec stand — release image, `--pull never`, platform network, the service's volumes,
  memory limit, dropped capabilities — except the settings source (M8).

---

### One model

- every app that deploys through Wheelhouse takes the same step: products, Identity instances, Files hosts and
  Wheelhouse (M12). Policy differs, mechanism does not:

| Policy | Platform apps | Products |
|---|---|---|
| expand only | always; lint in CI | by default; a contract in the same release is allowed while the product has no external users, and that release is not rollback-compatible |
| rollback | promised (`rollbackCompatible` on the target) | when the bundle says so |
| prod promotion | the owner, typed confirmation | the product's policy |
| break-glass | `self-deploy.py` runs `migrate` too | none |

- Wheelhouse replaces itself: the detached runner job runs the step, so the console going away runs nothing;
  `self-deploy.py` must run the new image's `migrate` before the swap (M19).
- interim: Wheelhouse may set `ApplyWhenDeployed` for its SDK bump only, removed once its own step ships, together with
  `AllowOrphanedHistory` until M21 records kinds; without it an older Wheelhouse refuses the newer history (S5).

---

### Expand and contract

The step runs the new schema under the old release for its duration, and under an older release after a rollback;
expanding keeps both safe ([parallel change](https://martinfowler.com/bliki/ParallelChange.html),
[evolutionary database design](https://martinfowler.com/articles/evodb.html)).

| Change | Release N | N+1 | N+2 |
|---|---|---|---|
| remove a column | code stops reading and writing it | contract `since=N` | — |
| rename or reshape | expand and backfill; code writes both, reads the new | code stops writing the old | contract `since=N+1` |
| make a column required | add it nullable and backfill; code always writes it | `CHECK … NOT VALID`, `VALIDATE`, `SET NOT NULL` as a contract `since=N` | — |

- must mark a contract file `-- @contract since=vX.Y`, naming the oldest release that no longer reads or writes what it
  removes; the migrator records kind and `since` in history (M21).
- must keep a contract in its own file (the rule exists for data-destroying steps, `sql/bespoke-migrations.md:33`).
- compatibility: release R may run on a set when every applied ordinal above R's level is an expand, or a contract with
  `since ≤ R`. The older image's `--check` and its boot both evaluate it (M15, M16).
- a product without external users may contract in the same release as the change; the bundle then says
  `rollbackCompatible: false` and the snapshot is the recovery (M20, `breaking-changes.md:14`).
- lint: Wheelhouse's `ExpandOnlyTests` moves to `Testing.Data` as a helper every repository runs, with lock-risk rules
  beside it: `CREATE INDEX` without `CONCURRENTLY` on an existing table, `ADD CONSTRAINT` without `NOT VALID`,
  `ALTER COLUMN … TYPE`, a volatile default (M22; [strong_migrations](https://github.com/ankane/strong_migrations),
  [Atlas analyzers](https://atlasgo.io/lint/analyzers)).

---

### Data migrations

- small: an idempotent SQL file in the set (`WHERE new_column IS NULL`), after the expand it needs, seconds on prod-size
  data; must not share a file with DDL, because a batch holds every earlier lock until it commits (`bespoke.md:75`)
  (M23).
- large or code-bound: an SDK background migration (M24):
  - registered by name in the owner's code and run by the be sdk `Jobs/` worker once the release that adds it is live;
  - walks a key range in batches, commits per batch and keeps a cursor in `{schema}.background_migrations`, so a crash
    or a redeploy resumes;
  - idempotent per batch; throttled by batch size, pause and `lock_timeout`;
  - states `queued` · `running` · `paused` · `finished` · `failed`, readable through `migrate --check`.
- SQL or code: SQL when set-based SQL expresses it; code when it needs application keys (Identity's plaintext TOTP keys
  becoming encrypted, T10), external input (Files' id map) or per-row logic.
- order: expand (step) → release N live → background migration → a later release's contract declaring
  `-- @requires <name>`; `migrate` refuses that contract with exit `1` until the background migration finished (M25).
  GitLab gates the same dependence, but its finalize helper runs the remaining batches inline
  ([batched background migrations](https://docs.gitlab.com/development/database/batched_background_migrations/)).
- reference data: idempotent upserts in the set; per-environment seeds (first admin, OIDC clients) through
  configuration or a host CLI (M26).
- moves: Files imports ([T9](https://github.com/wow-two-sdk-beta/wow-two-sdk-beta.files/blob/main/engineering/research/files-analysis-2026-10/t9-wheelhouse-migration.md)),
  tenant moves, server moves and an Identity takeover are Wheelhouse jobs with their own plan, freeze, cutover and
  verify; a product change that consumes a move's output (the id map → `file_id`) is a background migration that the
  cutover release starts (M33).

---

### Multi-service products

- facts: one database per product environment; every `needs: [postgres]` service gets the same connection key
  (`deploy-descriptor.md:298`); a product may span repositories (decision 70, `deploy-descriptor.md:243-271`).
- must keep one set per repository by default; a second set only for a module or a planned split.
- must let the services of one repository share the set's Persistence assembly, and declare its step once.
- must not share a set across repositories; their services talk through APIs, as Ocharo Studio reads Desk's sign-in
  tickets through Desk.
- must run every step of a release set before its first wave: repositories in cross-repository `dependsOn` order, then
  descriptor order (M28).
- B fails after A applied: nothing restarted, A's migrations are expand so the running release keeps working, the job
  fails, B fixes forward and the redeploy finds A current. No cross-set rollback (M27; closes `backlog.md:134`).
- `dependsOn` stops sequencing migrations (Ocharo's `jobs`) and keeps only runtime readiness.
- ForeverPin under the model: one item on `management`; both hosts verify at boot; `redirect` never meets a pending set,
  because the step ran before either wave.
- Haven under the model: one item on the `database` image; the four other services verify; its startup flag stays for
  local runs, and its HTTP apply and rollback give way to read-only status and operator actions (M44).
- Ocharo under the model: one item per image that holds state — `desk`, `brand`, `catalogue`, `marketing`, `blog`,
  `studio`, `motion` — each in its own repository's `deploy.yml`; `jobs` and `image-worker` declare none; the five on
  `EnsureCreated` or hand DDL adopt a set first (M43, M46).
- prior art: [database per service](https://microservices.io/patterns/data/database-per-service.html) wants private
  tables per service; here the private unit is the set's schema, and the private database is the instance product's.

---

### Platform services and instances

| Case | Declares | Owns and versions | Runs | Consumer depends on |
|---|---|---|---|---|
| Form 1 module in a product | the module's registration in the product host | the module repository; the level follows the product's package pin | the product's `migrate` (every registered set) | the in-process contract |
| Form 2 instance per owner (wow2 Identity; Ocharo's Identity, decided 2026-10-21 and declared nowhere yet) | the service repository's `deploy.yml` | the service repository; the instance's release | the instance product's rollout | the HTTP contract and its version |
| Form 3 shared host (Files B; Ocharo starts here, decided 2026-10-26 and declared nowhere yet) | the same | the same | the host's own rollout, once for every tenant | the same |
| takeover (Form 1 → instance) | — | ownership moves by an audited `claim` | an operator job | — |

- each instance product has its own database and pace (Q5 · B); a new service release reaches instances one product at
  a time, and a fleet roll-out over the same step can come later (M29).
- a Form 1 module's set runs inside the product's step: `MigrateBespokeForDeployAsync` already applies every set (M30).
- the service must keep serving the previous client contract version, proven by running the previous client's
  conformance suite against the new image (`capability-forms.md:40`; the domain repository's compat job) (M31).
- a product release should declare the platform services it calls and the minimum contract version (`requires:`), and
  Wheelhouse should refuse a deploy onto an environment whose bound instance is older (M32).
- a shared host upgrades once for every tenant; no tenant pins it back.
- Files' Wheelhouse migration module is a move job: it shares the runner's one-off container and step journal, not the
  migrate step (M33).
- down scripts, repair, baseline and `claim` are operator actions on the image's CLI with the existing target guards
  (`sql/migration-tooling.md:51-59`) (M34).

---

### Rollback and safety

| Failure | State after | Recovery |
|---|---|---|
| a script fails | its batch rolled back; earlier batches and sets committed, all expand | fix forward, redeploy |
| a `-- @no-transaction` file fails midway | partial and unrecorded | idempotent rerun (existing rule) |
| a lock is not acquired | nothing applied | the runner retries once, then fails "busy" |
| the step times out | container stopped; the open batch rolls back when its session ends | inspect, redeploy |
| the new release is unhealthy after the step | schema expanded | the runner restores the previous images, which boot on a compatible `Ahead` |
| a contract was wrong | data lost | restore the prod snapshot by hand (`deployment.md:956-975`) or a backup |
| a dev schema change must be undone | — | the guarded `rollback` operator action |

Layers, outermost first: expand-only rule, marker and lint (M20–M22) · `lock_timeout` and retries (M17) · batch
transactions (exist) · prod snapshot before the step (exists) · dry run on dev (exists; prod later, M18) · rollback
check (M15) · level check at boot (exists, M16).

---

### Observability

- job record: per step `status` (`applied` · `current` · `refused` · `failed` · `busy` · `timed out`), `exitCode`,
  `seconds`; per set from `migrate-result`: name, level before and after, applied labels with kind, rollback floor,
  background migrations pending, lock waits (M37).
- product page: per environment and set: level, newest label and when, rollback floor, background progress, last check;
  "check now" runs `migrate --check` read-only (M36, M38).
- rollout: one row per set, "Migrate identity: 1 applied (002-oidc) in 3s".
- Wheelhouse keeps no second history table; the database's history stays the authority.
- operator actions are audited commands, like every other mutation.

---

### Testing

| Layer | Test | Where | State |
|---|---|---|---|
| set | Apply → Rollback → Apply, idempotency, drift | the migrations tier on `MigratorHarness` | exists |
| set | expand-only and lock-risk lint | a `Testing.Data` helper | Wheelhouse only today |
| host with several sets | apply all, owner conflicts | `MigratorHarness.CreatePostgres(sets)` | exists |
| image | `migrate` exits `0`/`1`/`2`/`3` and the `migrate-result` line | each product's E2E tier | new |
| upgrade | N-1 schema and seed → apply N → N-1 smoke on the new schema | the rehearsal rig, platform apps first | new (M35) |
| background migration | crash mid-run, resume, idempotent rerun | be sdk tests | new |
| runner | step placement, `--check` on rollback, failures before any restart | runner unit tests and the rig | spec |

---

## Use cases

Every distinct case the two sweeps of 2026-10-27 found, deduplicated: 18 wow2 repositories, 29 venture, client and
Ocharo repositories with server state, 3 with browser storage only. "Pilots" are the ten SQLite SaaS pilots
(`retainer-balance`, `documentation-checker`, `file-watch`, `procedure-review`, `training-seats`, `epub-review`,
`customer-promises`, `vendor-renewals`, `config-checker`, `podcast-readiness`): a product database and an identity
database each. Each case names the point that decides it.

| Use case | Repositories | How the model handles it | Points |
|---|---|---|---|
| **Schema ownership** | | | |
| U1 — a product owns its schema as SQL in a default set; EF only maps | Wheelhouse, canary, both templates, ForeverPin, Desk, Haven, TranscriptForge, TNIS, TBS, Sift, Arcade, ListingShelf, Matinee, PbnStudio, 8 pilots | the product's default set in `public` | M3, M4 |
| U2 — a domain package ships its set in a NuGet and applies it into the consumer's database (Form 1) | Identity and Harvest Modules (named sets); Files (a default set the service host registers) | a named set with the `module` marker; the product's step applies every registered set; Files moves to a named set first | M4, M30, M40 |
| U3 — one domain in three forms; the owner marker refuses a second claimant | Identity (built); Files, Harvest (designed) | the instance product owns its sets; the marker names the instance | M29–M31 |
| U4 — two owners' sets in one database, each with its own history and lock | Identity, Harvest (a keyed data source beside the host's) | named sets; table prefixes where SQLite has no schemas | M3, M4 |
| U5 — one set owning several schemas | Desk (7 schemas), Wheelhouse (`vault` by `CREATE SCHEMA` in its default set) | allowed: a schema belongs to the set that creates it; a second owner needs a named set | M3, M4 |
| U6 — a package's DDL outside the product's set | Hangfire's self-created `hangfire` (TranscriptForge, Desk); SDK idempotency `EnsureTableAsync`; outbox, inbox and webhook DDL copied by consumers (ForeverPin `012`); ASP.NET Identity DDL frozen into Desk `002-access` and the pilots' EF `InitialAccess` | the package ships a named set; Hangfire's installer runs in the step | M39 |
| U7 — one logical schema in two SQL dialects | Identity (parity tests); Files SQLite only; Harvest PostgreSQL only | a set per dialect for domain packages | M40 |
| U8 — references across stores by id, never by key | Harvest captures across partitions checked in code; Studio and the other apps reach Desk through tickets | ids only | M5 |
| U9 — tenants as rows | Desk `organization_id` with composite keys; Files and Harvest tenant tables; the pilots, one workspace per account | rows inside the owner's set | M3 |
| U10 — a schema or database per tenant | be sdk `Tenancy/PerSchema`, `PerDb` (empty folders) | deferred until the SDK builds it | M55 |
| **Mechanisms** | | | |
| U11 — a bespoke set on PostgreSQL | Wheelhouse, canary, Harvest, ForeverPin, Desk, Haven, TranscriptForge, TNIS, TBS | the step's native case | M10 |
| U12 — a bespoke set on a SQLite volume | Identity, Files, both templates, Sift, Arcade, ListingShelf, Matinee, PbnStudio, 8 pilots | the step with the service's volume; one applicant per file | M49 |
| U13 — EF migrations | at boot: Marketing, the pilots' identity databases, two pilots' product databases, YPD, the kb `jobs` sample; Development only: Hijinx; never applied: 6 other kb samples | one helper over bespoke, EF and DbUp | M11 |
| U14 — `EnsureCreated`, no history | Brand, Catalogue, Blog, Motion, HomeAtlas, tnis-mintrans | adopt into a set | M46 |
| U15 — hand additive DDL behind `IF NOT EXISTS` or `pragma_table_info` | Catalogue, Studio, Blog; nasiya (about 33 guarded `ALTER TABLE`s) | adopt into a set | M46 |
| U16 — several mechanisms in one product | Ocharo (four); the pilots (a bespoke or EF product database beside an EF identity database); YPD (EF and Django) | each image runs its own `migrate`; the ones without history adopt first | M11, M43, M46 |
| U17 — stacks other than .NET | nasiya (Python: SQLAlchemy `create_all`, raw `sqlite3`, Alembic abandoned); YPD's Django service | a language-neutral image contract | M45 |
| U18 — adopting a store created before its migrator | ListingShelf (idempotent `001`, later drops the "pre-migrator schema ledger"); Haven (converts v1.0's `migration_history`); Sift (renames the file to avoid it) | an idempotent first file or SDK `baseline`; one journal converter in the SDK | M34, M46 |
| U19 — dev scripts beside the set | `Migrations/Dev/` in ForeverPin, TranscriptForge, TNIS, TBS; `wow-migrate new` and `promote` | only promoted files reach the step | M56 |
| U20 — template residue in the baseline | `greeting_logs` in PbnStudio and tnis-mintrans; dropped by Arcade, ListingShelf and Files `005` | a drop file; templates ship no sample table | M56 |
| **Data and seed** | | | |
| U21 — re-encoding, folding and renumbering rows in SQL | Wheelhouse `002`, `006`–`015`, `025`; ForeverPin `004`, `013`; Haven `003`; ListingShelf `002` | a small backfill in its own file | M23 |
| U22 — reshape and backfill, then a constraint | ForeverPin `006`; TranscriptForge `004`; Haven `002` | expand, backfill, contract | M20, M23 |
| U23 — expand and contract in one file | TranscriptForge `003` (add, backfill, drop) | allowed for products without external users; not rollback-compatible | M20, M21 |
| U24 — destructive "the database is resettable" migrations | ForeverPin `007`–`010`; Arcade `002`; Harvest `002`; Wheelhouse `013`, `015` (before its lint cutoff) | a contract; the lint starts at a cutoff ordinal | M20, M22 |
| U25 — a nullable column without backfill; old and new formats side by side | TranscriptForge `008`, `012`; TNIS `003`; ListingShelf compresses only new captures | a pure expand | M20 |
| U26 — derived columns the database maintains | Haven's trigger-kept `listing_phones`; ListingShelf's FTS5 triggers; both with a backfill | DDL and backfill in the set | M23 |
| U27 — a backfill that keeps a new feature from misfiring | Haven `005` marks old listings alerted | a small backfill | M23 |
| U28 — derived tables rebuilt from sources, never migrated | TNIS and TBS `004`, `005` (`POST /api/interchange/ingest`, `/api/traffic/ingest`) | the table in the set; its rows by an import | M52 |
| U29 — long-running or resumable work | TranscriptForge's Hangfire recovery; ListingShelf's run queue; Matinee's scan workers; Files' planned dual write | a background migration on the jobs worker | M24, M25 |
| U30 — reference rows in SQL | Wheelhouse `007`, `010` (product rows, default workspace); Desk `001` (`schema_version` row); Sift `003` (singleton settings) | idempotent upserts in the set | M26 |
| U31 — seed files with an owner per file | Haven: 12 JSON files, `upsert` or `insert`, journalled, after the sets | per-file mode in the step | M51 |
| U32 — seeds from configuration at startup | Identity's OIDC clients; Files' default tenant; Harvest's operator key | per-environment configuration | M26 |
| U33 — seeds from a file or folder at boot | HomeAtlas (when empty); Marketing's bundle every boot; Brand and Catalogue seed roots absent on hosts; YPD's code seeds | seed files in the step, or an import | M51, M52 |
| U34 — host CLI imports with `--dry-run` | Desk `--import-sourcing`, `--import-events`, `--provision-operator` | operator jobs | M52 |
| U35 — one-time adoption from another store | Desk's `LegacyCommerceReader` (SQLite pilots into PostgreSQL, with source hashes); Wheelhouse `vault import --from-db` (key re-wrap) | an import; a move when it crosses systems | M33, M52 |
| **Multi-service** | | | |
| U36 — several services over one set, each applying at boot | ForeverPin (`management`, `redirect`; a test boots a second host) | one item; both verify | M7, M9 |
| U37 — one service applies, another refuses a missing schema | Desk applies; `jobs` waits by `dependsOn` | the step before the waves; `dependsOn` for readiness only | M14, M28 |
| U38 — a dedicated schema service | Haven `database` (5 `DbContext`s; flag-gated apply; apply, rollback and seed endpoints) | its image runs the step; the endpoints turn read-only | M44 |
| U39 — a product of several repositories | Ocharo: 4 repositories, 9 services, 7 holding state, 1 shared database | one item per image that holds state; cross-repository order | M28, M43 |
| U40 — products calling each other over HTTP | Haven → ListingShelf; Marketing, Blog → Catalogue, Brand; Studio → Desk | a contract version, no shared tables | M31, M32 |
| U41 — a vendored library served by another service's tables | `Ocharo.Sso` (4 copies) against Desk's `access.sso_*` | through Desk's API only | M5 |
| **Platform services and instances** | | | |
| U42 — a platform service as its own product | Identity (`migrate` with exits), Files, Harvest, Wheelhouse | the instance product's rollout | M12, M29 |
| U43 — planned platform moves | Ocharo Identity (Desk accounts, memberships, `telegram_links`); Ocharo onto the shared Files host (Desk `bytea`, 3 `MediaStore` copies, Marketing blobs); Events (`008-events` by bundle import) | moves, not migrations | M33 |
| U44 — databases placed by Wheelhouse (`needs: [postgres]`) | Wheelhouse, canary, Harvest, ForeverPin, Desk, `jobs` | a role and a database per product environment; a migrate key | M6, M8 |
| U45 — a hosted external database | 10x-fin-nt (Supabase, planned) | the image's step if declared; no Wheelhouse snapshot | M6, M18 |
| U46 — Wheelhouse as subject and orchestrator | Wheelhouse (boot apply on 10.0.80, expand-only from `031`) | the step in its self-deploy and `self-deploy.py` | M19 |
| **Deploy and rollback** | | | |
| U47 — boot apply on a pin below the gate | 35 of 37 solutions; 5 more on the pre-rename package, among them TBS (sync-over-async) and secrets-vault (unawaited, inside DI registration) | the step first, then the bump or the rename | M48 |
| U48 — a deployed boot that opts back into apply | Files `ApplyWhenDeployed` | interim; removed with the step | M19, M47 |
| U49 — an explicit command beside the boot | Identity `migrate` (exits `0`/`1`/`2`), Desk `--migrate`, TNIS's CLI (on the boot helper, so verify-only past the gate) | the be sdk helper | M10, M47 |
| U50 — apply only in Development | Hijinx | a `migrate` command and the step | M47 |
| U51 — deployed outside Wheelhouse | Haven, ListingShelf, TranscriptForge, secrets-vault (compose); TNIS, TBS (no deploy) | the same command as a compose one-shot | M47 |
| U52 — expand-only with rollback onto the newer schema | Wheelhouse decision 65 (`ExpandOnlyTests`, self-promotion rollback) | the `--check` gate and the contract marker | M15, M16, M21 |
| U53 — an upgrade with dump-and-restore rollback | Haven v1.0 → v1.1 | the snapshot recovers a release that is not rollback-compatible | M18, M20 |
| U54 — backups outside the migrator | Haven's `backup` service; `SqliteBackupWriter` in config-checker and podcast-readiness; Wheelhouse's prod snapshot | the snapshot before the step; product backups stay theirs | M18 |
| U55 — down scripts as operator actions | every bespoke set; Haven's HTTP rollback behind `AllowRollback`; Desk's CLI never enables rollback | a guarded operator action | M2, M34, M44 |
| U56 — applicants and locks | the SDK lock (FNV-1a of the set name); Desk's own key; app-level `pg_advisory_xact_lock` in the same key space; SQLite's single applicant; Files' one process per store | bounded waits; a reserved key class | M17, M50 |
| U57 — ordinals with gaps | Wheelhouse (`014`, `019`–`021`, `023`–`024`, `028`–`029` never committed) | allowed; an ordinal is never reused; a late lower ordinal refuses on deploy | M56 |
| U58 — releases that prove deploy flows | wheelhouse-canary (`002` additive on purpose) | the rehearsal rig | M35 |
| **Non-relational state** | | | |
| U59 — SQLite, single instance by design | about 28 services | the step beside the writer | M49 |
| U60 — rows and bytes outside the database kept consistent | Files blobs; Brand, Catalogue, Blog and Marketing `blobs/`; ListingShelf photos by SHA-256; HomeAtlas media | the snapshot pairs the dump with volume tars; a layout change is a background migration | M24, M42 |
| U61 — media as `bytea` | Desk (size CHECKs) | rows; leaving for Files is a move | M33, M42 |
| U62 — keys outside the database | DataProtection volumes (ForeverPin, Desk, the pilots); Wheelhouse's vault root key; secrets-vault's master key; Identity's ring (database planned, Q26) | never migrated; re-keying is an operator job | M42 |
| U63 — pinned models and downloaded data | `image-worker` `/models` (md5), ForeverPin `geo` | provisioned, not migrated | M42 |
| U64 — rows a migration must not rewrite | Wheelhouse `audit_entries` (a trigger refuses UPDATE and DELETE; hash chain); vault canary rows; secrets-vault payloads; HomeAtlas originals | the trigger enforces it; re-keying is an import | M42, M52 |
| U65 — partitions kept by a function | Harvest's monthly `harvest_captures` and `harvest_ensure_capture_partitions` | DDL in the set; upkeep by the owner's job | M41 |
| U66 — extension and encoding preflight | Harvest (`pg_trgm`, UTF-8, a Cyrillic probe) | placement creates the extension; `migrate` preflights | M41 |
| U67 — a document in one row | HomeAtlas `AtlasSnapshot` (JSON with a `Revision`) | adopt the table; the JSON shape migrates in code, like client storage | M46, M54 |
| U68 — state shipped in the repository or held on devices | ocharo-assets (Git LFS library), TNIS's baked payload, Matinee's device files | outside the step: it ships in the image or lives on devices | M42, M54 |
| **Client-side state** | | | |
| U69 — versioned browser storage | fe sdk `VersionedStore` and IndexedDB `upgrade`; PRISM `migrateModel` and import-time migrators; Surface Pattern refuses an unreadable key; Whiteout presets drop on clear | out of the step, in the fe sdk | M54 |
| U70 — device data synced with the server | Arcade (device books joined with cloud books); Hijinx (playlist export and import); Studio (SQLite plus browser storage) | the server half in a set, the device half in the fe sdk; the sync payload versions like an API | M31, M54 |
| **Tests** | | | |
| U71 — a dedicated migrations tier | ForeverPin (a second host proves an idempotent boot), Sift, Matinee, Arcade, PbnStudio, Identity (dialect parity), Files, Harvest, Wheelhouse, canary, templates | Apply → Rollback → Apply on `MigratorHarness` | M53 |
| U72 — migration checks inside other tiers, or none | ListingShelf, the pilots (integration, unit); Desk, Haven, TranscriptForge, TNIS (E2E fixtures only) | a required tier once the step runs | M53 |
| U73 — an expand-only lint | Wheelhouse `ExpandOnlyTests` (`-- contract:`, cutoff `030`) | the `Testing.Data` helper | M22 |
| U74 — a second schema source in tests | `RelationalTestDb` on `EnsureCreated`; `NoOpBespokeMigratorExtensions` | unit tiers only; SQL tiers run the set | M53 |

---

## Prior art

| Practice | Source | wow2 takes |
|---|---|---|
| expand, migrate, contract | [parallel change](https://martinfowler.com/bliki/ParallelChange.html) | expand-only with marked contracts |
| drop a column over releases; post-deployment migrations | [GitLab: avoiding downtime](https://docs.gitlab.com/development/database/avoiding_downtime_in_migrations/) | contract a release later, `since` marker |
| batched background migrations, finalize before depending | [GitLab: batched background migrations](https://docs.gitlab.com/development/database/batched_background_migrations/) | SDK background migration, `@requires` gate |
| checks for unsafe operations | [strong_migrations](https://github.com/ankane/strong_migrations), [Atlas analyzers](https://atlasgo.io/lint/analyzers) | a lint helper in `Testing.Data` |
| a migration job from the release image before the rollout | [Kubernetes Jobs](https://kubernetes.io/docs/concepts/workloads/controllers/job/), [Helm pre-upgrade hooks](https://helm.sh/docs/topics/charts_hooks/), [EF bundles](https://learn.microsoft.com/en-us/ef/core/managing-schemas/migrations/applying) | a one-off container from the release image |
| a deploy identity with DDL, a runtime identity without | [EF: applying migrations](https://learn.microsoft.com/en-us/ef/core/managing-schemas/migrations/applying) | a separate migrate key now, roles later |
| baseline an existing database | [Flyway baseline migrations](https://documentation.red-gate.com/fd/baseline-migrations-273973336.html) | `BaselineAsync` (exists) |
| tagged rollback | [Liquibase rollback](https://docs.liquibase.com/commands/rollback/rollback.html) | down scripts as operator actions only |
| dependencies on another project's change | [Sqitch changes](https://sqitch.org/docs/manual/sqitchchanges/) | none: sets do not depend on each other |
| data migrations beside schema ones | [Django data migrations](https://docs.djangoproject.com/en/stable/topics/migrations/#data-migrations) | small backfills as SQL files in the set |
| online migrations through dual writes | [Stripe](https://stripe.com/blog/online-migrations) | the reshape sequence above |
| lock waits and the lock queue | [PostgreSQL `lock_timeout`](https://www.postgresql.org/docs/current/runtime-config-client.html), [explicit locking](https://www.postgresql.org/docs/current/explicit-locking.html) | migrator `lock_timeout` and retries |
| private data per service | [database per service](https://microservices.io/patterns/data/database-per-service.html) | a schema per set, a database per instance product |

---

## Points

Parent before child; a child names its parent. Each point: the decision, its options, the pick and why.

### Definitions

- [ ] M1 — Words for the three kinds of change: one word "migration" for all · "migration" and "move" · "migration",
  "background migration" and "move" → three words; Files' "migration module" copies bytes across systems for hours
  with a freeze and a cutover, which shares nothing with a schema step but the container runner.
- [ ] M2 — Down scripts: keep `Rollback.sql` mandatory, never run by a deploy · optional for expand-only files · drop
  them → keep; Apply → Rollback → Apply catches non-idempotent SQL and dev needs the undo, while prod recovers forward
  or from the snapshot (`server-lifecycle.md:99`).

### Ownership

- [ ] M3 — Unit of ownership: the set · the service · the database → the set; a service may host several sets and a set
  may be hosted by several services, so only the set has exactly one owner.
- [ ] M4 (M3) — Schemas: every set in its own schema, products included · named schemas for module and service sets,
  product default sets stay in `public` · `public` for all with table prefixes → named schemas for module and service
  sets; isolation where two owners share a database, and no churn for the products already on a default set.
- [ ] M5 (M3) — References across sets: foreign keys allowed · ids only, no key, view or query across sets · read-only
  views the owner publishes → ids only; a foreign key ties two owners' migration order and blocks the referenced
  set's contracts (T10's side tables keyed by `sub` already follow it).
- [ ] M6 — Database topology: one database per product environment with a schema per set (today) · one database per
  service · one per repository → one per product environment, and an instance product gets its own; placement,
  snapshots and settings already work that way, and isolation comes from instance products (Q5 · B).
- [ ] M7 (M6) — `DbContext` across a product's services: share the set's Persistence assembly within a repository · a
  context per service over its own set · any repository maps any set → share within a repository, never map another
  repository's set; the mapper follows the set's owner.
- [ ] M8 (M6) — Credentials for the step: the service's settings file and role (spec) · a separate migrate connection
  key, the same role in v1 · owner and runtime roles now → a separate key with the same role, roles split once a
  product has external users or a takeover needs schema grants; the key keeps least privilege open without a
  contract change.
- [ ] M39 (M3) — DDL a package owns (Hangfire's `hangfire` schema; the SDK idempotency, outbox, inbox and webhook
  tables; ASP.NET Identity's tables): the package creates its tables at runtime (Hangfire at every boot; the
  idempotency store's opt-in `EnsureTableAsync`) ·
  consumers copy the DDL into their own set (ForeverPin `012`, Desk `002-access`, the pilots' `InitialAccess`) · the
  package ships a named set that the product's step applies → a named set per package, and Hangfire, which versions its
  own storage, runs its installer in the step; a runtime create needs DDL rights at every boot and escapes the level
  check, and a copy freezes a schema the package keeps changing.
- [ ] M40 (M4) — Dialects: one dialect per set, the author's choice · a set per supported dialect with the same ordinals
  and a parity test (Identity) · one portable SQL for both → a set per dialect for domain packages, one dialect for
  products; Identity proves the parity test, and Files' SQLite-only default set leaves a PostgreSQL consumer no schema
  path.
- [ ] M41 (M8) — Server prerequisites (Harvest's `pg_trgm`, encoding and Cyrillic probes; partitions a function must
  extend): the set creates extensions itself (today) · Wheelhouse's database placement creates allowed extensions, and
  `migrate` preflights and refuses with exit `1` · a boot probe only → the set creates trusted extensions, placement
  the untrusted ones, and `migrate` preflights; `pg_trgm` is trusted, so the role Wheelhouse makes the database's owner
  (`prepare.py:59-60`) installs it, while an untrusted one needs a superuser
  ([CREATE EXTENSION](https://www.postgresql.org/docs/current/sql-createextension.html)), and a refusal before any
  restart beats a boot that fails after one. Partition upkeep stays the owner's job, never a migration.
- [ ] M42 (M6) — State outside the database (blob volumes, key rings, model and geo volumes) and rows no migration may
  rewrite (hash-chained audit, encrypted payloads): the step migrates files too · outside the step: the snapshot pairs
  the dump with volume tars (exists), a file layout change is a background migration (M24), and keys change only by an
  operator job → outside the step; no swept repository migrates files, its stores are content-addressed or append-only,
  and Wheelhouse's `vault import` already re-keys as a job.
- [ ] M55 (M4) — Tenants by schema or database (be sdk `Tenancy/PerSchema` and `PerDb`, empty folders; no repository
  uses either): settle it now · defer until the SDK builds them · rule them out → defer; every swept tenant is a row
  (Desk, Files, Harvest, the pilots), and named sets with `{{schema}}` and an owner marker are the likely seam.

### Declaration

- [ ] M9 — Where the step is declared: `services.<name>.migrate` (spec) · a product-level `migrate:` list naming image,
  command and timeout · inferred from images that register sets → a product-level list, one item per hosting image; the
  step belongs to sets rather than to one service's wave, and one declaration ends ForeverPin's two applicants.
- [ ] M10 — Image contract: the be sdk helper (`app migrate`, `app migrate --check`) with exits `0`/`1`/`2` and a
  `migrate-result` line · a `wow-migrate` CLI image · each product's own code → the helper, plus `--check` and exit `3`
  "busy" (M17), and the templates gain the command; the image already embeds the SQL and binds the settings.
- [ ] M11 (M10) — Strategies under the step: bespoke only, EF and DbUp products convert · one helper for all three under
  one exit contract · a command per strategy → one helper for all three; the conventions allow three strategies
  (`migrations.md:9-12`), and Ocharo Marketing, Hijinx and the pilots' identity databases run EF on SQLite.
- [ ] M43 (M9) — Items in a product of several repositories and images (Ocharo: 4 repositories, 9 services, 7 holding
  state): one item per repository · one item per image that holds a set, in that repository's `deploy.yml` · one list
  in the hub → one per image; Ocharo's platform repository builds three images with stores of their own (`desk`,
  `brand`, `catalogue`), and the release set merges the items in M28's order.
- [ ] M44 (M9) — A dedicated schema service (Haven's `database`: five `DbContext`s over one set; apply behind a flag;
  apply, rollback, status and seed endpoints): keep apply and rollback over HTTP · its image declares the step, its
  status and seed views stay read-only, and rollback becomes an operator action (M34) · fold its DDL into each service
  → the second; it already is the one owner M3 asks for, and an HTTP rollback on prod is the down script M2 keeps out
  of deploys.
- [ ] M45 (M10) — Images on other stacks (nasiya on Python, YPD's Django service): .NET only · a language-neutral image
  contract (exits `0`–`3`, the `migrate-result` line) with the be sdk helper for .NET · a contract per stack → the
  language-neutral contract; it costs nothing, and neither product deploys through Wheelhouse yet.
- [ ] M46 (M11) — Mechanisms without history (`EnsureCreated`, hand additive DDL, an abandoned Alembic, a foreign
  `migration_history`): leave them at boot, outside the step · adopt each into a set — an idempotent `001-baseline`
  (`IF NOT EXISTS`, as ListingShelf did) or SDK `baseline`, and Haven's `LegacyJournalRepository` turned into one SDK
  converter · rename the store and start fresh (Sift) → adopt before the product's first deploy with the step; without
  history neither `--check` nor the rollback gate can read a schema, and 8 swept services have none. EF migrations stay
  under M11.
- [ ] M56 (M10) — A pending ordinal below the applied level (lanes on one branch allocate ordinals in parallel; the
  engine applies every unapplied ordinal in any order, `MigrationRunnerService.cs:77-78`): apply it (today) · refuse it
  outside a local run, so its author renumbers above the level · renumber by hand at merge only → refuse on deploy;
  such a file runs on a schema its author never tested, and a rollback to a release above it meets an orphan below
  its level, which M21's rule does not classify. Settled beside it: an ordinal is never reused and gaps stay
  (Wheelhouse); `Dev/` scripts reach a set only through `wow-migrate promote`; the templates' baseline ships no sample
  table (U20, S17).

### Expand and contract

- [ ] M20 — Who must expand only: Wheelhouse (decision 65) · every platform app, while products may contract in the same
  release when they have no external users, marking it not rollback-compatible · every set everywhere → the middle;
  platform apps promise rollback, and `breaking-changes.md:14` spares products shims for users who do not exist.
- [ ] M21 (M20) — Recording a contract: a lint-only `-- contract:` comment (Wheelhouse) · the migrator parses
  `-- @contract since=vX.Y` and records kind and `since` in history · nothing → record it; an older image's boot and
  Wheelhouse's rollback check then read compatibility from the database alone.
- [ ] M22 (M20) — The lint: Wheelhouse's `ExpandOnlyTests` · a `Testing.Data` helper with expand-only and lock-risk
  rules · an external linter (Squawk, Atlas) → the SDK helper (`backlog.md:237`); one rule set, no new toolchain.

### Execution

- [ ] M12 — Platform apps and products: one mechanism, stricter policy for platform apps · two models · platform apps
  keep boot apply → one mechanism; Wheelhouse, Identity and Files deploy through the same runner, and their differences
  (always rollback-compatible, lint in CI, owner-only promotion) are policy.
- [ ] M13 — When the step runs: only when the declaring image changed (spec) · on every forward deploy · when the bundle
  says migrations changed → every forward deploy; a current set exits in seconds, and a restore or a hand repair can
  leave a set behind with no image change.
- [ ] M14 — Place in the rollout: each step before its own service's wave (spec bullet) · every step after the pull and
  before the first wave · expand before the waves, contract after the last → every step before the first wave; with
  expand-only the running release keeps working, and a failure never leaves a product half restarted.
- [ ] M15 — Rollback and older releases: skip the step (spec) · run `--check` from the older image and refuse an
  incompatible schema · run down scripts → the `--check` gate; it turns decision 65's promise into a checked fact and
  names the snapshot when the answer is no.
- [ ] M16 — An older image on newer history, in a deployed boot's level check and on the apply path interim boots still
  run (pins below 10.0.82, `ApplyWhenDeployed`): refuse anything but current (SDK today) · tolerate every `Ahead`
  (spec; `AllowOrphanedHistory` and `LevelMismatch = Warn` do it today, the second also letting `Behind` and `Drifted`
  boot) · tolerate `Ahead` only when compatible (M21), on both paths → only when compatible, on both paths; an older
  image boots after a rollback, but never on a schema a contract narrowed under it. Refusing already broke a real
  Wheelhouse rollback onto an expand-only `033` (S5). Until M21 records kinds, a set that lints expand-only may set
  `AllowOrphanedHistory`, plus `LevelMismatch = Warn` once past 10.0.82.
- [ ] M17 — Lock safety: none (today) · migrator defaults: `lock_timeout` per batch, bounded retries, a bounded
  advisory-lock wait, exit `3` when it gives up · `SET LOCAL` by each author → migrator defaults with a per-file
  override; an `ALTER TABLE` queued behind a long transaction blocks every reader of that table, so the step must fail
  fast and retry rather than stall the app.
- [ ] M18 — Prod rehearsal: trust the dev run and the snapshot · a dry run against prod before promoting · rehearse on a
  redacted prod copy in dev → trust dev and the snapshot in v1, then rehearse on the dev refresh once `backlog.md:123`
  ships; a prod dry run takes the same locks as the real run (`bespoke.md:64`).
- [ ] M19 (M12, M16) — Wheelhouse itself: boot apply forever through `ApplyWhenDeployed` · the step in its self-deploy
  and in `self-deploy.py` · boot apply only while it bumps past 10.0.82, then the step → the third, with
  `AllowOrphanedHistory` on its set from the next release (M16); Wheelhouse is the first platform app on the step,
  break-glass must not rest on boot behaviour the SDK removed, and without the flag its rollback fails (S5). A rollback
  to a release built before the flag still needs the history-row workaround.
- [ ] M47 (M16) — Apply paths beside the step (Hijinx's Development-only EF runner, Haven's `Schema:ApplyOnStartup`,
  Files' `ApplyWhenDeployed`, Desk's `--migrate`, TNIS's CLI, products deployed by compose): each product keeps its own
  · one `migrate` command per image, run by Wheelhouse as the step and by compose as a one-shot service the app waits
  on (`depends_on: service_completed_successfully`), with every boot flag removed → one command; Hijinx shows a
  Development-only path leaves production with none, and a compose host past 10.0.82 verifies like any deployed boot
  (`IsLocalRun` is Development without `DEPLOY_ENVIRONMENT`), as does TNIS's CLI, which calls the boot helper
  (`MigrateCommand.cs:34`).
- [ ] M48 (M12) — The SDK spread (35 of 37 solutions below 10.0.82): bump everyone now · per product, in one release:
  its `migrate` command, its step, then the bump · stay below the gate until forced → per product, the step first,
  in this order: Wheelhouse (M19), the canary (rig), Identity and Files (dropping `ApplyWhenDeployed`), Harvest,
  ForeverPin and Ocharo, then each venture at its next release, the 5 on the pre-rename package taking the rename in
  that release; a bump alone turns a boot that applied into one that refuses.
- [ ] M49 (M14) — SQLite sets in the step (about 28 single-instance services): migrate beside the running writer
  (spec) · stop the writer for the step · copy, migrate and swap the file → beside the writer, bounded by M17; the
  batch runs in `BEGIN IMMEDIATE` and holds the write lock until it commits (`bespoke.md:76`), so the old release's
  writes wait out `busy_timeout` and an expand keeps its rows readable. The dialect demands one applicant per file
  (`bespoke.md:10`), so the old release must verify at boot rather than apply (M48).
- [ ] M50 (M17) — Advisory lock keys: one bigint space shared by the migrator (FNV-1a of the set name), Desk's own key
  and the SDK's app-level `pg_advisory_xact_lock` (`Data/EntityFrameworkCore/Locks/Extensions/TransactionLockExtensions.cs:51`)
  · the migrator moves to the two-key form under a reserved class → the reserved class; PostgreSQL keeps the two key
  spaces apart, so no app lock can hold the step until its timeout, at the cost of one SDK change.

### Data migrations

- [ ] M23 — Small data changes: an idempotent SQL file of its own in the set · mixed into the DDL file · application
  code at boot → its own SQL file, seconds on prod-size data; under batch scope a long data file holds every earlier
  lock (`bespoke.md:75`).
- [ ] M24 — Large or code-bound data changes: an SDK background migration (named, batched, resumable, journaled in the
  set's schema, run by `Jobs/`) · each product's own job · scripts by hand → the SDK primitive, built in the migrations
  vector pass after the step; GitLab solved the same problem this way, and every product needs one implementation.
- [ ] M25 (M24) — A contract that needs a finished backfill: `-- @requires <name>`, refused by `migrate` with exit `1`
  until finished · the step first finishes the remaining batches inline (GitLab's
  `ensure_batched_background_migration_is_finished`) · a convention only → the refusal; nothing may depend on a
  background migration before it finishes, and an inline remainder of unknown size runs under the step's timeout.
- [ ] M26 — Reference data and seeds: reference rows as upserts in the set, per-environment seeds through configuration
  or a host CLI · everything in sets · everything at boot → the split; a migration runs the same in every environment,
  and a first admin or an OIDC client differs per environment.
- [ ] M51 (M26) — Seed files the repository ships: every one an upsert in the set (M26) · a file per table with a mode,
  `upsert` (the file wins) or `insert` (the runtime owns the row once it exists), journalled and applied by the step
  after the sets, as Haven does · an import at every boot (Marketing's bundle) → per-file modes in the step; an upsert
  overwrites what the owner edited in the app, and a boot import repeats its work on every start. Per-environment and
  secret values stay configuration (M26).

### Multi-service products

- [ ] M27 — B fails after A migrated (`backlog.md:134`): roll A back · keep every migration expand and migrate
  everything before any restart · restart first, migrate after → the second; nothing restarted, A's expand is harmless
  to the running release, and B fixes forward.
- [ ] M28 — Step order across a release set's repositories: cross-repository `dependsOn`, then descriptor order · an
  explicit `after:` per item · unordered → `dependsOn`, then descriptor order; M5 bans dependencies between sets, so
  order rarely matters and needs no new key.

### Platform services and instances

- [ ] M29 — Who runs a standalone service's migrations: the instance product's own rollout · each consumer product's
  rollout · one fleet job across instances → the instance product; Q5 · B gives each instance its own product,
  database and pace, and a fleet roll-out can come later over the same step.
- [ ] M30 — A Form 1 module's set: the product's `migrate` applies every registered set (today) · a declared step per
  module · boot → the product's step; `MigrateBespokeForDeployAsync` already applies every set, the module repository
  authors it and the product's package pin sets its level.
- [ ] M31 — Product ↔ service compatibility: lockstep upgrades · the service keeps the previous client contract version,
  proven by the previous client's conformance suite · no promise → the previous version; a shared host upgrades once
  for every tenant, and none can hold it back.
- [ ] M32 (M31) — A product's minimum service version: none · `requires:` in `deploy.yml`, checked by Wheelhouse
  against the bound instance · checked at the product's boot → `requires:` checked by Wheelhouse, later; it fails a
  deploy before any restart instead of a request after one.
- [ ] M33 — Moves (Files' migration module, tenant and server moves): a separate Wheelhouse job type sharing the one-off
  container and step journal · part of the migrate step · the service's CLI by hand only → a separate job type; moves
  run for hours across hosts with a freeze and a cutover, and their product-side change is a background migration.
- [ ] M34 — Operator actions (down script, repair, baseline, claim): Wheelhouse jobs running the image's CLI, typed and
  audited · `wow-migrate` by hand · not offered → by hand now, Wheelhouse jobs later; the CLI already carries the
  target guards, and a takeover needs `claim` first (T10).
- [ ] M52 (M33) — Imports, adoptions and rebuilds (Desk's `--import-sourcing`, `--import-events` and
  `--provision-operator`; `LegacyCommerceReader` from SQLite into PostgreSQL; `vault import --from-db`; TNIS's derived
  tables): inside a migration · operator jobs that run the owning image's CLI with `--dry-run`, audited, beside M34's
  actions · at boot → operator jobs; their input lives outside the release (a bundle, a private folder, another
  store), so they cannot run alike in every environment, and Desk already ships the CLI shape.

### Testing

- [ ] M35 — Compatibility testing: lint only · lint plus an upgrade smoke for platform apps on the rehearsal rig (N-1
  schema and seed, apply N, N-1 smoke) · the full N-1 suite on the N schema everywhere → lint plus the platform-app
  smoke; it catches what a regex cannot, at a cost one rig absorbs.
- [ ] M53 (M35) — A migrations tier per repository: optional (Desk, Haven, TranscriptForge and TNIS have none) ·
  required for every set the step runs, stamped by the templates → required; the step trusts Apply → Rollback →
  Apply, and unit tiers on `EnsureCreated` (`RelationalTestDb`) never run a set's SQL.

### Client-side state

- [ ] M54 — Browser and device storage (the fe sdk's `VersionedStore` and IndexedDB `upgrade`; PRISM's migrators;
  Surface Pattern's refusal; Arcade's device books): inside the migration model · outside it: client data migrates on
  read through the fe sdk, every persisted key behind `VersionedStore`, and a sync endpoint versions its payload like
  any API (M31) → outside; the data lives on devices no rollout reaches and outlives every release.

### Observability and Wheelhouse UI

- [ ] M36 — Where Wheelhouse reads schema state: job history only (spec) · history plus an on-demand read-only `--check`
  · a periodic check → history plus on demand; drift after a restore or a hand repair shows without a deploy, and no
  second table appears.
- [ ] M37 — The job record: the spec's record per service · per set: level before and after, applied labels with kind,
  rollback floor, background migrations pending, lock waits → per set; the rollback floor is what the owner needs
  before pressing roll back.
- [ ] M38 — Product page and rollout UI: level and newest label (spec) · plus rollback floor, background progress and
  "check now" · nothing → staged: the spec's view first, the rest with M21, M24 and M36, which produce the floor, the
  progress and the on-demand read; rollout rows read "Migrate {set}".

---

## Answer batches

Answered in order: each batch holds the parents of later batches' points, and lists its own points parent first.

| # | Theme | Points |
|---|---|---|
| 1 | what a migration is and who owns it | M1, M2, M3, M4, M5, M6 |
| 2 | one mechanism, expand only, and an older image on newer history (the confirmed rollback failure) | M12, M20, M21, M22, M15, M16, M19 |
| 3 | ownership details: mappers, credentials, package DDL, dialects, prerequisites, outside state, tenancy | M7, M8, M39, M40, M41, M42, M55 |
| 4 | declaration and the image contract | M9, M10, M11, M43, M44, M45, M46, M56 |
| 5 | running the step: when, where, locks, rehearsal, SQLite, apply paths, the SDK spread | M13, M14, M17, M18, M49, M50, M47, M48 |
| 6 | data, seeds and client state | M23, M24, M25, M26, M51, M54 |
| 7 | several services and platform services | M27, M28, M29, M30, M31, M32 |
| 8 | moves, operator actions, tests and what Wheelhouse shows | M33, M52, M34, M35, M53, M36, M37, M38 |

---

## Spec gaps

Against [wheelhouse-migrate-step-spec.md](../wheelhouse-migrate-step-spec.md), lines as read on 2026-10-27.

Agreed as written: the one-off container mechanics (`:78-89`), replacing the entrypoint (Open 1), no down scripts in
the step (Open 2), trusting dev and the snapshot in v1 (Open 3), failing before any restart (`:101-104`), the job's
reason text, and no second history table (`:119-121`).

- S1 — The spec declares `migrate` per service (`:26-46`), but the owner is the set: ForeverPin's two images host one
  set and both boot-check it, so which one declares is arbitrary. → M3, M9
- S2 — Order contradicts itself: the table puts the step before every wave (`:69-76`), a bullet runs each "before its
  own wave" (`:46`); a per-wave step lets a sibling that reads the same set restart first and refuse to boot. → M14
- S3 — It skips when the image is unchanged (`:96`); a restore or a hand repair leaves a set behind under an unchanged
  image, and the deployed boot then refuses. → M13
- S4 — A rollback skips the step and the SDK tolerates every `Ahead` (`:97`, `:131`); nothing checks that the newer
  migrations are expand, so an older image may boot on a contracted schema. → M15, M16, M21
- S5 — The `Ahead` change covers the deployed boot's check only (`:131`); the apply path refuses newer history as
  orphaned (`MigrationRunnerService.cs:72`, `:721-741`). Confirmed by a run on 2026-10-27:
  - Wheelhouse v0.7.2 (be sdk 10.0.80) on a database v0.7.3 had migrated (`033`, `ADD COLUMN IF NOT EXISTS … NOT NULL
    DEFAULT`) aborted in `MigrateBespokeOnStartupAsync` before any SQL: "History holds applied migrations absent from
    the source: 033."; the schema itself did not block it.
  - on 10.0.87 the apply call fails alike; `VerifyMigrationLevelsOnStartupAsync` refuses by default ("database at 033
    is newer than the code (032)") and boots only with `LevelMismatch = Warn`, which tolerates `Behind` too.
  - the runner's automatic restore after a failed probe hits the same refusal, so Wheelhouse `deployment.md:149` and
    `:184-185` ("the previous release can read" the expanded database) are false today.
  - the spec's rollback row (`:97`), Open 2 (`:160-161`) and its rig test (`:149-150`) hold only once both paths
    tolerate a compatible `Ahead`.
  - workarounds that worked: deleting `033`'s history row (v0.7.2 boots; the re-upgrade re-applies the idempotent
    `033`), or building with `AllowOrphanedHistory = true` (code-only in 10.0.80). → M16, M19
- S6 — The container mounts the service's settings file (`:84`), tying the step to the runtime role and leaving no room
  for a deploy identity. → M8
- S7 — No lock safety: a timeout of up to 60 minutes (`:33`, `:40`), no `lock_timeout`, no retry, no "busy" exit; a
  lock wait hangs until that timeout, or, under an author's `SET LOCAL lock_timeout`, lands in exit `2` "script
  failed". → M17
- S8 — No data migrations: nothing on backfills, batch-held locks, background migrations or contract gates. → M23–M25
- S9 — Expand-only binds every product (`:44-45`) without a machine-readable marker, against `breaking-changes.md:14`
  for products without users. → M20, M21
- S10 — Release sets of several repositories and "B fails after A" are absent; `backlog.md:134` stays open. → M27, M28
- S11 — Identity appears only as the first consumer (`:10-11`); instance products (Q5 · B), Form 1 module sets, shared
  hosts and product ↔ service versions are absent. → M29–M32
- S12 — The helper and contract are bespoke only (`:61`, `:130`); EF and DbUp products, such as Ocharo Marketing,
  Hijinx and the pilots' identity databases, get no `migrate`. → M11
- S13 — The bundle's existing `migrations` fact (runner `transport.py:264-270`, `release_sets.py:208-211`,
  `artifacts.py:468`) is not reconciled with the new key. → M9
- S14 — Wheelhouse's self-deploy and `vps/self-deploy.py` are not covered, though Wheelhouse is the first app whose
  boot stops applying once it bumps the SDK. → M19
- S15 — The product page reads job history only (`:119-121`); drift after a restore stays invisible until the next
  deploy. → M36
- S16 — `migrate-result` carries name, applied labels and level (`:58-59`); it lacks the level before, kind, rollback
  floor and background status. → M37
- S17 — The changes outside Wheelhouse (`:128-135`) miss the product and domain templates (boot only), the bespoke
  convention (sets, owner, level check), `capability-forms.md:71-72` (per schema since Q54) and the SDK bump of 35 of
  37 backend solutions. → M3, M10, M48, M56
- S18 — The step assumes a set with history; images on `EnsureCreated` or hand DDL (Ocharo Brand, Catalogue, Blog,
  Studio, Motion; HomeAtlas) have no level for `--check` or `migrate-result`, and "no service declares `migrate`: no
  step at all" (`:99`) leaves their boot DDL in place without a word. → M46
- S19 — DDL outside any set still runs at the deployed boot: Hangfire creates `hangfire` with the runtime role, and the
  SDK idempotency store ships an opt-in `EnsureTableAsync` beside its `CreateTableSql` (no swept host calls it);
  mounting the service's settings (`:84`) hides that a runtime role then needs DDL rights. → M39, M8
- S20 — No seed phase: Haven applies its seed files right after its migrations, and Ocharo Marketing imports a seed
  bundle at every boot; the step has no place for either. → M51
- S21 — SQLite overlap (`:107-108`) holds for the bespoke runner, whose batch holds the write lock
  (`bespoke.md:76`), but the dialect requires one applicant per file (`bespoke.md:10`): an old release below 10.0.82
  that restarts during the step applies the same file, and EF-run SQLite sets (Marketing, Hijinx) take no such lock (U).
  → M49, M48
- S22 — Extensions and preflight are absent: Harvest's set runs `CREATE EXTENSION pg_trgm` and probes the encoding at
  boot only. `pg_trgm` is trusted, so the database owner Wheelhouse places (`prepare.py:59-60`) installs it; an
  untrusted extension, or a runtime role that no longer owns the database (M8), cannot, and nothing in placement
  creates one. → M41, M8
- S23 — The be sdk change (`:130-131`) reaches every product that bumps, whatever deploys it: products on compose
  (Haven, ListingShelf, TranscriptForge) and Hijinx get no step and lose boot apply; the order of the bumps across 35
  solutions is absent. → M47, M48
- S24 — "The be sdk's advisory lock covers PostgreSQL replicas" (`:105-106`), but that lock shares one bigint key space
  with the SDK's app-level `pg_advisory_xact_lock` and Desk's own key. → M50

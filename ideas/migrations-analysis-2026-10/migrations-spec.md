# Migrations — wow2 spec

*Last updated: 2026-10-28*

## 1. Scope

How every wow2 app changes persistent state across releases: sets and their owners, the `app migrate <verb>` command
tree each image carries, the descriptor's `migrate:` list, Wheelhouse's migrate step and rollback gate, data
migrations, seeds, platform-service instances, cross-owner foreign keys and column types. Built from the
[analysis](migrations-analysis-2026-10.md), whose points M1–M80 are all answered; a line marked "owner
2026-10-27" there wins over the original pick. Supersedes the Identity chat's
[migrate step spec](../wheelhouse-migrate-step-spec.md) (§ 5 maps it). Terms: [concepts](../../docs/concepts.md).

- **Status:** draft for the developer's refinement. Point ids cite the analysis, where the reasoning lives.
- Names the analysis left open are marked *proposed* and listed in § 6 item 14.
- The Identity chat's parts: § 4 phases 5 and 6, § 6 item 10.

---

## 2. Decisions

### Model and ownership

- must express every persistent-state change the code depends on as a migration in exactly one set (M1).
- must keep three kinds apart: a migration (schema, reference data, a bounded backfill; in a set), a background
  migration (batched, resumable; in the owner's code) and a move (across a system boundary; a Wheelhouse job) (M1).
- must give every set exactly one owner, the repository and assembly that embed it; databases and services host sets
  and own none (M3).
- must keep a platform service's set one named set in both consumption modes — pulled image or built-in library —
  with its own history, lock and schema; a library's files never merge into the product's default set (M3, M76).
- must give module, package and service sets a named schema; the product's own sets stay in `public`, a second one as
  a named set with `{name}_migration_history` (M4).
- must keep one database per product environment, `<product>_{env}`, holding the product's sets, its modules' and
  packages' sets and every per-product instance's sets, on one PostgreSQL server (M6).
- must give a shared instance its own database on a server apart from every product's host, deployed as a Wheelhouse
  product of its own (M6, M29).
- must ship DDL a package owns (outbox, inbox, webhook, idempotency, ASP.NET Identity) as the package's named set in
  the product's step, never a runtime create or a copy; Hangfire's installer runs in the step (M39).
- must keep tenants as rows of the owner's set; schema- and database-per-tenant are ruled out (M55).
- must use PostgreSQL for every set; SQLite only where the owner accepts losing the data, none today (M40, M49).
- must keep outside the step: per-environment seeds, imports and moves (M26, M33, M52), files on volumes and keys
  (M42), browser and device storage, which migrates on read through the fe sdk (M54).

### Declaration

- must register sets in code — `AddDatabaseBespokeMigrations`, `AddDatabaseBespokeMigrationSet`, or the EF or DbUp
  runner — with SQL embedded as `Migrations/NNN-name/{Apply,Rollback}.sql` (M10, M11).
- must ship `app migrate <verb>` in every image that hosts a set; EF and DbUp sets answer the same tree (M10, M11, M57).
- must declare a product-level `migrate:` list in `deploy.yml`: one item per image that hosts a set (`service`,
  `command`, `timeout`), never one per service that reads a set (M9, M43).
- must declare a pulled per-product instance as a service of the product with an image pinned by tag from its own
  repository, and list its item before every item whose sets reference its set (M28, M77).
- must allocate an ordinal once and never reuse it; gaps stay; `Dev/` scripts reach a set only by
  `wow-migrate promote`; a template's baseline ships no sample table (M56).
- must adopt `EnsureCreated`, hand additive DDL and foreign journals into a set — an idempotent `001-baseline` or the
  `baseline` verb, Haven's journal through one SDK converter — before the image's first deploy with the step (M46).
- must avoid non-.NET images; one that is unavoidable answers the same verbs, exits and `migrate-result` line (M45).
- should derive the bundle's `migrations` fact from the release manifest's levels (M9, M78; S13).

### Image contract and actions

- must serve every action as a verb of one be sdk command tree in the image; `wow-migrate` runs the same tree over a
  manifest for developers and CI (M57). Verbs: § 3.1.
- must run `apply` then `seed` for a bare `migrate`, the command a rollout declares (*proposed*, M51).
- must exit alike for every verb: `0` done or current · `1` refused · `2` failed · `3` busy (M10, M17).
- must print one `migrate-result` JSON line per run as the last line starting `migrate-result `, and no secret (M37).
- must make every verb idempotent: a rerun that finds its target state exits `0` and changes nothing (M2).
- must make every `Apply.sql` and `Rollback.sql` idempotent, and keep `Rollback.sql` in every set (M2, M20).
- must keep `check`, `plan`, `locks` and `sets` free of side effects: no schema, history table, marker or lock appears;
  a fresh database reads every set `Behind` (M2, M58).
- must answer applied state from history, never from a script failing; a schema fingerprint per set joins it (M2, M58).
- must report per set and per migration: applied, pending, compatible or incompatible `Ahead`, orphaned, drifted,
  owner conflict; level, rollback floor, extensions and background progress (M37, M58).
- must guard every verb that writes outside a rollout with `--confirm <database>`; the verb enables its own engine
  guard, so `AllowRollback` stays off in the app (M2, M34).
- must record every writing verb: history rows for `apply` and `baseline`; an event row for `rollback`, `forget`,
  `repair`, `baseline`, `claim`, `unlock` and `bg` (M61).
- must not run `rollback`, `forget`, `repair`, `baseline`, `claim` or `unlock` inside a rollout (M2).

### Execution

- must run every declared item on every forward deploy, dev and prod; a current set exits `0` in seconds (M13).
- must run all items after the pull and before the first wave, in order: list order within a repository, every set
  after the sets it depends on; any failure stops the job before any restart (M14, M28).
- must run each item in a one-off container — the item's release image, `--pull never`, the command as entrypoint, the
  service's environment, volumes and memory, the platform network, all capabilities dropped, the image's user (old
  spec `:78-89`) — connecting through its own migrate key, the runtime role in v1 (M8).
- must keep a deployed boot read-only; only a local run (Development, no `DEPLOY_ENVIRONMENT`) applies at boot (M16).
- must remove every other apply path — `ApplyWhenDeployed`, Development-only runners, `Schema:ApplyOnStartup`,
  `--migrate` flags, a CLI on the boot helper; Wheelhouse's bridge is the one interim exception (M19, M47).
- must run the same command as a one-shot compose service the app waits on (`depends_on:
  service_completed_successfully`) for a product deployed by compose (M47).
- must bound waiting: `lock_timeout` per batch, bounded retries per batch, a bounded advisory-lock wait, then exit `3`;
  a file may override the timeout; the runner retries a `3` once (M17).
- must take the migrator's advisory lock in a reserved key class, apart from app-level locks (M50).
- must snapshot prod before the step and hold the target's deployment lock for the job (both exist); the dev run is the
  rehearsal in v1 (M18).
- must let a SQLite set not yet moved migrate beside the running writer, its old release verifying at boot (M49).
- must take the step product by product in M48's order, each in one release: the command, the step, then the SDK
  bump; a bump alone never ships (M48).

### Rollback and compatibility

- must keep platform apps expand-only, linted in CI; a product without external users may contract in the release of
  the change, and that bundle says `rollbackCompatible: false` (M20).
- must put a contract in its own file marked `-- @contract since=vX.Y`, naming the oldest owner release that no
  longer reads or writes what it removes; the migrator records kind and `since` in history (M21).
- must let release R run on a set when every applied ordinal above R's level is an expand, or a contract with
  `since ≤ R`; `since` counts in the set owner's releases — library releases for a module set (M16, M21, M76).
- must count a history row without a kind as incompatible (*proposed*, M16).
- must boot a deployed image on a compatible `Ahead` with a warning, on the level check and on the apply path, and
  refuse `Behind`, an incompatible `Ahead`, orphans below the level, drift and owner conflicts (M16).
- must gate every return to an older release — operator rollback, the runner's automatic restore, a deploy of an older
  release — with the older image's `migrate check`: proceed on `0`, else refuse and name the snapshot (M15).
- must refuse a pending ordinal below the applied level outside a local run (M56).
- must recover a set B that fails after set A applied by fixing B forward; no cross-set rollback (M27).
- must recover prod forward or from the snapshot; `rollback` runs on prod only when forward fails (M2).
- must offer `forget` for images built before the tolerant boot, so no operator deletes history rows by hand (M60).

### Data, seeds, background migrations, moves, imports

- must write a small backfill (seconds on prod-size data) as its own idempotent SQL file after its expand (M23).
- must write reference data the code needs in every environment as idempotent upserts in the set; per-environment and
  secret seeds (first admin, OIDC clients) stay in configuration or a host CLI (M26).
- must ship each seed change as one seed file: it fills every table the change needs in one transaction, is
  journalled once, keeps its mode (`upsert`: the file wins; `insert`: the runtime owns an existing row), and runs in
  the step after every set; a correction is a new file (M51).
- must run a large or code-bound change as an SDK background migration: named, batched over a key range, committed per
  batch with a cursor, idempotent per batch, run by the new release's `Jobs/` worker once that release is live (M24).
- must mark a contract that needs a finished background migration `-- @requires <name>`; `apply` refuses it until then
  with exit `1` (M25).
- must control background migrations by `bg pause · resume · retry · rollback`; `bg rollback` runs the declared
  batched inverse, else pauses and resets the journal; data rollback mirrors schema rollback (M63).
- must run a move (Files imports, tenant and server moves, a per-product instance turning shared, a takeover) as a
  Wheelhouse job type sharing the one-off container and step journal, never inside a rollout; its product-side change
  is a background migration the cutover release starts (M33).
- must run imports, adoptions and derived-table rebuilds as audited operator jobs on the image's CLI, with `--dry-run`
  (M52).
- must keep partition upkeep and re-keying as the owner's jobs; the snapshot pairs the dump with volume tars, and a
  file-layout change is a background migration (M41, M42).

### Platform services and instances

- must migrate a per-product instance in its product's step, as an item of the product's list (pulled image, M77) or
  inside the product's image (module, M30); its level is the product's pin (M29).
- must migrate a shared instance in its own rollout, once for every tenant; no tenant pins it back (M29, M31).
- must keep a service serving the previous client contract version, proven by the previous client's conformance suite
  against the new image; a per-product instance's referenceable tables join that contract (M31).
- must ship a service update with its client package, taken by each product at its next release (M31).
- should declare `requires:` for shared instances, checked by Wheelhouse before any restart — later (M32).
- must switch a set between modes, or take it over, by an audited `claim`; per-product to shared is a move plus a
  contract in each referencing set (M6, M33, M34).
- must run operator actions through the image's verbs, by hand first and as Wheelhouse jobs later (M34).
- must let a set create trusted extensions (`CREATE EXTENSION IF NOT EXISTS pg_trgm`); the product declares the
  untrusted ones, Wheelhouse creates them as superuser at placement, and `apply` refuses before any SQL while a
  declared extension is missing (M41).
- must keep Wheelhouse free of package- or service-specific migration logic: it runs each item's command (M39).

### Cross-owner references

- may key a table into another owner's published tables inside one database; one `users` table, Identity's, and no
  product copy of it (M5).
- must declare each dependency at the referencing set's registration (`DependsOn("identity", 3)`), and ship the
  referenceable tables, keys and readable columns beside the referenced set's registration (M79).
- must refuse with exit `1` before any SQL when a dependency is missing or below the level it names (M28, M79).
- must change referenceable tables and keys by expand and contract only (M5, M20, M21).
- must follow the referenced owner's `ON DELETE` contract; Identity soft-deletes users and scrubs erased rows in
  place, so a `RESTRICT` never blocks (M5).
- must write only the sets the repository owns; another owner's published tables may be mapped read-only, and writes
  go through that owner's module or API (M7).
- must grant `REFERENCES` and `SELECT` on published tables once roles split (M8).
- must reference a shared instance by id, never by key, with loose-FK cleanup driven by the owner's events
  (`PersonDeleted`, a file deleted) in each consumer, which checks a parent exists before writing a child (M80).
- must name a dependency's schema in SQL by `{{schema:<set>}}`, resolved from the database's owner marker
  (*proposed*, M79).

### Column types

- must name tables, columns, constraints and stored values in unquoted snake_case (M64).
- must key rows by `uuid` v7 made in the app with no database default; rows SQL inserts take v7 from SQL; a public
  token stays a separate random value; `bigint GENERATED … AS IDENTITY` only for claim rows and append-only logs;
  `integer CHECK (id = 1)` for a singleton (M65).
- must store an instant as `timestamptz` in UTC, `DateTimeOffset` at offset zero, named `*_at` (M67).
- must store a calendar date as `date` (`DateOnly`) named `*_on`, every one; package-owned names stay (M68).
- must store a time of day as `time` (`TimeOnly`) named `*_time`, with an IANA zone column when it belongs to a
  place; never `timetz`; a zoneless `timestamp` only for a declared local wall-clock value beside its zone (M69).
- must store a span SQL computes with as `interval` (`TimeSpan`), a measured elapsed time as `bigint` `*_ms` (M70).
- must use a native enum with snake_case labels for every new column; an existing text enum converts when its product
  next changes it; a label added is an expand, removed or renamed a contract (M71).
- must store money as `bigint` minor or micro units with its currency in a column or the name; `numeric(p,s)` only
  for an exact ratio; `double precision` for measurements (M72).
- must bound a string by `varchar(n)` wherever the domain has a sensible limit, unbounded `text` only for free-form
  bodies; case-insensitive uniqueness by a unique `lower(…)` index, a normalized column only where a library reads
  one, no `citext`; widening is an expand, narrowing a contract (M73).
- must use `jsonb`, `json` only for a document whose exact text is the value; SQL writing stored JSON uses camelCase
  keys and ISO-8601 durations (M66).
- must stamp `created_at` and `updated_at` in the interceptor, with `DEFAULT now()` on `created_at` for rows SQL
  inserts; no `updated_at` trigger (M74).
- must soft-delete by `deleted_at timestamptz NULL` alone; unique indexes `WHERE deleted_at IS NULL` (M75).
- settled rules stand: `boolean`, `bytea`, `NOT NULL` unless optional, quantities as integers in a documented unit.

### Testing and lint

- must give every repository whose set the step runs a migrations tier, stamped by the templates (M53).
- must prove idempotency: Apply → Rollback → Apply, Apply → Apply, Rollback → Rollback, history bypassed (M59).
- must run the `Testing.Data` lint in every migrations tier: expand-only from a per-set cutoff ordinal with the
  `@contract` exemption, lock-risk rules, and keys or mappings onto unlisted tables (M22, M79).
- must test each image's verbs in its E2E tier: exits, reruns, a write-free `check`, the `migrate-result` line (M57).
- must run the upgrade smoke for platform apps on the rehearsal rig: N-1 schema and seed, apply N, N-1 smoke (M35).

### Observability

- must record per item `status` (`applied` · `current` · `refused` · `failed` · `busy` · `timed out`), `exitCode`,
  `seconds`, and per set its level before and after, applied labels with kind, rollback floor, background migrations
  pending and lock waits (M37).
- must show per environment and set the level and newest label from the latest job, then rollback floor, background
  progress and "check now", staged with M21, M24 and M36 (M36, M38).
- must keep the database's history the only history, Wheelhouse job records beside it, and audit operator actions;
  the rollout row reads "Migrate {set}: 1 applied (002-oidc) in 3s" (M36, M38).

---

## 3. Components to build

One work package per repository; seams name files under each repository's codebase root.

### 3.1 be sdk — `wow-two-sdk-beta.be` (`src/Data/Migrations/`, `src/Testing.Data/`, `src/Jobs/`)

Lane A — the command tree and the engine (`src/Data/Migrations/`):

| Verb | Writes | In a rollout | Guard | Today |
|---|---|---|---|---|
| `check [--set s] [--json]` | nothing | after `apply`; the rollback gate | — | `CheckLevelAsync`; CLI `check` |
| `plan` | nothing, no lock | — | — | missing |
| `apply [--dry-run]` | history rows | yes | — | `MigrateBespokeForDeployAsync`; `DryRunPendingAsync` |
| `seed` | seed rows, seed journal | yes, after `apply` | — | missing |
| `sets --json` | nothing, no database | build time | — | missing |
| `rollback --to N` | runs `Rollback.sql`, deletes rows | no | `--confirm <db>` | `RollbackAsync` |
| `forget --above N` | deletes rows, runs no SQL | no | `--confirm <db>` | missing |
| `repair` · `baseline --to N` | checksums · baseline rows | no | `--confirm <db>` | `RepairAsync` · `BaselineAsync` |
| `claim --owner o --instance i` | owner marker | no | `--confirm <db>` | missing |
| `locks` · `unlock` | nothing · ends the holder | no | `unlock`: `--confirm <db>` | missing |
| `bg pause·resume·retry·rollback <name>` | the journal | no | `--confirm <db>` | lane C |

- adds the tree as a library shared by `wow-migrate` and hosts: the verbs leave `cli/CliCommandBuilder.cs` and
  `cli/CliRunnerService.cs`; a host calls one helper before `app.Run()` (`MigrateCommand.IsCommand(args)`, then
  `app.RunMigrateCommandAsync(args)`, *proposed*), replacing Identity's `HostConfiguration.MigrateAsync`; seams
  `PostgresPersistenceStartupExtensions.cs:94-112`, `MigrationSetServiceProviderExtensions.cs:31`, `:58`, `:89-108`,
  `IMigrationRunnerService.cs`, `Ef/EfMigrationsServiceCollectionExtensions.cs`, `DbUp/` (M11).
- exits `0`–`3`; the result line:

```text
migrate-result {"verb":"apply","exit":0,"sets":[{"name":"identity","schema":"identity","state":"current","levelBefore":2,
"levelAfter":3,"applied":[{"label":"003-x","kind":"expand"}],"rollbackFloor":"v0.4","background":[],"lockWaitMs":0}]}
```

- `sets --json` (M78): name, schema, owner kind, level, contracts with `since`, `@requires`, `DependsOn`, extensions,
  the package and version that embeds the set; it builds the service provider without settings or a database.
- kinds (M21): the header grammar `-- @contract since=vX.Y`, `-- @requires <name>`, `-- @lock-timeout <s>`
  (*proposed*) beside `-- @no-transaction`; history gains `kind` and `contract_since`, added to existing history
  tables by `apply` under the set's lock (seams: `RawMigration.cs`, `MigrationDescriptor.cs`,
  `MigrationHistoryEntry.cs`, `PostgresMigrationDialect.EnsureHistoryTableAsync`).
- tolerant boot (M16): `MigrationLevelState` tells a compatible `Ahead` apart; `VerifyMigrationLevelsOnStartupAsync`
  boots on it with a warning, and the apply path's orphan refusal (`MigrationRunnerService.cs:72`, `:721-741`)
  tolerates it; the rollback floor is the highest `since` among applied contracts.
- lock safety (M17): `SET LOCAL lock_timeout` per batch (5 s), 3 attempts with backoff, a `pg_try_advisory_lock` loop
  bounded at 2 min (*proposed* defaults), then exit `3` (seam: `PostgresMigrationDialect.cs:41-43`).
- reserved key class (M50): the two-key `pg_advisory_lock(class, key)` with one reserved class for every set, the
  default set included (its id is the constant at `MigrationOptions.cs:35`; named sets hash at
  `MigrationServiceCollectionExtensions.cs:101`, `:224`); for one transition line it also takes the legacy key.
- events (M61): `{history}_events` per set (`migration_history_events`, `identity_migration_history_events`): verb,
  ordinals, by, job, at, detail; append-only.
- `forget` (M60); `locks` and `unlock` (M62: holder pid, `application_name`, since, query; `pg_terminate_backend`);
  `claim` (M34, `bespoke.md:138`); `baseline` through the same ordinal and `rollback --to N` at N exit `0` (M2); a
  pending ordinal below the level refuses outside a local run (M56; seam `MigrationRunnerService.cs:77-78`).
- `DependsOn` and referenceable tables (M79) on `MigrationOptions`; an image applies its sets in dependency order
  (registration order today); `{{schema:<set>}}` resolves through `MigrationSchemaOwnerStore.cs`.
- extensions (M41): `MigrationOptions` lists required extensions; `apply` and `check` read `pg_extension` first.
- migrate key (M8): `Migrations:ConnectionString` (*proposed*), when set, connects every set in a `migrate` verb.
- seed files (M51): `Seeds/NNN-name.json` (*proposed*: a `mode` and rows per table), embedded beside a set and
  journalled in `{set}_seed_history`; one transaction per file.
- clean-ups: `ISoftDeletable` keeps `DeletedAt` only (M75); `Tenancy/PerSchema` and `Tenancy/PerDb` go (M55); a v7
  function for SQL inserts (M65); the stale `applied_by` CHECK in `bespoke.md:411-426`.

Lane B — `src/Testing.Data/Migrations/`: the lint helper (M22, M79) with Wheelhouse's `ExpandOnlyTests.cs` rules,
lock-risk rules (`CREATE INDEX` without `CONCURRENTLY` on an existing table, `ADD CONSTRAINT` without `NOT VALID`,
`ALTER COLUMN … TYPE`, a volatile default) and the published-tables check, reading `-- contract:` until Wheelhouse
converts; the idempotency mode of `MigratorHarness.cs` (M59); a verb harness for image E2E tiers (M57).

Lane C — background migrations, after the step ships (M24, M25, M63; seams `src/Jobs/Batches/IBatchHandler.cs`,
`BoundedBatchPipeline.cs`, `src/Jobs/Core/`): registration by name, journal `{set}_background_migrations`
(*proposed*), states `queued` · `running` · `paused` · `finished` · `failed`, progress in `check`, the `bg` verbs.

Lane D — the schema fingerprint (M58): a hash of the schemas a set creates or claims, recorded by each writing verb
and compared by `check`.

Acceptance:

- each verb on a Testcontainers database: current `0`, drift `1`, broken script `2`, a lock another session holds
  `3` within the bound; a second run of every verb exits `0` and changes nothing.
- `check` on an empty database creates no schema, history, events or marker and reports every set `Behind`.
- `docker run --rm --network none <image> migrate sets --json` exits `0` with no settings file.
- an image at level 32 boots on a database at 33 when `033` is an expand and refuses when `033` is a contract whose
  `since` is above its release; the apply path behaves alike (S5 replayed).
- before any SQL, `1` for a set depending on `identity` at 3 against `identity` at 2, and for a missing untrusted
  extension; a pending ordinal below the level refuses on a deployed run and applies on a local one.
- `forget --above 32 --confirm <db>` deletes row 33, runs no SQL, writes one event row; without `--confirm`, `1`.
- the migrator's lock and an app-level `pg_advisory_xact_lock` on the same bigint never block each other; the lint
  flags a non-concurrent index and an unmarked `DROP COLUMN`.

### 3.2 pipelines — `wow-two-platform.pipelines` (`generator/release.py`)

- adds the top-level `migrate:` list (`TOP_KEYS`, `:54`): `service` of this descriptor, `command` (non-empty),
  `timeout` (default `10m`, `10s`–`60m`); `release.json` carries `migrate: [{service, command, timeoutSeconds}]` (M9).
- adds a service from another repository's image pinned by tag (M77): `image` with a tag and no `build`; today
  `:348-351` refuses a tag and every service builds; the generator resolves the tag to a digest, pins it in compose
  and versions the service by its tag; a tag change is a descriptor change.
- adds `extensions:` (*proposed*), the untrusted extensions placement creates (M41).
- adds the manifest levels (M78): runs each item image's `migrate sets --json` and writes `migrations` per service;
  derives the boolean `migrations` fact that runner `transport.py:264-270` and `release_sets.py:208-211` read (S13).
- leaves `requires:` for a later minor (M32); ships as the next minor tag after `v0.11.0`.
- acceptance: a valid list builds; a bad timeout, an unknown service or an empty command refuses; a descriptor
  without the key builds the same bundle byte for byte; a pinned image resolves to a digest; a tagged image with
  `build` refuses; `migrations` lists the canary's set and level.

### 3.3 descriptor and conventions — `wow-two-ws` (hub)

- `conventions/deployment/descriptor/deploy-descriptor.md` and `deploy.schema.json`: `migrate:`, the pinned-image
  service, `extensions:`, the migrate key under § Settings at deploy; `needs` stops calling postgres "a platform
  service" (§ 6 item 9).
- the migrations conventions (`migrations.md`, `sql/bespoke-migrations.md`, `sql/migration-tooling.md`,
  `sql/migration-dialects.md`): sets, owners, schemas, kinds, the compatibility rule, lock safety, data migrations,
  seed files, idempotency, the verb tree, exits `0`–`3`, `--confirm <database>`.
- `conventions/development/capability-forms.md:71-72`, `docs/concepts.md` (M3 marked open), the PostgreSQL type rules
  (M64–M75), `entity-contracts.md` soft delete, `deployment/servers/server-lifecycle.md:80`, `:99`.
- acceptance: every rule cites its point; the schema validates the spec's examples; no convention contradicts § 2.

### 3.4 Wheelhouse — `wow-two-platform.wheelhouse` (runner, console, deployment kit)

- step: one "Migrate `<service>`" per item after "Pull images" (`runner.py:1871`) and before the first wave (`:1881`);
  a one-off container modelled on `verify_release` (`:2006-2045`), named `<project>-migrate-<service>-<job 8>`, label
  `wheelhouse.migrate=<project>`; a failure leaves `mutation_started` false and the old release serving; an exit `3`
  retries once, then fails "busy"; a timeout stops the container (M17).
- migrate key (M8): a settings layer for the migrate container fills `Migrations:ConnectionString` from the target's
  database; the service's rendered settings ride beside it.
- rollback gate (M15): before the automatic restore (`:1972-1975`), an operator rollback or a deploy of an older
  release, the older image's `migrate check --json`; non-zero refuses, naming the snapshot; an older release with no
  `migrate:` item falls back to `rollbackCompatible` with a warning (*proposed*).
- job record `migrations` per item and set (M37); rollout rows and the product page's level and newest label (M38
  stage 1); "Check now" runs `migrate check` from the image the target runs (M36); floor and progress later.
- placement creates declared untrusted extensions as superuser (M41; `deployment/vps/prepare.py:58-60` and product
  database placement); pinned foreign images pull and deploy like any service (M77).
- itself (M19): `Wheelhouse.Api/Program.cs` gains the verb beside `VaultCli` and drops `MigrateBespokeOnStartupAsync`
  the release after the bridge; its `deploy.yml` declares `migrate:` on `console`; `self-deploy.py` loads the release's
  own runner (`:187-201`), so it inherits the step, and `gated()` (`:221-230`) stops forcing `rollbackCompatible: true`
  once the gate exists; `ExpandOnlyTests` yields to the SDK lint.
- rig: the canary declares `migrate:` on PostgreSQL; a release adding a migration deploys; a broken script fails while
  the old release serves; a rollback onto an expand boots; onto a contract the gate refuses; a held lock exits `3`.
- acceptance: runner unit tests for placement, order, a run on every forward deploy (no "image unchanged" skip),
  exits `1`, `2`, `3`, a crash and a timeout failing before any restart with the right reason, a malformed
  `migrate-result` tolerated, the gate on all three return paths; the rig cases; the bridge on `wheelhouse-dev` first.

### 3.5 templates — `wow-two-sdk-beta.product-template`, `wow-two-sdk-beta.domain-template`

- `Sample.Api` (`Configurations/HostConfiguration.cs:40`; domain `service/Sample.Api/…:35`) keeps local boot apply
  only and gains the verb helper; `engineering/deployment/deploy.yml` gains its `migrate:` item (M10).
- `tests/Sample.Tests.Migrations` turns required, with the idempotency mode, the lint and an E2E test of the verbs
  (M53, M59); the baseline ships no sample table (M56); a shipped compose file gains the one-shot service (M47).
- acceptance: a repository stamped by `create-repo` passes its migrations tier, answers `migrate sets --json` and
  `migrate check`, and its bundle carries `migrate` and `migrations`.

---

## 4. Build order

| Phase | Repository | Contents | Needs | Parallel with |
|---|---|---|---|---|
| 0 | hub | conventions, schema, concepts (§ 3.3) | this spec | 1, 2 |
| 1 | be sdk | lanes A then B (§ 3.1); release, consumers re-pin | — | 0; B once A's marker parser lands |
| 2 | pipelines | `migrate:`, pinned images, `extensions:`, manifest levels | 1A's `sets --json`, for levels only | 0, 1 |
| 3 | Wheelhouse | runner step, gate, record, key, UI stage 1, rig | 1A published, 2 tagged | runner code beside 2 |
| 4 | Wheelhouse | bridge release R, then R+1 (M19) | 3 | — |
| 5 | per product | the step, then the bump, in M48's order | 4 | products of one rank |
| 6 | per repository | the product sweep | 5 for that product | every repository |
| 7 | be sdk, Wheelhouse | lanes C, D; `requires:`; operator jobs; UI stage 2; dev-refresh rehearsal | 5 | per repository |

- phase 0 comes first in the owner's order (conventions → migrator → sweep, analysis § Answer batches); it touches
  only the hub, so an agent may run it beside phase 1.
- phase 4 (M19): release R bumps the be sdk past 10.0.82 with `ApplyWhenDeployed` and `AllowOrphanedHistory`, and
  ships the verb, the `migrate:` item and phase 3's runner; the previous runner rolls R out, so R applies at boot.
  R+1 drops `ApplyWhenDeployed`: R's runner runs R+1's `migrate` before swapping either console, and `self-deploy.py`
  does the same through R+1's runner. A rollback to a release built before the flag still needs `forget`.
- phase 5 ranks (M48), one agent per repository, each rank after the one before: the canary · Identity (drops its own
  exit mapping) and Files (its set rewritten as the named PostgreSQL set `files`, registered by its Module; drops
  `ApplyWhenDeployed`) · Harvest · ForeverPin (one item on `management`) and Ocharo (`desk`, the one image with a
  PostgreSQL set) · each venture at its next release, the 5 on the pre-rename package taking the rename there.
- phase 6, one agent per repository:
  - Identity: `identity_users.deleted_at` (M5, M75); reverse "never by a foreign key into this schema"
    (`packages/Module/Migrations/Postgres/001-accounts/Apply.sql:9-10`) and T10's ban
    (`t10-schema-migrations.md:170`, `:336`); referenceable tables in `IdentityDatabaseOptions`; retire the SQLite set
    and its parity tests (M40).
  - Haven: `migrate` on the `database` image as a compose one-shot; its HTTP apply, rollback and seed endpoints and
    `Schema:ApplyOnStartup` go, status stays read-only; seeds become SDK seed files; `haven_uuid_v7()` yields to
    PostgreSQL 18's `uuidv7()`; its journal converter and `updated_at` trigger move to the SDK or go (M44, M46, M51,
    M65, M74).
  - every product (owner 2026-10-28): rewrites its sets as if § 2 and the type rules held from the start, converts
    any EF set to bespoke SQL, and drops and recreates its databases; Wheelhouse keeps its data, so its own renames
    take two releases (§ 6 item 6).
  - Ocharo: Marketing (EF) and Brand, Catalogue, Blog, Studio and Motion (`EnsureCreated`, hand DDL) move from SQLite
    into `ocharo_{env}` with rows by an import, the history-less ones adopting sets, each joining `migrate:` in that
    release; `jobs` keeps `dependsOn: [desk]` for readiness only; Hangfire's installer joins the step; Ocharo's
    Identity arrives as the first item when Q66 moves `access.*` (M11, M43, M46, M49, M52, M77).
  - every other SQLite service moves to PostgreSQL at the release that takes the step, rows by an import or empty when
    throwaway (M49, M52); package DDL copies (ForeverPin `012`, Desk `002-access`) yield to package sets by `baseline`
    (M39); existing columns conform per § 6 item 6.

---

## 5. Superseded spec

[wheelhouse-migrate-step-spec.md](../wheelhouse-migrate-step-spec.md), lines as read 2026-10-27.

| Old spec | Verdict | By |
|---|---|---|
| Problem and status: boot verifies, slot after the pull, Identity waits (`:10-20`) | stands; Identity may also be a per-product instance | M6, M13, M77 |
| `services.<name>.migrate` (`:26-40`) | changed: a product-level `migrate:` list | M9, M43 |
| `command` replaces the entrypoint; `timeout` 10m, 10s–60m; pin pipelines (`:32-47`, Open 1) | stands | M9 |
| idempotent command, exit `0` when current (`:42`) | stands, for every verb | M2, M57 |
| expand-only for every migration (`:44-45`) | changed: platform apps always, products may contract | M20, M21 |
| several services, dependency order, each before its own wave (`:46`) | changed: all before the first wave, order checked | M14, M28, M79 |
| exits `0`/`1`/`2`/other (`:51-56`) | changed: adds `3` busy | M17 |
| `migrate-result` with name, applied, level; no secret (`:58-60`) | changed: verb, levels before and after, kinds, floor | M37 |
| be sdk provides the command (`:61`) | changed: a verb tree for bespoke, EF and DbUp | M11, M57 |
| step per declaring service whose image changed (`:74`, `:95-96`) | changed: every forward deploy | M13 |
| container facts (`:82-89`) | stands; settings gain the migrate key | M8 |
| rollback or older release skips the step (`:97`) | changed: the older image's `check` gates it | M15, M16 |
| no `migrate` declared: no step (`:99`) | changed: history-less stores adopt a set first | M46 |
| failure before any restart; database unchanged (`:101-104`) | stands; earlier batches and sets stay, all expand; adds busy, timed out | M17, M27 |
| `deployment_lock`; advisory lock covers replicas (`:105-106`) | lock stands; key moves to a reserved class | M50 |
| SQLite beside the old container (`:107-108`) | changed: until moved to PostgreSQL, one applicant | M48, M49 |
| rollback scripts never run here (`:109-110`) | stands; operator verbs named | M2, M34, M57 |
| job record per service with `skipped` (`:116-117`) | changed: per item and set, no `skipped` | M13, M37 |
| rollout row, product page from the latest job, no second table, no audit (`:118-122`) | stands per set; page adds "check now" and staged extras; operator verbs audited | M36, M38, M61 |
| be sdk tolerates every `Ahead` (`:131`) | changed: a compatible `Ahead`, on both paths | M16, M21 |
| pipelines `release.json` `migrate` per service (`:132`) | changed: product list plus manifest levels | M9, M78 |
| conventions: the key, the contract, expand-only (`:133`) | changed: § 3.3 | M3, M20 |
| Identity declares `migrate`, drops its own mapping (`:135-138`) | stands | M48 |
| runner tests: skipped when unchanged and on rollback (`:144-147`) | dropped; the gate replaces the rollback skip | M13, M15 |
| rig on a SQLite volume (`:148-150`) | changed: PostgreSQL | M40, M49 |
| prod runs dev's image (`:98`); generator tests; Open 2 down scripts; Open 3 trust dev (`:151-164`) | stands | M2, M18 |

---

## 6. Open items

1. M69 settled (owner 2026-10-27): `time` plus an IANA zone column, `TimeOnly`, named `*_time`.
2. Exits: `sql/migration-tooling.md` returns `2` for a refused guard and prompts `[y/N]` unless `--force`; § Actions
   returns `1` for a missing `--confirm <database>` and exits `check` `1` "when not current", while the gate needs `0`
   on a compatible `Ahead`. This spec follows § Actions for the guard and exits `check` `0` when the image may run.
3. Operator actions: M34 picks "by hand now, Wheelhouse jobs later", § Actions has Wheelhouse run every verb, and M60
   and M62 argue against the shell on prod that "by hand" needs. This spec: verbs in phase 1, jobs in phase 7.
4. `forget`'s guard: M60 refuses unless every row is an expand "or the operator names the database", yet every
   writing verb needs `--confirm <database>`. Proposed: `--confirm` always, plus a flag for a contract or kind-less row.
5. Haven's boot flag: § Multi-service products keeps `Schema:ApplyOnStartup` "for local runs"; M47 removes every boot
   flag, and M44 tailors Haven to the standard. This spec follows M44 and M47.
6. Settled (owner 2026-10-28): existing columns conform in the product sweep — each product rewrites its sets as if
   the rules held from the start, then drops and recreates its databases; Wheelhouse keeps its data, so a rename
   there is a contract over two releases (`*_at_utc`). Rows the code depends on stay in migrations (M26); rows
   content owners edit go in `upsert` seed files (M51).
7. Settled (owner 2026-10-28): drop `AllowOrphanedHistory` from the bridge; recorded kinds let R tolerate a
   compatible `Ahead` (M16, M21).
8. M50 transition: an applicant on the legacy bigint key (a boot below 10.0.82, `ApplyWhenDeployed`) does not exclude
   one on the reserved class; this spec adds taking both keys for one transition line.
9. Conventions behind the answers: `capability-forms.md:71-72` gives a Form 1 consumer the migrations and forbids
   reading a Form 2/3 service's tables (M3, M5–M7); `docs/concepts.md:37-38`, `:44` still mark M3 open;
   `deploy-descriptor.md:49-50` calls postgres "a platform service", concepts' term for Identity. Phase 0 fixes them.
10. Identity decisions reopened, for the Identity chat to record: Q5 · B's own database for a per-product instance,
    Q63, Q64's "SQLite stays Form 1 only", and T10's ban on foreign keys into its schema (M5, M6, M40, M77).
11. Code against the analysis: the default set's lock is the constant `4_855_178_001L` (`MigrationOptions.cs:35`), not
    an FNV-1a hash (U56); the history table's `execution_ms integer` (`PostgresMigrationDialect.cs`) breaks M70's
    `bigint`; `self-deploy.py` needs no step of its own (S14, M19), since it runs the release's runner, but its
    `rollback` runs the older release's runner (`:376-377`), which lacks the gate until releases built after phase 3.
12. Settled (owner 2026-10-28): every host, compose file and test container moves to PostgreSQL 18, the newest
    stable major, whose built-in `uuidv7()` serves SQL inserts; the SDK ships no function. The live hosts' 16 → 18
    move is a dump and restore (postgres convention § Version).
13. Multi-repository order: M43 merges items "in M28's order", a per-repository list order; across repositories this
    spec orders items by the sets' `DependsOn` from the manifest, then catalog order (*proposed*).
14. Names this spec proposes: the host helper, `Migrations:ConnectionString`, `extensions:`, a bare `migrate` =
    `apply` + `seed`, `Seeds/NNN-name.json` with `{set}_seed_history`, `{set}_background_migrations`,
    `{{schema:<set>}}`, `-- @lock-timeout`, the lock defaults (5 s, 3 attempts, 2 min), kind-less rows as
    incompatible, the gate's fallback for releases without `migrate:`.
15. Settled (owner 2026-10-28): EF migrations are banned; every set is bespoke SQL, and an EF set converts at its
    product's sweep. DbUp starts no set.

# Migrations — wow2 analysis

*Last updated: 2026-10-27 02:30 PM*

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
| pipelines | `workbench/wow-two-platform/wow-two-platform.pipelines/` |
| migration conventions | `conventions/development/backend/dotnet/core/mla/domains/persistence/migrations/` |

- read 2026-10-27; line numbers as of that read; `(U)` = read in code, not run.
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

---

## Verdict

- **The set is the unit of ownership.** A migration set (ordered SQL, one history table, one lock, optionally one
  schema) has exactly one owner; databases host sets and services host sets, and neither owns them.
- **One path for every deployed app.** Wheelhouse runs each release image's `migrate` in a one-off container after the
  pull and before the first wave, for products, Identity, Files and Wheelhouse itself; only a local run applies at boot.
- **Schemas stay one release backward compatible.** Migrations expand; a contract lands a release later in its own
  marked file that history records, so an older image boots on a newer schema and Wheelhouse checks a rollback before
  it runs. Down scripts never run on deploy; prod recovers forward or from the snapshot.
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
  `Ahead` and fails too (`MigrationLevelReport.cs:73-74`).
- no migration kind: history records nothing about expand vs contract, so neither an older image nor Wheelhouse can
  tell a safe `Ahead` from an unsafe one.
- no data-migration primitive: no batched or background migration, no progress journal, no gate a contract can wait on.
- no exit-code helper: each image maps the `Result` to `0`/`1`/`2` itself (Identity
  `service/Identity.Api/Configurations/HostConfiguration.cs:59-80`).
- stale doc: `bespoke.md:411-426` shows an `applied_by` CHECK of `startup|endpoint|cli`; the code has `varchar(60)` and
  no CHECK (`PostgresMigrationDialect.cs:54-63`) and writes `deploy` and `baseline`.
- adoption: about 25 backend solutions pin 10.0.71–10.0.81, before the boot gate; only Identity and Files are past
  10.0.82. Each bump turns a boot that applied into a boot that refuses a pending set.

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
- nothing says which of several services sharing a set runs it.

### Pipelines

- the release manifest carries `rollbackCompatible`, false by default (pipelines `generator/release.py:754`); no
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
| roll back to the previous release when the bundle or the target promises compatibility | built | `runner.py:1970-1973` |
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
- the runner rolls a failed self-promotion back on that promise (`deployment.md:148`, `:184`).
- gap (U): the previous image applies at boot and refuses the newer release's ordinals as orphaned
  (`MigrationRunnerService.cs:72`; `AllowOrphanedHistory` is unset), so a rollback across a migration probably fails
  to boot today.
- gap: a bump past 10.0.82 makes its deployed boot verify-only; its self-deploy and `deployment/vps/self-deploy.py` then
  need the step, or the first release with a migration fails to boot.
- the built-in vault (decision 59) lives in Wheelhouse's own set, schema `vault` beside `public`
  (`Wheelhouse.Persistence/Migrations/030-built-in-vault/Apply.sql`).

### Products

| Product | Shape | Today |
|---|---|---|
| ForeverPin | `management` and `redirect` over one set (`ForeverPin.Persistence/Migrations`) and one database (`deployment/deploy.yml:36-80`) | both hosts apply the set at boot (`ForeverPin.Api/Configurations/HostConfiguration.cs:56`, `ForeverPin.Redirect.Api/Configurations/HostConfiguration.cs:41`), be sdk 10.0.72; the advisory lock serializes two applicants |
| Ocharo | 4 repositories, one product; Desk and `jobs` on PostgreSQL; Marketing and Blog on SQLite volumes | Desk applies at boot with its own loop (`ocharo-platform/…/BrandWorkspace.Api/Configurations/HostConfiguration.Extensions.cs:452-470`) plus an `api-cli` migrate (`:482`); `jobs` waits through `dependsOn: [desk]` (`ocharo-platform/engineering/deployment/deploy.yml:64`); Marketing runs EF migrations at boot on SQLite (`ocharo-marketing/…/OcharoMarketing.Api/Configurations/HostConfiguration.Extensions.cs:90-91`) |
| templates | product and domain templates | boot only (`Sample.Api/Configurations/HostConfiguration.cs:40` and `:35`); no `migrate` command |

- gap: no product has a deploy-time `migrate` command but Identity (and Desk's hand-rolled one); every product relies on
  boot apply.
- gap: Ocharo mixes strategies inside one product (bespoke on PostgreSQL, EF on SQLite); a bespoke-only step misses half.

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

- up is `Apply.sql`; down is `Rollback.sql`.
- expand: a change the previous release survives — a new table, a nullable column, a column with a constant default,
  an index built `CONCURRENTLY`, an enum label, a constraint `NOT VALID`, a widened type.
- contract: a change the previous release may not survive — a drop, a rename, a narrowed type, `SET NOT NULL`, rows
  deleted or rewritten that old code reads.
- level: a set's highest applied ordinal. Rollback floor: the oldest release that can run on the current level.

Rules:

- must express every persistent-state change the code depends on as a migration in exactly one set.
- must keep `Rollback.sql` and run it only locally, in tests, or as a guarded operator action; a deploy never runs it
  (M2).
- must not put a seed or a move in a set (M26, M33).

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
- interim: Wheelhouse may set `ApplyWhenDeployed` for its SDK bump only, removed once its own step ships.

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
  `-- @requires <name>`; `migrate` refuses that contract with exit `1` until the background migration finished (M25),
  as GitLab requires ([batched background migrations](https://docs.gitlab.com/development/database/batched_background_migrations/)).
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
- prior art: [database per service](https://microservices.io/patterns/data/database-per-service.html) wants private
  tables per service; here the private unit is the set's schema, and the private database is the instance product's.

---

### Platform services and instances

| Case | Declares | Owns and versions | Runs | Consumer depends on |
|---|---|---|---|---|
| Form 1 module in a product | the module's registration in the product host | the module repository; the level follows the product's package pin | the product's `migrate` (every registered set) | the in-process contract |
| Form 2 instance per owner (wow2 Identity, Ocharo Identity, Ocharo Files A) | the service repository's `deploy.yml` | the service repository; the instance's release | the instance product's rollout | the HTTP contract and its version |
| Form 3 shared host (Files B) | the same | the same | the host's own rollout, once for every tenant | the same |
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
  sets; isolation where two owners share a database, and no churn for about 25 products.
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

### Declaration

- [ ] M9 — Where the step is declared: `services.<name>.migrate` (spec) · a product-level `migrate:` list naming image,
  command and timeout · inferred from images that register sets → a product-level list, one item per hosting image; the
  step belongs to sets rather than to one service's wave, and one declaration ends ForeverPin's two applicants.
- [ ] M10 — Image contract: the be sdk helper (`app migrate`, `app migrate --check`) with exits `0`/`1`/`2` and a
  `migrate-result` line · a `wow-migrate` CLI image · each product's own code → the helper, plus `--check` and exit `3`
  "busy" (M17), and the templates gain the command; the image already embeds the SQL and binds the settings.
- [ ] M11 (M10) — Strategies under the step: bespoke only, EF and DbUp products convert · one helper for all three under
  one exit contract · a command per strategy → one helper for all three; the conventions allow three strategies
  (`migrations.md:9-12`), and Ocharo Marketing and Blog run EF on SQLite.

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
- [ ] M16 — A deployed boot's level check: refuse anything but current (SDK today) · tolerate every `Ahead` (spec) ·
  tolerate `Ahead` only when compatible (M21) → only when compatible; an older image boots after a rollback, but never
  on a schema a contract narrowed under it.
- [ ] M17 — Lock safety: none (today) · migrator defaults: `lock_timeout` per batch, bounded retries, a bounded
  advisory-lock wait, exit `3` when it gives up · `SET LOCAL` by each author → migrator defaults with a per-file
  override; an `ALTER TABLE` queued behind a long transaction blocks every reader of that table, so the step must fail
  fast and retry rather than stall the app.
- [ ] M18 — Prod rehearsal: trust the dev run and the snapshot · a dry run against prod before promoting · rehearse on a
  redacted prod copy in dev → trust dev and the snapshot in v1, then rehearse on the dev refresh once `backlog.md:123`
  ships; a prod dry run takes the same locks as the real run (`bespoke.md:64`).
- [ ] M19 (M12) — Wheelhouse itself: boot apply forever through `ApplyWhenDeployed` · the step in its self-deploy and in
  `self-deploy.py` · boot apply only while it bumps past 10.0.82, then the step → the third; Wheelhouse is the first
  platform app on the step, and break-glass must not rest on boot behaviour the SDK removed.

### Expand and contract

- [ ] M20 — Who must expand only: Wheelhouse (decision 65) · every platform app, while products may contract in the same
  release when they have no external users, marking it not rollback-compatible · every set everywhere → the middle;
  platform apps promise rollback, and `breaking-changes.md:14` spares products shims for users who do not exist.
- [ ] M21 (M20) — Recording a contract: a lint-only `-- contract:` comment (Wheelhouse) · the migrator parses
  `-- @contract since=vX.Y` and records kind and `since` in history · nothing → record it; an older image's boot and
  Wheelhouse's rollback check then read compatibility from the database alone.
- [ ] M22 (M20) — The lint: Wheelhouse's `ExpandOnlyTests` · a `Testing.Data` helper with expand-only and lock-risk
  rules · an external linter (Squawk, Atlas) → the SDK helper (`backlog.md:237`); one rule set, no new toolchain.

### Data migrations

- [ ] M23 — Small data changes: an idempotent SQL file of its own in the set · mixed into the DDL file · application
  code at boot → its own SQL file, seconds on prod-size data; under batch scope a long data file holds every earlier
  lock (`bespoke.md:75`).
- [ ] M24 — Large or code-bound data changes: an SDK background migration (named, batched, resumable, journaled in the
  set's schema, run by `Jobs/`) · each product's own job · scripts by hand → the SDK primitive, built in the migrations
  vector pass after the step; GitLab solved the same problem this way, and every product needs one implementation.
- [ ] M25 (M24) — A contract that needs a finished backfill: `-- @requires <name>`, refused by `migrate` until finished
  · a convention only · nothing → the declared gate; nothing may depend on a background migration before it finishes.
- [ ] M26 — Reference data and seeds: reference rows as upserts in the set, per-environment seeds through configuration
  or a host CLI · everything in sets · everything at boot → the split; a migration runs the same in every environment,
  and a first admin or an OIDC client differs per environment.

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

### Testing

- [ ] M35 — Compatibility testing: lint only · lint plus an upgrade smoke for platform apps on the rehearsal rig (N-1
  schema and seed, apply N, N-1 smoke) · the full N-1 suite on the N schema everywhere → lint plus the platform-app
  smoke; it catches what a regex cannot, at a cost one rig absorbs.

### Observability and Wheelhouse UI

- [ ] M36 — Where Wheelhouse reads schema state: job history only (spec) · history plus an on-demand read-only `--check`
  · a periodic check → history plus on demand; drift after a restore or a hand repair shows without a deploy, and no
  second table appears.
- [ ] M37 — The job record: the spec's record per service · per set: level before and after, applied labels with kind,
  rollback floor, background migrations pending, lock waits → per set; the rollback floor is what the owner needs
  before pressing roll back.
- [ ] M38 — Product page and rollout UI: level and newest label (spec) · plus rollback floor, background progress and
  "check now" · nothing → staged: the spec's view first, the rest with M24 and M36; rollout rows read "Migrate {set}".

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
- S5 — The `Ahead` change covers the deployed boot only; the apply path refuses newer history as orphaned
  (`MigrationRunnerService.cs:72`), and that is what Wheelhouse's own boot on 10.0.80 runs: its rollback across a
  migration probably fails today (U). → M16, M19
- S6 — The container mounts the service's settings file (`:84`), tying the step to the runtime role and leaving no room
  for a deploy identity. → M8
- S7 — No lock safety: a timeout of up to 60 minutes (`:33`, `:40`), no `lock_timeout`, no retry, no "busy" exit; a
  lock wait lands in exit `2` "script failed". → M17
- S8 — No data migrations: nothing on backfills, batch-held locks, background migrations or contract gates. → M23–M25
- S9 — Expand-only binds every product (`:44-45`) without a machine-readable marker, against `breaking-changes.md:14`
  for products without users. → M20, M21
- S10 — Release sets of several repositories and "B fails after A" are absent; `backlog.md:134` stays open. → M27, M28
- S11 — Identity appears only as the first consumer (`:10-11`); instance products (Q5 · B), Form 1 module sets, shared
  hosts and product ↔ service versions are absent. → M29–M32
- S12 — The helper and contract are bespoke only (`:61`, `:130`); EF and DbUp products, such as Ocharo Marketing and
  Blog, get no `migrate`. → M11
- S13 — The bundle's existing `migrations` fact (runner `transport.py:264-270`, `release_sets.py:208-211`,
  `artifacts.py:468`) is not reconciled with the new key. → M9
- S14 — Wheelhouse's self-deploy and `vps/self-deploy.py` are not covered, though Wheelhouse is the first app whose
  boot stops applying once it bumps the SDK. → M19
- S15 — The product page reads job history only (`:119-121`); drift after a restore stays invisible until the next
  deploy. → M36
- S16 — `migrate-result` carries name, applied labels and level (`:58-59`); it lacks the level before, kind, rollback
  floor and background status. → M37
- S17 — The changes outside Wheelhouse (`:128-135`) miss the product and domain templates (boot only), the bespoke
  convention (sets, owner, level check), `capability-forms.md:71-72` (per schema since Q54) and the SDK bump of about
  25 products. → M3, M10

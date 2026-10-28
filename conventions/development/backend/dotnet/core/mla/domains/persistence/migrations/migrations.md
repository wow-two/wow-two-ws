# Migrations

*Last updated: 2026-10-28*

> How every set of persistent state changes across releases, whatever its strategy: kinds, owners, the `migrate`
> verbs, execution, compatibility, data and cross-owner references.
> Point ids (`M1`–`M80`) cite the
> [migrations analysis](../../../../../../../../../ideas/migrations-analysis-2026-10/migrations-analysis-2026-10.md),
> where the reasoning lives.

## Model

| Kind | Holds | Lives in | Runs |
|---|---|---|---|
| migration | schema, reference data, a bounded backfill | a set | the migrate step |
| background migration | batched, resumable DML or code | the owner's code | the new release's `Jobs/` worker |
| move | data crossing a system boundary | a Wheelhouse job | an operator job, never a rollout |

- must express every persistent-state change the code depends on as a migration in exactly one set (M1).
- must keep the three kinds apart (M1).
- must give every set exactly one owner: the repository and assembly that embed it (M3).
- must treat databases and services as hosts of sets; they own none (M3).
- must keep a platform service's set one named set in both consumption modes, a pulled image or a built-in library,
  with its own history, lock and schema (M3, M76).
- must not merge a library's files into the product's default set (M76).
- must give module, package and service sets a named schema (M4).
- must keep the product's own sets in `public`; a second one is a named set with `{name}_migration_history` (M4).
- must keep one database per product environment, `<product>_{env}`, on one PostgreSQL server: the product's sets,
  its modules' and packages' sets and every per-product instance's sets (M6).
- must give a shared instance its own database on a server apart from every product's host (M6, M29).
- must keep tenants as rows of the owner's set; no schema or database per tenant (M55).
- must use PostgreSQL for every set; SQLite only where the owner accepts losing the data (M40, M49).
- must keep outside the step: per-environment seeds, imports and moves (M26, M33, M52), files on volumes and keys
  (M42), and browser and device storage, which migrates on read through the fe sdk (M54).

---

## Strategy

- must choose one strategy per set; never apply two journals to one schema.
- must use [bespoke SQL](sql/bespoke-migrations.md) by default.
- may use [EF migrations](ef/ef-migrations.md) when the EF model owns the set's schema.
- may use DbUp only under its [selection](dbup/dbup-migrations.md#selection) rule.
- must answer the same verbs and exits whatever the strategy (M11) → [actions](#actions).
- must retain explicit schema ownership when changing strategy.

---

## Declaration

- must register each set in code: `AddDatabaseBespokeMigrations`, `AddDatabaseBespokeMigrationSet`, or the EF or DbUp
  runner (M10, M11); file layout → [bespoke migrations](sql/bespoke-migrations.md#layout).
- must embed every set in the image that hosts it; filesystem sources serve `wow-migrate` and local work only.
- must ship `app migrate <verb>` in every image that hosts a set (M10, M57) → [actions](#actions).
- must declare the step in `deploy.yml`'s `migrate:` list, one item per image that hosts a set (M9, M43) →
  [deploy descriptor](../../../../../../../../deployment/descriptor/deploy-descriptor.md#migrate).
- must ship DDL a package owns (outbox, inbox, webhook, idempotency, ASP.NET Identity) as the package's named set,
  applied in the product's step; never a runtime create or a copy (M39).
- must run Hangfire's installer in the step (M39).
- must let a set create trusted extensions itself (`CREATE EXTENSION IF NOT EXISTS pg_trgm`) (M41).
- must declare untrusted extensions in the descriptor's `extensions:`; Wheelhouse creates them at placement (M41).
- must make `apply` refuse with `1` before any SQL while a declared extension is missing (M41).
- must adopt `EnsureCreated`, hand additive DDL and foreign journals into a set before the image's first deploy with
  the step: an idempotent `001-baseline`, or the `baseline` verb (M46).
- must convert Haven's journal through the one SDK converter (M46).
- must avoid non-.NET images; an unavoidable one answers the same verbs, exits and `migrate-result` line (M45).

---

## Lifecycle

- must preserve an applied migration's content and identity; correct it by a new migration.
- must apply development migrations before accepting work that depends on the new schema.
- must not infer production safety from an environment name alone; a guard names the database (M2).

---

## Actions

One be sdk command tree serves every action as `app migrate <verb>` in each image that hosts a set; `wow-migrate`
runs the same tree over a manifest for developers and CI (M57).

| Verb | Writes | In a rollout | Guard |
|---|---|---|---|
| `check [--set s] [--json]` | nothing | after `apply`; the rollback gate | — |
| `plan` | nothing; takes no lock | — | — |
| `apply [--dry-run]` | history rows | yes | — |
| `seed` | seed rows, seed journal | yes, after `apply` | — |
| `sets --json` | nothing; opens no database | build time | — |
| `rollback --to N` | runs `Rollback.sql` files, deletes their rows | no | `--confirm <database>` |
| `forget --above N` | deletes rows, runs no SQL | no | `--confirm <database>` |
| `repair` · `baseline --to N` | checksums · baseline rows | no | `--confirm <database>` |
| `claim --owner o --instance i` | the owner marker | no | `--confirm <database>` |
| `locks` · `unlock` | nothing · ends the holding session | no | `unlock`: `--confirm <database>` |
| `bg pause · resume · retry · rollback <name>` | the background journal | no | `--confirm <database>` |

- must run `apply` then `seed` for a bare `migrate`, the command a rollout declares (M51).
- must exit alike for every verb (M10, M17):
  - `0` — done, or already current
  - `1` — refused: drift, orphan, owner conflict, incompatible, a missing dependency, extension or `--confirm`
  - `2` — failed: a script or the connection
  - `3` — busy: a lock not acquired within its bound
- must exit `check` `0` when the image may run on the database: current, or a compatible `Ahead`; `1` otherwise (M15).
- must print one `migrate-result` JSON line per run, the last line starting `migrate-result `, with no secret (M37).

```text
migrate-result {"verb":"apply","exit":0,"sets":[{"name":"identity","schema":"identity","state":"current",
"levelBefore":2,"levelAfter":3,"applied":[{"label":"003-x","kind":"expand"}],"rollbackFloor":"v0.4",
"background":[],"lockWaitMs":0}]}
```

- must make every verb idempotent: a rerun that finds its target state exits `0` and changes nothing (M2).
- must keep `check`, `plan`, `locks` and `sets` free of side effects: no schema, history table, marker or lock
  appears, and a fresh database reads every set `Behind` (M2, M58).
- must answer applied state from history, never from a script failing (M2).
- must join history with a schema fingerprint per set, recorded by each writing verb and compared by `check` (M58).
- must report per set and per migration: applied, pending, compatible or incompatible `Ahead`, orphaned, drifted,
  owner conflict; and the level, rollback floor, extensions and background progress (M37, M58).
- must guard every verb that writes outside a rollout with `--confirm <database>` (M2, M34).
- must let that verb enable its own engine guard for its run; `AllowRollback` stays off in the app (M2, M34).
- must require `--confirm <database>` on every `forget`, plus an explicit flag to forget a contract or a kind-less row
  (M60).
- must record every writing verb: history rows for `apply` and `baseline`; an event row for `rollback`, `forget`,
  `repair`, `baseline`, `claim`, `unlock` and `bg` (M61).
- must not run `rollback`, `forget`, `repair`, `baseline`, `claim` or `unlock` inside a rollout (M2).
- must run operator verbs from the target's image, by hand until Wheelhouse runs them as audited jobs (M34).
- the schema fingerprint and the `bg` verbs ship in a be sdk release after the step's.
- composition, guards and configuration → [migration tooling](sql/migration-tooling.md).

---

## Execution

- must run the step as the
  [deploy descriptor](../../../../../../../../deployment/descriptor/deploy-descriptor.md#migrate) declares it: every
  forward deploy, every item before the first wave (M13, M14).
- must keep a deployed boot read-only: it checks levels and applies nothing (M16).
- must apply at boot only on a local run: `Development` with no `DEPLOY_ENVIRONMENT` (`IsLocalRun`) (M16).
- must remove every other apply path: `ApplyWhenDeployed`, Development-only runners, `Schema:ApplyOnStartup`,
  `--migrate` flags, a CLI on the boot helper (M19, M47).
- may keep Wheelhouse's bridge release as the one interim boot applier (M19).
- must run the same `migrate` command as a one-shot compose service the app waits on
  (`depends_on: service_completed_successfully`) for a product deployed by compose (M47).
- must serialize each set's applicants by its advisory lock; journal idempotency is no mutual exclusion.
- must verify an EF or DbUp runner's lock before letting two applicants meet one set.
- must take the migrator's advisory lock in a reserved key class, apart from app-level locks (M50).
- must take the legacy bigint key too during the transition, so a boot still applying on it is excluded (M50).
- must bound waiting, then exit `3` (M17):
  - `SET LOCAL lock_timeout` 5 s per batch; a file may override it with `-- @lock-timeout <s>`
  - 3 attempts per batch, with backoff
  - a `pg_try_advisory_lock` loop bounded at 2 min
- must let a SQLite set not yet moved migrate beside the running writer, its old release verifying at boot (M49).
- must take the step product by product in M48's order, each in one release: the command, the step, then the SDK
  bump; a bump alone never ships (M48).

---

## Compatibility

- must classify each migration file as an expand or a contract (M20, M71, M73):
  - expand — a new table, a nullable column, a column with a constant default, an index built `CONCURRENTLY`, a
    `NOT VALID` constraint the writes satisfy, a widened type, an enum label added
  - contract — a drop, a rename, a narrowed type, `SET NOT NULL`, rows deleted or rewritten that old code reads, an
    enum label removed or renamed
- must keep platform apps expand-only, linted in CI (M20).
- may contract a product without external users in the release of the change; that bundle says
  `rollbackCompatible: false` (M20).
- must put a contract in a file of its own, marked with `since`: the oldest owner release that no longer reads or
  writes what it removes (M21) → [markers](sql/bespoke-migrations.md#markers).
- must count `since` in the set owner's releases: library releases for a module or package set (M21, M76).
- must record kind and `since` in history on apply (M21).
- must let release R run on a set when every applied ordinal above R's level is an expand, or a contract with
  `since ≤ R` (M16, M21).
- must count a history row without a kind as incompatible (M16).
- must boot a deployed image on a compatible `Ahead` with a warning, on the level check and the apply path (M16).
- must refuse to boot on `Behind`, an incompatible `Ahead`, orphans below the level, drift or an owner conflict (M16).
- must refuse a pending ordinal below the applied level outside a local run (M56).
- must gate every return to an older release with the older image's `migrate check` (M15) →
  [deploy descriptor](../../../../../../../../deployment/descriptor/deploy-descriptor.md#migrate).
- must recover a set B that fails after set A applied by fixing B forward; no cross-set rollback (M27).
- must recover prod forward or from the snapshot; `rollback` runs on prod only when forward fails (M2).
- must use `forget` when an image built before the tolerant boot refuses newer history (M60).

---

## Data

- must write a small backfill, seconds on prod-size data, as its own idempotent SQL file after its expand (M23).
- must write reference data the code needs in every environment as idempotent upserts in the set (M26).
- must keep per-environment and secret seeds (first admin, OIDC clients) in configuration or a host CLI (M26).
- must ship each seed change as one seed file, `Seeds/NNN-name.json`, embedded beside its set (M51):
  - it fills every table the change needs in one transaction
  - it is journalled once in `{set}_seed_history`
  - its mode stays: `upsert` (the file wins) or `insert` (the runtime owns an existing row)
  - `seed` runs it after every set's `apply`; a correction is a new file
- must run a large or code-bound change as an SDK background migration (M24):
  - named, in the owner's code
  - batched over a key range, committed per batch with a cursor in `{set}_background_migrations`
  - idempotent per batch
  - run by the new release's `Jobs/` worker once that release is live
- must mark a contract that needs a finished background migration `-- @requires <name>`; `apply` refuses it with
  `1` until then (M25).
- must control a background migration by `bg pause`, `resume`, `retry` and `rollback` (M63).
- must make `bg rollback` run the declared batched inverse, else pause and reset the journal (M63).
- must mirror schema rollback for data: a backfill by its `Rollback.sql`, a background migration by `bg rollback`, a
  move by its own job (M63).
- must run a move (Files imports, tenant and server moves, a per-product instance turning shared, a takeover) as a
  Wheelhouse job type sharing the one-off container and step journal, never inside a rollout (M33).
- must make a move's product-side change a background migration the cutover release starts (M33).
- must run imports, adoptions and derived-table rebuilds as audited operator jobs on the image's CLI, with
  `--dry-run` (M52).
- must keep partition upkeep and re-keying as the owner's jobs; a file-layout change is a background migration
  (M41, M42).
- the background-migration primitive ships in a be sdk release after the step's.

---

## Platform services

- must migrate a per-product instance in its product's step, at the product's pin (M29):
  - a pulled image — an item of the product's `migrate:` list (M77)
  - a module — inside the product's image, whose `migrate` applies every registered set (M30)
- must migrate a shared instance in its own rollout, once for every tenant; no tenant pins it back (M29, M31).
- must keep a service serving the previous client contract version, proven by the previous client's conformance
  suite against the new image (M31).
- must add a per-product instance's referenceable tables to that contract (M31).
- must ship a service update with its client package; each product takes it at its next release (M31).
- should declare the shared instances a product calls in `requires:`, checked by Wheelhouse before any restart; the
  key arrives later (M32).
- must switch a set between modes, or take it over, by an audited `claim` (M6, M34).
- must turn a per-product instance shared by a move plus a contract in each referencing set (M6, M33).
- must keep Wheelhouse free of package- or service-specific migration logic: it runs each item's command (M39).

---

## Cross-owner references

- may key a table into another owner's published tables inside one database (M5).
- must keep one `users` table, Identity's; no product copy of it (M5).
- must declare each dependency at the referencing set's registration: `DependsOn("identity", 3)` (M79).
- must ship the referenceable tables, keys and readable columns beside the referenced set's registration (M79).
- must apply an image's sets in dependency order (M79).
- must refuse with `1` before any SQL when a dependency is missing or below the level it names (M28, M79).
- must change referenceable tables and keys by expand and contract only (M5, M20, M21).
- must follow the referenced owner's `ON DELETE` contract (M5):
  - Identity soft-deletes users and scrubs erased rows in place, so a `RESTRICT` into its users never blocks
- must write only the sets the repository owns (M7).
- may map another owner's published tables read-only; writes go through that owner's module or API (M7).
- must grant `REFERENCES` and `SELECT` on published tables once roles split (M8).
- must name a dependency's schema in SQL by `{{schema:<set>}}`, resolved from the database's owner marker (M79).
- must reference a shared instance by id, never by key (M80).
- must clean up such ids on the owner's events (`PersonDeleted`, a file deleted) in each consumer (M80).
- must check a shared instance's parent exists before writing a child (M80).

---

## Testing

- must give every repository whose set the step runs a migrations tier, stamped by the templates (M53).
- must prove idempotency there, history bypassed (M59):
  - Apply → Rollback → Apply
  - Apply → Apply
  - Rollback → Rollback
- must run the `Testing.Data` lint in every migrations tier (M22, M79):
  - expand-only from a per-set cutoff ordinal, exempting `-- @contract` files
  - lock-risk rules → [migration dialects](sql/migration-dialects.md#lock-safety)
  - a key or a mapping onto an unlisted table
- must test each image's verbs in its E2E tier: exits, reruns, a write-free `check`, the `migrate-result` line (M57).
- must run the upgrade smoke for platform apps on the rehearsal rig: N-1 schema and seed, apply N, N-1 smoke (M35).
- harness → [test databases](../testing/test-databases.md).

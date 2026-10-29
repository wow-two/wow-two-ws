# Irreversible migration changes — wow2 analysis

*Last updated: 2026-10-29*

> What wow2 does when a migration destroys data that `Rollback.sql` cannot bring back: a dropped column re-added comes
> back empty. Owner question of 2026-10-29, with two ideas to weigh — a backup before the step, or a copy of exactly
> the tables and columns a migration changes; complex is fine when reliable. Builds on the
> [migrations spec](migrations-spec.md) and the [analysis](migrations-analysis-2026-10.md), whose point ids (M1–M80)
> it cites; its own points are IR1–IR8.

## Status

- ⬜ Analysis for the owner; nothing built. Points IR1–IR8 open.
- ✅ Read 2026-10-29: be sdk `10.0.93-beta` (kinds, `since`, rollback floor, guarded `rollback`, lint), Wheelhouse
  `v0.7.8` (migrate step, rollback gate, prod snapshot), the migrations and PostgreSQL conventions.
- ⬜ The live hosts still run PostgreSQL 16 (Wheelhouse v0.7 Iteration 9, paused), so the recommended mechanism must
  work on 16 as well as 18; it does.

| Short | Path under the hub |
|---|---|
| engine | be sdk `src/Data/Migrations/Bespoke/` (`MigrationRunnerService.cs`, `MigrationCompatibility.cs`, `MigrationHeaderParser.cs`, `PostgresMigrationDialect.cs`) |
| lint, proof | be sdk `src/Testing.Data/Migrations/` (`Lint/MigrationLint.cs`, `MigrationIdempotencyProof.cs`) |
| runner | Wheelhouse `codebase/wheelhouse.runner-services/runner.py` (`take_snapshot`, `migrate_release`, `gate_release`, `restore_allowed`) |
| deployment | Wheelhouse `deployment/deployment.md` § Rollout steps, § Target state and recovery, § Migrate step |
| conventions | [migrations](../../conventions/development/backend/dotnet/core/mla/domains/persistence/migrations/migrations.md), [bespoke migrations](../../conventions/development/backend/dotnet/core/mla/domains/persistence/migrations/sql/bespoke-migrations.md), [redundancy](../../conventions/deployment/servers/redundancy.md), [server lifecycle](../../conventions/deployment/servers/server-lifecycle.md) |

---

## Verdict

- **No rollback restores destroyed values; only a copy taken before the destruction does.** `Rollback.sql` restores
  shape. The conventions already forbid calling a no-op inverse a restore (`bespoke-migrations.md` § Rollback), yet
  `rollback` runs that no-op today and reports success.
- **Expand and contract keep most drops out of the rollback window.** A contract lands once no release at or above its
  `since` reads the data, and the gate refuses any older release (M15, M16, M21). Three holes remain: a product's
  same-release contract (M20), a contract that turns out wrong, and destructive data changes (lower-casing, dedup,
  clamping), which kinds do not cover at all.
- **The prod snapshot is a reliable last resort and a poor rollback.** It rewinds every set in the product database to
  before the deploy: Identity's sign-ups, the outbox and the idempotency keys included. It is manual, prod-only and on
  the same disk.
- **Recommended: an engine-managed targeted copy, `-- @preserve <table>(<columns>)`.** The migrator copies the
  before-image into a `migration_backup` schema in the file's own transaction, under a write lock, and keeps only what
  the file changed. It restores that copy by primary key after `Rollback.sql`, or forward through `-- @restore`; newer
  writes win. The lint requires it, or an explicit `-- @irreversible <reason>`, on every lossy file, and a round-trip
  proof tests each one.
- **Backstops stay independent of authors and the engine.** The prod snapshot covers what nothing preserved. PITR
  (base backup plus WAL, already the [redundancy](../../conventions/deployment/servers/redundancy.md) model) covers
  anything older than the newest five snapshots, and the loss of a host.

---

## 1. What is irreversible

| Class | Operations (PostgreSQL) | Loses | `Rollback.sql` alone gives back |
|---|---|---|---|
| reversible contract | drop an index, constraint, view or function; rename a column, table or enum label (`RENAME VALUE`); `SET NOT NULL`; widen a type | nothing but rebuild time | everything: recreate, rename back, `DROP NOT NULL` |
| lossy by value | `DROP COLUMN`; a narrowing `ALTER COLUMN … TYPE` (`numeric` scale rounds, `timestamptz → date` drops the time, `USING left(…)` truncates); an overwriting `UPDATE` (lower-casing, re-keying, merging two columns, clamping before a `CHECK`, filling NULLs before `SET NOT NULL`); removing an enum label (a new type, the column converted `USING` a mapping) | each affected cell's old value; for filled NULLs, which rows were NULL; for a removed label, which rows held it | the column's shape, empty or holding whatever the inverse can derive |
| lossy by row | `DROP TABLE`, `TRUNCATE`, `DELETE` (dedup before a unique index, orphans before a foreign key, a purge), and every child an `ON DELETE CASCADE` takes along | whole rows, children included | the table's shape, empty |
| lossy by design | hashing or encrypting a secret, scrubbing personal data, a key rotation that drops the old key | what the change exists to destroy | nothing, and nothing may |
| outside the database | files on volumes, blobs, keys (M42); emails, webhooks and payments already sent | not a set's to restore | — |

- the two lossy classes lose the before-image of a bounded, nameable set of cells or rows, which a targeted copy can
  hold.
- contract ≠ irreversible:
  - a rename is a contract, since an older release breaks on it, yet it reverses exactly
  - an overwriting backfill passes as an expand today: the lint's contracting pattern lists `DELETE FROM` but no
    `UPDATE` (`Lint/MigrationLint.cs:105`)
  - kinds (M21) answer "may an older release run"; this analysis answers "can the data come back"
- a narrowing without `USING` fails loudly on a value it cannot hold (`varchar(n)` length, integer overflow); the
  silent losses are rounding, a lossy cast and an explicit `USING`.
- `DROP COLUMN` only hides the column; PostgreSQL keeps the bytes until a rewrite, but no SQL reads them back.
  Forensic readers (the third-party `pg_dirtyread`) are not a plan.
- seed `upsert` files overwrite rows by design (M51); a correction is a new seed file, out of scope here.

---

## 2. When the data is needed back

| # | Case | Today | Loss today |
|---|---|---|---|
| C1 | the release fails right after its step, and the automatic restore runs | an expand-only release returns cleanly; after a same-release contract (products, M20) the gate refuses, and the product stays down until the owner restores the snapshot by hand | every write since the snapshot, plus the downtime |
| C2 | a bug found days later; the owner returns to the older release | as C1 | days of writes in every table of the database |
| C3 | a contract dropped data the product still needs, and it stays on the new release | extract from the snapshot dump into the live database by hand, or restore it whole | none when extracted by hand, through a manual, untested procedure |
| C4 | a data change wrote wrong values (a lossy backfill, dedup on the wrong key) | as C3 | as C3 |
| C5 | hand SQL, or a lossy file nobody marked | the snapshot, within the newest five prod deploys; nothing on dev | as C2 |
| C6 | the host or its disk is lost | nothing: snapshots share the disk, and off-provider backups are backlog | everything |

- expand and contract take C1 and C2 off the table for platform apps and for any product that contracts a release
  later: the older release survives every expand above its level.
- kinds and the gate leave C3–C5 untouched; those cases need the before-image itself.

---

## 3. Options

| Option | Reliability | Cost on our hosts | Write loss on recovery | Several sets and databases | Fit with rollout and gate | Verdict |
|---|---|---|---|---|---|---|
| O1 whole-database snapshot before the step (built, prod) | high for "the exact pre-deploy database": `pg_dump` reads one consistent snapshot; taken before the pull, so writes during the pull fall outside it; same disk; newest five deploys | a full dump of each prod database plus volume tars per prod deploy, five kept on the products host's disk; dump time grows with the database | everything after the snapshot, in every set of the database: per-product Identity, outbox, inbox, idempotency keys, so emails, webhooks and Stripe events recorded since replay or vanish | one database's sets restore together, consistently (M6); a shared instance's database restores apart, to another point (M27) | built; the gate's refusal names it (`snapshot_hint`); restore by hand, every service stopped; dev takes none | keep, as the last resort |
| O2 targeted copy written by each author in `Apply.sql` and `Rollback.sql` | as good as each author: a copy taken without a lock first misses commits that land before the change, a restore that overwrites clobbers newer values, nothing retains or purges, and no lint can check it; PostgreSQL 18's `RETURNING old.*` makes one DML statement's capture race-free, on 18 only, when written | as O3 | as O3 when done right | per file | needs nothing new | rejected as the norm; O3 is O2 done once, in the engine |
| O3 engine-managed `@preserve` (§ 4) | copy, change and catalog row commit in one transaction; a `SHARE` lock before the copy closes the race; only changed cells and rows kept; restore by key, compare-and-set; required by lint, proven per file | a copy of the named columns inside the step, writers waiting for its length (readers do not); disk holds changed rows × retention, inside the product database; no standing process; PostgreSQL 16 and 18 | none outside the preserved cells; inside them a row changed since keeps its newer value, reported; rows inserted since read NULL or default in a restored column | per set and file; no cross-set atomicity needed (M27); per-product instances alike | restore inside `rollback` (operator verb) or a forward `@restore` file in a normal rollout; the gate gains a "restorable" answer | recommended |
| O4 retire in place: rename a column, or `ALTER TABLE … SET SCHEMA` a table, instead of dropping; purge K releases later | exact and O(1): a move carries indexes, constraints and owned sequences; covers drops only, never updates, deletes or narrowing | none at apply; dead columns stay in live tables until the purge | none | per set | rename back in `Rollback.sql`; a second, purging contract later | parked: live tables keep retired columns that `SELECT *`, the published-tables contract and the schema fingerprint (M58) all see; worth it only for a table too large to copy within the step |
| O5 expand and contract with a soak (built) | prevents the need rather than recovering; the gate makes `since` a checked fact | an extra release per contract | none | per set | built (M15, M16, M21) | keep, as layer 0; leaves C3–C5 and same-release contracts open |
| O6 PITR: base backups plus a WAL archive, a restore point per deploy | high and independent of authors: any point within WAL retention, any change, preserved or not; covers C6 once off-host. PostgreSQL recovers a whole cluster, never one database: one product's data comes back through a side instance, then a dump or a by-key copy | `archive_mode = on` (one PostgreSQL restart per host); the WAL of every database on the host plus periodic base backups, shipped off-host (a storage bill); a side container while recovering | none when extracted selectively; a whole rewind loses everything after the target | the whole cluster: every product on the host | Wheelhouse records `pg_create_restore_point('<project>-<job>')` before the migrate step (superuser, which placement already uses), so the target is exact | the backup layer, planned anyway; not a rollback |
| O7 delayed physical standby (`recovery_min_apply_delay`) | fast extraction within its delay | a second PostgreSQL always running: memory and a full disk copy again, or another server | as O6 | the whole cluster | none | rejected: PITR covers it with no standing instance |
| O8 per-table `pg_dump` by Wheelhouse before the step | outside the transaction: the old release keeps writing during the step, so the dump misses commits before the change | a dump per touched table | as O3, minus the missed commits | per table | Wheelhouse must learn each file's tables | rejected: O3 is strictly better |
| O9 history triggers or temporal tables | captures row updates and deletes at runtime, never DDL: a `DROP COLUMN` fires no row trigger; PostgreSQL has no system-versioned tables, and the extension is third-party | a cost on every write, forever | — | per table | — | rejected |
| O10 a `sql_drop` event trigger that refuses a drop no preserve recorded | enforcement, not recovery; catches hand SQL | a superuser creates it per database; it fires on every drop, temporary tables included | — | per database | placement would install it | parked: the lint and "history only through the verbs" suffice while one owner writes the SQL |

### Costs on our hosts

One control host (Wheelhouse's console and database), one products host (one Docker PostgreSQL holding each product's
databases), each a VPS of at least 8 GB RAM and 100 GB disk (`vps.md`).

| Layer | Disk | At each deploy | Standing | Recovery |
|---|---|---|---|---|
| prod snapshot (built) | full dumps and volume tars, newest five, on the host's own disk | a full `pg_dump` before the pull | none | by hand: stop services, `pg_restore --clean`, untar; down for its length |
| `@preserve` | changed cells and rows for the retention window, inside the database, so counted again in every snapshot and backup | a copy of the named columns, only for files carrying the header | none | inside `rollback` or a forward file; down only for the swap |
| PITR | periodic base backups plus every 16 MB WAL segment the host writes within retention, off-host | a restore point | the archiver; one restart to turn it on; storage bill | a side container recovered to the restore point, briefly a second PostgreSQL in memory, then extraction; minutes to an hour by size, untested |

---

## 4. Recommendation

Four layers, each catching what the one before misses, with independent failure modes:

| Layer | Catches | State |
|---|---|---|
| L0 expand and contract, the rollback gate | an older release on a newer schema: C1 and C2 for releases that contract a release later | built: be sdk `10.0.93-beta`, Wheelhouse `v0.7.8` |
| L1 `@preserve` | C1–C4 for every lossy file, keeping every other write | new |
| L2 prod pre-deploy snapshot | C5, within the newest five prod deploys | built |
| L3 PITR, off-host | C5 at any point within WAL retention; C6 | backlog (Wheelhouse "off-provider backups", redundancy's storage role) |

### 4.1 `@preserve`

A header directive on a transactional `Apply.sql`; names marked *proposed* follow the spec's habit (§ 6 item 14):

```sql
-- @contract since=v0.6
-- @preserve users(phone, phone_verified_on)
ALTER TABLE users DROP COLUMN phone, DROP COLUMN phone_verified_on;
```

Apply, inside the file's batch transaction:

1. refuse with `1` before any SQL when the table has no primary key or the file is `-- @no-transaction`.
2. take `LOCK TABLE users IN SHARE MODE` under the file's lock timeout (M17): writers wait, readers continue. Without
   it, a commit landing between the copy and the change reaches neither — and the old release keeps writing during
   the step, exactly in the same-release contract case.
3. copy the key and the named columns into `migration_backup.<set>_<NNN>_<table>` (*proposed*); `@preserve users`
   alone copies every column.
4. run the file.
5. diff: drop each copied row the file left as it was; record the after-value of each column that survives. The
   backup then holds exactly what the file changed: dropped cells, overwritten values, deleted rows.
6. write one row to `migration_backup.entries` (*proposed*): set, ordinal, label, table, key, columns, rows, bytes,
   owner release, applied at.

Restore, one routine on two paths:

- backward: `rollback --set s --to L --confirm <db>` runs `Rollback.sql`, which re-adds the column (nullable), widens
  the type, drops the constraint or recreates the table; the engine then writes the backup back in the same
  transaction.
- forward: a new expand file headed `-- @restore 035 users(phone)` (*proposed*) re-adds what it needs, and the engine
  restores into it. It mends C3 and C4 on the running release and keeps "recover prod forward" (M2).
- by key, newer writes winning:
  - a value returns only where the live cell still holds the after-value, or was re-added empty
  - a row returns only when the file deleted it; one the app deleted since stays deleted
  - a recreated table's row returns only while its parents exist
  - every skipped row stays in the backup; `migrate-result` counts `restored` and `skipped`
- refuse with `1` before any SQL when a backup it needs is purged or missing, unless `--accept-loss` (*proposed*), so a
  rollback never re-adds an empty column silently.

Retention: `apply` purges an entry once K later owner releases have applied to the set and D days have passed (IR2),
recording an event row (M61); `check --json` lists the backups held.

Opt-out: `-- @irreversible <reason>` marks a lossy file whose data must not or cannot be kept: a secret being hashed,
personal data being scrubbed, a table too large to copy within the step. A large change goes to a background
migration whose batches preserve into the same catalog (lane C, M24, M63), or relies on L2 and L3.

### 4.2 Why it is reliable

- atomic: copy, change and catalog row commit together or not at all, and the lock taken first makes the before-image
  exact while the old release writes.
- minimal: it gives back only the cells and rows the file changed, by key and compare-and-set, so nothing written since
  is overwritten or resurrected — what O1 cannot do.
- enforced: the lint refuses a lossy file that carries neither `@preserve` nor `@irreversible`; forgetting is a red
  build, not a lost column.
- proven per file: the round-trip proof seeds rows, runs Apply → Rollback and Apply → `@restore`, and compares the
  preserved columns row by row; dev runs every apply on every deploy before prod.
- one implementation: in the engine every image carries, on PostgreSQL 16 and 18; authors write a header line, not
  locking SQL.
- backstopped: L2 and L3 fail independently of the author and the engine.

### 4.3 Limits

- rows inserted after the change have no before-image: a restored column reads NULL or its default there, so the
  older release must tolerate NULL in rows the newer one created.
- a return through `rollback --to L` also runs the newer release's expand inverses, dropping what it wrote into its own
  new columns and tables (IR6); a forward `@restore` loses nothing.
- the copy holds writers for its length inside the step: seconds at today's sizes (no external users); `plan` should
  report an estimate from `pg_class` before a deploy (*proposed*).
- backups live in the product database: they ride every snapshot and backup, and the planned dev refresh from a
  redacted prod copy (M18) must drop `migration_backup`.
- personal data in a backup outlives an erasure unless the erasure scrubs backups too (IR8).

---

## 5. What changes

### 5.1 be sdk — `src/Data/Migrations/`, `src/Testing.Data/Migrations/`

| # | Change | Seam |
|---|---|---|
| 1 | directives `@preserve <table>[(<columns>)]` (repeatable), `@restore <NNN> <table>(<columns>)`, `@irreversible <reason>`; an unknown directive already refuses | `MigrationHeaderParser.cs`, `MigrationHeader.cs` |
| 2 | the engine-owned schema `migration_backup` per database: `entries` plus one table per preserve; outside every set's owner marker and the schema fingerprint (M58) | `PostgresMigrationDialect.cs` beside `EnsureHistoryTableAsync`, `MigrationSchemaOwnerStore.cs` |
| 3 | apply: lock, copy, run, diff, catalog row, inside the file's batch | `MigrationRunnerService.cs` apply loop, `MigrationTransactionScope.cs` |
| 4 | rollback: the restore after each `Rollback.sql`, in its transaction; refuse a needed missing backup without `--accept-loss`; restored and skipped counts in the event row (M61) | `MigrationRunnerService.cs:627-642` (`RollBackOneAsync`) |
| 5 | `rollback --to N --dry-run`, read-only: per contract above N, whether it restores, from which backup, with what loss | `Commands/MigrateCommandBuilder.cs`, `Commands/MigrateCommandRunner.cs` |
| 6 | `migrate-result` and `check --json` carry held backups and restore counts; `sets --json` marks each contract `preserved` or `irreversible` | `MigrateRunResult.cs`, `MigrateSetContract.cs`, `MigrationSetDescriber.cs` |
| 7 | the purge at `apply` past retention (IR2), with an event row | `MigrationRunnerService.cs` |
| 8 | lint rule `preserve-lossy`: `DROP TABLE`, `DROP COLUMN`, `DROP TYPE`, `TRUNCATE`, `DELETE`, `ALTER COLUMN … TYPE` and an `UPDATE` not bounded by `WHERE <set column> IS NULL` need `@preserve` covering the table, or `@irreversible`; above each set's cutoff, contract or not; `-- lint-allow:` suppresses with a reason | `Lint/MigrationLint.cs`, `Lint/MigrationLintRules.cs` |
| 9 | round-trip proof: per preserving file, a fixture in the migrations tier (`Fixtures/NNN-name.sql`, *proposed*) inserts rows before it; the proof runs Apply → Rollback and Apply → `@restore` and compares the preserved columns | `MigrationIdempotencyProof.cs`, `MigratorHarness.cs` |
| 10 | lane C: a background migration's batches preserve into the same catalog, so `bg rollback` restores (M63) | `src/Jobs/` |

### 5.2 Wheelhouse — runner and console

- the migrate step runs unchanged: preserving happens inside `apply`.
- rollback gate (M15): when the older release's `check` refuses, the runner asks the leaving release's images, still
  local, for `rollback --to <older level> --dry-run --json` per set; levels come from the older manifest's
  `migrationSets` (M78). When every contract above is restorable, the refusal names two ways back: return with
  restore, or the snapshot. Older images need no new code: only the leaving image reads the backups.
- "Return with restore", an operator job on the product page, typed target ID on prod, audited:
  1. the leaving release's `migrate rollback --set s --to L --confirm <db>` per item, in reverse `migrate:` order, so
     a set that keys into another rolls back first
  2. a gated return to the older release, whose `check` now reads `current`
  - two steps, because a rollout never runs `rollback` (M2); errors last only between step 1 and the swap.
- the automatic restore after a failed rollout: the same sequence once IR4 allows it; until then it refuses as today,
  naming both ways back.
- rollback risk (v0.5) per release, from the manifest: `compatible` (expands only above the older level), `restorable`
  (every contract preserves), `snapshot` (an `@irreversible` or unmarked contract).
- snapshot step unchanged; once PITR exists, a restore point before the migrate step, its LSN in the job record.
- `self-deploy.py` `gated()`: unaffected; its forced `rollbackCompatible` goes with v0.7 Iteration 9.

### 5.3 `rollbackCompatible` and gated returns

- `rollbackCompatible` keeps its narrow role: the fallback for a release with no `migrate:` item, and Wheelhouse's own
  forced flag until Iteration 9 drops it.
- a release with `migrate:` gets three gate answers instead of two:
  - may run — the older image's `check` exits `0`
  - restorable — the leaving image's dry run restores every contract above the older level
  - refused — the snapshot or PITR is the way back
- M20's "a same-release contract says `rollbackCompatible: false`" becomes "restorable" when every such contract
  preserves (IR3).

### 5.4 Spec and conventions (hub)

- spec § 2 Rollback and compatibility: M2's "rollback runs on prod only when forward fails" gains the restorable
  return; § 3.1 lanes A and B gain § 5.1; § 3.4 gains § 5.2.
- `migrations.md` § Compatibility and § Actions: restorable contracts, `rollback --dry-run`, `--accept-loss`.
- `bespoke-migrations.md` § Markers gains the three directives; § Rollback's "an explicit no-op with an explanation"
  becomes "preserve every lossy file, or mark it `@irreversible`".
- `server-lifecycle.md` § Backups: PITR as the backup form, with `redundancy.md`.

### 5.5 What stays manual

- returning with restore on prod, by typed confirmation, until IR4.
- a whole-snapshot restore: stop services, `pg_restore`, untar volumes (`deployment.md` § Target state and recovery).
- PITR recovery: a side instance, recovery to the restore point, extraction by key — a runbook.
- judging `@irreversible` and its reason, in review.
- rows a restore skipped: the owner reads them in the backup and decides.
- files, blobs, keys and external effects (M42): no database mechanism reaches them.

---

## Points

Each point: the decision, its options, the proposed pick and why.

1. [ ] IR1 — Lossy files: the engine's `@preserve`, required by the lint, with `-- @irreversible <reason>` as the
   opt-out · the snapshot alone (today) · author-written copies → `@preserve`; atomic with the change, restores only
   what changed, enforced and proven per file, while the snapshot rewinds every set.
2. [ ] IR2 — Retention of a backup: K later owner releases and D days, whichever comes later → 3 releases, matching
   the three releases whose images Wheelhouse keeps, and 30 days.
3. [ ] IR3 — Same-release contracts in products (M20): keep them, with `@preserve` required, so the release reads
   restorable · forbid them, contracting a release later like platform apps → keep; breaking changes spare shims for
   users who do not exist, and a header line costs less than a release.
4. [ ] IR4 — The automatic restore after a failed rollout: return with restore automatically (a rollout running
   `rollback`, against M2) · an operator job only, typed on prod → operator only until a rig drill proves it, then
   automatic on dev, then prod.
5. [ ] IR5 — Restore conflicts, a row changed after the migration: newer writes win, the row skipped and reported ·
   the backup wins → newer writes win; a restore must not undo users' work.
6. [ ] IR6 — A return also runs the newer release's expand inverses, losing what it wrote into its own tables: accept
   it, and prefer a forward `@restore` once a release has served for hours · build a contract-only revert, which leaves
   a gap in history that M56 refuses → accept.
7. [ ] IR7 — PITR (L3): build the WAL archive and base backups now, before the first product with external users ·
   with redundancy's storage role · not at all → now, on both hosts; the off-host storage is a bill only the owner
   approves, and the provider is the owner's pick.
8. [ ] IR8 — Personal data in backups: an erasure also scrubs `migration_backup` rows by key · personal columns are
   never preserved, always `@irreversible` → scrub; Identity already scrubs erased rows in place (M5), and one more
   table keyed by the same id costs little.

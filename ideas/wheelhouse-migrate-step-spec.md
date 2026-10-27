# Wheelhouse — Migrations as a Rollout Step

*Last updated: 2026-10-27*

> A product declares which service's image migrates its database; Wheelhouse runs that image's `migrate` command in a
> one-off container after the images are pulled and before any service restarts, records what it applied, and fails
> the rollout cleanly when it cannot. It builds Wheelhouse's backlog row "Run each app's migrations as a rollout step
> and show their state" (user decision 2026-10-14) and Identity's Q57 (production migrates in an explicit deploy step).
>
> **Status:** spec for the Wheelhouse chat to build, 2026-10-27. First consumer: the Identity service, whose image
> already ships `dotnet Identity.Api.dll migrate`. Identity's first deployment waits for this step.

## Problem

- The be sdk's boot helper (`MigrateBespokeOnStartupAsync`, core `10.0.82-beta` and later) applies migrations only on
  a local run; a deployed boot verifies the schema read-only and refuses to start while a set is behind.
- Descriptor 2 has no step that runs a command before the new image serves, so a release that adds a migration cannot
  boot on a target until someone runs `migrate` by hand.
- Wheelhouse already pulls, snapshots (prod), restarts in waves and verifies; the migrate step slots between pull and
  the first wave, reusing the one-off-container mechanics of the dev check (`verify_release`).

---

## Descriptor contract

A service that owns migrations declares `migrate`; most products declare it on one backend service.

```yaml
services:
  identity:
    migrate:
      command: [dotnet, Identity.Api.dll, migrate]   # replaces the entrypoint, as `verify.command` does
      timeout: 10m                                   # default 10m; 10s-60m
```

| Key | Default | Meaning |
|---|---|---|
| `services.<name>.migrate` | none | Run `command` from this service's release image before the service restarts |
| `services.<name>.migrate.command` | — | The command, entrypoint included; required |
| `services.<name>.migrate.timeout` | `10m` | Longer fails the step; `10s`–`60m` |

- must keep the command idempotent: exit `0` when it applied migrations or found the schema current.
- must use the exit codes below, so Wheelhouse can tell a refusal from a broken script.
- must keep every migration expand-only while the release before it may still run: the old containers keep serving
  during the step, and a rollback boots the older image on the newer schema (expand, then contract one release later).
- may declare `migrate` on several services; they run in dependency order, each before its own wave.
- must pin the pipelines release that accepts the key (below); an older generator refuses it.

### Image contract

| Exit | Meaning | Rollout |
|---|---|---|
| `0` | applied, or already current | continues |
| `1` | refused: drift, orphaned history, another owner's schema, a missing setting | fails before any restart |
| `2` | a script failed; its batch rolled back | fails before any restart |
| other, or timeout | the command crashed or hung | fails before any restart; a timeout stops the container |

- The last output line starting `migrate-result ` carries a JSON summary the runner keeps:
  `migrate-result {"sets":[{"name":"identity","applied":["002-oidc"],"level":"current"}]}`.
- The command prints no secret: no connection string, no setting value.
- The be sdk provides this command for every .NET product (below), so products write one line, not the contract.

---

## Runner behaviour

Order inside one deployment job (`runner.py`, the deploy job's steps):

| # | Step | Today | With this spec |
|---|---|---|---|
| 1 | Render settings, Check target | yes | unchanged |
| 2 | Snapshot data (prod) | yes | unchanged: the restore point precedes the migration |
| 3 | Pull images | yes | unchanged |
| 4 | **Migrate `<service>`** | — | new: one step per declaring service whose image changed |
| 5 | Start waves, Start containers, Verify services, Publish sites, Probe sites | yes | unchanged |
| 6 | Verify end to end (dev) | yes | unchanged |

### The one-off container

| Fact | Value |
|---|---|
| Image | the service's new release image, `--pull never` (step 3 pulled it) |
| Command | `migrate.command`, as the entrypoint (same as `verify`) |
| Settings | the service's rendered settings file, mounted at its `settings.file` path: the migration needs the connection string the service gets |
| Environment | what the service gets: `DEPLOY_ENVIRONMENT`, and the .NET environment when `dotnetEnvironment: true` |
| Volumes | the service's named volumes at their mount paths (a SQLite file lives there) |
| Network | the platform network, so `needs: [postgres]` databases answer |
| Limits | the service's `memory`; `--cap-drop ALL`, `no-new-privileges`, the image's user |
| Name, label | `<project>-migrate-<service>-<job id 8>`, label `wheelhouse.migrate=<project>`; removed after it exits |

### When it runs

| Situation | Step |
|---|---|
| the service is added, or its image changed | runs |
| the image is unchanged (a settings-only change, a redeploy) | skipped, "image unchanged" |
| a rollback, or a deploy of a release older than the target's current one | skipped, "older release: schema stays" — the older image boots on the expanded schema |
| a prod promotion | runs, with the very image dev ran |
| no service declares `migrate` | no step at all; bundles build byte for byte as before |

- A failed or timed-out step fails the job before any container restarts, so the old release keeps serving; the job
  records `reason` = "Migrate `<service>` failed (refused | script failed | crashed | timed out): `<last line>`".
- The database is unchanged after a failure, because the be sdk applies a batch in one transaction; a
  `-- @no-transaction` file is the exception the step's detail names when the summary reports it.
- One deployment per target already holds `deployment_lock`, so two migrations never race on one target; the be sdk's
  advisory lock covers PostgreSQL replicas.
- SQLite: the step migrates while the old container holds the file open; the migrator's write lock and busy timeout
  cover the brief overlap.
- Rollback scripts never run here. Undoing a migration is a separate, confirmed operator action (later; `wow-migrate
  rollback` against the target's database), as the backlog row says.

---

## What Wheelhouse records and shows

- The job record gains `migrations`: per declaring service, `status` (`applied` · `current` · `skipped` · `failed`),
  `exitCode`, `seconds`, the parsed `migrate-result` sets, and the output's last line.
- The live rollout shows the step like the others: "Migrate identity: 1 applied (002-oidc) in 3s" or "current".
- The product page shows each environment's schema from its latest successful job: set, level, newest applied label.
  The app database's own history table stays the authority; Wheelhouse keeps what it saw in the job history and never
  a second table.
- An audit entry is not needed: the deployment job is already audited.

---

## Changes outside Wheelhouse

| Where | Change | Order |
|---|---|---|
| be sdk | a `migrate` command helper for hosts (`app.RunMigrateCommandAsync(args)` or similar): calls `MigrateBespokeForDeployAsync`, maps the result to exit `0`/`1`/`2`, prints the `migrate-result` line | 1 |
| be sdk | a deployed boot tolerates `Ahead` (a newer schema than this build) with a warning instead of refusing, so a rollback after a migration boots; `Behind`, `Drifted`, `Orphaned` and owner conflicts still refuse | 1 |
| pipelines | descriptor 2 accepts `services.<name>.migrate`; `deploy.schema.json`; `release.json` carries `migrate` (`command`, `timeoutSeconds`) per service; a minor release (`v0.11.0`) | 2 |
| wow-two-ws conventions | `deploy-descriptor.md`: the key, the image contract and the expand-only rule; `migrations.md` § Lifecycle points at it | 2 |
| Wheelhouse | runner step, job record, rollout and product-page display; rehearsal rig coverage | 3 |
| Identity | `deploy.yml` declares `migrate` on `identity`, replacing its own exit-code mapping with the be sdk helper | 4 |

- Identity's `HostConfiguration.MigrateAsync` already maps `0`/`1`/`2`; the helper moves that into core so every
  product shares it.

---

## Tests

- Runner unit tests: the plan places the step after pull and before the first wave; skipped when the image is
  unchanged, on a rollback and for an older release; the container gets the settings mount, environment, volumes,
  network and limits above; exit `1`, `2`, a crash and a timeout each fail the job before any restart, with the right
  reason; `migrate-result` parsing tolerates a missing or malformed line.
- Rehearsal rig: the canary declares `migrate` with a SQLite volume and a PostgreSQL database; a release adding a
  migration deploys, a release with a broken script fails while the old release keeps serving, and a rollback boots
  the older image on the newer schema.
- Generator tests: the key validates, defaults apply, a bad timeout or an empty command is refused, and a descriptor
  without the key builds the same bundle as before.

---

## Open

1. Command form: `command` replaces the entrypoint, as `verify` does · arguments appended to the image's entrypoint
   → replace, one rule for both one-off containers.
2. Rollback across a migration: the older image boots on the newer schema (expand-only rule, `Ahead` tolerated) ·
   rollback runs the down scripts → boots on the newer schema; down scripts stay a separate operator action.
3. Prod rehearsal: run the migration with `--dry-run` against prod before promoting · trust the dev run and the
   snapshot → trust dev and the snapshot in v1; a dry run is a later option (the be sdk already has
   `DryRunPendingAsync`).

# Identity — migrations changes

*Last updated: 2026-10-28*

What the [migrations spec](migrations-spec.md) changes in `wow-two-sdk-beta.identity`, for the Identity chat. Point ids
cite the [analysis](migrations-analysis-2026-10.md); the settled rules live in the migrations conventions
(`conventions/development/backend/dotnet/core/mla/domains/persistence/migrations/`). Paths are relative to
`engineering/codebase/identity.backend-services/`.

## Status

- ✅ be sdk command tree and engine: `WoW2.Sdk.Beta.Be` `10.0.89-beta`
- ✅ conventions and descriptor schema in the hub (`9e006fc`…`d4c4b02`)
- ✅ Identity: § 1 adopted on be sdk `10.0.90-beta` — `402ee0f`, idempotency cutoff `1c3a117`
- ⬜ pipelines: `migrate:` list and pinned foreign images (spec phase 2)
- ⬜ Wheelhouse: the migrate step, rollback gate and bridge (spec phases 3–4)

---

## 1. Now, on the published be sdk

| # | Change | Where | Points |
|---|---|---|---|
| 1 | Re-pin `BackendSdkVersion` 10.0.86 → `10.0.89-beta` | `Directory.Packages.props:11` | — |
| 2 | Replace the hand-made `migrate` with the SDK verb tree (namespace `WoW.Two.Sdk.Beta.Be.Data`): after `Build()` and before `Configure`, `if (MigrateCommand.IsCommand(args)) return await app.RunMigrateCommandAsync(args);`; then delete `MigrateAsync` and its exit mapping. The tree answers `check · plan · apply · seed · sets · rollback · forget · repair · baseline · claim · locks · unlock`, exits `0` done/current · `1` refused · `2` failed · `3` busy, guards writing verbs with `--confirm <database>`, and ends stdout with one `migrate-result` line; a bare `migrate` runs `apply` then `seed`. `Migrations:ConnectionString` connects the run with no extra call | `service/Identity.Api/Program.cs:16-17`, `Configurations/HostConfiguration.cs:59-80` | M10, M11, M17, M37, M57 |
| 3 | Add `identity_users.deleted_at timestamptz NULL` in a new expand file (`004-…`); make the user-name and email unique indexes partial, `WHERE deleted_at IS NULL`; deleting a user soft-deletes it, and erasure scrubs personal columns in place, never deleting the row, so a product's `RESTRICT` key never blocks | `packages/Module/Migrations/Postgres/`, the user store | M5, M75 |
| 4 | Publish the referenceable tables on the set's `MigrationOptions`: `AddReferenceableTable("identity_users", ["id"], [<readable columns>])`, the same for `identity_organizations`; a product declares `.DependsOn("identity", <level>)` on its own set, and `apply` refuses before any SQL while `identity` is missing or below that level | `packages/Module/Core/IdentityDatabaseServiceCollectionExtensions.cs:56-59`, `IdentityDatabaseOptions.cs` | M79 |
| 5 | Lift the foreign-key ban in the docs: products may key into Identity's published tables inside one database. Never edit an applied `Apply.sql` (its checksum would drift); record the reversal in T10 and the architecture docs instead | `research/identity-analysis-2026-10/t10-schema-migrations.md:170`, `:336`; the `001-accounts/Apply.sql:9-10` comment stays | M5 |
| 6 | Keep writes Identity's: products map published tables read-only and write through the module or the API | docs | M7 |
| 7 | Change published tables, keys and readable columns by expand and contract only; they join the client contract the previous client's conformance suite proves | migrations, `Identity.Tests.Conformance` | M5, M20, M21, M31 |
| 8 | Put any contract in its own file headed `-- @contract since=vX.Y` (Identity's library release that no longer reads or writes what it removes) | migrations | M21, M76 |
| 9 | Migrations tier on `…Be.Testing.Data`: the lint (`Migrations/Lint/`: expand-only from a cutoff, lock-risk rules, published tables; suppress per file with `-- lint-allow: <rule> <reason>`), the idempotency mode (`MigrationIdempotencyProof`: Apply → Rollback → Apply, Apply → Apply, Rollback → Rollback) and an E2E test of the verbs on the verb harness (`Migrations/Verbs/`: exits, reruns, a write-free `check`, the `migrate-result` line) | `tests/Identity.Tests.Migrations`, `tests/Identity.Tests.E2E` | M22, M53, M57, M59 |
| 10 | Seeds: OIDC clients and the first admin stay in configuration (`Identity:Server:Clients:N`); reference rows the code needs in every environment become idempotent upserts in the set or an SDK seed file | — | M26, M51 |
| 11 | New columns follow the type rules: snake_case, app-made uuid v7, `*_at timestamptz`, `*_on date`, native enums with snake_case labels, `varchar(n)` limits, unique `lower(…)` indexes, no `citext`; `normalized_*` stay, since ASP.NET Identity reads them | — | M64–M75 |

Re-pin notes — breaking changes in this be sdk release; a scan of Identity's code on 2026-10-28 found none it uses
(it reads `IMigrationSetRegistry.GetOptions` only):

- `ISoftDeletable.IsDeleted` removed; `HasSoftDelete` takes `DateTimeOffset?`.
- `MigrationLevelState.Ahead` split into `AheadCompatible` and `AheadIncompatible`; a compatible `Ahead` boots with a
  warning.
- `IMigrationSetRegistry.GetBroker` and `IMigrationEngine.DescribeAsync` are new interface members.
- `wow-migrate`: `status` and `verify` removed, `--confirm <database>` replaces `--force` and the prompt, `rollback`
  needs `--to`, a guard refusal exits `1`.
- An unknown `-- @` header directive refuses; a `-- @requires` file refuses until background migrations ship.

## 2. After pipelines ships `migrate:` and pinned images

| # | Change | Points |
|---|---|---|
| 12 | `deploy.yml` gains a product-level `migrate:` item: `{ service: identity, command: [dotnet, Identity.Api.dll, migrate], timeout: 10m }` | M9, M43 |
| 13 | The image answers `docker run --rm --network none <image> migrate sets --json` with no settings file | M78 |
| 14 | Settings gain the migrate key `Migrations:ConnectionString` (the runtime role in v1) | M8 |

## 3. After Wheelhouse's step and bridge

| # | Change | Points |
|---|---|---|
| 15 | Identity takes the step in rank 2 with Files, in one release: the command, the step, then the SDK bump | M48 |
| 16 | A per-product instance is a service in the product's `deploy.yml` — the Identity image pinned by tag, its settings — listed in the product's `migrate:` before every item whose set depends on `identity`; its set lives in the product's database, `<product>_{env}`, schema `identity` | M6, M28, M77 |
| 17 | A shared instance (wow2's Identity for the platform apps) is a Wheelhouse product of its own, with its own database, server and rollout; tenants are rows; consumers key it by id and clean up on `PersonDeleted` | M6, M29, M55, M80 |
| 18 | Ocharo's Identity arrives as Ocharo's first `migrate:` item when `access.*` moves (Q66) | M77 |

## 4. Decisions to record in the identity analyses

- Q5 · B: holds for shared instances only; a per-product instance's set lives in the product's database (M6, M77).
- Q63 (B): reopened for per-product instances, which take option A — a service of the product (M77).
- Q64's "SQLite stays Form 1 only": falls; PostgreSQL only (M40), already done 2026-10-27.
- T10's ban on foreign keys into the schema: reversed (M5).

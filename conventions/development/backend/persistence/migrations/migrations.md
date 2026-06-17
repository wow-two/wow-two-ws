# Migrations

*Last updated: 2026-06-16*

> Picks the migration runner for a wow-two product — `Bespoke` (default), `Ef`, or `DbUp` — and the operational contract all three share; scoped to
> backend persistence, not schema design.
> Purpose — one runner per product, registered with one DI call, so apply/rollback/journal behavior is uniform and schema ownership is explicit.
> Use case — wiring a product's DB-migration host, or deciding whether the schema lives in raw SQL, the EF model, or a forward-only journal.

---

## Strategy

Three runners ship as folders in the backend-beta mono-lib under `src/Data/Migrations/`. Pick one per product; don't mix.

- **`Bespoke` (default)** — register `AddDatabaseBespokeMigrations(sqlAssembly)` (embedded) or `AddDatabaseBespokeMigrations(migrationsRoot)` (filesystem,
  CLI/dev). Raw `.sql` `Apply`/`Rollback` pairs; schema owned by SQL, EF a pure mapper. Default for wow-two products — own the schema, dev rollback,
  embedded + filesystem off one folder.
- **`Ef`** — register `AddEfMigrationsRunner<TContext>()`. Code-first: `DbContext` owns the schema, `MigrateAsync` at boot. Pick when the consumer is
  code-first and no raw-SQL ownership is wanted.
- **`DbUp`** — register `AddDbUpRunner(configure)`. Forward-only embedded scripts, no rollback. Pick for the simplest legacy forward-only journal —
  no squash or dev rollback needed.

Registration detail:

- `Bespoke` → `AddDatabaseBespokeMigrations` (design-stage — engine proven in `smart-qr`, extraction pending; contract in `bespoke-migrations.md`).
- `Ef` → `AddEfMigrationsRunner<TContext>` wires `EfMigrationsHostedService<TContext>` → `context.Database.MigrateAsync(ct)`; tuned by
  `EfMigrationsOptions` (`Enabled`, `MaxConnectAttempts`, `ConnectRetryDelay` — Docker boot-race retry).
- `DbUp` → `AddDbUpRunner(Action<DbUpOptions>)` wires `DbUpHostedService`; `DbUpOptions` (`ScriptsAssembly`, `ScriptsNamespacePrefix`,
  `UpgradeEngineFactory`, `ConnectionString`); provider via `DbUpProviderFactories.Postgres` / `.SqlServer` / `.MySql`.

---

## Shared concepts

Every strategy honors the same operational contract:

- **Apply + rollback** — every strategy applies forward; rollback varies (`Bespoke` ships explicit `Apply`/`Rollback` pairs · `Ef` uses `Up`/`Down` ·
  `DbUp` is forward-only, no rollback). *How* to write the SQL → `migration-dialects.md`.
- **Roll forward by default; rollback is a guarded recovery op** — never *edit* an applied migration (that's drift); fix forward. Rollback (where
  supported) is allowed in **any** environment incl. prod — gated by an explicit enable + target-DB confirm — for when a forward-fix isn't viable.
- **History / journal table** — each runner records applied migrations in its own table so re-apply is a no-op (`Bespoke` → `migration_history`;
  `DbUp` → its journal; `Ef` → `__EFMigrationsHistory`).
- **Embedded vs filesystem source** — runtime hosts embed scripts in the product assembly (no deploy-time filesystem); CLI/dev reads on-disk (edit +
  apply live, no rebuild). `Bespoke` does both off one folder; `DbUp` is embedded-only (`ScriptsAssembly`).
- **Idempotent boot-apply under a lock** — apply is safe to call from every host; a DB-level lock serializes concurrent applicants (first applies,
  rest no-op). `Bespoke` uses a Postgres advisory lock; `Ef`/`DbUp` rely on `MigrateAsync` / journal idempotency.
- **Dev auto vs prod explicit** — dev applies on boot (gated to `IsDevelopment()` in the hosted-service adapter); prod applies via an explicit
  action (CLI / init step / HTTP endpoint), never silently on boot.

---

## Leaf docs

This index routes; the leaf docs carry the detail.

- `bespoke-migrations.md` — `Bespoke` strategy product contract: layout, registration, drift/orphans, dual-ship csproj.
- `migration-dialects.md` — authoring `Apply`/`Rollback` pairs: reserved-word quoting, `-- @no-transaction` idempotency, native PG enums, ordinals.
- `ef-migrations.md` — `Ef` code-first runner: `AddEfMigrationsRunner<TContext>`, boot-race retry options.
- `dbup-migrations.md` — `DbUp` forward-only runner: `AddDbUpRunner`, provider factories, embedded scripts.
- `migration-tooling.md` — `dotnet tool` CLI host shape: packaging, arg parsing, exit codes, confirmation guards (`smart-qr-migrate` first consumer).

> Engine internals (advisory lock, normalized checksum, one-engine/three-hosts) live in the SDK design doc `src/Data/Migrations/Bespoke/bespoke.md`.

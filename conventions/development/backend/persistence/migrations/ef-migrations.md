# EF Core Migrations

*Last updated: 2026-06-16*

> EF Core code-first strategy — `DbContext` owns the schema, generated C# migrations ship in `Migrations/`, applied on boot by a hosted runner.
> Purpose — keep schema co-evolving with the model so one edit-regenerate-ship loop covers both, no hand-written DDL drift.
> Use case — reach for it on a C#-first product with a single owning context and no external schema-first DB dictating shape.

---

## When to pick

- Rapid C#-first product where the schema **co-evolves with the model** — edit entities, regenerate the migration, ship.
- Single owning `DbContext`; no external/legacy schema-first DB driving the shape.
- Opposite of the raw-SQL strategy in `migrations.md` (schema-first — `Migrations/*/Apply.sql` is the owned truth, EF only maps over it).
- **One repo picks one** — code-first OR schema-first, never both.

---

## Register

- One call wires a startup runner per context — `AddEfMigrationsRunner<TContext>` in `EfMigrationsServiceCollectionExtensions`:

```csharp
services.AddEfMigrationsRunner<AppDbContext>();                       // defaults
services.AddEfMigrationsRunner<AppDbContext>(o => o.Enabled = false); // out-of-band apply
```

- Registers `EfMigrationsHostedService<TContext>` (an `IHostedService`) + validates `EfMigrationsOptions` on start
  (`AddOptions<EfMigrationsOptions>().ValidateOnStart()`).
- `TContext : DbContext` — the context that owns the schema and carries the generated `Migrations/` C# files.

---

## Apply on boot

- `EfMigrationsHostedService<TContext>.StartAsync` calls `context.Database.MigrateAsync(...)` — applies all pending migrations,
  idempotent (already-applied no-op).
- Resolves `TContext` from a fresh DI scope (`CreateScope`); logs per attempt.
- Connect-race resilient — retries up to `MaxConnectAttempts`, sleeping `ConnectRetryDelay` between tries (the classic "DB not ready yet"
  Docker startup race). Final attempt rethrows.
- `Enabled = false` short-circuits before any DB touch — logs "disabled" and returns.

---

## `EfMigrationsOptions`

| Flag | Default | Purpose |
|---|---|---|
| `Enabled` | `true` | Master switch. Flip `false` in prod when migrations apply out-of-band (CI step, ops job). |
| `MaxConnectAttempts` | `10` | Connect tries before giving up — mitigates Docker DB-not-ready race. |
| `ConnectRetryDelay` | `2s` (`TimeSpan`) | Wait between attempts. |

- `init`-only record — set inline in `configure` or bind from config.

---

## Authoring a migration

- The `DbContext` + entity config (`OnModelCreating` / `IEntityTypeConfiguration<T>`) is the source of truth — **edit the model,
  never the DB by hand**.
- Generate the diff against the current model, then ship the C# migration files:

```bash
dotnet ef migrations add AddServiceColumn   # diffs model → Migrations/<ts>_AddServiceColumn.cs
dotnet ef migrations remove                  # undo the last unapplied migration
```

- Run from the project owning the `DbContext`; CLI tool wiring → `migration-tooling.md`.
- Don't hand-author SQL — let the model diff produce `Up`/`Down`. (Raw SQL escape hatch only for what EF can't express,
  inside the generated migration.)
- Apply happens automatically at boot via the runner above — no separate `dotnet ef database update` step for dev/runtime hosts.

---

## Dev auto vs prod explicit

- Dev: `Enabled = true` → schema follows the model on every boot.
- Prod: set `Enabled = false`, apply out-of-band so a deploy never silently mutates schema on startup — mirrors the SQL strategy's
  dev-auto / prod-explicit split in `migrations.md`.

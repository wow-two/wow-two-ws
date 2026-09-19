# Test Databases

*Last updated: 2026-09-10*

> Which database a backend test runs against, and how the tier picks it — Postgres by default,
> SQLite as a switchable speed fallback.
> Purpose — fidelity by default, with a no-Docker fast lane when the Postgres suite gets slow.
> Use case — writing any DB-touching test, or moving a slow suite onto the SQLite lane.

## Test tiers

Pick the tier by what the test exercises; each MUST use the SDK harness, never a hand-rolled fixture.

- **pure-logic** — evaluators, formatters, mappers, generators → **no database**; a plain unit test, no harness.
- **repository / handler** — reads/writes through `DbContext` → `RelationalTestDb<TContext>`.
  - ships in `WoW.Two.Sdk.Backend.Beta.Testing.Data`.
- **E2E (host-boot)** — real HTTP through the real pipeline.
  - `MultiHostFixture` + `WebApiTestHost<T>` + `PostgresFixture`, Respawn resetting between tests.
- **migrator-engine** — apply / rollback / drift over real SQL.
  - `MigratorPostgresFixture` + `MigratorHarness`, both in `Testing.Data`.

- E2E + migrator tiers are Postgres-only — they boot the real engine.
- the SQLite switch below applies only to the **repository / handler** tier.
- E2E-first rationale + the full integration stack live in [testing](../../../../../shapes/service/architecture/clean/testing.md).
- this doc governs only the DB-selection seam.

---

## Database default — Postgres

Postgres is the fidelity baseline — the engine closest to production, so test behavior matches prod.

- a DB-touching test MUST run on Postgres by default (§ *The switch*).
- while on SQLite a test MUST NOT assert behavior that diverges between the engines.
  - `jsonb`, `xmin` concurrency, `ON CONFLICT`, sequences, snake_case edge cases — those belong on Postgres.
- use `RelationalTestDb<TContext>` for the repository / handler tier.
  - it owns the provider, the container / connection, and the per-test reset.
- **subclass per app** — override `CreateContext(DbContextOptionsBuilder<TContext>)`, then construct the context.
  - the builder arrives already pointed at the test provider.
  - apply the app's model conventions (`UseSnakeCaseNamingConvention`) + interceptors (audit) there.
- the base supplies the rest — `NewContext()` for a fresh context, `ResetAsync()` to empty between tests.
- expose the subclass as an xUnit `ICollectionFixture` so the container / connection is shared across the suite.

```csharp
public sealed class AppTestDb : RelationalTestDb<AppDbContext>
{
    protected override AppDbContext CreateContext(DbContextOptionsBuilder<AppDbContext> builder) =>
        new(builder.UseSnakeCaseNamingConvention().Options);
}
```

---

## Provider selection

- must let each `RelationalTestDb<TContext>` instance own its provider.
- must default the parameterless fixture constructor to `DatabaseProvider.Postgres`.
- must pass `DatabaseProvider.Sqlite` to the base constructor for a SQLite suite.
- must not use static or process-global provider selection.
- must read the provider only through the `Testing.Data` fixture.

---

## Adopting SQLite

SQLite is a **speed** fallback — in-memory, no Docker — **not** the fidelity baseline.
Reach for it only when the Postgres suite is the bottleneck.

- a test depending on a Postgres-only feature MUST stay on Postgres.
- to make a suite SQLite-capable, pass `DatabaseProvider.Sqlite` to `RelationalTestDb<TContext>`.
  - **nothing else changes**; the same fixture runs on either engine.
- a suite that can't go green on SQLite relies on PG-only behavior.
  - keep it on Postgres rather than weakening the assertion.

---

## How to switch

```csharp
public sealed class AppTestDb : RelationalTestDb<AppDbContext>
{
    public AppTestDb() : base(DatabaseProvider.Sqlite) { }

    protected override AppDbContext CreateContext(DbContextOptionsBuilder<AppDbContext> builder) =>
        new(builder.Options);
}
```

- **→ SQLite** — pass `DatabaseProvider.Sqlite` from that suite's fixture.
- **→ back to Postgres** — remove the constructor; the base default is Postgres.
- **when to flip** — default to Postgres for fidelity.
  - switch to SQLite only when the suite gets slow (~2–3 min+) **and** no test relies on PG-only behavior.

---

## E2E host-boot — point the host at the test container

The E2E tier boots the real host through `WebApiTestHost<T>` / `WebApplicationFactory`.

- must inject each host's connection string through `ConfigureConfigurationHook`.
- must add an in-memory value for `DatabaseSettings:ConnectionString`.
- must evaluate the fixture's connection string when the host builds, after its container starts.
- must not mutate process environment variables to configure a test host.
- must keep configuration values on the host that consumes them.
- this is the host-boot analogue of the repository tier's `RelationalTestDb` seam.
  - same goal (point the DB at the test instance), different layer (host configuration vs. fixture-owned context).

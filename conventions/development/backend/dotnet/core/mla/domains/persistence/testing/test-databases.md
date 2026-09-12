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

## The switch — `TestSetupOptions`

The provider is one code-level setting — `TestSetupOptions.Current.Database`, defaulting to Postgres.
No environment variable.

- it defaults to `DatabaseProvider.Postgres`; assign `DatabaseProvider.Sqlite` to flip the whole suite.
- set it **once** before the fixtures start — a `[ModuleInitializer]` in the test assembly is the canonical home.
  - the value is version-controlled, never an external var.
- a suite MAY override `RelationalTestDb<TContext>.Provider` to pin one provider — the future per-suite seam.
  - otherwise it follows `TestSetupOptions.Current`.
- a test MUST read the provider only through the `Testing.Data` fixtures.
- a test MUST NOT hard-code a provider, or new up a `DbContext` against a fixed one.

---

## Adopting SQLite

SQLite is a **speed** fallback — in-memory, no Docker — **not** the fidelity baseline.
Reach for it only when the Postgres suite is the bottleneck.

- a test depending on a Postgres-only feature MUST stay on Postgres.
  - per-test opt-out is a **future** capability, not available yet.
  - the choice is per-run today — the whole suite follows the switch.
- to make a suite SQLite-capable, use `RelationalTestDb<TContext>` — it already branches on the switch.
  - **nothing else changes**; the same fixture runs on either engine.
- a suite that can't go green on SQLite relies on PG-only behavior.
  - keep it on Postgres rather than weakening the assertion.

---

## How to switch

```csharp
// one place in the test project, e.g. TestSetup.cs
internal static class TestSetup
{
    [ModuleInitializer]
    internal static void Init() => TestSetupOptions.Current.Database = DatabaseProvider.Sqlite;
}
```

- **→ SQLite** — add the module initializer above, or set
  `TestSetupOptions.Current.Database = DatabaseProvider.Sqlite` once, then run the tests.
- **→ back to Postgres** — remove that line (or set `DatabaseProvider.Postgres`); the default is Postgres.
- **scope** — it's a committed code change, so flip it on a branch when measuring and keep `main` on Postgres.
- **when to flip** — default to Postgres for fidelity.
  - switch to SQLite only when the suite gets slow (~2–3 min+) **and** no test relies on PG-only behavior.

---

## E2E host-boot — point the host at the test container

The E2E tier boots the real host (`WebApiTestHost<T>` / `WebApplicationFactory`), and the host's
`AddPostgresPersistence<TContext>` **resolves the connection string eagerly, at service registration** —
before `WebApplicationFactory.ConfigureAppConfiguration` applies.
Configuration alone is therefore too late: the host migrates against the appsettings default,
and the suite fails with Respawn `"No tables found"`.

- a host-boot fixture MUST publish the container's connection string via **`DB_CONNECTION`, set before the
  host builds**.
  - `AddPostgresPersistence` reads env first (env wins over config), and env is visible at registration time.
- set it in the fixture's `InitializeAsync` — container started, host not yet built.
- must serialize fixtures that change the same environment variable; it is process-global during host construction.
- must save its prior value and restore it on dispose, including failed initialization.
- must not claim restoration prevents overlapping host-build races.
- this is the host-boot analogue of the repository tier's `RelationalTestDb` seam.
  - same goal (point the DB at the test instance), different layer (process env vs. fixture-owned context).

# Test Databases

*Last updated: 2026-06-23*

> What — which database a backend test runs against and how the tier picks it: Postgres by default, SQLite as a switchable speed fallback.
> Purpose — fidelity by default (the test DB matches production) while keeping a no-Docker fast lane for when the Postgres suite gets slow.
> Use case — reach for it when writing any DB-touching test, or when a suite gets slow enough to want the SQLite lane.

## Test tiers

Pick the tier by what the test exercises; each MUST use the SDK harness, never a hand-rolled fixture.

- **pure-logic** — evaluators, formatters, mappers, generators → **no database**; a plain unit test, no harness.
- **repository / handler** — code that reads/writes through `DbContext` → `RelationalTestDb<TContext>` (`WoW.Two.Sdk.Backend.Beta.Testing.Data`).
- **E2E (host-boot)** — real HTTP through the real pipeline → `MultiHostFixture` + `WebApiTestHost<T>` + `PostgresFixture` (Respawn reset between tests).
- **migrator-engine** — apply / rollback / drift over real SQL → `MigratorPostgresFixture` + `MigratorHarness` (`Testing.Data`).

- E2E + migrator tiers are Postgres-only (they boot the real engine) — the SQLite switch below applies to the **repository / handler** tier.
- E2E-first rationale + the full integration stack live in [testing.md](testing.md); this doc governs only the DB-selection seam.

---

## Database default — Postgres

Postgres is the fidelity baseline — the engine closest to production, so behavior under test matches behavior in prod.

- a DB-touching test MUST run on Postgres by default — `TestSetupOptions.Current.Database` defaults to Postgres (see *The switch*).
- while on SQLite a test MUST NOT assert behavior that diverges between the two engines — `jsonb`, `xmin` concurrency, `ON CONFLICT`, sequences,
  snake_case edge cases; those belong on Postgres.
- use `RelationalTestDb<TContext>` for the repository / handler tier — it owns the provider, the container / connection, and the per-test reset.
- **subclass per app** — override `CreateContext(DbContextOptionsBuilder<TContext>)` (the builder arrives already pointed at the test provider) to apply
  the app's model conventions (e.g. `UseSnakeCaseNamingConvention`) + interceptors (e.g. audit), then construct the context.
- the base supplies the rest: `NewContext()` for a fresh context on the active DB, `ResetAsync()` to empty between tests.
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

The provider is a single code-level setting — `TestSetupOptions.Current.Database` — defaulting to Postgres. No environment variable.

- `TestSetupOptions.Current.Database` defaults to `DatabaseProvider.Postgres`; assign `DatabaseProvider.Sqlite` to flip the whole suite.
- set it **once** before the fixtures start — a `[ModuleInitializer]` in the test assembly is the canonical home; the value is version-controlled, not an external var.
- a suite MAY override `RelationalTestDb<TContext>.Provider` to pin itself to a specific provider (the future per-suite seam) — otherwise it follows `TestSetupOptions.Current`.
- a test MUST read the provider only through the `Testing.Data` fixtures — it MUST NOT hard-code a provider or new up a `DbContext` against a fixed one.

---

## Adopting SQLite

SQLite is a **speed** fallback — in-memory, no Docker — **not** the fidelity baseline; reach for it only when the Postgres suite is the bottleneck.

- a test that depends on a Postgres-only feature MUST stay on Postgres — per-test opt-out is a **future** capability, not available yet, so today the
  choice is per-run (the whole suite follows the switch).
- to make a suite SQLite-capable: use `RelationalTestDb<TContext>` — it already branches on the switch, so **nothing else changes**; the same fixture
  runs on either engine.
- if a suite can't go green on SQLite, that's the signal it relies on PG-only behavior — keep it on Postgres rather than weakening the assertion.

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

- **→ SQLite** — add the module initializer above (or set `TestSetupOptions.Current.Database = DatabaseProvider.Sqlite` once), then run the tests.
- **→ back to Postgres** — remove that line (or set `DatabaseProvider.Postgres`); the default is Postgres.
- **scope** — it's a committed code change, so flip it on a branch when measuring and keep `main` on Postgres.
- **when to flip** — default to Postgres for fidelity; switch to SQLite only when the Postgres suite gets slow (~2–3 min+) **and** the tests don't rely on PG-only behavior.

---

## E2E host-boot — point the host at the test container

The E2E tier boots the real host (`WebApiTestHost<T>` / `WebApplicationFactory`), and the host's `AddPostgresPersistence<TContext>` **resolves the connection string eagerly, at service registration** — which runs *before* `WebApplicationFactory.ConfigureAppConfiguration` applies. Injecting the container's connection string through configuration alone is therefore too late: the host migrates against the appsettings default and the suite fails with Respawn `"No tables found"`.

- a host-boot fixture MUST publish the test container's connection string via the **`DB_CONNECTION` environment variable, set before the host builds** — `AddPostgresPersistence` reads env first (env wins over config), and env is visible at registration time.
- set it in the fixture's `InitializeAsync` (container started → before the host builds) and clear it on dispose, so concurrent suites don't leak a connection string into each other.
- this is the host-boot analogue of the repository tier's `RelationalTestDb` seam — same goal (point the DB at the test instance), different layer (process env vs. fixture-owned context).

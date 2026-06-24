# Backend — Testing

*Last updated: 2026-06-24*

> How we test .NET services. Prefer **end-to-end / integration over unit** — run the real flow, mock as little as possible.

## Principle — E2E first, unit only for pure logic

- A service with **few external dependencies** → test it **end-to-end**: real HTTP through the real pipeline, against a **real database**, mocking nothing you can run for real.
- Reserve **unit tests** for **pure, I/O-free logic** (evaluators, formatters, generators) — fast, deterministic, no host/DB.
- Why: handlers/repos are thin; testing them in isolation over an in-memory DB exercises little and hides provider-specific, serialization, auth, and ownership bugs. One E2E test covers the same logic **plus** the wiring — and the cross-service flows units can't see.

## E2E / integration stack

| Concern | Choice |
|---|---|
| Runner | xUnit |
| Host | `WebApplicationFactory<Program>` (in-proc) — one per host; multi-host flows build several on one DB |
| DB | **Testcontainers** real engine (e.g. `postgres:N-alpine`) — **never** SQLite / in-memory for the integration layer (dialect drift hides bugs) |
| Reset | **Respawn** between tests — **exclude the migration-history table** |
| Assertions | one fluent lib (AwesomeAssertions) |
| Time | `FakeTimeProvider` for time-dependent paths |

- **One shared container** per suite (collection fixture); non-parallel within the collection.
- Migrations **auto-apply on host startup** — no separate migrate step.
- Inject the container connection string via config/env override; all hosts point at the same DB.
- **Only stub genuinely-external 3rd-party APIs** (a WireMock fixture). In-proc components (codegen, detectors, queues) run for real.
- **Async work** (background flushers/queues): assert via **poll-with-timeout**, never a fixed `Task.Delay`.
- **Docker required** locally + in CI — this is the pre-ship gate.

## Coverage

Per feature, success **and** the edges (`401` auth, `404` ownership with **no existence leak**, validation, invariants). Goal: edge cases are automated, so the **frontend only smoke-tests the happy path**.

## Layout & naming

- Tests live in a `tests/` folder in the backend solution.
- **Test projects are named `{Product}.Tests.{Type}`** — every test project sits under a shared `.Tests.` prefix; `Type` ∈ {`Unit`, `Integration`, `E2E`}, one project per tier that has tests:
  - **`{Product}.Tests.Unit`** — pure, I/O-free logic (evaluators, formatters, generators, validators in isolation). No host, no DB, Docker-free.
  - **`{Product}.Tests.Integration`** — real DB / infra **below** the HTTP pipeline (a repository or handler over a real `DbContext`).
  - **`{Product}.Tests.E2E`** — the full API over HTTP via host-boot (real Postgres, real pipeline). The **primary tier** — push request-flow coverage here; it catches serialization / mediator / model-binding / filter failures that green handlers miss. Ships a `README.md` noting the Docker prerequisite + coverage.
- A **descriptive `{Type}`** is allowed for a specialized suite that doesn't fit the three tiers — e.g. **`{Product}.Tests.Migrations`** for migrator-engine tests. Keep it a single noun naming the suite's subject.
- **The bare `{Product}.Tests` name is disallowed** — ambiguous about its type. Create a `{Product}.Tests.{Type}` project instead.
- The tier maps 1:1 to the DB-selection tiers in [test-databases.md](test-databases.md): `Tests.Unit` → pure-logic (no DB) · `Tests.Integration` → repository / handler (`RelationalTestDb<TContext>`) · `Tests.E2E` → host-boot (`MultiHostFixture` + `PostgresFixture`).
- Existing apps (`SmartQr.*`, `SecretsVault.*`) are being renamed to match; stragglers get retrofitted.

## Method naming

Pattern — `{Unit}_Should{Expectation}[_When{Condition}]`. PascalCase segments; the `_` separates the three parts (not words). Reads as a sentence: *"{unit} should {expectation} when {condition}"*.

- **`{Unit}`** — the action / method / behaviour under test: `Create`, `GetById`, `Attempt`, `Classify`.
- **`Should{Expectation}`** — the asserted outcome. Integration → `ShouldReturn{Status}` (`ShouldReturn404`); unit → `Should{Behaviour}` (`ShouldReturnCanceled`, `ShouldThrow`).
- **`When{Condition}`** — the scenario under test.

| | Rule |
|---|---|
| must | three-part `_Should…_When…`, PascalCase each segment |
| must | integration names state the HTTP status (`ShouldReturn201`, `ShouldReturn422`) |
| must | the `When` describes behaviour / state, never implementation |
| may | drop `_When…` only when the behaviour is unconditional |

| Layer | Shape | Example |
|---|---|---|
| Integration (E2E) | `{Action}_ShouldReturn{Status}_When{Condition}` | `Create_ShouldReturn422_WhenMedicationDoesNotExist` |
| Unit (pure logic) | `{Method}_Should{Outcome}_When{Condition}` | `Attempt_ShouldReturnCanceled_WhenOperationCanceled` |
| Unconditional | `{Method}_Should{Outcome}` | `Flatten_ShouldCapDepthAtFive` |

✅ `GetById_ShouldReturn404_WhenRecordDoesNotExist` · `Classify_ShouldBeTransient_WhenDbTimeout`
❌ `Attempt_converts_cancellation_to_canceled` (snake, no Should/When) · `Test_Create` · `Should_Work`

## Harness extraction

The **generic** E2E harness (host factory, container fixtures, base classes) **mirrors the backend-beta SDK testing scaffold** (`WebApiTestHost<T>`, `WebApiTestBase<T>`, `PostgresFixture`, `IAsyncTestFixture`, …) with API-identical signatures, so it lifts into the SDK mechanically. **Product-coupled** fixtures (the app's specific multi-host wiring, auth helper, DTO mirrors) stay in the product test project.

Reference implementation: `smart-qr-poc/.../backend/SmartQr.IntegrationTests`.

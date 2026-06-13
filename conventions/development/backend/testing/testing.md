# Backend — Testing

*Last updated: 2026-06-12*

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
- `{Brand}.Tests` — pure-logic units (Docker-free).
- `{Brand}.IntegrationTests` — E2E (Testcontainers); ships a `README.md` noting the Docker prerequisite + coverage.

## Harness extraction

The **generic** E2E harness (host factory, container fixtures, base classes) **mirrors the backend-beta SDK testing scaffold** (`WebApiTestHost<T>`, `WebApiTestBase<T>`, `PostgresFixture`, `IAsyncTestFixture`, …) with API-identical signatures, so it lifts into the SDK mechanically. **Product-coupled** fixtures (the app's specific multi-host wiring, auth helper, DTO mirrors) stay in the product test project.

Reference implementation: `smart-qr-poc/.../backend/SmartQr.IntegrationTests`.

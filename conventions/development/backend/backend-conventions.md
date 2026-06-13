# Conventions — Development — Backend (.NET)

*Last updated: 2026-06-13*

> .NET conventions for every backend service under `wow-two-ws/`. Lookup table — open a file when the
> task touches it; do not pre-read. Organized by **sub-domain** (one folder per concern; scales as the
> surface grows). Repo layout is one level up: [../repo/repo-structure.md](../repo/repo-structure.md).
> How to write a doc here: [authoring.md](authoring.md) (cite symbols + paths, never namespaces).

## Sub-domains

| Folder | Concern | Status |
|---|---|---|
| `code-style/` | Layer-agnostic authoring — files, docs, models | Active |
| `architecture/` | Layering, host wiring, service shape | Active |
| **`persistence/`** | Schema, EF Core, Dapper, entities, migrations | **Focus** |
| `presentation/` | Delivery surface — controllers, CQRS contracts, responses (REST now; GraphQL/gRPC later) | Active |
| `runtime/` | Config binding + launch profiles | Active |
| `foundation/` | Cross-cutting primitives — results, errors, validation, time | Active |
| **`integrations/`** | Outbound HTTP clients + resilience | **Focus** |
| `testing/` | Test strategy + harness | Active |
| `messaging/` · `observability/` · `identity/` · `platform/` | Mediator · logging/tracing · auth · email/jobs/etc. | Proposed (write as built) |

> **Focus (this workstream):** `persistence/` + `integrations/` — delivered by the smart-qr migrator work,
> polished here. Other sub-domains are updated opportunistically, not the primary target.

## code-style/ — layer-agnostic authoring

| File | What it covers |
|---|---|
| [documentation.md](code-style/documentation.md) | XML doc format + consolidated starter table per type-kind |
| [code-organization.md](code-style/code-organization.md) | One file per type, section dividers, parameter formatting, raw strings, SQL line length |
| [models.md](code-style/models.md) | Record style (`{ get; init; }`), member rules, naming |

## architecture/ — layering + host wiring

| File | What it covers |
|---|---|
| [service-architecture.md](architecture/service-architecture.md) | Solution-folder grouping + 5-layer Clean Arch (Api / Application / Domain / Infrastructure / Persistence) |
| [domain-structuring.md](architecture/domain-structuring.md) | Subdomain pattern, `Core/` vs operation folders |
| [host-configuration.md](architecture/host-configuration.md) | `HostConfiguration.Configure` + Extensions split, slim `Program.cs` |
| [services.md](architecture/services.md) | Service / Client / Factory / Repository naming + doc starters |

## persistence/ — schema · EF · Dapper · migrations  (focus)

| File | What it covers |
|---|---|
| [database.md](persistence/database.md) | Schema-first rule (canonical = `Migrations/*/Apply.sql` for Sql-strategy), column constraints, type mappings, EF-as-mapper |
| [entities.md](persistence/entities.md) | Entity records, `IKeyedEntity<TId>` PK contract, audit/soft-delete/tenant traits |
| [enums.md](persistence/enums.md) | Enum naming, native PG enum mapping (`MapEnums`), string-conversion fallback |
| [data-access.md](persistence/data-access.md) | Dapper, `IDbConnectionFactory`, `SqlNaming`, generic repositories |
| [migrations.md](persistence/migrations.md) | SQL migrator authoring — layout, Apply/Rollback, `@no-transaction`, drift/orphan, `AddSqlMigrations` |
| [tooling-cli.md](persistence/tooling-cli.md) | `dotnet tool` CLIs — packaging, exit codes, destructive-op target guard, secret hygiene |

## presentation/ — delivery surface

| File | What it covers |
|---|---|
| [controllers.md](presentation/controllers.md) | Thin-dispatcher controllers — `ISender.Send` + `Result.Match` |
| [api-endpoints.md](presentation/api-endpoints.md) | CQRS naming, DTO rules, response shape *(reconcile with controllers.md — see open decisions)* |

## runtime/ — config + launch

| File | What it covers |
|---|---|
| [settings.md](runtime/settings.md) | Settings records — `sealed record`, `init`-only, `IOptions<T>` binding |
| [launch-profiles.md](runtime/launch-profiles.md) | `launchSettings.json` single http profile + `.http` files |

## foundation/ — cross-cutting primitives

| File | What it covers |
|---|---|
| [result-pattern.md](foundation/result-pattern.md) | Result carrier — `Result<T>` Ok/Fail, `DomainError`, CQRS containers |

## integrations/ — outbound HTTP  (focus)

| File | What it covers |
|---|---|
| [clients.md](integrations/clients.md) | HTTP API wrappers — `HttpClient` injection, resilience pipeline (`AddSdkResilience`), Refit |

## testing/

| File | What it covers |
|---|---|
| [testing.md](testing/testing.md) | E2E-first (Testcontainers + `WebApplicationFactory`, Respawn); unit for pure logic; harness mirrors the SDK scaffold |

## Notes

- Initial extraction (2026-02-23) lifted from Haven's `backend-development-guidelines.md`, generalized; re-organized into sub-domains 2026-06-13.
- Applies to **every** backend repo under `wow-two-ws/`; a repo-level rule overrides for that repo.
- Frontend sibling: [../frontend/](../frontend/).

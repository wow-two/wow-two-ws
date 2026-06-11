# Conventions — Development — Backend (.NET)

*Last updated: 2026-06-09*

> .NET code-style conventions for every backend service under `wow-two-ws/`. Lookup table — open a
> file when the task touches it; do not pre-read. Repo layout is one level up:
> [../repo/repo-structure.md](../repo/repo-structure.md).

## Language

| File | What it covers |
|---|---|
| [documentation.md](documentation.md) | XML doc format + consolidated starter table per type-kind |
| [code-organization.md](code-organization.md) | One file per type, section dividers, parameter formatting, raw strings, SQL line length |
| [models.md](models.md) | Record style (`{ get; init; }`), general member rules, naming |

## Type-kinds

| File | What it covers |
|---|---|
| [entities.md](entities.md) | Entity modeling, PK/FK, navigation, collections, numeric units |
| [enums.md](enums.md) | Enum naming, backing type, PG enum mapping, value docs |
| [services.md](services.md) | Service / Client / Factory / Repository naming + doc starters |
| [clients.md](clients.md) | HTTP API wrappers — `HttpClient` injection, lifetime, base URL |
| [settings.md](settings.md) | Settings records — `sealed record`, `init`-only, `IOptions<T>` |
| [result-pattern.md](result-pattern.md) | Success / Failure sealed inheritance, static factories |

## Architecture

| File | What it covers |
|---|---|
| [service-architecture.md](service-architecture.md) | 5-layer Clean Arch (Api / Application / Domain / Infrastructure / Persistence) |
| [domain-structuring.md](domain-structuring.md) | Subdomain pattern, `Core/` vs operation folders |
| [host-configuration.md](host-configuration.md) | `HostConfiguration.Configure` + Extensions split, slim `Program.cs` |
| [database.md](database.md) | Schema-first rule, column constraints, EF Core configs |
| [data-access.md](data-access.md) | Dapper, `IDbConnectionFactory`, SQL fragment reuse |
| [api-endpoints.md](api-endpoints.md) | CQRS naming, mediator wrappers, `ApiResponse<T>`, controllers, `Problem()` |
| [launch-profiles.md](launch-profiles.md) | `launchSettings.json` even/odd ports + `.http` files (Rider) |

## Notes

- Initial extraction (2026-02-23) lifted from Haven's `backend-development-guidelines.md`, generalized.
- These apply to **every** backend repo under `wow-two-ws/`; a repo-level rule overrides for that repo.
- Frontend sibling: [../frontend/](../frontend/).

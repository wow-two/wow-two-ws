# Service architecture

*Last updated: 2026-02-23*

## Layers

Every backend service follows **layered Clean Architecture**:

| Layer | Folder | Purpose |
|---|---|---|
| Api | `Api/Endpoints/`, `Api/Hubs/`, `Api/Configurations/` | HTTP endpoints, SignalR hubs, DI & host configuration |
| Application | `Application/Models/`, `Application/Services/`, `Application/Pipelines/` | DTOs, interfaces, business logic |
| Domain | `Domain/Entities/` | Immutable records, enums, value objects |
| Infrastructure | `Infrastructure/Services/`, `Infrastructure/Settings/`, `Infrastructure/Scheduling/` | Implementations, config classes, background services |
| Persistence | `Persistence/Repositories/` | Data access (Dapper, EF Core repository-style) |

## Rules

- `Program.cs` is a slim 3-liner: `builder.Configure()` → `app.Configure()` → `app.Run()`
- All DI registration lives in `Api/Configurations/HostConfiguration.Extensions.cs` as extension methods — see [host-configuration.md](host-configuration.md)
- `HostConfiguration.cs` defines `Configure(builder)` and `Configure(app)` as partial class
- **Interfaces in `Application/`, implementations in `Infrastructure/`** — the dependency rule
- Settings classes in `Infrastructure/Settings/`, loaded via configuration binding
- Background services in `Infrastructure/Scheduling/`
- Pipeline services may group by feature under `Application/Pipelines/{PipelineName}/` (`Models/` + `Nodes/`)

## Dependency direction

```
Api ──► Application ──► Domain
 │            ▲
 ▼            │
Infrastructure  (implements Application interfaces)
Persistence     (implements Application repository interfaces)
```

- Domain has **no** outbound dependencies — pure types
- Application depends on Domain only
- Infrastructure + Persistence depend on Application (for interfaces) + Domain (for entities)
- Api depends on Application + Infrastructure (for DI registration)

## When to deviate

- **Modular monolith / single-process services** — same 5 layers, just within one assembly
- **Pure SDK packages** (the beta SDK) — Application/Infrastructure/Persistence split doesn't apply; SDK packages are libraries, not services
- **CLI tools** — `Application` + `Domain` only; no `Api`, no `Persistence` unless reading/writing files

## See also

- [host-configuration.md](host-configuration.md) — the `Configure` / `Extensions` split
- [domain-structuring.md](domain-structuring.md) — subdomains within `Domain/` and `Infrastructure/`
- [api-endpoints.md](api-endpoints.md) — Api layer details

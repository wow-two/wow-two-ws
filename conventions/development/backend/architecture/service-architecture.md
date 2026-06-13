# Service architecture

*Last updated: 2026-06-13*

## Solution organization

A backend solution (`{slug}.backend-services/*.sln[x]`) groups its projects into **solution folders** — virtual `.sln` nodes, not on-disk paths. Projects are named `{Brand}.{Domain}[.{SubDomain}]` (PascalCase).

| Folder | Holds | Examples (SmartQr) |
|---|---|---|
| `services/` | the product itself — deployable hosts **+** their domain / persistence / feature libs | `SmartQr.Api`, `SmartQr.Redirect`, `SmartQr.Common`, `SmartQr.Common.Domain`, `SmartQr.Common.Persistence`, `SmartQr.Codes` |
| `platform/` | SDK-bound extractables — generic infra, **named `{Brand}.Platform.*`** | `SmartQr.Platform.Core`, `SmartQr.Platform.Migrations`, `SmartQr.Platform.Testing` |
| `libraries/` | product-level shared libs that aren't service code (reserved) | — |
| `tools/` | CLIs / dev utilities | `SmartQr.Migrations.Cli` |
| `tests/` | test projects | `SmartQr.Tests`, `SmartQr.IntegrationTests` |

- **Reference rule: `services → platform`, never reverse.** `platform/*` references only the kit + BCL. This keeps the eventual lift of `platform/*` into the backend-beta SDK a **move + namespace-rename, not a rewrite**.
- **Add folders when real** — omit `libraries/` / `tools/` until a project needs them; a roadmapped folder (e.g. `platform/` before the first extraction) may be declared empty to signal intent.
- **Reference implementation:** SmartQr — `workbench/ventures/smart-qr-poc/.../SmartQr.sln`.

### `.sln` / `.slnx` encoding

A solution folder is a virtual node; projects join it by **GUID**, not disk path.

- **Classic `.sln`** (SmartQr): a folder is `Project("{2150E333-8FDC-42A3-9474-1A3956D46DE8}") = "platform", "platform", "{folderGuid}"`; membership via `GlobalSection(NestedProjects) = preSolution` lines `{childGuid} = {folderGuid}`. An **empty** folder simply omits its NestedProjects lines. (`2150E333-…` = the "solution folder" type GUID; `FAE04EC0-…` = a C# project.)
- **`.slnx`** (drydock, SDK): XML `<Folder Name="/platform/"><Project Path="…csproj" /></Folder>` — same grouping, terser.
- Moving a project between folders changes only its nesting entry — never its own GUID or `ProjectConfigurationPlatforms` block.

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
- [api-endpoints.md](../presentation/api-endpoints.md) — Api layer details

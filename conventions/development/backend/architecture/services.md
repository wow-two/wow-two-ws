# Services

*Last updated: 2026-02-23*

Application and infrastructure services that contain business logic, data access, or integration code.

## Location

Services live in the layer that matches their responsibility (see [service-architecture.md](service-architecture.md)):

| Layer | Folder | Examples |
|---|---|---|
| Application | `Application/Services/` | `IChannelStatsService` (interface) |
| Infrastructure | `Infrastructure/Services/` | `PipelineSeedService`, `PipelineConfigService` |
| Common (shared across services) | `{Repo}.Common/...` | `PipelineRegistry`, shared services |

Interface in `Application/`, implementation in `Infrastructure/` — the Clean Arch dependency rule.

## Modeling

### Class shape

- **Non-static** class
- **Primary constructor** for DI injection (allowed exception to the body-property rule for records — see [models.md](../code-style/models.md))
- **Sealed** unless intentionally designed for inheritance — `sealed` should be the default

### Lifetime

Register in the appropriate `HostConfigurationExtensions` method (see [host-configuration.md](host-configuration.md)):
- **Singleton** — stateless, thread-safe, expensive to construct
- **Scoped** — request-scoped state, holds DbContext or similar
- **Transient** — lightweight, no caching benefit

## Naming

| Suffix | Purpose | Examples |
|---|---|---|
| `Service` | Internal business logic, orchestration, data operations | `ChannelsSeedService`, `ListingPublishingService`, `SeedDataReaderService` |
| `Client` | External HTTP/API calls (single provider) — see [clients.md](../integrations/clients.md) | `TelegramClient`, `ClaudeClient`, `LocationApiClient` |
| `Factory` | Creates/resolves instances dynamically | `AiClientFactory` |
| `Repository` | Direct DB queries (Dapper/SQL) — see [data-access.md](../persistence/data-access.md) | `OtpRepository`, `LandmarkRepository` |
| `Registry` | Static / scoped lookup of pre-registered items | `PipelineRegistry`, `ChannelDefinitions` |
| `Tracker` | Mutable **in-process** state (not DB I/O — that's a `Repository`) | `PipelineExecutionTracker` |
| `Extensions` | **Static helper** classes — expose the helpers as extension methods where natural | `MigrationChecksumExtensions`, `CorsExtensions` |
| (no suffix) | Static **definitions** only — constants, enums, registries | `ChannelSlugs`, `DatabasePathConstants` |

## Documentation

Per the starter table in [documentation.md](../code-style/documentation.md):

### Service class

- `/// <summary>` starts with **Provides**
- `/// <remarks>` describes the flow or key behaviors (multi-line allowed for numbered flow steps)

```csharp
/// <summary>Provides channel and pipeline seeding on application startup.</summary>
/// <remarks>
/// Seed flow:
///   1. Read channels from seed file via SeedDataReaderService
///   2. Upsert channels + sources via EF Core
///   3. Insert missing pipeline_configs rows with code defaults
///   4. Fetch ALL rows → merge DB-configurable values into registry
///   5. Crash recovery: reset stale 'processing' URLs to 'pending'
/// </remarks>
public class ChannelsSeedService { }
```

### Factory class

- `/// <summary>` starts with **Creates**

```csharp
/// <summary>Creates AI clients keyed by provider and model tier.</summary>
public class AiClientFactory { }
```

### Registry / tracker / no-suffix class

- `/// <summary>` starts with **Tracks** or **Holds** (registry/tracker) or describes content (constants class — **Contains**)

```csharp
/// <summary>Tracks live pipeline executions keyed by pipeline id.</summary>
public class PipelineExecutionTracker { }

/// <summary>Contains the canonical kebab-case slugs for every channel.</summary>
public static class ChannelSlugs { }
```

### Method docs

- `/// <summary>` one-liner — start with a verb (`Gets`, `Sends`, `Creates`, `Builds`)
- Multi-step methods may add `/// <remarks>` with numbered flow

## See also

- [clients.md](../integrations/clients.md) — HTTP API wrappers
- [data-access.md](../persistence/data-access.md) — Dapper repositories
- [host-configuration.md](host-configuration.md) — DI registration
- [documentation.md](../code-style/documentation.md) — XML doc + starter table

# Host configuration

*Last updated: 2026-02-23*

DI registration, middleware, and startup wiring split into two files in `Api/Configurations/`.

## Location

- `{Service}/Api/Configurations/HostConfiguration.cs` — slim orchestrator
- `{Service}/Api/Configurations/HostConfiguration.Extensions.cs` — all extension methods

## Program.cs

**Pristine** — the entry point does nothing but wire + run. No comments, no logs, no DI, no startup calls. Only the two `Configure` calls, `app.Run()`, and the test marker.

```csharp
using {Brand}.{Service}.Configurations;

var builder = WebApplication.CreateBuilder(args);
builder.Configure();

var app = builder.Build();
app.Configure();

app.Run();

public partial class Program;
```

- `public partial class Program;` (no XML doc) lets `WebApplicationFactory<Program>` resolve the host in integration tests.
- **All startup work** — migrations, seeding, warm-up, startup logs — lives in `HostConfiguration.Configure(WebApplication)` (or an extension it calls), never in `Program.cs`. A blocking startup task uses `.GetAwaiter().GetResult()` inside `Configure(app)` to keep the entry point sync.

## HostConfiguration

Static class with two `Configure` overloads — one for `WebApplicationBuilder`, one for `WebApplication`. No DI logic inline — just chains extension methods in order.

```csharp
public static class HostConfiguration
{
    /// <summary>Configures all services: settings, integrations, application services, pipelines, SignalR, CORS.</summary>
    public static WebApplicationBuilder Configure(this WebApplicationBuilder builder)
    {
        builder
            .AddEnvironmentOverrides()
            .AddSettings()
            .AddIntegrations()
            .AddApplicationServices()
            .AddPipelines()
            .AddSchedulers()
            .AddObservers()
            .AddControllers()
            .AddSignalR()
            .AddCors();

        return builder;
    }

    /// <summary>Configures middleware and maps endpoints.</summary>
    public static WebApplication Configure(this WebApplication app) { ... }
}
```

## HostConfigurationExtensions

Static class with extension methods on `WebApplicationBuilder`. Each method registers a logical group of services. Methods are called in order by `HostConfiguration.Configure()`.

| Method | Purpose |
|---|---|
| `AddEnvironmentOverrides()` | Maps env vars to config keys (overrides appsettings) |
| `AddSettings()` | Binds `IOptions<T>` for all settings classes + DB setup |
| `AddIntegrations()` | Registers typed `HttpClient`s for external APIs |
| `AddApplicationServices()` | Registers application-layer services (interfaces → implementations) |
| `AddPipelines()` | Registers pipeline nodes, orchestrators, registry, executor, schedulers |
| `AddSchedulers()` | Registers `IHostedService` background schedulers |
| `AddObservers()` | Registers pipeline event observers (e.g. SignalR notifier) |
| `AddMediator()` | Registers mediator + scans assembly for query/command handlers |
| `AddControllers()` | Configures MVC controllers + JSON serialization |
| `AddSignalR()` | Adds SignalR hub services |
| `AddCors()` | Configures CORS from settings |

## Documentation

Only `/// <summary>` required — one-liner starting with **"Configures"** (per [documentation.md](../code-style/documentation.md) starter table). No `<remarks>` or `<example>`.

```csharp
/// <summary>Configures all services: settings, integrations, application services, pipelines, SignalR, CORS.</summary>
public static WebApplicationBuilder Configure(this WebApplicationBuilder builder) { }

/// <summary>Configures middleware and maps endpoints.</summary>
public static WebApplication Configure(this WebApplication app) { }

/// <summary>Configures typed HTTP clients for external API integrations.</summary>
public static WebApplicationBuilder AddIntegrations(this WebApplicationBuilder builder) { }

/// <summary>Configures pipeline nodes, orchestrators, registry, and execution infrastructure.</summary>
public static WebApplicationBuilder AddPipelines(this WebApplicationBuilder builder) { }
```

## Rules

- `Program.cs` is **pristine** (see above) — only the two `Configure` calls, `app.Run()`, and the `Program` marker. No comments, logs, DI, or startup calls — those live in `HostConfiguration`.
- `HostConfiguration.Configure()` chains extension methods — no inline DI logic
- Each extension method in `HostConfigurationExtensions` groups related registrations
- Inline comments above registration groups explain the "why"
- Return `WebApplicationBuilder` for chaining

## See also

- [service-architecture.md](service-architecture.md) — the 5 layers
- [api-endpoints.md](../presentation/api-endpoints.md) — what registers in `AddControllers` + endpoint conventions

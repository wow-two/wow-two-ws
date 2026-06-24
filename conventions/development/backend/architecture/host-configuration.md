# Host configuration

*Last updated: 2026-06-22*

> All host wiring — DI registration, configuration binding, middleware, startup — lives in the host's `Api/Configurations/` composition root, sourced only from the SDK or the host itself.
> Purpose — one place to read everything a service is wired with; no hidden, self-registering config buried in a layer, service, or model.
> Use case — reach for this whenever you add a setting, a service registration, or a startup step to a backend host.

## Configuration source

- configuration enters from exactly two places: the **SDK** (its public `Add*` / `Use*` extensions — `AddApiDefaults`, `AddDatabaseBespokeMigrations`, `AddDataSourceConnectionFactory`) or the **host itself** (`HostConfiguration` + its extensions).
- non-host projects — the application, domain, infrastructure, and persistence [layers](service-architecture.md), plus models — **never** bind or register configuration: no `services.Configure<T>()`, no `AddOptions<T>()`, no `IConfiguration` reads, no self-registering `IServiceCollection` extension methods.
- a layer that needs a setting takes it as a **method parameter** the host passes in (`AddPersistence(this IServiceCollection services, IConfiguration configuration)`) — it does not reach into config on its own.
- this kills **hidden config methods** — a registration buried in an infra/persistence project that the host calls blind; every wire-up must be readable from the host's `Configure` chain alone.
- the SDK is the only allowed non-host source because its surface is a published, reviewed contract (see [startup-defaults.md](startup-defaults.md)); a product layer is not — if layers keep needing the same block, extract it to the SDK first.

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
/// <summary>Provides host configuration extensions.</summary>
public static partial class HostConfiguration
{
    /// <summary>Configures the application builder (services).</summary>
    /// <param name="builder">The web application builder to configure.</param>
    /// <returns>The same <paramref name="builder"/> for chaining.</returns>
    public static WebApplicationBuilder Configure(this WebApplicationBuilder builder)
    {
        builder.AddApiDefaults(o => o.ServiceName = "{service}");   // SDK boot floor first

        builder
            .AddSettings()
            .AddPersistence()
            .AddApplicationServices();   // product seams — no trailing comments; method names self-document

        return builder;
    }

    /// <summary>Runs startup tasks, then configures middleware and endpoints.</summary>
    /// <param name="app">The built web application to configure.</param>
    /// <returns>The same <paramref name="app"/> for chaining.</returns>
    public static WebApplication Configure(this WebApplication app) { ... }
}
```

- the class summary and the two `Configure` summaries above are **locked** — identical across every app, don't reword per app.

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

## Layer registration

Layers (`Application`, `Infrastructure`, `Persistence`) ship **no** `DependencyInjection.cs` and **no** `Add*(this IServiceCollection)` — the host inlines their registrations into the matching `Add{Layer}Layer` extension above. Two consequences to handle when collapsing a layer into the host:

- **Assembly scans** (mediator handlers, FluentValidation validators) anchor on a **public marker type in the scanned layer** — `typeof(IApplicationMarker).Assembly` — never the parameterless overload: called from the host, `Assembly.GetCallingAssembly()` resolves to the *host* assembly, not the layer (see [mediator.md](../messaging/mediator.md)). Add one empty `public interface I{Layer}Marker;` to each scanned layer.
- **Internal adapters** (EF stores, typed clients) stay `internal` — the host registers them by concrete type, so grant it visibility with `<InternalsVisibleTo Include="{Host}" />` in the layer's `.csproj`. Don't widen them to `public` just to wire them.

Startup tasks (DB init, seeding, warm-up) move host-side too — into `Configurations/AppInitialization.cs`, called from `Program.cs` after `Build()` (per [Program.cs](#programcs) — the entry point stays pristine).

## Documentation

- the class + the two `Configure` overloads use the **locked** summaries shown above (don't reword per app).
- each private `Add*` extension gets a one-liner `<summary>` starting with **"Registers"** (or "Configures"). No `<remarks>` on host wiring.
- the `Configure` chain carries **no trailing per-method comments** — the method names self-document. Inline comments only where a step's *why* isn't obvious (imperative one-liner, per [documentation.md](../code-style/documentation.md)).

## Rules

- **service-registration `Add*` extensions live only in `Configurations/`** — never in a layer (persistence, infrastructure, codes, …). The host calls the SDK's `Add*` directly and inlines the product glue; a layer never ships its own `AddXyz(this IServiceCollection)`. (A multi-host app duplicates the few glue lines per host — that is the accepted cost of host-owned wiring.)
- all configuration is wired **only** in the host, sourced from the SDK or the host itself — never a layer/service/model (see Configuration source).
- `Program.cs` is **pristine** (see above) — only the two `Configure` calls, `app.Run()`, and the `Program` marker. No comments, logs, DI, or startup calls — those live in `HostConfiguration`.
- `HostConfiguration.Configure()` chains extension methods — no inline DI logic
- Each extension method in `HostConfigurationExtensions` groups related registrations
- Inline comments above registration groups explain the "why"
- Return `WebApplicationBuilder` for chaining

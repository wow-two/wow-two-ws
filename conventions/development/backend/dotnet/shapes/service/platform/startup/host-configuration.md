# Host configuration

*Last updated: 2026-10-26*

> Product composition in the host; reusable registration contracts in the SDK.

## Configuration source

- must declare product DI registration, configuration binding and startup wiring in the host.
- must call reusable SDK registration methods through their published contracts.
- must not add self-registering `IServiceCollection` extensions to product Domain, Application or implementation projects.
- must pass a bound settings record or an explicit value into a collaborator; do not pass `IConfiguration` into it.
- must not bind configuration inside a service, model or product implementation project.
- may repeat small product glue blocks per host; shared reusable wiring follows SDK extraction rules.
- must keep the configuration chain readable without opening every registration body.

Ownership rationale is [separate](host-configuration-rationale.md#ownership).

---

## Location

- must keep `HostConfiguration.cs` and `HostConfiguration.Extensions.cs` in the host's `Configurations/` folder.
- must declare one `public static partial class HostConfiguration` across the two files.
- must put the two public `Configure` entry points and their ordered chains in `HostConfiguration.cs`.
- must put private registration/startup extension methods in `HostConfiguration.Extensions.cs`.
- must keep DI implementation out of the entry-point chains.

---

## Program.cs

- must keep three statement groups with the comments in this example.
- must leave the public partial test marker undocumented.
- must keep registration, middleware, migrations, seeding, warm-up and startup logs behind `Configure`.
- must await `ConfigureAsync` when startup work is asynchronous; that replaces the second group's call.

```csharp
using {Brand}.{Service}.Configurations;

// Build and configure the host.
var builder = WebApplication.CreateBuilder(args);
builder.Configure();

// Build and configure the app.
var app = builder.Build();
app.Configure();

// Run.
app.Run();

public partial class Program;
```

---

## Naming a registration method

- must name a product registration for its subject, never its architectural layer.
- must use `Add{Domain}` for a domain's vertical, such as `AddCodes`.
- must use `Add{Resource}` for shared resources, such as `AddPostgresDatabase`.
- must use `Add{Surface}` for delivery surfaces, such as `AddControllers`.
- must not use `AddApplicationServices`, `AddApplicationLayer`, `AddInfrastructure`, `AddInfrastructureLayer`, `AddPersistence`, `AddPersistenceLayer` or `AddDomain`.
- must not append `Services` when the domain name already states the subject.
- must give every documented product registration a concrete method body.

---

## Domain registration

- must group a domain's related services, settings, options and adapters in its `Add{Domain}` method, including registrations whose types live in different project layers.
- may split registration by subdomain once the domain itself has subdomains.
- must register shared resources once, outside any domain that merely consumes them.
- must reserve `AddSettings` for host-wide settings not owned by one domain.
- must bind records through the [settings recipe](../../../../core/mla/components/settings.md).
- must order the chain by dependencies, with prerequisite settings before their consumers and delivery surfaces last.
- must anchor assembly scans on a public marker type in the assembly being scanned.
- must not rely on calling-assembly discovery after moving a registration to the host.
- must preserve internal adapter visibility; use `InternalsVisibleTo` for the host when required to register them.
- must return the builder from registration extensions for chaining.

---

## Async startup

- must await asynchronous initialization through `ConfigureAsync(WebApplication)` and its caller.
- must not use `.Result`, `.Wait()` or `.GetAwaiter().GetResult()` to block on startup tasks.
- must finish required initialization before exposing endpoints that depend on it.
- must apply [durable startup logging](../../../../core/mla/domains/observability/serilog/serilog.md#startup).
- must let a failed mandatory startup task abort startup; do not silently accept traffic with incomplete state.
- must pass cancellation through cancellable startup operations.

```csharp
// Build and configure the app.
var app = builder.Build();
await app.ConfigureAsync();
```

---

## Background work

- must register host-run work in its owning domain's registration.
- must run work repeated on an interval through the be sdk's `AddPeriodicJob`; never hand-write a timer loop.
- must put a periodic pass in a scoped service method; the job resolves it from a fresh scope each pass.
- must read the interval from settings in the job's `configure`; an `Interval` of zero or less turns it off.
- must not add a separate enabled flag, a catch-all or a retry loop around a pass; a failed pass is logged
  and the next runs on schedule.
- must set `PassTimeout` on a pass that waits on a process or a remote system.
- must set `LogExceptionDetails = false` on a pass whose exceptions can carry input, output or secrets.
- must not use a periodic job for work needing one runner across replicas, retries or persistence.
- must use `BackgroundService.ExecuteAsync` for any other long-running loop, such as a queue drain.
- must use `IHostedService.StartAsync` for a one-shot task required to complete during startup.
- must pass the stopping token into each cancellable asynchronous operation.
- must create and dispose an `IServiceScopeFactory` scope for each run needing scoped collaborators.
- must not capture a scoped collaborator in the singleton host-run service.
- must state the failure policy: abort mandatory startup, or explicitly retry/stop for background work.
- must keep the declared retry budget and shutdown behavior in the type's documentation.
- must take declaration and naming from [background services](../../../../core/mla/constructs/behavior/background-service.md).

---

## Environment overrides

- must take settings file names and environments from
  [environment files](../../../../../../../deployment/hosting/environment-files.md) § *Settings*.
- must keep secrets out of checked-in settings; use environment values, a secret store or development user secrets.
- must name explicit deployment aliases by role in UPPER_SNAKE, such as `DB_CONNECTION`, without a product prefix.
- must apply explicit alias mappings before binding their settings consumers.
- must remove ambient environment configuration sources before binding application settings.
- must map only explicitly named aliases into application configuration; do not re-add a broad environment provider.
- must apply present aliases after file/default sources so explicit deployment values win.
- must leave a missing alias absent so it does not erase a configured fallback.
- must document any host-bootstrap inputs read during builder creation separately from application aliases.
- must preserve required hosting values explicitly when removing their original source.

```csharp
foreach (var source in builder.Configuration.Sources
    .OfType<EnvironmentVariablesConfigurationSource>().ToArray())
{
    builder.Configuration.Sources.Remove(source);
}

var connection = Environment.GetEnvironmentVariable("DB_CONNECTION");
if (connection is not null)
{
    builder.Configuration.AddInMemoryCollection(new Dictionary<string, string?>
    {
        ["Database:ConnectionString"] = connection,
    });
}
```

- must use the actual settings section/key in each host's mapping; `Database:ConnectionString` is an example.
- must test both prefixed and unprefixed unexpected variables, alias precedence and fallback behavior.

---

## Settings files

Deployed dev runs as `Development`, so `Development` alone never means the developer's machine.

- must treat a host as deployed when `DEPLOY_ENVIRONMENT` is set; the runner sets it on every deployed container.
- must call a run local only in `Development` without `DEPLOY_ENVIRONMENT`.
- must gate local-only conveniences on a local run, never on `IsDevelopment()` alone: an open allowlist, OpenAPI,
  log-delivered sign-in codes, relaxed rate limits, polling instead of webhooks.
- must read the two optional settings files through the be sdk's `AddSettingsFiles`; `AddApiDefaults` calls it, so a
  host calls it itself only when it reads settings earlier.
- must load in this order: `appsettings.json`, `appsettings.{Environment}.json`, `appsettings.Target.json`,
  `appsettings.Local.json`, user secrets and environment variables, then later sources such as the vault.
- `appsettings.Target.json` is the deployed target's file, mounted by its release bundle (pipelines v0.7.0 or later).
- must read `appsettings.Local.json` only on a local run whose launch profile sets `LOCAL_SETTINGS=true`
  ([launch profiles](launch-profiles.md)); tests and containers never set it.
- must document `LOCAL_SETTINGS` and `DEPLOY_ENVIRONMENT` as host-bootstrap inputs, not application aliases.
- transition: a deployed host (`DEPLOY_ENVIRONMENT` set) without `appsettings.Target.json` reads a legacy
  `appsettings.Local.json`, which bundles before pipelines v0.7.0 mount, and logs a warning; the be sdk drops this
  fallback in a later release.

```csharp
var builder = WebApplication.CreateBuilder(args);
builder.AddSettingsFiles();   // idempotent; only when the host reads settings before AddApiDefaults
```

---

## Middleware

- must use [startup defaults](startup-defaults.md) for the common pipeline.
- must apply forwarded headers before middleware consumes the effective scheme, host or client address.
- must put the exception handler outside the operations it must catch.
- must place response compression before response writers whose bodies it must compress.
- must place request decompression before readers of compressed request bodies.
- must apply URL/path rewriting before routing consumes the resulting path.
- must put default-file rewriting before static-file serving.
- must place cookie policy before middleware whose cookies it governs.
- must call routing before middleware that depends on endpoint metadata.
- must place CORS after routing and before authentication/authorization for endpoint policies.
- must authenticate before authorization or any limiter whose partition reads the authenticated principal.
- may place an IP-only limiter before authentication when it needs no authenticated identity.
- must place endpoint-specific rate limits and timeouts after routing.
- must place route-data localization after routing; other culture providers follow their own dependencies.
- must place antiforgery after authentication and authorization when it validates the authenticated user.
- must place identity-dependent cache policies after authentication and authorization.
- must register terminal middleware only after the operations it must permit to run.
- must apply the same dependency constraints inside branches; there is no universal interchangeable slot.
- must check the SDK's composition seam before adding middleware that must run inside its bundle.

Framework API availability follows the [ASP.NET Core API reference](https://learn.microsoft.com/en-us/dotnet/api/?view=aspnetcore-10.0).

---

## Framework boundaries

- must set fixed host identity, environment and content-root options when creating the `WebApplicationBuilder`.
- must not use legacy `UseStartup`, `ConfigureWebHost` or `ConfigureWebHostDefaults` to reconfigure that builder.
- must use its `Services`, `Configuration` and `Logging` surfaces for supported composition changes.
- must consult the framework API reference for package requirements and supported overloads.

---

## Documentation

- must summarize `HostConfiguration` as `Extends the host builder and the web application for startup wiring.`
- must summarize builder `Configure` as `Configures the application builder (services).`
- must summarize app `Configure` as `Runs startup tasks, then configures middleware and endpoints.`
- must document each private registration with `Registers` or `Configures`; no remarks on wiring.
- must keep trailing per-method comments out of the chain; reserve inline comments for non-obvious constraints.

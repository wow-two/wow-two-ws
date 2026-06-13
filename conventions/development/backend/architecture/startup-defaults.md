# Startup defaults

*Last updated: 2026-06-13*

A production-shaped API host boots through the paired SDK calls `AddApiDefaults()` / `UseApiDefaults()` — never a hand-rolled per-area `Add*` / `Use*` set.

## The two calls

The boot floor is two lines. Everything between them is per-app (auth, mediator, data).

```csharp
using WoW.Two.Sdk.Backend.Beta;

var builder = WebApplication.CreateBuilder(args);
builder.AddApiDefaults();

// auth + mediator + data go HERE — explicit, after AddApiDefaults, before Build()

var app = builder.Build();
app.UseApiDefaults();

// auth middleware + your endpoints go HERE — after UseApiDefaults

app.Run();
```

- `AddApiDefaults(this WebApplicationBuilder, Action<ApiDefaultsOptions>? configure = null)` — registers the P1 service baseline; returns the builder for chaining.
- `UseApiDefaults(this WebApplication)` — adds the matching middleware pipeline and maps the OpenAPI + health endpoints; returns the app.
- Both defined in `src/meta/ApiDefaultsExtensions.cs` (root namespace `WoW.Two.Sdk.Backend.Beta` — one `using` lights it up).
- Pristine `Program.cs` still applies (see [host-configuration.md](host-configuration.md)) — when the product wraps these in `HostConfiguration`, the two `Configure` extensions call `AddApiDefaults` / `UseApiDefaults` and nothing per-area.

## What the bundle folds in

`AddApiDefaults` composes these (each its own per-area extension — do **not** call them yourself):

| Concern | Add-side symbol | Use-side symbol |
|---|---|---|
| Logging | `UseSerilogConventional` (on `builder.Host`) | — |
| Time | `AddTimeProviders` | — |
| Tracing | `AddOpenTelemetryTracing` | — |
| Metrics | `AddOpenTelemetryMetrics` | — |
| OTLP export | `AddOtlpExporters` | — |
| Health | `AddHealthChecksBuilder` | `MapHealthChecks(options.HealthEndpointPath)` |
| Proxy-aware hosting | `AddProxyAwareHosting` | `UseProxyAwareHosting` |
| Secure headers | — | `UseOwaspSecureHeaders` |
| OpenAPI | `AddOpenApiDefaults` | `MapOpenApiEndpoint` |
| ProblemDetails | `AddTraceAwareProblemDetails` | — |
| Validation exceptions | `AddValidationExceptionHandler` | — |
| Rate limit | `AddPerIpSlidingWindowRateLimit` | `UseRateLimiter` |
| Output cache | `AddDefaultOutputCache` | `UseOutputCache` |
| Compression | `AddBrotliGzipCompression` | `UseResponseCompression` |
| CORS | `AddDefaultCorsPolicy` (origins given) | `UseCors` (origins given) |
| Validators | `AddFluentValidatorsFromAssemblies` (assemblies given) | — |

## Tuning — flip flags, don't re-compose

Tune via `ApiDefaultsOptions` (`src/meta/ApiDefaultsOptions.cs`). Every concern defaults **on** — flip a flag off rather than dropping `AddApiDefaults` and re-listing the per-area extensions by hand.

```csharp
builder.AddApiDefaults(o =>
{
    o.ServiceName = "smart-qr";                            // OTel service name (default: app name)
    o.ValidatorAssemblies.Add(typeof(Program).Assembly);   // empty ⇒ validators skipped
    o.CorsOrigins.Add("https://app.example.com");          // empty ⇒ CORS not registered
    o.EnableRateLimiting = false;                          // off-flag, not a removed call
    o.ExposeOpenApi = false;                               // hide the OpenAPI endpoint in prod
});
```

| `ApiDefaultsOptions` member | Type | Default | Effect when changed |
|---|---|---|---|
| `ServiceName` | `string?` | host app name | OTel resource service name |
| `ValidatorAssemblies` | `IList<Assembly>` | empty | non-empty ⇒ `AddFluentValidatorsFromAssemblies` runs |
| `CorsOrigins` | `IList<string>` | empty | non-empty ⇒ `AddDefaultCorsPolicy` + `UseCors` |
| `EnableOtlpExporters` | `bool` | `true` | gates `AddOtlpExporters` |
| `EnableRateLimiting` | `bool` | `true` | gates `AddPerIpSlidingWindowRateLimit` + `UseRateLimiter` |
| `EnableOutputCache` | `bool` | `true` | gates `AddDefaultOutputCache` + `UseOutputCache` |
| `EnableResponseCompression` | `bool` | `true` | gates `AddBrotliGzipCompression` + `UseResponseCompression` |
| `ExposeOpenApi` | `bool` | `true` | gates `MapOpenApiEndpoint` |
| `HealthEndpointPath` | `string` | `/health` | path passed to `MapHealthChecks` |

## Stays explicit (added after the call)

Auth, mediator, and data are **deliberately excluded** — they need per-app keys, assemblies, and connection strings.

- Register services (auth/mediator/data) between `AddApiDefaults` and `Build()`.
- Add auth middleware and map endpoints **after** `UseApiDefaults` so the forwarded-headers / secure-headers / CORS pipeline is already in place.

## Rules

- Boot a production-shaped API host with `AddApiDefaults` + `UseApiDefaults` — not a hand-assembled `Add*` / `Use*` list.
- Change behavior through `ApiDefaultsOptions` flags only; never bypass the bundle to call a folded-in per-area extension directly.
- Keep auth + mediator + data out of the bundle; add them explicitly, mediator/data before `Build()`, auth middleware after `UseApiDefaults`.
- Need finer control than the flags expose? Raise it — extend `ApiDefaultsOptions`, don't fork the wiring per product.

## See also

- [host-configuration.md](host-configuration.md) — pristine `Program.cs` + `HostConfiguration` split that wraps these calls
- [service-architecture.md](service-architecture.md) — the 5 layers
- `src/meta/README.md` (in `wow-two-sdk.backend.beta`) — the boot-floor quickstart + per-area composition escape hatch

# Logging and tracing — analysis

*Last updated: 2026-08-17*

> What the backend SDK and the reference product log and trace today, and what a convention would rule on.
> Purpose — research feeding a future `mla/domains/observability/`; this is analysis, not the convention.
> Citation roots: `sdk:` = `wow-two-sdk.backend.beta/engineering/codebase/wow-two-back-beta-sdk/src/`,
> `sqr:` = `ventures/10x-venture-forever-pin/engineering/codebase/forever-pin.backend-services/`; both under `workbench/`.

## Verdict

- one trace id spans inbound HTTP → mediator handler → EF repository, carried by `Activity.Current`, not by our code
- it never reaches a log line — the Serilog text template renders no `TraceId`, so logs cannot be joined to traces
- the mediator handler is invisible in the trace: `LoggingBehavior` times with a `Stopwatch` and opens no span,
  and forever-pin does not register it at all
- forever-pin handlers catch every exception, so `AppErrorObserver` never runs — no `errors_total`, no error span status
- biggest gap: **no trace id in logs**; second: the product template ships without `AddApiDefaults`

---

## What exists

Rows cite SDK files unless the path carries the `sqr:` prefix.

| Capability | Where | Verified symbol | Maturity |
|---|---|---|---|
| Serilog wiring | `LoggingHostExtensions.cs:13` | `UseSerilogConventional` | shipped |
| Console + file sink | `LoggingHostExtensions.cs:26` | `WriteTo.Async` | shipped |
| Enrichers | `LoggingHostExtensions.cs:21` | `Enrich.FromLogContext` | wired, unrendered |
| OTel tracing | `TracingServiceCollectionExtensions.cs:13` | `AddOpenTelemetryTracing` | shipped |
| Auto-instrumentation | `TracingServiceCollectionExtensions.cs:24` | `AddAspNetCoreInstrumentation` | shipped |
| EF Core spans | `TracingServiceCollectionExtensions.cs:28` | `AddEntityFrameworkCoreInstrumentation` | shipped |
| OTel metrics | `MetricsServiceCollectionExtensions.cs:13` | `AddOpenTelemetryMetrics` | shipped |
| OTLP export | `OtlpServiceCollectionExtensions.cs:15` | `AddOtlpExporters` | traces + metrics only |
| Prometheus export | `PrometheusServiceCollectionExtensions.cs:12` | `AddPrometheusMetricsExporter` | opt-in |
| Boot floor | `Meta/ApiDefaultsExtensions.cs:29` | `AddApiDefaults` | shipped |
| Error body traceId | `ProblemDetailsServiceCollectionExtensions.cs:22` | `Extensions["traceId"]` | shipped |
| Error → log/metric/span | `Observability/Errors/AppErrorObserver.cs:19` | `AppErrorObserver.Record` | 3 call sites |
| Mediator request log | `Mediator/Logging/LoggingBehavior.cs:53` | `AddMediatorLoggingBehavior` | opt-in |
| Correlation | `HeaderPropagationServiceCollectionExtensions.cs:18` | `AddConventionalHeaderPropagation` | opt-in |
| Messaging spans | `Messaging/MessagingDiagnostics.cs:18` | `ActivitySource("WoW.Two.Messaging")` | shipped |
| W3C header out | `Messaging/Transport/TransportEventBus.cs:118` | `BuildPropagatedHeaders` | shipped |
| W3C header in | `Messaging/Transport/EventProcessingPipeline.cs:175` | `ExtractParentContext` | shipped |
| Log-method generator | 30 files, 127 call sites | `[LoggerMessage]` | house style |

- exactly **one** `ActivitySource` exists SDK-wide (`Messaging/MessagingDiagnostics.cs:9`) — nothing else spans
- `UseSerilogRequestLogging` — zero hits SDK-wide; the request log is the `Microsoft.AspNetCore` default
- `OtlpServiceCollectionExtensions.cs:11` claims "traces, metrics, **and logs**"; the body wires only the tracer
  and meter providers, so logs are never exported
- forever-pin adopts the floor twice — `sqr:ForeverPin.Api/Configurations/HostConfiguration.cs:17` (`forever-pin-api`)
  and `sqr:ForeverPin.Redirect.Api/Configurations/HostConfiguration.cs:18` (`forever-pin-redirect`)
- the product template calls neither `AddApiDefaults` nor `UseApiDefaults` — zero hits under
  `wow-two-sdk-beta.product-template/engineering/codebase/sample.backend-services/`
- forever-pin's own logging is 15 call sites, all `LogError` / `LogWarning` in `catch` — no business event is logged

---

## Tracing chain

The path an owner request takes, and what carries across each hop.

1. **inbound HTTP** — `AddAspNetCoreInstrumentation` opens the server span and adopts an inbound `traceparent`.
   **survives** — a trace id exists from here on.
2. **middleware** — `sqr:ForeverPin.Api/Configurations/HostConfiguration.cs:61` calls `UseApiDefaults` *after*
   `UseStaticFiles` (`:59`) and a custom header middleware (`:55`), so `UseExceptionHandler` is not outermost.
   **survives**, but a throw from those two outer layers escapes the ProblemDetails pipeline.
3. **controller** — no instrumentation of its own; still inside the server span. **survives**.
4. **mediator handler** — `Activity.Current` flows over `await`, so the id is intact, but nothing opens a child
   span, and `AddMediatorLoggingBehavior` is unregistered
   (`sqr:ForeverPin.Api/Configurations/HostConfiguration.Extensions.cs:57`).
   **survives, invisible** — the slowest layer produces no span and no timing.
5. **repository → EF Core → Postgres** — `AddEntityFrameworkCoreInstrumentation` emits a child DB span, and
   `sqr:ForeverPin.Redirect.Api/Infrastructure/Routing/DbRedirectCodeRepository.cs:19` is EF. **survives**.
6. **outbound HTTP (Stripe, Google)** — `AddHttpClientInstrumentation` is registered, but both callers are vendor
   SDKs (`sqr:ForeverPin.Api/ForeverPin.Api.csproj:14`, `:11`) and no `AddHttpClient` exists in the product.
   **unverified** — see `## Open`.
7. **every log line written along the way** — `[INF] {Message}` and nothing else. Verified from
   `sqr:ForeverPin.Api/logs/log-20260812.txt:1`: `2026-08-12 17:41:11.147 +05:00 [INF] Migrations up to date`.
   **breaks** — no `TraceId`, no `SpanId`, no `SourceContext`, and not one of the four enrichers renders.
8. **failure path** — handlers catch and return a result
   (`sqr:ForeverPin.Infrastructure/Codes/Core/CommandHandlers/CodeDeleteCommandHandler.cs:30`), so nothing reaches
   `Web/ExceptionHandling/UnhandledExceptionHandler.cs:27`. **breaks** — `AppErrorObserver.Record` never runs,
   the span keeps status `Unset`, and `errors_total` never increments. Its only 3 call sites are the two
   exception handlers plus `Mediator/ExceptionHandling/ExceptionToResultBehavior.cs:38`, also unregistered.
9. **failure response** — `sqr:ForeverPin.Api/ControllerProblemExtensions.cs:20` returns a hand-built `ObjectResult`
   and never `IProblemDetailsService`, so `CustomizeProblemDetails` does not run. **breaks** — a business failure
   carries no `traceId`, while a framework 404 does: `"traceId": "00-ae2f4d1e763b1eb481f6a6c34736e961-…"`.
10. **redirect analytics** — `sqr:ForeverPin.Redirect.Api/Infrastructure/Analytics/ChannelScanRecorder.cs:22` hands
    the scan to a channel and `ScanFlushBackgroundService.cs:19` drains it later. **breaks** — `ScanRecord`
    carries no trace id, and the request span has ended by flush time.
11. **cross-service** — the two hosts share Postgres and never call each other, so no HTTP seam needs propagation
    today. `AddConventionalHeaderPropagation` exists but neither host registers it. **not exercised**.

- level filtering is dead: `sqr:ForeverPin.Api/appsettings.json:5` sets `Microsoft.AspNetCore: Warning`, yet
  `log-20260727.txt` holds 59 `Request starting` lines at `[INF]` — Serilog replaces the `ILoggerFactory`, so
  `Logging:LogLevel` is inert, and no `Serilog:MinimumLevel` section exists

---

## Per-method logging

Four ways to get entry / exit / duration without hand-writing it per method.

- **mediator pipeline behavior** — `Mediator/Logging/LoggingBehavior.cs`, registered by one line
  - cost: one DI call; already written, already covered by `Mediator.Tests/Behaviors/LoggingBehaviorTests.cs`
  - covers: every `ISender.SendAsync` request — name, elapsed ms, failure with exception
  - cannot reach: controllers, repositories, background services, vendor SDK calls
  - emits log lines only, opens no span
  - safe by construction — it logs `typeof(TRequest).Name`, never the request body
- **`ActivitySource` span** — the shape `Messaging/Transport/EventProcessingPipeline.cs:41` already uses
  - cost: one `ActivitySource` per module plus a `using var activity = …StartActivity(…)` per method
  - covers: anything hand-instrumented; nests under the server span; `AddSource("WoW.Two.*")` already collects it
  - near-free when unsampled — `StartActivity` returns `null` with no listener attached
  - cannot reach: nothing structurally, but every call site is hand work, and a span is not a log line
- **interceptor / dynamic proxy** — Castle, or a Scrutor decorator
  - cost: a new dependency — no proxy or weaving package sits in `Directory.Packages.props` today
  - cost: interface-dispatch only, a DI registration rewrite, and stack traces that hide the real caller
  - covers: every interface-dispatched call, repositories included
  - cannot reach: sealed, static, and concretely-resolved calls
- **`[LoggerMessage]` source generator** — the SDK's house style already, at 127 call sites
  - cost: one `partial` method per message
  - covers: allocation-free, strongly typed, stable `EventId`
  - cannot reach: anything automatically — it lowers the cost of a log line, never decides one is warranted

**Recommendation.** Register `AddMediatorLoggingBehavior()` in every product, and change `LoggingBehavior` to open
an `ActivitySource` span instead of a bare `Stopwatch` — a duration on a span nests and is queryable, a stopwatch
number is only greppable. Keep `[LoggerMessage]` as the only way an SDK log line is written. Reject interception:
it buys repository coverage that EF Core instrumentation already gives, at the price of a proxy dependency.

---

## Unused Serilog capability

Only what has a concrete use in this codebase today.

- **`{TraceId}` in the output template** — `LogEvent.TraceId` and `OutputProperties.TraceIdPropertyName` both exist
  in the pinned Serilog 4.2.0 (`~/.nuget/packages/serilog/4.2.0/lib/net9.0/Serilog.xml:2241`, `:2767`) and are
  already populated from `Activity.Current`. One template string closes the top gap in `## Verdict`.
- **`LogContext.PushProperty`** — `Enrich.FromLogContext()` is on (`LoggingHostExtensions.cs:21`) and nothing ever
  pushes. Use: push `UserId` / `CodeId` once per request instead of repeating them across eight templates.
- **destructuring policy + `Destructurama.Attributed`** — referenced at
  `WoW.Two.Sdk.Backend.Beta.csproj:235` with zero usages and no `.Destructure.UsingAttributes()` call, so the
  attributes are inert. Use: `[NotLogged]` on `BillingWebhookCommand.RawBody`, `.StripeSignature`, and
  `GoogleSignInCommand.IdToken` before anything is allowed to log a request body.
- **compact JSON formatter** — not referenced anywhere. Use: the file sink is plain text, so `MachineName`,
  `ProcessId`, `ThreadId` and `EnvironmentName` are attached to every event and rendered by nothing.
- **`Serilog.Expressions` filter / sub-logger** — not referenced. Use: drop `Request starting` and
  `Executing endpoint` from the file sink while keeping app events — what the dead `Logging:LogLevel` block wanted.
- **`Serilog.Sinks.Seq`** — pinned at `Directory.Packages.props:82`, absent from the csproj. Use: a structured
  local viewer, the only way the enriched properties above become searchable.
- **sampling** — one concrete candidate: `GET /{slug}` on `forever-pin-redirect` is the single hot route, and it
  writes a full MVC request log per scan into a 7-day rolling file.

---

## Proposed rules

Levels.

- must log `Error` only for a failure the service could not handle and a human must act on
- must log `Warning` for a handled failure — a retried call, a rejected signature, a dropped record
- must log `Information` for a business event that changed state, never for control flow reaching a line
- must log `Debug` for developer detail, and must not depend on it being enabled outside a local run
- must not log per request from application code — the framework already writes one
- must set the minimum level under `Serilog:MinimumLevel`, never `Logging:LogLevel`, which Serilog ignores

Message template.

- must write a constant template with named holes — `"CodeDelete failed for {CodeId}"`, never interpolation
- must name a hole in `PascalCase` after the value's meaning, and keep one name per concept per service
- must declare an SDK log line as a `[LoggerMessage]` partial method with a stable `EventId`
- must not renumber or reuse an `EventId` once released

Never logged.

- must not log a secret, token, password, API key, connection string, or signature header
- must not log a whole request, command, or response — log the identifiers the operation turned on
- must not put a raw exception message into a user-facing error; `AppError` messages reach the caller
- must mark a credential-bearing field `[NotLogged]`, and must call `.Destructure.UsingAttributes()` for it to bite
- must hash or drop a personal identifier before it reaches a sink — `UserAgentHash` is the shape

Seam.

- must inject `ILogger<T>`, and must not name a Serilog type outside the host wiring
- must not use a static or globally shared logger in library or product code
- must let `AddApiDefaults` own the Serilog configuration, and override through `Serilog:*` config, not code

Exceptions.

- must pass an exception as the first argument, never interpolated into the message
- must not log and rethrow the same exception — one or the other, and the outer handler logs
- must let an unexpected exception reach `UnhandledExceptionHandler` rather than catch it in a handler
- must register `AddMediatorExceptionToResultBehavior` when failures are returned as results, so the observer runs
- must record a swallowed failure through `AppErrorObserver` when it is not allowed to propagate

Correlation.

- must render `{TraceId}` in every output template, so a log line joins its trace
- must return a business failure through `IProblemDetailsService`, not an `ObjectResult`, so `traceId` attaches
- must call `AddConventionalHeaderPropagation` + `UseHeaderPropagation` in a service that calls another over HTTP
- must carry the trace context onto work leaving the request scope — a queued record, a flush, an outbox row
- must open an `ActivitySource` span, not a stopwatch, when a unit of work deserves a duration

Hosts.

- must call `AddApiDefaults` / `UseApiDefaults` in every host, the scaffolded template included
- must call `UseApiDefaults` before any middleware that can throw, so `UseExceptionHandler` stays outermost
- must gitignore the `logs/` directory the file sink writes into the content root
- must log a drop when a bounded queue discards work — `ChannelScanRecorder` drops silently today

---

## Open

1. Does `AddHttpClientInstrumentation` cover the `HttpClient` that `Stripe.net` and `Google.Apis.Auth` create
   internally, and does `traceparent` leave on those calls? Not verifiable from this tree.
2. Is the default-on OTLP exporter (`Meta/ApiDefaultsOptions.cs:18`) failing silently against `localhost:4317` on
   every local run? No `OTEL_*` variable is set in forever-pin, and no exporter error appears in any log file.
3. Which backend receives traces in production — a collector, Seq, or Azure Monitor? The sink and sampling rules
   depend on the answer.
4. Should the file sink survive once a structured sink exists, or is it a development-only affordance?
5. Should `AddApiDefaults` fold in `AddMediatorLoggingBehavior` and header propagation, or do they stay opt-in like
   auth and data? `engineering/architecture/analysis/VECTOR-ANALYSIS.md:180` already flags the floor eroding.

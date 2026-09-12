# OpenTelemetry

*Last updated: 2026-09-10*

> Activity and meter instrumentation collected by the SDK's tracing and metrics helpers.

## Instrumentation

- must use `ActivitySource` and `Meter` through long-lived owners, not new instances per operation.
- must name SDK sources and meters by module using `WoW.Two.{Module}`.
- must keep source and meter names stable so hosts can select them independently.
- must dispose an operation's activity when that operation ends.
- must accept `StartActivity` returning `null` when no listener requests the activity.
- must use null-safe activity updates; telemetry sampling must not change business behavior.
- must put expensive tag construction behind the activity's data-request check.
- must reuse instruments and keep metric dimensions bounded.
- must follow the [observability contract](../observability.md#contract) for data and failure ownership.

Platform behavior: [activity instrumentation](https://learn.microsoft.com/en-us/dotnet/core/diagnostics/distributed-tracing-instrumentation-walkthroughs)
and [metrics instrumentation](https://learn.microsoft.com/en-us/dotnet/core/diagnostics/metrics-instrumentation).

---

## Collection

- must register `AddOpenTelemetryTracing` and `AddOpenTelemetryMetrics` with the host's service identity.
- must explicitly register application source and meter names outside the helpers' `WoW.Two.*` selection.
- must configure an exporter separately from instrumentation collection.
- must treat `AddOtlpExporters` as trace and metric export; its current implementation does not export logs.
- must configure a log exporter separately when log export is required.
- must follow the [host composition](../../../../../shapes/service/platform/startup/host-configuration.md)
  owner for boot-floor wiring.

---

## Verification

- must observe a subscribed SDK source and meter through the configured exporter.
- must observe a custom application source only after registering its name.
- must verify trace parentage across outbound and queued work instead of inferring it from a registration call.

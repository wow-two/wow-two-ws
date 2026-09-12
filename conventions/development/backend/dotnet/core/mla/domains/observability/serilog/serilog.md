# Serilog

*Last updated: 2026-09-10*

> Logging through the SDK's host wiring, including failures before the application logger exists.

## Seam

- must inject `ILogger<T>` into application and SDK behavior types.
- must keep Serilog-specific configuration in the host.
- must declare SDK log events with `[LoggerMessage]`, constant named templates and stable event IDs.
- must pass the exception separately from the message template.
- must follow the [observability contract](../observability.md#contract) for sensitive data and failure ownership.
- must use `ErrorRecordingService.Record` for the SDK's combined error log, metric and active-span recording.
- must not record the same error again in a caller after its handling boundary records it.

---

## Host

- must use `UseSerilogConventional` or the explicit boot-floor composition that invokes it.
- must configure Serilog levels under `Serilog:MinimumLevel`.
- must preserve `{TraceId}` in text sinks used to correlate operations.
- must verify custom sink templates; adding a sink does not inherit another sink's output template.
- must keep the log directory outside version control and configure storage retention in the deployment.
- must keep source defaults in the [SDK logging owner](../../../../../../../../../workbench/wow-two-sdk-beta/wow-two-sdk.backend.beta/engineering/codebase/wow-two-back-beta-sdk/src/Observability/Logging/logging.md).

---

## Startup

- must initialize bootstrap logging before creating or building the host.
- must give bootstrap failures a durable sink that does not depend on application DI or the final pipeline.
- must keep the startup failure channel independently readable from the application log.
- must capture host creation, binding, validation and startup exceptions at the outer host boundary.
- must preserve the original exception and a nonzero process exit on startup failure.
- must flush bootstrap events during failure shutdown and configure final logging separately.
- must not assume `UseSerilogConventional` alone captures failures before its host callback runs.
- may use the [two-stage initialization](https://github.com/serilog/serilog-aspnetcore#two-stage-initialization)
  bootstrap logger; the final logger replaces it and needs its own sink configuration.

---

## Verification

- must exercise a failure before host construction and a failure during options validation.
- must confirm both remain in the startup channel after process exit.
- must confirm a normal startup hands off to final logging without duplicate application events.

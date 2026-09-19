# C22 observability contract verification

*Verified: 2026-09-16*

## Result

C22 is complete. SDK sources and meters are collected by the brand-prefixed helpers, message trace context crosses the queue boundary, metrics retain bounded dimensions and exporter failure does not replace the operation result.

## Corrections

- `AddOtlpExporters` documentation now states traces and metrics only; log export remains separate.
- `LoggingInterceptor` opens a long-lived-module `WoW.Two.Mediator` activity for each request.
- The interceptor no longer logs and rethrows failures; the result/exception handling boundary records them once.
- `ErrorRecordingService` marks the span as failed without copying the potentially unbounded application message into the status description.
- OTLP and tracing/metrics examples now pass a `Uri` matching the shipped signature.

## Verification

- `dotnet build Mediator.Tests/WoW.Two.Sdk.Backend.Beta.Mediator.Tests.csproj --no-restore -m:1`: passed.
- `dotnet test Mediator.Tests/WoW.Two.Sdk.Backend.Beta.Mediator.Tests.csproj --no-build -m:1`: 69 passed.
- `dotnet build Messaging.Tests/WoW.Two.Sdk.Backend.Beta.Messaging.Tests.csproj --no-restore -m:1`: passed.
- `dotnet test Messaging.Tests/WoW.Two.Sdk.Backend.Beta.Messaging.Tests.csproj --no-build -m:1`: 121 passed, 1 Kafka test skipped.
- Focused tests observe `WoW.Two.*` activity and meter export, producer-to-consumer parentage, the two allowed messaging metric dimensions, disabled-listener transparency through the existing suites and a throwing trace exporter that cannot replace the operation result.

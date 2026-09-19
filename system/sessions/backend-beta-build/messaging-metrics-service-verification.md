# Messaging metrics service verification

*Last updated: 2026-09-15*

## Scope

- `IMessagingMetrics` → `IMessagingMetricsService`.
- `DefaultMessagingMetrics` → `DefaultMessagingMetricsService`.
- `NoOpMessagingMetrics` → `NoOpMessagingMetricsService`.
- All three types moved to `Messaging/Services/` with matching namespace.
- Updated exact DI registration, pipeline/bus/pump dependencies, XML and feature/planning documentation: 13 files.
- Concrete summaries start with `Provides`; interface summary with `Defines`.
- Preserved the method API, meter/instrument names, tags, counters/histogram, probe registration/removal,
  gauge observation, disposal, default singleton `TryAdd` behavior and no-op instance semantics.
- `MessagingMeterConstants` and other suffix families are unchanged.
- No new tests, package changes, staging, commits or pushes.

---

## Checks

- `dotnet build Messaging.Tests/WoW.Two.Sdk.Backend.Beta.Messaging.Tests.csproj --no-restore -m:1`, from SDK `src/`:
  exit 0, 170 warnings, 0 errors. Log: `/private/tmp/messaging-metrics-service-build.log`.
- `dotnet test Messaging.Tests/WoW.Two.Sdk.Backend.Beta.Messaging.Tests.csproj --no-build --no-restore --filter FullyQualifiedName~MessagePumpTests`:
  exit 0, 4 passed, 0 failed, 0 skipped. Native permission granted and execution completed; session `35199`.
- Exact old-type search under SDK content, excluding generated output and the parent-owned historical sweep tracker,
  returned no references.
- SDK `git diff --check` passed.

---

## Coverage limits and prior lane

- No existing tests directly assert metrics instruments, tags or values. The four pump cases exercise default DI,
  sequential/parallel dispatch, keyed ordering and shutdown through the affected publishing/consuming components.
- The preceding guest-session service work is complete: Identity.Tests build passed with 62 warnings and 0 errors;
  its existing configured-registration test passed 1/1. See
  [guest-session-service-verification.md](guest-session-service-verification.md) for details and the retained hash-chain follow-up.
- These are scoped local checks, not full SDK or release validation.

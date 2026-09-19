# Envelope role verification

*Last updated: 2026-09-15*

## Scope

- `EventEnvelope` → `EventEnvelopeModel`, moved to `Messaging/Models/` with matching namespace.
- `OtpDeliveryEnvelope` → `OtpDeliveryEnvelopeModel`, moved to `Identity/Otp/Models/` with matching namespace.
- `ApiEnvelope<T>` → `TestApiResponse<T>`, kept beside HTTP test helpers under `Testing/Web/`.
- Updated exact source, XML, feature/planning documentation and existing test references: 84 files.
- All domain event names retain their existing `Event` suffix; no `EventModel` domain-event renames.
- Preserved wrapper properties, defaults, payload type/routing behavior, serialization helpers and method APIs.
- `TestApiResponse<T>` remains a data-only success-response mirror with exactly `[JsonPropertyName("data")]`
  on `Data`; `ReadEnvelopeAsync<T>` keeps its method name and behavior.
- No new tests, package changes, staging, commits or pushes.

---

## Checks

Commands ran serially from SDK `src/`.

- `dotnet build Messaging.Tests/WoW.Two.Sdk.Backend.Beta.Messaging.Tests.csproj --no-restore -m:1`:
  exit 0, 170 warnings, 0 errors. Log: `/private/tmp/envelope-messaging-build.log`.
- `dotnet build Testing/WoW.Two.Sdk.Backend.Beta.Testing.csproj --no-restore -m:1`:
  exit 0, 5 warnings, 0 errors. Log: `/private/tmp/envelope-testing-build.log`.
- `dotnet test Messaging.Tests/WoW.Two.Sdk.Backend.Beta.Messaging.Tests.csproj --no-build --no-restore --filter FullyQualifiedName~ClaimCheckTests`:
  exit 0, 8 passed, 0 failed, 0 skipped. Native permission granted; actual execution completed in session `54075`.
- SDK-wide exact old-type search excluding generated output and the parent-owned historical sweep tracker returned no references.
- SDK `git diff --check` passed.

---

## Coverage limits

- Existing claim-check tests exercise the event wrapper's body substitution, wire bytes/type, rehydration and failure paths
  using in-memory transport and a recording blob repository.
- No direct OTP-delivery-wrapper or HTTP test-response-mirror tests were found. Those changes have source and compile coverage.
- These are scoped local checks, not live broker compatibility, full SDK or release validation.

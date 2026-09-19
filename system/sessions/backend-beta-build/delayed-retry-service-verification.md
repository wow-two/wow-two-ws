# Delayed retry service verification

*Last updated: 2026-09-13*

> Scoped evidence for the confirmed delayed-retry orchestration rename.

## Scope

- `DelayedRetryCoordinator` → `DelayedRetryService`.
- Declaration moved into `Messaging/Reliability/Services/`, with matching namespace.
- Constructor, logger category type, DI registration, exact caller references and XML/comment references follow the name.
- Scheduling order, retry decisions, retry budgets, cancellation and failure fallback remain unchanged.
- `SecondLevelRetryCoordinator` retains its own name and behavior; only its renamed dependency references changed.
- `SagaCoordinator` remains untouched.

Changed files, relative to the SDK's `engineering/codebase/wow-two-back-beta-sdk/src/Messaging/`:

- `Reliability/Services/DelayedRetryService.cs` (moved declaration).
- `Reliability/DelayedRetryServiceCollectionExtensions.cs`.
- `Reliability/SecondLevelRetryCoordinator.cs`.
- `Reliability/Polly/PollyEventResilienceServiceCollectionExtensions.cs`.
- `InMemory/DefaultEventResiliencePipeline.cs`.
- `Transport/EventProcessingPipeline.cs`.

---

## Verification

Commands ran serially from the SDK source directory using .NET SDK `10.0.300`.

- `dotnet build Messaging.Tests/WoW.Two.Sdk.Backend.Beta.Messaging.Tests.csproj --no-restore -m:1`
  passed: exit 0, 170 warnings, 0 errors.
- `dotnet test Messaging.Tests/WoW.Two.Sdk.Backend.Beta.Messaging.Tests.csproj --no-build --no-restore --filter FullyQualifiedName~FaultClassificationAndBusControlTests`
  passed: exit 0, 6 passed, 0 failed, 0 skipped.
- The test command used native `require_escalated` approval for the runner's local socket; the actual execution result completed.
- SDK `engineering/` search found no remaining `DelayedRetryCoordinator` references outside generated output.
- `git diff --check` passed.
- Logs: `/private/tmp/delayed-retry-service-build.log` and `/private/tmp/delayed-retry-service-tests.log`.

---

## Limits

- The existing tests exercise in-memory fault outcomes and bus control, not the enabled delayed-redelivery path.
- Build warnings include existing dependency advisories and analyzer findings; the build is not warning-clean.
- The pre-existing options registration inside `AddDelayedEventRetry`'s `Configure` callback remains outside this rename.
  The root lane received the exact finding for its existing options-registration sweep.
- No new tests, package version changes, commits, pushes or release verification.

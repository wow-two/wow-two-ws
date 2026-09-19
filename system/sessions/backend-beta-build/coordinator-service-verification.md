# Coordinator service verification

*Last updated: 2026-09-13*

> Scoped evidence for the confirmed second-level retry and saga service names.

## Scope

- `SecondLevelRetryCoordinator` → `SecondLevelRetryService` under `Messaging/Reliability/Services/`.
- `SagaCoordinator<TState>` → `SagaService<TState>` under `Messaging/Saga/Services/`.
- Namespace, constructor, logger category type, exact DI registrations, handler/interceptor callers and documentation references follow the names.
- `NoOpMigrationRunner` → `NoOpMigrationRunnerService` under `Testing.Data/Migrations/Services/`, matching its existing `IMigrationRunnerService` contract.
- The no-op registration and null-object convention example follow the actual renamed file.
- Retry decisions, scheduling, saga state changes, concurrency replay and empty migration results are unchanged.
- No new tests, package version changes or Git mutations.

---

## Checks

Commands ran serially from the SDK's `engineering/codebase/wow-two-back-beta-sdk/src/`.

- `dotnet build Messaging.Tests/WoW.Two.Sdk.Backend.Beta.Messaging.Tests.csproj --no-restore -m:1`
  passed: exit 0, 170 warnings, 0 errors.
- `dotnet build Testing.Data/WoW.Two.Sdk.Backend.Beta.Testing.Data.csproj --no-restore -m:1`
  passed: exit 0, 47 warnings, 0 errors.
- Old-name search under SDK `engineering/`, excluding generated output, found no remaining references to the three old names.
- `git diff --check` passed for SDK changes and the edited null-object convention.
- Build logs: `/private/tmp/coordinator-service-messaging-build.log` and `/private/tmp/coordinator-service-testing-data-build.log`.

---

## Test execution

- Requested existing `SagaStateMachineTests`, `SagaTestHarnessTests` and `FaultClassificationAndBusControlTests` together.
- Command: `dotnet test Messaging.Tests/WoW.Two.Sdk.Backend.Beta.Messaging.Tests.csproj --no-build --no-restore --filter 'FullyQualifiedName~SagaStateMachineTests|FullyQualifiedName~SagaTestHarnessTests|FullyQualifiedName~FaultClassificationAndBusControlTests'`.
- The first native permission request was dismissed because the session ended; no tests ran from that request.
- Retried the same scoped command through native escalation without shell output redirection and retained execution until completion.
- Result: exit 0, 17 passed, 0 failed, 0 skipped; duration 2 seconds. Tool execution session: `35183`.
- The passing result was captured directly in tool output; the original `/private/tmp/coordinator-service-tests.log` target is not the passing-run evidence.
- Existing tests cover saga transitions and messaging behavior; no enabled second-level retry scenario was found in the current test source.
- These tests used the normal binaries from the builds above. The later event-saga rename was separately compiled with isolated outputs; see
  [event-saga-service-verification.md](event-saga-service-verification.md).

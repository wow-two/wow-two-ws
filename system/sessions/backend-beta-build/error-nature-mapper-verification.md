# Error nature mapper verification

*Last updated: 2026-09-13*

> Scoped evidence for the confirmed error-nature mapper rename.

## Scope

- `IErrorNatureClassifier` → `IErrorNatureMapper`.
- `ErrorNatureClassifier` → `ErrorNatureMapper`.
- Both files moved into `Foundation/Errors/Mappers/`, with the matching namespace.
- Contract method and exact implementations/callers changed from `Classify` to `Map`.
- Existing `ErrorNatureTests` scenarios retain their inputs and assertions.
- `ErrorRecordingService` still maps the same error type before choosing its logging behavior.
- `TryAddSingleton<IErrorNatureMapper, ErrorNatureMapper>` preserves consumer DI overrides.
- `EventFaultClassifier` and `IEventFaultClassifier` remain unchanged by this lane.
- Runtime mapping branches are unchanged; no new tests, Git mutations or package changes.

---

## Changed references

Paths are relative to the SDK's `engineering/codebase/wow-two-back-beta-sdk/src/`.

- `Foundation/Errors/Mappers/IErrorNatureMapper.cs` and `ErrorNatureMapper.cs`.
- `Foundation/Errors/errors.md`.
- `Foundation.Tests/Errors/ErrorNatureTests.cs`.
- `Observability/Errors/AppErrorObserverServiceCollectionExtensions.cs`.
- `Observability/Errors/ErrorRecordingService.cs`.
- `Mediator.Tests/Behaviors/ExceptionToResultBehaviorTests.cs`.
- SDK `engineering/planning/errors/errors-architecture-investigation.md` exact type references.

---

## Verification

- Permission recovery completed through native escalation for the scoped test commands.
- `ErrorNatureTests`: 16 passed, 0 failed, 0 skipped.
- `ExceptionToResultBehaviorTests`: 6 passed, 0 failed, 0 skipped.
- Both used `dotnet test <project> --no-build --no-restore --filter FullyQualifiedName~<test-class> --nologo -v:q`.
- The original socket failure below is historical; no test-runner permission block remains for these checks.

- SDK `engineering/` search found no remaining `IErrorNatureClassifier` or `ErrorNatureClassifier` references outside generated output.
- `git diff --check` passed.
- The existing Foundation test command compiled the changed SDK and Foundation.Tests project.
- Test execution aborted because the sandbox denied the test runner's local socket: `SocketException (13): Permission denied`.
- Scoped command: `dotnet test Foundation.Tests/WoW.Two.Sdk.Backend.Beta.Foundation.Tests.csproj --no-restore -m:1 --filter FullyQualifiedName~ErrorNatureTests`.
- Original log: `/private/tmp/error-nature-mapper-foundation-tests.log`.
- Native escalation for the same tests was dismissed because the session ended; no approved run occurred.
- Retry log target: `/private/tmp/error-nature-mapper-foundation-tests-approved.log`.
- The dependent Mediator project compile passed in the following policy-rename batch: exit 0, 109 warnings, 0 errors.
- Command: `dotnet build Mediator.Tests/WoW.Two.Sdk.Backend.Beta.Mediator.Tests.csproj --no-restore -m:1`.
- Consumer build log: `/private/tmp/error-nature-mapper-mediator-build.log`.
- Test passes are recorded above; no pack or release result is claimed.

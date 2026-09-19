# Event fault policy verification

*Last updated: 2026-09-13*

> Scoped evidence for the confirmed event-fault policy rename.

## Permission recovery

Native escalation resolved the test-runner local-socket restriction. Existing
`FaultClassificationAndBusControlTests` executed: 6 passed, 0 failed, 0 skipped.
Command: `dotnet test Messaging.Tests/WoW.Two.Sdk.Backend.Beta.Messaging.Tests.csproj --no-build --no-restore --filter FullyQualifiedName~FaultClassificationAndBusControlTests --nologo -v:q`.
Compilation-only limitations in the original evidence below are superseded by this scoped test result;
no whole-suite, pack or release claim is made.

---

## Scope

- `IEventFaultClassifier` → `IEventFaultPolicy`.
- `EventFaultClassifier` → `EventFaultPolicy`.
- Both declarations moved into `Messaging/Reliability/Policies/`, with matching namespace.
- The decision method changed from `Classify(Exception)` to `Decide(Exception)`.
- Exact pipeline fields/parameters, calls, registration references, XML links and package docs follow the names.
- Custom registration changed to `AddEventFaultPolicy<TPolicy>` and retains `Replace` semantics.
- `AddEventFaultClassification` and `EventFaultClassificationOptions` retain their configured-rule API.
- `EventFaultClassificationOptions.Classify(rule)` adds a rule; it does not evaluate a fault, so it is unchanged.
- First non-null configured verdict still wins; throwing rules still fall through; no match still returns `Retry`.
- The default registration remains `TryAddSingleton` with `RetryAll`, preserving custom DI overrides.
- No other classifiers/parsers, runtime branches, tests, package versions or Git state were changed by this lane.

---

## Files

Paths below are relative to the SDK's `engineering/codebase/wow-two-back-beta-sdk/src/Messaging/`.

- `Reliability/Policies/IEventFaultPolicy.cs` and `EventFaultPolicy.cs`.
- `Reliability/EventFaultClassificationServiceCollectionExtensions.cs`.
- `Reliability/IEventResiliencePipeline.cs`.
- `Reliability/DelayedRetryCoordinator.cs` and `SecondLevelRetryCoordinator.cs`.
- `Reliability/Polly/PollyEventResiliencePipeline.cs` and `PollyEventResilienceServiceCollectionExtensions.cs`.
- `InMemory/DefaultEventResiliencePipeline.cs`.
- `MessagingServiceCollectionExtensions.cs` and `ConsumeOutcome.cs`.
- `Transport/EventProcessingPipeline.cs` (comment reference).
- `Messaging.spec.md` and `Messaging.standard.md`.

---

## Verification

Commands ran serially from the SDK source directory with .NET SDK `10.0.300`.

- `dotnet build Messaging.Tests/WoW.Two.Sdk.Backend.Beta.Messaging.Tests.csproj --no-restore -m:1`
  passed: exit 0, 170 warnings, 0 errors. This compiled shared SDK and testing dependencies as well as existing messaging tests.
- `dotnet build Mediator.Tests/WoW.Two.Sdk.Backend.Beta.Mediator.Tests.csproj --no-restore -m:1`
  passed: exit 0, 109 warnings, 0 errors. This closes the renamed error-nature mapper's dependent consumer compile.
- Warnings include existing analyzer findings and dependency advisories; these builds are not warning-clean.
- SDK `engineering/` search found no old `EventFaultClassifier` or `IEventFaultClassifier` names outside generated output.
- No renamed-policy caller retains `_faultPolicy.Classify`.
- `git diff --check` passed.
- Logs: `/private/tmp/event-fault-policy-messaging-build.log` and `/private/tmp/error-nature-mapper-mediator-build.log`.
- Runtime tests passed through native escalation as recorded above. No whole-suite, pack or release claim is made.

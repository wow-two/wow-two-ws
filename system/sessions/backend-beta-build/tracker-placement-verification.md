# Tracker placement verification

*Verified: 2026-09-15*

## Result

The three previously renamed trackers now occupy `Trackers/` role folders with matching namespaces. Their type summaries already began with `Tracks`; those summaries and all runtime logic remain unchanged. This closes the placement remainder for these three types, not the broader SDK conformance sweep.

SDK root: `workbench/wow-two-sdk-beta/wow-two-sdk.backend.beta`.

All `src/` paths below are relative to its `engineering/codebase/wow-two-back-beta-sdk/` directory.

## Moves

| Type | Previous path | Current path | Current namespace |
|---|---|---|---|
| `InterceptorInvocationTracker` | `src/Data.Tests/Harness/InterceptorInvocationTracker.cs` | `src/Data.Tests/Harness/Trackers/InterceptorInvocationTracker.cs` | `WoW.Two.Sdk.Backend.Beta.Data.Tests.Harness.Trackers` |
| `RecordedMessageTracker` | `src/Testing.Messaging/RecordedMessageTracker.cs` | `src/Testing.Messaging/Trackers/RecordedMessageTracker.cs` | `WoW.Two.Sdk.Backend.Beta.Testing.Messaging.Trackers` |
| `RecordedTransitionTracker<TState>` | `src/Testing.Messaging/RecordedTransitionTracker.cs` | `src/Testing.Messaging/Trackers/RecordedTransitionTracker.cs` | `WoW.Two.Sdk.Backend.Beta.Testing.Messaging.Trackers` |

The data-test tracker stays owned by the existing `Harness` capability. Messaging trackers remain owned by the testing-messaging domain.

## Consumer updates

Added the appropriate tracker namespace import to:

- `src/Data.Tests/Harness/FirstRecordingInterceptor.cs`
- `src/Data.Tests/Harness/SecondRecordingInterceptor.cs`
- `src/Data.Tests/Harness/RecordingSaveChangesInterceptorBase.cs`
- `src/Data.Tests/Tests/InterceptorWiringTests.cs`
- `src/Testing.Messaging/MessagingRecorder.cs`
- `src/Testing.Messaging/MessagingTestHarness.cs`
- `src/Testing.Messaging/SagaRecorder.cs`
- `src/Testing.Messaging/SagaTestHarness.cs`

Updated `src/Testing.Messaging/Testing.Messaging.md` to identify the role namespace for callers that name the public tracker types explicitly.

An exact-symbol search of current `.cs` and `.md` files under workspace `workbench/`, excluding generated directories and the historical sweep register, found references only in this SDK. SDK engineering source/docs contain no old tracker file-path references or fully qualified pre-move tracker names. Historical session evidence is retained as history.

## Validation

Commands ran serially from SDK `engineering/codebase/wow-two-back-beta-sdk/src/`:

| Command | Result |
|---|---|
| `dotnet build Data.Tests/WoW.Two.Sdk.Backend.Beta.Data.Tests.csproj --no-restore -m:1 -v:q` | Exit 0; 87 warnings, 0 errors. Log: `/tmp/tracker-data-build.log`. |
| `dotnet build Messaging.Tests/WoW.Two.Sdk.Backend.Beta.Messaging.Tests.csproj --no-restore -m:1 -v:q` | Exit 0; 154 warnings, 0 errors. Compiled its `Testing.Messaging` dependency. Log: `/tmp/tracker-messaging-build.log`. |
| `dotnet test Messaging.Tests/WoW.Two.Sdk.Backend.Beta.Messaging.Tests.csproj --no-build --no-restore --filter 'FullyQualifiedName~MessagingTestHarnessTests\|FullyQualifiedName~SagaTestHarnessTests' -v:minimal` | Exit 0; 13 passed, 0 failed, 0 skipped; .NET 10. The backslash before the pipe is Markdown table escaping, not part of the executed filter. |
| `git diff --check -- engineering/codebase/wow-two-back-beta-sdk/src/Data.Tests engineering/codebase/wow-two-back-beta-sdk/src/Testing.Messaging` | Exit 0. |

The first test invocation aborted before running tests because VSTest could not bind its local communication socket (`SocketException (13): Permission denied`). The same scoped command was retried through native `require_escalated` execution. That execution remained alive until it returned the actual passing result (session `15442`, exit 0); there is no pending approval or unresolved permission block.

The existing messaging tests exercise recorded round trips, delivery faults, waits/timeouts, saga transitions, concurrency replay and scheduled timeouts. No new tests were added for these namespace-only moves.

## Limits

- Data interceptor runtime tests were not run: their shared fixture provisions Postgres. Data-test verification here is compilation only.
- Existing build warnings remain outside this mechanical slice.
- The public messaging-tracker namespaces changed; consumers that name those types must import the new namespace.
- No queue, synchronization, waiting, cancellation, DI registration or assertion behavior changed.
- No staging, commit, push, CI run or release occurred.

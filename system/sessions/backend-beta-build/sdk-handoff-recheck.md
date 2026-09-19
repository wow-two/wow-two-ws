# SDK handoff recheck

*Last updated: 2026-09-15*

> Live-source verification of completed naming slices versus remaining SDK conformance work.

## Verdict

Subsequent N100 closure: [exporter verification](exporter-conformance-verification.md) closes the remaining
Exporter contract work below. The core compiled, 34 runtime scenarios were inspected, and seven CSV cancellation
regression assertions passed. N100 has left the active handoff; N101 and general N108 documentation work remain.
Earlier findings below record the original inspection, not reopened tasks.

Subsequent Parser closure: [parser conformance verification](parser-conformance-verification.md) supersedes
the Parser residual below. All 14 declarations moved to owning role folders, contracts describe actual input
behavior, and Cron occurrence calculation uses the parsed result. Compilation and 17 existing VTT cases passed;
other parser formats retain the stated source-only verification boundary. Transport/Exporter work remains.

Subsequent N91 closure: [CloudEvents decoder verification](cloudevents-decoder-verification.md) supersedes
the inspected decoder gap below. Complete-document validation and malformed-input failure results are applied;
all 37 serializer tests passed, including 15 new regressions. Inbound context attributes remain semantically
unvalidated by this payload decoder. N91 is removed from the active handoff again with fresh evidence.

Subsequent work in the same turn: the tracker placement gap below is closed by
[tracker placement verification](tracker-placement-verification.md): both affected builds passed and all
13 existing messaging/saga harness tests passed. The inspected paths below record the earlier snapshot;
the report lists the new paths. General member-documentation work remains under N108.

All confirmed session renames are present in current non-generated C# source, and searches for the exact retired symbols return no matches. Remove their rename instructions from the active handoff; retain the reports as evidence. N100/N101 cannot yet close: Parser and Transport conformance remain, alongside the narrower retained-role contract and documentation follow-ups below. This is a source/report recheck, not a new build or test run.

SDK paths below are relative to `workbench/wow-two-sdk-beta/wow-two-sdk.backend.beta/engineering/codebase/wow-two-back-beta-sdk/src`.

---

## Verified completed naming slices

| Slice | Current declarations and placement | Current wiring/reference evidence |
|---|---|---|
| Recorder names | `Data.Tests/Harness/InterceptorInvocationTracker.cs:8`; `Testing.Messaging/RecordedMessageTracker.cs:16`; `RecordedTransitionTracker.cs:18` | `Data.Tests/Harness/RecordingSaveChangesInterceptorBase.cs:9`; `Testing.Messaging/MessagingRecorder.cs:27`; `SagaTestHarness.cs:122` |
| Error classification | `Foundation/Errors/Mappers/ErrorNatureMapper.cs:4`, `IErrorNatureMapper.cs:4` | `Observability/Errors/AppErrorObserverServiceCollectionExtensions.cs:20` registers the interface/implementation |
| Fault decisions | `Messaging/Reliability/Policies/EventFaultPolicy.cs:10`, `IEventFaultPolicy.cs:15` | `MessagingServiceCollectionExtensions.cs:87` supplies default; `Reliability/EventFaultClassificationServiceCollectionExtensions.cs:25,36` retains configured/custom overrides |
| Retry orchestration | `Messaging/Reliability/Services/DelayedRetryService.cs:17`, `SecondLevelRetryService.cs:17` | `DelayedRetryServiceCollectionExtensions.cs:40`, `SecondLevelRetryServiceCollectionExtensions.cs:45` |
| Saga orchestration | `Messaging/Saga/Services/SagaService.cs:18`; `Messaging/EventSaga/Services/EventSagaService.cs:13`, `IEventSagaService.cs:8` | `Saga/SagaServiceCollectionExtensions.cs:43`; `MessagingServiceCollectionExtensions.cs:171` |
| No-op migration runner | `Testing.Data/Migrations/Services/NoOpMigrationRunnerService.cs:11` | `Testing.Data/Migrations/NoOpBespokeMigratorExtensions.cs:23` registers against `IMigrationRunnerService` |
| Formatters | Both relative-time and humanized-text interface/implementation pairs under `Localization/Formatters/` | `LocalizationServiceCollectionExtensions.cs:79–80` registers both approved pairs |
| Google identity evidence | `Identity/OAuth/Google/Authenticators/GoogleIdTokenAuthenticator.cs:9`, `IGoogleIdTokenAuthenticator.cs:4` | `GoogleIdTokenAuthenticatorServiceCollectionExtensions.cs:21` |
| Hash integrity | `Foundation/Audit/Validators/HashChainValidator.cs:9`, `IHashChainValidator.cs:6`; result is `HashChainValidationResult` | `HashChainServiceCollectionExtensions.cs:30,55`; method contract is `Validate` |
| Guest sessions | `Identity/Guest/Services/IGuestSessionService.cs:4`, `CookieGuestSessionService.cs:8` | `GuestSessionServiceCollectionExtensions.cs:24`; existing registration assertion at `Identity.Tests/ConfiguredRegistrationTests.cs:31` |
| Messaging metrics | Three approved `*MessagingMetricsService` declarations under `Messaging/Services/` | `MessagingMetricsServiceCollectionExtensions.cs:22`; the no-op override guidance references the renamed interface |
| Internal envelopes | `Messaging/Models/EventEnvelopeModel.cs:10`; `Identity/Otp/Models/OtpDeliveryEnvelopeModel.cs:4` | `Identity/Otp/IOtpDeliveryHandler.cs:11`; message recorders and transport operations refer to `EventEnvelopeModel` |
| HTTP test mirror | `Testing/Web/TestApiResponse.cs:13`, a data-only record | `Testing/Web/HttpExtensions.cs:71,74` consumes the renamed mirror |
| Exporter placement | Three retained declarations in `Media/Csv/Exporters`, `Media/Excel/Exporters`, `Media/Tabular/Exporters` | CSV registrations at `CsvServiceCollectionExtensions.cs:23–24`; Excel at `ExcelServiceCollectionExtensions.cs:22–23` |
| Serializer placement | GeoJSON pair under `Geo/GeoJson/Serializers`; four messaging declarations under `Messaging/Serialization/Serializers` | `MessagingServiceCollectionExtensions.cs:88,229–244` references the moved contracts and preserves default/custom selection |
| Bus placement | `Messaging/Buses/IEventBus.cs:10`, `TransportEventBus.cs:20` | `MessagingServiceCollectionExtensions.cs:67`; provider registration files reference the same bus implementation |

The recorder row verifies names and consumers only; it does not certify role-folder or XML documentation completion.

---

## Retain as concrete SDK work

1. **Parser conformance:** 14 declarations remain outside `Parsers/`, in `Foundation/Time`, `Media/Captions` and `Media/Csv`. `Foundation/Time/ICronExpressionParser.cs:18` exposes `NextOccurrence`, an operation over the parsed result; `:7` starts the interface summary with `Provides`. Complete placement, interface documentation and the agreed syntax-only responsibility separation. These are implementation tasks under the retained Parser decision.
2. **Transport conformance:** provider transports remain directly under provider folders; shared interfaces remain under singular `Messaging/Transport`. `Messaging/EventSaga/InProcessEventSagaTransport.cs:20–34` orchestrates routing checks and calls `IEventBus.SendAsync`; it does not own a delivery medium. Apply the settled Service boundary for that wrapper and finish Transport placement/docs rather than treating retention of the Transport suffix as completion.
3. **Recorder completion beyond rename:** at inspection all three renamed trackers remained in their pre-rename folders, outside `Trackers/`. Parent has dispatched the placement repair to its own lane; that lane's final evidence supersedes this snapshot. `Testing.Messaging/RecordedMessageTracker.cs:7–15` still used multiline summary/remarks and `:26–34` had property/method summaries without the required starters/returns coverage. Keep documentation/placement work only until its owning lane verifies it; do not repeat the completed rename.
4. **Retained-role behavior contracts:** retain the explicit follow-ups in [retained-role verification](retained-role-conformance-verification.md). Exporter schema/empty-input/stream/partial-output contracts are not complete; `ExcelTabularExporter.cs:20–25` only checks cancellation before synchronous in-memory workbook creation/save. GeoJSON retains lossy ID reconstruction and permissive feature-collection input. CloudEvents malformed-input work is owned by the active source lane and must not be declared complete from this recheck.
5. **Hash-chain segments:** `Foundation/Audit/HashChain.standard.md:39–40` and `audit.md:57` still recommend validation of version segments, while `Validators/HashChainValidator.cs:36–37` always starts at sequence 1 with an empty previous hash. The rename and honest consistency-only summaries are complete; segment/checkpoint contract reconciliation remains.
6. **Google cancellation/options:** `GoogleIdTokenAuthenticator.cs:29` accepts cancellation, but `:41` invokes the provider without using that token. `GoogleIdTokenAuthenticatorOptions.cs:7` exposes a get-only mutable audience collection. Preserve these existing behavior/options follow-ups separately from the completed Authenticator naming slice.

No new suffix or user naming decision is required for these residuals.

### N91 reopening

The historical completed N91 claim that malformed serializer input never throws is refuted by the inspected current CloudEvents implementation. Reopen N91 rather than burying this defect in N101 naming work:

- `Messaging/Serialization/Serializers/IMessageSerializer.cs:27–28` explicitly promises `SerializationFailed` for malformed input and no throw for undecodable bodies.
- `CloudEventsMessageSerializer.cs:82–126` has no exception-to-failure boundary. `Utf8JsonReader.Read` at `:90/:94`, `JsonSerializer.Deserialize` at `:105/:118` and `GetBytesFromBase64` at `:114` can throw on malformed input.
- The immediate returns at `:105/:116/:118` also skip the remainder of the JSON document. Whole-document acceptance is an additional boundary question, distinct from conversion of parse failures.
- The active CloudEvents source lane owns correction and regression evidence. A later verified fix can close N91 again; a historical checked marker cannot certify the inspected implementation.

This recheck does not validate other historical completed sweep rows outside its explicit naming/serializer scope.

---

## Verification evidence rechecked

- All session verification reports referenced below exist. Their test-class targets also remain in current source: error nature, exception-to-result, fault/bus control, saga state/harness, guest registration, message pump, claim check and message serializer tests.
- Retained build logs were read, not merely checked for existence. Recorder, mapper consumer, policy, retry/coordinator, event-saga, formatter, Google, hash, guest, metrics, envelope and retained-role logs contain `Build succeeded` with zero errors; their recorded nonzero warnings remain.
- `/private/tmp/delayed-retry-service-tests.log` still contains 6 passed, 0 failed, 0 skipped.
- The mapper approved-log path and original coordinator test-log path do not exist. Their reports explicitly identify the initial dismissed requests and separately record later successful native tool output; do not cite those missing paths as passing-run logs.
- Reports retain these earlier results: mapper/consumer/policy 28 tests; coordinator/saga 17; guest registration 1; metrics pump 4; envelope claim check 8; retained serializer/bus 26. They overlap and must not be summed as unique coverage. They are historical scoped results, not newly rerun against every subsequent edit.
- Existing reports accurately retain missing direct runtime coverage for formatters, Google/hash checks, event-saga step execution, exporters and GeoJSON. Those limitations do not undo completed mechanical naming, but they prevent a blanket runtime/release claim.

Evidence owners: [recorders](recorder-rename-verification.md), [mapper](error-nature-mapper-verification.md), [policy](event-fault-policy-verification.md), [delayed retry](delayed-retry-service-verification.md), [coordinators](coordinator-service-verification.md), [event saga](event-saga-service-verification.md), [formatters](humanized-text-formatter-verification.md), [Google](google-id-token-authenticator-verification.md), [hash chain](hash-chain-validator-verification.md), [guest](guest-session-service-verification.md), [metrics](messaging-metrics-service-verification.md), [envelopes](envelope-role-verification.md), [retained roles](retained-role-conformance-verification.md).

---

## Handoff cleanup

- Remove completed rename instructions and Exporter/Serializer/Bus relocation instructions from the active handoff.
- Keep the narrow residuals above and their existing task ownership; keep completed verification reports as history.
- N100/N101 remain source-conformance rows, not unanswered vocabulary rows.
- SDK work is not empty; this recheck does not justify moving directly to CI or release.
- Only this report was written by the recheck lane. No SDK source, tracker, Git state, build output or package state was changed.

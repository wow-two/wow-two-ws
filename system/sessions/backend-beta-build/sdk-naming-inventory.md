# SDK naming inventory — N100 / N101

Date: 2026-09-13. Read-only source inspection; no Git mutation or SDK edits.

## Current disposition

Updated 2026-09-15: all naming decisions are closed. The [active SDK handoff](../../../workbench/wow-two-sdk-beta/wow-two-sdk.backend.beta/be-convention-sweep.md)
owns remaining implementation; [live recheck](sdk-handoff-recheck.md) verifies completed source slices.
Exporter/Serializer/Bus role placements are complete ([evidence](retained-role-conformance-verification.md)).
The three recorder Trackers role placements are also complete ([evidence](tracker-placement-verification.md)).
Parser placement/responsibility and contract documentation are complete; compilation and 17 existing VTT cases
passed against the current SDK ([evidence](parser-conformance-verification.md)).
Earlier test results below are scoped historical results, not a fresh whole-SDK certification.

Recorder role confirmed: `InterceptorLog` → `InterceptorInvocationTracker`. This type records invocations;
the interceptors that call it retain their own `Interceptor` suffix. Data.Tests source rename applied;
equivalent message/transition recorders renamed to `RecordedMessageTracker` / `RecordedTransitionTracker`.
Old-name source searches, scoped whitespace and three scoped builds pass; [verification](recorder-rename-verification.md).

`ErrorNatureMapper` / `IErrorNatureMapper` applied with the injected override preserved; SDK/Foundation.Tests
compiled; native escalation resolved the test socket restriction. All 28 scoped mapper/consumer/policy tests
passed. `EventFaultPolicy` / `IEventFaultPolicy` applied for Retry/DeadLetter/Ignore decisions.

Parser retained for syntax decoding; definition/indexes and SDK placement/contracts are applied.
Cron occurrence calculation uses the returned expression directly; it is removed from the parser contract.
`DelayedRetryCoordinator` → `DelayedRetryService` confirmed and source rename applied under the existing
Service role; Messaging.Tests compiled and six existing fault/bus tests passed through native approval.
[Verification](delayed-retry-service-verification.md) retains the active-delayed-scheduling coverage limit.
Remaining coordinators applied as `SecondLevelRetryService` and `SagaService<TState>`; scoped builds and
17 existing tests passed. [Verification](coordinator-service-verification.md) retains coverage limits.
`EventSagaService` / `IEventSagaService` confirmed for executing supplied steps and compensating completed
steps on failure; source rename and isolated core build passed, without direct runtime coverage.
[Verification](event-saga-service-verification.md). The existing Pipeline shape requires continuation
wrapping; this executor instead owns a forward loop and a reverse compensation stack.
`NoOpMigrationRunnerService` applied to match its existing `IMigrationRunnerService` contract mechanically;
Testing.Data build passed. No pending approvals or builds remain.
Exporter retained for structured data written as a data exchange document. Convention and indexes added;
SDK placement and exporter contracts are complete. CSV caller cancellation is preserved; the core compiled,
34 runtime scenarios were inspected and seven regression assertions passed. [Verification](exporter-conformance-verification.md).
Formatter retained for values expressed as display text under culture/format rules, including clock-relative
phrases. Its definition, indexes and SDK placement are complete; IRelativeTimeFormatter remains the accepted contract name.
`HumanizedTextFormatter` / `IHumanizedTextFormatter` confirmed for the current TextHumanizer pair. Linguistic
forms stay under Formatter; no distinct Humanizer role. Definition clarified; both formatter pairs moved to
Localization/Formatters with matching namespaces and documentation. Core build passed; no direct existing
formatter tests found. [Verification](humanized-text-formatter-verification.md).
N100 decisions, implementation and scoped verification are complete. N101 vocabulary decisions are closed;
its remaining source conformance is tracked in the active SDK handoff.
Transport retained for sending or receiving messages through a selected delivery medium, including in-process
channels. Definition and indexes added. Source conformance remains N101 work: the saga transport wrapper calls
IEventBus and guards routing, so its own role/placement must be checked against the settled boundary rather
than preserving its suffix merely because Transport is accepted.
Serializer retained for object data encoded to or decoded from a specified representation. Definition and
indexes and source placement are complete; explicit behavior/contract follow-ups remain. Per-type stored-JSON wrappers stay retired.
GoogleIdTokenVerifier follows the existing Authenticator role: evidence establishes an identity. Mechanical
rename to GoogleIdTokenAuthenticator/IGoogleIdTokenAuthenticator applied; core build passed, no direct tests.
Hash-chain checks confirmed under Validator: HashChainValidator/IHashChainValidator, Validate and
HashChainValidationResult rename applied; core build passed, no direct tests. Validator covers integrity rules; FluentValidation
remains the input/field implementation, not a requirement of every Validator. No separate Verifier role.
Bus retained for application-facing publish/send over a Transport; definition and indexes added.
Guest session behavior aligns mechanically with Service: IGuestSessionService/CookieGuestSessionService
rename applied; Identity.Tests build and one existing registration test passed. No Session role introduced.
IMessagingMetricsService/DefaultMessagingMetricsService/NoOpMessagingMetricsService applied; Messaging.Tests
compiled and four existing pump tests passed. [Verification](messaging-metrics-service-verification.md).
Metrics is a responsibility noun; the Service suffix completes the role. Clarified the existing naming rule.
Envelope naming confirmed: EventEnvelopeModel and OtpDeliveryEnvelopeModel for internal data, and
TestApiResponse<T> for the existing data-only HTTP response mirror. Payload events retain their Event suffix;
no EventModel or Envelope role. Model definition clarified; SDK renames applied. Messaging.Tests and Testing
compiled; eight existing claim-check tests passed. [Verification](envelope-role-verification.md).
All N100/N101 vocabulary decisions and final convention acceptance are complete. The remaining SDK source
conformance work is unblocked; no full SDK completion or release claim.
Original inventory below is pre-rename evidence.

## Original first concrete decision

`InterceptorLog` at `Data.Tests/Harness/InterceptorLog.cs:8` stores ordered callback names in a ConcurrentQueue, with Add, Entries snapshot, and CountOf. Recommendation: `InterceptorInvocationTracker` under the existing Tracker role. `Repository` is broader and permits persistence; `Model` cannot explain producer-updated behavior. This type is in Data.Tests, not a shipped Testing package as the row says. The two shipped logs are analogous Trackers with await support.

Technical role selection is derivable; however N100 explicitly records “per case” and discussion rather than a blanket fold. Present the concrete Tracker proposal once if honoring that historical user boundary, and do not coin a Log suffix without approval.

## Mechanical vs developer decisions

- Clear existing-role alignment: NoOpMigrationRunner -> NoOpMigrationRunnerService (implements canonical IMigrationRunnerService); test logs -> Tracker; pure ErrorNatureClassifier -> Mapper; orchestration coordinators -> Service. These require no new vocabulary, but historical N100 per-case discussion should be honored where explicitly reserved.
- Not mechanical: retaining any of the unrecognized suffixes requires the current adding-a-suffix gate and developer coining approval; accepting all shipped suffixes because they exist fails that gate.
- Existing N100 explicitly rejects a blanket Renderer merge for Exporter/Formatter/Humanizer. Do not treat newly written renderer baseline as permission to reverse that specific decision.
- N101 Parser rationale is stale: current Mapper owns explicit transform failures. Current counts and responsibilities below supersede the row counts, not the row IDs.
- Duplicate N94–N98 rows preserved; no tracker rows were edited.

## Evidence and scope

Required root instructions were in context. Read SDK CLAUDE.md; `rg --files --hidden` found no SDK AGENTS.md or `.claude/rules` Markdown files. Read root convention index, current constructs role gate, and Service/Mapper/Tracker/Renderer definitions. SDK CLAUDE.md has known historical framework/layout text and is not evidence of current package topology.

Source paths below are relative to: `/Users/max/Projects/10x-ws/workbench/career/engineering/wow-two/wow-two-ws/workbench/wow-two-sdk-beta/wow-two-sdk.backend.beta/engineering/codebase/wow-two-back-beta-sdk/src`. Declaration counts cover current public/internal top-level declarations ending with each suffix; no generated output or framework-owned declarations were counted.

## Inventory

### Log — 3 declarations

Tracker fits these live append-only test observations. InterceptorLog only appends strings, snapshots Entries, and counts; message/transition variants additionally await observations. Repository is broader and permits persistence; Model cannot own the active waiting behavior. Existing N100 requests per-case discussion: surface this concrete proposal, not a new blanket Log fold.

- `InterceptorLog` — `Data.Tests/Harness/InterceptorLog.cs:8`
- `RecordedMessageLog` — `Testing.Messaging/RecordedMessageLog.cs:16`
- `RecordedTransitionLog` — `Testing.Messaging/RecordedTransitionLog.cs:18`

### Classifier — 4 declarations

ErrorNatureClassifier maps an AppErrorType argument to ErrorNature without state: Mapper candidate. EventFaultClassifier owns a configured ordered rule set and returns Retry/Discard disposition: Policy candidate (decision about whether operation runs), Service fallback. Two responsibilities; do not coin/fold Classifier globally.

- `ErrorNatureClassifier` — `Foundation/Errors/ErrorNatureClassifier.cs:4`
- `IErrorNatureClassifier` — `Foundation/Errors/IErrorNatureClassifier.cs:4`
- `EventFaultClassifier` — `Messaging/Reliability/EventFaultClassifier.cs:10`
- `IEventFaultClassifier` — `Messaging/Reliability/IEventFaultClassifier.cs:15`

### Parser — 14 declarations

14 declarations, shared by N100 and N101 (count once). Current mapper.md permits explicit failure, so the historical premise “Mapper denies a failure mode” is stale. Cron parser additionally computes occurrences through Cronos; caption composite injects parsers and dispatches; CSV consumes an I/O stream. Pure per-format text transforms can fit Mapper; composition fits Service; library fitting may fit Adapter. Keeping a distinct Parser role requires developer decision against these actual candidates.

- `CronExpressionParser` — `Foundation/Time/CronExpressionParser.cs:8`
- `ICronExpressionParser` — `Foundation/Time/ICronExpressionParser.cs:8`
- `CompositeCaptionParser` — `Media/Captions/CompositeCaptionParser.cs:8`
- `ICaptionParser` — `Media/Captions/ICaptionParser.cs:8`
- `IJson3CaptionParser` — `Media/Captions/IJson3CaptionParser.cs:4`
- `ISrtCaptionParser` — `Media/Captions/ISrtCaptionParser.cs:4`
- `ITtmlCaptionParser` — `Media/Captions/ITtmlCaptionParser.cs:4`
- `IVttCaptionParser` — `Media/Captions/IVttCaptionParser.cs:4`
- `Json3CaptionParser` — `Media/Captions/Json3CaptionParser.cs:13`
- `SrtCaptionParser` — `Media/Captions/SrtCaptionParser.cs:13`
- `TtmlCaptionParser` — `Media/Captions/TtmlCaptionParser.cs:14`
- `VttCaptionParser` — `Media/Captions/VttCaptionParser.cs:12`
- `CsvDocumentParser` — `Media/Csv/CsvDocumentParser.cs:8`
- `ICsvParser` — `Media/Csv/ICsvParser.cs:4`

### Coordinator — 3 declarations

DelayedRetryCoordinator and SecondLevelRetryCoordinator decide and perform scheduling; SagaCoordinator correlates, loads, transitions, writes through collaborators. Existing Service covers orchestration. Policy covers decision-only work, not the scheduling/state transition whole. Names can be job-prefixed Service without coining, but N100 explicitly keeps case discussion.

- `DelayedRetryCoordinator` — `Messaging/Reliability/DelayedRetryCoordinator.cs:15`
- `SecondLevelRetryCoordinator` — `Messaging/Reliability/SecondLevelRetryCoordinator.cs:15`
- `SagaCoordinator` — `Messaging/Saga/SagaCoordinator.cs:17`

### Runner — 3 declarations

Only 3 current suffix declarations, versus historical 6. NoOpMigrationRunner implements the already-canonical IMigrationRunnerService: NoOpMigrationRunnerService is a mechanical role-alignment candidate. EventSagaRunner executes steps and compensates failures; Service covers this orchestration. Existing Pipeline is a competing narrower candidate only if its complete role shape matches.

- `EventSagaRunner` — `Messaging/EventSaga/EventSagaRunner.cs:14`
- `IEventSagaRunner` — `Messaging/EventSaga/IEventSagaRunner.cs:8`
- `NoOpMigrationRunner` — `Testing.Data/Migrations/NoOpMigrationRunner.cs:10`

### Exporter — 3 declarations

Rows -> tabular document written to caller stream. Renderer is the nearest representation role; Service could cover I/O orchestration. N100 explicitly says no merge into Renderer, so this cannot be called mechanical or silently applied. Preserving Exporter as a distinct role is developer coining work.

- `CsvTabularExporter` — `Media/Csv/CsvTabularExporter.cs:8`
- `ExcelTabularExporter` — `Media/Excel/ExcelTabularExporter.cs:7`
- `ITabularExporter` — `Media/Tabular/ITabularExporter.cs:8`

### Formatter — 2 declarations

RelativeTimeFormatter uses injected TimeProvider and Humanizer to phrase an instant relative to now. Renderer representation and Service computation are existing candidates. N100 explicitly reserves this and says no Renderer merge; keep pending.

- `IRelativeTimeFormatter` — `Localization/Humanizing/IRelativeTimeFormatter.cs:6`
- `RelativeTimeFormatter` — `Localization/Humanizing/RelativeTimeFormatter.cs:11`

### Humanizer — 2 declarations

TextHumanizer delegates plural/singular/quantity/ordinal language operations to Humanizer, with ambient CurrentCulture. Adapter (library fitting) and Service (language computation) are candidates; Renderer is another neighbor but prior N100 forbids a blanket merge. Preserving Humanizer as owned suffix needs a scoped role decision.

- `ITextHumanizer` — `Localization/Humanizing/ITextHumanizer.cs:8`
- `TextHumanizer` — `Localization/Humanizing/TextHumanizer.cs:7`

### Transport — 16 declarations

16 declarations: contracts plus 6 provider pairs and saga pair; N101 text saying five provider pairs is stale. ISendTransport accepts our EventEnvelope; IReceiveTransport supplies our ReceiveContext callback. Broker matches our vocabulary over external systems, Adapter fits library wrappers; InMemory and saga orchestrate in-process. “Transport is the wire” does not by itself defeat current Broker definition. A retained Transport role requires deliberate role-gate exception/specialization, not automatic exemption.

- `AzureServiceBusReceiveTransport` — `Messaging/AzureServiceBus/AzureServiceBusReceiveTransport.cs:27`
- `AzureServiceBusSendTransport` — `Messaging/AzureServiceBus/AzureServiceBusSendTransport.cs:23`
- `IEventSagaTransport` — `Messaging/EventSaga/IEventSagaTransport.cs:8`
- `InProcessEventSagaTransport` — `Messaging/EventSaga/InProcessEventSagaTransport.cs:18`
- `InMemoryReceiveTransport` — `Messaging/InMemory/InMemoryReceiveTransport.cs:7`
- `InMemorySendTransport` — `Messaging/InMemory/InMemorySendTransport.cs:12`
- `KafkaReceiveTransport` — `Messaging/Kafka/KafkaReceiveTransport.cs:21`
- `KafkaSendTransport` — `Messaging/Kafka/KafkaSendTransport.cs:20`
- `NatsReceiveTransport` — `Messaging/Nats/NatsReceiveTransport.cs:22`
- `NatsSendTransport` — `Messaging/Nats/NatsSendTransport.cs:21`
- `RabbitMqReceiveTransport` — `Messaging/RabbitMq/RabbitMqReceiveTransport.cs:23`
- `RabbitMqSendTransport` — `Messaging/RabbitMq/RabbitMqSendTransport.cs:23`
- `RedisStreamsReceiveTransport` — `Messaging/RedisStreams/RedisStreamsReceiveTransport.cs:23`
- `RedisStreamsSendTransport` — `Messaging/RedisStreams/RedisStreamsSendTransport.cs:21`
- `IReceiveTransport` — `Messaging/Transport/IReceiveTransport.cs:7`
- `ISendTransport` — `Messaging/Transport/ISendTransport.cs:8`

### Serializer — 6 declarations

IMessageSerializer is a selectable content-type codec returning bytes and rebuilding runtime typed objects; three codecs implement it. GeoJsonSerializer reads/writes a family of GeoJSON shapes. These are not per-type stored JSON wrappers (P08 does not delete them). Mapper is the pure transform neighbor, Adapter for library-backed implementations; Renderer is one-way and fails round-trip role. Recommendation: discuss Serializer as a distinct round-trip wire codec role; coining approval required.

- `GeoJsonSerializer` — `Geo/GeoJson/GeoJsonSerializer.cs:7`
- `IGeoJsonSerializer` — `Geo/GeoJson/IGeoJsonSerializer.cs:12`
- `CloudEventsMessageSerializer` — `Messaging/Serialization/CloudEventsMessageSerializer.cs:22`
- `IMessageSerializer` — `Messaging/Serialization/IMessageSerializer.cs:15`
- `MessagePackMessageSerializer` — `Messaging/Serialization/MessagePackMessageSerializer.cs:18`
- `SystemTextJsonMessageSerializer` — `Messaging/Serialization/SystemTextJsonMessageSerializer.cs:11`

### Verifier — 4 declarations

GoogleIdTokenVerifier returns a trusted identity from evidence: existing Authenticator is a strong candidate; its provider SDK may access signing keys. HashChainVerifier recomputes hashes and validates chain links: Hasher is narrower (digest only); Validator targets caller input validation; Service covers integrity checking. Do not assume one Verifier decision fits both.

- `HashChainVerifier` — `Foundation/Audit/HashChainVerifier.cs:9`
- `IHashChainVerifier` — `Foundation/Audit/IHashChainVerifier.cs:5`
- `GoogleIdTokenVerifier` — `Identity/OAuth/Google/GoogleIdTokenVerifier.cs:9`
- `IGoogleIdTokenVerifier` — `Identity/OAuth/Google/IGoogleIdTokenVerifier.cs:4`

### Bus — 2 declarations

IEventBus publishes/sends owned events; TransportEventBus creates envelopes, tracing, claim checks and observers before sending. Service covers orchestration, Broker a provider-independent external seam. Distinct Bus vocabulary needs coining approval; not justified solely by industry prevalence.

- `IEventBus` — `Messaging/IEventBus.cs:12`
- `TransportEventBus` — `Messaging/Transport/TransportEventBus.cs:17`

### Session — 2 declarations

IGuestSession/ CookieGuestSession EnsureGuest and Clear operate request cookies and cache the provisioned id. GuestSessionService is existing Service role, Issuer is narrower and misses clear/read behavior. Current Session is behavior, not a data model. No new suffix needed if choosing Service; N101 still reserves naming decision.

- `CookieGuestSession` — `Identity/Guest/CookieGuestSession.cs:8`
- `IGuestSession` — `Identity/Guest/IGuestSession.cs:4`

### Metrics — 3 declarations

3 declarations, not historical 2. IMessagingMetrics records counters/duration and observes in-flight probes; default owns Meter, NoOp records nothing. Service covers instrumentation behavior; Tracker only matches in-memory live status and misses metric instrument emission. Retaining Metrics as behavior needs developer role decision.

- `DefaultMessagingMetrics` — `Messaging/DefaultMessagingMetrics.cs:12`
- `IMessagingMetrics` — `Messaging/IMessagingMetrics.cs:17`
- `NoOpMessagingMetrics` — `Messaging/NoOpMessagingMetrics.cs:13`

### Envelope — 3 declarations

3 declarations, not historical 2. EventEnvelope contains owned event plus delivery metadata; OtpDeliveryEnvelope is internal delivery data; ApiEnvelope<T> mirrors the wire response data member. Model/Dto/ApiResponse candidates differ by boundary. They are data containers, not a uniform behavior suffix. Keeping Envelope as a Model/Dto specialization requires developer decision analogous to accepted Capabilities.

- `OtpDeliveryEnvelope` — `Identity/Otp/OtpDeliveryEnvelope.cs:4`
- `EventEnvelope` — `Messaging/EventEnvelope.cs:9`
- `ApiEnvelope` — `Testing/Web/ApiEnvelope.cs:13`

Total: 70 unique declarations across these suffix groups. Parser occurs in both tracker rows but is inventoried once.

## Limits

Candidate roles are evidence-based recommendations, not approved renames. No build/tests were run because the assignment is read-only. Full transport implementations were not audited for runtime correctness; naming assessment uses their owned send/receive contracts and declaration inventory.

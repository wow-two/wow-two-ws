# Backend convention repair evidence

*Last updated: 2026-09-13*

> Mechanical repair evidence for the [full audit](conventions-audit.md). The decision queue remains in that audit's `Points` section. Original audit reports preserve the pre-repair findings.

SDK source was read to verify claims; this pass edits conventions and trackers only. A convention closure is not an SDK implementation or release claim. Local sample checks are named below; the SDK build/test/pack battery has not run in this pass.

## Final convention acceptance — 2026-09-15

- All eight design points and both naming discussion rows are settled; BC03 and BC25 close the 25-task audit.
- Final wording repairs align internal Model inputs/wrappers with Event payloads, scope Service/Validator
  summaries to concrete types, and distinguish collaborating-abstraction prefixes from competing role suffixes.
- Formatter examples no longer mandate one global capability name; Transport points application publishing
  to Bus and workflow orchestration to Service. Validator references the actual Consumption heading.
- Independent acceptance reread the final edits and checked 159 backend docs plus 1,050 local links/fragments;
  no convention blocker remains in the naming scope. [Evidence](naming-final-acceptance.md).
- Workspace task con-t-003 closed. SDK tracker retains implementation obligations; no package/release claim.
- Metrics renames passed compilation and four existing pump tests. Envelope renames passed two scoped builds
  and eight existing claim-check tests; [evidence](envelope-role-verification.md).

## Metrics complete-name decision — 2026-09-15

- MetricsService confirmed; clarified that responsibility nouns precede the behavior role suffix in constructs.
  SDK interface/default/no-op renames dispatched; no new Metrics role.
- Guest session Service rename compiled and its existing configured-registration test passed.
  [Evidence](guest-session-service-verification.md).
- Envelope is the final active naming case; internal Model and HTTP ApiResponse roles are proposed.

## Bus definition — 2026-09-15

- Bus confirmed for application-facing publishing/sending over a Transport. Added its definition and both
  construct/behavior index entries, including metadata and completion-guarantee boundaries.
- Guest session behavior follows the existing Service role; mechanical rename dispatched.
- Google authenticator and hash-chain validator renames compiled; no existing direct tests found.
  [Google evidence](google-id-token-authenticator-verification.md), [chain evidence](hash-chain-validator-verification.md).
- Reports and context retain the hash-chain segment/checkpoint documentation gap and Google cancellation/options
  observations for the SDK implementation sweep. Metrics is the active naming decision.

## Validator integrity scope — 2026-09-15

- Hash-chain integrity checks confirmed under Validator. Broadened its role to supplied data checked against
  rules with validity/failure results. Domain contracts can retain structured results without inheriting
  AbstractValidator; dedicated input/field validation continues through the existing FluentValidation integration.
- Updated construct/behavior indexes and scoped the validation domain's authoring/consumption instructions.
- HashChainValidator source/result/method renames dispatched. No Verifier convention is introduced.
- Bus is the active vocabulary decision.

## Serializer definition — 2026-09-14

- Serializer confirmed for object data to/from a specified representation. Added its behavior definition
  and construct/behavior index entries; stored-JSON wrapper policy is linked to its existing owner.
- All 102 local targets across the definition and indexes exist; `git diff --check` passed.
- SDK source conformance remains in N101. Google token verification aligns with the existing Authenticator
  role; source rename dispatched. Hash-chain integrity Verifier is the active vocabulary decision.

## Transport definition — 2026-09-14

- Transport confirmed for sending or receiving messages through a selected delivery medium, including
  in-process channels. Added `core/mla/constructs/behavior/transport.md` and both construct/behavior entries.
- Defined delivery ownership, processing boundary and guarantee/lifecycle documentation requirements.
- All 99 local targets across the definition and two indexes exist; `git diff --check` passed.
- SDK conformance remains in N101, including checking the saga wrapper against the medium-ownership boundary.
- Formatter source rename/placement completed; core build passed with no direct existing runtime tests.
  [Evidence](humanized-text-formatter-verification.md). No builds or approvals pending.
- Serializer is the active vocabulary discussion; per-type stored-JSON wrappers remain retired.

## Humanized text naming — 2026-09-13

- Confirmed `HumanizedTextFormatter` / `IHumanizedTextFormatter`; Formatter owns linguistic forms as well as
  relative-time and value formatting. Added the specialization to the Formatter definition; no Humanizer role.
- SDK rename and Formatter placement/documentation conformance dispatched; verification remains pending.
- N100 vocabulary discussion closed; its SDK tracker row remains open for outstanding implementation.
- N101 Transport is the active vocabulary discussion.

## Formatter role and service verification — 2026-09-13

- Formatter definition was absent. Added `core/mla/constructs/behavior/formatter.md` for values expressed
  as display text under culture/format rules; registered it in behavior and construct indexes.
- Definition covers culture source, format/input contracts and the clock seam for relative-time phrases.
- All 98 local link targets across the definition and two indexes exist; `git diff --check` passed.
- SDK placement/documentation conformance remains in N100. Humanizer is the active vocabulary discussion.
- Coordinator/no-op renames verified: scoped builds and 17 existing tests passed;
  [evidence](coordinator-service-verification.md). Event-saga rename and isolated core compilation passed;
  [evidence](event-saga-service-verification.md) retains the lack of direct runtime coverage.
- No pending builds or approvals remain.

## Exporter role — 2026-09-13

- Exporter retained for structured data written as a data exchange document. Added
  `core/mla/constructs/behavior/exporter.md` with location, naming, responsibility and destination contracts;
  registered it in behavior and construct indexes. Existing CSV/XLSX SDK names remain.
- All 95 local link targets across the new convention and two indexes exist; `git diff --check` passed.
- SDK folder/documentation conformance remains in N100; this is a convention closure, not SDK completion.
- Formatter is the active vocabulary discussion; no Formatter or Humanizer convention change is claimed.

## Permission recovery and Parser — 2026-09-13

- Recovery procedure captured in the global `/Users/max/.codex/AGENTS.md` and read back after native-approved
  editing. No security settings or approval rules changed. New instruction chains inherit the guidance;
  existing chats may need to reread it. [Capture details](permission-recovery.md#shared-capture).
- `DelayedRetryService` confirmed/applied; Messaging.Tests compiled and six existing fault/bus tests passed
  through native approval. [Evidence](delayed-retry-service-verification.md) records scope and coverage limits.

- Native escalation resolved the two outstanding execution blocks: test-runner local socket and official NuGet
  restore. All 28 existing mapper/consumer/policy tests passed. FastCloner 3.5.6 restored and passed all 32 graph
  assertions on .NET 10.0.8 Arm64. [Permission evidence](permission-recovery.md) and [clone output](experiments/fastcloner/results.txt).
- Parser confirmed and defined for format syntax decoding; behavior and keep-list indexes updated. Failure
  carriers remain inherited; partial-input and stream contracts are explicit. [Convention verification](parser-convention-verification.md).
- C26 retains SDK clone integration; N100/N101 retain parser source conformance, including the mixed Cron
  evaluation member. Active naming decision: DelayedRetryService for the retry coordinator that performs scheduling.

## Recorder role application — 2026-09-13

Recorder verification completed: Data.Tests, Testing.Messaging and Messaging.Tests builds passed, with existing
warnings; [exact evidence](recorder-rename-verification.md). No runtime test, pack or release claim.

Error-nature mapper applied: `ErrorNatureMapper` / `IErrorNatureMapper`, with DI override retained.
[Evidence](error-nature-mapper-verification.md): SDK/Foundation.Tests compiled; runtime tests reached a sandbox
socket denial. Native retry was dismissed on session end, not approved; no executed test pass is claimed.
`EventFaultPolicy` / `IEventFaultPolicy` confirmed for Retry/DeadLetter/Ignore selection; implementation and
consumer verification are delegated. The active naming decision is Parser for syntax decoding; its definition
remains proposed pending the user's vocabulary decision.

User confirmed the recorder/interceptor distinction: `InterceptorInvocationTracker` records invocations;
an interceptor retains its own `Interceptor` suffix. Renamed the Data.Tests declaration/file and four source
reference files without changing behavior. Equivalent live recorders renamed to `RecordedMessageTracker` /
`RecordedTransitionTracker`, with their source and SDK doc references updated. No old recorder type names
remain in source; scoped whitespace checks pass. Compilation results are recorded above; no runtime test or
release result is claimed. N100 remains open for its other cases.

## Direct stored JSON usage — 2026-09-13

User clarification: no dedicated per-type options-holder class either. Custom discriminators/converters or
legacy formats require configuration only; explicit options or a registered profile key cover that need.
Removed the holder requirement from the persistence owner. Current SDK source supports explicit options in
`SystemTextJsonMessageSerializer` and EF converters; no general keyed JSON-options registry was found in the
source inventory. C29 records the shared abstraction/options-profile completion and documentation migration,
including removal of the old `{Root}JsonConstants` recommendation. This is a source gap to resolve in the SDK
sweep, not a reason to retain product wrappers. Tracker: 107 rows, 73 marked complete, 6 refuted, 28 open.

- P08 confirmed/applied: retire the per-type Json role, static exception and its construct/component docs. The persistence domain now owns stored JSON independently of HTTP. Default SDK options/converters are used directly; document-specific pinned options remain only for a format-specific need. Existing absence and malformed-document behavior must survive any wrapper migration.
- Current SDK source inspection found no per-type `*Json` class/record declarations to remove. Existing `JsonValueConverter<T>` uses the stored preset and rejects a decoded null; it is not treated as a nullable wrapper replacement. N24 retains product migration follow-up, including boundary semantics; real serializer implementations remain in their own naming cases.
- N25 closes as a convention-only row. Tracker recount across N/R/D/C IDs: 106 rows, 73 marked complete, 6 refuted, 27 open. Historical duplicate IDs are preserved. No SDK build/test/pack or release claimed.
- Link/anchor check: 153 current backend documents, 973 local targets, no missing paths or heading fragments. Whitespace checks passed in both repositories. All eight shared design decisions are applied; BC03 still contains N100/N101 and BC25 final acceptance still awaits their resolution.
- [SDK naming inventory](sdk-naming-inventory.md) records 70 current declarations and distinguishes role candidates from reserved vocabulary decisions. Active case: test recorder naming. The inventory corrects old location/count/failure-mode premises without silently deciding them.

## Test comments and acceptance sweep — 2026-09-13

- P07 confirmed: test-body AAA markers and scenario/rationale comments are optional when clarifying. Descriptive names remain required; useful setup/timing/provider explanations are preserved. Service testing owns the rule and SDK testing links it. N108 retains SDK documentation application without an unconditional comment-addition/deletion pass.
- Launched the authorized bounded acceptance sweep of settled conventions. [Acceptance evidence](conventions-acceptance.md) records link/anchor checks and two mechanical cleanup findings; all applied. External method/dedicated-validator alternatives are now explicit, and repeated tracked-write/request-companion obligations point to their application owners.
- BC20 closes; BC03's JSON/suffix decisions and BC25 final acceptance remain. P08 is the sole open point in the eight-point design pool; N100/N101 retain their separate case-by-case scope. No SDK source/build/release completion is claimed by the convention sweep.

## Shared handler work — 2026-09-13

- P06 confirmed: command/query handlers reuse shared services rather than dispatching another request. The messaging owner now states the settled restriction, the prohibition on direct-handler/proxy-dispatch workarounds, and the validation/permission/transaction obligations that extraction must preserve.
- Mediator and handler owners point to that contract; the open nested-request exception is removed. Event publication keeps its separately declared contract. C21 extends SDK source/example inventory and behavior verification; BC04 closes at the convention level.
- While reading the next queued testing owner, corrected its invalid-input HTTP example from 422 to the already-settled 400 convention. P07 test-body prose remains undecided.

## API mapping placement evidence — 2026-09-13

- P05 confirmed: an API request and its dedicated mapping extension companion stay together in the request file. API messages own the small deterministic boundary mapping contract and rationale; business logic and validation remain at the application boundary. HTTP payload complexity is not treated as a protocol limitation.
- Updated request and extension declaration owners plus MLA/LLA file rules, including folder, receiver-name and type-summary scope. The companion is `{RequestType}Extensions`; ordinary domain extensions retain their existing rules. The exception does not admit unrelated types.
- C28 records SDK inventory, examples and checks without claiming runtime changes. P05 closes BC07; the queue advances to P06 nested handler dispatch.

## Documentation inheritance evidence — 2026-09-13

- P04 confirmed: applicable per-block and declaration-kind defaults survive omitted role fields or whole Type doc/Member docs sections. Explicit restrictions override only their declared scope; a type restriction does not implicitly restrict members.
- Replaced the documentation owner's omission-as-ban rule with inherited fields and explicit overrides, including mapper-field and type-remarks examples. Retained optional/conditional tag requirements; inheritance does not require irrelevant tags.
- Replaced the params owner's stale `Declared fields only` reference and made its collaborator-only constructor summary exemption explicit. Existing explicit role restrictions remain effective, including API request type remarks.
- Swept `conventions/` for old admission wording and references; the active omission-based prohibition is gone. Historical audit evidence below remains a pre-repair snapshot. SDK application extends the existing N108 documentation pass; BC20 remains partial solely for P07 test-body documentation.

## Root closure

- Reconciled scope/shape routing, the definition/application chain, indexes and source ownership.
- Added provider-free observability contract and Serilog/OpenTelemetry application owners.
- Recovered logging research from commit `0236daf:ideas/logging-analysis.md`; rechecked selected findings against current source instead of treating historic proposals as settled rules.
- Added SDK rows `C14`–`C25`; existing options, naming, result, registry and lifetime rows remain their owners.
- SDK row count is 103: 72 historically completed, 6 refuted, 25 open. Historical `N94`–`N98` labels repeat; references require the subject.
- P01 reopened 2026-09-12: class confirmation withdrawn; entity record baseline restored; N114 awaits a new decision.
  [Record/class analysis](entity-record-analysis.md) separates concrete costs from external recommendations.
  The lane reports below preserve the earlier mechanical-pass dispositions.
- Final scan: all 154 backend documents, 163 files including affected indexes/reports/trackers, 1,028 local links;
  zero missing paths or unmatched heading fragments. Scoped whitespace checks pass in both repositories.

---

## Language and construct convention resolution

*Completed mechanical pass: 2026-09-10*

## Scope

- Allowlist only: core/lla/** except lla.md; core/mla/constructs/**.
- Existing constructs.md changes preserved as intentional baseline.
- No SDK code, staging, commit or push.
- All workspace edits used apply_patch; only /private/tmp reports/scripts were shell-written.

## Checks

- `git diff --check -- conventions/development/backend/dotnet/core/lla conventions/development/backend/dotnet/core/mla/constructs` passed.
- Local file and explicit fragment targets checked for all 74 allowed documents: 0 broken.
- Table row width check: 0 rows over 120 characters.
- Stale-rule sweep: 0 hits for IOutboxClaimStrategy, IPipelineBehavior, Result<ValidationOutcome>, C#13/.NET10 claim, init-blocks-tracker, reversed Client/Broker test, Tracker-only mutable-state ban, NamespaceCreateApiRequest.
- Current SDK declaration reads verified: Result abstract cases; IValidator ValidationError? bridge; IRequestInterceptor/LoggingInterceptor; IOutboxClaimRepository and provider; OutboxRecord body properties; EventSagaDefinition class constructor; AppDbContextBase hook flow; observing interceptor contract; existing Tracker/Renderer/Generator/Rasterizer/Spec roles.
- Documentation-only verification; no SDK runtime build/test.

- Manifest measurement: 60 changed; 74 checked; 0 link issues; 0 table-width issues.

## Per-finding closure

### L01: resolved

Client/Broker swap test corrected; unchanged house vocabulary selects Broker.

Evidence: `conventions/development/backend/dotnet/core/mla/constructs/constructs.md:237` — - must test whether a provider swap changes the surface: yes → `Client`; no → `Broker`.

---

### L02: partial: N25 decision

Consolidated static-form exceptions, removed stale IMigrationSource carveout and invalid QuietZoneConstants counterexample. Json remains an explicit current exception pending N25.

Evidence: `conventions/development/backend/dotnet/core/mla/constructs/constructs.md:324` — - may use the `Factory`, non-generic companion and `Json` forms declared below and in their role docs.

---

### L03: resolved

Result definition is the shared abstract closed union with private constructor, nested sealed cases and non-null case payloads. Per-operation carrier instruction removed.

Evidence: `conventions/development/backend/dotnet/core/mla/constructs/data/result.md:34` — - must declare an `abstract record` with a private constructor and nested `sealed record` cases.

---

### L04: resolved

Role-wide Result mandates removed; behavior roles route to components/result.md. Mapper is total over success/failure and preserves TryX/throw-return owner.

Evidence: `conventions/development/backend/dotnet/core/mla/constructs/behavior/mapper.md:62` — - failure modes, bare values and `TryX` pairs → [results](../../../conventions/development/backend/dotnet/core/mla/components/result.md).

---

### L05: resolved

Validator lookup, Infrastructure placement and invented ValidationOutcome instructions removed. Domain owns purity, placement and Validate/ValidateAndThrow bridge; existing async deferrals remain.

Evidence: `conventions/development/backend/dotnet/core/mla/constructs/behavior/validator.md:38` — - input phases, lookup boundaries and placement → [validation](../../../conventions/development/backend/dotnet/core/mla/domains/validation/validation.md).

---

### L06: resolved

Required enforcement is construction-path dependent; Activator/binder require validation. Removed claim defaults invert when moving Options to Settings.

Evidence: `conventions/development/backend/dotnet/core/mla/constructs/constructs.md:254` — - must validate required members when reflection constructs the value — the binder and `Activator` bypass `required`.

---

### L07: resolved

Removed noun-first positive ApiRequest type example rather than inventing an unverified replacement type. Verb-first normative formula remains.

Evidence: `conventions/development/backend/dotnet/core/mla/constructs/data/api-request.md:42` — - must be named `{Verb}{Noun}ApiRequest`, verb-first — it exists for one controller action.

---

### L08: resolved

Adapter example uses verified FluentValidationAdapter<T> : IValidator<T>. Pattern links declaration/naming owner instead of restating it.

Evidence: `conventions/development/backend/dotnet/core/mla/constructs/behavior/adapter.md:44` — public sealed class FluentValidationAdapter<T> : IValidator<T>

---

### L09: resolved

Controlling interceptors receive continuation; observing contracts receive hooks only. Replaced incorrect phase/job ordering sample with the canonical name formula.

Evidence: `conventions/development/backend/dotnet/core/mla/constructs/behavior/interceptor.md:54` — - must give an observing interceptor observation hooks only, without a continuation or settlement capability.

---

### L10: resolved; one subclaim refuted

Updated pipeline to IRequestInterceptor/LoggingInterceptor and outbox to IOutboxClaimRepository/PostgresSkipLockedOutboxClaimRepository. OutboxRecord example uses body initializer. EventSagaDefinition is a class with an actual constructor, so calling its constructor was NOT an N113 positional-record violation; builder sample only needed block-body formatting.

Evidence: `conventions/development/backend/dotnet/core/mla/constructs/patterns/outbox.md:25` — OutboxRecord message = new()

---

### L11: resolved

Mapper construction and registry branching positive samples use block bodies under the six gates. Builder construction sample also uses a block.

Evidence: `conventions/development/backend/dotnet/core/mla/constructs/behavior/registry.md:73` — public Type Get(CodeContentType key)

---

### L12: resolved

LLA defaults to no mutable operational state unless a role owns a lifecycle. Builder/Registry have explicit linked construction/composition allowances; Tracker baseline defines live state.

Evidence: `conventions/development/backend/dotnet/core/mla/constructs/behavior/registry.md:64` — - may mutate its binding set during composition, overriding the state-free baseline in

---

### L13: decision; local repairs landed

Mapper/Registry declare their demonstrated Params/Returns, Registry sample includes Returns, Broker explicitly declares Remarks. The global missing-section inheritance/admission policy remains unchanged.

Evidence: `conventions/development/backend/dotnet/core/lla/notation/documentation/documentation.md:57` — A component doc names the doc fields its types carry, one sub-heading each. **A field the component does not declare is

---

### L14: resolved

Remarks is optional by default with explicit consumer-contract exceptions. Computed-property evaluation differs from field initialization; itinerary sample replaced by actionable EventSaga guidance. Old heading anchor retained.

Evidence: `conventions/development/backend/dotnet/core/lla/notation/documentation/remarks.md:38` — - must not treat a field initializer as read-time evaluation; reading a stored value runs no initializer again.

---

### L15: resolved

Conventional typeparams may be omitted only when the whole parameter set is conventional. A domain-specific sibling makes the set complete.

Evidence: `conventions/development/backend/dotnet/core/lla/notation/documentation/typeparams.md:13` — - must skip `<typeparam>` when every parameter is conventional — `T`, `TKey`, `TValue`, `TResult`, `TRequest`, `TResponse`.

---

### L16: resolved audited owner set; L13 remains separate

One LLA Files owner; role leaves link MLA exception layer. Type/interface/member starters centralized, data/behavior leaves inherit defaults, field documentation and using-static/var rules point to owners. Genuine role-specific changes remain local.

Evidence: `conventions/development/backend/dotnet/core/lla/constructs/constructs.md:110` — ## Files

---

### L17: resolved audited owner set

Failure rules moved out of Type name to application owner links. Validator placement/purity lives in domain; background lifecycle/scopes in shapes. Repository definition covers data beyond database rows.

Evidence: `conventions/development/backend/dotnet/core/mla/constructs/behavior/background-service.md:71` — [host configuration](../../../conventions/development/backend/dotnet/shapes/service/platform/startup/host-configuration.md#background-work).

---

### L18: partial: existing N100/N101 decisions

Added ten already-confirmed baseline docs and indexed accepted Capabilities as a Model kind. No unconfirmed N100/N101 roles coined. Current framework Clock contracts are explicit vocabulary exceptions.

Evidence: `conventions/development/backend/dotnet/core/mla/constructs/data/capabilities.md:27` — - must treat this as a kind of `Model`; it declares supported operations rather than executing them.

---

### L19: resolved

Language catalogue declares C#14/.NET10 and adds missing partial constructor/event, compound assignment declaration, lambda modifiers, span conversion, null-conditional assignment, generic nameof and file-app directive verdicts.

Evidence: `conventions/development/backend/dotnet/core/lla/constructs/constructs.md:11` — - must apply this catalogue to C# 14 / .NET 10; language availability does not override a house ban.

---

### L20: resolved

Event ban preserved without false inherent race rationale; volatile described as acquire/release; omitted ref-readonly call modifier described as warning.

Evidence: `conventions/development/backend/dotnet/core/lla/constructs/statements.md:322` — - what it does: prefers `in` or `ref` at the call; omission warns

---

### L21: decision; inaccurate rationale removed

House record entity doctrine preserved through data baseline. Removed unverified init-blocks-tracker claim. EF identity/equality compatibility requires owner decision and targeted verification, not an automatic class rewrite.

Evidence: `conventions/development/backend/dotnet/core/mla/constructs/data/entity.md:39` — - must declare `{ get; set; }` for the mutable entity contract.

---

### L22: resolved existing policy

Composite/Flyweight/Visitor bans remain explicit house policy. Removed false derivations from suffix folds, allocation prerequisite and Result.Match. No reconsideration queued without a current contradictory rule.

Evidence: `conventions/development/backend/dotnet/core/mla/constructs/patterns/patterns.md:240` — - must preserve the house bans below; the alternatives do not establish a general language limitation.

---

### L23: resolved

Singleton/service-locator distinguish bounded per-operation scopes from retaining scoped state. Each operation disposes scope, including cancellation and failure.

Evidence: `conventions/development/backend/dotnet/core/mla/constructs/patterns/service-locator.md:34` — - must dispose that operation's scope before returning, including on cancellation and failure.

---

### L24: resolved

Owned template entries are nonvirtual; inherited framework entry/base-call obligations are explicit exceptions. Positive sample uses actual AppDbContextBase.ConfigureConventions -> ConfigureConventionsCore flow.

Evidence: `conventions/development/backend/dotnet/core/mla/constructs/patterns/template-method.md:12` — - must preserve an inherited framework entry contract when it requires an override.

---

### L25: resolved

EF save interception identified as callback instead of generated proxy and routed to EF owner. Refit remains proxy example.

Evidence: `conventions/development/backend/dotnet/core/mla/constructs/patterns/proxies.md:16` — - EF save interception → [EF mapping](../../../conventions/development/backend/dotnet/core/mla/domains/persistence/access/ef/ef-mapping.md); it is a callback, not a proxy.

---

### L26: resolved

Lazy Initialization catalogue status is owned; stale Open claim removed and existing LLA gate linked. Memento stays deferred.

Evidence: `conventions/development/backend/dotnet/core/mla/constructs/patterns/patterns.md:108` — | Lazy Initialization | `Lazy<T>` for one expensive field | `owned` |

---

### L27: resolved audited checks

Fixed nonexistent data Declaration and TimeProvider-language-table references; normalized long tables and verified local file/fragment links. Full runtime compilation of all historical illustrative snippets was not performed.

Evidence: `conventions/development/backend/dotnet/core/mla/constructs/behavior/time.md:35` — - clock contract and `TimeProvider` usage → [time](../../../conventions/development/backend/dotnet/core/mla/components/time.md).

---

## Remaining decisions

1. L13: do omitted Type doc/Member docs sections inherit lower-layer allowed fields, while an explicitly declared section restricts them, or must every role enumerate every allowed field? Existing admission rule is unchanged; local contradictory examples are repaired.
2. L21: keep mutable record entities with explicitly tested EF identity/equality safeguards, or revise the entity representation? Preserve current doctrine until decided; test navigation reference equality, mutable hash/equality, duplicate tracked instances and detached attach/update.
3. Existing N25: does Json stay a per-type static seam now stored JSON presets/registries exist? Its current exception is explicit, not silently removed.
4. Existing N100/N101: unresolved suffix classification/coining remains in its original sweep rows; accepted Capabilities baseline landed. StateMachine/Saga taxonomy remains among the existing unsupported-suffix inventory, not a new name coined by this pass.

## SDK sweep consequences

- Re-run existing sweep after convention decisions. No duplicate task IDs created.
- N69/R7/R8: shared carriers and failure-mode selection; do not restore per-operation result records or blanket role-based wrappers.
- N74/N111: required-member boot validation follows construction path.
- N108: new confirmed-role baselines supply starters and declaration rules; apply in SDK sweep.
- C8: observation-only contracts retain no continuation/settlement power.
- N113: retain OutboxRecord body-property initialization; do not classify EventSagaDefinition constructor call as a positional record.
- Interceptor names: job must remain adjacent to suffix; current ClaimCheckRehydratingConsumeInterceptor differs from this rule and belongs in the existing naming sweep.
- New role-folder defaults are role-owned; SDK placement consequences must respect its library layout overrides.

## New baseline docs

- `conventions/development/backend/dotnet/core/mla/constructs/behavior/tracker.md`
- `conventions/development/backend/dotnet/core/mla/constructs/behavior/cipher.md`
- `conventions/development/backend/dotnet/core/mla/constructs/behavior/generator.md`
- `conventions/development/backend/dotnet/core/mla/constructs/behavior/rasterizer.md`
- `conventions/development/backend/dotnet/core/mla/constructs/behavior/hasher.md`
- `conventions/development/backend/dotnet/core/mla/constructs/behavior/authenticator.md`
- `conventions/development/backend/dotnet/core/mla/constructs/behavior/issuer.md`
- `conventions/development/backend/dotnet/core/mla/constructs/behavior/renderer.md`
- `conventions/development/backend/dotnet/core/mla/constructs/data/capabilities.md`
- `conventions/development/backend/dotnet/core/mla/constructs/data/spec.md`


---

## Backend component/domain resolution

Date: 2026-09-10. Allowed component/domain convention files edited through `apply_patch`; no SDK source edits, builds, staging, commits or pushes.

## Verification

- All Markdown file targets under `core/mla/components` and `core/mla/domains` resolve after the edits (0 missing).
- `git diff --check -- conventions/development/backend/dotnet/core/mla/components conventions/development/backend/dotnet/core/mla/domains` passes.
- Current SDK signatures inspected for validated option/settings registration, Result bridges, mediator registration/interceptors, DbUp registration/provider selectors, EF registration/base context, SQL naming, migration runner/constants/CLI, JWT, and validation projection.
- Official Npgsql API confirms `MapEnum<T>(enumName, schemaName, nameTranslator)` and external-data-source driver+EF mapping requirements.
- PostgreSQL official ALTER TYPE / CREATE INDEX references support corrected transaction and recovery rules.
- No SDK compilation or runtime tests executed: SDK tree was read-only and shared dirty baseline was not built.
- New source examples are signature-checked, not claimed compilation-tested.

## Per-finding disposition

| ID | Status | Resolution / remaining scope |
|---|---|---|
| D01 | resolved | `components/options.md` implements settled N47 direct rule-free singleton / N74 validated helper / compositional PostConfigure cases; `settings.md` uses AddValidatedSettings with actual rules and domain-local binding. |
| D02 | resolved | `api-messages.md` owns verb-first dedicated requests, shared CreateUpdate shape, nested DTOs, and the existing narrowly scoped direct-body exception (complete body equals application inputs). `api.md` and mediator link it. |
| D03 | partial / decision | Same-file mapping exception is explicit `api-messages.md` Open; project layout moved to shape owner. Do we keep request + mapping class in one file, or apply the default one-type-per-file/domain extension grouping? No new exception invented. |
| D04 | partial / decision | Model payload, notification-vs-request result shape and service carrier links reconciled. Domain's existing no-subdispatch default preserved; formerly allowed mediator handler-subrequest example explicitly disputed in `messaging.md` Open. Should an application handler invoke another mediator request, or share a flow service? |
| D05 | resolved | Actionable mediator/validation names use Interceptor APIs; removed Resolver and Foundation location claims now point to current Web/ErrorMapping source. No premature ICurrentUser rename. |
| D06 | resolved | Shared failure/carrier/typed-failure/catalog/consumption/bridge policy now lives in `components/result.md`; extensions and mapper defer there. N105 TryX/Parse and Validate/ValidateAndThrow bridges retained. Totality includes explicit failure output. |
| D07 | partial / decision | Invalid init/with/deep-immutability/equality guarantees removed; current record/default-equality policy retained. `value-object.md` states two concrete decisions: constrained construction for cross-member invariants, structural collections/identity-excluded members under the no-custom-equality rule. These are representation decisions, not missing syntax. |
| D08 | resolved conventions / SDK follow-up | `postgres.md` uses named `assemblies:` and matching explicit EF `MapEnum` with same translator. Runtime round-trip and bulk EF registration completeness belong to SDK sweep; no claim current driver helper performs EF mapping. |
| D09 | resolved | Persistence/schema/EF docs select authority by migration strategy. SQL-only DDL/migration prohibitions scoped; EF-owned model retains generated migration metadata. |
| D10 | resolved | Single-column identity no longer excludes composite rows; optional domain columns can be nullable; PG list mapping removed from entity contract owner. Added tenant trait ≠ isolation rule with authority/read-write boundary obligations. |
| D11 | resolved | Dapper mapper calls pass CaseStyle explicitly. Global casing and malformed/raw Task<List<T>> examples removed. Current API sources linked; cancellable query sample uses CommandDefinition and AsList. |
| D12 | resolved | PostgreSQL ADD VALUE may be transactional; commit-before-use requirement replaces false prohibition. |
| D13 | resolved conventions / SDK verification | Concurrent index recovery checks validity and definition; IF NOT EXISTS alone is explicitly insufficient. Interrupted-build verification is the closure criterion. |
| D14 | resolved | Shared migration contract requires serialized application and verifies actual provider locking; journal idempotency is not a mutex. Missing rollback means a required explained no-op file, never omitted file. |
| D15 | resolved | Migration surface inventories/old symbols replaced with current source links and operational rules. DbUp provider-selector snippet current; CLI result mapping replaces removed drift exception. Preserved unfinished malformed-source broker throw limitation (N104). |
| D16 | resolved | New portable enum storage follows styled-text policy; existing ordinal schema explicitly remains until data migration. CHECK constraints evolve when a new value lies outside the set. |
| D17 | resolved conventions / SDK follow-up | Identity config ownership and JWT trust rules clear. Docs accurately state current helper accepts both key sources and follows URI scheme. Enforce intended single key source/HTTPS in SDK; no user permission question needed for the existing trust contract. |
| D18 | resolved conventions / SDK follow-up | Cron uses instance seam, clock registration precedence accurate, two-clock test obligation explicit. Test env var is process-global: serialize overlapping mutation/host build and restore previous value even on failed init. Scoped host-configuration alternative belongs SDK. |
| D19 | resolved contradictions / SDK/design backlog | Validation failure distinction is caller-field versus operation failure, with ValidationError recognized as AppError subtype. Provider authoring/projection moved into new `validation/fluentvalidation/fluentvalidation.md`. Phase-order gap remains explicitly unimplemented; no claim handler ordering suppresses earlier interceptor execution. Existing async/scope/read-seam/lower-pass items retained in Open for SDK design, not new approval blockers. |
| D20 | resolved targeted defects / further ownership verification | Result/mapper/value-object now match component Location/Declaration/Content form. Constants/enums/extensions type-doc obligations link constructs. EF configuration one-type-per-file applied. Dapper/EF/migration/HTTP/JWT/time instance inventories link current source. Root should run global duplication/anchor checks after all lanes settle; no claim all prose duplicates across the complete tree are gone. |

## SDK follow-ups grounded in settled rules

1. N111/N74 registration closure: validated option/settings usages and final composed values must satisfy real startup rules, not empty validation callbacks. Convention now coherent; SDK still needs its existing sweep.
2. Npgsql native enums: verify all external data-source EF consumers configure both levels; shared discovery API can serve both, but cannot claim driver-only registration is sufficient. Test EF insert/read with a multi-word enum label.
3. N104 migration broker errors: malformed source still throws before Result-returning runner recovery. Existing row remains, not a new duplicate.
4. Migration reliability: provider concurrency test, interrupted concurrent-index recovery, accurate nontransactional command behavior. Current CLI result classification must match 0/1/2 convention rather than flattening every returned failure to 1 (requires case-by-case verification of result kinds).
5. N94 current-user lifetimes: retain scoped user resolution per save, not singleton-captured identity. Tenant markers alone do not enforce isolation.
6. JWT registration: reject conflicting key-source configuration and enforce deployed-service HTTPS metadata according to the existing trust rule. An explicit local-development opt-out is a possible implementation mechanism, not implicit insecure acceptance. `JwksUri` naming/discovery semantics must be reflected accurately by SDK surface docs.
7. Clock/testing: verify deterministic paths reading both TimeProvider/IClock and isolate per-host database configuration without overlapping process-env races.
8. Validation: SDK target-resolution/phase-order seam must precede claiming generic interceptor compliance; evaluate async/caller scope/read attach semantics as complete capability work. Do not create product workarounds for missing SDK surface.
9. Outbound HTTP: current HttpResilienceOptions has no operation-replay-safety selector. Check standard retry/hedge configuration against side effects; existing transport-resilience requirement does not permit unsafe repeated effects.

## BC25 coverage disposition

- async/cancellation: language/shape lane owns general async rules; HTTP, mediator, CLI, Dapper, messaging shutdown now retain concrete propagation rules.
- resource ownership: Dapper per-independent-operation connection disposal; HTTP response/stream disposal; CLI provider plus explicitly constructed datasource disposal; framework-owned lifetime via shape owner.
- authentication/authorization: identity default-deny plus separate authentication/resource permission and authoritative caller context; JWT trust enforcement gap recorded above.
- tenant isolation: entity-contract Tenancy section requires authoritative scope and enforced read/write boundaries, explicitly denies marker-only guarantee. Full tenant-capability implementation remains SDK scope.
- messaging delivery: existing shipped Messaging.standard.md supports at-least-once, stable identity, atomic dedupe/effect, outbox, bounded retry/deadletter, cancellation and backpressure; concise application rules added to messaging.md with source link.
- outbound resilience: helper registration and budget rules retained; unsafe retry/hedging and cancellation constraints added; actual SDK support to be verified in sweep.
- observability: root-created owner added to domains built index; placeholder removed.
- recognized caching/blob stay deferred. Domain index now states concrete requirements trigger writing a contract, not an automatic feature expansion.

## Remaining decisions to surface (minimum)

1. Value-object representation combining invariant-safe copying and meaningful equality.
2. API mapping ownership: same-file exception versus conventional type/file/domain grouping.
3. Handler subdispatch: retain prohibition or allow an explicit exception.
4. Json keep-list N25 remains the existing decision owned jointly with the construct/shape lane; components/json.md is intentionally not refactored into an invented replacement.

Numeric precision exceptions are future scoped needs, not a present decision without a concrete required range. JWT broader behavior is an SDK follow-up under a settled trust contract. Existing validation capability items can be designed in SDK sweep rather than asked as permissions now.

---

## Shapes convention resolution

*Updated: 2026-09-10.*

## Scope and verification

- Only `conventions/development/backend/dotnet/shapes/**` edited.
- Existing dirty `results.md` and `serialization.md` treated as intentional baseline; current verified contracts retained while resolving contradictions.
- No SDK code, project, workflow, stage, commit or publish changes.
- 25 existing files updated; 5 shape/supporting documents added.
- All 96 local Markdown links from the shapes tree resolve; referenced local anchors checked too.
- Cross-convention links into shapes checked: no missing local target anchors.
- `git diff --check -- conventions/development/backend/dotnet/shapes` passed.
- Seven real MSBuild evaluations of the documented property condition passed. `Brand.Tests.Unit`, `.Integration`, `.E2E`, `.Migrations`, and `Sdk.Foundation.Tests` receive `IsPackable=false` and runsettings; `Brand.Api` and shipped `Sdk.Testing.Data` retain packaging defaults. Scratch projects under `/private/tmp`; no SDK solution tests run.
- Isolated net10 WebApplicationBuilder recipe compiled and ran: ambient and prefixed env keys removed, explicit alias overrides default, absent alias preserves fallback, bootstrap Development environment retained. Configuration file reload disabled only in the scratch test to avoid filesystem-watcher startup blocking; no repo host changed.
- Source-backed release inspection: `.github/workflows/publish.yml`, `src/Directory.Build.props`, main SDK `.csproj`; current workflow packs seven projects and does not run tests. No version guessed or bumped.

Paths in the table are relative to `conventions/development/backend/dotnet/shapes/`.

## Resolution table

| Finding | Status | Changes and closure |
|---|---|---|
| S01 | resolved | `service/platform/build/directory-build-props.md:28` defines a name predicate covering every product tier plus current SDK test suffix, applies non-packability after shared defaults, distinguishes WebApplicationFactory vs generic-host defaults. Seven MSBuild cases verified. |
| S02 | resolved | `service/architecture/clean/testing.md:7,19,49` separates Unit/Integration/E2E, delegates provider/reset ownership to persistence, consumes shared SDK fixtures, restricts HTTP-status naming to HTTP tests. No false absolute SQLite ban remains. |
| S03 | resolved | `testing.md:36` uses virtual `Tests/`, distinguishes physical layout and links repository folder-doc rule; no nested README requirement. Clean links solution owner instead of repeating lowercase folder name. |
| S04 | resolved | `service/platform/responses/results.md:20` scopes ExceptionMappingInterceptor to supported exceptions inside enabled result-capable pipelines; no unconditional never-throw guarantee. ProblemDetails links that owner. |
| S05 | resolved | `results.md:7` now owns AppResult handler/controller projection only. Shared failure/carrier/catalog/consumption rules moved by domains lane into components/result; notation lane owns declaration. Typed failure maps to AppError at handler boundary; no duplicated blanket role-based Result requirement here. |
| S06 | resolved convention; SDK follow-up | `serialization.md#contract` preserves existing string-only enum contract, rejects unnamed values instead of numeric ordinals, specifies `allowIntegerValues: false`. Wiring names real `AddControllersWithSdkJson()`. Missing enforcement belongs to SDK; no new policy decision. |
| S07 | resolved convention; SDK follow-up | Existing ISO-8601 TimeSpan directive preserved as `P2DT1S`; built-in `2.00:00:01` explicitly identified as insufficient. Source mismatch alone does not justify weakening a normative wire contract. Shared SDK converter/round-trip checks added as follow-up. |
| S08 | resolved convention; implementation follow-up | Host-owned typed settings and domain-vs-host-shared binding resolved. Existing alias-only policy preserved: remove ambient env sources, append present explicit aliases with precedence, preserve absent aliases' fallback. Host-bootstrap inputs separately documented. Concrete inline recipe replaces phantom helper requirement. |
| S09 | resolved | Host binding and three-group Program/partial-class obligations have one shape owner in `host-configuration.md`. Clean/platform/startup link it. Domain structuring references folder naming owners instead of duplicating their rules. |
| S10 | resolved | `architecture/architecture.md` owns arrangement selection and virtual solution organization. Clean-specific placement moved to `clean/clean.md#placement`; Api executable and Persistence implementation exceptions explicit. Domain cannot depend on service outer projects; shared domain/value contract dependencies scoped. |
| S11 | resolved | `clean/domain-structuring.md` uses consistent unprefixed concern folders and an explicit Core, permits absent counterparts, removes stale Service/Infrastructure project nesting. Example respects distinct role/project ownership. |
| S12 | resolved | `startup-defaults.md` imports actual `.Meta` namespace, documents nullable Development-only OpenAPI behavior, references option surface beside source rather than copying inventory. No contradictory direct-per-area escape hatch. SDK owns finer composition seams. |
| S13 | resolved convention; SDK follow-up | `host-configuration.md:125` replaces universal numeric slots with real dependency constraints: routing metadata, authenticated-user limiter vs IP-only limiter, provider-specific localization, identity-aware cache. New SDK composition verification required, not implemented here. |
| S14 | resolved convention; SDK follow-up | `directory-build-props.md:7` uses supported TFM default language and explicit SDK/roll-forward policy for reproducibility; package versions correctly owned by Directory.Packages.props. SDK currently still uses latest/10.0.x; applying new build convention belongs to SDK sweep. |
| S15 | resolved convention; SDK follow-up | `sdk/sdk.md` indexes new architecture/build/testing/delivery docs. Actual repo layout/registry/workflow linked; artifact set derives from live metadata. Version bump remains workflow-owned. Required verification distinguishes tested local artifacts from subsequently bumped workflow artifacts. No fabricated production-consumer constraint or version. |
| S16 | resolved | Framework/SDK inventories replaced by source/API pointers and operative constraints; host async rationale moved to `host-configuration-rationale.md`. Historical package rationale and route rename history removed; ongoing route-change obligations retained. Normalized rewritten docs without dropping callback/cookie/proxy authorization implications. |

## Remaining decisions, one at a time

1. **Test body documentation (pre-existing):** AAA markers and whether a gist beyond method name is needed. Kept at `service/architecture/clean/testing.md#open`; no invented XML-doc requirement.

Strict enums and alias-only environment configuration are already explicit normative requirements; removed the proposed policy re-votes. TimeSpan ISO duration was also a directive, so retained it and classified the missing converter as implementation debt.

Library/CLI/topology/delivery/alternative architecture shells now have explicit activation triggers and preserve existing owners. CLI links existing SDK delivery and migration-tooling, not a fabricated general CLI implementation. SDK shell was filled because this task directly needs it.

## SDK follow-up rows for root tracker

### SDK-S01 — Evaluated test packability and runner configuration

- `engineering/codebase/wow-two-back-beta-sdk/src/Directory.Build.props`: current test group sets `IsPackable=false`, then later unconditional packaging group resets it to true.
- Apply non-packability after defaults; evaluate every actual test and every intentionally shipped testing library. Cover supported product-style test naming when shared conventions are adopted.
- Verify runsettings environment at runner/host level; no assumption that every host defaults Production.

### SDK-S02 — JSON wire enforcement and ISO duration

- `Web/Json/JsonControllerBuilderExtensions.cs` and stored preset/registry converters currently allow undefined numeric enum values.
- Enforce existing string-only API contract on input/output, with known/unknown/flags cases; keep stored JSON versioning separate.
- Add a shared ISO-8601 TimeSpan duration converter and round-trip examples; built-in constant formatting is not the existing wire contract.
- Verify configured controller defaults for dictionary casing, null omission and date/time scalar behavior. Full preset method already exists; do not recreate it.

### SDK-S03 — Middleware bundle composition

- Validate identity-dependent output-cache behavior and authenticated-user partitioning against actual `UseApiDefaults` order.
- Bundle installs limiter/cache before caller-added auth, while docs now describe conditional dependencies correctly.
- Introduce a supported insertion/composition seam if required; do not work around bundle order in products.
- Verify request routing/metadata and response compression behavior with focused host tests.

### SDK-S04 — Compiler selection and release evidence

- Choose and record concrete SDK pin/roll-forward policy matching repo requirements; no version selected in this docs lane.
- Align local and CI compiler/analyzer inputs; current workflow uses `10.0.x`, props use latest language/analyzers.
- Current publishing workflow does not run test suites. Add required test evidence to the actual published revision/version path.
- Validate all seven declared pack outputs, own-family dependencies, runtime-vs-test dependency isolation, tool metadata and declared XML/symbol assets.
- Workflow increments Version/FileVersion before pack; avoid double bumping and distinguish local current version from candidate release.

### SDK-S05 — Status/source reconciliation from audit

- N60 marked closed but current `Web/ExceptionHandling/AppErrorProblemDetailsFactory.cs:10` is still static. Reconcile before claiming completion; static citation is real, not phantom.
- Existing R5/C11/N98 semantics preserved by convention changes; no reason to reintroduce blanket exception catching.

## Added documents

- `sdk/architecture/architecture.md`
- `sdk/build/build.md`
- `sdk/testing/testing.md`
- `sdk/delivery/delivery.md`
- `service/platform/startup/host-configuration-rationale.md`

### SDK/product-S06 — Explicit environment aliases

- Apply documented provider removal and explicit aliases before settings binding in host composition.
- Preserve required host boot/runtime values explicitly; removing app providers cannot retroactively alter host identity already read during CreateBuilder.
- Verify prefixed/unprefixed ambient keys do not bind, present aliases win, absent aliases preserve fallback.
- Identify a reusable SDK seam only if shared host code earns extraction; do not recreate the old phantom AddEnvironmentOverrides API without implementation.

No external messages, Git mutations or package publication performed.

## Record comparison, copying and validation — 2026-09-12

- P03 confirmed: explicit value-object equality is allowed when generated equality does not express the value, including collection contents. Matching hashing, declared order/duplicate semantics, consistent non-value exclusions and stable hash inputs are required. Value-object owners updated; C27 added for SDK inventory/implementation. P01–P03 close BC09 at the convention level; runtime work remains separate.

- Resolved P02 from the developer's explicit policy: model validation starts externally, through a pure extension method or dedicated FluentValidation-backed validator. Constructor data checks are exceptional documented contracts, since validation can grow. Programmer argument guards remain distinct.
- Updated domain validation and value-object application rules to validate candidates at the accepting boundary, including copied and deserialized candidates. Removed the pending get-only/always-valid-construction recommendation. SDK work extends C21.
- Entity rules distinguish same-key comparison, selected-field comparison, stable extracted hash keys and EF navigation reference membership. A field comparer does not make mutable hash inputs stable; a deep clone does not supply structural collection equality.
- P01 resolved: retain sealed records; mutate the original entity for tracked load-modify-save. Prototype and EF conventions prohibit submitting a replacement copy while its key is tracked, regardless of copy mechanism. N114 owns SDK verification of same-instance writes and rejection of duplicate replacements; no implicit merge is requested. Copies remain detached candidates/snapshots.
- [Deep-copy library analysis](deep-copy-analysis.md) retains comparison and isolated experiment sources/results. DeepCloner 0.10.4 passes 28 of 32 checks; cloned reference-hash and record-with-list hash-key lookups fail. FastCloner is confirmed and saved in the prototype convention; 3.5.6 package execution still awaits the original network tool request. C26 retains verification/integration; no SDK source or dependency has changed.

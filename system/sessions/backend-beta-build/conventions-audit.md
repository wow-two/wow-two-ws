# Backend conventions audit

*Last updated: 2026-09-13*

> Full-tree review of the backend conventions, with additions to the existing sweep.
> Convention decisions precede SDK changes; SDK verification precedes the new release.

## Status

- [x] Inventory the backend tree: 135 Markdown files, 11,105 lines.
- [x] Recover the existing sweep and distinguish it from stale handoffs.
- [x] Consolidate the full convention audit into 25 grouped sweep tasks.
- [x] Apply the self-resolvable convention repairs and record SDK consequences.
- [ ] Settle the remaining convention decisions and run final acceptance.
- [ ] Complete the SDK sweep in its independent repository.
- [ ] Verify and publish the new SDK version.

This audit uses the current working trees, including existing uncommitted changes. Prior claims of
332 passing tests, 978 source files, or a green build are historical, not current verification.
The SDK belongs to the developer and has no production consumers. Breaking changes are permitted;
compatibility shims are not a prerequisite for correcting its design.

The mechanical repair pass is complete. Twenty-three of the 25 grouped convention tasks are closed at the
convention level; two retain policy decisions or final acceptance. Runtime implementation and release
verification remain SDK work. The original evidence reports below preserve the pre-repair findings;
[repair evidence](conventions-resolution.md) records the changes and checks.

---

## Scope and evidence

The backend tree is entirely under `conventions/development/backend/dotnet/`. The audit covers every file:

| Area | Files | Review |
|---|---:|---|
| Root index and core scope leads | 5 | Routing, ownership, scope definitions |
| Language, notation, constructs and patterns | 64 | Definitions, contracts, examples, duplication |
| Components and domains | 39 | Application rules, technology rules, SDK references |
| Deliverable shapes | 27 | Architecture, testing, build, startup, responses, release coverage |
| Total | 135 | Full documentation read plus static reference checks |

The directory inventory and Markdown-link scan found no missing local path targets and no files beside
subfolders contrary to the folder-lead rule. Two heading links in `host-configuration.md` target
`#async-startup`, while the heading generates `#async-startup-required`.

This is documentation analysis, not a fresh SDK correctness certification. Examples have been inspected;
the entire example corpus has not been compiled. SDK symbols are checked where cited by findings, not
claimed exhaustively verified across the whole SDK. New runtime defects require implementation evidence
and focused regression tests during the SDK pass.

---

## Existing work

The active SDK tracker is [Backend convention sweep](../../../workbench/wow-two-sdk-beta/wow-two-sdk.backend.beta/be-convention-sweep.md).
Its pre-audit row markers contained **90 rows: 73 marked completed, 6 refuted, 11 open**, versus the
header's 89/10 and the older [handoff](../../../be-handoff.md)'s six-open snapshot. Source verification
reopened `N60`: `AppErrorProblemDetailsFactory.cs:10` is still static. The post-audit count was
**90 rows: 72 marked completed, 6 refuted, 12 open**. The repair pass added `C14`–`C25`, bringing the
tracker to 102 rows. Earlier P01 added N114; copying, equality and request mapping added C26–C28: the current tracker has **106 rows: 72 marked completed,
6 refuted, 28 open**. Other completion markers record prior work;
this audit does not convert them into new verification results.

| Existing row | Remaining subject | Treatment |
|---|---|---|
| `N25` | Reassess the one-type `Json` role after `N24` | Preserve the naming decision |
| `N26` | Bare static types | Preserve; remeasure against current source |
| `N94` | Current-user seam and interceptor lifetimes | Resolve lifetime safety before the rename |
| `N100` | Disputed suffixes, case by case | Preserve the explicit case-by-case decision |
| `N101` | New role vocabulary | Resolve definitions before applying names |
| `N102` | `CryptoCore` to the cipher role | Preserve; distinguish SDK work from product adoption |
| `N103` | Closed registries versus legitimate lookup misses | Classify the contract before changing failure behavior |
| `N104` | Expected failures in request and migration seams | Preserve; remeasure the remaining sites |
| `N108` | Summary starters | Fix convention conflicts before repeating the SDK pass |
| `N110` | Inline comment cleanup | Preserve caller-facing and ordering facts |
| `N111` | Options registration paths | Settle one coherent registration recipe first |
| `N60` | Replaceable ProblemDetails creation | Reopened: current source still has a static factory |

Other recovered work remains part of the sweep:

- `con-t-001`: presentation conventions; reconcile its obsolete request/response-model pointers.
- `con-t-002`: DTO versus response naming; keep product adoption separate from convention ownership.
- `car-t-008`, `car-t-011`, `car-t-014`: logging/tracing, diagnostics, and persistent startup-failure reporting.
- `car-t-009`, `car-t-010`, `car-t-012`: result/exception boundaries, nullability/fixture ownership, and
  replaceable ProblemDetails creation. Reconcile against completed SDK rows rather than repeating work.
- `car-t-013` is mentioned in the handoff as largely delivered; its current open row was not found in
  the parent task file. Preserve the reference without inventing an open task or a completion.

The parent task source is `10x-ws/system/planning/pln-tasks.md`; it was read, not edited.
The handoff's research paths for logging, exceptions and nullability are absent from the current `ideas/`
inventory. Logging research was recovered from `0236daf:ideas/logging-analysis.md`; relevant claims were
rechecked against current SDK source. The old research is not a live file or proof of current implementation.

The old component handoff is also stale: `result.md`, `value-object.md`, and `mapper.md` already exist.
Ten component leaf docs plus their lead are present. Counts against the frontend do not establish missing
backend components: the backend application register can live in `domains/`.

---

## Sweep additions

This is the convention task source linked by `con-t-003` and the SDK sweep. The 25 items consolidate
overlapping evidence; they are not 25 newly discovered SDK defects. Existing IDs below are extended,
not duplicated. Checking an audit item requires its closure evidence, not merely editing its prose.

Evidence keys: `B` refers to the baseline findings below; `D` refers to the numbered findings in
[components and domains](conventions-audit-domains.md); `L` refers to
[language and roles](conventions-audit-language.md); `S` refers to
[deliverable shapes](conventions-audit-shapes.md). Each evidence group includes source locations and closure checks.

### Ownership and contracts

- [x] `BC01` Repair routing, ownership, and the worked architecture trees. Evidence: `B01`, `L17`, `S10-S11`; scope Clean-specific placement to Clean.
- [x] `BC02` Reconcile tracker counts, completed-row evidence, and stale handoff/task pointers. Evidence: `B02`, `L27`; preserve every existing SDK row.
- [x] `BC03` Settle the role tests, static forms, and suffix vocabulary case by case. Evidence: `L1-L2`, `L18`, `D6`; extends `N25`, `N26`, `N100`, `N101`. Final definition/index acceptance: [evidence](naming-final-acceptance.md).
- [x] `BC04` Unify result carriers, payload naming, expected failures, and message dispatch rules. Evidence: `L3-L4`, `D4`, `D6`, `S04-S05`; P06 confirms shared services instead of nested command/query dispatch. Existing `N69`, `R7`, `R8`, `C11` reconciled without reinstating removed result types; SDK composition work extends C21.
- [x] `BC05` Reconcile validator purity, return types, validation phases, and deferred sequencing. Evidence: `L5`, `D19`; preserve explicit async/ruleset deferrals.
- [x] `BC06` Define one options/settings registration and required-member recipe. Evidence: `L6`, `D1`; extends `N111` and rechecks convention closure for `N47`, `N74`, `N106`.
- [x] `BC07` Reconcile API request naming, nested DTOs, model reuse, and edge-mapping placement. Evidence: `L7`, `D2-D3`; P05 confirmed a dedicated mapping companion in the request file. Extends `con-t-001`, `con-t-002` and SDK C28.
- [x] `BC08` Define intercepting versus observing contracts without restoring settlement authority. Evidence: `L9`, `L25`; preserve `C8` and the settled `Interceptor` vocabulary.
- [x] `BC09` Make entity/value-object construction and equality guarantees enforceable. Evidence: `L21`, `D7`, `D10`; P01 resolved to records with original-instance tracked writes, P02 to external validation, P03 to explicit structural equality where required. SDK consequences remain N114, C21 and C27.

### Persistence and runtime behavior

- [x] `BC10` Correct EF/PostgreSQL enum registration and scope schema rules by migration strategy. Evidence: `D8-D10`; verify both driver and EF mapping with the current signatures.
- [x] `BC11` Correct SQL enum transactions, interrupted index recovery, and SQLite enum evolution. Evidence: `D12-D13`, `D16`; include failure/retry cases in the resulting SDK work.
- [x] `BC12` Specify migration coordination and rollback guarantees per provider. Evidence: `D14`; separate sequential idempotency from concurrent execution safety.
- [x] `BC13` Repair stale SDK references and executable examples after settled renames. Evidence: `L8`, `L10-L11`, `D5`, `D11`, `D15`, `D18`; extend the convention closure of completed rename rows.
- [x] `BC14` Reconcile test tiers, naming, build-property selection, and test documentation layout. Evidence: `S01-S03`; validate matching `.Tests.{Type}` project names and each tier's database policy.
- [x] `BC15` Specify deterministic clocks and isolated multi-host test configuration. Evidence: `D18`; preserve the currently real `IClock` divergence until its implementation is fixed.
- [x] `BC16` Align the JSON contract with installed converters and serializer options. Evidence: `S06-S07`; verify enum numeric inputs, dictionary keys, null omission, and duration representation.
- [x] `BC17` Align startup/defaults and middleware prescriptions with actual host behavior. Evidence: `S08`, `S12-S13`; repair the two async-startup anchors and verify option defaults without broadening opt-ins.
- [x] `BC18` Align JWT configuration and key/metadata guarantees with implementation. Evidence: `D17`; distinguish a missing safeguard from a deliberately configurable policy.
- [x] `BC19` Scope mutable state and DI lifetime rules for builders, registries, and background work. Evidence: `L12`, `L23`; extends `N94` and `N103` without converting legitimate misses into wiring faults.

### Language, documentation, and completion

- [x] `BC20` Reconcile XML documentation obligations and remove duplicate rule ownership. Evidence: `L13-L16`, `D20`, `S09`, `S16`; P04 confirms inherited fields with explicit overrides, P07 confirms optional clarifying test-body comments. Caller-facing facts and test XML exemptions retained.
- [x] `BC21` Correct the C#/.NET catalogue and its language facts. Evidence: `L19-L20`; distinguish deliberately unsupported features from missing catalogue verdicts.
- [x] `BC22` Reconcile pattern verdicts and examples with their actual applicability. Evidence: `L22`, `L24-L26`; keep justified house policy explicit instead of presenting it as a language limitation.
- [x] `BC23` Close observability, diagnostics, and persistent startup-failure conventions. Evidence: `B03`; carries `car-t-008`, `car-t-011`, `car-t-014`, with no duplicate task IDs.
- [x] `BC24` Complete the SDK architecture/testing/delivery and reproducible-build rules. Evidence: `B03`, `S14-S15`; preserve developer-owned beta compatibility policy.
- [x] `BC25` Record capability coverage dispositions and perform the final convention acceptance pass. Evidence: `B03`; named deferral triggers and SDK consequences retained. Final acceptance: 159 docs, 1,050 local links/fragments pass; [evidence](naming-final-acceptance.md).

`BC03` vocabulary decisions and final convention consistency verification are complete.
The convention's coining gate requires a confirmed role before implementation. `BC09` is closed:
records, original-instance tracked writes, external validation and explicit value-object equality are settled. Mechanical
repairs elsewhere do not need renewed permission. `BC20` is closed: documentation inherits applicable defaults
with explicit scoped overrides, and test-body comments are optional when clarifying. `BC22` preserves house pattern bans unless their owner revises them.

---

## Repair resolution — 2026-09-10

A checked `BC` item means its convention repair is complete, with source consequences linked to the SDK
tracker. It does not certify runtime behavior. A partial item retains the completed repair plus a concrete
unanswered choice. [Detailed repair evidence](conventions-resolution.md) maps every original finding.

| Task | Disposition | Closure or remainder |
|---|---|---|
| BC01 | closed | Scope/shape routing, documentation chain and worked architecture trees use their actual owners. |
| BC02 | closed | Counts derive from markers; duplicated historical IDs are qualified by subject; handoffs and planning pointers distinguish history from current work. |
| BC03 | closed | Role tests/static exceptions repaired; all N100/N101 vocabulary decisions settled and definitions/indexes verified. Per-type Json retired; SDK source conformance remains separate. |
| BC04 | closed | Shared carriers, typed failures, bare-value cases and boundary bridges reconciled. P06 confirms shared services for handler reuse; no nested command/query dispatch. C21 retains SDK composition checks. |
| BC05 | closed | Validator contract/purity and field-vs-operation failures reconciled; provider owner added. Existing phase-order/design debt stays explicit in C21. |
| BC06 | closed | Direct rule-free options, validated options/settings and composed PostConfigure cases agree; N111 owns SDK application. |
| BC07 | closed | Body naming, DTO sub-blocks, direct-binding conditions and edge mapping agree. P05 confirmed request-file mapping companions with scoped file/folder/naming overrides; C28 retains SDK application. |
| BC08 | closed | Observing contracts have neither continuation nor settlement power; controlling contracts retain continuation. |
| BC09 | closed | P01–P03 resolved: sealed records, original-instance tracked writes, external validation and explicit structural equality when needed. N114/C21/C27 retain SDK work. |
| BC10 | closed | Driver and EF enum mapping signatures corrected; schema authority scoped by migration strategy. C19 owns runtime evidence. |
| BC11 | closed | PostgreSQL enum commit boundary, concurrent-index validity recovery and SQLite constraint evolution corrected. C19 owns runtime evidence. |
| BC12 | closed | Journals distinguished from execution locks; rollback limits explicit per provider. C19 owns coordination/retry checks. |
| BC13 | closed | Audited removed APIs replaced with current symbols/source owners; illustrative snippets are not claimed exhaustively compiled. |
| BC14 | closed | Tier, file and build-selection rules reconciled; seven MSBuild selector cases pass. P07 now permits optional clarifying test-body comments. |
| BC15 | closed | Two-clock determinism and process-global configuration hazards explicit. C18 owns isolated SDK host fixtures. |
| BC16 | closed | Full JSON preset named; strict string-enum and ISO-duration requirements preserved. C14 owns missing conversion and round-trip evidence. |
| BC17 | closed | Startup/default values, async anchors, alias-only recipe and middleware dependency constraints corrected. Config recipe compiled and exercised; C15 owns bundle ordering. |
| BC18 | closed | JWT trust obligations distinguished from current helper enforcement. C20 owns source corrections. |
| BC19 | closed | Role-owned mutable lifecycle and per-operation scope exceptions explicit. N94 (current user) and N103 retain source work. |
| BC20 | closed | Documentation owners/defaults/examples repaired. P04 inherits applicable defaults with explicit scoped overrides; P07 uses optional clarifying test-body comments. |
| BC21 | closed | C# 14/.NET 10 feature catalogue and language facts corrected; house restrictions remain explicit. |
| BC22 | closed | Pattern applicability/examples corrected; intentional bans retained as house policy without false technical proofs. |
| BC23 | closed | Observability, Serilog and OpenTelemetry owners written; existing logging/startup tasks map to C22/C23. |
| BC24 | closed | SDK architecture/build/testing/delivery defined; actual release metadata remains repository-owned. C16/C17 own implementation and evidence. |
| BC25 | closed | Capability coverage and named deferral triggers recorded; final acceptance covers 159 backend docs and 1,050 local links/fragments. Settled source consequences retained in the SDK sweep. |

### Verification boundary

- Checked all 154 backend documents plus affected indexes/reports/trackers: 163 files, 1,028 local Markdown
  links, zero missing targets and zero unmatched heading fragments. Inline authoring examples are excluded.
- Whitespace checks pass for the changed backend convention tree and owned tracker/report files.
- Seven actual MSBuild evaluations cover product test tiers, SDK test suffixes and shipped testing libraries.
- The alias-only environment recipe compiles and runs in an isolated .NET 10 host: prefixed/unprefixed
  unexpected inputs disappear, explicit aliases win, absent aliases preserve fallback, bootstrap identity survives.
- Representative SDK APIs were inspected against current declarations. SQL/EF/JWT and other runtime closure
  belongs to the SDK rows; no SDK solution build, test run, pack or publication occurred here.
- Capability coverage includes cancellation, disposal, authorization, tenant scope, messaging delivery and
  outbound replay safety. Caching/blob, alternative architectures and other shells have activation triggers;
  they are not silently added to this conformance release.

---

## Points

All eight design decisions in this convention-repair pool are resolved; P01–P03 on 2026-09-12, P04–P08 on 2026-09-13. Check an item only
after its answer is applied and verified. Existing suffix cases in N100/N101 retain their own source
inventory and are handled case by case after the shared design rules; they are not silently closed or
collapsed into a blanket rename.

- [x] **P01 — Entity representation (BC09).** Resolved 2026-09-12: retain sealed records and their comparison/copy benefits. For load-modify-save, apply validated changes to the single tracked entity and save; prohibit replacing it with `Update(entity with { ... })`, a deep clone or a manually copied class while that key is tracked. No implicit merge/detach/clear workaround. Copies remain useful for detached candidates/snapshots; any detached-update contract is explicit. Applied in EF tracked-write and prototype conventions; N114 owns SDK verification. [Concrete analysis](entity-record-analysis.md) retains ten BCL checks and twenty EF/SQLite checks. External recommendations are inputs, not a deciding authority.
- [x] **P02 — Value-object construction (BC09).** Resolved 2026-09-12: start with external validation through an extension method or dedicated validator (currently FluentValidation), since rules can grow. Constructor data checks are exceptional and documented. Record/init candidates, including copies and deserialized values, are checked at their accepting boundary; no always-valid-construction or get-only default. Domain validation and value-object application rules updated; SDK integration extends C21.
- [x] **P03 — Value-object equality (BC09).** Confirmed 2026-09-12: permit explicit equality when generated record equality does not express the value, including list content comparison. Require matching hashing, documented order/duplicate semantics, and consistent exclusion only of non-value members. Generated equality remains the default when suitable. Applied in value-object conventions; C27 owns SDK inventory and verification.
- [x] **P04 — XML field admission (BC20).** Confirmed 2026-09-13: omitted fields/sections inherit applicable general and declaration-kind defaults; explicit role restrictions override only their stated scope. A summary-only role does not ban method params/returns, while an explicit type-remarks ban remains effective. Updated the documentation owner, preserved the collaborator-only constructor exemption explicitly, swept convention references/examples. SDK documentation sweep extends N108; P07 remains separate.
- [x] **P05 — API mapping files (BC07).** Confirmed 2026-09-13: keep the request and its dedicated `{RequestType}Extensions` mapping companion in `{RequestType}.cs`. Mapping stays a simple deterministic boundary projection; application logic/validation stay outside. Updated API messages, request/extension declarations and file-placement owners with scoped exceptions. Saved the rationale as house policy, not a claim that HTTP payloads cannot be complex. C28 retains SDK application.
- [x] **P06 — Nested handler dispatch (BC04).** Confirmed 2026-09-13: reuse shared services instead of sending another command/query from a request handler. Do not invoke another handler directly or hide nested dispatch in a service. Preserve the shared operation's validation/permission obligations and explicit transaction ownership. Updated messaging, mediator and handler owners; removed the open exception. Event publication retains its own contract. SDK source/example verification extends C21.
- [x] **P07 — Test body documentation (BC20).** Confirmed 2026-09-13: AAA markers and scenario/rationale comments are optional when they clarify the body. Descriptive test names remain required; no mandatory second gist or narration. Preserve useful explanations, without blanket deletion of optional markers. Service testing owns the rule; SDK testing links it. Test XML exemptions remain separate. SDK documentation pass extends N108.
- [x] **P08 — Per-type Json seam (BC03 / N25).** Confirmed 2026-09-13: use SDK stored-JSON options/converters directly; retain pinned document-specific options only when the format needs customization. Retired the Json role, static exception and component/construct docs. Persistence owns the stored contract independently of HTTP. Preserve accepting-boundary absence/error behavior during wrapper removal. No per-type Json wrapper declaration found in current SDK source; real serializer/converter roles remain separate. N25 closes as a convention change; N24 retains product migration follow-up.

Explicitly deferred validation features and unadopted capability shells remain at their documented triggers.
They are neither erased nor presented as immediate permission questions. N100/N101 vocabulary cases still
require the existing developer coining decision before their individual renames.

## Naming points

P08 clarification (2026-09-13): remove the dedicated per-type options-holder requirement as well. Custom
formats justify configuration, passed to the shared serializer or selected by a registered key, not a wrapper
or holder type. C29 owns verification/completion of that shared SDK capability; the current source inspection
does not prove a general keyed JSON-options registry exists. N25 remains a convention closure.

The existing SDK naming rows remain the decision pool; this does not add sweep tasks. Current source
inventory: [SDK naming inventory](sdk-naming-inventory.md). Individual cases within each row are discussed
before closing the row. No blanket suffix fold is implied by an existing-role candidate.

- [x] **N100 — Disputed suffix decisions settled; SDK implementation remains.** Recorder role confirmed: `InterceptorInvocationTracker` owns ordered
  callback observations, while interceptors retain their own `Interceptor` suffix. The analogous live message
  and transition recorders are renamed to `RecordedMessageTracker` / `RecordedTransitionTracker` under the same
  existing Tracker role. Source checks and Data.Tests / Testing.Messaging / Messaging.Tests builds pass.
  `ErrorNatureClassifier` → `ErrorNatureMapper` and `IErrorNatureMapper` applied, retaining the DI override;
  scoped mapper/consumer tests pass following native permission recovery. Event-fault naming applied:
  `EventFaultPolicy` / `IEventFaultPolicy` decide Retry, DeadLetter or Ignore; the pipeline performs the action.
  existing policy tests pass. Parser retained for syntax decoding; construct and indexes applied, with scope
  checks for mixed-responsibility SDK types remaining implementation work. `DelayedRetryCoordinator` →
  `DelayedRetryService` applied; Messaging.Tests compiled and six existing fault/bus tests passed.
  `SecondLevelRetryService` and `SagaService<TState>` applied; scoped builds and 17 existing tests passed.
  `EventSagaService` / `IEventSagaService` applied; isolated core build passed, no direct runtime coverage.
  `NoOpMigrationRunnerService` applied with Testing.Data build passing. No pending approval or build.
  Exporter retained for structured-data exchange documents; convention and indexes
  added. SDK Exporter placement/documentation conformance remains. Formatter retained for values to display text
  under culture/format rules; definition and indexes added. SDK Formatter placement/documentation remain.
  `HumanizedTextFormatter` / `IHumanizedTextFormatter` confirmed under Formatter, with no separate Humanizer
  role. Convention clarified; SDK rename/placement applied and core build passed (no existing direct tests).
  This checkbox closes the vocabulary discussion only;
  the SDK sweep row remains open until placement, documentation and remaining conformance work are verified.
- [x] **N101 — Vocabulary decisions settled; SDK implementation remains.** Parser is defined for syntax decoding;
  its duplicate N100 case is resolved by the same decision. No open vocabulary question remains.
  Parser failure carriers remain governed by the existing result rules.
  Transport retained for message delivery over a selected medium; definition and indexes added. SDK conformance
  remains, including the saga wrapper that delegates delivery to IEventBus. Serializer retained for object
  data to/from a specified representation; definition/indexes added, per-type stored-JSON wrappers stay retired.
  GoogleIdTokenAuthenticator and HashChainValidator applied; core builds passed, no existing direct tests.
  Validator definition broadened beyond input/FV contracts; no separate Verifier role.
  Bus retained for application-facing publish/send over a Transport; definition/indexes added.
  Guest session Service rename applied; Identity.Tests compiled and one existing registration test passed.
  MetricsService applied; Messaging.Tests compiled and four existing pump tests passed. Responsibility noun +
  role suffix clarified in constructs. EventEnvelopeModel/OtpDeliveryEnvelopeModel confirmed internally and
  TestApiResponse<T> for the data-only HTTP test mirror; renames compiled and eight claim-check tests passed.
  Events retain Event, not EventModel. Final convention acceptance passed; SDK source conformance remains.

---

## Baseline findings

### B01 — Repair the routing vocabulary and indexes

The physical `core/` plus `shapes/` recut is implemented, but several descriptions still describe the old tree:

- `conventions/conventions.md:159-166` sends role declarations to `mla/components/` and architecture/build
  to nonexistent `mla/architecture/` and `mla/platform/` locations.
- `core/core.md:20` excludes host/project placement from core, but `:48-55` still defines five buckets
  including architecture and platform, and names Application/Infrastructure placement.
- `core/mla/mla.md:9-17` presents architecture/platform as its buckets while linking into `shapes/`.
- `conventions/conventions.md:106` reserves “layer” for `lla`/`mla`/`hla`; `development-conventions.md:24-41`
  and `dotnet-conventions.md:33-48` use it for baseline/definition/application as well.

Consequence: the next convention can be filed in the wrong owner even when every Markdown path resolves.
Use the existing physical recut and the root's scope/register distinction as the repair baseline.
Closure: every routing example resolves to the same owner; shape placement rules remain in shapes;
scope and register no longer share the word “layer.” No new directory taxonomy is required.

### B02 — Reconcile status and handoff evidence

Before the audit corrections, `be-convention-sweep.md:11` and `be-handoff.md:24` reported different stale counts. The tracker also
says `N26` was deleted at `:16` even though its open row exists at `:71`, and retains product-lane counts
after moving product rows away. Workspace task pointers still name old convention files.

Consequence: continuing from a handoff can repeat completed work or skip a live row.
Closure: derive counts from row markers; keep the current audit linked from both entry points; reconcile
stale narrative and planning pointers without deleting another lane's work or renumbering old tasks.

Applied during this audit: corrected the SDK count, reopened `N60` against source, added the convention
prerequisite link to the SDK sweep, and registered `con-t-003` in the workspace board. Historical narrative
and the remaining completed-row evidence still need the `BC02` pass.

### B03 — Turn missing coverage into explicit scope decisions

`domains/domains.md:37-43` recognizes caching, blob storage and observability without rule owners yet.
Observability is already a raised task; it must not be added as a second independent task. SDK, library,
CLI, topology, delivery and alternative-architecture pages explicitly declare themselves shells.

Consequence: a shell is visible scope debt, not an implemented convention and not automatic permission
to select the alternative. Completing this audit does not mean implementing every SDK capability.

Closure for this sweep:

- Complete the SDK's architecture/testing/delivery rules needed to verify and release this SDK.
- Close the already-raised observability and startup-failure decisions.
- Inventory async/cancellation, resource ownership, authentication/authorization, tenant isolation,
  messaging delivery, and outbound resilience at their existing owners; add concrete missing rules,
  rather than a second generic checklist.
- Keep other shells deferred with a named adoption trigger; re-open one when this SDK work needs it.
- Keep deliberately planned capabilities, such as caching, outside this convention-conformance release
  unless the developer explicitly expands its feature scope.

---

## Execution order

1. Reconcile the convention owners and the existing task evidence.
2. Resolve incompatible rules and the outstanding role decisions.
3. Repair examples, SDK symbol references, and missing convention coverage.
4. Re-run the convention consistency checks and review each closure condition.
5. Resume the existing SDK rows; add source-level consequences of newly settled rules.
6. Run the sweep battery, focused regression tests, solution build/tests and package checks against
   the final SDK working tree. Record the exact commands and results.
7. Inspect the repository's actual versioning/publishing workflow, select its next valid version,
   publish the authorized release, and verify the published package. Do not infer a version from
   the conflicting .NET 9/.NET 10 and `0.0.y`/`10.0.x-beta` historical descriptions.

The SDK pass remains in `workbench/wow-two-sdk-beta/wow-two-sdk.backend.beta`, an independent Git repository.
No consumer migration is a gate for this developer-owned SDK correction.

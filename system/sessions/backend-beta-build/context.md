# backend-beta-build context

*Last updated: 2026-09-19*

## Current state

- SDK changes are drained into signed batches with the user-enabled turn-only commit switch.
  The follow-up sweep fixed inbox gate retirement, release tags, remaining helper roles and the Release child probe.
  All eleven signatures verify; SDK HEAD is `b01f6b6` and its working tree is clean. Final Release checks pass 455 tests
  with one existing skip; all seven package/symbol pairs verify against that revision. Commit permission is OFF again.
  [Batch verification](commit-batches-verification.md).
- Backend conventions are complete: all 25 BC01–BC25 tasks and all design/naming decisions are closed.
  [Final acceptance](naming-final-acceptance.md) verifies 159 docs and 1,050 local links/fragments.
- The SDK implementation sweep and local release verification are complete. [Remaining work](../../../workbench/wow-two-sdk-beta/wow-two-sdk.backend.beta/be-convention-sweep.md)
  carries the developer-owned publish and release-dependent consumer adoption.
- Completed session naming/placement slices were checked against live source and removed from active obligations.
  [SDK recheck](sdk-handoff-recheck.md) distinguishes source evidence from historical test results.
- Tracker role placement is complete; Data.Tests and Messaging.Tests builds pass, with 13 existing messaging/saga
  harness tests passed. [Verification](tracker-placement-verification.md).
- N91 CloudEvents decoding is complete: full-document validation and malformed-input failure results;
  all 37 serializer tests passed, including 15 regressions. [Verification](cloudevents-decoder-verification.md).
- Parser conformance is complete: 14 declarations relocated, parsing contracts documented, Cron evaluation
  delegated to the parsed expression. Compilation and 17 existing VTT cases passed. [Verification](parser-conformance-verification.md).
- Exporter contracts and CSV cancellation are complete, closing N100. The core compiled; 34 scenarios were
  inspected and seven cancellation assertions passed. [Verification](exporter-conformance-verification.md).
- Transport conformance is complete: 12 provider implementations moved under `Transports/`; the saga delivery
  wrapper became `EventSagaPublisherService`. The SDK build passed and Messaging.Tests passed 111 with 1 skipped.
  [Verification](n101-conformance-verification.md).
- N101 is complete: GeoJSON preserves ID kind and rejects permissive wrong shapes; Google authentication observes
  caller cancellation within the provider API's non-cancelable certificate-refresh limit.
- N60 is complete: ProblemDetails creation is a replaceable factory seam consumed by all SDK exception paths;
  the SDK build passed and all 39 Web.Tests passed. [Verification](n60-problem-details-factory-verification.md).
- N104 is complete: request timeouts and migration-source failures use `Result` contracts; Messaging.Tests passed
  111 with 1 skipped and all 17 Migrations.Tests passed. [Verification](n104-result-contract-verification.md).
- C21 is complete: mediator validation aggregates all SDK validator failures, preserves authored rule codes and
  documents target-free versus target-bearing phase placement. Foundation.Tests passed 115 and Mediator.Tests
  passed 68. [Verification](c21-validation-conformance-verification.md).
- C14 is complete: the HTTP preset rejects numeric and undefined enum values, writes ISO 8601 durations and
  preserves casing/null/scalar behavior. Web.Tests passed 44. [Verification](c14-http-serialization-verification.md).
- C29 is complete: stored JSON supports direct options or immutable keyed profiles with explicit unknown-key
  failure; Foundation.Tests passed 119. [Verification](c29-stored-json-profiles-verification.md).
- N114 is complete: generic and identity repositories preserve tracked-instance updates, reject replacement
  copies and retain explicit detached full-state writes. Data tests passed 3 and Identity.Tests passed 7.
  [Verification](n114-tracked-write-verification.md).
- C26 is complete: FastCloner 3.5.6 is pinned and exported for explicit deep copies of owned detached graphs;
  Foundation.Tests passed 123. [Verification](c26-fastcloner-integration-verification.md).
- N103 is complete: local event-type and explicit serializer registration gaps fail loudly; inbound unknown type
  tokens and runtime membership/correlation predicates retain their non-throwing paths. Messaging.Tests passed
  113 with 1 skipped. [Verification](n103-registry-failure-verification.md).
- N102 is complete: `ICryptoCore` / `CryptoCore` became `IValueCipher` / `ValueCipher`; Foundation.Tests passed
  123. SecretsVault changes remain in the post-release consumer pass. [Verification](n102-value-cipher-verification.md).
- N94 is complete: one singleton `ICurrentUserService` resolves the ambient principal per access for controllers,
  audit and soft-delete. Identity.Tests passed 8 and Data.Tests passed 23.
  [Verification](n94-current-user-service-verification.md).
- C28 is complete by inventory: the SDK has no HTTP `*ApiRequest` declarations or request-to-command/query mappings;
  no unused mapping surface was added. [Verification](c28-api-request-mapping-verification.md).
- C27 is complete by inventory: the SDK declares no `*ValueObject`; collection-bearing records are DTOs, options
  or operational state, so no custom equality or hashing was added. [Verification](c27-value-object-equality-verification.md).
- N26 is complete by current-source inventory: all 247 static classes use a permitted role suffix, apart from the
  allowed non-generic `SagaTestHarness` companion. [Verification](n26-static-class-conformance-verification.md).
- N110 is complete: every authored production inline comment is one line; generated assembly metadata is the only
  multi-line run left. The main SDK project builds. [Verification](n110-inline-comment-verification.md).
- N108 is complete: public roles, interfaces and fixed-value fields use their required summary starters. Hash-chain
  version docs now match the genesis-only validator API. [Verification](n108-summary-conformance-verification.md).
- N111 is complete: SDK-owned code options use direct singleton values or startup-validated pipelines; only the
  five topology composers retain raw `AddOptions<T>`. The delayed-retry registration no longer mutates the service
  collection during resolution. [Verification](n111-options-registration-verification.md).
- N115 is complete: all 14 projects pass the live vulnerability audit, the solution builds and 399 tests pass.
  NuGet advisories are warning-as-error again. [Verification](n115-dependency-remediation-verification.md).
- C15 is complete: `UseApiDefaults` supplies an explicit identity middleware callback after routing and before
  limiter/cache policies. A real host passed all 47 Web tests. [Verification](c15-api-defaults-pipeline-verification.md).
- C16 is complete: all seven test projects evaluate non-packable, the seven release projects stay packable and
  local/CI use SDK `10.0.300` with `latestPatch`. [Verification](c16-build-packaging-verification.md).
- C17 is complete: CI tests one release commit and verifies seven package/symbol pairs before publish; local release
  tests passed 402 with one skipped. [Verification](c17-release-pipeline-verification.md).
- C18 is complete: both time abstractions share one test clock, multi-host configuration is host-local and each
  relational fixture owns its provider. [Verification](c18-test-host-isolation-verification.md).
- C19 is complete: PostgreSQL owns whole-loop locking, SQLite requires one deployment applicant, no-transaction
  recovery runs statements sequentially and all 26 migration tests pass. [Verification](c19-migration-guarantees-verification.md).
- C20 is complete: JWT bearer validation requires one key source, HTTPS metadata and a compatible pinned algorithm;
  issuance enforces HMAC key lengths. All 20 Identity tests pass. [Verification](c20-jwt-trust-verification.md).
- C22 is complete: module telemetry is collected, queued traces correlate, metric tags stay bounded and failures are
  recorded once without exporter faults replacing results. [Verification](c22-observability-contract-verification.md).
- C23 is complete: a pre-host durable logger captures creation and validation failures, flushes and rethrows; child
  processes prove persisted output and nonzero exits. [Verification](c23-startup-failure-reporting-verification.md).
- C24 is complete: unsafe HTTP methods run once unless an idempotency selector permits replay; cancellation, total
  budgets, streaming rejection and response disposal pass nine focused tests. [Verification](c24-http-replay-safety-verification.md).
- C25 is complete: EF and generated Dapper CRUD enforce ambient tenant scope; messaging retains at-least-once delivery,
  atomic same-context inbox effects, bounded queues/retries and failed-outbox evidence. Data passed 27, Web passed 63,
  and Messaging passed 122 with one intentional Kafka skip. [Verification](c25-tenant-messaging-guarantees-verification.md).
- Release readiness is verified locally: the Release solution built with zero errors, 453 tests passed with one
  intentional Kafka skip, and all seven package/symbol pairs passed the package verifier at `10.0.55-beta`.
  One local pack required native network escalation despite `--no-restore`. [Verification](release-readiness-verification.md).
- Current order in the active handoff: drain SDK commit batches, sweep again, verify/publish, migrate ForeverPin,
  then analyze missing SDK vectors. Other consumer repins remain recorded without preceding ForeverPin.
- SDK repository: `workbench/wow-two-sdk-beta/wow-two-sdk.backend.beta/`, an independent Git repository.
  Code root: `engineering/codebase/wow-two-back-beta-sdk/src/`. C17 owns stale onboarding/version/structure claims;
  use evaluated project/workflow state for release work.

## Confirmed constraints

- WoW2 owns its conventions; external philosophies are inputs, not authority.
- Sealed record entities remain. Tracked writes edit the original instance; no implicit replacement-copy merge.
- External validation is the default; constructor data checks need exceptional type-specific justification.
- Collection value equality/hashing follows the value contract; generated equality is retained when correct.
- Request mapping stays in the request file. Shared services replace nested request-handler dispatch for reuse.
- Stored JSON uses shared SDK serialization with options or registered profiles; no per-type wrappers/holders.
- FastCloner 3.5.6 is approved, integrated and covered by standalone and SDK graph-copy tests.
- The SDK has no production consumers; breaking changes are approved. The developer publishes.
  Ordinary agent commits default OFF; explicit user consent enables the repository-scoped switch for one turn.
  See [commit permission](../../../.codex/commit-permission.md).
- Run shared-output builds serially. For authorized commands blocked by sandbox sockets/network, use native
  escalation and retain execution until its actual result. [Permission recovery](permission-recovery.md).

## Evidence and history

- [Naming decisions and report index](sdk-naming-inventory.md).
- [Retained-role verification](retained-role-conformance-verification.md): Exporter/Serializer/Bus placement;
  scoped build and 26 existing serializer/pump tests passed. Separate behavior gaps remain tracked.
- [Convention audit](conventions-audit.md) and [resolution evidence](conventions-resolution.md).
- [Record/EF analysis](entity-record-analysis.md) and [deep-copy analysis](deep-copy-analysis.md).
- [Earlier context snapshot](context-history.md) preserves the old build journal, architecture snapshots and
  completed naming handoff. It is historical evidence, not the current task queue.

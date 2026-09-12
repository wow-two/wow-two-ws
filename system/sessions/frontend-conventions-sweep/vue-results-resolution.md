# Vue results and HTTP resolution

*Last updated: 2026-09-10*

## Completed scope

Vue source paths below are relative to `workbench/wow-two-sdk-beta/wow-two-sdk-beta.ui/engineering/codebase/wow-two-front-vue-beta-sdk/`.

- **Row 12:** added `foundation/results` with the exact readonly `Result<TSuccess, TFailure>` carrier, transport-independent `AppError`, closed `AppErrorType`, safe `AppErrorFactory`, and `ResultExtensions`. Classifier-based synchronous/asynchronous third-party adapters preserve unclassified programmer errors. Native validation returns the shared carrier with `ValidationFailure.issues`; `Validator<TOutput,TInput>` preserves editable input separately through transforms, defaults and all composites; Standard Schema retains its required `{ value } | { issues }` protocol. Custom validator checks/transforms no longer silently relabel programmer exceptions as bad user input.
- **Row 13:** semantic live controls renamed: `UseWorkerControls`, `UseUploadQueueControls`, `MountWithQueryControls`, `RunWithQueryControls`. The scalar snapshot inside the computed query batch became `AppQueryState` (it has no refs or commands). The credential exchange payload became `BearerCredentials`, and the routing decision became `GuardDecision`; neither is a controls bag or a completed failure result. These are breaking public type changes; source imports/exports were migrated.
- **Row 14:** HTTP methods return `Result<unknown, ApiFailure>` by default. A typed payload requires an explicit `ApiDecoder<T>`; a void response requires `response: 'empty'`. Distinct transport, cancellation, timeout, protocol, validation and HTTP failure cases preserve safe messages and separate status/header/problem diagnostics. Strict envelope validation, content type/JSON checks and empty-body handling prevent unchecked casts. Transport retry is opt-in and limited to GET/HEAD/OPTIONS; mutation retry is never inferred. Programmer bugs in the token or decoder delegate still throw.
- **Row 36:** removed `reviveTemporal`, `parseJson<T>` and global `temporalReviver`. JSON stays `unknown`; date-looking identifiers and wide-number strings stay strings. Caller decoders own fields and exact backend encodings. No decimal/int64/TimeSpan encoding was invented.
- **Query:** endpoint/query/mutation/prefetch callbacks return Result. Private `resolveQueryResult` unwraps only at TanStack's rejection boundary; expected outcomes are restored for `mutateAsync` and lazy `fetch`. Safe `ApiFailure` state reaches house callers; cancellation does not retry or trigger the global error callback. Programmer errors are not classified as network errors or retried. Suspense intentionally propagates rejection into Vue's error boundary protocol. `prefetchProps` now requires an explicit client, removing the shared module client that mixed independent roots.
- **Auth/row 40:** strategies and `AuthApi` operations return Result. Cookie strategies require user decoding; 401 resolves an anonymous success. Provider generations cover resolve/sign-in/sign-out, strategy replacement and disposal; invalidation aborts superseded operations. Bearer credentials have independent generations, clear immediately on logout, and ignore stale completions. Bridge listeners finish fan-out and guard waiter resolution before reporting callback exceptions as an AggregateError. Mandatory logout state updates survive strategy cleanup errors. Redirects accept application-local paths by default; a named custom URL builder explicitly owns an alternative trust policy. Token storage documents the isolated-memory default.

## Verified evidence

`npx vitest run --project unit --project dom tests/unit/auth tests/unit/foundation/http tests/unit/foundation/results tests/unit/foundation/validation tests/unit/query tests/unit/providers` — **8 files, 44 tests passed**. The checks cover expected failure identity, invalid envelope/JSON/content type, empty responses, explicit decoding, safe diagnostic separation, cancellation/timeout, no mutation retries, preservation of programmer exceptions, Standard Schema protocol, stale auth operations/token writes, bridge callback failures, redirect inputs, provider replacement/disposal and provider mounts.

`npx vue-tsc --noEmit` — no diagnostics after the Result/query/auth migration and new tests (concurrent parent browser work later changes the overall tree). `npx prettier --write` applied to the owned changes. The final release gate remains parent-owned.

No source callers remain for the removed Result-suffix names or temporal reviver. This is a reference check, not proof that all semantics across the SDK were audited. Parent owns remaining browser operation carriers and presentation migration; another agent owns both forms adapters and their parsed-output/snapshot/autosave regressions.

## Explicit application identity cleanup

Auth intentionally does not import optional query, analytics or draft-storage peers. A consuming app owns its session/tenant key and composes the existing bridge at bootstrap. For example, subscribe to `bridge.subscribeSession`, compare the previous authenticated identity key with the new key, then:

1. Call `queryClient.cancelQueries` with a predicate matching the old identity's protected keys. Remove those same queries immediately with `removeQueries`; cancellation also prevents late responses from restoring removed identity state.
2. Delete only drafts keyed to that old identity/tenant through the app's draft store.
3. Reset the analytics adapter's identity through its app-selected provider API.
4. Unsubscribe when that app root is destroyed.

These actions must be idempotent, and each cleanup should run even if another adapter fails. Report aggregated cleanup errors through the app's diagnostics channel. Apps define protected keys and identity equality explicitly; the SDK cannot infer which anonymous/shared caches or drafts should survive logout.

## Remaining boundaries

No unresolved choice is required for this implementation. Actual endpoint decimal/int64/enum/duration encodings remain backend-specific decoder contracts, not a global SDK migration. Existing optimistic mutation is retained: the settled React hook preference against `useOptimistic` is not a blanket Vue library prohibition. Overlapping optimistic transactions now serialize per QueryClient through cancellation, snapshot/patch, request, rollback and invalidation. This deliberately trades same-client mutation concurrency for deterministic rollback; separate clients remain parallel. Pure target patch functions are required.

## Rows 22/26 — utility placement and folder casing

The utility bucket migration completed after a coordinated imports-only checkpoint with all three active owners. The initial inventory contained **31 leaf modules / 62 files**, including **26 PascalCase folders**. All were assigned to concrete capabilities:

| Capability | Former utility modules |
|---|---|
| `foundation/styles` | cn, tv, CssExtensions, ColorExtensions, SurfaceStyles, Layers, StyleTokens, Tones, Severity, Orientation, Align, Side, CornerPosition, OverlayPosition, ProgressTone, StatusTone |
| `foundation/dom` | ElementTag, AriaAttribute, AttributeValue, DomEvent, HtmlExtensions, KeyboardExtensions, PressExtensions, composeEventHandlers, dataAttr, polymorphic |
| `foundation/optionals` | OptionalExtensions |
| `foundation/animation` | TransitionExtensions |
| `foundation/collections` | Equality |
| `foundation/i18n` | Compare |
| `foundation/config` | Environment |

The migration rewrote named imports by exported symbol, splitting mixed imports where needed; 463 files were written (including moves and barrels). AriaAttribute content and concurrent component/form/browser edits were preserved. The old `foundation/utils` source bucket and export were retired; parent owns the package/root export manifest. Utility tests were split into their actual capability folders. A runtime self-import discovered in Animate was fixed to import the transitionExtensions leaf; a full foundation same-capability import scan found no other generated self-import. The original PascalCase utility folders were removed. This closes the utility-placement portion of rows 22/26; row 22 also includes the parent-owned `forms-engine` → `formsEngine` source/adapters correction. This is not a claim of whole-foundation role-layout or behavior coverage.

## Additional behavior closure

- Optimistic query tests cover overlap, rollback after a later target patch throws, queue recovery, independent clients, explicit prefetch clients, reactive query keys/page changes and lazy reset. Scope disposal now invalidates lazy local writes.
- Persistence now requires `includes(queryKey)`, enforced both when writing and before restoring; mutation state is excluded. Future/nonfinite timestamps are discarded. It remains JSON persistence; applications allowlist JSON payload caches and derive rich values after reading them.
- `feedbackQueryErrors` accepts the shared AppError shape and displays only its catalog message; raw server title/detail never becomes notice text. Cancellation produces no notice.
- The shared controlled helper fixes ownership at setup, seeds defaults once, suppresses identical setter emissions and exposes `reset()` through the same ownership path. Native input DOM reset integration is owned by presentation components.
- Analytics flush waits for already-dispatched asynchronous deliveries before invoking vendor flush methods. Flags isolate targeting-array snapshots, notify computed evaluations after the current async refresh, route imperative reads through the live provider client, and isolate provider-free clients between roots.
- Added `foundation/dom/UrlExtensions.ts` after the utility split. `safeNavigation` allows web/mail/tel/relative destinations; `safeResource` allows web/blob/relative destinations. Both validate normalized protocol and reject controls or executable/data schemes, including scheme-relevant HTML entity obfuscation. These helpers select URLs; they do not sanitize arbitrary HTML.

## Final owned-lane checkpoint

`npx vitest run --project unit --project dom tests/unit/auth tests/unit/query tests/unit/providers tests/unit/feedback tests/unit/analytics tests/unit/flags tests/unit/foundation/http tests/unit/foundation/results tests/unit/foundation/validation tests/unit/foundation/state tests/unit/foundation/styles tests/unit/foundation/dom tests/unit/foundation/collections tests/unit/foundation/i18n tests/unit/foundation/animation` — **22 files / 105 tests passed**. The form agent separately confirmed native string-to-number object schema integration in both form adapters.

Source and test `vue-tsc --noEmit -p tsconfig.typecheck.json` found no owned-lane errors; its concurrent snapshot had three presentation test undefined-value diagnostics, handed to the component owner. Owned-lane ESLint has no errors; the final two long-comment warnings were shortened. `git diff --check` passed for the owned scope. Parent still owns aggregate release gates and publishing.


## Final role-layout correction and speech startup

The final owner check uses [Library / Capability roles](../../../conventions/development/frontend/shapes/library/library.md#capability-roles), rather than folder casing alone. The split now removes all **32** one-leaf wrappers (the original 31 plus UrlExtensions), with **24** actual import/barrel files adjusted:

| Capability | Role placement |
|---|---|
| `styles` | `enums/` has 9 closed-set files; `extensions/` has CssExtensions and ColorExtensions; `constants/` has Layers and Tones; Cn, Tv and the SurfaceStyles factory stay flat. |
| `dom` | `enums/` has 6 closed-set files, including HtmlValues and Key (renamed from misleading extension filenames). Polymorphic is the singleton model; PressExtensions is the singleton fixed-value object; UrlExtensions is the singleton extension object; ComposeEventHandlers and DataAttr are flat seams. |
| `animation`, `collections`, `i18n`, `config`, `optionals` | TransitionExtensions, Equality, Compare, Environment and OptionalExtensions are flat singleton members. |

Every new role folder has at least two files. Supporting exported types stay with their primary object; public capability export names are unchanged. Direct internal references resolve to the concrete leaf, avoiding self-barrel runtime cycles. Existing other foundation hooks/primitives/adapters have separate component/role owners; a mechanical count of 32 folders with one non-barrel TS/Vue source includes valid root capabilities and visual primitives and is not a violation count or a claim that those roles were semantically audited.

Speech recognition startup now returns `Result<void, RecognizerStartFailure>`. Unsupported engines and construction/start failures are failed outcomes; an existing starting/listening session is idempotent success and does not invoke native start again. The `SpeechRecognizer` runtime handle and `SpeechRecognitionControls` reactive bag retain their names. Five new unit/DOM tests cover unsupported engines, construction failures, native startup failure/retry, idempotency/end/restart, and composable forwarding.

`pnpm exec vitest run --project unit --project dom tests/unit/foundation/styles tests/unit/foundation/dom tests/unit/foundation/collections tests/unit/foundation/i18n tests/unit/foundation/config tests/unit/foundation/speech` — **10 files / 30 tests passed** after role moves. Scoped ESLint and Prettier passed for all moved files and actual import edits. Parent owns subsequent whole-package build/consumer/release gates.


## Remaining-capability closure

The follow-up [capability layout and operation carrier audit](vue-capability-layout-audit.md) records the semantic retirement of `foundation/hooks`, role groups beyond the former utility bucket, own-file Result extraction, final operation alias/failure-code names, and reproducible capability-cycle gates. That document supersedes historical source-path and alias names earlier in this implementation log. Parent tracks whole-layout acceptance separately in sweep row 43.

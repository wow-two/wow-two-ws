# Vue behavior audit

*Last updated: 2026-09-10*

## Scope and state

Vue package paths below are relative to `workbench/wow-two-sdk-beta/wow-two-sdk-beta.ui/engineering/codebase/wow-two-front-vue-beta-sdk/`. Source is being modified concurrently by the Result migration lane; evidence records the inspected implementation, not transient import failures. Rows refer to `engineering/planning/ui-sdk-conventions-sweep.md`. Forms implementation is now assigned to this lane; other findings are handoffs. No full-vector completion claim is made from smoke coverage.

## Row 38 — form behavior

1. **P1 — parsed output is discarded.** `src/forms-engine/SchemaValidation.ts:42,94` reduces schema success to an empty error map; `AppForm.ts:27,31,53` exposes one input/output type. House submits raw current values (`house/HouseFormCore.ts:336,347`); TanStack submits the raw vendor value (`tanstack/UseAppForm.ts:285,293`). Add separate input/output generics, preserve successful schema output, and never cast invalid editing input into output. Standard Schema's successful `value` is explicitly the output: [official specification](https://standardschema.dev/).
2. **P1 — asynchronous validation and submission use different snapshots.** House validates a captured values object then reads `peek().values` again after awaiting. Editing while validation waits can therefore send an unvalidated value. Capture one immutable input snapshot, submit its corresponding parsed output, and keep later editing values intact.
3. **P1 — autosave drops the latest edit.** Both single-flight guards return the current promise (`HouseFormCore.ts:369–377`; `tanstack/UseAppForm.ts:404–413`) when an autosave timer fires during a pending request. No trailing queue exists. Queue/coalesce the latest dirty snapshot; after the active request settles, save that snapshot once. Failure must not create an automatic retry loop.
4. **P2 — reset/disposal and stale errors need generation guards.** House resets only its validation epoch (`:299`) and dispose clears only its timer (`:412`); submission completion still changes the new form's verdict/errors. Both adapters map server errors against current path existence instead of submitted field value equality. Bare reset reads original defaults after a loaded baseline, and successful saves never advance that baseline. Implement lifecycle generations, current-baseline reset and successful submitted-baseline advancement as part of the submission coordinator.
5. **P2 — wizard subset validation is absent.** `AppForm.ts:validate` and both implementations validate the entire schema; the comments suggest using this directly as a wizard step gate. Existing API can use a separate current-step schema supplied reactively, but final-submit schema must be explicit. A built-in step schema/subset API remains a bounded capability extension; do not claim existing tests prove it.

Existing test evidence: `tests/unit/forms-engine/forms-engine.test.ts` has 13 smoke tests (path manipulation, house dirty/reset/arrays/server mapping, both adapters exporting a function). It does not exercise TanStack behavior, transforms, async races, autosave, step validation or cancellation. New shared behavior regression tests and implementation results are recorded below when completed.

## Row 40 — auth and trust boundaries

1. **P1 — provider identity generations do not cover sign-in/out.** `src/auth/AuthProvider.vue:149–168`: sign-in increments the generation only after awaiting and always authenticates; sign-out increments before awaiting but always writes anonymous in `finally`. A stale sign-in can resurrect a signed-out session; an older sign-out can erase a newer sign-in. Capture generation at operation start, invalidate competing resolves, and commit only while generation/strategy/owner still match. Unmount and strategy replacement must invalidate old work. `runResolve` already guards generation (`:88–114`), so extend that existing mechanism.
2. **P1 — fixing provider state alone does not fix bearer credentials.** `src/auth/BearerStrategy.ts:56–85`: a late `resolveUser` returning null clears whichever token is current; late sign-in always stores its token; sign-out clears only after its remote delegate completes. Add a strategy-local generation/token comparison; clear the local credential immediately on logout and suppress stale writes. Deferred tests must verify provider session and storage together.
3. **P2 — callback failures interrupt mandatory auth bookkeeping.** `AuthBridge.ts:62–69` invokes session subscribers before resolving guard waiters; one throwing callback strands the waiters. Unauthorized listener failure stops later listeners (`:51–52`). `AuthProvider.vue:138–142` calls strategy cleanup before clearing session, so a thrown cleanup prevents logout. Mandatory state/waiter cleanup must complete regardless of consumer callback failure; define an explicit error reporting callback instead of swallowing unexplained failures. Existing unsubscribe/bridge replacement cleanup works.
4. **P2 — redirect policy needs a concrete local-return contract.** `RedirectStrategy.ts:57,78` forwards arbitrary caller return URLs to the challenge endpoint. Default return URL is pathname plus query, and default challenge endpoint is same-origin; this is not proof of an exploitable open redirect because backend validation may reject it. Default to application-local paths and test absolute/protocol-relative/control-character inputs; allow external redirects only through a named explicit policy. Preserve backend enforcement.
5. **P2 — identity cleanup composition is undocumented/incomplete.** `AuthBridge` exposes session subscriptions, query exposes cache removal, and token storage defaults to an isolated memory store. Those are usable opt-in seams. No auth-owned cache/analytics cleanup composition is present. Add an explicit app wiring example/adapter that cancels protected requests, removes identity-scoped cache/drafts and resets analytics identity; do not automatically connect auth to every optional module. `TokenStorage.ts:1` still advertises localStorage for credentials and should match the settled memory-default security rule.

Existing tests: `tests/unit/auth/auth.test.ts` covers 9 memory-store/bridge happy paths. `tests/unit/providers/ProvidersCases.ts:23` disables resolution for the AuthProvider DOM/SSR smoke case. It proves mount/slot/server render only; there are no sign-in/out, strategy, redirect, callback-failure or token-race tests in the reviewed Vue test tree.

## Row 39 — locale, time and lifecycle

1. **P2 — implicit browser locale can mismatch server rendering.** `src/foundation/i18n/LocaleContext.ts:58–60` chooses `navigator.language` when available and otherwise `en-US`. Server markup can therefore format differently from initial browser render when the caller omits locale. Seed the same explicit locale on both sides or use a deterministic fallback and opt into browser detection after hydration. Vue documents environment-dependent server/client output as a [hydration mismatch source](https://vuejs.org/guide/scaling-up/ssr.html#hydration-mismatch).
2. **Existing support to retain:** `LocaleProvider.vue:29–32` passes reactive getters; context messages resolve from the current getter; `useLocaleFormatters` computes from current locale (`LocaleFormatters.ts:61–63`); provider-free `useLocale` has deterministic en-US fallback (`LocaleContext.ts:68–77`); plural formatting already exists (`LocaleFormatters.ts:49`). These are implemented, not missing roadmap items.
3. **Bounded missing tests:** explicit locale/message replacement, provider-free fallback, two independent roots, unmount/remount and matching SSR/client initial rendering. `ProvidersCases.ts` does not include LocaleProvider. Date/time formatting accepts caller Intl options including timeZone; absence of a provider timeZone property alone is not a defect. App root `lang`/`dir` and timezone selection stay app-owned. Temporal-native formatter expansion is separate from correcting implicit hydration behavior.

## Row 36 — wire codecs

1. **P1 — heuristic revival is not typed decoding.** `src/foundation/http/temporalReviver.ts:17–53` transforms every matching string regardless of field schema, then `parseJson<T>` casts the result. A date-looking identifier changes type; invalid date text remains a string even when the caller claims Temporal. `CreateApiClient.ts:64–67,215` enables this only through opt-in `reviveTemporal` (default false), so ordinary client reads already retain wire strings. Replace that client option with an explicit decoder and keep raw JSON as unknown until decoded. HTTP owner is implementing this during Result migration.
2. **Existing codec boundaries:** the reviver handles Instant, PlainDate, fractional PlainTime and ISO Duration; it does not decode CLR constant TimeSpan or PlainDateTime. Do not silently add another global regex. Backend TimeSpan contract and explicit field decoder must agree. Wide numbers require endpoint evidence/declared encoding, not an invented global switch to string.
3. **Test correction:** `tests/unit/foundation/http/http.test.ts:12–40` deliberately asserts heuristic revival and raw-string fallback on invalid dates. These tests currently preserve the old behavior, so passing them does not satisfy row 36. Replace with typed boundary tests: date-looking ordinary string unchanged, valid typed field decoded, malformed field produces failure, exact duration fixtures, absence/null distinctions and declared enum handling.

## Genuine choices and mechanical resolutions

- Mechanical: schema output preservation, validated snapshots, queued latest autosave, stale completion guards, deterministic initial locale, auth/token operation generations and exception-safe mandatory cleanup.
- Explicit app policy: allowed external return destinations, session/tenant cache keys, root language/direction and display timezone. Defaults can be secure/local/deterministic; consumers supply named policies where needed.
- Backend-coordinated: precise decimal/int64 transport representation and legacy TimeSpan migration. Use current contract fixtures and record the selected representation beside the codec.
- Capability extension: built-in wizard subset API and Temporal-native formatter overloads. Existing reactive schema/options seams provide narrower support, but require concrete documented usage and tests.

## Forms implementation verification

Implemented in both adapters: separate editing/output generics, parsed-output submission, captured validation snapshots, coalesced trailing autosave, current saved baseline/reset, stale completion/validation suppression, typed expected submit failures, safe unexpected-failure messages and disposal cancellation of queued work. Removed `submitInvalid`; invalid input cannot be passed as transformed output. Added adjacent `AppForm.spec.md`.

The form consumes `Result<unknown, AppError>` from `onSubmit`; `handleSubmit` deliberately remains a boolean UI verdict. Native validators consume the new shared Result while the external Standard Schema protocol remains unchanged. TanStack's facade owns snapshot submission sequencing and shares its parser result with the native schema validation pass.

Forms verification: **43 tests passed** (13 existing smoke tests and 30 new cases across both mounted adapters). Covers native and third-party transforms, invalid input, asynchronous editing, duplicate submit, trailing latest autosave, saved/loaded baseline, reset during parsing and submission, stale invalid validation, expected failure without retry, replacement submission after reset, and teardown of queued saves. The combined forms/datetime command passed **80/80** tests. Final current-tree `vue-tsc --noEmit -p tsconfig.typecheck.json` is clean; `check-sfc` compiles all **407 SFCs**. Owned lint and diff checks are clean. Full browser/package/release gates remain parent-owned.

The remaining step/subset, cancellation/session and manual error-focus scope was subsequently implemented; see the final row-38 amendment below. The former no-abort limitation is superseded.

Native-validator handoff completed: `Validator<TOutput>` previously declared both Standard Schema input and output as `TOutput`, so a string-to-number transform claimed numeric input. The validator owner added independent `TInput` propagation. Both mounted-form adapters now have a passing `object({ amount: string().transform(Number) })` regression with statically distinct input/output types.

## Row 33 — focus and dismissable primitives

Implemented in `src/foundation/primitives/focusScope/**` and `dismissableLayer/**`:

- Explicit `modal` prop owns background inertness separately from `trapped`/`loop`; default nonmodal leaves background available. Presentation owner wires modal callers.
- Logical Vue ancestry preserves nested portal ownership. Only the top trap recovers focus, and document keyboard routing covers a portalled nonmodal descendant's final Tab stop.
- Per-owner-document registries preserve prior inert attributes, observe late DOM branches, restore touched values and release listeners/observers on last teardown.
- Ancestors register before already-mounted logical children; closing an ancestor removes its whole scope subtree before child cleanup can restore focus into closing content.
- Restoration checks connected targets and the remaining trap, retains outside focus for a nonmodal close, and supports iframe owner documents. Focus moves preserve scroll.
- Focus candidates exclude negative tab indices, hidden/inert subtrees, hidden inputs and disabled fieldsets. Cancelable autofocus hooks remain available.
- Dismissable layers preserve logical nesting across Teleport and handle each Escape/pointer event once, including synchronous callback teardown. Disabled top layers do not activate lower layers.

Added adjacent specs and `tests/unit/foundation/primitives/FocusScope.browser.test.ts`: 11 real-browser cases, run by normal Chromium and forced-colors configurations (22 expected executions). Browser execution is **pending parent verification**: sandbox refused loopback listen with `EPERM ::1:63315`; the elevated attempt was dismissed because a newer permission request superseded it. No browser pass is claimed here. Existing primitive DOM/SSR smoke: **50/50 passed**. Owned lint/typecheck/diff checks are clean.

Platform basis: native [inert semantics](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Global_attributes/inert) remove background interaction and accessibility-tree reachability; modal focus/return behavior follows the [WAI dialog pattern](https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/). Browser tests remain required because DOM emulation cannot prove keyboard or inert behavior.

## Row 36 — explicit temporal codecs implemented

Added `src/foundation/datetime/TemporalCodecs.ts`, its adjacent spec, and tests/fixture evidence under `tests/unit/foundation/datetime/`. Public `TemporalCodecs` names five distinct field encodings: Instant, PlainDate, PlainTime, ISO duration and CLR constant TimeSpan. Decode/encode return the shared Result; no HTTP dependency, global reviver or ordinary-string mutation exists. Nullability/omission remain containing-schema responsibilities.

CLR conversion uses exact BigInt ticks internally, preserves ±1 tick and both signed TimeSpan extrema, rejects overflow/sub-tick precision, rejects calendar years/months and treats weeks/days as fixed elapsed units. ISO calendar durations remain a separate named codec. Four-digit ISO date/time fields preserve subsecond precision and reject malformed or unrepresentable canonical values. Endpoint-specific year ranges remain explicit refinements.

Observed evidence: isolated .NET SDK **10.0.300**, target `net10.0`, default System.Text.Json emitted all seven TimeSpan round-trip fixtures plus DateOnly/TimeOnly/DateTimeOffset fields. The complete producer and actual output are saved in `TemporalFixtures.md`. Read-only backend evidence is `src/Foundation/Serialization/JsonOptionsConstants.cs` in the backend beta SDK: its preset configures NodaTime and does not register a CLR TimeSpan converter. This is source plus framework-runtime evidence; no backend service or complete configured backend serializer was executed.

`pnpm exec vitest run --project unit --project dom tests/unit/foundation/datetime tests/unit/forms-engine`: **80/80 passed** (37 datetime, 43 forms). Tests reject immediate TimeSpan overflow neighbors, invalid dates/clocks, missing offsets, unexpected null/undefined, cross-encoding durations and precision loss. Wide decimal/int64 encoding remains outside this amendment.

## Final forms review — detached snapshots

Resolved the independent review finding that shallow references were not immutable snapshots. Supported writes are fields, `setValue`, arrays and reset; `values` is documented as a read view, and direct nested mutation bypasses notifications. Added `FormSnapshot.ts`: plain objects, arrays and Date detach at ingress and before validation/submission. The validator receives a separate copy from the saved-baseline snapshot. File/Blob, Temporal and custom immutable class leaves retain identity and prototypes; mutable custom class internals require an editing model or whole-leaf replacement. No JSON/structuredClone conversion is used.

Corrected `deepEqual` to honor its documented identity fallback for opaque classes, preventing different Temporal values with no enumerable properties from comparing equal. New mounted regressions mutate caller-held defaults, nested form values and Date while an async schema waits; both adapters still submit the original snapshot, preserve opaque types, keep newer edits dirty and restore the confirmed baseline. Synchronous/asynchronous schema exceptions also release validating/submitting state and the in-flight latch, with a successful retry afterward. The established form contract maps unexpected schema exceptions to a safe validation fallback rather than rethrowing them.

Latest forms run: **47/47 passed**. Owned ESLint, TypeScript and diff checks are clean. Source is held after this bounded amendment; browser verification and aggregate release gates remain parent-owned.


## Final row-38 amendment — step validation, cancellation and manual focus

Closed all three remaining concrete row-38 capabilities in the relocated `src/formsEngine/**` tree; public package subpaths remain `forms-engine`, `forms-engine/house`, `forms-engine/tanstack`. No SDK package/config or other capability sources were edited by this lane.

Migration-relevant public signatures (`src/formsEngine/AppForm.ts:27–38,56,72,274–278`):

```ts
interface AppFormSubmitContext { readonly signal: AbortSignal }
interface AppFormValidationOptions<TValues extends object> {
  readonly fields?: ReadonlyArray<string>;
  readonly schema?: StandardSchemaV1<TValues, unknown>;
}
onSubmit(values: TOutput, context: AppFormSubmitContext): Promise<Result<unknown>>;
focusRoot?: () => ParentNode | null | undefined;
form.validate(options?: AppFormValidationOptions<TValues>): Promise<boolean>;
form.cancelSubmit(): void;
form.invalidateSession(next?: TValues): void;
```

Existing one-argument submit callbacks remain assignable; mocks asserting exact callback arity must include the context. Forward `signal` to transport/mutation calls. Cancellation is recorded as the existing shared `AppErrorType.Cancelled`, never as a second error carrier.

- Step gates validate a detached input snapshot using the configured schema or an explicit step schema; selected paths include descendants, and root/cross-field issues always block. They update selected client errors and touched state while preserving other errors. `state.isValid` describes currently known errors, not final validation of every step. Final submission always parses the configured whole schema; step output is never submitted. House implementation: `adapters/house/HouseFormCore.ts:443`; TanStack: `adapters/tanstack/UseAppForm.ts:489`; shared segment matching/parsing: `FormOperations.ts:12–45`.
- `cancelSubmit` aborts the request signal, clears queued autosave, releases active flags/latches, retains dirty editing values/baseline and resolves the verdict false. Reset, disposal and `invalidateSession(next)` also abort and suppress obsolete validation/submission/focus, but session/reset operations clear the cancellation banner. A delegate ignoring abort cannot hold the UI indefinitely or later change the baseline. This does not promise server rollback. `invalidateSession` takes an explicit new-session model; without it, reset restores the saved baseline, so logout wiring must supply the app's empty model. No auth-to-forms runtime dependency was introduced. Implementations: house `HouseFormCore.ts:373,420,501`; TanStack `UseAppForm.ts:362,441,470,614`; shared abort race: `FormOperations.ts:48`.
- Manual submission captures the event current target synchronously, waits for Vue's next DOM update, focuses the first enabled invalid field and otherwise a focusable `[data-form-error-summary]`. Imperative submits use `focusRoot`. Hidden/inert/disabled controls are skipped. Reset/cancel/dispose invalidate obsolete focus; validation and autosave never focus. Summary content and one coordinated live announcement remain the view's responsibility. Shared implementation: `FormOperations.ts:68`; both adapters call it only from `handleSubmit`.

Evidence: `tests/unit/formsEngine/Submission.dom.test.ts:411` adds ten mounted conformance cases (five per adapter): selected/explicit step schema with final whole-form rejection; root constraints/stale async validation; ignored transport abort and successful retry; session invalidation during parsing with no stale request/errors; first invalid focus, summary fallback and no autosave focus. Existing 47 cases still cover parsed-output snapshots, autosave, lifecycle and failure mapping. Final forms suite: **57/57 passed**. Owned ESLint, current-tree TypeScript and diff checks are clean. DOM tests exercise wiring and lifecycle; real-browser focus/keyboard acceptance remains under the parent's aggregate browser gate.

`AppForm.spec.md` records the complete operational contract. Source is held after this amendment; no genuine design choice remains for row 38.

## Final row-39 disposition — date-only formatting

`conventions/development/frontend/core/mla/domains/i18n/i18n.md:34–38` requires locale-aware date/time formatting and preserving calendar dates across timezones; it does not prescribe a Temporal overload on `LocaleFormatters.date/time`. Their explicit `Date | number` input contract does not accept PlainDate, so the absence of an overload is a capability extension, not a release blocker. No speculative overload was added.

Date-only fields must format their calendar components without interpreting them as a local or UTC instant and then applying the viewer's timezone. If an Intl date-only adapter uses a Date bridge, it must construct the chosen calendar fields and pin the formatter to the same calendar/timezone (with explicit handling of years 0–99), rather than passing the bridge to the ordinary instant formatter with an arbitrary timezone. Instant formatting remains the existing Date/epoch contract; Temporal wire conversion remains the explicit field codec boundary. A named PlainDate formatting helper can be added when that concrete public capability is selected, with leap-day/year-boundary/timezone fixtures. This is removed from the genuine blocker list.


## Final foundation visual layout amendment

Moved four root visual components into their own camelCase folders under the existing foundation capability: `icons/icon/Icon.vue`, `icons/spinner/Spinner.vue`, `i18n/formattedRelative/FormattedRelative.vue`, and `animation/animatedLayout/AnimatedLayout.ts`. Each has its own `index.ts` and adjacent `*.spec.md`. Capability barrels preserve all existing public names and types; optional peer metadata and package entries are unchanged. Existing provider role folders were preserved.

`AnimatedLayout.ts:74` declares `defineComponent` and its setup returns a render function producing a `div` and cloned slot children. Its primary role is therefore a rendered component, even though it is authored in TypeScript; the pure motion helpers remain at the animation capability seam. Specs describe the actual API and distinguish source/SSR smoke evidence from behavior not established by this layout-only change.

Validation: `vue-tsc --noEmit -p tsconfig.typecheck.json` passed; `scripts/check-sfc.mjs` compiled **407 SFCs**; affected icons/i18n suites passed **7/7** Node/DOM/SSR tests across four files; owned ESLint and source/spec-link checks passed. Logs: `/private/tmp/visual-roots-{types,sfc,tests,lint}.log`. Source held after the moves.

## Read-only query/router adapter placement disposition

The physical source correction is required by `conventions/development/frontend/shapes/library/library.md:36–38`: implementation-specific adapters belong in `adapters/{provider}/`, vendor imports remain there, and a contract entry must not reach the vendor. Line 37 explicitly separates public subpath names from physical folders. Current `src/query/CreateQueryClient.ts:1,55` imports and returns TanStack QueryClient; `query/hooks/UseAppQuery.ts:4,17` uses the vendor QueryKey; `router/CreateAppRouter.ts:2–12` imports Vue Router runtime/types, and `router/RouteConfig.ts:2,29–49` exposes vendor locations, params and redirects. These implementation/type dependencies are still physically flat or mixed with generic hook roles.

`README.md:16–18,44–48,66` already declares `/query`, `/query/testing` and `/router` as selected application-adapter entries with their optional peers. Those entries are not claimed to be vendor-free contracts. Therefore their names and existing peer requirements can remain while source moves to `query/adapters/tanstack/` and `router/adapters/vueRouter/`, with public barrels re-exporting the selected adapters. Keep vendor-free reusable seams outside the adapter only when their complete import/type graph is vendor-free; do not move provider-independent helpers merely because they were adjacent.

`swappable-modules.md:9–16,22–27,53` requires vendor-free shared contracts for capabilities treated as interchangeable, and permits typed native escape hatches at selected adapter boundaries. `data/state-and-data.md` plus `data/tanstack/tanstack.md` additionally require house Result/error/live-state adaptation, already implemented by the query lane. Physical relocation alone does not establish interchangeable QueryClient/Router behavior or prove conformance to a new contract. A new engine-neutral router/query-client lifecycle API, alternative engine and cross-engine conformance suite would be a separate public-contract design scope. The current forced source task is adapter placement with existing behavior preserved; retaining explicit vendor-bound entry names does not require a user decision. No query/router architecture source was changed in this read-only assessment.


## Query/router physical adapter amendment — implemented

Following the read-only disposition, moved **39 implementation files** beneath `src/query/adapters/tanstack/` and `src/router/adapters/vueRouter/`. The runtime implementation barrels moved with them. Existing `src/query/index.ts` and `src/router/index.ts` are thin re-export entries; `src/query/testing.ts` still explicitly re-exports test-only helpers. All three build entry filenames and package export names are unchanged, so this amendment requires no manifest changes.

Public `/query` and `/router` remain explicitly vendor-bound adapters: factories and native escape surfaces retain TanStack/Vue Router types and require the already-declared optional peers. This amendment makes no new vendor-free/shared-engine contract claim and introduces no alternative engine. Vendor imports now occur only beneath the respective named adapter folders. Native Result adaptation, query lifecycle and route behavior are unchanged.

Vendor-free helpers stay outside where their independent role is clear: `query/PageExtensions.ts`, `router/Paths.ts`, the manual `router/hooks/UseNavigationProgress.ts` context, `ProgressProvider.vue` and navigation-progress tokens. Query's manual progress bridge imports that vendor-free context directly, preserving the existing absence of a Vue Router dependency in `/query`. Visual adapter SFCs occupy component folders with barrels (including `queryDevtools/QueryDevtools.vue`, app nav link, route announcer, not-found, navigation progress and error boundary); provider files retain their provider role. Existing source and test imports were rewritten by resolved target, not by ambiguous basename replacement.

Validation: current source TypeScript passed; **407 SFCs** compiled; query/router suites passed **15/15** tests across five files; owned lint and diff checks are clean. A source scan confirms zero vendor imports outside `adapters/` in the two capabilities and verifies the three public build-entry sources remain present. Logs: `/private/tmp/query-router-layout-{types,sfc,tests,lint}.log`. Source is held; packed-artifact graph verification remains the parent's aggregate release gate.


## Row 17 — qualified native root handles: accepted with eight corrections

The old blanket finding against `defineExpose({ el })` is refuted by the settled contract. Vue macros explicitly allow a documented element-handle API, require consumer inventory before removal, require target/null-lifetime documentation and reject treating arbitrary `$el` as a stable HTMLElement (`conventions/development/frontend/core/lla/constructs/vue/macros.md:48–51`). Root exposure is retained for native focus, positioning, scrolling and measurement. A root handle is not permission to expose unrelated component internals or treat fragment/Teleport placeholders as elements.

Current source inventory found **309 SFCs with defineExpose**, including **291 exact root-only el exposures** (a syntax count, not proof of every prop/slot branch). Native template refs and deliberate inner-root forwarding account for the usual implementation. The actual consumer inventory is:

| Consumer family | Current source evidence | Native requirement |
|---|---|---|
| Layer trigger registration/restoration | `presentation/overlays/popover/PopoverTrigger.vue`, `modal/ModalTrigger.vue`, `drawer/DrawerTrigger.vue`; `OverlayExtensions.ts:16` | Register a real trigger element; restore native focus when content closes |
| Navigation/roving focus | `presentation/nav/menu/MenuItem.vue:67,75`; `foundation/primitives/rovingFocusGroup/RovingFocusContext.ts:122–125,200` | Registered item `.el.focus()`; guard runtime component `$el` before using it |
| Positioning and measurements | `foundation/primitives/anchoredPositioner/AnchoredPositioner.vue:7,68,79`; `presentation/overlays/bottomSheet/BottomSheet.vue:195–200` | Real HTMLElement anchor/owner document and `getBoundingClientRect()` |
| Nested root forwarding | `presentation/layout/hStackLayout/HStackLayout.vue`, `vStackLayout/VStackLayout.vue`; inner `.el` forwarding | Preserve one documented native handle through wrapper layers |
| Presence and focus scopes | `foundation/primitives/presence/Presence.ts:29–32`; `focusScope/FocusScope.vue:60` | Distinguish mounted elements from absent/comment roots before lifecycle/focus work |
| Picker containment and scrolling | `presentation/forms/selectPicker/SelectPickerContent.vue:94`; `comboboxPicker/ComboboxPickerContent.vue:90,120`; `ComboboxPickerInput.vue:43,130–131` | Native containment/scroll targets across portalled content |

There is no universal component-handle `resolveElement` API in the current tree; the identically named local function in shortcuts resolves hotkey targets. Concrete consumer helpers are `toHtmlElement`, guarded `$el` adapters, documented `.el` forwarding and context-owned element refs. This distinction avoids inventing a generic resolver as acceptance evidence.

Eight wrappers were genuine violations: their template ref pointed to Card/RovingFocusGroup and `defineExpose({ el })` exposed that child component instance under an API documented as a DOM node. The prior `ComponentElement` annotation narrowed declarations but did not change this runtime shape. Corrected exactly:

- `presentation/nav/navigationMenu/NavigationMenuList.vue`
- `presentation/nav/menubar/Menubar.vue`
- `presentation/display/stepperGroup/StepperGroupList.vue`
- `presentation/display/tabsGroup/TabsGroupList.vue`
- `presentation/display/treeViewer/TreeViewer.vue`
- `presentation/display/featureCard/FeatureCard.vue`
- `presentation/display/pricingCard/PricingCard.vue`
- `presentation/display/stepCard/StepCard.vue`

Each keeps its private child-component template ref and exposes a computed `HTMLElement | null` from the child's documented `.el`, guarded with that node's owner-document HTMLElement constructor. Adjacent instance contracts now state the target and null lifetime. No root API was removed, no imperative action was fabricated, and no private inferred Vue SFC helper type was added to the public signature.

New `tests/unit/presentation/display/RootHandles.dom.test.ts` passes **2/2** representative public-import tests: a nested StepCard/Card root supports native focus and `measureRect`, exposes no nested `.el`, and becomes null after unmount; a provider-owned TabsGroupList exposes the RovingFocusGroup DOM root. TypeScript accepts these as native handles through `InstanceType` of public exports. Owned ESLint/diff checks are clean; **407 SFCs** compile. Logs: `/private/tmp/root-handle-{tests,types,lint,sfc,diff}.log`. Packed strict declaration checks and real-browser focus/geometry remain the parent's aggregate gates. Source was released to the canonical-model naming lane after these bounded corrections.

Disposition: row 17's removal proposal is closed/refuted; the eight actual wrapper contract defects are fixed. Remaining root exposures are intentionally retained under the qualified element-handle contract, not counted as hundreds of violations merely because their exposed surface is `el`.

## Row 41 — runtime claims reconciled with evidence

The existing README correctly separated DOM-free imports, Node SSR render fixtures, happy-dom interaction and Chromium behavior, but did not yet meet the library compatibility owner's exhaustive public-subpath matrix requirement. Added a matrix directly to the package `README.md` so it is shipped in the tarball rather than linked to an unpublished internal document. Its **70 rows exactly equal all 70 manifest export keys**, with no omissions/duplicates: 66 JavaScript entries and four assets/metadata entries. This was checked against `package.json` after writing.

The matrix distinguishes the package gate's **62 DOM-free import/typecheck entries without optional adapter peers** from **66 with selected peers**, and from bounded SSR fixture evidence. It names per-entry operational Web APIs/owner requirements and the actual tested baseline: Node 20.10.0, Vue 3.5.41, TypeScript 5.9.3, Chromium 151.0.7922.34 / Playwright 1.62.1 and ES2022 ESM output. Firefox/WebKit are unverified; no broader browser minimum is verified. ES2022 does not imply API/CSS support. The complete new browser gate is explicitly pending, and final source changes require re-verifying the release artifact.

Evidence boundaries are explicit: `check-package.mjs:84–130` launches Node imports/strict declaration compilation with selected peers; `tests/support/Smoke.ts:187–196` creates a fresh SSR app and renders registered fixtures without DOM globals. Provider cases register AuthProvider, FlagsProvider and ProgressProvider only; the matrix does not imply analytics/feedback/query-router SSR coverage from that suite. Locale's two mounted tests prove independent-root/replacement behavior and one deterministic happy-dom hydration probe. Auth replacement/unmount races, isolated query clients/lazy-query reset, form invalidation and primitive nested-scope cleanup have named focused tests; provider mounting alone does not prove arbitrary supplied adapter cleanup. No package-wide hydration or assistive-technology guarantee is made.

Runtime-source changes were not needed for this documentation closure. Server callers remain responsible for explicit cleanup of resources they start because client unmount hooks do not run after SSR. Temporal is imported locally rather than installed as a global mutation; browser operations retain their own documented unsupported/error contracts. Row 41 is documented accurately, with the aggregate browser/packed-artifact gate remaining an explicit release acceptance condition.

Parent's later PascalCase correction is preserved: the test-only query source entry is now `src/query/Testing.ts`, with matching dist targets; public `./query/testing` is unchanged. Earlier lower-case source-path evidence in this report describes its checkpoint, not the current filename.

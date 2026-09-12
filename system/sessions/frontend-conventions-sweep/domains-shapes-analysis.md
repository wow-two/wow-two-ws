# Domains and shapes conventions audit

2026-09-09. Read all 25 Markdown files under `conventions/development/frontend/core/mla/domains/` and `conventions/development/frontend/shapes/`. Existing uncommitted shape additions are intentional current input. No repository edits or SDK source verdicts. Paths below are repository-relative; evidence comes from current files.

## Verdict and severity

The conventions are not a settled baseline. Preserve the listed SDK sweep and add the following convention corrections before measuring SDK compliance. P1 = fix before implementing the affected SDK contract; P2 = structural/baseline correction before declaring the whole sweep complete. Suggested task groups are D1–D11; they are independent analysis identifiers, not new SDK row numbers.

## D1 — P1: representable scalar wire contract

Evidence:

- `conventions/development/frontend/core/mla/domains/api/type-mapping.md:15` maps every long/decimal to number, prohibiting bigint and decimal strings. Backend `conventions/development/backend/dotnet/shapes/service/platform/responses/serialization.md:15` repeats this policy. Large integers and precision-sensitive decimals cannot round-trip through binary64. Fix requires coordinated wire policy, not frontend-only wording.
- `type-mapping.md:22` maps JSON object dictionaries to ReadonlyMap<K,V> without decoding/encoding rules. JSON.parse creates ordinary objects; ordinary JSON.stringify(Map) produces `{}`.
- `type-mapping.md:20,29,48-55` assumes ISO TimeSpan durations. Default System.Text.Json TimeSpan uses strings such as `2.00:00:01`. Backend `serialization.md:16,25-26` requires ISO but names no TimeSpan converter. Runtime converter existence remains UNVERIFIED; do not claim SDK defect until inspected.
- `type-mapping.md:48-55` detects Temporal types by string contents. A date-shaped free-text string is indistinguishable from an actual date without type metadata. Strict regex does not prevent false conversions; key exclusions cannot distinguish equal field names in different schemas.
- `type-mapping.md:19,50` omits fractional TimeOnly from the reviver pattern. Naive DateTime gets a PlainDateTime row at :37 but no matching decoder branch.
- `type-mapping.md:23,80-82` universally equates nullable and optional. Explicit-clear versus omitted/unchanged update semantics and nulls in collections are unspecified.

Action: define safe numeric ranges and an exact-number encoding, dictionary wire models/converters, schema-directed codecs, all backend converters, and nullable/update semantics. Round-trip tests: >2^53 integer, high precision decimal, dictionary, fractional time, duration, naive datetime, date-shaped text, nullable collection entry, omitted versus clear.

Primary sources: [RFC 8259](https://www.rfc-editor.org/info/rfc8259/), [System.Text.Json TimeSpan](https://learn.microsoft.com/en-us/dotnet/core/compatibility/serialization/6.0/timespan-serialization-format), [System.Text.Json dates](https://learn.microsoft.com/en-us/dotnet/standard/datetime/system-text-json-support), [JSON.stringify](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/JSON/stringify).

Sweep mapping: NEW convention task + subsequent SDK codec audit. Not covered by Result rows 12–14.

## D2 — P1: HTTP/query/validation/form error interoperability

Evidence:

- `conventions/development/frontend/core/mla/domains/data/state-and-data.md:25-29,50` requires public Result failure values while mandating TanStack Query without defining the internal conversion into rejected promises. Returning a failed Result as resolved data marks engine success unless an adapter translates it. The no-content `undefined as T` rule also makes any requested T falsely inhabitable.
- `conventions/development/frontend/core/mla/constructs/data/result.md:24-28` requires house Results from validators. `conventions/development/frontend/core/mla/domains/validation/validation.md:11-14` requires Standard Schema; its protocol is `{value}|{issues}`, optionally async. Explicit foreign-protocol boundary is absent.
- `state-and-data.md:24` cites RFC7807; backend `conventions/development/backend/dotnet/shapes/service/platform/responses/problem-details.md:5` owns RFC9457.
- `conventions/development/frontend/core/mla/domains/forms/submission.md:31-32` specifies fieldErrors; backend `problem-details.md:15,33` emits errors arrays with property/code/message.
- `state-and-data.md:27` makes AppError carry status; `result.md:48` forbids HTTP status. Clarify status-at-edge metadata versus domain fields.

Action: preserve public Result semantics while documenting vendor-error translation, no-content endpoint typing, Standard Schema adapters, canonical ProblemDetails field/code/path mapping, malformed response handling, cancellation/timeout classification and query cache identity isolation.

Acceptance: failure Result triggers query error/retry semantics; cancellation avoids error toast; .NET validation fixtures map to fields; 204 is typed no-content; sync/async schema results preserve protocol.

Primary sources: [TanStack query functions](https://tanstack.com/query/latest/docs/framework/react/guides/query-functions), [Standard Schema](https://standardschema.dev/).

Sweep mapping: EXTEND rows 12–14; avoid duplicate Result task.

## D3 — P1: form input/output, steps and autosave

Evidence:

- `conventions/development/frontend/core/mla/domains/forms/forms.md:44-46` requires editing ApiRequest/Dto directly while allowing forgiving enum strings. Numeric/date/enum transport types cannot represent all incomplete edits.
- `forms.md:106` demonstrates RuleValues despite banning Values types at :45.
- `conventions/development/frontend/core/mla/domains/forms/submission.md:18-19` discards schema transforms and requires manually redoing them on submit. Standard Schema supports separate input/output types.
- `forms.md:48,81` combines a whole-form schema with wizard gating via validate(); `submission.md:61-62` validates and touches everything. Later-step required fields can block the current step; no subset protocol exists.
- `submission.md:20-21,39-43` coalesces auto-submit onto the in-flight run without specifying whether edits during that run receive a trailing save.

Action: distinguish editing input from submitted output; choose validated output or named mapper; define step-scoped validation, trailing latest-value autosave, stale async-validation and stale server-error suppression. Add conformance cases for each.

Sweep mapping: NEW convention task + form conformance extension. Existing spec/demo rows 8/18/27 do not cover these behaviors.

## D4 — P2: provider-free contracts versus React/Vue wiring

Evidence:

- `conventions/development/frontend/core/mla/domains/domains.md:17-24` requires provider-free leads and library-specific subfolders.
- `data/state-and-data.md:48-59` embeds React state and TanStack choices.
- `forms/forms.md:15-20,29-37,67-90` embeds React render props, JSX and TanStack pin.
- `forms/submission.md:83-85` names the React TanStack peer.
- `icons/icons.md:27` names lucide-vue-next in the lead.
- `conventions/development/frontend/shapes/app/routing/routing.md:13-16` mandates React Router in shared shape rules; `domains/domains.md:52-53` says routing also follows provider split.

Action: contracts at roots; React/Vue/engine wiring in provider leaves; stable behavior stays central; public prop inventories/shipped implementation details move beside code.

Sweep mapping: NEW conventions task; retain SDK row 9 (React spellings), row 27 (stale React specs).

## D5 — P2: extraction and route ownership contradictions

- `conventions/development/frontend/shapes/app/routing/routing.md:23-26` waits for a second consumer; `conventions/development/frontend/shapes/app/architecture/boundaries.md:22-25` requires immediate extraction when generic, one consumer enough.
- `routing.md:58-59` assigns useParams to bootstrap/layout; :68 puts useParams in Page. Choose one route-to-page seam.
- `conventions/development/swappable-modules.md:12,14` limits facade growth to real usage and 2+ consumers; `conventions/development/dev-cycle.md:40-44` mandates proactive capability completeness, delaying only alternative adapters. Distinguish whole-capability completeness from vendor-facade parity.

Action: reconcile with genericness/whole-vector doctrine and the user's permission for radical private-SDK changes.

Sweep mapping: NEW convention task; informs SDK router/capability pass.

## D6 — P2: make current shape additions executable

- `conventions/development/frontend/shapes/library/library.md:15-16` requires colocated stories; central `conventions/development/repo/structure/sdk-structure.md:44,73-80` prohibits src stories and places them in tests/stories.
- `library.md:40-54` permits only role folders/no nested capabilities; `domains/domains.md:14,18,22` and `swappable-modules.md:21-23` need provider subpaths. Define source adapter placement separately from exports.
- `library.md:58` rejects a flat single model and single hook beside seam; :52 says singleton roles stay flat. Example contradicts threshold.
- `conventions/development/frontend/shapes/app/architecture/architecture.md:12-21` omits the application-to-integration edge; `boundaries.md:52-53` says ports are not adopted. Define current consumption edge or explicitly adopt ports.
- `architecture.md:44` makes bootstrap flat; :58 domain-slices every layer. State bootstrap exception.
- `architecture.md:74-75` reserves common/pages for no-domain pages; :130 places domain-owned CreateCodePage/CodesListPage in codes/common/pages.
- `architecture.md:121` flattens integration client/interceptors despite :46-52 domain-first rule. `data/state-and-data.md:20-24` instead prescribes src/api/client.ts/types.ts; `forms/forms.md:29` prescribes src/form.ts outside five layers.
- `shapes/app/platform/styling.md:14` says src/index.css; :31-33 and architecture say bootstrap/index.css.

Action: one canonical tree, linked story ownership, legal provider source placement, threshold-consistent examples, current application/integration seam. Do not revert intentional uncommitted shape changes.

Sweep mapping: NEW convention reconciliation; extend rows 22/26 folder cleanup and 8/18 spec/demo moves only after target settles.

## D7 — P2: operational security baseline

- `conventions/development/frontend/core/mla/domains/config/config.md:17,29-38` redacts secret error fields but sources VITE/browser-global values without declaring them public. Bundled secrets remain exposed despite redaction.
- `auth/auth.md:11-24,32-35` lacks trust/CSRF/safe-return-URL/logout cleanup and stale session-response rules.
- `storage/storage.md:17-20` versions/namespaces keys without sensitive-data limits or tenant/logout cleanup.
- `uploads/uploads.md:12-19` admits files client-side without stating authoritative server validation or retry idempotency.
- `flags/flags.md:11-24` lacks backend-authorization boundary.
- `analytics/analytics.md:13-18` covers consent buffering without identity reset/data minimization; `observability/observability.md:14-17` key redaction does not cover arbitrary free-text URLs/messages.

Action: one security owner plus domain extensions for public config, backend authorization, CSRF pairing, redirects, persistent credentials, session-scoped cleanup, server file validation, retries and safe telemetry. These are missing baselines, not claims of exploited SDK vulnerabilities.

Primary sources: [Vite public env](https://vite.dev/guide/env-and-mode), [OWASP CSRF](https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html), [OWASP uploads](https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html).

Sweep mapping: NEW convention/SDK audit tasks.

## D8 — P2: lifecycle and SSR support scope

- `auth/auth.md:17,19,24` mixes module-scope session bridge with SSR import safety.
- `feedback/feedback.md:6` explicitly chooses module-state hub.
- `analytics/analytics.md:21` claims unchanged SSR operation.
- `i18n/i18n.md:17-20` independently chooses browser locale/server default without hydration seed.

Action: distinguish import-safe from SSR-render/hydration support. If SSR supported, require per-request clients/stores/buses and shared initial locale/theme; otherwise state import-only support. Suppress late async responses after logout/disposal/reset. No live request leak is established by document review.

Primary source: [Vue SSR request isolation](https://vuejs.org/guide/scaling-up/ssr.html).

Sweep mapping: NEW lifecycle baseline + conformance tests. Components auditor owns provider.md accessor-throws contradiction with i18n.md:16; flags.md:20 also promises standalone fallback.

## D9 — P2: accessibility and locale application rules

- `conventions/development/frontend/frontend-conventions.md:173` acknowledges missing consumer keyboard/ARIA/focus baseline.
- `i18n/i18n.md:11-22` lacks document/subtree lang/dir, timezone and escaping ownership.
- `shapes/app/routing/routing.md:15-16,65-67` gives scroll/title but not navigation focus/announcements.
- `forms/forms.md:67-81` gives chrome IDs/errors but not invalid-submit focus/summary and custom-control checks.
- `feedback/feedback.md:11-21` lacks live-region urgency, accessible timing and action behavior.

Action: baseline plus domain references, preserving existing kind/Tailwind rules. Include keyboard routes/focus, invalid-submit summary, status-versus-alert, lang/dir/timezone and real-browser interaction checks.

Primary sources: [WCAG language](https://www.w3.org/WAI/WCAG22/Understanding/language-of-page.html), [W3C direction](https://www.w3.org/International/questions/qa-html-dir).

Sweep mapping: ACKNOWLEDGED gap, NEW tracked work; extend row 18 interaction stories. Row 30 ARIA constants is not accessibility behavior coverage.

## D10 — P2: testing and release delivery gates

- `shapes/library/library.md:66-69` says architecture/delivery/testing unwritten.
- `shapes/app/platform/platform.md:23-24`, `app/app.md:16` say build output/assets/delivery unwritten.
- `frontend-conventions.md:172-175` already lists these gaps.
- `conventions/development/repo/structure/sdk-structure.md:97-103,123` already owns dist-only tarball/pack checks; link and extend, do not duplicate.
- `conventions/deployment/hosting/single-host-serving.md:17-30,38-47,51-72` already owns wwwroot/fallback/build. Link it from platform rather than calling the entire area absent.
- `shapes/app/platform/dev-server.md:35` uses changeOrigin:true; central single-host-serving.md:81 uses false. Choose one host-header policy.
- Central `single-host-serving.md:60-65` incremental inputs omit lockfile/public/env/config dependencies; install occurs only when node_modules absent. Changes to those inputs can leave stale build/dependencies under the published recipe.

Action: define library export/type resolution, ESM/browser/SSR matrix, optional peers and runtime isolation, CSS side effects, packed clean-consumer smoke, bundle/tree-shaking checks, version/changelog/release verification. Optional peer metadata is package-level; describe subpath runtime isolation accurately.

Testing tiers: pure logic, adapter conformance, rendered interaction, browser integration, accessibility, packed-consumer. App delivery: browser/polyfill baseline, fonts/images/public assets, cache/hash policy, chunk-load recovery, source-map policy; central owner fixes incremental inputs.

Primary sources: [Node exports](https://nodejs.org/api/packages.html), [npm manifest](https://docs.npmjs.com/cli/v11/configuring-npm/package-json/).

Sweep mapping: ACKNOWLEDGED gaps, NEW tracked testing/delivery tasks. Preserve four existing SDK gates; add build/pack/consumer checks for release.

## D11 — P2: rule ownership and stale surface narration

- Presentation-router prohibition duplicated at library.md:26-29 and routing.md:27,57.
- type-mapping.md:72-74 repeats collection spelling; :65-66 repeats backend serializer obligation.
- analytics.md:20, feedback.md:17, observability.md:20-21 repeat central opt-in rule.
- forms.md Entities/prop/escape-hatch inventories and routing.md:63-70 shipped wrapper details are surface register content, forbidden by central convention ownership.
- shapes.md:14 calls library a shell despite normative layout; precise partial status needed.

Action: link one owner per obligation and move shipped surface inventories beside code. D4 owns provider relocation; do not duplicate its work.

Sweep mapping: NEW convention cleanup; row 27 spec update when inventories move.

## Coverage ledger

All assigned files read (relative to `conventions/development/frontend/`):

| File | Coverage |
|---|---|
| core/mla/domains/domains.md | provider shape/ownership; D4/D6/D10 |
| core/mla/domains/analytics/analytics.md | consent/buffering/sinks; D7/D8/D11 |
| core/mla/domains/api/type-mapping.md | scalars/dates/nulls/collections; D1/D11 |
| core/mla/domains/auth/auth.md | session/strategy/bridges/SSR; D7/D8 |
| core/mla/domains/config/config.md | precedence/parsing/secrecy; D7 |
| core/mla/domains/data/state-and-data.md | HTTP/errors/state/mutations; D2/D4/D6 |
| core/mla/domains/feedback/feedback.md | bus/lifecycle/render/query; D7/D8/D9/D11 |
| core/mla/domains/flags/flags.md | total eval/context/fallback; D7/D8 |
| core/mla/domains/forms/forms.md | pin/schema/fields/arrays; D3/D4/D6/D9 |
| core/mla/domains/forms/submission.md | errors/submit/validation/testing; D2/D3/D4 |
| core/mla/domains/i18n/i18n.md | locale/messages/formatters; D8/D9 |
| core/mla/domains/icons/icons.md | adapter/semantic/provider; D4 |
| core/mla/domains/observability/observability.md | hostile context/redaction/sinks; D7/D11 |
| core/mla/domains/storage/storage.md | sync seam/migration/namespace; D7 |
| core/mla/domains/uploads/uploads.md | admission/retry/cancel/progress; D7/D8 |
| core/mla/domains/validation/validation.md | schema/errors/codes/providers; D2/D3/D4 |
| shapes/shapes.md | deliverable/vector boundary; D11 |
| shapes/library/library.md | kind/capability/layout/gaps; D6/D10 |
| shapes/app/app.md | app scope/delivery; D10 |
| shapes/app/architecture/architecture.md | layers/roles/slices/examples; D6 |
| shapes/app/architecture/boundaries.md | extraction/packages/ports; D5/D6 |
| shapes/app/platform/platform.md | wiring/output/assets; D10 |
| shapes/app/platform/styling.md | source depth/tokens/theme/helper; D6 |
| shapes/app/platform/dev-server.md | HTTPS/proxy/headless/preview; D10 |
| shapes/app/routing/routing.md | model/ownership/extraction/params; D4/D5/D9 |

All non-HTTP Markdown target paths in the assigned files exist; path check did not verify prose section pointers. Existing SDK sweep counts are historical and require remeasurement in SDK phase. No current SDK code behavior is certified by this convention audit.


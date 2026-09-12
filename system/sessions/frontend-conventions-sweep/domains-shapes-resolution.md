# Domains and shapes resolution

*Last updated: 2026-09-10*

> Convention changes for the Vue sweep; implementation and release verification remain in the SDK phase.

## Status

- [x] Resolved the domain/shape contract and ownership defects within this lane.
- [x] Preserved intentional app/library role-group additions and corrected their examples.
- [x] Added Vue provider leaves, security, compatibility, testing, delivery and asset owners.
- [x] Checked all outgoing and incoming explicit Markdown targets/fragments for this lane.
- [ ] Resolve the exact wide-number wire policy with the backend owner.
- [ ] Reconcile backend CLR TimeSpan serialization wording with its actual converter policy.
- [ ] Verify the declared contracts against the Vue SDK implementation and packed artifact.

---

## Changes by consolidated task

| Task | Lane result | Remaining dependency |
|---|---|---|
| C01 | Library stories defer to central SDK structure; provider source folders differ from public subpaths; singleton examples fixed; same-domain application-to-integration edge explicit; bootstrap exception and route param ownership fixed. | Parent reconciles cross-area indexes; shared swappable-module wording is fixed. |
| C02 | No taxonomy changes owned here; library/app placement follows the visual kind owner. | Component lane. |
| C03 | Forms separate editing input from parsed output and field binding; framework spelling is in Vue leaf. | Component controlled/native-attribute contract. |
| C04 | Auth/feedback use explicit instance handles; hosts are unique per hub/destination; provider lifetime and replacement explicit. | Component modal/navigation/provider contracts. |
| C05 | Added route focus/announcement, invalid-submit focus/summary, notice live-region policy and browser interaction matrix. | Shared accessibility owner and SDK browser/AT evidence. |
| C06 | DTOs use real JSON types; declared schema codecs; object/Map conversion; safe integer/decimal limits; failure/vendor translation; RFC9457 errors; no-content Result<void>; cancellation and session cache scope. | Exact wide-number wire choice and backend TimeSpan wording; backend runtime fixtures. |
| C07 | Parsed schema output submitted; editable models allowed; scoped wizard validation; single-flight manual submit; trailing latest autosave; stale responses/errors suppressed; Vue leaf. | SDK form-engine conformance and Vue interaction tests. |
| C08 | Provider-free domain roots with Vue form/query/router wiring; import safety distinct from SSR/hydration; explicit request/instance lifecycle. | Framework/LLA lane, then SDK behavior verification. |
| C09 | App CSS entry corrected to bootstrap, Vue plugin/package sample, library CSS delivery and side-effects owner added. | LLA CSS rules. |
| C10 | Wire static types explicitly do not validate input; unknown enums, safe numerics, collections and omission/null/clear distinguished. | LLA TypeScript rules and exact numeric wire choice. |
| C11 | Locale, timezone, lang/dir, pluralization, escaping and hydration seed; shared resource cleanup and identity transitions. | SDK control/locale/lifecycle verification. |
| C12 | Testing tiers, discovery, interaction matrix, per-subpath runtime matrix, feature detection/polyfill ownership and explicit SSR claim levels. | SDK publishes concrete supported versions and runs applicable tests. |
| C13 | Export/type existence, package-level optional peers, transitive import isolation, CSS, tarball clean-consumer checks, publication identity and partial-publication recovery. | SDK build/pack/version/workflow verification. |
| C14 | Public config, trust/render/URL boundaries, auth/CSRF, storage/upload/telemetry; app build inputs, host handoff, assets/fonts/cache/source-map policy. | Backend/host owner implements its portion; shared BuildSpa recipe is aligned and executable fixture checks pass. |
| C15 | Removed stale React surface rosters and impossible examples; one library layout and routing owner; replaced gap placeholders with actual owners. | Parent performs global semantic duplicate/section-pointer check. |

---

## Decisions implemented

- Wire DTOs remain integration-owned. A straight read may keep its DTO; integration maps only when a richer/different representation is needed.
- Date/time DTO fields are wire strings. Schema-selected integration codecs produce Temporal values; free-text strings are never guessed as dates.
- Standard Schema retains its own result protocol. Query adapters translate house failure Results into vendor rejections internally and back at the public boundary.
- One manual submit snapshot is single-flight. Autosave preserves the latest edit with a trailing save; newer values are not overwritten by older completion state.
- Pages receive decoded route inputs through bootstrap adapters. Generic router behavior belongs in the SDK as soon as generic; a second product is not required.
- The uncommitted role-group tables remain authoritative. Provider source lives in `adapters/{provider}/`; public export spelling can differ from source folders.
- Shared mutability is app-instance/request-scoped. DOM-free import, SSR render and hydration are separate per-subpath claims.
- The browser/runtime matrix is versioned beside each package/entry. Choosing exact supported versions belongs in the Vue package release validation, not a universal floating convention.

---

## Remaining choices and recommendations

### Exact wide numbers

Evidence: backend `engineering/codebase/wow-two-back-beta-sdk/src/Foundation/Serialization/JsonOptionsConstants.cs:22-31` uses ordinary JSON numbers and enables reads from strings; no exact-number output codec is configured there. The backend convention requires number output. Binary64 cannot represent all CLR long/decimal values exactly.

Recommendation: agree a backend/API-wide exact-value policy (decimal strings for precision-sensitive values and a declared representation for wide integer identifiers), then add matching endpoint schemas and round-trip fixtures. Until that change is agreed, support only proven safe numeric contracts and reject unsupported precision claims. Do not silently reinterpret every number/string in the frontend. This is the one genuine domain contract choice left open in this lane.

### CLR TimeSpan

Evidence: the same preset registers NodaTime but no CLR TimeSpan ISO converter; backend `serialization.md` still requires ISO strings universally. Frontend convention now requires an explicitly declared duration codec and permits the actual constant-format wire shape. It rejects calendar months/years when encoding fixed elapsed TimeSpan units.

Recommendation: retain the observed wire format unless the backend owner explicitly adopts an ISO converter and supplies fixtures. Reconcile the backend doc in its active lane; this frontend lane did not edit backend files.

### Shared convention amendments

- `swappable-modules.md` now inherits the vector-completeness owner instead of using a 90%-surface or two-consumer gate. Adapter ceilings remain explicit; shared conformance asserts both supported behavior and declared unsupported outcomes.
- Library delivery owns shipping-source aliases: relative imports unless declaration emit rewrites them; no private aliases in the package declarations; `@src` is test-only by default.
- `single-host-serving.md` runs frozen install and the SPA build without a timestamp-only shortcut. It refreshes `Content` before static-asset discovery, including removal of deleted files by item identity.
- `publish --no-build` preserves its existing verified build. `BuildSpa=false` is reserved for output supplied by another build stage. Fresh publication uses a clean staging directory.
- Optional caching must fingerprint the complete file set, contents, tool versions and relevant environment inputs; file deletion and missing outputs invalidate it.
- The host doc now links the current host-configuration owner and does not claim API/SPA route correctness depends solely on registration order.


---

## Verification

- 35 domain/shape Markdown files exist after the sweep: 25 updated and 10 added.
- All non-HTTP outgoing Markdown target paths and explicit fragments in the assigned trees resolved.
- All incoming frontend Markdown references targeting these trees resolved.
- Example review: library singleton roles now meet their threshold; app tree uses domain-owned pages, sliced integration and explicit bootstrap router group; Vue examples contain no React API requirement.
- Text regression search: no fieldErrors contract, arbitrary undefined-as-T success, second-consumer router gate or unwritten shape gap remains in this lane.
- Actual backend factory read: `AppErrorProblemDetailsFactory.cs:43-48` emits code as a string and validation data under `errors`.
- No SDK tests/builds, rendered browser checks, .NET runtime serializer fixtures or published artifacts were produced by this documentation lane. Those remain required release evidence.
- Shell-authored documentation updates are not inferred into the shared touch ledger; no staging/commit was attempted.

---

## External evidence

The initial audit verified these primary sources; they support the amended contracts rather than certify SDK implementation:

- [RFC8259 numeric interoperability](https://www.rfc-editor.org/info/rfc8259/).
- [System.Text.Json TimeSpan representation](https://learn.microsoft.com/en-us/dotnet/core/compatibility/serialization/6.0/timespan-serialization-format).
- [Standard Schema protocol](https://standardschema.dev/).
- [TanStack query failure semantics](https://tanstack.com/query/latest/docs/framework/react/guides/query-functions).
- [Vite public environment variables](https://vite.dev/guide/env-and-mode).
- [Vue SSR instance isolation and hydration](https://vuejs.org/guide/scaling-up/ssr.html).
- [Node package exports](https://nodejs.org/api/packages.html).
- [npm package-level peer metadata](https://docs.npmjs.com/cli/v11/configuring-npm/package-json/).
- [OWASP CSRF boundary](https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html).
- [OWASP upload validation](https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html).
- [W3C language of page](https://www.w3.org/WAI/WCAG22/Understanding/language-of-page.html).
- [W3C direction markup](https://www.w3.org/International/questions/qa-html-dir).

---

## Executable BuildSpa verification

The documented XML was extracted directly into a temporary .NET 10 Web SDK project, with its `SpaRoot` placeholder replaced by a real frontend directory. The frontend uses a dependency-free Node asset builder and real `pnpm`; this verifies MSBuild/content/publication behavior, not a full Vite application.

| Case | Result | Assertion |
|---|---|---|
| clean publish | passed | initially absent generated index/asset are included in the publish output |
| changed source + deleted/replaced asset | passed | new content is published and removed asset is absent |
| publish --no-build | passed | prior verified SPA content is retained without regeneration |
| BuildSpa=false | passed | externally supplied/current SPA output is retained |
| stale lockfile with node_modules present | expected failure | ERR_PNPM_OUTDATED_LOCKFILE stops the publish |

- Runtime: .NET SDK `10.0.300`; commands ran against temporary files only.
- Evidence: `/var/folders/hy/sr0n_yrx7pz55hqd6dfnbm8c0000gn/T/fe-buildspa-vxb_0zlo/results.json` and adjacent command logs.
- Reproduction driver: `/private/tmp/verify_buildspa.py` (the stale-lockfile negative case was a separate targeted invocation).
- The shared XML does not claim an HTTP pipeline test, serializer fixture, cross-platform MSBuild run or Vite compilation.
- Source references: [MSBuild current-input timestamp limitation](https://learn.microsoft.com/en-us/visualstudio/msbuild/incremental-builds?view=visualstudio), [pnpm frozen install](https://pnpm.io/cli/install), [ASP.NET SPA publish integration](https://learn.microsoft.com/en-us/aspnet/core/client-side/spa/intro?view=aspnetcore-10.0).

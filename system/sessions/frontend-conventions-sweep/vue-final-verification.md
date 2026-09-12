# Vue sweep — final verification and release readiness

*Last updated: 2026-09-13*

## Scope and outcome

**2026-09-13 close-out:** the owner authorized autonomous commits for the remaining Vue sweep.
`9577d6c` commits the prepared error/logging slice; `3ae7df7` commits the remaining coupled implementation.
All current gates passed again: 93 Node/DOM/SSR files / 1,639 tests, 30 Chromium tests, 407 SFCs,
types, lint, formatting, capability graph, library/playground builds and a fresh independent npm consumer.
All 14 case-only paths are committed with their intended spelling and no duplicate legacy entries.
Current logs are `/private/tmp/vue-closeout-{types,lint,format,tests,browser,build,playground,package}.log`.
The verified local `0.0.5` artifact is `/private/tmp/ui-vue-closeout-20260913.tgz`; it is not a new release.

**2026-09-12 amendment:** the owner-selected lossless JSON/exact-number prototype is implemented.
Current gates pass: 1,634 Node/DOM/SSR tests, 30 Chromium ordinary/forced-colors tests, types/lint/format,
library/playground builds and an independent fresh npm consumer. Packed checks cover 72 targets and
exact numeric behavior. [Current implementation and evidence](lossless-numbers.md#integrated-verification--2026-09-12).
The detailed table below retains the earlier 2026-09-10 checkpoint; its pending items are superseded.

The full frontend conventions review covered all 363 original documents and produced 10 additional
documents. C01–C15 amendments are implemented; their evidence and SDK task mapping are in
[analysis](analysis.md), [baseline resolution](lla-resolution.md), [component resolution](components-resolution.md)
and [domain resolution](domains-shapes-resolution.md).

The selected SDK is `@wow-two-beta/ui-vue`. React implementation and release remain parked.
The implementation sweep is complete for the recorded Vue work; publication remains open.
The table below is historical. Neither a new package version nor a publication is claimed.

## Integrated gates — 2026-09-10 checkpoint

These results apply to the final combined source, including canonical models, DOM root handles,
theme contrast corrections, capability moves and typed operation results.

| Gate | Result | Evidence |
|---|---|---|
| Node/DOM/SSR regression suite | Pass: 89 files, 1,529 tests | `/private/tmp/vue-release-tests.log` |
| Strict source/test types | Pass | `/private/tmp/vue-release-types.log` |
| SFC compilation | Pass: 407 SFCs | Same typecheck log |
| Capability graph | Pass: 56 nodes, 1,021 cross-capability references, no cycles/unresolved imports | Same typecheck log |
| ESLint | Pass: zero errors/warnings | `/private/tmp/vue-release-lint.log` |
| Source/test formatting | Pass | `/private/tmp/vue-release-format.log` |
| Library and declarations build | Pass | `/private/tmp/vue-release-build.log` |
| Playground production build | Pass; large all-fixture gallery chunk warning | `/private/tmp/vue-release-playground.log` |
| Theme generation | Pass: 183 themes pass declared contrast pairs in both modes | [Contrast report](vue-theme-contrast-resolution.md) |
| Actual packed exports, strict consumer declarations and generated utility CSS | Pass: 70 exports, 62 core JS entries without optional peers, 66 with adapters | `/private/tmp/vue-release-package.log` |
| Chromium, ordinary and forced colors | Pending elevated loopback access | Final browser command requested; no new pass claimed |
| Fresh npm installation in an independent temporary root | Pending network access | Final isolated install command requested |
| Published version lookup | Pending network access | Default sandbox lookup failed with DNS `ENOTFOUND` |
| Frozen lockfile | Pass without replacing installed modules | `/private/tmp/vue-lockfile-verified.log` |

Temporary logs are local execution evidence, not shipped package files. The earlier nested-root npm
install could resolve dependencies from an ancestor fixture and is not sufficient isolated-install
evidence. The updated gate uses a separate temporary root and normal peer resolution.

## Resolved work

| Area | Result and detailed evidence |
|---|---|
| Component names, API and coverage | 109 family mappings; 95 canonical model surfaces; 379 adjacent specs; 349 public SFC fixtures; [component report](vue-components-resolution.md) |
| Native/composite controls | 54 native-reset roots, controlled/uncontrolled seeds, draft values, IME handling, semantic clear/reset and focus restoration; component report |
| Accessibility and motion | Persistent pause controls, keyboard exit, drag alternatives, nonmodal focus, nested modal ownership, forced-colors fallback; component and [behavior reports](vue-behavior-audit.md) |
| Forms | Parsed snapshots, trailing saves, step validation, request cancellation, session invalidation and manual invalid-field focus across both adapters; behavior report |
| Results, transport and auth | Shared carriers, explicit JSON decoding, vendor protocol boundaries, auth generations and safe redirects; [Result report](vue-results-resolution.md) |
| Browser operations and locale | Typed failures, stale-completion guards, cleanup and deterministic locale hydration; [browser report](vue-browser-resolution.md) |
| Capability structure | Retired generic buckets, semantic owners, grouped roles, adapter folders, standalone carrier files and public entry repair; [layout report](vue-capability-layout-audit.md) |
| Date/time wire values | Five named Temporal codecs, exact CLR ticks and .NET serializer fixtures; behavior report |
| Theme contrast | Text and required indicators corrected; exact token ledgers linked in the contrast report |
| Package and release | Manifest-driven entries, optional-peer isolation, strict declarations, packed CSS source registration and publish-the-verified-tarball workflow |

The migration document is SDK `engineering/codebase/wow-two-front-vue-beta-sdk/MIGRATION.md`.
The preserved sweep track is SDK `engineering/planning/ui-sdk-conventions-sweep.md`, rows 31–43
plus the explicitly resolved original rows. Row 42 remains the release acceptance row.

## Remaining discussion and verification boundaries

1. **Endpoint numeric contracts:** the owner selected a lossless JSON prototype on 2026-09-12.
   Exact numeric JSON can remain unquoted on the wire; the selected client codec must parse/write it
   without binary64 conversion. This prototype does not migrate every endpoint or native numeric form
   control. Restricted numeric representations are the last design option, not the default.
2. **Theme visual validation:** Smart QR is now an authored candidate because its tokens changed.
   Its application must revalidate the appearance. Automated declared-pair contrast checks do not
   establish contrast for every custom image, background or composition.
3. **Runtime evidence:** Firefox and WebKit are unverified. Browser minimums beyond the documented
   tested baseline are not promised. The README distinguishes DOM-free imports, bounded SSR fixtures,
   and operation-specific browser capability requirements for every public export.

The last two items describe explicit evidence limits and app scope, not permission to infer a pass.
There is no remaining Vue implementation decision in the component, Result or forms lanes.

## Release state

The local Vue manifest and verified npm registry version are both `0.0.5` as of 2026-09-12. The release workflow
bumps the beta patch version before building and checks the exact tarball it will publish.
Local commits were completed on 2026-09-13: `9577d6c` error/logging conventions, `3ae7df7` implementation,
`0e4aaae` documentation and `877f022` release gates. The SDK working tree and index are clean.
No version bump, tag, git push or npm publication was performed by this sweep.
Browser execution, the isolated npm consumer and the registry check are complete. Select/build/verify the
new version through the release workflow. Preserve the pre-existing shared staged/unstaged work when preparing commits.
Fourteen case-only filename renames (including the earlier JSON/PDF component renames) are committed
for macOS/Linux portability. The current operation inventory is `/private/tmp/vue-closeout-casing.json`.

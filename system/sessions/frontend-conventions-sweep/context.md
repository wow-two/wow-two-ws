# Frontend conventions and SDK sweep

*Last updated: 2026-09-12*

## Scope

- User order: fully analyze frontend conventions; add missing work to the existing sweep;
  finish conventions, finish the SDK sweep, publish a new version.
- User permits radical SDK changes and confirms no production consumers.
- Conventions root: `conventions/development/frontend/` (363 Markdown files).
- SDK repo: `workbench/wow-two-sdk-beta/wow-two-sdk-beta.ui/`.
- Existing track: SDK `engineering/planning/ui-sdk-conventions-sweep.md`; retain its IDs and completed work.
- Active SDK scope: Vue only, confirmed 2026-09-10. React implementation/release is parked.
- User requests a full sweep with autonomous resolutions; retain only genuine decisions for brainstorming.

---

## State

- Full conventions reading complete; findings consolidated in [analysis](analysis.md).
- Baseline/notation evidence: [LLA analysis](lla-analysis.md).
- Component/construct evidence: [component analysis](components-analysis.md).
- Domain/shape evidence: [domain analysis](domains-shapes-analysis.md).
- Separate SDK baseline: [SDK baseline](sdk-baseline.md); not a full SDK implementation audit.
- Added SDK sweep rows 31–42 and expanded acceptance for existing rows; retained earlier work.
- Full analysis records 15 convention work groups with evidence-to-task traceability.
- Convention amendments are complete: `lla-resolution.md`, `components-resolution.md` and
  `domains-shapes-resolution.md`. All 363 original documents were reviewed; 10 documents were added.
- Convention links/fragments and applicable compile/CSS/.NET publish reproductions pass.
- Vue exports, strict packed-consumer types, optional peers, live props, forced-colors focus
  and release tarball verification were corrected.
- Before current API migrations: 60 files / 1,345 tests, types/SFC, lint, format, build,
  packed checks and fresh npm tarball installation passed. Final combined gates must rerun.
- Components: 109 family mappings, 379 adjacent specs, 349 public-SFC fixtures and 54 native-reset roots; presentation source is held.
- Result/HTTP/query/auth/validators, command outcomes and scoped capability layout corrections are implemented; all implementation lanes are held.
- Forms parsing, detached snapshots, trailing autosave, step gates, request cancellation/session invalidation and manual error focus pass 57 tests in both adapters.
- Generic autosave now serializes writes, cancels queued disposal work and observes late failures; 13 regression tests pass.
- Forms source is `src/formsEngine/adapters/{house,tanstack}`; public `forms-engine` package keys are preserved.
- Explicit Temporal codecs pass 37 tests against recorded .NET 10 serializer fixtures.
- Final combined gate including exact numbers: 93 Node/DOM/SSR files / 1,634 tests, 407 SFCs, full types/lint/format passed.
- Library and playground production builds passed. Packed checks passed 72 targets / 64 core JS entries / 68 total JS entries, strict public types, exact numeric behavior and generated consumer CSS.
- Generic hooks retired, capability roles grouped, Result carrier files/names corrected, query/router adapters placed, and visual foundation roots folded into component folders.
- Added row 43 for the final source-role inventory; capability graph checks now run in typecheck.
- Artifact review's smart-qr/text/indicator contrast failures are resolved. All 183 themes pass declared contrast pairs; Smart QR is an authored candidate awaiting app visual review.
- Canonical models are corrected across 95 component surfaces, with 97 spec refreshes and a migration table. DOM root wrappers expose native roots consistently.
- Packed CSS now registers its own source directory; the production consumer gate catches missing SDK-only utilities.
- Fresh npm installation passed in a separate temporary root with normal peer resolution and no workspace dependency links.
- Frozen lockfile-only verification passes with the existing pnpm store; it did not replace installed modules.
- Full Chromium ordinary/forced-colors suite passed: 30 tests across six project files.
- Locale deterministic hydration and provider isolation have two passing regression tests.
- Owner chose a lossless JSON prototype on 2026-09-12 and rejected restricted numbers as the default.
- General representation choices now rank implementation-driven restrictions last; frontend codecs must preserve numeric tokens and use explicit arithmetic/rounding.
- New Vue `foundation/numbers` and `foundation/json` provide ExactNumber and LosslessJson; an explicit client JSON codec handles both HTTP directions. Both form adapters preserve exact values. [Prototype and complete evidence](lossless-numbers.md).
- SDK aggregate/browser/fresh-consumer checks are complete. Nothing published; prototype adoption and exact-number UI/schema extensions remain explicitly scoped follow-ups.
- Final evidence and release limits: [Vue final verification](vue-final-verification.md).
- Fourteen case-only filename renames are explicitly recorded in Git's index; every staged blob and all unrelated entries were verified unchanged. No source contents were newly staged.
- Current local manifests: React `@wow-two-beta/ui` `0.0.108`; Vue `@wow-two-beta/ui-vue` `0.0.5`.
  Vue npm registry version `0.0.5` was verified 2026-09-12; React registry version was not checked.

---

## Working tree

- Root frontend app/library shape docs already had intentional edits; two old frontend handoffs were deleted.
- SDK had 690 status entries, including staged work, at the baseline read.
- This session now owns convention amendments and the Vue implementation lanes listed above.
- Do not restore deleted handoffs, discard earlier changes, or commit the shared staged index indiscriminately.
- Vue source, tests, package/configuration and release-workflow edits exist. No commits or publication.

---

## Resume

1. Read resolution reports; initial analysis findings are historical, not current defects.
2. The owner-requested lossless-number prototype (row 44) is implemented and all gates pass; read its report for API boundaries.
3. Preserve parked React/app tasks; the numeric prototype does not silently migrate all clients or native-number controls.
4. Resolve prototype feedback and rerun affected gates for actual source changes.
5. Review the shared staged/unstaged content while preparing the commit; case-only names are already recorded.
6. Verify the intended version against the registry and release workflow before publication.

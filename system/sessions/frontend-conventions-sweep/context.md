# Frontend conventions and SDK sweep

*Last updated: 2026-09-26*

## Scope

- User order: fully analyze frontend conventions; add missing work to the existing sweep;
  finish conventions, finish the SDK sweep, publish a new version.
- User permits radical SDK changes and confirms no production consumers.
- Conventions root: `conventions/development/frontend/` (363 Markdown files).
- SDK repo: `workbench/wow-two-sdk-beta/wow-two-sdk-beta.ui/`.
- Existing track: folded on 2026-09-29 into the SDK's `engineering/planning/version-track/v0.1/v0.1.md` (iterations 10–11); open work in its `backlog.md`, method and gates in `engineering/development/rules.md`.
- Active SDK scope: Vue only, confirmed 2026-09-10. React library/release is parked.
- On 2026-09-13 the owner added a full SDK optimization pass, all playground/showcase/theme apps, and CI repair. React app-only corrections are authorized.
- User requests a full sweep with autonomous resolutions; retain only genuine decisions for brainstorming.

---

## Current milestone — ForeverPin adoption, 2026-09-26

- Native escaped directive enabled ordinary commits for ForeverPin in this chat. Workspace/template permissions remain OFF.
- All standing ForeverPin changes were committed first, with personal signatures: `3718f7c` routing,
  `f0d9203` CI/release verification, and `ae04e2b` gap analysis. The tree was clean before new work.
- `aeea5ba` closed the owner-accepted internal v0.9 milestone, moved all 41 unchecked rows exactly once into
  planned v0.11, preserved 22 parked hero rows, and opened v0.10. The separate backend lane remains unchecked.
- `132e14c` moved the app into `forever-pin.frontend-services/apps/web`, keeping root pnpm commands/IDE paths stable.
  All 134 source/test files moved byte-for-byte; dependency resolutions were unchanged. The app remains React.
- `0d3eba0` records the [full frontend audit](../../../workbench/ventures/10x-venture-forever-pin/engineering/architecture/frontend-adoption.md),
  verification, and adoption position. Only the frontend workspace checkbox is complete; Vue/backend adoption remain open.
- Verified ForeverPin typecheck, 4 unit tests, production build, frozen install, API BuildSpa target, 14 matching artifact
  hashes, Docker SPA stage, API HTML/assets, and real local guest/create/dashboard/edit/preview flows.
- [Frontend workspace convention](../../../conventions/development/frontend/shapes/app/architecture/workspace.md) now requires
  private pnpm root + apps/web from day one; optional packages and peer apps do not move existing paths.
  Runtime federation remains a separate decision. Conventions/skill/generator changes are uncommitted.
- Actual product-template source now uses Vue/ui-vue 0.0.7 in apps/web. Its typecheck/build, 6 tests, lint/format,
  Docker SPA stage, and independently renamed frozen-install/build/test/deploy fixture pass. Template remains uncommitted.
- [Visual comparison](foreverpin-visual-20260926/comparison.md): 6 matched native screenshots, source hashes and viewport metrics.
  The owner accepted the AppLayout.tsx/index.css candidate; signed commit `59c708b` records it.
  Mobile overflow is gone at 390/360px; computed typography and source contrast checked. Candidate build/typecheck pass.
- Owner-authorized [palette refinement](foreverpin-palette-20260926/comparison.md) applies neutral surfaces, separate
  structural/control borders, readable inactive tabs, and explicit semantic feedback pairs in both modes.
  Signed palette commit `6264a34` contains only this frontend/design batch; concurrent backend work remains separate.
  Typecheck/build and 98 declared contrast pairs pass; matched light/dark/mobile screenshots are retained.
- Managed runtimes remain available for this review: PostgreSQL container `foreverpin-frontend-review-db-20260926`
  on 127.0.0.1:15492; API HTTPS 7020/HTTP 7021 (session 93693); HTTPS Vite 7024 (session 47268).
  These belong to this task; keep them while review continues, stop them when review ends. Do not touch Wheelhouse/Ocharo containers.
- Browser tab 1 is handed off at the disposable edit route. Viewport override reset. Capture metadata identifies the test record.
- The owner confirmed the after palette; `6264a34` is the accepted visual baseline for Vue.
- Implement Vue adoption against published 0.0.7;
  use the audit's correctness/interaction matrix. Do not complete v0.10 until the separate backend lane and owner acceptance finish.

## Prior SDK milestone — 2026-09-26

- Pushed candidate `cbadbd4` reached [release CI](vue-release-20260926.md), which stopped at one Firefox
  iframe-fixture failure (2,100 passed). Reproduced under Linux; the corrected load/activation fixture
  passes all 2,101 tests across 172 files. After explicit index-coordination approval, the one-file correction
  was committed as `8a80db8` with a verified personal GPG signature. All 39 Ocharo staged blobs/modes and remaining
  unstaged tracked work were preserved. The owner pushed the correction; release run `36189754639` matches
  `8a80db8`. Run `36189754639` now passed every gate, including all 2,101 tests and packed-consumer checks.
  Public npm now serves `latest=0.0.7`; registry/tarball hashes, manifest and all 72 exports match.
  The GitHub release/tag resolve to bot commit `3295e9f`, which changes only the Vue manifest version and
  directly follows tested source `8a80db8`. This task did not pull over Ocharo's staged manifest.
- Identity repair complete: the owner [corrected all five commit identities](commit-identity-repair.md)
  to personal Gmail and pinned the repository identity. Original trees, messages and dates match;
  the script reported unchanged index/worktree. The owner pushed the corrected chain.
  Corrected sweep tip is `cbadbd4`; the release-fixture follow-up is `8a80db8`. Other tasks' work remains separate.
- The owner expanded the active pass to the entire Vue SDK, including rewrites and missing reusable capabilities.
  Manual per-component review is optional. React remains parked; QR rendering remains ForeverPin-owned.
- Source baseline is `f4fe5c6477bc83a344e8c10cc4d6467dabf176b8` plus earlier staged readiness changes.
  Release `0.0.7` and its public tarball are independently verified above. Concurrent local manifest edits
  are separate from the published source.
- [Full implementation and coverage](../../../workbench/wow-two-sdk-beta/wow-two-sdk-beta.ui/engineering/architecture/analysis/vue-sdk-optimization/full-sweep-implementation.md)
  records the complete capability pass, API migrations, source-family evidence and remaining proof limits.
- Implemented exact editing/config/flags, session-owned HTTP/query/auth, form identities/validation/native types,
  browser cleanup, localization, focus/menus, display/media/layout fixes and measured class-merge optimization.
- Final combined gates pass: 2,025 unit/DOM/SSR tests; 57 Chromium/forced-colors/WebKit checks; 408 SFCs;
  types, acyclic capability graph, lint/format, library/playground builds, 183 theme contrast pairs,
  seven-family gallery smoke, 72 packed exports and a clean npm tarball consumer with strict Vue templates.
- Firefox's installed runtime cannot launch on this Mac (`sandbox_extension_issue_file_to_process` permission
  failure), even with native escalation. No OS/browser sandbox was weakened. Linux CI matrix includes Firefox;
  the complete hosted matrix now passes. Live OAuth/device permissions and product visuals are not proved by mocks.
- Consumer gzip measurements: Button 27,340→19,920 bytes; Text 22,746→15,089; Card 23,622→15,975.
  Packed gates enforce explicit bundle budgets. HTTP grows to 3,589 bytes with cancellation/metadata contracts.
- User enabled ordinary-commit autonomy for the preceding SDK turn; the scoped switch registered ON.
  The subsequent commit received the generic workspace denial. No commit was created or guard bypassed.
  Verified SDK index contains 445 sweep paths; cached whitespace check passes. The developer publishes.
- [Commit permission repair](commit-permission-analysis.md), September 26: installed one persistent flag per repository.
  OFF remains unchanged. ON survives replies/subagents; a different chat must explicitly reconfirm before committing.
  Exact native user directives own mutations; the helper is read-only. Shared Git conventions and local entrypoints updated.
  All 71 permission/adapter/lifecycle/staging tests pass. SDK/workspace flags remain absent (OFF); no commits ran.
  The former shared-turn state collision was reproduced live while OFF. It fits the earlier failure, but the exact
  historical writer was not journaled; the separate-legacy-hook diagnosis remains unproven.
- September 26 commits complete: [five verified batches](commit-batches.md), `99f832b`, `c405ed1`, `4001b1f`,
  `c094ce6`, `cbadbd4`, cover all 445 reviewed paths. Final committed blobs/modes match the manifest;
  each commit contains exactly its planned paths. Implementation boundaries typecheck; focused tests pass (728 / 372).
- Escaped directive fix installed after explicit approval: the parser accepts the exact Markdown-escaped
  marker spelling and preserves the original native prompt as evidence. All 78 installed permission,
  lifecycle and index tests pass. A fresh native escaped directive enabled SDK commits for this chat;
  all five actual commits succeeded. SDK permission remains ON; workspace permission remains OFF.
- Shared-index coordination: the owner approved temporary Ocharo staging isolation. Two React router files
  joined the original 20 paths before isolation. All 22 exact staged blobs/modes were restored after committing.
  Concurrent Ocharo Vue port changes appeared during this turn, including PointControl and package exports;
  preserve those uncommitted changes. The [batch manifest](commit-batches.json) records the restoration evidence.
- The owner confirmed moving away from React. Vue 3 / strict TypeScript / Vite / Tailwind v4 and `ui-vue` now
  form the [frontend standard](../../../conventions/development/repo/repo-conventions.md#frontend-standard).
  React is legacy maintenance/migration work; new React exceptions require explicit repository-scoped consent.
  Seven convention/entrypoint files were updated and checked; they remain unstaged in the workspace.
  The current Vue starter implementation is recorded above; templates/skills follow the framework standard.
- Unrelated React edits include AlertModal and Ocharo adoption work; all remain outside the Vue sweep.
- The corrected Vue candidate is published. ForeverPin v0.10 adoption is active;
  playground/sandbox/theme-app optimization follows migration.

## Prior sweep evidence

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
- Final combined gate including exact numbers: 93 Node/DOM/SSR files / 1,639 tests, 407 SFCs, full types/lint/format passed on 2026-09-13.
- Library and playground production builds passed. Packed checks passed 72 targets / 64 core JS entries / 68 total JS entries, strict public types, exact numeric behavior and generated consumer CSS.
- Generic hooks retired, capability roles grouped, Result carrier files/names corrected, query/router adapters placed, and visual foundation roots folded into component folders.
- Added row 43 for the final source-role inventory; capability graph checks now run in typecheck.
- Artifact review's smart-qr/text/indicator contrast failures are resolved. All 183 themes pass declared contrast pairs; ForeverPin is an authored candidate awaiting app visual review.
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
- Fourteen case-only filename renames are committed with their intended spelling and no duplicate legacy index paths.
- Current local manifests: React `@wow-two-beta/ui` `0.0.108`; Vue `@wow-two-beta/ui-vue` `0.0.5`.
  Vue npm registry version `0.0.5` was verified 2026-09-12; React registry version was not checked.

---

## Working tree

- Ordinary commit execution follows the current persistent repository switch and confirmed chat.
  The owner activated SDK commits on September 26; five sweep commits are complete.
  Preserve unrelated workspace edits. The owner publishes.

- Root frontend app/library shape docs already had intentional edits; two old frontend handoffs were deleted.
- SDK had 690 status entries, including staged work, at the baseline read.
- This session now owns convention amendments and the Vue implementation lanes listed above.
- Do not restore deleted handoffs, discard earlier changes, or commit the shared staged index indiscriminately.
- Before the optimization pass, the Vue SDK working tree and index were clean. Local commits: `9577d6c` error/logging conventions,
  `3ae7df7` implementation sweep, `0e4aaae` migration/verification docs, `877f022` release gates.
- All release checks passed again, including Chromium and an independent fresh npm consumer.
  Evidence: [final verification](vue-final-verification.md). Nothing has been published by this session.

---

## Resume

1. Read resolution reports; initial analysis findings are historical, not current defects.
2. The owner-requested lossless-number prototype (row 44) is implemented and all gates pass; read its report for API boundaries.
3. React library/release remains parked; all four demo apps are included in the optimization pass. The numeric prototype does not silently migrate all clients or native-number controls.
4. The original conventions sweep is committed. The current Vue batch is verified; commit cohesive batches when
   the native repository switch confirms this chat. The human publishes.
5. The owner can push the SDK commits to run the Vue release workflow; it bumps and verifies the new tarball.
6. Verify registry/tag/release state after publication, and brainstorm the documented follow-ups separately.

## Optimization milestone — 2026-09-13

- Full SDK inventory and core/component/browser/app audit findings are consolidated in the SDK's
  `engineering/architecture/analysis/vue-sdk-optimization/optimization.md`; lane reports and coverage ledgers sit beside it.
- Core ownership/scale corrections, lazy themes, lazy playground groups and all three React app fixes are implemented.
- Final local combined checks: 120 unit/DOM/SSR files, 1,774 passing tests; source/test types, 407 SFCs, lint,
  format, library/declarations/theme build and Vue playground build passed, including supporting-core corrections.
- Exact-number retained heap measured about 83% smaller; default playground JavaScript graph about 79% smaller.
- Latest hosted release failure confirmed at run `34718320600`, commit `efaa23d`: Linux rejected case-only imports
  still recorded with old Git filenames. The prior local `3ae7df7` corrected those names; a new host-independent gate
  catches import/index casing discrepancies. Release recovery, exact-artifact source checks and app smoke gates added.
- The owner executed `/private/tmp/sdk-native-verification.py`: 30 Chromium tests and the full built Vue playground smoke passed.
  React playground/showcase passed; theme-studio had an invalid Playwright style-text selector, now corrected to applied CSS.
  Package cleanup failed on Node 24 directory symlinks; `unlinkSync` replaces `rmSync` and the local packed checks pass.
  The agent reran React app browser checks and fresh installation with manual native approval; both passed.
  `/private/tmp/sdk-native-verification.json` records all four native check groups with exit code 0.
  All SDK changes in this batch belong to the authorized sweep; final verification is complete and commits remain.
- Root backend/hook/convention edits outside this report remain another lane's work. No push or publication occurred.

## Execution permissions — 2026-09-13

- The owner requested unrestricted routine development execution. The active native runtime still uses
  `workspace-write`, restricted networking and automatic approval review; a loopback test server fails with `EPERM`.
- Corrected `.claude/hooks/guard-git.py` argument parsing so chained read-only Git commands remain independent.
  Preserved its pre-existing policy edits. Added synthetic command-boundary regression tests;
  all 27 command-boundary, index-operation and Codex-hook tests passed. This does not prove live hook trust.
- Full access is not a prerequisite for ordinary builds or unit tests. The owner's screenshots show that
  Full access is available in Settings while this chat selects Approve for me. Those settings do not combine.
- A fresh one-shot Node TCP listener on `127.0.0.1` failed with `EPERM` under the default sandbox.
  A single `require_escalated` retry remained pending without an approval or denial; its waiting tool cell
  was terminated. Reviewed app logs did not establish the cause of the missing escalation result.
- Official permission documentation says Approve for me routes eligible boundary-crossing requests to a
  reviewer, with execution continuing on approval; no human popup is expected for those requests.
  Test servers need working escalation in this runtime, not necessarily Full access.
- The owner selected Ask for approval. The identical escalated listener ran successfully, followed by
  the React app browser checks and fresh packed-consumer installation (both exit code 0).
  Manual escalation works without Full access. No native permission setting was changed by the agent.
- The owner switched back to Approve for me. An initial request was explicitly dismissed because its
  owning session ended; the active session resubmitted the scoped Vue browser test command and retained
  the request until execution returned. All 30 Chromium tests passed, and the Vue production build passed.
  Automatic escalation is working in this retry; the earlier internal dismissal cause is not established.
- Restored the workspace commit ban in the Git guard, conventions and active session state.
  All 28 hook tests passed, including Claude/Codex commit rejection and authorized index operations.
- The owner committed the 22-path core batch as `b70ba4c`.
- The owner committed the 62-path state/browser batch as `4283c46`.
- The owner committed the 35-path presentation batch as `5cbb914`.
- The owner committed the 39-path demo-app batch as `b8ea93f`.
- The owner committed the 9-path CI batch as `176e2d2`.
- The owner committed the 4-path supporting-core batch, corrected its message to
  `fix: hardened text formatting and CSS token resolution`, and pushed the replacement `b678a59`.
  The supplied terminal screenshot confirms the exact-lease push succeeded on September 14.
- The owner committed the final 18-path SDK documentation/benchmark batch as `f6c396c`.
  SDK working tree and index are clean, verified September 15.
  Hosted release verification remains open; the analysis separates the older inspected runs from the new push.
  Workspace policy edits remain unstaged.
- September 15 retry: the native tool explicitly dismissed its pending request because the session ended.
  A scoped resubmission succeeded; both GitHub run listing and failed-log reads returned exit code 0.
  App logs confirm this task selected the user reviewer. The missing prompt's internal cause remains unproven.
- Hosted Vue run `34932447116` at `f6c396c` failed before publication: playground theme imports resolved to missing `dist`.
  Reproduced both TypeScript diagnostics and two DOM failures in `/private/tmp/vue-ci-typecheck-340l0ylq/package`,
  a package copy without build output using existing dependencies. Corrected test TypeScript aliases and reused the
  playground's manifest-derived source aliases in Vitest. Clean-output typechecking, 1,774 unit/DOM/SSR tests and
  30 Chromium tests passed. SDK checkout type/capability/SFC gates, ESLint and changed-config formatting passed.
  The three-file SDK correction (two configs plus optimization report) awaits the owner's commit/push.
  Hosted publication, npm version and matching tag remain open. Workspace index was left untouched.
- September 15 approval diagnosis: GitKraken's enabled/trusted `PermissionRequest` hook uses `--blocking` with an
  86,400-second timeout. Its installed code emits the exact dismissal; its CLI log rotates this live task to other
  chat IDs at both dismissal times. The block precedes normal ChatGPT approval routing and affects both reviewers.
  Evidence is in `approval-diagnosis.md`. The owner approved the individual-hook disable; applied
  `/private/tmp/gitkraken-permission-hook.diff` through native escalation and verified `enabled = false` in personal
  hook state. All four workspace config/hook files have no conflicting local override. The global setting needs
  no per-workspace trust renewal and preserves native review, other GitKraken hooks and workspace Git enforcement.
  GitHub reads passed under `auto_review` after the change. Latest hosted run `34934970480` at `2f6aa63` reached
  npm publication after the validation/build/packed-consumer gates. Publishing `@wow-two-beta/ui-vue@0.0.6` failed
  with npm `E404` on PUT to the package URL: resource missing or caller lacks access. Credential identity, package
  rights and token scope still need diagnosis; do not assume the exact cause from E404 alone. No npm publish or
  matching version/tag completion was established. SDK worktree/index are clean.
- Release authentication follow-up: every validation/build/playground/packed-consumer/source step in run
  `34934970480` succeeded; only npm publication failed. Its publish-step environment contains masked
  `NODE_AUTH_TOKEN: ***`, establishing a supplied value, not its validity or publish permissions. Public npm
  metadata still reports `@wow-two-beta/ui-vue` latest `0.0.5`, maintainer `sulton-max`.
  `gh secret list` was executed successfully through native escalation but GitHub returned HTTP 403 for the
  CLI credential's secret-metadata permissions. This is a GitHub authorization limit, not a sandbox block.
  Opened the package access page in Arc; it redirects to npm Sign In. Owner sign-in is needed to inspect
  publishing settings/token permissions. No credential value was read, no registry setting changed.
  npm's documented trusted publishing is an alternative to rotating tokens; it requires package-side trust
  for `wow-two-sdk-beta/wow-two-sdk-beta.ui`, workflow `release-vue.yml`, plus workflow OIDC permission.
  Authentication migration was not applied at that point; superseded by the preparation below.
- Signed-in npm inspection confirmed `sulton-max` has write access and the sole listed `npm-token` expired
  August 18, 2026 (last used August 13). Package read/write and bypass-2FA were enabled. Exact equality with
  GitHub `NPM_TOKEN` remains unverified, but no active token exists in this account.
  Prepared and staged `.github/workflows/release-vue.yml` plus the SDK optimization report for trusted publishing:
  job-scoped OIDC permission, no stored npm token/placeholder npmrc, explicit public registry, same tested tarball.
  YAML, every shell step syntax, three version-helper tests and staged whitespace checks pass.
  Proposed message: `fix: migrated Vue releases to npm trusted publishing`.
  No package-side trust or other npm setting changed; owner confirmation is still required to grant direct
  publishing to `wow-two-sdk-beta/wow-two-sdk-beta.ui` workflow `release-vue.yml`, environment empty.
  In-app browser package-settings navigation hit `ERR_TOO_MANY_REDIRECTS` after successful token inspection.
  System Git is blocked by an unaccepted Xcode license; the installed Codex fallback Git performed index work.
  No license accepted, commit or push executed. Root index preserved. Human should configure trust before push.
- Owner pushed the trusted-publishing change and explicitly approved the exact package-side grant above.
  Hosted run `34998940096`, head `ed07e96ba08f003286956b9a4c47201d5f43fd5c`, was in progress on verification.
  Grant remains unapplied: existing and fresh in-app npm tabs hit the login redirect loop; Arc navigation was
  interrupted by user control. Do not ask again for authorization for this same grant. Recover signed-in
  package settings, add the approved publisher, verify the saved configuration, and inspect the hosted run.
- Superseding release state: npm saved the approved OIDC trusted publisher for
  `wow-two-sdk-beta/wow-two-sdk-beta.ui`, workflow `release-vue.yml`, label `Vue release`, with direct
  `npm publish` and `npm stage publish` permissions. The package remains public at `0.0.5` until the owner
  reruns the failed release; agents do not initiate publishing under the workspace Git policy.
- Release closed September 19: the owner reran failed jobs for run `34998940096`; attempt 2 passed every
  validation, build, browser-smoke, packed-consumer and source gate. npm published public
  `@wow-two-beta/ui-vue@0.0.6` through the saved OIDC publisher with signed provenance. Release commit
  `e2ca132`, tag `ui-vue-v0.0.6` and the matching GitHub release exist. A fresh-cache `npm pack` retrieved
  the public artifact with integrity `sha512-n14JnUL46s4VZljI8qZkn8uEoBbmPHAoN2cXhrKFWz9qCX7yhXbPN/Xt59hgXM/OPsl3LGXRbc+AnV9PwhQRLA==`.

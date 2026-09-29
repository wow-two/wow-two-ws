# ForeverPin: finish v0.9 or adopt Vue first?

*Reviewed: 2026-09-26*

## Recommendation

Adopt Vue before completing the remaining React UI. Re-scope v0.9 to the implemented internal milestone,
with the owner's explicit acceptance, and make the next version an SDK adoption version. Keep unfinished
feature work in the backlog for the next feature version. Do not describe this internal milestone as a
public-ready release, and do not defer existing security or data-integrity defects behind UI polish.

This is a proposal only. The product's version status, iteration checkboxes, source, index and Git history
were not changed. The application migration has not started.

## Current evidence

- Product checkout: `341d0a92296b73035797ac59f2e9dedadc79bcc0`, plus existing routing/deployment changes.
- The index is empty. Eight tracked files are modified; four files are untracked. These belong to existing work.
- [v0.9](../../../workbench/ventures/10x-venture-forever-pin/engineering/planning/version-track/v0.9/v0.9.md)
  has 22 checked and 41 unchecked rows, including five manual verification rows. Counts describe the plan,
  not independently verified capabilities or remaining implementation estimates.
- The frontend still uses React 19 and `@wow-two-beta/ui@0.0.97`.
- There are 132 TypeScript/TSX source files, including 49 TSX files, 15 raw `fetch` calls and nine files
  with React state/effect flows. This is a framework and integration migration, not a package-number change.
- The sole frontend test file contains four content-default/catalog tests. It does not establish builder,
  pointer, copy, session, preview or route correctness.
- Vue SDK `0.0.7` is public and `latest`, independently verified at `2026-09-25T21:55:54.998Z`.
  Its tarball matches the registry SHA-1/SHA-512, contains all 72 export mappings and 140 unique targets,
  and matches the tested release source. [Artifact evidence](/private/tmp/ui-vue-0.0.7-verification.json).
- Existing [Vue readiness inventory](../../../workbench/wow-two-sdk-beta/wow-two-sdk-beta.ui/engineering/architecture/analysis/forever-pin-vue-readiness.md)
  maps every currently used UI root to Vue. Its older `0.0.6` version and test counts are historical;
  the subsequent full sweep and verified `0.0.7` release supersede that baseline.
- Backend runtime/testing pins remain `10.0.45-beta` / `10.0.40-beta`. The
  [backend adoption plan](../../../workbench/wow-two-sdk-beta/wow-two-sdk.backend.beta/engineering/research/foreverpin-adoption/foreverpin-adoption.md)
  targets the published `10.0.58-beta` family. A fresh GitHub query still returns `v10.0.58-beta` at
  `546466ef67e0b8c5ba1ad01957052c682b2c447f` as the newest tag. NuGet contents were not re-downloaded here.
- Backend SDK working HEAD `94b32a9` contains later data-session/HTTP work. That code is not proven to be
  in the tagged `.58` release. Do not block Vue on this new framework or silently compile against local SDK
  source while claiming published-package adoption. Freeze an actually published backend cut separately.

This review refreshed source and planning evidence. It did not rerun the product's old 213-backend/four-frontend
test baseline, start runtimes, or reproduce the September 19 HTTP probes. Previously reproduced defects are
called current only where their mechanisms remain visible in current source.

## Why not finish the whole current version first?

The remaining Copy dialog, control explanations and rule-layout work would be implemented against React
components, then immediately rewritten for Vue slots, model events and form bindings. Model and server-state
cleanup also overlaps the new SDK's HTTP, auth, query, router, config, exact-value and Temporal boundaries.

The current builder binds the entire union twice, including a falsely narrowed conditional-row binding.
The Vue SDK already supports guarded discriminated array branches. Replacing this while migrating is useful;
building a second temporary React abstraction is not a migration prerequisite.

The backend also needs adoption independently of Vue. Completing backend work against obsolete SDK contracts
would repeat changes already planned for rendering, identity, JSON, validation and error handling.

However, moving every unchecked task into a distant feature backlog would conceal real defects. The migration
acceptance criteria must include existing flow correctness, and public release must retain all safety gates.

## Every unfinished iteration

The rows below account for all 41 unchecked tasks. “Adoption” is the proposed next version; “Feature” means
the next feature cut after adoption. Neither label changes today's version plan.

| Current area | Open rows | Disposition and acceptance |
|---|---:|---|
| Iteration 1: resolve host, per-type path, geo | 3 | Feature. Set the delivery matrix before adding non-URL pages/actions. These decisions do not block a local Vue migration. Unsupported delivery must not be presented as working. |
| Iteration 1: mobile-app and geo preset design | 2 | Later feature backlog. Neither abstraction is required to port existing controls or fix direct URL selection. |
| Iteration 1: version-history seam | 1 | Later feature backlog. Preserve existing stored content; do not build unused history infrastructure during adoption. |
| Iteration 1: pointer scan attribution | 1 | Settle when verifying routing/analytics semantics. Preserve current target-order behavior during adoption; explicitly distinguish that policy from the reorder defect. |
| Iteration 3: polymorphic conditions | 1 | Later feature backlog. Preserve the current enum/value wire contract. Country lookup remains separately unimplemented. |
| Iteration 8: member naming and DTO names | 2 | Adoption, alongside the models being touched. Keep wire-field names compatible; frontend names need not mirror backend value-object suffixes. |
| Iteration 8: reported calendar defect | 1 | Characterize during adoption. Existing fixtures do not prove the report; obtain a failing payload/round-trip case before changing encoding or timezone meaning. |
| Iteration 9: one Copy action, target dialog, legality in dialog | 3 | Feature, implemented once in Vue. Preserve existing supported copy behavior during adoption and reject illegal copies. Multi-rule-to-static selection remains product behavior, not an automatic conversion. |
| Iteration 9: static Add-rule prohibition | 1 | Adoption correctness. Enforce in the Vue UI and against persisted mode in the server; require API and browser regressions. |
| Iteration 9: builder explanation popovers | 1 | Feature. No dependency blocks migration. |
| Iteration 9: discriminated `FieldArray` | 1 | Adoption. Consume the SDK's guarded union branches and stable row identities; do not reproduce the existing unsafe narrowing. |
| Iteration 9: unified single/multiple-rule layout | 1 | Feature. Keep functional parity and accessible controls during adoption; postpone optional redesign. |
| Iteration 10: async reads, entity gates, validation ordering and service-level validation | 4 | Backend adoption/correctness. Authenticate, load and authorize before deeper update checks. Use an actually published contract; do not make the full future data-session design a prerequisite for Vue. |
| Iteration 10: static update invariant | 1 | Adoption correctness. Validate the loaded entity's mode and reject extra rules through the API. |
| Iteration 10: concurrency and unique short links | 2 | Backend correctness accompanying adoption. Test plan-cap races, bounded slug collision recovery and conflicting updates. A row token alone does not serialize concurrent inserts under an owner's cap. |
| Iteration 10: empty payload fallback | 1 | Adoption correctness. Encode static URL/mobile-app content explicitly; reject absent/unsupported payloads. Verify decoded SVG/PNG output, not merely HTTP success or file presence. |
| Iteration 10: `SlugPlaceholder` and SDK render request | 2 | Backend adoption. Keep product mode/rule-to-payload mapping local; consume the published renderer's actual request/result contract. |
| Iteration 10: per-domain `CodeService` | 1 | Conditional. Extract only if it owns the selected validation/write flow; the class name itself is not a release gate. Avoid refactoring once before and again during SDK adoption. |
| Iteration 11: print-ready vector and sizing guidance | 2 | Existing SVG/PNG download is already implemented. Verify format/payload safety during adoption; finish print guidance and physical scanning in the later Feature/acceptance pass. Do not rebuild export from scratch. |
| Iteration 12: test/style camelCase converters | 2 | Backend adoption. Preserve existing persisted JSON and enum tokens through corpus tests; replace obsolete converter recipes with the final SDK serialization contract. |
| Iteration 13: dynamic content retrieval and device actions | 2 | Feature. Implement the agreed delivery matrix on the chosen host. Directly redirecting arbitrary encoded text remains a release defect, not an acceptable placeholder. |
| Iteration 13: stale E2E name | 1 | Reconcile with the existing routing lane during adoption. Current tests use real destination names; avoid changing an obsolete example without checking the owned diff. |
| Manual verification | 5 | Redistribute to the capability's acceptance step. Migration verifies preserved create/edit/copy and routing flows; new delivery and physical print checks follow their implementation. Only the owner closes manual checks. |

Iterations 2, 4, 5, 6 and 7 have no unchecked rows. Their checked status does not override known defects
in static payloads, update invariants or delivery. Existing implementation is the starting point, not proof
that all ten content types work end to end in both modes.

## Correctness that must stay visible

These are not all represented by the current version's checkboxes. Keep the existing
[gap analysis](../../../workbench/ventures/10x-venture-forever-pin/engineering/research/gap-analysis-2026-09-19.md)
as their source, and carry the relevant acceptance criteria into adoption.

| Area | Current mechanism | Required boundary |
|---|---|---|
| Guest identity | Old SDK ownership still consumes the old guest identity contract. | Adopt authenticated guest cookies; prove tamper rejection, claiming and key persistence. Coordinate browser auth/CSRF requirements. |
| Static payloads | URL/mobile encoders return no payload; mapper substitutes an empty string. | Correct before treating default create/export as working. |
| Dynamic routing | Dirty routing change fixes URL only; mobile and non-URL paths remain incomplete. | Direct HTTP(S) URL/mobile behavior must work; restrict unsupported delivery until implemented. |
| Static updates | Update validation lacks the persisted mode; UI allows another rule. | Enforce the same mode invariant server-side and in the migrated builder. |
| Pointer identity | Submit normalization renumbers conditionals without remapping `targetOrder`. | Preserve logical target through reorder, insert, remove, edit and copy. SDK row identity alone cannot repair this product mapping. |
| Write limits | Count and insert are separate; slug allocation is a separate race. | Database-backed invariants and forced-concurrency/collision tests. |
| Rendering | Old renderer integration and raw SVG DOM insertion remain. | Adopt input safety/format guarantees and explicitly establish the preview trust boundary. |
| Startup | React root awaits an unbounded config fetch. | Bounded loading, timeout, retry and visible failure in the Vue bootstrap. |
| Paid entitlements | Retained plan is used without sufficient provider-state policy. | Release gate before enabling paid subscriptions, not a prerequisite for local Vue work. |
| Scan analytics | Event insertion and counter updates are separate; queued batches can be lost. | Test atomicity and bounded shutdown handling; keep durable analytics as a separate product decision. |
| Operations | Dirty deployment changes and old local evidence do not certify a hosted release. | Commit/verify the owned release candidate, health, real providers, backups and scan behavior before public launch. |

## Proposed version handling

1. Owner accepts a reduced internal v0.9 milestone. Move unimplemented tasks intact into the backlog;
   leave no false completion ticks. Re-evaluate checked capabilities against the declared reduced scope.
2. Plan `v0.10` as Adoption: backend contracts and Vue application migration. Work can use disjoint
   backend/frontend lanes, but browser identity, error paths, numeric/Temporal contracts and persisted content
   require one coordinated acceptance cut.
3. Keep new Copy UX, explanations, dynamic content pages/actions and print guidance in the backlog for
   the next Feature version. Do not create another active feature plan prematurely.
4. Retain marketing, paid launch, custom domains, analytics expansion, presets, condition redesign and
   static version history outside this adoption cut unless explicitly selected later.

The existing `v0.11` folder is an explicitly parked hero experiment, not the next active release. Before
assigning that number to real feature work, relocate/reconcile its experiment record without losing tasks.
The unrecorded `v0.8` reservation is not a delivered adoption version.

The existing local instructions exclude migration from the old product lane. A decision to activate the
new adoption lane should update those stale scope statements together; it is not permission to overwrite
another task's dirty routing/deployment files. Ordinary commits need this repository's own switch.

## Adoption acceptance

- Build/typecheck/tests pass for the Vue app and every backend project, using published packages.
- Baseline fixtures preserve stored rules/style, content discriminators, enum tokens and Temporal values.
- Owner identity, claiming, logout and stale-session cancellation behave consistently across both hosts and UI.
- Create, list, edit, copy, rule reorder, preview and downloads receive product-level regression coverage.
- Static URL/mobile output is decoded; PNG bytes and MIME agree; unsupported delivery fails explicitly.
- Failed and superseded previews cannot overwrite current state; bootstrap cannot hang on an empty root.
- Both hosts and the built SPA pass the existing PostgreSQL/Docker verifier plus the missing correctness cases.
- The owner verifies `smart-qr` visuals and manual product flows. QR rendering remains product-owned.
- New feature acceptance, public deployment, real provider flows and physical scans remain separately visible.

## Source anchors

Paths below are relative to the ForeverPin repository unless stated otherwise.

- `engineering/planning/version-track/v0.9/v0.9.md:18`: outstanding design choices.
- `engineering/planning/version-track/v0.9/v0.9.md:87`: remaining model tasks.
- `engineering/planning/version-track/v0.9/v0.9.md:95`: builder/copy tasks.
- `engineering/planning/version-track/v0.9/v0.9.md:112`: validation/write tasks.
- `engineering/planning/version-track/v0.9/v0.9.md:129`: print, converters, delivery and manual tasks.
- `engineering/planning/version-track/version-track.md:5`: active v0.9 and parked hero distinction.
- `engineering/codebase/forever-pin.frontend-services/package.json:22`: current React SDK pin.
- `engineering/codebase/forever-pin.frontend-services/src/presentation/codes/routing/components/RuleControls.tsx:56`: union narrowing and reorder.
- `engineering/codebase/forever-pin.frontend-services/src/presentation/codes/routing/components/RuleControls.tsx:87`: unguarded Add-rule action.
- `engineering/codebase/forever-pin.frontend-services/src/application/codes/createCodeForm.ts:191`: order normalization and immutable-mode omission.
- `engineering/codebase/forever-pin.frontend-services/src/presentation/codes/common/listCodes/screens/CodesListScreen.tsx:204`: opposite-mode copy action.
- `engineering/codebase/forever-pin.frontend-services/src/presentation/codes/common/createCode/views/PreviewView.tsx:106`: existing SVG/PNG downloads.
- `engineering/codebase/forever-pin.frontend-services/src/presentation/codes/common/createCode/components/QrPreview.tsx:103`: SVG DOM insertion.
- `engineering/codebase/forever-pin.frontend-services/src/bootstrap/main.tsx:12`: startup waits for runtime config.
- `engineering/codebase/forever-pin.frontend-services/tests/domain/codes/content/operations.test.ts:9`: existing frontend test scope.
- `engineering/codebase/forever-pin.backend-services/ForeverPin.Tests.E2E/ForeverPin.Tests.E2E.csproj:20`: old backend family pins.
- `engineering/codebase/forever-pin.backend-services/ForeverPin.Domain/Codes/Rules/CodePayloadMapper.cs:28`: empty static payload fallback.
- `engineering/codebase/forever-pin.backend-services/ForeverPin.Redirect.Api/Infrastructure/Routing/RoutingService.cs:52`: partial URL fix and generic redirect fallback.
- `engineering/codebase/forever-pin.backend-services/ForeverPin.Application/Codes/Core/Validators/CodeUpdateCommandValidator.cs:24`: missing persisted mode.
- `engineering/codebase/forever-pin.backend-services/ForeverPin.Infrastructure/Codes/Core/CommandHandlers/CodeCreateCommandHandler.cs:35`: quota and slug write races.
- `engineering/codebase/forever-pin.backend-services/ForeverPin.Persistence/Configurations/CodeEntityConfiguration.cs:22`: existing unique slug index.
- `engineering/codebase/forever-pin.backend-services/ForeverPin.Infrastructure/Billing/CommandHandlers/BillingWebhookCommandHandler.cs:47`: entitlement state handling.
- `engineering/codebase/forever-pin.backend-services/ForeverPin.Redirect.Api/Infrastructure/Analytics/ScanFlushBackgroundService.cs:74`: scan/counter write boundary.
- SDK `engineering/codebase/wow-two-front-vue-beta-sdk/src/formsEngine/AppForm.spec.md:27`: guarded union branches.
- Workspace `conventions/planning/version-track/version-track.md:20`: Feature/Adoption types and owner-controlled lifecycle.

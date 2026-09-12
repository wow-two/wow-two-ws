# Frontend conventions sweep analysis

*Last updated: 2026-09-09*

> Full review of the 363 frontend convention documents, reconciled against the existing SDK sweep.
> Verdict: the conventions are not a settled migration target yet. Correct behavioral contradictions and factual premises
> before expanding the SDK rename/refactor campaign.

## Status

- [x] Read all frontend convention documents, including current uncommitted app/library changes.
- [x] Compare findings with the existing SDK task IDs and completed entries.
- [x] Verify disputed platform claims against primary documentation and bounded local reproductions.
- [x] Record missing convention work and downstream SDK verification tasks.
- [x] Finish the convention amendments and validate their examples.
- [ ] Complete the selected SDK package sweep and its full validation.
- [ ] Publish and verify the selected package version.

The user permits radical SDK changes and confirms no production consumers. Compatibility shims are not a default requirement.
The active package is Vue, confirmed 2026-09-10. React implementation and release are parked.

---

## Coverage and evidence

| Area | Files | Evidence |
|---|---:|---|
| Language, React, Vue, HTML, CSS, Tailwind and notation | 65 | [Baseline analysis](lla-analysis.md) |
| Component application conventions | 242 | [Components analysis](components-analysis.md) |
| Visual, behavior, data and compound constructs | 27 | [Components analysis](components-analysis.md) |
| Capability domains | 16 | [Domains and shapes analysis](domains-shapes-analysis.md) |
| App and library shapes | 9 | [Domains and shapes analysis](domains-shapes-analysis.md) |
| Frontend index and scope leads | 4 | [Baseline analysis](lla-analysis.md) |
| **Total** | **363** | [Snapshot hashes and checks](coverage.json) |

The separate [SDK baseline](sdk-baseline.md) verifies package ownership, selected old counts, local versions,
instruction conflicts and release plumbing. It is not a claim that all SDK source has been semantically audited.

Relative Markdown file links resolve across the full tree. Explicit fragments passed a heading-slug check.
Prose section references still contain stale targets, and link resolution does not prove the linked rule agrees.
The lexical duplicate check found 25 repeated directive-line candidates, including templates; semantic findings below
do not treat that raw number as a defect count.

---

## What the sweep must preserve

- Keep the two orthogonal cuts: scope under `core/`, deliverable under `shapes/`.
- Keep one owner per rule and instance-specific API documentation beside the SDK implementation.
- Keep explicit opt-in wiring, component composition and inward application dependencies.
- Keep kind-based naming where the gate yields a stable role; settle exceptions before automated renaming.
- Keep framework-specific implementations of shared contracts; a React callback is not a Vue emit spelling.
- Keep intentional decisions distinct from claims about what TypeScript, browsers or frameworks can do.
- Keep existing completed work and task IDs. Reopen only a concrete incomplete acceptance criterion.

---

## Convention amendments — resolved 2026-09-10

The checkboxes below track rule amendments, not SDK implementation. Evidence lives in
[LLA resolution](lla-resolution.md), [component resolution](components-resolution.md) and
[domain/shape resolution](domains-shapes-resolution.md). Endpoint-specific exact decimal/int64
representation remains a backend coordination question; the convention requires explicit lossless contracts.

These checkboxes are the convention work queue. SDK implementation remains in its existing sweep document.
Each task closes only when its owning rules agree and a representative example passes the relevant check.

### C01 — restore the scope and ownership boundaries

- [x] Use the shape's subject-existence test consistently; replace `core.md`'s stale change-with-deliverable test.
- [x] Move app bootstrap paths, library import constraints and stylesheet placement out of universal notation.
- [x] Reconcile product and library role-group rules, including singleton-flat exceptions.
- [x] Reconcile library story placement with the central SDK structure owner.
- [x] Resolve application-to-integration dependency direction and route parameter ownership.
- [x] Separate product extraction triggers from the SDK's proactive vector-completeness pass.
- Evidence: baseline L6; domain/shape evidence. Scope, path placement and dependency direction are separate questions.
- Close when an app and a library each have an unambiguous source/test/style layout without mutual exceptions hidden elsewhere.

### C02 — settle component taxonomy and composition before renaming

- [x] Reconcile broad kind composition limits with the components that legitimately compose other kinds.
- [x] Resolve the pure-layout duplication conflict against the central extract/keep/remove convention.
- [x] Resolve trailing modifiers, shape words, compound subparts and primitive exceptions in the suffix gate.
- [x] Classify by intended responsibility, not by an accidental omission in today's props.
- [x] Permit simple single-domain pages and views without a second interchangeable implementation.
- [x] Resolve layout chrome, feedback/state replacements and compound-owned versus caller-slot composition.
- Evidence: components analysis; existing SDK rows 7 and 25.
- Close when each current component root maps to a kind or a documented exception and the rename map is deterministic.

### C03 — define one controlled-state and native-attribute contract

- [x] Define controlled/uncontrolled mode, seed-only initialization, clear values, resets and update payloads.
- [x] Give React and Vue their own spellings without requiring both legacy aliases indefinitely.
- [x] Resolve standalone booleans, forwarded native flags, field inheritance and callback-presence behavior.
- [x] Replace the required-`open` uncontrolled example with a type-correct example.
- [x] Define composite/fused fields: group naming, multiple label targets, draft text and multipart values.
- [x] Cover composition events, paste, caret preservation and autofill for bespoke controls.
- Evidence: baseline L9 and component application rules; the no-production-consumers instruction permits deleting redundant aliases.
- Close with controlled, uncontrolled, clear, external-update, disabled and form-reset examples for each supported framework.

### C04 — distinguish modal, navigation and provider behavior

- [x] Restrict focus trapping to modal interaction; nonmodal popovers/tooltips/hover cards need their own policy.
- [x] Restrict roving focus to composite widgets; ordinary navigation links retain normal tab behavior.
- [x] Distinguish required providers from optional providers with documented fallback behavior.
- [x] Resolve contradictory Drawer/BottomSheet selection rules.
- [x] Define host uniqueness per app/capability/request and reactive provider replacement.
- Evidence: overlay versus HoverCard, nav versus Breadcrumb, provider versus i18n/flags in components analysis.
- Close when each family states who owns focus, dismissal, keyboard navigation and fallback behavior.

### C05 — complete the accessibility contract

- [x] Correct the ring-only forced-colors recipe and verify an outline survives.
- [x] Separate heading hierarchy from programmatic landmark naming.
- [x] Separate generated reusable IDs from caller IDs and stable document fragment targets.
- [x] Add keyboard alternatives to pointer/drag operations, focus restoration and nested-overlay behavior.
- [x] Require an advertised keyboard exit from editors that intercept Tab.
- [x] Require persistent pause/stop controls where continuous motion needs them; hover pause is insufficient.
- [x] Define route announcements, route focus, page language/direction and form error announcements.
- [x] Define zoom/reflow, long-label, reduced-motion, contrast and forced-colors verification responsibilities.
- Evidence: baseline L1/L8; component interaction findings; the existing index already acknowledges incomplete accessibility coverage.
- Close with rendered browser checks and manual keyboard/screen-reader checks where automated checks cannot establish behavior.

### C06 — align transport and failure contracts

- [x] Set lossless policies for large integers, decimal values, timestamps, date-only values and durations.
- [x] Parse by declared field schema rather than by recognizing date-like strings anywhere in a payload.
- [x] Align validation-error member names with the actual backend contract.
- [x] Define where `Result` values are adapted to third-party query rejection semantics and back.
- [x] Reconcile DTO location and null/omission rules without losing explicit clear operations.
- [x] Specify codecs for Map/dictionary and duration values; verify backend serialization fixtures.
- [x] Separate live hook state from operation outcomes; keep third-party Standard Schema result shapes intact.
- [x] Model empty HTTP responses without casting `undefined` into an arbitrary success type.
- Evidence: domain/shape analysis and model findings; expands SDK rows 12–14.
- Close with wire fixtures covering precision limits, null/omission/clear, unknown enum values, cancellation and field failures.

### C07 — define form parsing and asynchronous submission behavior

- [x] Separate editable raw values, parsed schema output and submitted request values.
- [x] Define current-step versus final wizard validation and draft/autosave validation.
- [x] Define race handling, double-submit prevention, cancellation and stale server-error clearing.
- [x] Define autosave coalescing and trailing edits so in-flight saves cannot silently discard newer input.
- [x] State the provider-free contract and isolate React/Vue form adapter wiring.
- Evidence: domain/shape analysis; existing form docs cover engine selection and chrome but leave these seams inconsistent.
- Close with transformation, wizard, autosave, reset and out-of-order response examples.

### C08 — correct framework premises and lifecycle guarantees

- [x] Correct the client-action, context deprecation, transition-class and function-ref claims.
- [x] Qualify root exposure removal; `$el` is not a universal element handle.
- [x] Add render purity, hook/dependency rules, cleanup, stale async response and Strict Mode expectations.
- [x] Keep house API preferences explicit; do not reverse every ban merely because its rationale was wrong.
- Evidence: baseline L3/L4 and missing lifecycle coverage; expands SDK rows 9 and 17.
- Close when the modernized ref/provider APIs preserve their functional contract in representative nested components.

### C09 — correct CSS/Tailwind facts and bounded layout defaults

- [x] Correct important-modifier compatibility, arbitrary-value merging and custom-utility merging rules.
- [x] Define a deliberate button cursor policy for Tailwind v4.
- [x] Reconcile one-column responsive grids, semantic calendar grids, static centering and flex/grid z-index.
- [x] Reconcile duration/easing defaults and focus versus focus-visible exceptions.
- [x] Separate theme token declaration, application overrides and library stylesheet delivery.
- Evidence: baseline L2/L7; [local reproductions](reproductions.json).
- Close with generated CSS and class-merging checks, plus responsive and reduced-motion examples.

### C10 — correct TypeScript guarantees and closed-value modeling

- [x] Distinguish erased readonly typing from runtime freezing.
- [x] Distinguish array syntax preferences from mutability and allow intentional internal mutable collections.
- [x] Correct namespace/ambient-enum `isolatedModules` claims.
- [x] Scope camelCase wire values to house vocabularies; preserve external protocol and DOM spellings.
- [x] Keep runtime input validation separate from a DTO's static type.
- Evidence: baseline L5; enum and type-mapping owners.
- Close with compile-time and runtime counterexamples demonstrating the actual guarantees.

### C11 — finish locale, time and capability lifecycle boundaries

- [x] Define default locale, caller strings, pluralization, RTL behavior and locale changes for both frameworks.
- [x] Align Temporal/date/time controls with one value contract and a browser/polyfill policy.
- [x] State cleanup for subscriptions, observers, timers, object URLs, streams and cancellable asynchronous work.
- [x] Preserve explicit opt-in registration and identify optional-provider defaults.
- Evidence: both component and domain analyses; several date/time docs already record spec/source mismatch.
- Close with locale switching, date-only/timezone fixtures and repeated mount/unmount behavior.

### C12 — write the frontend testing and compatibility conventions

- [x] Define unit, DOM, browser, interaction/demo and packed-consumer responsibilities.
- [x] Define the supported runtime/browser baseline and feature-detection/fallback rules.
- [x] Distinguish safe package import without DOM from complete SSR/hydration support.
- [x] Require test discovery and representative behavior; empty or skipped projects are not coverage.
- [x] State which checks close each sweep row and which behavior still needs review.
- Evidence: frontend index `Open`, domain/shape analysis and SDK baseline.
- Close when a new component, capability and breaking refactor each have an executable acceptance path.

### C13 — write the library delivery contract

- [x] Specify public exports, declarations, CSS/theme assets, optional peers and dependency isolation.
- [x] Require every advertised runtime/type export to exist in the packed artifact.
- [x] Require import smoke tests from an isolated consumer of that artifact.
- [x] Specify release validation, version/tag ownership and partial-publication recovery.
- Evidence: library delivery is explicitly unwritten; the Vue baseline finds four stale export sources after folder moves.
- Close only when a build cannot silently omit an advertised export and the selected package can be consumed from its tarball.

### C14 — finish app platform, assets and security boundaries

- [x] Define image/font/public asset handling, bundler paths, base paths and cache behavior.
- [x] Define build inputs and lockfile handling for reproducible SPA artifacts.
- [x] State trusted rendering/URL boundaries, authentication versus authorization, persistence boundaries and error redaction.
- [x] Cover public build variables, auth redirects/CSRF, logout cleanup, upload validation authority and analytics consent.
- [x] Link shared deployment/security owners where available instead of cloning their rules into frontend docs.
- Evidence: explicit static-asset/build gaps and domain/shape findings.
- Close with focused build/cache/asset examples and testable trust boundaries, without expanding into backend implementation.

### C15 — make the conventions maintainable and executable

- [x] Remove implementation counts, port history and current SDK deficiencies from normative rules.
- [x] Move instance props/defaults to code-adjacent specs; keep selection guidance in conventions.
- [x] Repair prose section pointers, React/Vue import grouping and omitted application-layer ordering.
- [x] Align the document template with its actual permitted sections; fix malformed tables and self-failing examples.
- [x] Give each obligation one owner and link repeats; preserve distinct rules in independent vectors.
- Evidence: all three analyses. Existing SDK spec coverage/accuracy rows 8 and 27 remain separate implementation work.
- Close with links, representative compiled/rendered examples and semantic duplicate review; formatting alone is insufficient.

---

## Evidence-to-task traceability

Finding IDs belong to their evidence document; they are not SDK sweep IDs. The consolidated C01–C15 tasks above
are the implementation queue. Multiple findings can close together when they share an owning contract.

| Evidence | Finding IDs → consolidated tasks |
|---|---|
| Baseline analysis | L1→C05; L2→C09; L3→C08; L4→C08; L5→C10; L6→C01; L7→C09; L8→C05; L9→C03; L10→C15 |
| Components analysis | C01→C15; C02→C02; C03→C02; C04→C03; C05→C03; C06→C02; C07→C04; C08→C04; C09→C05; C10→C06; C11→C06; C12→C02; C13→C02; C14→C15; C15→C03/C08; C16→C04/C11; C17→C03/C05/C11; C18→C02/C05; C19→C15 |
| Domains and shapes analysis | D1→C06/C10; D2→C06; D3→C07; D4→C07/C08; D5→C01; D6→C01; D7→C14; D8→C08/C11/C12; D9→C05/C11; D10→C12/C13/C14; D11→C15 |

---

## Existing SDK work: preserve and extend

| Existing row | Disposition |
|---|---|
| 7 — component groups | Keep; apply C02/C04 before moving components. |
| 8 — missing specs | Keep; refresh the component denominator and settle the local instruction override. |
| 9 — React 19 forms | Keep as React-owned; validate behavior, not only a zero-token grep. |
| 11 — Screen to Page | App-owned; do not silently include smart-qr edits in the SDK package sweep. |
| 12–14 — Result and HTTP | Keep; expand to query adapters, cancellation and backend error fixtures under C06. |
| 17 — Vue root exposure | Keep as Vue-owned; validate root/imperative consumers under C08. |
| 18 — demo coverage | Keep; zero stories does not mean zero demos. Build a component-to-demo inventory. |
| 22 — folder casing | Keep; remeasure by package and include export/build/test references in acceptance. |
| 23 — live Vue props | Narrative still open outside the table; give the three sites an explicit current disposition. |
| 25 — kind suffixes | Keep; derive names after C02, including compound and modifier exceptions. |
| 26 — capability folders | Keep; use role/subject ownership rather than lexical noun replacement alone. |
| 27 — stale specs | Keep; match each spec to current source and intended API. |
| 30 — ARIA constants | Keep; distinguish code extraction from template-only names and actual ARIA behavior. |

Additional SDK work is appended as rows 31–42 in the
[existing sweep](../../../workbench/wow-two-sdk-beta/wow-two-sdk-beta.ui/engineering/planning/ui-sdk-conventions-sweep.md),
linked to these convention tasks.
Old counts remain historical unless the [SDK baseline](sdk-baseline.md) explicitly remeasured them.

---

## Execution and release acceptance

1. Correct the behavioral contracts and false technical premises before mass source changes.
2. Complete the missing convention owners; resolve code-adjacent spec/instruction conflicts.
3. Apply the resulting rules to the selected SDK package in disjoint areas; remeasure each row.
4. Run that package's typecheck, lint, formatting where configured, complete tests and build.
5. Inspect the packed artifact and compile/import it in a separate consumer fixture.
6. Check the selected registry version and the release workflow, publish, and verify npm, tag and release independently.

The current release workflows publish before committing/tagging the version bump. A publication success does not prove
the tag or repository version updated. Both must be checked at release time.

Large staged and unstaged SDK changes already exist. Preserve them, establish which files the sweep owns, and avoid
committing the shared index as though this analysis authored it. No source changes or release actions were performed here.

---

## Review limits

- Full conventions reading is complete; this is not proof that the resulting policy covers every possible future feature.
- Findings distinguish confirmed contradictions, verified factual errors, explicit known gaps and proposed missing contracts.
- The report does not automatically authorize inventing new SDK capabilities absent from the product/SDK roadmap.
- Framework/browser facts cite primary sources in the evidence documents. House choices still need coherent stated intent.
- No production consumers reduces migration constraints; it does not remove package correctness or behavioral acceptance checks.

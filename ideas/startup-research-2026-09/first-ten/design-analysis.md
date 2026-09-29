# Design analysis — the first ten

*Recommended proposals · 2026-09-29 · No approved design locks*

## Scope and evidence

The ten products are selected for exploration. Their visual identities, palettes, layouts and interaction details remain proposals. This document explains the common design system and the different working surfaces; it does not authorize production implementation or claim market validation.

The primary source pages linked below supply **conceptual interaction references**, mainly through product documentation. They establish that a workflow or feature is described; they do not establish that our proposed premium is useful. Their logged-in interfaces were not inspected. Root visually inspected only the marketing hero on [Linear’s public features page](https://linear.app/features). That limited observation does not support claims about Linear’s application, tables, dialogs, keyboard behavior or responsive states. No vendor interface or logo is copied here.

The proposed compositions are original inferences from each buyer’s decision. Current mock source and product dossiers inform this synthesis. Browser, screenshot, keyboard, theme and responsive verification belong in the root verification record and individual `verification.md` files. This document contains **requirements and rationale, not browser pass results**.

## The governing interaction

**Capture → inspect → decide → record → leave.** The user should be able to name the pending decision and the evidence needed without interpreting a dashboard. Show progress only when its denominator has a useful meaning: findings reviewed, seats allocated, requirements complete, or hours reconciled.

The shell carries navigation, the synthetic-data boundary, palette/theme proposals, state previews, reset and feedback. Each product owns its task. A shared button does not justify identical page composition across a financial ledger, a document review and an episode board.

The user’s decisive action stays beside its evidence. Import is distinct from execution; confirmation is distinct from delivery; intent is distinct from an external change. The visual language must preserve those distinctions even when a green badge would look cleaner.

## Design axes and proposed choices

| Axis | Recommended direction | Alternative or tradeoff |
|---|---|---|
| Canvas | Mist as the neutral starting proposal | Paper emphasizes reading; Porcelain minimizes hue |
| Identity | One restrained accent per product | Distinction comes chiefly from the task layout, not ten decorative themes |
| Type | System sans for operations; mono for code/identifiers | EPUB’s original sample cover may use serif display type; controls remain consistent |
| Hierarchy | One product outcome, then one working surface | Small metrics explain the work; they must not delay access to it |
| Density | Compact lists beside a readable decision area | Reading and form areas receive more space than metadata |
| Shape | Quiet bordered panels and moderate corner rounding | Avoid nested cards where a separator communicates hierarchy |
| Actions | One obvious next step; secondary export and reversible actions | Consequential simulation labels remain explicit |
| Motion | Minimal state changes, no decorative animation | Honor reduced-motion preferences; preserve selection instead of animating it away |

Review one axis at a time. The current shell compares three canvas proposals against the same records, layout and accent. Later typography or density comparisons should hold the selected canvas constant. No selection is treated as a lock until the user explicitly chooses it.

Working names such as Proofroom, Kept and Guestroom describe these concepts. Trademark, domain and naming availability have not been established.

## Three canvas proposals

| Proposal | Intended use | Main tradeoff | Recommendation |
|---|---|---|---|
| Mist | A cool, quiet operations workspace | Can feel technical for editorial work | Default comparison baseline across the suite |
| Paper | Long reading, client statements and publication context | Warm surfaces can soften visual separation | Strong alternative for EPUB, procedures and statement views |
| Porcelain | Neutral records, code and dense comparisons | Depends more on spacing and hierarchy to avoid flatness | Strong alternative for docs, config and ledger work |

These are in-context alternatives, not three separate brands. Both light and dark must preserve the same selected record, statuses and action priority. A palette change must not change calculations, filters, saved records or workflow semantics.

The table records the current **token proposal** from shared CSS. It is a reproducible starting point, not a claim that every combination passes visual QA.

| Palette/theme | Canvas | Surface | Supporting surface | Primary text | Secondary text | Separator |
|---|---|---|---|---|---|---|
| Mist / light | `#f3f5f8` | `#ffffff` | `#f6f8fa` | `#1d2935` | `#617080` | `#dde3e9` |
| Mist / dark | `#12181e` | `#1a222a` | `#202a34` | `#e7edf3` | `#a1afbd` | `#33414e` |
| Paper / light | `#f5f2eb` | `#fffefa` | `#f6f3ed` | `#302d28` | `#716b60` | `#e3dfd5` |
| Paper / dark | `#1b1916` | `#25221e` | `#302b24` | `#f1ebe0` | `#b7ae9e` | `#494136` |
| Porcelain / light | `#f4f4f4` | `#ffffff` | `#f7f7f7` | `#272727` | `#686868` | `#dedede` |
| Porcelain / dark | `#171717` | `#232323` | `#2b2b2b` | `#ededed` | `#b1b1b1` | `#414141` |

## Semantic tokens and theme rules

- `--canvas` is the environment; `--surface` contains the primary record; `--surface-alt` holds supporting context.
- `--ink` carries decisions and primary reading. `--muted` carries secondary context that remains readable.
- `--line` groups and separates; it must not be the only indicator of a selected or interactive control.
- `--accent` identifies focus, selected context and links. `--accent-soft` is a selection fill, not a success signal.
- `--accent-fill` retains an appropriate filled-button tone independently from brightened dark-theme link colors.
- Per-product card and navigation accents must derive theme-appropriate foreground colors; raw light-theme brand hex values are insufficient in dark mode.
- `--danger` means an actionable problem such as unresolved failure or overdue work. `--warning` means pending attention or a bounded uncertainty. `--success` means the explicitly named local outcome.
- Every status has words or another accessible indicator. A color never establishes acceptance, certification or external delivery.

Proposed shared geometry uses 12px panel corners, smaller control corners, visible field boundaries and a consistent spacing rhythm. Main headings distinguish the product promise from panel titles. Body text and evidence use comfortable line height; numeric summaries use tabular figures. Code, source identifiers and filenames use a system monospace stack and wrap or scroll locally.

For acceptance, ordinary meaningful text should meet at least 4.5:1 contrast; qualifying large text at least 3:1. Measure the actual foreground/background pair, including mixed fills and hover states. [W3C text contrast guidance](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html). Required control boundaries, states and graphical information should meet applicable 3:1 non-text contrast requirements. [W3C non-text contrast guidance](https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html). These targets do not constitute a compliance claim for the prototypes.

## Ten task-specific compositions

### 1. Retainer — W0252

**Question:** how much work is authorized, and which entries still need reconciliation?

Use a reconciliation desk beside a statement-shaped client view. The balance strip sits directly above the entries that affect it. An extra-hours request stays visually pending until a recorded approval changes the allowance. The source entry, period and prepared statement revision should remain inspectable.

The important views are the ledger, selected entry, import preview, allowance request and client statement. Negative available hours remain visible as overage; do not clamp them to a reassuring zero. Proposed reusable patterns are bounded import preview, arithmetic summary and revision-bound approval.

[Harvest’s budget documentation](https://support.getharvest.com/hc/en-us/articles/360048686811-How-to-set-project-budgets) supplies the conceptual comparison between hours or fees consumed and remaining. Our evidence-to-statement arrangement is an original proposal. See [product analysis](products/retainer/product.md).

### 2. Documentation examples — W0012

**Question:** which example failed in which attempt, and what should the maintainer change?

Use a failure list, a source/code panel and an owner/run context panel. Prioritize the precise location and diagnostic above aggregate charts. A staged correction must never recolor a failed result as passed; a fresh successful run is different evidence.

Important states are failure, pending rerun, unsupported runner, stale report and all-passing filtered queue. Code scrolls within its panel. Proposed reusable patterns are a bounded code viewer, source locator and attempt history.

[GitHub Actions run-log documentation](https://docs.github.com/en/actions/how-tos/monitor-workflows/use-workflow-run-logs) supplies run selection, failing-step detail and line references as conceptual moves. No GitHub account UI was inspected. See [product analysis](products/docs/product.md).

### 3. Missing-file monitor — W0031

**Question:** which expected arrival needs attention today, and what receipt supports that judgment?

Use a short date strip and expected-arrival timetable beside receipt/exception detail. The timetable is the main working surface. Expected, within grace, late, received and excused states must be named separately; absent collector evidence must not be presented as proof that a partner failed.

The pilot labels times explicitly in UTC. IANA timezone and daylight-saving support are a later verified extension. Proposed reusable patterns are expected-occurrence status, receipt evidence and a reasoned calendar exception.

[Healthchecks documentation](https://healthchecks.io/docs/) provides the conceptual schedule/grace/signal distinction. The partner timetable is our proposal. See [product analysis](products/files/product.md).

### 4. Procedure review — W0263

**Question:** which instruction needs a person to review its current version?

Use a small Due / In review / Current board beside a reading desk. The board finds the obligation; the desk shows source version, excerpt, checks and attestation evidence. Revision resets pending review checks. “Current” describes a dated review record rather than proving the procedure is correct.

Proposed reusable patterns are version-bound attestation, review history and source ownership. A missing source permission should pause review without inventing an excerpt.

[Notion’s wiki and verified-page documentation](https://www.notion.com/help/wikis-and-verified-pages) supplies ownership and verification expiry as conceptual references. The reading desk and review gate are original proposals. See [product analysis](products/procedures/product.md).

### 5. Training seats — W0289

**Question:** do purchased, reserved, attended and available seats still reconcile after substitutions?

Use an entitlement equation and seat tokens above an operational roster. Cohort cards filter the same records. The selected-learner desk keeps the earlier allocation and substitution reason visible. A substitution’s unchanged total should be observable immediately; a release and an attendance correction are distinct actions.

Proposed reusable patterns are capacity validation, linked substitution history and a sponsor statement. Seats must have text totals and accessible descriptions in addition to fill styles.

[Arlo’s customer-portal page](https://www.arlo.co/features/customer-portal) describes registration transfer and course history. It is a conceptual workflow reference, not a copied seat-map interface. See [product analysis](products/training/product.md).

### 6. EPUB review — W0521

**Question:** what was found in this proof, and what evidence supports each correction or human check?

Use publication context above an outline, finding queue and evidence inspector. Distinguish supplied machine findings from human checks. The proof selector changes all relevant evidence together. A new proof must not inherit previous success silently. Client review is a separate, explicit record.

Proposed reusable patterns are a version selector, source-located finding and correction evidence form. A clean queue is not an accessibility certificate.

[Ace’s HTML report documentation](https://daisy.github.io/ace/docs/report-html/) supplies violations, outlines and contextual information for manual review. Our proof-specific handoff is the proposed paid workflow. See [product analysis](products/epub/product.md).

### 7. Customer promises — W0276

**Question:** which accepted customer commitment is due, who owns it, and what can be said honestly?

Use a due-date timeline beside ownership, source conversation and update history. Keep unconfirmed commitments out of customer digests. The digest preview must show a fixed set of reviewed revisions; later edits do not rewrite old approvals. An all-account preview is internal preparation, not a safe multi-customer delivery payload.

Proposed reusable patterns are an owner-confirmation card, dated update trail and immutable digest preview. Avoid health scores that disguise missing owner acceptance.

[Basecamp features](https://basecamp.com/features) supplies contextual work, responsibility and scheduling concepts; [Canny](https://canny.io/pricing) supplies account-related feedback context. Neither establishes an underserved commitment ledger. See [product analysis](products/promises/product.md).

### 8. Vendor renewals — W0261

**Question:** when must a person decide, and what external action remains?

Use a notice-date agenda beside a decision file. Put notice deadline before the later renewal date. The selected record preserves source terms, owner acknowledgment, intent and next step. An overdue deadline remains overdue; a cancellation intention does not become an executed cancellation.

Proposed reusable patterns are date-window comparison, owner acknowledgment and intent history. Reassignment or source-date changes require renewed review.

[ContractSafe’s upcoming-date documentation](https://www.contractsafe.com/support/upcoming-contract-dates) supplies chronological date navigation as a conceptual reference. The bounded decision file is our proposal. See [product analysis](products/renewals/product.md).

### 9. Configuration check — W0034

**Question:** which environment difference is unexplained for the selected release comparison?

Use a side-by-side key roster with selected-key detail and a decision trail. Missing, matching, different and approved states must remain distinct. Environment labels stay close to the columns. Presence comparison is the initial boundary; any optional customer-held keyed equality comparison requires separate protocol review. The interface never asks for raw secret values.

Proposed reusable patterns are comparison-pair context, scoped exception with expiry and a change trail. An exception applies to the inspected pair, not every future value under the same name. A matching display is not a statement that deployment is safe.

[ConfigCat’s feature/pricing page](https://configcat.com/pricing/) supplies environments, reasons and history as conceptual references. Our comparison roster is original. See [product analysis](products/config/product.md).

### 10. Podcast guest readiness — W0507

**Question:** what remains before this guest and producer are prepared for the episode?

Use an episode board with Needs prep / Ready / Recorded stages beside a guest checklist and host notes. Stage and percentage derive from required items. The guest-form preview has a warmer, shorter reading flow than the producer workspace. A reminder names only missing items; recording a simulation must not imply an email or audio capture.

Proposed reusable patterns are readiness checklist, guest packet and reminder preview. Participation information and genuine permission evidence require human handling; the mock acknowledgment is not a signature.

[Riverside’s guest preparation guide](https://riverside.fm/blog/higher-quality-guest-interviews) and [Transistor’s collaboration features](https://transistor.fm/features/) supply preparation and producer-role concepts. The guest board is an original proposal. See [product analysis](products/podcast/product.md).

## Responsive requirements

Target widths are 390px, 820px and 1440px. These are acceptance frames, not a claim that screenshots were captured. Use viewport breakpoints around 768px and 1024px, while evaluating available content width after the shell navigation consumes space. No product should assume that an 820px viewport provides an 820px working panel.

| Product | 390px | 820px | 1440px |
|---|---|---|---|
| Retainer | Balance, ledger, statement in order; table scrolls locally | Statement follows ledger when constrained | Ledger beside statement |
| Docs | Checks, code, context stack | Checks/code share space only if readable; context below | Checks/code/context across workbench |
| Files | Date strip and timetable precede receipt detail | Timetable and detail may share a row | Timetable plus receipt/exception desk |
| Procedures | Vertical lanes, then reading desk | Board above reading desk | Review board beside reading desk |
| Training | Seat totals/map, cohort filter, roster, detail | Detail follows roster | Roster and learner desk share space |
| EPUB | Outline, findings and evidence stack | Outline spans above queue/detail | Outline, queue and inspector in three columns |
| Promises | Timeline, detail, digest stack | Full-width timeline; detail/digest below | Timeline beside commitment inspector |
| Renewals | Notice agenda, then decision file | Agenda before decision desk | Agenda beside decision file |
| Config | Locally scrollable matrix; detail below | Keep columns legible; detail may follow | Matrix beside selected-key decision |
| Podcast | Board columns become consecutive sections | Board above guest inspector | Three-stage board beside inspector |

A page must not acquire horizontal overflow to preserve a desktop composition. Wide code and comparison tables may scroll inside clearly bounded regions. Wrap long titles, customer names, source paths and filenames. Do not hide the field needed for a decision merely to fit a phone. Dialogs fit within the viewport, scroll internally and retain visible dismissal. Controls should remain usable at text zoom and with a mobile keyboard open.

## State matrix

| State | Required behavior | Evidence boundary |
|---|---|---|
| Working sample | Synthetic label, current selection and functional actions | Local state only |
| First visit | Explain the first useful result and provide a sample route | Shell preview; no real onboarding service |
| Empty filtered result | Explain why no work matches; retain filter/clear route | Different from no saved data |
| Loading | Preserve context, label pending state, avoid fake progress | Shell visual preview; no background fetch implied |
| Connection failure | Preserve saved work and make retry explicit | Simulated locally; production failure path still needs testing |
| Invalid form/import | Identify affected field/row; keep input; make no partial write | Each product’s implemented validation is bounded |
| Blocked action | Explain the missing prerequisite beside the disabled action | Missing evidence must not look like successful completion |
| Successful local change | Recompute dependent figures and give concise feedback | Name exactly what changed |
| Draft/approval pending | Keep draft distinct from accepted scope or approved output | Preparing never means sending |
| Changed/stale evidence | Show which version changed; require new review | Production concurrency is not verified by a single-browser mock |
| Export | Export current selected scope and label synthetic content | Click feedback alone is not download-content verification |
| Persistence failure | Warn that storage failed; offer export and usable recovery | No claim of cloud backup |
| Reset | Explain scope; allow cancellation; restore only selected sample | Do not imply undo for a discarded local session |

Product-specific success semantics are stricter than a universal green state: retainer allowance changes only after approval; docs require a fresh run; file watch requires a receipt or explicit exception; procedures require versioned evidence; training preserves seat arithmetic; EPUB retains human checks; promises preserve approved snapshots; renewals preserve external-action boundaries; config exceptions expire; podcast readiness requires all named items.

## Keyboard and accessibility requirements

- Use a landmark structure, a skip-to-workspace route and one main product heading. Product navigation exposes the current page.
- Every visible action is a keyboard-reachable button or link. Selection has a programmatic state as well as color.
- Native dialogs have accessible names, an explicit close control and meaningful initial focus. Escape closes reversible dialogs; focus returns to the invoker. Background controls are inert while modal interaction is active.
- Mobile navigation has a labeled close action, Escape dismissal, contained focus while open and focus restoration. It must not strand focus behind the shade.
- Labels persist after input. Associate validation errors with fields, preserve entered values and move or announce focus usefully after rejection.
- Announce important changes politely without reading every calculated number repeatedly. A toast must not be the only place a required correction is explained.
- Tables expose headings and scope; code and locally scrollable regions have useful labels and keyboard access. Plain buttons are preferable to incomplete ARIA tabs or grids.
- Checkboxes, radios, statuses and progress bars expose their meaning and current value. Do not require color perception or pointer hover to understand a result.
- Make primary mobile targets comfortably reachable, aiming for at least 44px. Keep focus rings visible inside panels and around destructive/reset actions.
- Check real computed contrast in every palette/theme, selected/hover/focus state, meaningful placeholder and status fill. Respect reduced motion and browser text resizing.
- A saved mock is not proof of assistive-technology compatibility. Production acceptance includes keyboard and screen-reader task completion, not only static markup review.

## Reuse and implementation boundaries

The shared public Vue SDK target is `@wow-two-beta/ui-vue`. The shell currently imports its public `Button` and `useMediaQuery`; this does not establish availability of every pattern below. Production integration must verify pinned public exports, event behavior and accessibility contracts before adopting a control. The legacy React package is not the target.

Good shared-control candidates are labeled field/error presentation, modal focus behavior, status badges, toast feedback, bounded import preview, source/version locator, revision-aware approval receipt and export feedback. Domain calculations and decisive verbs stay in the product: a seat substitution is not a generic approval event, and a proof review is not a file receipt.

Persist theme tokens and design rationale centrally; keep product-specific layout CSS scoped to its workspace. Avoid remote fonts, stock photography and decorative assets that create network or licensing dependencies. Original text/geometry covers are sufficient for the EPUB and podcast context in this research suite.

## Review sequence and acceptance record

1. Compare the three canvas proposals on the same working product and both themes.
2. Review the task’s evidence-to-decision layout using its ordered smoke scenario.
3. Check 390px, 820px and 1440px plus text zoom; correct page overflow before cosmetic detail.
4. Complete keyboard paths, dialogs, inline errors, blocked states and focus restoration.
5. Verify local exports and reload persistence separately from visual appearance.
6. Record actual observations, remaining defects and any explicit user design choices in the root verification record.

No browser result is claimed by this document. The next evidence comes from executed interaction and visual checks, followed by user choices and eventual paid workflow experiments. A selected palette or attractive mock does not establish demand or production readiness.

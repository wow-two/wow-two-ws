# Components and constructs resolution

*Last updated: 2026-09-10*

Status: assigned convention implementation complete. No SDK runtime verification is claimed by this record.

Scope: all 269 Markdown files under `conventions/development/frontend/core/mla/components/` and `conventions/development/frontend/core/mla/constructs/`; 265 changed. The original complete coverage list and paired evidence remain in [components-analysis.md](components-analysis.md). Changes are limited to those two trees and this record. No SDK files, other convention owners, staging or commits were changed by this lane.

## Resolved contracts

Paths below beginning `constructs/` or `components/` are relative to `conventions/development/frontend/core/mla/`. Line references identify the corrected contract as of this resolution, not the old audit evidence.

| Main queue | Resolution in this lane | Primary corrected evidence |
|---|---|---|
| C01 | Kept component selection, role definition and instance surface separate. Extraction follows the shared boundary; the central composition rule defers capability dependencies to the owning shape. Package placement and product placement remain different responsibilities. | `components/components.md:44`, `components/components.md:55`, `constructs/visual/visual.md:116`, `constructs/visual/visual.md:136` |
| C02 | Classified editable semantic values independently of current prop spelling. Presentation state may remain in display composites. Replaced the total composition ladder with owned-part, caller-slot and capability rules. Corrected fields, views, pages, panels, layouts, feedback, indicators and state replacement/masking. | `constructs/visual/visual.md:116`, `constructs/visual/control.md:9`, `constructs/visual/field.md:9`, `constructs/constructs.md:36` |
| C03 | Linked controlled/uncontrolled ownership to the LLA owner; added draft/commit, reset, external update, composite labels/focus targets, inherited flags and item availability distinctions. Generic field chrome stays value-free; fused fields forward the model and reuse or create context appropriately. | `constructs/visual/control.md:9`, `constructs/visual/control.md:65`, `constructs/visual/control.md:100`, `constructs/visual/field.md:77` |
| C04 | Native link navigation keeps normal Tab behavior; roving focus belongs to actual composites. Modal, nonmodal and descriptive floating surfaces have different focus/background rules. Added nested dismissal and restoration, scoped host registration/remounting, optional/required providers and live seam replacement. | `constructs/visual/nav.md:9`, `constructs/visual/overlay.md:9`, `constructs/visual/overlay.md:81`, `constructs/visual/provider.md:50`, `constructs/visual/host.md:9` |
| C05 | Required keyboard escape from Tab-intercepting editors, keyboard and single-pointer drag alternatives, group naming, stable focus, non-color meaning, pause/reduced-motion behavior, accessible chart/image meaning and transient notice lifecycle. | `constructs/visual/control.md:100`; component entries for CodeEditor, Sortable, Carousel, Marquee, Typewriter, Tooltip, Image, Sparkline, ToastHost and UndoBar |
| C06 | DTOs and requests are integration-owned; straight validated wire reads remain DTOs, while richer decoded representations map at integration. Live hooks expose lifecycle state rather than fabricated successful Results. Expected failures use Result; total mappers and third-party validator protocols retain their appropriate contracts. | `constructs/data/models.md:13`, `constructs/data/models.md:101`, `constructs/data/result.md:9`, `constructs/data/result.md:54`, `constructs/behavior/hooks.md:27` |
| C07 | Distinguished editable input, parsed schema output and submitted request; linked form lifecycle to its domain owner. Structured controls and send actions do not automatically own the surrounding form lifecycle. Preserved edits during saves and discarded stale validation results. | `constructs/data/models.md`, `constructs/visual/control.md:9`, `constructs/visual/control.md:100`; AddressForm and ChatComposer entries |
| C08 | Vue compound parts use flat named exports; React attachment syntax remains framework-specific. Removed partial Vue snippets that contradicted the macro rules, replacing relevant cases with contract examples and framework links. Added hook cleanup, stale-work and public entry-point ownership. | `constructs/compound/compound.md:17`, `constructs/behavior/hooks.md:53`, `constructs/behavior/hooks.md:63` |
| C09 | Removed duplicated component styling surface inventories; kept actual house preferences and layout selection. Shared CSS/Tailwind correctness remains with its owner. | `components/components.md`, layout selection entries |
| C10 | Added the missing failure vocabulary type alias and explicit discriminant narrowing. Removed fabricated total-mapper failures and distinguished reusable hook `*Controls` interfaces from rendering suffix routing. | `constructs/data/result.md:54`, `constructs/behavior/hooks.md:27` |
| C11 | Added per-app/request provider and host isolation, replacement cleanup and stale-work rejection. Date/time selection entries require domain-appropriate date/wall-clock values and localized display; currency increment follows actual currency/business precision. | `constructs/visual/provider.md:50`, `constructs/visual/host.md:9`, `constructs/behavior/hooks.md:53`; date/time/currency component entries |
| C12 | Added concrete control/lifecycle conformance cases and compound public-import validation requirements. Shared testing/browser/compatibility contracts remain with the shape owners. | `constructs/visual/control.md:100`, `constructs/compound/compound.md:17` |
| C13 | Clarified one implementation owner with a documented package public export; unrelated capability barrels must not republish hooks. Packaging, declaration and release mechanics remain with the library owner. | `constructs/behavior/hooks.md:63`, `components/components.md:55` |
| C14 | Added safe upload/server validation, preview resource cleanup, Markdown sanitization/URL handling, safe result messages, password-strength and provider authorization boundaries where these component choices need them. Shared platform/security policy remains with its owner. | FilePicker, FileUpload, MarkdownEditor, GoogleSignInButton and PasswordStrength entries; `constructs/data/result.md` |
| C15 | Swept every component entry: removed full API inventories, stale spec warnings, migration history, unsupported-feature ceilings and duplicated defaults-as-facts. Retained selection guidance and intentional house preferences. Redirected obsolete LabeledInput/SegmentedControl recommendations, fixed dead conceptual choices, removed hardcoded register counts, clarified definition versus selection document formats. | `components/components.md:44`; full two-tree diff; complete coverage in [components-analysis.md](components-analysis.md) |

## Classification and naming consequences for the SDK sweep

The desired kind is explicit even where a selection doc remains in a historical discovery folder. SDK moves and public names must follow that kind; editing a model prop name is not evidence for the kind.

- Link is navigation. ToggleButton, ToggleButtonGroup and OptionTile edit selection and are controls; OptionTileGroup is field/group chrome.
- DataGrid and NodeEditor edit semantic values and are controls. Tooltip is an overlay. ScheduleView and ThreadView are views. NotificationDot and Status are indicators.
- ControlGroup is field chrome. AddressForm is a structured value control, not a submission owner. Stepper owns presentation state and panels; Wizard owns the multi-step form lifecycle.
- NotificationCenter is a display composite. EmptyState remains state; a loading mask is also state. Visual selection grouping does not require reclassifying either one.
- Suffix matching applies after compound-part, primitive and trailing-modifier exceptions. Shape tables and kind leaf rules agree for Group, Badge/Tag/Glyph, Timeline and Tab. `*Context` names the context contract/key; the component installing it is a `*Provider`.
- The existing gate already requires direct entry `*Input`, presented choice `*Picker`, structured editing `*Editor` and arrangement `*Layout`. The SDK can implement those renames autonomously. Compatibility aliases and current surface details belong in package specs.
- `*Controls` on a reusable live hook contract names state plus operations. The visual suffix table applies only after determining that a declaration renders.

No required semantic design decision remains in this assigned lane. A general relaxation of the existing suffix gate would be a new product preference, not a prerequisite for completing the authorized sweep; the recommendation is to keep the existing gate and apply it consistently.

## Verification and remaining execution

- Read the complete assigned corpus during the analysis pass and reviewed changed contracts and selection rules during implementation.
- Checked local Markdown file targets across all 269 docs: no missing targets.
- Checked explicit local section fragments: no missing targets.
- Checked fence pairing and section content including descendant sections: no unbalanced fences or empty sections.
- `git diff --check -- conventions/development/frontend/core/mla/components conventions/development/frontend/core/mla/constructs` passed.
- Reviewed restored house preferences separately from deleted API inventories and stale implementation constraints.
- No SDK compile, runtime browser, accessibility or release test was run by this lane. Behavioral cases above are acceptance criteria for that next implementation stage, not claims of current SDK support.

SDK tasks still need to implement the target kind/name map, complete code-adjacent specs, correct behavior and exercise the new state/keyboard/locale/lifecycle cases. Deleted instance API inventories are recoverable in the baseline diff and original audit; their accurate replacement must be written from the selected Vue package's actual corrected implementation. The volume of those tasks is implementation work, not a brainstorming blocker.

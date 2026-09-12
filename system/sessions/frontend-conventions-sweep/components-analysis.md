# Frontend conventions audit — components and constructs

Date: 2026-09-09
Scope: `conventions/development/frontend/core/mla/components/**` and `conventions/development/frontend/core/mla/constructs/**`.
Status: Read-only analysis complete. No workspace files changed. No SDK behavior claimed verified by this pass.

## Verdict

The conventions are not a settled target for a mechanical SDK sweep. Their general contracts contradict their component recommendations in several implementation-driving places: controlled values, composition, naming, keyboard behavior, focus, lifecycle results, placement, and framework spelling. Resolve those convention contracts before using the existing SDK sweep rows as acceptance criteria.

The largest maintainability failure is specific: many application-register rules preserve today's incomplete SDK behavior and stale specs as permanent `must` instructions. Moving a component to a kind folder or renaming it cannot resolve that mismatch. The intended contract must be settled independently of today's prop spelling.

## Method and limits

- Read the substantive content of all 269 assigned Markdown files, including every component choice/value rule and every construct contract/example. Coverage is listed below.
- Compared findings against `workbench/wow-two-sdk-beta/wow-two-sdk-beta.ui/engineering/planning/ui-sdk-conventions-sweep.md` (open/done rows and its claim that all convention conflicts were closed).
- Read the convention authoring/index policy and adjacent MLA, props, Vue macro, React index, forms, state/data, i18n, and accessibility utility contracts where needed to verify a cross-reference or conflict.
- Parsed local Markdown links in the assigned trees and resolved their filesystem targets: no missing local file targets. This does not verify section prose references or SDK names placed in backticks.
- Verified selected accessibility claims against W3C primary sources, linked with the relevant findings. No broad certification or runtime accessibility pass was performed.
- Line references refer to the files as read in this pass. Paths beginning `components/` or `constructs/` are relative to `conventions/development/frontend/core/mla/`; paths beginning `core/` are relative to `conventions/development/frontend/`; `conventions/conventions.md` is workspace-relative.

## Existing sweep disposition

| Existing task | Disposition from this audit |
|---|---|
| 7 — components failing their group gate | Expand and reopen the convention verdict. In particular the proposed EmptyState move conflicts with the current state placement rule. Classify by semantic ownership, not whether a component currently spells its value `modelValue`. |
| 8 — missing component specs | Keep; make completeness include behavioral acceptance cases, not only creating files. |
| 9 — React-era syntax | Existing SDK migration work; add convention examples and framework-specific compound/export rules to the convention pass. |
| 12–14 — Result carrier, bag renames, API returns | Keep, but settle live-hook lifecycle vs operation-result contracts before implementation. |
| 18 — no per-component demo | Keep; pair stories with keyboard, state, locale and composition cases where applicable. |
| 25 — kind suffixes | Block the mechanical rename on an internally consistent suffix/kind policy. Current table conflicts cannot yield a unique target name. |
| 27 — stale React-era specs | Expand with a convention cleanup task: stale-spec notes and API limitations are currently repeated as normative application rules. |
| 30 — missing ARIA attribute names | Keep; this is syntax vocabulary coverage, not the navigation/focus/motion behavior defects below. |

The sweep file's `## Rule conflicts` assertion that conventions have no open contradictions is refuted by the paired citations below. Updating that assertion is necessary when incorporating these tasks.

## Findings and proposed tasks

### C01 — P1 — Separate desired conventions from the SDK's current surface and defects

Evidence:

- `components/components.md:31–34` assigns individual props/slots/emits/states to SDK specs and forbids parameter enumeration in the application register.
- `components/layout/stack.md:32` enumerates every supported gap value; `components/layout/grid.md:31–32` enumerates tracks and breakpoint map shape.
- `components/layout/frame.md:32` tells callers not to trust the spec and enumerates additional code-only radii.
- `components/layout/appShell.md:33–34` records React provenance and competing boolean aliases with precedence.
- `components/forms/addressForm.md:30–34`, `dateInput.md:35`, `field.md:39`, `searchInput.md:34–35`, and `wizard.md:36` preserve stale specs and Vue/React migration state.
- `components/forms/codeEditor.md:12–13` makes first-generation missing functionality a rule; `components/display/nodeEditor.md:12`, `dataGrid.md:12`, `pdfViewer.md:12`, and `gantt.md:12` do the same.
- `conventions/conventions.md:64–66` requires conventions to state rules rather than change history.

Impact: a sweep can faithfully enforce an old bug, miss a new capability, or update a spec while leaving contradictory authoritative usage instructions behind. There are two sources for the same SDK surface today.

Task: Classify every leaf rule as component selection, house preference, kind contract, SDK surface, migration debt, or product requirement. Keep the first two in `components/`; place kind contracts in `constructs/`; move current surface facts to specs and defects to SDK tasks. Preserve a reasoned default such as a preferred delay, but remove accepted-range enumeration and `the code currently does X` rules. A future SDK addition must not require rewriting generic conventions simply because an old feature cap was enumerated there.

Owner: conventions component register, with SDK spec/ledger follow-up. Existing coverage: expands #27; migration of current-surface notes is new convention work.

Acceptance: no `stale`, `React-era`, `first-generation`, `none ships`, alias-precedence, or supported-value inventory remains as a perpetual application rule without a deliberately stated policy reason.

### C02 — P1 — Classify a component by its semantic contract, not its current event spelling

Evidence:

- `constructs/constructs.md:29` says ownership determines kind.
- `constructs/visual/action.md:11` says an output read back makes a control; `:27` explicitly puts `SegmentedControl` in actions.
- `constructs/visual/nav.md:18` calls `SegmentedControl` a control.
- `components/actions/toggleButtonGroup.md:5,11–14` says the group owns a selection/value while linking the action kind.
- `components/actions/toggleButton.md:11` says its pressed value is read back while linking the no-value action contract.
- `components/display/dataGrid.md:11,31` describes cell editing; `nodeEditor.md:11,13` describes editable node positions; both link display.
- `constructs/visual/display.md:12` requires same-props/same-output purity, yet `components/display/carousel.md:5,29–30`, `animatedNumber.md:11–12`, and `tree.md:13,30–31` explicitly own temporal or selection state.
- Sweep #7 uses absence of `modelValue` to retain several components in display, although `modelValue` is an implementation consequence of the kind, not the definition of ownership.

Impact: changing only an emit/prop name changes a component's supposed architecture; correct behavior can be moved to the wrong kind or prohibited because its current implementation lacks the desired model API.

Task: Define semantic axes for editable domain value, UI interaction state (open/selected view/scroll), intent emission, and ownership of side effects. Decide how composites fit. Use those decisions to re-verdict all action/display/control groups, and only then pick folders and APIs. Do not infer a control solely from any event, nor infer a display solely from missing `modelValue`.

Owner: constructs visual taxonomy, followed by #7 and #25 SDK sweep. New convention prerequisite to existing rows.

### C03 — P1 — Replace the impossible global composition ladder with explicit composition rules

Evidence:

- `constructs/visual/visual.md:112–120` permits composition down `page → layout → view → panel → display/control/action → indicator/state` and forbids upward composition.
- `constructs/visual/panel.md:100` expressly permits a panel to compose a view, which that ladder forbids.
- `constructs/visual/display.md:105` forbids a display mounting panels or views, while `components/display/tabs.md:12` requires `TabsPanel` and `constructs/visual/view.md:31,99` puts `MonthView` under `EventCalendar`.
- `constructs/visual/control.md:103` forbids a control mounting a panel, while `components/forms/stepper.md:6,12` defines a control whose normal parts include `StepperPanel`.
- `constructs/visual/control.md:101` only permits action/indicator decoration composition, yet complex editors, date/time inputs and pickers require other controls; `control.md:106` itself shows `ColorPicker → Popover → ColorArea`.
- `constructs/visual/field.md:100` forbids field nesting, while `components/forms/checkboxField.md:14` recommends nesting a `CheckboxField` in `Field` for help/error.
- `constructs/visual/feedback.md:105` forbids controls inside feedback; `components/feedback/alertSimple.md:11` and `bannerSimple.md:11` explicitly recommend form content.

Impact: ordinary Tabs, Stepper, JSON editor and field composition cannot satisfy every MUST. A rename does not solve it.

Task: Define allowed owned implementation parts separately from caller-supplied slot content. Model composite roots and primitive composition directly; keep bans tied to architectural dependencies (e.g. reusable display cannot fetch product data), not a total ordering of visual words. Document context validity for compound parts. Add positive and negative examples covering Tabs, Stepper, Calendar views, editor sub-controls and fused fields.

Owner: constructs visual composition + compound; follow-up to SDK #7/#25. New convention prerequisite.

### C04 — P1 — Settle controlled, uncontrolled, draft and multi-part values as one input contract

Evidence:

- `constructs/visual/control.md:12` requires every control to be fully controlled, with no private copy of truth.
- `:73,85–86` requires `modelValue` and parsed `update:modelValue` on committed changes.
- `components/forms/checkbox.md:32–33`, `colorPicker.md:31`, `colorSlider.md:34`, `colorWheel.md:32`, `fontPicker.md:32` and many others explicitly permit or prescribe uncontrolled values.
- `components/forms/colorArea.md:31–34` defines two separate models (`saturation`, `value`), permits a paired event and sets uncontrolled seeds, despite the exactly-one-value gate.
- `components/forms/colorInput.md:30–32` requires an invalid intermediate draft and commit-on-blur/Enter rollback; a strict no-private-copy interpretation prevents typing incomplete valid input.
- `components/forms/calendar.md:33` and `rangeCalendar.md:33` require `isDisabled` to be a day predicate, while `control.md:74` expects the common disabled state inherited from context.
- `core/lla/notation/naming/props.md:38–50` explicitly standardizes controlled and uncontrolled triads, a wider contract than `control.md` admits.

Impact: the sweep has no stable decision for default props, aliases, draft state, clear/reset or disabled inheritance. Picking one rule silently breaks existing behavior sanctioned by another.

Task: Define controlledness and ownership per mode; distinguish canonical committed model from uncommitted presentation draft; standardize controlled/uncontrolled detection, null versus omitted, default seeds, reset, change vs commit, and grouped values. Define whole-control disabled separately from item/day disabling. Apply framework spelling as a separate layer.

Owner: visual/control + props/Vue adapter; SDK controls follow-up. New scope beyond #7/#25; current aliases overlap #27.

### C05 — P1 — Make the field contract work for composite and fused controls

Evidence:

- `constructs/visual/control.md:48` demands one focusable element targeted by `htmlFor` for every control.
- `constructs/visual/field.md:11–14,74–84,97–100` requires exactly one control, no value/emits on the field, and no nested field.
- `components/forms/addressForm.md:11–13` describes an address as one model, says it is `role="group"` rather than a control, and requires `Field` around it. This contradicts the universal direct-label target assumption.
- `components/forms/pinInput.md:5,29` describes many input cells for one value; `dateTimeInput.md:11–12` combines day and time; groups have per-item focus targets.
- `components/forms/checkboxField.md:5,13–14` and `radioField.md:5,13` are fused value-bearing pairs that forward values while the generic field contract forbids value/emits.
- `components/forms/chatComposer.md:6–7` exempts its `submit` because an action is composed inside it, whereas `constructs/visual/control.md:14` calls anything with submit a form.
- `constructs/visual/field.md:54` routes `*Form` to a field kind that is otherwise expressly non-submitting and value-free.

Impact: grouped input names, focus-on-error, field values and submit ownership cannot be implemented uniformly from the current rules.

Task: Define field chrome versus fused field, single DOM input versus composite value editor, focus target registration, group labeling, and form/submit responsibility. Permit one semantic value to use several controls where that is the deliberate contract; do not force a hidden input to become the focus target. Settle `AddressForm`, ChatComposer and Wizard against those semantics.

Owner: field/control plus forms domain. Existing #7/#25 need these definitions; behavioral acceptance additions are new.

### C06 — P1 — Make suffix routing internally consistent before the public rename sweep

Evidence:

- `constructs/constructs.md:49–58,66–70` requires every name to end in its kind or an explicitly admitted shape; `:92–100` then requires trailing Simple/Compact modifiers.
- `constructs/visual/visual.md:70` routes `*Item` exclusively to nav, while compound parts such as `AccordionItem`, `CarouselItem`, `ListItem`, `TimelineItem` are declared elsewhere. The separate compound exemption needs to govern matching explicitly, not rely on prose priority.
- `visual.md:67` calls `*Tab` a routing suffix; `panel.md:59` calls it a shape word.
- `visual.md:90` admits `*Group` for display; `display.md:53–61` does not. `visual.md:96` admits Badge/Tag/Glyph for indicator; `indicator.md:52–54` does not. `visual.md:99` admits Timeline for layout; `layout.md:52–54` does not.
- `layout.md:52` restricts `*Layout` to chrome around a router outlet while its own examples include StackLayout, BoxLayout and GridLayout (`:17`).
- `constructs.md:61,82` approves `CodesListPage`, but the three-slot account disallows independent subject words unless sourced from a domain folder; it does not explain `List` there.
- `components/display/scheduleView.md:6` and `threadView.md:6` call components displays while their names route to view.
- `components/actions/segmentedControl.md:11` deprecates a name still recommended by `forms/choiceCard.md:23`, `emojiSizeControl.md:24`, `radio.md:23`, `radioGroup.md:23`, `switch.md:23` and `display/tabs.md:22`.
- Existing sweep #13 intends hook return bags to use `*Controls`, a suffix routed only to visual controls at `visual.md:72`.

Task: Write one canonical routing algorithm and resolve modifiers, compound roots/parts, headless return bags and shape words. Keep kind leaf docs authoritative without contradictory duplicated tables. Rebuild examples and all recommendations against it, and give the SDK rename row an unambiguous target map.

Owner: naming/constructs + existing #13/#25. This is a policy consistency task, not a preference for shorter names.

### C07 — P1 — Correct the universal navigation keyboard contract

Evidence:

- `constructs/visual/nav.md:13` requires a roving tab stop for every nav, rejecting a list of separate tab stops.
- `:47` mandates RovingFocusGroup and DismissableLayer for all of them.
- The same kind includes Breadcrumb, Pagination, sidebar navigation and TableOfContents (`:17`; `components/nav/nav.md:12–22`).
- `components/nav/breadcrumb.md:29–31` describes a normal ancestor link trail, not a menu or composite widget.

External check: [WAI APG Breadcrumb](https://www.w3.org/WAI/ARIA/apg/patterns/breadcrumb/) describes a navigation landmark containing links and has no special keyboard interaction. Native link navigation should not be converted into a menu-like roving focus contract merely because the folder is named nav.

Task: Select keyboard behavior from the semantic pattern (links/disclosure/navigation, menu, listbox, tabs, toolbar), and require native link behaviors to survive. Move roving and dismissal to the patterns that require them. Cover breadcrumb/sidebar/pagination keyboard navigation separately from menu/menubar.

Owner: nav kind plus accessibility pattern guidance. New; #30's ARIA name constants do not cover it.

### C08 — P1 — Distinguish modal, nonmodal and descriptive floating surfaces

Evidence:

- `constructs/visual/overlay.md:14` mandates trap/restore focus on every overlay.
- `components/overlays/hoverCard.md:5,12` says a HoverCard never takes/traps focus; `components/display/tooltip.md:12` says the Tooltip takes no focus and holds nothing operable.
- `constructs/visual/overlay.md:53` expressly includes `*Tooltip` in the overlay kind.
- `components/overlays/popover.md:5,12` hardcodes focus trapping while describing a surface beside the unblocked page. This requires an explicit modal/nonmodal contract, not inferring it from its visual anchor.
- `components/overlays/bottomSheet.md:21` sends a bottom panel needing no handle to Drawer; `components/overlays/drawer.md:30` forbids that exact bottom Drawer.
- `components/overlays/modal.md:31` sends any flow unable to afford outside dismissal to AlertModal, though `alertModal.md:11` restricts that kind to destructive/irreversible confirmation. A dirty editor is not necessarily an alert dialog.

External check: [WAI APG Tooltip](https://www.w3.org/WAI/ARIA/apg/patterns/tooltip/) keeps focus on the trigger and uses `aria-describedby`; that particular APG page labels its pattern as work in progress. The internal contradiction does not depend on treating APG as normative.

Task: Specify focus and background interactivity by modal semantics; define accessible naming/description, dismissal, trigger restoration, nested nonmodal surfaces and route-independent dirty-form close handling. Keep anchor geometry orthogonal. Resolve the fixed-height bottom-surface recommendation.

Owner: overlay kind and overlay selection docs. New convention prerequisite; Tooltip placement overlaps #7.

### C09 — P1 — Add safe keyboard-exit and persistent-motion controls

Evidence:

- `components/forms/codeEditor.md:31` recommends enabling Tab indentation where desired and explicitly notes that it costs the keyboard exit. It supplies no required alternative exit affordance or instruction.
- `components/display/marquee.md:5,11–13,29–30` prescribes a forever-scrolling decorative strip and a hover-only pause preference.
- `components/display/typewriter.md:31` makes multiple phrases loop by default; no persistent pause control is required.
- `constructs/visual/indicator.md:48` covers reduced-motion preference, but that is not the same contract as a user-operated pause that lets the rest of the page remain usable.

External checks:

- [WCAG 2.2 No Keyboard Trap](https://www.w3.org/WAI/WCAG22/Understanding/no-keyboard-trap.html) requires a keyboard exit and instructions when nonstandard keys are needed; its editor example includes an advertised exit shortcut.
- [WCAG 2.2 Pause, Stop, Hide](https://www.w3.org/WAI/WCAG22/Understanding/pause-stop-hide.html) explains when automatically moving or updating content requires a pause/stop/hide mechanism. A pause that only lasts while focus is held on the animation is insufficient; reduced-motion support alone does not settle this requirement.

Task: Require the editor's keyboard escape contract alongside indentation and test it. Require operable persistent pause/stop/hide for applicable prolonged automatic animation, including keyboard and touch users. Keep reduced motion as a separate required behavior, not the only substitute.

Owner: controls/display behavior + accessibility guidance; SDK CodeEditor and motion components. New; not #18 story coverage alone.

### C10 — P1 — Separate operation Results from live hook lifecycle

Evidence:

- `constructs/behavior/hooks.md:29–30` says a fallible hook returns Result and never a loose error field.
- The next example (`:34–36`) returns `{ listings, loading, error, refetch }`, directly breaking the stated rule.
- `components/behavior/behavior.md:11–13` declares object returns only for non-failing hooks and eliminates shape choice for fallible ones.
- `constructs/data/result.md:12–14` has exactly success(value) and failure(failure). It does not model not-yet-loaded, disabled, pending or previous-success-while-refreshing.
- `core/mla/domains/data/state-and-data.md:50,54–56` assigns query loading/error/pagination/poll lifecycle to these same hooks.

Impact: mechanically replacing hook return bags with Result either discards operations and reactive status or requires an unstated second wrapper. Pending may be misrepresented as failure or false success. The outcome of a `refetch` operation is not the identity of the hook controlling that refetch.

Task: Define the live hook state/operations contract, with explicit idle/pending/success/failure or equivalent reactive fields, and use Result for the fallible operations and completed outcome payloads. Describe how stale data and refreshing coexist, how cancellation is represented, and where throwing query-engine boundaries translate into the house contract. Correct the example and settle return-bag naming.

Owner: behavior/data constructs and data domain; prerequisite to SDK #12–14. Existing migration gets an expanded convention acceptance gate.

### C11 — P1 — Pick one DTO ownership and mapping boundary

Evidence:

- `constructs/data/models.md:29,34` places read shapes and row DTOs in domain.
- `:63–64` places DTOs beside clients in integration.
- `:19,53,106–109` explicitly permits straight DTO reads with no model/mapper, and requires mapping at the integration boundary only when an app model exists.
- `core/mla/domains/data/state-and-data.md:60–61` requires mapping DTO to model at the hook boundary and bans every raw DTO in the view tree.

Task: Decide read DTO location and when a separate app-owned model is justified; specify the mapping seam once and link it. Verify straight reads, reshaped reads, nested write sub-shapes, list query DTOs and fallible mappings against the chosen policy.

Owner: models + app architecture/data domain. New convention conflict; SDK Result mapper work must consume it.

### C12 — P2 — Correct page and view gates that exclude legitimate small routes

Evidence:

- `constructs/visual/page.md:11` defines route identity, then `:14` requires every page to compose two or more subdomains.
- `:18` approves LoginPage and BlogPostPage, which need not span multiple subjects; a single-subject body is instead forced to view.
- `constructs/visual/view.md:11` requires every view to have an actual swappable sibling, leaving a single-subject routed screen with neither legal kind if read literally.
- `page.md:15` permits only the page to start route data fetching; `components/display/tabs.md:31` recommends manual activation when a panel costs a fetch, but no exception or owner is specified.
- `page.md:72` says a router supplies no props because it is not a caller. Even if no route props is a house choice, the claimed absence of a caller is not its mechanism.

Task: Make route ownership sufficient for Page regardless of subdomain count. Define view/composite intent without requiring a speculative sibling and specify ownership of lazy data loads, nested routes and route-provided inputs as explicit policy. Do not force unnecessary subdivisions only to satisfy naming.

Owner: page/view + app routing. New; extends no existing simple rename row.

### C13 — P2 — Make layout chrome and display ownership boundaries usable

Evidence:

- `constructs/visual/layout.md:11–14` restricts layouts to children, position/spacing, no colour/tone/state and in-flow rendering.
- `components/layout/surface.md:5,11,30–32`, `frame.md:11–12,30`, `section.md:12,33`, and `navbar.md:33` prescribe fill, border, tone, radius and shadow as layout responsibilities.
- `components/layout/controlGroup.md:5,11,31–32` gives a layout its own label and field association.
- `components/layout/divider.md:5,12,31–32` gives a layout its own text label.
- `components/layout/overlay.md:11–12,30` is an absolutely positioned layout pin, contradicting the universal in-flow rule.
- `components/layout/pullToRefresh.md:30` gives a layout an asynchronous action and own spinner lifecycle.
- `components/layout/resizablePanels.md:11–12` works only with a specific child type and owns resize behavior, unlike `layout.md:12` and its open-state-only emit restriction at `:82`.

Task: Permit presentation chrome as layout if that is the intended distinction, and define behaviorful layout composites separately from data displays. Classify ControlGroup as labeling chrome/field or document its explicit role rather than listing it under an incompatible kind. Keep absolute anchoring distinct from a modal overlay.

Owner: layout/display/control taxonomy; expands #7 beyond its current small display subset.

### C14 — P2 — Remove duplicate rules and resolve authoring-format contradictions

Evidence:

- `constructs/constructs.md:157` says to duplicate a pure DRY/layout wrapper inline; `components/components.md:62` says not to duplicate a pure layout wrapper across products. If different scopes are intended, neither rule states that boundary clearly enough to implement.
- `core/mla/mla.md:43–61` requires Location/Declaration/Content sections and plural `components` role files.
- `components/components.md:46–49` repeats that requirement, but all component leaves use Reach for it when / Instead of / Values and singular component filenames. The mandatory template does not describe the intended application register.
- Host single mounting is stated in `constructs/visual/host.md:12,29,100,102` and `components/feedback/toastHost.md:11,30`.
- No-throw Result handling repeats in `constructs/data/result.md:24–29`, `components/data/data.md:10,17–18` and the data domain.
- Repeated input defaults appear in `forms/textInput.md:32–35`, `emailInput.md:30–31`, `telInput.md:29–30`, `textAreaInput.md:31–32`, `searchInput.md:30,32`, etc.

Task: Give definition and application registers distinct allowed templates. Extract each shared contract once; make component leaves state only differences and selection/house preference. Choose or precisely scope the layout-wrapper duplication policy. Do not blanket-format every leaf into the wrong template to make headings uniform.

Owner: MLA authoring + constructs/components. New convention task; complements the earlier comment compacting work, which did not settle ownership here.

### C15 — P2 — Make framework-neutral kind contracts neutral and move spelling to adapters

Evidence:

- `constructs/visual/visual.md:12–13` says rules are framework-neutral and fences only show Vue spelling.
- Rules outside fences still mandate `modelValue` and `update:modelValue` (`control.md:73,85`), `provide()` (`provider.md:52`) and literal `<slot />` (`provider.md:11`).
- `constructs/compound/compound.md:19–26` mandates attached Object.assign component statics, `displayName` and a forwardRef example comment for every framework.
- `components/layout/appShell.md:33` and `resizablePanels.md:34` explicitly prohibit those attached spellings because Vue exports are flat.
- Most visual-kind positive fences use inline `defineProps<{...}>` without readonly members, even though `constructs.md:131–136` and `core/lla/constructs/vue/macros.md:27–28` prohibit that shape.
- `constructs/visual/primitive.md:60` uses a `Traps…` component doc while `constructs.md:124` requires `Renders…`.

Task: State behavioral obligations once (value in/change out, context provision, compound association); link to Vue/React spellings and export choices. Make positive examples either valid complete local examples or clearly scoped fragments that cannot be copied as a contradictory scaffold. Remove the pre-19 comment where it endorses a banned form.

Owner: constructs and framework adapters. Existing #9/#27 are SDK debt; convention examples/neutrality are new prerequisite work.

### C16 — P2 — Scope provider requirements and host singleton rules to the capability instance

Evidence:

- `constructs/visual/provider.md:52–54` requires a loud missing-provider failure and live seam replacement for every provider.
- `core/mla/domains/i18n/i18n.md:16` requires working without a provider, using fallback messages/default locale.
- `core/lla/constructs/vue/macros.md:41` permits a read-once provided client created once and never swapped; the provider type contract needs to say which lifetime applies.
- `constructs/visual/host.md:12,76,100–102` requires one mount while allowing a caller-supplied bus, but does not say whether the invariant is per application, bus, request or process.
- `components/feedback/feedbackToastHost.md:29` explicitly drops pre-mount notices, while host naming/documentation implies rendering everything published. The delivery policy must be deliberate and discoverable beside the contract.

Task: Mark required and optional provider access separately; declare whether a seam is immutable or replaceable. Define host uniqueness per owned bus/app instance, cleanup/remount and request isolation, plus pre-mount/no-listener event semantics. Keep those in capability contracts and link component selection to them.

Owner: provider/host kinds + i18n/feedback domains. New convention task; SDK code must be remeasured rather than assumed deficient.

### C17 — P2 — Finish the behavioral requirements missing from bespoke input and interaction contracts

This is a gap finding, not a claim of current SDK failure.

Evidence:

- `control.md:85–86` describes parsed commits but does not state IME composition, text selection/caret, paste, native form reset or autofill behavior.
- `components/forms/chatComposer.md:30–31` sends on Enter without qualifying composition-in-progress.
- `components/forms/tagsInput.md:30` commits on delimiter/Enter/Tab; `pinInput.md:12` acts on completion; `maskedInput.md:31` filters characters. Those are precisely where composition and paste semantics affect correctness.
- `components/display/sortable.md:11–13,29–30` defines handle drag/reorder indices but no keyboard or non-drag command path.
- `components/forms/keyboardShortcutPicker.md:30` delegates all reserved-chord collision handling to callers without a shared rule or platform capability source.
- `components/forms/addressForm.md:31` accepts unlocalized embedded English and `calendar.md:34` hardcodes Sunday-first; the i18n domain provides a resolver/formatter seam but does not connect all component copy, week-start or direction-sensitive behavior to it.

Task: Add a reusable control/interaction conformance checklist in the contract owner's scope: IME, paste, caret, autofill, reset, null clearing, async race/cancellation, disabled/read-only, focus on error, keyboard alternatives and locale/direction. Component specs should select applicable cases. Reconcile locale policy with embedded copy and day-order assumptions rather than canonizing English-only constraints.

Owner: control/behavior/accessibility/i18n conventions; expand SDK #8/#18 with behavior coverage and add implementation rows only when measured.

### C18 — P2 — Fix feedback/state distinctions and preserve announcement semantics

Evidence:

- `constructs/visual/state.md:11` says a state replaces content; `components/feedback/loadingOverlay.md:11–12` says the content stays visible underneath a state.
- `state.md:73–83` requires title/copy/actions and forbids emits for every state; `components/feedback/skeleton.md:29–31` instead describes shape-only, aria-hidden blocks.
- `constructs/visual/feedback.md:14` says copy-bearing reports are feedback and bare marks are indicators; `components/feedback/statusIndicator.md:12` says it is not an indicator because it carries copy but links the indicator construct at `:6`.
- `constructs/visual/indicator.md:72–77` expressly permits label/description copy, weakening the stated separator again.
- `constructs/visual/feedback.md:76,88` requires tone and dismiss; `components/feedback/alert.md:31–32` prescribes severity and close, and `toast.md:30–31` does likewise.
- `components/feedback/toast.md:12` permits a caller-owned timer for a bespoke viewport; `:32` forbids adding a timer around that same card.
- `state.md:27` and `components/display/emptyState.md:6–7` deliberately keep the empty-state case in display; sweep #7's move to feedback therefore uses a different convention than the one currently written.

Task: Define the distinctions by semantic job, allow copy/visual variants without changing kind, distinguish replacement/loading-mask/skeleton behavior and name which layer owns the live region. Pick the shared report vocabulary and close lifecycle once. Reconcile EmptyState placement with the sweep target before moving any code.

Owner: state/feedback/indicator constructs and selection docs; expands #7/#27, adds report lifecycle acceptance.

### C19 — P3 — Repair cross-choice and index drift without mistaking file links for API validation

Evidence:

- `components/components.md:81` says 8 overlays, while `components/overlays/overlays.md:13–21` lists 9.
- `constructs/constructs.md:12–16` lists visual/behavior/data but omits the compound folder linked elsewhere.
- `components/forms/colorSwatchPicker.md:24` and `emojiSizeControl.md:23` recommend OptionTileGroup for per-option titles/descriptions, while `components/actions/optionTile.md:5,11` explicitly defines icon-only glyph/swatch tiles and `optionTileGroup.md:5,11` defines the wrapping label/fieldset, not rich per-option copy.
- `components/display/tag.md:22` refers to bare `Chip`; `radiusGlyph.md:21` refers to `Progress`; `card.md:24` refers to standalone `Panel`, although `constructs/visual/panel.md:11,18` rejects a standalone panel. These plain-code references bypass the local link checker and need resolution against the settled component surface.
- `components/display/badgeOverlay.md:12` says the wrapped child stays unchanged while layout/shape classification gives it conflicting ownership with the in-box pin. Treat this as part of the shape-choice cleanup, not proof of an SDK mutation bug.

Task: Validate selection-table targets against canonical exported/component spec names, remove deprecated recommendations, repair the reversed/rich-tile choice, and derive/remove human-kept counts. Use link checks as one gate, never as proof that a named SDK component exists or fits the use case.

Owner: components indexes and choice tables. Mostly absorbs into #25/#27 follow-up; separate convention integrity acceptance.

## Suggested sequencing for the parent sweep

1. Resolve C01–C06 plus C10–C16/C18 as the convention target: register ownership, semantic kind/composition, models, lifecycle, naming and framework boundaries.
2. Add C07–C09/C17 behavior requirements, grounded in platform semantics, and fix C19 selection references.
3. Re-measure existing SDK sweep rows using the settled rules; retain old measurements as historical evidence only.
4. Implement SDK gaps and publish only after the package's requested release gates. This read-only pass does not claim any SDK implementation, test result or readiness to publish.

## Coverage list

The list below records every assigned file read. It is a coverage manifest, not evidence that every rule in those files is correct.


### constructs

- `conventions/development/frontend/core/mla/constructs/behavior/behavior.md`
- `conventions/development/frontend/core/mla/constructs/behavior/headless-suffixes.md`
- `conventions/development/frontend/core/mla/constructs/behavior/hooks.md`
- `conventions/development/frontend/core/mla/constructs/compound/compound.md`
- `conventions/development/frontend/core/mla/constructs/constructs.md`
- `conventions/development/frontend/core/mla/constructs/data/data.md`
- `conventions/development/frontend/core/mla/constructs/data/enum-display.md`
- `conventions/development/frontend/core/mla/constructs/data/enum-payload.md`
- `conventions/development/frontend/core/mla/constructs/data/models.md`
- `conventions/development/frontend/core/mla/constructs/data/result.md`
- `conventions/development/frontend/core/mla/constructs/visual/action.md`
- `conventions/development/frontend/core/mla/constructs/visual/control.md`
- `conventions/development/frontend/core/mla/constructs/visual/display.md`
- `conventions/development/frontend/core/mla/constructs/visual/feedback.md`
- `conventions/development/frontend/core/mla/constructs/visual/field.md`
- `conventions/development/frontend/core/mla/constructs/visual/host.md`
- `conventions/development/frontend/core/mla/constructs/visual/indicator.md`
- `conventions/development/frontend/core/mla/constructs/visual/layout.md`
- `conventions/development/frontend/core/mla/constructs/visual/nav.md`
- `conventions/development/frontend/core/mla/constructs/visual/overlay.md`
- `conventions/development/frontend/core/mla/constructs/visual/page.md`
- `conventions/development/frontend/core/mla/constructs/visual/panel.md`
- `conventions/development/frontend/core/mla/constructs/visual/primitive.md`
- `conventions/development/frontend/core/mla/constructs/visual/provider.md`
- `conventions/development/frontend/core/mla/constructs/visual/state.md`
- `conventions/development/frontend/core/mla/constructs/visual/view.md`
- `conventions/development/frontend/core/mla/constructs/visual/visual.md`

### components

- `conventions/development/frontend/core/mla/components/actions/actions.md`
- `conventions/development/frontend/core/mla/components/actions/backToTopButton.md`
- `conventions/development/frontend/core/mla/components/actions/button.md`
- `conventions/development/frontend/core/mla/components/actions/buttonGroup.md`
- `conventions/development/frontend/core/mla/components/actions/copyButton.md`
- `conventions/development/frontend/core/mla/components/actions/disclosureButton.md`
- `conventions/development/frontend/core/mla/components/actions/fab.md`
- `conventions/development/frontend/core/mla/components/actions/googleSignInButton.md`
- `conventions/development/frontend/core/mla/components/actions/link.md`
- `conventions/development/frontend/core/mla/components/actions/optionTile.md`
- `conventions/development/frontend/core/mla/components/actions/optionTileGroup.md`
- `conventions/development/frontend/core/mla/components/actions/segmentedControl.md`
- `conventions/development/frontend/core/mla/components/actions/speedDial.md`
- `conventions/development/frontend/core/mla/components/actions/toggleButton.md`
- `conventions/development/frontend/core/mla/components/actions/toggleButtonGroup.md`
- `conventions/development/frontend/core/mla/components/actions/toolbar.md`
- `conventions/development/frontend/core/mla/components/behavior/behavior.md`
- `conventions/development/frontend/core/mla/components/components.md`
- `conventions/development/frontend/core/mla/components/data/data.md`
- `conventions/development/frontend/core/mla/components/display/accordion.md`
- `conventions/development/frontend/core/mla/components/display/activityFeed.md`
- `conventions/development/frontend/core/mla/components/display/animatedNumber.md`
- `conventions/development/frontend/core/mla/components/display/annotationMarker.md`
- `conventions/development/frontend/core/mla/components/display/audioPlayer.md`
- `conventions/development/frontend/core/mla/components/display/audioWaveform.md`
- `conventions/development/frontend/core/mla/components/display/avatar.md`
- `conventions/development/frontend/core/mla/components/display/avatarGroup.md`
- `conventions/development/frontend/core/mla/components/display/badge.md`
- `conventions/development/frontend/core/mla/components/display/badgeOverlay.md`
- `conventions/development/frontend/core/mla/components/display/card.md`
- `conventions/development/frontend/core/mla/components/display/carousel.md`
- `conventions/development/frontend/core/mla/components/display/chatBubble.md`
- `conventions/development/frontend/core/mla/components/display/code.md`
- `conventions/development/frontend/core/mla/components/display/collapsible.md`
- `conventions/development/frontend/core/mla/components/display/commentThread.md`
- `conventions/development/frontend/core/mla/components/display/confetti.md`
- `conventions/development/frontend/core/mla/components/display/countBadge.md`
- `conventions/development/frontend/core/mla/components/display/countUp.md`
- `conventions/development/frontend/core/mla/components/display/dataGrid.md`
- `conventions/development/frontend/core/mla/components/display/dataTable.md`
- `conventions/development/frontend/core/mla/components/display/descriptionList.md`
- `conventions/development/frontend/core/mla/components/display/diffViewer.md`
- `conventions/development/frontend/core/mla/components/display/display.md`
- `conventions/development/frontend/core/mla/components/display/emptyState.md`
- `conventions/development/frontend/core/mla/components/display/eventCalendar.md`
- `conventions/development/frontend/core/mla/components/display/eyebrow.md`
- `conventions/development/frontend/core/mla/components/display/featureCard.md`
- `conventions/development/frontend/core/mla/components/display/frameGlyph.md`
- `conventions/development/frontend/core/mla/components/display/gantt.md`
- `conventions/development/frontend/core/mla/components/display/gradientText.md`
- `conventions/development/frontend/core/mla/components/display/heading.md`
- `conventions/development/frontend/core/mla/components/display/heatmapCalendar.md`
- `conventions/development/frontend/core/mla/components/display/highlight.md`
- `conventions/development/frontend/core/mla/components/display/image.md`
- `conventions/development/frontend/core/mla/components/display/infoRow.md`
- `conventions/development/frontend/core/mla/components/display/kbd.md`
- `conventions/development/frontend/core/mla/components/display/keyboardShortcut.md`
- `conventions/development/frontend/core/mla/components/display/list.md`
- `conventions/development/frontend/core/mla/components/display/mark.md`
- `conventions/development/frontend/core/mla/components/display/marquee.md`
- `conventions/development/frontend/core/mla/components/display/messageList.md`
- `conventions/development/frontend/core/mla/components/display/metaInline.md`
- `conventions/development/frontend/core/mla/components/display/metricChip.md`
- `conventions/development/frontend/core/mla/components/display/moduleGlyphs.md`
- `conventions/development/frontend/core/mla/components/display/nodeEditor.md`
- `conventions/development/frontend/core/mla/components/display/notificationDot.md`
- `conventions/development/frontend/core/mla/components/display/pdfViewer.md`
- `conventions/development/frontend/core/mla/components/display/pricingCard.md`
- `conventions/development/frontend/core/mla/components/display/quote.md`
- `conventions/development/frontend/core/mla/components/display/radiusGlyph.md`
- `conventions/development/frontend/core/mla/components/display/reactionBar.md`
- `conventions/development/frontend/core/mla/components/display/scheduleView.md`
- `conventions/development/frontend/core/mla/components/display/scrollReveal.md`
- `conventions/development/frontend/core/mla/components/display/sectionHeader.md`
- `conventions/development/frontend/core/mla/components/display/separator.md`
- `conventions/development/frontend/core/mla/components/display/snippet.md`
- `conventions/development/frontend/core/mla/components/display/sortable.md`
- `conventions/development/frontend/core/mla/components/display/sparkline.md`
- `conventions/development/frontend/core/mla/components/display/stat.md`
- `conventions/development/frontend/core/mla/components/display/status.md`
- `conventions/development/frontend/core/mla/components/display/stepCard.md`
- `conventions/development/frontend/core/mla/components/display/swipeActions.md`
- `conventions/development/frontend/core/mla/components/display/table.md`
- `conventions/development/frontend/core/mla/components/display/tabs.md`
- `conventions/development/frontend/core/mla/components/display/tag.md`
- `conventions/development/frontend/core/mla/components/display/text.md`
- `conventions/development/frontend/core/mla/components/display/threadView.md`
- `conventions/development/frontend/core/mla/components/display/tilt.md`
- `conventions/development/frontend/core/mla/components/display/timeline.md`
- `conventions/development/frontend/core/mla/components/display/tooltip.md`
- `conventions/development/frontend/core/mla/components/display/tree.md`
- `conventions/development/frontend/core/mla/components/display/typewriter.md`
- `conventions/development/frontend/core/mla/components/display/videoPlayer.md`
- `conventions/development/frontend/core/mla/components/feedback/alert.md`
- `conventions/development/frontend/core/mla/components/feedback/alertSimple.md`
- `conventions/development/frontend/core/mla/components/feedback/banner.md`
- `conventions/development/frontend/core/mla/components/feedback/bannerSimple.md`
- `conventions/development/frontend/core/mla/components/feedback/callout.md`
- `conventions/development/frontend/core/mla/components/feedback/feedback.md`
- `conventions/development/frontend/core/mla/components/feedback/feedbackToastHost.md`
- `conventions/development/frontend/core/mla/components/feedback/inlineSpinner.md`
- `conventions/development/frontend/core/mla/components/feedback/liveCursor.md`
- `conventions/development/frontend/core/mla/components/feedback/loadingOverlay.md`
- `conventions/development/frontend/core/mla/components/feedback/loadingState.md`
- `conventions/development/frontend/core/mla/components/feedback/meterBar.md`
- `conventions/development/frontend/core/mla/components/feedback/notificationCenter.md`
- `conventions/development/frontend/core/mla/components/feedback/onboardingChecklist.md`
- `conventions/development/frontend/core/mla/components/feedback/presenceIndicator.md`
- `conventions/development/frontend/core/mla/components/feedback/progressBar.md`
- `conventions/development/frontend/core/mla/components/feedback/progressCircle.md`
- `conventions/development/frontend/core/mla/components/feedback/progressSteps.md`
- `conventions/development/frontend/core/mla/components/feedback/skeleton.md`
- `conventions/development/frontend/core/mla/components/feedback/spinner.md`
- `conventions/development/frontend/core/mla/components/feedback/statusIndicator.md`
- `conventions/development/frontend/core/mla/components/feedback/toast.md`
- `conventions/development/frontend/core/mla/components/feedback/toastHost.md`
- `conventions/development/frontend/core/mla/components/feedback/toastSimple.md`
- `conventions/development/frontend/core/mla/components/feedback/trendIndicator.md`
- `conventions/development/frontend/core/mla/components/feedback/typingIndicator.md`
- `conventions/development/frontend/core/mla/components/feedback/undoBar.md`
- `conventions/development/frontend/core/mla/components/forms/addressForm.md`
- `conventions/development/frontend/core/mla/components/forms/calendar.md`
- `conventions/development/frontend/core/mla/components/forms/characterCount.md`
- `conventions/development/frontend/core/mla/components/forms/chatComposer.md`
- `conventions/development/frontend/core/mla/components/forms/checkbox.md`
- `conventions/development/frontend/core/mla/components/forms/checkboxField.md`
- `conventions/development/frontend/core/mla/components/forms/checkboxGroup.md`
- `conventions/development/frontend/core/mla/components/forms/choiceCard.md`
- `conventions/development/frontend/core/mla/components/forms/codeEditor.md`
- `conventions/development/frontend/core/mla/components/forms/colorArea.md`
- `conventions/development/frontend/core/mla/components/forms/colorInput.md`
- `conventions/development/frontend/core/mla/components/forms/colorPicker.md`
- `conventions/development/frontend/core/mla/components/forms/colorSlider.md`
- `conventions/development/frontend/core/mla/components/forms/colorSwatch.md`
- `conventions/development/frontend/core/mla/components/forms/colorSwatchPicker.md`
- `conventions/development/frontend/core/mla/components/forms/colorWheel.md`
- `conventions/development/frontend/core/mla/components/forms/combobox.md`
- `conventions/development/frontend/core/mla/components/forms/cronInput.md`
- `conventions/development/frontend/core/mla/components/forms/currencyInput.md`
- `conventions/development/frontend/core/mla/components/forms/dateInput.md`
- `conventions/development/frontend/core/mla/components/forms/datePicker.md`
- `conventions/development/frontend/core/mla/components/forms/dateRangePicker.md`
- `conventions/development/frontend/core/mla/components/forms/dateTimeInput.md`
- `conventions/development/frontend/core/mla/components/forms/editable.md`
- `conventions/development/frontend/core/mla/components/forms/emailInput.md`
- `conventions/development/frontend/core/mla/components/forms/emojiPicker.md`
- `conventions/development/frontend/core/mla/components/forms/emojiSizeControl.md`
- `conventions/development/frontend/core/mla/components/forms/field.md`
- `conventions/development/frontend/core/mla/components/forms/fieldset.md`
- `conventions/development/frontend/core/mla/components/forms/filePicker.md`
- `conventions/development/frontend/core/mla/components/forms/fileUpload.md`
- `conventions/development/frontend/core/mla/components/forms/fontPicker.md`
- `conventions/development/frontend/core/mla/components/forms/formErrorMessage.md`
- `conventions/development/frontend/core/mla/components/forms/formHelperText.md`
- `conventions/development/frontend/core/mla/components/forms/forms.md`
- `conventions/development/frontend/core/mla/components/forms/gradientPicker.md`
- `conventions/development/frontend/core/mla/components/forms/iconPicker.md`
- `conventions/development/frontend/core/mla/components/forms/inputAddon.md`
- `conventions/development/frontend/core/mla/components/forms/inputGroup.md`
- `conventions/development/frontend/core/mla/components/forms/jsonEditor.md`
- `conventions/development/frontend/core/mla/components/forms/keyboardShortcutPicker.md`
- `conventions/development/frontend/core/mla/components/forms/knob.md`
- `conventions/development/frontend/core/mla/components/forms/label.md`
- `conventions/development/frontend/core/mla/components/forms/labeledInput.md`
- `conventions/development/frontend/core/mla/components/forms/legend.md`
- `conventions/development/frontend/core/mla/components/forms/listbox.md`
- `conventions/development/frontend/core/mla/components/forms/markdownEditor.md`
- `conventions/development/frontend/core/mla/components/forms/maskedInput.md`
- `conventions/development/frontend/core/mla/components/forms/multiSelect.md`
- `conventions/development/frontend/core/mla/components/forms/numberInput.md`
- `conventions/development/frontend/core/mla/components/forms/passwordInput.md`
- `conventions/development/frontend/core/mla/components/forms/passwordStrength.md`
- `conventions/development/frontend/core/mla/components/forms/percentInput.md`
- `conventions/development/frontend/core/mla/components/forms/phoneInput.md`
- `conventions/development/frontend/core/mla/components/forms/pinInput.md`
- `conventions/development/frontend/core/mla/components/forms/radio.md`
- `conventions/development/frontend/core/mla/components/forms/radioField.md`
- `conventions/development/frontend/core/mla/components/forms/radioGroup.md`
- `conventions/development/frontend/core/mla/components/forms/rangeCalendar.md`
- `conventions/development/frontend/core/mla/components/forms/reactionPicker.md`
- `conventions/development/frontend/core/mla/components/forms/recurrenceEditor.md`
- `conventions/development/frontend/core/mla/components/forms/searchInput.md`
- `conventions/development/frontend/core/mla/components/forms/select.md`
- `conventions/development/frontend/core/mla/components/forms/slider.md`
- `conventions/development/frontend/core/mla/components/forms/stepper.md`
- `conventions/development/frontend/core/mla/components/forms/switch.md`
- `conventions/development/frontend/core/mla/components/forms/switchField.md`
- `conventions/development/frontend/core/mla/components/forms/tagsInput.md`
- `conventions/development/frontend/core/mla/components/forms/telInput.md`
- `conventions/development/frontend/core/mla/components/forms/textAreaInput.md`
- `conventions/development/frontend/core/mla/components/forms/textInput.md`
- `conventions/development/frontend/core/mla/components/forms/timeInput.md`
- `conventions/development/frontend/core/mla/components/forms/timePicker.md`
- `conventions/development/frontend/core/mla/components/forms/urlInput.md`
- `conventions/development/frontend/core/mla/components/forms/wizard.md`
- `conventions/development/frontend/core/mla/components/layout/appShell.md`
- `conventions/development/frontend/core/mla/components/layout/aspectRatio.md`
- `conventions/development/frontend/core/mla/components/layout/box.md`
- `conventions/development/frontend/core/mla/components/layout/center.md`
- `conventions/development/frontend/core/mla/components/layout/cluster.md`
- `conventions/development/frontend/core/mla/components/layout/container.md`
- `conventions/development/frontend/core/mla/components/layout/controlGroup.md`
- `conventions/development/frontend/core/mla/components/layout/divider.md`
- `conventions/development/frontend/core/mla/components/layout/flex.md`
- `conventions/development/frontend/core/mla/components/layout/frame.md`
- `conventions/development/frontend/core/mla/components/layout/grid.md`
- `conventions/development/frontend/core/mla/components/layout/hStack.md`
- `conventions/development/frontend/core/mla/components/layout/inline.md`
- `conventions/development/frontend/core/mla/components/layout/layout.md`
- `conventions/development/frontend/core/mla/components/layout/navbar.md`
- `conventions/development/frontend/core/mla/components/layout/overlay.md`
- `conventions/development/frontend/core/mla/components/layout/pullToRefresh.md`
- `conventions/development/frontend/core/mla/components/layout/resizablePanels.md`
- `conventions/development/frontend/core/mla/components/layout/scrollArea.md`
- `conventions/development/frontend/core/mla/components/layout/section.md`
- `conventions/development/frontend/core/mla/components/layout/spacer.md`
- `conventions/development/frontend/core/mla/components/layout/stack.md`
- `conventions/development/frontend/core/mla/components/layout/surface.md`
- `conventions/development/frontend/core/mla/components/layout/twoColumn.md`
- `conventions/development/frontend/core/mla/components/layout/vStack.md`
- `conventions/development/frontend/core/mla/components/nav/breadcrumb.md`
- `conventions/development/frontend/core/mla/components/nav/commandPalette.md`
- `conventions/development/frontend/core/mla/components/nav/contextMenu.md`
- `conventions/development/frontend/core/mla/components/nav/dropdownMenu.md`
- `conventions/development/frontend/core/mla/components/nav/menu.md`
- `conventions/development/frontend/core/mla/components/nav/menubar.md`
- `conventions/development/frontend/core/mla/components/nav/nav.md`
- `conventions/development/frontend/core/mla/components/nav/navItem.md`
- `conventions/development/frontend/core/mla/components/nav/navigationMenu.md`
- `conventions/development/frontend/core/mla/components/nav/pagination.md`
- `conventions/development/frontend/core/mla/components/nav/scrollSpy.md`
- `conventions/development/frontend/core/mla/components/nav/tableOfContents.md`
- `conventions/development/frontend/core/mla/components/overlays/actionSheet.md`
- `conventions/development/frontend/core/mla/components/overlays/alertModal.md`
- `conventions/development/frontend/core/mla/components/overlays/backdrop.md`
- `conventions/development/frontend/core/mla/components/overlays/bottomSheet.md`
- `conventions/development/frontend/core/mla/components/overlays/drawer.md`
- `conventions/development/frontend/core/mla/components/overlays/hoverCard.md`
- `conventions/development/frontend/core/mla/components/overlays/modal.md`
- `conventions/development/frontend/core/mla/components/overlays/overlays.md`
- `conventions/development/frontend/core/mla/components/overlays/popover.md`
- `conventions/development/frontend/core/mla/components/overlays/tour.md`


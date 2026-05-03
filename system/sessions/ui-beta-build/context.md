# ui-beta-build context

*Last updated: 2026-05-03*

## Current phase

**P3 — Base layer build-out** (L3 atoms ✅ + theme ✅ + L4 molecules ✅. L5 organisms next.)

## Last action

2026-05-03 — P5 external library audit (initial walk) landed: [`docs/audits/library-references.md`](../../../docs/audits/library-references.md). Walked Radix · shadcn · Mantine · MUI · Ark · React Aria (~340 components combined) → master matrix → 29 net-new additions to P3 (2 L2 · 1 L3 · 10 L4 · 16 L5) + skip list with rationale. Roadmap P5 marked done. Per direction: P4 haven audit deferred until layer build-out complete (initial L5 work), before P6 iteration.

2026-05-03 — L4 molecule build-out landed: 57 new components across 6 domains (incl. new `nav/` domain). Plus `useClipboard` hook in L1, `nav` slot in eslint+tsup+package exports, architecture doc updated to formalize "L4 may compose other L4s in same domain". All four pipelines (typecheck / lint / build / storybook) green.

## Live state

- Latest published: `@wow-two-beta/ui@0.0.7` (CI auto-bumps `0.0.y` per push; pre-L4-build was 0.0.6)
- Storybook: https://wow-two-sdk-beta.github.io/wow-two-sdk-beta.ui/ (light/dark toggle in toolbar)
- **Components shipped: 49 atoms + 57 molecules + 13 primitives = 119 building blocks**
  - **L3 atoms (49):** actions (3) · display (11) · feedback (7) · forms (17) · layout (11)
  - **L4 molecules (57):**
    - **actions (8):** ButtonGroup, ToggleButton, ToggleButtonGroup, SegmentedControl, FAB, CopyButton, DisclosureButton, OverlayButton
    - **display (15):** Card, AvatarGroup, Tooltip, EmptyState, Stat, Snippet, NotificationDot, CountBadge, Status, KeyboardShortcut, DescriptionList, InfoRow, BadgeOverlay, SectionHeader, Highlight
    - **feedback (10):** Alert (slotted), Banner (slotted), Toast (slotted), Callout, InlineSpinner, LoadingState, ProgressSteps, StatusIndicator, MeterBar, TrendIndicator
    - **forms (17):** FormField, CheckboxField, RadioField, SwitchField, CheckboxGroup, RadioGroup, PinInput, MaskedInput, CurrencyInput, PercentInput, CharacterCount, InputAddon, InputGroup, LabeledInput, ChoiceCard, PasswordStrength, FilePicker
    - **layout (4):** Inline, Cluster, Frame, TwoColumn
    - **nav (3):** Breadcrumb, Pagination, NavItem
  - **L2 primitives (13):** Slot, Portal, VisuallyHidden, Presence, DirectionProvider, AccessibleIcon, FocusScope, DismissableLayer, AnchoredPositioner, RovingFocusGroup, Collection, FormControlContext, ScrollLockProvider
- Stack: **Tailwind v4** + `@tailwindcss/vite` plugin · CSS vars source-of-truth · `tailwind-merge@^3` · `tailwind-variants@^0.3` · DTS via `tsc --emitDeclarationOnly`
- Foundation utils (6): `cn`, `composeRefs`, `composeEventHandlers`, `dataAttr`, `tv`, polymorphic types
- Foundation hooks (11): `useControlled`, `useDisclosure`, `useId`, `useEventListener`, `useOutsideClick`, `useEscape`, `useFocusTrap`, `useScrollLock`, `useResizeObserver`, `useMediaQuery`, **`useClipboard`** (new this round)
- Deps: `@radix-ui/react-focus-scope`, `@floating-ui/react`, `lucide-react`
- Subpath exports: `./utils`, `./hooks`, `./icons`, `./primitives`, `./actions`, `./display`, `./feedback`, `./forms`, `./layout`, **`./nav`**, `./styles.css`
- CI: green; auto-bumps `0.0.y` on push

## Decisions locked

- **Layer model:** L0 tokens · L1 utils/hooks/icons · L2 primitives · L3 atoms · L4 molecules · L5 organisms · L6 patterns · L7 domain. ESLint `boundaries` enforces foundation-vs-domain.
- **Atom rule (convention, not lint-enforced):** L3 atoms never compose other atoms — atom-on-atom = L4.
- **L4 may compose other L4s within the same domain.** ESLint `same-domain` boundary covers this. Convention: composition inside a domain is fine; cross-domain composition still forbidden.
- **`nav/` is a 6th domain** for wayfinding components (Breadcrumb, Pagination, NavItem now; Tabs/Accordion/Menu/Sidebar at L5+).
- **Severity components ship in pairs:** `*Simple` atomic at L3 + slotted `*` at L4 (Alert/Banner/Toast).
- **Inputs split by type** rather than one `Input` with `type` prop.
- **Polymorphism rule:** layout atoms use `as` prop; interactive atoms use `Slot`/`asChild`.
- **Same-domain shared styles allowed** via `_styles.ts` underscore-prefixed file.
- **No SSR. Pure CSR.** Package targets browser-only consumers.
- **Tailwind v4 + CSS-first config.** `@theme {}` in `src/index.css` is source of truth.
- **Theme vocabulary = shadcn-aligned** (24 semantic tokens). Raw scales preserved as escape hatch.
- **Dark mode = `.dark` class on body/html.** Component classes never use `dark:` modifiers.
- **Theming reference doc:** `docs/theming.md`.
- **L4 API conventions locked:**
  - **Card** — compound (`Card.Header/Title/Description/Body/Footer`).
  - **Tooltip** — single child trigger; portaled content; default delays 700ms open / 0ms close.
  - **Alert / Banner / Toast slotted** — same prop shape: `{ icon, title, description, actions, onClose }`.
  - **FormField** — props-driven (`label`, `helper`, `error`, `isRequired`); single-control child.
  - **`useClipboard` hook** — added to L1 (used by `CopyButton`, `Snippet`).
  - **Generic `OverlayButton` + `BadgeOverlay`** at our L4 (haven's bespoke `*Overlay*` variants will eventually consume these).

## Open items

- **Commit L4 build + P5 audit** — current diff = `useClipboard` + nav domain infra + 57 L4 components + arch doc update + `docs/audits/library-references.md` + roadmap P5 update + this context update. Push triggers `0.0.8`.
- **P4 Haven audit** — deferred per direction until layer build-out complete (initial L5 work), before P6 iteration. Will produce `wow-two-ws/docs/audits/haven-component-gaps.md`.
- **L5 selection (next conversation):** organisms — Modal, AlertDialog, Drawer, Popover, HoverCard, Menu, ContextMenu, CommandPalette, Combobox, Select, MultiSelect, DatePicker, TimePicker, ColorPicker, FileUpload (Dropzone), TagsInput, RichTextEditor, Tabs, Accordion, Stepper (with state), Toaster (manager), Table, List, Tree, Carousel, ResizablePanels, Splitter. Strong haven priorities: Select, MultiSelect, Collapsible (DisclosureButton's stateful counterpart), DataTable, FloatingBar.
- **P5-derived additions** (from `library-references.md`):
  - **L2:** Announce (a11y live region), OverlayArrow.
  - **L3:** NativeSelect.
  - **L4:** Form (root), List, OverflowList, Calendar, DateField, TimeField, ColorField, ColorSwatch, RangeSlider, Rating.
  - **L5 (append to candidate list above):** Listbox, Menubar, NavigationMenu, Toolbar, DateRangePicker, RangeCalendar, ColorArea, ColorWheel, ColorSlider, ColorSwatchPicker, Disclosure (state-managed), Backdrop, LoadingOverlay, Editable, Timeline, advanced List, SpeedDial.
- **L4 deferred to P6 refactor:** RovingFocus arrow-key nav for `ToggleButtonGroup`, `CheckboxGroup`, `RadioGroup` (currently rely on default Tab focus order — works, but lacks the arrow-key polish a11y patterns expect).
- **NavSection / Sidebar (haven's `sidebarSection`) → L6** as confirmed — modal-from-left expandable pattern; not L4.

## Parked

- NuGet stub publish (`Wow.Two.Sdk.Beta.Placeholder`) — `car-t-007`, scheduled 2026-05-02
- L3 + L4 stories: minimal coverage (default + key states); rich variant matrices deferred to P6
- L3 + L4 specs: terse format (Purpose + Props + Dependencies); fuller anatomy/states sections deferred to P6

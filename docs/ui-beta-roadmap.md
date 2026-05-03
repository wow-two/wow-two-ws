# `@wow-two-beta/ui` roadmap

*Last updated: 2026-05-03*

> **Scope**: Track B execution beyond the launch — the plan for actually building `@wow-two-beta/ui` into a real, broadly useful component library.
>
> **Source goal**: `car-wow-two-beta-launch` (10x-ws Q2 2026)
> **Linked task**: `car-t-004` (Track B operational)
> **Repo**: `workbench/wow-two-sdk-beta/wow-two-sdk-beta.ui/`
> **Live**: [`@wow-two-beta/ui`](https://www.npmjs.com/package/@wow-two-beta/ui) · [Storybook](https://wow-two-sdk-beta.github.io/wow-two-sdk-beta.ui/)

---

## Philosophy

**YAGNI does NOT apply here.** Build base components broadly — coverage beats minimalism. Beta-forever lets us iterate fast; missing components are friction every consumer feels. Build before need; refactor as patterns emerge.

---

## Phase index

| Phase | Title | Status | Primary deliverable |
|---|---|---|---|
| P1 | Component layering analysis | ✅ done (2026-04-29) | 8-layer model in repo `docs/architecture.md`; `primitives/` foundation slot added |
| P2 | Shell setup (theme, dark mode, focus, motion) | ✅ done (2026-05-03) | Tailwind v4 + 24 semantic tokens in `@theme`; `.dark` overrides; Storybook toolbar toggle; `docs/theming.md` reference |
| P3 | Base layer build-out (max coverage) | L3 atoms ✅ (49) · L4 molecules ✅ (57) · L5 organisms next | ~60–90 components across 6 role groups |
| P4 | Haven audit | scheduled after layer build-out (initial work) — before P6 iteration | Gap list — components haven uses but beta lacks |
| P5 | External library audit | ✅ initial walk done (2026-05-03) — re-walk before P6 | Reference list from Radix · shadcn · Mantine · MUI · Ark · React Aria |
| P6 | Refactor pass | blocked on P3–P5 | Shared utils/hooks extracted, naming/variants normalized |
| P7 | Haven migration | blocked on P6 | Haven imports come from `@wow-two-beta/ui`; inline copies retired (= `car-t-006`/Track D) |

P1 → P2 → P3 are sequential. P5 ran first walk during P3 (2026-05-03); P4 runs once L5 initial build-out lands. P6 lands once base layer is broad. P7 is final.

---

## P1 — Component layering analysis

**Why first**: Before building 40+ components, we need a precise layer model so we know what imports what. The current `docs/architecture.md` says "foundation vs domain" — that's the minimum. Composite components (Card = Stack + Heading + Body; Modal = Overlay + Box + Stack + Button) need a clearer home.

**Open questions to resolve**:
- Is there a "primitives" layer below "components" (à la Radix)?
- Do we need a "patterns" layer above (à la Mantine `Pattern`s)?
- Compound components (`Tabs.Trigger`, `Tabs.Content`) — flat or nested?
- Where does `Card` live — `display/` or its own `composite/` group?
- Polymorphic components (`as` prop / `asChild`) — when allowed?

**Tasks**:
- [ ] Survey Radix, shadcn/ui, Mantine, Ark — extract their layering models
- [ ] Synthesize 3- or 4-layer model for our package
- [ ] Update repo's `docs/architecture.md` with model + diagram + examples
- [ ] Update `eslint.config.js` boundary rules to enforce the model
- [ ] Document polymorphism rule (when `asChild` is OK)

**Deliverable**: PR that updates `docs/architecture.md` and `eslint.config.js` in the repo.

---

## P2 — Shell setup

**Why second**: Without theme + dark mode + focus + motion baselines, every component hardcodes visuals → impossible to refactor uniformly. Establish the contract once.

**Open questions to resolve**:
- Theme strategy: CSS-variables (Mantine/Radix-style) or Tailwind `class="dark"` (shadcn-style)?
- Dark mode toggle mechanism in consumer apps
- How a consumer overrides theme tokens (preset extension? CSS-var override?)
- Default theme location: `tokens/theme/` or `theme/`?
- Reset / normalize CSS — bundled into `index.css` or separate import?
- Focus ring system — utility class or per-component variant?
- Motion primitives — Framer Motion adapter or pure CSS transitions?

**Tasks**:
- [ ] Pick theme strategy + write `docs/decisions/001-theming.md` ADR
- [ ] Implement default light + dark themes in `tokens/`
- [ ] Add theme toggle to `.storybook/preview.ts` (toolbar global)
- [ ] Build focus ring utility (consumed by every interactive component)
- [ ] Define motion primitives (`tokens/motion`) — durations + easings
- [ ] Verify Button + 1-2 sample components reflow correctly across themes

**Deliverable**: Storybook page showing live light/dark toggle on existing components; ADR committed.

---

## P3 — Base layer build-out (max coverage)

**Why third**: With layers + shell defined, build broadly. YAGNI suspended.

**Sources to pull from**: haven, Radix, shadcn/ui, Mantine, MUI, Ark UI, Park UI, React Aria.

### Initial target list (will grow)

#### actions/
- Button ✅
- IconButton
- ToggleButton
- ButtonGroup
- Link

#### display/
- Avatar / AvatarGroup
- Badge
- Card
- Tag / Chip
- Tooltip
- Code / Kbd
- Image
- Icon (wrapper around lucide / heroicons / custom)

#### feedback/
- Alert / Banner
- Toast (system)
- Skeleton
- Spinner / Loader
- ProgressBar
- ProgressCircle
- EmptyState

#### forms/
- Input (text · email · password · number variants)
- Textarea
- Select
- Combobox
- MultiSelect
- Checkbox + CheckboxGroup
- Radio + RadioGroup
- Switch
- Slider
- DatePicker · TimePicker · DateRangePicker
- FileUpload / Dropzone
- FormField (label + error + hint wrapper)
- Search
- ColorPicker

#### layout/
- Box
- Stack (HStack, VStack)
- Grid
- Container
- Divider / Separator
- AspectRatio
- ScrollArea
- Tabs
- Accordion
- Modal / Dialog
- Drawer / Sheet
- Popover
- Menu / DropdownMenu
- ContextMenu
- Breadcrumb
- Pagination
- Stepper
- Timeline

**Total: ~60 components.** Realistic, not aspirational — most have direct precedents in haven and major libraries.

**Working pattern per component**:
1. `{Component}.spec.md` first (fills `docs/component-standard.md`)
2. `{Component}.tsx` implements spec
3. `{Component}.variants.ts` for tailwind-variants
4. `{Component}.stories.tsx` covers every visual state
5. `index.ts` barrel
6. Push to main → CI auto-publishes

**Tasks**:
- [ ] Refine target list (add anything missed)
- [ ] Order list by dependency depth (leaves first)
- [ ] Build, push, repeat
- [ ] Track progress here — strike through completed items

---

## P4 — Haven audit

**Trigger**: P3 ~80% complete.

**Process**:
1. Walk `workbench/ventures/10x-ven-haven/platform/src/frontend-services/packages/ui/src/components/`
2. List every component
3. For each: equivalent in `@wow-two-beta/ui`? Yes / partial / missing
4. Gaps → append to P3 target list, build them

**Deliverable**: `wow-two-ws/docs/audits/haven-component-gaps.md` (created when P4 starts).

---

## P5 — External library audit

**Status**: ✅ initial walk done 2026-05-03 — [`docs/audits/library-references.md`](audits/library-references.md).

**Process**: Walk component lists from Radix · shadcn · Mantine · MUI · Ark · React Aria. For each:
- Useful for wow-two ecosystem? Y/N
- Missing from beta? Y/N
- If both yes → add to P3.

**Outcome (first walk)**:
- 2 new L2 primitives (Announce, OverlayArrow)
- 1 new L3 atom (NativeSelect)
- 10 new L4 molecules (Form root, List, OverflowList, Calendar, DateField, TimeField, ColorField, ColorSwatch, RangeSlider, Rating)
- 16 new L5 organisms (Listbox, Menubar, NavigationMenu, Toolbar, DateRangePicker, RangeCalendar, ColorPicker + 4 building blocks, Disclosure, Stepper-stateful, Backdrop, LoadingOverlay, Editable, Timeline, advanced List, SpeedDial)
- L5 candidate list confirmed (no removals from prior list)
- Skip list captured with rationale

**Re-walk**: snapshot in time; rerun before P6 to catch library additions.

**Deliverable**: [`docs/audits/library-references.md`](audits/library-references.md).

---

## P6 — Refactor pass

**Trigger**: P3–P5 settled, ~50+ components shipped.

**Process**:
- Re-read every component
- Extract duplicate logic to `utils/` or `hooks/`
- Normalize prop naming (e.g., `size` vs `density`)
- Unify variant scales (`sm/md/lg` everywhere — no `small/medium/large` anywhere)
- Audit accessibility attributes — fix gaps
- Audit polymorphism — apply consistently per P1's rule

**Risk**: Breaking changes. But beta-forever — fix-forward in haven during P7.

**Deliverable**: Cleaner package + shared abstractions in `utils/` + `hooks/`.

---

## P7 — Haven migration

**Trigger**: P6 done. **This is `car-t-006` / Track D in `beta-launch.md`.** Two views of the same work — keep them in sync.

**Per-component migration**:
1. Find all import sites of haven's local copy
2. Replace with `@wow-two-beta/ui` import
3. Verify visually + functionally
4. Delete haven local copy
5. Commit

**Order**: leaves of haven's dependency graph first, then composites. One commit per component is fine.

---

## Working notes

- Each phase can own a dedicated chat — naming pattern: `wow-two - ui-beta-P{N}-{slug}` (e.g. `wow-two - ui-beta-P1-layering`)
- Components added to P3 mid-build: append at the bottom of the relevant role-group bullet list
- This file is the single source of phase truth — update status / strike completed items here, not elsewhere
- For component-level granular progress, use Storybook itself as the catalog

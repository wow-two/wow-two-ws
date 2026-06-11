# ui-beta-build context

*Last updated: 2026-05-19 — Select/Listbox K/V generics + searchable + clearable + isLoading*

## Select / Listbox generic refactor (2026-05-19)

In support of haven migration — `<SelectInput>` → `<Select>`. Lib now supports complex value types via unconstrained generic + equality comparer.

### Listbox (`src/forms/listbox/Listbox.tsx`)

- `<Listbox<T = string>>` — value is any T, no string-only constraint
- `isEqual?: (a: T, b: T) => boolean` — defaults to `Object.is`
- Single mode: `value?: T`, `defaultValue?: T`, `onValueChange?: (v: T | undefined) => void` (undefined = no selection)
- Multi mode: `value?: T[]`, `defaultValue?: T[]`, `onValueChange?: (v: T[]) => void`
- `ListboxItem.value: unknown` (typed at call site, compared via parent's `isEqual`)
- forwardRef + generic preserved via `as` cast pattern

### Select (`src/forms/select/Select.tsx`)

- `<Select<T = string>>` — fully generic value
- `null` = explicitly cleared · `undefined` = uncontrolled (per `useControlled` convention)
- New props on root: `clearable`, `isLoading`, `isEqual`, `serialize` (for form `name` hidden input)
- New props on `Select.Content`: `searchable`, `searchPlaceholder`, `noResultsLabel`
- `Select.Item` has `value: unknown` + optional `text?: string` (override search-filter text — defaults to extracted from children)
- Trigger: X clear button (when `clearable && hasValue`), Loader2 spinner (when `isLoading`), Chevron otherwise
- Composes existing `<SearchInput>` (size="sm", clearable, autofocus) inside `SelectContent` when `searchable`
- Recursive `extractText(ReactNode)` for search filtering — works on string/number/array/element children
- `isEqual` and `serialize` ref-stabilised internally (so consumers can pass inline fns without churn)

### MultiSelect (`src/forms/multiSelect/MultiSelect.tsx`)

- Adapted to new Listbox API: `<Listbox<string> multiple value={ctx.values} onValueChange={ctx.setValues}>`
- Kept string-only value (no generic surface yet — defer until haven's MultiSelect migration)
- Inlined `MultiSelectItemProps` (no longer re-exporting weakened `ListboxItemProps`)

### Stories

- `Select.stories.tsx` — added Searchable, Clearable, Loading, GenericObject (User type with isEqual by id)
- `Listbox.stories.tsx` — added GenericObject demo
- Existing stories updated for `string | null` value typing

### Build status

- `pnpm typecheck` ✅
- `pnpm lint` ✅ (clean — ref-stabilised callbacks)
- `pnpm build` ✅
- `pnpm build:storybook` ✅
- **Awaiting user push for CI to publish next `0.0.x`**

### Migration path for haven `<SelectInput>` → `<Select>`

Old (haven):
```tsx
<SelectInput<string, PropertyType>
  options={[{ key: 'a', value: PropertyType.A, label: 'A', meta: 3 }]}
  selected={'a'}
  onChange={(sel, action) => setX(sel?.value ?? null)}
  searchable showClearButton loading
/>
```

New (lib):
```tsx
<Select<PropertyType>
  value={selectedPropertyType}
  onValueChange={setSelectedPropertyType}
  clearable isLoading={loading}
>
  <Select.Trigger><Select.Value placeholder="All" /></Select.Trigger>
  <Select.Content searchable>
    {opts.map(o => (
      <Select.Item key={o.value} value={o.value} disabled={o.count === 0}>
        {o.label}
        {o.count != null && <span className="ml-auto text-subtle-foreground">{o.count}</span>}
      </Select.Item>
    ))}
  </Select.Content>
</Select>
```



## Quick state

- **Library**: `@wow-two-beta/ui`, beta-forever, no SSR (CSR only).
- **Latest published**: `0.0.23` (batch 14 — specialty inputs).
- **Pending push**: `0.0.24` (batch 15 — communication / collab).
- **Building blocks shipped**: ~227 (214 + 13 communication/collab from batch 15). Recount per-domain via `ls src/{domain}/` if exact numbers needed.
- **Domains**: `actions / display / feedback / forms / layout / nav / overlays`. Foundation: `tokens / tailwind / utils / hooks / icons / primitives`.
- **External deps**: `@floating-ui/react`, `@radix-ui/react-focus-scope`, `lucide-react`, `marked`, `clsx`, `tailwind-merge`, `tailwind-variants`.

## Convention update (2026-05-04)

Per-component file convention simplified: build code + stories + barrel only. Drop `*.spec.md` and `*.standard.md` during build batches — those land in the per-component standardization pass (separate chat per component, later phase). The repo `CLAUDE.md` now reflects this.

> Many components shipped in earlier batches still have a legacy `*.spec.md` file. They'll be rewritten (or replaced by the dual-doc pair) during the standardization pass. **Don't author new specs during build.**

## Standardization pilot — Button complete (2026-05-05)

The Button pilot ran in a separate chat and locked the patterns every future per-component standardization chat must follow. **Read `docs/common-standards.md` first** in any standardization chat — it's the single source of truth for cross-cutting rules.

### Files created during pilot (now part of foundation)

| File | What it provides |
|---|---|
| `docs/templates/component-standard.md` | Skeleton for `*.standard.md` files (Subject Philosophy + RFC 2119 spec + DR + Related) |
| `docs/templates/component-spec.md` | Skeleton for `*.spec.md` files (concrete API: enums, prop tables, anatomy) |
| `docs/common-standards.md` | Project-wide conventions — Common.1–9 (comments, naming, displayName, magic-value extraction) |
| `src/utils/CssExtensions.ts` | `CssExtensions.{toCss, resolvePadding, resolveRadius, resolveBoxSize}` + `PaddingProp` / `RadiusProp` / `SizeValue` / `BoxSizeOverrides` types |
| `src/utils/OptionalExtensions.ts` | `OptionalExtensions.from(condition, value)` — DOM-attribute conditional helper |
| `src/utils/PressExtensions.ts` | `PressEvent<T>` type + `PressExtensions.longPressDelay.{min, max, default}` |
| `src/utils/HtmlExtensions.ts` | `HtmlElement.{Button, Anchor, Span, Div}` + `ButtonType.{Button, Submit, Reset}` |
| `src/utils/KeyboardExtensions.ts` | `Key.{Space, Enter, Escape, Tab, Backspace, Delete, Home, End, PageUp, PageDown, Arrow*}` |
| `src/hooks/useDebounceHandler.ts` | Generic event-handler throttle (first-call-wins; subsequent within window get `preventDefault()`) |
| `src/icons/Spinner.tsx` | Lucide `Loader2` + `animate-spin` + `1em` sizing — replaces inline SVG |

### Conventions established (apply to every standardization pass)

| # | Rule | Example |
|---|---|---|
| 1 | Boolean props use `is*` prefix — including shadowing native HTML attrs | `isDisabled` (forwards to native `disabled`), `isLoading`, `isSkeleton`, `isFullWidth`, `isMultiline` |
| 2 | `ReactNode` slot props use `*Slot` suffix | `leadingSlot`, `trailingSlot`, `loadingSlot` |
| 3 | Top-of-file JSDoc: one line OR omit entirely | `/* Slim wrapper around Button — variant=glass + shape=circle. */` |
| 4 | Prop comments: single-line `/* */` (NOT JSDoc), blank line between props | (see Button.tsx) |
| 5 | Don't name downstream consumers in comments | "Used by Button" → ❌ |
| 6 | `COMPONENT_NAME` const drives `displayName` + console-warn prefixes | `const COMPONENT_NAME = 'Button';` |
| 7 | Magic strings/numbers in type+default → extract to `*Extensions.ts` (shared) or local `as const` (component-specific) | `ButtonType.Button` (shared), `ButtonDataState.Loading` (local) |
| 8 | Numeric prop ranges → validate at runtime + console-warn + fall back to default | `longPressDelay` validated against `PressExtensions.longPressDelay.{min, max}` |
| 9 | Mutual exclusion → emit dev warning + pick a winner | `isLoading` ⊥ `isSkeleton` → skeleton wins |
| 10 | Press / long-press / debounce → use `useButtonInteractivity` pattern (private hook in component file) — extract to `src/hooks/` if a 2nd component needs it | (see Button.tsx) |
| 11 | DOM attribute defaulting → `OptionalExtensions.from(cond, value)` | `disabled={OptionalExtensions.from(isDisabled, true)}` |
| 12 | User-handler chaining → `composeEventHandlers(theirs, ours)` | onPointerDown wiring |

### Button surface (final state — reference for sibling button-family components)

- **Style**: 7 variants × 5 tones (`solid · soft · surface · outline · ghost · link · glass` × `primary · neutral · danger · success · warning`)
- **Size**: 5 presets × density CSS-var hook (`xs · sm · md · lg · xl`, all height/padding via `calc(* var(--ui-density-scale, 1))`)
- **Spacing**: 4 sizing modes — preset+auto-padding · preset+manual-padding · manual-size · fixed-dimensions (`width / height / minWidth / minHeight`)
- **Shape**: `default | square | circle`
- **Slots**: `leadingSlot · trailingSlot · loadingSlot` (overrides built-in Spinner)
- **States**: `default · hover · focus-visible · active · disabled · loading · skeleton` — `data-state="loading|skeleton|disabled"`
- **Interaction**: `onPressStart · onPressEnd · onLongPress (+ longPressDelay) · debounceMs` plus native event passthrough
- **Polymorphism**: `asChild` via `Slot`
- **A11y**: `forced-colors` border + `prefers-reduced-motion` + WCAG 2.2 SC 2.5.8 hit target + `aria-busy`/`tabIndex` for skeleton

### Storybook structure (template for future standardizations)

Functional grouping: `Actions/Button/Playground` + `Actions/Button/Matrix` + `Actions/Button/Recipes`. Files: `Button.stories.tsx` (Playground only — argTypes), `Button.matrix.stories.tsx` (programmatic grids via `.storybook/grid.tsx` `Grid` + `Row` helpers), `Button.recipes.stories.tsx` (named real-world combos). Pseudo-state addon (`storybook-addon-pseudo-states@4.0.4`) installed for hover/focus/active visualization across matrices.

### Next standardization candidate (recommended order)

After Button, the natural sequence in the actions domain (per the consolidation analysis from the pilot):

1. ~~**OverlayButton**~~ — **DELETED 2026-05-07.** Extracted `<Overlay>` layout primitive (`src/layout/overlay/`), composed it with `<Button variant="glass" shape="circle">` at the call site. See "Overlay extraction" section below.
2. ~~**IconButton**~~ — **DELETED 2026-05-07.** Pure preset surface (5 variants × 4 sizes × 2 shapes), all of which Button already provides via `variant × tone × size × shape`. Replace consumers with `<Button shape="square">` or `<Button shape="circle">`. See "IconButton deletion" section below.
3. ~~**CopyButton**~~ — **STANDARDIZED 2026-05-07.** Slim wrapper around Button + `useClipboard` — kept (real new behavior: clipboard write + transient `copied` state + error path). Added `data-copied="true"` observable, `onError` callback, `copiedAriaLabel` for i18n discipline, required `aria-label`. See "CopyButton standardization" section below.
4. **FAB** — slim to Button wrapper (`<Button shape="circle" size="lg">` + position className). **DEFERRED** — haven migration first to validate Button in production (per session direction 2026-05-07).
5. **ToggleButton** — slim. Adds `pressed` state via `useControlled`. Reuse Button's variant×tone matrix.
6. **DisclosureButton** — slim. Adds `open` state + auto chevron in `trailingSlot`.
7. **BackToTopButton** — slim. Adds scroll-detection logic.
8. **ButtonGroup** / **ToggleButtonGroup** / **SegmentedControl** / **Toolbar** / **SpeedDial** / **Link** — keep as-is, just standardize.

Each future standardization chat: open `common-standards.md` → open the targeted component → walk Button's standard/spec as a reference → produce the docs + apply the conventions to the component code → verify pipelines → push.

## Overlay extraction (2026-05-07)

Standardization pass 2: instead of standardizing `OverlayButton` as a slim wrapper, the analysis showed it added zero behavior beyond preset bundling (`variant="glass" + shape="circle" + size="sm" + tone="neutral"`) plus two layout axes (`position`, `appearOn`). Layout axes don't belong in an action atom. Extracted to a layout primitive that works with **any** child component.

### What landed

| File | Purpose |
|---|---|
| `src/layout/overlay/Overlay.tsx` | Slot-based layout primitive — positioning + visibility + transitions |
| `src/layout/overlay/Overlay.variants.ts` | tailwind-variants config — 9 positions × 4 visibility modes × 7 transitions, with `motion-reduce:` safety in compound variants |
| `src/layout/overlay/Overlay.standard.md` | Behavioral contract — RFC 2119 spec rules + DR + Related |
| `src/layout/overlay/Overlay.spec.md` | Concrete API — anatomy, axes, props, composition, non-goals |
| `src/layout/overlay/Overlay.stories.tsx` | Playground + 9 named stories covering every mode |
| `src/layout/overlay/index.ts` | Barrel |

Reused: existing `<Presence>` foundation primitive (`src/primitives/presence/`) — no new `usePresence` hook needed. `<Overlay>` wraps in `<Presence>` automatically when `isOpen` is provided.

### What was deleted

- `src/actions/overlayButton/` (4 files) — Button + `<Overlay>` composition replaces it.
- `export * from './overlayButton'` line in `src/actions/index.ts`.
- Updated Button.spec.md "Image-overlay buttons" composition example to use `<Overlay>`.
- Updated Button.recipes.stories.tsx `GlassOverlay` recipe to use `<Overlay>`.

### Overlay surface (lock for future per-component standardizations)

- **Position**: 9-value preset (`top-right · top-left · bottom-right · bottom-left · top · bottom · left · right · center`) OR raw inset object `{ top?, right?, bottom?, left? }`. Mirrors Button's `padding: PaddingToken | { x, y }` pattern.
- **Inset**: `SizeValue` override for preset spacing (default `'0.5rem'`). Driven via `--ui-overlay-inset` CSS variable.
- **Visibility (`appearOn`)**: `'always' | 'hover' | 'focus-within'`. Hover/focus-within require parent `className="group"` (documented; runtime check deferred).
- **Presence (`isOpen`)**: optional. When set, wraps in `<Presence>`; emits `data-state="open|closed"`; defers unmount until `transitionend`.
- **Transitions**: `'none' | 'fade' | 'fade-scale' | 'fade-slide-{up|down|left|right}'`. Auto-defaults to `'fade'` when any visibility gating is active. Every transform-bearing variant strips its transform under `motion-reduce:` (Tailwind modifier; codified in compound variants).
- **Asymmetric durations**: `transitionDuration: number | { enter, exit }`. Pure-CSS via two CSS variables (`--ui-overlay-enter`, `--ui-overlay-exit`); no JS state machine.
- **Polymorphism**: `asChild` defaults to `true` (Slot-based merge onto child) — primary use is overlaying an existing element. `asChild={false}` renders a positioning `<div>`.
- **z-index**: default 10; override via `zIndex` prop.

### Decisions locked during this pass

| # | Decision |
|---|---|
| 21 | Slim wrappers that add NO new behavior (only preset bundling) get deleted, not standardized. Wrappers that add real new axes (FAB, ToggleButton, DisclosureButton, BackToTopButton) get slimmed + standardized. |
| 22 | Layout concerns (positioning, visibility gating, mount/unmount transitions) belong in layout primitives, not action components. |
| 23 | Reuse foundation `<Presence>` primitive instead of duplicating presence logic. Same pattern applies to future Dialog/Drawer/Tooltip/Menu/Popover/Toast standardizations. |
| 24 | `motion-reduce:` Tailwind modifier is codified inside the variants config (compound variants), not in consumer-side branching. Consumers can't accidentally bypass reduced-motion safety. |
| 25 | Asymmetric durations via CSS variables, not JS state. Keeps motion on the compositor thread. |

### Roadmap note (added to `targets.md` + `ideas.md`)

- **FLIP / animated layout shift** bumped from MAYBE → NEXT in `targets.md` 2.8 Motion. Concrete consumers: SortableList · NotificationCenter / ToastStack · TabIndicator slide · MasonryGrid · DataGrid row reorder · KanbanBoard column shift. Implementation: View Transitions API + `useFlip` hook + `<AnimatedLayout>` primitive fallback. Lands as its own primitive — not part of `<Overlay>`.
- **Spring physics** stays MAYBE — different motion model, JS-only. Earns its place when first drag-driven primitive (Drawer dismiss, swipeable carousel) needs interruption-aware momentum. CSS `ease-out` is a good-enough settle approximation for opacity+scale fades.

## IconButton deletion (2026-05-07)

Standardization pass 3 — same logic as OverlayButton (locked decision #21): a slim wrapper that adds NO new behavior beyond preset bundling gets deleted, not standardized. IconButton's surface (5 variants × 4 sizes × 2 shapes + required `aria-label`) is a strict subset of what Button already provides via `variant × tone × size × shape`.

### What was deleted

- `src/actions/iconButton/` (5 files: `IconButton.tsx`, `IconButton.variants.ts`, `IconButton.stories.tsx`, `IconButton.spec.md`, `index.ts`)
- `export * from './iconButton'` line in `src/actions/index.ts`

### Migration mapping for consumers

| Old IconButton API | New Button equivalent |
|---|---|
| `<IconButton variant="solid">` | `<Button shape="square" variant="solid">` |
| `<IconButton variant="soft">` | `<Button shape="square" variant="soft">` |
| `<IconButton variant="outline">` | `<Button shape="square" variant="outline">` |
| `<IconButton variant="ghost">` (default) | `<Button shape="square" variant="ghost">` |
| `<IconButton variant="danger">` | `<Button shape="square" variant="solid" tone="danger">` |
| `<IconButton shape="circle">` | `<Button shape="circle">` |
| `<IconButton size="xs/sm/md/lg">` | `<Button size="xs/sm/md/lg">` (Button also has `xl`) |
| `aria-label` (TS-required) | Documentation/lint level — Button doesn't TS-enforce, but icon-only Button still requires it for a11y (Button standard rule 12) |

### Doc/comment sweep

Mentions of IconButton replaced or removed in:

- `src/actions/button/Button.standard.md` — sibling list
- `src/actions/button/Button.spec.md` — Overlay-deletion historical note
- `src/actions/buttonGroup/ButtonGroup.spec.md` — purpose + dependencies
- `src/actions/toolbar/Toolbar.spec.md` — composition examples
- `src/layout/overlay/Overlay.spec.md` — example child-component list
- `src/forms/numberInput/NumberInput.tsx` + `.spec.md` — atom-rule rationale rewritten
- `src/display/badgeOverlay/BadgeOverlay.tsx` — example list

### Decisions reinforced

The OverlayButton + IconButton deletion pattern is now locked twice. **Slim wrappers that add zero new behavior get deleted; slim wrappers that add real new axes get standardized.** The actions-domain queue going forward (CopyButton through BackToTopButton) all add real new behavior (clipboard logic, toggle state, disclosure state, scroll detection) so they get standardized, not deleted.

## CopyButton standardization (2026-05-07)

First "real-logic slim wrapper" through the standardization template. Validates the kept-not-deleted branch: CopyButton manages clipboard write + transient success state + error path, none of which Button provides. The wrapper earns its place; rest is presentation, forwarded to Button.

### API changes (breaking — beta-forever, fix-forward)

| Change | From | To | Why |
|---|---|---|---|
| `aria-label` | optional, defaults to `'Copy'` | required at type level | i18n discipline (Button standard rule 19); icon-only buttons must be programmatically named |
| Hardcoded `'Copied'` swap | implicit | explicit via `copiedAriaLabel?: string` (optional, falls back to `aria-label`) | Same i18n discipline — consumer supplies all user-facing strings |
| Error handling | swallowed silently | `onError?: (error: Error) => void` callback, fires once per error transition | Consumers can surface failures (toast, retry, log) without try/catch around event handlers |
| Observable state | none | `data-copied="true"` while copied, absent otherwise | Test selectors, CSS overlays, analytics can target without prop drilling |
| Render-prop signature | `({ copied })` | `({ copied, error })` | Consumers can render error states inline if they want UI for it |
| Top-of-file comment | JSDoc `/**` style | plain `/* */` per Common.5 | Lint discipline |
| `displayName` | inline string `'CopyButton'` | `COMPONENT_NAME` const per Common.8 | Single source of truth |

### Why `data-copied` not `data-state="copied"`

Button reserves `data-state` for its own lifecycle states (`loading | skeleton | disabled` per Button standard rule 10). CopyButton's success state lives in a separate `data-*` namespace to avoid collision when both states are simultaneously active (e.g., a copying button mid-success-reset that's also showing skeleton). Both attributes can coexist on the same DOM node; CSS targets each independently.

### Once-per-transition `onError` semantics

Implemented via a ref-stabilized effect in CopyButton — consumer's `onError` callback can be re-passed unstably (anonymous arrow functions are fine) without re-firing on every render where `error` is set. Fires exactly once when `useClipboard`'s error state goes `null → Error`.

### Files

- `src/actions/copyButton/CopyButton.tsx` — code (rewritten with new conventions)
- `src/actions/copyButton/CopyButton.standard.md` — RFC 2119 spec (new — 16 numbered items + DR)
- `src/actions/copyButton/CopyButton.spec.md` — concrete API (rewritten from template)
- `src/actions/copyButton/CopyButton.stories.tsx` — Playground + recipes (broken `variant: 'secondary'` fixed; argTypes added)

### Pattern locked

CopyButton is now the canonical example of "slim wrapper around Button that adds real new behavior, kept and standardized." Future standardization passes (FAB, ToggleButton, DisclosureButton, BackToTopButton — when their turn comes) follow the same shape:

1. Slim implementation: wrap Button via `<Button {...rest}>`, add only the unique-to-this-component logic
2. Component-specific `data-*` attribute for observable state (avoid `data-state` collision)
3. Required props that enforce a11y at type level (e.g. `aria-label`)
4. i18n discipline — no hardcoded English strings; consumer supplies user-facing text
5. Callback-based opt-in for error/event handling, ref-stabilized to avoid effect-deps churn
6. Standard.md with RFC 2119 items + DR
7. Spec.md from template with anatomy + props + recipes + non-goals + inspirations

## Next session — start here (revised 2026-05-07)

Pivot to **haven migration** before continuing actions-domain standardization. Rationale: validate Button + Overlay + CopyButton in production before slimming the remaining wrappers. Real consumer feedback exposes API gaps that pure design can miss; better to find and fix them in `0.0.x` than to standardize four more wrappers in isolation.

**Haven migration scope (recommended first pass):**

1. Pull `@wow-two-beta/ui@0.0.33+` (next CI bump after this push)
2. Replace haven's text-button usages → `<Button>` (subpath: `@wow-two-beta/ui/actions`)
3. Replace haven's icon-only button usages → `<Button shape="square">` or `<Button shape="circle">`
4. Replace haven's image-overlay buttons → `<Overlay><Button variant="glass" shape="circle"/></Overlay>` (subpath: `@wow-two-beta/ui/layout` + `@wow-two-beta/ui/actions`)
5. Replace haven's copy-id / copy-link buttons → `<CopyButton>` with `aria-label` + (optional) `copiedAriaLabel`
6. Defer FAB / ToggleButton / DisclosureButton / BackToTopButton replacements until after haven validates the migrated set
7. Capture API gaps / friction in this context.md as fix-forward items for the lib

After haven validates Button + Overlay + CopyButton, return here to continue actions-domain standardization (FAB next, then ToggleButton / DisclosureButton / BackToTopButton, then ButtonGroup family).

## Pipeline (strategic compass)

1. **Capture all possible components** — done. `docs/analysis/ui-philosophy/ideas.md` §5 covers ~340 components across 35 categories.
2. **Capture all standards / browser APIs / patterns** — substantially in `ideas.md` §4 / §6 / §7 / §8. Gap-fill in a later pass.
3. **Build first-generation implementations** — *currently active*. ~227 components shipped across 15 batches. Remaining clusters: AI / chat, status / DevOps, DX / dev-tooling, marketing / landing, settings / admin, auth / privacy.
4. **Analyze & cross-reference** patterns × components. Output: per-component cross-cutting matrix (TBD format).
5. **Standardize each component** — per-component chats. Each adds `*.standard.md` + `*.spec.md`, fixes API drift, polishes styling, fixes Storybook render glitches. Pilot was Button in a separate chat.
6. **Haven audit** — `docs/audits/haven-component-gaps.md`. Mapped/partial/gap/deprecated against the inventory.
7. **Haven migration** — replace haven's inline UI with `@wow-two-beta/ui`.

This chat = step 3 (build batches). Steps 4–7 happen elsewhere.

## Next session — start here

1. **Verify batch-15 push** landed as `@wow-two-beta/ui@0.0.24`. If still `0.0.23`, ask user to push.
2. **Continue first-gen build batches.** Remaining clusters in suggested order:
   - **Batch 16+ — AI / chat** (~17 components): AIChatBubble · StreamingTextRenderer · ToolCallCard · ChainOfThoughtToggle · CitationFootnote · TokenUsageBar · ModelPicker · ParameterPanel · PromptSuggestionChip · ConversationList · BranchPicker · RegenerateButton · FeedbackVote · AgentTrace · ArtifactRenderer · MultimodalUpload · WelcomeSuggestions.
   - **Batch 17+ — Status / DevOps** (~10): StatusBoard · IncidentBanner · BuildList · LogStream · LogTable · StackTraceViewer · MetricSparkline · AlertCard · DeploymentTimeline · TraceViewer.
   - **Batch 18+ — DX / dev-tooling** (~8): DebugPanel · InspectorPanel · LayersPanel · PropertiesPanel · A11yPanel · ColorContrastChecker · ColorBlindnessSimulator · DeviceFrame.
   - **Batch 19+ — Marketing / landing** (~10, lower priority): Hero · FeatureGrid · BentoGrid · PricingTable · ComparisonTable · TestimonialCard · LogoCloud · TeamSection · CookieBanner · NewsletterForm.
   - **Batch 20+ — Settings / admin** (~10): PermissionsMatrix · RoleSelector · InviteByEmail · TeamMemberList · AccountSwitcher · APIKeyManager · SecretInput · AuditLog · WebhookManager · IntegrationCard.
   - **Batch 21+ — Auth / privacy** (~10, semi-domain-specific): SignInForm · SignUpForm · SocialSignInRow · MagicLinkSentState · TOTPSetup · PasskeyEnroll · ResetPasswordForm · ConsentForm · CookiePreferences · GDPRRequestForm.
   - **Beyond**: Education/quiz, commerce, maps, 3D — domain-specific, evaluate need before building.
3. **Each batch**: pick simplest → most complex; ship code + stories + barrel; run `pnpm typecheck && pnpm lint && pnpm build && pnpm build:storybook`; update this file's quick-state with new total + version; ask user to push.

## Locked decisions (do not re-litigate)

| # | Decision |
|---|---|
| 1 | Hybrid school: headless engine + Tailwind v4 (CSS-first via `@theme`). |
| 2 | React 19 + TS strict. |
| 3 | Single package, subpath exports per top-level domain. |
| 4 | `pnpm` workspace; `tsup` ESM build; `tsc` DTS. |
| 5 | Storybook 8 catalog. |
| 6 | ESLint flat + `eslint-plugin-boundaries` (foundation/domain). |
| 7 | Foundation never imports domains. |
| 8 | Domains may import any sibling domain (relaxed 2026-05-04). |
| 9 | One component per folder; never flatten. |
| 10 | Beta-forever: no CHANGELOG, no PR gate, no required tests, push to main, fix-forward, CI auto-bumps `0.0.y`. |
| 11 | No SSR — pure CSR. |
| 12 | Theme vocabulary = shadcn-aligned (24 semantic tokens); raw scales preserved. |
| 13 | Dark mode = `.dark` class on body/html; components never use `dark:` modifiers. |
| 14 | Polymorphism: layout atoms use `as`; interactive atoms use `Slot`/`asChild`. |
| 15 | Severity components ship in pairs: `*Simple` (L3) + slotted `*` (L4). |
| 16 | Inputs split by type, not one `Input` with `type` prop. |
| 17 | Helper file naming: `*Extensions.ts` / `*Styles.ts` / `*Helpers.ts` / `*Chrome.tsx` / `*Grid.tsx` (domain-internal, not in barrel). |
| 18 | Layer model: L0 tokens · L1 utils/hooks/icons · L2 primitives · L3 atoms · L4 molecules · L5 organisms · L6 patterns · L7 domain. |
| 19 | Atom rule (convention): L3 never composes other atoms. |
| 20 | Build-first / standardize-later (2026-05-04). First-gen components ship code + stories + barrel only; `*.standard.md` + `*.spec.md` added in per-component standardization pass. |

## Conventions to honor during build

- Files PascalCase, folders camelCase, only `index.ts` lowercase.
- Stories cover ≥ default + key states.
- Run `pnpm typecheck && pnpm lint && pnpm build && pnpm build:storybook` before declaring a batch done.
- For interactive components: respect `prefers-reduced-motion` (skip animation or short-circuit to final state).
- For form components with non-string `value`/`defaultValue`: `Omit<HTMLAttributes<…>, 'defaultValue'>` (and `'title'` if needed). The `FrictionlessDivProps` helper is past-due — add to `forms/FormHelpers.ts` opportunistically when you next touch a forms component.
- Drawer's compound members (`Drawer.Content`, `Drawer.Title`, etc.) only exist on the *default* export. Internal cross-domain imports must use the *named* exports (`DrawerContent`, `DrawerTitle`).
- JSDoc comments must avoid `*/` even inside backticks (TS parser collides). Describe in words.

## Key files (read on demand only)

- `workbench/wow-two-sdk-beta/wow-two-sdk-beta.ui/CLAUDE.md` — repo conventions (build-first/standardize-later locked here).
- `workbench/wow-two-sdk-beta/wow-two-sdk-beta.ui/docs/architecture.md` — layering rules + cross-domain.
- `workbench/wow-two-sdk-beta/wow-two-sdk-beta.ui/docs/analysis/ui-philosophy/ideas.md` — universe doc (~340 components, ~1960 lines).
- `workbench/wow-two-sdk-beta/wow-two-sdk-beta.ui/docs/analysis/ui-philosophy/targets.md` — verdict per item.
- `docs/ui-beta-roadmap.md` — phase plan (P1–P7).
- `docs/audits/library-references.md` — P5 component matrix audit.

## Recurrent gotchas (so you don't re-discover them)

- **Storybook `ENFILE: file table overflow`** — system-wide FD exhaustion under heavy concurrent processes (lots of MSBuild / GitKraken renderers). Retry once with `ulimit -S -n 65535`; usually clears. Not a code issue.
- **`marked.parse(value)` returns Promise in v18** — must pass `{ async: false }` for sync output.
- **`pnpm` from workspace root** errors `ERR_PNPM_NO_IMPORTER_MANIFEST_FOUND` — always `cd` into the package dir first.
- **Empty interfaces** (`@typescript-eslint/no-empty-object-type`) — use `export type Foo = HTMLAttributes<…>` not `export interface Foo extends HTMLAttributes<…> {}`.
- **`HTMLAttributes['defaultValue']`** is `string | number | readonly string[] | undefined` — Omit it before adding your own typed `defaultValue`.

## Recent open items (carry-over)

- **`forms/FormHelpers.ts`** — add `FrictionlessDivProps` / `FrictionlessSpanProps` / `FrictionlessButtonProps` Omit helpers. 8+ components have repeated the Omit dance manually. **Do this opportunistically next time you touch a forms component.** (Batch 15 hit the same `'title'` collision again — `ThreadView`, `NotificationCenter`, `NotificationItem` all needed manual `Omit<…, 'title'>`.)
- **`useTween()` hook** in `src/hooks/` — extract from `CountUp` + `AnimatedNumber`'s shared rAF tween shape.
- ~~**`useReducedMotion()` hook**~~ — done in batch 15. Lives at `src/hooks/useReducedMotion.ts` and is exported from the hooks barrel.
- **`fab` static variant** — SpeedDial's Trigger uses `!important` overrides to nullify FAB's fixed-position; should add a `position: 'static'` variant to `fabVariants` instead.
- **Animation keyframe split** — `src/index.css` has `indeterminate / gradient-shift / marquee-x / marquee-y / blink-caret`. Move to `src/animations.css` if the list crosses ~10.

These are not blockers; pick them up when nearby.

## Domain inventory snapshot (recoverable from `src/`, kept here for orientation)

```
actions    9 atoms · 9 molecules
display   11 atoms · 23 molecules · ?? organisms (Carousel, DataGrid, NodeEditor, EventCalendar, ScheduleView, Gantt, AudioPlayer, VideoPlayer, MessageList, ThreadView, CommentThread, ActivityFeed)
                + batch 15: AnnotationMarker (atom-ish), ReactionBar, ChatBubble (molecules)
feedback   7 atoms · 11 molecules · 4 organisms (Toaster, LoadingOverlay, OnboardingChecklist, Tour, NotificationCenter)
                + batch 15: TypingIndicator, PresenceIndicator, LiveCursor (atoms/molecules)
forms     17 atoms · 33 molecules · 11 organisms (Listbox, Select, MultiSelect, Combobox, RangeCalendar, DatePicker, TimePicker, DateRangePicker, ColorSlider, ColorArea, ColorWheel, ColorSwatchPicker, ColorPicker, Stepper, MarkdownEditor, JSONEditor, RecurrenceEditor, Wizard) — count drift; recount before quoting externally
                + batch 15: ReactionPicker, ChatComposer (molecules)
layout    11 atoms · 5 molecules · 1 organism (ResizablePanels, AppShell)
nav        – atoms · 4 molecules · 7 organisms (Menu, DropdownMenu, ContextMenu, Menubar, NavigationMenu, CommandPalette, TableOfContents)
overlays   – atoms · 1 molecule · 7 organisms (Dialog, AlertDialog, Drawer, Popover, HoverCard, ActionSheet, BottomSheet)
primitives 15 (foundation L2)
hooks      adds useReducedMotion (batch 15)
```

(Exact per-domain counts get fuzzy after 15 batches; treat the ~227 total as authoritative and recount per domain via `ls src/{domain}/` if you need exact numbers.)

# Frontend baseline analysis

*Last updated: 2026-09-09*

> Evidence from all 65 `core/lla/` documents and the four frontend scope/index documents.
> Paths below are relative to `conventions/development/frontend/` unless stated otherwise.
> Findings describe the conventions; they are not claims that every SDK component has the defect.

## Factual defects

### L1 — focus styling loses its fallback in forced colors

- Evidence: `core/lla/constructs/tailwind/border.md:36` requires `outline-none` plus a ring.
- `core/lla/constructs/tailwind/effects.md:45` recommends that ring as the remedy for shadows disappearing in forced colors.
- Tailwind rings are themselves box shadows. Removing the outline leaves the recipe without a forced-colors indicator.
- Fix the recipe to retain a transparent outline (`outline-hidden`) or provide an explicit forced-colors outline.
- Acceptance: render the example in forced-colors mode; keyboard focus stays visible, including on dark surfaces.
- Sources: [Tailwind rings](https://tailwindcss.com/docs/box-shadow),
  [Tailwind outlines](https://tailwindcss.com/docs/outline-style),
  [forced-colors behavior](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@media/forced-colors).

### L2 — Tailwind and class-merging premises are false

- `core/lla/constructs/tailwind/tailwind.md:50–52` says the v3 important prefix emits nothing under v4.
  Tailwind retains it for compatibility. A house ban can remain; the claimed compiler failure cannot.
- The same section and `core/lla/constructs/css/selectors.md:51` say important utilities cannot be merged.
  `tailwind-merge` supports important modifiers. Important and ordinary utilities remain distinct groups.
- `core/lla/constructs/css/values.md:50–51` and `tailwind/spacing.md:44` say arbitrary scale-equivalent values cannot merge.
  Local installed-package reproduction: `p-[1rem] p-4` → `p-4`; `gap-[0.5rem] gap-2` → `gap-2`.
- `core/lla/constructs/tailwind/authoring.md:35–37` assumes any custom `@utility` is understood by the merger.
  Custom classes need a documented merging strategy; CSS registration does not configure the JavaScript merger.
- `core/lla/constructs/tailwind/interactivity.md:52–53` says buttons already have a pointer cursor.
  Tailwind v4 uses the browser's default button cursor; a pointer policy must be explicit.
- Fix: separate house preferences, CSS generation, and merger behavior. Add a minimal generated-CSS/merge fixture.
- Sources: [Tailwind upgrade guide](https://tailwindcss.com/docs/upgrade-guide),
  [merge features](https://github.com/dcastil/tailwind-merge/blob/main/docs/features.md),
  [merge configuration](https://github.com/dcastil/tailwind-merge/blob/main/docs/configuration.md).
- Local results: [reproductions](reproductions.json). These are bounded counterexamples, not an SDK test run.

### L3 — framework preferences are presented as framework impossibilities

- `core/lla/constructs/react/hooks.md:65–66` says `useActionState` needs a Server Action runtime.
  It accepts client actions; retaining the form-engine policy does not require this false reason.
- `core/lla/constructs/react/boundaries.md:48–49` says `Context.Provider` warns today.
  React's reference calls it legacy; the React 19 announcement places deprecation in a future version.
  Adopt the new spelling as a house rule without claiming a present runtime warning.
- `core/lla/constructs/vue/builtins.md:40–43` says `Transition` requires non-utility classes and `@apply`.
  Its custom transition-class props accept existing classes. Preserve the SDK abstraction decision separately.
- `core/lla/constructs/vue/template.md:69–70` says function refs receive null and node on every patch.
  Vue documents update calls and null on unmount, not that unconditional pair.
- `core/lla/constructs/html/interactive.md:53–54` rules out native dialog exits and backdrop tokens.
  Dialog display/overlay transitions and styled `::backdrop` are supported; browser support belongs in a compatibility policy.
- Fix: correct these premises before treating the bans as automatic deletion instructions.
- Sources: [useActionState](https://react.dev/reference/react/useActionState),
  [Context reference](https://react.dev/reference/react/createContext),
  [React 19 announcement](https://react.dev/blog/2024/12/05/react-19),
  [Vue transition classes](https://vuejs.org/guide/built-ins/transition.html#custom-transition-classes),
  [Vue function refs](https://vuejs.org/guide/essentials/template-refs.html#function-refs),
  [dialog transitions](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/dialog).

### L4 — removing exposed roots needs a replacement contract

- `core/lla/constructs/vue/macros.md:52` justifies removing `defineExpose({ el })` because parents can use `$el`.
- `$el` is undefined before mount and may be a text/comment placeholder for multiple roots.
  Vue recommends template refs for direct element access.
- Existing sweep row 17 must inventory consumers and define the supported root/imperative API before deleting handles.
- Acceptance: focus, positioning, measured dimensions, portals and conditional/multiple roots continue to work.
- Source: [Vue component instance](https://vuejs.org/api/component-instance#el).

### L5 — static typing is confused with runtime immutability

- `core/lla/components/constants.md:20` says `as const` freezes objects; `extensions.md:41` says it prevents mutation.
- `as const` is erased. Local transpilation emits an ordinary mutable object; `Object.isFrozen` is false.
- `core/lla/constructs/typescript/typescript.md:97–98` groups `readonly T[]` with arrays exposing mutators.
  `readonly T[]` and `ReadonlyArray<T>` are both readonly views; the spelling preference is separate.
- `typescript.md:93–94` and `extensions.md:45` say `isolatedModules` rejects namespaces generally.
  The documented restriction applies to namespaces in non-module files; ambient const-enum references are another distinct restriction.
- Fix: state compile-time readonly guarantees accurately, name permitted internal mutable collections,
  and put runtime freezing only where a runtime contract actually needs it.
- Sources: [TypeScript const assertions](https://www.typescriptlang.org/docs/handbook/release-notes/typescript-3-4.html#const-assertions),
  [isolatedModules](https://www.typescriptlang.org/tsconfig/isolatedModules.html).

## Rule conflicts and scope defects

### L6 — shape rules leak into the shared baseline

- `core/core.md:19` files a rule by whether it changes with the deliverable.
  `shapes/shapes.md:24–39` explicitly rejects that test in favor of whether the subject exists without the shape.
- `core/lla/notation/naming/naming.md:58–71` fixes app-shell names and bootstrap paths inside supposedly universal notation.
- `core/lla/components/enums.md:24–25` fixes a product domain path; `extensions.md:64–66` fixes app placement.
- `core/lla/constructs/css/css.md:26–27` requires every stylesheet under `bootstrap/`.
  Library packages have no such app composition root; library delivery needs its own stylesheet contract.
- `core/lla/constructs/vue/vue-sfc.md:26–30` carries library import/alias restrictions that should also cover React declarations.
- Fix: keep the source-form rule in core, move placement/build rules to the owning shape, and retain links.
  Replace the stale core routing test; do not introduce a third shape or another layer.

### L7 — layout bans contradict allowed examples and semantic widgets

- `tailwind/grid.md:28,43` bans a one-column grid, while `grid.md:34,55` requires and demonstrates one at mobile size.
- The same mandatory collapse would break calendar week grids; responsive layout policy needs semantic-grid exceptions.
- `tailwind/transforms.md:32` requires every transform to animate, while `position.md:33` and `transforms.md:51`
  demonstrate static translation for centering.
- `tailwind/z-index.md:31` demands positioning for every z-index, while `z-index.md:46–47` acknowledges flex/grid items.
- `tailwind/transitions.md:22–23` permits raw built-in durations/easings; `css/values.md:36,52–54` bans them.
- `tailwind/border.md:37` forbids `focus:` rings; `tailwind/variants.md:14,39` allows focus styling when mouse focus should show it.
- Fix: declare narrow defaults with explicit exceptions, and make accepted examples pass their own rules.
- Acceptance: one-column responsive cards, seven-day calendars, static centered overlays, and static grid stacking have unambiguous verdicts.

### L8 — generated identity and landmark naming are overgeneralized

- `html/global-attributes.md:44` requires every ID to come from `useId()`.
  `tailwind/accessibility.md:55` demonstrates `href="#main"`; stable document fragment targets need a distinct policy.
- Reusable internal IDs should be generated; caller-supplied IDs must propagate to labels, descriptions and references.
- `html/headings.md:23,36` and `html/landmarks.md:18,38` imply that a nested heading automatically names a section landmark.
  A region needs an accessible name, normally linked with `aria-labelledby`; merely nesting a heading is insufficient.
- `html/landmarks.md:27,47–48` says an unnamed section is a named-role stop announced as region.
  Without an accessible name it is not implicitly exposed as a region landmark.
- Fix: distinguish heading structure, landmark naming, reusable identity and stable page anchors.
- Source: [region semantics](https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/region_role).

### L9 — the controlled API examples do not define an enforceable mode

- `notation/naming/props.md:44–55` defines three canonical triads and forbids mixing controlled/uncontrolled values.
- Its `InfoBannerProps` example makes `open` and `onOpenChange` required, so a seed-only uncontrolled usage cannot typecheck.
- Vue models use update emits; the nominally framework-neutral document gives only React callback spellings.
- Absence (`undefined`), explicit clear (`null`), seed-only initialization, callback payloads, mode changes,
  native attributes and custom boolean names need one shared contract with framework-specific spelling.
- Fix: put invariant semantics in core and React/Vue spellings in their framework owners; use examples that compile.
- Acceptance: controlled-only, uncontrolled-only, clear, form reset and external update cases have explicit outcomes.

### L10 — imports and comments still carry stale or contradictory instructions

- `notation/style/imports.md:80` points at a removed style section; the target section is now `react/jsx.md:62`.
  All Markdown file/fragment targets exist; prose section references require separate checking.
- SDK group matching lists only `@wow-two-beta/ui/*`; it does not assign the Vue SDK to a group.
- The app alias layer order lists `domain → integration → presentation`, omitting `application` and `bootstrap`.
- Empty-group wording says adjacent groups touch even though every non-empty group must have a blank separator.
- `core/mla/mla.md:49–69` requires a fixed three-section doc form, field-level example pairs and a member order;
  current selection docs use a different pattern. The template also includes `Neighbours` beyond its stated three sections.
- Baseline directives repeat rules across rosters, banned sections, notation and construct files.
  The lexical checker found 25 repeated directive-line candidates, including template lines; this is not 25 confirmed defects.
- Fix: choose one owner per obligation, repair prose targets and examples, and retain runtime obligations in API docs.

## Missing coverage

These are scoped additions, not demands to document every web API or ship every possible SDK capability.

- **Execution contract:** browser baseline, feature detection, import-time DOM access, SSR-safe import versus full SSR support,
  and polyfill ownership. React-only SPA restrictions currently become blanket library restrictions.
- **React lifecycle correctness:** render purity, hook-call placement, exhaustive dependencies, Strict Mode setup/cleanup,
  async stale-result suppression and ref callback cleanup. Lifecycle disposal exists; the complete contract is not assembled.
- **Interaction contract:** modal versus nonmodal focus, disabled event suppression, focus restoration, IME composition,
  keyboard alternative to drag, pointer cancellation and lost capture. Individual components cover pieces only.
- **Visual verification:** forced colors, reduced motion, zoom/reflow, RTL, long labels, dark mode and accessible names.
- **Enforcement:** executable representative examples, rule-to-check mapping, and documented review-only exceptions.
  A lint-green package does not establish behavioral or accessibility conformance.

## Method and limits

- Read every assigned document; cross-read central shape, extraction and SDK planning owners.
- Mechanically checked relative Markdown file links across all 363 convention documents: zero missing files.
- Checked explicit URL fragments against generated heading slugs: zero suspected fragment failures.
- Prose `§` references are not covered by that mechanical result; L10 records a confirmed stale one.
- Source snapshot hashes and duplicate candidates are in [coverage](coverage.json).
- Official documentation verified the disputed technical claims; no SDK behavior was inferred from a house ban alone.
- No browser conformance matrix, full SDK build or full SDK test run was performed in this conventions-analysis phase.

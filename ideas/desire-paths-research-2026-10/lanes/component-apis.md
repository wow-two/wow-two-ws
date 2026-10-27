# Component library and design-system APIs: desire paths that got paved (Vue 3 focus)

Research date: 2026-10-27. Prefers 2020 onward. Doc versions and dates are noted where a source gave them. Anything a source did not give is listed under Gaps, not guessed.

## 1. Which widely adopted patterns started as workarounds, what did each replace, and what did it cost?

### Takeaway
The recurring arc: developers fought a library's markup, styles or internals with wrappers and CSS overrides, then the ecosystem moved the override point into the API. Pattern by pattern: open code (shadcn), unstyled behavior (Headless UI, Radix, Reka), element swapping (`asChild`, `as`), class passthrough plus merge helpers, state exposed as data attributes or slot props, and logic hooks. Each fix added a new cost: ownership of the code, an accessibility duty, a runtime cost, or a bigger API-stability surface.

### Cited Findings

**Open code / copy-paste ownership (shadcn/ui)**
- Stated thesis: "This is not a component library. It is how you build your component library." — [shadcn/ui Introduction](https://ui.shadcn.com/docs)
- Workaround it replaced, as the docs describe it: npm libraries break down when you need deep customization, leading to wrapper components, style overrides, or mixing libraries with incompatible APIs. — [shadcn/ui Introduction](https://ui.shadcn.com/docs)
- Mechanism: "The top layer of your component code is open for modification." A flat-file schema plus a CLI distributes components across projects and frameworks. Docs also claim "Beautiful Defaults" that stay easy to override, and "AI-Ready" open code. — [shadcn/ui Introduction](https://ui.shadcn.com/docs)
- Trade-off, upstream dependency risk: third-party blogs say Radix development slowed after WorkOS acquired Modulz in 2022, that Base UI (built by ex-Radix engineers at MUI) reached v1.0 in December 2025, and that a July 2026 shadcn changelog made Base UI the default for new projects with Radix still supported. These are secondary sources; the shadcn changelog itself was not checked. — [dev.to](https://dev.to/mashuktamim/is-your-shadcn-ui-project-at-risk-a-deep-dive-into-radixs-future-45ei); [byteiota](https://byteiota.com/shadcn-ui-base-ui-default-what-react-devs-must-know-now/)

**Headless / unstyled libraries (Headless UI, Radix, Reka UI, Ark UI)**
- Headless UI announced October 6, 2020 by Adam Wathan as "a set of completely unstyled, fully accessible UI components for React and Vue (and soon Alpine.js)". v0.2.0 shipped Menu, Listbox and Switch. — [Tailwind blog: Headless UI](https://tailwindcss.com/blog/headless-ui-unstyled-accessible-ui-components)
- Workarounds it named: off-the-shelf packages are "tightly coupled with their own provided styles," so matching a design "almost always involves writing a bunch of CSS overrides." Building from scratch means keyboard navigation, ARIA and focus trapping, and "3-4 weeks trying to build a truly bullet-proof dropdown menu." — [Tailwind blog: Headless UI](https://tailwindcss.com/blog/headless-ui-unstyled-accessible-ui-components)
- The announcement's API already used compound parts (`Menu`, `Menu.Button`, `Menu.Items`, `Menu.Item`), an `as` prop, and render-prop children exposing state (`active`). — [Tailwind blog: Headless UI](https://tailwindcss.com/blog/headless-ui-unstyled-accessible-ui-components)
- Radix Primitives principles: accessible, unstyled, "open" (add listeners, props or refs to each part), "uncontrolled by default but can also be controlled", fully typed and consistent API, incremental adoption (install `radix-ui` or individual primitives). The intro page does not name compound components as a principle. — [Radix Introduction](https://www.radix-ui.com/primitives/docs/overview/introduction)
- Reka UI (formerly Radix Vue) restates the same principles for Vue: unstyled, WAI-ARIA, open, uncontrolled by default but fully controllable, fully typed, tree-shakeable single package, adopt wholesale or "integrate them progressively." — [Reka UI Introduction](https://reka-ui.com/docs/overview/introduction)
- Trade-off: you supply even functional styles; e.g. a Dialog overlay will not cover the viewport until you write that CSS. — [Reka UI Styling](https://reka-ui.com/docs/guides/styling)

**`asChild` / `as` (polymorphism)**
- Problem stated: parts render a default element (`Tooltip.Trigger` renders a `button`), but you may want a link or your own design-system component. `asChild` stops the default element and clones the child, passing it the props and behavior. — [Radix Composition](https://www.radix-ui.com/primitives/docs/guides/composition)
- Requirements: the custom component must spread incoming props onto its DOM node and forward refs. `asChild` nests, so one element can combine several primitives (Tooltip.Trigger over Dialog.Trigger over a custom button). — [Radix Composition](https://www.radix-ui.com/primitives/docs/guides/composition)
- Trade-off: "you are responsible" for keeping the element accessible and behaving; `Tooltip.Trigger` must stay focusable and respond to pointer and keyboard events. — [Radix Composition](https://www.radix-ui.com/primitives/docs/guides/composition)
- Vue form: Reka passes props and behavior "to the first child of the slots"; same nesting and same accessibility duty. The page does not cover single-root, fragment or text-node limits, and documents only `asChild`, not an `as` prop. — [Reka Composition](https://reka-ui.com/docs/guides/composition)
- Ark UI (React, Solid, Vue, Svelte switcher): `asChild` accepts a single child only; some parts (e.g. `Checkbox.Root`, `RadioGroup.Item`) need specific children, so changing the element needs care. All page examples were React. — [Ark UI Composition](https://ark-ui.com/docs/guides/composition)
- The `as` prop predates these: Headless UI's 2020 example used `<Menu as="div">`. — [Tailwind blog: Headless UI](https://tailwindcss.com/blog/headless-ui-unstyled-accessible-ui-components)

**Utility classes as paved inline styling**
- Adam Wathan, August 7, 2017: judge by dependency direction, not "separation of concerns." Content-based class names keep HTML independent but CSS is not reusable; utility classes make CSS reusable but "your HTML is not restyleable." Utilities also limit inconsistency by picking from a fixed value set. — [Wathan 2017](https://adamwathan.me/css-utility-classes-and-separation-of-concerns/)
- Costs he admits: verbose markup, design changes edit HTML, and he still extracts components (`.btn-purple`) when patterns repeat; complex interactions are "hard to do with utilities-only." — [Wathan 2017](https://adamwathan.me/css-utility-classes-and-separation-of-concerns/)

**`class` passthrough and `tailwind-merge`**
- Reka components accept `class`, applied to the rendered element; stateful parts expose `data-state` (e.g. `data-state="open"`), targetable with `.X[data-state="open"]` or Tailwind `data-[state=open]:`. Teleported parts (modals, popovers) escape scoped styles and need `:deep()`. — [Reka Styling](https://reka-ui.com/docs/guides/styling)
- Problem `tailwind-merge` solves: `twMerge('px-2 py-1 bg-red hover:bg-dark-red', 'p-3 bg-[#B91C1C]')` returns `'hover:bg-dark-red p-3 bg-[#B91C1C]'`. Without it both `px-2` and `p-3` stay and stylesheet order decides. Current README supports Tailwind v4.0 through v4.3; Tailwind v3 needs tailwind-merge v2.6.0. — [tailwind-merge README](https://raw.githubusercontent.com/dcastil/tailwind-merge/main/README.md)
- Nuxt UI builds on Tailwind Variants, which uses tailwind-merge "under the hood," so conflicting classes resolve without extra work. — [Nuxt UI theme](https://ui.nuxt.com/docs/getting-started/theme/components)

**CSS-in-props escape hatches (MUI `sx`) and their retreat**
- MUI `sx`: "a shortcut for defining custom styles that have access to the theme"; a superset of CSS with theme-aware shorthand (`bgcolor: 'primary.main'`, spacing scale). Cost: changing `sx` objects each render can insert extra `style` tags; for highly dynamic values MUI recommends inline CSS variables instead. — [MUI sx](https://mui.com/system/getting-started/the-sx-prop/)
- Primer React deprecated `sx` (a December 2024 PR deprecated the `SxProp` type) because of high runtime cost and moved to CSS Modules; GitHub reports "55% less time to server-side render a page"; v38 dropped the styled-components dependency and `sx` support, with a temporary `@primer/styled-react` bridge and a migration guide. Figures come from search snippets of GitHub's engineering blog, not a full read. — [GitHub engineering blog](https://github.blog/engineering/architecture-optimization/improving-site-performance-by-shipping-more-css/); [Primer React v38 discussion](https://github.com/primer/react/discussions/7086)

**Render props to hooks to composables**
- Kent C. Dodds (April 6, 2020): downshift was a render-prop component because that was "the best option at the time" for headless components; hooks are better for the job. His state-reducer pattern is inversion of control: the author lets the user change how internal state updates are computed, so a multi-select can keep the menu open without a new option. — [Dodds: state reducer](https://kentcdodds.com/blog/the-state-reducer-pattern-with-react-hooks)
- Trade-off he states: once users can intercept state updates, the update logic becomes part of the API and changing it can break users. — [Dodds: state reducer](https://kentcdodds.com/blog/the-state-reducer-pattern-with-react-hooks)
- Vue's own docs: renderless components add component-instance overhead that "can become a noticeable performance overhead"; guidance is "use composables when reusing pure logic, and use components when reusing both logic and visual layout." Mixins are no longer recommended (unclear property source, name collisions, implicit cross-mixin coupling). The Composition API was partly inspired by React hooks. — [Vue: Composables](https://vuejs.org/guide/reusability/composables.html)

**Pass-through props (PrimeVue `pt`)**
- Stated rationale: "Your components, not ours." Traditional libraries limit customization to the props, events and slots the author exposes; `pt` exposes internal DOM sections so you can add attributes, listeners and styling without waiting for a release. — [PrimeVue Pass Through](https://primevue.dev/passthrough/)
- Trade-off: you must know each component's internal section names, and the page recommends `pt` when a feature is missing, not as the default. — [PrimeVue Pass Through](https://primevue.dev/passthrough/)

### Inferences
- Pattern, workaround, cost, as one lookup:
  - shadcn: wrapper/override stacks, so code ownership; cost is you carry upgrades and the primitive-layer dependency.
  - Headless: CSS-override fights and 3-4 week from-scratch builds, so unstyled behavior; cost is the consumer styles every state.
  - `asChild` / `as`: wrapper elements and duplicated markup, so element swap; cost is an a11y duty moved to the consumer plus a props-spread/ref contract.
  - Utility classes and `class` passthrough: bespoke stylesheets and override CSS, so inline classes; cost is conflicts, hence `tailwind-merge` as a second paved tool.
  - `sx` / `pt`: wrapper `styled()` components, so inline theme-aware styling or section targeting; cost is runtime cost (`sx`) or exposing internals as public API (`pt`).
  - Hooks / composables: render-prop nesting and mixins, so logic reuse without a component instance; cost is the logic's update rules become API.
- Several "desire path" patterns were initially hacks whose cost later surfaced (`sx` perf, Primer retreat). Evidence of a hatch's long-term cost shows up in runtime and API-stability terms, so audit those first.
- shadcn removes the override problem by moving the source into the consumer's repo, which only fits a team shipping one app. A Vue SDK consumed by several products cannot copy-paste without forking, so for an SDK the closer analogues are headless primitives plus a thin styled layer.

### Gaps
- shadcn/ui launch date and creator's own rationale: not confirmed; searches returned only third-party descriptions.
- The July 2026 shadcn switch to Base UI is reported only by secondary blogs; no official changelog was fetched.
- Which workaround `asChild` replaced is not stated by Radix or Reka; the "wrapper elements" reading is inference.
- Radix's own history (Modulz/WorkOS, Reach UI lineage) was not read from a primary source.
- MUI's page does not say what `sx` replaced (no `makeStyles`/`withStyles` mention), so that link is not documented here.
- shadcn-vue (the Vue port) was not fetched.

## 2. Vue-specific: `v-model`/`defineModel`, attribute fallthrough, slots, provide/inject, composables, and how Vue libraries handle escape hatches, theming and defaults

### Takeaway
Vue paved `v-model` twice: the Vue 3 rename plus arguments (replacing `value`/`input`, the `model` option and `.sync`), then `defineModel` (3.3 experimental, 3.4 recommended) to kill the prop+emit boilerplate that VueUse's `useVModel` had already popularized. Fallthrough attributes make `class`/`style`/listener passthrough the default. Vue libraries split on theming: Nuxt UI (`ui` prop, `class`, `app.config`), PrimeVue (`pt`, `dt`, `cssLayer`), Vuetify (`defaults`, nested defaults, `VDefaultsProvider`) and Element Plus (`ConfigProvider`).

### Cited Findings

**`v-model` history**
- Vue 2: `v-model` on a component meant a `value` prop plus `input` event; Vue 2.2 added a `model` option to rename them but allowed one `v-model` per component; `.sync` was a separate shorthand for `update:title`. — [Vue 3 migration: v-model](https://v3-migration.vuejs.org/breaking-changes/v-model.html)
- Vue 3: `v-model` is `modelValue` plus `update:modelValue`; `v-model:title` replaces `model` and `.sync`; multiple `v-model`s per component are allowed. The page does not give the reason `.sync` was removed beyond calling `v-model` arguments "a replacement." — [Vue 3 migration: v-model](https://v3-migration.vuejs.org/breaking-changes/v-model.html)
- `defineModel`: "starting in Vue 3.4, the recommended approach"; returns a ref synced with the parent's `v-model`; compiles to a `modelValue` prop and `update:modelValue` event; accepts prop options (`required`, `default`). Docs call the manual version "quite a bit more verbose." — [Vue: component v-model](https://vuejs.org/guide/components/v-model.html)
- RFC discussion #503 (started April 28, 2023): shipped as experimental in 3.3 beta behind an opt-in compiler option; a maintainer says it "works very similar to `useVModel` from VueUse"; commenters named VueUse `useVModel` and vue-macros `defineModels` as existing workarounds. — [vuejs/rfcs #503](https://github.com/vuejs/rfcs/discussions/503)
- RFC design points: `local: true` made the ref locally mutable when the parent passes no `v-model` (implemented "as an extra layer, with an additional ref and watchers," default `false`); assigning the same value emits no event; modifier support (`[model, modifiers] = defineModel()`, `get`/`set` transforms) landed in 3.4.0-rc.3 on Dec 28, 2023. — [vuejs/rfcs #503](https://github.com/vuejs/rfcs/discussions/503)
- Known sharp edge: with a `default` on `defineModel` and no parent value, parent and child can desynchronize (parent `undefined`, child `1`). — [Vue: component v-model](https://vuejs.org/guide/components/v-model.html)
- Community friction in the RFC: mutating object props does not emit, and one user preferred emitting a new object. — [vuejs/rfcs #503](https://github.com/vuejs/rfcs/discussions/503)
- Reka UI renamed `v-model:checked` / `v-model:pressed` to plain `v-model` for "a more familiar API for form component." — [Reka migration](https://reka-ui.com/docs/guides/migration)
- Radix and Reka both default to uncontrolled state and allow full control. — [Radix Introduction](https://www.radix-ui.com/primitives/docs/overview/introduction); [Reka UI Introduction](https://reka-ui.com/docs/overview/introduction)

**Attribute fallthrough (`inheritAttrs`)**
- Fallthrough attributes (`class`, `style`, `id`, `v-on` listeners not declared as props/emits) land on a single root element automatically; `class` and `style` merge; if the root already has a `click` listener, both fire. — [Vue: fallthrough attributes](https://vuejs.org/guide/components/attrs.html)
- `inheritAttrs: false` (via `defineOptions` in 3.3+) plus `v-bind="$attrs"` forwards them to another element; listeners appear as `$attrs.onClick`; attributes keep original casing. — [Vue: fallthrough attributes](https://vuejs.org/guide/components/attrs.html)
- Multi-root components get no automatic fallthrough and warn at runtime unless `$attrs` is bound explicitly. `useAttrs()` returns the latest attrs but is not reactive; use a prop or `onUpdated()`. — [Vue: fallthrough attributes](https://vuejs.org/guide/components/attrs.html)

**Composables vs components**
- See Question 1: composables for logic only, components for logic plus layout; renderless components carry instance overhead. — [Vue: Composables](https://vuejs.org/guide/reusability/composables.html)

**Vue UI libraries: escape hatches, theming, defaults**
- Nuxt UI layers, lowest to highest: component defaults and resolved variants; global config in `app.config.ts` (`vite.config.ts` in plain Vue); `UTheme` for a subtree; the `ui` prop (per-instance slot override); the `class` prop merged last on `root`/`base`. Components expose named `slots`, `variants`, `defaultVariants`, `compoundVariants`. A slot set to a function replaces defaults instead of merging, and the docs warn to set it in only one layer because Nuxt merges layers with `defuFn`. `Link` and `Icon` have no `ui` prop, so `class` is their only override. — [Nuxt UI theme](https://ui.nuxt.com/docs/getting-started/theme/components)
- PrimeVue `pt`: keys name internal sections; a value can be string (treated as class), object or function; `class`/`style` take Vue binding syntax; `pc`-prefixed sections reach nested PrimeVue components (e.g. `pcBadge` inside Button); `hooks` registers lifecycle callbacks; global `pt` applies to every instance but a component's own `pt` wins; `usePassThrough` has `mergeSections` (default `true`) and `mergeProps` (default `false`, so props are overridden). The page does not give an introduction version (footer shows docs v5.0.4). — [PrimeVue Pass Through](https://primevue.dev/passthrough/)
- PrimeVue styled-mode theming: three token tiers (primitive, semantic, component); the `dt` property scopes tokens to one component and the docs recommend it over `:deep()`; presets Aura, Material, Lara, Nora (16px standard plus 14px "compat" variants maintained until June 2027). — [PrimeVue styled mode](https://primevue.dev/theming/styled/)
- Vuetify: `createVuetify({ defaults })` sets default props per component (`VBtn: { elevation: 2 }`), camelCase names; a `global` key applies a prop to every component that supports it (`ripple: false`) but cannot hold `class`/`style`; per-component `class`/`style` defaults merge with template values; nested keys scope by parent (`VCard: { VBtn: { variant: 'outlined' } }`); `VDefaultsProvider` scopes defaults to a subtree; "A prop written directly in the template still wins over any of this." — [Vuetify global configuration](https://raw.githubusercontent.com/vuetifyjs/vuetify/master/packages/docs/src/pages/en/features/global-configuration.md)
- Vuetify defaults gotchas: internal controls need nested keys (`VSelect: { VChip: { size: 'large' } }`); pagination and stepper buttons use role keys (`VPaginationBtn`, `VStepperActionsPrevBtn`) that ignore `VBtn`; menu/dialog content starts from global defaults, not template position, so nest under `VMenu`/`VDialog` rather than `VOverlay`. — [Vuetify global configuration](https://raw.githubusercontent.com/vuetifyjs/vuetify/master/packages/docs/src/pages/en/features/global-configuration.md)
- Element Plus `ConfigProvider`: global `locale`, `size`, `zIndex`, `namespace` (CSS prefix, default `el`), `experimental-features`, `empty-values`/`value-on-clear`; per-component objects for `button`, `link`, `card`, `dialog`, `message`, `table`. Provided config is "inherited from the top," and an explicit prop on a column overrides the inherited value. Nested-provider merge behavior is not documented. — [Element Plus ConfigProvider](https://element-plus.org/en-US/component/config-provider.html)
- Naive UI (secondary sources only): `themeOverrides` passed to `NConfigProvider`, with a `common` section for global variables and per-component keys (`Button`, `DataTable`); third-party summary claims a type-safe overrides object per component. Official docs were not readable. — [Aliyun guide](https://developer.aliyun.com/article/1727016); [openapps.pro](https://openapps.pro/packages/naive-ui)
- Quasar: no current official evidence found for global per-component defaults in core. The Nuxt Quasar module documents `components.defaults` keyed by component name (e.g. `dense`, `flat` on `QBtn`). Per-instance props, slots and `class`/`style` also work. — [nuxt-quasar](https://github.com/Maiquu/nuxt-quasar); [Quasar button docs](https://Quasar.dev/vue-components/button)
- Reka UI rename (Radix Vue to Reka UI, v2): import `radix-vue` to `reka-ui`; CSS variable and data-attribute prefix `radix` to `reka` (e.g. `--radix-accordion-content-width` to `--reka-accordion-content-width`); Combobox refactored (`filter-function` removed, `displayValue` moved to `ComboboxInput`); `Select` `SelectValue` no longer teleports (SSR flicker); `forceMount` changed for SSR. — [Reka migration](https://reka-ui.com/docs/guides/migration)

### Inferences
- Vue gives a free passthrough that React must hand-build: single-root components forward `class`, `style` and listeners with no code. A Vue SDK component that renders multiple roots, or forwards `$attrs` to the wrong element, silently breaks the escape hatch the ecosystem expects.
- The two Vue defaults mechanisms map to different needs: Vuetify's prop defaults (change a prop globally or for a subtree) vs Nuxt UI/PrimeVue theme objects (change styling). An SDK that wants both needs provider-based defaults and a styling hatch, and must document precedence the way Nuxt UI does.
- `defineModel` removes the boilerplate but its `default`-vs-parent desync and local-state semantics need a library-wide convention (always supply a `defaultValue` prop for uncontrolled mode, or never use `default` on the model).
- Audit checklist derived from this section:
  - Every component forwards `class`/`style`/listeners to the right element, or sets `inheritAttrs: false` deliberately.
  - Every two-way value uses `modelValue` (or a named model) consistently; no `.sync`-era names.
  - Uncontrolled behavior is explicit and tested.
  - Precedence (template prop vs global default vs theme) is written down.
  - Teleported parts (modals, popovers) are styleable without `:deep()`.

### Gaps
- No primary source fetched for scoped slots and provide/inject in Vue docs, so nothing about them is asserted here beyond Vuetify's `VDefaultsProvider` and Element Plus's inherited config.
- Whether Vuetify/Element Plus build their provider on provide/inject: not stated on the fetched pages.
- Naive UI official docs and current Quasar v2 docs: not read (JS-rendered docs, and search returned old versions or third parties).
- PrimeVue pass-through introduction version, and Reka UI rename date: not found.
- Official statement of `defineModel`'s uncontrolled/local-state behavior in stable 3.4: the RFC shows `local: true` as proposed; the stable Vue page does not describe it.
- `useModel`/`defineModel` interplay with `v-model` modifiers in libraries: not researched beyond the RFC.

## 3. Escape-hatch design: how libraries make overrides safe and how they decide which hatches to promote

### Takeaway
Safe escape hatches are layered and predictable: tokens first, then component-scoped tokens, then slot/section overrides, then raw `class`, with documented precedence and a merge helper for utility classes. CSS `@layer` makes library styles lose to app CSS. Evidence for promoting a hatch into a first-class prop comes from override-detection tooling (static analysis, library analytics), but no source documents a formal promotion workflow.

### Cited Findings
- Documented precedence ladder (Nuxt UI): defaults, then global config, then `UTheme`, then `ui` prop, then `class`. — [Nuxt UI theme](https://ui.nuxt.com/docs/getting-started/theme/components)
- Token tiers (PrimeVue): primitive (no context), semantic (role-named), component (isolated to one component). `dt` scopes component tokens to one instance; the docs call it cleaner than `:deep()` and avoiding overriding CSS rules. — [PrimeVue styled mode](https://primevue.dev/theming/styled/)
- Cascade layers (PrimeVue `cssLayer`): off by default; when on, built-in classes are wrapped in the `primevue` layer, so unlayered app CSS wins "regardless of selector strength." The page does not discuss Tailwind ordering. — [PrimeVue styled mode](https://primevue.dev/theming/styled/)
- Unstyled modes: Radix, Reka and Headless UI ship with no styles; PrimeVue mentions an unstyled mode where built-in classes are not included (details on a separate page, not read). — [Reka UI Styling](https://reka-ui.com/docs/guides/styling); [PrimeVue styled mode](https://primevue.dev/theming/styled/)
- State-as-attribute and CSS-variable contract: Reka exposes `data-state`; its migration guide shows `--reka-*` CSS variables exist (e.g. accordion content width). The Styling page itself does not mention any CSS variables. — [Reka UI Styling](https://reka-ui.com/docs/guides/styling); [Reka migration](https://reka-ui.com/docs/guides/migration)
- Merge helpers make class overrides deterministic: `tailwind-merge` resolves conflicts instead of relying on stylesheet order. — [tailwind-merge README](https://raw.githubusercontent.com/dcastil/tailwind-merge/main/README.md)
- Override safety rules in practice: Vuetify's template props always beat defaults; Element Plus explicit props beat provider config; PrimeVue component `pt` beats global `pt`. — [Vuetify](https://raw.githubusercontent.com/vuetifyjs/vuetify/master/packages/docs/src/pages/en/features/global-configuration.md); [Element Plus](https://element-plus.org/en-US/component/config-provider.html); [PrimeVue Pass Through](https://primevue.dev/passthrough/)
- A hatch can be retired when its cost is high: Primer removed `sx` for runtime performance and offered CSS Modules plus CSS-variable primitives. — [GitHub engineering blog](https://github.blog/engineering/architecture-optimization/improving-site-performance-by-shipping-more-css/); [Primer React v38 discussion](https://github.com/primer/react/discussions/7086)
- Inversion-of-control hatches become API: Dodds warns that exposing a reducer makes update logic part of the contract. — [Dodds: state reducer](https://kentcdodds.com/blog/the-state-reducer-pattern-with-react-hooks)
- Accessibility is the unguarded edge of `asChild`: the consumer must keep the swapped element focusable and responsive to keyboard and pointer events. — [Radix Composition](https://www.radix-ui.com/primitives/docs/guides/composition)
- Watching hatch usage (tooling, not process docs):
  - antbear (npm) analyses custom styles in a codebase (overridden components, CSS properties and values, components and props; styled-components, Emotion, Theme UI `sx`, CSS Modules, Sass), with the stated aim of spotting "missing component props, missing design tokens". — [antbear](https://www.npmjs.com/package/antbear)
  - Fabric used React Scanner (static AST analysis) to measure component usage per route and flag hard-coded colors and style components. — [GitNation: Measuring Coverage of React Design System](https://gitnation.com/contents/measuring-coverage-of-react-design-system)
  - Figma's updated Library Analytics (from February 11, 2025) gives Organization and Enterprise customers deeper insight into component, variable and style adoption; guidance elsewhere says to watch detachments and style overrides as signals the system is not meeting needs. — [Figma: Design Systems 104](https://www.figma.com/blog/design-systems-104-making-metrics-matter/)
  - Omlet (Zeplin) offers component analytics for developers and design-system teams. — [Zeplin: Omlet](https://blog.zeplin.io/meet-omlet-component-analytics-for-developers)

### Inferences
- A hatch is safe when four things hold: a documented precedence ladder, a merge helper so `class` overrides are deterministic, a contract of stable hooks (tokens, `data-*` attributes, CSS variables) rather than internal class names, and library CSS in a layer that loses to app CSS.
- Pass-through hatches (`pt`, `ui`) make internal section names public API. Treat each section/slot name as a semver-covered surface from the day it ships.
- For promotion: count repeated overrides per component and per CSS property (antbear-style or an AST pass over product repos), then decide prop, token or variant. A repeated `class` override of the same property across products is a prop or variant candidate; a repeated color/spacing override is a token candidate. No source documents this exact loop, so it is a method proposal.
- For a small team: a single `rg`/AST scan of `class=` and `:ui=` usage against the SDK's components is the cheap equivalent of Figma/Omlet analytics.

### Gaps
- No source describes a documented workflow where a library measured override usage and promoted the most common one to a first-class prop (the search found tools and metrics advice, not a case study).
- How Nuxt UI/PrimeVue maintainers decide which `ui`/`pt` slots to expose: not found.
- How `@layer` ordering works with Tailwind v4 in PrimeVue: the fetched page does not say.
- The Reka UI list of exposed CSS variables: not found on the Styling page.

## 4. Developer-experience principles: pit of success, convention over configuration, defaults, progressive disclosure, typed discoverability, naming and rename cost

### Takeaway
The principles agree: make the right path the default and cheapest (pit of success, convention over configuration, beautiful defaults), keep the first screen of API small and push advanced control behind a visible second level, and treat names as public contracts, since renames cost every consumer (Vue 2 to 3 `v-model`, Radix Vue to Reka). Types make the second level discoverable.

### Cited Findings
- Pit of success: coined by Rico Mariani, popularized by Jeff Atwood on 29 Aug 2007. "We want our customers to simply fall into winning practices"; "To the extent that we make it easy to get into trouble we fail." Brad Abrams extends it to APIs that "steer and point developers in the right direction." — [Atwood: Falling Into The Pit of Success](https://blog.codinghorror.com/falling-into-the-pit-of-success/)
- Convention over configuration (Rails doctrine): shared defaults stop developers re-deciding routine details; "Constraints liberate even the most able minds"; beginners can build "without knowing why everything is the way it is." Perils: "most applications worth building have some elements that are unique," and "The hard part is knowing when to stray from convention." The page never uses the phrase "sensible defaults." — [Rails Doctrine](https://rubyonrails.org/doctrine)
- Progressive disclosure: Jakob Nielsen, December 3, 2006: show core options first, push advanced ones to a secondary display. "The very fact that something appears on the initial display tells users that it's important." Keep to two levels (more than two "usually have poor usability"), decide the split with usage data, and make the reveal control obvious. — [NN/g: Progressive Disclosure](https://www.nngroup.com/articles/progressive-disclosure/)
- Zero-config happy path examples: Headless UI promised open/close, Escape and outside-click, arrow/Home/End navigation, disabled-item skipping and screen-reader announcements "without writing a single event listener." — [Tailwind blog: Headless UI](https://tailwindcss.com/blog/headless-ui-unstyled-accessible-ui-components)
- Progressive adoption: Radix lets you install one primitive or the whole package; Reka lets you adopt wholesale or "integrate them progressively." — [Radix Introduction](https://www.radix-ui.com/primitives/docs/overview/introduction); [Reka UI Introduction](https://reka-ui.com/docs/overview/introduction)
- Consistency as predictability: shadcn says "Every component uses a common, composable interface, making them predictable"; Radix and Reka advertise a "fully typed" and "consistent" API. — [shadcn/ui Introduction](https://ui.shadcn.com/docs); [Radix Introduction](https://www.radix-ui.com/primitives/docs/overview/introduction); [Reka UI Introduction](https://reka-ui.com/docs/overview/introduction)
- Types as discoverability: `defineModel` with `required: true` removes `undefined` from the model type, and a `default` gives a non-undefined type. PrimeVue lists IDE autocomplete for its declarative `pt` syntax as planned work, not shipped. — [vuejs/rfcs #503](https://github.com/vuejs/rfcs/discussions/503); [PrimeVue Pass Through](https://primevue.dev/passthrough/)
- Naming that matches a mental model: Reka renamed `v-model:checked` / `v-model:pressed` to plain `v-model` for "a more familiar API for form component." — [Reka migration](https://reka-ui.com/docs/guides/migration)
- Cost of renames, concrete cases:
  - Vue 2 to 3: `value`/`input` became `modelValue`/`update:modelValue`, `.sync` became `v-model:arg`, with `COMPONENT_V_MODEL` / `COMPILER_V_BIND_SYNC` compat flags. — [Vue 3 migration: v-model](https://v3-migration.vuejs.org/breaking-changes/v-model.html)
  - Radix Vue to Reka: package name, `--radix-*` CSS variables and `data-radix-*` attributes became `reka` equivalents; consumer selectors and imports must change. — [Reka migration](https://reka-ui.com/docs/guides/migration)
- Components needing explicit contracts: Ark UI warns that single-child `asChild` and required children (labels) constrain element swaps. — [Ark UI Composition](https://ark-ui.com/docs/guides/composition)

### Inferences
- "Pit of success" for a component API: the default render is accessible and correct without any prop; the wrong thing (breaking a11y, duplicating state) takes visible effort. `asChild` and `pt`-style hatches are the "stay possible but harder" half of Atwood's framing.
- Progressive disclosure maps onto three API levels at most: props (level 1), slots and `defineModel` (level 2), pass-through/`ui`/`asChild` (level 3). Nielsen's two-level warning suggests keeping level 3 rare and clearly labeled.
- Convention over configuration plus Rails' warning implies the SDK should ship one opinionated default per decision (naming, controlled/uncontrolled shape, class passthrough) and document the deliberate deviations.
- Rename costs fall on selectors and attributes, not only imports; a safe rename ships an alias for one release (as the Dialog to Modal pattern in this team's own history did) and a codemod or migration page.
- Audit questions for the team's SDK: Does the default render pass a11y with zero props? Can a new consumer guess prop names from sibling components? Are model names uniform (`modelValue`, same `update:` events)? Do types narrow on `required`/`default`? Are data attributes and CSS variable names treated as semver surface?

### Gaps
- No source found quantifying the cost of API renames (adoption or breakage metrics); only migration guides listing what changed.
- No primary source on typed autocompletion as a discoverability principle for component libraries beyond the cited `defineModel` and PrimeVue items.
- Joshua Bloch's API design talk and Vue core team's own stated API principles were not researched.
- "Sensible defaults" as a named principle: the Rails doctrine page does not use the phrase, so it is not attributed to DHH here.

## 5. Contribution models that pave local components into the system (snowflakes, community backlog, Polaris patterns)

### Takeaway
Mature systems separate three tiers: system components, product-level recipes, and one-off snowflakes. They give snowflakes a legitimate home and a documented promotion path instead of forbidding them. GOV.UK runs a public GitHub backlog scored on cross-service reuse; Polaris splits contributions into minor and major with proposals for major ones; Brad Frost's guidance is to default to a design-system mindset while building locally and keep product-only pieces out of the core.

### Cited Findings
- Team models, as summarized from Nathan Curtis: solitary ("one team make[s] a system available, but with efforts focused primarily on that team's needs"), centralized ("a single, central design team produces and supports a system used by others"), and federated ("designers from multiple product teams decide on the system together"); a federated team needs a dedicated core or the style guide "can seem quite dead." Salesforce's Jina Bolton wrote that her team used a mix of centralized and federated. These come from republished copies and a search summary, not from Curtis's original site. — [Center Centre: Team Models](https://articles.centercentre.com/?p=860); [Center Centre: Salesforce team model](https://articles.centercentre.com/?p=1980)
- Brad Frost (3 February 2021): design-system components are context-free and shared (Accordion, Button, Card); recipes combine components for one product (ProductCard, AddressField) and stay out of the system; snowflakes are one-off pieces such as an airline `Seat` used on one page. He suggests a standalone "extras" library for recipes, snowflakes and utilities. Quotes: "Everything is a component"; "default to thinking about things as a design system component"; "think globally, act locally"; "Polluting a design system library with a bunch of product-specific components gets noisy and messy." A recipe can move into the system once widely used. — [Frost: components, recipes, snowflakes](https://bradfrost.com/blog/post/design-system-components-recipes-and-snowflakes/)
- Snowflake governance elsewhere: Zebra's Zeta process asks whether an existing component fits, meets requirements, and extends beyond the project, to route a request to snowflake, modification, or system build. A Prototypr piece argues product designers should keep building snowflakes while system intake is slow. Frost's search-surfaced writing points to formal contribution processes (Canonical's decision tree) being defined early. — [Zebra Zeta process](https://design.zebra.com/docs/Design/zetaProcess/); [Prototypr: snowflakes](https://blog.prototypr.io/why-snowflakes-are-counterintuitively-integral-to-design-systems-654dac639d81); [Brad Frost](https://bradfrost.com/?p=11358)
- GOV.UK community backlog, "How we prioritise additions" (7 September 2022): new components/patterns prioritised by use across the most services and flexibility across contexts; iterations judged more broadly (e.g. staying accessible). A two-week community survey drew 302 responses (131 complete) and 245 comments; scores were boosted for items that "exist in multiple department's pattern libraries," "could be a pattern made up of existing components," are "unlikely to need complex Javascript," or "reduce potential harm to users." The team analysed the top 12 in a workshop and plans to repeat yearly. The post sets no minimum number of services per item. — [GOV.UK Design Notes, Sept 2022](https://designnotes.blog.gov.uk/2022/09/07/how-we-prioritise-additions-to-the-gov-uk-design-system/)
- GOV.UK backlog is public on GitHub with stages (proposed, to do, in progress, in review, published, not doing); once "To do," the team decides with the proposer who builds it. The team's strategy says it will not build every component nor components specifically for internal services. These details come from a search summary of the backlog page and the team playbook, not a full read. — [Upcoming components and patterns](https://design-system.service.gov.uk/community/upcoming-components-patterns); [Team playbook: future of the design system](https://team-playbook.design-system.service.gov.uk/what-we-do/future-of-the-govuk-design-system)
- GOV.UK opened the system to contributions in a September 26, 2018 post (title only seen in search results). — [Opening up the GOV.UK Design System for contributions](https://designnotes.blog.gov.uk/2018/09/26/opening-up-the-gov-uk-design-system-for-contributions/)
- Polaris contributing guidance: minor changes are bug fixes, docs, icons, style changes; major are new or redesigned components, API changes and patterns, which need a proposal and more team involvement; contributions go through GitHub except Figma UI kits; contributions should address a known gap and "add value at scale." A new pattern can be added as an example in an existing component's docs or as a new component or utility. — [Polaris: Contributing](https://polaris.shopify.com/contributing); [Polaris React: Contributing to components](https://polaris-react.shopify.com/contributing/components)
- shadcn's distribution model is also a contribution path: a flat-file schema plus CLI means a team can publish its own components in the same format. — [shadcn/ui Introduction](https://ui.shadcn.com/docs)

### Inferences
- The shared contract of all three: a visible intake (GitHub backlog or proposal), explicit criteria (cross-product reuse, a11y, harm reduction), and a parking place (recipes/snowflakes/extras) so product teams do not wait on the system.
- GOV.UK's strongest signal is "exists in multiple departments' pattern libraries"; the SDK equivalent is the same local component appearing in two or more products. That is a repo-level grep, not a survey.
- For a small team with an SDK and several products: keep an "extras" folder per product for snowflakes and recipes, review it on a cadence, and promote what appears in two or more products. Promotion is the point at which the SDK adds the headless part plus a styled default.
- Polaris' minor/major split suggests a lightweight bar for prop/variant additions and a written proposal for new components or breaking API changes.

### Gaps
- No Nathan Curtis source on "snowflakes" was found (search surfaced Frost, Prototypr, Zebra, UXcel); attributing the term to Curtis is unsupported.
- GOV.UK: the backlog and team-playbook pages were seen only as search-result summaries; no numeric evidence threshold (e.g. required number of services) is published in the post read.
- The 2018 GOV.UK contribution post and Polaris' "patterns" docs were not opened in full; Polaris details come from search-result summaries of official pages.
- Canonical's decision tree and UXcel governance lesson were only seen as search mentions.
- No data on how often promotions actually happen, or contributor effort, for any of these systems.

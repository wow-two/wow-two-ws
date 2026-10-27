# Own codebase: fe sdk docs, showcase apps, gallery metadata and the Wheelhouse hosting path

Sources are local repository files, read 2026-10-27, with no network calls. Path roots used below:
`WS/` = `wow-two-ws/` (workspace root) · `FE/` = `WS/workbench/wow-two-sdk-beta/wow-two-sdk-beta.fe/` ·
`PKG/` = `FE/engineering/codebase/wow-two-sdk-beta-fe/` (the Vue package `@wow-two-beta/fe`) ·
`REACT/` = `FE/engineering/codebase/wow-two-front-beta-sdk/` (the parked React package) ·
`WH/` = `WS/workbench/wow-two-platform/wow-two-platform.wheelhouse/`. Counts come from `find`/`grep` over the working
tree, excluding `node_modules` and `dist`.

## 1. What are `apps/atlas` and `apps/playground` today, and is there any Storybook or Histoire?

### Takeaway
The Vue package has two private, undeployed Vite sandboxes. `playground` is a smoke-tested gallery of every exported
component, built from typed fixtures. `atlas` is a map of layouts, patterns, screens, components and themes, and its
grey-wireframe kit is already close to a "dimmed layout" view. The Vue package has no Storybook, no Histoire and no
`*.stories.*` files: all 238 story files belong to the parked React package, which used to deploy Storybook, a showcase
and a theme studio to GitHub Pages.

### Cited Findings
- **Workspace shape.** `apps/*` are pnpm workspace members of the package (`PKG/pnpm-workspace.yaml` → `packages: ['apps/*']`). Both are `"private": true`, version `0.0.0`, and depend on `@wow-two-beta/fe: workspace:*` (`PKG/apps/atlas/package.json`, `PKG/apps/playground/package.json`).
- **Both run against live source.** Neither app consumes `dist/`. They alias every public export to `src/` through `PKG/apps/lib-source-alias.mjs:4-21`, which reads `package.json#exports` and throws if a public export has no source file. Each app also sets `optimizeDeps.exclude: ['@wow-two-beta/fe']` (`PKG/apps/atlas/vite.config.ts`, `PKG/apps/playground/vite.config.ts`).
- **Dev ports.** Playground runs on 5176 and atlas on 5178 (`PKG/apps/playground/vite.config.ts`, `PKG/apps/atlas/vite.config.ts:16`). The port ledger lists both as local dev ports: "playground (Vite) · atlas — layouts, patterns, themes (Vite) | 5176 · 5178" (`WS/conventions/deployment/hosting/ports.md:25`). Playground starts with `pnpm playground` (`PKG/package.json` scripts; `PKG/README.md:200`), atlas with `pnpm --filter atlas dev` (`PKG/apps/playground/src/App.vue:58`).
- **Playground navigation.** Seven groups appear one at a time: layout, actions, forms, display, feedback, nav, overlays. Each loads lazily, and `?g=<group>` selects the group (`PKG/apps/playground/src/App.vue:7-18`, `PKG/apps/playground/src/navigation.ts:4-38`). The header has a theme select, a dark toggle and an "err / warn" diagnostics panel (`App.vue:62-106`). Vue warnings and errors are captured into that panel (`PKG/apps/playground/src/main.ts`, `app.config.warnHandler` / `errorHandler`).
- **How playground examples are registered.**
  - Each group has a hand-curated `groups/{Group}Group.vue`, 8 files in `PKG/apps/playground/src/groups/`.
  - `AutoGroup.vue` then renders every barrel-exported component that the curated page does not cover. It discovers them at runtime with `isComponent()` (an object carrying `__name`, `setup`, `render` or `template`) and `uncoveredComponents()` (`PKG/apps/playground/src/gallery/auto.ts:3-36`, `AutoGroup.vue:9-46`).
  - Typed fixtures live in `gallery/fixtures/*Examples.ts` and are built with `smokeCase(name, component, props, options)`. `props` is type-checked as `PropsOf<C>` (`PKG/apps/playground/src/gallery/fixtures/Example.ts:4-45`).
  - The fixtures are imported "through the public barrel on purpose — a component missing from `index.ts` fails here" (`PKG/apps/playground/src/gallery/fixtures/ActionsExamples.ts:21-25`).
- **Fixture counts.** Counted `smokeCase(` calls: actions 14 · display 124 · feedback 34 · forms 117 · layout 44 · nav 41 · overlays 50, for **424 in total** (`grep -c` over `PKG/apps/playground/src/gallery/fixtures/*.ts`). `componentExamples` concatenates all seven (`fixtures/index.ts:9-17`). The same fixtures feed the render and SSR tests (`PKG/README.md:273-279`, "fixtures: corresponding `tests/unit/presentation/*/*.ssr.test.ts`").
- **Playground in CI.** The release workflow builds playground and then runs a browser smoke test against the built dist: "Playground" → `pnpm --filter playground build`, then "Playground browser smoke" → `node apps/playground/tests/gallery-smoke.mjs` (`FE/.github/workflows/release-fe.yml:89-93`). The smoke script serves `../dist` from a local Node HTTP server and drives Playwright Chromium (`PKG/apps/playground/tests/gallery-smoke.mjs:1-50`).
- **Atlas sections.** Hash routes `#/section/id?query` cover home, layouts, patterns, guides, lab, screens, components, themes and studio, plus a hidden `frame` route for device-preview iframes (`PKG/apps/atlas/src/router.ts:3-40`; pages are lazy, `PKG/apps/atlas/src/App.vue:8-20`). The home page calls itself "A map of how our products are put together — grey wireframes to reason about structure, live components to check the details, and every theme to try the mood" (`PKG/apps/atlas/src/pages/HomePage.vue:44-49`).
- **Atlas content is typed data.** Counted from the content files:
  - 20 layout archetypes (`content/layouts.ts`), 5 pattern groups holding 23 patterns (`content/patterns.ts`), 4 decision guides (`content/guides.ts`) and 8 screens built from real SDK components (`content/screens.ts`).
  - Each archetype carries `summary`, `anatomy`, `shines`, `avoid`, `examples` (product evidence: `'TNIS' | 'Ocharo' | 'Haven' | 'Wheelhouse' | 'Atlas' | 'SDK'`), `related` and `tags` (`PKG/apps/atlas/src/content/model.ts:124-142`).
  - Each `Screen` lists "The SDK components the screen is built from, in reading order" (`content/screens.ts:1-9`). For example, the dashboard screen uses `SidebarMenu, StatCard, Sparkline, ToggleGroup, DataTable, Badge, Alert` (`screens.ts:12-18`).
- **Atlas Components page.** It reuses the playground fixtures, so "the atlas renders exactly what the render and SSR tests mount" (`PKG/apps/atlas/src/pages/ComponentsPage.vue:1-34`). Each family has a one-line role, such as "Buttons, toggles, toolbars and dials people press." Overlays render only on request (`ComponentsPage.vue:15-34`). Each card shows only the name and a live render inside an error boundary (`PKG/apps/atlas/src/shell/ComponentCard.vue:21-40`).
- **Research doc behind atlas.** `FE/engineering/architecture/analysis/layout-atlas/layout-atlas.md:1-8`. Its roadmap lists "Component wireframes per family (the lab currently draws layouts; components render live)" and "Real-component renderings of each archetype … beside the wireframe" (`layout-atlas.md:168-176`).
- **Neither app is deployed.** `release-fe.yml` grants only `contents: write` and has no Pages or deploy step (`FE/.github/workflows/release-fe.yml:17-18`). No workflow builds `atlas` (`grep -n atlas FE/.github/workflows/*.yml` finds nothing). The catalog entry for the fe sdk is `kind: sdk`, `deploy: none` (`WS/catalog.yml:367-374`).
- **Storybook and Histoire count.**
  - `*.stories.*`: **238 in total, all under `REACT/`**, and 0 under `PKG/` (find counts).
  - `.storybook/` exists only at `REACT/.storybook` and in its `dist`. No `histoire.config*` or `*.story.vue` exists anywhere in the repository (find).
  - The Vue rules say "Vue tests and executable demos live under `tests/` and `apps/playground/`; do not add colocated React stories" (`FE/CLAUDE.md:17`).
- **Legacy React precedent.**
  - The React `release.yml` built Storybook, `apps/showcase` and `apps/theme-studio` and deployed them as one GitHub Pages artifact (`FE/.github/workflows/release.yml:18-19, 162-192`), with `BASE_URL="https://wow-two-sdk-beta.github.io/wow-two-sdk-beta.ui"` (`release.yml:104`).
  - `REACT/apps/` still holds `playground`, `showcase`, `theme-studio` and `tests`.
  - The React showcase plan (`FE/engineering/architecture/analysis/showcase-plan.md:1-14, 31-60`) describes a routed showcase with "Per-domain kitchen-sink galleries" plus "Composed realistic screens". It also specifies a `scripts/build-manifest.mjs` that writes `manifest.gen.json` (route → components used) and a `#/coverage` page comparing that manifest with the barrel exports.
  - The roadmap still links "[Storybook](https://wow-two-sdk-beta.github.io/wow-two-sdk-beta.ui/)" (`WS/docs/ui-beta-roadmap.md:10`).

### Inferences
- Atlas is the natural seed for the gallery. It already has typed content models with "shines / avoid / product examples" verdicts, a page per family, live fixtures, theme switching, device frames and a code scaffold. A gallery would mostly add per-component metadata and a spotlight render.
- The playground fixtures already exist for all 424 smoke cases. A spotlight card can reuse them, so live examples need no new authoring. Only the "where to use" text and the philosophy text need writing.
- The React showcase's manifest and coverage design (route → components used, compared with the barrel) is a ready-made pattern for "every component appears in at least one spotlight". It was never ported to Vue.

### Gaps
- I did not check whether the React GitHub Pages site is still live: that needs a network call, which this lane excludes.
- I did not run the atlas or the playground, so the claims about what renders come from source, not from screens.

## 2. What per-component documentation exists, and what taxonomy and categories does the SDK use?

### Takeaway
Every Vue component has a co-located `*.spec.md` API contract: contract bullets, Props, Emits and Slots tables, an
exposed handle, and a link to its verification fixture. None has a philosophy or "when to use" document. The Vue package
has no `*.standard.md` files. The React-era "Subject Philosophy" template is the only precedent for one. The SDK's
categories are its seven presentation folders, mirrored by the subpath exports. A workspace convention adds a
16-kind "visual constructs" taxonomy with columns for "used with" and "used for".

### Cited Findings
- **Counts under `PKG/src`.** 468 `.vue` SFCs and 468 `*.spec.md` files. Every `.md` under `src` is a spec (find counts). 468 SFC files declare `defineOptions({ name … })` (grep). Pairing was not checked one to one: `src/reporting/Reporting.spec.md` documents a headless module.
- **Spec shape, using `Button` as the example.**
  - A one-sentence summary ("Renders a button that runs one command, carrying tone and size variants plus loading and skeleton states."), the source link and the public import (`PKG/src/presentation/actions/button/Button.spec.md:1-7`).
  - Then `## Contract`, `## Props` as a table of Prop · Type · Required · Default · Meaning (`:17-48`), `## Listeners`, `## Emits`, `## Slots`, `## Exposed handle` and `## Verification` linking the public render fixture (`:50-80`).
- **Spec headings across all 468 specs.**
  - `## Verification` 440 · `## Contract` 435 · `## Props` 430 · `## Slots` 429 · `## Emits` 427 · `## Exposed handle` 425 · `## Editing guarantees` 42 · `## Interaction guarantees` 18 · `## Behavior` 12.
  - 400 specs contain "Public render fixture" (grep counts).
  - Only 26 specs match a loose "when to use / use it when / prefer … over / philosophy / instead of" regex. That is a rough measure; the match lists were not reviewed.
- **JSDoc.**
  - Props interfaces carry one-line JSDoc per prop, for example `/** The visual surface style. */ readonly variant?: ButtonVariant;` (`PKG/src/presentation/actions/button/Button.vue:26-29`).
  - The summary sentence also appears as JSDoc above `defineOptions({ name: 'Button', inheritAttrs: false })` (`Button.vue:163-164`).
  - `Button.vue` has 40 `/**` blocks (grep). Other files were not sampled.
- **No philosophy docs in Vue.**
  - The Vue tree has 0 `*.standard.md` files; the React tree has 4 `*.standard.md` and 203 `*.spec.md` (find).
  - The React-era template `FE/engineering/architecture/templates/component-standard.md:3-7` opens with `## Subject Philosophy` ("What this component IS and what it's FOR … when-to-use vs alternatives … Continuous prose").
  - The React-era spec template has a `## Storybook coverage` section (`templates/component-spec.md:58-61`).
  - The Vue rules forbid "duplicate `*.standard.md` rules" (`FE/CLAUDE.md:18`).
- **What a new component must ship.** "source, spec, gallery fixture, focused DOM tests and the SSR/mount breadth cases" (`FE/engineering/development/rules.md:12`).
- **Workspace convention: three doc registers** (`WS/conventions/development/frontend/core/mla/components/components.md:10-19`):
  - definition (role, suffix, home) → `mla/constructs/`;
  - application ("which one to reach for, with what values") → `mla/components/`;
  - surface (every prop, slot, emit and state) → `{Component}.spec.md` in the SDK repo.
  - The same file rules that one component's props, slots, emits and states stay in its spec (`components.md:33`; also `mla/mla.md:32`).
- **Visual kinds taxonomy** (`WS/conventions/development/frontend/core/mla/constructs/visual/visual.md:36-53`).
  - 16 kinds, each with Is · Used with · Used for · Lives in: page, view, panel, layout, overlay, nav, action, control, field, display, feedback, indicator, state, provider, host, primitive.
  - Examples: `action` = "an intent trigger, no value", used for "running a command", lives in `actions/`; `state` = "a region replacement or busy mask", used for "empty · loading · failed".
  - Rule: "must pick the kind first — it fixes the suffix … and the group folder" (`visual.md:20`).
- **Folder taxonomy, the seven presentation categories** (`PKG/src/presentation/*`):

  | Category | Component folders | `.vue` SFCs | Playground smoke cases | Atlas family role (`ComponentsPage.vue:15-34`) |
  |---|---|---|---|---|
  | actions | 17 | 15 | 14 | Buttons, toggles, toolbars and dials people press |
  | display | 120 | 130 | 124 | Data, media and text shown to read |
  | feedback | 38 | 34 | 34 | Status, progress, alerts and toasts |
  | forms | 119 | 131 | 117 | Inputs and pickers that hold a value |
  | layout | 54 | 44 | 44 | Shells, stacks, grids and panels |
  | nav | 16 | 42 | 41 | Menus, bars, tabs and links between places |
  | overlays | 15 | 42 | 50 | Modals, popovers and sheets over the page |
  | **total** | 379 | 438 | 424 | |

  Folder counts come from `ls -d`, SFC counts from `find -name '*.vue'` and smoke cases from `grep -c 'smokeCase('`.
  The other 30 SFCs sit outside `presentation`: foundation primitives (14 under `src/foundation/primitives`), plus
  router, auth, flags, i18n, icons and query adapters (find).
- **Subpath exports mirror the categories.** `./presentation/{actions,display,feedback,forms,layout,nav,overlays}`, plus a few single-component subpaths with CSS: point-control, tour-popover, toast-host and modal styles (`PKG/package.json` `exports`).
- **`ideas/constructs-taxonomy-analysis.md` is not a UI taxonomy.** It measures the .NET backend suffix keep-list: "Measured against `conventions/development/backend/dotnet/core/mla/constructs/constructs.md` … keep-list rows 37" (`WS/ideas/constructs-taxonomy-analysis.md:9-17`).
- **`ideas/mla-components-discovery.md` is also .NET only.** "Read: `wow-two-sdk.backend.beta` (637 `.cs`)" (`WS/ideas/mla-components-discovery.md:9`).
- **The React-era component catalog is generated, but stale for Vue.**
  - `FE/engineering/architecture/component-catalog.md:1-15` says "Every shipped component in `@wow-two-beta/ui` … **249 entries**", last updated 2026-07-13.
  - It is generated by `gen-catalog.mjs`, which takes each name from the spec h1 and each purpose from the spec's `## Purpose` line, with hand `OVERRIDES` (`gen-catalog.mjs:1-6, 20-40`).
  - The generator points only at React source: `SRC = '../codebase/wow-two-front-beta-sdk/src'` (`gen-catalog.mjs:13-15`).
- **Design conventions relevant to component pages.**
  - Theme patterns are ambient glass or solid; the fe sdk default theme is solid (`WS/conventions/design/theme/theme-patterns.md:12-16`).
  - UI copy: "must not add an eyebrow, a tagline or a pitch to an operational screen", and "must keep marketing copy on marketing surfaces" (`WS/conventions/design/content/ui-copy.md:12, 19`).
  - Text read once, such as a legend or a how-to, goes to the guidance domain (`ui-copy.md:17-18`).

### Inferences
- The spec.md first line is a ready one-line "what it is" for every card. The `## Props` / `## Slots` / `## Emits` tables are a ready integration section, parseable as Markdown tables.
- "Where to use" metadata has a home in two places already: the 16-kind table (`Used with` / `Used for`) and the application register (`mla/components/`). A gallery that writes its own "where to use" prose would add a fourth place unless it reads from, or writes to, one of these.
- The forbidden duplicate `*.standard.md` rule and the "one doc, one register" design mean a philosophy page needs an explicit home decision. Options are a new section in `*.spec.md`, a revived Vue `*.standard.md` "Subject Philosophy", or gallery-owned content.
- Folder and kind are not one to one. `display/` holds view, panel, state and indicator kinds (`visual.md:39-50`). The gallery could offer both a category facet (folder) and a kind facet.

### Gaps
- I did not verify whether the 468 specs pair one to one with the 468 SFCs, or whether any spec lacks a Props table on purpose.
- I did not read the 7 specs that match "generated|do not edit|derived from" to see whether any spec is machine-generated.
- I did not check the curated `groups/*Group.vue` demos for per-component notes; `Demo.vue` takes an optional `note` prop (`PKG/apps/playground/src/gallery/Demo.vue:13-26`).

## 3. Which hooks could a spotlight or outline render mode use?

### Takeaway
Components expose state attributes (`data-state`, `data-disabled`, `data-skeleton` and others) but **no attribute or
class names the component**: `data-slot`, `data-component` and `data-part` have 0 hits, and there are no `ui-*`
classes. They are identifiable only through the Vue instance name, which every SFC sets with `defineOptions`. Theme
tokens are complete CSS custom properties. Skeleton state is a prop on 32 SFCs and can also be provided to a whole
subtree. "Outline" exists only as a visual variant on a few components, not as a wireframe mode. The atlas wire kit
already draws themed grey wireframes with one accented element.

### Cited Findings
- **No component-identifying DOM hooks.** `grep` finds 0 `data-slot`, and no `data-(component|ui|sdk|part|name)` or `(ui|wt|w2)-*` class across `PKG/src/presentation/**/*.vue` or its `.ts`.
- **State attributes that exist** (`grep -o` frequency over `presentation/**/*.vue`):

  | Attribute | Occurrences |
  |---|---|
  | `data-state` | 80, in 50 SFCs |
  | `data-disabled` | 28 |
  | `data-readonly` | 25 |
  | `data-skeleton` | 24, in 25 files |
  | `data-active` | 13 |
  | `data-selected` | 11 |
  | `data-roving-focus-item` | 10 |
  | `data-stack` | 9 |
  | `data-orientation` | 9 |
  | `data-side` | 7 |
  | `data-dragging` | 7 |
  | `data-pressed` | 5 |
  | `data-loading` | 3 |

  Example: `Button` defines `ButtonDataState = { Loading, Skeleton, Disabled }` (`PKG/src/presentation/actions/button/Button.vue:148-153`) and binds `'data-state': dataState.value` on the root (`Button.vue:488`).
- **Stable component names.**
  - Every SFC has `defineOptions({ name })`; Button spells it out as `defineOptions({ name: 'Button', inheritAttrs: false })` (`Button.vue:161-164`).
  - The playground relies on compiled `__name` to tell components apart (`PKG/apps/playground/src/gallery/auto.ts:3-16`).
  - Two SFCs also declare `const ComponentName = '…'`, which feeds dev warnings (`Button.vue:144, 263-277`).
- **Skeleton hooks.**
  - The `isSkeleton` prop appears in 32 SFCs (grep).
  - Button's spec: "The content-loading state — keeps size and radius, masks content, pulses under `motion-safe`. Defaults to the nearest `DataRegion` first load." (`Button.spec.md:34`).
  - Subtree context: `useSkeletonState()` and `provideSkeletonState(mode)` (`PKG/src/presentation/feedback/skeletonState/SkeletonStateContext.ts:44, 61`).
  - The skeleton style keeps a `GrayText` outline in forced-colors mode (`Button.variants.ts:62-63`).
- **Outline variant, visual only.** `Outline: 'outline'` is declared in 6 files: the Button, Badge, CheckboxInput and ToggleInput variants, plus `foundation/styles/SurfaceStyles.ts` and `foundation/styles/constants/Tones.ts` (grep). In Button, `outline: 'bg-transparent'` comes with an outline × tone matrix (`Button.variants.ts:12, 70, 202-204`).
- **Theme tokens.**
  - `PKG/src/index.css` declares `@theme {` at `:57` and holds 178 custom-property lines (grep). Semantic colors include `--color-primary`, `--color-primary-foreground` and `--color-primary-soft` (`:138-141`), with dark overrides at `:256-259`. The `dark` variant is `@custom-variant dark (&:where(.dark, .dark *))` (`:7`).
  - The token model is TypeScript: `ToneFamilies = ['primary', 'accent', 'destructive', 'info', 'success', 'warning']`, `SurfaceTokens` and `SemanticTokens` (`PKG/src/foundation/themes/Tokens.ts:14, 19, 75`).
  - The theme registry: `THEMES`, `getTheme` and `ThemeCatalog` (`PKG/src/foundation/themes/Registry.ts:300-331`). The build emits `dist/themes.css` and `dist/themes.json` (`PKG/scripts/build-themes-css.mjs:1-6`), exported as `./themes.css` and `./themes.json` (`PKG/package.json`).
- **Density and ambient hooks.**
  - `[data-density='compact'|'comfortable'|'spacious']` rescales every spacing utility through `--spacing`; `--ui-density-scale` is 0.875 / 1 / … (`index.css:537-555`).
  - `.surface-ambient { background-image: var(--theme-ambient, none) }` (`index.css:418-420`).
- **Atlas wire kit, the closest existing "dimmed layout + one highlight".**
  - `wire.css` mixes wireframe inks from the active theme: `--w-ink` is `color-mix(… var(--color-foreground) 17%, transparent)` and `--w-accent` is `color-mix(… var(--color-primary) 72%, transparent)`. The file says: "every wireframe reads in the chosen theme, light or dark" (`PKG/apps/atlas/src/wire/wire.css:1-15`).
  - `LayoutWire` "Draws one `LayoutSpec` as a grey wireframe at a device size", adapting sidebars to rails and menus on phones (`LayoutWire.vue:9-12, 28-38`). Single elements get accent marks (`wdot-accent`, `wl-accent`; `LayoutWire.vue:82-217`, `PanelWire.vue:20-102`).
- **Scoping and framing helpers in atlas.**
  - `ThemeScope.vue` "Scopes a subtree to one mode of a previewed theme without touching the atlas root. Portaled UI escapes the scope to `<body>`" (`PKG/apps/atlas/src/shell/ThemeScope.vue:4-7`).
  - `FramePage.vue` renders one screen bare in an iframe, so "media queries, `useMediaQuery` and touch layouts all see the frame's width", and it applies `data-density` from the query (`PKG/apps/atlas/src/pages/FramePage.vue:9-22`).
  - `PreviewBoard.vue` builds "A product surface built only from SDK components and theme tokens", with the note that portaled UI "would leave the preview scope" (`PKG/apps/atlas/src/shell/PreviewBoard.vue:29-30`).

### Inferences
- A spotlight cannot select a component by CSS today. It has three options:
  1. Wrap the spotlit example in a gallery-owned marker element (simplest; fixtures already render inside a card).
  2. Walk Vue instances by `type.name`, a dev-only approach that is brittle in production builds.
  3. Add a stable root attribute such as `data-component="Button"` to SDK roots. That is an SDK change, which the workspace's "SDK change loop" doctrine allows.
- The "dimmed layout" could be built two ways: the atlas wire kit (a grey `LayoutSpec` drawing plus one accented region), or a real screen with `provideSkeletonState` over the surrounding subtree and the spotlit component left live. Both reuse existing mechanisms.
- Overlays, toasts and popovers portal to `<body>` and escape `ThemeScope`. A spotlight of an overlay needs an iframe (the `FramePage` pattern) or on-demand mounting, as the atlas does for overlays.

### Gaps
- I did not verify whether any component already accepts a consumer `data-*` attribute that reaches its root. `Button` forwards passthrough attrs (`Button.vue:466-490`), but other components were not checked.
- I did not check whether `isSkeleton` or skeleton context covers every display and forms component; only the 32 SFCs that declare `isSkeleton` were counted.

## 4. Is there a machine-readable component list, and do any tools generate prop tables today?

### Takeaway
There are several partial machine-readable sources and no single component manifest:
- `package.json#exports`, 72 keys;
- the runtime barrels, enumerable through the playground's `isComponent`;
- `defineOptions` names;
- the typed fixtures, 424 cases with type-checked props;
- the spec.md Markdown tables;
- the `.d.ts` output.

No Vue tool generates prop tables. No `vue-component-meta` or `vue-docgen-api` is installed. The only catalog generator
(`gen-catalog.mjs`) targets the parked React source.

### Cited Findings
- **Export manifest.** The README says "This matrix covers all **72 manifest export keys**: 68 JavaScript entries and four asset/metadata entries" (`PKG/README.md:217`). `lib-source-alias.mjs` already parses `manifest.exports` into source paths (`PKG/apps/lib-source-alias.mjs:9-21`).
- **Runtime enumeration.** `allComponentNames(namespace)` "Counts every component a barrel exports, curated or not" (`PKG/apps/playground/src/gallery/auto.ts:30-36`). AutoGroup shows "{rest.length} of {total} exported components" (`AutoGroup.vue:33, 42-46`).
- **Barrels.** Each category `index.ts` re-exports its component folders (`export * from './button'` …), and each folder exports `default as X` plus variants, enums and types. Example: `export { default as Button, type ButtonProps, type ButtonSize } from './Button.vue'` (`PKG/src/presentation/actions/index.ts`, `.../button/index.ts`).
- **Typed fixtures.** `SmokeCase { name, component, props, slot?, wrap?, skipSsr?, skipMount? }`, built through `smokeCase<C>(name, component, props: PropsOf<C>, …)` (`PKG/apps/playground/src/gallery/fixtures/Example.ts:12-45`).
- **Spec tables.** 430 specs carry a `## Props` Markdown table, 427 `## Emits` and 429 `## Slots` (Q2 counts).
- **No doc-generation tooling in the Vue package.**
  - `grep` of `PKG/package.json` finds no `vue-component-meta`, `vue-docgen`, `typedoc` or `api-extractor`.
  - `@microsoft/api-extractor` appears only in `PKG/pnpm-lock.yaml:483-486`. It is probably a transitive dependency of `vite-plugin-dts`, which is a devDependency (`PKG/package.json`); this was not confirmed.
  - `PKG/scripts/` holds `benchmark-core`, `build-themes-css`, `check-capabilities`, `check-package`, `check-sfc` and `source-paths`. None generates docs (header comments read).
- **Type output.** `vite-plugin-dts` emits the `.d.ts` files that `types` points to (`PKG/package.json` `"types": "./dist/index.d.ts"`, devDependency `vite-plugin-dts`).
- **React-era generator.** `node engineering/architecture/gen-catalog.mjs` regenerates `component-catalog.md` from spec h1s and `## Purpose` lines, using "Node builtins only; no deps" (`FE/engineering/architecture/gen-catalog.mjs:1-6`). Its `SRC` is the React package (`:13`). The catalog convention says "**Derived, not hand-maintained** … Never hand-edit rows — they drift." (`FE/engineering/architecture/component-catalog.md:11-12`).
- **Other JSON in the repo is not a component list.** `vue-sdk-optimization/components-coverage.json` is a file inventory (`scope`, `totals`, and `files[] { path, lines, kind, inspection, riskFeatures }`) (`FE/engineering/architecture/analysis/vue-sdk-optimization/components-coverage.json`).
- **Code-generation precedent in atlas.** `scaffold(spec)` writes "A starter SFC for a lab composition: named regions, SDK components and placeholder data" (`PKG/apps/atlas/src/content/scaffold.ts:305-306`), shown through `shell/ExportBlock.vue`.

### Inferences
- The cheapest manifest would be a Node script in the style of `gen-catalog.mjs`, pointed at `PKG/src/presentation`. It would join three sources:
  - the folder, giving the category;
  - the spec's h1, first line and Props / Slots / Emits tables, giving name, summary and API;
  - the fixtures, giving the live example.
- Real prop types without parsing Markdown need a docgen step such as `vue-component-meta` over the `.vue` sources. That would add a new devDependency and is not in the repo today.
- The spec tables are maintained by hand, by inference: no generator was found. A gallery that reads them shows the specs as written, drift included.

### Gaps
- I did not confirm whether the spec.md Props tables are generated by a tool outside the repo, such as an agent sweep.
- I did not count the components each barrel exports at runtime. That needs the Vite runtime; the static grep of `export { default as … }` undercounts because of nested re-exports.

## 5. What does it take to host a new web app via Wheelhouse, and which platform apps could serve gallery feedback or analytics?

### Takeaway
Wheelhouse deploys **products**, never single apps or libraries. To be deployed, a repository needs:
- a hub catalog entry with `deploy: wheelhouse`;
- an `engineering/deployment/deploy.yml` (descriptor 2) declaring sites and Docker services, each with a health check;
- a Dockerfile that builds the image without environment values;
- the marker workflow `.github/workflows/publish-docker-image.yml`, which calls the shared pipelines workflow.

Wheelhouse imports the catalog entry and derives the release source itself. Each `main` release goes to dev
automatically and is promoted to prod by digest. Wheelhouse binds each site to a host per environment, with public or
private exposure.

No product in the workspace is a static-only Wheelhouse deploy yet. Haven's Caddy edge image is the nearest precedent
(compose only), and the descriptor convention's example models such an `edge` service.

Feedbacks, Logs, Monitoring and the Docs site (`wiki`) are planned, not built. The fe sdk already ships the
`/reporting` and `analytics` client modules a gallery could wire.

### Cited Findings
- **What Wheelhouse is.** "the internal product ops & deploy control plane … Deploys product release bundles to the VPS targets its inventory defines, over SSH (Docker + ingress) … Single-user; **never exposed publicly**." (`WH/CLAUDE.md:5-7`). Its own frontend is Vue 3, Vite, Tailwind v4 and `@wow-two-beta/fe` (`WH/CLAUDE.md`, Structure block).
- **Catalog import.**
  - Wheelhouse reads `catalog.yml` from three hubs at `main`: `wow-two/wow-two-ws`, `sulton-max/10x-ventures` and `ocharo-hq/ocharo-ws` (`WH/engineering/architecture/architecture.md:436-438`).
  - `POST /api/catalog/import` turns "an entry with `deploy: wheelhouse` and a repository" into a product; anything else is skipped with a warning (`architecture.md:455-462`).
  - The catalog rule: "must set `deploy: wheelhouse` when Wheelhouse deploys the repo … and `ci` when the repository's own CI does" (`WS/conventions/development/repo/catalog/catalog.md:120-121`).
- **Release source is derived, never typed.** "asset `{slug}-release.tar.gz`, workflow `publish-docker-image.yml`, one image per `deploy.yml` service at the branch head" (`WH/engineering/architecture/architecture.md:357-359`). Images live on GHCR, one repository per service, and "the digest is the deployment identity" (`architecture.md:306`).
- **The descriptor file.** One `engineering/deployment/deploy.yml` per product repo (`WS/conventions/deployment/descriptor/deploy-descriptor.md:17`). Key rules:
  - "must build every image environment-free" (`:21`);
  - "must let an SPA read its public settings at runtime, never from build-time variables" (`:22`);
  - "must give every service a health check; the runner refuses a service without one" (`:34`);
  - "must declare the product's entry points as named `sites`" (`:39-40`);
  - "must not name a host, zone, address or proxy setting; Wheelhouse binds each site to one host per environment" (`:41`);
  - "must not publish host ports" (`:42`);
  - `sites.<site>.exposure` is `public` (internet) or `private` (private network), default `public` (`:133`).
- **Routing.** "One product per host; a product's API lives under its own host's `/api`" (`deploy-descriptor.md:202`). The runner renders Traefik routers per site path (`:212-221`).
- **Static-service shape in the convention's example.** An `edge` service with `port: 80`, `health: { command: [wget, -q, -O-, http://localhost/healthz] }` ("when the image has no curl") and `capabilities: [NET_BIND_SERVICE]` (`deploy-descriptor.md:109-118`).
- **Real static-edge precedent.** Haven's `edge.Dockerfile` builds the pnpm workspace in a Node stage, then copies each `apps/*/dist` into a `caddy:2-alpine` runtime with a Caddyfile (`WS/workbench/maxs-projects/ventures/saas/10x-ven-haven/engineering/deployment/edge.Dockerfile`). Haven has no `deploy.yml` yet, only `docker-compose.yml` (directory listing). The delivery-pipeline doc says Haven does not call the shared workflow yet (`WS/docs/delivery-pipeline.md:23`).
- **Common product shape is single-host .NET serving the SPA.**
  - The product template's descriptor has one `sample` service serving `app: { paths: [/, /api] }`, with `health: /health` and `memory: 256m` (`WS/workbench/wow-two-sdk-beta/wow-two-sdk-beta.product-template/engineering/deployment/deploy.yml`).
  - Its Dockerfile builds the Vue SPA in a `node:24` stage and copies `apps/web/dist` into `Sample.Api/wwwroot` before `dotnet publish` (`.../product-template/engineering/deployment/Dockerfile`).
  - Museums Gallery, "frontend-only v0.1" in memory, still deploys as one .NET service serving `/` and `/api` (`WS/workbench/maxs-projects/ventures/consumer/ventures.museums-gallery/engineering/deployment/deploy.yml:27-43`).
  - Every `deploy.yml` found in the workbench declares exactly one Dockerfile; the `.local` copies were excluded (sampled by `grep -c dockerfile`).
- **CI.** A product keeps `.github/workflows/publish-docker-image.yml` as "the marker file Wheelhouse detects; it is the product's one CI file", calling `wow-two-platform.pipelines/.github/workflows/delivery.yml` pinned to a tag `v0.9.0` or later (`deploy-descriptor.md:407-411`). The shared workflow skips publishing for docs-only pushes and builds each changed service from `deploy.yml` (`deploy-descriptor.md:442-450`).
- **Release flow.** "must work on `main` only", "must run two environments per product: `dev` and `prod`", "must deploy every `main` release to dev automatically", "must promote that same release to prod by digest" (`deploy-descriptor.md:384-389`).
- **Versions.** Products take `X.Y` from the newest `version-track/v{X.Y}/` folder; CI assigns `Z` (`WS/docs/delivery-pipeline.md:13-23`).
- **Domains are not automated yet.** "Domains remain a scaffold model" (`WH/CLAUDE.md`, Core domains). "Today a target names each site's host, or dev follows the server's host pattern; domain bindings replace both." (`deploy-descriptor.md:210`).
- **Platform apps a gallery could use** (`WS/docs/platform-apps.md`):
  - #5 **Feedbacks**: "incident reports → issues; triage inbox", state "client in the fe sdk `/reporting`; app not started" (`:30`).
  - #6 **Logs**: "SDK emits OTel; no store" (`:31`).
  - #7 **Monitoring**: uptime and health checks, Telegram alerts, domain and SSL expiry; "Wheelhouse spec P3 only" (`:32`).
  - #13 **Docs site**: "the platform's knowledge site (Starlight / Docusaurus)", ship gate "conventions + SDK docs published" (`:38`), to be renamed `wiki` (`:91`).
  - Product analytics is deferred: "a product needs funnels | Plausible / Umami via Wheelhouse" (`:123`).
  - The roadmap rates the docs site "**Buy/wrap** (Docusaurus / Astro Starlight)" (`WS/docs/platform-roadmap.md:83, 110`).
- **fe sdk client modules a gallery could wire today.**
  - `@wow-two-beta/fe/reporting`, wired with `createReporter({ app, sink: httpReportSink({ endpoint: '/api/reports' }) })`. "Nothing records until the app wires a tracker … and nothing leaves the device until an incident is sent." (`PKG/src/reporting/Reporting.spec.md:1-26`).
  - `@wow-two-beta/fe/analytics` contains `Analytics.ts`, `AnalyticsProvider.ts`, `ConsoleAnalyticsProvider.ts` and `MemoryAnalyticsProvider.ts` (directory listing). The React-era vector registry describes it as a "headless bus: `track`/`identify`/`page` · provider fan-out … consent gate" (`FE/engineering/architecture/vector-registry.md`, Analytics row).
  - The Feedbacks spec frames itself as "a self-hosted Sentry for the fleet, user-facing first" (`WS/ideas/feedbacks-spec.md:1-7`).
- **Distribution forms.** Wireable infra (library), self-hosted service (client + Docker image) or provided service (`WS/docs/platform-model.md`, Three Distribution Forms table).

### Inferences
- **Minimum Wheelhouse path for a static gallery.** One `edge`-style service: a Node build stage followed by a Caddy or nginx runtime. It needs a health endpoint (for example `/healthz`) and a `wget`/`curl` health command, one `site` (`primary: true`, `exposure: public` or `private`), the marker workflow calling `delivery.yml`, a catalog entry with `deploy: wheelhouse`, and a version track. No backend is required, but no product has shipped that shape through the descriptor yet, so the first one is the proving run.
- **Feedback before Feedbacks exists.** `/reporting` needs an HTTP sink endpoint. A static-only gallery has none, so collecting feedback means either waiting for Feedbacks or adding a small backend `/api` service.
- **Usage analytics.** The SDK `analytics` bus needs a provider; only console and memory providers ship. Plausible or Umami is the planned buy, and it is deferred until a trigger.
- **The Docs site overlaps the gallery's purpose.** Its ship gate includes "SDK docs published". The gallery and the docs site should probably be decided together: a gallery inside the wiki, or a gallery the wiki links to.

### Gaps
- I did not read the `wow-two-platform.pipelines` `README.md` or `delivery.yml`, so the exact caller keys for a frontend-only check are unverified.
- Server targets, placement and the private-network setup are deliberately not described. Those are private host facts, out of scope.
- I found no doc that says whether Wheelhouse supports a product whose only service is a static file server. The descriptor allows it structurally; nothing confirms it in practice.

## 6. Which conventions constrain the gallery: the frontend standard, a new repo vs an app in the fe sdk repo, naming and versioning?

### Takeaway
The gallery must be Vue 3, strict TypeScript, Vite, Tailwind v4 and lucide, and must consume only `@wow-two-beta/fe`'s
public exports. The SDK repo allows sandboxes under `apps/*`, but they are never published, and a library's catalog
entry stays `deploy: none`. Hosting the gallery from the fe sdk repo therefore conflicts with today's rules; a
separate repository (product or platform-app shape) fits them. Platform-app naming forbids brands and wants a plural
or mass noun. Products version as `X.Y.Z` from a version track; the SDK stays `0.0.y`.

### Cited Findings
- **Frontend standard.** "must use Vue 3, strict TypeScript, Vite and Tailwind v4 for new product frontends and UI work", "must build reusable frontend capabilities in the fe sdk `@wow-two-beta/fe`; products consume its public exports", "must use `lucide-vue-next` as the icon set" (`WS/conventions/development/repo/repo-conventions.md:67-72`). New SDK capabilities stay on the Vue track (`:75`).
- **Archetypes.** Product or venture (`product/` + `engineering/`), SDK or library ("`engineering/` only, one package under `engineering/codebase/{slug}/`"), and domain ("product shell; be packages + service + tests, fe package + hosted app") (`WS/conventions/development/repo/structure/repo-structure.md:12-14`). "must scaffold a product repo with the `create-repo` skill, from `wow-two-sdk-beta.product-template`" (`repo-structure.md:16`).
- **Sandboxes in an SDK repo.** The SDK structure lists `apps/` as "workspace sandboxes — playground, atlas" (`WS/conventions/development/repo/structure/sdk-structure.md:56`). "must keep sandboxes in `apps/*` inside the package, as workspace members" and "must not publish `apps/*`" (`sdk-structure.md:118-119`). The SDK repo has no `deployment/` folder in its layout (`sdk-structure.md:40-60`).
- **Catalog rules.** "must give a library, KB module or template its own single-repository entry with `deploy: none`" (`WS/conventions/development/repo/catalog/catalog.md:12`). "must keep a library, KB module or template on its own single-repository entry; several repositories mean one deployable product, nothing else" (`catalog.md:144-145`). The fe sdk entry today is `kind: sdk`, `deploy: none` (`WS/catalog.yml:367-374`). Platform apps are filed under `wow2-platform` with kind `platform`, and community apps under `wow2-apps` (`catalog.md:115-119`).
- **Domain repos are the one SDK-org shape with a hosted app.** "must build the hosted pages and the admin console as one app, `apps/web/`" (`WS/conventions/development/repo/structure/domain-structure.md:120`). Files and Harvest are SDK-org repos under platform entries, `deploy: none` for now (`WS/catalog.yml:265-290`).
- **Platform-app naming** (`WS/docs/platform-apps.md:50-51`): "must name a platform app for what it handles, never with a brand" and "must use the plural of what the app manages", or a mass noun. The identifier table gives repo `wow-two-platform.{name}`, code dirs `{name}.frontend-services/` and workspace packages `@{name}/{app}` (`platform-apps.md:62-65`). Apps are built strictly in queue order: "must ship the top unshipped app … before starting the next app's own repo" (`platform-apps.md:13`), and a gallery has no row in the Order table.
- **KB org.** `wow-two-kb` is described as "code samples, runnable demos, real-world docs" (`WS/.claude/repo-registry.md:93`).
- **Versioning.** The SDK is "Beta-forever … Package-scoped CI auto-bumps `0.0.y`" (`FE/CLAUDE.md:8`). Products take `X.Y` from the version-track folder and CI assigns `Z` (`WS/docs/delivery-pipeline.md:13-23`).
- **Dev ports.** "check here before picking one"; a frontend Vite port is an even port (`WS/conventions/deployment/hosting/ports.md:5-6`).
- **Design spec location for a product UI.** "must keep it at `engineering/research/design-research/design-research.md` in the product repo", with light and dark token tables mapped to `@wow-two-beta/fe` (`WS/conventions/design/design-conventions.md`, Per-app specs).
- **SDK gaps go to the SDK.** "A product blocked on a missing or wrong SDK API fixes the SDK rather than working around it in the product" (`WS/CLAUDE.md`, SDK doctrine). This covers, for example, adding a `data-component` root attribute.

### Inferences
- There are three conforming placements:
  1. **Keep the gallery as an `apps/*` sandbox in the fe sdk repo, undeployed** (today's atlas model). It fits every rule but is not hosted.
  2. **A new product-shaped repo**, scaffolded with `create-repo`, catalog `deploy: wheelhouse`, consuming the published `@wow-two-beta/fe`. This is hostable but loses atlas's live-source hot reload, and its examples pin to a published SDK version.
  3. **Fold it into the planned Docs site / `wiki` (#13).** This matches "SDK docs published", but #13 sits far down the queue.

  Hosting the gallery straight from the fe sdk repo would need a convention change: the library catalog entry, or the SDK archetype, gaining `deployment/`.
- Under platform-app naming, a hosted gallery repo would read like `wow-two-platform.components` (plural of what it shows), not a brand. That is an inference from the rule; no doc names it.
- A separate repo that pins the published SDK cannot reuse the playground fixtures by relative import, as `ComponentsPage.vue:3-9` does today, unless the fixtures move into an exported or shared package.

### Gaps
- I found no convention or decision about where SDK documentation and showcase sites live, beyond Docs site row #13 and the React-era GitHub Pages deploy.
- I did not check whether `create-repo` supports a frontend-only shape without the .NET backend. `product-conformance.md:13` allows "a frontend-only product owes no backend row", but the template ships the .NET single-host shape.

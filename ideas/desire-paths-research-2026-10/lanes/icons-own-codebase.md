# Icons in our own codebase — fe sdk and its consumers

*Research date: 2026-10-27. Read-only sweep of the local workspace; no network calls.*

Path keys used below (all relative to the `wow-two-ws` root):

- `SDK/` = `workbench/wow-two-sdk-beta/wow-two-sdk-beta.fe/engineering/codebase/wow-two-sdk-beta-fe/`
- `V/` = `workbench/maxs-projects/ventures/`
- `WH/` = `workbench/wow-two-platform/wow-two-platform.wheelhouse/engineering/codebase/wheelhouse.frontend-services/apps/web/`
- `CONV/` = `conventions/development/frontend/core/mla/`

Method and scope:

- Consumers = every `package.json` under `workbench/` that names `"@wow-two-beta/fe"`, minus `node_modules`, `dist` and the parked React `wow-two-front-beta-sdk`. That gives 42 files; minus the SDK's own root, **41 consumer package roots in 31 repos**. The roots include the SDK's `apps/playground` and `apps/atlas`, 4 domain `fe-*` packages and the product template.
- The census scripts skipped `node_modules`, `dist`, `build`, `coverage`, `public`, `ios` and `android` (Capacitor copies of built assets). The template-attribute and state scans also skipped `tests` and `e2e`.
- Counts come from regex scans (import statements, tag names, attribute patterns), not from an AST, so treat them as close but not exact. The scripts are in the session scratchpad and are not committed.
- Not repeated here: `lanes/own-codebase.md` (it already covers `Destinations [{label, path, icon}]` in 10 apps, `:249`), `lanes/interaction-timing.md` and `lanes/notifications.md`.

---

## 1. Which icon package(s) the SDK and apps depend on, and how icons are rendered

### Takeaway
There is exactly one icon library, `lucide-vue-next` `0.460.0`. It is a regular SDK dependency and every consumer that declares it uses the same range. Icons are passed as components (per-icon ESM imports). Consumers mostly render the lucide component directly (859 tags); only one app goes through the SDK `Icon` wrapper (76 tags). No consumer uses a sprite, an icon font, a string-name registry or a second icon package.

### Cited Findings
- The SDK declares `lucide-vue-next: ^0.460.0` under `dependencies`, not as a peer. The other runtime deps are `@floating-ui/vue`, `clsx`, `marked`, `tailwind-merge`, `tailwind-variants` and so on. — `SDK/package.json` (dependencies block)
- Installed version: `0.460.0` in the SDK and in all 29 consumer roots that declare it. — `SDK/node_modules/lucide-vue-next/package.json`; per-root `node_modules/lucide-vue-next/package.json` (census)
- Consumer declarations: 28 roots declare `^0.460.0` and one pins exactly `0.460.0` (`V/saas/ventures.surface-pattern/.../apps/web/package.json`). The SDK's `apps/playground` and `apps/atlas` import lucide without declaring it and resolve it through the SDK workspace. The other 10 roots neither declare nor import it: domain-template ×2, files ×2, harvest ×2, identity ×2, product-template, Arcade. — census over all 41 `package.json` files
- No second icon package is declared or imported anywhere. The checks covered `@heroicons/*`, `@phosphor-icons/*`, `@tabler/icons*`, `@iconify/*`, `unplugin-icons`, `~icons/*`, `@fortawesome/*`, `@mdi/*`, `simple-icons`, `vite-svg-loader` and others: 0 hits in deps and 0 import statements. No `.svg` file is imported as a module (0 `from '….svg'`). — census (`other_icon_imports`, `svg_imports` both empty)
- The installed `lucide-vue-next 0.460.0` ships 1,540 icon modules (`dist/esm/icons/*.js`) under the ISC licence. — `SDK/node_modules/lucide-vue-next/dist/esm/icons/`, `.../package.json` `"license": "ISC"`
- The SDK `Icon` wrapper takes a component, not a name. It is `readonly icon: IconAdapter` (`SDK/src/foundation/icons/icon/Icon.vue:36`), and `IconAdapter = Component<IconAdapterProps>` with a numeric `size` only (`:5-18`). The `size` defaults to 20 (`:61`). It renders `<component :is="icon">` and adds `aria-hidden` unless an `aria-label` is passed, in which case it sets `role="img"` (`:73-82`).
- The `size` prop is narrowed to `number` on purpose. The source comment says widening it "makes every lucide icon unassignable to `IconAdapter`". — `SDK/src/foundation/icons/icon/Icon.vue:6-14`
- `foundation/icons` exports `Icon`, `Spinner`, `SeverityIcons` and `SeverityIconClasses`, and re-exports no lucide glyphs. — `SDK/src/foundation/icons/index.ts:1-3`
- The SDK build keeps lucide external: `dist` files import `lucide-vue-next` (28 dist files), so each app tree-shakes per glyph. — `SDK/vite.config.ts:29-40,76`; grep of `SDK/dist`
- `AccessibleIcon` clones the child icon vnode with `aria-hidden` and adds a `VisuallyHidden` label. — `SDK/src/foundation/primitives/accessibleIcon/AccessibleIcon.ts:20-33`
- Inside the SDK: 86 source files import lucide; 40 lucide tags are rendered directly in templates and 88 go through `<Icon>`. — grep `SDK/src`; attribute scan
- In consumers: 859 lucide tags are rendered directly and 76 `<Icon>` tags are used. All 76 `<Icon>` tags are in Transcript Forge (e.g. `V/saas/10x-ventures-transcript-forge/.../src/presentation/settings/SettingsPage.vue:61-62`). Another 57 `<component :is="…icon…">` sites in 19 roots render an icon taken from data. — attribute scan; census `icon_wrapper_tags`
- Two string-name registries exist, both outside the SDK contract:
  - The SDK `IconPicker` keeps a module-private `BuiltInIcons: Record<string, IconAdapter>` of about 50 lucide glyphs (`SDK/src/presentation/forms/iconPicker/IconPicker.vue:2-60` and the map after it; spec: "a 50+ `lucide-vue-next` subset").
  - A parked prototype has `<Icon name="…">` resolving 27 names to lucide with `stroke-width 1.7`. It is used 13 times, in `ideas/startup-research-2026-09/first-ten/shared/Icon.vue:33-75`.
- Docs disagree about the registry. `vector-registry.md` still describes the vector as "`<Icon>` registry (lucide)", but the code takes a component, and the convention forbids "a name the seam resolves from a registry". — `workbench/wow-two-sdk-beta/wow-two-sdk-beta.fe/engineering/architecture/vector-registry.md:60`; `CONV/domains/icons/icons.md:17`

### Inferences
- In practice the "icon system" is direct lucide imports with no SDK layer: 92% of consumer glyph renders bypass `Icon` (859 of 935). The SDK wrapper is mainly an internal tool.
- Swapping the set (or adding a harness) is a component-level change, because the seam is a component (`IconAdapter`). Any replacement must be importable per glyph as a Vue component that accepts a numeric `size` and SVG attributes.

### Gaps
- Bundle weight of lucide per app was not measured: no build was run. The SDK backlog notes shared chunks of 385 kB in ForeverPin and Haven but does not attribute them to icons (`workbench/wow-two-sdk-beta/wow-two-sdk-beta.fe/engineering/planning/backlog.md:102`).
- The release date of `0.460.0` was not checked (no network). How far it lags behind current lucide is unknown.

---

## 2. Usage census — distinct icons, top 30 by apps, and how icons enter SDK components

### Takeaway
Across 31 lucide-importing roots in 25 repos, consumers use **304 distinct lucide glyphs** and the SDK uses **104**, for a union of **343** (about 22% of the 1,540 available). The distribution has a long tail: 189 glyphs appear in only one root. Icons enter SDK components through **slots**, mostly `#leading`, `#trailing` and `#icon` (245 slot sites). SDK icon props are a mix of four types: component, string (rendered as text), `VNodeChild` and `unknown`.

### Cited Findings
- Lucide is imported by 31 of the 41 consumer roots and 25 of the 31 repos. It has 1,085 import specifiers across consumers. — census (`census.json`)
- Distinct glyphs: 304 in consumers, 104 in the SDK `src`; the union is 343. 239 glyphs are used only by consumers. 189 consumer glyphs appear in exactly one root. — census plus SDK scan
- Distinct glyphs per root, highest first: Wheelhouse 112 · PRISM 63 · Haven/web 51 · ListingShelf 48 · Transcript Forge 47 · Museums 36 · ForeverPin 36 · TNIS/studio 33 · SurfacePattern 28 · fe-sdk atlas 27 · Haven/landing 21 · Hijinx 17 · Matinee 15 · Haven/admin 13 · playground 12 · ProcedureReview 11 · FileWatch 10 · Sift 9 · RetainerBalance 9 · Haven/channels 9 · PodcastReadiness 8 · DocumentationChecker 7 · CustomerPromises 7 · VendorRenewals 7 · ConfigChecker 6 · PbnStudio 4 · EpubReview 4 · Haven/map 4 · TrainingSeats 4 · PoseCoach 2 · TNIS/showcase 1. — census
- SDK's own top glyphs by number of importing files: `ChevronRight` 16, `Check` 15, `ChevronDown` 14, `X` 14, `ChevronLeft` 9, `Minus` 7, `Plus` 7, `Calendar` 5, `Clock` 5, `Loader2` 3. — scan of `SDK/src`

Top 30 glyphs by number of consumer roots. "Roots" is out of the 31 roots that import lucide; "repos" is out of 25; "files" counts importing files; "in SDK" means the SDK also imports it.

| # | Glyph | Roots | Repos | Files | In SDK |
|---|---|---|---|---|---|
| 1 | `Check` | 23 | 20 | 50 | yes |
| 2 | `Trash2` | 17 | 16 | 30 | yes |
| 3 | `Download` | 16 | 16 | 26 | yes |
| 4 | `Plus` | 15 | 13 | 41 | yes |
| 5 | `ArrowLeft` | 13 | 12 | 22 | no |
| 6 | `X` | 12 | 10 | 38 | yes |
| 7 | `ChevronDown` | 11 | 11 | 23 | yes |
| 8 | `Moon` | 11 | 11 | 13 | yes |
| 9 | `Sun` | 11 | 11 | 13 | yes |
| 10 | `RefreshCw` | 10 | 9 | 12 | no |
| 11 | `LogOut` | 10 | 10 | 11 | yes |
| 12 | `ExternalLink` | 8 | 7 | 25 | yes |
| 13 | `ArrowRight` | 8 | 7 | 21 | no |
| 14 | `Pencil` | 8 | 8 | 18 | yes |
| 15 | `Eye` | 8 | 7 | 14 | yes |
| 16 | `Play` | 7 | 7 | 16 | yes |
| 17 | `Undo2` | 7 | 6 | 11 | no |
| 18 | `Sparkles` | 7 | 7 | 9 | no |
| 19 | `Copy` | 7 | 7 | 8 | yes |
| 20 | `MapPin` | 6 | 5 | 15 | no |
| 21 | `RotateCcw` | 6 | 6 | 11 | yes |
| 22 | `Clock` | 6 | 5 | 10 | yes |
| 23 | `EyeOff` | 5 | 5 | 11 | yes |
| 24 | `Minus` | 5 | 5 | 9 | yes |
| 25 | `Monitor` | 5 | 5 | 6 | yes |
| 26 | `Settings` | 5 | 4 | 5 | yes |
| 27 | `KeyRound` | 4 | 4 | 17 | no |
| 28 | `ChevronLeft` | 4 | 4 | 10 | yes |
| 29 | `RotateCw` | 4 | 4 | 7 | no |
| 30 | `CalendarClock` | 4 | 4 | 6 | yes |

Source for the table: census (`census.json`, `agg.json` in the session scratchpad). Tied at 4 roots just outside it: `History`, `Pause`, `Star`, `ArrowUpRight`, `Info`, `SearchX`, `Square`, `Printer`, `Search`.

How icons are passed into SDK components:

- SDK prop declarations:
  - `IconAdapter` (component): `Icon.vue:36`, `RatingPicker.vue:51`, `AppSwitcherMenu.vue:32`, and `IconPicker`'s `icons: Record<string, IconAdapter>`.
  - `string`, rendered as text: `Alert.vue:8` → rendered at `:97` as `{{ props.icon }}`; `Toast.vue:8` → `:124`; `Callout.vue:8` → `:73`; `Banner.vue:8` → `:95`; `NotificationItem.vue:7` → `:154`.
  - `string | number`: `ChoiceCard.vue:13` → rendered at `:166`.
  - `VNodeChild`: `SpeedDialGroupTrigger.vue:8,11` (`closedIcon`, `openIcon`) and `SpeedDialGroupAction.vue:15`.
  - `unknown`, "intentionally untyped": `SDK/src/foundation/commands/Command.ts:42`.
  - `Notify.ts:17` `icon?: string` is an image URL for the OS notification, not a glyph.
  - All under `SDK/src/presentation/...` unless shown otherwise; grep `readonly …icon…?:`.
- SDK icon slots declared: `icon` 18 · `trailing` 9 · `leading` 4. Two components take `*Slot: VNodeChild` prop fallbacks, e.g. `Button` `leadingSlot` and `trailingSlot`. — grep `SDK/src` slot declarations
- Consumer side:
  - 245 slot sites (`<template #leading|#trailing|#icon…>`) in 24 roots.
  - 1 `leadingSlot` prop use.
  - 76 `:icon=` bindings, all Transcript Forge's `<Icon :icon>`.
  - 146 `icon: SomeGlyph` data entries in 18 roots (nav arrays, state maps).
  - 0 string `icon="…"` props on SDK `Alert`, `Toast`, `Callout`, `Banner`, `NotificationItem` or `ChoiceCard`.
  - 0 uses of the SDK `IconAdapter` type; 8 uses of lucide's own `LucideIcon` type in 2 roots (ForeverPin `MarketingContent.ts:11,27`; ListingShelf `FlowStateLook.ts:2,6`, `RunListingLook.ts:2`).
  - Source: consumer pattern scan.
- `IconPicker` is used once, in the SDK playground (`SDK/apps/playground/src/groups/FormsGroup.vue:453`), and in no product. — consumer scan

### Inferences
- The shared core is small. About 30 glyphs appear in 4 or more apps, and roughly 25 of the top 30 are generic chrome (navigation, CRUD, theme toggle, refresh). A curated "core set" of about 60–100 glyphs would cover most cross-app use. The 189 single-app glyphs are domain-specific (e.g. `BusFront`, `DatabaseBackup`, `FlaskConical`).
- How a component accepts an icon depends on the component, not on a rule. That matters for any harness: an animated state icon has to fit a slot, an `IconAdapter` prop, a `VNodeChild` prop or a text prop, depending on the component.

### Gaps
- The census counts imports and template tags, not runtime renders (icons inside `v-for` or data maps count once).
- The SDK playground and atlas are counted as consumer roots. Excluding them changes the top-30 counts by at most 2 per glyph (not recomputed).

---

## 3. Gaps and desire paths — hand-drawn SVG, second libraries, emoji/text as icons, brand marks, requests for missing icons

### Takeaway
No second icon library has crept in. Where lucide falls short, teams hand-draw instead: 51 consumer files hold inline `<svg>` (70 elements). The repeated patterns are a product `BrandMark` in 9 apps, a 28-glyph file-kind set in the files domain, map and status micro-glyphs, and 6 parametric glyph components in the SDK. Two party-game apps use emoji and Unicode text glyphs as icons; Arcade has no lucide at all. No code comment asks for a missing icon.

### Cited Findings
- Inline `<svg>` in consumers: 51 files, 70 `<svg>` elements; 0 `h('svg')` render functions. — census (`svg_files`). Classified by reading the file headers and `<svg>` blocks:
  - **Brand marks (9 apps):** each `BrandMark.vue` is a hand-drawn product symbol on a `fill-primary` tile, sized by `size` with a default of 28. Example: `V/saas/ventures.config-checker/.../src/presentation/common/BrandMark.vue:7-14`. Inline-SVG versions exist in Matinee, PbnStudio, PodcastReadiness, ProcedureReview, PRISM, CustomerPromises, FileWatch, VendorRenewals and ConfigChecker; all 11 `BrandMark.vue` files are 14–28 lines. ListingShelf's `BrandMark` uses `<img src="/favicon.svg">` (`V/saas/ventures.listing-shelf/.../common/components/BrandMark.vue:16`). SurfacePattern's wraps lucide `Flower2` at `stroke-width 1.4` (`V/saas/ventures.surface-pattern/.../presentation/brand/BrandMark.vue:12`). Sift has a separate `SiftGlyph.vue` (a sieve drawn at `stroke-width 1.9`, `V/saas/sift/.../common/components/SiftGlyph.vue:11-23`).
  - **Domain glyph set (files):** `FileIcon.vue` draws a page in the kind's colour plus a kind glyph and an extension label (`workbench/wow-two-sdk-beta/wow-two-sdk-beta.files/engineering/codebase/files.frontend-services/packages/fe-files/src/icons/FileIcon.vue:43-60`). It draws 28 kinds as stroked 24-unit paths with hex colours that `--files-icon-{kind}` can override (`.../fe-files/src/icons/FileKindVisuals.ts:3-25`, 28 `glyph:` entries). The plan behind it says "a small set of hand-drawn kind glyphs, a generated page per extension", chosen so "no outside licence binds the published package" (`workbench/wow-two-sdk-beta/wow-two-sdk-beta.files/engineering/research/files-analysis-2026-10/t7-file-icons.md:5-6,72-74`).
  - **Map glyphs (TNIS):** `Icons.ts` bakes a bus-stop SDF from a base64 PNG alpha mask, a plus badge built as an SVG string, and a Tashkent metro «М» mark (`V/saas/ventures.tnis/.../apps/studio/src/presentation/network/map/Icons.ts:1-30`; 7 `<svg>` elements). Also a compass rose (`.../network/controls/NavControls.vue:109-117`) and a position arrow with a hex fill (`.../apps/showcase/src/presentation/mocks/screens/PositionMarker.vue:33-36`).
  - **Status micro-glyphs (Wheelhouse):** 8-px half-filled-circle and X marks drawn inline (`WH/src/presentation/deployments/components/history/DeploymentsInfo.vue:42-54`).
  - **Charts, renderers and generators (not icon substitutes):** Wheelhouse `WeeklyBars`, `TrendLine`, `ActivityGrid`, `ServiceMap`; Museums `BusynessChartRenderer`, `ColumnChartRenderer`, `QrCodeRenderer`, carousel and cover; ListingShelf `PriceHistoryChart`, `GraphCanvas`; PRISM `PlanRulers`, `PlanCanvas`, `AssetModeler`; ForeverPin `StaticQrPreview`, `PrintSizing.ts`; PbnStudio `Svg.ts`; SurfacePattern `PatternEngine.ts` and `scripts/render-brand-assets.mjs`; Hijinx `PickerWheel`, `TimerRing`. Plus tests and fixtures in 6 roots and 3 SDK playground examples.
- Inline `<svg>` in the SDK: 16 `.vue` files. Six are parametric glyph components: `DotsGlyph`, `VerticalBarsGlyph`, `HorizontalBarsGlyph`, `CellsGlyph` (`SDK/src/presentation/display/moduleGlyphs/`, split from one React `ModuleGlyphs.tsx`, `ModuleGlyphs.ts:6-11`), `RadiusGlyph` (props for inner radius fraction, track stroke width and opacity, `radiusGlyph/RadiusGlyph.vue:2-16`) and `FrameGlyph` (corner radius, pupil roundness, dot-only mode, `frameGlyph/FrameGlyph.vue:2-13`). The rest are drawing or visual components: `OverlayArrow`, `SignatureInput`, `NodeEditor`, `KnobInput`, `LiveCursorIndicator`, `ProgressCircleIndicator`, `Sparkline`, `ConfettiOverlay`, `AudioWaveformPreview`, `GanttTimeline`. — grep `<svg` in `SDK/src`
- The 6 SDK glyph components have 0 consumer uses. — grep across consumers for `<DotsGlyph|CellsGlyph|…|FrameGlyph`
- Emoji and text as icons:
  - **Arcade** (no lucide dependency) has 24 `.vue` lines with emoji or symbols as UI marks. Examples: a `✕` close glyph (`V/consumer/ventures.arcade/.../shell/components/PlayerSeating.vue:30`, `gifCourt/pages/GifCourtPage.vue:49`), `←` and `→` arrows (`mazeHunt/pages/MazeHuntPage.vue:145,154`), `✓` and `✗` (`whodunit/pages/WhodunitPage.vue:86,88`), `🌐` in the language switcher (`shell/components/LanguageSwitcher.vue:18`), `🤖` (`MachineBadge.vue:19`), `⚖️` with `role="img"` (`gifCourt/components/CourtScoreboard.vue:21`) and `🏆` (`hotTake/pages/HotTakePage.vue:126`). Another 265 `.ts` lines with emoji are mostly game content, e.g. 79 `emoji:` reaction cards (`domain/gifCourt/Content.ts:60-64`).
  - **Hijinx** has 26 `.vue` lines with emoji. Examples: picker modes `icon: '🎡' | '🎲' | '🪙' | '🔀' | '👥'` (`V/consumer/ventures.hijinx/.../presentation/picker/PickerPage.vue:21-25`), hero emoji (`compatibility/CompatibilityPage.vue:72`, `movie/MoviePage.vue:83`) and `🎰` inside a `Button` (`hotseat/HotSeatPage.vue:185`). It also has 39 `emoji:`/`icon:` emoji assignments, including the game deck (`application/deck/DeckGames.ts:26-29`).
  - Elsewhere there are only stray text glyphs: TNIS `→` (`V/saas/ventures.tnis/.../network/panels/ClosureDial.vue:35`), the SDK `NodeEditor` `←`/`→` move buttons (`SDK/src/presentation/forms/nodeEditor/NodeEditor.vue:393-394`) and a ForeverPin `✓` in status text (`.../codes/preview/SavedCodePanel.vue:46`). Other `×`/`→` hits (49 and 59 non-comment lines) are dimensions or prose, not icons.
  - Source: emoji/glyph scans.
- Brand or logo glyphs from lucide: `Github` in Wheelhouse only; `Youtube` in Sift only. Both are on lucide's brand list. — census (`names`)
- The Google sign-in button exists as an SDK component (`SDK/src/presentation/actions/googleSignInButton/`). It has no inline `<svg>` (not in the 16-file list); how it draws the G mark was not checked.
- No comments ask for missing icons. Searches for `lucide has no|lacks|not in lucide|missing icon|TODO…icon|hand-drawn|custom glyph` found none in product or SDK source. The only hits were unrelated diagram notes and the files T7 plan. `lanes/own-codebase.md:359` likewise found 1 workaround comment across 35 apps, and it is not about icons. — grep across consumers and the SDK
- An SDK backlog row reads "Replace `lucide-vue-next` | engineering | Haven; the package depends on it too", with no reason given. — `workbench/wow-two-sdk-beta/wow-two-sdk-beta.fe/engineering/planning/backlog.md:104`
- The conventions route lucide's gaps to hand-drawn components. They say "must write a custom adapter component for a brand mark or a glyph the set lacks" and "must not paste a set's SVG into a template" (`CONV/domains/icons/lucide/lucide.md:14-16`), and list "a custom component … a brand mark, or a glyph the set lacks" as a provider (`CONV/domains/icons/icons.md:28`).

### Inferences
- The desire paths point to three needs lucide does not cover:
  1. Product brand marks: 11 apps each built their own `BrandMark`.
  2. Domain glyph families with colour and labels: file kinds, transit map marks.
  3. Parametric or stateful glyphs: the SDK module, radius and frame glyphs; Wheelhouse micro status glyphs.
- In each case the team wrote one-off SVG components with their own stroke weights (1.2–1.9) and sizes. That is an argument for a shared glyph-authoring harness (grid, stroke, size and export rules) more than for a bigger bought or scraped catalogue.
- The emoji usage in Arcade and Hijinx is partly intended (party-game tone, content) and partly missing UI icons: close, back/forward, check and language marks have direct lucide equivalents.

### Gaps
- Arcade's choice to skip lucide is not documented anywhere I found.
- Whether Haven's "Replace `lucide-vue-next`" row is about bundle size, style or coverage is not recorded (Haven `.md` files mention lucide only as "minimal deps", `V/saas/10x-ven-haven/engineering/research/crm/crm-deep-analysis.md:88`).

---

## 4. State and animation today — loading/success/error, spinners, icon transitions, reduced motion

### Takeaway
Loading has one standard: `Button` `isLoading` swaps the leading icon for a spinner and keeps the label. It is used 168 times in 26 roots. Success and error states are not part of the button, the only built-in success/failure swap is `CopyButton`'s instant `Copy → Check → X`, and apps build their own state→icon maps. The SDK has no animated or morphing icons (no `pathLength` draws, no `<Transition>` around glyphs). The only icon motion is spinning (`animate-spin`) and rotation transitions, and reduced motion is covered by a library-wide CSS safety net plus per-component `motion-reduce:` classes.

### Cited Findings
- `Button` `isLoading` (`SDK/src/presentation/actions/button/Button.vue`):
  - The prop reads "a spinner replaces the leading icon, the label stays, it dims and blocks clicks" (`:57-58`).
  - `loadingText` replaces the label (`:60-61`), and a `loading` slot or `loadingSlot` replaces the spinner (`:54-55,201-202`).
  - With a leading icon the spinner takes its place (`:516-523`). Without one, the label turns transparent so the width and accessible name stay, and the spinner centres over it (`:527-541`).
  - Loading sets `aria-busy` (`:485`).
  - `ButtonDataState` has only `loading`, `skeleton` and `disabled` — no success or error state (`:148-152`).
- `CopyButton` picks its fallback icon with `copied ? Check : error ? X : Copy` and renders it at `size 16` (`SDK/src/presentation/actions/copyButton/CopyButton.vue:85,109`). It resets after `resetAfter`, default 2000 ms (`:22`), exposes `{ copied, error }` to a slot (`:61-62`) and has no transition between glyphs. Consumers use it 18 times in 8 roots. — consumer scan
- There are two spinners:
  - `foundation/icons` `Spinner` is lucide `Loader2` with `animate-spin motion-reduce:animate-none size-[1em]` (`SDK/src/foundation/icons/spinner/Spinner.vue:33-36`). `Button` uses this one (`Button.vue:139,520`).
  - `presentation/feedback` `Spinner` is a CSS border ring with `role="status"` and a visually hidden label (`SDK/src/presentation/feedback/spinner/Spinner.vue:53-56`; `Spinner.variants.ts:18` has `animate-spin` without a `motion-reduce:` class).
  - `InlineSpinner` pairs the ring with "Loading…" text (`SDK/src/presentation/feedback/inlineSpinner/InlineSpinner.vue:50-53`).
- Other SDK icon motion: the `SelectPicker` chevron uses `transition-transform` + `rotate-180` when open (`SDK/src/presentation/forms/selectPicker/SelectPickerTrigger.vue:171-173`) and its loading spinner uses `animate-spin` without `motion-reduce:` (`:175`; `SelectPickerContent.vue:188`). The `ToastHost` countdown ring uses `stroke-dasharray` (`SDK/src/presentation/feedback/toastHost/ToastHost.vue:370-385`). `ProgressCircleIndicator` animates `stroke-dashoffset 300ms ease` (`SDK/src/presentation/feedback/progressCircleIndicator/ProgressCircleIndicator.vue:98-101`).
- The SDK has no glyph-level animation primitives: 0 `pathLength`/`path-length`/draw/morph hits, and 0 `<Transition>` tags in `SDK/src` `.vue`. Its `@keyframes` cover fades, pops, slides, shimmer, skeleton and marquee (`SDK/src/index.css:560-742`), and none target icons. — grep `SDK/src`
- Reduced motion:
  - A library-wide rule under `@media (prefers-reduced-motion: reduce)` forces `animation-duration: 0.01ms`, `iteration-count: 1` and `transition-duration: 0.01ms` on every element. Its comment says the safety net exists "so an un-tagged animation can't slip through" (`SDK/src/index.css:753-765`).
  - On top of that, `SDK/src` has 139 `motion-reduce|motion-safe|prefers-reduced-motion` hits across 48 files, plus a `useReducedMotion()` hook (`SDK/src/foundation/device/hooks/UseReducedMotion.ts:11`).
- Consumers:
  - `Button` with `isLoading`: 168 uses in 26 roots; `loadingText` 8 uses in 3 roots.
  - SDK `<Spinner>`: 10 uses in 3 roots; `<InlineSpinner>`: 6 uses in 5 roots.
  - `Loader`/`Loader2`/`LoaderCircle` imported directly: 3 roots. `animate-spin`: 10 uses in 3 roots, all in Wheelhouse. `animate-pulse`: 15 uses in 6 roots.
  - `prefers-reduced-motion`: 24 uses in 11 roots; `motion-reduce:`: 19 uses in 4 roots; `useReducedMotion`: 2 uses in 1 root (Museums `MuseumMapViewer.vue:16,36`).
  - Source: consumer state scan.
- App-built state→icon maps:
  - Wheelhouse `StatusIcons` has 10 states, and `deploying` maps to `LoaderCircle` (`WH/src/presentation/common/components/StatusStyles.ts:39-50`). `DeployStateIcons` maps `in_progress` to `LoaderCircle` and `rolled_back` to `Undo2` (`:56-60`). There are 5 `Record<…, Component>` icon maps in 2 files, the other being `deployments/components/StepKindIcons.ts:27`.
  - Wheelhouse has a hand-tuned "slow spin" `animate-spin [animation-duration:2s] motion-reduce:animate-none` (`StatusStyles.ts:136-141`), repeated inline in `DeploymentStateChip.vue:56`.
  - ListingShelf `FlowStateLook` pairs `Pending → CircleDashed`, `Active → Loader` and `Done → Check` with card, badge and screen-reader word (`V/saas/ventures.listing-shelf/.../presentation/pipelines/FlowStateLook.ts:13-30`).
- Conventions:
  - "must show a running refresh on its control through `Button` `isLoading`: the icon turns into a spinner, the label stays and the control dims" (`CONV/domains/data/state-and-data.md:69-70`).
  - "must honor `prefers-reduced-motion` for placeholder animation and result transitions" (`:66`).
  - `icons.md` lists "the spinner" as its own provider ("a busy indicator, which is not an app-chosen icon", `CONV/domains/icons/icons.md:29`).

### Inferences
- Loading is solved and widely adopted. Success and failure feedback after an action is not: the button has no `success`/`error` state, and swaps happen instantly or in app code. An "animated state icon" (spinner → check / cross morph, or a drawn check) has a clear slot: `Button`'s `loading` slot and `CopyButton`'s fallback glyph. The global reduced-motion net would already cap any CSS-driven icon animation.
- Status icon maps are being rebuilt per app: Wheelhouse, ListingShelf, and the SDK's own `SeverityIcons`. Shared "state glyph" vocabularies (pending, running, done, failed, rolled back, degraded) are a candidate SDK export.

### Gaps
- Whether `SelectPicker`'s untagged `animate-spin` stops visibly under reduced motion was not checked in a browser. The CSS safety net should limit it to one 0.01 ms iteration, but that is unverified.
- Toasts and notifications state handling is covered in `lanes/notifications.md` and not repeated here.

---

## 5. Sizing and style conventions — stroke, sizes, colour tokens, icon design rules

### Takeaway
The conventions set one set (lucide), a numeric size scale of 12/14/16/20/24+, lucide's default stroke, `currentColor` with text-token tones, and `SeverityIcons` for severity. The code mostly keeps the stroke and colour rules, but about 30% of size values are off the scale (15, 18 and 13 are common). Two rules have no adoption at all: `SeverityIcons` is never used in consumers, and labelled `<Icon aria-label>` never appears.

### Cited Findings
- The conventions on icons:
  - `repo-conventions.md` § Frontend standard: "must use `lucide-vue-next` as the icon set" (`conventions/development/repo/repo-conventions.md:72`).
  - `lucide.md` selection rules: only set; declare the SDK's range; no second set, icon font or sprite; no pasted SVG; custom adapter for brand marks and missing glyphs (`CONV/domains/icons/lucide/lucide.md:11-16`).
  - Import rules: by name; never a whole-set import or a name string; pass to an SDK icon prop or slot; meaningful glyphs through `Icon` with an `aria-label` (`:22-26`).
  - Size scale: `12` dense metadata, `14` inside a control, `16` beside body text, `20` standalone (the `Icon` default), `24`+ state or hero marks; off-scale sizes "need a reason" (`:32-40`).
  - "must keep the set's default stroke width" (`:42`).
  - "must let a glyph inherit `currentColor`; a tone comes from a text token class, never a hex value" (`:43`).
  - "must take a severity glyph from the SDK's `SeverityIcons`" (`:44`).
  - The icon contract (`CONV/domains/icons/icons.md:11-19`): numeric adapter size, CSS sizes on the class, decorative by default, `img` role only when labelled, component never name, set chosen by the app.
- Product identity icons are a separate system: brand files under `product/brand/icons/` in `{form}-{color}-{theme}.{svg|png}`, `svg` preferred, at most 256 KiB, with a 6-step fallback ending in a monogram. — `conventions/design/identity/product-icons.md:20-102`. Neither `conventions/design/design-conventions.md` nor `conventions/design/` names a UI-icon drawing grid, stroke or style rule. — file list of `conventions/design/` (9 files) and grep
- SDK defaults: `Icon` size 20 (`SDK/src/foundation/icons/icon/Icon.vue:61`). `IconPicker` glyph size 20 with a 36-px button (`IconPicker.spec.md` props table; `CONV/components/forms/iconPicker.md` § Values). `SeverityIconClasses` map severities to `-soft-foreground` text tokens (`SDK/src/foundation/icons/SeverityIcons.ts:18-24`).
- Sizes in use:
  - The SDK passes `size` 14 ×40, 16 ×20, 12 ×8, 18 ×4, 28/20/15 ×2 each, 11/13 ×1. Class sizes: `h-4 w-4` ×17, `size-4` ×7, `h-3.5 w-3.5` ×5.
  - Consumers pass `size` 14 ×265, 16 ×199, 15 ×123, 12 ×54, 18 ×44, 13 ×32, 22 ×20, 24 ×15, 20 ×14, 17 ×9, 11 ×5, 10 ×5. Class sizes: `size-4` ×65, `size-3.5` ×42, `size-5` ×9, `size-3` ×8.
  - Off-scale values (15, 18, 13, 22, 17, 11, 10) are 238 of 785 `size` values, about 30%.
  - Source: attribute scan of lucide and `Icon` tags.
- Stroke: lucide's default (2) is overridden on lucide tags only 5 times — TNIS `MapControls.vue:210,234,250` (1.75), `PlaceCursor.vue:208` (2) and the SurfacePattern `BrandMark.vue:12` (1.4) — plus `1.7` in the parked prototype `Icon.vue`. Hand-drawn SVGs pick their own: Sift 1.9, FileIcon 1.25, Wheelhouse micro-glyphs 1.2 and 1.6, and the SDK `RadiusGlyph` exposes the stroke as a prop. — attribute scan; files cited in §3
- Colour classes on glyphs:
  - Consumers: `text-muted-foreground` ×43, `text-primary` ×20, `text-success` ×12, `text-warning` ×8, `text-destructive` ×8. Raw palette classes are rare: `text-sky-600` ×2, `text-success-600` ×1.
  - SDK: `text-muted-foreground` ×14.
  - Hex colours appear only in hand-drawn work: FileKindVisuals (overridable through a CSS var) and the TNIS showcase mocks.
  - Source: attribute scan.
- Severity-glyph drift: consumers use `SeverityIcons` 0 times. Instead they import severity-like glyphs directly — `Info` 4 roots, `TriangleAlert` 3, `AlertTriangle` 2, `CheckCircle2` 2, `ShieldAlert` 2, `CircleCheck` 1, `CircleX` 1, `CircleAlert` 1. — consumer scan
- Labelled icons: 0 `<Icon … aria-label>` in consumers, against `lucide.md:25`. — consumer scan
- Lucide deprecated aliases in use. Checked against `SDK/node_modules/lucide-vue-next/dist/esm/lucide-vue-next.js`, these resolve to other files:

  | Alias in use | Resolves to | Where |
  |---|---|---|
  | `AlertTriangle` | `triangle-alert` | 2 consumer roots, SDK |
  | `CheckCircle2` | `circle-check` | 2 roots |
  | `Home` | `house` | 2 roots, SDK `IconPicker` |
  | `Loader2` | `loader-circle` | 1 root, SDK `Spinner` |
  | `Edit` | `square-pen` | SDK `IconPicker` |
  | `UploadCloud` | `cloud-upload` | SDK |
  | `MoreHorizontal` | `ellipsis` | 1 root |

  The same meaning is also spread over several glyphs: refresh-like `RefreshCw` 10 / `RotateCcw` 6 / `Undo2` 7 / `RotateCw` 4 roots; back `ArrowLeft` 13 vs `ChevronLeft` 4; loading `Loader` / `Loader2` / `LoaderCircle`.

### Inferences
- The rules that hold (one set, default stroke, token colours) are the ones lucide or Tailwind enforce on their own. The rules that need a choice at each call site (size scale, `SeverityIcons`, labelled `Icon`, one glyph per meaning) drift. A harness or a curated SDK set that bakes in size and meaning (e.g. semantic names like `refresh`, `back` and `severity.warning` exported as components) would address the drift better than a larger catalogue.

### Gaps
- No visual audit was done. Whether the off-scale sizes are justified "in the layout", as `lucide.md:40` allows, was not judged.

---

## 6. What `icon-scraper-spec.md` planned versus what the codebase uses, and whether anything was built

### Takeaway
The scraper spec (2026-04-12) is still an `idea`. It planned a local, searchable index aggregating about 18,000 SVGs from six free sets (and possibly scraped Font Awesome Pro), with a later `WowTwo.Icons` SDK package. Nothing was built: no script, repo, package or catalog entry exists. Meanwhile the conventions locked in a single set (lucide), and the October idea review dropped the scraper (score 27, licence blocker). The only "own icon" work since is the files domain's generated file-kind glyphs.

### Cited Findings
- Scope of the spec:
  - Problem: icon libraries "charge ~$100/year", e.g. Font Awesome Pro at $99/year (`ideas/icon-scraper-spec.md:7`).
  - Research: Font Awesome's search page renders all icons, Free and Pro, as inline `<svg>` paths with "No anti-scraping protection" and "Low" difficulty (`:9-25`).
  - Legal note: Pro icons need a subscription "even for private use", yet "Enforcement for private/internal use is effectively zero" (`:27-30`).
- The spec's concept: aggregate Font Awesome Free (~2,000), Lucide (~1,500+), Heroicons (~300+), Phosphor (~7,000+), Tabler (~5,000+) and Bootstrap Icons (~2,000+), "~18,000+" in total, all free licences (`:34-45`).
  - MVP: a CLI or local web UI with fuzzy search, copying SVG / React component / CSS class, size previews and the source library shown (`:47-52`).
  - Future: a VS Code extension, cross-library suggestions, icon diff, and a "wow-two SDK integration — `WowTwo.Icons` package" (`:54-58`).
- Tech direction: Node and Playwright scraping (npm where possible), a JSON or SQLite index, a React dev server or Electron UI, periodic re-scrape (`:60-64`).
- Open questions in the spec: whether to include FA Pro; standalone tool vs SDK package; "How to handle icon style normalization across libraries (stroke width, fill vs outline)?" (`:66-69`).
- Status: "`idea` — research done, needs implementation plan" (`:71-72`).
- Assumptions to note:
  - It frames icons as a paid-catalogue problem, but the codebase already uses a free ISC set (§1).
  - Its output is copy-paste (SVG, React component, CSS class). The conventions now forbid pasting SVG into templates and forbid other sets and name-string resolution (`CONV/domains/icons/lucide/lucide.md:13-14,23`).
  - It targets React and Electron, while the frontend standard is Vue 3 (`conventions/development/repo/repo-conventions.md:69`).
  - It leaves style normalisation open, which is the very drift §5 measures.
- Nothing was built:
  - No file or folder named `*icon*` outside `src/` and brand assets, other than unrelated items: Wheelhouse brand export scripts (`workbench/wow-two-platform/wow-two-platform.wheelhouse/engineering/scripts/export-icon-set.py:1-6`, which copy approved brand PNGs into `product/brand/icons/`), `export-app-icons.py` and the files T7 research.
  - No `icon-scraper`, `icon index tool` or `WowTwo.Icons` reference in code, `catalog.yml` or `.claude/repo-registry.md`.
  - Source: `find`/`grep` across `workbench/`, `ideas/`, `scripts/`, `docs/`.
- The idea review dropped it: "O14 Icon scraper (DX tool) … Spec only … 27 … Drop", reasoned as "Free-source aggregation is a feature; Pro scraping is not viable" and "Scraping Font Awesome Pro is a licence breach; free aggregators already exist", with "Licence" as the blocker. — `ideas/own-ideas-review-2026-10/own-ideas-review-2026-10.md:111,261,478,574`
- Earlier SDK analysis lists icon delivery patterns (per-icon ESM, single component + name, sprite, icon font, inline SVG, Iconify API, CSS `mask-image`) and 13 libraries, with Lucide marked "Default for shadcn; we use" (`workbench/wow-two-sdk-beta/wow-two-sdk-beta.fe/engineering/architecture/analysis/ui-philosophy/ideas.md:2297-2325`). An SVG sprite is "MAYBE — icons via Lucide individually-imported" (`.../ui-philosophy/targets.md:245`).
- The closest built "own icon" pipeline is the files domain's planned `file-types.json` registry, with "a generated page per extension" over "about 24" (built: 28) hand-drawn kind glyphs. It treats VS Code icon themes only as coverage references, "licences and asset terms to verify" (`workbench/wow-two-sdk-beta/wow-two-sdk-beta.files/engineering/research/files-analysis-2026-10/t7-file-icons.md:15-16,72-74`; `.../fe-files/src/icons/FileKindVisuals.ts`).

### Inferences
- The spec and the codebase have diverged. The spec optimised for breadth (18k icons, copy-paste); the codebase uses 343 lucide glyphs (§2), and its real gaps are brand marks, domain families, parametric or state glyphs, and consistency (§3–§5). Breadth is not what is missing.
- If a scraped or aggregated set were revived, it would conflict with three current convention rules (single set, no pasted SVG, no name strings) and would need the stroke and fill normalisation step the spec left open. The files domain's "generate from a registry and draw our own glyphs" route is the in-house precedent for an own-harness option.

### Gaps
- No usage or licensing data for any of the six aggregated sets was gathered (out of scope: no web).
- Whether the developer still holds the spec's "$100/year" premise is unknown; the 2026-10 review suggests not.

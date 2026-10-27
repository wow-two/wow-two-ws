# Spotlight illustrations of UI components (muted context, full-color focal component)

Research date: 2026-10-27. Scope: how to generate "spotlight" cards for a Vue 3 component gallery (~35 apps on the library), kept in sync with real components, light + dark. Evidence grading: "Cited Findings" were read in a fetched page this session (unless a finding says "search snippet", meaning only a search-result summary was seen). "Inferences" are my reasoning, not sourced. Anything from memory that I could not confirm is under "Gaps".

## 1. Visual styles in the wild (muted-context / highlighted-component imagery)

### Takeaway
No design-system site I could reach (Material 3, Apple HIG, Polaris, Atlassian, Fluent 2) documents or visibly demonstrates a "dim everything but the featured component" image style in text I could read; their pages are JS-rendered SPAs or expose only alt text. The verifiable prior art for "muted context, focal element lit" is product-tour libraries (scrim with a cutout) and interactive-anatomy tooling (live DOM highlight). The style vocabulary (grayscale / opacity / wireframe / blur / scrim) is therefore a design choice for us, not an established convention to copy.

### Cited Findings
- Driver.js (tour library) implements spotlight as a backdrop with a cutout: `overlayColor` (default black), `overlayOpacity` (default 0.5), `stagePadding` ("Distance between the highlighted element and the cutout", default 10), `stageRadius` ("Radius of the cutout around the highlighted element", default 5), and `disableActiveInteraction` (default false). Docs note overlay color helps "when the page has a dark background and you want to highlight light elements". — [Driver.js configuration](https://driverjs.com/docs/configuration)
- Intro.js (tour library): `overlayOpacity` default 0.5; `disableInteraction` ("To disable interactions with elements inside the highlighted box"); `highlightClass` is "added to the helperLayer"; `helperElementPadding` default 10. — [Intro.js options](https://introjs.com/docs/intro/options)
- Intro.js 7.2.0 minified CSS (per the fetch summary, not independently re-read): `.introjs-overlay` z-index 999999, `.introjs-helperLayer` z-index 9999998, `.introjs-showElement` z-index `9999999!important`. I.e. the tour lifts the target above the scrim by z-index, not by cloning it. — [introjs.min.css 7.2.0](https://unpkg.com/intro.js@7.2.0/minified/introjs.min.css)
- Generic CSS spotlight recipes: (a) a `box-shadow` with a huge spread gives a viewport-covering shade with a shape-accurate cutout, but no light-emitting glow on its own; (b) a full-viewport shade with a hole punched by `clip-path` polygon (SVG or `clip-path: path()` for complex shapes); (c) a `clip-path` circle driven by CSS custom properties. — [DEV: nicm42](https://dev.to/nicm42/spotlight-on-hidden-background), [GeeksforGeeks](https://www.geeksforgeeks.org/?p=557255) (search snippets), [Codrops 2021](https://tympanus.net/codrops/2021/05/04/dynamic-css-masks-with-custom-properties-and-gsap/)
- `component-anatomy` (open source, small: 77 commits, 25 stars) argues docs anatomy is usually "static annotated images exported from Figma" that "go stale", and instead turns `data-part` attributes on the live DOM into a synchronized panel with hover highlighting; ships presets `default`, `minimal`, `contrast`, `blueprint` and `--ca-*` CSS variables. — [component-anatomy](https://github.com/julien-deramond/component-anatomy)
- A Medium article on design-system concept illustrations recommends minimal, geometric, text-free wireframes to focus attention on specific UI elements (e.g. a header diagram instead of a full Figma screenshot). Single-author article, not an authoritative standard. — [Medium: emmchier](https://medium.com/@emmchier/concept-illustrations-for-design-systems-answering-key-questions-69138f0d3644) (search snippet)
- IBM Carbon component pages use labeled anatomy diagrams per subpart (label, icon slot, container, focus ring), per a secondary blog. — [Magic Patterns](https://www.magicpatterns.com/blog/design-system-documentation) (search snippet)
- Fluent 2 Button usage page: illustrations are named by type ("Button", "Split Button", "Menu Button", "Compound Button", "Toggle Button") plus do/don't pairs; the text reveals nothing about dimming or outline treatment. — [Fluent 2 Button usage](https://fluent2.microsoft.design/components/web/react/core/button/usage)
- Atlassian Button usage: illustrations are mostly small do/don't mock-ups with sentence-length alt text ("Two buttons in a group. One says cancel and is grey, the other says primary and is blue..."); visible alt text never mentions dimmed surroundings (page was truncated at ~100k chars). — [Atlassian Button usage](https://atlassian.design/components/button/usage)
- Material 3 overview on developer.android.com (updated 2023-12-20) shows six category figures captioned only "Figure 1: Action Components" ... "Figure 6: Text Input" with empty `alt`; page text does not say whether components are isolated or in context. — [Android Developers: Material Components](https://developer.android.com/design/ui/mobile/guides/components/material-overview)
- `m3.material.io/components/buttons/overview`, Apple HIG `buttons` and Polaris `button` returned only a title (SPA) or a redirect (Polaris moved to shopify.dev/docs/api/polaris); no content could be read. — fetch attempts this session

### Inferences
- Style taxonomy for our own decision (focal mark in parentheses):
  - Grayscale (`filter: grayscale(1)`): keeps layout fidelity; focal = only colored thing, so no extra mark is needed; breaks if the library is mostly neutral already.
  - Reduced opacity: cheap, but alpha-blends against the page background, so dark/light behave differently and overlapping elements show through; opacity on a container also dims the focal child inside it (see section 2).
  - Wireframe/outline (token swap: transparent fills, 1px border, text as bars): most "designed" look, hides sample copy that distracts; needs a render mode, not a filter.
  - Blur (`filter: blur`): expensive on 50-100 cards if live; reads as "depth of field", can imply a modal; poor for accessibility of dimmed text.
  - Scrim (tour-style overlay with cutout): trivially achieved with `box-shadow` spread or `clip-path`; focal gets an optional ring/glow; scrim color must differ by theme (Driver.js doc hints at this for dark backgrounds).
  - Focal marking options: untouched full color (primary), 1-2px accent ring/offset outline, soft glow, or a small label chip; ring + full color is the lowest-noise combination.
- The live-DOM approach (component-anatomy) and a spotlight card are the same idea: image == the real component with CSS state applied. That supports generating cards from a live "stage" page instead of drawing them.

### Gaps
- Could not verify how Material 3, Apple HIG, Polaris, Atlassian or Fluent 2 style their "component in context" images (SPAs returned no readable alt text or image descriptions). From background recollection (unverified, do not cite): M3/HIG component pages mostly show the component isolated on a plain surface with callout numbers, and HIG often shows full-screen context with the focal control in color. Needs a visual pass in a real browser (e.g. view the pages and screenshot) to be reliable.
- Figma Community "component in context" documentation kits: no source found.
- Intro.js/Shepherd exact scrim implementation (box-shadow vs SVG path): Shepherd source URL guessed wrong (404); Intro.js CSS summary showed no box-shadow declaration in the minified file (possibly set inline by JS). Not confirmed.

## 2. Live rendering approaches (CSS spotlight mode on a real layout)

### Takeaway
The robust live technique is a token swap (neutralize color/border/shadow custom properties on non-target components, restore them on the target), not `filter`/`opacity` on containers: a filter or opacity on any ancestor of the target cannot be undone by the target and also becomes a stacking context and a containing block for `position: fixed`. Teleported overlays (Vue `<Teleport>`, `showModal()` dialogs, popovers) live outside the layout subtree, so subtree-scoped selectors and ancestor filters do not reach them.

### Cited Findings
- Stacking contexts: elements with `opacity < 1`, and any of `transform`, `filter`, `backdrop-filter`, `clip-path`, `mask`/`mask-image`/`mask-border` other than `none`, `isolation: isolate`, `will-change` of such a property, or `contain: layout|paint|strict|content` create a stacking context. — [MDN: Stacking context](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_positioned_layout/Understanding_z-index/Stacking_context)
- Vue docs: `position: fixed` "is relative to the viewport only when no ancestor has a `transform`, `perspective`, or `filter` property set", and a child's `z-index` "is constrained by its containing elements". — [Vue: Teleport](https://vuejs.org/guide/built-ins/teleport.html)
- `<Teleport>` "only alters the rendered DOM structure"; the component stays a logical child, props/events/inject work, but the DOM node lands at the `to` target (e.g. `body`). — [Vue: Teleport](https://vuejs.org/guide/built-ins/teleport.html)
- `filter` is "Inherited: no" and functions apply "in order declared". The page text read did not state the stacking/containing-block rules (it was truncated at 100k chars; the final 46k not read). — [MDN: filter](https://developer.mozilla.org/en-US/docs/Web/CSS/filter)
- `inert`: the element and its flat-tree descendants get no click or focus events, are not find-in-page searchable, text can't be selected or edited, and are excluded from the accessibility tree and tab order. "By default, there is no visual way to tell whether or not an element or its subtree is inert", so authors must style it. Baseline widely available, "available across browsers since April 2023". — [MDN: inert](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Global_attributes/inert)
- Modal `<dialog>` opened with `showModal()` "escape inertness": it does not inherit `inert` from ancestors; "No other element can escape inertness." — [MDN: inert](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Global_attributes/inert)
- Top layer: elements shown via `showModal()`, `showPopover()`, fullscreen, and open customizable `<select>` pickers sit in a viewport-wide layer above all other content and "generate a new stacking context". The page does not say how ancestor `filter`/`opacity` affects them. — [MDN: Top layer](https://developer.mozilla.org/en-US/docs/Glossary/Top_layer)
- `:has()`: Baseline "available across browsers since December 2023". Performance warning: complex or broadly anchored selectors (`body`, `:root`, `*`) are re-evaluated on DOM mutations and "can significantly impact page performance". Not nestable; no pseudo-elements inside. Example `section:has(.featured)`. — [MDN: :has()](https://developer.mozilla.org/en-US/docs/Web/CSS/:has)
- Tour libraries lift the target above the scrim by `z-index` (`.introjs-showElement` `z-index: 9999999 !important`), which only works when no ancestor stacking context traps the target; they offer `disableInteraction` / `disableActiveInteraction` to block clicks on the target. — [Intro.js CSS](https://unpkg.com/intro.js@7.2.0/minified/introjs.min.css), [Intro.js options](https://introjs.com/docs/intro/options), [Driver.js configuration](https://driverjs.com/docs/configuration)
- Playwright's `stylePath` option "applied during capture" lets a stylesheet be injected at screenshot time (so spotlight CSS can live in the capture tooling rather than the component library). — [Playwright LocatorAssertions](https://playwright.dev/docs/api/class-locatorassertions)

### Inferences
- What breaks with `filter`/`opacity` spotlight on a layout root or any ancestor of the target: (1) the target is filtered/dimmed too, because a child cannot opt out of its ancestor's compositing (standard CSS behavior; I did not re-verify on MDN this session); (2) `position: fixed` descendants (sticky headers, drawers) re-anchor to the filtered ancestor, per the Vue docs quote; (3) the ancestor becomes a stacking context, so `z-index` on the target no longer wins over siblings outside it (the tour-library z-index trick fails). So apply dimming only to leaves and to ancestor-owned paint (background/border), never as compositing on a container.
- Teleported overlays (modals, dropdown menus, tooltips, toasts) leave the layout subtree: a selector like `[data-spotlight] .ui:not(...)` or a filter on the stage will not reach them. Options: (a) put the spotlight attribute/class on the Teleport target (`body` or `html`, where `data-theme` usually lives) so tokens cascade into portals; (b) render demo overlays `disabled`/inline in the stage; (c) if the featured component IS an overlay, use a stage-owned container as the Teleport `to` target and spotlight that.
- `inert` is the right tool for the interactive version of a card (context not focusable or announced) but gives no visual mute; combine with the visual mode. Do not put `inert` on the featured component.
- Token-swap design (untested sketch). Components read an indirection layer so a spotlight variable can override the theme value; the target resets it with `initial` (guaranteed-invalid), which makes the `var()` fallback apply:
  ```css
  /* component layer: --c-bg: var(--spot-bg, var(--bg)); same for --c-fg, --c-border, --c-accent, --c-shadow */
  [data-spotlight] .ui:not([data-spot-target]) { --spot-bg: var(--spot-surface); --spot-fg: var(--spot-ink-low); --spot-border: var(--spot-line); --spot-accent: var(--spot-line); --spot-shadow: none; }
  [data-spotlight] [data-spot-target] { --spot-bg: initial; --spot-fg: initial; --spot-border: initial; --spot-accent: initial; --spot-shadow: initial; }
  ```
  Because only custom properties change, no stacking context, filter, or containing-block side effects occur; light/dark come free (`--spot-*` defined per theme). Cost: the library must already consume semantic tokens through one alias layer; if it does, the change is a theme-file edit, not a per-component edit. Wireframe mode is the same mechanism with transparent fills and text rendered as bars (`color: transparent` + background gradient).
- `:has()` is only needed for the ancestor case, e.g. to avoid muting the chrome of a card that contains the target (`.card:has([data-spot-target])`). Keep anchors narrow (inside the stage, not `body`) given MDN's performance warning.
- Pointer-events: set `pointer-events: none` on the stage in static cards; use `inert` on non-target regions for interactive cards.

### Gaps
- Ancestor `filter` effect on top-layer elements (dialog/popover): not documented in what I read; test in Chromium/WebKit/Firefox.
- MDN filter page section on containing blocks and performance (characters 100,000+) not read.
- No engineering write-up found of a "spotlight mode" implemented in CSS for a design system gallery; everything above is composed from primitives.

## 3. Static generation (Playwright/Puppeteer in CI, formats, visual-regression tools)

### Takeaway
Playwright locator screenshots under two `colorScheme` projects produce deterministic element-clipped images; the main operational risk is cross-OS rendering drift, solved by generating in one pinned container. The visual-regression products (Chromatic, Argos) keep images in their own review UIs with no documented public URL, and Lost Pixel is archived (2026-04-22), so for gallery assets a self-owned Playwright (or Vitest browser mode) script is the lowest-dependency path.

### Cited Findings
- `toHaveScreenshot` baseline file names include browser/project and platform (e.g. `example-test-1-chromium-darwin.png`), stored in `<test-file>-snapshots`; PNG default, `.webp` extension stores lossless WebP; `--update-snapshots` regenerates; docs warn rendering varies by "host OS, version, settings, hardware, power source, headless mode" and advise running "in the same environment where the baseline screenshots were generated". — [Playwright: visual comparisons](https://playwright.dev/docs/test-snapshots)
- `expect(locator).toHaveScreenshot` options and defaults: `animations` `"disabled"` ("stops CSS animations, CSS transitions and Web Animations"), `caret` `"hide"`, `scale` `"css"`, `threshold` 0.2, `maskColor` `#FF00FF`, `omitBackground` false, plus `mask`, `stylePath`, `maxDiffPixels`, `maxDiffPixelRatio`. — [Playwright LocatorAssertions](https://playwright.dev/docs/api/class-locatorassertions)
- Light/dark with Playwright: define two projects with different `colorScheme` values; Argos prefixes screenshot names by project (`light/homepage`, `dark/homepage`). — [Argos: Playwright](https://argos-ci.com/docs/playwright); same pattern in [DEV: duncanma](https://dev.to/duncanma/visual-regression-testing-using-playwright-and-github-actions-4lpb) (search snippet)
- Argos `argosScreenshot(page, name, options)` supports an `element` target, default `stabilize: true` (fonts, images, carets, scrollbars, sticky elements, background images), disables hover effects, pauses infinite SVG animations/GIFs on first frame; stores to `./argos` and uploads; docs describe no API or direct URL to retrieve images; 50 MB per snapshot. — [Argos: Playwright](https://argos-ci.com/docs/playwright)
- Vitest browser mode `toMatchScreenshot` (docs page shows v5.0.5): element-level, Playwright provider documented, references in `__screenshots__` next to tests named by test + browser + platform, "stable screenshot detection" retries until two captures match, recommends Docker, a separate `vrt` project with fixed viewport, generating references in CI via a manual workflow, Git LFS for large suites, and guarding `--update` behind a CI check. No Vue-specific text. — [Vitest: Visual Regression Testing](https://vitest.dev/guide/browser/visual-regression-testing)
- Chromatic "modes": one snapshot per applied mode (theme, viewport, locale); each mode has its own baseline and approval; modes require Storybook 6+. Snapshots are images captured in Chromatic's cloud and cropped to the component bounding box (search snippet); docs read do not say whether images can be exported. — [Chromatic: Modes](https://www.chromatic.com/docs/modes/), [Chromatic: Snapshots](https://www.chromatic.com/docs/snapshots/)
- Lost Pixel: repository "archived by the owner on Apr 22, 2026", banner "Lost Pixel is joining Figma" and "We are sunsetting the product". Supported Storybook, Ladle, Histoire, pages, custom shots. — [lost-pixel/lost-pixel](https://github.com/lost-pixel/lost-pixel). Argos's blog (competitor, vendor content) says Argos is the closest replacement and removes committing baselines to Git; one source says Argos self-hosting is not supported or documented. — [Argos: Lost Pixel alternatives](https://argos-ci.com/blog/lost-pixel-alternatives) (search snippet)
- Vue-relevant story tooling: Histoire has an official `@histoire/plugin-screenshot` that generates screenshots in the build to `.histoire/screenshots` (secondary Japanese slides and a plugin guide only). — [Speaker Deck: oekazuma](https://speakerdeck.com/oekazuma/histoirewoshi-tutesveltekonponentowoguan-li-siyou), [bytenote](https://bytenote.net/article/histoire-plugin-development). A migration comparison notes Argos, Chromatic, Percy and Happo lists do not name Ladle or Histoire. — [Argos: Lost Pixel alternatives](https://argos-ci.com/blog/lost-pixel-alternatives)
- Storybook screenshot tooling: `storycap` (Puppeteer) and `storycap-testrun`; `StoryFreeze`, a Playwright-based independent fork for Storybook 10. — [Storybook addons: screenshot](https://storybook.js.org/addons/tag/screenshot), [StoryFreeze](https://storybook.js.org/addons/storyfreeze)
- Real example of docs images generated from stories: the `coder/mux` repo's README images (`docs/img/*.webp`) are "deterministically generated from Storybook stories", not hand-captured. — [skills.cat: generate-readme-screenshots](https://skills.cat/skills/coder/mux/generate-readme-screenshots) (search snippet)
- `shot-scraper` (Simon Willison, 2022-03) is a Playwright-based tool for automated documentation screenshots. Pre-2023, included for method only. — [Simon Willison](https://simonwillison.net/2022/Mar/10/shot-scraper/)
- Practitioner advice (single-author blog, low authority): CI is good for generating but risky for publishing screenshots blindly; keep a manifest per screenshot and send changed images to human review. — [DEV: jakexkim](https://dev.to/jakexkim/ci-can-take-screenshots-it-should-not-publish-them-blindly-51bb), [DEV: jakexkim 2](https://dev.to/jakexkim/playwright-screenshots-for-documentation-what-to-automate-and-what-to-review-3h44)
- Image formats: for screenshots, diagrams and line art MDN says prefer lossless; WebP lossless is typically ~26% smaller than PNG; AVIF lossy ~50% smaller than JPEG and supports alpha but not progressive rendering; AVIF support: Chrome 85, Edge 121, Firefox 93, Safari 16.1 (use `<picture>` fallbacks); WebP supported everywhere current. — [MDN: image file types](https://developer.mozilla.org/en-US/docs/Web/Media/Guides/Formats/Image_types)

### Inferences
- Pipeline that fits a 1-2 person team: one stage route in the gallery app (`/stage/:component?theme=&spot=`), one Playwright script looping components x {light, dark}, `page.emulateMedia`/project-level `colorScheme` for theme, `locator.screenshot()` or `toHaveScreenshot` on the stage root, `animations: disabled`, run in the official Playwright Docker image locally and in CI, encode to WebP lossless (or AVIF lossy at high quality for large stage images) after capture, commit or upload.
- Using VRT baselines as gallery images is possible (Playwright/Vitest store plain files in git) but couples gallery freshness to test tolerance: `threshold` 0.2 and `maxDiffPixels` mean small visual changes keep passing against the old baseline, so the "baseline" image can lag the real component. A dedicated generator without tolerance (always overwrite, diff in review) gives stricter sync. Names with platform suffixes (`-darwin`/`-linux`) need a rename step.
- Hosted tools (Chromatic, Argos) are strong for approval workflows but their images live behind their UI; no documented stable asset URLs were found, so they are not a gallery-image CDN.
- Cache-busting: content-hash in the filename (`button.dark.<hash8>.webp`) computed from the image bytes, referenced via a generated manifest; changed component = new hash = new URL, unchanged = no churn in git/CDN. To avoid regenerating all 35 apps' worth of images, key the regeneration on the component's source/token hash. (No source; design suggestion.)
- Determinism checklist: pinned Playwright image, bundled web fonts (no system font fallback), frozen `Date`/random seeds in demo data, `animations: disabled`, `caret: hide`, fixed viewport and `deviceScaleFactor` 2, mask or remove volatile content, wait for `document.fonts.ready` and images.
- Format choice: lossless WebP is the safe default for UI stills (sharp text edges); AVIF saves more bytes but has weaker legacy support and is not progressive; SVG only if vector section 4 route is taken.

### Gaps
- Whether Chromatic or Argos expose snapshot images by stable public URL/API for reuse: not found in docs read.
- Reg-suit and Percy/Happo docs not read.
- No engineering post from GitHub Primer, Shopify, Vercel or Linear about auto-generating doc screenshots was found in searches; only generic Playwright/Storybook material.
- Histoire `plugin-screenshot` current status/options unverified from primary docs (only secondary slides/guide).

## 4. Vector/schematic approaches (SVG from DOM, Satori, wireframe render mode)

### Takeaway
Of the SVG routes, `dom-to-svg` (in a real browser, e.g. under Puppeteer/Playwright) is the only one that converts a real rendered component to a text-preserving, design-tool-compatible SVG; Satori re-renders a React-like element tree with its own layout engine (so it can't take real Vue components), and `html-to-image` produces a `foreignObject` SVG that only browsers render. A "wireframe render mode" via tokens gives the schematic look without a conversion step and works with any screenshot or live approach.

### Cited Findings
- Satori returns an SVG string from an element tree; text is converted to `<path>` by default (`embedFont: false` gives `<text>`); fonts are mandatory (TTF/OTF/WOFF/WOFF2, variable fonts at default instance); "It's not a complete CSS implementation"; `:hover` never matches; `@font-face`, `@keyframes`, `@import` ignored; `<link>`/`<script>` not loaded; tables unsupported; invalid inline styles fail the whole render; React hooks unsupported; supports flexbox, grid (not `subgrid`), CSS variables, `opacity`, `filter`, `boxShadow`, `clipPath`, `mixBlendMode`, `@layer`, limited `@media`. PNG needs a separate step (Sharp / librsvg). — [vercel/satori](https://github.com/vercel/satori)
- `dom-to-svg`: converts a DOM node to an "accessible SVG screenshot" via `elementToSVG(element)` / `documentToSVG(document)`; keeps text as text, annotates ARIA, keeps links, preserves CSS stacking order, avoids `<foreignObject>` so output opens in Illustrator/Figma; `inlineResources` embeds fonts/images as data URIs; "Designed to run in the browser" (JSDOM likely fails; Puppeteer works). Repo: 213 commits, 37 open issues, 17 open PRs, 440 stars, no releases listed in the capture, so maintenance is unclear. — [felixfbecker/dom-to-svg](https://github.com/felixfbecker/dom-to-svg)
- `html-to-image`: clones the DOM, copies computed styles (recreating pseudo-elements), inlines `@font-face` fonts and images as data URLs, wraps in `<foreignObject>` in an SVG data URL; exports `toSvg`, `toPng`, `toJpeg`, `toCanvas`, `toBlob`; options include `filter` (exclude nodes and their children), `backgroundColor`, `pixelRatio`, `cacheBust` (default false, appends timestamp to URL requests), `fontEmbedCSS`, `imagePlaceholder`; known failure on huge DOMs (data URI size limits), tainted canvases; "Chrome performs significantly better on large DOM trees"; tested on Chrome 49, Firefox 45, Safari 16 at time of writing. — [bubkoo/html-to-image](https://github.com/bubkoo/html-to-image)
- `component-anatomy` shows the live-DOM annotation route (no image at all): `data-part` on live elements, theme tokens and runtime `setTheme()`, 4 presets including `blueprint`. — [component-anatomy](https://github.com/julien-deramond/component-anatomy)

### Inferences
- Satori fit: good for OG/social images and a separately authored schematic, poor for "stay in sync with the real component": you'd maintain a second, React-style description of every component, and Vue SFCs can't be passed in. Reject for this use case (unless used on an HTML-string-to-vnode shim, which I did not verify).
- `dom-to-svg` fit: crisp at any card size, small files for outline/wireframe style (few fills, text as text), theme baked in at conversion so ship one SVG per theme or post-process colors into CSS variables; risks: unreleased/uncertain maintenance, CSS features (filters, backdrop-filter, complex gradients) may fall back poorly, text becomes real `<text>` so fonts must be available or paths needed. Best used on the wireframe-mode output, where DOM is already simple.
- `html-to-image`: runs in the page (so can be a "download as image" button) but SVG is a `foreignObject` wrapper around HTML, so it is not a true vector asset and depends on the browser to rasterize; accuracy issues with fonts/pseudo-elements vs. a headless Chromium screenshot. Prefer Playwright for CI; keep for in-browser export only.
- Wireframe render mode ("components draw themselves as boxes"): implement as the token swap in section 2 plus `data-render="wireframe"` CSS that sets fills to transparent, borders to 1px, text to bars; costs one theme layer and is reusable for loading skeletons. Pros: always in sync, one source of truth, works live and for screenshots, small gzip if converted to SVG. Cons: needs discipline in components (icons, images, canvas-based components, third-party inner widgets ignore tokens); text-as-bars needs a `font`/`color` hack; looks generic.
- Screenshots vs. SVG summary: screenshots are higher fidelity and zero conversion risk but heavier (hence WebP/AVIF) and not themable after the fact; SVG is themable only if you keep CSS variables (which dom-to-svg, as described, does not).

### Gaps
- No evidence of dom-to-svg release cadence, supported CSS list or known issues with Vue/Teleport; test before relying on it.
- No benchmark of SVG size vs WebP size for wireframe output.
- Whether `satori-html` or similar shims allow real HTML strings into Satori: not researched.

## 5. Live mini-previews instead of images

### Takeaway
Live previews trade zero image staleness for per-card runtime cost; with 50-100 cards the standard mitigations are mounting only visible cards (IntersectionObserver or native lazy loading) and `content-visibility: auto`, plus a static thumbnail fallback. No source I found measured scaled-iframe or scaled-DOM thumbnails at 50-100 cards, so performance claims below are inference.

### Cited Findings
- `content-visibility: auto`: off-screen elements gain layout/style/paint containment and, while not relevant, size containment and skipped painting/hit-testing; the article's demo gives "a 7x rendering performance boost on initial load" (travel-blog example: 232 ms to 30 ms); requires `contain-intrinsic-size` (placeholder size, or `auto` to remember last rendered size) or elements collapse to 0 height and scrollbars jump; content stays in the accessibility tree and searchable; Baseline newly available since 2025-09-15 (Chrome 85, Edge 85, Firefox 125, Safari 18). — [web.dev: content-visibility](https://web.dev/articles/content-visibility)
- Iframes isolate content but cost performance (generic). — [Framer glossary](https://www.framer.com/ja/dictionary/lazy-loading) (search snippet)
- Lazy-loading patterns for embeds: native `loading="lazy"` on iframes (Drupal Lazy iframe module) and "static thumbnail, swap for the real iframe via IntersectionObserver". — [Drupal: lazy_iframe](https://drupal.org/project/lazy_iframe), [Brilliant Directories: lazyload iframes](https://support.brilliantdirectories.com/support/solutions/articles/12000106650) (search snippets, vendor support pages)
- Vue docs: a `transform`/`filter`/`perspective` ancestor makes `position: fixed` descendants relative to that ancestor instead of the viewport; teleported content goes to its `to` target. — [Vue: Teleport](https://vuejs.org/guide/built-ins/teleport.html)

### Inferences
- `transform: scale()` thumbnails: layout box keeps the unscaled size, so wrap in a fixed-size `overflow: hidden` box with `transform-origin: 0 0`; text is resampled (soft) at small scales; `position: fixed` content inside a scaled wrapper is contained by it (Vue docs rule) while Teleport-to-body content escapes it, so overlay demos must be inline or teleported into the wrapper.
- Real components in the same document (not iframes) share the Vue runtime, CSS and fonts, so 100 cards cost DOM/style/layout, not 100 separate documents. Iframes would each need CSS + JS, so avoid iframes for 100 cards unless isolation is needed (e.g. per-app theme packs).
- Budget estimate: a spotlight card with ~20-40 components x 100 cards = 2,000-4,000 live component instances; mount lazily (IntersectionObserver) and unmount off-screen, with `content-visibility: auto` + `contain-intrinsic-size` on the card shell, and a static WebP as placeholder. Hybrid recommended: static image by default, live stage on hover/focus or on the component's own page. (No measurement behind these numbers.)
- Live mini-previews and static images can share one stage page: the same URL feeds the iframe and the Playwright screenshot.
- Reduced-motion and `inert` apply to live cards (section 6).

### Gaps
- No measurements for 50-100 scaled iframes or scaled DOM trees; the search returned only generic lazy-load advice.
- Doc sites that actually ship scaled live thumbnails (Storybook "inline stories", Histoire grid, Ladle) not inspected; verify how Histoire's variant grid/preview handles it.

## 6. Accessibility of such cards

### Takeaway
A spotlight card is an image of UI, so it needs a text alternative that names the component and what is featured; the dimmed context can be low-contrast without failing WCAG 1.4.3 (inactive-component and "picture with significant other visual content" exceptions), but the focal component should still meet normal contrast, and any hover animation must honor `prefers-reduced-motion`.

### Cited Findings
- WCAG 2.2 1.4.3: "Text or images of text that are part of an inactive user interface component, that are pure decoration, that are not visible to anyone, or that are part of a picture that contains significant other visual content, have no contrast requirement." — [W3C: Understanding 1.4.3](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html)
- WAI image decision tree: informative image needs short alt text conveying the meaning; decorative image gets empty alt; complex image: "Include the information contained in the image elsewhere on the page". — [W3C WAI: images decision tree](https://www.w3.org/WAI/tutorials/images/decision-tree/)
- Alt-text practice in design systems varies: Atlassian uses sentence-length descriptions of each mock-up ("Two buttons in a group. One says cancel and is grey, the other says primary and is blue...") — [Atlassian Button usage](https://atlassian.design/components/button/usage); Fluent 2 uses short names ("Split Button", "Button layout don't") — [Fluent 2 Button usage](https://fluent2.microsoft.design/components/web/react/core/button/usage); Material overview on developer.android.com uses captions with empty `alt` — [Android Developers](https://developer.android.com/design/ui/mobile/guides/components/material-overview).
- `prefers-reduced-motion`: values `no-preference` / `reduce`; Baseline widely available since January 2020; animations like "scaling or panning large objects can be vestibular motion triggers". — [MDN: prefers-reduced-motion](https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion)
- `inert` removes content from the accessibility tree and tab order and has no default visual cue. — [MDN: inert](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Global_attributes/inert)
- Playwright `animations: "disabled"` freezes CSS animations/transitions/Web Animations for stills. — [Playwright LocatorAssertions](https://playwright.dev/docs/api/class-locatorassertions)
- `content-visibility: auto` keeps off-screen content in the accessibility tree. — [web.dev](https://web.dev/articles/content-visibility)

### Inferences
- Alt text pattern: `"{Component} ({state/variant}) highlighted in a {context} layout; surrounding components are dimmed."` — short, no repetition of on-card text; put variant detail in the card's visible caption instead of long alt. Whether the card should also be a link: if the whole card is a link, alt contributes to the link name (functional-image rule in the same decision tree), so keep it consistent with the visible title.
- Contrast: the dimmed context probably falls under the exemption (picture with other significant visual content, or inactive components when rendered live and `inert`), but this is an interpretation; keep the focal component at the real component's normal contrast (it is the content), and keep the dim level legible enough to read as context (avoid dropping to the point where chrome disappears on either theme). Verify dim colors in both themes with a contrast checker; a fixed `--spot-ink-low` for light and dark is simpler than percentage opacity.
- Live cards: mark context `inert`, keep the focal component's own accessible name, ensure the whole card has one focus stop (the link), and don't let hover animation (scale, lift, scrim fade) run under `prefers-reduced-motion: reduce`; swap to an instant opacity/outline change instead.
- Dark mode: a scrim tuned for light backgrounds looks muddy on dark; define spotlight tokens per theme rather than a single opacity.

### Gaps
- Contrast for non-text components (WCAG 1.4.11) on dimmed context not examined; no authoritative source on dim-level legibility.
- No testing with assistive tech for image-based component galleries.

## 7. Cross-cutting: approach comparison for a 1-2 person team (all inference, built from sections 1-6)

### Takeaway
One stage page with a token-swap spotlight mode is the single source of truth; a Playwright script screenshots it per component x theme for the default card image, and the same page can serve as the optional live preview. Hosted VRT tools and Satori are weak fits for gallery assets.

### Cited Findings
- See sections 2-5 for the sourced facts behind each row.

### Inferences
| Approach | Build cost | Sync with code | Theming | Effort (1-2 people) | Main risk |
|---|---|---|---|---|---|
| A. Live spotlight on stage page (token swap) | Medium: token alias layer + stage route + `--spot-*` per theme | Exact, always | Native (CSS vars) | ~3-5 days if tokens exist | Portals and overlays need Teleport-target handling; runtime weight if all cards live |
| B. Playwright element screenshots of A, two `colorScheme` projects, WebP/AVIF | Medium: script + pinned Docker + CI job + manifest | Exact at CI time; stale if not triggered by component/token changes | Two contexts | ~2-3 days on top of A | Font/OS drift; image churn without content-hash naming |
| C. Reuse VRT baselines (Playwright/Vitest) as card images | Low | Lags within tolerance (`threshold` 0.2, `maxDiffPixels`) | Per project | ~1 day | Platform-suffixed names, tolerance staleness, coupled to test lifecycle |
| D. Hosted VRT (Chromatic/Argos) | Low setup, recurring cost | Exact | Modes / projects | ~1 day | No documented public image URLs; Lost Pixel archived 2026-04-22 |
| E. SVG via dom-to-svg inside Playwright | High | Exact at CI time | One SVG per theme (baked) | ~4-6 days | Maintenance uncertainty, CSS fidelity, text/font handling |
| F. Satori | High | None (second authoring) | Manual | ~5+ days per component set | Cannot render Vue components; CSS subset |
| G. Wireframe render mode (extends A) | Medium | Exact | Native | +1-2 days | Components with icons/images/third-party internals ignore tokens |
| H. Live scaled previews | Low-medium | Exact | Native | ~1-2 days | 50-100 cards perf; scale blur; overlay escapes |

- Suggested pick: A + B (+ G as a second style option); hover/focus swaps to H only for the opened card. Revisit C only if Playwright VRT already exists in the repo.

### Gaps
- Effort figures are estimates, not sourced; they assume the library already has semantic design tokens and a gallery app with per-component demo pages.

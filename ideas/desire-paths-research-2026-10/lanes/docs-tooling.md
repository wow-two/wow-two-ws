# Documenting and showcasing a Vue 3 component library: Storybook vs custom gallery vs hybrid

Research date: 2026-10-27. Method: WebSearch plus WebFetch of primary pages (Storybook docs/release pages, GitHub/raw package.json files, GitHub REST API for release dates). WebFetch returns summaries produced by a small model, so quoted wording on fetched pages (for example the Storybook 10.6 deprecation line) is worth re-checking on the page before it is repeated as fact. Anything dated before 2024 is tagged "(possibly stale: YEAR)".

## Q1. Storybook as of late 2026 (v9/v10+): Vue 3 support quality, docgen/ArgTypes, Vitest addon, a11y and visual testing, composition, iframe embedding, size/speed, Vue pain points

### Takeaway
Storybook 10.x (latest seen: 10.6, September 2026) supports Vue 3 on Vite through `@storybook/vue3-vite`, with prop/slot/event ArgTypes from `vue-component-meta` (opt-in) or `vue-docgen-api` (still the default), a Vitest-based component-test addon, an axe-core a11y addon, and Chromatic-based visual testing. Vue gets new features about one release after React (CSF factories, docgen service), and its main Vue-specific frictions are docgen/tsconfig setup and the single-`args` model that merges props and slots.

### Cited Findings
**Release timeline**
- Storybook 10.0 shipped October 2025; its one breaking change is ESM-only, install size is 29% smaller, on top of a 50% reduction in Storybook 9; Node 20.16+, 22.19+ or 24+ is required; module automocking via `sb.mock`; Vitest 4 support added — [Storybook 10 announcement](https://storybook.js.org/blog/whats-new/storybook-10), [10.0 release page](https://storybook.js.org/releases/10.0)
- In 10.0, CSF factories were React-only (Preview status); Vue/Angular/Web Components were "expected in 10.x" — [Storybook 10 announcement](https://storybook.js.org/blog/whats-new/storybook-10)
- 10.2 (January 2026) added typesafe CSF factories for Vue, Angular and Web Components (Preview), a viewports/zoom UI, and experimental MDX support for Storybook MCP — [10.2 release page](https://storybook.js.org/releases/10.2)
- 10.5 (July 2026): Angular-vite preview, Vitest `initialGlobals` (run tests across themes/viewports/locales), experimental agentic review, an experimental React docgen service shared across MCP/Docs/Controls; no breaking changes; no Vue-specific items — [10.5 release page](https://storybook.js.org/releases/10.5)
- 10.6 (September 2026): "new skills architecture for agentic workflows"; for Vue: MCP and skills support plus improved docgen and snippets, marked experimental; performance and smaller bundle; no breaking changes listed — [10.6 release page](https://storybook.js.org/releases/10.6)

**Vue 3 framework and docgen / ArgTypes**
- `@storybook/vue3-vite` requires Vue 3 (Vue 2 unsupported; Storybook 7 suggested as the fallback) and Vite 5+ — [Storybook Vue+Vite docs](https://storybook.js.org/docs/get-started/frameworks/vue3-vite)
- `framework.options.docgen` accepts `'vue-docgen-api'`, `'vue-component-meta'` or a boolean; default is `vue-docgen-api`; `vue-component-meta` is "maintained by the Vue team", recommended for most projects, extracts props/events/slots/exposed, still opt-in — [Storybook Vue+Vite docs](https://storybook.js.org/docs/get-started/frameworks/vue3-vite)
- The same page (as summarised by the fetch tool) says `vue-docgen-api` is "deprecated since Storybook 10.6" and will be removed in the next major; `features: { experimentalDocgenServer: true }` is an alternative that uses `vue-component-meta` and becomes the default in Storybook 11 — [Storybook Vue+Vite docs](https://storybook.js.org/docs/get-started/frameworks/vue3-vite). Re-check this wording on the page.
- Caveat: with tsconfig `references`, `vue-component-meta` may need `docgen.tsconfig` pointed at a specific file such as `tsconfig.app.json`, otherwise "missing component types/descriptions or unresolvable import aliases like `@/some/import`"; the docs say this is how `vue-component-meta` works, not a Storybook limitation — [Storybook Vue+Vite docs](https://storybook.js.org/docs/get-started/frameworks/vue3-vite)
- `docgen: false` improves build performance but argTypes are no longer inferred, so Controls/autodocs need manual argTypes — [Storybook Vue+Vite docs](https://storybook.js.org/docs/get-started/frameworks/vue3-vite)

**Vitest addon (component testing)**
- Turns stories into component tests that run in a real browser, reports status in the Storybook UI, can compute coverage from stories; needs a Vite-based framework (`vue3-vite` qualifies) and Vitest 3.0+ — [Vitest addon docs (10.6)](https://storybook.js.org/docs/writing-tests/integrations/vitest-addon)
- The `storybookTest` Vitest plugin converts stories via portable stories; each story gets a smoke render test and its `play` function runs; default include tag is `test`, adjustable with include/exclude/skip — [Vitest addon docs (10.6)](https://storybook.js.org/docs/writing-tests/integrations/vitest-addon)
- Browser mode with Playwright Chromium is the default and recommended setup; WebdriverIO is an alternative; snapshot tests are not supported by the addon (the older test-runner supports them) — [Vitest addon docs (10.6)](https://storybook.js.org/docs/writing-tests/integrations/vitest-addon)
- Listed limitations: Vite-only; the Vite config `test` property merges into the addon's Vitest config; "Failed to fetch dynamically imported module" errors in CI under load (fix: `isolate: false` or sharding); non-default public dirs need `publicDir`; Vitest 4 uses `projects`, Vitest 3.x below 3.2 a workspace file — [Vitest addon docs (10.6)](https://storybook.js.org/docs/writing-tests/integrations/vitest-addon)

**Accessibility**
- `@storybook/addon-a11y` is built on Deque axe-core, which the docs say "automatically catches up to 57% of WCAG issues"; default ruleset WCAG 2.0/2.1 A and AA plus best practices; config under `parameters.a11y` (`context`, `config`, `options`, `test`) — [a11y docs (10.6)](https://storybook.js.org/docs/writing-tests/accessibility-testing)
- `a11y.test` is `'off'`, `'todo'` (warnings) or `'error'` (fails UI and CI); with the Vitest addon the checkbox in the testing widget runs a11y with component tests, and CI fails only for `'error'` stories — [a11y docs (10.6)](https://storybook.js.org/docs/writing-tests/accessibility-testing)
- Limits: async components may not finish rendering before checks (false negatives); results can differ across browser versions — [a11y docs (10.6)](https://storybook.js.org/docs/writing-tests/accessibility-testing)

**Visual testing**
- Cross-browser visual testing is "native" through Chromatic (a cloud service by the Storybook team) via `@chromatic-com/storybook`; stories are sent to the cloud for snapshots; CI needs a Chromatic project token; visual tests run independently of component tests and are included when the Vitest addon runs all tests — [visual testing docs](https://storybook.js.org/docs/writing-tests/visual-testing), [Vitest addon docs](https://storybook.js.org/docs/writing-tests/integrations/vitest-addon)
- The visual-testing page gives no pricing and does not say whether self-hosting is possible — [visual testing docs](https://storybook.js.org/docs/writing-tests/visual-testing)

**Composition (several Storybooks in one)**
- `refs` in `.storybook/main.ts` (keys `title`, `url`, optional `expanded`, `sourceUrl`; can be a function of `configType`) shows other Storybooks in the sidebar, any framework, as long as each is reachable by URL — [Composition docs](https://storybook.js.org/docs/sharing/storybook-composition)
- Composition depends on the referenced Storybook's `index.json`; `storybook extract` no longer exists in 8.0+; "Addons in composed Storybooks will not work as they normally do" — [Composition docs](https://storybook.js.org/docs/sharing/storybook-composition)
- The page does not mention cross-origin, authentication or version-mismatch behaviour — [Composition docs](https://storybook.js.org/docs/sharing/storybook-composition)

**Embedding stories elsewhere**
- Iframe embeds work out of the box but the Storybook must be published and publicly reachable; URL forms: `…/?path=/story/<id>&full=1&shortcuts=false&singleStory=true` (with toolbar) or `…/iframe.html?id=<id>&viewMode=story&shortcuts=false&singleStory=true` (canvas only); docs embed uses `viewMode=docs` and the `<component>--docs` id — [Embed docs](https://storybook.js.org/docs/sharing/embed)
- oEmbed (Notion/Medium/Ghost) needs a Chromatic-published Storybook — [Embed docs](https://storybook.js.org/docs/sharing/embed)
- zeroheight (a third-party design-docs tool) embeds Storybook via iframe and notes that a Storybook behind a VPN only renders for users on the VPN — [zeroheight help](https://help.zeroheight.com/hc/en-us/articles/35886961403675-Storybook-Embed-Storybook)

**Build size and speed**
- Install size: -50% in 9, -29% in 10 (published code un-minified); the Storybook 10 article makes no build-speed claims — [Storybook 10 announcement](https://storybook.js.org/blog/whats-new/storybook-10)
- Third-party figures (PkgPulse, 2026-03-08, "medium project, 50 stories", Storybook 8 era, no hardware/version/method stated): Storybook 8 Vite cold start ~8 s (Webpack 15-20 s), HMR ~2 s; Histoire ~2 s / ~500 ms — [PkgPulse](https://www.pkgpulse.com/guides/storybook-8-vs-ladle-vs-histoire-2026)

**Known pain points for Vue users**
- Props and slots with the same name collide because Storybook merges both into one `args` object while Vue keeps them separate (maintainer explanation) (possibly stale: 2023) — [storybook#23470](https://redirect.github.com/storybookjs/storybook/issues/23470)
- Generated code snippets / "Show code" with slots were repeatedly wrong: extra brackets, named slots, reactive string slots rendered as empty template tags (possibly stale: 2023) — [storybook#21129](https://redirect.github.com/storybookjs/storybook/issues/21129), [PR #22518](https://redirect.github.com/storybookjs/storybook/pull/22518), [PR #23784](https://github.com/storybookjs/storybook/pull/23784)
- A GitLab UI team described Vue 3 arg bindings as a known Storybook problem "since version 7" (date not captured) — [gitlab-ui MR 4827](https://gitlab.com/gitlab-org/gitlab-ui/-/merge_requests/4827)
- A comparison guide says Storybook's Vue support "sometimes falls through because Storybook is usually only up to date with React" (secondary source, opinion) — [PkgPulse](https://www.pkgpulse.com/guides/storybook-8-vs-ladle-vs-histoire-2026)

### Inferences
- Vue features trail React by roughly one to three minor releases: CSF factories React-only in 10.0 and Vue Preview in 10.2 (about 3 months later); docgen service experimental for React in 10.5 and for Vue in 10.6. The Vue path is supported but not first-class.
- Trade-off of keeping Storybook: it gives the Vitest/a11y/visual-test tooling and a stories-as-fixtures format for free, but it costs a second app with its own dev server, `docgen` and tsconfig quirks, and an `args` model that is awkward for slot-heavy components.
- With a `vue-docgen-api` deprecation announced for 10.6 and `vue-component-meta` becoming the default path, any new pipeline (Storybook or custom) should standardise on `vue-component-meta` now.
- The 2023 issue threads may be fixed in 9/10; they are evidence of the category of friction (slots in args), not current status. A spike against the SDK's slot-heavy components would settle it.

### Gaps
- No primary-source Storybook build time or output size for a Vue project; only the unverified PkgPulse figures.
- Whether the 2023 Vue slot/snippet bugs are fixed in 9/10: not checked.
- Storybook 9 release date and feature list not fetched (only referenced via the Storybook 10 article).
- Chromatic pricing and self-hosted alternatives for the visual-test addon: not documented on the fetched page.

## Q2. Vue-native alternatives and which are maintained (Histoire, VitePress, Nuxt Content/Docus, Vue Styleguidist, others)

### Takeaway
Histoire is alive but slow to release (last tagged release v1.0.0-beta.1 on 2026-01-07, commits as recent as 2026-10-26), VitePress and Nuxt Content/Docus are actively maintained and are what most Vue libraries actually use for docs, and Vue Styleguidist is effectively dormant (Vue 2 era, last release May 2023).

### Cited Findings
**Histoire**
- Repo `histoire-dev/histoire`: `pushed_at` 2026-10-26, not archived, 205 open issues, 3,585 stars — [GitHub API](https://api.github.com/repos/histoire-dev/histoire)
- Recent releases (all pre-1.0): v1.0.0-alpha.1 2025-01-22 (Vite 6), alpha.2 2025-02-21, alpha.3 2025-07-30 (Vite 7), alpha.4 2025-10-20 (CommonJS, `vitePlugins` hook, style isolation), alpha.5 2025-11-20, v1.0.0-beta.1 2026-01-07 (Nuxt 4 support, fix for story collection on Vue 3.5.26+, Vitest 4) — [GitHub releases API](https://api.github.com/repos/histoire-dev/histoire/releases)
- No release in the ~9.5 months after beta.1, although the default branch is still being pushed to; the README offers per-commit nightly builds from `main` — [GitHub releases API](https://api.github.com/repos/histoire-dev/histoire/releases), [Histoire repo](https://github.com/histoire-dev/histoire)
- The README states support for Vue 3, React 18/19, Svelte 4/5, Nuxt 3/4, SvelteKit; requires Vite 7 or 8 and Node 22+; no maintenance notice — [Histoire repo](https://github.com/histoire-dev/histoire)
- Features: write stories, controls, no-config (reuses the Vite config), themable app, auto-generated copyable template code, dark mode; commands `histoire dev|build|preview`; Nuxt 3 via `@histoire/plugin-nuxt` — [histoire.dev](https://histoire.dev/), [Vue 3 getting started](https://histoire.dev/guide/vue3/getting-started)
- Story format is `.story.vue`, not CSF; moving to or from Storybook means rewriting stories — [PkgPulse](https://www.pkgpulse.com/guides/storybook-8-vs-ladle-vs-histoire-2026)
- Vendor-neutral comparison articles say Histoire is lighter/faster for Vue but has a much smaller addon ecosystem (no first-party a11y/Chromatic/Vitest integration) (secondary, low rigor, mostly undated or 2023-2026) — [PkgPulse](https://www.pkgpulse.com/guides/storybook-8-vs-ladle-vs-histoire-2026)
- A 2023 Zenn article lists histoire@0.17.6 as the latest version at that time; shows how long Histoire stayed pre-1.0 (possibly stale: 2023) — [Zenn](https://zenn.dev/ormair/articles/158f62f4787c11)

**VitePress**
- Stable line is 1.6.x (Element Plus pins `^1.6.4`, Reka UI `1.6.3`); the 2.0 line is still alpha: v2.0.0-alpha.17 2026-03-19, alpha.18 2026-07-06, alpha.19 2026-08-02, alpha.20 2026-09-04, alpha.21 2026-10-25; release notes just point to CHANGELOG.md — [VitePress releases API](https://api.github.com/repos/vuejs/vitepress/releases), [Element Plus docs package.json](https://raw.githubusercontent.com/element-plus/element-plus/dev/docs/package.json), [Reka UI docs package.json](https://raw.githubusercontent.com/unovue/reka-ui/v2/docs/package.json)
- Component-demo plugins exist outside core: `@vitepress-demo-preview` (`:::preview` container, shows rendered demo plus source; collapsibility not confirmed), Wikimedia Codex's pattern of one `.vue` file per example in an examples directory — [ecosyste.ms entry](https://awesome.ecosyste.ms/projects/2045166), [Codex component demos](https://doc.wikimedia.org/codex/main/contributing/contributing-code/component-demos.html)

**Nuxt Content / Docus**
- Docus is a documentation CLI and Nuxt layer for Markdown (MDC syntax embeds Vue components), built on Nuxt 4, Nuxt UI 4 and Tailwind CSS 4; features include full-text search, dark mode, auto sidebar, and (newer versions) AI assistant, MCP server, i18n — [Docus repo](https://github.com/nuxt-content/docus)
- `@nuxt/content` is at ^3.15.2 in shadcn-vue's docs app (Nuxt `^4.5.2`) — [shadcn-vue apps/v4 package.json](https://raw.githubusercontent.com/unovue/shadcn-vue/dev/apps/v4/package.json)
- `nuxt-component-meta` (NuxtLabs/nuxt-content org) collects component metadata at build time, exposes it via `/api/component-meta/<name>` and a standalone `getComponentMeta` (props, slots, events, exposed), plus `propsToJsonSchema`; 92 stars, 238 commits; no releases listed on the repo page — [nuxt-component-meta](https://github.com/nuxt-content/nuxt-component-meta)

**Vue Styleguidist and docgen**
- `vue-styleguidist` latest 4.72.4, published May 2023; Snyk rates it "Inactive" (no npm release in 12 months) although the repo showed commits about 2 months before Snyk's snapshot; a Yarn mirror page says it supports Vue 2.x only (possibly stale: 2023) — [Snyk Advisor](https://dev.snyk.io/advisor/npm-package/vue-styleguidist)
- `vue-docgen-api` (same org) has `dist-tags.latest` 4.79.2 on npm; publish date not retrieved — [npm registry](https://registry.npmjs.org/vue-docgen-api)

**Other**
- Ladle and Histoire are the two "lighter than Storybook" tools in the PkgPulse guide; it recommends Histoire for Vue 3/Svelte (Ladle's framework scope was not verified here) — [PkgPulse](https://www.pkgpulse.com/guides/storybook-8-vs-ladle-vs-histoire-2026)

### Inferences
- Maintenance ranking for a Vue SDK in October 2026: VitePress and Nuxt Content/Docus (active, large user base) > Storybook (active, Vue second-tier) > Histoire (alive, pre-1.0, release gaps) >> Vue Styleguidist (dormant).
- Trade-offs: Histoire is cheapest to adopt if stories already exist as Vue components and the team wants a Storybook-like app without CSF, but a 9-month gap between tags on a beta is a bus-factor risk and it has no first-party test/a11y story. VitePress is lowest-friction for a static, self-hosted docs site (fits a plain Node/static VPS); VitePress 2 being alpha means pinning 1.6.x. Docus/Nuxt Content gives richer content features (collections, search, MDC) and Nuxt Studio-style editing, at the cost of a Nuxt app and heavier moving parts.
- For a custom "gallery" app (illustrated cards, philosophy pages, where-used), the practical choice is VitePress or Nuxt Content as the shell and a custom Vue theme/components, not Histoire or Styleguidist.

### Gaps
- Histoire's own docs on controls, docs blocks, embedding/SDK and visual testing were not retrievable (fetch returned only nav); features beyond the homepage list are unconfirmed.
- No maintainer statement about Histoire's roadmap or the delay since beta.1 was found.
- VitePress 2.0 stable timeline: not found.
- Nuxt Content/Docus release dates not retrieved.
- Other candidates (Vue Playground-style tools, Docz, Catalog) were not evaluated for Vue 3 maintenance.

## Q3. How Nuxt UI, PrimeVue, Vuetify, Reka UI, shadcn-vue, Element Plus, Naive UI and Ark UI build their docs sites

### Takeaway
None of the eight public docs sites I inspected is a Storybook; four are Nuxt-based or Next-based custom apps, two are VitePress, and two (Vuetify, Naive UI) are hand-rolled Vite apps with custom markdown pipelines. I found no maintainer statement explaining why any of them chose their stack.

### Cited Findings
**Stack matrix (from each repo's docs `package.json`, read 2026-10-27)**

| Library | Docs framework | Component API data | Highlighting | Search | Live/embedded examples | Source |
|---|---|---|---|---|---|---|
| Nuxt UI | Nuxt + `@nuxt/content` + `@nuxt/ui` + `@nuxtjs/mdc` (docs app in `nuxt/ui/docs`: `app/`, `content/`, `modules/`, `server/`, `content.config.ts`) | `nuxt-component-meta` + `vue-component-meta` | `shiki` + color/icon-highlight transformers | none listed in package.json | examples as Vue components in `app/components/content/examples` | [package.json](https://raw.githubusercontent.com/nuxt/ui/v4/docs/package.json), [docs tree](https://github.com/nuxt/ui/tree/v4/docs), [contribution guide](https://ui.nuxt.com/docs/getting-started/contribution) |
| PrimeVue | Nuxt (`apps/showcase`, `nuxt generate`) | `typedoc` 0.23.23 via `scripts/build-apidoc.cjs` | none listed | `@docsearch/js` (Algolia DocSearch) | `@stackblitz/sdk` embeds | [package.json](https://raw.githubusercontent.com/primefaces/primevue/master/apps/showcase/package.json) |
| Vuetify | Custom Vite + Vue 3 app (`vite-plugin-pages`, `vite-plugin-md`, `vite-plugin-vue-layouts`, `vite-plugin-pwa`) | `@vuetify/api-generator` workspace package (`src/`, `templates/`; internals not inspected) | `markdown-it-prism` / `prismjs` (no Shiki) | Algolia (`algoliasearch`, `vue-instantsearch`) | none listed | [package.json](https://raw.githubusercontent.com/vuetifyjs/vuetify/master/packages/docs/package.json), [api-generator](https://github.com/vuetifyjs/vuetify/tree/master/packages/api-generator) |
| Reka UI | VitePress 1.6.3 | `vue-component-meta` ^3.3.11 + `docs:gen` script (`scripts/autogen.ts`) | `shiki` ^4.0.2 | `minisearch` ^6.3.0 + `mark.js` | `@stackblitz/sdk`, `codesandbox` | [package.json](https://raw.githubusercontent.com/unovue/reka-ui/v2/docs/package.json) |
| shadcn-vue | Nuxt ^4.5.2 + `@nuxt/content` ^3.15.2 (`apps/v4`) | `vue-metamorph` 3.3.4 listed (purpose not stated); registry built by `tsx` scripts | `shiki` ^4.4.3 + `nuxt-shiki` | none listed | none listed | [package.json](https://raw.githubusercontent.com/unovue/shadcn-vue/dev/apps/v4/package.json), [apps tree](https://github.com/unovue/shadcn-vue/tree/dev/apps) |
| Element Plus | VitePress ^1.6.4 + UnoCSS + Crowdin i18n | not listed in docs package.json | VitePress default | `@docsearch/js` ^4.6.2 | `docs/.vitepress/plugins/` exists (demo mechanism not verified) | [package.json](https://raw.githubusercontent.com/element-plus/element-plus/dev/docs/package.json), [.vitepress tree](https://github.com/element-plus/element-plus/tree/dev/docs/.vitepress) |
| Naive UI | Custom Vite 8 + Vue 3 demo site in the main repo (`demo/`, `build:site`); `scripts/md-to-vue.ts` converts Markdown to Vue using `marked` | not listed | `highlight.js` ^11.8 (no Shiki) | not listed | `codesandbox` ^2.2.3 | [package.json](https://raw.githubusercontent.com/tusen-ai/naive-ui/main/package.json), [repo](https://github.com/tusen-ai/naive-ui) |
| Ark UI | Next.js 15.5.27 (`website/`), content via `velite` | `@zag-js/docs`, `generate:examples` script | `shiki` 4.5.0 + `@shikijs/rehype` | `match-sorter` (usage not shown) | `@stackblitz/sdk` | [website package.json](https://raw.githubusercontent.com/chakra-ui/ark/main/website/package.json) |

**Other observations from those files**
- Four of the eight emit LLM-oriented docs output: Nuxt UI (`nuxt-llms`, `@nuxtjs/mcp-toolkit`), PrimeVue (`build:llmdocs`), Reka UI (`vitepress-plugin-llms`), Element Plus (`gen-llms` script) — package.json files linked above
- Nuxt UI's docs also build OG images (`nuxt-og-image`), sitemap and schema.org data; shadcn-vue uses `nuxt-og-image` — [Nuxt UI package.json](https://raw.githubusercontent.com/nuxt/ui/v4/docs/package.json), [shadcn-vue package.json](https://raw.githubusercontent.com/unovue/shadcn-vue/dev/apps/v4/package.json)
- Ark UI's repo root has a `.storybook` folder next to `website/`, so Storybook exists in the repo; which frameworks it covers and whether it is public was not shown — [Ark repo root](https://github.com/chakra-ui/ark/tree/main)
- Ark UI is a multi-framework library (React/Vue/Solid) but its docs site is a Next.js app, not a Vue app — [Ark website package.json](https://raw.githubusercontent.com/chakra-ui/ark/main/website/package.json)
- Nuxt UI scaffolding: `pnpm cli make component <name>` generates component, theme, tests and docs (`--template=docs` for docs only); component docs live under `content/docs/2.components` — [Nuxt UI contribution guide](https://ui.nuxt.com/docs/getting-started/contribution)

### Inferences
- Pattern: Markdown-first docs framework (VitePress or Nuxt Content) plus examples that are real `.vue` files plus a generated API table from `vue-component-meta`. Three of eight (Nuxt UI, Reka UI, and indirectly Storybook's own default) already converge on `vue-component-meta`; shadcn-vue's docs app and Nuxt UI both use Shiki 4.
- Choice tracks the library's own ecosystem: Nuxt-family libraries (Nuxt UI, PrimeVue, shadcn-vue) use Nuxt; the Vue-core-adjacent Reka and Element Plus use VitePress; the older Vuetify/Naive UI sites predate VitePress maturity (unverified reason).
- Evidence that a library ships "a custom docs app instead of Storybook" is strong; evidence about why is absent. The likely reasons (SEO, MDX-like prose, i18n, LLM output, branding) are guesses.

### Gaps
- No maintainer post, talk or README explaining the stack choice for any of the eight; "why" is unanswered.
- Whether the other seven repos also run an internal Storybook/Histoire for development: not checked (only Ark's `.storybook` folder seen).
- Naive UI and Element Plus demo/preview mechanism, and Vuetify api-generator internals: files not readable via fetch.
- shadcn-vue's use of `vue-metamorph`: purpose unknown.
- Search for Nuxt UI/shadcn-vue not in package.json; may be built in via Nuxt Content/Nuxt UI (`UContentSearch`) but not verified.

## Q4. Building blocks for a custom app: prop/slot/event tables, live examples, highlighting, search, isolation, theming, deep links

### Takeaway
Use `vue-component-meta` for the API tables (it is what Storybook, Nuxt UI and Reka UI converge on), Shiki 4 for highlighting, an existing Markdown shell (VitePress or Nuxt Content) for content, and either `@vue/repl` (self-hostable) or the StackBlitz SDK (hosted, third-party) for editable examples; iframes remain the safe default for example isolation.

### Cited Findings
**Prop/slot/event tables**
- `vue-component-meta` statically extracts `name`, `description`, `type`, `props`, `events`, `slots`, `exposed`; props carry description (JSDoc), type string, default, required, global flag, tags, schema — [language-tools component-meta](https://github.com/vuejs/language-tools/tree/master/packages/component-meta)
- API: `createChecker(tsconfigPath, options)`, `createCheckerByJson`, `checker.getComponentMeta(filePath, exportName)`, `getExportNames`, `updateFile`/`deleteFile` (for virtual files or live editing), `reload`, `clearCache`, `getProgram`; `schema` option parses type structure with an `ignore` list — [language-tools component-meta](https://github.com/vuejs/language-tools/tree/master/packages/component-meta)
- npm shows `vue-component-meta` 3.0.5 on the page returned by search; Reka UI pins `^3.3.11`, so later 3.x exists — [npm](https://npmjs.com/package/vue-component-meta), [Reka UI docs package.json](https://raw.githubusercontent.com/unovue/reka-ui/v2/docs/package.json)
- Known practical caveat: tsconfig `references` and path aliases need an explicit tsconfig — [Storybook Vue+Vite docs](https://storybook.js.org/docs/get-started/frameworks/vue3-vite)
- A sibling package (`kdu-component-meta`) notes static analysis cannot read defaults for props built by function execution; not confirmed for `vue-component-meta` — [npm kdu-component-meta](https://npmjs.com/package/kdu-component-meta)
- `nuxt-component-meta` wraps this into a Nuxt module with `/api/component-meta/<name>`, a standalone parser (`rootDir`, `cache`, `cacheDir`) and `propsToJsonSchema` — [nuxt-component-meta](https://github.com/nuxt-content/nuxt-component-meta)
- `vue-docgen-api` latest 4.79.2 on npm; Storybook's docs say it is deprecated since 10.6 — [npm registry](https://registry.npmjs.org/vue-docgen-api), [Storybook Vue+Vite docs](https://storybook.js.org/docs/get-started/frameworks/vue3-vite)
- PrimeVue instead uses `typedoc` plus a custom `build-apidoc.cjs` script for its API data — [PrimeVue showcase package.json](https://raw.githubusercontent.com/primefaces/primevue/master/apps/showcase/package.json)

**Live editable examples**
- `@vue/repl` ("Vue SFC REPL as a Vue 3 component", MIT, ~1.1k stars): `Repl` component takes an explicit `editor` prop (CodeMirror: light, no intellisense; Monaco: Volar intellisense, heavier, loads `.d.ts` from a CDN); `useStore` configures Vue version/output mode and can serialise state (the demo syncs to the URL hash); a `Sandbox` component renders only the preview; the Vue compiler, TypeScript lib and es-module-shims load from configurable CDN URLs (override with `resourceLinks`); current major is v4; must be excluded from Vite `optimizeDeps` — [vuejs/repl](https://github.com/vuejs/repl)
- Reka UI, PrimeVue and Ark UI all use `@stackblitz/sdk` (opens or embeds projects on StackBlitz); Reka UI and Naive UI also depend on `codesandbox` — package.json files linked in Q3
- StackBlitz WebContainers licensing: aggregator listings (not StackBlitz's own terms) say commercial production use needs a custom-priced commercial licence and self-hosting falls under an Enterprise tier on Kubernetes; Pro/Teams prices conflict between listings — [aicoolies StackBlitz pricing](https://aicoolies.com/pricing/stackblitz) (low confidence; the exact listing carrying each claim was not isolated)

**Syntax highlighting**
- Shiki 4.x is used by Reka UI (^4.0.2), shadcn-vue (^4.4.3 plus `nuxt-shiki`), Ark UI (4.5.0 with `@shikijs/rehype`, langs, themes, transformers) and Nuxt UI (plus colour/icon-highlight transformers); Vuetify uses Prism, Naive UI highlight.js — package.json files linked in Q3

**Client-side search**
- Pagefind: runs after the build, indexes generated HTML, no server component; works with any static HTML; version 1.5.0 introduced a Component UI (search modal, better accessibility, more customisation) replacing the Default UI — [Pagefind docs](https://pagefind.app/docs/)
- A 2026 comparison blog (opinion, no benchmarks) calls Pagefind the most consistently recommended option for static docs, says its index is public (cannot hide protected content), describes Orama (Apache-2.0, full-text/vector/hybrid, TypeScript-friendly) and MiniSearch (browser library, you build the index pipeline and UI) — [merginit.com](https://merginit.com/blog/22062026-free-site-search-comparison)
- MiniSearch is an explicit dependency of Reka UI's VitePress docs (with `mark.js` for highlighting); DocSearch (Algolia) is used by PrimeVue and Element Plus; Vuetify uses Algolia InstantSearch; Ark lists `match-sorter` — package.json files linked in Q3

**Example isolation (iframe vs shadow DOM vs in-page)**
- Storybook renders stories in an iframe (`iframe.html`) — [Embed docs](https://storybook.js.org/docs/sharing/embed)
- Histoire added "style isolation" in v1.0.0-alpha.4 (2025-10-20) — [Histoire releases API](https://api.github.com/repos/histoire-dev/histoire/releases)
- Docz maintainers wanted inline playgrounds with style isolation and tried a Shadow DOM wrapper that injected the library's stylesheets; it worked but broke HTML preview and was clunky per demo (possibly stale: Docz issue is old, date not captured) — [docz#290](https://github.com/doczjs/docz/issues/290)
- A Semi Design page says most component libraries do not work inside Shadow DOM without adaptation, mainly because styles do not cross the boundary — [Semi Design web-components page](https://lf3-static.semi.design/obj/semi-tos/semi_main/page-data/en-US/ecosystem/web-components/page-data.b1cc784dab72677950cc1ea48ee3ebc93ff4bc12.json)
- Shadow DOM still inherits colour, font and CSS custom properties; `::part()` styles exposed parts — [html-include README](https://cdn.jsdelivr.net/npm/html-include-element@0.3.0/README.md)

**Theme / dark-mode switching**
- Storybook: `@storybook/addon-themes` (needs Storybook 7+; Vue listed as supported) switches themes from the toolbar; `globals: { theme: 'dark' }` at meta or story level pins a theme; Vuetify 3 needs a custom decorator — [addon-themes](https://storybook.js.org/addons/@storybook/addon-themes)
- Histoire lists dark mode and a themable generated app as built-in — [histoire.dev](https://histoire.dev/)
- Vitest addon 10.5 `initialGlobals` can run the same stories under several themes/viewports/locales — [10.5 release page](https://storybook.js.org/releases/10.5)

**Deep links per example**
- Storybook: `?path=/story/<id>` and `iframe.html?id=<id>&viewMode=story|docs` — [Embed docs](https://storybook.js.org/docs/sharing/embed)
- `@vue/repl` can serialise REPL state into the URL hash — [vuejs/repl](https://github.com/vuejs/repl)

### Inferences
- Trade-off of `@vue/repl`: self-hostable and free of third-party licence terms, but the SDK must be resolvable by the REPL's import map (published ESM bundle on a CDN or served from the VPS), the compiler loads from a CDN by default, and Monaco is heavy. StackBlitz SDK is the least work (three of the eight libraries use it) but embeds a hosted third-party service and ties examples to npm-published versions.
- Because `updateFile` exists, `vue-component-meta` can in principle regenerate metadata for edited examples in a Node service, but no source shows this pattern in use; treat as untested.
- Search: for a few hundred pages Pagefind (drop-in UI, needs a build step over HTML) or MiniSearch (VitePress-style, JSON index you control, can index component metadata directly) are both enough; Orama only earns its weight if semantic/vector search matters. If the gallery is an SPA rather than static HTML, Pagefind indexing HTML is less direct than MiniSearch/Orama over a generated JSON.
- Isolation default: iframe (clean CSS, Storybook-compatible deep links, matches what the Vitest/Playwright screenshot runs want); in-page rendering is fine for the philosophy/illustration cards where the SDK's own CSS is the page CSS.

### Gaps
- Did not retrieve a source on how nuxt/ui, Reka or Vuetify render the API table UI from metadata (only the dependencies).
- No Vue-specific benchmark or maintenance data for Orama and MiniSearch beyond the blog and package.json usage.
- No official StackBlitz WebContainers licence text found; only aggregators.
- Where-used info (which of the ~35 apps import which component/prop): no tool or library pattern found in this research; it would need a custom AST scan (inference, not sourced).

## Q5. Combine vs separate: linking, embedding, `index.json` as a data source, and the maintenance cost of two apps

### Takeaway
Storybook officially supports three integration points a gallery can use: deep links to stories/docs, iframe embeds of single stories or docs entries, and a machine-readable `/index.json` (plus custom indexers); its "composition" feature merges Storybooks into Storybook, not into an arbitrary site. No source quantifies the cost of running two apps, so that part is inference.

### Cited Findings
- `index.json` is served at the `/index.json` route of a Storybook; its entries come from `IndexInput` fields: `type` (`story` or `docs`), `id` (generated from title and export name), `name`, `title`, `importPath`, `exportName`, `tags`, `rawComponentPath`, optional `subtype` (`story`/`test`, experimental), `metaId` — [Indexers API](https://storybook.js.org/docs/api/main-config/main-config-indexers)
- Custom indexers (`experimental_indexers`, object with `test` regex and `createIndex`) can turn non-CSF files into index entries, but need a builder plugin to make them renderable (unplugin recommended); custom `importPath` works only in Vite projects — [Indexers API](https://storybook.js.org/docs/api/main-config/main-config-indexers)
- The page does not say whether `/index.json` is served in dev as well as in a static build — [Indexers API](https://storybook.js.org/docs/api/main-config/main-config-indexers)
- Embed forms and constraints (public URL, `viewMode=story|docs`, `<component>--docs` id): see Q1 — [Embed docs](https://storybook.js.org/docs/sharing/embed)
- Composition shows other Storybooks inside a Storybook UI (`refs`), needs each ref's `index.json`, and addons do not work normally in composed Storybooks — [Composition docs](https://storybook.js.org/docs/sharing/storybook-composition)
- A design-documentation product (zeroheight) uses the iframe route to embed Storybook, with a VPN caveat — [zeroheight help](https://help.zeroheight.com/hc/en-us/articles/35886961403675-Storybook-Embed-Storybook)
- The Nuxt UI docs app holds its live examples as ordinary Vue components inside the docs repo rather than linking out to a Storybook — [Nuxt UI contribution guide](https://ui.nuxt.com/docs/getting-started/contribution)

### Inferences
Trade-offs per option (no source states these; derived from the findings above):
- Keep Storybook, add gallery that links out ("open in Storybook" via `?path=/story/<id>`): cheapest to start; the gallery can read `index.json` at build time to know which stories exist per component and generate links. Costs: two deploys, two themes to keep aligned, two places to document a component; links break if story ids change.
- Keep Storybook, embed it in the gallery via `iframe.html?id=…&viewMode=story` (or `viewMode=docs`): one navigation surface and live controls inside gallery pages; costs: iframe sizing/theme sync, Storybook must be reachable from the browser (static deploy on the VPS is fine), embed ids must be tracked. Composition is not the tool for this; it embeds Storybooks in Storybook.
- Replace Storybook with the custom app: one app, one theme, one search, examples reused as fixtures; costs: you rebuild controls, source-snippet display, a11y panel and test-runner integration (the Vitest addon and addon-a11y), and you own API-table generation and slot/event docs (all feasible with `vue-component-meta` per Q4).
- `index.json` as a data source is cheap, but only describes stories; it carries no prop tables or illustrations, so the gallery's cards and philosophy content still need their own data source.
- The ~35 consuming apps do not need Storybook; they need the SDK and the gallery's "where used" data. Storybook's value is concentrated in the SDK maintainers' dev loop and CI.

### Gaps
- No case study or maintainer post of a Vue library running a custom gallery and Storybook side by side with measured upkeep.
- Cross-origin, auth and version behaviour of composition and iframe embeds with a self-hosted private Storybook: not documented on the fetched pages.
- Whether `/index.json` is available from the dev server: unclear.

## Q6. Testing overlap: what replaces stories as fixtures if Storybook goes, and can gallery examples double as visual-regression fixtures?

### Takeaway
Vitest browser mode (Playwright provider) with `vitest-browser-vue` is the documented replacement for story-driven component tests, with `toMatchScreenshot` for visual regression; Playwright's own Vue component testing is still labelled experimental. Gallery examples can serve as fixtures only if each is individually renderable at a stable URL or importable as a component.

### Cited Findings
- Vitest browser mode renders Vue components through the community package `vitest-browser-vue` (API modelled on `@testing-library/vue`; requires Vitest 4.0.0+; `render` must be awaited; auto-cleanup in the default entry) — [Vitest browser Vue API](https://v4.vitest.dev/api/browser/vue), [alexop.dev guide](https://alexop.dev/posts/vue3_testing_pyramid_vitest_browser_mode/)
- Vitest visual regression: `await expect(page.getByRole('button')).toMatchScreenshot()`; baselines in `__screenshots__` beside the test, named with browser and platform (for example `button-chromium-darwin.png`); update with `vitest --project vrt --update`; the diff image marks changed pixels red and anti-aliasing yellow; comparator is `pixelmatch` by default with SSIM/GMSD options — [Vitest visual regression](https://vitest.dev/guide/browser/visual-regression-testing)
- Vitest's docs warn that screenshots differ by GPU, OS, fonts, browser version and headless mode; they recommend self-hosted/Docker runners, generating references in CI, or cloud services; Playwright is the fullest provider and disables animations by default — [Vitest visual regression](https://vitest.dev/guide/browser/visual-regression-testing)
- The Vitest visual-regression page does not mention Vue explicitly — [Vitest visual regression](https://vitest.dev/guide/browser/visual-regression-testing)
- Playwright `toHaveScreenshot`: baselines in `<file>.spec.ts-snapshots`, names include browser and platform, `threshold` default 0.2, `maxDiffPixels` unset by default, `stylePath` for hiding volatile elements, `--update-snapshots`; advice is to run in the same environment that created the baselines — [Playwright snapshots](https://playwright.dev/docs/test-snapshots)
- `@playwright/experimental-ct-vue` is still documented as "Components (experimental)"; a third-party post says maintainers gave no graduation date, that config/hook signatures changed between releases, and (unverified) that Playwright 1.59 (April 2026) removed the Svelte CT package — [Playwright components docs](https://playwright.dev/docs/test-components), [Currents](https://currents.dev/posts/playwright-component-testing)
- Storybook's Vitest addon reuses stories as test fixtures via portable stories, runs `play` functions, and includes a11y/visual runs; the standalone alternative to its Chromatic visual testing is not covered on Storybook's page — [Vitest addon docs](https://storybook.js.org/docs/writing-tests/integrations/vitest-addon), [visual testing docs](https://storybook.js.org/docs/writing-tests/visual-testing)
- Storybook 10.5's Vitest `initialGlobals` lets one story set run across themes, viewports and locales — [10.5 release page](https://storybook.js.org/releases/10.5)

### Inferences
- Replacement stack if Storybook goes: Vitest browser mode + `vitest-browser-vue` + Playwright provider for behaviour and screenshots; axe-core (the engine Storybook's a11y addon wraps) run directly in those tests for a11y (inference: running axe-core directly is not documented in the fetched sources). Fixtures become the example `.vue` files themselves, which is exactly what a gallery already needs.
- Gallery examples as visual-regression fixtures: two workable shapes. (a) Import each example SFC in a Vitest browser test and `toMatchScreenshot` it; (b) a manifest of example deep links (one stable URL per example, no site chrome) and a Playwright loop with `toHaveScreenshot`. Both need deterministic data, disabled animations and one canonical runner image (Docker on the VPS or CI) because baselines are platform-suffixed.
- Cost of dropping Storybook's test layer: lose the single-click path from story to test to a11y to visual diff (and Chromatic's review UI); gain one fewer toolchain and no CSF maintenance. Self-hosted screenshot diffs have no review UI unless built.
- Playwright CT's experimental status makes it a weaker base than Vitest browser mode for a long-lived SDK.

### Gaps
- No source tested Vue-specific visual-regression behaviour in Vitest (docs examples are framework-neutral).
- No head-to-head data on Chromatic vs self-hosted Playwright/Vitest screenshot review workflows or costs.
- No source for a11y via axe-core directly in Vitest browser mode for Vue (only through Storybook's addon).
- `vitest-browser-vue` release date and maintenance status not captured (only that it is community-maintained and needs Vitest 4+).

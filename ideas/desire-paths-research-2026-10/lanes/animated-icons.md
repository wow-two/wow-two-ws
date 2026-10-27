# Animated / state-morphing UI icons and an LLM icon harness (Vue 3 SDK on lucide)

Lane scope: icon animation between states and LLM generation of icons and their animations. Licensing and coverage of icon sets, and our own usage, are other lanes. Research date 2026-10-27. Tags: **primary** (vendor docs, paper, repo, fetched) · **secondary** (press, aggregator, vendor blog about a rival) · **snippet** (search-result summary only, page not read in full) · **opinion** (practitioner blog). Numbers reached me through a page summariser, so treat exact decimals as approximate.

## 1. Prior art for state transitions (as of 2026)

### Takeaway
Apple's SF Symbols is the most complete reference model: a fixed vocabulary of effects (bounce, pulse, variable colour, scale, appear/disappear, replace → wiggle, rotate, breathe → draw on/off, variable draw, enclosure-aware Magic Replace) triggered by state values. On the web the closest open equivalent is lucide-animated (MIT, React + Motion, ~350–470 icons, hover-triggered). Its Vue port is small and lightly maintained. True path morphing (GSAP MorphSVG, now free; flubber; KUTE.js) exists but is a different technique from what Apple ships.

### Cited Findings
**Apple SF Symbols**
- SF Symbols 7 (WWDC25, session 337) added **Draw On / Draw Off**, presets "inspired by the calligraphic movement of handwriting". Playback modes are By Layer (default, staggered), Whole Symbol, and Individually (new: each layer waits for the previous one) — [WWDC25 What's new in SF Symbols 7](https://developer.apple.com/videos/play/wwdc2025/337/) (primary)
- Draw relies on designer-placed **guide points** (start, end, corner, bidirectional, attachments for arrowheads), because symbol shapes have variable width and "can't simply be stroked". Only the Regular weight is annotated; the system interpolates guide points to Ultralight and Black — [WWDC25 337](https://developer.apple.com/videos/play/wwdc2025/337/) (primary)
- **Variable Draw** (SF Symbols 7) partially draws chosen layers to show progress or strength (download, temperature). A symbol may support both Variable Color and Variable Draw, but only one is used at render time — [WWDC25 337](https://developer.apple.com/videos/play/wwdc2025/337/) (primary)
- **Magic Replace** pre-dates SF Symbols 7. Version 7 added enclosure matching: "If two symbols share the same enclosure, the system will preserve them, while simultaneously replacing the differing layers". Draw-capable symbols draw off, then draw on, during the swap — [WWDC25 337](https://developer.apple.com/videos/play/wwdc2025/337/) (primary)
- SF Symbols 7 ships over 6,900 symbols plus gradient rendering — [Apple SF Symbols page](https://developer.apple.com/sf-symbols) (snippet); [9to5Mac, 2025-06-11](https://9to5mac.com/2025/06/11/apple-releases-sf-symbols-7-beta/) (secondary)
- SF Symbols 6 (WWDC24) added the universal presets **Wiggle, Rotate, Breathe** and updated Replace and Variable Color. Apple suggests Wiggle for a change or call to action and Rotate for "a task in progress", with bi-layer rotation for parts of a symbol — [WWDC24 session 10188](https://developer.apple.com/videos/play/wwdc2024/10188/) (snippet); [WWDC Notes](https://wwdcnotes.com/documentation/wwdc24-10188-whats-new-in-sf-symbols-6/) (secondary)
- Bounce, pulse and replace date from SF Symbols 5. In SwiftUI, effects run through `.symbolEffect(...)`, and swapping two symbols runs through `.contentTransition(.symbolEffect(.replace))` — [Blake Crosley, Symbol Effects vocabulary](https://blakecrosley.com/blog/symbol-effects-vocabulary) (opinion/secondary); [createwithswift](https://www.createwithswift.com/animating-sf-symbols-with-the-symbol-effect-modifier/) (snippet)
- SwiftUI triggers Draw from a state value: "when the value of isHidden updates, the symbol will draw off and back on again" — [WWDC25 337](https://developer.apple.com/videos/play/wwdc2025/337/) (primary)

**Google Material Symbols (variable font)**
- Axes: FILL 0–1, wght 100–700, GRAD (the example range is −50..200), opsz 20–48dp. Apache 2.0 licence — [Material Symbols guide](https://developers.google.com/fonts/docs/material_symbols) (primary)
- Google's guidance: "To convey a state transition, use the fill axis for animation or interaction". For CSS animation, use the variable font and request axis ranges in the CSS API URL (e.g. `:FILL,ROND@0..1,100`) — [Material Symbols guide](https://developers.google.com/fonts/docs/material_symbols) (primary)
- Cost: the full variable font with all axes is 7.9 MB. An icon subset with FILL and ROND axes is 2.6 KB. The static default font with all icons is 295 KB — [Material Symbols guide](https://developers.google.com/fonts/docs/material_symbols) (primary)
- Custom axes are set via `font-variation-settings: 'FILL' 1` — [material-web icon docs](https://material-web.dev/components/icon) (snippet)

**Animated icon libraries**
- **lucide-animated** (repo `pqoqubbw/icons`, site lucide-animated.com): MIT, animated **React** icons built with Motion (motion.dev). The page says "350+" in one place and lists 468 icons. It installs per icon through a shadcn registry URL, which writes `components/icons/<name>.tsx` and adds `motion`. Icons animate on hover and forward standard SVG props. It also ships `llms.txt`, a full-corpus file and an MCP server (`search_icons`, `list_icons`, `get_icon`) — [lucide-animated index.md](https://lucide-animated.com/index.md) (primary)
- The lucide-animated repo adds a term: components are free for personal and commercial use, but "tutorials and demos … cannot be redistributed or resold" — [Mintlify mirror of pqoqubbw/icons](https://www.mintlify.com/pqoqubbw/icons) (snippet)
- Ports listed: Vue (`imfenghuang.github.io/icons`), Svelte (movingicons.dev), Angular (`ajitzero/animated-icons`), Flutter (`flutter_lucide_animated`) — [lucide-animated index.md](https://lucide-animated.com/index.md) (primary)
- The **Vue port** `imfenghuang/icons` is MIT and uses `@vueuse/motion` (not motion-v). It has 39 stars, 59 commits and no releases, and documents no install method or API — [GitHub imfenghuang/icons](https://github.com/imfenghuang/icons) (primary)
- **Lordicon** (Lottie-based): the licence page says the free tier is CC BY-ND 4.0-based but "non-commercial" only, needs attribution, and is capped at 1M CDN requests. Its attribution page says free icons can be used commercially with credit, so Lordicon's own pages conflict. PRO removes attribution. The API PRO plan is $149/month with 1,500 icon downloads — [Lordicon licences](https://lordicon.com/licenses) (snippet); contradicted by [Lordicon attribution](https://lordicon.com/docs/license/attribution) (snippet); [Lordicon API pricing](https://lordicon.com/docs/api/pricing) (snippet)
- **useAnimations** (Lottie/After Effects icons, React): the repo licence reads "other". A third-party README says the files are CC BY with attribution required, commercial use allowed. No official licence page was found — [awesome.ecosyste.ms entry](https://awesome.ecosyste.ms/projects/github.com%2Fuseanimations%2Freact-useanimations) (snippet); [use_widgets README](https://pub-web-s1.flutter-io.cn/packages/use_widgets/versions/0.2.0) (snippet)

**Morphing engines**
- **GSAP**: free since Webflow's support, including former Club plugins such as **MorphSVG** and SplitText. The Standard "No Charge" licence took effect 2025-04-30 (page modified 2025-05-30) and covers commercial websites and apps. It prohibits use in no-code visual animation builders that compete with Webflow, reverse engineering, and removing notices. The FAQ says AI tools that generate GSAP code are not a prohibited use — [GSAP Standard License](https://gsap.com/community/standard-license/) (primary); [Webflow forum](https://discourse.webflow.com/t/webflow-makes-gsap-100-free/319967) (snippet)
- `gsap-trial` is deprecated; install the plain `gsap` package — [npm gsap-trial](https://npmjs.com/package/gsap-trial) (snippet)
- **KUTE.js** has `svgMorph` (implements "some D3.js and flubber functionality") and `svgCubicMorph`; npm shows 2.2.4 with no date — [KUTE.js GitHub](https://www.GitHub.com/thednp/kute.js) (snippet); [npm kute.js](https://www.npmjs.com/package/kute.js) (snippet)
- **flubber** is still used in Motion's path-morphing tutorials as the interpolator — [Motion: SVG path morphing](https://motion.dev/tutorials/js-svg-path-morphing) (snippet)
- A 2023 forum user found KUTE.js smoother than MorphSVG on polygon corners — [GSAP forum thread 38001](https://gsap.com/community/forums/topic/38001-different-morphing-behavior-between-morphsvgplugin-and-kutejs/) (opinion)

**Rive / Lottie**
- Rive claims its files are 10–15× smaller than uncompressed Lottie JSON (example: 240 KB → 16 KB). LottieFiles' own comparison repeats the ratio, but a DEV post claims the opposite — [Rive blog](https://rive.app/blog/rive-as-a-lottie-alternative) (secondary, vendor); [LottieFiles blog](https://lottiefiles.com/blog/lottie-animations/lottiefiles-or-rive) (secondary, vendor); contradicted by [DEV Community](https://dev.to/uianimation/rive-vs-lottie-which-animation-tool-should-you-use-in-2025-p4m) (opinion)
- Rive has the more mature state machine (boolean, trigger and pointer inputs). LottieFiles added a state machine to Lottie Creator in late 2025 — [LottieFiles blog](https://lottiefiles.com/blog/lottie-animations/lottiefiles-or-rive) (snippet)
- Web runtime sizes are unverified: one blog gives Rive ~146 KB minified and Lottie light ~18 KB — [learnwithhasan](https://learnwithhasan.com/js-libraries/rive/) (opinion, snippet)

**Vue-specific**
- **motion-v** (Motion for Vue) exports `motion` and `AnimatePresence`. AnimatePresence runs `:exit` animations when children leave through `v-if`, `v-show`, a changed `key` or a `v-for` removal. SVG `x`/`y` use `attrX`/`attrY` — [Motion Vue AnimatePresence](https://motion.dev/docs/vue-animate-presence) (snippet); [Motion Vue animation](https://motion.dev/docs/vue-animation) (snippet)
- Vue's built-in `<Transition>` with `mode="out-in"` (or overlapping enter/leave) swaps two elements keyed differently, using CSS classes and no runtime library — [Vue docs: Transition](https://vuejs.org/guide/built-ins/transition.html) (primary, not re-fetched this session)

### Inferences
- Apple's vocabulary splits into **transient** effects (bounce, wiggle, draw on), **indefinite** effects (pulse, rotate, breathe, variable colour/draw) and **replace** (state A → state B). That split maps cleanly onto an SDK API (see §3).
- Apple needed guide points because its glyphs are filled outlines. Lucide icons are already uniform 2px centred strokes, so a web "Draw On" is cheap: `pathLength="1"` + `stroke-dasharray: 1` + animated `stroke-dashoffset`. Magic Replace's enclosure trick (keep shared parts, draw off/on the rest) is reproducible when the two lucide icons share sub-elements (e.g. `circle` + `check` vs `circle` + `x`). This is general web-platform knowledge, not sourced above.
- Lucide is stroke-only, so the Material FILL-axis idea does not transfer directly. The analogue is animating `fill`/`fill-opacity` on closed shapes (heart, star, bookmark) for toggle states.
- lucide-animated is the best corpus of "how lucide icons should move" (motion vocabulary per icon). It is a React + Motion runtime, so it is a reference and few-shot source for us rather than a dependency.

### Gaps
- Whether WWDC26 (June 2026) added SF Symbols 8 effects was not verified. Latest confirmed: SF Symbols 7 (2025).
- The exact SF Symbols version that introduced Magic Replace is not confirmed by a fetched source. SF Symbols 6 (2024) is from memory.
- Licences and maintenance status of flubber and KUTE.js were not confirmed (no dated commits seen).
- Official Rive / dotLottie web runtime sizes were not checked on npm.
- Whether motion-v supports `pathLength` on SVG like Motion for React was not confirmed.

## 2. Which transitions are worth it, usability evidence, and costs

### Takeaway
Evidence supports motion as **feedback** and **state-change explanation**: NN/g names icon morphing (pencil → disk) as clearer than an instant swap. The same sources warn about distraction, overuse and "down-time" animation. WCAG 2.3.3 (AAA) requires interaction-triggered motion to be disableable (`prefers-reduced-motion`). The worthwhile set is small: action → loading → done/error, copy → copied, toggles (play/pause, menu/close, favourite), and progress.

### Cited Findings
- NN/g lists animation purposes as feedback ("noticeable feedback that an action has been recognized by the system"), state change, signifiers, and spatial or navigation metaphors. Motion fits best as subtle microinteraction feedback — [NN/g, Laubheimer, 2020-01-12](https://www.nngroup.com/articles/animation-purpose-ux/) (primary)
- NN/g: "morphing a pencil icon into a disk" signals Edit → Save more clearly than swapping icons instantly. It cites Material's pencil → + example for Edit vs Add — [NN/g](https://www.nngroup.com/articles/animation-purpose-ux/) (primary)
- NN/g warnings: users are "prone to be distracted by any type of motion"; many simultaneous animations compete for attention; "down-time animations" frustrated participants in testing; animation used to "hijack the users' attention" is a dark pattern. Motion should be "unobtrusive, brief, and subtle" — [NN/g](https://www.nngroup.com/articles/animation-purpose-ux/) (primary)
- Durations of 100–500ms are commonly cited, with "a good reason" needed above ~300ms. Feedback within 0.1s feels instant and 1s is the limit of the user's flow of thought, attributed to NN/g — [Val Head](https://valhead.com/?p=2978) (secondary, snippet); [Kijo](https://kijo.london/blog/microinteractions) (secondary, snippet)
- Google: use the FILL axis "to convey a state transition" — [Material Symbols guide](https://developers.google.com/fonts/docs/material_symbols) (primary)
- Apple ties Rotate to "a task in progress" and Wiggle to a change or call to action. Variable Draw is meant for progress such as downloads — [WWDC24 10188](https://developer.apple.com/videos/play/wwdc2024/10188/) (snippet); [WWDC25 337](https://developer.apple.com/videos/play/wwdc2025/337/) (primary)
- **WCAG 2.3.3 Animation from Interactions (AAA)**: "Motion animation triggered by interaction can be disabled" unless essential. It protects people with vestibular disorders (dizziness, nausea, headaches). The technique is C39, the CSS `prefers-reduced-motion` query — [W3C Understanding 2.3.3](https://www.w3.org/WAI/WCAG22/Understanding/animation-from-interactions.html) (primary)
- Lordicon / Lottie-style animated icons are positioned as decorative or marketing assets (WordPress plugin, CDN embed with request caps) rather than product-UI state icons — [Lordicon WordPress plugin](https://wordpress.org/plugins/lordicon) (snippet); [Lordicon licences](https://lordicon.com/licenses) (snippet)

### Inferences
- High-value transitions for a product SDK, in rough priority:
  1. submit/send → spinner → check or x (async action feedback)
  2. copy → check, reverting after ~1.5–2s
  3. play ↔ pause, menu ↔ close, chevron rotate (expand/collapse)
  4. favourite/bookmark/star outline ↔ filled
  5. checkbox/check draw-on
  6. indefinite "in progress" (rotate or pulse)
- Low value: hover-wiggle on every nav icon (lucide-animated's default trigger). NN/g's distraction and overuse warnings apply most to many hover animations at once in dense UIs.
- Reduced motion should still switch state, through an instant swap or a ≤100ms crossfade. The state must not depend on the motion; it is information, so it is not "essential motion".
- Performance: transform and opacity animations are compositor-friendly. `stroke-dashoffset` and `d` animations repaint the SVG, which is cheap at 16–24px but adds up across long lists. Per-instance JS animation controllers (Motion, GSAP, Lottie players) cost more than CSS keyframes with many icons. General web-performance knowledge, not measured here.

### Gaps
- No controlled study was found that measures task performance with morphing vs swapped icons. NN/g's claim is expert guidance, not a quoted experiment.
- Apple HIG Motion page content could not be fetched (page body empty). Material 3 motion duration/easing tokens were not fetched.
- No primary NN/g duration article was retrieved; duration figures are secondary.

## 3. Delivering animated icons as components

### Takeaway
Three API shapes exist in the wild:
- a **declarative state value** that triggers the effect (SwiftUI `symbolEffect(value:)`, `contentTransition(.symbolEffect(.replace))`)
- **hover-triggered self-contained components** (lucide-animated)
- **imperative players** (Lottie, Rive, GSAP timelines)

For a Vue SDK, a declarative `state` prop over existing lucide icons, with CSS-only animation and the static icon as rest frame, keeps SSR trivial and adds almost no runtime.

### Cited Findings
- SwiftUI binds effects to a value: the effect runs when the value changes (`isHidden` example). Replace runs as a content transition between two symbol names — [WWDC25 337](https://developer.apple.com/videos/play/wwdc2025/337/) (primary); [Blake Crosley](https://blakecrosley.com/blog/symbol-effects-vocabulary) (opinion)
- lucide-animated ships one file per icon via the shadcn registry, animates on hover, forwards SVG props (`className`, `onClick`, `aria-label`) and depends on `motion` — [lucide-animated index.md](https://lucide-animated.com/index.md) (primary)
- The Vue port uses `@vueuse/motion` with `useMotion` on a template ref, so each icon is a JS-driven component — [imfenghuang/icons](https://github.com/imfenghuang/icons) (primary)
- Material Symbols animate through CSS `font-variation-settings` on a font glyph. The trade-off is font weight (7.9 MB full variable font vs 2.6 KB subset) — [Material Symbols guide](https://developers.google.com/fonts/docs/material_symbols) (primary)
- Rive drives icons through runtime state-machine inputs (booleans, triggers, pointer), which is an imperative player model — [LottieFiles vs Rive](https://lottiefiles.com/blog/lottie-animations/lottiefiles-or-rive) (snippet)
- motion-v `AnimatePresence` animates exits when a keyed child changes, which is a declarative swap model for Vue — [Motion Vue AnimatePresence](https://motion.dev/docs/vue-animate-presence) (snippet)

### Inferences
- Proposed SDK shape:
  - `<StateIcon :state="status" :icons="{ idle: Send, loading: Loader2, done: Check, error: X }" />`: a controlled swap. Each pair uses a named transition (`crossfade`, `scale`, `rotate`, `draw`, `shared` for Magic-Replace-style shared parts).
  - `<AnimatedIcon :icon="Copy" effect="bounce" :trigger="hover|click|manual" />`, plus an exposed `play()` for `manual`, for transient emphasis.
  - An `indefinite` effect (spin, pulse) driven by a boolean.
- The static fallback is free when the **final frame of every transition equals the static lucide icon**. Under SSR and before hydration the static SVG renders; with `prefers-reduced-motion: reduce` the component snaps to the final state.
- CSS keyframes keyed off a `data-state` attribute run without hydration and add only CSS bytes. Motion/GSAP add a JS runtime plus per-instance setup.
- Tree-shaking: transitions defined per icon pair (not per icon) keep the matrix small. ~6–10 named pair recipes cover §2's list; free-form per-icon choreography does not scale.

### Gaps
- Not verified: lucide-animated's imperative ref API (`startAnimation`/`stopAnimation`) and its reduced-motion handling. The fetched page mentions neither.
- Bundle sizes of motion-v, `@vueuse/motion` and GSAP core were not measured.

## 4. LLM-generated icons: quality, style consistency, existing tools, cost

### Takeaway
Frontier LLMs are the strongest general text-to-SVG generators in 2025–26 benchmarks. Claude Sonnet 4.5 sits within ~1.5 points of GPT-5.1 and Gemini 3 Pro on VectorGym Text2SVG. All models degrade sharply with complexity, and icons sit at the easy end. Style consistency is not measured by these benchmarks; it has to come from constraints (lucide's 24×24 / 2px / round rules), few-shot neighbours, linting and human review. Paid vector generators exist: Recraft at $0.08 per vector image, QuiverAI Arrow (SVG-native, 2026). No mature open-source "icon-set harness" was found, only thin agent skills.

### Cited Findings
**Quality evidence**
- **SVGenius** (arXiv 2506.03139, 2025-06-03): 2,377 queries, 8 task categories, 18 metrics. The generation subset is 300 icons across 24 domains, drawn from ~100K IconFont SVGs. 22 models were evaluated, including Claude 3.7 Sonnet, GPT-4o, Gemini 2.0 Flash, StarVector-8B, IconShop and LLM4SVG — [SVGenius](https://arxiv.org/html/2506.03139v1) (primary)
- SVGenius: all models degrade with complexity. Perceptual-QA accuracy falls Easy → Hard: Claude 3.7 Sonnet 80.25% → 33.33%, GPT-4o 82.72% → 42.22%. GPT-4o text-to-SVG HPS falls 20.35 → 16.69 — [SVGenius](https://arxiv.org/html/2506.03139v1) (primary; decimals via summariser)
- SVGenius Easy text-to-SVG: Claude 3.7 Sonnet HPS 21.35 / rCLIP 92.90; GPT-4o HPS 20.35 / rCLIP 90.95. SVG-specialised models collapse on Hard tasks (IconShop 12.95 HPS, LLM4SVG PSS 0.02). Small models show "fundamental syntactic failures" — [SVGenius](https://arxiv.org/html/2506.03139v1) (primary)
- **VectorGym** (arXiv 2603.29852, v1 dated 2026-02-22), Text2SVG task scores: GPT-5.1 70.68, Gemini 3 Pro 69.92, Claude Sonnet 4.5 69.19, GPT-4o 63.09. On editing, Gemini 3 Pro scores 88.71 and Claude Sonnet 4.5 88.07. A fine-tuned Qwen3-VL-8B ("Gym", GRPO with rendering rewards) matches GPT-4o but trails the frontier models — [VectorGym](https://arxiv.org/html/2603.29852v1) (primary)
- VectorGym failure modes: "incorrect primitive usage, semantic misunderstanding, and incomplete shape representations". It reports no icon-only breakdown — [VectorGym](https://arxiv.org/html/2603.29852v1) (primary)
- **OmniSVG** (NeurIPS 2025): an end-to-end multimodal SVG generator on pre-trained VLMs, covering icons through complex illustrations — [OmniSVG GitHub](https://github.com/OmniSVG/OmniSVG) (snippet). **InternSVG** (ICLR 2026) brings the SAgoge dataset and the SArena benchmark, covering static and animated SVG — [ICLR 2026 poster](https://iclr.cc/virtual/2026/poster/10008856) (snippet)
- Practitioner (Feb 2025, unnamed Claude.ai model): Claude does well on geometric or abstract subjects such as a three-pip die icon. It struggled with real objects (wrench, dart), where the author fell back to Recraft v3 or CC images. Expect "roughly the complexity level of a toddler with a set of crayons". Small fixes are faster by hand — [Ola Hungerford](https://www.olahungerford.com/drawing-and-animating-with-claude/) (opinion)

**Style constraints (lucide)**
- Lucide rules:
  - 24×24 canvas, ≥1px padding, exactly 2px centred stroke, round joins, round caps on open paths
  - corner radius 2px (1px for shapes <8px; ~2.41px for diagonals at right angles)
  - ≥2px between elements; coordinates and arc centres aligned to the pixel grid
  - optical volume matched against `circle`/`square`; prefer arcs and quadratics; avoid extra control points
  - reuse base shapes from existing icons unchanged
  - [Lucide icon design guide](https://lucide.dev/contribute/icon-design-guide) (primary)
- Code-level SVG conventions are on a separate Lucide page, not fetched — [Lucide icon design guide](https://lucide.dev/contribute/icon-design-guide) (primary)

**Existing tools and harnesses**
- `S6U5/lucide-svg-skill` (MIT, unofficial) is an agent skill that generates Lucide-style SVG plus Lucide-format metadata JSON. It self-checks padding, forbidden elements and naming, has an `evals/` folder, and recommends the official icon when the concept already exists. 0 stars, 7 commits — [GitHub lucide-svg-skill](https://github.com/S6U5/lucide-svg-skill) (primary)
- Other community Claude skills fetch official lucide SVG instead of generating it, warning that paths generated "from memory" risk hallucinated or malformed paths — [mcpmarket Lucide Icon Fetcher](https://mcpmarket.com/tools/skills/lucide-icon-fetcher) (snippet); [mcpmarket Icon Designer](https://mcpmarket.com/tools/skills/icon-designer) (snippet)
- lucide-animated exposes `llms.txt`, a full-corpus file and an MCP server, so a harness can pull animated-lucide examples as few-shot input — [lucide-animated index.md](https://lucide-animated.com/index.md) (primary)
- **Recraft** API: V3 Vector $0.08 per image (80 units; $1 = 1,000 units), V4.1 vector $0.08, V4.1 Pro vector $0.30 — [Recraft API pricing](https://www.recraft.ai/docs/api-reference/pricing) (snippet, official docs)
- **QuiverAI Arrow**:
  - Arrow 1.0 launched Feb 2026 with an $8.3M a16z-led seed
  - Arrow 1.1 (Apr 2026) targets icons, logos and illustrations; $0.20/image on Vercel AI Gateway, listed as going away 2026-10-16
  - Arrow 2 (Sept 2026) covers generation, vectorisation, editing and animation, listed at $4 / $20 per 1M input/output tokens
  - [Vercel AI Gateway Arrow 1.1](https://vercel.com/ai-gateway/models/arrow-1.1) (snippet); [Noqta](https://www.noqta.tn/en/news/quiverai-arrow-1-svg-native-ai-model-2026) (secondary); [Design Compass](https://designcompass.org/en/2026/09/29/quiver-ai-vector-generation-arrow-2/) (secondary); [LLM Reference Arrow 2](https://www.llmreference.com/model/arrow-2) (secondary)
  - A claimed SVG Arena #1 score (1583) for Arrow 1.0 comes from one unverified source — [Noqta](https://www.noqta.tn/en/news/quiverai-arrow-1-svg-native-ai-model-2026) (secondary)

### Inferences
- Benchmarks score semantic match and visual quality, not "fits our set". Our acceptance problem is style conformance plus recognisability at 16–24px, so most quality control comes from deterministic linting rather than model choice.
- Lucide's constraints suit lint rules well:
  - `viewBox="0 0 24 24"`; only `path/circle/rect/line/polyline/ellipse`; `stroke-width=2`, `stroke-linecap/linejoin=round`, `fill="none"`
  - all coordinates within [1, 23] after stroke expansion; coordinates snapped to 0.5 or 1px; a max element/node count
  - `svgo` with a pinned config for normalisation
- Few-shot from **semantic neighbours** (e.g. for `file-lock`, give `file`, `lock`, `file-key`) enforces lucide's "reuse base shapes unchanged" rule. This is where a frontier LLM is strongest (editing and composition, ~88 on VectorGym edit) rather than drawing from scratch.
- Raster-first generators (Recraft, Arrow) probably don't emit lucide-conformant 2px centred strokes, though this is unverified. At $0.08–0.20 per image they are cheap enough as an occasional reference sketch, not as the pipeline.
- Opus 5.5 is not in any benchmark found. Claude Sonnet 4.5 is the latest Claude model measured (VectorGym), so Opus 5.5 quality is unmeasured; extrapolating from Sonnet 4.5 is the only basis.
- Human review stays mandatory: recognisability and metaphor choice ("what icon means 'archive'?") are judgement calls the benchmarks don't measure.

### Gaps
- No source measures LLM conformance to a specific icon style guide (lucide or otherwise).
- "IconBuddy"-like tools and Figma AI icon plugins were not found or priced in this pass.
- Lucide's code-level SVG conventions page was not fetched.
- No independent Arrow 2 benchmark against frontier LLMs was found.

## 5. Can an LLM author the transitions, and what validation loop is needed

### Takeaway
LLMs reliably write CSS/SMIL transform, opacity and stroke-draw animations, but they are weak at non-rigid path deformation, i.e. true morphs. 2026 papers report ~12–14% failure rates for frontier models on open-domain SVG animation, plus identity drift when they rewrite whole documents. A harness should restrict the LLM to a declarative choreography over persistent element IDs and verify by rendering frames headlessly. It should not ask for free-form morph paths.

### Cited Findings
- **VAnim** (arXiv 2605.01517, 2026-05-02) reports:
  - General-purpose LLMs "mostly animate with CSS/SMIL transforms, which are limited to affine motion" and struggle with non-rigid deformation that edits `d`
  - Regenerating full SVG per frame costs ~86k tokens for 24 frames and causes object-identity drift and flicker
  - Its fix, Sparse State Updates (id, attribute, value) on a persistent DOM, cuts that to 9.2k tokens
  - [VAnim via Emergent Mind](https://www.emergentmind.com/papers/2605.01517) (secondary summary of paper)
- VAnim results on SVGAnim-Test: success rate Gemini 3 Pro 86.2%, GPT-5.2 88.5%, VAnim (fine-tuned Qwen3-VL-8B + GRPO) 100%. Blind visual-integrity scores: VAnim 4.62, Gemini 3 Pro 3.42. Dropping sparse updates for frame-by-frame generation cut success to 62.3%. SVGAnim-134k is built from professional Lottie files on Flaticon. Claude was not evaluated — [VAnim via Emergent Mind](https://www.emergentmind.com/papers/2605.01517) (secondary)
- **LiveSVG** (May 2026): "LLM-based code synthesis fails to express fine, non-rigid Bézier deformations". Its alternative is a video model plus differentiable fitting (per-group homographies + per-path control-point offsets) — [papers.cool 2605.30174](https://papers.cool/arxiv/2605.30174) (snippet)
- Practitioner: Claude added animation to SVGs unprompted or on request. Converting SVG animation to CSS animations made headless video export (Puppeteer + ffmpeg) work — [Ola Hungerford](https://www.olahungerford.com/drawing-and-animating-with-claude/) (opinion)
- Morph engines handle point-count mismatch internally: KUTE.js `svgMorph` reuses flubber-style interpolation, `svgCubicMorph` works on cubic paths, and GSAP MorphSVG is now free — [KUTE.js](https://www.GitHub.com/thednp/kute.js) (snippet); [GSAP licence](https://gsap.com/community/standard-license/) (primary)
- VectorGym and VAnim both score generation by **rendering** the output and judging frames: VLM judge, rendering-based GRPO rewards, SSIM, temporal tLPIPS — [VectorGym](https://arxiv.org/html/2603.29852v1) (primary); [VAnim](https://www.emergentmind.com/papers/2605.01517) (secondary)

### Inferences
- Lucide icon pairs often differ in **topology** (`play` = 1 polygon; `pause` = 2 rects; `menu` = 3 lines; `x` = 2 lines). Point-matched morphing needs either an engine (MorphSVG/flubber resampling, producing wobbly in-betweens) or hand-built matching paths. Line-based pairs (menu ↔ x, chevron rotate, plus ↔ x) are better done as per-element transforms, which an LLM writes reliably.
- Recommended harness contract: the LLM emits a **choreography spec**, not raw keyframes. Example: `{ from: "copy", to: "check", keep: [], exit: [{el: "rect", fx: "draw-off", ms: 120}], enter: [{el: "path#check", fx: "draw-on", delay: 80, ms: 180}] }`. The SDK compiles it to CSS. This mirrors VAnim's "sparse updates on persistent IDs" finding.
- Validation loop:
  1. **Lint** static SVGs (lucide rules, svgo, element whitelist, bounds, precision).
  2. **Render** in headless Chromium (Playwright): pause all `document.getAnimations()`, seek to 0/25/50/75/100%, screenshot at 24px and 96px.
  3. **Assert** the 0% frame pixel-matches the static `from` icon and the 100% frame matches the static `to` icon. This guarantees the static fallback.
  4. **Bounds/clip check**: no frame paints outside the 24×24 box.
  5. **Reduced motion**: emulate `prefers-reduced-motion: reduce` and assert an instant final state.
  6. **Timing**: total duration ≤ ~300ms for transient swaps; indefinite effects have a reduced-motion alternative.
  7. **Contact sheet**: a grid of the new icon or transition beside its neighbours for human review, optionally pre-scored by a VLM judge.
  8. **Human approve**, then commit.
- Steps 1–5 are deterministic and cheap; only step 7 needs a person. This catches the documented failure modes (invalid output, drift, incomplete shapes) mechanically.

### Gaps
- No benchmark measures LLMs on small UI-icon state transitions specifically. Evidence is from open-domain SVG animation, so icons are probably easier (inference).
- No Claude model appears in the animation benchmarks found (VAnim compared Gemini 3 Pro and GPT-5.2).
- No existing open-source harness implementing the render-and-assert loop for icon transitions was found.

## 6. Feasibility verdict for a 1–2 person team

### Takeaway
**Build** a thin CSS-only state-icon layer over lucide plus a small LLM harness for missing icons and transition recipes. **Adopt** lucide-animated as a reference corpus. **Skip** true path morphing, Lottie/Rive for UI icons, paid icon generators as the pipeline, and model training. The effort is realistic for 1–2 people because the hard parts (style rules, render checks) are deterministic, and the LLM only fills constrained slots.

### Cited Findings
- Apple's own system uses a small fixed effect vocabulary plus enclosure-preserving replace rather than arbitrary morphs — [WWDC25 337](https://developer.apple.com/videos/play/wwdc2025/337/) (primary); [WWDC24 10188](https://developer.apple.com/videos/play/wwdc2024/10188/) (snippet)
- lucide-animated is MIT, with an MCP server and llms.txt corpus; its Vue port is a 39-star `@vueuse/motion` project with no releases — [lucide-animated](https://lucide-animated.com/index.md) (primary); [imfenghuang/icons](https://github.com/imfenghuang/icons) (primary)
- Frontier LLMs lead text-to-SVG and editing benchmarks, and all degrade with complexity — [VectorGym](https://arxiv.org/html/2603.29852v1) (primary); [SVGenius](https://arxiv.org/html/2506.03139v1) (primary)
- LLM animation is reliable for affine/CSS motion and weak for path deformation — [VAnim](https://www.emergentmind.com/papers/2605.01517) (secondary); [LiveSVG](https://papers.cool/arxiv/2605.30174) (snippet)
- GSAP including MorphSVG is free for commercial apps under a non-OSI "No Charge" licence — [GSAP licence](https://gsap.com/community/standard-license/) (primary)
- Lordicon free-tier commercial terms conflict across its own pages; PRO API costs $149/month — [Lordicon licences](https://lordicon.com/licenses) (snippet); [Lordicon API pricing](https://lordicon.com/docs/api/pricing) (snippet)
- WCAG 2.3.3 requires a way to disable interaction motion (`prefers-reduced-motion`) — [W3C](https://www.w3.org/WAI/WCAG22/Understanding/animation-from-interactions.html) (primary)

### Inferences
- **Build (SDK, ~days)**:
  - `StateIcon` (controlled `state` prop, lucide icons per state) and `AnimatedIcon` (transient effect, `trigger`, exposed `play()`)
  - ~6–10 CSS transition recipes: crossfade-scale, rotate, draw-on/off via `pathLength`, shared-part replace, fill toggle, spin/pulse
  - a global reduced-motion snap
  - rest frame equals the static lucide icon, so SSR and fallback come free
- **Build (harness, ~1–2 weeks, inference)**:
  - a Claude-driven CLI with neighbour few-shot from lucide and the lucide-animated corpus
  - output: a static icon or a choreography spec
  - deterministic lint (lucide rules + svgo), Playwright frame render with endpoint pixel assertions and a reduced-motion check
  - a contact-sheet page for human approval
  - it lives beside the fe sdk icon package and runs on demand, not in CI
- **Adopt**: lucide (unchanged) as the static source; lucide-animated as a motion-vocabulary reference to port selectively into CSS recipes, respecting its no-redistribution-of-tutorials clause; `S6U5/lucide-svg-skill`'s rule list as a starting checklist, not a dependency.
- **Adopt only if a specific pair truly needs a morph**: GSAP MorphSVG (free, non-OSI licence; check it fits the SDK's distribution) behind a lazy import, never in the default path.
- **Skip**:
  - general path morphing (topology mismatch, LLM-weak)
  - Lottie, Rive, Lordicon and useAnimations for product UI (separate designer pipeline, runtime weight, licence ambiguity)
  - Material Symbols FILL axis (wrong set; font weight)
  - training or fine-tuning (StarVector, OmniSVG, VAnim-style RL is research-grade)
  - Recraft or Arrow as the pipeline (an occasional reference sketch only)
- **Main risks**: style drift in generated icons, caught by lint plus human review. Animation sprawl across ~35 apps, contained by a fixed recipe set and no per-icon free-form keyframes. Distraction from hover-animating everything: default trigger is state change, not hover.

### Gaps
- Effort estimates are judgement, not sourced.
- Opus 5.5's SVG quality was not measured anywhere found. A 20-icon pilot through the harness is the cheapest way to settle it.

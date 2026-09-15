# WoW 2.0 — Remotion Motion-Graphics Playbook

*Last updated: 2026-08-15*

> **Scope:** Producing motion graphics (promo videos, looping page-header animations, social shorts, data-driven video variants) with **Remotion** — React that renders to MP4 / GIF / WebM. Covers the project shape, the animation primitives, theming for dark/light, transparent-background export, and the Claude-Code verify loop.
> **Status:** Living document. Reference implementation: `workbench/ventures/10x-venture-forever-pin-promo` (ForeverPin promo + hero). Extract shared scaffolding into a template/repo once a 2nd product needs video.

---

## Why this exists

Motion graphics recur across the ecosystem — product promos, landing-page hero loops, venture content shorts. Remotion makes them **code**: deterministic, reviewable, data-driven, re-renderable. This playbook codifies the decisions so the next video starts from a known-good shape instead of a blank `create-video`.

Aligns with the SDK doctrine: the first video is the trigger; the reusable pieces (theme threading, transparent-export pipeline, render scripts) are the vector to complete once, so the next product finds them there.

---

## When to reach for it

| Need | Fit |
|---|---|
| Product promo (scenes, transitions, CTA) | scene-based composition + `TransitionSeries` |
| Page-header loop (always-on, seamless) | node-graph / looping composition, `durationInFrames === N × cycle` |
| Social short (vertical, captioned, batch) | data-driven `defaultProps` + `--props`, 1080×1920 |
| Transparent overlay over a real page bg | dark/light variants + alpha export (WebM preferred) |

Not for: one-off static images (use SVG/Figma), or live UI animation (that's CSS/Framer Motion in the app).

---

## Mental model

**Every frame is a pure function of `frame`.** No timers, no imperative tweening. Read `useCurrentFrame()`, map it to a style. Same frame in → same pixels out → renders are reproducible and any frame is directly inspectable.

Determinism rules:
- Randomness must be seeded — `random('seed')` from `remotion`, never `Math.random()`.
- No wall-clock — no `Date.now()`.
- All motion derives from `frame` + `useVideoConfig()` (`fps`, `width`, `height`, `durationInFrames`).

---

## Core primitives

| Primitive | From | Drives |
|---|---|---|
| `useCurrentFrame()` | `remotion` | the clock for everything |
| `interpolate(f,[in],[out],{extrapolate…:'clamp'})` | `remotion` | fades, slides, any frame→value map; `clamp` stops overshoot |
| `spring({frame,fps,config})` | `remotion` | natural pop/ease — `damping`+`stiffness` set the feel |
| `random('seed')` | `remotion` | deterministic noise (e.g. procedural QR cells) |
| `Sequence` / `Series` | `remotion` | time-shift / stagger; rebases child `frame` to 0 |
| `TransitionSeries` + `fade`/`slide`/`wipe` | `@remotion/transitions` | scene-to-scene; total = Σ sequences − Σ transitions |
| `linearTiming` / `springTiming` | `@remotion/transitions` | transition curves |
| `AbsoluteFill` | `remotion` | full-frame layout layer |
| bezier packet | hand-rolled | a dot at `bez(curve, t)` travelling a wire (node-graph flows) |

**Depth = more primitives composed, not more prose.** A "packet travelling a curved wire" is just `interpolate` on `t` feeding a cubic-bezier point function.

---

## Project shape

```
src/
  index.ts            registerRoot(RemotionRoot)
  Root.tsx            <Composition> registry — one per renderable (id, fps, size, duration, defaultProps)
  theme.ts            colors + font (the base palette)
  components/         reusable, composition-agnostic (Background, QrCode, Counter, …)
  scenes/             one file per scene (scene-based comps)
  <feature>/          a self-contained composition + its parts (e.g. hero/: flow.ts, Wire, Packet, nodes…)
```

Conventions:
- **`Root.tsx` is the registry** — register each renderable variant as its own `<Composition>` so it renders by id with no `--props` juggling.
- **`flow.ts` / geometry module** — put node coords, bezier helpers, per-cycle timing math in one non-component file both wires and nodes import, so they can't disagree.
- **Derive `durationInFrames`** from named scene/cycle constants; never hardcode a total that can drift.
- **Seamless loop** ⇔ `durationInFrames === cycle × count` (frame `DURATION` ≡ frame `0`).

---

## Two archetypes (reference impl)

### 1. Scene-based promo — `ForeverPinPromo`
Vertical 1080×1920. `TransitionSeries` of scenes (title → routing → never-expire → stats/CTA). Each scene animates from local frame 0. Motion: `spring` pop-ins, `interpolate`+`clamp` fades/slides, a spring-eased `Counter`, procedural QR reveal with a diagonal `spring` stagger.

### 2. Looping node-graph hero — `ForeverPinHero`
Landscape 1920×1080, seamless 7s loop. n8n/Zapier style: requester nodes → central hub → rules engine → destination nodes, wired with curved beziers. Per cycle a **request packet** travels a wire (`bez(curve, t)`), the hub pulses, the matched rule lights, a packet flows out to the destination which pops a badge. Idle wires carry a slow `strokeDashoffset` flow so the graph feels alive between events.

---

## Dark / light theming

Goal: one component tree renders both variants. **Do not** hardcode colors in components or duplicate the tree.

Pattern (see `hero/palette.ts`):
1. Define a `Palette` type + a `palettes` record (`dark`, `light`). Light uses **deeper accents** + dark ink for contrast on white.
2. Thread the active palette as a `t: Palette` prop through every node/part. (Prop-threading is explicit and deterministic; a React context works too but is more magic.)
3. Store per-item accent as a **key** (`colorKey: 'green'|'cyan'|…`), resolve `t[colorKey]` at render — so accents follow the variant.
4. Shared style helpers (`cardStyle(active, color, t)`) take `t`, never import a singleton theme for color.
5. Expose `variant` as a composition prop; register `…Dark` / `…Light` compositions in `Root.tsx` with fixed `defaultProps`.

---

## Transparent background — the pipeline

**Toggle:** a `transparent: boolean` composition prop that omits the `<Background>` element. Remotion emits an **alpha channel** for uncovered area automatically when rendered with `--image-format=png`.

### GIF caveat — 1-bit alpha
GIF transparency is a **single fully-transparent palette index** (`alpha_threshold`), not partial alpha. Soft glows, `box-shadow`, `backdrop-filter: blur`, and anti-aliased edges **can't blend** → they harden or fringe against transparency.

**Rules for a clean transparent build:**
- Make card backgrounds **opaque** (`palette.card`), not `rgba(…,0.7)`.
- **Drop `backdropFilter: blur`** — meaningless over transparency, causes artifacts.
- Keep wires / strokes / QR modules solid (alpha 1) → they composite crisply.
- Accept that big glows harden; keep them modest, or gate them by `transparent`.

### Format matrix

| Format | Codec | Alpha | Size (1080p/7s) | Use |
|---|---|---|---|---|
| **WebM** | `vp9` (`--pixel-format=yuva420p`) | **true** | **~0.9 MB** | **preferred for web** — `<video autoplay loop muted playsinline>` |
| GIF (½-scale) | `gif` `--scale=0.5` | 1-bit | ~3.4 MB | universal `<img>` embed |
| GIF (full) | `gif` | 1-bit | ~8.5 MB | fallback only — heavy |
| MP4 | `h264` | none | ~1.5 MB | solid-bg promo |

APNG / animated WebP are the middle ground (true alpha, `<img>`-embeddable, smaller than GIF) if `<video>` isn't an option.

### Commands

```bash
# transparent, per-variant composition ids
remotion render ForeverPinHeroDark  out/hero-dark.webm  --codec=vp9 --image-format=png --pixel-format=yuva420p
remotion render ForeverPinHeroDark  out/hero-dark.gif   --codec=gif --image-format=png --every-nth-frame=2            # 15fps
remotion render ForeverPinHeroLight out/hero-light.gif  --codec=gif --image-format=png --every-nth-frame=2 --scale=0.5 # 960×540
```

`--every-nth-frame=2` halves GIF fps (smaller); `--scale=0.5` halves dimensions (~¼ size). Wrap the common ones as `npm` scripts (`gif`, `gif:web`, `webm`).

---

## Data-driven variants

For batch output (captioned shorts, per-campaign promos) add a `defaultProps` object (optionally a Zod `schema` for the Studio editor) to the `<Composition>`, read it as component props, and render with `--props='{...}'`. One composition → N videos from a JSON list.

---

## Verify loop in Claude Code

Remotion isn't a Vite app — the browser-preview tools don't drive it. Verify via the CLI render + image read:

1. **Still** — `remotion still <Comp> out/f.png --frame=N` → `Read` the PNG. Catches build errors + shows the frame. Cheap; do this per scene/phase.
2. **Transparency** — render with `--image-format=png`; confirm alpha with `sips -g hasAlpha out/f.png`.
3. **On-background proof** — composite the transparent still over the target matte (PIL: `Image.alpha_composite`) and `Read` it — proves the variant reads on its real page bg and that the surround is genuinely transparent.
4. **Full render** — `remotion render` the MP4/loop to confirm transitions/flow over time (stills can't show transitions).

No `Math.random()` / `Date.now()` in scripts — they break determinism (and Remotion's own workflow tooling forbids them).

---

## Gotchas

- All `remotion` + `@remotion/*` packages must share **one version** — `remotion upgrade` enforces it.
- First render fetches a headless Chromium (~90 MB) once, then caches the bundle.
- `TransitionSeries` total length = Σ sequence frames − Σ transition frames — off-by-this makes the comp end early/late.
- A `<Background>` outside the `TransitionSeries` spans the whole comp (continuous), and slide/wipe transitions parallax over it — put persistent layers there deliberately.
- Node text wrapping: fixed-width cards + `whiteSpace: nowrap`, or the label re-flows per variant.

---

## Reference implementation — file map

`workbench/ventures/10x-venture-forever-pin-promo/`

| Path | What |
|---|---|
| `src/Root.tsx` | registers `ForeverPinPromo`, `ForeverPinHero`, `ForeverPinHero{Dark,Light}` |
| `src/theme.ts` | base palette + font |
| `src/components/QrCode.tsx` | procedural animated QR (themeable via `moduleColor`/`plate`/`frameStroke`) |
| `src/scenes/*` | promo scenes |
| `src/hero/flow.ts` | geometry, bezier helpers, cycle timing |
| `src/hero/palette.ts` | dark/light `Palette` + `palettes` |
| `src/hero/{Wire,Packet}.tsx` | connector + travelling request |
| `src/hero/{UserNode,SiteNode,RulesNode,QrHub}.tsx` | graph nodes |
| `src/hero/ForeverPinHero.tsx` | `{variant, transparent}` composition |
| `README.md` | run commands + per-composition detail |

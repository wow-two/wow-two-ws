# nth26 map & tiles → SDK map vector

*Last updated: 2026-08-10*

> **Status:** analysis, nothing built. Subject = `ventures.nth26` frontend
> (`ventures/ventures.nth26/engineering/codebase/nth26.frontend-services`), specifically whether its MapLibre +
> PMTiles layer can become an SDK vector. Every figure measured off the working tree on **2026-08-10**.
>
> Verdict up front: **yes, ~2,500 LOC of it is genuinely generic** — and the map is the *easiest* part of
> nth26 to move to Vue, not the hardest.
>
> Spun out of [frontend-sdk-vue-port-analysis.md](frontend-sdk-vue-port-analysis.md). Valid independently of
> any Vue decision.

---

## 1 · nth26 shape

pnpm workspace: `apps/studio` · `apps/showcase` · `packages/shared`.

| Area | files | LOC | React |
|---|---:|---:|---|
| `apps/studio` | 254 | **20,169** | 58% React-free |
| `apps/showcase` | 13 | 2,110 | — |
| `packages/shared` | 5 | 457 | — |

`apps/studio/src` by layer:

| Layer | files | LOC | React files |
|---|---:|---:|---:|
| `domain/` | 147 | 4,040 | **0** |
| `application/` | 34 | 4,958 | 9 |
| `presentation/` | 55 | 10,658 | most |
| `integration/` | 14 | 427 | — |
| `bootstrap/` | 3 | 57 | — |

- **11,724 LOC (58%) has no React import.**
- `domain/` runs 10 slices, each `constants/ enums/ models/` — the Clean-Arch split already does the work a
  framework port needs.
- `application/` heavyweights: `network` 1,929 · `street` 1,581 · `console` 411 · `walkgraph` 312.
- Deps: `maplibre-gl ^5.0.0` · `pmtiles ^4.4.1` · `@nth26/shared` · `@tabler/icons-react` ·
  `react-router-dom ^7.18.2` · `@wow-two-beta/ui 0.0.104` (5 files, 9 symbols).

---

## 2 · The map surface — 15 files, 6,914 LOC

| File | LOC | Nature |
|---|---:|---|
| `console/map/routeDelayLayers.ts` | 1,183 | transport domain |
| `console/map/paint.ts` | 908 | **generic layer compiler** |
| `console/map/outcomePaint.ts` | 574 | transport domain |
| `console/map/icons.ts` | 318 | generic SDF baking |
| `console/map/ConsoleMap.tsx` | 253 | orchestration, mixed |
| `common/components/MapControls.tsx` | 209 | generic |
| `console/tools/Marquee.tsx` | 204 | generic box-select |
| `console/tools/MeasureTool.tsx` | 192 | generic |
| `packages/shared/src/map/index.ts` | 169 | generic, env-coupled |
| `common/components/NetworkLayer.tsx` | 168 | transport domain |
| `common/components/PositionLayer.tsx` | 151 | generic |
| `common/components/MapView.tsx` | 133 | generic canvas lifecycle |
| `console/tools/ZoomWindow.tsx` | 76 | generic |
| `console/screens/ConsolePage.tsx` | 2,258 | app screen |
| `rider/screens/RiderPage.tsx` | 118 | app screen |

**Split: ~2,511 LOC generic · ~2,178 LOC domain-locked · 2,376 LOC app screens.**

Generic set: `shared/map` 169 + `paint.ts` ~900 + `icons.ts` 318 + tools 472 + `MapControls` 209 +
`PositionLayer` 151 + `MapView` 133 + geo hooks 159.

---

## 3 · The extractable kernel — `LayerSpec` → `buildLayers`

`domain/layers/models/LayerSpec.ts` declares a layer once; `console/map/paint.ts` compiles it into MapLibre
layers. This is the piece worth owning in the SDK.

```
LayerSpec {
  id · title · group · geometry · featureCount
  delivery { kind, url }
  render    { minzoom, maxzoom }     // inclusive floor, exclusive ceiling
  aggregate { mode, below? }         // what happens below render.minzoom
  glyph?    { above }                // dot → drawn glyph threshold
  interactive · colour · join? · provenance
}
```

- **Three-rung zoom ladder** — counts below `aggregate.below`, plain circle up to `glyph.above`, glyph above
  it. One rule, twenty layers. Written per-layer it would be twenty copies of one `if`.
- `paint.ts` also emits pick + glow layers (`pickLayerId`, `glowLayerId`, `pickFilter`), `rampExpression`,
  `sourceOptions` (clustering), `markBand`, `beforeIdFor` layer ordering, `queryLayerIds`.
- `icons.ts` — `bakeSdfIcon` / `registerIcons`: SVG → SDF sprite at runtime. Fully generic.
- Only `LayerId` and `LayerGroup` enums are nth26-specific → become type parameters.
- The manifest itself (`domain/layers/constants/layerManifest.ts`) stays in nth26.

Domain-locked, stays put: `routeDelayLayers.ts` (1,183), `outcomePaint.ts` (574), `NetworkLayer.tsx` (168 —
bus/metro feeds), all panels, `ConsolePage.tsx`.

---

## 4 · Why the map is the *easiest* part to move to Vue

- **No `react-map-gl`.** MapLibre is used imperatively — `createMap(container)` returns a `Map` object.
  React owns mount/unmount and prop→imperative bridging only.
- Actual React-coupled map code ≈ **1,400 LOC of effect wrappers**.
- `PositionLayer` builds its marker with `document.createElement` — already framework-neutral, 151 LOC.
- `paint.ts` · `icons.ts` · `outcomePaint.ts` · `routeDelayLayers.ts` · all of `domain/` — zero React,
  copy verbatim.
- `MapView.tsx` 133 LOC → `onMounted` / `onUnmounted` + `useTemplateRef`. Near-mechanical.
- Had nth26 used a declarative React map wrapper, every layer would be a component and Vue would mean a
  full rewrite. It didn't.

The hard-won bits are **DOM facts, not React facts**, and survive the port intact:

- `ResizeObserver` + a `requestAnimationFrame` backstop, because a flex child's final size lands after the
  map is constructed — stale, MapLibre keeps its initial viewport guess and `project()` returns off-screen
  coordinates. Looks like a data problem; isn't.
- `position:absolute; inset:0` instead of `height:100%` — a percentage height inside a flex child doesn't
  resolve, collapsing the box to zero; MapLibre then draws into a 400×300 corner.
- Lifting the loading veil on `styledata` rather than `load`/`idle`, which both wait for every tile.

---

## 5 · Blockers before extraction

- `packages/shared/src/map/index.ts` reads `import.meta.env.VITE_TILES_URL` / `VITE_STYLE_URL` at **module
  scope** → must become constructor options.
- `TASHKENT_CENTRE` / `TASHKENT_BOUNDS` hardcoded → options.
- `basemapStyle()` hardcodes hex colours per theme, because a MapLibre style is JSON handed to WebGL and
  cannot read CSS custom properties. **Integration point:** the SDK's OKLCH engine in `foundation/themes`
  could emit the style object per theme. Real vector, not a workaround.
- ⚑ **`foundation/geolocation` overlap.** The SDK already ships 844 LOC: `distanceBetween` (haversine),
  `getCurrentPosition`, `watchPosition`, `useGeolocation`, `useWatchPosition`, typed permission states.
  nth26's local `useGeolocation` (64 LOC) and `distanceMetres` duplicate it. Reconcile before extracting.
- `useHeading` (95 LOC, `deviceorientation`) has no SDK equivalent — new vector.
- `metresPerPixel` (`application/measurement`) — generic geo math, no SDK home yet.
- **Packaging:** `maplibre-gl` is heavy. Ship as a companion package `@wow-two-beta/ui-map` with
  `maplibre-gl` + `pmtiles` as optional peers — mirrors the backend's `Testing.Data` companion pattern, and
  keeps core `ui` unaffected.
- **One consumer.** Per `conventions/development/dev-cycle.md` § *Vector completeness*, a product's need is
  the trigger, not the scope — but a single consumer is thin evidence for the generic shape. Decide whether
  `LayerSpec` goes generic on day one or gets generalized at the second consumer.

---

## 6 · nth26's real SDK gap isn't the map

`console/primitives/` hand-rolls 322 LOC that the SDK already ships:

| Local | LOC | Shipped SDK equivalent |
|---|---:|---|
| `Disclosure.tsx` | 34 | `display/accordion`, `display/collapsible` |
| `Tooltip.tsx` | 35 | `display/tooltip` |
| `HoverPopover.tsx` | 41 | `overlays/hoverCard`, `overlays/popover` |
| `Section.tsx` | 58 | `layout/section`, `display/sectionHeader` |
| `Row.tsx` | 43 | `display/infoRow` |
| `InfoHint.tsx` · `Note.tsx` · `KindIcon.tsx` | 111 | partial |

Generic app-shell pieces nth26 built that the SDK **doesn't** ship — candidates flowing the other way:

- `console/controls/NavControls.tsx` 260 · `ScenarioRail.tsx` 241 · `ToolBar.tsx` 152 · `Legend.tsx` 84
- `console/docks/DockTab.tsx` 73 + `useDock.ts` 91 — dockable panel system

nth26 pins current `0.0.104` and still imports only 9 symbols. The adoption gap is UI chrome, not geospatial.

---

## 7 · Sequence

1. **Close the chrome gap first** — replace the 322 LOC of local primitives with shipped SDK components.
   Cheap, proves the pin, no new package.
2. **Reconcile `foundation/geolocation`** — drop nth26's local `useGeolocation` + `distanceMetres`.
3. **Extract the map vector** *after* the forever-pin Vue pilot resolves — target framework should be decided,
   not guessed.
4. Ship as `@wow-two-beta/ui-map` companion: `createMap` · `MapView` · `LayerSpec<TId,TGroup>` +
   `buildLayers` · `bakeSdfIcon` · `PositionLayer` · `MapControls` · `Marquee` / `MeasureTool` / `ZoomWindow`.
5. **Theme bridge** — `foundation/themes` emits the MapLibre style object, replacing hardcoded hex.

### Open questions

- `LayerSpec` generic on day one, or extract nth26's exact shape and generalize at consumer #2?
- Does the dock/toolbar/legend set belong in `ui` core or in `ui-map`?
- Second consumer for the map vector — is there one, or does this stay a one-app library?

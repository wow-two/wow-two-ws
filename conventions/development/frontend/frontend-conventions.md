# Conventions — Development — Frontend

*Last updated: 2026-09-10*

> Conventions for every frontend under `wow-two-ws/`. Lookup table — open a file when the task
> touches it; do not pre-read. The tree splits twice, and the cuts are orthogonal.
> How to write a doc here → template + rules in [conventions](../../conventions.md).

## The two cuts [REQUIRED]

| Cut | Answers | Folder |
|---|---|---|
| scope | how far a rule reaches — one symbol, one app, between frontends | [core/](core/core.md) |
| shape | what is being built — a product app, a component library | [shapes/](shapes/shapes.md) |

- rule ownership → [the shape test](shapes/shapes.md#the-test), based on the subject rather than different wording.
- must name only the **folder** in a construct or component doc — `overlays/`, `pages/` — and leave which tree
  holds it to the shape.

---

## The scopes and the shapes

The scope model — what `lla` · `mla` · `hla` each own, and how to route a rule between them — lives in
[core](core/core.md). The deliverable model — the two shapes, the test, the vectors inside one — lives in
[shapes](shapes/shapes.md). Read them there; this index does not restate either.

**Routing.** A kind you declare → `core/mla/constructs/{kind}.md`; which one to reach for, and with what values
→ `core/mla/components/`. A language form used end to end → `core/lla/components/{form}.md`; how any symbol is
written → `core/lla/notation/`. A concrete technology or capability → `core/mla/domains/{domain}/`; a framework's
own constructs → `core/lla/constructs/{framework}/`. A rule spanning frontends we both own → `core/hla/`.
Where a folder is created, how the thing builds, routes, styles and ships → `shapes/{app,library}/`.

---

## The layers of a thing [REQUIRED]

The model is [development conventions](../development-conventions.md) § *The layers of a thing*.
What it means here:

| Layer | Home | Example |
|---|---|---|
| 1 · baseline | [lla/constructs](core/lla/constructs/constructs.md) | `type` · `const` · `<button>` · `@theme` |
| 2 · construct | [mla/constructs](core/mla/constructs/constructs.md) | what a `Page` or a `Model` **is** |
| 3 · application | `lla/components` · `mla/components` · `mla/domains` | how it is applied, by who owns the form |

- must not document a third-party library's own surface → [development conventions](../development-conventions.md)
  § *Whose thing earns a doc*. Naming `tailwind-variants` in a rule of ours is the allowed case; documenting
  TanStack Query is not.
- must place a rule at the lowest layer that can hold it — a rule about a `const` object is layer 1, a rule
  about our enum value sets is layers 1 and 3.

### Reading the map

A thing occupies one home per layer it has. Two tests, applied in order:

1. **Does TypeScript, the browser or a framework ship the form?** → it has a `lla/constructs` row.
2. **Do we define a thing of our own on top of it?** → it earns a `mla/constructs` doc, and its conditions land
   in `lla/components` when the language supplied the form, `mla/components` when we coined the thing, and
   `mla/domains` when it needs collaborators.

| Thing | Layer 1 — the platform form | Layer 2 — what ours **is** | Layer 3 — every condition |
|---|---|---|---|
| `Constants` | `const` · `as const` | the language's own | [constants](core/lla/components/constants.md) |
| `Enums` | `const` object · union | the language's own | [enums](core/lla/components/enums.md) |
| `Extensions` | `const` object of statics | the language's own | [extensions](core/lla/components/extensions.md) |
| `Page` · `Overlay` | — | the 16 kinds that render | [components](core/mla/components/components.md) |
| `Model` · `Dto` | `interface` · `type` | the layer a type may cross | [data](core/mla/constructs/data/data.md) |
| `Result` | discriminated union | the carrier every call returns | [result](core/mla/constructs/data/result.md) |
| a hook | `useState` · `useEffect` | the `use*` state it owns | [behavior](core/mla/constructs/behavior/behavior.md) |
| a route | — | a place, a guard, metadata | [routing](shapes/app/routing/routing.md) |

- must not read a missing `lla` row as a missing layer — `Page`, `Overlay` and `Result` are roles we coined, so
  they start at layer 2.
- must not read a missing `components` doc as a gap — a thing needing collaborators has its layer 3 in the
  domain that supplies them.
- must keep a variation out of `mla/constructs` — a responsive presentation is an application of `Overlay`, so
  it lives wherever that kind's layer 3 lives.

---

## Layer direction [REQUIRED]

Rules flow `lla` → `mla` → `hla`. A higher layer may **override or extend** a lower one; a lower layer never
reaches up. A shape overrides neither — it answers a question `core/` never asks.

- must state an override in the higher layer's own file, never by editing the lower layer's rule.
- must carry a **backlink** from the higher layer to the exact lower-layer rule it overrides or extends —
  `{file}` § *Section*, the way a kind doc cites [notation](core/lla/notation/notation.md).
- must cite the lower layer rather than restate it when the higher layer adds nothing.
- must resolve a conflict in favour of the higher layer, and say so at the point of override.

---

## Files

### `core/lla/` — one symbol

The lead is [lla](core/lla/lla.md) — the three buckets and the boundary.

- [constructs/](core/lla/constructs/constructs.md) — one folder per platform, each construct and its ban:
  [typescript](core/lla/constructs/typescript/typescript.md) · [html](core/lla/constructs/html/html.md) ·
  [css](core/lla/constructs/css/css.md) · [tailwind](core/lla/constructs/tailwind/tailwind.md).
- [components/](core/lla/components/components.md) — a language form end to end:
  [constants](core/lla/components/constants.md) · [enums](core/lla/components/enums.md) ·
  [extensions](core/lla/components/extensions.md).
- [notation/](core/lla/notation/notation.md) — [naming](core/lla/notation/naming/naming.md) ·
  [props](core/lla/notation/naming/props.md) ·
  [documentation](core/lla/notation/documentation/documentation.md) ·
  [style](core/lla/notation/style/style.md) · [imports](core/lla/notation/style/imports.md).

### `core/mla/` — one app

The lead is [mla](core/mla/mla.md) — the three buckets, SDK boundary and the shape of each register's documents.

| File | What it covers |
|---|---|
| [constructs](core/mla/constructs/constructs.md) | The authoring pass: kind → name → docs → props → gate |
| [visual](core/mla/constructs/visual/visual.md) | The 16 kinds that render, suffix routing, where a group is placed |
| [behavior](core/mla/constructs/behavior/behavior.md) | The seams a component consumes, and the `use*` state it owns |
| [data](core/mla/constructs/data/data.md) | The `*Dto` family, `*Model`, `*Content`, and the `Result` carrier |
| [compound](core/mla/constructs/compound/compound.md) | A root that owns named subparts, and how both halves export |
| [components](core/mla/components/components.md) | The three registers, the gate, and one folder per visual group |

### `core/mla/domains/` — a capability, its contract and its providers

One row per domain → [domains](core/mla/domains/domains.md). The four with the most surface:
[data](core/mla/domains/data/state-and-data.md) (the `/api` client, `Result`, server vs UI state) ·
[forms](core/mla/domains/forms/forms.md) (engine pin, values, schema, field chrome) ·
[submission](core/mla/domains/forms/submission.md) (submit path, field errors, validation timing) ·
[api](core/mla/domains/api/type-mapping.md) (the .NET ↔ wire ↔ TS scalar contract).

### `core/lla/constructs/{react,vue}/` — each framework's own constructs

- [react](core/lla/constructs/react/react.md) — [components](core/lla/constructs/react/components.md) ·
  [hooks](core/lla/constructs/react/hooks.md) · [jsx](core/lla/constructs/react/jsx.md) ·
  [boundaries](core/lla/constructs/react/boundaries.md).
- [vue](core/lla/constructs/vue/vue.md) — [SFC](core/lla/constructs/vue/vue-sfc.md) ·
  [composition](core/lla/constructs/vue/composition.md) · [macros](core/lla/constructs/vue/macros.md) ·
  [reactivity](core/lla/constructs/vue/reactivity.md) · [template](core/lla/constructs/vue/template.md) ·
  [builtins](core/lla/constructs/vue/builtins.md).

### `core/hla/` — between our own frontends

[hla](core/hla/hla.md) — named ahead of its contents; empty until a second frontend exists.

### `shapes/app/` — a product frontend

The lead is [app](shapes/app/app.md) — its vectors and their status.

| File | What it covers |
|---|---|
| [architecture](shapes/app/architecture/architecture.md) | Five layers × domain slices, the slice tree |
| [boundaries](shapes/app/architecture/boundaries.md) | In-app restraint, the SDK-extraction trigger, packaging |
| [platform](shapes/app/platform/platform.md) | The vector lead over the styling and dev-server wiring |
| [styling](shapes/app/platform/styling.md) | The `index.css` entry, `@source` depth, brand tokens, dark mode |
| [dev-server](shapes/app/platform/dev-server.md) | HTTPS through mkcert, the `/api` proxy, previewing a route |
| [routing](shapes/app/routing/routing.md) | `createAppRouter`, the `AppRoute` model, places vs actions |

### `shapes/library/` — a package another frontend imports

[library](shapes/library/library.md) — kind-grouped layout and capability modules.

- [delivery](shapes/library/delivery/delivery.md) — exports, declarations, CSS, peers and release verification.
- [compatibility](shapes/library/platform/compatibility.md) — runtimes, browser features, SSR and polyfills.
- [testing](shapes/library/testing/testing.md) — unit, DOM, browser and packed-consumer evidence.

---

## Verification and platform owners

- interaction semantics → [HTML interaction](core/lla/constructs/html/interactive.md#interaction).
- visual and assistive checks → [accessibility](core/lla/constructs/tailwind/accessibility.md#verification).
- app assets → [assets](shapes/app/platform/assets.md).
- app artifacts and build inputs → [delivery](shapes/app/delivery/delivery.md).
- each sweep row must name its representative check; a lint pass alone does not prove behavioral conformance.

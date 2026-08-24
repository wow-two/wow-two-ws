# CSS

*Last updated: 2026-08-20*

> What raw CSS is still allowed to do in a Tailwind-only codebase, and the features banned outright.
> Purpose — Tailwind owns declarations; CSS keeps only the four jobs a utility cannot do.
> Use case — reach here before adding anything to a stylesheet, and whenever a `.css` file grows a rule.

## The groups

| Group | Covers | Doc |
|---|---|---|
| custom properties | `--*` declaration, scope, theming, runtime override | [custom properties](custom-properties.md) |
| at-rules | `@import` · `@media` · `@keyframes` · `@supports` · `@layer` | [at-rules](at-rules.md) |
| selectors | element · class · pseudo-class · combinator · specificity | [selectors](selectors.md) |
| values | `var()` · `calc()` · `color-mix()` · gradients · units | [values](values.md) |

---

## The four jobs

- must keep CSS to these four, and must express everything else as a utility ([tailwind](../tailwind/tailwind.md)):
  - **tokens** — the `@theme` block and the `.dark` override that re-points it.
  - **keyframes** — an animation body, since `@keyframes` has no utility form.
  - **authored-content scope** — a `.prose` block styling HTML the author wrote, not the component.
  - **global reset** — `html` / `body` defaults, and the reduced-motion safety net.
- must place every stylesheet in `bootstrap/`; a `.css` file next to a component is a lane violation
  ([architecture](../../../../shapes/app/architecture/architecture.md)).
- must keep the wiring order as [styling](../../../../shapes/app/platform/styling.md) states it, never
  restating it here.

---

## Banned

- **CSS Modules · styled-components · Sass · a per-component `.css`** — reach for utilities; a second source of
  appearance disagrees with the first silently ([styling](../../../../shapes/app/platform/styling.md)).
- **`<style>` in a Vue SFC, scoped or not** — reach for utilities; 406 SFCs carry none today.
- **`!important`** — reach for a more specific utility or `cn()` ordering; the reason and the one exception are
  [selectors](selectors.md)' ([selectors](selectors.md) § *The selectors*).
- **`@import` of a remote stylesheet** — reach for a bundled dependency; it blocks first paint and defeats the CSP.

---

## Neighbours

- [tailwind](../tailwind/tailwind.md) — the layer that owns the declarations
- [html](../html/html.md) — what these rules select

# Theme patterns

*Last updated: 2026-10-20*

> The named visual patterns a product theme follows: how each looks, which fe sdk pieces build it, when to pick it.
> A product's own colours stay in its design spec ([per-app specs](../design-conventions.md#per-app-specs)).

## Patterns

| Pattern | Look | Reference |
|---|---|---|
| **Ambient glass** | glassmorphism: blurred translucent surfaces over a gradient backdrop | Wheelhouse, `platform` |
| **Solid** | opaque surfaces on a flat background | the fe sdk default theme |

- must name a product's pattern in its design spec, beside its token tables.
- must pick one pattern per product; the marketing pages and the app share it.
- should pick ambient glass for a product with few dense tables and a brand colour worth showing.
- should pick solid for a dense data tool, a print-first surface or a theme without a usable brand hue.

---

## Theme

- must take the colour tokens as [styling](../../development/frontend/shapes/app/platform/styling.md) § *Brand tokens*
  states: the library theme, a registry theme (`theme-{id}` from `@wow-two-beta/fe/themes.css`) or the app's `@theme`.
- must define an ambient glass backdrop as `--theme-ambient`, light and dark: a registry theme's `ambient`, or the
  app's stylesheet beside its brand tokens.
- must keep every text pair AA on the opaque fallback surface and on the glass over the brightest glow.

---

## Backdrop

- must paint the backdrop with `surface-ambient` on the frame root, never a hand-written page gradient.
- must build the ambient from two or three still radial glows: the brand hue and one accent hue.
- must keep the glows faint — about 6–10% alpha in light, 10–20% in dark, as `platform` does.
- must keep the backdrop still: no animation, fixed to the viewport.

---

## Surfaces

- must make the outer chrome glass: `AppShellHeader` / `Navbar` `variant="glass"`, menus and the bottom bar.
- may make panels glass with `Card` `variant="glass"`; content inside a panel stays opaque.
- must stack one glass layer per surface; never glass on glass.
- must give each glass surface a hairline edge, a one-pixel inner highlight and a soft shadow.
- must fall back to the opaque card colour without `backdrop-filter` and under `prefers-reduced-transparency`.
- must keep inputs, tables and long text on opaque fills.

---

## Neighbours

- [styling](../../development/frontend/shapes/app/platform/styling.md) — the stylesheet entry, brand tokens, colour mode
- [effects](../../development/frontend/core/lla/constructs/tailwind/effects.md) — shadows, blur and surface treatments
- [design exploration](../research/design-exploration.md) — how a product picks its colours

# Icons

*Last updated: 2026-09-10*

> The icon component contract an app satisfies, and the wrapper that gives every glyph its accessibility posture.
> Purpose — one wrapper decides decorative versus semantic, so no call site hand-wires the hidden state.
> Use case — passing an icon into a component, shipping a bespoke glyph, or sizing one.

## The contract

- must accept any component whose props satisfy the adapter shape — a numeric size plus SVG attributes.
- must use a numeric adapter size; adapt a vendor with a different prop contract at its boundary.
- must express a CSS-unit size on the class, never on the size prop.
- must render decorative by default — with no label the glyph is hidden from assistive technology.
- must flip to an image role exactly when a label is passed.
- must let a caller-supplied attribute win over the wrapper's own binding.
- must take an icon as a component, never as a name the seam resolves from a registry.
- must leave the icon set to the app — the contract names none.
- must keep a built-in set module-private where one exists; it is not part of the surface.

---

## Providers

| Provider | Implements | Reach for it when |
|---|---|---|
| SVG component adapter | the declared numeric-size and SVG attribute contract | an app-selected icon set |
| a custom component | the adapter shape, hand-written over an SVG | a brand mark, or a glyph the set lacks |
| the spinner | a fixed spinning glyph sized by class | a busy indicator, which is not an app-chosen icon |

---

- must verify an unlabeled glyph is hidden and an explicitly labeled glyph is exposed as an image.
- must reject a CSS-unit string at the numeric size boundary; express CSS sizing through a class.

---

## Neighbours

- [domains](../domains.md) — the shape every domain follows
- [display](../../constructs/visual/display.md) — the kind a glyph belongs to
- [visual kinds](../../constructs/visual/visual.md) — the controls that take an icon prop
- [styling](../../../../shapes/app/platform/styling.md) — where a class-driven size is decided

---

## Framework binding

- must adapt framework-specific component types at the provider boundary.
- must preserve accessible names and hidden state when forwarding attributes.
- must not let a decorative default hide an explicitly named semantic glyph.

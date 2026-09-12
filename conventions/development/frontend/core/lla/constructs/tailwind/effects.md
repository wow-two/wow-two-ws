# Effects

*Last updated: 2026-09-10*

> Every shadow, opacity and blend utility, and the ones that make an element invisible without removing it.
> Purpose — elevation and opacity are the two cheapest ways to say "this is above" and "this is unavailable".
> Use case — reach here before raising a surface, dimming a control or blending two layers.

## The utilities

| Utility | Applies | Verdict |
|---|---|---|
| `shadow-sm` · `shadow` · `shadow-md` · `shadow-lg` · `shadow-xl` | the elevation scale | `use` |
| `shadow-2xl` | the top of the scale, for a lifted overlay | `use with care` |
| `shadow-none` | elevation removed, usually by a `flat` variant | `use` |
| `shadow-{token}/{alpha}` | a tinted shadow — `shadow-primary/10` | `use with care` |
| `inset-shadow-*` · `inset-ring-*` | an inner bevel or edge | `use with care` |
| `opacity-0` … `opacity-100` | the opacity scale | `use` |
| `opacity-50` on a disabled control | the disabled look, paired with the real attribute | `use` |
| `opacity-0` as the closed half of a transition | a fade, with the unmount deferred | `use` |
| `opacity-0` used as hiding | an element invisible, focusable and still clickable | `banned` |
| `mix-blend-*` | a box blended into what is painted behind it | `use with care` |
| `bg-blend-*` | a background image blended with its background colour | `use with care` |
| `mask-*` | a box clipped by an image or a gradient | `use with care` |
| `text-shadow-*` | a shadow behind text | `use with care` |
| an arbitrary shadow — `shadow-[inset_0_-1px_…]` | an inset hairline the scale lacks | `use with care` |
| a shadow used as a border | an edge with no colour token behind it | `use with care` |
| a shadow-only focus indicator | focus disappears in forced colors | `banned` |
| `opacity-*` on a text run to lower its contrast | contrast dropped below the tuned ratio | `banned` |

- must take elevation from the scale, and let a higher tier mean a higher stacking tier too ([z-index](z-index.md)).
- must use the [focus recipe](border.md); Tailwind rings are box shadows and need its outline fallback.
- must lower a text's emphasis with `text-muted-foreground`, not with opacity ([color](color.md)).
- must reach for the ambient surface treatments already defined rather than a new gradient
  ([values](../css/values.md)).

---

## Banned

- **`opacity-0` used as hiding** — reach for `hidden`; a transparent element still takes focus, still receives the
  click, and still covers whatever sits behind it.
- **a shadow-only focus indicator** — use the [outline-and-ring recipe](border.md).
- **`opacity-*` lowering text contrast** — reach for `text-muted-foreground` or `text-subtle-foreground`
  ([color](color.md)); the token contrasts were measured at full opacity, so dimming lands below AA and the theme
  audit cannot see it.

```vue
<!-- ✅ elevation from the scale, disabled says so, muted text uses its own token -->
<div class="rounded-lg bg-card shadow-md">
  <button type="button" disabled class="opacity-50">Save</button>
  <p class="text-xs text-muted-foreground">Nothing to save yet</p>
</div>

<!-- ❌ dimmed text drops below AA, and the "hidden" panel is still clickable -->
<p class="text-xs text-foreground opacity-50">Nothing to save yet</p>
<div class="opacity-0">…</div>
```

---

## Neighbours

- [color](color.md) — the tokens a tint or a muted run should use instead
- [border](border.md) — the ring that owns focus
- [filters](filters.md) — `blur` and `backdrop-blur`, the other layering tools
- [display](display.md) — how to actually hide something
- [interactive](../html/interactive.md) — the `disabled` attribute `opacity-50` pairs with

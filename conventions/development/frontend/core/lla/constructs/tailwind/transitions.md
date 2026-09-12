# Transitions

*Last updated: 2026-09-10*

> Every transition and animation utility, the motion tokens they must consume, and the motion nothing can stop.
> Purpose — motion is a token scale like any other, and the reduced-motion contract only holds if it stays one.
> Use case — reach here before animating anything, and whenever an exit animation is cut short.

## The utilities

| Utility | Applies | Verdict |
|---|---|---|
| `transition-colors` | colour, border, fill and stroke — the default | `use` |
| `transition-opacity` · `transition-transform` · `transition-shadow` | one cheap property | `use` |
| `transition` | the common property set | `use` |
| `transition-all` | every animatable property, including layout | `banned` |
| `transition-none` | motion removed for one element | `use` |
| `transition-[width]` · `transition-[grid-template-rows]` | a property with no utility of its own | `use with care` |
| `duration-(--duration-fast\|base\|slow)` | a duration read from the motion scale | `use` |
| `ease-(--ease-out\|in\|standard)` | an easing read from the motion scale | `use` |
| `duration-150` · `duration-300` | a raw duration outside the motion tokens | `banned` |
| `ease-linear` · `ease-out` · `ease-in` | curves outside the motion tokens | `banned` |
| `delay-*` | a start deferred | `use with care` |
| `animate-(--animate-fade-in)` and its siblings | a named animation from the theme | `use` |
| `animate-spin` · `animate-pulse` · `animate-ping` · `animate-bounce` | the built-in loops | `use` |
| `animate-none` | an animation removed, usually under `motion-reduce:` | `use` |
| `animate-[name_1.4s_ease-in-out_infinite]` | inline timing outside the tokens | `banned` |
| `motion-safe:` · `motion-reduce:` | motion gated on the user's preference | `use` |
| `will-change-transform` | a layer promoted ahead of an animation | `use with care` |
| an exit animation with no deferred unmount | a component removed before its animation runs | `banned` |
| an animation on a `role="status"` region's own text | movement under text a reader is announcing | `banned` |
| a raw easing — `ease-[cubic-bezier(…)]` | a curve outside the scale | `banned` |

- must take duration and easing from the motion tokens ([custom properties](../css/custom-properties.md)).
- must transition a specific property — colour, opacity, transform — never the whole set.
- must gate a decorative animation on `motion-safe:`, and reach for `motion-reduce:animate-none` on the rest.
- must host an exit animation on `Presence` or `Overlay`, which defer the unmount until it ends
  ([visual kinds](../../../mla/constructs/visual/visual.md)).
- must drive an enter/exit pair from `data-[state=open|closed]` ([variants](variants.md)).

---

## Banned

- **`transition-all`** — reach for the property that actually changes; it animates layout properties too, so a
  width or height change that used to be instant now runs a paint every frame on every element carrying the class.
- **an exit animation with no deferred unmount** — reach for `Presence`; the element is removed from the DOM the
  moment its state flips, so the exit animation is defined, compiled, shipped, and never seen.
- **a raw `cubic-bezier()` in a class** — reach for an `--ease-*` token; a curve typed at a use site drifts from
  every other easing in the app, and the difference is visible when two components animate side by side.
- **animated status text** — keep the announcement text static; animate a decorative sibling instead.

```vue
<!-- ✅ tokens for both halves, state-driven, and reduced motion honoured -->
<div :data-state="isOpen ? 'open' : 'closed'"
     class="transition-opacity duration-(--duration-base) ease-(--ease-out)
            motion-reduce:transition-none data-[state=closed]:opacity-0">…</div>

<!-- ❌ every property animated, and a curve that matches nothing else in the app -->
<div class="transition-all duration-[240ms] ease-[cubic-bezier(0.2,0,0,1)]">…</div>
```

---

## Neighbours

- [transforms](transforms.md) — the property most transitions animate
- [effects](effects.md) — opacity, the other one
- [variants](variants.md) — `motion-safe:`, `motion-reduce:`, `data-[state=…]`
- [custom properties](../css/custom-properties.md) — the motion scale and the safety net
- [at-rules](../css/at-rules.md) — where a `@keyframes` body and its `--animate-*` token are written

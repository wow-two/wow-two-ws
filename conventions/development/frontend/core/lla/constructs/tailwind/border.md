# Border

*Last updated: 2026-09-10*

> Every border, radius, ring and outline utility, and the spellings that break the focus recipe.
> Purpose — the ring is the focus indicator for the whole codebase, so its utilities are an accessibility contract.
> Use case — reach here before drawing an edge, rounding a corner or styling a focus state.

## The utilities

The focus recipe uses `outline-hidden` with `focus-visible:ring-2 focus-visible:ring-ring`.

| Utility | Applies | Verdict |
|---|---|---|
| `border` · `border-2` · `border-0` | edge width on all sides | `use` |
| `border-t` · `border-r` · `border-b` · `border-l` | one edge | `use` |
| `border-x` · `border-y` | one axis | `use` |
| `border-solid` · `border-dashed` · `border-dotted` | edge style | `use` |
| `border-{token}` | edge colour ([color](color.md)) | `use` |
| `rounded` · `rounded-sm` … `rounded-3xl` | the corner scale | `use` |
| `rounded-full` · `rounded-none` | a pill or circle, and square corners | `use` |
| `rounded-t-*` · `rounded-l-*` · `rounded-br-*` | one side or one corner | `use` |
| `rounded-[inherit]` | a child matching whatever its parent rounds to | `use with care` |
| `ring` · `ring-1` · `ring-2` · `ring-0` | the focus ring's width | `use` |
| `ring-offset-*` | the gap between element and ring | `use` |
| `ring-inset` | a ring drawn inside the box | `use` |
| `divide-x` · `divide-y` | rules between children, without a border per child | `use` |
| `outline` · `outline-2` · `outline-offset-*` | the outline, for forced-colors and print | `use with care` |
| `outline-hidden` paired with a `focus-visible:` ring | transparent outline survives forced colors | `use` |
| `outline-none` without a forced-colors replacement | focus can disappear in forced colors | `banned` |
| `focus:` ring | indicator also shown for pointer focus | `use with care` |
| an arbitrary width — `border-[0.5px]` | a hairline the scale does not offer | `use with care` |
| an arbitrary radius — `rounded-[2.5rem]` | a corner outside the radius scale | `use with care` |
| `border-x-0 border-y` style resets to fake a divider | a rule assembled from edge overrides | `use with care` |

- must preserve a forced-colors focus indicator; use `outline-hidden` with the focus ring on the same element.
- must default to `focus-visible:`; may use `focus:` when pointer focus also needs a visible indicator.
- must add `ring-offset-*` with `ring-offset-background` wherever the ring would touch the element's own fill.
- must reach for `divide-*` over a border on every child, so the first or last edge needs no reset.
- must take a radius from the scale, which the theme's `--radius-*` tokens define
  ([custom properties](../css/custom-properties.md)).

---

## Banned

- **`outline-none` without a forced-colors replacement** — use the outline-and-ring recipe above.
- **a border colour with no token** — reach for `border-border` or `border-input` ([color](color.md)); a literal edge
  stays put when the theme flips, and a dark surface gets a light hairline.

```vue
<!-- ✅ native outline replaced, not removed; ring offset against the page surface -->
<button class="rounded-md border border-input outline-hidden
               focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2
               focus-visible:ring-offset-background">Save</button>

<!-- ❌ focus made invisible — the element still takes focus, and shows nothing -->
<button class="rounded-md border border-input outline-none">Save</button>
```

---

## Neighbours

- [color](color.md) — the tokens these edges and rings take
- [effects](effects.md) — shadow, which reads as an edge at low elevation
- [interactivity](interactivity.md) — the focus-visible variant's other half
- [variants](variants.md) — `focus-visible:`, `peer-focus-visible:`, `group-focus-within:`

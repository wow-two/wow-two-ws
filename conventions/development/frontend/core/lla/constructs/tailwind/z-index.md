# Z-index

*Last updated: 2026-09-10*

> The semantic stacking tiers, the utilities they generate, and the raw numbers that stack by accident.
> Purpose — stacking is global state, so it needs one ordered vocabulary rather than a number picked per component.
> Use case — reach here before raising anything above its siblings, and whenever an overlay lands behind something.

## The utilities

| Utility | Applies | Verdict |
|---|---|---|
| `z-hide` | pushed behind its parent — a decorative layer | `use` |
| `z-base` | the ground floor | `use` |
| `z-raised` | a badge, a chip, a hovered card | `use` |
| `z-docked` · `z-sticky` · `z-banner` | pinned chrome, in ascending order | `use` |
| `z-dropdown` | a menu attached to a trigger | `use` |
| `z-overlay` · `z-modal` | a backdrop, and the dialog above it | `use` |
| `z-popover` · `z-toast` · `z-tooltip` | floating surfaces, in ascending order | `use` |
| `z-debug` | a development-only layer above everything | `use with care` |
| `z-auto` | stacking left to the document order | `use` |
| a raw number — `z-10`, `z-20`, `z-40` | a tier compared against tiers it cannot see | `banned` |
| an arbitrary value — `z-[1]` | the same, spelled to dodge the scale | `banned` |
| a `z-*` on a static box outside flex/grid item layout | an inert stacking value | `banned` |
| a new tier added between two existing ones | a vocabulary that grows per component | `use with care` |
| `isolate` on a subtree | a stacking context that contains its children's tiers | `use` |

- must take every `z-*` from the semantic tiers, whose token scale is the single ordering.
- must apply `z-*` to a positioned box or a flex/grid item; static flex/grid items need no positioning utility.
- must reach for `isolate` when a subtree's stacking must not escape, rather than a higher tier.
- must add a tier to the theme when a genuinely new layer appears, taking one of the gaps of ten
  ([custom properties](../css/custom-properties.md)).
- must let the SDK's overlay components own their own tier ([visual kinds](../../../mla/constructs/visual/visual.md)).
- must check for a transformed or filtered ancestor before assuming a tier failed ([transforms](transforms.md)).

---

## Banned

- **a raw `z-*` number** — reach for a tier; a hand-picked number is chosen against whatever was on screen at the
  time, so it wins today and loses the first time a tooltip opens over the same box.
- **`z-[1]` and other arbitrary values** — reach for `z-raised`; the value dodges the scale while claiming a place
  in it, and a reader has no way to tell which tier it was meant to beat.
- **a `z-*` on a static non-flex/grid item** — reach for `relative`; `z-index` applies to positioned boxes and flex or
  grid children, so on a static block it is inert and the layering bug survives the "fix".
- **a tier invented per component** — reach for the twelve already declared; a second vocabulary means two orderings
  that nothing reconciles, and the conflict only shows when both are on screen at once.

```vue
<!-- ✅ a named tier on a positioned box, and a subtree that cannot escape its own stack -->
<div class="relative isolate">
  <span class="absolute -top-1 z-raised">{{ count }}</span>
</div>
<div class="fixed inset-0 z-overlay" />

<!-- ❌ a raw number on a static box: inert, and unordered against every real tier -->
<span class="z-50">{{ count }}</span>
```

---

## Neighbours

- [position](position.md) — what makes a `z-*` apply at all
- [transforms](transforms.md) · [filters](filters.md) — the properties that create a stacking context
- [custom properties](../css/custom-properties.md) — where the tiers are declared
- [visual kinds](../../../mla/constructs/visual/visual.md) — the overlays that already own a tier

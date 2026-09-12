# Spacing

*Last updated: 2026-09-10*

> Every padding, margin and gap utility, and the spellings that make a component's spacing its neighbour's problem.
> Purpose — one scale for every gap in the codebase, so rhythm is a property of the system rather than of each file.
> Use case — reach here before separating two boxes, or padding one.

## The utilities

| Utility | Applies | Verdict |
|---|---|---|
| `gap-*` · `gap-x-*` · `gap-y-*` | the space between flex or grid children | `use` |
| `p-*` · `px-*` · `py-*` | padding on all sides, or one axis | `use` |
| `pt-*` · `pr-*` · `pb-*` · `pl-*` | padding on one side | `use` |
| `ps-*` · `pe-*` | padding that follows the writing direction | `use` |
| `m-*` · `mx-*` · `my-*` · `mt-*` … | margin, in the same shape | `use with care` |
| `mx-auto` · `ml-auto` · `ms-auto` | a box centred, or one item pushed to the end | `use` |
| `-ml-px` · `-mt-px` | a negative margin collapsing two adjacent borders | `use with care` |
| a negative margin used for layout — `-mx-4` | a box escaping its parent's padding | `use with care` |
| `space-x-*` · `space-y-*` | spacing between children, applied through a sibling rule | `use with care` |
| `p-0` · `m-0` | an inherited spacing removed | `use` |
| `gap-0` | children deliberately flush | `use` |
| a margin on a reusable component's own root | spacing decided by the wrong side of the boundary | `banned` |
| a margin between flex or grid children | spacing a wrap or a reorder relocates | `banned` |
| an arbitrary gap — `gap-[0.5rem]` | a step that already exists, spelled differently | `banned` |
| padding used to fake a gap between siblings | a gap only one of the two boxes knows about | `banned` |

- must reach for `gap-*` between children, and `p-*` inside a box, and nothing else for rhythm.
- must let the parent own the space between its children — a component never margins its own root.
- must reach for `space-y-*` only where the children are not a flex or grid container's own.
- must reach for `ml-auto` to push a single item, rather than a margin sized to the leftover space.

---

## Banned

- **a margin on a reusable component's root** — reach for `gap-*` on the parent; the component then carries spacing
  into every context, and each consumer that wants it flush has to fight a margin `tailwind-merge` cannot see.
- **a margin between flex or grid children** — reach for `gap-*`; a margin survives a `flex-wrap` line break as a
  leading edge gap, and `flex-col-reverse` moves it to the wrong side of the item.
- **an arbitrary value duplicating a scale step** — use the scale spelling so theme changes reach it;
  `tailwind-merge` can resolve these conflicts, but cannot make the literal follow the token.
- **padding standing in for a gap** — reach for `gap-*`; only one of the two boxes carries it, so removing that box
  removes the space and the remaining sibling shifts.

```vue
<!-- ✅ the parent owns the rhythm; the child carries only its own padding -->
<div class="flex flex-col gap-3">
  <Card class="p-4">…</Card>
  <Card class="p-4">…</Card>
</div>

<!-- ❌ the child decides its own outer spacing, in every context it is ever used -->
<div class="flex flex-col">
  <Card class="mt-3 p-4">…</Card>
  <Card class="mt-3 p-4">…</Card>
</div>
```

---

## Neighbours

- [flexbox](flexbox.md) · [grid](grid.md) — the parents `gap-*` belongs to
- [sizing](sizing.md) — the same scale, applied as width and height
- [border](border.md) — where `-ml-px` collapses two edges into one
- [styling](../../../../shapes/app/platform/styling.md) — how a consumer's spacing class merges in

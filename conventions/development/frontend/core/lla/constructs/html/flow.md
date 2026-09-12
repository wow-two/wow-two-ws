# Flow

*Last updated: 2026-09-10*

> The two elements that carry no meaning, and the framework wrappers that emit none at all.
> Purpose — a meaningless box is the right default for layout, and the wrong one for anything a user operates.
> Use case — reach here before wrapping markup, and whenever a `div` is about to grow a `role` or a click handler.

## The elements

| Element | Means | Verdict |
|---|---|---|
| `<div>` | nothing — a block-level box for layout | `use` |
| `<span>` | nothing — an inline box around a text run | `use` |
| `<template>` — Vue | a compile-time group that emits no element | `use` |
| `<>…</>` fragment — React | the same grouping in TSX | `use` |
| `<slot>` — Vue · `children` — React | the hole a consumer fills | `use` |
| `<template>` — HTML | inert markup a script clones at runtime | `use with care` |
| `<noscript>` | content rendered only when scripting is off | `use with care` |
| `<div role="button">` · `<span role="link">` | a control rebuilt out of a meaningless box | `banned` |
| a `<div>` carrying a click handler alone | a target the pointer reaches and the keyboard does not | `banned` |
| a `<div>` wrapping one child to hold a list key | a box that exists for the compiler, not the layout | `banned` |

- must reach for `<div>` and `<span>` for layout and text runs only, never for anything the user operates.
- must nest `<span>` inside phrasing content, and `<div>` only where a block box is legal.
- must prefer `<template>` or a fragment over a wrapper a list only needs for grouping.
- must move a repeated `div` plus its utility string into a component
  ([constructs](../../../mla/constructs/constructs.md)).

---

## Banned

- **`<div role="button">` · `<span role="link">`** — reach for `<button>` / `<a>`
  ([interactive](interactive.md)). The role announces a control but supplies no focus stop, no Enter/Space
  activation and no disabled state — all three get rebuilt by hand, and each is a place to get it wrong.
- **a `<div>` carrying a click handler and nothing else** — reach for `<button type="button">`; no keyboard user ever
  reaches it, and a screen reader reads its text as static content.
- **a `<div>` wrapping a single child purely to hold a list key** — reach for `<template v-for>` or a fragment; the
  extra box breaks a `flex` / `grid` parent's direct-child rules and re-spaces every `gap-*`.
- **`<br>` between two blocks** — reach for `space-y-*` ([spacing](../tailwind/spacing.md)); a line break is content,
  and its collapsing differs per browser, so the gap is not the one the scale defines.

```vue
<!-- ✅ the element supplies the focus stop, Enter/Space, and the disabled state -->
<button type="button" :disabled="isBusy" @click="dismiss">Dismiss</button>

<!-- ❌ a click target no keyboard reaches, announcing a control that is not one -->
<div role="button" @click="dismiss">Dismiss</div>
```

---

## Neighbours

- [interactive](interactive.md) — the elements a click handler belongs on
- [landmarks](landmarks.md) · [text](text.md) — the meaningful boxes a `div` is usually standing in for
- [global attributes](global-attributes.md) — what `role` and `tabindex` cost once added by hand
- [constructs](../../../mla/constructs/constructs.md) — where a repeated wrapper goes

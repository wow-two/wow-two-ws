# Lists

*Last updated: 2026-09-10*

> The three list families, what each announces, and the shapes that lose the count.
> Purpose — a list element tells a screen reader how many items are coming; a stack of `div`s tells it nothing.
> Use case — reach here whenever markup repeats a sibling, and before styling a list's markers away.

## The elements

| Element | Means | Verdict |
|---|---|---|
| `<ul>` | an unordered group — order carries no meaning | `use` |
| `<ol>` | an ordered group — position is part of the content | `use` |
| `<li>` | one item, only ever a direct child of `<ul>` / `<ol>` / `<menu>` | `use` |
| `<ol start>` · `<ol reversed>` · `<li value>` | a numbering that does not begin at one | `use` |
| `<ol type>` | numeric, alphabetic or roman markers | `use with care` |
| `<dl>` · `<dt>` · `<dd>` | a name/value group — labels paired with their values | `use` |
| `<div>` wrapping a `<dt>` / `<dd>` pair | a grouping box the spec permits inside `<dl>` | `use with care` |
| `<menu>` | a list of commands — a `<ul>` by any other name | `use with care` |
| `list-none` on a `<ul>` | markers removed, semantics kept | `use` |
| `role="list"` on a marker-less `<ul>` | the list role restored after Safari drops it | `use` |
| `<ul>` holding anything but `<li>` | items a screen reader cannot count | `banned` |
| a stack of sibling `<div>`s as a list | a group with no count and no item boundaries | `banned` |
| `role="list"` + `role="listitem"` on `div`s | a list rebuilt out of meaningless boxes | `banned` |
| `<dir>` | the obsolete directory list | `banned` |

- must reach for `<ul>` whenever markup repeats a sibling — nav items, chips, results, cards.
- must reach for `<ol>` only where the position is content, such as ranked results or numbered steps.
- must keep `<li>` a direct child of its list; a wrapper between them breaks the count.
- must pair `list-none` with `role="list"` — Safari drops the list role once the marker is gone.
- must style a marker through `li::marker` inside the `.prose` scope, not by replacing the element
  ([selectors](../css/selectors.md)).
- must let a listbox, menu or tree use its ARIA roles rather than list roles
  ([global attributes](global-attributes.md)).

---

## Banned

- **`<ul>` holding anything but `<li>`** — reach for an `<li>` around each child; a screen reader announces "list, N
  items" from the `<li>` count alone, so a wrapper `<div>` reports zero items in a visibly full list.
- **a stack of sibling `<div>`s standing in for a list** — reach for `<ul>` / `<li>`; the group gets no count, no
  boundaries between items, and no way to jump item-by-item.
- **`role="list"` with `role="listitem"` on `<div>`s** — reach for the real elements; the roles restore the
  announcement but not `<li>`'s parsing, so one misplaced wrapper silently drops an item from the count.
- **`<dir>`** — reach for `<ul>`; it is removed from the standard and browsers map it to `<ul>` anyway.

```vue
<!-- ✅ marker-less nav, count intact — role="list" survives Safari's marker removal -->
<ul role="list" class="flex list-none flex-col gap-1">
  <li v-for="item in items" :key="item.id"><RouterLink :to="item.to">{{ item.label }}</RouterLink></li>
</ul>

<!-- ❌ a wrapper between list and item: announced as "list, 0 items" -->
<ul class="flex flex-col gap-1">
  <div v-for="item in items" :key="item.id"><a :href="item.href">{{ item.label }}</a></div>
</ul>
```

---

## Neighbours

- [text](text.md) — the elements inside an item
- [tables](tables.md) — the group to reach for when items share columns
- [global attributes](global-attributes.md) — `role` and when restoring one is right
- [typography](../tailwind/typography.md) — `list-none` and the marker utilities

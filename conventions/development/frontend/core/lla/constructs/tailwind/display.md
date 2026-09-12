# Display

*Last updated: 2026-09-10*

> Every display utility, what each does to the box tree, and the ones that hide content from only half the audience.
> Purpose — `display` is the one property that changes what an element *is* to layout and to a screen reader.
> Use case — reach here before hiding, showing or re-boxing an element.

## The utilities

| Utility | Applies | Verdict |
|---|---|---|
| `block` | a block box, filling its parent's width | `use` |
| `inline` | an inline box, no width or vertical padding | `use` |
| `inline-block` | an inline box that accepts width and padding | `use` |
| `flex` · `inline-flex` | a flex container ([flexbox](flexbox.md)) | `use` |
| `grid` · `inline-grid` | a grid container ([grid](grid.md)) | `use` |
| `hidden` | `display: none` — gone from layout and from the accessibility tree | `use` |
| `contents` | a box removed, its children promoted to the parent | `use with care` |
| `flow-root` | a block that contains its children's floats and margins | `use with care` |
| `table` · `table-row` · `table-cell` | table boxes on non-table elements | `use with care` |
| `list-item` | a box that generates a marker | `use with care` |
| `hidden` with a breakpoint — `hidden sm:block` | one layout per breakpoint, both in the DOM | `use` |
| `hidden` on a focusable element | a control that leaves the tab order with it | `use` |
| `contents` on an element carrying a role | a role with no box, dropped by some engines | `banned` |
| `hidden` used to hide a live region | an announcement that never fires | `banned` |
| `sr-only` used to hide from everyone | text still read aloud, from a zero-sized box | `banned` |
| `opacity-0` used as hiding | an invisible element still focusable and still clickable | `banned` |
| `display` utilities re-boxing table elements | a table's row and column relationships destroyed | `banned` |

- must reach for the `hidden` attribute or a `v-if` when the content should not exist at all
  ([global attributes](../html/global-attributes.md)).
- must keep a live region rendered — announcements come from mutations to a region already in the tree.
- must reach for `contents` only on a plain wrapper, never on anything carrying a role or a label.
- must leave table elements at their own display ([tables](../html/tables.md)).
- must render one layout and re-flow it, before rendering two and toggling `hidden` between them.

---

## Banned

- **`contents` on an element carrying a role** — reach for a wrapper that keeps its box; some engines drop the role
  along with the box, so the element is announced correctly in one browser and not at all in another.
- **`hidden` on a live region** — reach for `sr-only`; `display: none` removes the region from the tree, so the
  mutation that should announce a result fires against nothing.
- **`sr-only` used to hide from everyone** — reach for `hidden`; `sr-only` clips the box to a pixel but keeps it in
  the tree, so a screen-reader user hears text no sighted user can see.
- **`opacity-0` used as hiding** — reach for `hidden`; a transparent element still takes focus, still receives clicks,
  and still blocks whatever is behind it.
- **`display` utilities on `<tr>` / `<td>`** — reach for a separate component ([tables](../html/tables.md)); `flex` on
  a row dissolves the table's internal boxes, and the row/column relationships go with them.

```vue
<!-- ✅ gone for everyone, or visible only to a reader — never one pretending to be the other -->
<span class="hidden sm:inline">Filters</span>
<span class="sr-only">Filters</span>
<p role="status" class="sr-only">{{ savedCount }} codes saved</p>

<!-- ❌ the live region is removed from the tree, so the announcement never fires -->
<p role="status" class="hidden">{{ savedCount }} codes saved</p>
```

---

## Neighbours

- [accessibility](accessibility.md) — `sr-only` and what it is actually for
- [flexbox](flexbox.md) · [grid](grid.md) — the two container displays with their own docs
- [overflow](overflow.md) · [effects](effects.md) — clipping and opacity, the other ways to hide badly
- [global attributes](../html/global-attributes.md) — `hidden` and `inert`

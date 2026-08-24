# Display

*Last updated: 2026-08-23*

> A render of content the component does not own — it shows what it is given and changes nothing.
> Purpose — the largest kind gets one rule set: take data in, render it, emit intent, never mutate.
> Use case — text, cards, tables, media, timelines, charts, avatars, badges, glyphs.

## Gate

- must **not own its content** — a component that produces a value is a [control](control.md).
- must render from props alone, so the same props always render the same output.
- must stay in flow and stay non-blocking; a floating surface is an [overlay](overlay.md).
- must report system state through [feedback](feedback.md) instead of styling an error itself.

```txt
✅ Card · DataTable · PdfViewer · VideoPlayer · DotsGlyph · StatusBadge · PricingCard
❌ EmptyState             (it stands in for content that is absent — a state)
```

---

## Location

### Group

- must live in `presentation/display/` in the SDK, whatever the medium — text, table, media, or SVG.
- must live in the sub-domain that owns the subject in an app
  ([architecture](../../../../shapes/app/architecture/architecture.md)).

```txt
✅ presentation/display/dataTable/{DataTable.vue, DataTable.spec.md, index.ts}
❌ presentation/display/codesTable/         (a product's subject does not ship from the SDK)
```

---

## Declaration

### Component doc

#### [Renders](../../../lla/notation/documentation/documentation.md)

- must name what is shown, never how it is fetched.

### Construct

- must be generic over the row or item type when it renders a collection — `DataTable<TRow>`.
- must keep a compound display's parts in one folder ([compound](../compound/compound.md)).

### Component name

- must end `*Preview` for a stand-in render of a larger thing.
- must end `*Viewer` for a read-only document surface, `*Player` for a media transport one.
- must end `*Renderer` for a render dispatching on a discriminator.
- must admit `*Table` · `*Grid` · `*Row` · `*Cell` for a tabular surface, `*Carousel` · `*Gallery` for a media set,
  `*Card` for a bordered box, `*Badge` · `*Tag` · `*Status` for a chip, `*Glyph` for a fixed SVG mark, `*Overlay`
  for a layer over one child, and `*Text` for a styled run.
- must admit `*Heading` for a typographic outline entry, `*Avatar` for a portrait mark, `*Sparkline` for an
  axis-free trend, and `*Timeline` for a vertical event rail.
- must read every one of them as a shape word ([visual kinds](visual.md) § *Shape words*).

```vue
<script setup lang="ts">
/** Renders a column-driven table with client-side sorting. */
defineOptions({ name: 'DataTable', inheritAttrs: false });
</script>
```

---

## Content

### Props

#### [The](../../../lla/notation/documentation/documentation.md)

- must take the content itself — an array or a scalar, never a fetcher or a query key.
- must pair a scalar prop with a same-named slot when the caller may need rich content.

### Slots

- must expose a slot per repeated unit — the row, the cell, the item, the node.

### Emits

#### [Fires when](../../../lla/notation/documentation/documentation.md)

- must emit the user's intent — `select`, `sort`, `expand` — and leave the change to the caller.

```vue
<script setup lang="ts">
defineProps<{ rows: ReadonlyArray<TRow>; columns: ReadonlyArray<ColumnDef<TRow>> }>();   // ✅
defineEmits<{ (e: 'sort', descriptor: SortDescriptor): void }>();                        // ✅ intent
defineProps<{ queryKey: string }>();                                                     // ❌ it would fetch
</script>
```

---

## Composition

- must be composed by a [page](page.md), a [view](view.md), a [panel](panel.md), or a [layout](layout.md).
- must compose [indicator](indicator.md) and [action](action.md) inside its own slots.
- must not mount a [view](view.md), a [panel](panel.md), or a [page](page.md).

```txt
✅ CodesTableView → DataTable → Badge + CopyButton
❌ DataTable → LoadingState      (the caller decides whether there is anything to show)
```

---

## Neighbours

- [display](../../components/display/display.md) — which one to reach for, and with what values
- [state](state.md) — the stand-in when there is nothing to display
- [indicator](indicator.md) — the passive marks a display hangs off its rows
- [feedback](feedback.md) — the kind that reports system state rather than content
- [visual kinds](visual.md) — every other kind, and the composition ladder

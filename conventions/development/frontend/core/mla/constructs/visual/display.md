# Display

*Last updated: 2026-09-10*

> A render of content the component does not own — it shows what it is given and changes nothing.
> Purpose — the largest kind gets one rule set: take data in, render it, emit intent, never mutate.
> Use case — text, cards, tables, media, timelines, charts, avatars, badges, glyphs.

## Gate

- must render caller-owned content rather than fetch or mutate a product's records.
- may own presentation state: expansion, active view, playback, scrolling and animation.
- must classify a structured editor as a [control](control.md) when its primary contract edits a value.
- must use [feedback](feedback.md) for an operation report and [state](state.md) for a region replacement.
- must use an [overlay](overlay.md) contract for a floating descriptive or interactive surface.

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
- must admit `*Group` for grouped content.
- must read every one of them as a shape word ([visual kinds](visual.md) § *Shape words*).

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

---

## Composition

- must follow the shared [composition contract](visual.md#composition-order).
- may own compound panels, alternate views and controls needed to present its subject.
- may show an empty row or fallback for its collection; the page decides route-level loading and failure.
- must pass user intent to the caller when it changes domain records.
- must preserve each composed widget's semantics and avoid nested interactive elements with competing activation.

```txt
✅ EventCalendar → MonthView; DataTable → empty row; Tabs → TabsPanel
❌ DataTable → a product-specific API client
```

---

## Neighbours

- [display](../../components/display/display.md) — which one to reach for, and with what values
- [state](state.md) — the stand-in when there is nothing to display
- [indicator](indicator.md) — the passive marks a display hangs off its rows
- [feedback](feedback.md) — the kind that reports system state rather than content
- [visual kinds](visual.md) — every other kind, and the composition contract

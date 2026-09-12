# View

*Last updated: 2026-09-10*

> One presentation of a parent-owned subject, optionally swappable with another mode.
> Purpose — a display mode becomes a component, so the parent switches modes instead of branching.
> Use case — month vs agenda vs day, tree vs raw text, thread vs list.

## Gate

- must present a parent-owned subject without route ownership; a second mode is optional.
- must receive the subject from its parent, never fetch it.
- must not own which view is showing — the mode lives in the parent or the route.
- must be mounted by a [page](page.md) or a composite root; a URL of its own makes it a page.

```txt
✅ MonthView · AgendaView · TimeGridView · JsonEditorTreeView · JsonEditorTextView
❌ SettingsView            (nothing swaps with it — that is a page or a panel)
```

---

## Location

### Group

- must sit with its owning subject; alternate modes stay beside their composite root.
- must live in the owning sub-domain in an app, never in the domain's `common/` slice.

```txt
✅ display/eventCalendar/MonthView.vue · AgendaView.vue · TimeGridView.vue
❌ display/monthView/MonthView.vue         (split from the siblings it swaps with)
```

---

## Declaration

### Component doc

#### [Renders](../../../lla/notation/documentation/documentation.md)

- must name the mode, since the subject is already in the parent's doc.

### Construct

- must read shared root state through context inside a compound; a standalone view receives its subject as props.

### Component name

- must end `*View` — one swappable presentation of a subject the parent owns.
- must name the **mode** in the stem, not the subject — `Month`, not `Calendar`.

---

## Content

### Props

#### [The](../../../lla/notation/documentation/documentation.md)

- must take the subject and the mode's own parameters as props — the anchor date, the selection, the range.
- must not take a `mode` prop — being the mode is what the component is for.

### Slots

- must expose a slot for each item the parent may re-render — the day cell, the row, the node.

### Emits

#### [Fires when](../../../lla/notation/documentation/documentation.md)

- must emit selection and navigation upward, and never mutate the subject it was handed.

---

## Composition

- must follow the shared [composition contract](visual.md#composition-order).
- may compose layout, controls, fields and displays needed for its subject.
- must leave the page frame and sibling-mode selection to its owner.

---

## Neighbours

- [display](../../components/display/display.md) — which one to reach for, and with what values
- [page](page.md) — the routed owner that picks which view shows
- [panel](panel.md) — the sibling kind for a region a composite positions rather than swaps
- [display](display.md) — the parts a view renders its subject with
- [visual kinds](visual.md) — every other kind, and the composition contract

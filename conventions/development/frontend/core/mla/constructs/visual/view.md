# View

*Last updated: 2026-08-23*

> One presentation of one subject, swappable for a sibling that presents the same subject differently.
> Purpose — a display mode becomes a component, so the parent switches modes instead of branching.
> Use case — month vs agenda vs day, tree vs raw text, thread vs list.

## Gate

- must be swappable for a **sibling view over the same subject** — no sibling means it is a [display](display.md).
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

- must sit beside its sibling views inside the composite that switches them — `display/{composite}/`.
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

- must read the composite's context rather than re-declaring a prop the root already holds.

### Component name

- must end `*View` — one swappable presentation of a subject the parent owns.
- must name the **mode** in the stem, not the subject — `Month`, not `Calendar`.

```vue
<script setup lang="ts">
/** Renders the month-grid view. */
defineOptions({ name: 'MonthView' });
</script>
```

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

```vue
<script setup lang="ts">
defineProps<{ readonly events: ReadonlyArray<CalendarEvent>; readonly anchor: Date }>();  // ✅
defineEmits<{ (e: 'select', day: Date): void }>();                                        // ✅
defineProps<{ readonly mode: 'month' | 'agenda' }>();                                     // ❌ it is the mode
</script>
```

---

## Composition

- must compose [display](display.md), [control](control.md), and [indicator](indicator.md) components only.
- must not mount a [layout](layout.md) that decides the page frame — the [page](page.md) owns that.
- must not mount a sibling view; switching is the parent's job.

```txt
✅ EventCalendar → MonthView → DayCell → StatusIndicator
❌ MonthView → AgendaView       (a view switching to its own sibling)
```

---

## Neighbours

- [display](../../components/display/display.md) — which one to reach for, and with what values
- [page](page.md) — the routed owner that picks which view shows
- [panel](panel.md) — the sibling kind for a region a composite positions rather than swaps
- [display](display.md) — the parts a view renders its subject with
- [visual kinds](visual.md) — every other kind, and the composition ladder

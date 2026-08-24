# Feedback

*Last updated: 2026-08-23*

> A report of what the system just did or is doing — the outcome of an action, not the content of a page.
> Purpose — outcome reporting is one kind, so severity, dismissal, and live-region wiring are decided once.
> Use case — a save succeeded, a request is running, a step is 3 of 5, an undo is still available.

## Gate

- must report **system state**, not domain content — content the user asked for is a [display](display.md).
- must be readable by a page reader without focus moving to it — a live region, not a silent swap.
- must stand in for nothing; a component that replaces missing content is a [state](state.md).
- must carry its own copy; a bare mark with no text is an [indicator](indicator.md).
- the ✅ list names **kinds**, never the folder's residents — a state or an indicator may live in
  `presentation/feedback/` when its case sends it there ([state](state.md) § *Location*).

```txt
✅ Alert · Banner · Callout · Toast · UndoBar
❌ Badge                  (a category chip on content — a display)
❌ Skeleton               (it replaces a region's content — a state, filed in this folder by case)
❌ ProgressBar            (a bare mark with no copy — an indicator)
```

---

## Location

### Group

- must live in `presentation/feedback/` in the SDK, whether it is inline, pinned, or transient.
- must keep the queue and the surface apart — the store publishes, a [host](host.md) renders.

```txt
✅ presentation/feedback/toast/{Toast.vue, ToastSimple.vue, Toast.spec.md, index.ts}
❌ presentation/feedback/feedbackBus/       (a bus is a seam → headless suffixes)
```

---

## Declaration

### Component doc

#### [Renders](../../../lla/notation/documentation/documentation.md)

- must state the placement — inline, full-width, transient, blocking.

### Construct

- must set the ARIA live semantics the severity earns — `status` for progress, `alert` for an error.
- must ship a slotted root and an atomic `*Simple` counterpart where callers need free children.
- must subscribe a viewport to a store or bus rather than take its items as props.

### Component name

- must end an inline note `*Callout`, a transient one `*Toast`, a section note `*Alert`.
- must admit `*Banner` for a full-width strip and `*Bar` for a persistent one — `UndoBar` — all shape words ([visual
  kinds](visual.md) § *Shape words*).

```vue
<script setup lang="ts">
/** Renders a transient toast card with an icon, title, description, and actions. */
defineOptions({ name: 'Toast' });
</script>
```

---

## Content

### Props

#### [The](../../../lla/notation/documentation/documentation.md)

- must take `tone` from the shared severity vocabulary, never a free string.
- must take the copy as scalar props with same-named slots, so a caller can enrich either half.
- must take a `duration` only where the component dismisses itself.

### Slots

- must expose `icon`, `title`, `description`, and `actions` on any slotted root.

### Emits

#### [Fires when](../../../lla/notation/documentation/documentation.md)

- must emit `dismiss` for every close path, so the caller can drop the item from its queue.

```vue
<script setup lang="ts">
defineProps<{ tone?: StatusTone; title?: string; duration?: number }>();   // ✅
defineEmits<{ (e: 'dismiss'): void }>();                                   // ✅
defineProps<{ color?: string }>();                                         // ❌ severity is a vocabulary
</script>
```

---

## Composition

- must be mounted by a [layout](layout.md) region, a [page](page.md), or a [field](field.md).
- must compose [action](action.md) and [indicator](indicator.md) in its slots — retry, undo, a spinner.
- must portal a transient surface to the app root, so a toast survives its trigger unmounting.
- must not mount a [view](view.md), a [panel](panel.md), or a [control](control.md).

```txt
✅ AppShell → ToastHost → Toast → Button      ·      Field → FormErrorMessage
❌ Toast → TextInput                        (asking for input inside a report)
```

---

## Neighbours

- [feedback](../../components/feedback/feedback.md) — which one to reach for, and with what values
- [indicator](indicator.md) — the kind for a passive mark with no copy of its own
- [state](state.md) — the kind that stands in for content instead of reporting on it
- [state and data](../../domains/data/state-and-data.md) — the bus and store a viewport subscribes to
- [visual kinds](visual.md) — every other kind, and the composition ladder

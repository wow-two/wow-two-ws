# Feedback

*Last updated: 2026-09-10*

> A report of what the system just did or is doing — the outcome of an action, not the content of a page.
> Purpose — outcome reporting is one kind, so severity, dismissal, and live-region wiring are decided once.
> Use case — a save succeeded, a request is running, a step is 3 of 5, an undo is still available.

## Gate

- must report **system state**, not domain content — content the user asked for is a [display](display.md).
- must be readable by a page reader without focus moving to it — a live region, not a silent swap.
- must stand in for nothing; a component that replaces missing content is a [state](state.md).
- must report an operation or condition; a compact passive state mark is an [indicator](indicator.md), with or without a label.
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

- must use polite status updates by default and an alert only for information that warrants interruption.
- must keep the announcement owner stable; component mounting alone is not a reliable status announcement.
- must ship a slotted root and an atomic `*Simple` counterpart where callers need free children.
- must delegate queue subscription, timers and portal ownership to the [host](host.md) or an explicit custom viewport.

### Component name

- must end an inline note `*Callout`, a transient one `*Toast`, a section note `*Alert`.
- must admit `*Banner` for a full-width strip and `*Bar` for a persistent one — `UndoBar` — all shape words ([visual
  kinds](visual.md) § *Shape words*).

---

## Content

### Props

#### [The](../../../lla/notation/documentation/documentation.md)

- must type semantic severity through the shared vocabulary; each component spec names its exact prop.
- must take the copy as scalar props with same-named slots, so a caller can enrich either half.
- must take a `duration` only where the component dismisses itself.

### Slots

- must expose `icon`, `title`, `description`, and `actions` on any slotted root.

### Emits

#### [Fires when](../../../lla/notation/documentation/documentation.md)

- must report accepted dismissal through one documented event; the queue owner removes the item.

---

## Composition

- must follow the shared [composition contract](visual.md#composition-order).
- may accept caller-owned actions and free-form content; embedded controls keep their own names and form lifecycle.
- must keep the transient card visual; its viewport owns timers, portal placement and queue removal.
- must avoid announcing the same message from both the card and its host.
- must let persistent actionable feedback remain reachable until the relevant action can be completed.

---

## Neighbours

- [feedback](../../components/feedback/feedback.md) — which one to reach for, and with what values
- [indicator](indicator.md) — the kind for a passive mark with no copy of its own
- [state](state.md) — the kind that stands in for content instead of reporting on it
- [state and data](../../domains/data/state-and-data.md) — the bus and store a viewport subscribes to
- [visual kinds](visual.md) — every other kind, and the composition contract

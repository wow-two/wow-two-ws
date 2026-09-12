# Host

*Last updated: 2026-09-10*

> A component that renders, at one fixed mount point, whatever a domain's bus publishes.
> Purpose — a notice raised from a query hook needs a surface, and that surface belongs to no view.
> Use case — the toast viewport today; a modal or command-palette mount on the same shape.

## Gate

- must render only what its bus publishes — a host takes no children of its own.
- must have one active renderer per bus and application scope; a duplicate in that scope fails clearly.
- must isolate state per SSR request and release the registration on unmount so a remount is valid.
- must own no copy — every word it shows arrives with the notice it was handed.
- must not install a capability; a component rendering only its slot is a [provider](provider.md).

```txt
✅ ToastHost · FeedbackToastHost
❌ ToastProvider          (it renders a stack and a timer, so it is not slot-only)
❌ ToastLayout            (it arranges nothing the caller passed in)
```

---

## Location

### Group

- must live in the group its domain's own surfaces live in — the toast host beside `feedback/`.
- must take mount placement from the capability's application or local scope.

### Folder

- must sit beside the surface it stacks, so the host and its card ship as one unit.

```txt
✅ src/presentation/feedback/toastHost/{ToastHost.vue, ToastHost.spec.md, index.ts}
❌ src/presentation/layout/toastHost/     (it is not chrome — it renders no region)
```

---

## Declaration

### Component doc

#### [Renders](../../../lla/notation/documentation/documentation.md)

- must name what the app gains a surface for, never the store behind it.

### Construct

- must subscribe to exactly one bus, and unsubscribe on unmount.
- must expose `use{Domain}Host()` as the only way view code publishes into it.
- must key each rendered item, so a re-fire updates in place instead of stacking a duplicate.

### Component name

- must end `*Host` — one bus, one host, and the domain word leads.
- must name the domain hosted, never the widget stacked — `ToastHost`, not `CardHost`.

---

## Content

### Props

#### [The](../../../lla/notation/documentation/documentation.md)

- must accept an explicit bus or use the app-scoped bus installed by its capability.
- must define pre-mount delivery in the bus contract: buffer, reject or drop explicitly; never imply guaranteed delivery.
- must take placement and limits as props — position, max, default duration.

### Slots

- may expose a scoped item-render slot without accepting unrelated layout children.

### Emits

#### [Fires when](../../../lla/notation/documentation/documentation.md)

- must emit nothing — the publisher already knows what it published.

---

## Composition

- must take application-wide mounting from bootstrap; an isolated scoped host may live with its scope.
- must compose its capability's surface and keep its queue/lifecycle ownership explicit.
- must keep duplicate-host detection scoped to the actual bus, not to unrelated app instances.

---

## Neighbours

- [provider](provider.md) — the slot-only kind a host is most often mistaken for
- [feedback](feedback.md) — the reports a host stacks, each carrying its own copy
- [hooks](../behavior/hooks.md) — the `use{Domain}Host()` composable a host is published through
- [visual kinds](visual.md) — every other kind, and the composition contract

# Host

*Last updated: 2026-08-22*

> A component that renders, at one fixed mount point, whatever a domain's bus publishes.
> Purpose — a notice raised from a query hook needs a surface, and that surface belongs to no view.
> Use case — the toast viewport today; a modal or command-palette mount on the same shape.

## Gate

- must render only what its bus publishes — a host takes no children of its own.
- must be mounted once, and must fail loudly on a second mount rather than render everything twice.
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
- must be mounted from `bootstrap/`, never from inside a page.

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

```vue
<script setup lang="ts">
/** Renders every toast published on the feedback bus, stacked at one corner. */
defineOptions({ name: 'ToastHost' });
</script>
```

---

## Content

### Props

#### [The](../../../lla/notation/documentation/documentation.md)

- must take its bus as a prop, defaulting to the app's own, so a test can drive it.
- must take placement and limits as props — position, max, default duration.

### Slots

- must declare no slot; a mount point accepting children is a [layout](layout.md).

### Emits

#### [Fires when](../../../lla/notation/documentation/documentation.md)

- must emit nothing — the publisher already knows what it published.

```vue
<script setup lang="ts">
defineProps<{ bus?: FeedbackBus; position?: Corner; max?: number }>();   // ✅ the bus comes in
defineSlots<{ default(): unknown }>();                                   // ❌ children make it a layout
</script>
```

---

## Composition

- must be mounted once in `bootstrap/`, above every route.
- must compose its own domain's surface, never a foreign one.
- must not nest — two hosts for one bus render every notice twice.

```txt
✅ App → ToastHost → Toast
❌ CodesListPage → ToastHost      (a page cannot own an app-wide mount)
```

---

## Neighbours

- [provider](provider.md) — the slot-only kind a host is most often mistaken for
- [feedback](feedback.md) — the reports a host stacks, each carrying its own copy
- [hooks](../behavior/hooks.md) — the `use{Domain}Host()` composable a host is published through
- [visual kinds](visual.md) — every other kind, and the composition ladder

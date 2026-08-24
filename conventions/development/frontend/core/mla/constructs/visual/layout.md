# Layout

*Last updated: 2026-08-23*

> An arrangement of whatever it is given — it places children and owns no content of its own.
> Purpose — spacing, stacking, and framing become named components instead of ad-hoc utility strings.
> Use case — any time the answer is "put these next to each other", not "show this data".

## Gate

- must render **only its children** — a component with copy, an icon, or data of its own is a [display](display.md).
- must stay meaningful with any children at all; a layout that only works with one child type is that child's parent.
- must decide position and spacing only — colour, tone, and state belong to what it wraps.
- must stay in flow; a component that floats out of flow is an [overlay](overlay.md).

```txt
✅ BoxLayout · StackLayout · GridLayout · TwoColumnLayout · AppShell · SurfaceLayout · FrameLayout
❌ SectionHeader           (it renders a title and actions — that is a display)
```

---

## Location

### Group

- must live in `presentation/layout/` in the SDK, and in the layer's `common/` slice in an app.
- must keep the app frame here too — `AppShell` is a layout with named regions, not a page.

```txt
✅ presentation/layout/stackLayout/{StackLayout.vue, StackLayout.spec.md, index.ts}
❌ presentation/display/stack/Stack.vue      (arrangement is not display)
```

---

## Declaration

### Component doc

#### [Renders](../../../lla/notation/documentation/documentation.md)

- must state the arrangement — the axis, the frame, the constraint.

### Construct

- must expose an `as` prop for the rendered element when the semantic tag varies
  ([styling](../../../../shapes/app/platform/styling.md)).

### Component name

- must end `*Layout` for chrome around a router outlet, `*Shell` for the app frame — one `*Shell` per app.
- must admit `*Bar` · `*Group` · `*Area` · `*Section` · `*Grid` · `*Row` · `*Cell` — all shape words ([visual
  kinds](visual.md) § *Shape words*).

```vue
<script setup lang="ts">
/** Renders a flex container with gap and alignment variants. */
defineOptions({ name: 'Stack', inheritAttrs: false });
defineProps<{ as?: ElementType }>();
</script>
```

---

## Content

### Props

#### [The](../../../lla/notation/documentation/documentation.md)

- must take arrangement props only — direction, gap, align, width, ratio, breakpoint.
- must not take a data prop; a list of items to place is the caller's `v-for`, not the layout's job.

### Slots

- must expose a `default` slot, and one **named** slot per region a frame positions.
- must name a region slot for the region, not the component that usually fills it — `header`, not `navbar`.

### Emits

- must emit only when a region is collapsible, and then only the open state.

```vue
<script setup lang="ts">
defineSlots<{ header(): unknown; sidebar(): unknown; default(): unknown }>();   // ✅
defineProps<{ items: ReadonlyArray<NavEntry> }>();                              // ❌ data is not arrangement
</script>
```

---

## Composition

- must be mounted by a [page](page.md) or another layout, and compose every other visual kind inside.
- must not reach into a child to style it — the child owns its own appearance.
- must not branch on route or auth; a conditional region is a [state](state.md) or a guard the page owns.

```txt
✅ CreateCodePage → AppShell → TwoColumnLayout → StackLayout → FillControls
❌ AppShell → useAuth()          (a layout reading session state)
```

---

## Neighbours

- [layout](../../components/layout/layout.md) — which one to reach for, and with what values
- [page](page.md) — the routed owner that picks the frame
- [panel](panel.md) — the kind for a region a composite owns rather than one a caller fills
- [styling](../../../../shapes/app/platform/styling.md) — tokens, `cn()`, and the variant files a layout uses
- [visual kinds](visual.md) — every other kind, and the composition ladder

# Layout

*Last updated: 2026-09-10*

> An arrangement of whatever it is given — it places children and owns no content of its own.
> Purpose — spacing, stacking, and framing become named components instead of ad-hoc utility strings.
> Use case — any time the answer is "put these next to each other", not "show this data".

## Gate

- must arrange caller-supplied content and may own its surrounding fill, border, radius and elevation.
- must leave domain records, fetching and product commands to the caller.
- may own arrangement behavior such as resizing, scrolling and region collapse.
- must apply the field contract when a wrapper also owns control labeling or validation associations.
- must distinguish an in-box absolute anchor from a floating surface with focus and dismissal behavior.

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

- must end `*Layout` for arrangement or chrome, `*Shell` for the app frame.
- must admit `*Bar` · `*Group` · `*Area` · `*Section` · `*Grid` · `*Row` · `*Cell` · `*Timeline` — all shape words ([visual
  kinds](visual.md) § *Shape words*).

---

## Content

### Props

#### [The](../../../lla/notation/documentation/documentation.md)

- must take arrangement and chrome props; a behaviorful layout may take its documented interaction handlers.
- must not take a data prop; a list of items to place is the caller's `v-for`, not the layout's job.

### Slots

- must expose a `default` slot, and one **named** slot per region a frame positions.
- must name a region slot for the region, not the component that usually fills it — `header`, not `navbar`.

### Emits

- must report layout interaction changes, such as region openness, resized proportions or a refresh request.

---

## Composition

- must follow the shared [composition contract](visual.md#composition-order).
- may constrain child roles in an explicit compound, such as resizable panels.
- must style owned chrome and arrangement without rewriting a child's semantic state.
- must let the page or an explicit guard decide auth/route-dependent regions.
- must allow the caller to avoid nested `main` landmarks when layouts compose.

---

## Neighbours

- [layout](../../components/layout/layout.md) — which one to reach for, and with what values
- [page](page.md) — the routed owner that picks the frame
- [panel](panel.md) — the kind for a region a composite owns rather than one a caller fills
- [styling](../../../../shapes/app/platform/styling.md) — tokens, `cn()`, and the variant files a layout uses
- [visual kinds](visual.md) — every other kind, and the composition contract

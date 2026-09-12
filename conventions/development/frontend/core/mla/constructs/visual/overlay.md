# Overlay

*Last updated: 2026-09-10*

> A surface that leaves the document flow and paints above the page until it is dismissed.
> Purpose — an action gets its own surface without taking a URL, so it never forks by breakpoint.
> Use case — a confirm, a picker's panel, a detail peek, a mobile action list.

## Gate

- must render a floating surface with a documented open/close lifecycle.
- must distinguish modal interaction, nonmodal interaction and descriptive hover/focus content.
- must trap focus and make background content unavailable only while modal.
- must leave focus on the trigger for a tooltip or descriptive hover card.
- must let keyboard users leave a nonmodal surface without trapping them in its controls.
- must preserve route identity for bookmarkable places; geometry alone does not determine navigation.
- must offer a keyboard-reachable dismissal or completion path.

---

## Location

### Group

- must live in `presentation/overlays/` in the SDK when it is a standalone surface a caller opens.
- must live with its owner when it only ever decorates one child — `display/badgeOverlay/`.

```txt
✅ presentation/overlays/bottomSheet/{BottomSheet.vue, BottomSheet.spec.md, index.ts}
❌ presentation/layout/modal/Modal.vue        (an out-of-flow surface is not a layout)
```

---

## Declaration

### Component doc

#### [Renders](../../../lla/notation/documentation/documentation.md)

- must state the anchor — centred, edge-anchored, trigger-anchored.

### Construct

- must build on the overlay primitives — `Portal`, `FocusScope`, `DismissableLayer`, `Presence`.
- must not re-implement focus trapping, scroll locking, or outside-click detection ([primitive](primitive.md)).

### Component name

- must end `*Modal` for a blocking dialog.
- must end a trigger-anchored floating panel `*Popover` · `*Tooltip`.
- must admit `*Drawer` for an edge slide, `*Sheet` for a bottom one, `*Card` for `HoverCard`, and `*Overlay` for a
  layer painted over one child — all shape words ([visual kinds](visual.md) § *Shape words*).
- must not prefix `Overlay*`; the word says what the thing is, so it trails.

---

## Content

### Props

#### [The](../../../lla/notation/documentation/documentation.md)

- must apply the [controlled-state contract](../../../lla/notation/naming/props.md#controlled-state) to openness;
  model spellings belong to the framework adapter.
- must accept a dismissal opt-out per channel rather than one blanket flag — Escape and scrim differ.

### Slots

- must expose `default` for the body, plus named slots for the parts a caller replaces — header, footer.

### Emits

#### [Fires when](../../../lla/notation/documentation/documentation.md)

- must report every accepted close through the open-state contract, including Escape and outside interaction.
- must let a dirty-flow owner veto dismissal without changing the surface into an alert dialog.

---

## Composition

- must follow the shared [composition contract](visual.md#composition-order).
- must give dialogs an accessible name and connect an optional description.
- must keep a tooltip descriptive and connect it with `aria-describedby`; it does not replace the trigger's name.
- must restore focus to a valid trigger or a meaningful continuation when the trigger no longer exists.
- must coordinate nested floating surfaces: the topmost eligible layer handles Escape and outside interaction.
- must default a nested blocking flow to the existing modal surface rather than stacking another modal.
- must preserve the same task and data when adapting its geometry across breakpoints.
- must allow hover/focus content to remain reachable while the pointer crosses to it.

---

## Neighbours

- [overlays](../../components/overlays/overlays.md) — which one to reach for, and with what values
- [action](action.md) — the trigger that opens an overlay
- [primitive](primitive.md) — the portal, focus-scope, and dismiss behaviour an overlay builds on
- [routing](../../../../shapes/app/routing/routing.md) — why an action stays routeless and a place does not
- [visual kinds](visual.md) — every other kind, and the composition contract

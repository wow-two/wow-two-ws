# Overlay

*Last updated: 2026-08-23*

> A surface that leaves the document flow and paints above the page until it is dismissed.
> Purpose — an action gets its own surface without taking a URL, so it never forks by breakpoint.
> Use case — a confirm, a picker's panel, a detail peek, a mobile action list.

## Gate

- must **leave the flow** — a surface that pushes siblings around is a [layout](layout.md) or a [panel](panel.md).
- must be dismissable — Escape, a scrim click, or an explicit action; a permanent layer is not an overlay.
- must carry no route ([routing](../../../../shapes/app/routing/routing.md)); a bookmarkable place is a [page](page.md).
- must own focus while it is open — trap it, restore it on close.

```txt
✅ Modal · AlertModal · Drawer · BottomSheet · ActionSheet · Popover · HoverCard · LoadingOverlay
❌ Sidebar                  (it shares the flow with the content — a layout region)
```

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

```vue
<script setup lang="ts">
/** Renders a bottom-anchored sheet with a drag handle and snap points. */
defineOptions({ name: 'BottomSheet' });
</script>
```

---

## Content

### Props

#### [The](../../../lla/notation/documentation/documentation.md)

- must model openness as `open` with an `update:open` emit, and support an uncontrolled default.
- must accept a dismissal opt-out per channel rather than one blanket flag — Escape and scrim differ.

### Slots

- must expose `default` for the body, plus named slots for the parts a caller replaces — header, footer.

### Emits

#### [Fires when](../../../lla/notation/documentation/documentation.md)

- must emit `update:open` for every close path, including Escape and the scrim.

```vue
<script setup lang="ts">
defineProps<{ open?: boolean; defaultOpen?: boolean }>();          // ✅ controlled + uncontrolled
defineEmits<{ (e: 'update:open', open: boolean): void }>();        // ✅
defineProps<{ isVisible: boolean }>();                             // ❌ not the model contract
</script>
```

---

## Composition

- must be opened by an [action](action.md), and never mount the component that opened it.
- must compose [field](field.md), [control](control.md), and [display](display.md) inside its body.
- must present the same place identically at every breakpoint — swap Modal ↔ BottomSheet, never route.
- must not stack a second blocking overlay; a nested flow belongs in the same surface.

```txt
✅ Button → AlertModal → Field → Button           (confirm inside one surface)
❌ Modal → Modal                                  (a second blocking layer over the first)
```

---

## Neighbours

- [overlays](../../components/overlays/overlays.md) — which one to reach for, and with what values
- [action](action.md) — the trigger that opens an overlay
- [primitive](primitive.md) — the portal, focus-scope, and dismiss behaviour an overlay builds on
- [routing](../../../../shapes/app/routing/routing.md) — why an action stays routeless and a place does not
- [visual kinds](visual.md) — every other kind, and the composition ladder

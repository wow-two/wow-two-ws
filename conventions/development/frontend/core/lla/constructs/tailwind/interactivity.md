# Interactivity

*Last updated: 2026-09-10*

> Every cursor, selection, pointer and scroll utility, and the ones that lie about whether a control works.
> Purpose — these utilities change what the pointer reports, not what the element does; the two must agree.
> Use case — reach here before changing a cursor, blocking a pointer or tuning a scroll.

## The utilities

| Utility | Applies | Verdict |
|---|---|---|
| `cursor-pointer` | the hand cursor, on something that is not already a link | `use with care` |
| `cursor-default` · `cursor-text` · `cursor-grab` · `cursor-grabbing` | the drag and text cursors | `use` |
| `cursor-not-allowed` | the disabled cursor, beside the real `disabled` attribute | `use` |
| `cursor-col-resize` · `cursor-row-resize` · `cursor-ns-resize` | a resize affordance | `use` |
| `cursor-pointer` on a native button or link | a house cursor override | `banned` |
| `cursor-not-allowed` with no `disabled` or `aria-disabled` | a control that looks dead and still fires | `banned` |
| `pointer-events-none` | a box the pointer passes through | `use` |
| `pointer-events-auto` | pointer events restored inside a `none` ancestor | `use` |
| `pointer-events-none` used to disable a control | a control the keyboard still activates | `banned` |
| `select-none` · `select-text` · `select-all` | what a drag selects | `use` |
| `select-none` on readable content | text a user cannot copy | `banned` |
| `appearance-none` | a native control's chrome removed before restyling | `use` |
| `resize-none` · `resize-y` · `resize` | a textarea's resize handle | `use` |
| `field-sizing-content` | an input growing with its own value | `use with care` |
| `accent-{token}` | a native checkbox, radio or range's accent colour | `use` |
| `caret-{token}` | the text caret's colour | `use with care` |
| `scroll-smooth` · `scroll-auto` | scroll behaviour, ignoring the motion preference | `use with care` |
| `scroll-m-*` · `scroll-p-*` | the margin a scroll target lands with | `use` |
| `snap-x` · `snap-center` · `snap-mandatory` | scroll snapping | `use with care` |
| `touch-none` · `touch-pan-y` | the gestures the browser keeps for itself | `use with care` |
| `will-change-*` | a layer promoted ahead of a known change | `use with care` |

- must let the cursor follow the `disabled` attribute, never replace it ([interactive](../html/interactive.md)).
- must preserve the browser cursor on native buttons and links; Tailwind v4 does not give buttons a pointer cursor.
- must reach for `pointer-events-none` only on decoration: an icon, an overlay wash, a chart annotation.
- must pair `appearance-none` with a full restyle, including the focus ring ([border](border.md)).
- must gate `scroll-smooth` on `motion-safe:` ([transitions](transitions.md)).
- must keep `select-none` to chrome — a drag handle's label, a toolbar — never to readable content.

---

## Banned

- **`pointer-events-none` used to disable a control** — reach for the `disabled` attribute; the element stays in the
  tab order and Enter still activates it, so it is disabled for the mouse and live for the keyboard.
- **`cursor-not-allowed` with nothing disabled** — reach for `disabled`; the pointer says the control is dead while
  the click still fires, which is the same bug in the other direction.
- **`cursor-pointer` on a native button or link** — keep its native cursor under the house policy above.
- **`select-none` on readable content** — reach for it on chrome only; a user cannot copy an error message, an ID or
  a code, which are exactly the strings they need to paste somewhere else.

```vue
<!-- ✅ the attribute disables it; the cursor follows the state rather than faking it -->
<button type="button" :disabled="isBusy" class="disabled:cursor-not-allowed disabled:opacity-50">Save</button>
<IconCheck aria-hidden="true" class="pointer-events-none absolute right-2 size-4" />

<!-- ❌ disabled for the mouse, live for the keyboard -->
<button type="button" class="pointer-events-none cursor-not-allowed opacity-50">Save</button>
```

---

## Neighbours

- [border](border.md) — the focus ring an `appearance-none` control has to rebuild
- [effects](effects.md) — the `opacity-50` that pairs with a disabled state
- [overflow](overflow.md) — the scroll container these scroll utilities tune
- [interactive](../html/interactive.md) — the elements that carry the behaviour for free

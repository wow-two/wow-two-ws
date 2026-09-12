# Interactive

*Last updated: 2026-09-10*

> The elements a user operates, what each one does for free, and the ones we build ourselves instead.
> Purpose — `<button>` and `<a>` arrive with focus, keyboard activation and a role; a substitute rebuilds all three.
> Use case — reach here before wiring any click, and whenever a control must decide between navigating and acting.

## The elements

| Element | Means | Verdict |
|---|---|---|
| `<button type="button">` | an action in this page — the default control | `use` |
| `<button type="submit">` | the control that submits its form | `use` |
| `<button type="reset">` | a form returned to its default values | `banned` |
| `<a href>` | navigation to another document or fragment | `use` |
| `<a target="_blank" rel="noreferrer">` | navigation into a new tab, referrer withheld | `use` |
| `RouterLink` · `Link` · `NavLink` | in-app navigation that renders an `<a href>` | `use` |
| `<a>` with no `href` | a link no keyboard reaches and no reader announces | `banned` |
| `<button>` used to navigate | an action that changes the URL, with no target to open | `banned` |
| `<a>` used to act | a navigation that goes nowhere, offering to open in a tab | `banned` |
| `<details>` · `<summary>` | native disclosure with its own open state | `use with care` |
| `<dialog>` | a native modal with a top-layer and its own focus trap | `use with care` |
| `role="dialog"` + `Overlay` / `Modal` | our overlay stack — focus trap, `Presence`, portal | `use` |
| `<label>` wrapping a control | a click target that forwards to the control | `use` |
| `popover` + `popovertarget` | native anchored popovers in the top layer | `use with care` |
| `<menu>` | a list of commands — a `<ul>` by another name | `use with care` |
| `tabindex="0"` on a non-interactive element | a focus stop added by hand | `use with care` |
| `tabindex` above `0` | a tab order that ignores the document | `banned` |

- must give every `<button>` an explicit `type`; inside a form the missing default is `submit`.
- must reach for `<a href>` whenever the result is a URL, and `<button>` whenever it is not.
- must route in-app navigation through the router's link component, never a bare `<a>` to an internal path
  ([routing](../../../../shapes/app/routing/routing.md)).
- must pair every `target="_blank"` with `rel="noreferrer"`.
- must express disabled through the `disabled` attribute, and `aria-disabled` only where focus must stay reachable.
- must give an icon-only control an `aria-label` ([global attributes](global-attributes.md)).

---

## Banned

- **`<a>` with no `href`** — reach for `<button type="button">`; without `href` the element leaves the tab order and
  loses its link role, so the control becomes invisible to both keyboard and screen reader.
- **`<button>` that navigates** — reach for a link; the URL never appears in the status bar, and middle-click,
  cmd-click and "open in new tab" all do nothing.
- **`<a>` that performs an action** — reach for `<button>`; the browser offers to open it in a tab, and the reader
  announces "link" for something that mutates state.
- **`<button type="reset">`** — reach for the form's own `reset()`; the native reset restores the DOM defaults rather
  than the form's `defaultValues`, so the model and the inputs disagree ([forms](../../../mla/domains/forms/forms.md)).
- **`tabindex` above `0`** — reach for `0` and fix the DOM order; a positive value jumps ahead of every natural stop
  on the page, so the tab order stops matching what the user sees.
- **`<dialog>` as an uncoordinated overlay primitive** — use the SDK overlay under the house stack policy;
  native dialogs support styled `::backdrop` and discrete exit transitions within their browser support limits.

---

## Interaction

- must suppress activation for `aria-disabled` controls in every event path; ARIA alone does not disable behavior.
- must contain focus and make background content inert only for a modal surface, not an ordinary popover.
- must restore focus on dismissal to the connected trigger or a documented logical successor when it is gone.
- must provide a keyboard route for every action, including a non-drag alternative to drag/reorder.
- must ignore submit/selection shortcuts while `KeyboardEvent.isComposing` is true.
- must end pointer gestures on `pointerup`, `pointercancel`, lost capture and owner disposal.
- must keep a disabled or hidden surface from retaining active global listeners or a focus trap.
- visual/assistive verification → [accessibility](../tailwind/accessibility.md#verification).

```vue
<!-- ✅ navigation is a link, the action is a button, and both say what they are -->
<RouterLink :to="{ name: 'codeDetail', params: { id } }">Open</RouterLink>
<button type="button" aria-label="Delete code" :disabled="isBusy" @click="remove">…</button>

<!-- ❌ an anchor with no href: out of the tab order, and announced as nothing -->
<a class="cursor-pointer" @click="remove">Delete</a>
```

---

## Neighbours

- [forms](forms.md) — the controls a submit button acts on
- [flow](flow.md) — why a clickable `div` is not a substitute
- [global attributes](global-attributes.md) — `aria-label`, `tabindex`, `disabled`
- [routing](../../../../shapes/app/routing/routing.md) — which targets are places and which are actions
- [visual kinds](../../../mla/constructs/visual/visual.md) — the overlay components to reach for first

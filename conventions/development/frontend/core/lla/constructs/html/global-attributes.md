# Global attributes

*Last updated: 2026-09-10*

> The attributes any element may carry — identity, state, description — and the ones we never write.
> Purpose — these are how a component says what it is when the element cannot, and how state reaches CSS.
> Use case — reach here before adding an `id`, a `role`, an `aria-*` or a `data-*` hook.

## The attributes

| Attribute | Means | Verdict |
|---|---|---|
| `class` | the utility string styling the element | `use` |
| `id` | a unique document handle | `use` |
| a hand-written `id` on a component | a handle that collides on the second instance | `banned` |
| `data-*` | component state exposed to CSS and to tests | `use` |
| `style` | one computed value a utility cannot express | `use with care` |
| `role` | a role the element does not already supply | `use with care` |
| `role` restating the element's own role | a second source for one fact | `banned` |
| `aria-label` · `aria-labelledby` | the accessible name, as text or as a reference | `use` |
| `aria-describedby` | supporting text — a hint or an error | `use` |
| `aria-hidden="true"` | content removed from the accessibility tree | `use` |
| `aria-hidden` on a focusable element | a control the reader denies and the keyboard reaches | `banned` |
| `aria-expanded` · `aria-controls` · `aria-haspopup` | a disclosure's state and its target | `use` |
| `aria-selected` · `aria-checked` · `aria-pressed` · `aria-current` | selection, toggle and location state | `use` |
| `aria-invalid` · `aria-required` · `aria-disabled` | a control's validity and availability | `use` |
| `aria-live` · `aria-busy` · `aria-atomic` | a region that announces its own updates | `use` |
| `aria-orientation` · `aria-activedescendant` | a composite widget's axis and virtual focus | `use with care` |
| `tabindex="0"` · `tabindex="-1"` | a focus stop, and a programmatic-only target | `use with care` |
| `tabindex` above `0` | a tab order that ignores the document | `banned` |
| `hidden` | content removed from render and from the tree | `use` |
| `title` | a tooltip on hover, invisible to touch and keyboard | `use with care` |
| `lang` · `dir` · `translate` | the language, writing direction and translation opt-out | `use with care` |
| `inert` | a subtree removed from focus and interaction | `use with care` |
| `popover` · `popovertarget` | native top-layer anchoring | `use with care` |
| `contenteditable` · `draggable` | in-place editing, and a drag source | `use with care` |
| `spellcheck` · `inputmode` | spell checking, and the soft keyboard to show | `use with care` |
| `autofocus` | focus taken on load | `use with care` |
| `accesskey` | a keyboard shortcut assigned per element | `banned` |
| an inline `on*` handler in markup | a listener the CSP has to allow | `banned` |

- must generate reusable internal IDs with the framework's `useId()` and share them with every reference.
- must honor a caller-supplied ID and derive labels/descriptions from the resolved ID rather than a second ID.
- may use stable page-owned IDs for fragment links and skip targets; the page must ensure their uniqueness.
- must not use random/time-based IDs during render or hydration; list identity is a separate key contract.
- must reach for `aria-label` on an icon-only control, and `aria-labelledby` whenever visible text already says it.
- must express component state as `data-state` and target it with a `data-[state=…]` variant
  ([variants](../tailwind/variants.md)).
- must add `role` only where no element carries the meaning ([flow](flow.md)).
- must keep `aria-hidden` off anything focusable, and reach for `inert` when a whole subtree must go.
- must pair `aria-expanded` with `aria-controls` — the state and what it controls travel together.

---

## Banned

- **a hand-written `id` on anything reusable** — reach for `useId()`; the second instance duplicates the `id`, and
  every `for` / `aria-controls` / `aria-describedby` pointing at it resolves to the first one on the page.
- **`role` restating the element's own role** — reach for the bare element; `<button role="button">` creates a second
  place the fact lives, and the two drift the moment the element changes.
- **`aria-hidden="true"` on a focusable element** — reach for `inert`, or remove the element; the keyboard still lands
  on it while the reader insists there is nothing there, which is a dead stop with no announcement.
- **`tabindex` above `0`** — reach for `0` and fix the DOM order; a positive value jumps ahead of every natural stop,
  so the tab order stops matching the visual one.
- **`accesskey`** — reach for a document-level key handler; the browser and the screen reader claim most combinations
  first, and which ones differ per platform.
- **an inline `on*` handler** — reach for the framework's binding; it needs a CSP `unsafe-inline` exemption that the
  whole app then runs under.

```vue
<!-- ✅ generated id, state on data-*, the icon silenced and the control named -->
<button type="button" :id="id" :aria-expanded="isOpen" :aria-controls="panelId"
        :data-state="isOpen ? 'open' : 'closed'" aria-label="Filters">
  <IconFilter aria-hidden="true" class="size-4" />
</button>

<!-- ❌ a fixed id collides on the second instance; the role restates what button already is -->
<button id="filters-toggle" role="button" @click="toggle">…</button>
```

---

## Neighbours

- [flow](flow.md) — why a `role` is usually the wrong fix
- [forms](forms.md) · [interactive](interactive.md) — where these attributes land most often
- [variants](../tailwind/variants.md) — the `data-[…]` and `aria-[…]` selectors that read them
- [accessibility](../tailwind/accessibility.md) — `sr-only` and the visually hidden name

# Panel

*Last updated: 2026-09-10*

> One pane of a composite that owns it — the composite positions it and decides when it shows.
> Purpose — a compound root keeps its regions as named parts instead of arbitrary children.
> Use case — a tab body, a wizard step body, a resizable split pane.

## Gate

- must be **invalid outside its root** — one that stands alone is a [view](view.md) or a [display](display.md).
- must take its identity from the root — the tab value, the step index, the pane order.
- must not decide its own visibility; the root's context does.
- must be one of two or more parts, or it folds back into the root ([compound](../compound/compound.md)).

```txt
✅ TabsPanel · StepperPanel · ResizablePanel
❌ FilterPanel             (usable anywhere — that is a display, or an overlay if it floats)
```

---

## Location

### Group

- must sit in its root's folder, beside the root file — `display/tabs/TabsPanel.vue`.
- must be exported both flat and attached as `Root.Panel` ([compound](../compound/compound.md)).

### Folder

- must not take a folder of its own — a compound subpart is not a component folder.

```txt
✅ display/tabs/{Tabs.vue, TabsList.vue, TabsTab.vue, TabsPanel.vue, TabsContext.ts, index.ts}
❌ display/tabsPanel/TabsPanel.vue        (a subpart split away from the root that owns it)
```

---

## Declaration

### Component doc

#### [Renders](../../../lla/notation/documentation/documentation.md)

- must name the pane's part in the root — `the panel for one tab`.
- must admit `*Section` for a bounded region of the same pane, as a shape word
  ([visual kinds](visual.md) § *Shape words*).

### Construct

- must read the root's context composable — `useTabsContext()`.
- must fail loudly when the context is absent, rather than rendering a detached fallback.

### Component name

- must be `{Root}Panel` — the root's name leads, so the pairing is readable.
- may take the pane's own shape word instead where the root has one — `*Tab` · `*Section`.

---

## Content

### Props

#### [The](../../../lla/notation/documentation/documentation.md)

- must declare the identity prop that pairs it with its trigger — `value`, `index`, `order`.
- must not re-declare a prop the root already holds; read it from the context instead.

### Slots

- must expose a single `default` slot — the pane's content is the caller's.

### Emits

- must declare no emits — the root owns the state, so a change is reported through the root's model.

---

## Composition

- must follow the shared [composition contract](visual.md#composition-order).
- may contain a view, form or other caller-supplied content.
- must let the root choose lazy mount, keep-alive or unmount behavior explicitly.
- must keep inactive panels unavailable to interaction and accessibility navigation.
- must preserve in-progress drafts when the chosen mount policy requires them to survive.
- must not instantiate its own root recursively.

---

## Neighbours

- [display](../../components/display/display.md) · [layout](../../components/layout/layout.md) — which one to reach
  for, and with what values
- [view](view.md) — the sibling kind for a body that swaps rather than one a root positions
- [layout](layout.md) — the kind for arrangement that carries no identity of its own
- [compound](../compound/compound.md) — the compound root and subpart export rules
- [visual kinds](visual.md) — every other kind, and the composition contract

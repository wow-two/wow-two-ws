# Visual constructs

*Last updated: 2026-09-10*

> The index of the **kinds that render** — what each kind is, what it composes with, what it is for.
> Purpose — pick the kind before the name; the kind fixes the suffix, the group folder, and the contract shape.
> Use case — starting a component, or placing one that already exists.

`visual` is the word the kind docs already use — a primitive is the layer "every visual kind is built on"
([primitive](primitive.md)), and a layout composes every other one ([layout](layout.md)).

Behavioral contracts apply to both frameworks. Vue model and event spellings live in
[macros](../../../lla/constructs/vue/macros.md); React spellings live in
[react](../../../lla/constructs/react/react.md).

---

## Reading it [REQUIRED]

- must pick the kind first — it fixes the suffix (§ *Suffix routing*) and the group folder.
- must read a component's co-located `{Component}.spec.md` for its props, slots, emits, and states.
- must not look for a component's own entry here — this file indexes kinds, the spec specifies the component.
- must add a kind only through the coining gate ([constructs](../constructs.md) § *Adding a new suffix*).

```markdown
<!-- ✅ the kind is looked up here, the component in its spec -->
overlay → overlays/ → `*Modal` · `*Drawer` · `*Sheet`  →  Modal.spec.md
<!-- ❌ a component's props do not live in a convention -->
| Modal | `open` · `dismissable` · `size` |
```

---

## Kinds

| Kind | Is | Used with | Used for | Lives in |
|---|---|---|---|---|
| [page](page.md) | a routed viewport owner | layout · view · overlay | one URL's whole surface | app `pages/` |
| [view](view.md) | one presentation of a subject | page · panel | one display mode | `display/` |
| [panel](panel.md) | a bounded region of a parent | view · layout | one pane of a whole | `display/` · `layout/` |
| [layout](layout.md) | an arrangement owning no content | every visual kind | placing children | `layout/` |
| [overlay](overlay.md) | a surface floating above the page | action · field | a task without leaving | `overlays/` |
| [nav](nav.md) | a move between places | layout · overlay | wayfinding | `nav/` |
| [action](action.md) | an intent trigger, no value | overlay · form | running a command | `actions/` |
| [control](control.md) | a widget editing one semantic value | field · form | reading input | `forms/` |
| [field](field.md) | a labeled control plus its help | control · form | one form value | `forms/` |
| [display](display.md) | a render of content it does not own | layout · view | showing data | `display/` |
| [feedback](feedback.md) | a report of system state | layout · provider | saying what happened | `feedback/` |
| [indicator](indicator.md) | a passive mark of live state | display · nav | status at a glance | `feedback/` · `display/` |
| [state](state.md) | a region replacement or busy mask | view · panel | empty · loading · failed | `display/` · `feedback/` |
| [provider](provider.md) | a context supplier, slot only | any subtree | sharing one capability | `auth/` · `query/` |
| [host](host.md) | a mount point for one bus | feedback · overlay | rendering what is published | the domain's group |
| [primitive](primitive.md) | headless behavior, no styling | every visual kind | reusing behavior | `primitives/` |

---

## Suffix routing

A suffix routes only when the word names a **relation** the component must stand in; a word naming the shape it
wears routes nothing and is listed per kind below
([constructs](../constructs.md) § *Relation or form*). Apply compound-subpart and modifier exceptions before suffix matching
([constructs](../constructs.md) § *Naming*). The kind's doc is the
**authority** — it states the suffix and the shape words it admits; this table only routes.

| Suffix | Kind, and the doc that states it |
|---|---|
| `*Page` | [page](page.md) |
| `*View` | [view](view.md) |
| `{Root}Panel` | [panel](panel.md) |
| `*Layout` · `*Shell` | [layout](layout.md) |
| `*Modal` · `*Popover` · `*Tooltip` | [overlay](overlay.md) |
| `*Menu` · `*Item` | [nav](nav.md) |
| `*Button` | [action](action.md) |
| `*Input` · `*Picker` · `*Editor` · `*Controls` | [control](control.md) |
| `*Field` | [field](field.md) |
| `*Form` | [forms domain](../../domains/forms/forms.md) |
| `*Viewer` · `*Player` · `*Renderer` · `*Preview` | [display](display.md) |
| `*Callout` · `*Toast` · `*Alert` | [feedback](feedback.md) |
| `*Indicator` | [indicator](indicator.md) |
| `*State` · `*Gate` · `*Boundary` | [state](state.md) |
| `*Provider` | [provider](provider.md) |
| `*Host` | [host](host.md) |
| none — the behaviour's own word | [primitive](primitive.md) |

---

## Shape words

A shape word ends a name the same way a suffix does, and says nothing about the kind. Every kind listed here
admits it; none owns it, so the reader takes the kind from the folder and the doc, never from the word.

| Shape word | Kinds that admit it |
|---|---|
| `*Bar` | indicator · feedback · action · layout |
| `*Group` | action · control · display · layout |
| `*Card` | display · overlay · field |
| `*Area` | control · layout |
| `*Overlay` | overlay · display · state |
| `*Text` | display · field |
| `*Table` · `*Grid` · `*Row` · `*Cell` | display · layout |
| `*Badge` · `*Tag` · `*Status` · `*Glyph` | display · indicator |
| `*Spinner` | indicator |
| `*Heading` · `*Avatar` · `*Sparkline` | display |
| `*Timeline` | display · layout |
| `*Carousel` · `*Gallery` | display |
| `*Sheet` · `*Drawer` | overlay |
| `*Banner` | feedback |
| `*Section` | panel · layout |
| `*Tab` | panel |

- must read the modifiers (`*Compact` · `*Simple` · `App*`) at [constructs](../constructs.md) § *Naming*.
- must run a new suffix through [constructs](../constructs.md) § *Adding a new suffix*.

---

## Composition order

- must classify by the intended responsibility, not a current prop name or shipping folder.
- must distinguish a committed editable value from interaction state: open, scroll and active view are not form values.
- may keep local interaction state in a display composite without changing it into a control.
- must distinguish a root's owned implementation parts from content supplied through a caller's slots.
- may compose layouts, fields, displays, actions, controls and overlays when the owning contract needs them.
- must keep compound parts under their root's context; a part cannot instantiate its own root recursively.
- must keep product data fetching and commands out of generic visual parts; the caller supplies data and handlers.
- must take capability dependency boundaries from the owning [shape](../../../../shapes/shapes.md).
- must let providers wrap content without taking ownership of that content.
- must keep primitives independent of styled components and domain capabilities.

```txt
✅ Tabs → TabsPanel → ContentView; JsonEditor → mode view → TextAreaInput
❌ DataTable → product API client; TabsPanel → its own Tabs root
```

---

## Placement

A kind doc names its **group** — `overlays/`, `forms/`, `actions/`. Where that group is created is the
deliverable's answer, not the kind's ([shapes](../../../../shapes/shapes.md) § *The test*).

- must take the group folder as the whole of a kind's placement rule; the tree above it belongs to a shape.
- must take a kind's folder and file shape from [constructs](../constructs.md) § *Folder* — stated once here,
  and restated in a kind doc only where that kind overrides it (`panel`, `provider`).
- must read a package's kind-grouped tree in [library](../../../../shapes/library/library.md) § *Layout* — the
  package groups visual components by kind and headless capabilities by domain.
- must read a product's domain slices in
  [architecture](../../../../shapes/app/architecture/architecture.md) § *Sub-domains*, its domain cut § *Domains*.
- must not carry a package's group folders into a product tree; the kind fixes the suffix and the contract, not
  the folder a product puts it in.
- must read a kind doc's `presentation/…` path as a **package-tree example** of its group, never as the group
  name itself — the name is the last segment, and the tree above it is the shape's.

---

## Headless kinds

Not components — the seams a component consumes. Their vocabulary is the
[headless suffixes](../behavior/headless-suffixes.md).

- must name a headless role from that keep-list, never from the routing table above.
- must not look for a seam among the kinds here — nothing on this page describes something that does not render.

---

## Neighbours

- [constructs](../constructs.md) — how any component is shaped, named, and the gate for coining a new suffix
- [headless suffixes](../behavior/headless-suffixes.md) — the second keep-list, for seams a component consumes
- [architecture](../../../../shapes/app/architecture/architecture.md) — the layer and domain a kind's folder sits in
- [hooks](../behavior/hooks.md) — the `use*` counterpart, for state a component owns rather than renders

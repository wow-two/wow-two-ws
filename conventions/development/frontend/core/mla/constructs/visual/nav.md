# Nav

*Last updated: 2026-09-10*

> A component whose whole job is moving the user somewhere — another place, another section, another command.
> Purpose — wayfinding is one kind, so a link row, a menu, and a palette share one contract and one a11y story.
> Use case — a sidebar, a breadcrumb trail, a pager, a right-click menu, a command palette.

## Gate

- must offer destinations or commands without owning an editable domain value.
- must use links for places so normal tabbing, middle-click, copy-link and browser navigation survive.
- must use buttons for commands.
- must derive keyboard behavior from the semantic pattern, not from the `nav/` folder.
- must keep ordinary breadcrumb, sidebar and outline links in the normal tab order.
- must use roving focus or active-descendant behavior only for a composite pattern that requires it.
- must receive destination data or an explicit source from the caller.

---

## Location

### Group

- must live in `presentation/nav/` in the SDK, including the menus, since a menu is a destination list with a trigger.
- must keep the chrome that positions the nav in [layout](layout.md) — `Navbar` places, `NavItem` navigates.

```txt
✅ presentation/nav/dropdownMenu/{DropdownMenu.vue, MenuItem.vue, MenuContext.ts, index.ts}
❌ presentation/actions/dropdownMenu/          (a menu names destinations, not one action)
```

---

## Declaration

### Component doc

#### [Renders](../../../lla/notation/documentation/documentation.md)

- must name the wayfinding shape — trail, pager, menu, outline.

### Construct

- must reuse the appropriate keyboard primitive for menus and composite widgets.
- must reuse dismissal behavior only when the navigation opens a dismissable surface.
- must render an `<a>` for a place and a `<button>` for a command, and expose `asChild` for the router link.

### Component name

- must end `*Menu` for a destination list behind a trigger — `DropdownMenu` · `ContextMenu`.
- must end `*Item` for one row of one; an item is a compound subpart
  ([architecture](../../../../shapes/app/architecture/architecture.md)).
- must name the shape, not the page it appears on — `Breadcrumb`, never `HeaderBreadcrumb`.

---

## Content

### Props

#### [The](../../../lla/notation/documentation/documentation.md)

- must take the current position as a prop — `isActive`, `current`, `page` — and never read the router itself.
- must stay generic over the item type when it renders a list.

### Slots

- must expose a slot per item so the caller renders the link with its own router component.

### Emits

#### [Fires when](../../../lla/notation/documentation/documentation.md)

- must emit the chosen destination and let the caller navigate — a nav never calls the router.

---

## Composition

- must follow the shared [composition contract](visual.md#composition-order).
- must preserve the underlying link's native navigation when reporting a selection.
- must provide a visible keyboard-reachable alternative to a context-only command menu.
- must name navigation landmarks and expose the current place through the applicable ARIA state.
- must keep rich menu panels distinct from menu-item roles; arbitrary controls do not become menu items.

---

## Neighbours

- [nav](../../components/nav/nav.md) — which one to reach for, and with what values
- [action](action.md) — the kind for a trigger that runs a command instead of moving
- [overlay](overlay.md) — the surface a menu or palette floats in
- [routing](../../../../shapes/app/routing/routing.md) — the route table a nav's destinations point at
- [visual kinds](visual.md) — every other kind, and the composition contract

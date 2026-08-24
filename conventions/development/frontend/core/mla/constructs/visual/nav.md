# Nav

*Last updated: 2026-08-23*

> A component whose whole job is moving the user somewhere — another place, another section, another command.
> Purpose — wayfinding is one kind, so a link row, a menu, and a palette share one contract and one a11y story.
> Use case — a sidebar, a breadcrumb trail, a pager, a right-click menu, a command palette.

## Gate

- must **move the user** — a component that changes a value is a [control](control.md), not a nav.
- must render its destinations as links when they are places, so middle-click and copy-link work.
- must expose a roving tab stop over its items ([primitive](primitive.md)); a list of separate tab stops is not a nav.
- must not own the destination list's source; a caller supplies the items.

```txt
✅ NavItem · Breadcrumb · Pagination · Menu · DropdownMenu · ContextMenu · CommandPalette · TableOfContents
❌ SegmentedControl        (it picks a value, not a destination — a control)
```

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

- must build item navigation on `RovingFocusGroup` and dismissal on `DismissableLayer`.
- must render an `<a>` for a place and a `<button>` for a command, and expose `asChild` for the router link.

### Component name

- must end `*Menu` for a destination list behind a trigger — `DropdownMenu` · `ContextMenu`.
- must end `*Item` for one row of one; an item is a compound subpart
  ([architecture](../../../../shapes/app/architecture/architecture.md)).
- must name the shape, not the page it appears on — `Breadcrumb`, never `HeaderBreadcrumb`.

```vue
<script setup lang="ts">
/** Renders a sidebar navigation row with an icon, a label, and a trailing slot. */
defineOptions({ name: 'NavItem', inheritAttrs: false });
defineProps<{ asChild?: boolean; isActive?: boolean }>();
</script>
```

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

```vue
<script setup lang="ts">
defineProps<{ isActive?: boolean }>();                       // ✅ position comes in as a prop
defineEmits<{ (e: 'select', href: string): void }>();        // ✅ the caller navigates
const route = useRoute();                                    // ❌ a nav reading the router itself
</script>
```

---

## Composition

- must be mounted by a [layout](layout.md) region or an [overlay](overlay.md) — a menu portals, a sidebar does not.
- must compose [display](display.md) and [indicator](indicator.md) inside an item — a count badge, a status dot.
- must not mount a [page](page.md), a [view](view.md), or a [field](field.md).

```txt
✅ AppShell → sidebar slot → NavItem → CountBadge
❌ NavItem → SettingsView        (navigating to a body by mounting it)
```

---

## Neighbours

- [nav](../../components/nav/nav.md) — which one to reach for, and with what values
- [action](action.md) — the kind for a trigger that runs a command instead of moving
- [overlay](overlay.md) — the surface a menu or palette floats in
- [routing](../../../../shapes/app/routing/routing.md) — the route table a nav's destinations point at
- [visual kinds](visual.md) — every other kind, and the composition ladder

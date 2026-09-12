# Page

*Last updated: 2026-09-10*

> The component the router mounts for one URL, owning the whole viewport under the app frame.
> Purpose — one component per URL carries the data fetch, the layout choice, and the sub-domain wiring.
> Use case — a new route; anything a user can bookmark, refresh, share, or land on from a search result.

## Gate

- must own a routed place, including a single-subject page.
- must preserve its route identity on refresh and direct navigation.
- must coordinate the page frame and application hooks needed by that place.
- may delegate a lazy region's data hook to a named feature owner; generic visual components receive data.
- must use a view or panel for a body that has no route ownership of its own.

---

## Location

### Group

- must take page placement from the owning app's [architecture](../../../../shapes/app/architecture/architecture.md).
- must sit in a `pages/` role-group — `presentation/{domain}/common/pages/`.
- must not ship from the SDK — the SDK ships the frame and the parts, the product ships the place.

```txt
✅ presentation/codes/common/pages/createCodePage/CreateCodePage.vue
❌ presentation/codes/core/design/CreateCodePage.vue       (a sub-domain cannot own a page)
```

---

## Declaration

### Component doc

#### [Renders](../../../lla/notation/documentation/documentation.md)

- must open the one-line doc with `Renders the … page.`, naming the place, not the widgets.

### Construct

- must make the route entry the file's default export ([vue SFC](../../../lla/constructs/vue/vue-sfc.md)).
- must be lazy-imported from the route table ([routing](../../../../shapes/app/routing/routing.md)).

### Component name

- must end `*Page` — a routed viewport owner takes no other suffix, whatever it composes.
- must name the place in the stem — `CodesList`, not `CodesPagePage`.

---

## Content

### Props

#### [The](../../../lla/notation/documentation/documentation.md)

- must take route inputs through the app router contract, including declared route props where that adapter supplies them.
- must validate route params and search state at the route boundary
  ([routing](../../../../shapes/app/routing/routing.md)).

### Slots

- must declare no slots — a page is a leaf of the route tree, not a wrapper.

### Emits

- must declare no emits — a page has no parent to hear them; navigation is the outward move.

---

## Composition

- must compose the parts the place needs; a small page needs no artificial view or sub-domain.
- must open an [overlay](overlay.md) for an action, and route to a sibling page for a place.
- must call `application/` hooks for data, never `integration/`
  ([architecture](../../../../shapes/app/architecture/architecture.md)).

```txt
✅ CodesListPage → AppShell → CodesTableView → EmptyState | LoadingState
❌ CodesListPage → codesApi.list()      (a page never reaches integration/ itself)
```

---

## Neighbours

- [view](view.md) — the swappable bodies a page mounts
- [layout](layout.md) — the frame a page renders inside
- [routing](../../../../shapes/app/routing/routing.md) — the route table, params, and code-splitting
- [visual kinds](visual.md) — every other kind, and the composition contract

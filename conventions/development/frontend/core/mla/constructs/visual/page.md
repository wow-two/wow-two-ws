# Page

*Last updated: 2026-08-19*

> The component the router mounts for one URL, owning the whole viewport under the app frame.
> Purpose — one component per URL carries the data fetch, the layout choice, and the sub-domain wiring.
> Use case — a new route; anything a user can bookmark, refresh, share, or land on from a search result.

## Gate

- must be reachable by **URL** — the address is the identity, so it survives a refresh and a paste into a new tab.
- must be a [view](view.md) or a [panel](panel.md) instead when only another component ever mounts it.
- must own the whole viewport under the app frame, deciding the [layout](layout.md) it renders inside.
- must compose two or more sub-domains — a single-subject body is a [view](view.md).
- must be the only place a route's data fetch starts; a child receives the result as props.

```txt
✅ CreateCodePage · CodesListPage · LoginPage · PricingPage · BlogPostPage
❌ ContentTabPage          (a tab body has no URL, so it is a panel)
```

---

## Location

### Group

- must live in the domain's `common/` slice — a page composes sub-domains, so it belongs to none.
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

```vue
<script setup lang="ts">
/** Renders the code builder page. */
defineOptions({ name: 'CreateCodePage' });
</script>
```

---

## Content

### Props

#### [The](../../../lla/notation/documentation/documentation.md)

- must declare no props — nothing mounts a page but the router, so there is no caller to pass any.
- must read route params and search state through the router hooks
  ([routing](../../../../shapes/app/routing/routing.md)).

### Slots

- must declare no slots — a page is a leaf of the route tree, not a wrapper.

### Emits

- must declare no emits — a page has no parent to hear them; navigation is the outward move.

```vue
<script setup lang="ts">
const { codeId } = useTypedSearchParams(CodeRouteSchema);   // ✅ params come from the router
const props = defineProps<{ codeId: string }>();            // ❌ no caller exists to pass this
</script>
```

---

## Composition

- must compose a [layout](layout.md), then [views](view.md) and [panels](panel.md) — never a bare grid of controls.
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
- [visual kinds](visual.md) — every other kind, and the composition ladder

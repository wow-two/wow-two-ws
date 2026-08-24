# Routing

*Last updated: 2026-08-23*

> How a wow-two React app defines routes — a declarative `RouteConfig` passed to the SDK-owned
> `createAppRouter` wrapper. Apps author routes; the wrapper owns the react-router machinery.
> Purpose — one routing model across every app, with cross-cutting behavior added in one place; pairs with
> [routing and responsive surfaces](../architecture/architecture.md).
> Use case — adding a place, guarding one, or deciding what the router wrapper owns rather than a page.

## Ownership

- must route with **`createAppRouter(routes)`** over `react-router-dom` v7 (data router) — never call
  `createBrowserRouter` / `<BrowserRouter>` / `<Routes>` directly.
- must add cross-cutting behavior in the wrapper, the single extension point — it injects
  `<ScrollRestoration>`, a root `errorElement` and the `*` → `NotFound`, and every app inherits them.
- must not keep view state in the URL hash — the data router owns real paths (permalinks depend on it).

---

## Home

- must author the wrapper **app-local in `bootstrap/router/`**, package-shaped — framework-only imports
  (`react` / `react-router-dom`, no `@/…`) — until a 2nd consumer.
- must combine it into the front SDK **`@wow-two-beta/ui`** (a `/router` subpath, a 1-line import swap) once a
  2nd consumer lands.
- must keep the SDK's *presentation* components router-free ([library](../../library/library.md)).

---

## The model — `AppRoute`

- must author routes as a `RouteConfig` (`ReadonlyArray<AppRoute>`):
  `{ path · index · element | lazy · layout · redirect · handle · children · errorElement · id }`.
- must code-split every **place** via `lazy: () => import('@/presentation/…/XPage')` — it accepts a `default`
  or a named `Component` export.
- must nest shared chrome via a **layout route** — `layout:` a `*Layout` in `bootstrap/` composing the SDK
  `AppShell` + `<Outlet>`.
- must attach per-route metadata via `handle: { crumb, title }`, read through `useMatches()`.
- must express a plain redirect as `redirect: '/path'`.

---

## Places and actions

- must read the doctrine at [architecture](../architecture/architecture.md) § *Routing and responsive surfaces*
  — which surface a place takes, which an action takes, and where responsiveness is decided.

---

## Composition

- must compose the shell in an app-owned `*Layout` (the layout route): the SDK `AppShell`
  (`@wow-two-beta/ui/presentation/layout`) with `<Outlet>` in `AppShell.Content`.
- must wire nav via **`<NavItem asChild><Link/></NavItem>`** — the SDK `NavItem` chrome forwarding to a router
  `<Link>`, active state from `useMatch`; reusable as `AppNavLink`.
- must not import a router in an SDK component — the app owns navigation.
- should keep `presentation/` pages router-agnostic — `bootstrap/` + the `*Layout` own `<Outlet>` /
  `<Link>` / `useParams`; a page takes value + callback props.

---

## Wrapper-provided (shipped)

- **`document.title` sync** — `createAppRouter(routes, { titleSuffix })` mounts a `DocumentTitle` in `AppRoot`;
  every navigation sets `document.title` to the deepest matched `handle.title`, falling back to the suffix
  alone when a route sets no `title` (e.g. `:id` detail routes).
- **route params** resolve via `useParams()` in the `*Page` — the wrapper adds no param plumbing.
- **baseline component names** — `AppRoot` · `AppLayout` · `AppErrorBoundary` · bare `NotFound` /
  `DocumentTitle` ([naming](../../../core/lla/notation/naming/naming.md) § *App-shell baselines*).

---

## Capability matrix

- must read what ships today in the SDK repo's `engineering/planning/capability-ledger.md`
  — a surface register lives beside its code, never in a convention.

---

## Neighbours

- [app](../app.md) — the shape this vector belongs to
- [architecture](../architecture/architecture.md) § *Routing and responsive surfaces* — places, actions, breakpoints
- [nav](../../../core/mla/constructs/visual/nav.md) — the kind a route is reached through
- [domains](../../../core/mla/domains/domains.md) — the capabilities a guard and a loader reach for

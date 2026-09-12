# Architecture

*Last updated: 2026-09-10*

> The slice tree a TypeScript app is built on — five Clean-Arch layers at `src/`, each sliced by domain.
> Purpose — one inward dependency direction, so a layer reads without its callers.
> Use case — placing a new file, or splitting a domain that has outgrown one folder.
> A package has no layers and no slices — its own layout is [library](../../library/library.md) § *Layout*.

## Layers [REQUIRED]

Dependencies: `presentation → application → domain`, `application → integration → domain`.
`bootstrap` composes all; application imports only the same-domain endpoint or a shared integration contract.

| Layer | Holds | Backend peer |
|---|---|---|
| `bootstrap/` | the composition root — app entry, providers, routes and layouts | Host |
| `presentation/` | components and pages; renders, never fetches | Presentation |
| `application/` | orchestration hooks, view-model mappers, submit orchestration, client state | Application |
| `domain/` | types, enums, extensions, pure ops (`build` · `parse` · `validate`); depends on nothing | Domain |
| `integration/` | clients, endpoints, wire codecs and DTOs; no component runtime | Infrastructure |

- must not import another domain slice directly; lift genuinely shared contracts into that layer's `common/`.
- must keep `common/` independent of concrete domain slices; `bootstrap/` may compose all slices.
- must read these five as a **product's** tree; an SDK package groups by kind and hangs capability modules off
  its root ([visual kinds](../../../core/mla/constructs/visual/visual.md) § *Placement*).
- must lint the declared layer and slice boundaries; test an illegal edge in the rule configuration.

---

## The folders a domain holds [REQUIRED]

A role-group hangs off a **subject**, never off a bare layer: an extension extends something, a model models
something, and the parent folder names what. The path is always `{layer}/{domain}/{role-group}/`, matching the
backend's `Api/{Domain}/Controllers/`
([architecture](../../../../backend/dotnet/shapes/service/architecture/architecture.md)
§ *Where a folder is created*).

| Layer | Role-groups a domain may open there | Backend peer's set |
|---|---|---|
| `domain/` | `models/` · `enums/` · `constants/` · `extensions/` · `builders/` · `parsers/` · `validators/` | `Entities/` `Enums/` `Constants/` `Extensions/` |
| `application/` | `hooks/` · `mappers/` · `models/` · `stores/` · `constants/` | `UseCases/` `Models/` `Constants/` |
| `integration/` | `clients/` · `endpoints/` · `interceptors/` · `models/` (holds `Dto`) | the foundation services |
| `presentation/` | the seven visual groups · `pages/` · `hooks/` · `extensions/` | `Controllers/` `Requests/` `Models/` |
| `bootstrap/` | entry files flat; named composition groups when needed; no domain slices | Host |

- must open a role-group under a domain or a sub-domain, never directly under a layer — `presentation/codes/
  extensions/`, never `presentation/extensions/`, because the second names nothing the extension extends.
- must read a repeated folder name by its layer — `models/` holds a `*Model` in `application/` and a `*Dto` in
  `integration/`, and the two never mix. This is the backend's rule, unchanged.
- must open a role-group only once it holds two files; one file stays flat and is its own group.
- must not invent a role-group outside its layer's set — a file fitting none of them belongs to another layer.
- must put a role-group serving two or more domains in that layer's `common/` slice (§ *Domains*).

---

## Domains

- must slice `domain/`, `application/`, `integration/` and `presentation/` by domain; bootstrap is exempt.
- must give each sliced layer a `common/` slice when two or more domains share its contract.
- must repeat a domain in every layer it touches — `presentation/codes/` · `domain/codes/`.

---

## Sub-domains

- must divide a domain into cohesive sub-domains — `codes` → `core` (the builder) · `content` (per type).
- must fold a concern into a sub-domain once it owns three or more components; keep it flat below that.
- may divide a sub-domain again by concern — `presentation/codes/core` → `design` · `shape` · `preview`.
- may hold components directly; a `components/` wrapper separates non-component files only, one style per domain.
- must name a folder either a sub-domain (a model noun — `core` · `design`) or a role-group (a plural role
  noun — `models/` · `enums/` · `pages/` · `hooks/` · `mappers/`), never the activity (`validation/`).
- must not treat a role-group as a sub-domain.
- must put in domain-`common/` whatever belongs to no sub-domain — shared components, composition role-groups.
- must place a routed page in the `pages/` role-group of the domain that owns it — `codes/pages/`.
- must place a page in `presentation/common/pages/` when no domain owns it, such as a cross-domain dashboard.

---

## Files

- must name files, folders and slice barrels per [naming](../../../core/lla/notation/naming/naming.md).
- must suffix a component by its [kind](../../../core/mla/constructs/visual/visual.md), a seam by a
  [headless role](../../../core/mla/constructs/behavior/headless-suffixes.md).
- must name a hook per [hooks](../../../core/mla/constructs/behavior/hooks.md); live query state follows
  [data](../../../core/mla/domains/data/state-and-data.md#state), separately from operation outcomes.
- must export `{domain}Api` from `integration/{domain}`, its fns `{verb}{Noun}`.
- must name an extension object `{Noun}Extensions` (`as const`); constant casing is
  [naming](../../../core/lla/notation/naming/naming.md)'s.

### Component files

A product may keep a component flat; a package never may
([library](../../library/library.md) § *Layout*).

- may keep components as flat files grouped by concern — `core/design/FillControls.tsx`; that concern folder's
  `index.ts` is then the public API.
- must give a component its own folder once it grows a sibling that is not internal to it.
- must take the rest of the component file's shape — internal sub-components, member order, imports — from
  [constructs](../../../core/mla/constructs/constructs.md) § *Folder*.

---

## Routing and responsive surfaces

- must take places, route parameters, app-shell names and navigation behavior from [routing](../routing/routing.md).
- must put responsive presentation in components while preserving the route's place identity.

---

## Slice tree

```text
src/
  bootstrap/     main.ts · AppRoot.vue · AppLayout.vue · index.css
    router/      routes.ts · route parameter adapters
  integration/
    common/      shared client/transport contracts
    codes/       endpoint functions · wire codecs · models/
  domain/
    codes/       enums/ · models/ · extensions/
  application/
    codes/       hooks/ · mappers/ · models/
  presentation/
    common/      pages/ (cross-domain routes)
    codes/       pages/ (CreateCodePage · CodesListPage)
      design/    controls and their internal subparts
```

---

## Neighbours

- [app](../app.md) — the shape this vector belongs to
- [boundaries](boundaries.md) — what stays in the app, what extracts to the SDK, how the app is packaged
- [compound](../../../core/mla/constructs/compound/compound.md) — the root-and-subpart rules a slice's folder holds
- [constructs](../../../core/mla/constructs/constructs.md) — the kinds each slice holds
- [models](../../../core/mla/constructs/data/models.md) — the model types a slice declares, and variant-set dispatch
- [routing](../routing/routing.md) — how a place becomes a route, and the router wrapper that owns it
- [domains](../../../core/mla/domains/domains.md) — the capabilities an app consumes

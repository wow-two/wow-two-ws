# Architecture

*Last updated: 2026-08-20*

> The slice tree a TypeScript app is built on — five Clean-Arch layers at `src/`, each sliced by domain.
> Purpose — one inward dependency direction, so a layer reads without its callers.
> Use case — placing a new file, or splitting a domain that has outgrown one folder.
> A package has no layers and no slices — its own layout is [library](../../library/library.md) § *Layout*.

## Layers [REQUIRED]

Dependency runs inward: `presentation → application → domain`, `integration → domain`.
`bootstrap` wires all.

| Layer | Holds | Backend peer |
|---|---|---|
| `bootstrap/` | the composition root — `App.tsx` · `main.tsx` · providers · `routes.tsx` · layouts | Host |
| `presentation/` | components and pages; renders, never fetches | Presentation |
| `application/` | orchestration hooks, view-model mappers, submit orchestration, client state | Application |
| `domain/` | types, enums, extensions, pure ops (`build` · `parse` · `validate`); depends on nothing | Domain |
| `integration/` | HTTP client, endpoint fns, interceptors, auth; returns wire DTOs, no React | Infrastructure |

- must not import sideways — share via `common/` or lift a layer; `common/` and `bootstrap/` are exempt.
- must read these five as a **product's** tree; an SDK package groups by kind and hangs capability modules off
  its root ([visual kinds](../../../core/mla/constructs/visual/visual.md) § *Placement*).
- should lint the direction (ESLint `no-restricted-paths`) — unlinted layering rots.

---

## Domains

- must slice every layer by domain — `codes` · `identity` · `billing` · `marketing`.
- must give each layer a `common/` slice for anything two or more domains use.
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
- must place it in domain-`common/pages/` only when no domain owns it — a 404, a dashboard spanning several.

---

## Files

- must name files, folders and slice barrels per [naming](../../../core/lla/notation/naming/naming.md).
- must suffix a component by its [kind](../../../core/mla/constructs/visual/visual.md), a seam by a
  [headless role](../../../core/mla/constructs/behavior/headless-suffixes.md).
- must name a hook per [hooks](../../../core/mla/constructs/behavior/hooks.md) § *Naming*; a data
  `use{Entity}` returns a [result](../../../core/mla/constructs/data/result.md), never a bespoke state bag.
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

A place is a URL, and a route renders the same place at every breakpoint.

- must give a place one route and a `*Page` — deep-linkable, refreshable, shareable.
- must give an action a routeless `*Modal` — ephemeral, so no URL and no cross-size mismatch.
- must not render one place as a modal on desktop and a page on mobile — that breaks copy-paste, refresh, back.
- must resolve a direct hit, refresh or new tab on a place-route to a standalone page; a desktop
  modal-over-context is allowed only through intercepting routes that keep that fallback.
- must put responsiveness in the component, not the route — a `*Modal` presents as `Modal` or `BottomSheet`.

---

## Slice tree

```
src/
  bootstrap/     App.tsx · main.tsx · index.css · AppLayout · routes.tsx · providers
  integration/   client.ts · interceptors.ts · auth.ts · common/ · codes/ identity/ billing/
  domain/        common/ · identity/ billing/
                 codes/ core/    (module · finder · preview · rule types + pure ops)
                        content/ (url · wifi · vcard = { def, Content, build, parse }) · registry.ts
  application/   common/ · identity/ (useAuth) · billing/
                 codes/  (useCodes · useCodeBuilder · toCodeRow mapper)
  presentation/  common/ · identity/ billing/ marketing/
                 codes/ core/     design/ (FillControls) · shape/ (ShapeControls) · preview/ (QrPreview)
                        content/  components/ (UrlForm · WifiForm) · ContentTypeForm
                        common/pages/   (CreateCodePage · CodesListPage)
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

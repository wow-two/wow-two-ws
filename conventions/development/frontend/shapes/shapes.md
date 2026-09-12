# Shapes

*Last updated: 2026-08-24*

> What differs by **deliverable** — the kind of thing being built, not how far a rule reaches.
> Purpose — an app and a component library share every naming, kind and notation rule, and almost no structure.
> Use case — starting a repo, placing a folder in the source tree, or wiring how the thing is built and shipped.

## The shapes

| Shape | Is | Status |
|---|---|---|
| [app](app/app.md) | a product frontend a browser loads — routes, pages, a composition root | written |
| [library](library/library.md) | a package another frontend installs and imports | written |

- must not coin a third shape — a monorepo `@{brand}/*` package is a library, and an SDK is a published one.

### The test

Not *does the rule change between deliverables* — a rule can be fixed forever and still belong here.
**Does the rule have a subject when this shape is absent?**

| Rule | Subject without the shape | Home |
|---|---|---|
| a route renders the same place at every breakpoint | none; only an app has places | shape — app |
| `index.css` lives in `bootstrap/`, two levels up from `node_modules` | none; only an app boots | shape — app |
| the package groups by kind, capability modules off its root | none; only a package has a root | shape — library |
| a `Modal` is named `{Noun}Modal` | an app names them too | core |
| a prop is `readonly`, an array prop `ReadonlyArray<T>` | an app declares props too | core |
| a component's doc block opens `Renders …` | both write the block | core |

- must file a rule by that test, not by whether it is stable — the layer direction never changes, and still has
  no subject in a package that ships no layers.
- must not read a constant rule as a core rule.
- must leave a rule in `core/` when both shapes have a subject for it, even when each answers differently — the
  doc states both answers in one place.

---

## Reading a shape

- must read [core](../core/core.md) first — every rule there holds here too, unchanged.
- must not restate a core rule in a shape; a shape states only what its deliverable changes.

---

## The vectors inside a shape

A shape is cut by vector, the same way a domain is. Each answers one question about the deliverable.

| Vector | Answers |
|---|---|
| `architecture/` | how the source is arranged inside it — the layers, the slices, the outer edge |
| `platform/` | how it is built, styled, served and previewed |
| `routing/` | how a place becomes a URL, and what owns the router |
| `delivery/` | how it is packaged and published — a `dist`, an `exports` map, a version |

- must give a vector its own folder, even when it holds one doc.
- must leave a vector absent rather than empty — a library has no `routing/`, so it has no `routing/` folder.
- must not put a placement rule in `core/` — which folder a `presentation/` group is created in is a shape's
  answer, and the kind doc names only the group.

---

## Neighbours

- [core](../core/core.md) — the other cut: how far a rule reaches
- [frontend conventions](../frontend-conventions.md) — the index over both cuts

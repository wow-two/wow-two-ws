# App

*Last updated: 2026-08-19*

> A product frontend a browser loads — a composition root, routed places, a build, a dev server.
> Purpose — the shape we ship today, and the only one whose vectors are written out.
> Use case — placing a file in `src/`, adding a route, wiring the build, or deciding what leaves for the SDK.

## Vectors

| Vector | Lead | Status |
|---|---|---|
| [architecture](architecture/architecture.md) | how the source is arranged, and where its outer edge runs | written |
| [platform](platform/platform.md) | how it is styled, served and previewed | written |
| [routing](routing/routing.md) | how a place becomes a URL, and what owns the router | written |
| [delivery](delivery/delivery.md) | build inputs, hosting, caching and verification | written |

- must take every naming, kind, notation and domain rule from [core](../../core/core.md) unchanged.
- must answer **where a folder is created** here — a kind doc names `overlays/`, this shape says the layer and
  the slice that hold it ([architecture](architecture/architecture.md) § *Domains*).
- must not read a rule here as a library rule — a package has no layers, no places and no composition root
  ([library](../library/library.md)).

---

## Neighbours

- [shapes](../shapes.md) — the test that put these docs here rather than in `core/`
- [library](../library/library.md) — the other shape, and what an app extracts into it
- [core](../../core/core.md) — every rule that holds whichever shape is being built

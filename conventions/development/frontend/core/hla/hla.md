# HLA — between our own frontends

*Last updated: 2026-09-10*

> High-level architecture: rules that only exist once one frontend has to agree with another at runtime.
> Purpose — keep fleet-shaped decisions out of `mla/`, where a single app would silently adopt them as defaults.
> Use case — reach here when a rule needs both apps to obey it, and we own both apps.

## The boundary

- **`hla/` when we own both ends** — a micro-frontend host/remote contract, a shared runtime, cross-app route
  ownership.
- **`mla/` when we own one end** — a third-party widget is *adapted*, never contracted. Its client and its limits
  live in `mla/domains/`.

A monorepo `@{brand}/*` package is **not** `hla/`: it is compiled into one app, so its rules are
[boundaries](../../shapes/app/architecture/boundaries.md).

- must classify SDK rules by their reach, not their package name; consuming a package is not an `hla/` contract.
- must put agreements between separately deployed frontends here when both ends are ours.

---

## Named ahead of its contents

- may add host/remote version-skew, shared-runtime or cross-app route/session contracts when both ends require them.
- must keep single-deliverable layout and publishing in [shapes](../../shapes/shapes.md).

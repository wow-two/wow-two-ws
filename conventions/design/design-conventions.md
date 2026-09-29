# Design conventions

*Last updated: 2026-09-29*

> What — product UI exploration and WoW2 family identity: shared methods and rules; product-specific choices stay in their owning guides. Index only — open the leaf.
> Purpose — repeatable design decisions and durable approved identities.
> Use case — starting a screen, redesign, component or WoW2 family logo.

## Index

| Need | File |
|---|---|
| Design exploration — variant-driven method (a few in-context options → pick → lock → cascade → spec) · other modes · mode-selection · per-app spec shape | [research/design-exploration.md](research/design-exploration.md) |
| Logo system — family scope · compositions · exact parent endorsement · masters · export verification | [identity/logo-system.md](identity/logo-system.md) |

---

## Per-app specs

- the durable output of exploration is a **per-app design spec**, not this folder.
- location — `workbench/{repo}/platform/research/design-research/design-research.md` (or the repo's analogue).
- shape — screens (device targets, [responsive](../development/frontend/shapes/app/responsive/responsive.md)) · token tables (light + dark) · semantic→`@wow-two-beta/ui` mapping · type · layout/shape · component rules · usage don'ts · iterate-next.
- first adopter — `forever-pin`.

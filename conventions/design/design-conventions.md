# Design conventions

*Last updated: 2026-06-24*

> What — how we design product UI across the ecosystem: the shared exploration method + where each app's visual spec lives. Index only — open the leaf.
> Purpose — one repeatable way to arrive at UI so every app's look is decided the same way, fast and comparably.
> Use case — starting any new screen, redesign, or component anywhere under `wow-two-ws/`.

## Index

| Need | File |
|---|---|
| Design exploration — variant-driven method (a few in-context options → pick → lock → cascade → spec) · other modes · mode-selection · per-app spec shape | [research/design-exploration.md](research/design-exploration.md) |

---

## Per-app specs

- the durable output of exploration is a **per-app design spec**, not this folder.
- location — `workbench/{repo}/platform/research/design-research/design-research.md` (or the repo's analogue).
- shape — token tables (light + dark) · semantic→`@wow-two-beta/ui` mapping · type · layout/shape · component rules · usage don'ts · iterate-next.
- first adopter — `smart-qr-poc`.

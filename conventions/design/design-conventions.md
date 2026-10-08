# Design conventions

*Last updated: 2026-10-01*

> Product UI exploration, screen copy and WoW2 family identity — shared methods and rules; a product's own
> choices stay in its design spec. Index only — open the leaf.

## Index

| Need | File |
|---|---|
| Design exploration — variants per decision, pick, lock, cascade, persist to the spec; other modes | [research/design-exploration.md](research/design-exploration.md) |
| UI copy — how many words a screen carries; sign-in, empty, confirm and loading text | [content/ui-copy.md](content/ui-copy.md) |
| Logo system — family scope, compositions, parent endorsement, masters, export verification | [identity/logo-system.md](identity/logo-system.md) |

---

## Per-app specs

- must persist the output of exploration in a per-app design spec, never in this folder or in chat.
- must keep it at `engineering/research/design-research/design-research.md` in the product repo.
- must open it with `## Screens` — the device targets
  ([responsive](../development/frontend/shapes/app/responsive/responsive.md#device-targets)).
- must carry token tables for light and dark, and the mapping from each semantic token to `@wow-two-beta/ui-vue`.
- must carry type, layout and shape, component rules, usage don'ts and the next iteration.
- must apply its tokens through the app's stylesheet
  ([styling](../development/frontend/shapes/app/platform/styling.md#brand-tokens)).

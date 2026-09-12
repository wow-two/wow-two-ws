# Platform

*Last updated: 2026-08-19*

> How an app is built, styled, served and previewed — everything between the source tree and a loaded page.
> Purpose — a package has none of this, so none of it may sink into `core/`.
> Use case — wiring a new app's `vite.config.ts` or `index.css`, or fixing a build that renders half-styled.

## Files

| File | Covers |
|---|---|
| [styling](styling.md) | the Tailwind v4 wiring in `index.css`, brand tokens, the dark-mode switch |
| [dev-server](dev-server.md) | HTTPS through mkcert, the `/api` proxy, previewing a route |
| [assets](assets.md) | images, fonts and public files |
| [delivery](../delivery/delivery.md) | reproducible builds, host handoff and caching |

- must take the utility, token and variant rules themselves from `core/` — this vector wires them, and states
  none of them ([tailwind](../../../core/lla/constructs/tailwind/tailwind.md)).

---

## Delivery

- must follow [app delivery](../delivery/delivery.md) for build outputs, supported targets and the host handoff.
- must follow [assets](assets.md) for images, fonts and public URLs.

---

## Neighbours

- [app](../app.md) — the shape this vector belongs to
- [architecture](../architecture/architecture.md) — the `bootstrap/` layer the wiring files live in

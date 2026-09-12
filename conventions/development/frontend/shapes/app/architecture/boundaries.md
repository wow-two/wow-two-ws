# Boundaries

*Last updated: 2026-09-10*

> The app's outer edge — what stays inside it, what extracts to a package, and how the repo is shaped.
> Purpose — in-app reuse and SDK reuse run on opposite triggers, and mixing them strands generic code.
> Use case — deciding whether a new surface belongs to the product, to a repo package, or to the SDK.

## Restraint [REQUIRED]

- must start at the page, and extract a shared component or hook **within the app** only once a second
  consumer is real — no speculative widgets.
- applies to in-app extraction only; the SDK boundary runs the opposite trigger, below.

---

## SDK extraction

The trigger is genericness, not consumer count — the SDK is shared across the portfolio, so the second
consumer is a matter of time, not of chance.

- must extract a surface to `@wow-two-beta/ui` (or `ui-vue`) as soon as it is generic — one consumer is enough.
- must not wait for a second app; "no other app uses it yet" is not a reason to keep it in the product.
- must extract at the earliest point it is generic — a later extraction pays migration in every app that
  copied it meanwhile.
- must keep in the app only what encodes what the product **is** — its business logic, its brand surface.
- may build inline first when speed matters, and must extract in the pairing Adoption version.
- must fix the SDK rather than work around a gap in a product — beta-forever, so publish and repin.
- landing, pricing, FAQ and blog chrome is generic; a product-specific hero or demo is not.

---

## Packaging

Two shapes, by app count, both under `engineering/codebase/{slug}.frontend-services/`
(`@{brand}` = the repo's package scope).

- must default to a **single app** — one Vite app with the layered `src/`, no workspace, until a second app
  or genuine cross-app reuse appears.
- must shape a **multi-app repo** as a pnpm workspace — `packages/{common,ui,domain}` (`@{brand}/*`) plus
  lowercase app folders, each with the same layered `src/`.
- must keep `@{brand}/ui` dumb (no data, context or storage), `@{brand}/common` for shared hooks, utils and
  identity, `@{brand}/domain` for pure types and enums with no component runtime.
- must extract to a repo-local package only once two apps in that repo need it.
- must keep only **product-specific** components in a repo's `@{brand}/ui` — a generic one goes upstream to
  `@wow-two-beta/ui` immediately.

---

## Application ports

- may declare an application-owned port when substituting infrastructure is needed; bootstrap supplies its implementation.
- must otherwise use the same-domain endpoint edge defined by [architecture](architecture.md#layers-required).

---

## Neighbours

- [app](../app.md) — the shape this vector belongs to
- [architecture](architecture.md) — the layers and the slice tree a surface is extracted from
- [library](../../library/library.md) — what the extracted surface becomes, and how that package is laid out
- [dev-server](../platform/dev-server.md) — how the app is served while that work happens
- [between our own frontends](../../../core/hla/hla.md) — the scope above, once a second frontend exists

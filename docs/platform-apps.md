# WoW 2.0 — Platform Apps, In Order

*Last updated: 2026-10-25*

> The order the wow-two platform apps get built and shipped — one list to focus on, top down. Scope: the internal
> apps every product stands on (ops, observability, backbone services). Products and ventures live in the
> ventures registry; the SDKs are not apps — they grow with every app ([dev cycle](../conventions/development/dev-cycle.md)).
> Why each brick exists and build-vs-buy: [platform roadmap](platform-roadmap.md) · forms: [platform model](platform-model.md).
> Open cross-cutting choices, ranked: [platform decisions](platform-decisions.md).

## Rules

- must ship the top unshipped app (its ship gate below) before starting the next app's own repo.
- may build a later app's client side in the SDK early when a shipping app needs it — the `/reporting` client
  landed 2026-09-29 ahead of Feedbacks.
- must route SDK gaps any app hits to the SDK at once — [dev cycle](../conventions/development/dev-cycle.md)
  § SDK change loop — never queue them behind the next app.
- must change the order only on the developer's decision, recorded under *Decisions*.

---

## Order

| # | App | Repo | What it is | State 2026-09-29 (rows 1 and 8: 2026-10-19; 2 and 3: 2026-10-21; 16: 2026-10-24; 17: 2026-10-25) | Ship gate | Needs |
|---|---|---|---|---|---|---|
| 1 | **Wheelhouse** | `wow-two-platform.wheelhouse` | deploy + ops control plane: products, servers, domains, deploys | v0.5 in progress: platform model built; infrastructure automation planned | a product deployed to a VPS from it, with rollback, domain and live logs | — |
| 2 | **Identity** | `wow-two-platform.identity` | own user store, OIDC provider, hosted sign-in, admin console; three forms ([spec](../ideas/identity-service-spec.md)) | SDK identity steps 1–9 done; no OIDC server; Ocharo first | two apps sign in through it | 1 |
| 3 | **File Storage** | `wow-two-platform.storage.file` | files, image variants, signed URLs, quotas, console; three forms ([spec](../ideas/file-storage-service-spec.md)) | SDK `Storage/` and `Media/Images` built; repo empty | two apps store and serve files through it | 2 |
| 4 | **Secrets Vault** | `wow-two-platform.secrets-vault` | envelope-encrypted secrets store + UI; env injection | Form 2 built | Wheelhouse deploys read their env from it; Form 1 wireable; hardened | 1 |
| 5 | **Feedbacks** | `wow-two-platform.feedbacks` | incident reports → issues; triage inbox ([spec](../ideas/feedbacks-spec.md)) | client in the fe sdk `/reporting`; app not started | one app's Report button lands grouped reports in its inbox | 1, 4 |
| 6 | **Logs** | `wow-two-platform.logs` | structured log store + `/logs` viewer, search by trace id ([analysis](../ideas/logging-analysis.md)) | SDK emits OTel; no store | Feedbacks issue → one click → the request's log lines | 1, 4 |
| 7 | **Monitoring** | `wow-two-platform.monitoring` | uptime and health checks, Telegram alerts, domain/SSL expiry; dashboards bought (Grafana/SigNoz) | Wheelhouse spec P3 only | a downed product or expiring domain alerts before a user notices | 1, 6 |
| 8 | **Pipelines** | `wow-two-platform.pipelines` | reusable GitHub Actions: build · test · pack · publish · deploy | `v0.8.1` shipped; Wheelhouse, the canary and Ocharo call it | every active repo runs the shared workflows | — |
| 9 | **`wow` CLI** | new | `wow new` / `wow add <brick>` over `product-template` + `create-repo` | template + skill | a new product from zero to deployed in one command | 1, 8 |
| 10 | **Notifications** | new | multi-channel: email · Telegram · push · in-app (build thin or wrap Novu) | email + Telegram in the SDK | one app sends through every channel from one call | 2 |
| 11 | **Audit Log** | new | standalone audit trail, harvested from the vault's hash chain | inside Secrets Vault | a second app writes and verifies its trail | 4 |
| 12 | **Admin** | new | turnkey per-product back-office on the fe sdk + Identity | — | one product's admin built from it | 2 |
| 13 | **Docs site** | new | the platform's knowledge site (Starlight / Docusaurus) | — | conventions + SDK docs published | — |
| 14 | **FlowDeck** | new | visual request-flow debugger over live traces ([spec](../ideas/flowdeck-spec.md)) | idea | one backend's flows browsable live | 6 |
| 15 | **AI Gateway** | `wow-two-platform.templates.ai` | shared LLM proxy: keys, routing, caching | skeleton | two apps share keys and a cache through it | 2, 4 |
| 16 | **Events** | `wow-two-platform.events` | shared event catalog, sources and harvesting, per-organization tracking; three forms ([spec](../ideas/events-service-spec.md)) | design ready ([spec](../ideas/events-service-spec.md)); built in a WoW2 chat, Desk integrates after | two products track events through it | 2, 17 |
| 17 | **Harvest** | new, grown from ListingShelf | 24/7 harvester: scheduled pipelines capture sources and extract records into a consumer's schema, then deliver them | ListingShelf pipelines, runs and captures | Events and one other product receive harvested records | 15 |

---

## Backbone — not queued

- the be sdk (`wow-two-sdk-beta.be`) and the fe sdk (`wow-two-sdk-beta.fe`) are the substrate; they move with every app.
- infra bought, not built: Traefik (gateway), GHCR, Cloudflare, Porkbun, Hetzner — wrapped by Wheelhouse.

---

## Deferred — buy on a named trigger

| Capability | Trigger | Pick |
|---|---|---|
| Billing / metering | a product earns money | Stripe (+ Lago) |
| Durable workflows | an app needs async sagas beyond the SDK messaging layer | Temporal |
| Search | an app outgrows Postgres full-text | Meilisearch |
| Product analytics | a product needs funnels | Plausible / Umami via Wheelhouse |
| Developer portal | the registry doc + CLI stop scaling | Backstage |

---

## Legacy apps — decide, not ranked

- `Feedback.Analyzer`, `DDLParser`, `StudyMate`, AirBnb clone — still in the old `WoW-2-0-Projects` org; migrate
  into `wow-two-apps` or archive, one decision each.

---

## Decisions

- 2026-09-29 — developer set #1 Wheelhouse, #2 Secrets Vault; Feedbacks, Logs and Monitoring follow as the
  observability set, then the backbone services.
- 2026-10-21 — developer chose to build Identity (own store; Ocharo first, phone + Telegram bot code) and
  File Storage, each in the three [capability forms](../conventions/development/capability-forms.md), and moved
  them to #2 and #3, right after Wheelhouse.
- 2026-10-21 — Identity: OpenIddict for the protocol on the SDK's own store; one instance per owner, Ocharo
  running its own; one person per instance with roles per organization and app permissions as claims.
- 2026-10-24 — developer chose to move Ocharo Desk's Events into a shared SDK module now (Form 1), with the
  service form once a second product tracks events.
- 2026-10-25 — developer chose one standardized Harvest service for every scheduled capture, grown from
  ListingShelf; Events consumes it, and the Events service is built in its own WoW2 chat.
- 2026-10-25 — File Storage runs one instance per owner: WoW2's own instance serves Harvest's captures and the
  Events catalogs' media; each product (Ocharo) keeps its own for its media.

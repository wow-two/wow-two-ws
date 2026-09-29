# WoW 2.0 — Platform Apps, In Order

*Last updated: 2026-09-29*

> The order the wow-two platform apps get built and shipped — one list to focus on, top down. Scope: the internal
> apps every product stands on (ops, observability, backbone services). Products and ventures live in the
> ventures registry; the SDKs are not apps — they grow with every app ([dev cycle](../conventions/development/dev-cycle.md)).
> Why each brick exists and build-vs-buy: [platform roadmap](platform-roadmap.md) · forms: [platform model](platform-model.md).

## Rules

- must ship the top unshipped app (its ship gate below) before starting the next app's own repo.
- may build a later app's client side in the SDK early when a shipping app needs it — the `/reporting` client
  landed 2026-09-29 ahead of Feedbacks.
- must route SDK gaps any app hits to the SDK at once — [dev cycle](../conventions/development/dev-cycle.md)
  § SDK change loop — never queue them behind the next app.
- must change the order only on the developer's decision, recorded under *Decisions*.

---

## Order

| # | App | Repo | What it is | State 2026-09-29 | Ship gate | Needs |
|---|---|---|---|---|---|---|
| 1 | **Wheelhouse** | `wow-two-platform.wheelhouse` | deploy + ops control plane: products, servers, domains, deploys | v0.3 built; IA pass open | a product deployed to a VPS from it, with rollback, domain and live logs | — |
| 2 | **Secrets Vault** | `wow-two-platform.secrets-vault` | envelope-encrypted secrets store + UI; env injection | Form 2 built | Wheelhouse deploys read their env from it; Form 1 wireable; hardened | 1 |
| 3 | **Feedbacks** | `wow-two-platform.feedbacks` | incident reports → issues; triage inbox ([spec](../ideas/feedbacks-spec.md)) | client in `ui-vue` `/reporting`; app not started | one app's Report button lands grouped reports in its inbox | 1, 2 |
| 4 | **Logs** | `wow-two-platform.logs` | structured log store + `/logs` viewer, search by trace id ([analysis](../ideas/logging-analysis.md)) | SDK emits OTel; no store | Feedbacks issue → one click → the request's log lines | 1, 2 |
| 5 | **Monitoring** | `wow-two-platform.monitoring` | uptime and health checks, Telegram alerts, domain/SSL expiry; dashboards bought (Grafana/SigNoz) | Wheelhouse spec P3 only | a downed product or expiring domain alerts before a user notices | 1, 4 |
| 6 | **Identity** | `wow-two-platform.identity` | central OIDC IdP / SSO — one Google client for the fleet ([spec](../ideas/identity-service-spec.md)) | SDK identity rebuild steps 1–9 done | two apps sign in through it | 2 |
| 7 | **Pipelines** | `wow-two-platform.pipelines` | reusable GitHub Actions: build · test · pack · publish · deploy | skeleton | every active repo runs the shared workflows | — |
| 8 | **`wow` CLI** | new | `wow new` / `wow add <brick>` over `product-template` + `create-repo` | template + skill | a new product from zero to deployed in one command | 1, 7 |
| 9 | **Notifications** | new | multi-channel: email · Telegram · push · in-app (build thin or wrap Novu) | email + Telegram in the SDK | one app sends through every channel from one call | 6 |
| 10 | **Audit Log** | new | standalone audit trail, harvested from the vault's hash chain | inside Secrets Vault | a second app writes and verifies its trail | 2 |
| 11 | **Admin** | new | turnkey per-product back-office on `ui-vue` + Identity | — | one product's admin built from it | 6 |
| 12 | **Docs site** | new | the platform's knowledge site (Starlight / Docusaurus) | — | conventions + SDK docs published | — |
| 13 | **FlowDeck** | new | visual request-flow debugger over live traces ([spec](../ideas/flowdeck-spec.md)) | idea | one backend's flows browsable live | 4 |
| 14 | **AI Gateway** | `wow-two-platform.templates.ai` | shared LLM proxy: keys, routing, caching | skeleton | two apps share keys and a cache through it | 2, 6 |

---

## Backbone — not queued

- `wow-two-sdk.backend.beta` and `wow-two-sdk-beta.ui` (`ui-vue`) are the substrate; they move with every app.
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

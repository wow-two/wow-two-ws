# WoW 2.0 — Platform Roadmap (Ranked Brick Backlog)

*Last updated: 2026-06-20*

> What platform bricks to build next, ranked by **consumers-unblocked-per-unit-effort**. The *ranking framework* is verified platform-engineering principles (cited). The *specific capability list, tool picks, and form calls* are engineering judgment grounded in current repo state — **not** independently verified (the deep-research verify pass was heavily rate-limited; see Provenance).
> Companions: `docs/platform-model.md` (the 3 distribution forms) · `docs/wow-two-refinement.md` (vision).

## Provenance — verified vs judgment

- **Verified (cited — CNCF + Dapr primary sources):** the 5 governing principles below. Only 6/25 claims survived 3-vote adversarial verification; all from vendor-neutral foundation docs.
- **NOT verified this round:** per-capability tool picks (Keycloak / OpenIddict / Temporal / …), the identity-brokering architecture, the sidecar/library→service evolution specifics, concrete anti-pattern lists. The verify pass hit heavy API rate-limiting → those claims **abstained (0-0), not refuted** — "plausible, re-verify before committing." **Treat the tool column as a shortlist, not a verdict.**
- **Grounded (repo-sourced):** the current-state column, from a direct sweep of the platform/sdk repos.

## Governing principles (verified)

1. **It's an Internal Developer Platform — treat it as an internal *product*, not a pile of libraries.** The catalog (`backend.beta` + `beta.ui` + `secrets-vault` + `drydock` + `product-template`) is the product; its users are your own product teams. `[CNCF-Platforms]`
2. **Buy/wrap before build.** *"Build the thinnest viable platform layer over implementations from managed providers; build a capability yourself only when it's not available elsewhere."* Most bricks = thin integration layers, not from-scratch services. `[CNCF-Platforms]`
3. **Sequence undifferentiated + frequently-required first.** *"Pipelines, databases and observability may be a good place to start."* For wow-two that's **CI/CD, secrets, observability, and the central IdP** (every app needs auth). `[CNCF-Platforms]`
4. **Don't chase max maturity — problem-driven MVP per brick.** recognize → MVP → iterate → scale. *"Each additional level of maturity costs more funding and people's time; reaching the highest should not be a goal."* Keep `secrets-vault` single-tenant, `drydock` partial, etc. until a consumer forces the next level. `[CNCF-Maturity]`
5. **Modular à-la-carte catalog.** Each brick independently adoptable — any subset, no obligation to take the rest. Validates the brick decomposition **and** the 3-forms migrate-up model. `[Dapr]`

## Capability map — current state

| Capability | Layer | State | Where |
|---|---|---|---|
| App hosting / bootstrap | infra | ✅ have | `backend.beta` (`AddApiDefaults`) |
| Observability — emit (OTel) | infra | ✅ have | `backend.beta` |
| Observability — store/dashboards/alerts | infra | ❌ missing | — (buy) |
| Identity — consumer-side | infra | ✅ have | `backend.beta` (16 OAuth + MFA/WebAuthn + JWT) |
| **Identity — central IdP / SSO** | infra | ❌ missing | **DECIDED** |
| **Secrets** | infra | 🟡 Form 2 only | `secrets-vault` |
| **CI/CD pipelines** | dev-ex | 🟡 skeleton | `platform.pipelines` |
| **Deploy / ops control plane** | infra | 🟡 partial | `drydock` |
| **Scaffolding / CLI** | dev-ex | 🟡 template+skill, no CLI | `product-template`, `create-repo` |
| Jobs / scheduling | infra | ✅ have | `backend.beta` (Hangfire) |
| Caching | infra | ✅ have | `backend.beta`, `storage.cache` |
| File / blob storage | infra | 🟡 partial | `storage.file` |
| Data layer / migrations | data | ✅ have | `backend.beta` EF, smart-qr migrator |
| Multi-tenancy | product | ✅ have | `backend.beta` |
| Feature flags / config | product | ✅ have | `backend.beta` |
| Comms / notifications | product | 🟡 email/Telegram | `backend.beta` comms |
| Audit log | product | 🟡 inside secrets-vault | `secrets-vault` |
| Admin console / back-office | product | ❌ missing | — |
| Billing / metering | product | ❌ missing | — (buy) |
| Analytics / product metrics | data | ❌ missing | — (buy) |
| Event bus / messaging | infra | 🟡 partial | `comms.infra` (MassTransit) |
| Durable execution / workflows | infra | ❌ missing | — (buy/defer) |
| API gateway / ingress | infra | ✅ have (Traefik) | via `drydock` |
| UI component library | dev-ex | 🟡 partial | `beta.ui` |
| AI gateway / LLM proxy | data/AI | ❌ skeleton | `templates.ai` |
| Internal developer portal | dev-ex | ❌ missing | — (DEFER) |
| Docs / knowledge site | dev-ex | ❌ missing | — |
| Search | data | ❌ missing | — (buy) |

## Ranked backlog

### Tier 0 — finish in-flight (top fanout, already moving)

| # | Brick | State → goal | Form | Build/Buy | Why |
|---|---|---|---|---|---|
| 1 | **Central Identity Provider** | consumer-side ✅ → standalone OIDC/SSO | 1→2→3 | **Build thin** — add OIDC-server endpoints (OpenIddict, OSS .NET) atop the existing `backend.beta` user store; *or* self-host Keycloak/Zitadel | Every app needs auth; ~80% already built; kills the "hundreds of OAuth clients across providers" problem. Undifferentiated + highest fanout. **Specifics unverified — see Open Questions.** |
| 2 | **secrets-vault — harden + Form 1** | Form 2 ✅ → + Form 1 wireable | 2 → +1 | Build (mostly done) | Every app needs secrets; Form 1 lets a new micro-SaaS embed in-process, then graduate to the container. Already decided + in-flight. |
| 3 | **drydock — deploy golden-path** | partial → 1-click deploy + streamed logs | service | **Build thin** (wrap Traefik / GHCR / Hetzner / Cloudflare) | Every product must ship; this *is* the self-service golden path = the IDP core. Finish SSH executor + Hangfire + SignalR. |

### Tier 1 — high fanout, cheap given current state

| # | Brick | State → goal | Form | Build/Buy | Why |
|---|---|---|---|---|---|
| 4 | **CI/CD reusable pipelines** | skeleton → standard build/test/pack/publish/deploy workflows | n/a | **Buy/wrap** GitHub Actions reusable workflows | Verified "undifferentiated — do first." Highest fanout-per-effort; every repo uses it. Don't build a CI system. |
| 5 | **`wow` CLI + scaffolding** | template + skill → `wow new`, `wow add <brick>` | tool | **Build thin** | Turns the catalog into a *self-service product* (the literal IDP definition). Wires bricks so a new app = near-zero infra work. Productizes `create-repo`. |
| 6 | **Observability backend** | emit ✅ → store + dashboards + alerts | 3 (provided) | **Buy/wrap** — self-host one Grafana stack or SigNoz, or managed | You already emit OTel; close the loop **once** and every app inherits dashboards/alerts. Don't build a telemetry store. |

### Tier 2 — product levers, medium fanout

| # | Brick | State → goal | Form | Build/Buy | Why |
|---|---|---|---|---|---|
| 7 | **Notifications brick** | email/Telegram → multi-channel (email/push/in-app/SMS) | 1→3 | Build thin, or wrap **Novu** | Every SaaS notifies users; extend the existing comms slice. |
| 8 | **Audit-log brick** | inside secrets-vault → standalone reusable | 1→2 | Build (harvest from `secrets-vault`) | Trust/compliance; the hash-chain pattern is already proven — extract it. |
| 9 | **Admin / back-office brick** | missing → turnkey per-product admin UI | 1 | Build thin (atop `beta.ui` + identity) | Every SaaS wants an admin panel; high reuse once built. |
| 10 | **Docs / knowledge site** | missing → the "knowledge + support" IDP pillar | service | **Buy/wrap** (Docusaurus / Astro Starlight) | IDP = APIs + tools + **knowledge + support**; cheap, raises catalog adoption. |

### Tier 3 — defer / buy / on-demand (anti-over-engineering)

- **Billing / metering** → **buy** Stripe (+ Lago/Orb for usage metering) *when a product earns money*. Non-commercial now → not yet.
- **Event bus / durable execution (Temporal)** → **defer** until an app actually needs async sagas; `comms.infra` (MassTransit) covers basic messaging.
- **AI gateway / LLM proxy** → build thin *when* shared key-mgmt + routing + caching pays off (relevant given the AI-native WoW 3.0 vision) — not before identity/CLI.
- **Own API gateway** → **don't build**; Traefik (already in the `drydock` deploy flow) suffices for companion-per-app.
- **Internal developer portal (Backstage)** → **defer**; a registry doc + the `wow` CLI deliver catalog + self-service at your scale. Standing up Backstage now is the classic small-team over-engineering trap.
- **BaaS (Supabase-style)** → **skip**; the .NET `product-template` already gives every app a real backend.
- **Search** → **buy** (Meilisearch / managed) on demand.

## Build-vs-buy verdicts (quick table)

| Capability | Verdict |
|---|---|
| Identity (central IdP) | **Build thin** — wrap OpenIddict / self-host Keycloak/Zitadel; you already own the user store *(picks unverified)* |
| Secrets | **Built** — keep, add Form 1 |
| Deploy plane | **Build thin** — `drydock`, wrap infra APIs |
| `wow` CLI / scaffolding | **Build thin** — no good off-the-shelf fit for your conventions |
| Notifications | **Build thin or wrap Novu** |
| Audit log | **Build** — harvest from secrets-vault |
| Admin console | **Build thin** — atop beta.ui |
| CI/CD | **Buy/wrap** — GitHub Actions |
| Observability store | **Buy/wrap** — Grafana / SigNoz / managed |
| Docs site | **Buy/wrap** — Docusaurus / Starlight |
| Billing | **Buy** — Stripe / Lago |
| Workflows | **Buy** — Temporal (on demand) |
| API gateway | **Buy** — Traefik (already in use) |
| Dev portal | **Defer** — registry doc + CLI instead |

## Open questions → next research (re-verify before committing)

1. **Identity (brick #1) specifics — highest priority.** Which architecture + product for ONE IdP fronting many first-party apps? Identity-brokering (one IdP federates external providers; apps integrate only with it) and the self-host (Keycloak/Zitadel/Ory/Authentik) vs managed (Clerk/WorkOS/Auth0) vs .NET-native (OpenIddict OSS; Duende — *commercial license*) decision **all scored 0-0 (rate-limited, unverified).** Given you already own consumer-side identity, OpenIddict-atop-existing-store is the natural hypothesis — but confirm with a focused deep-research pass.
2. **3-distribution-forms evolution** (in-process lib → sidecar → managed). Only the modular-catalog half is verified (Dapr). The sidecar-as-form and library→service maturation (strangler-fig, "platform as a product") need fresh sourcing.
3. **Per-capability build-vs-buy tool picks** — confirm the shortlist above with a fresh verify pass (the principle is verified; the specific tools are not).
4. **Concrete "don't build yet" list** — service mesh, multi-cluster, full Backstage, comprehensive observability beyond `backend.beta` — directionally consistent with the verified anti-over-engineering principle but individually uncited.

## Sources (verified)

- `[CNCF-Platforms]` — CNCF TAG App Delivery, *Platforms Whitepaper* — https://tag-app-delivery.cncf.io/whitepapers/platforms/
- `[CNCF-Maturity]` — CNCF TAG App Delivery, *Platform Engineering Maturity Model* — https://tag-app-delivery.cncf.io/whitepapers/platform-eng-maturity-model/
- `[Dapr]` — Dapr docs, *building blocks / overview* — https://docs.dapr.io/concepts/overview/

*Stats: 6 angles · 22 sources fetched · 92 claims extracted · 25 verified · 6 confirmed (5 after dedup) · 19 killed (mostly rate-limit abstentions, not refutations).*

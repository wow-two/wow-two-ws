# WoW Two Identity — Central Auth / SSO for the Portfolio

*Last updated: 2026-06-19*

> Proposed `wow-two-platform.identity` — one self-hosted OIDC identity provider that owns a **single** Google
> OAuth client (and later email / other social logins); every portfolio app delegates login to it instead of
> wiring Google directly. One-liner: *a self-hosted Auth0/Clerk for the fleet — integrate each provider once,
> every app consumes app-scoped sessions.*
>
> **Status:** parked — **start after `wow-two-platform.secrets-vault` is ready** (it holds the Google client
> secret + the IdP's token-signing keys + rotation). Spawned from **smart-qr v0.3** (Google OAuth built inline);
> this is where that auth infra extracts at portfolio scale. Deployed/monitored by `drydock` like any service.

## Problem

- Target: **100 startups** (`ven-msaas-context.md`, EOY-2026). Each needs login.
- **One shared Google client across apps** → shared token `aud` (cross-app token replay), one consent-screen brand for all, per-client origin caps, one suspension kills every app. ✗
- **One Google client per app (100)** → correct isolation but 100 projects / consent screens / verifications to create + manage; client sprawl. ✗ at scale.

## Solution — a central IdP

- One IdP owns **ONE** Google client (providers pluggable: email magic-link, GitHub, …). Apps redirect to it for login (OIDC auth-code + PKCE).
- IdP verifies Google → mints **app-scoped** sessions/tokens (per-app `aud`). No cross-app replay; isolated blast radius.
- Google's consent screen shows the **IdP brand once**; per-app look = the IdP's **themeable hosted login pages**.
- Collapses 100 Google clients → **1**. One place to rotate secrets, add providers, read auth metrics.

## Architecture (sketch)

- `wow-two-platform.identity` — Clean-Arch .NET + hosted login UI, sibling to `drydock` / `secrets-vault`.
- **Providers:** Google first → pluggable interface for email / social.
- **Tokens:** OIDC/JWT (or opaque session); signing keys from `secrets-vault`.
- **Registry:** per-app `client_id`/secret, redirect URIs, theme. **User store:** unified vs per-tenant (open Q).
- **SDK:** `WoW2.Sdk.Backend.Beta` auth client — apps drop in "Login with WoW Two ID" + validate IdP tokens (replaces each app's inline verifier + session wiring).

## Extraction from smart-qr v0.3

The v0.3 inline pieces ARE the IdP core, lifted:

| smart-qr v0.3 (inline) | → becomes in the IdP |
|---|---|
| `IGoogleTokenVerifier` seam | the IdP's Google provider |
| cookie session (`sqr-auth`) | IdP-issued session/token |
| `users` table + claim flow | IdP user store + account linking |

> Two-cycle model: v0.4 was "extract auth infra → SDK". This idea is the larger target that extraction grows into — extract to the SDK first, then promote to a running service.

## Sequencing & dependencies

1. **Gate:** `secrets-vault` ready (Google secret + IdP signing keys + rotation).
2. IdP MVP: Google + **one** consuming app (smart-qr) → migrate smart-qr off its own client.
3. Onboard the next apps; retire per-app Google clients.

## Open questions

- **Unified identity** (one account across all 100 = portfolio SSO) vs **per-app isolated** accounts (multi-tenant)? Drives the user-store model.
- Hosted login UI: per-app theming vs one neutral brand.
- Session transport: IdP cookie on a shared parent domain vs per-app token exchange.
- **Build vs adopt** the IdP core: Keycloak / Ory / Zitadel / Supabase Auth vs hand-rolled (the wow-two "own it" default — but auth is high-risk to hand-roll; evaluate first).

## Related

- `ideas/smart-qr-spec.md` (origin product) · `ideas/drydock-spec.md` (deploys it) · `ven-msaas-context.md` (the portfolio it serves).

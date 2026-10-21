# WoW 2.0 — Platform Decisions, Ranked

*Last updated: 2026-10-21*

> The big cross-cutting choices still open across WoW2 products and Ocharo, ranked by what each one unblocks.
> A made decision moves to [platform apps](platform-apps.md) § Decisions or its owning repo and leaves this list.
> Sources: the 2026-10-21 sweep of every active service, the [Identity](../ideas/identity-service-spec.md) and
> [File Storage](../ideas/file-storage-service-spec.md) specs.

## Proposed order

D1 → D2 → D3 → D9 → D4 → D6 → D10 → D11, then the rest as their triggers fire.

---

## Now — blocks Identity and File Storage

- **D1 · Identity build path** — OpenIddict on our SDK store · Keycloak · Zitadel · Logto or Authentik · managed
  (Clerk, WorkOS, Auth0). **Recommend** OpenIddict: only it keeps Form 1 and our Telegram flows. Unblocks every
  sign-in change.
- **D2 · Identity instances** — one central IdP for every owner · one instance per owner. **Recommend** per owner:
  Ocharo runs its own Form 2 now; the WoW2 portfolio shares one Form 3 later. Unblocks the Ocharo deploy.
- **D3 · Account model** — one person across an instance's apps with organization memberships · isolated accounts
  per app. **Recommend** one person per instance, roles per organization, app permissions as claims. Unblocks
  the Desk migration.
- **D4 · Ocharo sign-in methods** — bot code only · plus Log in with Telegram · plus Gateway codes · plus
  passkeys. **Recommend** bot code and Log in with Telegram in P1; Gateway only for a member who cannot use
  the bot; owner passkey in P2.
- **D5 · Ocharo bot ownership** — Identity owns its webhook · a Notifications service owns it. **Recommend**
  Identity owns the webhook; any service may send through the Bot API; a second bot if Marketing needs commands.
- **D6 · File backing store** — Contabo Object Storage · Cloudflare R2 · SeaweedFS on the VPS · local disk only.
  **Recommend** Contabo Object Storage hosted (same provider, no transfer fees), local disk in development.
- **D7 · Public file delivery** — every file through the API · public immutable URLs with a CDN. **Recommend**
  private by default with signed URLs; catalogue and blog images on immutable `/media/{sha}`; CDN in P2.
- **D8 · Desk's `bytea` move** — with Files P1 · after the smaller apps. **Recommend** last: Catalogue and Brand
  first, then Blog and Marketing, then Desk.
- **D9 · Rank of Identity and File Storage** — Identity stays #6 and Files joins as #15 · both move up right after
  Wheelhouse's ship gate. **Recommend** moving both up: Ocharo's launch needs real members and hosted files, and
  Feedbacks, Logs and Monitoring need users first.

---

## Next — shape the backbone

- **D10 · Secrets for running services** — host files (the secrets convention today) · Wheelhouse's built-in vault
  · the standalone Secrets Vault. **Recommend** host files rendered from Wheelhouse's vault (parked decision 60):
  Identity's signing keys and provider secrets are the first heavy user.
- **D11 · Database standard** — PostgreSQL for hosted, SQLite for local tools · SQLite allowed hosted.
  **Recommend** PostgreSQL for every Form 2 or 3 service and hosted multi-user app; Catalogue and Brand move.
- **D12 · Notifications capability** — build thin on SDK `Comms/` · wrap Novu. **Recommend** build thin: Desk's
  codes, Marketing's brokers and Haven's alerts already converge on the SDK.
- **D13 · Email provider** — no product sends email today. Amazon SES · Postmark · Resend · own SMTP.
  **Recommend** choosing one with Identity P2 (email sign-in, resets); Postmark for delivery, SES for cost.
- **D14 · Audit capability** — SDK module first · standalone service. **Recommend** SDK module harvested from
  Wheelhouse's audited commands and the vault's hash chain; Identity and Files write to it.
- **D15 · Localization** — per-app `UiMessages` (Marketing 4,953 lines; Desk and Catalogue copies) · a shared SDK
  catalogue · a translation service. **Recommend** a shared SDK catalogue for shell and common strings; app
  strings stay per app; the Desk and Catalogue designer copies merge.
- **D16 · AI gateway** — direct calls per app · one gateway. **Recommend** the gateway once keys or cost need one
  view: Marketing (OpenAI, Gemini), Haven (Anthropic) and TranscriptForge (Groq) already call providers directly.

---

## Later — on a named trigger

- **D17 · Billing and legal entity** — Stripe (+ Lago); the entity per `ideas/parent-company-2026-10/`. Trigger:
  a product earns money.
- **D18 · Search** — Postgres full-text, then Meilisearch. Trigger: an app outgrows full-text.
- **D19 · Analytics** — Plausible or Umami through Wheelhouse. Trigger: a product needs funnels.
- **D20 · Mobile shell** — Capacitor · Photino · native; no written standard. Trigger: a second mobile app ships.
- deployment choices (registrar, redundancy decision 69, migration rollback) stay in the Wheelhouse backlog.

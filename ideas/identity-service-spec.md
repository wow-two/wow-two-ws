# WoW Two Identity — Own Identity Store and SSO for Every Product

*Last updated: 2026-10-21*

> `wow-two-platform.identity`: our own user store, OIDC provider, hosted sign-in and admin console, shipped in the
> three [capability forms](../conventions/development/capability-forms.md). Every product signs in through it instead
> of wiring Google, Telegram or passwords itself.
>
> **Status:** the developer chose to build it on 2026-10-21; first consumer Ocharo (phone + Telegram bot code,
> admin-managed members). D1–D3 decided 2026-10-21; open: [platform decisions](../docs/platform-decisions.md) D4, D5.

## Problem

- sign-in is built per product four ways: Wheelhouse GitHub, ForeverPin Google, Haven Telegram code, the
  first-ten pilots email and password; Ocharo Desk has a fifth (password + Telegram code + its own SSO broker).
- Ocharo duplicates the client side: `Ocharo.Sso` is copied byte for byte into Studio, Marketing and Blog, plus
  four frontend session clients and three older ticket-introspection handlers.
- Desk's broker is not OIDC, keeps app sessions in memory (a restart signs everyone out, one instance only), and
  exposes no member administration: operators come from a CLI command and memberships from fixtures.
- one Google client per product does not scale to the portfolio; one shared client leaks token audiences.

---

## Placement

- **Form 1 · library** — the identity and OIDC server modules in the be SDK `Identity/`, the sign-in kit in the
  fe SDK; for one product with accounts in-process.
- **Form 2 · self-hosted service** — the module hosted with sign-in pages and an admin console, as the
  `wow-two-platform.identity` image; for one owner's apps: Ocharo runs its own.
- **Form 3 · provided service** — the same image, run once by us on the WoW2 control host, for the portfolio.

- the service hosts the SDK module; no identity logic lives only in the service repo.
- the image follows the [deployment descriptor](../conventions/deployment/descriptor/deploy-descriptor.md).
- apps integrate with one SDK OIDC client module whatever the form; it replaces `Ocharo.Sso`, Desk's integration
  tickets and every per-app session client.
- Ocharo runs Form 2 on its products host: its own bot, brand, members and database, separate from WoW2's (D2, decided).

---

## Build path

- **decided (D1):** OpenIddict (Apache-2.0, .NET) for the protocol on top of the SDK's own store.
  OpenIddict 6.0.0 already sits in the be SDK's `Directory.Packages.props`, unreferenced.
- why not Keycloak, Zitadel, Logto or Authentik: each replaces our store, has no Form 1, and custom flows such as
  the Telegram link need Java SPIs or Go actions; Duende needs a commercial licence.
- the risk of owning auth is protocol correctness: OpenIddict carries the protocol, and the OpenID Foundation
  conformance suite runs in CI before Form 2 ships.

---

## What already exists

Be SDK `Identity/` (about 92 tests):

- email + password: Argon2id with rehash on upgrade, length 8–128, identifier check, HIBP k-anonymity (fails open),
  lockout 5 attempts / 5 minutes, reset tokens bound to the security stamp.
- email magic link and email code; phone OTP sign-in; OTP channels SMS (Twilio, Vonage, Eskiz), email, WhatsApp,
  Telegram bot message, Telegram Gateway.
- passkeys (Fido2, usernameless), TOTP, hashed recovery codes, delivered-code second factors, API keys.
- 17 OAuth registrations (Amazon, Apple, Discord, Facebook, GitHub, GitLab, Google, LinkedIn, Microsoft, Notion,
  Reddit, Slack, Spotify, Twitch, X, VK, Yandex) and a generic OIDC client.
- cookie or JWT sessions; refresh tokens rotate and a reuse revokes the family.

Ocharo Desk (`brand-workspace`): organizations, memberships (`owner`, `editor`, `viewer`), `telegram_links`, the
bot's link-by-contact flow and 6-digit codes, an 8-hour session table, PKCE app codes.

Fe SDK: auth bridge and strategies, Google button, `accountMenu`, `pinInput`, `passwordInput`, a naive strength
callout.

---

## Gaps

- protocol — OIDC server endpoints, discovery, JWKS, asymmetric signing keys and rotation (JWT is HS256 only).
- accounts — organizations, memberships, invitations, admin-managed members, an OAuth callback-to-link route.
- passwords — expiry, history, forced reset, admin-generated temporary passwords, generator, a real strength meter.
- sessions — a durable OTP store (memory only today), a session list per user and device, revoke one or all.
- audit — sign-in log, security events (log lines only today), admin action trail.
- admin — user admin API, disable, impersonation, the console itself.
- Telegram — Log in with Telegram (OIDC), link-on-first-sign-in without a password.
- fe SDK — sign-in, phone + code, Telegram link, passkey, MFA and account screens; `passwordStrength` is empty.

---

## Features

The whole vector, phased. P1 is the Ocharo slice; P2 completes the vector; P3 waits on a named consumer.

### Sign-in methods

| Method | Phase | Notes |
|---|---|---|
| phone + code via own Telegram bot | P1 | free; the member opens the bot once and shares their contact |
| Log in with Telegram (OIDC) | P1 | one tap; `phone` scope returns a Telegram-verified number; same bot |
| phone + code via Telegram Gateway | P2 | no bot link; paid per delivered code, refunded if undelivered |
| phone + code via SMS or WhatsApp | P2 | adapters exist (Eskiz for Uzbekistan, Twilio, Vonage) |
| email + password | P2 | hosted pages over the existing SDK flow |
| email magic link, email code | P2 | exists in the SDK; needs email delivery |
| passkeys | P2 | passwordless default for owners and admins |
| social: the 17 registrations + generic OIDC | P2 | one client per provider per instance, linked to one account |
| enterprise: Microsoft Entra ID, Google Workspace, SAML 2.0 | P3 | per-organization connections |
| regional: Yandex ID, OneID (Uzbekistan e-gov) | P3 | OneID needs an integration agreement |
| device flow, client credentials, personal access tokens | P2 | CLIs, TVs, service-to-service |

### Accounts and members

- invite-only mode per client: an admin adds a member by phone or email with a role; self sign-up stays off (P1).
- self sign-up mode with email or phone verification for public products (P2).
- one person per instance (D3); organizations, memberships, roles and per-app permissions as token claims;
  Ocharo's `owner`, `editor`, `viewer` carry over with `can-edit` and `can-approve` (P1).
- account linking: phone, Telegram, Google and passkeys on one person; merge two accounts (P2).
- profile: name, avatar, locale (`uz`, `ru`, `en`), timezone (P1 name and locale).
- disable, remove, personal-data export and deletion (P1 disable and remove; export exists).

### Passwords

- Argon2id with rehash (exists); breached-password check (exists); zxcvbn-style strength score and meter (P2).
- policy per client or organization: minimum length, optional composition rules, history of the last N (P2).
- expiry after N days and rotation: off by default, as NIST SP 800-63B advises; on per policy (P2).
- forced reset by an admin or on a detected breach; a notification on every change (P2).
- generation: an admin-issued temporary password that must change at first sign-in; a generator in the password
  field with length, character sets and passphrase mode (P2).
- lockout with progressive delay per account and per IP (fixed lockout exists; progressive in P2).

### Second factors and step-up

- TOTP, passkeys, recovery codes (exist); a Telegram approve button: "Sign in to Ocharo Desk? Approve / Deny" (P2).
- required MFA per role, remembered devices, step-up before approve or delete actions (P2).

### Sessions and tokens

- OIDC authorization code + PKCE for every app; short access tokens; rotating refresh tokens (exist) (P1).
- per-app audience; first-party apps skip consent (P1); a consent screen for third parties (P3).
- signing keys rotate with an overlap in JWKS; keys stored per [secrets](../conventions/security/secrets/secrets.md) (P1).
- single sign-out across apps: back-channel logout (P1), front-channel (P2).
- durable session and OTP stores in PostgreSQL, safe across instances (P1).

### Abuse protection

- codes: 6 digits, 5-minute life, 5 attempts, 30-second resend, hashed at rest, one live code per phone (P1).
- rate limits per phone, per IP and per client; a country allow-list against SMS pumping (P1 limits, P2 list).
- the bot accepts only the sender's own contact (`contact.user_id` equals the sender) (P1).
- a new-device alert through Telegram or email (P2); impossible-travel and risk scoring (P3).

### Admin console and dashboards

- overview: sign-ins by day, method and app; failure rate; lockouts; code delivery rate and Gateway cost; active
  sessions; MFA adoption (P1 counts, P2 charts).
- sign-in log: every attempt with time, member, masked phone or email, method, app, result and reason, IP,
  country, device; filters; CSV export (P1).
- members: add, invite link, role, app access, disable, remove, sign out everywhere, unlink Telegram, reset or
  generate a temporary password, the member's sessions and sign-ins (P1 without passwords).
- sessions: every live session; revoke one, a member's, or all (P1).
- apps: client registry with redirect URIs, allowed methods, token lifetimes and theme (P1 by config, P2 in UI).
- policies: password, code, lockout, session lifetime, required MFA (P2).
- security events and admin actions on a hash-chained trail, harvested from Wheelhouse and the vault (P2).
- impersonation with a visible banner and an audit row (P3).

### Member self-service

- account page: profile, phone and email, linked sign-ins, passkeys, MFA, sessions with sign-out, recent sign-ins
  (P1 sessions and recent sign-ins; the rest P2).

### Developer surface

- be SDK OIDC client module: one registration, cookie session, claims, CSRF, back-channel logout (P1).
- fe SDK sign-in kit: phone + code, Telegram link step, password with meter, provider buttons, passkey, MFA,
  account page; `accountMenu` reads the session (P1 phone, code and link; the rest P2).
- hosted sign-in pages themed per client (`theme-ocharo`) and localized (P1).
- management API with scoped keys; webhooks such as `member.added` and `signed_in` (P2); SCIM (P3).

---

## Ocharo slice (P1)

- **member added** — the admin enters name, phone and role in the console; no password exists.
- **first sign-in** — the member enters their phone; the page shows "Open Ocharo bot" with a
  `t.me/{bot}?start={one-time token}` link; the bot asks to share the contact, checks it is the sender's own and
  matches the invited phone, stores the link and sends the code.
- **every later sign-in** — phone, then the code from the bot; or one tap on Log in with Telegram.
- **member removed** — every session and refresh token is revoked at once; apps sign out by back-channel logout.
- the bot's webhook moves from Desk to Ocharo Identity; other services may still send through the Bot API (D5).
- migration: Desk's `access` users, organizations, memberships and `telegram_links` move into the Ocharo
  Identity database; Desk, Catalogue, Brand, Studio, Marketing and Editorial become OIDC clients; integration
  tickets, the SSO broker and the `Ocharo.Sso` snapshots retire. Catalogue's planned sign-in comes with it.

---

## Sequencing

1. be SDK: OIDC server module, organizations and memberships, durable OTP and session stores, sign-in log,
   asymmetric keys with JWKS, Telegram link-on-first-sign-in, OIDC client module.
2. fe SDK: phone, code and Telegram link screens; members, sessions and sign-in log tables for the console.
3. `wow-two-platform.identity`: host, hosted pages, admin console, Dockerfile, `deploy.yml`, conformance suite.
4. Ocharo: deploy its instance, migrate Desk's accounts, move the apps one by one, retire the old paths.
5. P2 across the vector; then Form 3 for the portfolio, starting with ForeverPin and the pilots.

---

## Sources

- [Log In With Telegram](https://core.telegram.org/bots/telegram-login) — OIDC flow, `phone` scope, BotFather client.
- [Telegram Gateway API](https://core.telegram.org/gateway/api) — paid codes to any Telegram phone number.

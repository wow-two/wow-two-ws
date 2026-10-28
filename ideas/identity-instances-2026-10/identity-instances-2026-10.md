# Identity instances — wow2 and Ocharo

*Last updated: 2026-10-28*

> What the first two running Identity instances need, so the build starts in the right order: the wow2 instance
> (single sign-on with roles into every wow2 platform app, Wheelhouse first) and the Ocharo instance (Telegram code
> through Ocharo's own bot). It spans Identity, Wheelhouse and Ocharo, so it stays in the hub. No code, no commits.

## Verdict

- **Build Ocharo's instance first, then wow2's** (developer, 2026-10-27, reversing the first pick). Both share the OIDC
  spine (keys, server, sessions, client module), built 2026-10-27. Ocharo adds the Telegram, invitation, durable-code
  and member-admin slices; wow2's hosted passkey, password and TOTP pages follow.
- **The wow2 instance is operator-only and private.** It runs on the control host beside Wheelhouse, with no public
  site and no self sign-up. A public Form 3 instance for portfolio users is a separate, later instance on a products
  host (Q4 stays as its question).
- **Wheelhouse signs in through it and keeps a local break-glass login** (developer, 2026-10-26). P1's break-glass is
  today's GitHub sign-in, moved to an owner-only route. Wheelhouse's host-side rollback sits beneath it.
- **wow2 P1 methods:** passkey first, then email + password with TOTP, then recovery codes, then a host CLI.
  P1 has no email reset, because no email provider exists (D13).
- **Ocharo P1:** staff only, invite-only, phone + bot code. Identity owns the bot webhook (Q13) and keys each person
  on the Telegram user id (Q14). Desk's accounts are reset, not converted: the organization id is kept and members
  are invited again.
- **Q5 splits by instance kind** (revised 2026-10-28, migrations M77): the shared wow2 instance is a Wheelhouse product
  of its own (B); Ocharo's per-product instance is a service of `ocharo`, its set in Ocharo's database (A). The Ocharo
  instance waits on Wheelhouse's migrate step, domain binding and off-host backups (Q30).

## Inputs

- developer, 2026-10-26: "that instance will allow sso into all wow2 platforms with roles, starting with wheelhouse,
  then for ocharo (… telegram otp with our own telegram bot, for wow2 maybe a passkey and email and password?)".
- developer, 2026-10-26: Wheelhouse signs in through the wow2 instance normally and keeps a local emergency login,
  because it deploys Identity (§ 2). This replaces Q34's "stays Form 1".
- Identity repo `wow-two-sdk-beta.identity`: `product/product.md`, `product/context.md`, `engineering/planning/backlog.md`
  and the analysis batch `engineering/research/identity-analysis-2026-10/` (T1–T10, decision queue to Q58).
- be sdk `engineering/research/identity/identity-slices.md`: I1–I13 done, I14–I22 planned.
- Wheelhouse: `product/context.md`, `engineering/architecture/architecture.md`, `engineering/planning/backlog.md`,
  `engineering/deployment/deployment.md`.
- Ocharo hub `ocharo-ws`: `docs/architecture.md`; Desk `engineering/architecture/telegram-sign-in.md`,
  `engineering/deployment/operator-access.md`, `engineering/planning/backlog.md`.
- [platform apps](../../docs/platform-apps.md) · [platform decisions](../../docs/platform-decisions.md) ·
  [capability forms](../../conventions/development/capability-forms.md) ·
  [breaking changes](../../conventions/development/breaking-changes.md) ·
  [deploy descriptor](../../conventions/deployment/descriptor/deploy-descriptor.md).
- Modes `M0`–`M13` are T4's. Phases P1–P3 are the spec's. Hub points are `Q{n}`, and new ones start at Q59.

---

## 1 · The wow2 instance

### Scope

- Its people are operators of the wow2 platform: the developer today, a few operators later. It has no customers.
- It is invite-only, with self sign-up off for every client.
- It has one organization, `wow2`. Platform apps have no tenants, and one organization keeps Ocharo's role machinery:
  memberships, the last-owner guard and `app_access`.
- It is a platform app, so it runs on the control host, which hosts platform apps only. Its `app` and `console` sites
  are both private, so the control host opens no public port.
- It needs no bot, because P1 has no phone sign-in for operators.
- Form 3 for portfolio users (ForeverPin, the pilots) is not this instance. That instance has public sign-up, a public
  issuer and its own user table, key ring and client registry. T10 § 5(b) lists what mixing the two would merge.

### Apps, in order

| # | App | Client | Mode | Joins |
|---|---|---|---|---|
| 0 | Identity console (the instance's own) | `identity-console` | M3 server-rendered | with the instance; first admin from the host CLI |
| 1 | Wheelhouse canary | `wheelhousecanary` | M2 | first proof, on dev: Wheelhouse tests a new flow on the canary first (decision 2026-10-15) |
| 2 | Wheelhouse | `wheelhouse` | M2 + step-up | dev, then prod (§ 7) |
| 3 | Files console (wow2's own instance and the shared files host's admin) | `files` | M2; the Files API is an M8 resource | when Files P1 switches its tenants to Identity issuers |
| 4 | Feedbacks inbox | `feedbacks` | M2 | platform app #5; its spec already says operator-only, as Wheelhouse |
| 5 | Logs viewer | `logs` | M2 | #6 |
| 6 | Monitoring | `monitoring` | M2 | #7 |
| 7 | Events, Harvest, AI Gateway, FlowDeck consoles | one client each | M2 (+ M8 APIs) | as each ships |

- Secrets Vault is merging into Wheelhouse as its built-in vault, so it gets no client.
- Identity's ship gate is "two apps sign in through it". Wheelhouse and the canary meet it as written. The Files
  console meets it with a second real app.

### Client registry

- Each app gets one confidential client per instance environment. Dev and prod keep separate registries and issuers
  (T6: never a shared issuer).
- BFF only (Q7, yes): tokens stay in the app's server-side ticket and the SPA sees a `__Host-` cookie and
  `/api/identity/me`. No first-party SPA holds a token.
- Protocol: code + PKCE S256, exact HTTPS redirect and post-logout URIs, response type `code` only, no implicit or
  password grant (ASVS 10.4).
- First-party clients skip consent.
- Each client has its own audience. An app accepts only its own `aud`, and people are identified by `iss` + `sub`
  (T6 threat 14).
- The registry comes from instance configuration in P1 (`Identity:Server:Clients`, seeded at startup). In P2,
  Wheelhouse registers apps from their descriptors through `IAppBroker.UpsertAsync` over client credentials (M10).
- Each client entry carries:
  - its `app` key, which `app_access` uses
  - its permission namespace
  - its allowed methods and theme
  - its back-channel logout URI, once that is built
- Client secrets: the owner generates each one. Identity stores only its hash, and the app's vault namespace holds the
  value. Wheelhouse renders both sides, and agents never see a value.
- Programs such as MCP clients and scripts keep Wheelhouse's own scoped integration keys. In P1, Identity serves
  people only.

### Role model

| Layer | Holds | Stored in | Reaches an app as | Granted by |
|---|---|---|---|---|
| instance role | `admin`: clients, keys, policies, the console | `identity_roles` / `identity_user_roles` | console only; never in an app token | the host CLI for the first admin, then an `admin` after step-up |
| organization role | one per member (D3): `owner` · `operator` · `viewer` | `identity_memberships.role` | `org_role` = `{org}:{role}` | an `owner`, in the console |
| app access | the apps a member may sign in to | `identity_memberships.app_access` | sign-in to an unlisted app is refused, and no token for it is issued | an `owner` |
| app permission | what a role may do in one app (`wheelhouse:deploy`, `logs:read`) | instance configuration: role → permissions, namespaced by app | `org_permission` = `{org}:{app}:{permission}`, only the requesting app's namespace | a configuration change (a deploy) |
| resource scope | which Wheelhouse workspaces or products an operator sees | the app's own table, keyed by `sub` | app-local | the app's owner |

- Roles are global and permissions are per app. A member has one role across the instance, and each app reads only
  its own permission namespace. Per-app role overrides wait for a named need, because they multiply the matrix that
  D3 keeps flat.
- ReBAC stays outside Identity (T2). Wheelhouse keeps which workspaces an operator sees, so Identity never models
  Wheelhouse's inventory.
- Q8 (yes): a token carries one active organization. That is trivial in wow2 and needed in Ocharo.
- A grant rotates the member's stamp (I13 ruling). The app sees the new role at its next refresh, within the
  access-token lifetime.
- Granting `owner` or instance `admin` takes a fresh passkey. Every grant writes an audit event and raises an admin
  alert (T6 § 7).
- Nobody below `owner` grants anything; delegated admin is P3.

Proposed matrix, for the first apps:

| Role | Wheelhouse | Files | Feedbacks · Logs · Monitoring |
|---|---|---|---|
| `owner` | everything; destructive actions ask for step-up | everything | everything |
| `operator` | deploy, promote, settings, secrets write; no server delete, decommission or key management | read, upload | triage, read |
| `viewer` | read | read | read |

### People

| Who | Today | Later |
|---|---|---|
| the developer | `owner` + instance `admin`, enrolled by the host CLI | — |
| operators | none | an expiring, single-use invite link that carries the role, handed over by the owner (I14; no email needed); `operator` with app access |
| agents and programs | Wheelhouse integration keys | client credentials with the management API (P2) |

---

## 2 · Wheelhouse bootstrap (decided)

### Decision

- Developer, 2026-10-26: Wheelhouse signs in through the wow2 instance normally and keeps a local emergency
  (break-glass) login, because it deploys Identity.
- This replaces Q34's pick. Wheelhouse becomes an OIDC client (M2) and keeps one local scheme (M0) that never calls
  the instance.

### Layers

| Failure | Normal SSO | Local login | Host-side deploy and rollback (exists) |
|---|---|---|---|
| an Identity release breaks sign-in | — | covers: sign in, roll Identity back | covers |
| the Identity container is down, the host is up | — | covers | covers |
| Identity's database or keys are lost | — | covers: restore, re-render keys | partial |
| the owner's passkeys are lost | password + TOTP, recovery codes (§ 3) | covers | — |
| GitHub is down | covers | — | covers |
| the control host is down | — (Wheelhouse is down too) | — | the host recovery runbook |

- Placing the instance on the control host means its outages coincide with Wheelhouse's. It adds no failure of its
  own, and a host outage takes down both anyway.
- Fewer bad Identity releases reach prod:
  - Wheelhouse dev signs in through Identity dev, so every Identity release meets Wheelhouse's sign-in before prod.
  - Identity prod promotes only by typed confirm, never by auto-promote.
  - Identity releases stay `rollbackCompatible` (expand, then contract), so a bad one rolls back whole.

### The local login

- It is today's GitHub sign-in with the owner allowlist, moved off the normal path to its own route
  (`/api/identity/break-glass`) with its own callback.
- The normal sign-in page shows only the wow2 sign-in.
- It issues a Wheelhouse cookie and nothing else. It gives no Identity session and no access to other apps.
- Its session is marked break-glass, lasts at most 1 h with no sliding, and shows a banner.
- A break-glass session holds owner rights, except actions that need step-up (server delete, decommission). Those wait
  until Identity answers again, or run from the host.
- Its GitHub scopes shrink to identity scopes once the GitHub App serves every owner (an existing backlog item).
- Later, the Wheelhouse-local passkey of decision 67 (root-key recovery) replaces GitHub as the local login. That
  passkey must stay Wheelhouse-local anyway: a PRF result binds to the site that runs the ceremony, so SSO cannot
  supply it.

### Who holds it

- Only the owner (the developer) holds it. The allowlist names one GitHub login, set in Wheelhouse's own settings
  rendered at deploy, never in Identity.
- Operators never get it. While Identity is down, they wait.
- Wheelhouse dev and prod each keep their own OAuth app and allowlist, as they keep their own sign-in today.

### How it stays safe

- It is reachable only on the private network, like the rest of Wheelhouse.
- A deployed console still refuses to boot without a nonempty allowlist (existing guard).
- The owner's GitHub account carries a phishing-resistant second factor.
- Every use is an audited command (`auth.break_glass`) in the hash-chained trail, with actor `github:{login}`.
- Every use raises an attention item and, once an ops channel exists, an alert.
- An attention item also shows when the last drill is older than 100 days, the same rule as restore drills.

### How it gets tested

- Wheelhouse E2E: with the OIDC authority unreachable, the break-glass route signs in the allowlisted login (GitHub
  faked) and refuses any other.
- The same E2E run checks that the session is marked, expires at 1 h, is refused step-up actions and is audited.
- Dev drill:
  1. stop the Identity dev service
  2. sign in to Wheelhouse dev through break-glass
  3. roll Identity dev back
  4. sign in through SSO again
- Run the dev drill before the switch (§ 7 M4), after every change to Wheelhouse's auth and before every Identity
  release that changes the schema.
- Prod drill: quarterly, with the restore drill. It covers break-glass sign-in plus one host-side Identity rollback
  with both consoles signed out.

### Wheelhouse changes

- Wheelhouse takes `Identity.Client` (`Identity:Mode = Oidc`). The session routes `/api/identity/*` replace its own
  `IdentityController` sign-in, me and sign-out.
- GitHub keeps coming from `Identity.Providers`, for the break-glass scheme only.
- Normal sessions authorize on `org_permission` (`wheelhouse:*`). The allowlist now guards only the break-glass scheme.
- The actor becomes the Identity `sub` with a display name, and break-glass sessions use `github:{login}`.
- Pins re-key from the GitHub login to `sub`. That is a breaking change, allowed because pins are preferences.
- Step-up: dangerous actions ask Identity for a fresh passkey (`max_age=0`, `amr` contains `hwk`). This builds the
  backlog item "confirm dangerous actions with a second factor".
- Integration keys and MCP stay unchanged.

---

## 3 · wow2 sign-in methods

### P1 set

| Method | Role | Phishing-resistant | In the SDK | P1 work |
|---|---|---|---|---|
| passkey, usernameless | primary sign-in and step-up | yes | yes (I10); bump Fido2 to 4.3.1 | hosted pages, account page |
| email + password | fallback sign-in; email is the identifier only | no | yes (I1–I5) | hosted pages |
| TOTP | required after a password | no | yes (I6) | hosted enrollment |
| recovery codes | lost-device recovery, single use | no | yes (hashed) | hosted view and print, ≥ 64 bits |
| host CLI one-time sign-in | last resort | needs host access | no | CLI in the image |
| email reset, email code, magic link | out | — | yes | needs an email provider (D13); email is not a factor for operators (NIST 3.1.3.1) |

- MFA is required for every member, set per instance: a password never stands alone.
- Q18 already put an operator passkey or TOTP into P1.
- Enrollment at the first CLI-created sign-in:
  1. a one-time link
  2. two passkeys: a synced one in the owner's password manager and one on a second device
  3. password and TOTP
  4. recovery codes, shown once
- An account with fewer than two passkeys shows a warning on the account page.

### Recovery ladder

| Lost | Way back |
|---|---|
| the TOTP phone | passkey on another device, then re-enroll TOTP |
| every passkey device | password + TOTP, then enroll new passkeys |
| TOTP phone and passkeys | password + a recovery code, then re-enroll both |
| everything | host CLI on the control host: a one-time sign-in link; needs private-network access plus host credentials |

- Every recovery and factor change writes an audit event. NIST also asks for a notice through an independent
  channel. That waits on an ops channel (Monitoring #7 or an ops bot); P1 shows these events on the account page.

### Password policy

The instance runs Q20's configured defaults; nothing is tuned for wow2.

| Setting | Value |
|---|---|
| minimum length | 15 (above NIST's floor of 8 inside MFA; the owner uses a password manager) |
| maximum | 128 (NIST: accept at least 64) |
| composition, expiry, history | off |
| breached-password check | on; it fails open, a deviation recorded in the spec |
| hashing | Argon2id with rehash (exists) |
| lockout | 5 failures / 5 minutes on the password path only; passkey sign-in stays open (T6 threat 13) |

### Sessions and step-up

| Item | Value |
|---|---|
| Identity SSO session | 12 h absolute for operators (T6) |
| app cookie | ≤ 8 h (Wheelhouse's today) |
| access token | 10 min |
| code | 60 s |
| refresh | rotated, absolute 12 h |
| step-up | `max_age=0` + passkey for destructive actions and for grants of `owner` or `admin` |
| revocation | short access tokens + offline JWKS checks + refresh refused after a stamp rotation (Q9: no introspection); back-channel logout arrives with Ocharo's slice (§ 6) |
| front-channel logout | dropped (Q10, yes) |

---

## 4 · The Ocharo instance

### Sign-in (P1)

- The method is phone + a 6-digit code through Ocharo's own bot, one bot per environment (Q12 channel by
  configuration). The flow is the spec's Ocharo slice:
  1. An admin adds the member: name, phone, role, apps.
  2. At first sign-in, the member enters the phone.
  3. The page shows "Open Ocharo bot" with a one-time `start` token: ≥ 128 bits, 15 min, single use.
  4. The member shares their contact. The contact's user id must equal the sender's, and the phone must equal the
     invited one.
  5. Identity stores the link and sends the code.
- Q13 (yes): Identity owns the bot webhook, with dedupe on `update_id`. Desk's `/api/auth/telegram/updates` retires.
- Other Ocharo services send through the Bot API only. Marketing gets a second bot if it ever needs commands (D5).
- Q14 (yes): after the first link, identity keys on the Telegram user id (`identity_user_logins`), never the phone.
  - the phone is kept as a confirmed `identity_user_phones` row
  - a phone change never moves the link
  - Log in with Telegram's `phone_number` claim never matches an account
- Code rules:
  - 6 digits, 5 min life, 5 attempts, a 30 s resend, hashed at rest, one live code per phone
  - each code is bound to its sign-in request
  - the attempt count survives a regenerated code
  - limits apply per phone, per IP and per client
- The phone step answers the same for known and unknown numbers.
- Operators (the instance console's admins) also need a passkey or TOTP. A Telegram code alone guards members only.
- Log in with Telegram (one tap, OIDC) comes after the cutover. It needs the generic-issuer spike (T1) and is not
  needed to replace Desk.

### Users

| Group | Who | Sign-in | Membership | P1 |
|---|---|---|---|---|
| owner | Ocharo's owner | bot code + passkey or TOTP | `owner` of `ocharo`; instance `admin` | yes |
| platform operator | the developer, as a separate person in this instance | bot code + passkey or TOTP | instance `admin`; a role only if needed | yes |
| staff | designers, content, sales | bot code | `editor` or `viewer`, with app access | yes |
| services | Desk MCP, cross-app boundaries | client credentials, per-app audience | — | M8 in P1; M10 with the management API |
| customers | buyers on the public sites | — | none | deferred |

- The public sites (Atlas, Wear, Blog, the Catalogue reader) stay sign-in-free. Catalogue's guest saves stay in the
  browser.
- When customers arrive, they join this instance: one brand, one bot. Sign-up opens only on customer-facing clients,
  with no membership, and operator apps refuse anyone without one.

### Apps and clients

| Client | App | Repository | Mode | Order |
|---|---|---|---|---|
| `identity-console` | Ocharo Identity console | Identity image | M3, private | with the instance |
| `desk` | Desk | `ocharo-platform` | M2 + M12 brokers + M13 events | 1st |
| `catalogue` | Catalogue authoring | `ocharo-platform` | M2; its loopback-only write APIs go behind sign-in | 2nd |
| `brand` | Brand | `ocharo-platform` | M2 | 2nd |
| `studio` | Studio | `ocharo-studio` | M2 + M8 API audience | 3rd |
| `marketing` | Marketing operator UI | `ocharo-marketing` | M2 + M8 | 4th |
| `editorial` | Blog editor | `ocharo-marketing` | M2 + M8 | 4th |

- `Ocharo.Sso` and its three copies, the four frontend session clients, the SSO broker and the three
  ticket-introspection handlers retire as each app moves (T3 list).
- Desk's MCP keeps its own handler until M10 ships.
- Q11 (product check): Desk checks the actor's `org_permission` before a broker call and passes the actor along.

### Role model

- The instance has one organization per brand owner. `ocharo` comes first, and Desk's multi-organization model maps
  one to one.
- Brand-level scoping stays in Desk.
- Roles: `owner` · `editor` · `viewer` (spec), one per membership.
- Permissions: `can-edit` and `can-approve` (spec), plus Desk's responsibilities as permissions rather than roles:
  `desk:publish`, `desk:connections`. Desk's product doc lets one person hold several.
- `app_access` per member: a designer may get Studio only.
- One active organization per token, with the `accountMenu` switcher (Q8).

### Desk's existing accounts

- No product has external users (breaking changes § Scope, 2026-10-26).
- Desk's `access` schema holds:
  - CLI-provisioned operators with email + password
  - fixture memberships
  - Telegram links tied to password sign-in
- Its prod environment has held no data so far.
- Reset, don't convert. The breaking-changes rule copies data only when copying is cheaper than recreating it. Here
  the converter (PascalCase rename, text-to-`uuid` ids, link mapping) costs more than inviting a handful of people.
- Keep one thing: create `ocharo` in Identity with Desk's existing organization id. Desk and Catalogue rows keyed by
  organization id then stay valid.
- Members are invited again by phone, and the bot re-makes each Telegram link at first sign-in.
- Drop `access.*`: users, roles, claims, logins, tokens, sessions, Telegram links, requests and codes, SSO codes and
  grants.
- Desk rows that reference old user ids are dev data and reset with them. If any must survive, run a one-off map by
  phone.
- Desk's password sign-in retires. The Ocharo instance offers no password in P1.
- This revises Q55's one-time copy (Q66 below).

---

## 5 · Two instances side by side

| Aspect | wow2 instance | Ocharo instance |
|---|---|---|
| boundary (Q54) | wow2 platform operators | Ocharo, one owner |
| host (Q4) | the control host: platform apps only, private | Ocharo's products host |
| sites | `app` private · `console` private | `app` public (hosted pages, bot webhook) · `console` private |
| issuer | a stable private host name with a trusted certificate, set explicitly | `https://id.<ocharo domain>` after domain binding; never a baseline host |
| Wheelhouse product (Q5) | `identity`, as the repository's `deploy.yml` names it today | none: a service of `ocharo`, the image pinned by tag (A, below) |
| workspace | wow2 platform | Ocharo |
| database (T10) | its own PostgreSQL database per environment, schema `identity` | Ocharo's database `ocharo_{env}`, schema `identity` (M6, M77) |
| migrations (Q57) | the image's `migrate` step before the new image serves | Ocharo's first `migrate:` item, before every set that depends on `identity` |
| signing keys (Q25) | X.509 host files rendered from Wheelhouse's vault, a staged `NotBefore`, one set per environment | the same, never shared |
| Data Protection (Q26) | ring in its own database, certificate-wrapped, ASP.NET ≥ 10.0.7 | the same |
| bot | none | its own, one per environment |
| methods | passkey · password + TOTP · recovery codes | bot code; passkey or TOTP for operators |
| backups (Q30) | Wheelhouse database backups when they ship; the first owner can re-bootstrap without them | off-host encrypted backups and a restore proof before cutover |
| residency | no phone data | Uzbek members' phones: confirm the host's location against the cross-border list before the first real phone (T6 § 1) |
| alerts | sign-in log and meters; alerts wait on an ops channel | the T6 ops notifier through its own bot |

- Each instance keeps its own database, keys, ring, bot and issuer. Only replicas of one instance share any of them
  (T10 § 5).
- Files' shared host trusts both issuers side by side (Files C8, C15). `sub` is unique per issuer only.
- An API resource on a products host that validates wow2 tokens needs a granted network path to the wow2 instance's
  discovery and JWKS. The control host's instance stays private.
- Back-channel calls from co-located apps (discovery, token, JWKS) go over the platform network by service name,
  while `iss` stays the private host name. That needs a P1 spike.
- Passkeys bind to the instance's host. Settle the wow2 host name before the first passkey: a later change means
  re-enrolling every passkey and re-registering every client.

### Two owners' instances of one image (Q5)

| Option | How | For | Against |
|---|---|---|---|
| A · a service of the owner's product | Ocharo's descriptor runs the Identity image as an image-only service of `ocharo` | one release set, one domain | needs a foreign-image version pin; shares `ocharo_{env}` and its vault namespace, so a Desk restore also rewinds Identity; Identity upgrades ride Ocharo's releases; wow2's instance takes a different shape |
| **B · an instance product** | a Wheelhouse product per instance, naming the Identity repository as its release source; the runner uses the product's own slug in place of the descriptor's `product:` | Wheelhouse's existing placement gives a database per instance (`<slug>_{dev,prod}`); its own vault namespace, promotion pace, workspace and domain; Files' per-owner instances reuse the model | Wheelhouse lets one repository feed several products and overrides the slug |
| C · instances inside one product | product `identity` gains instance rows | one view of all instances | the largest change; breaks "one placement per product" |

- ~~Pick **B**~~ → revised 2026-10-28 (migrations M77): **B for shared instances only**; a per-product instance takes
  **A**. One snapshot, one release and one step for Ocharo turn A's drawbacks into the point. The wow2 instance needs no
  change, because it is the repository's own product.

### Before each goes live

| Gate | wow2 | Ocharo |
|---|---|---|
| the § 6 slices for the instance, green; conformance Basic OP and RP-initiated logout pass in CI (Q28) | yes | yes, plus back-channel logout |
| `deploy.yml` on PostgreSQL (`needs: [postgres]`), done 2026-10-27 | yes | yes |
| an explicit migrate step: Wheelhouse's step and bridge (migrations spec phases 3–4), or an owner-run `migrate` before the deploy until it ships (Q57) | yes | yes |
| migrator follow-ups: the owner marker names the instance, a baseline | yes | yes |
| keys and the ring certificate generated by the owner with the image CLI, held in the vault, rendered as host files | yes | yes |
| hosted-page headers: `frame-ancestors 'none'`, no third-party assets, `Referrer-Policy` (Q19, yes) | yes | yes |
| first admin from the host CLI; production refuses personas, ephemeral keys or no ring | yes | yes |
| break-glass drill passed (§ 2) | yes | — |
| the Identity service and its `migrate:` item in Ocharo's `deploy.yml` (Q5 · A) | — | yes |
| a domain bound, the issuer on it (Q30) | — | yes |
| off-host backups and a restore proof with the post-restore step (Q30) | — | yes |
| one bot per environment, the webhook set with its `secret_token`, a published privacy policy for the bot profile | — | yes |
| residency check of the host's location | — | yes |

---

## 6 · Minimum build

### Slices per instance

| Work | wow2 | Ocharo | Notes |
|---|---|---|---|
| groundwork: the SQL set in `Identity.Module`, migrator follow-ups, claim vocabulary (`sub`, `sid`, `org_id`, `org_role`, `org_permission`, `amr`), OpenIddict 7.7.2 with EF Core ≥ 10.0.11, Fido2 4.3.1 | yes | yes | first; the v0.1 split comes before it |
| I17 key-source seam, startup validation, rotation procedure | yes | yes | two spikes (T6 § 3) |
| I18 OIDC server: authorize, token, end-session, discovery, JWKS, PKCE, client registry by configuration | yes | yes | — |
| I18 back-channel logout sender | deferred | yes | member removal signs apps out at once |
| I16 sessions (`sid`, list, revoke) | yes | yes | — |
| I16 sign-in log | yes | yes | — |
| Data Protection ring in the database | yes | yes | Q26 |
| I19 client module and the session routes | yes | yes | Wheelhouse and every Ocharo app |
| hosted pages: passkey, password, TOTP, recovery codes, account page | yes | operators | `fe-identity` `./kit` |
| hosted pages: phone, code, Telegram link | — | yes | `fe-identity` `./kit` |
| host CLI: `admin create`, `keys generate`, one-time sign-in | yes | yes | — |
| test mode (fake channels, personas) and conformance in CI | yes | yes | Q18, Q28 |
| I15 durable OTP | throttles only | yes | hashed, bound, 30 s resend |
| I20 Telegram: link on first sign-in, the bot webhook | — | yes | Log in with Telegram deferred |
| I14 invitations | links | yes | a link carrying the role, with per-link expiry and use limit in the library; wow2 hands over expiring single-use links; phone pre-registration for Ocharo |
| I21 admin subset: members add, role, disable, remove; sessions revoke; sign-in log read | sessions and log only | yes | the repo backlog lists I21 under P2; this subset moves to P1 |
| OpenTelemetry meters, `/health` readiness | yes | yes | — |
| ops notifier through a bot | deferred | yes | T6 § 7 |

### Packages

| Consumer | References |
|---|---|
| the Identity service (both instances) | `Module` + `Server` + `Client` by project reference; `Providers` only once social sign-in lands |
| Wheelhouse | `Client` (Oidc) + `Providers` (GitHub, break-glass) + `Auth` (integration keys) |
| the canary, Files, Feedbacks, Logs, Monitoring | `Client`; API resources `Auth` |
| Ocharo apps | `Client`; Studio, Marketing, Blog APIs `Auth` for M8 |
| tests | `Testing` |
| fe, everywhere | `@wow-two-beta/fe` `auth` with end-session follow |
| fe, the service | `@wow-two-beta/fe-identity` `./kit` and `./admin` |

### Build order

1. Finish v0.1 (the split into seven packages, tests green), then the groundwork row.
2. I17 keys, then the I18 server core with the client registry by configuration.
3. I16 sessions and the sign-in log, then the Data Protection ring.
4. Hosted pages for wow2's methods, I14 invite links with their accept page, the console shell (Wheelhouse's layout)
   and the host CLI.
5. I19 client module, conformance in CI, then **the wow2 instance goes live** (§ 7 M2–M5).
6. I15 durable codes, I14 phone pre-registration, I20 Telegram link and webhook.
7. The I21 admin subset, back-channel logout, and the phone, code and link pages.
8. **The Ocharo instance goes live** (§ 7 M7–M10).

### Deferred

- I22 password lifecycle (temporary passwords, forced reset, generator).
- Log in with Telegram, Telegram Gateway, SMS and email channels; social providers.
- Device flow, token exchange, the management API with scoped keys, webhooks, `IAppBroker` registration from
  descriptors.
- Desk's member projection: the `GetManyAsync` broker serves its lists until queries need a join.
- Delegated admin, impersonation, the hash-chained trail, required MFA per role beyond "all operators".

---

## 7 · Rollout

| # | Milestone | Proves | Gate |
|---|---|---|---|
| M1 | the Identity P1 core green in CI | the server, pages, client and conformance against the image | § 6 steps 1–5 built |
| M2 | wow2 instance dev, deployed by Wheelhouse prod on the control host | private sites, migrate step, keys from the vault, first admin and passkeys | the "before live" wow2 column |
| M3 | the canary signs in through the dev instance | the OIDC flow on a test app first | M2 |
| M4 | Wheelhouse dev signs in through the dev instance; break-glass drill passed | Wheelhouse adoption, the local login, host-side rollback | M3 |
| M5 | **Wheelhouse signs in through the wow2 instance**: instance prod, Wheelhouse prod on SSO, step-up live | the developer's first target | M4 and a typed-confirm promotion |
| M6 | a second real platform app (the Files console) joins | SSO with roles across apps | Files P1 |
| M7 | the Ocharo slice green: I14 phone pre-registration, I15, I20, the I21 subset, back-channel logout | the Telegram flows on fake channels, then one real dev bot | § 6 steps 6–7 |
| M8 | Wheelhouse: the migrate step and bridge, Ocharo's domain bound, off-host backups with a restore proof | the Ocharo gates | Wheelhouse backlog |
| M9 | Ocharo instance dev with the dev bot; Desk dev as the first client; members invited | the reset path and a member's first sign-in through the bot | M7, M8 |
| M10 | **Ocharo's apps sign in through theirs**: instance prod, then Desk, Catalogue and Brand, Studio, Marketing and Editorial one by one; the old paths retire | Ocharo's cutover | M9, the residency check |

---

## Open decisions

Continuing the hub's queue. Each line: the question → the pick.

- [x] Q59 wow2 instance scope: operator-only, invite-only, private on the control host; Form 3 for portfolio users
  becomes a separate later instance on a products host (narrows Q4 and Q54) → yes (2026-10-27); members join by
  invite link, never by an admin typing their fields
- [ ] Q60 first OIDC client: the canary on dev, then Wheelhouse dev, then Wheelhouse prod → yes
- [ ] Q61 role model: one organization per instance, one role per member, app access per member, permissions
  namespaced by app with only the requesting app's namespace in its token, resource scope inside each app → yes
- [x] Q62 wow2 P1 methods: passkey first, password always with TOTP, recovery codes, host CLI last; no email reset;
  the instance's default password policy (minimum 15) → yes (2026-10-27)
- [x] Q63 two owners' instances (answers Q5): one Wheelhouse instance product per instance, naming the Identity
  repository under its own slug → B for shared instances only; reopened 2026-10-28, per-product instances take A, a
  service of the product (migrations M77)
- [x] Q64 Identity's `deploy.yml`: PostgreSQL and an explicit migrate step before the first instance; ~~SQLite stays
  Form 1 only~~ → yes; PostgreSQL only (2026-10-27, migrations M40)
- [ ] Q65 Ocharo users in P1: staff only, invite-only; customers later in the same instance, sign-up on
  customer-facing clients only, no membership → yes
- [x] Q66 Desk's accounts: reset, keep the organization id, invite members again, the bot re-links (revises Q55's
  one-time copy) → reset (2026-10-27)
- [x] Q67 minimum scope: Ocharo includes back-channel logout and the I21 member subset, defers Log in with Telegram;
  wow2 defers back-channel logout and I14 → yes, revised 2026-10-27: wow2 ships I14 invite links in P1, defers
  back-channel logout
- [ ] Q68 backups gate: only Ocharo's cutover waits on off-host backups; the wow2 instance goes live before them →
  yes

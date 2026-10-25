# Identity — full analysis before the build

*Last updated: 2026-10-25*

> The analysis batch behind `wow-two-platform.identity` (#2 in [platform apps](../../docs/platform-apps.md)): every
> integration, the feature vector against the market, the code we already have, how products plug in, and whether
> the be sdk splits. The [service spec](../identity-service-spec.md) stays the build source; settled findings move
> into it, and this folder keeps the evidence.

## Inputs

- spec: [identity-service-spec.md](../identity-service-spec.md) — D1 OpenIddict on our own store, D2 one instance
  per owner, D3 one person per instance; D4 and D5 open in [platform decisions](../../docs/platform-decisions.md).
- be sdk slices: `wow-two-sdk-beta.be` `engineering/research/identity/identity-slices.md` — I1–I13 done, I14–I22 planned.
- capability forms: [capability-forms.md](../../conventions/development/capability-forms.md) — one contract, three forms.
- developer, 2026-10-25: a product reaches a running Identity through an API client behind the
  [broker](../../conventions/development/backend/dotnet/core/mla/constructs/behavior/broker.md) contract.
- developer, 2026-10-25: the SDK will split into one repo per domain — be library, fe library, service (be + fe)
  and Docker together; T5 weighs Identity as the first such repo. This departs from capability forms § Layout.

---

## Tracks

| # | Track | File | Wave | State |
|---|---|---|---|---|
| T1 | Third-party integrations: protocol, channels, providers, infra | [t1-integrations.md](t1-integrations.md) | 1 | ✅ |
| T2 | Feature benchmark against the market | [t2-benchmark.md](t2-benchmark.md) | 1 | ✅ |
| T3 | Code reality and consumer inventory | [t3-code-and-consumers.md](t3-code-and-consumers.md) | 1 | ✅ |
| T4 | Integration modes: in-process, API client broker, OIDC sign-in, service tokens | [t4-integration-modes.md](t4-integration-modes.md) | 2 | ✅ |
| T5 | SDK split: Identity as the first per-domain repo (be + fe library, service, Docker) | [t5-sdk-breakdown.md](t5-sdk-breakdown.md) | 2 | ✅ |
| T6 | Hosting, security and conformance for Forms 2 and 3 | [t6-hosting-security.md](t6-hosting-security.md) | 2 | ✅ |
| T7 | Library architecture: abstractions layer, package graph, what the main SDK references | [t7-library-architecture.md](t7-library-architecture.md) | 3 | 🔄 |
| T8 | Domain library repo template and the rollout checklist | [t8-library-template.md](t8-library-template.md) | 3 | 🔄 |

- waves 1–2 landed 2026-10-25; wave 3 answers the developer's high-level breakdown ask of the same day.

---

## Points

The decision queue: parents before children, blocking first. Each line: the question → the pick, and the track
holding the evidence. Tick a line when the developer answers; the answer moves into the spec.

### A · Placement and shape — blocks the build

- [ ] Q1 Identity leaves the be sdk for its own repo (be + fe library, service, Docker) as P1 step 0 → yes, no blocker (T5)
- [ ] Q1a repo org: `wow-two-sdk-beta.identity` or `wow-two-platform.identity` → sdk-beta (T5)
- [ ] Q1b six packages: Contracts, Client, Module, Providers, Server, Testing; Form 3 takes Contracts + Client (T4, T5)
- [ ] Q1c the auth primitives staying in core rename to `…Be.Auth.*` (39 product files) → rename (T5)
- [ ] Q1d versions from tags with no release commit; a CI job tests Identity against each core release → both (T5)
- [ ] Q2 one registration, `Identity:Mode = Module | Oidc`, same routes, claims, brokers and events → yes (T4)
- [ ] Q3 Form 1 → 3 move: strictly config, or config plus deleting the module package → allow the delete (T4)
- [ ] Q4 Form 3 host: the control host is off-limits for products → a WoW2 products host, none exists yet (T6)
- [ ] Q5 two owners' instances of one image in Wheelhouse (descriptor keys one slug per repo) → model before Ocharo (T6)
- [ ] Q6 D2 widens to one instance per owner and per residency, with an onshore option → yes (T6)

### B · Tokens and protocol

- [ ] Q7 browser mode for Forms 2/3: BFF only, SPAs holding tokens forbidden → forbid (T4)
- [ ] Q8 organization scope in tokens: one active organization with switching, not every membership → one (T2, T4)
- [ ] Q9 revocation: short access tokens, offline JWKS checks, custom back-channel logout; no introspection in P1 (T1, T4)
- [ ] Q10 front-channel logout: OpenIddict has no plans → drop from P2 (T1)
- [ ] Q11 management calls: the product checks the acting user in P1; token exchange in P2 → product check (T4)

### C · Sign-in methods — Ocharo P1

- [ ] Q12 D4: bot code + Log in with Telegram in P1; Gateway deferred, it is paid in TON only (T1)
- [ ] Q13 D5: Identity owns the Ocharo bot webhook; others send through the Bot API → yes (spec)
- [ ] Q14 after first link, identity keys on the Telegram user id, never the phone claim → yes (T6)
- [ ] Q15 UZ SMS: Eskiz primary, Twilio and Vonage fallback; Eskiz needs a UZ legal entity (`ven-t-012`) (T1)
- [ ] Q16 social buttons: Google, Apple, Telegram, Microsoft, Yandex hosted; drop Spotify, Reddit, X; VK → VK ID (T1, T2)
- [ ] Q17 ForeverPin: redirect with a Google hint, or keep one-tap by exchanging the Google ID token (T4)

### D · Feature scope

- [x] Q18 (developer: agreed 2026-10-25) add to P1: test mode with fake channels, operator passkey or TOTP, claims-contributor hook, OTel + health (T2, T6)
- [ ] Q19 add to P1: CSP `frame-ancestors`, no third-party assets on hosted pages, OTP hashed + bound + 30 s resend (T6)
- [x] Q20 (developer 2026-10-25: keep all, configurable) composition, expiry, history, minimum length as policy
  settings; defaults off and minimum 15, per NIST SP 800-63B (T2, T6)
- [ ] Q21 add to P2: bulk import with foreign hashes, token exchange, erasure fan-out, consent records, guest upgrade (T2)
- [ ] Q22 add to P2: Telegram Mini App `initData`, phone and email change recovery, declarative config, paid-channel guard (T2)
- [ ] Q23 move to P3 or drop: SAML, SCIM, device flow, impossible travel, WhatsApp, account merge → link only (T2)
- [ ] Q24 hash-chained trail → events into the audit capability; charts → OTel + Grafana (T2)

### E · Security and operations

- [ ] Q25 signing keys: Wheelhouse-rendered host files as X.509 with staged `NotBefore`; I17 = key-source seam (T6)
- [ ] Q26 Data Protection ring in PostgreSQL, certificate-protected, ASP.NET ≥ 10.0.7 (T1, T6)
- [ ] Q27 counsel reading of the telecom-user clause before a UZ-audience product joins Form 3 (T6)
- [ ] Q28 conformance suite in CI with a `Testing` host mode; certification deferred (T6)
- [ ] Q29 D13 email: SES, already wired and cheapest (T1)
- [ ] Q30 domain binding and off-host backups gate Ocharo's cutover (Wheelhouse iterations 11, 12) (T6)

### F · Migration

- [ ] Q31 one migrator for identity tables across Form 1 hosts and the service before I14–I16 (T3)
- [ ] Q32 Ocharo: Desk runs Microsoft `AddIdentityCore` with text ids → rename + key-type plan; port Desk's prototypes (T3)
- [ ] Q33 Haven's several phones per user vs one `PhoneNumber` → settle the model before Haven moves (T3)
- [ ] Q34 Wheelhouse stays Form 1: it deploys Identity and must sign in without it → yes (T3)

### Self-served

- ✅ spec facts corrected from T3: 113 tests, I13 shipped, OTP defaults, Desk session store, OpenIddict support
- ⬜ build-step facts, no decision: OpenIddict 6.0.0 → 7.7.2 with EF Core ≥ 10.0.11; Fido2 3.0.1 → 4.3.1 (security)
- ⬜ claim vocabulary converges on `sub`, `sid`, `org_id` before an OIDC client ships (T4)
- ⬜ split prerequisites: an error-text hook in `Web/ErrorTranslation`, delete `IdentityApi/` and `Policies/`, own publish workflow (T5)

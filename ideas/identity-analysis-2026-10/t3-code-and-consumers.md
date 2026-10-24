# T3 — Identity code and consumers

*Last updated: 2026-10-25*

> What the be sdk, the fe sdk and every product ship for auth today, set against `identity-service-spec.md`: P1 protocol slices I17–I19 do not exist; Ocharo is the largest migration.

Path aliases (all under `W/workbench/`):

- `be` = `wow-two-sdk-beta/wow-two-sdk-beta.be/engineering/codebase/wow-two-sdk-beta-be/src`
- `fe` = `wow-two-sdk-beta/wow-two-sdk-beta.fe/engineering/codebase/wow-two-sdk-beta-fe/src`
- `oc` = `mfts-projects/ventures/ocharo-hq/ocharo-ws/workbench`
- Latest published be sdk: `10.0.76-beta` (carries I13); fe sdk `0.0.32`.

---

## A · be sdk Identity

### Test run

- `dotnet test Identity.Tests/WoW.Two.Sdk.Beta.Be.Identity.Tests.csproj`, run 2026-10-25 from `be`.
- Result: 113 passed, 0 failed, 0 skipped, 3 s.
- 95 `[Fact]`/`[Theory]` methods; no Docker; in-memory SQLite plus `WebApplicationFactory`.
- Spec says "about 92 tests"; real count is 113.

### Folders

| Folder (files) | Does | Maturity | Known issues |
|---|---|---|---|
| `ApiKeys/` (15) | marker-prefixed keys stored as hashes, `ApiKey` scheme (Bearer or `X-Api-Key`), scope policies, access-gate middleware | 17 tests; `api-keys.md` + `ApiKeys.spec.md`; used by Wheelhouse, TranscriptForge | `IApiKeyRepository` is product-owned, so each consumer writes its own; outside the Identity service scope |
| `Authorization/` (5) | principal allowlist (open when empty) + default-deny fallback on one scheme | no direct tests (6 via `AllowlistedSessionOrApiKeyAuthorizationTests`); `authorization.md` + spec + standard; used by Wheelhouse, Desk, 10 pilots | empty allowlist admits any authenticated user, so each host must guard it (Wheelhouse throws when deployed) |
| `Claims/` (8) | `wt:*` claim normalizer across 17 OAuth providers (`IClaimsTransformation`) | 0 tests; `claims.md` + spec + standard; Wheelhouse only | 6 provider profiles best-effort and unverified (X, Yandex, VK, Amazon, Slack, Notion); moot once Identity is the only issuer |
| `Cookies/` (3) | `AddCookieAuthentication`, secure defaults, `Mvc`/`Api` challenge mode | indirect tests (stamp sign-out); `cookies.md`; 13+ consumers | options built eagerly, no `Identity:*` host-section binding unlike other modules |
| `CurrentUser/` (5) | tri-state view: user / guest / anonymous | 2 tests in `ConfiguredRegistrationTests`; ForeverPin | none found |
| `Guest/` (6) | anonymous capability cookie sealed by Data Protection | 4 tests; `guest.md` + spec; ForeverPin | key-ring loss loses every guest; guest-to-user merge lives in product code |
| `Core/` (140) | own user store, 11-table EF schema, slices below | see sub-rows; `core.md` + 15 slice docs | consumers must add an EF migration for each schema addition (I10, I13 already did); no foreign keys |
| `IdentityApi/` (1) | `AddIdentityApiEndpoints` preset over Microsoft `AddIdentityCore` + `MapIdentityApi` | 0 tests, 0 consumers | contradicts "own, not a wrapper"; superseded by `Core/Endpoints`; keeps `Microsoft.AspNetCore.Identity.EntityFrameworkCore` referenced |
| `Jwt/` (7) | bearer validation + `ITokenIssuer` HMAC issuance | 8 tests (registration only); `jwt.md`, `issuance.md` | issuance is HS256/384/512 only (`Jwt/Issuance/JwtTokenIssuer.cs:34-38`); `ValidAlgorithms` takes one value (`Jwt/JwtServiceCollectionExtensions.cs:40`); no JWKS; `IKeyProvider` named in `issuance.md` does not exist |
| `Mfa/` (5) | `ITotpService` (Otp.NET), `AddFido2WebAuthn` | indirect via TwoFactor and passkey tests | TOTP secret stored in `identity_user_tokens`; no cipher or Data Protection call found |
| `OAuth/` (23) | 17 provider wrappers with one shape + `wt:provider` stamp; Google ID-token authenticator | Google authenticator 1 test; wrappers 0 tests | only GitHub (Wheelhouse) and Google ID token (ForeverPin) have consumers; no callback-to-link route |
| `Oidc/` (2) | `AddOpenIdConnectAuthentication`: generic OIDC client, code + PKCE, userinfo claims | 0 tests, 0 consumers; `oidc.md` | client only; no back-channel logout, no org claims; needs `AddCookieAuthentication` first |
| `Otp/` (40) | `IOtpService`, generator, per-culture formatter, channels `sms` · `whatsapp` · `telegram` · `telegram-gateway` · `email` | 7 tests; `otp.md` + 5 channel docs | memory store by default (`OtpServiceCollectionExtensions.cs:34`); `OtpRecord.Code` plaintext (`OtpRecord.cs:13`); resend gap default 5 s (`OtpOptions.cs:20`) |
| `PasswordHashing/` (2) | Argon2id `IPasswordHasher<TUser>` (m=19 MiB, t=4, p=1) | rehash covered in `PasswordSliceTests`; `argon2.md` | doc still shows ASP.NET `AddIdentityCore` wiring |
| `Policies/` (4) | `IRolePolicy` role-in-scope dictionary | 0 tests; 0 consumers found | superseded by org roles and permissions (I13) |

### `Core/` sub-slices

| Slice | Tests | Notes |
|---|---|---|
| users, EF stores, principal factory | 3 + 7 | tables `identity_users` · `roles` · `user_roles` · `user_claims` · `role_claims` · `user_logins` · `user_tokens` · `refresh_tokens` · `passkeys` · `organizations` · `memberships` |
| passwords, tokens, email, lockout, stamps | 7 + 5 + 5 | rules 8–128, HIBP fails open, lockout 5 / 5 min (`LockoutOptions.cs:7,10`), tokens bound to stamp |
| roles, claims, sign-in, external logins | 7 | `UserLoginService` persists a link only; no OAuth callback route |
| `TwoFactor/` | 3 | TOTP, recovery codes (SHA-256), delivered methods over any OTP channel |
| `Phones/` | 1 | service only; no HTTP route, no fe screen |
| `EmailSignIn/` | in endpoint tests | link or code over OTP |
| `Passkeys/` | 6 | usernameless; needs shared Data Protection key ring |
| `RefreshTokens/` | 3 | rotation + family revoke; no device, IP or label columns; no list-by-user (`IRefreshTokenRepository.cs`) |
| `Organizations/` | 7 | I13; `org_role` / `org_permission` claims; last-owner guard |
| `Endpoints/` | 7 | 28 routes (`UserAccountEndpointRouteBuilderExtensions.cs`); none for phone, organizations, sessions, Telegram |
| `PersonalData/` | in endpoint tests | export + erasure hooks |

### Suspects checked

| Suspect | Result |
|---|---|
| `init`-only options (CS8852 class of bug) | None. Every `*Options` property is `set` (110 setters, 0 `init`). `AllowlistOptions`, `ClaimNormalizationOptions`, `OtpOptions` are `set`; their dictionary and `Messages` members are get-only collections, which is fine. 145 `init` remain on request/response models and records; none on a configured options type. |
| Configured-path test coverage | Only `CurrentUser`, `Guest`, `Otp` have a configure-path test. `AddClaimNormalization(configure)` has none. `AddPrincipalAllowlist(configure)` is exercised only by Wheelhouse. |
| JWT HS256-only | Issuance: yes, symmetric only. Validation: asymmetric works via `MetadataAddress` (RS/PS/ES, HTTPS enforced). |
| OTP store memory-only | Default yes. Seam `IOtpRepository` exists. Haven and Desk each wrote a PostgreSQL store. |
| `<Compile Remove>` on OAuth leaves | None left. `WoW.Two.Sdk.Beta.Be.csproj` has 0 `Compile Remove`; its comment says the block is gone. Apple, GitHub, Microsoft compile. |
| OpenIddict | Pinned 6.0.0 at `Directory.Packages.props:162-163`; 0 references in csproj or code. |

### Code against I14–I22 and spec § Gaps

| Item | State | Already there | Missing |
|---|---|---|---|
| I14 invitations, admin-created members | not started | password-less user rows (`UserAccountService.CreateAsync`); `OrganizationService.AddMemberAsync` for existing users | invitation entity, single-use link, accept-on-sign-in, phone/email pre-registration; Desk `telegram_link_requests` is the prototype |
| I15 durable OTP | not started | seam `IOtpRepository`; Haven `Haven.Auth.Persistence/Identity/Repositories/OtpCodeRepository.cs` (plaintext); Desk `BrandWorkspace.Persistence/Access/TelegramAuthRepository.cs` (Data Protection) | one SDK store; hashed at rest; per-phone / IP / client limits |
| I16 sessions, sign-in log | not started | `RevokeFamilyAsync`, `RevokeUserAsync`; 6 log messages in `IdentityLogExtensions.cs`; `Foundation/Audit` hash chain; Desk `access.sessions` | session list, device columns, sign-in log entity, security-event store |
| I17 signing keys, JWKS | not started | validation side reads JWKS through `MetadataAddress` | key store, rotation with overlap, JWKS endpoint, asymmetric issuer, `Foundation/Security` envelope cipher for key storage |
| I18 OIDC server | not started | OpenIddict pin only | authorize, token, end-session, discovery, back-channel logout, client registry |
| I19 OIDC client module | partial | `Oidc/` (code + PKCE + userinfo), `Cookies/`, `Claims/`; `Ocharo.Sso` (407 lines) as prototype | org claims, logout receiver, CSRF, per-app audience, refresh |
| I20 Telegram | not started | Telegram bot OTP channel, Gateway channel, `Telegram` login-provider convention in `TwoFactorMethodOptions.cs:19` | link-on-first-sign-in, `t.me/{bot}?start=` token, contact check, Log in with Telegram; Desk `TelegramAuthEndpoints.cs` (196 lines) is the prototype |
| I21 admin API | not started | `LockUntilAsync`, `RotateSecurityStampAsync`, `OrganizationService`, `UserRoleService` | HTTP surface; user list and search; registered-app admin |
| I22 password lifecycle | not started | rules, Argon2 rehash, HIBP | expiry, history, forced reset, temporary passwords, generator, strength score |
| Gaps · accounts | partial | organizations, memberships, roles (I13) | invitations, admin-managed members, callback-to-link route |
| Gaps · audit | not started | log lines only | sign-in log, admin trail |

---

## B · fe sdk auth

- Session core `fe/auth/`: `AuthProvider.vue`, `AuthContext.ts` (`useAuth`), `AuthSession.ts` (`unknown → resolving → authenticated | anonymous`).
- Bridge `fe/auth/AuthBridge.ts`: one expiry per session on first 401 or `bridge.expire()`; `subscribeExpired`; spec `AuthBridge.spec.md`.
- Strategies: `CookieStrategy.ts` (me-resolve, default `/api/identity/me`, sign-out `/api/identity/sign-out`), `BearerStrategy.ts`, `RedirectStrategy.ts`, `TokenStorage.ts`.
- Router glue `fe/router/adapters/vueRouter/Guards.ts`: `requireAuth`, `signInRedirect`, `buildReturnTo`/`useReturnTo`.
- Expiry notice `fe/feedback/FeedbackSessionExpiry.ts`: `feedbackSessionExpiry`.
- Google: `fe/foundation/oauth/GoogleIdentity.ts` (`provideGoogleIdentity`, GIS script loader) + `fe/presentation/actions/googleSignInButton/GoogleSignInButton.vue`.
- Account menu `fe/presentation/nav/accountMenu/AccountMenu.vue` (503 lines): identity header, organization switcher (2+ orgs), locale, colour mode, versions, sign out.
- Inputs: `passwordInput/PasswordInput.vue` (reveal toggle), `pinInput/PinInput.vue` (6 cells, `complete` event), `phoneInput/PhoneInput.vue`, `telInput/TelInput.vue`, `emailInput/`.
- Strength: `feedback/passwordStrengthCallout/PasswordStrengthCallout.vue`, naive 0–4 score from length and character classes (`:16-25`); `forms/passwordStrength/` is an empty directory.
- Absent: sign-in, phone + code, Telegram link, passkey/WebAuthn helper, MFA setup, account page, members/sessions/sign-in-log tables, hosted-page theming loader (fe backlog line 174).
- `createRedirectStrategy` and `createBearerStrategy` have no importer in any product (grep over `*.ts`, `*.vue`).
- `PasswordStrengthCallout` has no importer in any product.
- `PinInput` is used only by Haven.
- Product usage: 8 pilots + ForeverPin use `createCookieStrategy` + `AuthProvider` + `createAuthBridge`.
- documentation-checker and retainer-balance use only `createAuthBridge`; Wheelhouse uses it with its own client (`apps/web/src/integration/auth/index.ts`); Ocharo Studio uses it too.

---

## C · Consumers

Effort: S = config and frontend swap; M = data move plus code change; L = several services, data and retired paths.

### Table

| Product | Auth methods | Session shape | be sdk · identity APIs used | Target | Effort | Notes |
|---|---|---|---|---|---|---|
| Wheelhouse (`wow-two-platform.wheelhouse`) | GitHub OAuth, login allowlist `Identity:AllowedGitHubLogins`; `wh_` integration keys | cookie, 8 h, API challenge mode | `10.0.71-beta` · `AddCookieAuthentication`, `AddGitHubAuthentication`, `AddClaimNormalization`, `AddPrincipalAllowlist`, `AddDefaultDenyAuthorization`, `AddApiKeyAuthentication`, `RequireAllowlistedSessionOrApiKeyScope` (`Wheelhouse.Api/Auth/AuthConfigurationExtensions.cs:41`) | stay Form 1 | S if ever moved | deploys Identity, so signing in through it is circular; no provider-token use found (GitHub App handles repo access) |
| Secrets Vault | admin password (Argon2) → JWT HS256; data-plane opaque tokens | bearer | `10.0.56-beta` under the old id `WoW2.Sdk.Backend.Beta` · `UseArgon2PasswordHasher`, `AddJwtTokenIssuance`, `AddJwtBearerAuthentication` | retire | none | inactive, merging into Wheelhouse |
| ForeverPin (was smart-qr) | Google ID token (GIS), guest-first | cookie `foreverpin-auth`, 30 d sliding | `10.0.72-beta` · `AddGoogleIdTokenAuthenticator`, `AddCookieAuthentication`, `AddGuestSession`, `AddCurrentUser`, `AddSpaAntiforgery`; fe `0.0.26` | OIDC client of Form 3 (first, per spec) | M | `users.id` is uuid (kept as identity id), `google_subject` becomes a Google login row; guest→user merge and Stripe subscriptions key on that id; DB still named `smartqr` |
| Haven | Telegram bot code | JWT HS256 in cookie, one key shared by 5 services (`Haven.Common.Identity/HavenSessionServiceCollectionExtensions.cs`) | `10.0.74-beta` · `AddJwtTokenIssuance`, `AddJwtBearerAuthentication` (via `AddCookieJwtBearerAuthentication`), `AddOtpService`, `AddTelegramOtpDelivery`, own `IOtpRepository` | OIDC client of Form 3, after the relaunch decisions | M–L | own `users` (uuid, role enum, `telegram_user_id`) + `user_phones` (several phones per user; SDK user has one `PhoneNumber`); `otp_codes` plaintext; relaunch (realtor subscription) still open |
| First-ten pilots ×10: retainer-balance, documentation-checker, config-checker, customer-promises, epub-review, file-watch, podcast-readiness, procedure-review, training-seats, vendor-renewals | email + password | cookie, 8 h | `10.0.74-beta` · `AddUserAccounts<IdentityUser>`, `AddEntityFrameworkStores`, `AddArgon2Passwords`, `AddLockout`, `AddSignIn`, `AddSecurityStampValidation`, `AddPersonalData` (5 of 10), `AddCookieAuthentication`, `AddDefaultDenyAuthorization`; fe `0.0.27` | stay Form 1 until launch, then OIDC clients of Form 3 | S each | same SDK schema and Argon2 hash format, so rows move unchanged; each has its own `AccessDbContext` + EF migration `InitialAccess`; none maps `MapUserAccountEndpoints` |
| TranscriptForge | API keys only; no user sign-in | `ApiKey` scheme + loopback gate | `10.0.74-beta` · `AddApiKeyAuthentication`, `UseApiKeyAccessGate` | OIDC client of Form 3 at hosted launch; keys stay Form 1 | S | backlog line 66: "Google sign-in on the SDK identity vector" |
| Sift | none | none | `10.0.74-beta` · none | undecided | S | fe `AccountMenu` only; `product/context.md` asks single-user versus multi-user |
| Hijinx | none for users; opaque room bearer (`Rooms/RoomAuthenticationHandler.cs`) | custom scheme | `10.0.74-beta` · none | stay Form 1 | none | room membership checked per operation |
| Arcade | Telegram Mini App `initData` HMAC (`Telegram/Services/TelegramInitDataValidator.cs`) | none, per request | `10.0.74-beta` · none | stay Form 1; Log in with Telegram later | none | validated in command handlers |
| Ocharo Desk (`oc/ocharo-platform`, `brand-workspace.*`) | password, Telegram bot code, operator CLI `--provision-operator` | cookie `__Host-brand-workspace-session`, 8 h, row in `access.sessions` checked on every request | `10.0.71-beta` · Microsoft `AddIdentityCore<AccessUser>` (not SDK Core), `AddCookieAuthentication`, `AddDefaultDenyAuthorization`, `AddOtpService`, `AddTelegramOtpDelivery`, own `IOtpRepository`, `JwtTokenIssuer` for tickets | home of Ocharo's Form 2 instance; Desk becomes a client | L | see artifact list |
| Ocharo Brand, Catalogue (`oc/ocharo-platform`) | Desk SSO via canonical `Ocharo.Sso` (ProjectReference) | host-only cookie `__Host-ocharo-{app}` + in-memory grant | `10.0.71-beta` · `AddOcharoSso` | OIDC clients of Ocharo Identity | S–M | SSO default-off; backlog line 28: public and sign-in-free until Identity lands |
| Ocharo Studio, Marketing, Blog (editorial) (`oc/ocharo-studio`, `oc/ocharo-marketing`) | Desk SSO via copied `Ocharo.Sso` snapshots | same | `10.0.71-beta` · `AddOcharoSso`; Studio also `StudioIntegrationAuthenticationHandler` | OIDC clients of Ocharo Identity | M each | Marketing and Blog keep `IntegrationBoundaryMiddleware` |
| No auth found | PoseCoach, Matinee, ListingShelf, PbnStudio, Museums Gallery, TNIS and Mintrans cut, PRISM, Whiteout, Surface Pattern, wheelhouse-canary | — | — | decide at first need | — | grep of `*.cs` and `*.swift` |
| Out of scope | Nasiya Finance (Python backend, own JWT), Your Pocket Doctor (2025 lab, Django identity-service), POCs | — | — | — | — | not .NET be sdk consumers |

### Ocharo — artifacts to retire or migrate

Desk `oc/ocharo-platform/engineering/codebase/brand-workspace.backend-services/`:

- Tables, schema `access`:
  - migration `BrandWorkspace.Persistence/Migrations/002-access/`: `users` (text id, ASP.NET PascalCase columns), `identity_roles`, `identity_role_claims`, `identity_user_claims`, `identity_user_logins`, `identity_user_roles`, `identity_user_tokens`, `organizations`, `memberships`, `sessions`
  - migration `009-telegram-access/`: `telegram_links`, `telegram_link_requests`, `telegram_codes` (code protected with Data Protection)
  - migration `010-app-sso/`: `sso_codes`, `sso_grants`
- Maps to SDK: `organizations` → `identity_organizations` and `memberships` → `identity_memberships` (same columns); `users` and `identity_*` need a snake_case rename; `telegram_links` → a `Telegram` login row plus confirmed phone; `sessions`, `telegram_codes`, `sso_*` retire into I16, I15, I18.
- Account endpoints: `BrandWorkspace.Api/Access/AccessEndpoints.cs` (`/api/auth/login|logout|session`, `/api/organizations`), `AccessSessionIssuer.cs`, `AccessClaims.cs`, `OrganizationAccessFilter.cs`, `SessionAntiforgeryDataProvider.cs`, `OperatorProvisioning.cs`.
- Telegram bot: `BrandWorkspace.Api/Identity/Telegram/` (`TelegramAuthEndpoints.cs` `/api/auth/telegram*` incl. `/updates` webhook, `TelegramBotUpdatesHandler.cs`, `TelegramPollingService.cs`, `TelegramAuthSettings.cs`) and `BrandWorkspace.Persistence/Access/TelegramAuthRepository.cs`.
- Broker: `BrandWorkspace.Api/Sso/` (7 files: `/api/sso/authorize|exchange|refresh|revoke`), `BrandWorkspace.Persistence/Sso/SsoGrantStore.cs`, `BrandWorkspace.Application/Sso/SsoContracts.cs`.
- Tickets: `BrandWorkspace.Api/Integrations/IntegrationTickets.cs` (`/api/organizations/{id}/integration-tickets`, `/api/integrations/introspect`, HS256 via `Integrations:SigningKey`), `BrandWorkspace.Api/Mcp/DeskMcpAuthenticationHandler.cs` (audience `ocharo-desk-mcp`, 5-minute access).
- Persistence and application: `BrandWorkspace.Persistence/Access/` (`AccessDbContext.cs`, `AccessRepository.cs`, `AccessUser.cs`), `BrandWorkspace.Application/Access/`.
- Tests: `tests/BrandWorkspace.Tests.E2E/Access/Sso*Tests.cs` (3 files), `tests/BrandWorkspace.Tests.E2E/IntegrationTicketTests.cs`.
- Config: `Sso:Enabled`, `Sso:Clients[]` (id, redirect URI, audience, organization, `SecretSha256`), `Integrations:SigningKey`, Telegram bot settings.
- Desk frontend `brand-workspace.frontend-services/apps/web/src/`: `presentation/workspace/LoginPage.vue`, `SessionGate.vue`, `AccountSettings.vue`, `IntegrationsPage.vue`, `McpAccessPanel.vue`, `integration/workspace/WorkspaceApi.ts` (auth calls), `TelegramDecoders.ts`, `domain/workspace/TelegramAccess.ts`, `SignInDestination.ts`, `domain/shared/TelegramUiMessages.ts`.

Client side (`Ocharo.Sso`, 5 `.cs` files, 407 lines):

- Canonical: `oc/ocharo-platform/engineering/codebase/ocharo-sso/Ocharo.Sso/` (`SsoMiddleware.cs`, `SsoBackchannel.cs`, `SsoSessionStore.cs`, `SsoOptions.cs`, `SsoRegistration.cs`) + `Ocharo.Sso.Tests/SsoFlowTests.cs`.
- Referenced in place by `ocharo-brand.backend-services/OcharoBrand.Api` and `ocharo-catalogue.backend-services/OcharoCatalogue.Api` (`ProjectReference` + `.slnx`).
- Byte-identical snapshots, each with `README.md`, `snapshot.json` (SHA-256 list) and `../sync-sso.py`:
  - `oc/ocharo-studio/engineering/codebase/ocharo-studio.backend-services/shared/Ocharo.Sso/`
  - `oc/ocharo-marketing/engineering/codebase/ocharo-marketing.backend-services/shared/Ocharo.Sso/`
  - `oc/ocharo-marketing/engineering/codebase/ocharo-blog.backend-services/shared/Ocharo.Sso/`
- App sessions are in memory per instance (`SsoSessionStore.cs`, 10 000 entries cap); Desk's side is durable.
- Host wiring to replace: `AddOcharoSso(...)` / `UseOcharoSso(...)` in each `HostConfiguration*.cs`; Brand and Catalogue also have `HostConfiguration.Sso.cs` and `tests/*/SsoBoundaryTests.cs`; Marketing and Blog have `tests/*/SsoHostTests.cs`.
- Config key per app: `Identity:Sso` (`Enabled`, `DeskOrigin`, `ClientOrigin`, `ClientId`, `ClientSecret`, `OrganizationId`).

Old ticket-introspection handlers (3):

- `oc/ocharo-studio/.../OcharoStudio.Api/Studio/Access/StudioIntegrationAuthenticationHandler.cs`
- `oc/ocharo-marketing/.../OcharoMarketing.Api/Marketing/IntegrationBoundaryMiddleware.cs`
- `oc/ocharo-marketing/.../OcharoBlog.Api/Blog/IntegrationBoundaryMiddleware.cs`

Frontend session clients (4, plus Desk's own):

- `oc/ocharo-platform/.../ocharo-catalogue.frontend-services/apps/web/src/integration/common/OcharoSsoClient.ts` + `presentation/common/SsoConnection.vue`
- `oc/ocharo-platform/.../ocharo-brand.frontend-services/apps/web/src/integration/common/OcharoSsoClient.ts` + `presentation/common/SsoConnection.vue`
- `oc/ocharo-studio/.../ocharo-studio.frontend-services/apps/web/src/integration/studio/SsoAccess.ts` (+ `access.ts`)
- `oc/ocharo-marketing/.../ocharo-marketing.frontend-services/packages/connect/src/session.ts` (shared by Marketing and Editorial)

Docs and the sync tooling to remove with them:

- `oc/ocharo-platform/engineering/architecture/app-sso-client.md`, `ocharo-sso/README.md`, each snapshot `README.md` and `shared/sync-sso.py`.

---

## Spec corrections

- § What already exists: "about 92 tests" → 113 cases (95 methods), all green.
- § What already exists omits organizations and memberships; they shipped as I13 (`identity_organizations`, `identity_memberships`, `OrganizationService`, `org_role` / `org_permission` claims) and are in `10.0.76-beta`.
- § Gaps · accounts lists "organizations, memberships" as missing; only invitations, admin-managed members and the callback-to-link route are.
- § Problem: Desk's broker does not keep sessions in memory; each app's `Ocharo.Sso` does (`SsoSessionStore.cs`). Desk stores codes and grants in `access.sso_codes` / `access.sso_grants`.
- § Problem: five apps (Brand, Catalogue, Studio, Marketing, Blog/Editorial) use the broker; Brand and Catalogue reference the canonical project rather than a copy.
- § Gaps · protocol: "JWT is HS256 only" is true for issuance only; validation already accepts RS/PS/ES through `MetadataAddress`.
- § Abuse protection P1 "hashed at rest" and "30-second resend": SDK default stores `OtpRecord.Code` plaintext and resends after 5 s; Desk protects codes with Data Protection; Haven stores plaintext.
- § Ocharo slice: bot flow "stays consumer-owned" per `Otp/Telegram/telegram.md`; the spec moves it into Identity, so that doc needs a rewrite with I20.
- § Build path: OpenIddict 6.0.0 is pinned; whether it supports .NET 10 / EF Core 10 is unverified.
- § What already exists "phone OTP sign-in": exists as `UserPhoneService` only; `MapUserAccountEndpoints` has no phone route.
- fe line "`passwordStrength` is empty": correct, the directory `fe/presentation/forms/passwordStrength/` is empty; the working meter is `PasswordStrengthCallout`.
- be sdk backlog line 137 says "Organizations first"; I13 is done (`wow-two-sdk-beta/wow-two-sdk-beta.be/engineering/planning/backlog.md`).
- Lead docs for `Jwt`, `Cookies`, `Oidc`, `Mfa/*`, `PasswordHashing`, `IdentityApi`, `OAuth/*` still show `dotnet add package WoW.Two.Sdk.Beta.Be.Identity.*` per-folder installs; everything ships in `WoW2.Sdk.Beta.Be`.

---

## Findings

- The OIDC server spine is absent: I17 (keys, JWKS), I18 (authorize, token, discovery, logout) and I19 (full client) have no code; OpenIddict is pinned and unreferenced. Every Ocharo migration step and all Form 3 clients depend on them.
- Ocharo is the largest migration (L): Desk plus 5 broker clients, 4 frontend clients, 3 introspection handlers, 3 `Ocharo.Sso` snapshots, 15 `access.*` tables, Telegram bot, MCP auth. Desk runs Microsoft `AddIdentityCore` with PascalCase columns, not SDK Core, so users need a rename and key-type decision (text ids).
- Desk and `Ocharo.Sso` are working prototypes for I14, I15, I19, I20 (link request token, Data-Protected code store, PKCE client with CSRF, contact-linked bot). Port them rather than redesign.
- Slices I8–I13 (refresh tokens, 2FA, passkeys, email sign-in, account endpoints, organizations) have zero product consumers; they are proven only by 113 in-memory SQLite tests. The only production use of Core is the pilots' password + lockout + stamp set.
- Each SDK schema addition forces one EF migration per consumer database (pilots keep `InitialAccess`); Desk, Haven and ForeverPin use hand-written SQL migrations instead. Form 2/3 needs one agreed migrator before I14–I16 add tables.
- OTP defaults are weak for a hosted service: memory store, plaintext code at rest, 5 s resend, no per-IP or per-client limits. Haven's own store repeats the plaintext shape.
- Phone and Telegram sign-in have services but no HTTP routes or fe screens; the account API has no organization, session or admin routes. P1 needs new endpoints, not only new slices.
- Sessions cannot be listed: refresh tokens carry no device, IP or label, and the repository has no list-by-user call. I16 adds columns and a repository method.
- Product pins lag: Ocharo and Wheelhouse on `10.0.71`, ForeverPin `10.0.72`, Haven/pilots/TranscriptForge `10.0.74`; none has I13 (`10.0.76`). fe pins span `0.0.26`–`0.0.31` against `0.0.32`.
- Wheelhouse should stay Form 1: it deploys the Identity image and must sign in without it.
- Haven's `user_phones` (several phones per user) does not fit the single `PhoneNumber` on `IdentityUser`; settle the model before its migration.
- Test gaps that matter before P1: no tests for the claim normalizer, the 17 OAuth wrappers, `Oidc/`, `Cookies/` or default-deny directly.
- fe sign-in kit is almost empty: `createRedirectStrategy` fits the OIDC redirect but has no importer; no passkey helper, no sign-in or MFA screens.
- TOTP secrets show no encryption at rest in code searched; `Foundation/Security` envelope cipher is available to reuse.
- `IdentityApi/` (ASP.NET wrapper) is dead weight with 0 consumers and 0 tests; removing it drops a package reference.

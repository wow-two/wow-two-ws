# Handoff — secrets-vault next phase (project reorg + admin auth)

*Written 2026-06-10. Fresh-chat resume context. Super-compact by design.*

## 0 · Read-first paths
- Standard (just rewritten): `wow-two-ws/conventions/development/repo/repo-structure.md`
- Vault: `wow-two-ws/workbench/wow-two-platform/wow-two-platform.secrets-vault/` → backend `engineering/codebase/secrets-vault.backend-services/Wow-Two-Platform.Secrets-Vault.sln` (5 projs `SecretsVault.{Api,Application,Domain,Infrastructure,Persistence}`); frontend `engineering/codebase/secrets-vault.frontend-services/`
- Kit source: `wow-two-ws/workbench/wow-two-sdk-beta/wow-two-sdk.backend.beta/src/`
- SmartQr exemplar: `wow-two-ws/workbench/ventures/smart-qr-poc/platform/src/backend/SmartQr.sln`

## 1 · DONE (don't redo)
- **Conventions overhaul** (this session): top-level `product/` + `engineering/`; all code under `engineering/codebase/`; code dirs `{slug}.backend-services/` + `{slug}.frontend-services/` (dot-prefixed by repo slug, collision-avoidance); **no README below root** — every folder leads with `{folder}.md`; tests in `{slug}.backend-services/tests/`; contracts (FE-consumed client→frontend, BE-consumed→`{Brand}.{Svc}.Client` pkg in backend); deployment per-service-image + compose, Dockerfile in `engineering/deployment/`, context `engineering/codebase/`.
- **Solution-folder grouping doc** (2026-06-13): moved out of `repo-structure.md` into **`conventions/development/backend/service-architecture.md` → "Solution organization"** (5 folders `services/ platform/ libraries/ tools/ tests/` + per-folder semantics + SmartQr exemplar + `.sln`/`.slnx` GUID encoding). `repo-structure.md` §5 rule 4 slimmed to a pointer; `backend-conventions.md` index row updated. Rationale: it's virtual .NET *solution* org (backend code concern), not repo on-disk layout.
- **Template** (`wow-two-sdk-beta.product-template`) re-scaffolded: ships a real `Sample.*` Clean-Arch + Vite example (builds clean), slim `{{PLACEHOLDER}}` docs, `{slug}.`-prefixed dirs. **create-repo** skill+`scaffold.sh` = copy-template + rebrand `Sample`→Brand + port reassign (dry-run verified).
- **secrets-vault**: conformant to all the above; on kit `WoW2.Sdk.Backend.Beta 10.0.21-beta` (mediator, FluentValidation, `Result`/`DomainError`→ProblemDetails, `IKeyedEntity`); v1.0 ✅, v1.1 iter-1 (SDK adoption) ✅, **iter-3 (admin auth) ✅ (2026-06-13)**. Backend builds 0-err. v1.1 iter-2 (UI-lib) + iter-4 (ops) pending.

## 2 · The kit (WoW2.Sdk.Backend.Beta, 10.0.21-beta on nuget.org)
- PackageId `WoW2.*` (owned); assembly+namespaces `WoW.Two.Sdk.Backend.Beta.*`. Mono-lib (huge closure). CI auto-bumps `10.0.z-beta` every push to main; `Directory.Build.props` is version source.
- **Ships + vault uses:** Result/DomainError, mediator (`AddMediator`/`ISender`/`IRequestHandler`), validation pipeline, `IKeyedEntity<TId>`, `AddTraceAwareProblemDetails`+`AddValidationExceptionHandler`.
- **Ships, vault NOT yet using (wire for iter-3):** `Argon2PasswordHasher<T>`, `ITokenIssuer`/`JwtTokenIssuer`, `AddJwtBearerAuthentication`, `AddPerIpSlidingWindowRateLimit`, `Foundation/Time`.
- **Kit GAPS (grep-confirmed — real platform-extraction targets):** AES-GCM cipher, envelope/DEK-KEK seal, hash-chained audit, DateTimeOffset→binary EF converter, Result→Problem bridge.

---

## T1 · secrets-vault project reorg + platform extraction
**STATUS (2026-06-13): ✅ grouping done.** The 5 projects now sit under `services/`; empty `platform/` + `tests/` solution folders declared (reserved). `.sln` verified via `dotnet sln list`. **Remaining T1 = the crypto platform EXTRACTION** (code-move below) — not yet started.

Split out the SDK-extractable generics as `SecretsVault.Platform.*` so the eventual lift to the beta SDK is **move + namespace-rename, not rewrite**.

**Target layout** (`secrets-vault.backend-services/`):
```
services/   SecretsVault.{Api,Application,Domain,Infrastructure,Persistence}   ← the vault product
platform/   SecretsVault.Platform.Cryptography   ← AesGcmCipher, EncryptedPayload
            SecretsVault.Platform.Envelope       ← ISealKeeper, EnvKekSealKeeper, ICryptoCore, CryptoCore, EnvelopeCryptoOptions(was VaultCryptoOptions)
            (SecretsVault.Platform.Data.Audit)   ← DEFERRED — hash-chain base; see risk
tests/      SecretsVault.*.Tests                 ← create (none yet)
```
- **PLATFORM (lift):** `Infrastructure/Crypto/{AesGcmCipher,CryptoCore,EnvKekSealKeeper,VaultCryptoOptions}.cs` + `Domain/Crypto/EncryptedPayload.cs` + the `ICryptoCore`/`ISealKeeper` interfaces (move from Application). Generic AEAD + envelope; zero vault concepts. Lift→`…Beta.Security.{Cryptography,Envelope}`.
- **BUSINESS (stays `services/`):** all entities/enums (namespaces, secrets, versions, DataKey, AccessToken, AuditEntry + vault columns), `ISecretStore`/`EfSecretStore`, `VaultDbContext`, `ITokenAuthenticator` (ns-scoped — too coupled to lift), all handlers/controllers/`DataPlaneAuthFilter`, host wiring.
- **ALREADY-IN-KIT (drop/consume):** `IClock`/`SystemClock` → kit `Foundation/Time`/`TimeProvider`. Result→Problem mapping is dup'd ~10× in controllers — candidate for a kit `Result↔ProblemDetails` bridge (`…Beta.Web.ProblemDetails`).
- **Refs invariant:** `services → platform`, never reverse; `platform/*` ref only kit+BCL. (Moving crypto contracts to `platform/` removes an infra→app coupling — net cleaner.)
- **RISK / sequencing:** the audit **hash-chain** is generic in principle but `EfAuditLog.ComputeHash` bakes in vault columns (field-ordering) — extracting it cleanly needs a base `IHashChainedEntry` + canonical-payload seam, and changing hash inputs on a **tamper-evident ledger** is a migration/repro hazard. → **Recommended first slice: Cryptography + Envelope only**; defer Audit-chain + the DateTimeOffset converter (leave inline) until deliberately designed. Reorg is refs-only/low-risk; do the `using`/`namespace` sweep in lockstep. Cross-org lift (vault is `wow-two-platform`; SDK is `wow-two-sdk-beta`) = a deliberate SDK PR, not silent.

**`.sln` solution-folder encoding (from SmartQr, classic `.sln`):** folder = `Project("{2150E333-8FDC-42A3-9474-1A3956D46DE8}") = "platform","platform","{newGuid}"`; membership via `GlobalSection(NestedProjects)=preSolution` lines `{childGuid}={folderGuid}`; empty folders just omit NestedProjects lines. (Drydock/SDK use `.slnx` XML `<Folder>/<Project>` — same logical grouping.)

## T2 · v1.1 iter-3 — authenticate the management plane (LOCAL login+pass, NO external IdP)
**STATUS (2026-06-13): ✅ DONE.** Implemented (backend 5 layers + FE), backend builds 0-err, runtime-verified (curl matrix: no-token→401, wrong→401, right→JWT `sub:admin`, bearer→200, create→201, `/api/secrets` gated, `/v1/` gone) + browser-verified (login→dashboard→sign-out). All 6 repo docs updated. **Kit gotcha:** `AddJwtBearerAuthentication` has init-only `JwtOptions` (CS8852, unusable) → bearer validation wired by hand via `AddJwtBearer`; kit `AddJwtTokenIssuance` (issuance) used as-is. Below = as-built spec.
Decided: local credential, **not** OAuth (don't depend on an external IdP for a secrets manager). "One account across the apps" = separate future ecosystem-auth concern.
- **ALSO drop URL versioning:** data-plane route `/api/v1/secrets/{ns}/{key}` → **`/api/secrets/{ns}/{key}`** (no `/v1/` for now). `SecretsController` route + FE client + `.http`.
- **Infra:** `AddJwtTokenIssuance` (HS256, issuer/aud `secrets-vault`, 1h) + Argon2 verify (kit `Argon2PasswordHasher`, `FixedTimeEquals`) + `AdminAuthOptions{ VAULT_ADMIN_PASSWORD_HASH, VAULT_ADMIN_JWT_KEY }` (runtime env, **fail-closed** if unset).
- **App:** `Auth/Commands/Login/{LoginCommand,Handler,Validator}` → `Result<AdminSessionDto{token,expiresAtUtc}>`; ports `IAdminAuthenticator` + `IAdminTokenIssuer` (keep Application infra-free); audit login success/deny + source IP. Add `AuditAction` login value (Domain, additive).
- **Api:** `AddJwtBearerAuthentication` (**`RequireHttpsMetadata=false`** — loopback behind tunnel, else tokens never validate) + `AddPerIpSlidingWindowRateLimit`; pipeline `UseAuthentication/UseAuthorization` (after static, before MapControllers) + `UseRateLimiter`; new `AuthController POST /api/admin/session` (`[AllowAnonymous]`, rate-limited); `[Authorize]` on `AdminSecretsController` + `NamespacesController`; replace hardcoded actor `"admin"` → `User.FindFirstValue("sub")` (delivers iter-3's "record who" for free). **Data plane untouched** (keeps `DataPlaneAuthFilter`+`X-Vault-Token`). Keep `/health` + `/api/system/status` + `/api/admin/session` anonymous.
- **No Persistence change** (env credential; DB multi-operator deferred). **FE:** in-memory token (not localStorage) + `Authorization: Bearer`, 401→clear→login; `LoginForm` + `useAuth` gate in `App.tsx` (no router).
- **Edge:** admin login MUST work while **sealed** (no master-key dependency); bootstrap doc for `VAULT_ADMIN_*`.
- **Verify:** `GET /api/admin/namespaces` no-token→401 (today 200=the bug); wrong pass→401+audit; right→token; bearer→200; bad-login×N→429; setSecret audit shows real subject; admin login works sealed.
- **Files:** `Api/Configurations/HostConfiguration{,Extensions}.cs`, `Api/Controllers/{AdminSecrets,Namespaces}Controller.cs`, `Infrastructure/DependencyInjection.cs`, FE `src/api/client.ts`+`App.tsx`. Kit refs: `…/src/Identity/Jwt/{Issuance/,*}`, `…/src/Identity/PasswordHashing/Argon2/`, `…/src/Web/RateLimit/`.
- **iter-3 ↔ T1:** disjoint code (crypto/audit vs Api+Application login); admin-auth is all kit bricks (no new platform primitive). Only overlap: both append audit — if Audit-chain extraction is in flight, land it first. Reorg-first gives a clean `services/` to add the admin controller into.

**Doc updates on iter-3 done:** `versions/v1.1/v1.1.md` iter-3 boxes; `planning/backlog.md` remove "authenticate management plane"; `planning/planning.md` tracker Management plane ⚠️→✅; `architecture.md` swap the "unauthenticated" note for the scheme + `RequireHttpsMetadata=false` note; `deployment/deployment.md` add the two env vars; `product/context.md`.

## T3 · roll solution-folder grouping to other repos
- ✅ **Documented** (2026-06-13) in `backend/service-architecture.md` → "Solution organization" (the convention's new home).
- smart-qr **already** has it (the exemplar). secrets-vault now grouped (T1 status). Apply to **drydock** + future. Template/create-repo already updated. Audit-track in `repo-structure.md` §11.

---

## Git & state
- **Assistant is read-only on git; the developer does ALL commits/pushes.** Everything below is uncommitted.
- 3 repos dirty: `wow-two-ws` (conventions rewrite + `scripts/active.sh` + `conventions/.../ports.md` + `.claude/skills/create-repo/*` + `engineering-planning/` rename + this handoff), `secrets-vault` (full conform + prefix re-align), `wow-two-sdk-beta.product-template` (slim + `Sample` example + prefix). Kit `10.0.20/21-beta` already published; secrets-vault pins `10.0.21-beta`.

## Run/build (secrets-vault)
```
ulimit -n 65535; export MSBUILDDISABLENODEREUSE=1
dotnet build engineering/codebase/secrets-vault.backend-services/Wow-Two-Platform.Secrets-Vault.sln -m:1   # 0 err, 25 warn (kit NU190x vuln advisories, non-blocking)
# run: cd …/secrets-vault.backend-services; export VAULT_MASTER_KEY=$(openssl rand -base64 32); dotnet run --project SecretsVault.Api  (https 8200 / http 8201)
```

## Security model (Q3 — why "any browser" is safe)
Two gates: **network boundary** (host binds loopback `127.0.0.1:8200`, reached only over Tailscale/SSH tunnel — not public; "any browser" = any browser on an already-authorized device) **+ per-plane auth** (management `/api/admin/*` → admin login [iter-3]; data `/api/secrets/{ns}/{key}` → namespace token `X-Vault-Token`, held only by apps, never the browser). Loading the SPA ≠ reading secrets — the SPA is UI; every call is authenticated. Tightest topology: co-locate apps → data plane loopback-only, never crosses a network; only the dashboard needs the tunnel.

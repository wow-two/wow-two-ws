# backend-beta-build context

*Last updated: 2026-06-10*

## Quick state

- **Repo**: `workbench/wow-two-sdk-beta/wow-two-sdk.backend.beta/` (its own git, gitignored from 10x).
- **Structure**: **MONO-LIB on .NET 10** — two csprojs only: `src/WoW.Two.Sdk.Backend.Beta.csproj` (publishes as `WoW2.Sdk.Backend.Beta`) + `src/testing/…Testing.csproj`. Per-area folders/namespaces unchanged. Version train `10.0.x-beta`, CI bumps on push. Rationale: repo `docs/analysis/mono-lib-migration.md`.
- **Coverage**: P0 testing + P1 foundation/observability/web + P2 mediator/identity + P3 data + **P3 http** + **auth Batch A** + **16 OAuth providers** + **meta `AddApiDefaults`** + **P4 comms/email (MailKit/SendGrid/SES)** + **P4 jobs/hangfire (+postgres)** (all 2026-06-10). **Caching deliberately skipped** — pre-fixes needed, discuss before starting. P4 remainder: messaging/CAP, webhooks, sms/push.
- Build: `cd src && dotnet build WoW.Two.Sdk.Backend.Beta.slnx -m:1` — 0 errors.

## Current state — http complete + auth Batch A shipped (2026-06-10)

**Shipped this session:**

- **http complete** (P3 outbound slice, joins core/refit/resilience): `hedging` (`AddSdkHedging` — standard-hedging preset), `header-propagation` (`AddConventionalHeaderPropagation` + `AddPropagatedHeaders`, X-Correlation-Id/X-Request-Id defaults), `auth-oauth2-client-credentials` (`AddOAuth2ClientCredentials` — per-client-name token cache, single-flight fetch, refresh skew), `auth-mtls` (`AddMutualTls` — PKCS#12 path via `X509CertificateLoader` or loaded cert).
- **Auth Batch A** — all 4 packages from `auth-extraction-analysis.md`: `Identity/Policies` (`AddRolePolicy`), `Identity/Jwt/Issuance` (`AddJwtTokenIssuance` — `JsonWebTokenHandler`, HS256/384/512, TimeProvider-driven), `Identity/Otp` (`AddOtpService` — IOtpService/IOtpStore/IOtpCodeGenerator/IOtpDeliveryHandler seams, crypto RNG, fixed-time compare), `Identity/Otp/Telegram` (`AddTelegramOtpDelivery`, dep `Telegram.Bot` 22.10.0.1).
- **OAuth expansion** — +12 providers: Facebook (first-party) + LinkedIn, Discord, Slack, GitLab, Amazon, Twitch, Spotify, Yandex, Reddit, Notion, Vkontakte (AspNet.Security.OAuth 10.0.0). Existing Apple/GitHub bumped 9.0.0 → 10.0.0. Total 16 providers.
- **Mono-lib exclusion backlog cleared** — all five CS1061s were **missing `using` directives**, not a pinning conflict: contrib + first-party OAuth `Add*` extensions live in `Microsoft.Extensions.DependencyInjection`; `AddRateLimiter`/`AddResponseCompression` live in `Microsoft.AspNetCore.Builder`. Compression, RateLimit, Apple/GitHub/Microsoft OAuth re-included; `<Compile Remove>` block deleted. Apple also updated to contrib 10.0 API (`UsePrivateKey` now wants `IFileInfo` → `PhysicalFileInfo(new FileInfo(path))`).

**Deviations from the analysis spec (deliberate):**

- `IOtpStore` slimmed: dropped `FindActiveAsync(subject, code, scope)` — the service compares codes fixed-time against `FindLatestPendingAsync`; "pending" = unconsumed regardless of expiry so `Expired` can surface.
- `OtpFailureReason.ScopeMismatch` dropped (unreachable with scope-keyed lookups).
- Options are house-style mutable classes with get-only collection properties (not init-only records).

**Open questions §11 resolved**: Telegram.Bot = MIT ✓ · `IRolePolicy` returns bool ✓ · `CreateAsync` returns code, caller delivers ✓ · `MemoryOtpStore` = Singleton ✓.

**Next**: **own sliced identity rebuild** — reverses the v1 "no user model" decision; deep-dive at repo `docs/planning/identity/identity-architecture.md`, tracked in repo `docs/planning/platform-planning.md` (new standing roadmap+backlog, format per `conventions/planning/platform-planning/`). Then: caching slice (after pre-fixes) · Haven.Auth dogfood · P4 remainder (messaging/CAP + webhooks + sms/push).

## Planning tree (new 2026-06-10)

- Repo `docs/planning/platform-planning.md` = standing roadmap + backlog of all lego features (the tracker). Deep-dives at `docs/planning/<feature>/<feature>-architecture.md`.
- First deep-dive: `docs/planning/identity/identity-architecture.md` — own ASP.NET-Identity-compatible user model as orthogonal store slices composed in host extensions (`AddIdentityCore<TUser>().AddEntityFrameworkStores().AddGoogleLogin()…`). Data-layer verdict: generic foundation (IKeyedEntity/IAuditable/ISoftDeletable/IHasTenant/IRepository/EF base) sufficient; identity needs its own 7 entities + EF schema + stores (no Data-abstraction changes). ~60% of slices reuse already-shipped packages (Argon2/OTP/OAuth/MFA/JWT-issuance/policies/cookies).

## Current state addendum — meta + email + jobs shipped (2026-06-10, same session)

- **`meta/` composition root**: `AddApiDefaults()` / `UseApiDefaults()` + `ApiDefaultsOptions` in ROOT namespace `WoW.Two.Sdk.Backend.Beta` (`src/meta/`). Wires the full P1 boot floor (serilog, TimeProvider, OTel tracing/metrics/OTLP, health, proxy hosting, OpenAPI, problemdetails + validation exception handler, rate limit, output cache, compression, optional CORS/validator-scan); every concern flag-off-able. Auth/mediator/data deliberately excluded (per-app decisions). Repo README quickstart now leads with it. Locked decision #1 ("one-import") realized.
- **`comms/email`**: `IEmailSender` + `EmailMessage`/`EmailSendResult` (result-typed) + `AddEmailDefaults` · providers: `AddMailKitEmailSender` (SMTP, default), `AddSendGridEmailSender` (v3 API), `AddSesEmailSender` (SES v2 simple send — attachments rejected with explicit reason, raw-MIME future). Pre-existing CPM pins reused (MailKit 4.9.0/MimeKit 4.9.0, SendGrid 9.29.3, AWSSDK.SimpleEmailV2 3.7.402 — v4 AWS bump REVERTED: conflicts with pinned v3 AWSSDK.S3/SQS from HealthChecks).
- **`jobs/hangfire` (+postgres)**: `AddHangfireJobs(storage, opts)` core + `AddInMemoryHangfireJobs` (dev) + `AddPostgresHangfireJobs(connStr)` + `UseHangfireJobsDashboard` (local-requests-only default). Pins: existing Hangfire 1.8.17 / PostgreSql 1.20.10 + new Hangfire.InMemory 1.0.0. **⚠️ Hangfire = LGPL-3.0 — sole exception to permissive-only (decision #16), blessed by targets.md §6 P4; revisit before non-beta distill.** Noted in csproj comment + registry + area README.
- **Collision fixes**: Hangfire.Core bundles a public `Cronos` namespace → `Foundation/Time/CronExpressionParser.cs` crefs now doc-id form (`T:Cronos.…`) with file-level CA1200 pragma · SendGrid namespace vs `…Comms.Email.SendGrid` → `global::` qualify.
- Build: 0 errors; no warnings from new code (delta = transitive NU advisories from Hangfire/SendGrid).

## Previous state — P3 data shipped (2026-02-23)

19 data packages scaffolded + compile clean. Breadth-first; polish/specs/standards by layers next:

| Slot | Package | Status |
|---|---|---|
| 1 | `…Data.Abstractions` (IEntity, IAuditable, ISoftDeletable, IHasTenant, IConcurrencyTracked, IAggregateRoot, IDomainEvent, IHasDomainEvents) | scaffold |
| 2 | `…Data.EntityFrameworkCore` (AppDbContextBase + AddEntityFrameworkCore&lt;T&gt;) | scaffold |
| 3 | `…Data.EntityFrameworkCore.Audit` (interceptor + IAuditCurrentUserAccessor) | scaffold |
| 4 | `…Data.EntityFrameworkCore.SoftDelete` (interceptor + ApplySoftDeleteFilter) | scaffold |
| 5 | `…Data.EntityFrameworkCore.NamingConventions` (snake/lower/camel/upper) | scaffold |
| 6 | `…Data.EntityFrameworkCore.Json` (JsonValueConverter+Comparer+HasJsonConversion) | scaffold |
| 7–11 | `…EntityFrameworkCore.{Postgres,SqlServer,MySql,Sqlite,Cosmos}` providers | scaffold |
| 12 | `…Data.EntityFrameworkCore.Bulk` (BulkExtensions re-export) | scaffold |
| 13 | `…Data.EntityFrameworkCore.Triggered` (UseTriggers + AddTriggersFromAssemblies) | scaffold |
| 14 | `…Data.EntityFrameworkCore.Projectables` (UseProjectables) | scaffold |
| 15 | `…Data.Dapper` (AddDapperConventions + IDbConnectionFactory) | scaffold |
| 16 | `…Data.Specifications` (Ardalis generic repo) | scaffold |
| 17 | `…Data.Migrations.Ef` (hosted runner w/ retry) | scaffold |
| 18 | `…Data.Migrations.DbUp` (hosted runner — Postgres/SqlServer/MySql; Sqlite deferred) | scaffold |
| 19 | `…Data` meta (curated default set) | scaffold |

**Build fixes applied to Directory.Packages.props**:
- Bumped all `Microsoft.Extensions.*` + `Microsoft.EntityFrameworkCore.*` from 9.0.0 → 9.0.2 (EFCore.BulkExtensions transitive requirements)
- `Microsoft.Extensions.TimeProvider.Testing` → 9.1.0 (no 9.0.2 published)
- `Npgsql.EntityFrameworkCore.PostgreSQL` 9.0.1 → 9.0.3 (BulkExtensions transitive)
- DbUp pinned: core 6.1.1 / postgresql 6.0.3 / sqlserver 6.0.16 / mysql 6.0.4
- Wrong-name fix: `EFCore.Projectables` → `EntityFrameworkCore.Projectables` 6.0.5
- Added 5 dbup-* package versions

**Migration of Haven still deferred** — packages exist; Haven's `Haven.Common.Domain/Persistence` to migrate later.

**Enforcement layer not yet built** — Roslyn analyzer (`…Data.Analyzers`) + arch-tests companion (`…Testing.ArchTests`) still to do. Decision §9.14 still open — once resolved, that's the next slot.

## Previous pivot — Auth extraction first (2026-05-07)

Pivoted from "P3 next (data + caching + http)" to "extract Haven.Auth first" — see `auth-extraction-analysis.md` in this folder.

Rationale:
- Haven (venture) is now active source-of-extraction. Layering *cross-Haven extraction* alongside the original phase-order plan — picking from Haven's existing assets in priority order based on stability + dependency surface + slot fit, not strictly P3→P4→P5→P6.
- Auth fills clean SDK gaps (JWT issuance, OTP primitives, OTP delivery interface, role policy) — none overlap with shipped packages, none compete with locked patterns.
- 4 new packages proposed under `src/identity/`: `otp` + `otp.telegram` + `jwt.issuance` + `policies`. ~700 LOC total across 4 packages.
- Exposes the abstract/specific split cleanly via DI — good first dogfood for the "orthogonal building blocks" approach. **No `IAuthUser` entity abstraction in v1** — consumers own their user model.

The original P3 plan (data + caching + http) below remains valid as Batch B; auth is Batch A.

Future cross-Haven candidates (matrix in `auth-extraction-analysis.md`'s sibling cross-ref): data audit interceptor, Postgres + Dapper utilities, SignalR realtime/observer pattern. Hard SKIPs: ApplicationResult/ApiResponse (overlap with shipped foundation/results + web/problemdetails), MediatR wrapper (overlap with custom MIT mediator), CronHelper (overlap with foundation/time/Cronos), ConfigurationLoader (.NET 9 IOptions binding source-gen).

## Source-of-truth docs

- **`docs/analysis/philosophy/ideas.md`** — encyclopedic .NET ecosystem catalog (~3,500 lines, no verdicts). 5 appendices spliced from parallel research agents.
- **`docs/analysis/philosophy/targets.md`** — verdicts (DONE/NOW/NEXT/LATER/MAYBE/SKIP/LOCKED). Contains revised P0–P6 phase mapping in §6.
- **`docs/conventions/package-registry.md`** — every package + status (single source of truth for package list).
- **`docs/conventions/{naming, package-layout, documentation}.md`** — conventions.
- **`docs/templates/`** — copy-paste templates per new package.
- **Repo-level `CLAUDE.md`** — cold-start onboarding.

## Phase model

| Phase | What | Status |
|---|---|---|
| P0 | Testing scaffold (parallel track) | ✅ 12 pkgs |
| P1 — foundation | Time, Errors, Results, Validation, Serialization, Guards, ValueObjects | ✅ 7 pkgs |
| P1 — observability | Logging, Tracing, Metrics, HealthChecks, OTLP, Prometheus, AzureMonitor, Datadog | ✅ 8 pkgs |
| P1 — web | Hosting, OpenApi, ProblemDetails, RateLimit, OutputCache, SecureHeaders, Cors, Compression, Versioning | ✅ 9 pkgs |
| P2 — mediator | mediator core + 4 behaviors (validation, logging, authorization, idempotency) | ✅ 5 pkgs |
| P2 — identity | jwt, cookies, oidc, identity-api, oauth-{google,microsoft,github,apple}, mfa-{totp,webauthn}, password-hashing-argon2 | ✅ 11 pkgs |
| **P3** — persistence + outbound | EF Core providers + audit/soft-delete/bulk/naming-conventions/projectables/triggered/specifications + Dapper + migrations + HybridCache + Redis + FusionCache + Refit + resilience | 🚧 **NEXT** |
| P4 | Distributed (CAP outbox + Hangfire + comms abstractions + webhooks) | planned |
| P5 | SaaS-shaped (Finbuckle multi-tenancy + Microsoft.Extensions.AI + Semantic Kernel + vector stores + feature flags) | planned |
| P6 | Heavy domain extensions (SignalR, storage, search, workflow, Aspire integrations, OIDC server, GraphQL, OData, AOT, payments, geo, OCR, docs site) | planned |

## Naming convention (LOCKED 2026-05-04)

**No `WowTwo` prefix on method/class names.** Package id carries the brand; method names describe what they concretely do.

Mirror of older `Backbone.Language.Features.Serialization` package's `AddSystemTextJsonSerializer` style.

Examples:
- `AddTimeProviders`, `AddFluentValidatorsFromAssemblies`
- `UseSerilogConventional`, `AddOpenTelemetryTracing`, `AddOtlpExporters`
- `AddProxyAwareHosting`, `UseOwaspSecureHeaders`, `AddPerIpSlidingWindowRateLimit`, `AddDefaultCorsPolicy`, `AddBrotliGzipCompression`
- `AddMediator`, `AddMediatorValidationBehavior`, …
- `AddJwtBearerAuthentication`, `AddCookieAuthentication`, `AddGoogleAuthentication`, `AddFido2WebAuthn`, `UseArgon2PasswordHasher`

Class names also descriptive: `JsonOptionsPresets`, `DomainError`, `IdentifierGuardExtensions`, `WebApiTestHost<T>`, `WebApiTestBase<T>`, `VerifyDefaults`, `BogusFakerFactory`.

Stable identifiers neutral: cookie `.app.auth`, policy `"default"`. `ActivitySource`/`Meter` keep `WoW.Two.<Area>` (intentional brand for cross-service trace filtering).

Full convention: [`docs/conventions/naming.md`](../../../workbench/wow-two-sdk-beta/wow-two-sdk.backend.beta/docs/conventions/naming.md).

## Locked decisions (do not re-litigate)

| # | Decision |
|---|---|
| 1 | Single big meta + many subpath packages. Dependency bloat accepted; one-import is the win. |
| 2 | .NET 9 baseline, C# 13+ free, multi-target later if needed. |
| 3 | `Microsoft.Extensions.DependencyInjection` is THE container. No swap-out. |
| 4 | Source-gen preferred over reflection (Mapperly, Vogen, source-gen JSON, source-gen `[LoggerMessage]`, source-gen options validation). |
| 5 | AOT-compatible best-effort. |
| 6 | Modular Monolith first, microservices later. |
| 7 | Clean Arch × Vertical Slice hybrid. |
| 8 | Beta-forever: `0.x.y`, CI auto-bumps `y`, no CHANGELOG, no PR gates, no required tests, push to main, fix-forward. |
| 9 | Standard + spec before code (for non-trivial APIs). |
| 10 | Foundation cannot import domain packages. Domains can import any sibling domain. |
| 11 | Subpath exports per top-level src folder. |
| 12 | STJ default, Newtonsoft only transitively. |
| 13 | `ILogger<T>` is the only public log surface (Serilog under the hood). |
| 14 | `ActivitySource` / `Meter` are the public observability seams. |
| 15 | No commercial-license deps in core meta. SKIP'd: MediatR (commercial 12+), AutoMapper (commercial 14+), MassTransit (commercial v9+), Duende.IdentityServer, iText. |
| 16 | Permissive licenses only in core: MIT, Apache-2.0, BSD-3, BSD-2, MS-PL, Unlicense. |
| 17 | Three-layer doc strategy: spec.md/standard.md per wrapper · `apps/playground/` Aspire AppHost (planned) · lazy KB for underlying libs. Don't pre-document libs we wrap. |
| 18 | Per-package shape: `csproj + <Module>ServiceCollectionExtensions.cs + Options.cs + standard.md + spec.md + README.md + tests.cs` (standard/spec/tests optional for tiny adapter pkgs). |
| 19 | Method/class names descriptive (no `WowTwo` prefix). Package id carries brand. |

## Build commands

```bash
cd workbench/wow-two-sdk-beta/wow-two-sdk.backend.beta/src
ulimit -n 65535          # macOS — avoid EMFILE
export MSBUILDDISABLENODEREUSE=1
dotnet restore WoW.Two.Sdk.Backend.Beta.sln -m:1
dotnet build WoW.Two.Sdk.Backend.Beta.sln --no-restore -m:1
```

`-m:1` = single-threaded MSBuild — avoids `EMFILE` (too many open files) on macOS at this package count.

## Pipeline (strategic compass)

1. **Capture all possible .NET libs / patterns / runtime APIs** — done. `docs/analysis/philosophy/ideas.md` covers ~10K+ packages addressable via composition. Five parallel research agents fed appendices §A–§E.
2. **Verdict per item** — done. `docs/analysis/philosophy/targets.md` mirrors ideas structure, every vector tagged DONE/NOW/NEXT/LATER/MAYBE/SKIP/LOCKED.
3. **Build wrappers in phase order P0–P6** — *currently active*. P0 + P1 + P2 shipped (52 pkgs). P3 next.
4. **Standardize per-package** — currently inline (each shipped pkg has spec.md + standard.md when API has shape; tiny adapters skip these). May tighten in a later pass.
5. **`apps/playground/` Aspire AppHost** — planned end-to-end smoke. Not started.
6. **Consumer migration** — wow-two apps (haven first) adopt the SDK once enough phases land. Not started.

This chat = step 3 (phase batches). Next batch is **P3**.

## Auth extraction (Batch A, 2026-05-07 pivot) — ✅ SHIPPED 2026-06-10

> Shipped as specced (with the small deviations listed in Current state above). Kept for reference.

Four new SDK packages under `src/identity/`:

1. **`identity/policies`** — `IRolePolicy` + `DictionaryRolePolicy` default + `RolePolicyOptions`. Smallest; ship first to validate package shape + spec/standard tooling. ~50 LOC.
2. **`identity/jwt.issuance`** — `ITokenIssuer` + `JwtTokenIssuer` (HS256 default) + `JwtTokenIssuerOptions` + `TokenIssuanceContext`. Sibling sub-package to existing `identity/jwt` (validation only) — keeps validation focused, lets non-ASP.NET workers issue tokens without pulling JwtBearer middleware. ~150 LOC.
3. **`identity/otp`** — `IOtpService` + `IOtpStore` (with `MemoryOtpStore` default) + `IOtpCodeGenerator` (with `NumericOtpCodeGenerator` default) + `IOtpDeliveryHandler` interface + `OtpOptions` + `OtpCreationResult` / `OtpVerificationResult` / `OtpFailureReason` / `OtpRecord` / `OtpDeliveryEnvelope` / `OtpDeliveryResult`. ~400 LOC.
4. **`identity/otp.telegram`** — `TelegramOtpDeliveryHandler` companion impl + `TelegramOtpOptions` (message template + scope display names). Depends on `identity/otp` + `Telegram.Bot`. ~80 LOC.

**No `IAuthUser` / `IUserStore<TUser>` entity abstraction in v1.** Consumers own their user model; SDK works on string subjects + claims. See §4 of `auth-extraction-analysis.md` for rationale (the SDK's verbs don't actually need a User type).

**Ship order**: policies → jwt.issuance → otp → otp.telegram. ~700 LOC total across 4 packages, 2–3 batches of work.

**After this batch lands**: Haven.Auth migrates to consume the 4 new SDK packages (dogfood validation). Then Batch B (P3 data) per the original plan below.

**Open questions to resolve before drafting specs** (from `auth-extraction-analysis.md` §11):
- `Telegram.Bot` license confirmation (MIT?) for permissive-only core
- `IRolePolicy` returns bool vs `RolePolicyDecision { Allowed, Reason? }` (recommend bool for v1)
- `IOtpService.CreateAsync` returns code (caller delivers) vs invokes delivery itself (recommend caller-controlled)
- `MemoryOtpStore` lifetime — Singleton (must be, to persist across requests)

## Next session — start here

### Action 1: P3 batch — persistence + outbound (~18 packages)

Subpath: `src/data/`, `src/caching/`, `src/http/`.

**Data (16 pkgs)** — folders already pre-created under `src/data/`:
- `WoW.Two.Sdk.Backend.Beta.Data` (meta — wires baseline)
- `…Data.EntityFrameworkCore` (base setup)
- `…Data.EntityFrameworkCore.{SqlServer, Postgres, MySql, Sqlite, Cosmos}` (provider presets)
- `…Data.EntityFrameworkCore.Audit` (`SaveChangesInterceptor` for `CreatedAt/UpdatedAt/By`)
- `…Data.EntityFrameworkCore.SoftDelete` (query filter + restore op)
- `…Data.EntityFrameworkCore.NamingConventions` (snake_case for Postgres)
- `…Data.EntityFrameworkCore.Bulk` (EFCore.BulkExtensions wrapper)
- `…Data.EntityFrameworkCore.Triggered` (EntityFrameworkCore.Triggered preset)
- `…Data.EntityFrameworkCore.Projectables` (EFCore.Projectables wrapper)
- `…Data.Dapper` (Dapper conventions)
- `…Data.Migrations.Ef` (EF Migrations runner)
- `…Data.Migrations.DbUp` (DbUp script-runner)
- `…Data.Specifications` (Ardalis.Specification)

**Caching (5–7 pkgs)** — folders under `src/caching/`:
- `…Caching` (meta — HybridCache defaults)
- `…Caching.Hybrid` (Microsoft.Extensions.Caching.Hybrid wiring)
- `…Caching.Memory` (in-process)
- `…Caching.Redis` (StackExchange.Redis L2)
- `…Caching.SqlServer` / `…Caching.Cosmos` (alt L2)
- `…Caching.FusionCache` (alt — pair with `Backplane.StackExchangeRedis`)

**Http (5–7 pkgs)** — folders under `src/http/`:
- `…Http` (meta — Refit + resilience defaults)
- `…Http.Refit` (Refit registration)
- `…Http.Resilience` (`Microsoft.Extensions.Http.Resilience` standard handler)
- `…Http.Hedging` (Standard-Hedging handler preset)
- `…Http.HeaderPropagation`
- `…Http.Auth.OAuth2ClientCredentials`
- `…Http.Auth.Mtls`

### Naming reminder

**Method names descriptive, no `WowTwo` prefix.** Pattern examples:
- EF: `AddEntityFrameworkCore`, `AddNpgsqlEntityFrameworkCore`, `AddEfCoreAuditInterceptor`, `AddEfCoreSoftDeleteFilter`, `UseSnakeCaseNamingConvention`, `AddEfCoreBulkExtensions`
- Caching: `AddHybridCache`, `AddRedisDistributedCache`, `AddFusionCache`
- Http: `AddRefitClient<T>`, `AddStandardResilienceHandler`, `AddStandardHedgingHandler`, `AddOAuth2ClientCredentialsHandler`, `AddMutualTlsHandler`

Verify the pattern table in `docs/conventions/naming.md` before naming new ones.

### Action 2 (parallel, smaller): P0 expansions

Add Testcontainers fixtures still **planned** in registry:
- `…Testing.Containers.Elasticsearch`
- `…Testing.Containers.Localstack`

Both follow the `ContainerFixtureBase<TContainer>` pattern (see `…Testing.Containers.Postgres` as template).

### Action 3 (after P3): P4 — distributed essentials

~30 pkgs (messaging meta + CAP + transports + raw broker clients + jobs + comms).

### Step-by-step batch protocol

For each new pkg in a batch:
1. csproj inside `src/<area>/<package>/` with appropriate FrameworkReference + PackageReferences.
2. `<Module>ServiceCollectionExtensions.cs` with descriptive `Add<Concrete>` methods (no `WowTwo` prefix).
3. README.md (1-screen quickstart).
4. For pkgs with non-trivial API: `<Module>.standard.md` (RFC 2119) + `<Module>.spec.md` (concrete API + usage).
5. Add to `docs/conventions/package-registry.md` with **shipped** status + concrete description.

After the batch:
1. `dotnet sln src/WoW.Two.Sdk.Backend.Beta.sln add <new csprojs>`
2. `dotnet sln src/WoW.Two.Sdk.Backend.Beta.slnx add <new csprojs>`
3. Add any new package versions to `src/Directory.Packages.props`.
4. `dotnet restore` + `dotnet build` (with `ulimit -n 65535` and `MSBUILDDISABLENODEREUSE=1`).
5. Update root `README.md` + `CLAUDE.md` phase status table.
6. Bump cumulative count in this `context.md`.

## Deep analysis files (in this session folder)

- `auth-extraction-analysis.md` (2026-05-07) — Haven.Auth deep map + abstract/specific split + 4-package SDK proposal + DI wiring (current focus, Batch A)
- *(future)* `data-extraction-analysis.md` — when Batch B starts (P3 data: audit + naming + postgres + dapper)
- *(future)* `signalr-extraction-analysis.md` — when realtime extraction starts (P6: SignalR + observer pattern + Redis backplane)

Sister: `wow-two-ws/system/sessions/ui-beta-build/` (frontend lib, parallel track).

## Parked (cleanup later)

- **Full rename to new convention** (status-before-function). Defer until a single dedicated pass — much cheaper all-at-once than piecewise. All four touchpoints in one go:
  1. **GitHub repo**: `wow-two-sdk.backend.beta` → `wow-two-sdk-beta.backend`
  2. **Local folder**: `workbench/wow-two-sdk-beta/wow-two-sdk.backend.beta/` → `workbench/wow-two-sdk-beta/wow-two-sdk-beta.backend/`
  3. **.NET project IDs** (csproj filenames + NuGet IDs): `WoW.Two.Sdk.Backend.Beta.*` → `WoW.Two.Sdk.Beta.Backend.*`
  4. **Namespaces inside code**: same shape as project IDs
- Touches: 52+ csproj renames, every `namespace` declaration, sln + slnx references, `Directory.Packages.props`, cross-project `ProjectReference`s, README + CLAUDE.md mentions, this `context.md`.
- Order-of-ops for the cleanup chat: rename GitHub repo first → re-clone locally → bulk-sed namespaces + csproj names → fix sln/slnx → rebuild → republish (NuGet versions auto-bump under the new IDs; old IDs stay published as historical).

## Out of scope (deliberately deferred)

- Tests of the SDK itself (beta-forever rule).
- CHANGELOG (git log is the changelog).
- PR review (push to main).
- Graduation/distill to non-beta lib (deferred until platform layer matures).
- AOT certification per package (planned P6).
- DocFX site (planned P6).

## Key file references

- Repo: `workbench/wow-two-sdk-beta/wow-two-sdk.backend.beta/`
- Sln: `src/WoW.Two.Sdk.Backend.Beta.sln` (+ `.slnx`)
- Central pkg versions: `src/Directory.Packages.props`
- Shared MSBuild props: `src/Directory.Build.props`
- EditorConfig: `src/.editorconfig` (incl. CA suppressions for naming-convention false-positives)
- Repo `CLAUDE.md` — cold-start onboarding
- Convention docs: `docs/conventions/{naming, package-layout, documentation, package-registry}.md`
- Templates: `docs/templates/{Module.cs, Options.cs, standard.md, spec.md, Tests.cs, README.md, package.csproj}.template`
- Strategic plan: `docs/analysis/philosophy/{ideas, targets}.md`

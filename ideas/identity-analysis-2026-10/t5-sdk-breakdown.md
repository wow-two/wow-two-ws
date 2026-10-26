# T5 — Identity as the first per-domain SDK repo

*Last updated: 2026-10-25*

> Identity leaves the be sdk mono-lib without a cycle once the auth primitives stay in core: one repo
> `wow-two-sdk-beta.identity` ships 6 NuGets, 1 npm package and the service image, at the price of one hard cut
> and a second release hop for every core change Identity needs.

- Aliases `be`, `fe`, `oc` as in [T3](https://github.com/wow-two-sdk-beta/wow-two-sdk-beta.identity/blob/main/engineering/research/identity-analysis-2026-10/t3-code-and-consumers.md); modes `M0`–`M13` and package names from
  [T4](https://github.com/wow-two-sdk-beta/wow-two-sdk-beta.identity/blob/main/engineering/research/identity-analysis-2026-10/t4-integration-modes.md); OpenIddict and Fido2 facts from [T1](https://github.com/wow-two-sdk-beta/wow-two-sdk-beta.identity/blob/main/engineering/research/identity-analysis-2026-10/t1-integrations.md); `(U)` = unverified.
- Counts are from grep over `be` and the product trees on 2026-10-25; nothing was built or edited.

---

## Verdict

- **Go.** Core imports Identity in one place only, `ICurrentUserService`; keeping the auth primitives in core removes the cycle.
- Repo: `wow-two-sdk-beta.identity`, two code dirs: `identity.backend-services/` (packages + service + tests) and `identity.frontend-services/`.
- Package ids `WoW2.Sdk.Beta.Be.Identity.*` keep today's namespaces, so moved code needs 0 `using` edits in 74 product files.
- 6 NuGets, not T4's 8: Auth stays in core; Validation and Projection fold into Client.
- A Form 3 product takes Contracts + Client; a Form 1 product takes Contracts + Module (+ Providers).
- Cost: core `10.0.N` keeps Identity, `10.0.N+1` drops it; 14 consumer repos re-pin in one commit each.
- Ongoing cost: every core change Identity needs costs a second push and CI release (~10 min).
- No hard blocker. First do three seams: an error-text contribution point, dead-code deletion, and a package-publish workflow.

---

## 1 · Coupling audit

### Identity → core (outbound)

| Core namespace | `using` sites | Importing Identity folders |
|---|---|---|
| `Foundation.Options` | 20 | Core, Otp, Mfa, OAuth, Jwt, Authorization, Policies |
| `Data.Abstractions` (own package) | 11 | Core entities |
| `Foundation.Naming` | 4 | Core |
| `Web.ExceptionHandling.Factories` | 2 | ApiKeys, Core/Endpoints |
| `Foundation.Errors` | 2 | ApiKeys, Core/Endpoints |
| `Comms.Email` · `Comms.Sms` · `Comms.WhatsApp` | 2 · 1 · 1 | Core mail, Otp channels |
| `Web.Contracts` · `Foundation.Validation` · `Localization` | 1 each | Core/Endpoints, Core, Otp formatter |

- All one-way and all staying in core, so Identity can depend on core as a published package.
- Today Identity imports no Messaging, Caching, Http, EF helpers, `Foundation.Security` or `Foundation.Audit`.
- P1 adds core imports: the EF outbox for back-channel logout, the envelope cipher, HybridCache and webhooks. All exist and point one way.
- Identity uses 0 `internal` core types, and the tree has no `InternalsVisibleTo`.
- Every SDK extension method sits in an SDK namespace; no hidden `Microsoft.*`-namespace coupling.

### Core → Identity (inbound)

| From (outside `Identity/`) | Uses | Kind | Fix |
|---|---|---|---|
| `Data/EntityFrameworkCore/Audit/` (2 files), `SoftDelete/` (2), `Mediator/Idempotency/DeduplicatingInterceptor.cs` | `Identity.CurrentUser.ICurrentUserService` | type | CurrentUser stays in core |
| `Web/ErrorTranslation/FieldCodeMessageConstants.cs` | ru/uz texts keyed by identity error codes | strings | contribution seam; Module registers its texts |
| `Testing/Auth/TestClaimTypeConstants.cs` | mirrors `NormalizedClaimTypeConstants` | doc comment | none |
| `Foundation.Tests/Comms/SmsBrokerTests.cs` (2 tests), `Web.Tests/ErrorTranslation` (1 test) | `Identity.Otp`, `IdentityErrorCodeConstants` | tests | move with Otp and the texts |
| `Mediator.Tests/Behaviors/IdempotencyOwnershipTests.cs` | `ICurrentUserService` | test | stays |

- `CookieCurrentUserService` uses Guest's `internal` `GuestCookieSerializer`, the one internal type that crosses folders, so Guest stays with CurrentUser.
- None of the four `Testing*` projects references Identity, so all four stay unchanged.

### Inside Identity

- `Core` → `Jwt.Issuance` (account endpoints), `Mfa.Totp`, `Otp`, `PasswordHashing.Argon`.
- `ApiKeys` → `Authorization`; `CurrentUser` → `Guest`; every other folder stands alone.
- The moving set depends on the staying set only through `Jwt`, one way, so the cut has no cycle.

### Disposition

| Folder | Files · LOC | Goes to | Package |
|---|---|---|---|
| `Core/` | 140 · 6,940 | Identity repo | Module |
| `Otp/` | 40 · 1,319 | Identity repo | Module |
| `Mfa/` | 5 · 183 | Identity repo | Module |
| `PasswordHashing/` | 2 · 125 | Identity repo | Module |
| `OAuth/` | 23 · 748 | Identity repo | Providers |
| `Claims/` | 8 · 488 | Identity repo | Providers (its profiles mirror the 17 providers) |
| `Oidc/` | 2 · 71 | Identity repo | Client |
| `Cookies/` | 3 · 92 | core | — |
| `ApiKeys/` | 15 · 577 | core | — |
| `Authorization/` | 5 · 134 | core | — |
| `CurrentUser/` | 5 · 125 | core | — |
| `Guest/` | 6 · 183 | core | — |
| `Jwt/` | 7 · 303 | core | — |
| `IdentityApi/` | 1 · 42 | deleted | 0 consumers, 0 tests (T3) |
| `Policies/` | 4 · 70 | deleted | 0 consumers, 0 tests (T3) |

- Totals: 220 files and 9,874 LOC move; 41 files and 1,414 LOC stay; 5 files are deleted.
- 38 lead, spec and standard docs move with the code, plus `be` `engineering/research/identity/` (3 files).
- Core's csproj loses 24 of 144 `PackageReference`s, plus the 2 OpenIddict pins in its props file.
- The 24: Facebook, Google, MicrosoftAccount and OpenIdConnect handlers; 14 `AspNet.Security.OAuth.*`; `Telegram.Bot`; `Fido2.AspNet`; Argon2; `Otp.NET`; `Google.Apis.Auth`; `Microsoft.AspNetCore.Identity.EntityFrameworkCore`.
- `JwtBearer` and the two `Microsoft.IdentityModel.*` packages stay with `Jwt/`; grep finds them used only there.
- Tests: `Identity.Tests` 95 methods → 62 move (Accounts 51, Otp 7, `UserAccountService` 3, Google 1).
- 33 stay in core: ApiKeys 17, Jwt 8, Guest 4, `ConfiguredRegistrationTests` 4 (that file splits).
- fe side: nothing moves. `fe/auth/` imports only `foundation/results`, `foundation/http` and `vue`.
- No other fe module imports `fe/auth/`; the session core, Google button, inputs and account menu stay generic.

---

## 2 · Repo design

### Name and org

| Option | For | Against |
|---|---|---|
| `wow-two-sdk-beta.identity` | packages are the main artifact; the direction makes domain repos SDK repos; ids fit `WoW2.Sdk.Beta.Be.{Module}` | catalog, platform-apps and spec say `wow-two-platform.identity`; the org is public |
| `wow-two-platform.identity` | already named; Wheelhouse knows the org | publishes the SDK's domain packages from the internal-infra org; two homes per domain later |

- Pick `wow-two-sdk-beta.identity`.
- Public is fine: the deploy descriptor holds no hosts or secrets (descriptor § Rules).
- Slug `identity` → code dirs `identity.backend-services/` and `identity.frontend-services/`.
- Catalog: the existing Identity entry keeps `kind: platform` and `deploy: wheelhouse` and points at the new repository.

### Layout

```
wow-two-sdk-beta.identity/
├── README.md · CLAUDE.md · .claude/ · .gitignore
├── .github/
│   ├── renovate.json
│   └── workflows/
│       ├── publish-packages.yml          NuGet + npm, tag-derived (be-v* · fe-v*)
│       ├── publish-docker-image.yml      pipelines delivery.yml → image vX.Y.Z (exact path: Wheelhouse detects it)
│       └── codeql.yml                    public repo
├── product/                              the service: product.md · product.json · brand/icons
└── engineering/
    ├── engineering.md
    ├── planning/                         backlog.md · version-track/v0.1/ (drives the image X.Y)
    ├── architecture/                     contract.md · package-registry.md · decisions/ · flows/
    ├── research/                         identity-slices.md, identity-architecture.md, two-factor-methods.md (from be)
    ├── deployment/                       deploy.yml · Dockerfile · docker-compose.yml (context engineering/codebase/)
    └── codebase/
        ├── codebase.md
        ├── identity.backend-services/
        │   ├── Identity.BackendServices.slnx
        │   ├── Directory.Build.props · Directory.Packages.props    BackendSdkVersion pin of core
        │   ├── packages/                 the NuGet family, namespace root WoW.Two.Sdk.Beta.Be.Identity
        │   │   ├── Contracts/ · Client/ · Module/ · Providers/ · Server/ · Testing/
        │   ├── service/                  Identity.Api · Identity.Application · Identity.Infrastructure
        │   └── tests/                    Identity.Packages.Tests · Identity.Tests.{Integration,E2E} · Identity.Tests.Conformance
        └── identity.frontend-services/
            ├── package.json · pnpm-workspace.yaml · pnpm-lock.yaml
            ├── packages/fe-identity/     @wow-two-beta/fe-identity → ./kit · ./admin · ./telegram · ./native
            └── apps/web/                 hosted pages + console, served single-host by Identity.Api
```

- Two code dirs, not four: one `.slnx` and one pnpm lockfile, and the Dockerfile copies both `{slug}.` dirs as today.
- The service references packages by `ProjectReference` and `workspace:*`; one commit ships library and service together.
- Service projects host the module and add only hosting, admin and app routing (capability forms § Layout).
- Domain and Persistence live in Module and Server; there is no service-side Domain project.
- One deployable `identity`; per-owner instances of one image are T6's open Q5.

### Ids and namespaces

| Artifact | Id | Namespace / subpaths |
|---|---|---|
| contract | `WoW2.Sdk.Beta.Be.Identity.Contracts` | `WoW.Two.Sdk.Beta.Be.Identity.Contracts` (new) |
| OIDC client | `WoW2.Sdk.Beta.Be.Identity.Client` | `…Identity.Client` (new) + `…Identity.Oidc` (kept) |
| in-process module | `WoW2.Sdk.Beta.Be.Identity.Module` | `…Identity.Core.*`, `…Identity.Otp.*`, `…Identity.Mfa.*`, `…Identity.PasswordHashing.*` (kept) |
| upstream providers | `WoW2.Sdk.Beta.Be.Identity.Providers` | `…Identity.OAuth.*`, `…Identity.Claims` (kept) |
| OIDC server | `WoW2.Sdk.Beta.Be.Identity.Server` | `…Identity.Server` (new) |
| test kit | `WoW2.Sdk.Beta.Be.Identity.Testing` | `…Identity.Testing` (new) |
| fe library | `@wow-two-beta/fe-identity` | `./kit`, `./admin`, `./telegram`, `./native` |
| image | `identity` (GHCR) | — |

- Ids follow the be sdk grammar: root + `.{Module}` (sdk-structure § Naming); all are free on nuget.org (404 on 2026-10-25).
- The `WoW2.*` prefix is reserved to our account, so only our workflow can push them.
- Package id ≠ namespace is allowed (SDK architecture § Packages); Module sets `RootNamespace` `WoW.Two.Sdk.Beta.Be.Identity`.
- Kept namespaces keep EF model snapshots stable: pilots' snapshots name `WoW.Two.Sdk.Beta.Be.Identity.Core.IdentityUser`.
- npm name `@wow-two-beta/fe-{domain}` marks the package as the fe sdk's domain companion; its peer range is in §4.

---

## 3 · Package split

### T4's cut against the audit

| T4 package | T5 | Reason from the audit |
|---|---|---|
| `Identity.Contracts` | keep | shared by Client and Module; needs `Result`, `AppError`, `IEvent` from core, which every product already references |
| `Auth` primitives | stay in core | `ICurrentUserService` is imported by core Data and Mediator; M0 products need them with no Identity; 0 third-party deps |
| `Identity.Validation` | fold into Client | its deps (JwtBearer, IdentityModel) stay in core with `Jwt/`; a package of its own removes nothing |
| `Identity.Client` | keep | OIDC client, session routes, brokers, receivers |
| `Identity.Client.Projection` | fold into Client, opt-in registration | EF Core already comes with core |
| `Identity.Module` | keep | owns Fido2, Otp.NET, Argon2, Telegram.Bot |
| `Identity.Providers` | keep | widest fan-out: 18 packages |
| `Identity.Server` | keep | the only OpenIddict consumer |
| `Identity.Testing` | keep | fakes stay out of runtime references |

- A package boundary pays only where it removes third-party deps; while core is a mono-lib, Validation and Projection remove none.
- T4's "dependency-free Contracts" needs a core abstractions package; nothing needs it yet.
- `Data.Abstractions` is the precedent for such a package when one does.

### Packages and heavy deps

| Package | Holds | Heavy third-party deps | References |
|---|---|---|---|
| Contracts | 6 brokers, models, `IEvent` records, claim constants, error catalogue (T4 § Contract) | none | core |
| Client | `Oidc/`, `/api/identity/*` session routes, `IIdentityManagementApi` + `IdentityApi*Broker`, `AddIdentityTokenValidation` (authority, audience, org policies), logout and webhook receivers, opt-in projection | `Microsoft.AspNetCore.Authentication.OpenIdConnect`; Refit, Resilience, HybridCache and JwtBearer arrive with core | Contracts |
| Module | `Core/`, `Otp/`, `Mfa/`, `PasswordHashing/`; I14–I16, I20–I22; `IdentityCore*Broker` | `Fido2.AspNet` (3.0.1 → 4.3.1, T1), `Otp.NET`, `Konscious.Security.Cryptography.Argon2`, `Telegram.Bot` | Contracts |
| Providers | `OAuth/` (17), Google ID-token authenticator, `Claims/` normalizer | 14 `AspNet.Security.OAuth.*`, Microsoft Google/Facebook/MicrosoftAccount, `Google.Apis.Auth` | core |
| Server | OpenIddict server, keys + JWKS (I17), client registry, back-channel sender, exchange grants | `OpenIddict.AspNetCore` + `OpenIddict.EntityFrameworkCore` 7.7.2 (EF Relational ≥ 10.0.11) | Module |
| Testing | fake brokers, personas, OTP code sink, fake instance | `WoW2.Sdk.Beta.Be.Testing` | Contracts |

- Every package adds `<FrameworkReference Include="Microsoft.AspNetCore.App" />`; without it restore hits NU1109 (be sdk companion lesson).
- Module needs no Providers: `UserLoginService` stores a provider name, not a handler type.

### Who references what

| Consumer | be packages (plus core) | fe |
|---|---|---|
| Form 3 product (M2 BFF) | Contracts + Client | fe sdk `auth`; `fe-identity/admin` for member admin (P2) |
| Form 1 product (M1) | Contracts + Module (+ Providers for social sign-in; + Server only under T4 option A) | `fe-identity/kit` |
| API resource (M8; M10 callee) | Client, registering token validation only | — |
| M0 product (no store) | core only; + Providers for upstream OAuth | fe sdk `auth` |
| Identity service | Contracts + Module + Server + Providers + Client (its console signs in through its own instance, T4) | `fe-identity` via `workspace:*` |
| test projects | + Testing | — |

- A Form 3 product pulls none of OpenIddict, Fido2, Otp.NET, Argon2, Telegram.Bot, the 17 providers or `Google.Apis.Auth`.
- Products that use no identity, such as Sift, drop all 24 packages from their restore graph, which closes be backlog line 194.

---

## 4 · Dependency on core

- `identity.backend-services/Directory.Packages.props` pins `WoW2.Sdk.Beta.Be` (+ `.Testing`, `.Testing.Data`) through `<BackendSdkVersion>`.
- That is the products' pattern (retainer-balance, Wheelhouse, product template).
- `identity.frontend-services` pins `@wow-two-beta/fe` to an exact version, as every product does.
- Each package's nuspec declares `WoW2.Sdk.Beta.Be >= {pinned}`.
- A product on an older core fails restore with NU1605, an error by default, so the floor is enforced.
- The ceiling is not enforced: a product on a newer core runs Identity built against the older one.
- A core break shipped in a `z` release surfaces at run time as `MissingMethodException`, not at build.
- The beta line is still `10.0.z` after 76 releases, so `y` does not mark breaks today.
- `@wow-two-beta/fe-identity` peers `@wow-two-beta/fe` at `>=0.0.n <0.1.0`; `^0.0.n` would admit one version only.
- The EF floor moves out of core: OpenIddict's EF ≥ 10.0.11 becomes an Identity pin (T1).
- Products already pin EF Core 10.0.12 (ForeverPin, Wheelhouse, retainer-balance).

### Release loop when Identity needs a core change

1. Change core, push; main CI releases `10.0.N-beta` in about 10 min (dev-cycle § SDK release sync).
2. Wait for the release commit, `git pull --ff-only` in core.
3. In Identity: bump `BackendSdkVersion`, make the change, push; Identity CI publishes packages and the image.
4. Each product bumps `BackendSdkVersion` and `IdentitySdkVersion` in one commit.

- Today the same change is one push; the split adds a push, a CI run and a pin bump.
- Expected P1 core touches: the error-text seam, the PostgreSQL Data Protection ring (T6 Q26) and outbox or webhook tweaks.
- OpenIddict, Fido2 and the EF floor no longer need a core release.

### Skew guard

- Products keep two properties side by side, `BackendSdkVersion` and `IdentitySdkVersion`, and bump them together.
- Identity release notes name the core version each release was built against.
- A `core-latest` compat job in Identity CI runs on every core release (`repository_dispatch` from core's publish) and nightly.
- The compat job builds and tests Identity against the newest core and fails before a product meets the break.

---

## 5 · Versioning and CI

| Artifact | Registry | Version line | Derived from | Tag | Workflow |
|---|---|---|---|---|---|
| 6 NuGets | nuget.org | `10.y.z-beta`, own line from `10.0.0-beta` | latest `be-v*` tag + 1 | `be-v10.0.z-beta` | `publish-packages.yml`, job `be` |
| `@wow-two-beta/fe-identity` | npm | `0.0.z` | latest `fe-v*` tag + 1 | `fe-v0.0.z` | `publish-packages.yml`, job `fe` |
| `identity` image | GHCR | `X.Y.Z` (version track) | pipelines `generator/release.py` | `vX.Y.Z` | `publish-docker-image.yml` → pipelines `delivery.yml` |

- Use an independent line, not lockstep: lockstep would republish unchanged Identity packages on every core push.
- `x = 10` keeps the .NET-major rule ([versioning strategy](../../docs/versioning-strategy.md)).
- Versions come from tags with no commit-back: CI passes `-p:Version` and sets the npm version in the checkout only.
- No `chore: release` commit means no release-sync wait in this repo, and the two package jobs never race on `main`.
- Prefixed tags have precedent: the fe sdk already tags `fe-v*`.
- `release.py` counts only `vX.Y.Z` tags without a pre-release on the active line, so `be-v`/`fe-v` tags never move the image patch.
- The package jobs run on changes under either `packages/` dir; delivery's plan decides the image build.
- A library change releases packages and the image together, because the service builds from the same commit.
- Gates: packages publish after package tests and the in-process broker conformance run.
- The image publishes after ci plus broker conformance against the built image; OIDF conformance runs nightly and on tags (T6).
- Shared pipelines cover images only (`ci.yml`, `delivery.yml`, `publish.yml`); be and fe sdks each keep their own publish workflow.
- Add a reusable `packages.yml` to `wow-two-platform.pipelines` before the second domain repo; until then it stays repo-local.
- Developer, one-time: a NuGet trusted-publishing policy for the new repo and workflow.
- The first npm publish of `fe-identity` is manual; the trusted publisher can be set only after it.
- Wheelhouse's access to GHCR images under the `wow-two-sdk-beta` org is untested (U).

---

## 6 · Migration

### Steps

1. Core `10.0.N`, non-breaking prep: an error-text contribution seam in `Web/ErrorTranslation`; delete `IdentityApi/` and `Policies/`.
2. N is the last mono-lib release that holds Identity.
3. Developer: create the GitHub repo, the NuGet trusted-publishing policy and the git flags.
4. Scaffold the repo (§2): copy the 7 folders, 62 tests, 38 docs and `research/identity/`; add csprojs and both workflows.
5. Core `10.0.N+1`: remove the moved folders, the 24 references and the 3 moved tests (+ the `Auth/` rename, Open 2).
6. N+1 is the one breaking release.
7. Identity `10.0.0-beta`, built against core N+1, which is also its floor.
8. The fe package waits for its first screens; nothing moves on the fe side.
9. Consumer sweep: each repo bumps core to N+1 and adds `IdentitySdkVersion` plus its package refs in one commit.
10. Docs and conventions (§9).

- Make it a hard cut: core cannot type-forward to Identity, because Identity depends on core.
- Core ≤ N and Identity packages together would define the same types twice (CS0433); the N+1 floor makes that unrestorable.
- A product that has not migrated stays on core ≤ N; migrating means changing two pins and the package refs.
- History: copy the files and cite the core commit in the first commit.
- A `git filter-repo` import is object surgery, which only the developer runs.

### Breaking changes for consumers

- Package refs: Module or Providers types now ship in new packages, so consumers add 1–2 `PackageReference` lines.
- Namespaces of moved code: none.
- Namespaces of the staying primitives: none, or 39 files if they become `Auth` (Open 2).
- Assembly: `WoW.Two.Sdk.Beta.Be.dll` no longer holds Identity types; the pilots wire EF by `ApplyIdentitySchema`, not assembly scans.

### Re-pins (pins from T3)

| Consumer | Core pin today | Adds | `using` edits: kept ns / `Auth` rename |
|---|---|---|---|
| pilots ×10 | `10.0.74` | Module | 0 / `Cookies`, `Authorization` in host config |
| Haven | `10.0.74` | Module (OTP) | 0 / `Jwt` files |
| Ocharo Desk | `10.0.71` | Module (OTP, Telegram channel) | 0 / `Jwt.Issuance` (`IntegrationTickets.cs`) |
| ForeverPin | `10.0.72` | Providers (Google ID token) | 0 / `Cookies`, `CurrentUser` |
| Wheelhouse | `10.0.71` | Providers (GitHub, claim normalizer) | 0 / `ApiKeys`, `Authorization`, `Cookies` |
| TranscriptForge | `10.0.74` | none | 0 / `ApiKeys` |
| Sift, Hijinx, Arcade, other core-only repos | various | none | none |
| Secrets Vault | `10.0.56`, old id | none | retiring |

### Cost

| Item | Kind | Size |
|---|---|---|
| core prep `10.0.N` | one-time | 1 chat |
| repo, NuGet policy, git flags; first npm publish later | one-time | developer, ~30 min (U) |
| scaffold, move 220 files and 62 tests, CI | one-time | 1–2 chats |
| core `10.0.N+1` removal | one-time | same chain |
| consumer sweep, 14 repos | one-time | 1 sweep chat, S each |
| conventions and docs | one-time | 1 chat |
| cross-repo change | ongoing | +1 push, +1 CI (~10 min), +1 pin |
| second pin in every consumer | ongoing | 1 line per bump |
| compat job and the repo-local package workflow | ongoing | 2 workflows |

- Gain: core sheds 24 references and 9.9k LOC.
- Gain: OpenIddict, EF and Fido2 bumps no longer wait for a core release.
- Gain: library and service land in one commit, with no publish wait between them.

---

## 7 · General rule

A domain earns its own repo when:

- it owns state or a hosted surface served in capability forms 2/3, so the repo holds ≥ 2 of be library, fe library and image.
- it leaves core without a cycle: no core area imports it, or the imported seam stays in core.
- it brings third-party deps nothing else in core uses (Identity: 24), or a release cadence of its own.
- it has a broker contract to version against.

Core keeps:

- anything another area imports: Foundation, Web, Data (+ Abstractions), Mediator, Http, Caching, Localization, Observability.
- Messaging abstractions (`IEvent`), Comms channels, the `Storage/` blob seam, the auth primitives and the Testing base.

Flag:

- Pure-library areas with heavy deps but no state or service have no fe or service half to unite.
- Examples: Messaging adapters, Media, Codes, Ai providers.
- For them, a companion package in the be sdk repo removes the deps without a second release loop.

| Candidate | Verdict | Evidence |
|---|---|---|
| File Storage | next domain repo | capability #3, three forms; core keeps `Storage/` because Messaging `Transport` imports it in 9 files |
| Events | born as a domain repo | Form 1 module chosen 2026-10-24 and not yet in core, so no move cost; needs Identity Contracts |
| Harvest | domain repo when built | service-first, grown from ListingShelf; library = client + pipeline contracts |
| Messaging | stays in core | 285 files; Identity Contracts and the outbox need it; no service form; adapters → companion packages |

---

## 8 · Agentic workflow

- An Identity chat gets its own working tree and index, so it never stages beside a core lane.
- Release windows split: an Identity push never blocks a core commit.
- With tag-derived versions, Identity has no release-sync wait of its own.
- A cross-repo change runs as two lanes in sequence, core first; no chat changes both atomically.
- P1 lanes split by folder inside one repo: Server, Client, Module slices, `fe-identity`, `apps/web`.
- The rule of 2–3 repos per session holds: Identity, sometimes core, and one consumer.
- A domain chat loads one repo's `CLAUDE.md` and backlog, not the mono-lib's whole surface.
- The Identity solution compiles ~230 files instead of the mono-lib, probably a faster test loop (U, not timed).
- Setup: git flags (`~git_on commit,push wow-two-sdk-beta.identity`, or the `*` default), an `active.sh` entry, and ports in the ledger.
- The SDK doctrine in `W/CLAUDE.md` gains a hop: a product chat fixes the domain repo, which fixes core when needed.

---

## 9 · Convention changes

| Doc | Gist of the change |
|---|---|
| `conventions/development/capability-forms.md` § Layout | library and service live in one domain repo `wow-two-sdk-beta.{capability}`; core be/fe sdk keep only shared seams; the service consumes in-repo packages |
| `conventions/development/repo/structure/sdk-structure.md` | new domain-repo archetype: SDK shell + `product/` + `engineering/deployment/` |
| — same doc | code dirs `{slug}.backend-services/` (`packages/` · `service/` · `tests/`) and `{slug}.frontend-services/` (`packages/` · `apps/`) |
| — same doc | naming: `WoW2.Sdk.Beta.Be.{Domain}.{Part}`, namespace root `WoW.Two.Sdk.Beta.Be.{Domain}`, `@wow-two-beta/fe-{domain}` |
| `conventions/development/repo/structure/repo-structure.md` § Archetypes | third row, domain repo, pointing at sdk-structure |
| `conventions/development/repo/structure/product-conformance.md` | domain rows: own packages by ProjectReference (exception to "SDK pins a published version"); no service Domain/Persistence project |
| `conventions/development/dev-cycle.md` § SDK change loop, § SDK release sync | the domain hop (core → domain → product); tag-derived domain repos have no release commit |
| `docs/versioning-strategy.md` | domain repos: three artifacts, three tags (`be-v`, `fe-v`, `v`) |
| be `package-registry.md`, `package-layout.md`, `CLAUDE.md` | Identity rows point to the domain repo from `10.0.N+1`; the tree drops `Identity/` (gains `Auth/` under Open 2) |
| `catalog.yml` | Identity entry → `repositories: [wow-two-sdk-beta/wow-two-sdk-beta.identity]`; be sdk purpose drops "identity" |
| `.claude/repo-registry.md` | regenerate with `scripts/gen-repo-registry.py`; the sdk-beta org gains the row |
| `docs/platform-apps.md`, `ideas/identity-service-spec.md` | repo name; Sequencing gains step 0, the split |
| `W/CLAUDE.md` § SDK doctrine | names domain repos and the extra hop |
| `wow-two-platform.pipelines` | reusable `packages.yml`: NuGet + npm, tag-derived |

---

## Open

1. Org and name: `wow-two-sdk-beta.identity` or the already-named `wow-two-platform.identity`?
   - Pick `wow-two-sdk-beta.identity`: every domain gets one home, beside the other SDK packages.
2. Staying primitives (`Cookies`, `ApiKeys`, `Authorization`, `CurrentUser`, `Guest`, `Jwt`): keep `…Be.Identity.*` (0 edits), or move to `…Be.Auth.*` in N+1 (39 product files)?
   - Pick the rename, in the same release: products are touched then anyway, and "Identity" then means only the domain repo.
3. Timing: split as P1 step 0, before I17/I18 code lands, or after Ocharo's P1 ships?
   - Pick step 0: Server, Client and Contracts are born in the repo, and only today's 220 files move.
4. Package release mechanics: tag-derived versions with no release commit, or copy the be sdk's bump-commit flow?
   - Pick tag-derived: no release-sync wait, and no race between the be and fe jobs.
5. Skew guard: a `core-latest` compat job in Identity, or ApiCompat in core forcing a `y` bump on breaks?
   - Pick the compat job now; add ApiCompat when the second domain repo depends on core.

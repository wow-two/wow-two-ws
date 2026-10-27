# B1 — proxy trust check (`X-Forwarded-For` → local access)

*Checked 2026-10-27 · read-only · be sdk HEAD `860bca19c7e992b2b65377612f86c57e27ac87fe` (2026-10-27 09:05 UTC), `git describe` = `v10.0.87-beta`*

Shorthands: `{sdk}` = `workbench/wow-two-sdk-beta/wow-two-sdk-beta.be/engineering/codebase/wow-two-sdk-beta-be/src` · `{be}` = `workbench/wow-two-sdk-beta/wow-two-sdk-beta.be` · `{id}` = `workbench/wow-two-sdk-beta/wow-two-sdk-beta.identity/engineering/codebase/identity.backend-services` · `{tf}` = `workbench/maxs-projects/ventures/saas/10x-ventures-transcript-forge/engineering/codebase/transcript-forge.backend-services` · `{sv}` = `workbench/wow-two-platform/wow-two-platform.secrets-vault/engineering/codebase/secrets-vault.backend-services`

## Verdict

**Not exploitable today.** A remote client cannot spoof `X-Forwarded-For: 127.0.0.1` into local access on any SDK version a product pins at or after `10.0.60-beta`.

- The claim describes an old hazard that was real until `10.0.59-beta`:
  - every SDK version through `10.0.59-beta` cleared `KnownProxies` and `KnownIPNetworks` and added nothing back
  - ASP.NET Core reads two empty lists as "trust every sender", so any client could set its own address, scheme and host
- `fca19ea` (2026-09-27, ForeverPin E4 "hardened proxy trust") fixed it, shipped in `v10.0.60-beta`:
  - the fix trusts loopback plus explicitly configured proxies and networks, and keeps `ForwardLimit = 1`
- `TrustProxiesFrom` (`60bba7b`, ForeverPin E11) is not the fix:
  - it only binds `Deployment:TrustedProxies` / `TrustedNetworks` from configuration into the hardened options
  - it shipped in the same `v10.0.60-beta`
- The SDK's keyless loopback pass (`ApiKeyAccessGate`, `AllowLocalWithoutKey`) also first shipped in `v10.0.60-beta` (`15747d0`):
  - no published SDK version combined the trust-all default with that loopback pass
- TranscriptForge (`10.0.74-beta`): its `ForwardedHeaders.None` post-configure guards against a default its pin no longer has, so it is redundant against header spoofing
- Secrets Vault (`10.0.56-beta`) does sit on the trust-all default, and its post-configure is a real fix:
  - its remote address feeds only audit records and the login rate-limit partition, not an access decision
- Only one live product sits on the trust-all default without its own fix: TransportBrain (`10.0.45-beta`):
  - it has no loopback-based access path and has rate limiting off, so spoofing gives no local access
  - it can still forge its logged IP, `X-Forwarded-Proto` and `X-Forwarded-Host`
- Residual risk is about topology, not header spoofing (see "Residual risk")

## 1. What the SDK configures at HEAD

`AddApiDefaults` → `AddProxyAwareHosting` → `Configure<ForwardedHeadersOptions>`:

| Setting | Value at HEAD | Where |
|---|---|---|
| Headers | `XForwardedFor \| XForwardedProto \| XForwardedHost` | `{sdk}/Web/Hosting/HostingServiceCollectionExtensions.cs:38` |
| `ForwardLimit` | `ProxyAwareHostingOptions.ForwardLimit`, default `1`, must be ≥ 1 | `HostingServiceCollectionExtensions.cs:31,39` · `ProxyAwareHostingOptions.cs:17` |
| `KnownProxies` | cleared, then `IPAddress.Loopback` + `IPv6Loopback` + each configured `TrustedProxies` entry | `HostingServiceCollectionExtensions.cs:41-45` |
| `KnownIPNetworks` | cleared, then each configured `TrustedNetworks` CIDR (none by default) | `HostingServiceCollectionExtensions.cs:40,46-47` |
| Parsing | a malformed proxy or CIDR throws at startup | `HostingServiceCollectionExtensions.cs:32-33,93-101` |
| Middleware | `UseForwardedHeaders()` inside `UseProxyAwareHosting` | `HostingServiceCollectionExtensions.cs:66-73` |
| Pipeline position | after `UseExceptionHandler`, before HTTPS redirection, routing and the identity callback | `{sdk}/Meta/ApiDefaultsExtensions.cs:122-124,158` |
| Pass-through | `ApiDefaultsOptions.TrustedProxies` / `TrustedNetworks` / `AllowedHosts` → hosting options | `ApiDefaultsExtensions.cs:67-76` · `ApiDefaultsOptions.cs:39,42` |

- `TrustProxiesFrom(section)` reads `TrustedProxies` and `TrustedNetworks` string arrays from the section:
  - it trims them and appends them to `ApiDefaultsOptions`; a missing section adds nothing — `{sdk}/Meta/ApiDefaultsOptionsExtensions.cs:16-32`
  - it changes which non-loopback senders are trusted; it leaves headers, limit and loopback trust unchanged
- SDK test pins the default:
  - a non-loopback socket keeps its own address
  - a loopback socket takes the forwarded one — `{sdk}/Web.Tests/Hosting/ProxyAwareHostingTests.cs:18-26`
- Documented contract: `{sdk}/Web/Hosting/hosting.md` § Proxy trust ("apply only from loopback, `TrustedProxies` and `TrustedNetworks`")

### History (why the products' comments exist)

| SDK state | Forwarded-headers trust | Evidence |
|---|---|---|
| ≤ `10.0.59-beta` (incl. `10.0.21`, `10.0.45`, `10.0.56`) | `KnownProxies.Clear()` + `KnownIPNetworks.Clear()`, nothing added → every sender trusted | `git show v10.0.56-beta:…/HostingServiceCollectionExtensions.cs` lines 28-30; same shape at release commits `35d1a84` (10.0.21) and `eef9c7c` (10.0.45) |
| `fca19ea` 2026-09-27 → first tag `v10.0.60-beta` | loopback + configured only | `git tag --contains fca19ea` |
| `60bba7b` 2026-09-28 → `v10.0.60-beta` | adds `TrustProxiesFrom` binding | `git tag --contains 60bba7b` |
| `15747d0` 2026-09-28 → `v10.0.60-beta` | adds the API key gate with the loopback pass | `git tag --contains 15747d0` |
| `0d4ab51` → `v10.0.82-beta` | Identity (incl. the gate) leaves core for `wow-two-sdk-beta.identity` | `git tag --contains 0d4ab51` |

- The ForeverPin extraction record states the old default outright: "the SDK default trusted every sender" — `{be}/engineering/research/foreverpin-extractions/foreverpin-extractions.md:66`; E4 at `:21`, E11 at `:28`

## 2. Code paths that grant access to a local / loopback caller

| Path | Behaviour | Where |
|---|---|---|
| API key access gate (SDK core `10.0.60`–`10.0.81`, now identity repo) | no key + `AllowLocalWithoutKey` (default `true`) + `RemoteIpAddress` null or loopback → passes the guarded paths | SDK `v10.0.74-beta:…/src/Identity/ApiKeys/ApiKeyAccessGateMiddleware.cs:59,73-75` · options `:17-22`; today `{id}/packages/Auth/ApiKeys/ApiKeyAccessGateMiddleware.cs:59,73-76` · `ApiKeyAccessGateOptions.cs:22` |
| Hangfire dashboard (SDK core, HEAD) | `localRequestsOnly = true` by default → Hangfire `LocalRequestsOnlyAuthorizationFilter` | `{sdk}/Jobs/Hangfire/HangfireDashboardApplicationBuilderExtensions.cs:14-28` (filter at `:25`) |
| TranscriptForge `LocalAccessGuardMiddleware` | runs before the gate; keyless pass also needs `Host` = `localhost`/loopback literal and same-site browser headers; below the open path it requires a local caller | `{tf}/TranscriptForge.Api/ApiKeys/Core/Middlewares/LocalAccessGuardMiddleware.cs:42-55,82-94` |

- Consumers of those paths:
  - TranscriptForge wires guard → gate → metering; its `/api/keys` path is local-only — `{tf}/TranscriptForge.Api/Configurations/HostConfiguration.cs:79-83`, `HostConfiguration.Extensions.cs:296-305`
  - TranscriptForge maps the Hangfire dashboard on `/jobs` — `HostConfiguration.cs:86`
  - Harvest wires the gate with `AllowLocalWithoutKey = false` — `workbench/wow-two-sdk-beta/wow-two-sdk-beta.harvest/…/Harvest.Api/Configurations/HostConfiguration.Extensions.cs:40`, `HostConfiguration.cs:45`
  - no other product calls `UseApiKeyAccessGate` or `UseHangfireJobsDashboard` (workbench-wide grep)
- Remote-address uses that are not access grants:
  - SDK per-IP rate-limit partitions — `{sdk}/Web/RateLimit/RateLimitServiceCollectionExtensions.cs:26`, `ConfiguredRateLimitServiceCollectionExtensions.cs:82`
  - quota subject — `{sdk}/Web/Quotas/ClaimQuotaSubjectService.cs:22`
  - captcha `remoteip` — `{sdk}/Web/Captcha/CaptchaValidator.cs:28`
  - Secrets Vault audit `sourceIp` — `{sv}/SecretsVault.Api/Auth/DataPlaneAuthFilter.cs:39`, `Controllers/SecretsController.cs:30`, `Controllers/IdentityController.cs:27`
  - Secrets Vault login limiter partition — `{sv}/SecretsVault.Api/Configurations/VaultHttpConfiguration.cs:31-32`
  - ForeverPin redirect analytics and geolocation — `…/ForeverPin.Redirect.Api/Endpoints/RedirectEndpoints.cs:35,41`
- Environment-based "local" checks (`IsLocalRun`, Wheelhouse `LocalRun.IsLocal`) read host config, not the request, and open only the OpenAPI document — `{sdk}/Meta/ApiDefaultsExtensions.cs:172`

## 3. Can a remote client spoof its way in today?

Reasoning chain for a product on SDK ≥ `10.0.60` with no post-configure:

1. A direct remote client's socket peer is neither loopback nor configured, so `ForwardedHeadersMiddleware` skips its headers. `RemoteIpAddress` stays the real address, and the gate asks for a key (`HostingServiceCollectionExtensions.cs:41-47`; test `ProxyAwareHostingTests.cs:19`).
2. Behind a loopback reverse proxy that appends or overwrites `X-Forwarded-For`, `ForwardLimit = 1` unwinds only the right-most entry. The proxy wrote that entry, so a client-supplied `127.0.0.1` further left is never read.
3. Behind a loopback proxy that forwards no `X-Forwarded-For`, every request is local whether or not headers are processed. That is a topology issue, which the gate's own remark warns about (`v10.0.74` `ApiKeyAccessGateOptions.cs:18-21`).
4. Processing headers from a loopback peer can only make a request less local than ignoring them. Without processing, that peer is already loopback.
5. Spoofing becomes possible only when a product trusts a non-loopback ingress (`TrustProxiesFrom` / `TrustedNetworks`) that passes the client's value through as the last hop. No product that trusts an ingress has a loopback-based access path:
   - TranscriptForge does not call `TrustProxiesFrom`
   - Harvest calls it but disables the local pass

- Result: **not exploitable** on any SDK version currently pinned at `10.0.60` or later
- Pre-fix SDKs (≤ `10.0.59`) were spoofable, but no product on them has a loopback access path:
  - those products have no gate and no dashboard
  - the gate and dashboard pairings above do not exist on those pins

## 4. Products, pins and whether they need a fix

| Product | Pinned SDK | Forwarded-headers trust in effect | Loopback access path | Status |
|---|---|---|---|---|
| Secrets Vault | `WoW2.Sdk.Backend.Beta` `10.0.56-beta` (`{sv}/Directory.Packages.props:19`) | trust-all default, overridden: none unless `VaultHttp:KnownProxies` set, then those only, `ForwardLimit = 1` (`VaultHttpConfiguration.cs:14-26`) | none (audit + rate-limit only) | fixed locally; fix still needed while pinned < 10.0.60 |
| TransportBrain | `WoW2.Sdk.Backend.Beta` `10.0.45-beta` (`…/tbs.backend-services/Directory.Packages.props:14`) | **trust-all default, no override** — `AddApiDefaults` / `UseApiDefaults` at `TransportBrain.Api/Configurations/HostConfiguration.cs:22,53` | none; rate limiting off (`:26`) | no local-access exploit; client IP, scheme and host are forgeable; re-pin ≥ 10.0.60 closes it |
| TnisMintrans | `WoW2.Sdk.Backend.Beta` `10.0.21-beta` (`…/tnis-mintrans.backend-services/Directory.Packages.props:14`) | not wired: no `AddApiDefaults` / `AddProxyAwareHosting` / `UseForwardedHeaders` in its code | none | not affected |
| Ocharo blog / brand / catalogue (retired copies) | `10.0.59-beta` | trust-all default (pin) | not checked | under `ocharo-ws/.local/retired-sources/2026-09-29/` — retired; live Ocharo repos pin `10.0.71-beta` |
| TranscriptForge | `10.0.74-beta` (`{tf}/Directory.Packages.props:6`) | `ForwardedHeaders.None` post-configure (`HostConfiguration.cs:48-51`) | gate + guard + Hangfire dashboard | safe; post-configure redundant against spoofing (see residual risk) |
| Harvest | `10.0.81-beta` | SDK default + `TrustProxiesFrom` | gate with local pass off | safe |
| Every other product (Wheelhouse `10.0.80`, Matinee `10.0.75`, ForeverPin / PoseCoach `10.0.72`, Wheelhouse Canary and live Ocharo repos `10.0.71`, Home Atlas / MedTextFab `10.0.63`, the 10.0.74 cohort) | ≥ `10.0.60-beta` | SDK hardened default, 26 repos add `TrustProxiesFrom` | none found | safe |

## Residual risk (not header spoofing)

- TranscriptForge's `ForwardedHeaders.None` combines with `AllowLocalWithoutKey = true`. Behind a same-machine reverse proxy or tunnel, every request would then look local and pass without a key:
  - the SDK default would restore the client address there, provided the proxy sets `X-Forwarded-For`
  - the product already flags this: `{tf}/TranscriptForge.Infrastructure/Settings/ApiAccessSettings.cs:6-10` and the "Hosted proxy trust is separate work" comment at `HostConfiguration.cs:48-49`
- `TrustProxiesFrom` products rely on their ingress to append to or overwrite `X-Forwarded-For`:
  - harmless today, since none of them has a loopback access path
  - it starts to matter if the identity gate's local pass reaches them

## Could not verify

- ASP.NET Core and Hangfire internals: not read from framework or package source, which sit outside the repos:
  - two empty `ForwardedHeadersOptions` lists disable the sender check
  - `ForwardLimit` unwinds right-to-left
  - Hangfire's filter compares `RemoteIpAddress` with loopback and the local address
  - the repo itself corroborates the first point twice: `foreverpin-extractions.md:66` and the Secrets Vault comment at `VaultHttpConfiguration.cs:14`
- Deployed topology of TranscriptForge, Secrets Vault and TransportBrain (direct, loopback proxy, ingress network) and each ingress's `X-Forwarded-For` handling; no host or deployment config was read
- Whether the `10.0.21`/`10.0.45` NuGet packages match the release commits: no local tags exist below `v10.0.56-beta`, so those were read at the `chore: release` commits `35d1a84` and `eef9c7c`
- Untagged intermediate SDK commits between `10.0.59` and `10.0.60`; only tagged releases are treated as published

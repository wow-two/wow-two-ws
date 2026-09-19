# Guest session service verification

*Last updated: 2026-09-15*

## Scope

- `IGuestSession` / `CookieGuestSession` → `IGuestSessionService` / `CookieGuestSessionService`.
- Both declarations moved to `Identity/Guest/Services/` with matching namespace.
- Updated exact registration, current-user XML references, guide, request-scope error text and existing registration test.
- Concrete summary starts with `Provides`; interface summary with `Defines`.
- Preserved `EnsureGuest`, `Clear`, `AddGuestSession`, options, request-scoped `TryAdd` registration,
  existing-id reuse, once-per-request caching, cookie attributes, cookie deletion and null/context guards.
- Seven source/doc/test files changed in this lane; no other suffix families changed.
- No new tests, package changes, staging, commits or pushes.

---

## Checks

- `dotnet build Identity.Tests/WoW.Two.Sdk.Backend.Beta.Identity.Tests.csproj --no-restore -m:1`, from SDK `src/`:
  exit 0, 62 warnings, 0 errors. Log: `/private/tmp/guest-session-service-build.log`.
- `dotnet test Identity.Tests/WoW.Two.Sdk.Backend.Beta.Identity.Tests.csproj --no-build --no-restore --filter FullyQualifiedName~AddGuestSession_ShouldResolveTheSession_WhenConfigured`:
  exit 0, 1 passed, 0 failed, 0 skipped. Native permission granted; actual run completed and output was captured directly.
- SDK-wide exact old-type search excluding generated output and the parent-owned historical sweep tracker returned no references.
- SDK `git diff --check` passed.

---

## Coverage limits and retained follow-up

- The existing test checks configured DI resolution. It does not exercise cookie issuance, reuse or clearing over HTTP.
- No release or full SDK validation is claimed.
- Hash-chain mixed-version segment validation remains an explicit follow-up: docs describe validating version segments,
  but the current algorithm starts from sequence 1 and an empty prior hash without a checkpoint input. See
  [hash-chain-validator-verification.md](hash-chain-validator-verification.md). This lane does not alter that behavior.

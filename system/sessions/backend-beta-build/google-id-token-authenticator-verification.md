# Google ID-token authenticator verification

*Last updated: 2026-09-14*

## Scope

- `IGoogleIdTokenVerifier` / `GoogleIdTokenVerifier` → `IGoogleIdTokenAuthenticator` / `GoogleIdTokenAuthenticator`.
- Moved the role pair to `Identity/OAuth/Google/Authenticators/`, with matching namespace.
- Renamed the contract method to `AuthenticateAsync` and the documented call site accordingly.
- Renamed options, registration extension type/file and `AddGoogleIdTokenAuthenticator` references.
- Options remain beside their registration under `Identity/OAuth/Google/`.
- Concrete summary starts with `Authenticates`; interface with `Defines`; options with `Holds`.
- Preserved Google validation settings and call, null/untrusted outcomes, email requirement, name fallback,
  invalid-token handling, logging, and `TryAddSingleton` override semantics.
- Preserved the existing `GoogleVerifiedIdentity` body-property shape; only its contract documentation/import changed in this lane.
- `HashChainVerifier` and other verification APIs are untouched.
- No new tests, package changes, staging, commits or pushes.

---

## Checks

- `dotnet build WoW.Two.Sdk.Backend.Beta.csproj --no-restore -m:1`, from SDK `src/`:
  exit 0, 37 warnings, 0 errors. Log: `/private/tmp/google-id-token-authenticator-build.log`.
- Old-name search under SDK content, excluding generated output and the parent-owned historical sweep tracker,
  returned no references. No old method name remains in the Google feature.
- No references to the old ID-token verification heading anchor were found.
- SDK `git diff --check` passed.
- No existing Google ID-token tests were found; no unrelated test suite was run.

---

## Limits and deferred observations

- This verifies source references and compilation, not live Google authentication or SDK release readiness.
- The existing cancellation parameter is not forwarded to the wrapped Google call; behavior remains unchanged.
- The existing options `Audiences` collection is get-only, unlike the current Options accessor convention.
  Reported both observations to the parent sweep without expanding this rename into behavioral changes.

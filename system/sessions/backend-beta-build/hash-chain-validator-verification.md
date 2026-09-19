# Hash-chain validator verification

*Last updated: 2026-09-15*

## Scope

- `IHashChainVerifier<TEntry>` / `HashChainVerifier<TEntry>` → `IHashChainValidator<TEntry>` / `HashChainValidator<TEntry>`.
- Role pair moved to `Foundation/Audit/Validators/` with matching namespace.
- `Verify` → `Validate`; `HashChainVerificationResult` → `HashChainValidationResult`.
- Updated the exact DI registrations, XML references, result factories, guide, standard and specification: 13 files total.
- Preserved the single-pass sequence/link/hash algorithm, comparison calls, first-failure reason/sequence/index,
  null guards, empty-chain success, generic variance and singleton `TryAdd` override semantics.
- Preserved the existing domain result shape; no FluentValidation conversion.
- Corrected success claims: the supplied chain is internally consistent, but completeness and authenticity are not
  established against a trusted checkpoint. Tail truncation and a consistently rewritten chain can pass.
- Corrected failure documentation that inferred a specific historical alteration from a mismatch alone.
- Corrected canonicalizer XML to identify the consumer as the selector.
- No new tests, package changes, staging, commits or pushes. Other pending naming families are untouched.

---

## Checks

- `dotnet build WoW.Two.Sdk.Backend.Beta.csproj --no-restore -m:1`, from SDK `src/`:
  exit 0, 37 warnings, 0 errors. Log: `/private/tmp/hash-chain-validator-build.log`.
- SDK-wide search excluding generated output and the parent-owned historical sweep tracker found no old type/result references.
- No old `Verify` API or `verifier` wording remains in the Audit feature; no old heading-anchor references found.
- SDK `git diff --check` passed.
- No existing hash-chain tests were found; no unrelated test suite was run.

---

## Limits and deferred observation

- This is scoped compile and source-reference verification, not runtime integrity testing or SDK release validation.
- Existing docs describe validating mixed-version history segment by segment, but the method starts from sequence 1
  and an empty prior hash with no checkpoint input. Reported this mismatch to the parent sweep without changing behavior.
- Google ID-token authenticator work remains complete. Its prior scoped build passed with 37 warnings and 0 errors;
  no direct tests were available. See [google-id-token-authenticator-verification.md](google-id-token-authenticator-verification.md)
  for the preserved cancellation/options observations. This core build also compiles that current source.

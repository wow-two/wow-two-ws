# C20 JWT trust verification

*Verified: 2026-09-16*

## Result

C20 is complete. Bearer registration now accepts exactly one verification-key source, enforces HTTPS discovery metadata by default and pins one compatible signing algorithm. Issuance enforces the selected HMAC algorithm's key length.

## Contract

- `SymmetricKey` and `MetadataAddress` are mutually exclusive and one is required.
- `MetadataAddress` names OpenID Connect discovery metadata; the old misleading `JwksUri` property is removed.
- HTTP metadata fails registration unless `AllowInsecureMetadataForDevelopment` is set explicitly.
- Symmetric validation accepts HS256/384/512 with minimum 32/48/64 UTF-8 bytes.
- Metadata validation accepts one configured RS, PS or ES algorithm and rejects HMAC algorithms.
- Issuance applies the same 32/48/64-byte minimums for HS256/384/512.
- Issuer, audience, source, URI, algorithm and key failures occur during registration or startup option validation.

## Verification

- `dotnet build Identity.Tests/WoW.Two.Sdk.Backend.Beta.Identity.Tests.csproj --no-restore -m:1`: passed.
- `dotnet test Identity.Tests/WoW.Two.Sdk.Backend.Beta.Identity.Tests.csproj --no-build -m:1`: 20 passed, 0 failed, 0 skipped.
- Tests cover required issuer/audience, source exclusivity, HTTPS escape, source-compatible algorithms, algorithm pinning and HMAC key lengths.

## Documentation

- SDK quick starts use `MetadataAddress` and an explicit algorithm.
- The JWT convention now states the enforced source, metadata and key-size contract.

# C29 stored JSON profile verification

*Last updated: 2026-09-16*

## Result

- Added `AddStoredJsonOptionsProfile(key, options)` for a pinned immutable options instance.
- Added `AddStoredJsonOptionsProfile(key, modifiers)` to build a profile through `StoredJsonOptionsFactory`.
- Added `GetRequiredStoredJsonOptionsProfile(key)` with explicit unknown-key failure.
- Rejected mutable options at registration so a stored format cannot drift after composition.
- Retained direct `JsonSerializerOptions` arguments on `JsonValueConverter`, `JsonValueComparer` and
  `HasJsonConversion`.
- Kept one resolved instance across EF writes, reads, equality, hashing and snapshots.
- Kept HTTP and stored JSON presets independent.
- Removed the stale options-holder recommendation from the factory guide and ForeverPin handoff.
- Preserved ForeverPin's null/blank absence behavior as an accepting-boundary adoption task after SDK repin.

## Verification

- `dotnet build Foundation.Tests/WoW.Two.Sdk.Backend.Beta.Foundation.Tests.csproj --no-restore -m:1`: passed,
  0 errors.
- `dotnet test Foundation.Tests/WoW.Two.Sdk.Backend.Beta.Foundation.Tests.csproj --no-build --no-restore -m:1`:
  119 passed, 0 skipped and 0 failed.
- Coverage verifies exact-instance resolution, subtype serialization through a keyed profile, factory-modifier
  registration, mutable-options rejection and unknown-key failure.
- Scoped `git diff --check` passed for Foundation/Web serialization source, tests and guides.
- Builds retain existing dependency-advisory and analyzer warnings.
- No product code, whole-solution, pack, CI, publish or consumer result is claimed.

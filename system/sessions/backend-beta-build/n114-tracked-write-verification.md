# N114 tracked-write verification

*Last updated: 2026-09-16*

## Result

- Changed `EfRepository.UpdateAsync` to save an already tracked entity without calling `DbSet.Update`.
- Applied the same tracked-instance behavior to `EfUserRepository.UpdateAsync`.
- Preserved EF original concurrency values and property-level change detection.
- Rejected a detached replacement when another instance with the same key is tracked.
- Avoided implicit merging, detaching and tracker clearing.
- Retained detached full-state updates when no same-key instance is tracked; this path explicitly uses
  `DbSet.Update` and marks the mapped state modified.
- Documented the tracked, replacement and detached paths on the repository contracts and guides.
- Retained the sealed-record convention; no class conversion was introduced.

## Equality and navigation inventory

- Current SDK production source has no entity navigation collection using a default `HashSet<TEntity>`.
- Current SDK production source has no hashed lookup keyed by a mutable entity object.
- SDK in-memory stores key records by stable scalar IDs.
- The retained EF experiment's 20 assertions verify that reference equality preserves identity-bearing
  navigation membership and that extracted stable keys avoid mutable record-hash failures.

## Verification

- `dotnet build WoW.Two.Sdk.Backend.Beta.csproj --no-restore -m:1`: passed, 0 errors.
- `dotnet build Data.Tests/WoW.Two.Sdk.Backend.Beta.Data.Tests.csproj --no-restore --no-dependencies -m:1`:
  passed, 0 errors.
- Targeted `EfRepositoryTrackedWriteTests`: 3 passed, 0 skipped and 0 failed.
- `dotnet build Identity.Tests/WoW.Two.Sdk.Backend.Beta.Identity.Tests.csproj --no-restore -m:1`: passed,
  0 errors.
- Full `Identity.Tests`: 7 passed, 0 skipped and 0 failed.
- Scoped `git diff --check` passed.
- No full Data.Tests, whole-solution, pack, CI, publish or consumer result is claimed.

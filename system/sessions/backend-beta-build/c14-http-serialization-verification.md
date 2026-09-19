# C14 HTTP serialization verification

*Last updated: 2026-09-16*

## Result

- Added `IsoDurationJsonConverter` and included it in `JsonOptionsConstants.Default`.
- Serialized `TimeSpan` as an ISO 8601 duration such as `P2DT1S`.
- Rejected non-string and malformed duration input with `JsonException`.
- Configured camelCase `JsonStringEnumConverter` with `allowIntegerValues: false`.
- Applied the same strict enum behavior to `AddJsonStringEnums` and the complete controller preset.
- Kept `StoredJsonConstants.Default` and `StoredJsonOptionsFactory` independent from the HTTP preset.
- Corrected the Web and Foundation serialization guides to describe the current contract.

## Verification

- `dotnet build Web.Tests/WoW.Two.Sdk.Backend.Beta.Web.Tests.csproj --no-restore -m:1`: passed,
  0 errors.
- `dotnet test Web.Tests/WoW.Two.Sdk.Backend.Beta.Web.Tests.csproj --no-build --no-restore -m:1`:
  44 passed, 0 skipped and 0 failed.
- Coverage verifies property and dictionary camelCase, null omission, enum and flags strings, numeric/unknown
  enum rejection, ISO duration output, and `Guid`/`bool`/numeric/date/time scalar round trips.
- Builds retain existing dependency-advisory and analyzer warnings.
- No stored-format migration, whole-solution, pack, CI, publish or consumer result is claimed.

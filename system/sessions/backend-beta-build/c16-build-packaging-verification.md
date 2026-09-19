# C16 build and packaging verification

*Last updated: 2026-09-16*

## Result

- the shared `IsPackable` default now applies only when a project has no explicit value.
- all seven test projects evaluate `IsPackable=false` and `IsTestProject=true`.
- the mono library, data abstractions, migration CLI and four testing libraries remain packable.
- every project evaluates `TargetFramework=net10.0` and `Version=10.0.55-beta`.
- `global.json` pins SDK `10.0.300` with `latestPatch` roll-forward.
- the publish workflow installs the SDK policy from that `global.json`.

## Verification

- `dotnet --version` resolved `10.0.300` from the repository pin.
- evaluated `TargetFramework`, `Version`, `PackageId`, `IsPackable` and `IsTestProject`
  for all 14 projects through `dotnet msbuild -getProperty`.
- `dotnet restore WoW.Two.Sdk.Backend.Beta.slnx -m:1` passed.
- `dotnet build WoW.Two.Sdk.Backend.Beta.slnx --no-restore -m:1` passed with zero errors.

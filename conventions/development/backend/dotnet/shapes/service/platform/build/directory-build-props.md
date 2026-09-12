# Directory.Build.props

*Last updated: 2026-09-10*

> Build defaults and test properties inherited by a backend service solution.

## Baseline

- must declare the shared target framework, nullable analysis and implicit usings here.
- must use the target framework's supported default C# version unless the repo declares an explicit exception.
- must not use `LangVersion=latest` as a reproducibility guarantee.
- must keep project-specific settings in their project; shared settings belong here.
- must record the compiler SDK selection and roll-forward policy in `global.json` for reproducible builds.
- must align local verification and CI with that SDK policy.

```xml
<Project>
  <PropertyGroup>
    <TargetFramework>net10.0</TargetFramework>
    <Nullable>enable</Nullable>
    <ImplicitUsings>enable</ImplicitUsings>
  </PropertyGroup>
</Project>
```

---

## Test runs

- must run service tests with the SUT environment explicitly set to `Development`.
- must wire `tests.runsettings` at the solution root through `RunSettingsFilePath` for VSTest projects.
- must distinguish host defaults: `WebApplicationFactory` defaults to `Development`; a generic host may not.
- must select all test names allowed by [testing](../../architecture/clean/testing.md#layout).
- must apply `IsPackable=false` after any shared package default; a later assignment wins in MSBuild.
- must verify the evaluated properties for each test tier, not only the predicate's text.
- must configure an equivalent environment mechanism when a runner does not consume `.runsettings`.

```xml
<PropertyGroup Condition="$(MSBuildProjectName.Contains('.Tests.')) Or $(MSBuildProjectName.EndsWith('.Tests'))">
  <RunSettingsFilePath>$(MSBuildThisFileDirectory)tests.runsettings</RunSettingsFilePath>
  <IsPackable>false</IsPackable>
</PropertyGroup>
```

---

## Analyzers

- may adopt warnings-as-errors and build-time analyzers for a stricter build.
- must keep correctness diagnostics as errors when adopting warnings-as-errors.
- must document each diagnostic exception beside its `WarningsNotAsErrors` entry.
- must leave exempt diagnostics visible; do not suppress them with `NoWarn` to make a build green.
- may exempt a dependency advisory temporarily when the dependency cannot yet be upgraded.
- must record the affected dependency and follow-up; an advisory exemption is not a clean audit result.
- must tie analyzer selection to the compiler SDK policy in [Baseline](#baseline).

---

## Packaging

- must apply [SDK delivery](../../../sdk/delivery/delivery.md) for package metadata and release validation.
- must not copy package-authoring metadata into an image-only product host.

# Central Package Management

*Last updated: 2026-09-10*

> NuGet version ownership for a backend service solution.

## Versions

- must enable `ManagePackageVersionsCentrally` in `Directory.Packages.props`.
- must declare a package version once with `PackageVersion`.
- must reference packages by name only with `PackageReference` in each consuming project.
- must not put `Version` on `PackageReference`; preserve the `NU1008` guard.
- must choose direct version floors that satisfy dependencies' transitive minimums.
- must group versions by concern; order package IDs within each group.

```xml
<Project>
  <PropertyGroup>
    <ManagePackageVersionsCentrally>true</ManagePackageVersionsCentrally>
  </PropertyGroup>
  <ItemGroup>
    <PackageVersion Include="{PackageId}" Version="{Version}" />
  </ItemGroup>
</Project>
```

---

## Changes

- must add the central version and a name-only reference in each project that uses the package.
- must bump the central version to update every reference to that package.
- must remove a central version when its last reference is removed.
- must update related SDK package versions together when the package family releases together.
- must read published IDs from package metadata; assembly names need not equal package IDs.

---

## Framework references

- must declare a required shared framework with `FrameworkReference` in the project that consumes it.
- must diagnose a downgrade from the evaluated dependency graph, not infer it from `ProjectReference` alone.
- may enable `CentralPackageTransitivePinningEnabled` for intentional central transitive constraints.
- must not treat transitive pinning as a lockfile or a compiler SDK pin.

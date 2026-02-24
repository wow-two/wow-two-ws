# WoW 2.0 — Versioning Strategy

> **Scope**: All .NET library packages (SDK + Platform repos).

---

## Version Format

```
{dotnet_major}.{release}.{patch}[-prerelease_suffix]
```

### The major version IS the .NET SDK version

The first segment of the version always matches the target .NET SDK major version. This makes it immediately clear which .NET version a package targets.

| .NET Target | Version Range | Example |
|-------------|---------------|---------|
| .NET 8 | `8.x.x` | `8.0.0`, `8.1.0`, `8.1.3` |
| .NET 9 | `9.x.x` | `9.0.0`, `9.0.1`, `9.2.0` |
| .NET 10 | `10.x.x` | `10.0.0` |

### Segment meanings

```
9.2.1
│ │ └── Patch: bug fixes, no API changes
│ └──── Release: new features, backward compatible within same .NET version
└────── .NET SDK version (always matches TargetFramework major)
```

### Examples

```
9.0.0-alpha.1    → First alpha on .NET 9
9.0.0-alpha.2    → Second alpha
9.0.0            → First stable release on .NET 9
9.0.1            → Bug fix
9.1.0            → New feature added
9.1.1            → Bug fix on 9.1
10.0.0-alpha.1   → Migration to .NET 10 begins
10.0.0           → First stable on .NET 10
```

---

## Pre-release Suffixes

| Suffix | Channel | Published To | Purpose |
|--------|---------|-------------|---------|
| `-alpha.{n}` | Dev | GitHub Packages | Active development, may break |
| `-beta.{n}` | Pre-release | NuGet.org (optional) | Feature-complete, testing |
| `-rc.{n}` | Release candidate | NuGet.org | Final validation before stable |
| *(none)* | Stable | NuGet.org | Production-ready |

### Typical flow
```
9.0.0-alpha.1 → 9.0.0-alpha.2 → ... → 9.0.0-beta.1 → 9.0.0-rc.1 → 9.0.0
```

For most packages, alpha → stable is sufficient (skip beta/rc):
```
9.0.0-alpha.1 → 9.0.0-alpha.2 → ... → 9.0.0
```

---

## .NET Version Migration

When .NET ships a new major version:

1. **Keep existing stable version** on old .NET (e.g., `9.3.1` on .NET 9)
2. **Start new alpha** on new .NET (e.g., `10.0.0-alpha.1` on .NET 10)
3. **No multi-targeting** for now — each package targets one .NET version
4. **Old versions are maintained** only for critical security fixes

---

## Where Version Lives

- **In `.csproj`**: `<Version>9.0.0-alpha.1</Version>`
- **CI override**: Pipeline can append/modify the pre-release suffix
  - Dev branch auto-increments alpha number
  - Main branch strips pre-release suffix for stable

### CI version logic
```
dev branch:   Version from .csproj + "-alpha.{run_number}" override
main branch:  Version from .csproj (no suffix = stable)
```

---

## Breaking Changes

Since the major version is locked to .NET version, breaking API changes within the same .NET version bump the **release** segment:

```
9.0.0  → stable release
9.1.0  → new feature (non-breaking)
9.2.0  → breaking API change (document in CHANGELOG)
```

**Note**: This is a deliberate deviation from strict SemVer where major = breaking. The trade-off is worth it for the clarity of .NET version alignment. Breaking changes are communicated via CHANGELOG and release notes.

---

## Cross-Package Version Alignment

All packages within the same solution/repo should share the same version:

```
WoW2.Sdk.Language.Serialization.Json.Abstractions          → 9.0.0-alpha.1
WoW2.Sdk.Language.Serialization.Json.System                 → 9.0.0-alpha.1
WoW2.Sdk.Language.Serialization.Json.System.DependencyInjection → 9.0.0-alpha.1
WoW2.Sdk.Language.Serialization.Json.Newtonsoft             → 9.0.0-alpha.1
... (all in sync)
```

Use `Directory.Build.props` to enforce this:
```xml
<PropertyGroup>
  <VersionPrefix>9.0.0</VersionPrefix>
</PropertyGroup>
```

---

## Applies To

| Repo Type | Uses This Strategy | Notes |
|-----------|-------------------|-------|
| SDK libs (`sdk.*`) | Yes | Public packages, strict versioning |
| Platform libs (`platform.*`) | Yes | Internal packages, same convention |
| Apps (`apps.*`) | Optional | Apps may use simpler versioning |
| KB modules (`kb.*`) | No | No published packages |

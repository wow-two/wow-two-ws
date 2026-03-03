# WoW 2.0 — NuGet Package Best Practices

> **Scope**: Standards for all published .NET packages (SDK + Platform repos).
> Derived from research of Polly, MediatR, AutoMapper, Serilog, and Microsoft guidance.

---

## Repository Layout

```
repo-root/
├── src/
│   ├── WoW2.Sdk.{Domain}/                 # Main package project
│   └── WoW2.Sdk.{Domain}.Abstractions/    # Contracts/interfaces (if needed)
├── tests/
│   ├── WoW2.Sdk.{Domain}.UnitTests/
│   └── WoW2.Sdk.{Domain}.IntegrationTests/
├── samples/                                # Optional: runnable example projects
├── benchmarks/                             # Optional: BenchmarkDotNet perf tests
├── docs/
├── Directory.Build.props                   # Shared build config
├── Directory.Packages.props                # Central package version management
├── .editorconfig
├── .gitignore
├── LICENSE                                 # MIT
├── CHANGELOG.md
├── CLAUDE.md                               # AI context for Claude workflows
├── README.md                               # Rendered on NuGet.org + GitHub
├── icon.png                                # 128x128 PNG (≤1MB)
├── NuGet.Config                            # Package sources
└── {Solution}.sln
```

---

## Directory.Build.props

Centralizes shared MSBuild properties across all projects in a solution.

```xml
<Project>
  <PropertyGroup>
    <TargetFramework>net9.0</TargetFramework>
    <LangVersion>latest</LangVersion>
    <Nullable>enable</Nullable>
    <ImplicitUsings>enable</ImplicitUsings>
    <TreatWarningsAsErrors>true</TreatWarningsAsErrors>
    <WarningsNotAsErrors>CS1591</WarningsNotAsErrors>
  </PropertyGroup>

  <!-- Shared package metadata -->
  <PropertyGroup>
    <VersionPrefix>9.0.0</VersionPrefix>
    <Authors>WoW 2.0 Team</Authors>
    <Company>wow-two</Company>
    <RepositoryUrl>https://github.com/wow-two-sdk/REPO_NAME</RepositoryUrl>
    <RepositoryType>git</RepositoryType>
    <PackageLicenseExpression>MIT</PackageLicenseExpression>
  </PropertyGroup>

  <!-- Source Link + symbol packages -->
  <PropertyGroup>
    <PublishRepositoryUrl>true</PublishRepositoryUrl>
    <EmbedUntrackedSources>true</EmbedUntrackedSources>
    <IncludeSymbols>true</IncludeSymbols>
    <SymbolPackageFormat>snupkg</SymbolPackageFormat>
  </PropertyGroup>

  <!-- XML docs for non-test projects -->
  <PropertyGroup Condition="'$(IsTestProject)' != 'true'">
    <GenerateDocumentationFile>true</GenerateDocumentationFile>
  </PropertyGroup>

  <!-- Suppress docs for test projects -->
  <PropertyGroup Condition="'$(IsTestProject)' == 'true'">
    <GenerateDocumentationFile>false</GenerateDocumentationFile>
  </PropertyGroup>

  <!-- Source Link package -->
  <ItemGroup>
    <PackageReference Include="Microsoft.SourceLink.GitHub" Version="8.0.0" PrivateAssets="All" />
  </ItemGroup>
</Project>
```

---

## Directory.Packages.props (Central Package Management)

Manages all NuGet dependency versions in one place.

```xml
<Project>
  <PropertyGroup>
    <ManagePackageVersionsCentrally>true</ManagePackageVersionsCentrally>
  </PropertyGroup>

  <ItemGroup>
    <!-- Test frameworks -->
    <PackageVersion Include="xunit" Version="2.8.1" />
    <PackageVersion Include="xunit.runner.visualstudio" Version="2.8.1" />
    <PackageVersion Include="Moq" Version="4.20.70" />
    <PackageVersion Include="Microsoft.NET.Test.Sdk" Version="17.12.0" />

    <!-- Code analysis -->
    <PackageVersion Include="Microsoft.CodeAnalysis.NetAnalyzers" Version="8.0.0" />
    <PackageVersion Include="Microsoft.SourceLink.GitHub" Version="8.0.0" />

    <!-- Common dependencies -->
    <PackageVersion Include="Microsoft.Extensions.DependencyInjection" Version="9.0.2" />
    <PackageVersion Include="Newtonsoft.Json" Version="13.0.3" />
  </ItemGroup>
</Project>
```

Individual .csproj files then reference without version:
```xml
<PackageReference Include="xunit" />
```

---

## .csproj Package Metadata

Each publishable project should include full NuGet metadata.

### Required properties

| Property | Purpose | Example |
|----------|---------|---------|
| `PackageId` | Unique NuGet identifier | `WoW2.Sdk.Language.Serialization.Json.System` |
| `Version` | SemVer (or use VersionPrefix from Directory.Build.props) | `9.0.0-alpha.1` |
| `Title` | Display name | `WoW2 SDK - JSON Serialization (System.Text.Json)` |
| `Description` | 2-3 sentence summary | Explain what problem it solves |
| `Authors` | Package authors | `WoW 2.0 Team` |
| `PackageTags` | Searchable keywords (semicolon-separated) | `json;serialization;system-text-json;wow2` |
| `PackageLicenseExpression` | SPDX license | `MIT` |
| `RepositoryUrl` | GitHub repo URL | `https://github.com/wow-two-sdk/sdk.language.serialization` |
| `RepositoryType` | VCS type | `git` |

### Recommended properties

| Property | Purpose | Example |
|----------|---------|---------|
| `PackageReadmeFile` | README rendered on NuGet.org | `README.md` |
| `PackageIcon` | Package icon | `icon.png` |
| `PackageProjectUrl` | Homepage | Same as RepositoryUrl |
| `PackageReleaseNotes` | Release notes or link to CHANGELOG | `See CHANGELOG.md` |

### Including README and icon in package

```xml
<ItemGroup>
  <None Include="..\..\README.md" Pack="true" PackagePath="\" />
  <None Include="..\..\icon.png" Pack="true" PackagePath="\" />
</ItemGroup>
```

---

## Source Link & Symbol Packages

Source Link enables step-into debugging directly into package source code from Visual Studio.

### Setup (in Directory.Build.props)

```xml
<PackageReference Include="Microsoft.SourceLink.GitHub" Version="8.0.0" PrivateAssets="All" />

<PropertyGroup>
  <PublishRepositoryUrl>true</PublishRepositoryUrl>
  <EmbedUntrackedSources>true</EmbedUntrackedSources>
  <IncludeSymbols>true</IncludeSymbols>
  <SymbolPackageFormat>snupkg</SymbolPackageFormat>
</PropertyGroup>
```

### Publishing

```bash
# Pack generates both .nupkg and .snupkg
dotnet pack -c Release

# Push both to NuGet.org
dotnet nuget push "*.nupkg" --api-key {key} --source https://api.nuget.org/v3/index.json
dotnet nuget push "*.snupkg" --api-key {key} --source https://api.nuget.org/v3/index.json
```

---

## README Structure for NuGet Packages

NuGet.org renders CommonMark markdown. This is the standard structure used by top packages.

```markdown
# Package Name

[![NuGet](badge-url)](nuget-url)
[![Build](ci-badge)](ci-url)
[![License](license-badge)](license-file)

Brief one-liner description.

## What is {Package}?

2-3 sentences on what problem it solves + key benefits.

## Installation

\`\`\`bash
dotnet add package WoW2.Sdk.{Domain}
\`\`\`

## Quick Start

10-20 lines of runnable code showing basic usage.

## Features

- Feature 1
- Feature 2
- Feature 3

## Usage Examples

### Scenario A
Complete, runnable code example.

### Scenario B
Another example.

## Service Registration (DI)

\`\`\`csharp
services.AddSystemTextJsonSerializer();
\`\`\`

## License

MIT — see LICENSE file.
```

### Key rules
- CommonMark only — no relative image paths, use absolute URLs
- Code samples must be syntactically correct and tested
- Preview on NuGet.org upload portal before publishing
- Badges from trusted domains only (shields.io, github.com)

---

## Test Conventions

### Framework: xUnit

xUnit is the modern .NET standard — simpler, better isolation, built-in parallelization.

### Project naming

| Type | Pattern | Example |
|------|---------|---------|
| Unit tests | `{Package}.UnitTests` | `WoW2.Sdk.Language.Serialization.Json.System.UnitTests` |
| Integration tests | `{Package}.IntegrationTests` | `WoW2.Sdk.Language.Serialization.Json.System.IntegrationTests` |

### Test method naming

```
MethodName_StateUnderTest_ExpectedBehavior
```

Examples:
- `Serialize_ValidObject_ReturnsJsonString`
- `Deserialize_NullInput_ThrowsArgumentNullException`
- `AddSerializer_DefaultConfig_RegistersSingleton`

### Test project structure

```
WoW2.Sdk.{Domain}.UnitTests/
├── {SutClassName}/
│   ├── SerializeTests.cs
│   ├── DeserializeTests.cs
│   └── ConfigurationTests.cs
├── Fixtures/
│   └── SampleDataFixture.cs
└── WoW2.Sdk.{Domain}.UnitTests.csproj
```

### Test .csproj

```xml
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <TargetFramework>net9.0</TargetFramework>
    <IsTestProject>true</IsTestProject>
  </PropertyGroup>

  <ItemGroup>
    <PackageReference Include="xunit" />
    <PackageReference Include="xunit.runner.visualstudio">
      <PrivateAssets>all</PrivateAssets>
    </PackageReference>
    <PackageReference Include="Microsoft.NET.Test.Sdk" />
    <PackageReference Include="Moq" />
  </ItemGroup>

  <ItemGroup>
    <ProjectReference Include="..\..\src\WoW2.Sdk.{Domain}\WoW2.Sdk.{Domain}.csproj" />
  </ItemGroup>
</Project>
```

---

## Sample Projects

Include samples when the library has non-obvious APIs or supports multiple patterns.

```
samples/
├── WoW2.Sdk.{Domain}.Sample/
│   ├── Program.cs               # DI setup + usage
│   ├── Examples/
│   │   ├── BasicUsageExample.cs
│   │   └── AdvancedConfigExample.cs
│   └── README.md                # How to run
```

### Rules
- Samples must be completely runnable with no manual setup
- Use realistic, production-like code
- Document with comments explaining "why, not what"

---

## CHANGELOG Format

Use [Keep a Changelog](https://keepachangelog.com/) format:

```markdown
# Changelog

## [9.0.0] - 2026-MM-DD

### Added
- Initial release under WoW2.Sdk namespace
- System.Text.Json serializer with async support
- Newtonsoft.Json serializer
- DI extension methods for both providers
- Enum description/field name converters

## [9.0.0-alpha.1] - 2026-02-24

### Added
- Renamed from Backbone.Language.Features.Serialization
- ProjectReference-based solution structure
```

---

## Pre-Publication Checklist

### Metadata
- [ ] PackageId follows `WoW2.Sdk.{Domain}` pattern
- [ ] Description is 2-3 sentences
- [ ] PackageTags include 5-10 keywords
- [ ] LicenseExpression set to MIT
- [ ] RepositoryUrl points to GitHub
- [ ] Authors and Company set

### Documentation
- [ ] README.md with quick start + examples
- [ ] CHANGELOG.md documents version history
- [ ] All public APIs have `///` XML doc comments
- [ ] No relative image paths in README

### Quality
- [ ] Unit tests exist and pass (>80% coverage for critical paths)
- [ ] No compiler warnings
- [ ] Nullable reference types enabled
- [ ] Source Link configured
- [ ] Symbol packages (.snupkg) enabled

### Structure
- [ ] Directory.Build.props with shared settings
- [ ] Directory.Packages.props for central version management
- [ ] Clean folder structure (src/, tests/, docs/)
- [ ] .gitignore covers obj/, bin/, .DS_Store, .idea/

### Presentation
- [ ] Package icon (128x128 PNG)
- [ ] LICENSE file (MIT)
- [ ] CHANGELOG.md
- [ ] Preview README on NuGet.org before stable release

---

## CI/CD Package Registry Strategy

### Dual-channel publish

| Channel | Registry | Trigger | Version | Speed |
|---------|----------|---------|---------|-------|
| **Alpha** | GitHub Packages | Push to `dev` | `9.0.0-alpha.{n}` | Fast (no validation) |
| **Stable** | NuGet.org | Push to `main` | `9.0.0` | ~5-10s validation delay |

### Sequential dependency updates (dev channel)

When package A change requires updates in B, C, D:

1. Push A to dev → alpha to GitHub Packages (instant)
2. Update B's reference → push to dev → alpha (instant)
3. Repeat down the chain

GitHub Packages is fast for this iterative workflow. NuGet.org's 5-10s delay per package is only for stable releases where the chain is already validated.

---

## References

- [NuGet Package Authoring Best Practices](https://learn.microsoft.com/en-us/nuget/create-packages/package-authoring-best-practices)
- [Write a High-Quality README for NuGet Packages](https://devblogs.microsoft.com/dotnet/write-a-high-quality-readme-for-nuget-packages/)
- [Source Link in .NET Projects](https://lurumad.github.io/using-source-link-in-net-projects-and-how-to-configure-visual-studio)
- [Directory.Build.props Centralization](https://blog.ndepend.com/directory-build-props/)
- [Central Package Management](https://learn.microsoft.com/en-us/nuget/consume-packages/central-package-management)
- [Unit Testing Best Practices (.NET)](https://learn.microsoft.com/en-us/dotnet/core/testing/unit-testing-best-practices)
- [Ensuring NuGet Best Practices](https://www.meziantou.net/ensuring-best-practices-for-nuget-packages.htm)

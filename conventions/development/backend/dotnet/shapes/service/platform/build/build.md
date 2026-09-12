# Build

*Last updated: 2026-09-10*

> Shared MSBuild properties and NuGet versions for a backend service solution.

## Files

- must place `Directory.Build.props` and `Directory.Packages.props` beside the backend solution.
- must inherit these files from projects beneath the solution root; do not shadow them per layer.
- must keep package versions in [central package management](central-package-management.md).
- must keep shared build properties in [directory build props](directory-build-props.md).
- must keep only project-specific properties and references in a `.csproj`.
- may declare the host's Web SDK, framework references and SPA targets in its own `.csproj`.
- must apply [repo structure](../../../../../../repo/structure/repo-structure.md) for the solution location.
- must use the [SDK shape](../../../sdk/sdk.md) for package-producing repositories.

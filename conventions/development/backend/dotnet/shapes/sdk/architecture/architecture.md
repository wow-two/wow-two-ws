# Architecture

*Last updated: 2026-09-10*

> Source and dependency boundaries inside a reusable .NET SDK.

## Packages

- must keep the concrete package list and source layout in the SDK repository's architecture docs.
- must not impose a service's Application/Infrastructure/Persistence project split on an SDK package.
- must group reusable code by capability and its owning source domain.
- must isolate test harness dependencies from runtime packages.
- must keep web-free contract packages free of an ASP.NET Core framework dependency.
- must compile each owned type in one project; use project references instead of duplicate source globs.
- must match exclusion paths to on-disk casing so Linux and local builds compile the same source set.
- must keep published package IDs distinct from assembly/namespace names when package metadata declares that split.

---

## Composition

- must expose explicit registration contracts rather than self-register on import.
- must preserve caller opt-in boundaries when adding capabilities.
- must keep the package's supported dependency surface documented beside its source.

Concrete ownership: [package layout](../../../../../../../workbench/wow-two-sdk-beta/wow-two-sdk.backend.beta/engineering/architecture/package-layout.md) and [package registry](../../../../../../../workbench/wow-two-sdk-beta/wow-two-sdk.backend.beta/engineering/architecture/package-registry.md).

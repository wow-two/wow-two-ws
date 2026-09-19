# Testing

*Last updated: 2026-09-13*

> Behavior, registration and package-consumption checks for the SDK.

## Behavior

- must run the affected capability's tests for each sweep change.
- must run the SDK's full required test set before publishing a family release.
- must use real provider tests where correctness depends on provider behavior.
- must report unavailable container-backed checks as unverified, not passing.
- must keep tests for public registration seams, including configured and default paths.
- must check that replacement APIs preserve their documented failure and cancellation behavior.
- must verify the package's intended public API from a consumer context, not only within the defining assembly.
- test-body comments follow the shared [optional-comment convention](../../service/architecture/clean/testing.md#body-documentation).

---

## Artifacts

- must pack the declared release projects in Release configuration.
- must inspect each package's ID, version, framework dependencies and own-family dependency versions.
- must verify expected runtime assets, XML docs and symbols when the project declares them.
- must verify a CLI package's tool metadata and entry point when it ships as a dotnet tool.
- must smoke-test installing or referencing the packed artifact for changed packaging surfaces.
- must confirm runtime packages exclude test-only dependencies and duplicate source assemblies.

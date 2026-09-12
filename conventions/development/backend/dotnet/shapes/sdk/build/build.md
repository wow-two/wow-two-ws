# Build

*Last updated: 2026-09-10*

> Build and packaging property evaluation for a .NET SDK family.

## Inputs

- must apply shared [compiler defaults](../../service/platform/build/directory-build-props.md#baseline).
- must apply [central package management](../../service/platform/build/central-package-management.md).
- must maintain one version source for packages released as one family.
- must not infer package IDs or packability from project names; read evaluated package properties.
- must exclude test projects from packaging after shared defaults are evaluated.
- must keep test harness packages packable when they are intentionally shipped libraries.
- must apply runtime/test source exclusions to prevent duplicate compilation and leaked test dependencies.

---

## Verification

- must restore and build the intended release project set with the same SDK policy used by CI.
- must evaluate `TargetFramework`, `Version`, `PackageId` and `IsPackable` for every release project.
- must verify each expected test project's evaluated `IsPackable` is false.
- must run [SDK tests](../testing/testing.md) before the [release cut](../delivery/delivery.md).

# SDK

*Last updated: 2026-09-10*

> Shared .NET package-family rules; package inventory and layout belong to the SDK repository.

## Scope

- must inherit [core](../../core/core.md) declaration, notation and application rules.
- must apply convention changes to the SDK as sweep work, not blanket exemptions.
- must use [extraction](../../../../sdk-extraction.md) to choose reusable capability boundaries.
- must keep product composition outside the SDK; expose explicit caller-owned registration seams.
- must document public APIs and the seams a consumer wires.

---

## Vectors

| Vector | Owns |
|---|---|
| [architecture](architecture/architecture.md) | package and source boundaries |
| [build](build/build.md) | evaluated properties and dependency inputs |
| [testing](testing/testing.md) | package and behavior verification |
| [delivery](delivery/delivery.md) | release artifacts and publishing handoff |

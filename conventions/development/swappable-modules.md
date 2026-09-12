# Swappable modules

*Last updated: 2026-09-10*

> House contracts and interchangeable engine adapters across the SDKs.

## Contract

- must define the house contract around a capability, independently of any vendor's feature list.
- must complete that capability under [vector completeness](dev-cycle.md#vector-completeness--build-the-whole-vector-not-the-ask).
- must use product evidence to shape semantics, not as a consumer-count gate on known missing capabilities.
- must keep vendor types out of the shared contract.
- may expose a typed native-engine escape hatch at the selected adapter boundary.
- must keep escape-hatch coupling local to its consumer; shared components depend on the house contract.
- must inventory repeated escape-hatch use as a possible contract gap during the completion pass.
- must not represent alternative engines as flags on one factory; each adapter owns its entry.

---

## Adapters

- must give each engine its own entry with the same house-facing signature and semantics.
- must isolate vendor runtime dependencies so importing the contract does not load a vendor.
- must follow frontend [delivery](frontend/shapes/library/delivery/delivery.md#dependencies) for optional peer metadata.
- must adapt engine timing, merge, reset and errors to the house contract.
- should establish swap freedom with two conforming implementations, including a house engine when appropriate.
- may defer additional adapters under the exception in [vector completeness](dev-cycle.md#vector-completeness--build-the-whole-vector-not-the-ask).
- may declare an adapter capability ceiling; it must reject unsupported requests explicitly rather than misbehave.
- must not use an adapter ceiling to omit a known capability from the SDK's completion inventory.

---

## Conformance

- must maintain one engine-independent behavioral suite over the shared contract.
- must run the suite unchanged against each adapter for its advertised capabilities.
- must declare optional capability cases centrally and verify unsupported outcomes for adapters lacking them.
- must not fork expected behavior per engine; a mismatch is a contract or adapter defect.
- must add framework integration tests where framework lifecycle changes the observable contract.

---

## App usage

- must pin an engine once at the app's composition root, through an app-owned re-export or registration.
- must let app code depend on that pin and the contract types, never a vendor package directly.
- must keep source placement in the owning app/library shape; this contract does not prescribe a source path.

---

## Retrofit

- must migrate a touched module through contract extraction, adapter alignment and consumer adoption.
- must track remaining capability gaps in its vector-completion plan, not wait for another consumer request.

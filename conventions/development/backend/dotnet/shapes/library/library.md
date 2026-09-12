# Library

*Last updated: 2026-09-10*

> Recognized shape for a library used inside one product; no standalone published-package policy.

## Activation

- must inherit [core](../../core/core.md) rules.
- must define this shape's project boundary, testing and delivery rules when a product extracts a contained library.
- must record its consumer and owning service before choosing references.
- must use the [SDK shape](../sdk/sdk.md) when the package is published as a reusable capability.
- must not interpret this shell as permission to bypass the containing product's architecture.

---

## Open

- contained-library architecture, test layout and delivery remain unwritten until that extraction is active.

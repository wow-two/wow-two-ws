# Validation

*Last updated: 2026-09-10*

> Standard Schema at validation boundaries, with house failures outside that protocol.

## Contract

- must accept Standard Schema without changing its `~standard.validate` input/output protocol.
- must preserve parsed output and every returned issue, including nested paths.
- must support a synchronous result or a promise; async completion follows the caller's value generation.
- must retain Standard Schema's `{ value } | { issues }` shape at that boundary.
- must adapt to a house `Result` only outside the schema protocol when a caller needs that carrier.
- must normalize an unexpected validator throw/rejection at the boundary; an explicit assertion helper may throw.
- must keep issue-to-field binding in [forms](../forms/forms.md).
- must preserve provider issue messages/paths and map house rule codes through the message catalog.
- must not invent a shared code when the provider supplies none; use a declared fallback category.
- must keep schema dependencies optional and isolated under [library delivery](../../../../shapes/library/delivery/delivery.md).

---

## Providers

- must let built-in and third-party Standard Schema implementations use the same contract.
- must keep library-specific transforms, imports and adapter rules in provider leaves.
- must define input/output types separately when parsing transforms a value.
- must run conformance for synchronous/asynchronous success, nested errors, rejection and transformed output.
- must parse external data at its boundary; a TypeScript assertion is not validation.

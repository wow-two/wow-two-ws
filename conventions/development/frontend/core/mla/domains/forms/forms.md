# Forms

*Last updated: 2026-09-10*

> Provider-free editing, schema output and accessible field wiring.

## Values

- must distinguish editable input, parsed schema output and the request submitted to the backend.
- may edit an `*ApiRequest` directly when it can represent every editing state without casts.
- must introduce an app-owned editing `*Model` when partial text, composite controls or UI-only fields differ.
- must validate through [Standard Schema](../validation/validation.md), preserving its input/output distinction.
- must submit parsed output, or a named mapper from that output to the request; do not repeat schema transforms.
- must allow incomplete input while editing without claiming it is already a valid request.
- must keep the schema and editing initializer in the owning application slice.
- must resolve messages through [i18n](../i18n/i18n.md); caller-authored text remains caller-owned.

---

## Binding

- must pin one engine adapter at the composition root; contract types import from the vendor-free entry.
- must keep framework spellings in their provider leaf: [Vue](vue/vue.md).
- must render fields through the form's field binding and shared field chrome.
- must inherit labels, descriptions, validity and interaction flags through the field context.
- must let composite controls use the [field contract](../../constructs/visual/field.md) for group and target naming.
- must render both client and server errors without repeating the same message.
- must mark interaction on blur or submit attempt; do not show initial errors as if the user already interacted.
- must remove a server error when its field changes; retain unrelated errors.
- must read submitted progress from the form's lifecycle rather than an independent saving flag.
- must let the disabled form state make submit inert and propagate through field context.

---

## Reset

- must distinguish initial values from the current dirty baseline.
- must make `reset()` restore the current baseline and `reset(values)` establish a new baseline.
- must apply edit-prefill atomically; do not populate fields through separate effects.
- must preserve dirty user edits when a background refetch arrives unless replacement is explicit.
- must invalidate pending validation/submission display updates when a reset replaces their value generation.

---

## Collections

- must give each rendered row a stable field-array key independent of its current index.
- must keep errors, touched state and focus attached to the row through insert/remove/reorder.
- must address a row's current path through the array binding; never cast an unknown row value to bypass typing.
- must clean up removed-row subscriptions and suppress their late errors.

---

## Submission

- must follow [submission](submission.md) for parsing, wizard steps, autosave and server failures.
- must follow [type mapping](../api/type-mapping.md) for date/time values and request encoding.
- must keep engine escape hatches app-local; shared controls depend on the form contract.
- must complete recurring missing capabilities in the SDK rather than propagate vendor-specific wiring.

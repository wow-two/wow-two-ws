# Stored JSON

*Last updated: 2026-09-13*

> Persisted documents have a contract independent of HTTP serialization.
> Applies to JSON columns, cache entries and files across backend shapes.

## Contract

- must use `StoredJsonConstants.Default` and the SDK converters directly when the default contract fits.
- must not declare a custom per-type serialization wrapper or a dedicated per-type options-holder class.
- must use the same pinned options for reading, writing and any persistence snapshot/comparison mechanism.
- must customize options only when the stored format requires it, such as a document's subtype registry.
- must supply custom options to the shared serializer or select an already registered options profile by key;
  format customization does not justify another wrapper type.
- must build stored options through the SDK's stored-options factory and retain the configured instance
  in the owning composition/registration scope. Reuse the instance without introducing a per-type holder.
- must implement any missing shared options/registration capability in the SDK, not a product wrapper.
- must not reuse or mutate the host's HTTP options for storage; the contracts change independently.
- must treat changes to persisted representation as compatibility/migration work, including enum names,
  discriminators and null handling.

## Boundaries

- must use the SDK's EF JSON conversion and comparison integration for mapped properties;
  mechanics belong to [EF mapping](access/ef/ef-mapping.md#json).
- may call `JsonSerializer` directly with the stored preset or the document's pinned custom options.
- must make absence and malformed-document behavior explicit at the accepting storage boundary.
  Preserve any existing null/blank-as-absence contract when removing a wrapper; do not silently convert
  malformed nonblank JSON into absence or feed blank text into a parser that previously never received it.
- must validate a deserialized candidate under [validation](../validation/validation.md) before acceptance.
- must keep real multi-format codecs and converters under their own roles; retiring the per-type wrapper
  does not remove serializer implementations that select or implement a format.

## Rationale

Shared SDK options and converters own the reusable behavior. Polymorphic discriminators, converters and
legacy stored formats can require different options; passing those options or selecting a registered profile
covers that need. Neither a per-type serialization wrapper nor a dedicated options-holder class is justified
by that customization. Real codecs implement serialization behavior; their options remain ordinary configuration.

The [HTTP serialization contract](../../../../shapes/service/platform/responses/serialization.md) remains separate.

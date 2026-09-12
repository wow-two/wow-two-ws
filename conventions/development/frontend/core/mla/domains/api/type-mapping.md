# Type mapping

*Last updated: 2026-09-12*

> The declared wire scalars and their validated frontend representations.

## Wire

- must take emitted JSON from the [backend contract](../../../../../backend/dotnet/shapes/service/platform/responses/serialization.md).
- must describe wire fields with JSON types in a `*Dto` or `*ApiRequest`; a static type does not validate input.
- must validate unknown input at integration before exposing a typed value.

| Wire value | DTO representation | Decoded value when needed |
|---|---|---|
| identifier or text | `string` | `string` |
| boolean | `boolean` | `boolean` |
| exact JSON number | lossless numeric value from original token | exact integer/decimal type |
| approximate numeric quantity | `number` under the declared precision contract | `number` |
| string-keyed object | `Readonly<Record<string, T>>` | explicit `ReadonlyMap<string, T>` conversion |
| array | `ReadonlyArray<T>` | validated element collection |
| timestamp string with offset | `string` | `Temporal.Instant` |
| date-only string | `string` | `Temporal.PlainDate` |
| time-only string, including fractional seconds | `string` | `Temporal.PlainTime` |
| declared zoneless date-time string | `string` | `Temporal.PlainDateTime` |
| declared duration string | `string` | `Temporal.Duration` through its declared codec |

- must apply [representation choices](../../../../../dev-cycle.md#representation-choices) to numeric contracts.
- must accept an integer as `number` only within `Number.isSafeInteger` limits when that representation is justified.
- must establish the endpoint's precision contract for decimals; `number` is not an exact decimal type.
- must parse exact numeric tokens before native JSON parsing can convert them to binary64.
- must not claim lossless `long` or `decimal` support through native `JSON.parse` or `Response.json`.
- must pair lossless JSON decoding with lossless request encoding.
- must use explicit exact-type arithmetic; native operators and `Math` do not dispatch to a custom numeric type.
- must state rounding and precision for division or other operations without a finite exact decimal result.
- must coordinate an exact-number wire change with the backend; a frontend cast cannot recover lost precision.
- must reject an unsupported numeric contract before relying on arithmetic or identity comparisons.
- must preserve external enum values; house enum values follow the backend contract.
- must define an unknown-value policy when decoding a closed enum: reject or model an explicit unknown case.

---

## Codecs

- must select a codec from the declared field or endpoint schema, never from a string's appearance.
- must decode date strings at integration; keep date-shaped text unchanged.
- must encode requests through the matching endpoint codec.
- must preserve fractional seconds and define accepted precision in round-trip fixtures.
- must declare the duration wire format; CLR `TimeSpan` default formatting is not ISO duration formatting.
- must convert a declared constant-format `TimeSpan` explicitly; do not silently assume an ISO converter exists.
- must reject calendar years/months when converting a `Temporal.Duration` into fixed elapsed `TimeSpan` units.
- must serialize a `Map` explicitly as the declared object/entry wire shape; plain `JSON.stringify` is insufficient.
- must keep field conversion in the codec and shape conversion in the mapper, without duplicated parsing.
- must format at the view using an explicit locale/timezone; never store display text as a timestamp.
- must follow [runtime compatibility](../../../../shapes/library/platform/compatibility.md) for Temporal support.

---

## Absence

- must distinguish an omitted property, explicit `null`, an empty value and a missing collection entry.
- must type an omitted property `field?: T`; use `T | null` only where the endpoint accepts or emits null.
- must not infer that omitted null object properties remove null array elements or dictionary values.
- must declare a write's clear operation explicitly; omission means unchanged only when the endpoint says so.
- must verify create/update/clear and collection-null fixtures against the backend.
- must take collection syntax from [TypeScript](../../../lla/constructs/typescript/typescript.md).

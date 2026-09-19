# Serialization

*Last updated: 2026-09-10*

> The API JSON contract; stored documents have a separate versioned contract.

## Contract

- must serialize property names and dictionary keys as camelCase.
- must serialize enum values as camelCase strings; numeric enum input and ordinal output are not the wire contract.
- must reject values without a declared wire name rather than serialize an integer ordinal.
- must omit null properties on write with `WhenWritingNull`.
- must serialize `Guid` as a string and `bool` as a boolean.
- must serialize `decimal`, `int` and `long` as JSON numbers.
- must serialize `DateTimeOffset`, `DateOnly` and `TimeOnly` using the framework's ISO date/time formats.
- must serialize `TimeSpan` as an ISO-8601 duration, such as `P2DT1S`.
- must provide that duration converter in the SDK preset; the built-in constant format `2.00:00:01` is not ISO-8601.
- must align frontend consumers with [type mapping](../../../../../../frontend/core/mla/domains/api/type-mapping.md).

---

## Wiring

- must register controller JSON through `AddControllersWithSdkJson()` at the host.
- must not treat `AddJsonStringEnums()` alone as installing the complete SDK preset.
- must use `JsonStringEnumConverter(JsonNamingPolicy.CamelCase, allowIntegerValues: false)` in the SDK preset.
- must not hand-roll options per controller or override casing, enum or null policy per endpoint.
- must follow the independent [stored JSON contract](../../../../core/mla/domains/persistence/stored-json.md)
  for persisted documents; never reuse wire options as the persistence contract.
- must keep relational enum storage separate; its owner is [Postgres](../../../../core/mla/domains/persistence/database/postgres/postgres.md).

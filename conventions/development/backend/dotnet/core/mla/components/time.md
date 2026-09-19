# Time

*Last updated: 2026-09-10*

> Applying the [clock seam](../constructs/behavior/time.md) to timestamps, durations and schedules.

## Location

- must use the construct's [location](../constructs/behavior/time.md#location).

---

## Declaration

- must use the construct's [declaration](../constructs/behavior/time.md#declaration).

---

## Content

- must inject `TimeProvider` for wall-clock reads and timers.
- must inject NodaTime `IClock` for instant and zoned-date arithmetic.
- must not read `DateTime.Now`, `DateTime.UtcNow`, `DateTimeOffset.Now` or `DateTimeOffset.UtcNow` in production code.
- must resolve cross-platform zone identifiers through `TimeZoneMapper`.
- must parse schedules through an `ICronExpressionParser` instance.
- must pass an injected instant and an explicit zone when calculating a cron occurrence.

```csharp
var next = parser.NextOccurrence(
    "0 0 8 * * *",
    timeProvider.GetUtcNow(),
    TimeZoneMapper.ResolveTimeZone("Asia/Tashkent"));
```

---

## Registration

- must register the clock seams at composition through `AddTimeProviders()`.
- must derive the default `IClock` from the registered `TimeProvider`.
- must register an independent `IClock` explicitly only when the two clocks intentionally differ.
- must replace both registrations when a test host owns the clock.
- registration surface → [time registration](../../../../../../../workbench/wow-two-sdk-beta/wow-two-sdk.backend.beta/engineering/codebase/wow-two-back-beta-sdk/src/Foundation/Time/TimeServiceCollectionExtensions.cs).

---

## Tests

- must use `FakeTimeProvider` for deterministic BCL clock tests.
- must adapt NodaTime `IClock` to that same fake clock.
- must advance the one fake clock when a flow reads both abstractions.

---

## Parsing

- must handle invalid zone ids and cron expressions at the input boundary.
- must not assume every zone id is available on every machine; zone data remains an OS dependency.
- API and exceptions → [zone mapper](../../../../../../../workbench/wow-two-sdk-beta/wow-two-sdk.backend.beta/engineering/codebase/wow-two-back-beta-sdk/src/Foundation/Time/TimeZoneMapper.cs)
  and [cron parser](../../../../../../../workbench/wow-two-sdk-beta/wow-two-sdk.backend.beta/engineering/codebase/wow-two-back-beta-sdk/src/Foundation/Time/ICronExpressionParser.cs).

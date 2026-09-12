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
- must register an intended `IClock` replacement explicitly; supplying a `TimeProvider` does not adapt it to NodaTime.
- must account for registration precedence: the default overload uses `TryAddSingleton` for both clocks;
  the instance overload adds the supplied `TimeProvider` and uses `TryAddSingleton` for `IClock`.
- registration surface → [time registration](../../../../../../../workbench/wow-two-sdk-beta/wow-two-sdk.backend.beta/engineering/codebase/wow-two-back-beta-sdk/src/Foundation/Time/TimeServiceCollectionExtensions.cs).

---

## Tests

- must use `FakeTimeProvider` for deterministic BCL clock tests.
- must also register a controlled NodaTime `IClock` when the tested path reads it.
- must advance both controlled clocks coherently when a flow reads both abstractions.
- must not assume the test host's `TimeProvider` replacement changes `IClock`.

---

## Parsing

- must handle invalid zone ids and cron expressions at the input boundary.
- must not assume every zone id is available on every machine; zone data remains an OS dependency.
- API and exceptions → [zone mapper](../../../../../../../workbench/wow-two-sdk-beta/wow-two-sdk.backend.beta/engineering/codebase/wow-two-back-beta-sdk/src/Foundation/Time/TimeZoneMapper.cs)
  and [cron parser](../../../../../../../workbench/wow-two-sdk-beta/wow-two-sdk.backend.beta/engineering/codebase/wow-two-back-beta-sdk/src/Foundation/Time/ICronExpressionParser.cs).

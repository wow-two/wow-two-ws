# Time

*Last updated: 2026-06-13*

Time is injected, never read from `static` ambient clocks — so handlers stay deterministic and tests control the clock.

## Rule

- **Never** call `DateTime.Now`, `DateTime.UtcNow`, `DateTimeOffset.Now`, or `DateTimeOffset.UtcNow` in production code.
- Inject **`TimeProvider`** (the BCL abstraction) for wall-clock reads — `provider.GetUtcNow()`, `provider.GetLocalNow()`, timers.
- Inject NodaTime **`IClock`** when you need instants / zoned arithmetic (`clock.GetCurrentInstant()`, `ZonedDateTime` math) — its type system makes UTC-vs-local mistakes unrepresentable.
- Both are registered together; pick per use-site. `TimeProvider` for the common "what time is it" read; `IClock` for date math, durations, zone-aware scheduling.

## Registration

`AddTimeProviders()` ([`TimeServiceCollectionExtensions.cs`](../../../../workbench/wow-two-sdk-beta/wow-two-sdk.backend.beta/src/Foundation/Time/TimeServiceCollectionExtensions.cs)) registers both abstractions in the composition root:

```csharp
builder.Services.AddTimeProviders();
// → TryAddSingleton(TimeProvider.System)
// → TryAddSingleton<IClock>(SystemClock.Instance)
```

Both use `TryAdd` — call it once at boot; a prior registration wins.

## Tests

Pass `FakeTimeProvider` (from `Microsoft.Extensions.TimeProvider.Testing`) so tests advance the clock deterministically. Two paths:

| Path | How | Notes |
|---|---|---|
| DI overload | `services.AddTimeProviders(fake)` — `AddTimeProviders(IServiceCollection, TimeProvider)` | Registers your `TimeProvider`; **but still pins `IClock` to `SystemClock.Instance`** (see drift) |
| Test host | `WebApiTestHost<T>.Clock` (a `FakeTimeProvider`) swaps `TimeProvider` via `RemoveAll<TimeProvider>()` + `AddSingleton` | Default in the testing scaffold; `WebApiTestBase<T>.Clock` exposes it |

```csharp
var fake = new FakeTimeProvider();
fake.SetUtcNow(DateTimeOffset.Parse("2026-06-13T00:00:00Z"));
// drive the system under test, then:
fake.Advance(TimeSpan.FromHours(2));
```

> **Drift — `IClock` is not faked.** Both `AddTimeProviders` overloads hardcode `TryAddSingleton<IClock>(SystemClock.Instance)` ([`TimeServiceCollectionExtensions.cs:19,33`](../../../../workbench/wow-two-sdk-beta/wow-two-sdk.backend.beta/src/Foundation/Time/TimeServiceCollectionExtensions.cs)). Code under test that reads `IClock` will hit the real system clock even when a `FakeTimeProvider` is registered. For deterministic NodaTime tests, register a `FakeClock` yourself after `AddTimeProviders`.

## Time zones

Resolve every zone through **`TimeZoneHelpers.ResolveTimeZone(string anyZoneId)`** ([`TimeZoneHelpers.cs`](../../../../workbench/wow-two-sdk-beta/wow-two-sdk.backend.beta/src/Foundation/Time/TimeZoneHelpers.cs)) — never `TimeZoneInfo.FindSystemTimeZoneById` directly. It wraps `TimeZoneConverter`, so the **same id works on any host OS** (Windows id `"Eastern Standard Time"` *or* IANA id `"America/New_York"`):

```csharp
var tz = TimeZoneHelpers.ResolveTimeZone("America/New_York");   // works on Windows
var tz2 = TimeZoneHelpers.ResolveTimeZone("Eastern Standard Time"); // works on Linux
```

- Throws `TimeZoneNotFoundException` on an unknown id.
- Cross-convert ids explicitly with `TimeZoneHelpers.IanaToWindows(string)` / `TimeZoneHelpers.WindowsToIana(string)`.

## Cron

Parse cron through **`CronExpressionParser.Parse(string)`** ([`CronExpressionParser.cs`](../../../../workbench/wow-two-sdk-beta/wow-two-sdk.backend.beta/src/Foundation/Time/CronExpressionParser.cs)) — a thin wrapper over `Cronos.CronExpression`. It auto-detects 5-field (standard) vs 6-field (with-seconds) forms; throws `Cronos.CronFormatException` on a bad expression.

```csharp
var expr = CronExpressionParser.Parse("*/15 * * * *");           // CronExpression
var next = CronExpressionParser.NextOccurrence(                  // DateTimeOffset?
    "0 0 8 * * *",
    timeProvider.GetUtcNow(),
    TimeZoneHelpers.ResolveTimeZone("Asia/Tashkent"));
```

`CronExpressionParser.NextOccurrence(string expression, DateTimeOffset from, TimeZoneInfo zone)` parses, then delegates to `CronExpression.GetNextOccurrence(from, zone)` — feed it a zone from `TimeZoneHelpers.ResolveTimeZone`, and an instant from the injected `TimeProvider`.

## See also

- [result-pattern.md](./result-pattern.md) — foundation sibling
- [Time/README.md](../../../../workbench/wow-two-sdk-beta/wow-two-sdk.backend.beta/src/Foundation/Time/README.md) — package quickstart
- [NodaTime](https://nodatime.org/) · [TimeZoneConverter](https://github.com/mattjohnsonpint/TimeZoneConverter) · [Cronos](https://github.com/HangfireIO/Cronos)

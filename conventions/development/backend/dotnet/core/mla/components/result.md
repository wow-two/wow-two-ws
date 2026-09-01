# Result

*Last updated: 2026-08-24*

> The value an operation hands back when it can fail.
> Purpose — a failure travels as a value the caller must read, so no path forgets to handle it.
> Use case — any operation with a failure mode; one that cannot fail by construction returns bare.

> Defined at [result — the construct](../constructs/data/result.md); this doc carries every condition for using one.

## Reaching for one

- must return a `Result` when the operation has a failure mode a caller can act on.
- must return the value bare when the operation cannot fail by construction — a `Result` that is always
  `Success` teaches every caller to skip the check.
- must keep configuration-at-boot and programmer errors as exceptions, because the host's own seams catch
  only what is thrown → *Bridging back to a throw* below.
- must not return `Result` from a framework hook the runtime calls — a `DelegatingHandler`, a consume
  filter, an `IHostedService`. Those seams read exceptions and nothing else.

---

## Choosing the shape

| Shape | When |
|---|---|
| `Result` | the operation succeeds or fails and carries no value back |
| `Result<T>` | success carries a value, and `T` is non-nullable |
| a bare value | no failure mode exists |

- must not reach for `Result<T>` when success can legitimately carry nothing — `T : notnull` rejects it, and
  the absence is either a failure or a separate case the caller asks about.
- must model "nothing found" as a `NotFound` failure when the caller cannot proceed without the value.

---

## Carrying the failure

- must author the error through the catalogue — `AppErrorFactory.{Kind}(...)`, never a hand-built `AppError`.
- must pick the kind by what the caller does next, never by where the failure arose:
  - `Validation` — the input was wrong and the caller can correct it
  - `NotFound` — the thing is absent and the caller must stop or create it
  - `DataIntegrity` — stored state contradicts an invariant
  - `ExternalUnavailable` — an outside system answered, unusably
  - `SerializationFailed` — a payload could not be read
- must attach the offending values as `Metadata` when a caller or an operator needs them named.
- must not put the failure's kind in the message text — the kind is the field.

---

## Consuming one

- must collapse with `.Match(onSuccess, onFailure)` when both branches produce the same shape.
- must guard with `.IsFailure(out var error, out var value)` when the failure propagates upward — it reads as
  the guard clause the call site wants, and no cast is needed at each hop.
- must not unwrap by pattern-matching the union in application code; the two above are the whole surface.
- must not swallow a failure — a caller that ignores the error acknowledges work that never happened.

---

## Bridging back to a throw

A failure is expressible either way over the same `AppError` → [results](../../../shapes/service/platform/responses/results.md) § *Throw and return bridge*.

- must convert at the boundary where the host reads only exceptions — `.ValueOrThrow()` · `.ThrowIfFailure()`.
- must place the conversion in the type that knows the host, never in the operation that produced the failure.
- must keep the boundary's own exception type when one exists, so the reason it reports stays specific.
- must not convert twice — one bridge per boundary, or the stack carries a wrapper per layer.

---

## Neighbours

- [result — the construct](../constructs/data/result.md) — what it is and how it is declared
- [results](../../../shapes/service/platform/responses/results.md) — the throw-and-return bridge, typed failure
- [problem-details](../../../shapes/service/platform/responses/problem-details.md) — how a failure reaches HTTP

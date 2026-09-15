# Exceptions

*Last updated: 2026-08-18*

> Where a throw is still the honest mechanism in a codebase whose default outcome contract is `Result` / `AppResult`.
> Purpose — the result pattern owns expected failure, so each exception that remains needs a reason to exist.
> Use case — research feeding a later convention; the contract itself is
> [results](../conventions/development/backend/dotnet/mla/platform/responses/results.md).

Citation roots, elided from every path below:

- `SDK` = `workbench/wow-two-sdk-beta/wow-two-sdk.backend.beta/engineering/codebase/wow-two-back-beta-sdk/src/`
- `QR` = `workbench/ventures/10x-venture-forever-pin/engineering/codebase/forever-pin.backend-services/`

---

## Verdict

- Throw when the caller is a **programmer** or the process cannot continue; return a `Result` when the caller
  is a **user**.
- The SDK already obeys that line — 767 of its 935 throw sites are argument guards, 19 throw a custom type.
- Biggest inconsistency: **11 of 11** forever-pin handlers wrap their whole body in `catch (Exception ex)` and
  return `AppError.Of(Unexpected, ex.Message)` — putting the raw exception message on the wire.
- Root cause is not the handlers: `AddMediatorExceptionToResultBehavior` has **zero call sites**, so the net
  `results.md` promises ("the mediator never throws") is wired in no product.
- All 5 bridges named in `results.md` have **zero** non-test call sites. `error.ToException()`, which the doc
  never names, is the only one carrying traffic.

---

## What ships

Ten custom exception types, all in the SDK. forever-pin declares **none** — grep for `class .*Exception` across
`QR` returns nothing.

| Exception type | Where | What it signals | Verdict |
|---|---|---|---|
| `AppException` | `AppException.cs:4` | the thrown form of an `AppError` | keep |
| `ValidationException` | `ValidationException.cs:6` | field errors, outside the mediator | keep |
| `MasterKeyFormatException` | `MasterKeyFormatException.cs:5` | master key configured but malformed | keep |
| `MigrationDriftException` | `MigrationDriftException.cs:4` | an applied migration's checksum moved | keep |
| `MigrationOrphanException` | `MigrationOrphanException.cs:6` | history holds migrations absent from source | keep |
| `SagaConcurrencyException` | `SagaContracts.cs:131` | a saga write lost a concurrency race | keep |
| `ClaimCheckPayloadException` | `ClaimCheck.cs:155` | offloaded body unreadable; dead-letters | keep |
| `RequestTimeoutException` | `RequestClient.cs:101` | no response within the timeout | keep |
| `RequestFaultException` | `RequestClient.cs:126` | response is not the expected contract | keep |
| `WebhookAddressBlockedException` | `WebhookSsrfGuard.cs:7` | target resolves to a blocked address | keep |

Homes the basename does not give: `Foundation/Errors/` · `Foundation/Validation/` · `Foundation/Security/` ·
`Data/Migrations/Bespoke/` · `Messaging/Saga/` · `Messaging/Transport/` · `Messaging/Webhooks/`.

### Throw sites, by kind

935 non-test throw sites in the SDK — 168 `throw` statements plus 767 `ThrowIf*` guard calls.

- 767 argument guards — `ArgumentNullException.ThrowIfNull` (627), `ThrowIfNullOrWhiteSpace` (123), the rest
  ordinal and length guards. Programmer error, every one. Keep.
- 51 `throw new InvalidOperationException` — misconfiguration and API misuse, e.g. a non-open-generic behavior
  at `MediatorServiceCollectionExtensions.cs:65`, a request not implementing `IRequest<>` at `Mediator.cs:52`.
- 18 `ArgumentException`, 8 `ArgumentOutOfRangeException`, 5 `InvalidCastException`, 3 `NotSupportedException`
  — same bucket. Keep.
- 19 custom-type throws — 14 `throw new`, plus 5 via `SagaConcurrencyException.For(...)`. Keep.
- The remaining `throw` statements are bare rethrows and `throw error.ToException()`.

### Fold to result

Three catch sites turn malformed input into a plausible success, so no caller can tell bad data from no data.

- `Media/Captions/TtmlCaptionParser.cs:29` — `catch (XmlException)` returns `[]`; broken TTML reads as
  "no captions".
- `Media/Captions/Json3CaptionParser.cs:28` — `catch (JsonException)` returns `[]`; same failure mode.
- `Media/Captions/CaptionTimecode.cs:32,36` — `FormatException` / `OverflowException` return `TimeSpan.Zero`,
  so a broken timecode silently becomes `00:00`.

`AppErrorType.SerializationFailed` already exists for exactly this, so the carrier is available.

### forever-pin

- 11 of 11 handlers open with `try` and close with `catch (Exception ex)` — `CodeCreateCommandHandler.cs:79`,
  `CodeGetByIdQueryHandler.cs:34`, `BillingCheckoutCommandHandler.cs:41`, and 8 more.
- Each returns `AppError.Of(AppErrorType.Unexpected, ex.Message)`. `AppErrorProblemDetailsFactory.cs:40` sets
  `Detail` from `IErrorMessageResolver`, whose default passes through to `AppError.Message`
  (`IErrorMessageResolver.cs:22`) — so the raw message reaches the client, against `problem-details.md`.
- The blanket catch also preempts `DbExceptionMappingRule.cs:9`: a Postgres `23505` that would map to
  `Conflict` (409) is reported as `Unexpected` (500).
- 18 `AppError.Of(...)` call sites and **0** uses of the `AppErrors` catalog, against the rule in `results.md`.

### Correct catch discipline already in the tree

- `ClaimCheck.cs:469` — `catch (Exception exception) when (exception is not (ClaimCheckPayloadException or
  OperationCanceledException))` rewraps foreign faults, preserving its own type and cancellation.
- `MessagePump.cs:159` — bare `catch` does its in-flight cleanup, then `throw;`.
- `SagaCoordinator.cs:78` — catches `SagaConcurrencyException` to drive a bounded retry, rethrowing once spent.
- `QR .../Analytics/ScanFlushBackgroundService.cs:40,44` — `OperationCanceledException` breaks the loop,
  everything else logs and continues, so one bad batch cannot kill the service.
- `MessagingMetrics.cs:242` — the one deliberate silent swallow, with a comment: a faulted probe must not take
  down collection for the whole meter.

---

## The boundary

- **Precondition violated on our own API** → **throw**. The caller is a developer, and a `Result` would ask a
  user to handle a bug. This is 82% of the SDK's throw sites and needs no change.
- **A third-party library that only throws** → **catch at the seam, return a `Result`**. The seam is
  `IExceptionMappingRule`; `DbExceptionMappingRule.cs:9` is the shipped example, Npgsql `23505` → `Conflict`.
- **Cancellation** → **neither** — let `OperationCanceledException` reach the single converter.
  `ExceptionToResultBehavior.cs:26,30` maps it to `Canceled` or `OperationTimeout`; a local catch loses that.
- **Unrecoverable startup failure** → **throw and let the host die**. `MigrationOrphanException` and
  `MasterKeyFormatException` are correct: there is no caller to hand a `Result` to.
- **Validation failure** → **return** a `ValidationError`. Throw `ValidationException` only outside the
  mediator, where `ValidationExceptionHandler.cs:10` (minimal APIs) or `ValidationExceptionFilter.cs:11` (MVC)
  is the path to a 400.
- **Not-found** → **return** `AppErrors.NotFound(...)`. Never an exception: it is the routine answer to a
  routine question.
- **Conflict** → **return** `AppErrors.Conflict(...)`. One literal exception: a saga write throws
  `SagaConcurrencyException` because the layer catches it itself at `SagaCoordinator.cs:78` to retry.

An exception whose catch site sits inside the same layer as its throw is control flow, not a failure report —
that is what makes the saga case legitimate and a handler-level `catch (Exception)` not.

The dividing question is not "is this bad" but **who reads the outcome**. A developer reading a stack trace
wants a throw; a caller that must branch wants a value. Everything else follows.

---

## Bridges

All five helpers named in `results.md` exist. All five are unused outside tests.

| Helper | Declared at | Direction | Non-test call sites |
|---|---|---|---|
| `error.Throw()` | `AppError.cs:77` | return → throw | 0 |
| `result.ValueOrThrow()` | `ResultExtensions.cs:11` | return → throw | 0 |
| `result.ThrowIfFailure()` | `ResultExtensions.cs:25` | return → throw | 0 |
| `(() => op()).Attempt()` | `AttemptExtensions.cs:11` | throw → return | 0 |
| `ExceptionToResultBehavior` | `ExceptionToResultBehavior.cs:13` | throw → return | registration never called |
| `error.ToException()` | `AppError.cs:70` | return → throw | 5 — the only live bridge |

- `AttemptAsync()` (`AttemptExtensions.cs:36`) is the async twin of `Attempt`, also unused.
- `ToException()`'s live sites: `AuthorizationBehavior.cs:38,46`, `ExceptionToResultBehavior.cs:51`,
  `ResultExtensions.cs:18,31`.

**Which direction each is correct for.**

- **throw → return** should dominate. `Attempt` / `AttemptAsync` is right at a seam wrapping a throw-only
  dependency: both catch `OperationCanceledException` to `Canceled` and unwrap `AppException` before falling
  back to `Unexpected` (`AttemptExtensions.cs:19-30`). `ExceptionToResultBehavior` is that same conversion
  applied once, centrally, for every handler — which is why 11 hand-rolled copies exist in forever-pin.
- **return → throw** is correct only where the frame above cannot carry a value: a constructor, a field
  initializer, a `Main`, an interface the framework owns. `AuthorizationBehavior.cs:38` is the honest use — a
  behavior whose `TResponse` is not known to be an `AppResult` has no value to return, so it throws.
- `ValueOrThrow` / `ThrowIfFailure` on a `Result` inside a handler is the anti-use: it discards a value the
  caller could have branched on, and hands the mediator an exception to convert straight back.
- `error.Throw()` and `error.ToException()` are one bridge, one composable and one not. `ToException()` won on
  usage because it composes into `throw ... .ToException()` at a `switch` arm or an expression body.

---

## Custom exceptions

Ten shipped types split into two shapes, and the split is not principled.

**Data-carrying, primary constructor, message baked in** — the better shape:

- `MigrationDriftException.cs:4` carries `IReadOnlyList<string> Drifted`, and its message names the repair.
- `MigrationOrphanException.cs:6` carries `IReadOnlyList<int> OrphanedOrdinals` and names the override option.
- `WebhookSsrfGuard.cs:7` carries `string Host`, and is `internal` because nothing outside catches it.

**Three BCL ceremony constructors, carrying nothing**:

- `SagaConcurrencyException`, `ClaimCheckPayloadException`, `RequestTimeoutException`, `RequestFaultException`
  each declare `()`, `(string)`, `(string, Exception)` and add no members.
- Only `SagaConcurrencyException` has a real factory — `SagaContracts.cs:162`, `For(correlationId,
  expectedVersion)` — and that is what every throw site uses (`InMemorySagaRepository.cs:62,76,84,98,101`).

**Base type.** `AppException` when the failure must reach the wire as a specific status — it carries an
`AppError`, and `ExceptionMapping.cs:41` unwraps it before consulting any rule, so the status is already
decided. Plain `Exception` for faults below the HTTP boundary, where a status is meaningless.

**Sealed.** Nine of ten are `sealed`. `AppException.cs:4` is deliberately open, and its own summary gives the
reason — "subclass only to carry members a catch site reads". `ValidationException` is the only subclass, and
it earns that by exposing a typed `ValidationError` the handler reads.

**The gap.** Only one `IExceptionMappingRule` ships (`DbExceptionMappingRule.cs:9`). None of the four messaging
types has a rule, so any that escapes into a request path maps to `Unexpected`/500 — `RequestTimeoutException`
would render 500 rather than the 504 `OperationTimeout` already exists for.

---

## Proposed rules

- must throw for a violated precondition on our own API, using a `ThrowIf*` guard rather than a hand-rolled `if`.
- must return a `Result` / `AppResult` for a failure the caller branches on — not-found, conflict, validation.
- must not throw to report a not-found, a conflict, or a validation failure across a boundary.
- must let `OperationCanceledException` reach the single converter, never catching it to translate it locally.
- must throw and let the host fail on an unrecoverable startup fault, rather than degrade into a wrong process.
- must convert a throw-only dependency to a `Result` at the seam that owns it, via `IExceptionMappingRule` or `Attempt`.
- must not wrap a handler body in `catch (Exception)` — register `AddMediatorExceptionToResultBehavior` once instead.
- must not put an exception message into `AppError.Message`; it reaches the client as ProblemDetails `detail`.
- must author every error through the `AppErrors` catalog or an app catalog, never `AppError.Of(...)` inline.
- must rethrow with a bare `throw;` after cleanup, and must not `throw ex;`.
- must exclude the exception's own type and `OperationCanceledException` from a rewrapping `when` filter.
- must log or map a caught exception; a silent swallow needs a comment naming what it protects.
- must not return an empty or default value for malformed input — return a `Result` carrying `SerializationFailed`.
- may catch an exception as control flow when the catch site sits in the same layer as the throw.
- must seal a custom exception unless it documents a subclass point, as `AppException` does.
- must make a custom exception carry the structured data a catch site reads, not only a message string.
- must give a custom exception a mapping rule when it can reach a request path, or it renders 500.
- must name a custom exception `{Subject}{Problem}Exception`, and declare it `internal` when nothing outside catches it.

---

## Open

1. Should `AddApiDefaults` auto-wire `AddMediatorExceptionToResultBehavior`, or does it stay opt-in? Auto-wiring
   deletes 11 catch blocks in forever-pin; opt-in keeps the mediator's behavior order explicit.
2. Delete the four unused bridges, or keep them as consumer-facing API? They are tested but uncalled, and a
   convention naming five helpers nobody uses will not be believed.
3. Do the messaging exceptions need SDK mapping rules, or is `Messaging/` guaranteed out-of-request? The answer
   decides whether `RequestTimeoutException` can ever render a 504.
4. Is silent-empty the intended contract for `Media/Captions/`, or should the parsers return a `Result`?
   Changing it breaks whatever consumes them.
5. Does `AppException`'s open subclass point still earn itself with exactly one subclass, or should it seal and
   let `ValidationError` be read off `AppException.Error`?

# Result

*Last updated: 2026-09-10*

> Choosing and consuming the [result construct](../constructs/data/result.md) for recoverable failure.

## Location

- must use the construct's [location](../constructs/data/result.md#location).

---

## Declaration

- must use the construct's [declaration](../constructs/data/result.md#declaration).

---

## Content

### Failure

- must return a result when an operation has a failure mode its caller can act on.
- must return a bare value when the operation cannot fail by construction.
- must keep programmer errors and configuration-at-startup failures as exceptions.
- must preserve a framework callback's declared return type; bridge failures where its runtime reads exceptions.
- may use a `TryX` / `bool` contract when absence or rejection needs no structured error.
- may pair that contract with an explicit throwing operation, such as `Parse` / `TryParse`.
- must preserve the declared `Validate` / `ValidateAndThrow` bridge in the validation contract.
- must not infer an exemption from a role suffix; these rules also apply to mappers and extensions.

### Carrier

- must use `Result` for success without a value and failure with an `AppError`.
- must use `Result<T>` for a non-null success value and failure with an `AppError`.
- must use `Result<TSuccess, TFailure>` when callers branch on distinct typed failures.
- must use a closed failure vocabulary for typed failures; handle every declared case.
- must not assume an enum or class hierarchy alone makes every possible runtime value exhaustively checked.
- must map a typed failure to the receiving boundary's error catalogue when crossing that boundary.
- must model absence explicitly when a successful operation can legitimately return no value.
- must use `NotFound` when absence prevents the caller from proceeding.
- handler/controller carrier choice → [service results](../../../shapes/service/platform/responses/results.md).

### Error

- must author errors through the SDK or owning domain's catalogue, never construct an `AppError` at a call site.
- must choose the failure kind by the caller's recovery, not by the layer that detected it.
- must keep HTTP status out of domain errors; the delivery boundary maps it.
- must not subclass `AppError` merely to model a closed set of typed failure alternatives.
- must attach useful diagnostic values as metadata without exposing secrets.
- must not repeat the kind in the message text.

### Consumption

- must use `.Match(onSuccess, onFailure)` when both branches produce one shape.
- may propagate `Result<T>` through `.IsFailure(out var error, out var value)` when a guard is clearer.
- must branch on the typed failure inside its failure arm when choosing recovery by case.
- must not silently discard failure or unwrap through casts in application code.

---

## Boundary bridge

- must convert to an exception only where the receiving framework requires one.
- must keep the bridge in the type that knows that framework, not in the operation producing the result.
- must preserve the boundary's exception type and original cause when one exists.
- must use one bridge per boundary.
- may use `.ValueOrThrow()` or `.ThrowIfFailure()` for the SDK's `AppException` bridge.
- must not promise every throw becomes a result: pre-dispatch, programmer-error and incompatible-response paths may throw.

- carrier API → [results](../../../../../../../workbench/wow-two-sdk-beta/wow-two-sdk.backend.beta/engineering/codebase/wow-two-back-beta-sdk/src/Foundation/Results/Result.cs).
- bridge API → [result extensions](../../../../../../../workbench/wow-two-sdk-beta/wow-two-sdk.backend.beta/engineering/codebase/wow-two-back-beta-sdk/src/Foundation/Results/ResultExtensions.cs).

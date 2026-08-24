# Results

*Last updated: 2026-08-20*

> The carrier every fallible operation returns — a typed success or a typed failure, never both, never a throw.
> Purpose — a caller branches on the type instead of wrapping the call, so one missed `try` cannot take a tree down.
> Use case — a browser seam, an API call, a validator, a mapper, a client factory.

## The carrier

```typescript
type Result<TSuccess = void, TFailure = AppError> =
  | { readonly ok: true; readonly value: TSuccess }
  | { readonly ok: false; readonly failure: TFailure };
```

| Spelling | Success | Failure |
|---|---|---|
| `Result` | no value | `AppError` |
| `Result<T>` | a `T` | `AppError` |
| `Result<T, AppError>` | a `T` | `AppError` — the explicit spelling of `Result<T>` |
| `Result<T, TFailure>` | a `T` | a closed type the caller switches on |

- must return a `Result` from any operation whose failure a caller may branch on.
- must return a `Result` from a validator and from a mapper — an invalid format, a missing field or a shape
  that does not match is a failure the caller reads, never a throw that reaches the render tree.
- which failure type to reach for is application ([data](../../components/data/data.md)).
- must not throw from an operation that returns a `Result` — the two together give a caller nothing single to read.
- must let a programmer error throw — a failed invariant is a bug, and a `Result` would ask a caller to handle it.

---

## `AppError`

The default failure, and the only one an operation needs until a caller has to tell cases apart.

```typescript
interface AppError {
  readonly type: AppErrorType;
  readonly message: string;
  readonly metadata?: Readonly<Record<string, unknown>>;
}
```

- must declare `AppErrorType` as a value set ([enums](../../../lla/components/enums.md)).
- must author an error through a catalog — SDK `AppErrorFactory.{Kind}(…)`, app `CodeErrors.*`.
- must not build an `AppError` literal at a call site.
- must not carry an HTTP status — `AppErrorType` is transport-agnostic and the status maps at the edge.
- must write `message` for the reader who sees it, since a toast renders it unedited.

---

## Typed failure

`AppError` carries a type and metadata. A caller that must branch on **distinct cases** needs the case in the type.

```typescript
export const ClipboardFailureCode = {
  Denied: 'Denied',
  Unsupported: 'Unsupported',
  InsecureContext: 'InsecureContext',
} as const;

interface ClipboardFailure {
  readonly code: ClipboardFailureCode;
  readonly message: string;
}
```

- must name a failure `{Noun}Failure`, and its vocabulary `{Noun}FailureCode`.
- must keep the failure type closed, so the caller's `switch` is checked.
- must not extend `AppError` to add cases — extension does not let a caller switch exhaustively.
- must use `AppError` where the caller only reports the failure or maps it to a status.

---

## Extensions

`ResultExtensions` is the one place the carrier is built and read ([extensions](../../../lla/components/extensions.md)).

| Member | Does |
|---|---|
| `ok(value)` · `fail(failure)` | constructs each branch |
| `isOk(result)` · `isFail(result)` | narrows, as a type predicate |
| `map(result, fn)` · `mapFailure(result, fn)` | transforms one branch, passing the other through |
| `match(result, { ok, fail })` | collapses both branches to one value |
| `unwrapOr(result, fallback)` | reads the success, or the fallback |
| `fromThrowing(fn, toFailure)` | wraps a throwing third party at the seam |

- must narrow through `isOk` / `isFail`, never by reading `.value` behind a truthiness check.
- must wrap a throwing dependency once, at the seam, with `fromThrowing` — never at each call site.
- must not add a member that hides a branch; `unwrapOr` is the only reader that drops a failure silently.

---

## File + name

- must give a result type its own file in the `models/` role-group of the slice that returns it
  ([models](models.md) § *File + name*).
- must name a per-operation alias `{Noun}{Verb}Result` — `CodeCreateResult`.
- must not declare an alias where the bare carrier reads the same.

---

## Neighbours

- [models](models.md) — the shapes a result carries
- [data](../../domains/data/state-and-data.md) — how an API failure reaches a component
- [extensions](../../../lla/components/extensions.md) — the `*Extensions` object form

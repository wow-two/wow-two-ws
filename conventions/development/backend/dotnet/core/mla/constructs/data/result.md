# Results

*Last updated: 2026-09-10*

> The closed outcome carrier: one success case or one failure case, with values owned by their case.

## Location

### Folder
- must keep the shared carrier in its result domain; operation-specific data uses a [model](model.md).

### File
- file rules → [one type, one file](../../mla.md).

---

## Declaration

### Type doc

#### [Summary](../../../lla/notation/documentation/summary.md)
- type summary baseline → [data](data.md) § *Shared rules*.
- must name the kind of outcome carried.
- must not describe the success and failure arms separately — the union is the shape.

```csharp
// ✅ names the outcome
/// <summary>Represents the outcome of an operation that returns no value.</summary>
// ❌ narrates the arms, which the type already carries
/// <summary>Represents either a list of channels or an error.</summary>
```

### Construct
- must declare an `abstract record` with a private constructor and nested `sealed record` cases.
- must use that closed root instead of the sealed-carrier default in
  [language constructs](../../../lla/constructs/constructs.md) § *Data components*.
- must give success and failure their own non-null payloads; neither case carries the other's value.
- must declare case payloads as body properties with `{ get; init; }`.
- must constrain a generic payload with `notnull`.

```csharp
// ✅
public abstract record Result
{
    private Result() { }
    public sealed record Success : Result;
    public sealed record Failure : Result
    {
        public required AppError Error { get; init; }
    }
}
```

### Type name
- must use the shared `Result`, `Result<T>`, `Result<TSuccess, TFailure>` or `AppResult<TSuccess>` carrier.
- must not declare a per-operation carrier such as `ChannelGetAllResult`; name its success payload as a model.

---

## Content

- carrier selection, failure modes and consumption → [results](../../components/result.md).
- handler/controller context → [service results](../../../../shapes/service/platform/responses/results.md).

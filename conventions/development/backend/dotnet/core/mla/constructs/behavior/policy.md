# Policies

*Last updated: 2026-09-10*

> A type that decides whether, when, or how often another operation runs, never running it.
> Purpose — the decision is the swappable part, so it is named apart from the work it governs.
> Use case — retry, backoff, propagation, eviction; anything answering "should this, and how much".

## Location

### Folder
- must sit in a `Policies/` folder beside the operation it governs.

### File
- file rules → [one type, one file](../../mla.md).

---

## Declaration

### Type doc

#### [Summary](../../../lla/notation/documentation/summary.md)
- must start with **Decides**, and name what the decision governs.
- must not describe the operation itself — the policy does not perform it.

```csharp
// ✅ names the decision and what it governs
/// <summary>Decides whether a failed send is retried, and after how long.</summary>
// ❌ describes the work, which belongs to the type that does it
/// <summary>Retries the failed send.</summary>
```

### Construct
- declaration and injection → [behavior](behavior.md) § *Shared rules*.
- must expose the decision through an interface.

### Type name
- must suffix with `Policy` — `RetryPolicy`, `MessageHeaderPropagationPolicy`.
- must reach for `Mapper` instead when the answer is a value rather than a decision.
- must reach for `Service` instead when the type also performs the operation.
- must not suffix with `Strategy` — swappability is a shape, not a responsibility.

```csharp
// ✅
public sealed class ExponentialRetryPolicy : IRetryPolicy
// ❌ `Strategy` names the pattern, so the responsibility stays unsaid
public sealed class ExponentialRetryStrategy : IRetryStrategy
```

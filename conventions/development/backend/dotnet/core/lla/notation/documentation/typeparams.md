# Type params

*Last updated: 2026-08-16*

> The `<typeparam>` block — carried when a substitution can be got wrong, skipped when the name already says it.

## Scope [REQUIRED]

A `<typeparam>` says what may be substituted and the role it plays here. A conventional name already says that,
so documenting it restates the name — the Redundant comment anti-pattern
([documentation](documentation.md) § *Comment anti-patterns*).

- must skip `<typeparam>` when every parameter is conventional — `T`, `TKey`, `TValue`, `TResult`, `TRequest`, `TResponse`.
- must document a **domain-meaningful** parameter — `TAggregate`, `TUserId`: name its role in this type.
- must not restate the `where` clause — the signature carries it, and a copy goes stale when it moves.
- must document **every** parameter once any one is documented ([params](params.md) § *Every parameter, every time*).
  - a partial set leaves a reader unable to tell an omission from a decision.
- must include a conventional parameter in that complete set when a domain-meaningful sibling needs documentation.

```csharp
// ✅ the role it plays, not the constraint
/// <typeparam name="TId">The key an entity is addressed by.</typeparam>
public interface IKeyedEntity<out TId> : IEntity;

// ❌ restates the name, then the where clause
/// <typeparam name="TKey">The type of the key.</typeparam>
```

---

## Neighbours

- [params](params.md) — the sibling rule for method parameters
- [summary](summary.md) — `<typeparamref>` inside a summary

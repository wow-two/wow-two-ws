# Storage

*Last updated: 2026-09-10*

> The synchronous client-side persistence seam every hook, store and draft writes through.
> Purpose — a tree swaps its backing store without a single caller changing, and a failure is never a throw.
> Use case — persisting a preference, isolating a feature's keys, or migrating a shape a user carried over.

## The contract

- must expose exactly read, write and remove, all synchronous, with JSON as the wire format.
- must degrade every failure to a miss — a quota, serialization or parse error never reaches the caller.
- must return null from a read that is absent, malformed or blocked.
- must resolve the backing store per call, so an unavailable store is a no-op rather than an import-time crash.
- must stay domain-agnostic — a key's meaning belongs to the caller, never to the seam.
- must let a decorator compose over any implementation by rewriting calls, never by widening the contract.
- must prefix keys with a namespace when two features or two tenants could collide on a bare key.
- must stamp a persisted value with a schema version, and walk migrations up on read.
- must degrade unrecoverable state — a missing migration, a future version, a broken read — to the declared initial.
- must not carry anything asynchronous or large; that is a different capability with a different seam.

---

## Providers

| Provider | Implements | Reach for it when |
|---|---|---|
| local-storage | guarded `localStorage` reads and writes | production — the default persistent broker |
| memory | an in-process map behind the same seam | tests, fixtures, or a deliberate no-op |
| vendor adapter | a store-specific persist interface | the consumer needs that store integration |

- must keep the vendor-shaped adapter on its own subpath, so the base seam stays vendor-name-free.

---

```txt
✅ broker.read<Draft>('draft') ?? emptyDraft     a miss is null, never a throw
✅ namespacedBroker(broker, 'codes')             two features never collide on 'draft'
❌ JSON.parse(localStorage.getItem('draft')!)    a global at import, and a throwing parse
```

---

## Neighbours

- [domains](../domains.md) — the shape every domain follows
- [config](../config/config.md) — the seam that fails loud where this one degrades silently
- [data](../data/state-and-data.md) — server state, which is cached rather than persisted here
- [architecture](../../../../shapes/app/architecture/architecture.md) — the layer a broker is wired in
- [swappable modules](../../../../../swappable-modules.md) — how a vendor adapter stays an optional subpath

---

## Boundaries

- must follow [security](../security/security.md#data) for sensitive fields and session cleanup.
- must validate decoded persisted values against their versioned schema, not only parse valid JSON.
- must distinguish in-memory storage from a no-op broker; a no-op never retains a write.

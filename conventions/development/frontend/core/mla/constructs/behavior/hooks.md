# Hooks

*Last updated: 2026-09-10*

> A `use*` function owning state, lifecycle and the operations over them for whatever calls it.
> Purpose — state and its cleanup share an owner that can be reused independently of presentation.
> Use case — naming a new hook, fixing its return shape, or deciding what disposes its subscription.

## Naming

- **Always prefix `use`** — `useAuth`, `useSupplyListings`.
- must name the owned resource or operation clearly — `useFilterOptions` or `useFilters`, according to its contract.
- File is PascalCase (`UseSupplyListings.ts`), export is camelCase (`useSupplyListings`)
  ([naming](../../../lla/notation/naming/naming.md)).

---

## Location

- layer and slice → [architecture](../../../../shapes/app/architecture/architecture.md) § *Sub-domains*,
  in a `hooks/` role-group.
- a cross-app hook ships from the repo's shared package
  ([boundaries](../../../../shapes/app/architecture/boundaries.md) § *Packaging*).

---

## Return shape

- must return live state and operations from a lifecycle hook; the hook itself is not a completed operation.
- must represent idle, pending, success and failure without false success values or treating pending as failure.
- must preserve previous data separately from refresh status when a refetch can run with visible cached data.
- must return a [result](../data/result.md) from a fallible operation exposed by the hook.
- must keep cancellation distinguishable from a reported operation failure when callers need to branch on it.
- must adapt third-party query rejection at the [query boundary](../../domains/data/state-and-data.md).
- must choose object or tuple shape through the [application rule](../../components/behavior/behavior.md).
- must reserve `*Result` for an operation outcome; name a reusable live state-and-operations contract `{Capability}Controls`.
- must classify a `*Controls` interface as a headless hook contract; rendering suffix routing applies only to components.

```txt
✅ Lifecycle handle: data + status + refetch; refetch returns an operation Result
❌ Result.ok(undefined) used to pretend an unstarted fetch already succeeded
```

---

## JSDoc

Verbs → [documentation](../../../lla/notation/documentation/documentation.md) § *Verb starters* — `Hook` and
`Context-accessor hook` are the two rows.

---

## Lifecycle rules

- must give every subscription, observer, timer, stream and object URL a disposer or owning framework scope.
- must make cleanup safe on repeated calls and leave no pending callback able to mutate disposed state.
- must cancel stale asynchronous work or ignore its result when cancellation is unavailable.
- must let the hook that owns the subscription dispose it itself, in its framework's teardown seam
  ([vue](../../../lla/constructs/vue/reactivity.md) · [react](../../../lla/constructs/react/hooks.md)).

---

## One export site

- must define a hook in exactly one module and expose it through the owning package's documented public entry point.
- must not republish a sibling capability's hook through unrelated barrels.
- must not alias it on the way out — a second name makes one hook read as two.
- a slice that needs a sibling's hook imports it; it does not republish it.

---

## Neighbours

- [state and data](../../domains/data/state-and-data.md) — the API client these wrap
- [documentation](../../../lla/notation/documentation/documentation.md) — the verb table
- [naming](../../../lla/notation/naming/naming.md) — the file / export casing

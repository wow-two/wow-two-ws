# TanStack data

*Last updated: 2026-09-10*

> TanStack Query adaptation behind the house data contract.

## Adapter

- must inherit the [data contract](../state-and-data.md).
- must keep `@tanstack/vue-query` imports inside the Vue engine adapter.
- must reject failed query operations internally so error, retry and cache semantics remain correct.
- must expose house failures and live query state outside the adapter, not vendor exception objects.
- must consume the query context signal for cancellation of shared requests.
- must keep query retry policy distinct from mutation idempotency policy.
- must run shared conformance plus [Vue integration](../vue/vue.md) cases.

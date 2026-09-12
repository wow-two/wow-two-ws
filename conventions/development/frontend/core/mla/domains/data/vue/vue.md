# Vue data

*Last updated: 2026-09-10*

> Vue bindings for the provider-free data contract.

## Binding

- must inherit the [data contract](../state-and-data.md).
- must use Vue `ref` / `reactive` / `computed` for local state and `provide` / `inject` for scoped shared state.
- must pin the query adapter in `bootstrap/`; app code consumes the SDK contract through that pin.
- must pass reactive query inputs as getters or refs so key changes trigger the intended query.
- must use the engine-owned cancellation signal for shared queries; one consumer unmount cannot cancel other consumers.
- must dispose consumer-owned subscriptions and standalone requests with their Vue scope.

- must follow the [TanStack adapter](../tanstack/tanstack.md) when that engine is selected.

# Vue routing

*Last updated: 2026-09-10*

> Vue Router bindings for app routing.

## Adapter

- must inherit the [routing contract](../routing.md).
- must create Vue Router through the SDK adapter pinned by the app's bootstrap.
- must keep Vue Router imports and route records behind that adapter and app bootstrap integration.
- must map route params/search into typed page props before rendering the page.
- must render nested places through `RouterView` in the app layout.
- must adapt navigation chrome to `RouterLink` while preserving actual anchors and active state.
- must use Vue lazy component imports for route chunks.
- must implement guards, title, not-found and error behavior in the adapter, not separately in every page.
- must test direct navigation, reload, history, nested layouts, guard resolution and failed lazy imports.

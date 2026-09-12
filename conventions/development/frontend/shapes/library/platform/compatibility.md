# Compatibility

*Last updated: 2026-09-10*

> Declared runtime support and capability fallbacks for library entries.

## Support matrix

- must publish a code-adjacent support matrix for each public subpath and adapter.
- must name supported framework versions, browser minimums, JavaScript target and required Web APIs.
- must derive build targets and test environments from that matrix, not a moving label such as latest.
- must distinguish browser-only, DOM-free import, server-renderable and hydration-supported entries.
- must make a vendor-free contract entry import without DOM globals or optional vendor packages.
- must declare a browser-only adapter explicitly; a safe base import does not certify that adapter for SSR.
- must load browser APIs lazily in supported client actions and feature-detect optional capabilities.
- must return the documented unsupported outcome when a required optional API is unavailable.

---

## Polyfills

- must declare who supplies each required polyfill and when it loads.
- must let the app pin a Temporal polyfill when its supported browsers lack required native Temporal APIs.
- must not mutate global prototypes or install polyfills as an import side effect.
- must test native and declared fallback paths where both are supported.

---

## SSR and hydration

- must create mutable clients, buses, caches and stores per app/request, never share user state process-wide.
- must seed locale, timezone-sensitive rendering, theme and IDs consistently across server/client first render.
- must avoid random, time-dependent or browser-derived first-render markup without a serialized seed.
- must document portal/teleport behavior during server render and hydration.
- must release request resources even when client mount/unmount hooks never run.
- must test server import separately from SSR render and hydration; none substitutes for another.
- must advertise only the support level verified for that subpath.

---

## App consumption

- must let an app choose a subset of the library's supported environments.
- must verify that app targets satisfy every imported subpath's requirements.
- must keep framework-specific effects and cleanup in the appropriate framework convention.

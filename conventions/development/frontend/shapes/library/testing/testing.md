# Testing

*Last updated: 2026-09-10*

> Behavioral and consumer verification for frontend libraries.

## Layers

| Tier | Verifies |
|---|---|
| unit | pure logic, parsing, state transitions and failure branches |
| conformance | identical public semantics across engine adapters |
| DOM interaction | controlled state, events, forms and lifecycle |
| browser | real focus, layout, portals, Web APIs and keyboard behavior |
| stories | representative visible states and executable user interactions |
| packed consumer | public exports, declarations, CSS and peer isolation |

- must choose tests by behavior and risk; snapshots alone do not establish interaction semantics.
- must test public outcomes rather than mirror internal implementation steps.
- must verify discovery counts and skipped cases; an empty project is not a passing coverage claim.
- must typecheck tests/stories even when they are excluded from package emit.
- must keep source/tests layout under [SDK structure](../../../../repo/structure/sdk-structure.md#tests).
- must make time, network and locale-dependent cases deterministic with explicit fixtures.
- must run the shared conformance suite against every advertised adapter.
- must test at least one integration of each adapter with its supported framework.

---

## Interaction matrix

- must cover controlled/uncontrolled state, clear/reset, external updates and disabled/read-only behavior when applicable.
- must cover keyboard operation, visible focus, focus restoration and nested overlays when applicable.
- must cover error announcements and accessible naming with rendered assertions.
- must verify reduced motion, forced colors, zoom/reflow, RTL and long labels for affected visual changes.
- must use manual keyboard/screen-reader checks when automation cannot establish the claimed behavior.
- must record browser/assistive technology and unverified cases with the release evidence.
- must link a component's behavioral acceptance to its story/spec; a static demo is not an interaction test.

---

## Sweep gates

- must run typecheck, lint, format and relevant tests for each integrated sweep row.
- must remeasure the row's original invariant and preserve independent preexisting work.
- must run build and [packed-consumer checks](../delivery/delivery.md#artifact) for export or release changes.
- must map every deferred failing case to a named blocker; do not count expected failures as covered behavior.
- must use [compatibility](../platform/compatibility.md) for runtime and hydration claims.

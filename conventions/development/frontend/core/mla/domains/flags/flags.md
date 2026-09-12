# Flags

*Last updated: 2026-09-10*

> Feature-flag evaluation — boolean, string, number and JSON-object reads against one source seam.
> Purpose — every evaluation is total, so a gated element never renders an error state or a loading flicker.
> Use case — gating a rollout, targeting a cohort, or pointing an app at a real flag service.

## The contract

- must resolve synchronously — a read happens inside a computed, where async forces a flicker or a boundary.
- must return the type asked for and never throw; every evaluation is total.
- must fall back to the caller's default on a miss, an off switch, a wrong wire type, or a throwing source.
- must report an unconfigured flag as a default, carrying no error — a pre-rollout flag is the normal state.
- must reserve the error reason for a genuine fault, and name it with a type-mismatch or source-error code.
- must re-check every resolved value at runtime; wire data is untyped and a stale definition really does lie.
- must surface a fault on the error handler alone.
- must merge a targeting context app-wide, and let a per-call context override it.
- must expose the seam that fires when the targeting context moves, so a remote source can refetch.
- must resolve a read with no provider mounted — the standalone fallback returns the caller's default.
- must carry the matched variant on the evaluation, so exposure logging has something to report.
- must name the source adapter `FlagProvider` and the component `FlagsProvider` — the plural is the component.
- must return a disposer from a context subscription ([hooks](../../constructs/behavior/hooks.md) § *Lifecycle rules*).
- must ship no UI — gates, banners and admin panels stay app-side.

---

## Providers

| Provider | Implements | Reach for it when |
|---|---|---|
| static | an in-memory map with variants, rules and an off switch | local dev and tests — targeting with no service |
| any source | the source seam over a fetched snapshot | production; refetch when the context moves |

---

```txt
✅ useFlag('newNav', false)               a miss reads 'default', the value is false
✅ client.setContext({ plan, region })    targeting merged app-wide, overridable per call
❌ if (await flags.get('newNav'))         an async read gating a render
```

---

## Neighbours

- [domains](../domains.md) — the shape every domain follows
- [provider](../../constructs/visual/provider.md) — the kind that installs the client for a subtree
- [analytics](../analytics/analytics.md) — where a variant is reported as an exposure
- [config](../config/config.md) — build-time settings, which do not vary per user

---

## Scope

- must follow [domain lifetime](../domains.md#lifetime) when context/providers change.
- must invalidate a stale remote-context response before it can update a newer identity.
- must treat flag evaluation as presentation policy, never backend authorization.

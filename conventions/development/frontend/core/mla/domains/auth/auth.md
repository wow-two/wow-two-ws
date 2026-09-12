# Auth

*Last updated: 2026-09-10*

> The session state machine an app renders against, and the sign-in shapes that settle it.
> Purpose — a page reads a status and a user; how the credential was obtained stays behind the strategy.
> Use case — gating a route, flipping the session on a 401, or adding a second sign-in shape.

## The contract

- must model the session as `unknown → resolving → authenticated | anonymous`.
- must carry a non-null user exactly when the status is `authenticated`.
- must resolve the current user once on mount, deduped through one instance-owned in-flight promise.
- must settle a failed resolve as anonymous and report it — the machine never stays pending.
- must keep one strategy the whole transport: resolve required, sign-in / sign-out / unauthorized optional.
- must let a strategy return no user from sign-in, leaving state unchanged for a navigating flow.
- must route a transport 401 through the instance-owned bridge, which flips the session.
- must let a route guard await an unsettled session before it allows or redirects.
- must publish transitions on the instance bridge; non-component callers receive that instance explicitly.
- must return a disposer from every bridge subscription
  ([hooks](../../constructs/behavior/hooks.md) § *Lifecycle rules*).
- must type the user generically; its shape is the app's, never the contract's.
- must ship no UI — gates, splash surfaces and sign-in pages stay app-side.
- must access browser APIs inside supported client actions; import safety alone is not SSR support.

---

## Providers

| Provider | Implements | Reach for it when |
|---|---|---|
| cookie | me-resolve over a backend-owned cookie + sign-out | the backend owns the cookie, guest gates included |
| bearer | a credential exchange, token storage, a token reader | no cookie exists and the token stays off disk |
| redirect | a cookie session whose sign-in navigates away | the OAuth callback is server-side and returns back |
| oauth | a provider script wrapped, surfacing a credential | the app renders a provider button, then signs in |

- must keep the provider-script wrapper below this domain — it knows nothing about sessions.

---

```txt
✅ createApiClient({ onUnauthorized: bridge.onUnauthorized })   a 401 flips the session
✅ requireAuth(bridge.isAuthenticated)                          the guard awaits the resolve
❌ useAuth() inside an interceptor                              a non-component seam reads the bridge
```

---

## Neighbours

- [domains](../domains.md) — the shape every domain follows
- [data](../data/state-and-data.md) — the client a strategy calls, and where a 401 originates
- [routing](../../../../shapes/app/routing/routing.md) — the guard that reads the settled session
- [provider](../../constructs/visual/provider.md) — the kind that installs the session for a subtree
- [swappable modules](../../../../../swappable-modules.md) — how a provider's vendor stays an optional peer

---

## Session safety

- must follow [security](../security/security.md#session) for CSRF, redirects and logout isolation.
- must cancel or invalidate an earlier resolve when sign-in/sign-out establishes a newer session generation.
- must report a resolve transport failure without exposing credentials or treating it as an authorization decision.
- must follow [domain lifetime](../domains.md#lifetime) for bridge ownership and replacement.

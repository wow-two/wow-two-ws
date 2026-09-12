# Controller known endpoints

*Last updated: 2026-09-10*

> Identity and system endpoints whose controller, route, action and path are fixed across every app —
> `api/identity/*`, `api/system/status`.
> Purpose — one identity surface per product; a frontend targets the same paths everywhere, not
> `auth/login` here and `admin/session` there.
> Use case — adding or renaming a sign-in, sign-out, current-user, guest or status endpoint, or aligning
> a controller that predates the convention.

## Identity — `IdentityController` @ `api/identity`

- must declare `sealed IdentityController` with `[Route("api/identity")]`.
- must summarize it `Exposes identity over HTTP.`
- must implement only the capabilities the app has.
- must take the exact action name and path below for each capability.
- the verb may vary by mechanism.

| Capability | Action | Path | Verb | Summary |
|---|---|---|---|---|
| Current identity | `Me` | `me` | `GET` | `Gets the current identity.` |
| Sign in | `SignIn` | `sign-in` | `POST` (credential) / `GET` (OAuth challenge) | `Begins sign-in.` |
| Sign out | `SignOut` | `sign-out` | `POST` | `Signs the caller out.` |
| Guest session | `Guest` | `guest` | `POST` | `Provisions a guest session.` |
| Sign up | `SignUp` | `sign-up` | `POST` | `Registers a new account.` |
| Refresh | `Refresh` | `refresh` | `POST` | `Refreshes the session.` |
| OAuth callback | `Callback` | `callback` | `GET` | `Completes the OAuth callback.` |

- must `POST` a credential or token sign-in — it carries a body.
- must `GET` an external-IdP challenge that only redirects — `sign-in` → 302 to the provider.
- must keep the path `sign-in` either way.
- must keep the mechanism out of the summary — OAuth, password and guest are *how*: `Begins sign-in.`,
  never `Challenges the GitHub scheme.` ([controller](../../../../core/mla/constructs/behavior/controller.md) § *Type doc*).
- must expose `callback` as an action only when the controller handles it.
- must leave `CallbackPath` with the auth middleware when the middleware owns it.
- must keep that path in sync rather than add a dead action.

---

## System — `SystemController` @ `api/system`

- must declare `sealed SystemController` with `[Route("api/system")]`.
- must summarize it `Exposes system status over HTTP.` — the `Exposes` starter every controller takes.
- must expose `Status` at `GET api/system/status` — liveness, service identity, any app-specific
  health fact such as the vault's seal state.
- must mark `Status` `[AllowAnonymous]` — the sign-in screen hits it pre-auth.
- must keep the `Status` action summary abstract, never the payload shape — `Reports service liveness.`,
  `Reports the vault's seal state.`

---

## Changes

- must update backend route configuration and frontend callers together when a fixed route changes.
- must preserve callback, cookie and proxy routing behavior at the new path.
- must preserve authorization explicitly when moving an endpoint out of a protected path prefix.

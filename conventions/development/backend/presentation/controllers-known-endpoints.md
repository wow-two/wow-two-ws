# Controller known endpoints

*Last updated: 2026-06-17*

> Identity & system endpoints whose controller, route, action name, and path are **fixed across every app** — `api/identity/*`, `api/system/status`.
> Purpose — one identity surface in every product, so a frontend (and the coming frontend beta SDK) targets the same paths everywhere; no `auth/login` here, `admin/session` there.
> Use case — reach for this when adding or renaming any sign-in / sign-out / current-user / guest / status endpoint, or aligning a controller that predates the convention.

## Identity — `IdentityController` @ `api/identity`

- Controller: `sealed IdentityController`, `[Route("api/identity")]`, `/// <summary>Manages identity.</summary>`.
- Implement only the capabilities the app has — but when you do, the **action name + path are exactly these** (verb may vary by mechanism):

| Capability | Action | Path | Verb | Summary |
|---|---|---|---|---|
| Current identity | `Me` | `me` | `GET` | `Gets the current identity.` |
| Sign in | `SignIn` | `sign-in` | `POST` (credential) / `GET` (OAuth challenge) | `Begins sign-in.` |
| Sign out | `SignOut` | `sign-out` | `POST` | `Signs the caller out.` |
| Guest session | `Guest` | `guest` | `POST` | `Provisions a guest session.` |
| Sign up | `SignUp` | `sign-up` | `POST` | `Registers a new account.` |
| Refresh | `Refresh` | `refresh` | `POST` | `Refreshes the session.` |
| OAuth callback | `Callback` | `callback` | `GET` | `Completes the OAuth callback.` |

- **Verb by mechanism** — credential / token sign-in is a `POST` (it carries a body); an external-IdP challenge that only redirects is a `GET` (`sign-in` → 302 to the provider). Path stays `sign-in` either way.
- **Mechanism is never in the summary** — OAuth vs password vs guest is *how* (`Begins sign-in.`, not `Challenges the GitHub scheme.`). See [controllers.md › Documentation](controllers.md).
- **OAuth callback** — only expose `callback` as an action if the controller handles it; if the auth middleware owns `CallbackPath`, leave it there and keep that path in sync — don't add a dead action.

---

## System — `SystemController` @ `api/system`

- Controller: `sealed SystemController`, `[Route("api/system")]`. Non-resource → verb-first summary (`Reports the vault's seal state.`), not `Manages …`.
- `Status` → `GET api/system/status` — liveness / service identity, plus any app-specific health fact (e.g. the vault's seal state). `[AllowAnonymous]` (the sign-in screen hits it pre-auth).
- Summary stays abstract — `Reports service liveness.` / `Reports the vault's seal state.`; never the payload shape.

---

## Migrating a legacy auth controller

- `AuthController` → `IdentityController`; `api/auth` or `api/admin/session` → `api/identity`.
- `Login` → `SignIn` · `Logout` → `SignOut` · `me` stays `Me`.
- **Grep the whole backend**, not just the controller — `CallbackPath`, `returnUrl`, cookie paths, reverse-proxy / path-prefix auth rules may hard-code the old path. Update every reference.
- If a path-prefix policy (e.g. everything under `api/admin` is `[Authorize]`) is load-bearing, flag it before moving a route out of that prefix.
- The frontend caller changes with it — update its paths in the same pass.

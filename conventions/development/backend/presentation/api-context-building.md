# API context building

*Last updated: 2026-06-17*

> How a controller sources **caller context** — the actor plus ambient request facts — to pass into an application request, via `ICurrentUser` with `User` / `HttpContext` as the fallback.

## `ICurrentUser`

- `ICurrentUser` is the app's identity abstraction - resolves the current actor (user id / guest id) for the request
- must read the actor through `ICurrentUser`, not raw claims - keeps the identity model in one place
- inject it into the controller only when an action needs the actor (a two-model request); a single-actor app may not need it

---

## Fallbacks

- use the inherited `User` (`ClaimsPrincipal`) / `HttpContext` for facts `ICurrentUser` doesn't expose - source IP, headers
- never read these in a handler - caller context is sourced at the edge and rides the application request ([mediator.md](../messaging/mediator.md))

---

## Usage

- source the context, then pass it explicitly into the mapping - `request.ToCommand(currentUser.Id)` ([request-models.md](request-models.md))
- guard a missing actor at the edge - `if (currentUser.Id is not { } userId) return Unauthorized();`

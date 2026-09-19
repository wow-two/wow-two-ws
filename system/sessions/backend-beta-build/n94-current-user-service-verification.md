# N94 current-user service verification

*Verified: 2026-09-16*

## Result

N94 is complete in the SDK. `ICurrentUserService` is the single current-user contract for HTTP callers, audit
stamping and soft-delete stamping. `IAuditCurrentUserService`, `ICurrentUser` and their duplicate lifetimes are removed.

## Lifetime

- `CookieCurrentUserService` is a singleton over singleton `IHttpContextAccessor`.
- Each `Id` or `Kind` access reads the current ambient `HttpContext`; no principal is cached on the singleton.
- No HTTP context returns anonymous and a null id, allowing background saves to remain unstamped.
- Audit and soft-delete interceptors read `ICurrentUserService.Id` inside every save callback.
- Custom current-user implementations registered by the interceptor helpers remain singleton-safe by contract.

## Verification

- A container with scope validation enabled builds and resolves `ICurrentUserService`.
- The same singleton returns two different authenticated IDs as the ambient context changes.
- The same singleton returns anonymous after the ambient context is cleared.
- Identity.Tests passed 8 of 8 tests.
- Data.Tests passed 23 of 23 tests.

## Consumer adoption

ForeverPin's four controllers still inject `ICurrentUser`; they remain in the post-release consumer repin pass.

# C15 API defaults pipeline verification

*Last updated: 2026-09-16*

## Result

- `UseApiDefaults` now calls routing before endpoint-metadata consumers.
- response compression now wraps routing and response writers.
- the optional identity callback runs after routing and CORS.
- rate limiting and output caching run after the identity callback.
- hosts retain explicit control of authentication and authorization wiring.

## Evidence

- `ApiDefaultsPipelineTests` starts a real in-memory `WebApplication` host.
- the global limiter sees both route metadata and the authenticated subject.
- an output-cache policy varies entries by authenticated subject.
- an authorization-required endpoint succeeds through the callback.
- a compressible endpoint returns `Content-Encoding: gzip`.
- `dotnet test Web.Tests/WoW.Two.Sdk.Backend.Beta.Web.Tests.csproj --no-restore -m:1`
  passed 47 tests.

## Adoption

- authenticated consumers must pass `UseAuthentication()` and `UseAuthorization()` through the
  `UseApiDefaults` callback when repinned.

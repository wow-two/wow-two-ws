# N60 ProblemDetails factory verification

*Last updated: 2026-09-16*

## Result

- Added `IAppErrorProblemDetailsFactory` as the replaceable ProblemDetails creation seam.
- Moved the interface and default `AppErrorProblemDetailsFactory` under `Web/ExceptionHandling/Factories/`.
- Converted the default from a static class to a sealed DI-managed factory with injected error mappers.
- Updated every exception handler and the MVC validation filter to consume the interface.
- Registered the default with `TryAddSingleton`, preserving an app implementation registered first.
- Retained status, type, code, message, field-error, reserved-header and origin-suppression behavior.

## Consumer impact

- Direct static callers must inject `IAppErrorProblemDetailsFactory` after they repin the published SDK version.
- Current direct callers exist in ForeverPin, TransportBrain, Tnis, TranscriptForge and SecretsVault.
- Consumer repair remains release-dependent in the active sweep handoff.

## Verification

- `dotnet build WoW.Two.Sdk.Backend.Beta.csproj --no-restore -m:1`: passed, 0 errors and 17 existing warnings.
- `dotnet test Web.Tests/WoW.Two.Sdk.Backend.Beta.Web.Tests.csproj --no-restore -m:1`: 39 passed, 0 skipped, 0 failed.
- The test suite covers all existing mapping behavior plus app-first replacement registration.
- No whole-solution, pack, CI, publish or consumer result is claimed.

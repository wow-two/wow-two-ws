# C21 validation conformance verification

*Last updated: 2026-09-16*

## Result

- Changed `ValidatingInterceptor<TRequest, TResponse>` to evaluate every registered SDK `IValidator<TRequest>`.
- Combined field failures in validator registration order and threw one SDK `ValidationException`.
- Preserved the original `ValidationError` when exactly one validator fails.
- Added regression coverage proving all validators run and authored field-error codes remain exact.
- Corrected the mediator validation guide's stale method name, exception type and ProblemDetails link.
- Reserved pre-handler interception for target-free requests.
- Placed target-bearing validation after target resolution and ownership checks in the handler or shared service.
- Retained the synchronous SDK validator contract and the explicit async/ruleset/read-seam deferrals.
- Documented external validation as the default for copied and deserialized candidates at their accepting boundary.
- Documented `GeoBoundingBox` as the SDK's exceptional constructor-enforced data contract.

## Inventory

- SDK production source contains no request handler that dispatches another command or query.
- No nested mediator dispatch or direct handler-reuse path required extraction to a shared service.
- `GeoBoundingBox` uses get-only edges and one validating constructor, so supported record copies cannot alter
  an edge and constructor-based deserialization applies the same ordering checks.
- Other constructor throws found in the validation scope are programmer/configuration guards, not request-model
  data validation.

## Verification

- `dotnet build Foundation.Tests/WoW.Two.Sdk.Backend.Beta.Foundation.Tests.csproj --no-restore -m:1`: passed,
  0 errors.
- `dotnet test Foundation.Tests/WoW.Two.Sdk.Backend.Beta.Foundation.Tests.csproj --no-build --no-restore -m:1`:
  115 passed, 0 skipped and 0 failed.
- `dotnet build Mediator.Tests/WoW.Two.Sdk.Backend.Beta.Mediator.Tests.csproj --no-restore -m:1`: passed,
  0 errors.
- `dotnet test Mediator.Tests/WoW.Two.Sdk.Backend.Beta.Mediator.Tests.csproj --no-build --no-restore -m:1`:
  68 passed, 0 skipped and 0 failed.
- Builds retain existing dependency-advisory and analyzer warnings.
- No whole-solution, pack, CI, publish or consumer result is claimed.

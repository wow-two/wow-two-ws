# C24 HTTP replay safety verification

*Verified: 2026-09-16*

## Result

C24 is complete. Retry and hedging now share one request replay classifier. GET, HEAD, OPTIONS and TRACE are replay-safe by default; unsafe and custom methods require an explicit client-level selector tied to the operation's idempotency contract.

## Contract

- `UnsafeRequestReplaySelector` opts in an otherwise unsafe request; the default runs it once.
- Caller cancellation prevents another retry or hedge.
- Invalid attempt, total-budget and circuit-breaker relationships fail during registration.
- `StreamContent` is never replayed. Hedging rejects it before the transport; streaming calls use an `AddSdkResilience` client.
- Retry and hedging are alternative client pipelines and are not stacked.
- Polly disposes discarded retry responses and unselected hedged responses; focused tests observe owned content disposal.

## Verification

- `dotnet build src/WoW.Two.Sdk.Backend.Beta.csproj --no-restore -m:1 --nologo`: passed.
- `dotnet test src/Web.Tests/WoW.Two.Sdk.Backend.Beta.Web.Tests.csproj --no-restore -m:1 --nologo --filter FullyQualifiedName~HttpReplaySafetyTests`: 9 passed.
- Coverage includes safe retry, default POST single execution, explicit idempotent POST replay with identical bodies, caller cancellation, total request budget, safe hedging, default POST single execution, stream rejection and invalid option relationships.

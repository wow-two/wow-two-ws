# C28 API request mapping verification

*Verified: 2026-09-16*

## Result

C28 is complete by source inventory. The SDK contains no dedicated top-level HTTP request body and therefore no
request mapping companion to relocate or create.

## Evidence

- No production C# declaration ends in `ApiRequest`.
- No production C# call or declaration uses `ToCommand(...)` or `ToQuery(...)`.
- `CodeRenderRequest` is an SDK rendering input model under `Codes/Models`.
- `PendingRequest` and `SagaTimeoutRequest` are internal messaging state objects.
- The API-request file exception remains convention-owned and will apply when a product declares its HTTP bodies.

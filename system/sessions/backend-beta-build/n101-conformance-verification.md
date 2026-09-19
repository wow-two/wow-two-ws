# N101 conformance verification

*Last updated: 2026-09-16*

## Result

- Moved the 12 provider send/receive implementations into each provider's `Transports/` folder and namespace.
- Retained `ISendTransport` and `IReceiveTransport` under `Messaging/Transport/` as the shared delivery contracts.
- Renamed `IEventSagaTransport` to `IEventSagaPublisherService` and `InProcessEventSagaTransport` to
  `EventSagaPublisherService`, under `EventSaga/Services/`. The implementation validates destinations and delegates
  delivery to `IEventBus`; it does not own a delivery medium.
- Updated registration, XML documentation and messaging documentation to the new namespaces and responsibility.
- Updated every concrete provider transport summary to use the required `Transports` starter.
- GeoJSON now requires matching root discriminators and required feature members, rejects unsupported position
  arity, and preserves feature-id string/number JSON kinds. The contract documents unsupported geometry and
  discarded `bbox`/foreign members; semantic ring/cardinality checks remain external validation.
- Google ID-token authentication now observes pre-cancellation and stops awaiting provider validation when canceled.
  Google.Apis.Auth exposes no cancellation token, so an already-running certificate refresh finishes independently.

## Verification

- `dotnet build WoW.Two.Sdk.Backend.Beta.csproj --no-restore -m:1`: passed, 0 errors and 17 existing warnings.
- `dotnet test WoW.Two.Sdk.Backend.Beta.Messaging.Tests.csproj --no-restore -m:1`: 111 passed, 1 skipped, 0 failed.
- `dotnet test WoW.Two.Sdk.Backend.Beta.Foundation.Tests.csproj --no-restore -m:1`: 114 passed, 0 skipped, 0 failed.
- `dotnet test WoW.Two.Sdk.Backend.Beta.Identity.Tests.csproj --no-restore -m:1`: 6 passed, 0 skipped, 0 failed.
- The first test attempt reached the known `SocketException (13): Permission denied` test-runner restriction.
  The scoped command was rerun through native escalation and completed; this is an execution restriction, not a
  source or test failure.
- No package, whole-solution, external-broker, pack, CI or release result is claimed.

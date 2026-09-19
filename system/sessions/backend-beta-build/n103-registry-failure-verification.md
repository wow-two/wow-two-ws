# N103 registry failure verification

*Verified: 2026-09-16*

## Result

N103 is complete. Registry lookup behavior now distinguishes incomplete local composition from open runtime input.

## Decisions

- `MessageTypeRegistry.GetToken` throws when a local outgoing event type was never registered.
- `MessageTypeMapper` no longer emits or resolves assembly-qualified fallback tokens.
- `MessageSerializerRegistry.Resolve` uses the default only for an absent content type.
- An explicit unregistered content type throws into each transport's unparseable-message path.
- Unknown inbound type tokens remain nullable because they are untrusted protocol input.
- `EventDispatcherRegistry.TryGet` remains a no-handler predicate used by the explicit `NoHandler` outcome.
- `DestinationBindingRegistry.IsDeclared` remains a set-membership predicate.
- `PendingRequestRegistry.TryComplete` remains a correlation/race predicate.
- `ConsumedMessageTypeRegistry` exposes its registered set and has no lookup miss.

## Verification

- Messaging.Tests built successfully.
- Messaging.Tests passed 113, skipped 1 and failed 0.
- Tests cover required outgoing registration, unknown inbound tokens, aliases, absent content types and explicit
  unregistered content types.
- Strict string-enum fixtures were refreshed where the earlier HTTP/shared JSON correction exposed stale expectations.

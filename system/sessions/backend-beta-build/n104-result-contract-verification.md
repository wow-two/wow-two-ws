# N104 Result contract verification

*Last updated: 2026-09-16*

## Result

- Changed `IRequestClient.GetResponseAsync` from a bare response to `Result<TResponse>`.
- Returned `OperationTimeout` when a reply misses its per-call deadline.
- Returned `SerializationFailed` when an accepted reply envelope carries an inconsistent body instance.
- Removed `RequestTimeoutException` and `RequestFaultException`; no SDK or direct consumer code still referenced them.
- Changed `IMigrationBroker.Read` to `Result<IReadOnlyList<RawMigration>>`.
- Returned `FileNotFound` for an Apply script without its required Rollback pair.
- Returned `DataIntegrity` when filesystem or embedded migration content cannot be read.
- Propagated migration-source failures through `MigrationRunnerService.Scan` into every public runner result.

## Boundary finding

- `PendingRequestRegistry` rejects a response whose declared type does not satisfy the pending response contract.
- The client's reply-body failure arm therefore guards an inconsistent envelope rather than a normal wrong-type reply.

## Consumer impact

- No direct consumer currently calls `IRequestClient.GetResponseAsync` or names the removed exception types.
- Migration consumers receive the same public runner `Result` shape; incomplete source pairs no longer escape as exceptions.

## Verification

- `dotnet test Messaging.Tests/WoW.Two.Sdk.Backend.Beta.Messaging.Tests.csproj --no-restore -m:1`: 111 passed,
  1 skipped and 0 failed.
- `dotnet build Migrations.Tests/WoW.Two.Sdk.Backend.Beta.Migrations.Tests.csproj --no-restore -m:1`: passed.
- `dotnet test Migrations.Tests/WoW.Two.Sdk.Backend.Beta.Migrations.Tests.csproj --no-build --no-restore -m:1`:
  17 passed, 0 skipped and 0 failed.
- New migration coverage verifies a complete filesystem pair and missing Rollback failures from both source types.
- No whole-solution, pack, CI, publish or consumer result is claimed.

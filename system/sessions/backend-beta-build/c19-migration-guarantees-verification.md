# C19 migration guarantees verification

*Verified: 2026-09-16*

## Result

C19 is complete. The bespoke migrator now states each provider's coordination boundary, executes multi-statement no-transaction scripts sequentially and has provider-level coverage for the requested migration guarantees.

## Implemented guarantees

- `MigrationCoordinationMode` exposes `DatabaseLock` for PostgreSQL and `SingleApplicantRequired` for SQLite.
- PostgreSQL holds its advisory lock for the complete apply loop; two competing runners serialize and only one applies a pending ordinal.
- SQLite no longer claims multi-applicant safety from `busy_timeout` or the history primary key.
- No-transaction SQL is split outside quoted strings, identifiers, comments and PostgreSQL dollar quotes, then issued as separate commands.
- Interrupted `CREATE UNIQUE INDEX CONCURRENTLY` recovery drops the invalid index before rebuilding it.
- PostgreSQL enum labels use separate add and use migrations; rollback documents that removing the history row cannot remove the label.
- SQLite constraint evolution uses a table rebuild that restores rows, indexes, triggers and foreign keys on apply and rollback.
- Native PostgreSQL enums round-trip through matching Npgsql driver and EF registrations with the `waiting_for_review` label.
- CLI child-process tests prove exit codes `0`, `1` and `2` for success, invalid input and destructive-target refusal.

## Verification

- `dotnet build Migrations.Tests/WoW.Two.Sdk.Backend.Beta.Migrations.Tests.csproj --no-restore -m:1`: passed.
- `dotnet test Migrations.Tests/WoW.Two.Sdk.Backend.Beta.Migrations.Tests.csproj --no-build -m:1`: 26 passed, 0 failed, 0 skipped.
- The test command ran through native escalation because the test runner and PostgreSQL Testcontainer require local sockets.

## Documentation

- `src/Data/Migrations/migrations.md` now reflects the shipped `Bespoke/` folder, current registration method and provider-specific coordination.
- `src/Data/Migrations/Bespoke/bespoke.md` records current concurrency, no-transaction, enum, SQLite rebuild and CLI exit guarantees.

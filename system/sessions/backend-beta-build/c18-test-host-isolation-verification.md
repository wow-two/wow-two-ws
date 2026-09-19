# C18 test-host isolation verification

*Last updated: 2026-09-16*

## Result

- `AddTimeProviders` derives NodaTime `IClock` from the registered `TimeProvider`.
- `WebApiTestHost<T>` replaces both clock registrations with one `FakeTimeProvider`.
- `ConfigureConfigurationHook` adds values to one host without process-environment mutation.
- `AddPostgresPersistence<T>` resolves its connection string when services build, after host-local configuration.
- `MultiHostFixture` no longer exposes or invokes `ConfigureEnvironment`.
- each `RelationalTestDb<TContext>` instance owns its Postgres or SQLite selection.
- the process-global `TestSetupOptions.Current` switch was removed.

## Verification

- `Foundation.Tests`: 125 passed, including two clock-adapter registration cases.
- `Web.Tests`: 48 passed, including two simultaneous hosts with independent clocks and configuration.
- `Data.Tests`: 25 passed, including fixture-provider isolation and late host-configuration resolution.
- the host-isolation test verifies the pre-existing process environment remains unchanged.

# C23 startup failure reporting verification

*Verified: 2026-09-16*

## Result

C23 is complete. `StartupFailureReporter` establishes a synchronous durable file sink before invoking any host code, keeps that channel independent of the final logger, flushes both paths and rethrows the original failure.

## Contract

- The caller wraps builder creation, configuration, build, start and run in `StartupFailureReporter.RunAsync`.
- `logs/startup-failures.log` is available before application DI or the `UseSerilogConventional` callback.
- An escaping failure is written to the retained startup logger even after the global logger hands off to final configuration.
- Logging and flush faults are suppressed so they cannot replace the host result or original exception.
- The original exception escapes; an unhandled top-level failure therefore preserves the nonzero process exit.
- A normal final-logger handoff writes an application event once and does not copy it into the startup channel.

## Verification

- `dotnet build Web.Tests/WoW.Two.Sdk.Backend.Beta.Web.Tests.csproj --no-restore -m:1`: passed.
- `dotnet test Web.Tests/WoW.Two.Sdk.Backend.Beta.Web.Tests.csproj --no-build -m:1`: 52 passed.
- Two nested child processes fail independently before host creation and during `ValidateOnStart`; both exit nonzero and leave the expected exception in the startup file after process exit.
- The normal-run test replaces the bootstrap logger with a final sink and observes exactly one application event outside the startup file.

# Recorder rename verification

*Last updated: 2026-09-13*

> Scoped compile evidence for the confirmed live-recorder `Tracker` names.

## Scope

- `InterceptorLog` → `InterceptorInvocationTracker` in `Data.Tests` (root lane).
- `RecordedMessageLog` → `RecordedMessageTracker` in `Testing.Messaging`.
- `RecordedTransitionLog<TState>` → `RecordedTransitionTracker<TState>` in `Testing.Messaging`.
- Exact source references, XML references and the messaging testing guide follow the names.
- Behavior is unchanged; no new tests, package version changes or Git mutations.

---

## Build results

SDK: `dotnet --version` returned `10.0.300`.
Working directory: `workbench/wow-two-sdk-beta/wow-two-sdk.backend.beta/engineering/codebase/wow-two-back-beta-sdk/src/`.
Builds ran serially to avoid shared-project contention.

| Project | Command arguments after `dotnet build` | Result |
|---|---|---|
| Data.Tests | `Data.Tests/WoW.Two.Sdk.Backend.Beta.Data.Tests.csproj --no-restore -m:1` | succeeded; 103 warnings, 0 errors |
| Testing.Messaging | `Testing.Messaging/WoW.Two.Sdk.Backend.Beta.Testing.Messaging.csproj --no-restore -m:1` | exit 0; 41 warnings, 0 errors |
| Messaging.Tests | `Messaging.Tests/WoW.Two.Sdk.Backend.Beta.Messaging.Tests.csproj --no-restore -m:1` | exit 0; 154 warnings, 0 errors |

- Data.Tests evidence comes from the completed root build log; the root process ID was not accessible to the child.
- `Messaging.Tests` is the only direct SDK project reference to `Testing.Messaging` found by the scoped project search.
- Warnings include NuGet dependency advisories and existing analyzer findings; these builds are not warning-clean.
- Build logs: `/private/tmp/interceptor-tracker-build.log`, `/private/tmp/messaging-tracker-build.log`,
  `/private/tmp/messaging-tracker-consumers-build.log`.

---

## Static checks

- `rg` for all three old type names under SDK `engineering/`, excluding `bin/` and `obj/`, returned no matches.
- `git diff --check` for `Testing.Messaging/` and `Data.Tests/` passed.
- Renamed declaration files match their public type names.
- No test execution, pack or release verification is claimed by these compile checks.

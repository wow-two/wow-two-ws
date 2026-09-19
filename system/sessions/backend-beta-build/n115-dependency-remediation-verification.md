# N115 dependency remediation verification

*Last updated: 2026-09-16*

## Result

- removed the redundant direct `Microsoft.Extensions.Http` reference
- removed the obsolete explicit `Microsoft.SourceLink.GitHub` dependency
- upgraded `Datadog.Trace` to `3.53.0`
- upgraded `MailKit` and `MimeKit` to `4.18.0`
- upgraded `MessagePack` to `3.1.8`
- upgraded `Microsoft.AspNetCore.OpenApi` to `10.0.12`
- upgraded `AspNetCore.HealthChecks.MongoDb` to `9.0.0`
- pinned secure transitive versions for `Azure.Identity`, `KubernetesClient`, `SharpCompress`,
  `Snappier`, `SQLitePCLRaw.bundle_e_sqlite3`, `SSH.NET` and `System.Linq.Dynamic.Core`
- restored NuGet advisories to warning-as-error enforcement
- linked the shared options registration source into the web-free migration CLI
- adapted SMTP authentication to MailKit's non-null password contract

## Verification

- `dotnet restore WoW.Two.Sdk.Backend.Beta.slnx -m:1` passed
- `dotnet build WoW.Two.Sdk.Backend.Beta.slnx --no-restore -m:1` passed with zero errors
- `dotnet test WoW.Two.Sdk.Backend.Beta.slnx --no-build --no-restore -m:1` passed:
  399 passed, 1 explicitly skipped Kafka integration test
- live `dotnet list WoW.Two.Sdk.Backend.Beta.slnx package --vulnerable --include-transitive --no-restore`
  reported no vulnerable packages for all 14 projects using `https://api.nuget.org/v3/index.json`

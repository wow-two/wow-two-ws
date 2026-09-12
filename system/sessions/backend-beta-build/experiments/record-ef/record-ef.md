# Record EF comparison

> Source and output retained from the isolated 2026-09-12 experiment; twenty expected outcomes verified.

Run `dotnet run --project experiment.csproj` from this folder. The SDK pin and exact SQLite provider reference
match the experiment. Restore needs those packages available from the configured sources or local cache.

An assertion can confirm an expected failure. [Evidence](../../entity-record-ef-evidence.md) explains every
case, environment and limit; `results.txt` is the captured original run, not a fresh run of the SDK.

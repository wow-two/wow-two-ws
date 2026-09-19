# Exporter contract diagnostic

*Last updated: 2026-09-15*

Standalone observational harness for the existing SDK exporter implementations. It references the actual SDK project and executes the current built core assembly; it does not copy exporter implementations or add NuGet dependencies. It is retained session evidence, not a new shipping test project.

## Run

From the workspace root, with the SDK core already built:

```sh
dotnet run --no-restore --project system/sessions/backend-beta-build/experiments/exporter-contracts/experiment.csproj -p:BuildProjectReferences=false -p:UseSharedCompilation=false -m:1
```

Initial restore used the existing package cache. Native execution completed the final command with exit 0. SDK 10.0.300; runtime 10.0.8; CsvHelper package 33.0.1 (assembly 33.0.0.0); ClosedXML package 0.104.2 (assembly 0.104.2.0). No package versions changed.

## Evidence

- [Program.cs](Program.cs): 17 scenarios per exporter, 34 observed scenarios total, plus seven explicit CSV cancellation assertions.
- [results.txt](results.txt): final runtime output, including expected exception cases; seven assertions passed.
- [baseline-results.txt](baseline-results.txt): 30 scenarios captured before the CSV cancellation fix.
- [Verification report](../../exporter-conformance-verification.md): contracts and limits.

The 34 scenarios are observations inspected against source and documented contracts. The seven cancellation checks are explicit assertions: direct cancellation exceptions, caller token preservation, zero pre-canceled output, partial mid-canceled output, and an unrelated enumeration failure retaining its provider exception even when the token is canceled. The two intentional stream failures demonstrate partial output, not stable byte counts. `fr-FR` current culture distinguishes invariant CSV conversion from typed XLSX cells. XLSX inspection uses ClosedXML; it does not establish how every spreadsheet viewer renders built-in number formats. Unannotated column order is observed for the declared sample types, not guaranteed for all runtimes or row shapes.

# Exporter conformance verification

*Last updated: 2026-09-15*

## Scope

`N100` Exporter contract slice: existing `ITabularExporter`, `CsvTabularExporter`, and `ExcelTabularExporter`. Names, role folders and namespaces were already aligned. This pass verifies provider-specific schema, output, stream ownership and cancellation behavior. Root owns source XML and package guide edits; this report and the retained diagnostic harness are the verification lane.

## Baseline runtime evidence

- Diagnostic: [experiments/exporter-contracts](experiments/exporter-contracts/exporter-contracts.md).
- [Baseline output](experiments/exporter-contracts/baseline-results.txt): 30 observed scenarios, process exit 0.
- Actual built core assembly via project reference; exporter implementations were not duplicated.
- .NET SDK 10.0.300, runtime 10.0.8, process culture `fr-FR`.
- Package pins: CsvHelper 33.0.1 (assembly 33.0.0.0), ClosedXML 0.104.2 (assembly 0.104.2.0).
- No dependency or package version changes. These are observational diagnostics, not a counted assertion suite.

## Baseline observed contracts

| Concern | CSV | XLSX |
|---|---|---|
| Object schema | Public instance properties; sample public field/static property omitted | Public fields and properties, including sample static property |
| Header / ordering | Member names by default; `Name`, `Index`, `Ignore` attributes honored | Member names by default; `XLColumn` header/order/ignore honored |
| Unannotated ordering | Sample followed declaration order | Sample followed field/property discovery order; no general stable ordering claim |
| Row-type configuration | Class-level CSV delimiter/culture attributes did not override the writer's fixed invariant configuration | Provider-specific attributes only; CSV attributes did not alter XLSX |
| Empty typed objects | Header row only | `Sheet1`, table headers, no data rows |
| Scalar integers | One column with no header; empty emits no bytes | One column headed `Int32`; empty retains its header |
| Culture / values | Invariant decimal `12.5`; date `09/15/2026 00:00:00` despite `fr-FR` | Decimal/date are Number/DateTime cells, not CSV-like text; date uses built-in number format 14 |
| CSV bytes | UTF-8 without BOM, comma delimiter, CRLF, quoting for comma-containing text | Not applicable; binary XLSX document |
| Caller ownership | Stream remained open on success, enumeration failure, destination failure and cancellation | Same |
| Fresh nonseekable stream | Supported, no seek calls | Supported, no seek calls; generated workbook reopens |
| Existing seekable contents | Writes at current position; does not truncate a longer tail | Rewinds/replaces existing contents, observed `SetLength`; final position at end |
| Existing nonseekable prefix | Appends at current position | Appends; prefixed whole document failed reopening with `FileFormatException` |
| Enumeration failure | `WriterException` wraps original failure; header and first row remain | Original `InvalidOperationException`; no destination bytes written in sample |
| Destination failure | `IOException`; partial bytes remain | `IOException`; partial bytes remain |
| Pre-canceled token | `WriterException` wraps `OperationCanceledException`; header remains | `OperationCanceledException`; no bytes written |
| Cancellation during enumeration | `WriterException` wraps `OperationCanceledException`; first row remains | Not observed during synchronous phase: export succeeds with all three rows |

## Smallest conformance change

Keep current provider-specific behavior and correct the shared interface's blanket public-properties/header claim. Document per-provider schema, attributes, scalar/empty output, destination ownership, seek/truncation behavior, buffering and cancellation boundaries. Do not promise identical schemas across formats or invent a uniform schema configuration API in this documentation slice.

Require a fresh nonseekable or write-only destination for a standalone XLSX document. A readable, seekable XLSX destination is replaced; a write-only, seekable destination is buffered/copied at the existing position without truncation. CSV neither resets position nor truncates. Both failures can leave partial output and require caller-owned recovery.

Baseline CSV exposed cancellation through `WriterException.InnerException`. The parent applied a scoped fix: reject a pre-canceled token before constructing writers and rethrow the original inner cancellation only when the caller token is canceled. Unrelated provider failures retain their original exception path. Seven explicit regression assertions pass.

Excel uses a fully synchronous in-memory workbook construction/save phase; cancellation after the initial check is not observed. Documentation states this limit without adding a fake asynchronous API.

## Final verification

The core project compiled with **17 warnings, 0 errors**, exit 0. Build log: `/tmp/exporter-core-build.log`. No solution build was used.

```sh
dotnet build workbench/wow-two-sdk-beta/wow-two-sdk.backend.beta/engineering/codebase/wow-two-back-beta-sdk/src/WoW.Two.Sdk.Backend.Beta.csproj --no-restore -m:1 -v:q -p:UseSharedCompilation=false
dotnet run --no-restore --project system/sessions/backend-beta-build/experiments/exporter-contracts/experiment.csproj -p:BuildProjectReferences=false -p:UseSharedCompilation=false -m:1
```

The final harness ran against that newly compiled assembly: **34 observed scenarios and seven passing assertions**, exit 0. [Final output](experiments/exporter-contracts/results.txt); native command session `88947` completed, with no pending approval.

Verified CSV changes: pre-canceled calls throw `OperationCanceledException` with the original caller token and zero destination bytes; mid-enumeration cancellation throws `OperationCanceledException` with the original caller token and can leave partial output. An iterator that cancels the caller token but throws `InvalidOperationException` still produces `WriterException` with that original inner exception; the cancellation fix does not mask unrelated failures.

Additional precision checks: both sampled iterators were enumerated once; this observation is not a universal guarantee. XLSX write-only/seekable destinations behave like nonseekable destinations: the supplied prefix remains and the whole prefixed stream fails reopening. The root received this evidence for its destination contract wording.

## Boundaries

No SDK algorithm edits, whole-solution build, test runner, CI run, commit or publish in this verification lane. The parent owns the cancellation fix and documentation; this lane compiled and exercised them. No large-dataset throughput/memory benchmark, arbitrary custom converter test, every row type, or cross-viewer Excel rendering verification was attempted.

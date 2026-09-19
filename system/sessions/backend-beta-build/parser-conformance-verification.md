# Parser conformance verification

*Last updated: 2026-09-15*

## Scope

The Parser portion of the SDK role-placement sweep (`N100`): declarations live in their owning `Parsers/` directories,
concrete summaries start with `Parses`, interfaces start with `Defines`, and contracts describe actual parsing behavior.
The accepted role excludes operations on the parsed result. The SDK's role definition remains
[parser.md](../../../conventions/development/backend/dotnet/core/mla/constructs/behavior/parser.md).

No serializer, transport, renderer or mapper refactoring is included. Caption and CSV runtime algorithms are preserved.

## Declaration moves

All paths below are relative to the SDK's `engineering/codebase/wow-two-back-beta-sdk/src/`.
Each source filename moved from the owner directory directly into its `Parsers/` child, with the corresponding namespace suffix.

| Owner | Declarations |
|---|---|
| `Foundation/Time` | `CronExpressionParser`, `ICronExpressionParser` |
| `Media/Csv` | `CsvDocumentParser`, `ICsvParser` |
| `Media/Captions` | `CompositeCaptionParser`, `ICaptionParser`, `Json3CaptionParser`, `IJson3CaptionParser`, `SrtCaptionParser`, `ISrtCaptionParser`, `TtmlCaptionParser`, `ITtmlCaptionParser`, `VttCaptionParser`, `IVttCaptionParser` |

`CsvServiceCollectionExtensions` and `CaptionParsingServiceCollectionExtensions` import the new namespaces.
Their extension names, lifetimes and `TryAdd` behavior are unchanged. Cron had no existing registration reference.

`CompositeCaptionParser` uses a primary constructor; readonly field initializers preserve collaborator null guards.

## API boundary

`NextOccurrence` was removed from both `ICronExpressionParser` and `CronExpressionParser`.
Callers parse once, then invoke `GetNextOccurrence` on the returned Cronos expression.
`Foundation/Time/time.md` shows instance-based parser usage and the direct returned-expression operation.
The former example incorrectly called instance methods through the class name; it was corrected with this change.

The parser retains the existing selection heuristic: six space-separated fields select `IncludeSeconds`; otherwise use `Standard`.
Argument checks reject null/blank input, and Cronos rejects malformed/incomplete syntax. No partial expression is returned.

## Documented contracts

- CSV reads lazily from the current stream position without seeking, leaves the caller's stream open, and forwards cancellation to CsvHelper.
  The stream must remain readable/open through enumeration or disposal. UTF-8 with BOM detection is the reader default.
  CsvHelper mapping/data exceptions propagate during enumeration, potentially after earlier rows have been yielded; there is no rollback.
- Caption auto-detection is a precedence-ordered heuristic, not validity checking or a multi-parser fallback.
  Unknown/blank inputs produce no segments; explicit unsupported enum values also produce no segments.
- `ICaptionParser.TryParse` reports recognition only. It can return `true` with empty/partial segments and can propagate leaf exceptions.
- VTT consumes through the first blank line as a header, skips unsupported/timing-less or text-less cues, and omits adjacent rolling duplicates.
  Matched invalid clock values can throw `FormatException`; headerless content can lose its first cue. No partial list escapes an exception.
- SRT skips blocks without recognized timing or nonempty text. Invalid conversions return zero, but numeric clock-component ranges are not strictly checked.
- TTML rejects invalid XML syntax to an empty list, skips paragraphs without required content, and usually maps unsupported time tokens to zero.
  Nonfinite/out-of-range numeric offsets or time arithmetic can throw without yielding a partial list.
- json3 rejects invalid JSON syntax to an empty list and skips certain missing/nonrepresentable fields.
  Wrong JSON kinds can throw `InvalidOperationException`; out-of-range times can throw `OverflowException`.
  Text is whitespace-normalized but markup/entities are preserved.

The caption guide's blanket claim that every parser normalizes identically and never throws was replaced with these per-format contracts.
No new strict-validation, lossless-roundtrip or never-throw guarantee is introduced.

## Reference inventory and adoption

Search scope: all SDK source/guides, plus `*.cs` and `*.md` throughout `workbench/`, excluding generated dependency/build directories.
SDK declaration/import/example references were updated. No other SDK calls to the removed `NextOccurrence` wrapper remain.

TranscriptForge is the only found external parser consumer. When that repo is repinned to the newly published SDK,
add `using WoW.Two.Sdk.Backend.Beta.Media.Captions.Parsers;` to these consumer files:

- `workbench/ventures/10x-ventures-transcript-forge/engineering/codebase/transcript-forge.backend-services/TranscriptForge.Infrastructure/Youtube/YtDlpCaptionFetcher.cs`
- `workbench/ventures/10x-ventures-transcript-forge/engineering/codebase/transcript-forge.backend-services/tests/TranscriptForge.Tests/VttParserTests.cs`

Its `TranscriptForge.Api/Configurations/HostConfiguration.cs` calls `AddVttCaptionParser`; that extension's namespace is unchanged.
Consumer code remains against its existing published pin until release adoption; these unpublished namespaces were not inserted into that repo.

## Verification

- Source inventory confirms all 14 declarations have matching `Parsers/` directories and namespace suffixes.
- Search confirms no `NextOccurrence` wrapper calls or static `CronExpressionParser.Parse` examples remain in the affected SDK areas.
- `git diff --check` passed after this slice's edits.
- Compilation passed. The SDK core compiled with the moved declarations; the temporary Foundation.Tests harness
  build completed with 135 warnings and 0 errors. No SDK source changed between compilation and test execution.
- All 17 existing TranscriptForge VTT cases passed against the current SDK assembly: 0 failed, 0 skipped, .NET 10.
  Native escalation supplied VSTest's required local socket permission; the command exited 0 with no pending approval.
- The pre/post `engineering/planning/sweep.sh` outputs were identical (987 declarations). The battery retains
  existing findings elsewhere; it is not a whole-SDK conformance pass. Logs: `/tmp/parser-conformance-sweep-before.log`
  and `/tmp/parser-conformance-sweep-after.log`.
- No parser-specific SDK tests existed at intake. Existing consumer VTT cases can be compiled against current source via a temporary test import;
  running the consumer's unchanged pinned project alone would exercise the published package, not this SDK worktree.

### Existing-test import

`/tmp/parser-conformance-test-import.targets` imports the existing consumer test source only into
`WoW.Two.Sdk.Backend.Beta.Foundation.Tests`. It adds global imports for `Xunit` and the new parser namespace.
The consumer's interface-typed field triggers CA1859 under the SDK test project's analyzer settings;
the temporary import leaves that performance diagnostic as a warning for this test project only.
No SDK project file, analyzer policy or consumer source was edited for verification.

Commands ran serially from SDK `engineering/codebase/wow-two-back-beta-sdk/src/`:

```sh
dotnet build Foundation.Tests/WoW.Two.Sdk.Backend.Beta.Foundation.Tests.csproj --no-restore -m:1 -v:q -p:BuildProjectReferences=false -p:CustomAfterMicrosoftCommonTargets=/tmp/parser-conformance-test-import.targets
dotnet test Foundation.Tests/WoW.Two.Sdk.Backend.Beta.Foundation.Tests.csproj --no-build --no-restore --filter 'FullyQualifiedName~TranscriptForge.Tests.VttParserTests' -v:minimal -p:CustomAfterMicrosoftCommonTargets=/tmp/parser-conformance-test-import.targets
```

The final harness build reused the SDK core already compiled during the preceding project-reference build;
that earlier command used the same project/import without `BuildProjectReferences=false`.
Final build log: `/tmp/parser-conformance-build-final.log`; preceding compile log: `/tmp/parser-conformance-build.log`.
VTT coverage includes cues, timestamps, text cleanup, rolling duplicates, malformed lines, empty input and CRLF.
CSV, Cron, SRT, TTML and json3 received compilation/source-contract checks, not new direct runtime tests.

## Residual scope

Parser placement and role contracts are implemented. Runtime permissiveness/exception behavior remains as documented; strengthening it is a separate behavior change.
The wider SDK `N100` task still includes other roles, and this report does not close the whole task.
No staging, commit, publish or consumer repin was performed in this slice.

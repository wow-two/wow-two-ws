# SDK commit batches and follow-up verification

*Last updated: 2026-09-19*

## Scope

The user enabled ordinary SDK commits for this turn. The workspace commit switch defaults OFF, scopes ON
to one repository and task turn, and preserves signing, native approval, publishing and history restrictions.
The switch instructions and tests remain uncommitted in the workspace repository; the SDK grant covers only
`workbench/wow-two-sdk-beta/wow-two-sdk.backend.beta`.

## Signed SDK commits

The starting revision was `4abb2c8c5d2be8d967eae580e0f416802490b3b1` (`10.0.55-beta`).
The original working tree contained 875 changed paths with untracked files expanded. Rename detection produces
different diff counts; the user's UI count and collapsed `git status` are not file totals.

| Revision | Cohesive batch |
|---|---|
| `d318e18` | Release workflow, SDK pin, seven-package verifier |
| `3e86af8` | Dependency remediation and package boundaries |
| `c0d510b` | Foundation and mediator contracts |
| `6b18c12` | Persistence, migrations, tenant enforcement and data tests |
| `e9aa95e` | Identity roles and JWT trust |
| `95a6850` | Messaging, transport roles, test harness and inbox race fix |
| `868391e` | HTTP replay, host/error boundaries and test-host isolation |
| `b5c529e` | Media, geo, localization, email and remaining adapter conventions |
| `f0d07f5` | Follow-up role corrections and verification fixes |
| `1b42da1` | SDK documentation, sweep history and ForeverPin-first handoff |
| `b01f6b6` | Synchronized HTTP cancellation regression test |

Intermediate commits share renamed APIs; runtime verification
covers the combined source, not every intermediate revision. These are breaking beta changes. No push, tag publication
or NuGet publication was performed.

## Follow-up findings resolved

- Release tags are annotated so the workflow's `git push --follow-tags` includes the release tag.
- Inbox gate acquisition and retirement share a short lock. Previously, the last returning caller could remove and
  dispose a semaphore after a new caller incremented its user count and acquired the gate reference. Handlers still
  execute outside the dictionary lock; independent message IDs progress concurrently.
- Two new inbox tests cover concurrent retry churn, successful deduplication, canceled waiters and independent IDs.
- SQL statement parsing now uses `ISqlStatementParser` / `SqlStatementParser` in `Parsers/`, resolved through DI.
  The interface documents supported quoting and incomplete-input behavior; SQL grammar validation remains provider-owned.
- HTTP replay and timeout checks use capability `Extensions` names in `Extensions/`.
- Startup failure orchestration is `StartupFailureReportingService` in `Services/`, created before host DI is available.
- The startup child probe now passes its parent's build configuration. A Release parent previously launched the default
  Debug binary, weakening the release test and failing on a clean CI checkout without Debug artifacts.
- The HTTP cancellation test waits for the first handler invocation before canceling. Its old 50 ms timer could expire
  during client construction, so the assertion of one invocation depended on machine timing. All nine replay tests pass
  with the explicit signal; no production retry behavior changed for this test correction.
- The sweep script resolves its source root relative to itself and excludes generated `bin/` and `obj/` code.
- The final source inventory has no folded/banned role suffix, bare concrete `IEntity`, positional public/internal
  record, `<para>` block or severity glyph reported by the existing checks. Five static factories are allowed forms;
  the three remaining `Default` prefixes are the deny registration capability or implementations with shipped siblings.
- A separate authored-production-source check found no multi-line ordinary inline-comment runs.

These are bounded mechanical and targeted behavior checks. They do not certify every convention against every line
or complete the larger SDK vectors retained in the roadmap.

## Validation

`dotnet test WoW.Two.Sdk.Backend.Beta.slnx -c Release --no-restore -m:1 -v quiet` succeeded.

| Suite | Passed | Skipped |
|---|---:|---:|
| Data | 28 | 0 |
| Foundation | 125 | 0 |
| Identity | 20 | 0 |
| Mediator | 69 | 0 |
| Messaging | 124 | 1 |
| Migrations | 26 | 0 |
| Web | 63 | 0 |
| Total | 455 | 1 |

The Kafka skip is pre-existing. Analyzer warnings remain advisory.

Final committed revision: `b01f6b6834b848fc6e94b55f6a794336284c83e0`.
The solution was rebuilt with `ContinuousIntegrationBuild=true`, `RepositoryCommit` and `SourceRevisionId` set to that
revision: zero errors and 409 advisory warnings. All seven suites then ran with `--no-build --no-restore` against those
outputs and passed the same 455 tests with one skip.

All seven release projects packed successfully with `--no-build --no-restore` at local version `10.0.55-beta`.
`verify-release-packages.sh` passed all seven package/symbol pairs against the final revision. The temporary artifacts
and manifest are in `/tmp/wow-sdk-final-packages.hBBbn2`; this local validation is not a new NuGet publication.
The main-push workflow owns the next version bump and remote publication.

All eleven commits report a good GPG signature (`G`). `git status --porcelain=v1 -uall` is empty in the SDK repository.
The workspace's switch, convention changes and verification notes remain uncommitted and preserve its earlier dirty work.

The commit switch's 14 tests, existing 22 hook tests and four index-operation tests all pass. A live signed SDK commit
verified the ON path. OFF, repository/task scope, malformed state, Stop and new-turn expiry are covered by isolated tests;
this report does not claim a live Stop callback has already run. Native escalation restored the configured GPG signing
agent access and the test runner's local socket without changing signing or sandbox settings.
The helper explicitly returned the live grant to OFF before handover, and a second status read confirmed OFF.

## Handoff

The active SDK handoff owns the sequence: commit drain, fresh sweep, local verification and human publication,
ForeverPin migration, then analysis of missing SDK pieces. Other consumer repins remain tracked without jumping ahead
of ForeverPin. Shared EF/Dapper transactions, session boundaries, complete translation and other unfinished vectors
remain separate work, not silently included in this commit drain.

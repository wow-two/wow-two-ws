# Snippetline — executable documentation checks

W0012 · first-ten order 2 · proposed $39/month · research and clickable prototype, not a production release.

## Decision and product philosophy

Build a narrow proof around Markdown examples for small developer-tool teams shipping Node or .NET SDKs. The buyer is the maintainer or developer-relations lead who owns the documentation; the user is the engineer repairing a broken example. The job is to discover which published example stopped working after an SDK change and prove its correction before publication.

The promise is “every supported example has a reproducible result.” The core object is a versioned snippet check: source location, runtime fixture, target SDK version, result, and owner. The human decides whether a failure reflects stale documentation, a real SDK regression, or an intentionally unsupported example. Automation extracts explicitly tagged snippets and records results. It never rewrites published docs, merges changes, or executes customer code on our servers. Passing results are quiet by default; one changed failure opens one attention item.

This is a proposal to test, not a finding of unmet demand. Paid documentation product offers are verified; actual customer budgets and demand for independent snippet checking are unverified.

## Market challenge and first paid test

[GitBook](https://www.gitbook.com/pricing) offers documentation hosting, Git sync, version history and review workflows. [Mintlify](https://www.mintlify.com/pricing) offers documentation hosting and paid automation. These adjacent offers demonstrate suppliers charging for documentation tooling, not willingness to pay for this particular checker. Free scripts and existing CI tests are the direct substitute. A customer whose examples are already executable tests has little reason to add this product.

The proposed advantage is source-to-published-page traceability across a small set of tagged examples, with a useful failure report for a documentation owner. It must require less ongoing glue code than keeping Markdown snippets synchronized with separate tests. Begin with five repositories belonging to maintainers who have reported a stale example, not a broad documentation audience. The channel hypothesis is a useful free extractor and a public, reproducible demonstration of a stale example; no channel has been customer-validated.

Continue only if three repositories expose a real stale example and two maintainers accept a $39 paid pilot. Stop if most setups exceed one hour, existing CI already covers the problem, or owners do not return after a second release. Do not infer demand from downloads or passing checks.

## Core journey and product boundary

1. A maintainer tags a small allowlist of code fences and commits an explicit fixture. Empty onboarding shows one annotated Markdown example and the expected local report.
2. Customer CI runs the checks using its own runtime, dependency cache and credentials. It uploads bounded result metadata under a project-scoped ingest token.
3. The release view groups the latest results by source snippet; selecting a failure shows the precise source location and sanitized diagnostic.
4. A documentation owner records a handoff, edits in their repository, and reruns customer CI. A staged correction never changes a failed result by itself.
5. A new successful attempt resolves the attention item while retaining failure history. A local export provides the evidence used for the release decision.

Failure states: missing tags produce an explicit empty result; unsupported runtime returns “unsupported,” not “passed”; dependency/runner failure is distinct from snippet failure; absent uploads leave a stale run visible. Conflicts: duplicate upload returns the existing attempt; the same run key with a changed payload is rejected; an owner edit using an old version returns a conflict instead of overwriting. Published-page mapping is a customer-authored URL template; no crawl or hosting integration is required initially.

MVP: Markdown-only, tagged TypeScript and C# examples, offline fixtures, one project dashboard, source links, ownership, 30-day history and bounded JSON export. Non-goals: arbitrary language execution, hosted sandboxes, AI-generated automatic fixes, docs hosting, visual regression, live production API tests, repository write permissions, public failure badges, or enterprise SSO in the pilot.

## Domain model and invariants

| Entity            | Required content                                                  | Invariant                                                                            |
| ----------------- | ----------------------------------------------------------------- | ------------------------------------------------------------------------------------ |
| Project           | Tenant, repository identifier, allowed docs paths                 | Authorization comes from authenticated project membership, not a client tenant field |
| SnippetDefinition | Stable tag, path, runtime, fixture, source hash                   | Stable tag survives line movement; duplicate tags fail extraction                    |
| Run               | Commit SHA, SDK version, runner identity, started/completed times | Completion is immutable; incomplete runs cannot imply success                        |
| Attempt           | Run ID, snippet ID, result, bounded diagnostic                    | Only a new execution result changes pass/fail                                        |
| Assignment        | Snippet, owner, reason, row version                               | Owner change never resolves a failed check                                           |
| AttentionItem     | Failure signature and lifecycle                                   | One open item per current failure signature; recovery closes it once                 |

Results carry source hash and fixture hash so changes cannot silently inherit a previous pass. A run marked “passed” with zero selected snippets is rejected or explicitly marked empty. Keep earlier attempts when rerunning only part of a release.

## Proposed implementation contracts

These routes and events are new product proposals, not existing WoW2 SDK APIs:

| Route                                                    | Behavior and authorization                                                  |
| -------------------------------------------------------- | --------------------------------------------------------------------------- |
| `POST /api/projects/{id}/runs`                           | Project ingest token; accepts manifest and results together, 256 KB maximum |
| `GET /api/projects/{id}/runs/latest`                     | Tenant member; returns bounded latest summary plus pagination               |
| `GET /api/projects/{id}/snippets/{snippetId}/attempts`   | Tenant member; immutable run history                                        |
| `PUT /api/projects/{id}/snippets/{snippetId}/assignment` | Editor; requires expected row version and reason                            |
| `GET /api/projects/{id}/exports?runId=...`               | Tenant member; generates metadata export                                    |

Upload idempotency is `(projectId, collectorRunId, attemptNumber)` plus a canonical payload digest; repeated identical content returns the prior result. A different digest for that key returns `409`. Validate schema before committing the run and attention changes in one transaction. Proposed events: `RunRecorded`, `SnippetFailureChanged`, `SnippetRecovered`, `OwnerAssigned`. An outbox worker sends an optional digest once per transition and applies retention daily. Alert delivery failure never discards run evidence.

Use a small ASP.NET Core API and relational metadata store. A persisted outbox with a hosted worker is a proposed low-cost implementation; Microsoft documents `BackgroundService` and scoped dependencies, but that facility alone does not provide durable scheduling or delivery. Leases, retry limits and idempotency remain application work. [Microsoft hosted-service documentation](https://learn.microsoft.com/en-us/aspnet/core/fundamentals/host/hosted-services?view=aspnetcore-10.0).

Vue owns query state, filters, selection and review forms. Customer CI owns extraction and execution. Runtime packages must be pinned per fixture; repository code is untrusted input and remains in the customer's execution boundary. The website must never expose an “execute code” API.

## Data ownership and security

The customer owns source, fixtures and outputs. By default store source locations, hashes, bounded redacted diagnostics and status, not entire repositories or raw logs. Offer an opt-in small snippet excerpt only after local redaction. Never collect CI secrets. Ingest tokens are scoped, revocable and stored hashed; browser sessions cannot use them as user authentication. All queries include server-derived tenant scope. Limit log length, escape content, and forbid raw HTML rendering. Deletion removes active records and applies the documented backup retention window. Production retention and deletion semantics require implementation acceptance tests.

The mock stores synthetic checks and patch text in browser storage and exports only local synthetic data. This is deliberately richer display data than the proposed default production payload. No code executes, notifications send, or repositories change.

## WoW2 integration boundaries

The installed public `@wow-two-beta/ui-vue` 0.0.7 declaration files were inspected on 2026-09-29. `Button`, `CodeText`, `Modal` and `Timeline` are exported components. Their availability supports a production mapping proposal; their detailed props, accessibility and interaction fit still need an adapter spike. Native semantic controls in this prototype are permitted by its research contract. No `SnippetRunner`, repository integration, code-execution client or domain workflow is claimed to exist in that package. The proposed backend would reuse current WoW2 authentication/configuration/observability packages only after inspecting their actual exports in the chosen production repository; no backend SDK API availability is assumed here.

## Price, cost and operating gate

Free: local extractor and public-repository checks, without hosted private history. Proposed paid: $39/month per small organization for private history, ownership and release reports, capped initially at 5 repositories and 200 uploaded results/day. Lifetime hosting is unsuitable for recurring retention and operational costs; a separate offline extractor license could be tested later. These are hypotheses, not current sales.

Budget design: estimated $20–40/month total early infrastructure, comprising $12–22 app/database allocation, $4–8 backups/log retention and $4–10 bounded delivery/domain allocation. These are planning allowances, not supplier quotes; founder labor, taxes, payment fees and customer CI minutes are excluded. No LLM or hosted compute is required. Stop ingestion at explicit plan quotas rather than accepting unbounded logs. The ~$300/month expansion budget opens only after revenue covers it and measured retention/usage justify dedicated capacity. Activation is the first useful failure with a named owner; retention is use on a second release. At the undiscounted $39 price, 129 paying organizations produce $5,031 gross MRR before fees, taxes, refunds or churn; this is arithmetic, not a revenue forecast.

## Design references and rationale

The [GitHub Actions run-log guide](https://docs.github.com/en/actions/how-tos/monitor-workflows/use-workflow-run-logs) documents run selection, expanded failing steps, source-line navigation, reruns and downloads. The extracted interaction move is failure-first drilldown with explicit attempts. This was a documentation/text inspection, not a visual audit of a live logged-in GitHub product. Our three-column composition is an original inference: checks left, example and compiler report center, owner/release context right. It keeps the repair decision next to the evidence rather than placing charts above it.

Screens: release workbench; snippet result; attempt history; assignment dialog; all-passing filtered empty state. At widths below 768 px, panels stack in reading order; from 768 px the check list and code share a row; at 1024 px context becomes a third column. Code scrolls within its panel. Native dialogs preserve keyboard focus behavior; status words accompany color.

| Semantic token                       | Light meaning                                   | Dark meaning                                      |
| ------------------------------------ | ----------------------------------------------- | ------------------------------------------------- |
| `--canvas` / `--surface`             | Quiet canvas and elevated paper                 | Low-glare canvas and distinct elevated panel      |
| `--ink` / `--muted`                  | Primary text / supporting context               | High contrast text / readable secondary text      |
| `--accent` / `--accent-soft`         | Selected check, primary action / selection fill | Same meaning with shell contrast-adjusted values  |
| `--danger`, `--warning`, `--success` | Failed result, pending decision, passing result | Identical semantics, never the sole status signal |

Proposed reusable controls: result badge, source-location label, attempt timeline, bounded code viewer and ownership handoff form. The shell's three palettes are proposals; no design selection is treated as locked.

## Staged delivery and acceptance

1. Validate five real repositories using a throwaway local extractor and manually reviewed output; measure installation time and failure usefulness.
2. Build a fixture-only CLI and protocol contract; test duplicate tags, empty runs, timeouts, retries and result/source mismatch.
3. Build tenant-scoped ingestion, read UI, assignment concurrency and JSON exports; prove replay safety and tenant isolation.
4. Add capped retention, optional change digest and billing only after paid-pilot commitments. Complete backup/restore and deletion drills before hosting customer metadata.

Production acceptance: a changed snippet cannot inherit a stale pass; retries do not duplicate attempts; owner assignment does not alter results; an incomplete run is visible; failure/recovery events are deduplicated; raw secrets do not appear in stored logs; exported totals equal filtered run evidence; keyboard navigation works at 390/820/1440 px in both themes. Prototype acceptance covers local interactions only. Root owns consolidated compilation and browser verification records.

## Exact prototype smoke scenario

Start with the shell's reset for this product.

1. Verify 2 failing, 2 passing and 4 attempts; “Walk through every page” is selected.
2. Click **Assign owner**, then **Save assignment** with blank fields. Validation keeps the dialog open.
3. Select **Maya Chen**, enter `Review the pagination response change`, and click **Save assignment**. The detail owner changes; failing remains 2.
4. Click **Simulate rerun** without a patch. It still fails; attempts becomes 5.
5. Click **Apply sample fix**. The sample uses `page.items`; the last result remains failed.
6. Click **Simulate rerun**. Failing becomes 1, passing becomes 3, attempts becomes 6.
7. Click **Run history (3)** and verify failure, failure, pass across the three attempts.
8. Click **Export run report**. Inspect `snippet-check-report.json`: summary is 1 failing, 3 passing, 6 attempts with the saved owner.
9. Refresh and verify saved state; reset restores the initial synthetic records.

Implemented mutations: assignment, staged sample fix and simulated rerun. Implemented detail, filtering, validation, export and persistence use the shared shell API. Real extraction, CI ingestion, billing, permissions, reminders and publishing remain mocked or unimplemented.

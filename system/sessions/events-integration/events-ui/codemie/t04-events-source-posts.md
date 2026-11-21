# T04 — Events: source posts on an event and the event page v2

*Last updated: 2026-11-21 · owner: `ocharo - sources and ai processing` (`local_c7cc71e5-c3ba-496c-98ca-6d0f00404e66`)*

Spec for a headless CodeMie run (`codemie-claude`, Sonnet). No human answers mid-run: when this spec does not settle
a choice, stop and end your reply with `QUESTION:`; when finished, end with `DONE:` and the evidence; when a rule
below stops you, end with `BLOCKED:`. Runs after T03 and T02; it touches only `wow-two-sdk-beta.events`.

## Goal

An event gathered from several sources shows each source's own post: the source's name, the post's own title, its
language, when it was posted, and a link to open it at the source. Today an event lists its sources by name and URL
only. Items UI07 and UI08 of `system/sessions/events-integration/events-ui/ocharo-events-ui-analysis.md` (§ 6). The
Ocharo app adopts the release later; the UI lane re-pins and reads back on dev.

## Inputs

Paths are relative to the WoW2 root `~/Projects/10x-ws/workbench/career/engineering/wow-two/wow-two-ws`.

- Repo: `workbench/wow-two-sdk-beta/wow-two-sdk-beta.events` (`E`). Code under `E/engineering/codebase/`:
  `events.backend-services/` (`EventSourceModel` in `packages/Abstractions/CatalogEvents/EventSourceModel.cs`, intake
  in `packages/Module/Intake/IntakeProcessor.cs`, observations, migrations `packages/Module/Migrations/`) and
  `events.frontend-services/packages/fe-events/` (`EventDetail`, `EventMediaCard`, the `./contracts` mirror).
- Specs: the analysis doc above, § UI07 and § UI08; the SCFD payload `wow2.event.v1` in
  `workbench/wow-two-sdk-beta/wow-two-sdk-beta.harvest/engineering/architecture/contract.md` (read only).

## Decisions (pre-answered)

| Situation | Do |
|---|---|
| Where the post fields live | New nullable columns on the event-source row: `title`, `language`, `posted_at`, `role`, written at intake from the observation that touches that source; a new migration pair `NNN-source-posts/{Apply,Rollback}.sql` (next free number) that also backfills them from each source's latest observation |
| `title` | the payload's source title as written (not the machine English title); null for an import or a curator's entry |
| `language` | the payload's language tag for that post (BCP 47, e.g. `ru`, `uz-Latn`); null when absent |
| `posted_at` | the post's publication time from the payload; null when the source gave none |
| `role` | always null in this ticket (UI11 fills it later); keep the field in the model and mirror |
| Who may read them | anyone with `events.read`; a member without `events.review` sees them |
| No post text, no media | never copy post text or images onto the source row |
| Posts section on the event page | under the facts, heading "Posts": one row per source -- source name, own title (the event's title when null), language by name (the kit's `languageName`), posted date in the reader's locale, a role pill when not null, and "Open at source ↗" (only for a safe `http(s)` URL) |
| Tracking form placement | from `lg` up the tracking form moves into a right side panel (sticky); below `lg` it stays where it is |
| Card source line | the card's panel names its sources by display name, `afisha · uzexpocentre`, when no deadline line shows (the existing rule) |
| A test asserts the old behaviour | update it to this spec |
| A gate fails in code this spec did not touch | stop that step; `BLOCKED:` with the failing test and its output tail |
| A file you must commit holds changes you did not make | leave it uncommitted, finish the rest, name it in `DONE:` |

## Rules

- Read first: `E/CLAUDE.md`, `E/engineering/development/{rules,backend-guidelines,frontend-guidelines,iteration-guide}.md`,
  `E/engineering/scripts/scripts.md` § Releases, `~/.claude/conventions/git.md`
- Never edit an applied migration; the contract lives in `packages/Abstractions`; Module and Client both implement it and
  `Events.Tests.Conformance` runs against both
- English only; stage explicit paths only; commit subjects follow `~/.claude/conventions/git.md` (subject only, no body)
- Sourced records serve internal use only and credit their source by the link: the "Open at source" link is required

## Steps

1. Backend: model fields, migration with backfill, intake writes, read path, HTTP mirror, Client, conformance.
   Integration test: an event with two sources (an Afisha post and an Uzexpocentre post), each with its own title and
   posted date, read by a member without `events.review`.
2. fe-events: contracts mirror; `EventDetail` Posts section and `lg` side panel; the card source line. Vitest: two posts
   render with their source names, titles, languages in words, dates and links; a null title falls back to the event's
   title; no link for a non-`http(s)` URL; the side panel at 1440 px and the stacked form at 390 px.
3. Gates: backend `dotnet build` of the solution and `dotnet test` on every tier (Docker is up; PostgreSQL through
   Testcontainers); frontend in `packages/fe-events`: `pnpm typecheck`, `pnpm lint`, `pnpm format:check`, `pnpm test`,
   `pnpm build`, `pnpm check:package`
4. Version track: the newest `E/engineering/planning/version-track/v*/v*.md` gets one iteration, "Source posts on an
   event", `- [x] Ability to …` lines
5. Commit, push `main`, and follow `scripts.md`: the push publishes the changed packages (`be-v*`, `fe-v*` tags pushed by
   CI) and the image; wait for each run to finish (`GH_TOKEN="$(gh auth token -u sulton-max)" gh run list …`), then
   `git pull --ff-only` if CI added a commit, and confirm `npm view @wow-two-beta/fe-events version`

## Done when

- The integration test above passes, and every backend tier and the fe-events gate pass, quoting each command's last lines
- `@wow-two-beta/fe-events` newer than `0.0.20` is on npm; the be packages and the image published on the pushed `HEAD`
- The version track names the iteration

## Never

- Edits outside `wow-two-sdk-beta.events`; production deploys; worktrees; force pushes; editing an applied migration
- `git reset --hard`, `checkout --`, `restore`, `stash` on changes you did not make
- Printing a secret, or writing a host address, token, phone number or password into a file, commit or report

## Report

End with `DONE:` then at most 10 lines: the fe-events version, the be package version, the image version, commit shas,
CI run ids, gate result lines, the migration name, anything left uncommitted.

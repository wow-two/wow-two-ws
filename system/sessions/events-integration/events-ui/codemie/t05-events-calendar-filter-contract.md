# T05 — Events: the calendar's filter contract

*Last updated: 2026-11-21 · owner: `ocharo - sources and ai processing` (`local_c7cc71e5-c3ba-496c-98ca-6d0f00404e66`)*

Spec for a headless CodeMie run (`codemie-claude`, Sonnet). No human answers mid-run: when this spec does not settle
a choice, stop and end your reply with `QUESTION:`; when finished, end with `DONE:` and the evidence; when a rule
below stops you, end with `BLOCKED:`. Runs after T04, on top of its fe-events release; it touches only
`wow-two-sdk-beta.events`.

## Goal

The calendar page reuses the feed's filters: whatever a member picked in the feed's facet bar (search, stages, kinds,
cities, sources, date presets) carries into the calendar's window query for the dates on screen. Item UI14 of
`system/sessions/events-integration/events-ui/ocharo-events-ui-analysis.md` (§ 6). The calendar views stay with the
calendar lane; this ticket only exposes the contract from the kit.

## Inputs

Paths are relative to the WoW2 root `~/Projects/10x-ws/workbench/career/engineering/wow-two/wow-two-ws`.

- Repo: `workbench/wow-two-sdk-beta/wow-two-sdk-beta.events` (`E`); kit `E/engineering/codebase/events.frontend-services/packages/fe-events/`
  (`EventsFeed` and its facet bar state, the tracking client and `TrackingQuery` mirror in `./contracts`).
- Spec: the analysis doc above, § UI14 (and § UI04 for the query fields).

## Decisions (pre-answered)

| Situation | Do |
|---|---|
| Shape of the contract | a composable in `./kit`, `useEventsFilters()`, that owns the facet bar state (the same state `EventsFeed` uses today; the feed is refactored onto it, behaviour unchanged) and exposes `toWindowQuery(from, to)` returning a `TrackingQuery` with every picked filter plus `from` / `to` |
| Sharing between pages | the state serialises to and from URL query params (`q`, `stages`, `kinds`, `cities`, `sources`); a consumer passes the same router query to both pages, so moving from feed to calendar keeps the filters |
| Date presets in the feed | a window query ignores the feed's date preset; the window's `from` / `to` win |
| Month- and year-precision events | pass through the window query with their precision unchanged, so the calendar can draw them in a strip (CAL05) |
| The calendar views | not in this ticket |
| A test asserts the old behaviour | update it to this spec |
| A gate fails in code this spec did not touch | stop that step; `BLOCKED:` with the failing test and its output tail |

## Rules

- Read first: `E/CLAUDE.md`, `E/engineering/development/{rules,frontend-guidelines,iteration-guide}.md`,
  `E/engineering/scripts/scripts.md` § Releases, `~/.claude/conventions/git.md`
- English only; stage explicit paths only; commit subjects follow `~/.claude/conventions/git.md` (subject only, no body)
- Export the composable and its types from `./kit`; `pnpm check:package` must list them

## Steps

1. Build `useEventsFilters()` and move `EventsFeed` onto it.
2. Vitest: a filter set in the feed (a stage, a city, a source and a search) yields a window query for 2026-12-01 to
   2026-12-31 carrying all four plus `from` / `to`; the feed's date preset is ignored there; the URL round-trip
   restores the same state; a month-precision event passes through with `precision: month`.
3. Gates in `packages/fe-events`: `pnpm typecheck`, `pnpm lint`, `pnpm format:check`, `pnpm test`, `pnpm build`,
   `pnpm check:package`
4. Version track: the newest `E/engineering/planning/version-track/v*/v*.md` gets one iteration, "Calendar filter
   contract", `- [x] Ability to …` lines
5. Commit, push `main`; the push publishes fe-events (`fe-v*` pushed by CI, `scripts.md`); wait for the run; confirm
   `npm view @wow-two-beta/fe-events version`

## Done when

- Every gate passes, quoting each command's last lines; the new tests are in the run
- A fe-events version newer than T04's is on npm, and the version track names the iteration

## Never

- Edits outside `wow-two-sdk-beta.events`; changes to the backend; production deploys; worktrees; force pushes
- `git reset --hard`, `checkout --`, `restore`, `stash` on changes you did not make
- Printing a secret, or writing a host address, token or password into a file, commit or report

## Report

End with `DONE:` then at most 8 lines: the fe-events version, commit sha, CI run id, gate result lines, the exported names.

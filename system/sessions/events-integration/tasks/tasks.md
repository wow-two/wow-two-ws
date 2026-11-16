# Next tasks for ChatGPT

*Written 2026-11-16 by the events-integration orchestrator, from three read-only reviews and a live check of Ocharo
Events on dev. 109 tasks.*

ChatGPT (Codex) builds these tasks. Each task is a spec: repo, why, what to do, a pass/fail check and its
dependencies. Each repo's backlog carries one row per task under `## Specced next`, pointing here by id.

| File | Ids | Covers |
|---|---|---|
| [tasks-scfd.md](tasks-scfd.md) | S01-S35 | SCFD's own side: finishing ChatGPT's uncommitted work, sources, matching, delivery, console, release |
| [tasks-events-path.md](tasks-events-path.md) | E00-E33 | SCFD → WoW2 Events → Ocharo Events: field map, live dev check, intake, facts, duplicates, tests |
| [tasks-platform.md](tasks-platform.md) | O01-O16, F01-F10, A01-A08, V01-V06 | Ocharo services and prod release, fe sdk, AI, Events server |

## Rules

- Read the target repo's `CLAUDE.md` and the rules at the top of each task file first.
- One task per commit where it fits; the commit records the work in the repo's active version track and deletes the
  task's backlog row, together with any older row the task covers.
- Run the task's "Done when" check and keep its output tail in the commit's version-track entry.
- `#N` cites [events-integration.md](../events-integration.md); decisions there and in
  [scfd-console-analysis.md](../scfd-console/scfd-console-analysis.md) bind unless the developer reverses one.
- No host addresses, tokens, phone numbers or personal names in any repo; `wow-two-sdk-beta.harvest` is public.
- Commit and push only as the repo's git flags allow; never force, stash, reset or use a worktree.

## Pull order

1. Finish open work: S01-S07 (ChatGPT's harvest work, released as `v0.2.7`), F01-F04 (the toast overhaul, released).
2. SCFD's events reach Ocharo: E00, E01, S18, S08, S09, E02, E03, E04, E30.
3. Facts shown right in Ocharo: E25, E33, E12, E05, E06, S13, E07, E08, E09, E10, E11, E15, E16, E13, E14.
4. Tests and scale: E26, E27, E28, E29, E19, E20, E21, E22, E23, E24, E17, E18.
5. Sources toward the 100 registries (#51): S10, S19, S20, S11, S12, S21-S26.
6. Console: S27-S32.
7. Ocharo prod and services: O13, O14, then O15-O16 on the developer's go, then O01-O12.
8. SDK lifts and the Events server: F05-F10, V01-V06.
9. AI, once the `ev-ai` lane's paused work is committed: A01-A08, then S14-S17.
10. Release: S33, S35; S34 on the developer's go.

## Needs the developer

- O15, O16: prod Identity cutover (G3) and the Files tenant on prod are parked.
- S16: promote AI relevance into Ocharo's delivery after the shadow week.
- S34: drop IP-lease pools and CAPTCHA solving from the public image.
- E31, E32: a triage view for untracked sourced events; a per-source thumbnail policy.
- F01: `engineering/features.md` in the fe sdk, asked for in ChatGPT, is against the version-track convention.

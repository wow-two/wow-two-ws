# Next tasks for ChatGPT

*Written 2026-11-16 by the events-integration orchestrator, from three read-only reviews and a live check of Ocharo
Events on dev. 109 tasks; Telegram delivery (I01, V07, O17) added 2026-11-17.*

ChatGPT (Codex) builds these tasks. Each task is a spec: repo, why, what to do, a pass/fail check and its
dependencies. Each repo's backlog carries one row per task under `## Specced next`, pointing here by id.

| File | Ids | Covers |
|---|---|---|
| [tasks-scfd.md](tasks-scfd.md) | S01-S39 | SCFD's own side: finishing ChatGPT's uncommitted work, sources, matching, delivery, console, release |
| [tasks-events-path.md](tasks-events-path.md) | E00-E33 | SCFD → WoW2 Events → Ocharo Events: field map, live dev check, intake, facts, duplicates, tests |
| [tasks-platform.md](tasks-platform.md) | O01-O17, F01-F11, A01-A08, V01-V07, I01, B01, W01 | Ocharo services and prod release, fe sdk, AI, Events server, Telegram delivery, be sdk, workspace |
| [tasks-ocharo-events.md](tasks-ocharo-events.md) | OE01-OE12 | Ocharo's events logic: what enters, the team's workflow, what the app shows, digests (review 2026-11-19) |

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

1. Finish open work: S01-S07 (ChatGPT's harvest work, released as `v0.2.7`; S03 and S07 have leftovers), F01-F04 (the
   toast overhaul, released); then the v0.2.7 review's fixes S36, S37, S39, F11, and B01 (Files CI fails on it).
2. SCFD's events reach Ocharo: E00, E01, S08, S09, S18, E02, E03, E04, E30.
3. Facts shown right in Ocharo: E25, E33, E12, E05, E06, S13, E07, E08, E09, E10, E11, E15, E16, E13, E14; then
   Telegram delivery on Ocharo's schedule: I01, V07, O17.
4. Tests and scale: E26, E27, E28, E29, E19, E20, E21, E22, E23, E24, E17, E18.
5. Sources, only after stages 2-4: S10, S19, S20, S11, S12, S21-S26, then the registries of ~700 more Ocharo sources
   (developer, 2026-11-17: "we can do integration first then work on registries of other 700 sources"; #51 set 100).
6. Console: S27-S32.
7. Ocharo prod and services: O13, O14, then O15-O16 on the developer's go, then O01-O12.
8. SDK lifts and the Events server: F05-F10, V01-V06.
9. AI, once the `ev-ai` lane's paused work is committed: A01-A08, then S14-S17.
10. Release: S33, S35; S34 on the developer's go.

## Needs the developer

- O15, O16: prod Identity cutover (G3) and the Files tenant on prod are parked.
- S16: promote AI relevance into Ocharo's delivery after the shadow week.
- S34: drop IP-lease pools and CAPTCHA solving from the public image.
- E31: a triage view for untracked sourced events.
- S38: what the Joymee and BirBir collectors may keep about sellers (names, street address, exact coordinates).
- W01: whether the two new `must`s (tooltip on icon-only controls, `ImageOff`) apply ecosystem-wide or to SCFD only.

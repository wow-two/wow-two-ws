# session: ui-beta-build

*Last updated: 2026-04-29*

- Repo: `workbench/wow-two-sdk-beta/wow-two-sdk-beta.ui/`
- Plan: [ui-beta-roadmap.md](../../../docs/ui-beta-roadmap.md) (P1–P7)
- State: [context.md](./context.md) ← read first

Recommended chat name: `wow-two - ui-beta-P{N}-{slug}`.

## Procedure

1. Read [context.md](./context.md) — 30-second snapshot
2. Pick the next sub-task from the current phase (cross-ref roadmap if needed)
3. Do the work in the repo
4. After each meaningful milestone: re-open [context.md](./context.md), update only what changed (1–2 lines), trim stale items, bump *Last updated*
5. Closing a chat: ensure context.md reflects final state; if a phase completed, update its status in the roadmap

## What lives where

| Concern | File | Volatility |
|---|---|---|
| Plan (P1–P7) | `docs/ui-beta-roadmap.md` | Rare |
| Procedure (this) | `session-ui-beta-build.md` | Almost never |
| Current state | `context.md` | Frequent, kept compact |
| Component specs / ADRs | repo's `docs/` | Per-component |

## context.md scope

**In scope**: current phase, last meaningful action, open items, live pointers (latest version, last commit SHA, components shipped count).
**Out of scope**: every commit, long reasoning, decisions already made, per-component prop debates.

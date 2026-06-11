# session: backend-beta-build

*Last updated: 2026-05-04*

- Repo: `workbench/wow-two-sdk-beta/wow-two-sdk.backend.beta/`
- Plan: repo's `docs/analysis/philosophy/targets.md` §6 (P0–P6 phase mapping)
- State: [context.md](./context.md) ← read first

Recommended chat name: `wow-two - backend-beta-{slug}`.

## Procedure

1. Read [context.md](./context.md) — 30-second snapshot
2. Pick the next sub-task from the current phase (cross-ref repo's `targets.md` if needed)
3. Do the work in the repo
4. After each meaningful milestone: re-open [context.md](./context.md), update only what changed (1–2 lines), trim stale items, bump *Last updated*
5. Closing a chat: ensure context.md reflects final state; if a phase completed, update its status in repo's `targets.md`

## What lives where

| Concern | File | Volatility |
|---|---|---|
| Plan (P0–P6) | repo's `docs/analysis/philosophy/targets.md` §6 | Rare |
| Procedure (this) | `session-backend-beta-build.md` | Almost never |
| Current state | `context.md` | Frequent, kept compact |
| Package registry | repo's `docs/conventions/package-registry.md` | Per-package |
| Conventions + templates | repo's `docs/conventions/`, `docs/templates/` | Rare |
| Deep analysis (per extraction) | `*-extraction-analysis.md` files in this folder | Per-batch |

## context.md scope

**In scope**: current phase, last meaningful action, open items, live pointers (package count, last commit SHA, sln build status).
**Out of scope**: every commit, long reasoning, decisions already made, per-package internal debates.

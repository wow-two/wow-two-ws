# Git flags — context

*Last updated: 2026-09-29*

## State

- Live in wow-two-ws, eis-ws and mft-10x-ws: two flags (`commit`, `push`) in one store per workspace,
  `.codex/git-flags.json`, with `*` defaults, per-repository overrides, a hash-chained log, pushed-history refusal,
  the store edit guard in both agents and Claude `SessionStart` status (G0–G7).
- Migrated (G5): wow-two-ws 25 overrides across 18 repositories (ocharo repositories included until ocharo-ws gets its
  own store); mft-10x-ws `.` commit and push; eis-ws had none. Old `.git` records deleted.
- 10x-ws: engine sync only (`COMMITS = "open"`, no module). eis-ws: STRICT kept, `pr checkout` block moved into its
  CONFIG. mft-10x-ws: kept `switch` (developer, 2026-09-29), contrary to the brief's "open".
- Product repository docs (point 6): 12 files in 11 repositories point at the workspace rule; Haven and TNIS
  committed, the rest staged or listed.
- Left uncommitted: wow-two-ws (other lanes' index), 10x-ws (other lanes' guard edits), eis-ws (EPAM); mft-10x-ws
  staged for the developer.
- Live check: a whole-message `~git_on commit` recorded through Claude and unlocked five repositories (2026-09-29).
- Deferred by the developer: re-trust `.codex/hooks.json` in Codex `/hooks` (wow-two-ws, eis-ws, mft-10x-ws).
- mft-10x-ws: another lane is adding a peer-workspace reader (`.codex/peer-workspaces.json`) on top of the staged
  store engine; commit together once that lane finishes.
- Deferred: ocharo-ws install and its store, until the developer says the other chat has left (asked 2026-09-29:
  not yet); `ventures.ocharo-studio/CLAUDE.md` pointer with it.
- Procedure: [session-git-flags.md](session-git-flags.md).

# Session — git flags everywhere

*Last updated: 2026-09-29*

> Brief for the chat that rolls the developer's git-flag decisions out to every workspace and every product repository.
> Analysis and open points: [docs/git-flags.md](../../../docs/git-flags.md). State: [context.md](context.md).

## Scope

| Workspace | Root | Guard today |
|---|---|---|
| wow-two-ws | `/Users/max/Projects/10x-ws/workbench/career/engineering/wow-two/wow-two-ws` | engine source, `COMMITS = "switch"`, 4 flags |
| 10x-ws | `/Users/max/Projects/10x-ws` | `COMMITS = "open"`, older engine |
| mft-10x-ws | `/Users/max/Projects/10x-ws/workbench/fam/mft-10x-ws` | `COMMITS = "open"`, hooks untracked |
| eis-ws | `/Users/max/Projects/Company/EPAM/eis/eis-ws` | `STRICT`, `COMMITS = "switch"`; EPAM repository — never commit there |
| ocharo-ws | `.../wow-two-ws/workbench/ocharo-hq/ocharo-ws` | none yet |

Product repositories live in each workspace's `workbench/`; each is its own Git repository.

Read first in wow-two-ws: `.claude/hooks/guard-git.py`, `.codex/hooks/commit_permission.py`,
`.claude/hooks/commit-switch.py`, `.codex/hooks/claude_adapter.py`, `.codex/hooks.json`, `.claude/settings.json`,
`.codex/commit-permission.md`, `/Users/max/.codex/conventions/git.md` § repository-commit-permission,
`conventions/development/repo/version-control/git.md` § Discipline.

## Decided

1. Two flags. `commit` covers everything local: the ordinary `commit -m` plus history rewrites (amend, rebase,
   cherry-pick, revert, merge, am, subtree, soft or mixed reset to a commit); rewrites keep the lane check and refuse
   commits already on the upstream. `push` covers everything that reaches GitHub: the ordinary push plus every gh
   write. The banned list and the free list stay as they are. Directives stay: `~commit_*`, `~push_*`,
   `~git_on|off <kinds> <repo>...`, `~git_status <repo>...`.
2. Store: one file per workspace, `<workspace>/.codex/git-flags.json`, gitignored, beside the engine that reads it;
   workspace defaults plus per-repository overrides keyed by the repository's path inside the workspace; lock and
   atomic replace; per-change evidence (session, turn, prompt, time); a hash-chained change log beside it, so a hand
   edit is detectable and the guard fails closed.
3. Edit guard: the store sits inside the workspace, where agents can write, so guard it in both agents. Claude
   `PreToolUse` on `Write|Edit|MultiEdit|NotebookEdit` refuses the store and its log; `guard-git.py` refuses shell
   commands that name them; Codex adds `apply_patch` to its `PreToolUse` matcher, which the developer re-trusts in
   `/hooks`. Hooks stay a guardrail, not a security boundary.
4. Parity: one module serves both agents; Claude's `SessionStart` shows the flags; one cross test proves a directive
   recorded through each adapter is honored by the other.
5. Coverage: the developer opens chats only at a workspace root, so each workspace's own hooks cover every
   repository inside it. No per-repository or user-level wiring.

## Analyze, then build

Every point below is decided; report each finding in one line and ask only when a fact contradicts a decision.

6. Product repository docs: `ventures/10x-ven-haven/CLAUDE.md` ("never push, amend or rewrite history"),
   `ventures/ventures.tnis/CLAUDE.md` and `ocharo-ws/workbench/ventures.ocharo-studio/CLAUDE.md` restate the old git
   rules. Replace each with a pointer to the workspace rule, and grep every product repository for other copies.
7. Migration: move each `<git-dir>/codex-<kind>-permission.json` record into the store (history → commit, gh → push,
   drop the inert `config` records), then delete the old files. Find them with
   `find <workspace> -path '*/.git/codex-*-permission.json'`.
8. Rollout: copy the engine (everything below the CONFIG block) to the other four workspaces and keep each CONFIG.
   10x-ws and eis-ws carry other lanes' uncommitted guard edits: merge around them, never revert, and stop on a
   conflict. 10x-ws and mft-10x-ws keep `COMMITS = "open"` with no flag module (engine sync only); eis-ws keeps
   `STRICT` with its switch; ocharo-ws installs the module with `COMMITS = "switch"`. ocharo-ws sits inside wow-two-ws: its
   repositories' flags live in `ocharo-ws/.codex/git-flags.json` (decided), and the guard reads the store of the
   innermost workspace that has one, from whichever workspace the chat runs in. Another chat works in ocharo-ws now:
   leave it for last. Until it has its own store, its repositories fall under wow-two-ws's store. When everything
   else is done, ask the developer whether ocharo-ws is free, then install and migrate there.
9. Change path, overview and lifetime (G2–G4, decided): directives stay the only way to change a flag, for the
   developer too; `~git_on|off <kinds> *` sets or clears the workspace default for every repository, present and
   future; a per-repository directive sets an override, and the effective flag is the override, else the default;
   `~git_status *` lists the defaults and every override; flags never expire.
10. When the store lands, tell the developer that `~git_on commit *` lets agents commit every repository, since the
   version-track migration that follows commits per repository.

## Rules

- A flag changes only through the developer's whole-message directive; never infer one from prose. The one-time
  migration is configuration work.
- Chats share working trees: check `git status` first, never revert another lane's change, stage only your paths.
- Auto mode may refuse hook edits; then ask the developer to approve guard edits.
- wow-two-ws's index holds other lanes' staged files: leave wow-two-ws uncommitted and list your paths.
- Run every hook suite (`.claude/hooks/tests/*.py`, `.codex/tests/*.py`) in each workspace you touch.
- Update `docs/git-flags.md` and `context.md` as points close.

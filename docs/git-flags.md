# WoW 2.0 — Git flags: management and storage

*Last updated: 2026-09-29*

> How the per-repository git flags are stored, changed, read and retired. Analysis pool; each decided point moves into
> the [adapter doc](../.codex/commit-permission.md) and the
> [personal git convention](/Users/max/.codex/conventions/git.md#repository-commit-permission).

## Today

| Concern | State on 2026-09-29 (built) |
|---|---|
| Kinds | `commit` (ordinary commits and rewrites of unpushed commits), `push` (ordinary pushes and gh writes); rarely needed risky commands are banned, safe ones need no flag |
| Store | One per workspace, `.codex/git-flags.json` (gitignored): defaults plus per-repository overrides; hash-chained `.codex/git-flags.log` beside it |
| Change | A whole-message directive (`~git_on <kinds> <repo>...`, `*` for the default), one log entry each with session, turn, prompt and time |
| Read | The guard reads the effective flag (override, else default) from the innermost workspace store; a store that disagrees with its log reads OFF |
| Status | `~git_status <repo>` per repository, `~git_status *` for the whole store; session start shows the working repository's flags in both agents |
| Lifetime | ON until `~git_off`; no expiry |

---

## Points

- [x] G0 — Kinds: two flags or four
- [x] G1 — Store and scope
- [x] G6 — Codex and Claude Code parity
- [x] G7 — Coverage for every product repository
- [x] G2 — Change path
- [x] G3 — Overview
- [x] G4 — Lifetime of risky grants
- [x] G5 — Migration

---

### G0 — Kinds: two flags or four

- Local history rewrites stay local until a push, and the reflog recovers them.
- Two local risks remain in a shared working tree: an amend or rebase can rewrite another lane's fresh commit, and a
  conflicted rebase or merge leaves every lane's tree mid-operation.
- gh writes are not local: each acts on GitHub the moment it runs.
- Two flags: `commit` for everything local (commits and history rewrites of unpushed commits, lane-checked) and
  `push` for everything that reaches GitHub (ordinary pushes and gh writes).
- Four flags (today): `commit`, `push`, `history`, `gh`.
- Decided 2026-09-29: two flags, `commit` (local, rewrites included) and `push` (GitHub, gh writes included). The
  banned list stays as it is.

### G1 — Store and scope

Decided 2026-09-29, revised the same day: one file per workspace, `<workspace>/.codex/git-flags.json` (gitignored),
beside the engine that reads it, with workspace defaults and per-repository overrides keyed by the repository's path
inside the workspace. Each workspace stays isolated (EPAM's eis-ws never shares a file with personal work), and the
store moves with its workspace. Codex's sandbox no longer shields it, so the edit guard and the hash-chained log carry
that. A repository's flags live in the innermost workspace that contains it: ocharo-ws, inside wow-two-ws, keeps its
own. Rejected: per-repository records in `.git` (no defaults, no overview, up to 412 records), one user-level file
(mixes workspaces) and a committed file (travels to every clone).

### G2 — Change path

Decided 2026-09-29: whole-message directives are the only way to change a flag, for agents and the developer alike;
a hand edit breaks the hash-chained log, and the guard then fails closed.

- `~git_on <kinds> *` sets the workspace default for every repository, present and future; `~git_off <kinds> *`
  clears it.
- `~git_on <kinds> <repo>...` sets per-repository overrides; the effective flag is the override, else the default.
- `~git_off <kinds> <repo>...` records an OFF override, so one repository can opt out of an ON default.

### G3 — Overview

Decided 2026-09-29: `~git_status *` lists the workspace defaults and every override, one line per repository;
`~git_status <repo>` shows one repository's effective flags; session start shows the working repository's effective
flags in both agents.

### G4 — Lifetime of risky grants

Decided 2026-09-29: every flag stays until turned off; no expiry. With two flags, `push` is the risky one, and it is
granted per workspace or per repository on purpose.

### G5 — Migration

Done 2026-09-29 in wow-two-ws: every valid ON record became an override (history → commit, gh → push); OFF records
equal the default and inert `config` records were dropped; a directive recorded in the store after the switch won
over an older record. 25 overrides across 18 repositories, one migration log entry carrying each source record's
evidence; all 37 old `.git/codex-*-permission.*` files deleted. Seven ocharo records named their pre-move paths, so
the old engine already read them OFF; they were dropped, not migrated.

### G6 — Codex and Claude Code parity

Done 2026-09-29: both agents load one module, `.codex/hooks/commit_permission.py`; it parses directives, owns the
store and judges the ordinary commit and push forms; `guard-git.py` judges everything else for both.

| Event | Claude Code | Codex |
|---|---|---|
| Directive | `UserPromptSubmit` → `style-recharge.sh` → `expand-markers.sh` → `commit-switch.py` | `UserPromptSubmit` → `claude_adapter.py` → `commit_permission.prompt` |
| Shell command | `PreToolUse` `Bash` → `guard-git.py` (asks the module for commit and push) | `PreToolUse` shell tools → `claude_adapter.py` → module, then `guard-git.py` |
| Session start | `SessionStart` → `commit-switch.py` → `session_status` | `SessionStart` → adapter → `session_status` |
| File edit tools | `PreToolUse` `Write\|Edit\|MultiEdit\|NotebookEdit` → `guard-git.py` refuses the store | `PreToolUse` `apply_patch` → adapter → `guard-git.py` refuses the store |

- The store path lives only inside the module, so both agents move together; lock and atomic replace guard concurrent
  writes from both.
- `guard-git.py` also refuses every shell command that names the store, its log or its lock. A hook stays a guardrail,
  not a security boundary; the hash-chained log catches a naive hand edit.
- Codex re-trusts `.codex/hooks.json` in `/hooks` once for the new `apply_patch` matcher.
- Verified by the cross tests in `.claude/hooks/tests/test_commit_switch.py` (`ParityTests`); the live `~git_status`
  in each agent is the developer's check.

### G7 — Coverage for every product repository

Decided 2026-09-29: chats open only at a workspace root, so each workspace's own hooks cover every repository inside
it; no per-repository or user-level wiring.

- The guard resolves each command's repository (`git -C`, else the working directory) and reads that repository's
  entry from its workspace's store.
- Done 2026-09-29: twelve product docs in eleven repositories restated old git rules; each now points to the workspace
  rule (Haven and TNIS committed). `ventures.ocharo-studio/CLAUDE.md` waits for the ocharo-ws step.
- Needs: G0, G1.

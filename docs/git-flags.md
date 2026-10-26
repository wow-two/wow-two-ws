# WoW 2.0 — Git flags: management and storage

*Last updated: 2026-10-26*

> How the per-repository git flags are stored, changed, read and retired. Analysis pool; each decided point moves into
> the [adapter doc](../.claude/commit-permission.md) and the
> [personal git convention](/Users/max/.claude/conventions/git.md#repository-commit-permission).

## Today

| Concern | State on 2026-10-26 (built) |
|---|---|
| Kinds | `commit` (ordinary commits and rewrites of unpushed commits), `push` (ordinary pushes to a configured remote and gh writes); rarely needed risky commands are banned, safe ones (clone included) need no flag |
| Store | One per workspace, `.claude/git-flags.json` (gitignored): defaults plus repository and folder (`<folder>/*`) overrides; hash-chained `.claude/git-flags.log` beside it |
| Change | A whole-message directive (`~git_on <kinds> <repo>...`, `<folder>/*` for every repository under a folder, `*` for the default), one log entry each with session, turn, prompt and time |
| Read | The guard reads the effective flag (repository override, else longest folder override, else default) from the innermost workspace store; a store that disagrees with its log reads OFF; a gh write it cannot match to a checkout reads OFF |
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
- [x] G8 — Folder overrides, fail-closed gh targets, named remotes

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

### G8 — Folder overrides, fail-closed gh targets, named remotes

Decided 2026-10-26 (queue Q41–Q43, from
[T9 § 3](../ideas/identity-analysis-2026-10/t9-release-automation.md#3--agent-permissions)), built the same day. An
agent can now create, clone and flag a new library repository without a per-repository directive, and two holes close.
No new kind, and consent stays a whole-message directive.

- P1, folder overrides: `~git_on|off <kinds> <folder>/*` records one override, keyed `<folder>/*`, for every
  repository under an existing folder, present and future; `~git_status <folder>/*` reads it. Kind by kind, the
  effective flag is the repository override, else the longest folder override, else the `*` default. The folder must
  exist inside the workspace and must not be the workspace itself; an unresolvable target voids the whole directive.
  The keys share `repositories`, so the store schema stays at version 3. A repository target must name its root: a
  folder named without `/*` (`workbench/wow-two-sdk-beta`) voids the directive, where it used to set the enclosing
  repository's flag, the hub's.
- P2, fail-closed gh targets: a gh write whose `owner/name` matches no checked-out repository reads OFF (before, it read
  `.`, the hub, whose push flag is ON, so any repository not cloned here was reachable); a write naming its repository
  through `GH_REPO` reads OFF too, and so does every `gh api graphql` mutation, whose target is a node ID; a document
  the command does not show plainly (`@file`, `--input`, a shell expansion) counts as a mutation. Repository creation (bare `gh repo create owner/name`, `POST orgs/{owner}/repos`,
  template generation, forks into an org) reads the flag of the path the new repository will be cloned into, per the
  workbench layout, through P1. No single folder (personal repositories, `POST user/repos`), an unstated
  `owner/name`, or an occupied path reads OFF. `gh repo create --source|--remote|--push` stays blocked, now with
  the short forms `-s` / `-r`.
- P3, clones and named remotes: `git clone` and `gh repo clone` need no flag, since a clone writes only the new
  repository and its own `origin`; clone options that write configuration, install hooks or run a command
  (`--config`, `--template`, `--upload-pack`) never run. An ordinary push names no remote or one the repository
  already has; a URL or a path is a remote write in disguise and never runs.
- Rejected: a `repo` kind (creation already sits under `push`), a `*` default ON (hands every future product both
  flags), allow-listing scripts by path, agent `git remote add`.
- Still read from the working repository: gh writes that name no repository, `gh api graphql` queries included.
- Needs: G1, G2.

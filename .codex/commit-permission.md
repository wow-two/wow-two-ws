# Repository git flags

*Last updated: 2026-09-29*

> Codex and Claude Code integration for the workspace git flags in `wow-two-ws`. Only commands that are risky and
> used often get a flag; risky commands that are rarely needed never run; safe commands need no flag.

## Contract

- flag, directive and consent rules: [personal Git conventions](/Users/max/.codex/conventions/git.md#repository-commit-permission); not repeated here.
- staging and batch handover: [workspace Git protocol](../conventions/development/repo/version-control/git.md#protocol-agent--human).
- analysis and decisions (G0–G7): [docs/git-flags.md](../docs/git-flags.md).
- this adapter applies to `wow-two-ws` and every repository inside it; each other workspace runs its own hooks.

---

## Adapters

- `.codex/hooks/commit_permission.py` owns the workspace store and answers each kind's permission check; both agents
  load this one module.
- Codex: `claude_adapter.py` feeds it native prompts, `SessionStart` and tool calls; `apply_patch` reaches the
  shared guard as a file edit.
- Claude Code: `.claude/hooks/commit-switch.py` feeds it `SessionStart` and exact prompts (tail-called by
  `expand-markers.sh`); `.claude/hooks/guard-git.py` consults it for gated commands and guards the store against
  `Write` / `Edit` / `MultiEdit` / `NotebookEdit`.
- must resolve directive paths against the workspace root; `.` selects the workspace repository, `*` the workspace
  default.
- must make the entire user message one directive: `~commit_*` / `~push_*` and one target, or
  `~git_on|off <kind>[,<kind>...] <target>...` / `~git_status <target>...`.
- must name each kind once; `all` only disables; one unresolvable repository voids the whole directive.
- `history` and `gh` merged into `commit` and `push` on 2026-09-29; a directive naming them changes nothing.

## Kinds

| Kind | While `ON` for the target repository |
|---|---|
| `commit` | `git -C <repo> commit -m "subject"`; `commit --amend`, `rebase`, `cherry-pick`, `revert`, `merge`, `am`, `subtree`, soft / mixed `reset` to a commit |
| `push` | `git -C <repo> push [-u] [<remote> [<refspec>...]]`; every gh write: pull requests, issues, releases, workflow runs, secrets, variables, repository settings, API writes |

- a rewrite never replaces a commit a remote-tracking branch already holds: amend checks `HEAD`, rebase
  `<upstream>..<branch>` (or everything with `--root`), reset `<commit>..HEAD`; a range the guard cannot resolve
  blocks. Merge, cherry-pick, revert, am and subtree add commits and replace none.
- allowed without a flag (safe): read-only git and gh, `fetch`, `pull`, staging, `stash`, branch and tag writes,
  unforced `mv` and `rm`, `apply` unless reversed, `submodule init|update|sync`, `notes` writes.
- never, whatever the flags (risky and rarely needed): forcing, deleting, mirror, pruning and hook-skipping pushes;
  worktree discards (worktree `restore`, path / `.` / forced `checkout`, forced `switch`,
  `reset --hard|--merge|--keep`, `clean`, forced `rm` / `mv`, reversed `apply`, `checkout-index`); every `config`
  write; `remote` and `worktree` writes; `submodule add|deinit|set-url|set-branch|absorbgitdirs`; ref and object
  surgery (`filter-*`, `fast-import`, `update-ref`, `update-index`, `replace`, `gc`, `prune`, `reflog` and
  `symbolic-ref` writes); `send-email`; `gh repo delete` and direct repository DELETE API calls;
  `gh repo create --source|--remote|--push`; LFS installation, direct upload, pruning and migration writes.
- LFS inspection, `migrate info`, hydration (`fetch|pull|checkout`) and scoped attribute changes
  (`track|untrack`) need no flag. Other LFS verbs remain human operations.
- Checkout path and patch forms remain worktree discards when the optional `--` separator is omitted.
- a new category earns a flag only when it is both risky and used often; otherwise it joins one of the two lists.
- a gated git command acts on `git -C <repo>`, else the working directory; a `cd`, `pushd`, `--git-dir` or
  `--work-tree` in the same command blocks it.
- a gh write acts on `-R owner/name`, a `repos/owner/name` API path or `repo <verb> owner/name`;
  the matching managed repository holds the flag, and an unmatched target reads `.`. Lookup follows
  nested `workbench` ownership without a fixed depth; it skips dependency trees and directory symlinks.
  Repository creation with `--source` remains blocked because it also changes local configuration.
- history rewrites still meet the lane check, which stops once on another lane's uncommitted files.

The following fenced examples are documentation, not consent:

```text
~commit_on workbench/wow-two-sdk-beta/wow-two-sdk-beta.ui
```

```text
~push_off workbench/wow-two-sdk-beta/wow-two-sdk-beta.ui
```

```text
~git_on commit,push workbench/wow-two-platform/wow-two-platform.wheelhouse
```

```text
~git_on commit *
```

```text
~git_off push workbench/ventures/10x-venture-forever-pin
```

```text
~git_status *
```

---

## Store

- one store per workspace: `.codex/git-flags.json`, gitignored, beside this engine; `.codex/git-flags.log` holds the
  hash-chained change log and `.codex/git-flags.lock` the writer lock.
- `defaults` holds the workspace default per kind; `repositories` holds overrides keyed by the repository's path
  inside the workspace (`.` for the workspace repository). The effective flag is the override, else the default.
- `~git_on|off <kinds> *` sets or clears the default for every repository, present and future; a per-repository
  directive records an override, `OFF` included, so one repository can opt out of an `ON` default.
- a repository's flags live in the innermost workspace store that contains it: a nested workspace with its own store
  (ocharo-ws) owns its repositories, whichever workspace the chat runs in; without one, its repositories fall under
  this store.
- every change appends one log entry (revision, time, changes, session, turn, prompt, recording workspace, the store
  hash, the previous entry's hash), then replaces the store atomically under the lock.
- a store that fails its schema or disagrees with its log reads as every flag `OFF`; an `on` directive is refused and
  any `_off` directive resets it to every flag `OFF` with a repair entry that commits to the broken log before it.
- `seen_consents` rejects a replayed event; `UserPromptSubmit` owns every transition, shell checks only read, and
  `Stop` leaves the store unchanged.
- must change the store only through a directive; no tool edits, moves or names it (both agents' guards block it).
  Hooks stay a guardrail, not a security boundary.

---

## Status

The helper is read-only and prints one repository's flags, or the whole store with `*`; it exposes no `on`, `off`, or
mutation command:

```sh
python3 -B .codex/hooks/commit_permission.py status --repo workbench/wow-two-sdk-beta/wow-two-sdk-beta.ui
python3 -B .codex/hooks/commit_permission.py status --repo '*'
```

- session start shows the working repository's effective flags in both agents.
- must report an invalid store or unavailable repository as blocked, preserving the stored state.
- unavailable or untrusted hooks cannot activate permission; offline fixtures must use isolated temporary state.

---

## Commit and push forms

```sh
git -C <absolute-repository> commit -m "subject"                  # commit flag ON
git -C <absolute-repository> push [-u] [<remote> [<refspec>...]]   # push flag ON
```

- must use explicit `git -C` for managed repositories; shell hook working-directory metadata may name the workspace.
- may use `git commit -m "subject"` only when the hook resolves the target repository unambiguously.
- must inspect staged paths, their diff, and whitespace; state the batch and proposed subject before committing.
- must preserve unrelated staged paths and exclude them from the reviewed batch.
- must report the resulting SHA after a commit or rewrite, and the pushed branch and range after a push.
- forcing, deleting and mirror pushes, implicit staging and pathspec commits never run.
- must reject compound shell forms and alternative Git configurations for the ordinary commit and push exceptions.
- must preserve configured signing; a signing-socket block uses native escalation for the same authorized command.
- this workflow guard does not claim a security boundary against arbitrary executable code.

---

## Verification

```sh
python3 -B .codex/tests/test_commit_permission.py
python3 -B .claude/hooks/tests/test_commit_switch.py
```

- must test persistence across chats, revocation, defaults and overrides, nested stores, tampering and repair.
- must test each kind's gated commands, pushed-history refusal, the never-run and flag-free lists, multi-kind and
  multi-repository directives, hidden targets, gh origin matching and the store edit guard.
- must test prompt provenance, replayed transitions, concurrency, and rejected commit forms without making commits.
- one cross test records a directive through each agent's adapter and checks the other agent's guard honors it.
- offline passing tests do not prove hook trust or a live permission change.

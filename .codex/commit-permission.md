# Commit and push permission

*Last updated: 2026-09-27*

> Codex and Claude Code integration for the repository commit and push flags in `wow-two-ws`.

## Contract

- flag, directive and consent rules: [personal Git conventions](/Users/max/.codex/conventions/git.md#repository-commit-permission); not repeated here.
- staging and batch handover: [workspace Git protocol](../conventions/development/repo/version-control/git.md#protocol-agent--human).
- this adapter applies to `wow-two-ws`; other workspaces retain their installed local policy.

---

## Adapters

- `.codex/hooks/commit_permission.py` owns both records: it applies directives and answers the commit and push checks.
- Codex feeds it native prompts and tool calls directly.
- Claude Code: `.claude/hooks/commit-switch.py` feeds it exact prompts (tail-called by `expand-markers.sh`).
- Claude Code: `.claude/hooks/guard-git.py` asks it before an ordinary commit or push, with the tool call's id as the turn.
- must resolve directive paths against the workspace root; `.` selects the workspace repository.
- must make the entire user message exactly two shell-style tokens: directive and repository path.

The following fenced examples are documentation, not consent:

```text
~commit_on workbench/wow-two-sdk-beta/wow-two-sdk-beta.ui
```

```text
~commit_off workbench/wow-two-sdk-beta/wow-two-sdk-beta.ui
```

```text
~commit_status workbench/wow-two-sdk-beta/wow-two-sdk-beta.ui
```

```text
~push_on workbench/wow-two-sdk-beta/wow-two-sdk-beta.ui
```

```text
~push_off workbench/wow-two-sdk-beta/wow-two-sdk-beta.ui
```

```text
~push_status workbench/wow-two-sdk-beta/wow-two-sdk-beta.ui
```

---

## Record

- two records inside the repository's resolved Git directory: `codex-commit-permission.json` and `codex-push-permission.json`.
- each record's `enabled` is its flag, and the only field its check reads; neither flag stands in for the other.
- `revision`, `last_change` (action, chat, turn, prompt, time) and `seen_consents` are evidence and replay protection.
- schema 2 dropped `confirmed_session_id`, a copy of `last_change.session_id`; v1 records merge on read and write.
- must keep the records outside tracked source; a clone starts without permission state.
- must change records only through the prompt hook, never by editing JSON or replaying events.
- `UserPromptSubmit` owns state transitions; shell checks only read records, and `Stop` leaves them unchanged.

---

## Status

The helper is read-only and prints both flags; it exposes no `on`, `off`, or mutation command:

```sh
python3 -B .codex/hooks/commit_permission.py status --repo workbench/wow-two-sdk-beta/wow-two-sdk-beta.ui
```

- must report an unreadable record or unavailable repository as blocked, preserving the stored record.
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
- must report the resulting SHA after a commit, and the pushed branch and range after a push.
- must leave forcing, deleting and mirror pushes (`--force`, `+ref`, `:ref`, `--delete`, `--mirror`), amend, history rewrites, implicit staging, and pathspec commits to their separate restrictions.
- must reject compound shell forms and alternative Git configurations for the ordinary commit and push exceptions.
- must preserve configured signing; a signing-socket block uses native escalation for the same authorized command.
- this workflow guard does not claim a security boundary against arbitrary executable code.

---

## Verification

```sh
python3 -B .codex/tests/test_commit_permission.py
python3 -B .claude/hooks/tests/test_commit_switch.py
```

- must test persistence across chats, revocation, repository isolation, schema merging and malformed state.
- must test prompt provenance, replayed transitions, concurrency, and rejected commit forms without making commits.
- offline passing tests do not prove hook trust or a live permission change.

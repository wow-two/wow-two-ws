# Commit permission

*Last updated: 2026-09-19*

## Switch

Ordinary agent commits are OFF by default. Explicit user consent may enable commits for one repository in
one Codex task turn. Staging remains permitted within the authorized task scope.

Use one standalone line in the user prompt:

```text
~commit_on workbench/wow-two-sdk-beta/wow-two-sdk.backend.beta
```

Disable it with a standalone `~commit_off`. Paths resolve against the workspace root; `.` selects the workspace
repository. Quoted examples, fenced code and XML-wrapped text never activate the switch.

The hook keys consent by workspace, session and turn. A new turn starts OFF. Stop closes the current grant.
A missing turn ID, unknown live turn, malformed state or unresolved repository leaves commits OFF.
This uses the documented [Codex hook turn identity](https://learn.chatgpt.com/docs/hooks#pretooluse).

## Natural-language consent

When the user explicitly enables commits for the active turn in prose, the agent may run:

```sh
python3 .codex/hooks/commit_permission.py on --repo workbench/wow-two-sdk-beta/wow-two-sdk.backend.beta
python3 .codex/hooks/commit_permission.py status
python3 .codex/hooks/commit_permission.py off
```

The helper uses `CODEX_THREAD_ID` and the live turn already observed by PreToolUse; it cannot invent a turn.
If native hooks are unavailable or untrusted, activation fails closed. Offline test events must use isolated
temporary storage and must never seed live consent. No trust store or native permission is changed.

## Scope

- The accepted commit form is `git commit -m "subject"`, with optional `git -C <repo>`.
- For a managed repository, use `git -C <absolute-repo> commit -m "subject"` so the hook sees the repository explicitly;
  the live shell hook may report the workspace cwd instead of the command's `workdir`.
- Inspect the exact staged paths, their diff and whitespace before each commit.
- State the batch and proposed subject before committing; report the resulting SHA.
- Existing unrelated staged work must be preserved and excluded from the batch.
- ON permits ordinary new commits only; it does not permit push, amend or other history rewrites.
- Compound shell commands, implicit staging, alternative Git configurations and pathspec commits stay blocked.
- Native sandbox approval and hook trust remain authoritative.
- If signing cannot reach the configured GPG agent, retry the same authorized commit through native escalation;
  preserve signing settings.
- This local hook is a workflow guardrail, not a security boundary against arbitrary executable code.

## Verification

`python3 -B .codex/tests/test_commit_permission.py` tests lifecycle, task and repository isolation, explicit
revocation, quoted markers, malformed state and rejected command forms without executing any Git commit.

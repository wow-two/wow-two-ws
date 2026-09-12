# Claude configuration in Codex

*Last updated: 2026-09-12 05:23 PM*

## Audit and scope

Reference: `/Users/max/Projects/Company/EPAM/eis/eis-ws/.codex/claude-port.md` and its lifecycle adapter. Reuse its shared-source architecture; retain this workspace's own policies instead of copying EIS's strict Git policy or mandatory empty Queue.

Replaced the renamed AGENTS.md and eight byte-identical copied hooks; native skill entry points load shared SKILL.md files.

- `AGENTS.md` loads `CLAUDE.md`, applicable `.claude/rules/` and `.codex/instructions.md`.
- Shared Claude instructions, hooks, settings and source skills remain unchanged.
- Indexes remain lazy; path-scoped rules are listed for conditional reads, not injected globally. Templates remain labeled as templates rather than current project declarations.
- No Claude permission allowlist, credentials, global settings, MCP registrations or trust state are imported. No project `.mcp.json` was present.

## Lifecycle

SessionStart, UserPromptSubmit, PreToolUse, PostToolUse and Stop. Shared Git policy, style pulse/recharge and marker expansion; successful Codex patches feed the shared touch ledger.

The adapter resolves files relative to its installation. Hook commands use the saved workspace's absolute path; update `.codex/hooks.json` if it moves. Session state is hashed with the workspace root and Codex session ID, isolating workspaces and Claude sessions. When config layers include parent and child workspaces, the parent adapter yields if the session cwd is under the child's own adapter.

Git policy always applies to the repository being edited. Hook dispatch follows the session cwd; a cross-repository task must still read and follow the target repository's own instructions. Shell-generated file edits are not inferred into the ledger. Tool hooks are a guardrail, not a complete enforcement boundary.

## Validation

Prepared port: 20 offline tests passed. Run from this workspace:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 .codex/tests/test_codex_hooks.py
```

Tests use synthetic event payloads; Git command strings are never executed as writes. Installed verification and native discovery are recorded below.

## Activation

Open `/hooks` in Codex CLI from this workspace and review any untrusted or modified hook definitions. Project trust and individual hook trust are separate. The port does not edit trust storage or bypass review. A new task loads `AGENTS.md`; the instructions apply through that fallback while lifecycle hooks await trust.

## Sources

- [Codex hook lifecycle, payloads and trust](https://learn.chatgpt.com/docs/hooks)
- [EIS reference port](/Users/max/Projects/Company/EPAM/eis/eis-ws/.codex/claude-port.md)

## Installed verification

Installed adapter: 20 tests passed. Native `skills/list` discovers `create-repo` and `open-active`; both skill validations passed.

Native `hooks/list`: project hooks are skipped because this nested workspace has no project trust entry. Open Codex CLI from this workspace, complete its project trust review, and review the project hook definitions through `/hooks`. Parent workspace trust does not establish trust for this independent repository.

Shared `CLAUDE.md` and `.claude/` source hashes are unchanged. `git diff --check` passed. No staging, commits or publishing performed. Hook activation remains a user trust step, not an offline test result.

## Personal conventions and staging — 2026-09-12 04:09 PM

Shared Codex defaults are extracted into `~/.codex/AGENTS.md`; duplicate adaptation bullets are removed from `.codex/instructions.md`. General response style is extracted to `~/.codex/conventions/response-style.md`; local rule files import it for Claude and Codex. Project-specific response styles, task schemas, business boundaries and Git restrictions stay local.

The Codex PreToolUse adapter loads the local `.codex/hooks/staging_guard.py`. Recognized index writes without an explicit native escalation request are denied. This does not verify conversational consent: the agent must already have explicit user approval for the repository and file set. Escalation is reviewed by the configured runtime, which may use automatic approval review rather than a human dialog. Tools that omit escalation metadata must hand staging to GitKraken. `~/.codex/rules/staging.rules` adds native prompt decisions for direct staging prefixes; it is not a universal shell firewall.

Reload/review modified hooks through Codex's hook trust UI; trust storage is not edited by this setup. New runs load the global instruction file. Offline tests do not establish live hook activation. Aliases, arbitrary programs and direct filesystem index writes are outside the shell recognizer; instructions forbid using them as bypasses. No security guarantee is claimed for arbitrary tool execution.

Current extraction and verification: [personal conventions setup](/Users/max/Projects/10x-ws/.codex/conventions-setup.md).

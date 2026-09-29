# Codex adaptations

*Last updated: 2026-09-29*

General defaults: `~/.codex/AGENTS.md`. Enforcement remains in `.codex/hooks/`;
index-only operations follow the shared Git conventions without a separate staging gate.

The [shared repository Git flags](/Users/max/.codex/conventions/git.md#repository-commit-permission)
govern commits, pushes, history changes and GitHub writes. The [local adapter](commit-permission.md)
implements the four independent flags, including persistence across chats and the human-only command restrictions.

## Product runtime ownership

- During Codex-led product work, Codex owns the required local runtimes and their logs.
- Start each runtime in a persistent managed terminal session; do not orphan background processes.
- Prefer the repository's watcher or HMR command and restart an affected runtime when reload is insufficient.
- Manual source edits keep Codex ownership; the managed watcher or restart applies them.
- Keep runtimes alive across related turns so the user can inspect the product in a browser.
- Verify readiness before handing over a URL; inspect attached logs when behavior fails or becomes stale.
- The user owns browser navigation and manual QA unless they ask Codex to operate the browser.
- Codex may stop or restart only processes it started or positively identified as belonging to the current task.
- A user-started replacement runtime or debugger transfers ownership when the user says so.
- Surface native certificate or trust prompts for user approval; do not weaken HTTPS to avoid them.
- Stop managed runtimes when the task ends, the user asks, or runtime ownership transfers.

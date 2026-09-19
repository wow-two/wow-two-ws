# Codex adaptations

*Last updated: 2026-09-12*

General defaults: `~/.codex/AGENTS.md`. Enforcement remains in `.codex/hooks/`; index-only operations follow the shared Git conventions without a separate staging gate.

Ordinary commits default to OFF. Explicit user consent may enable the task- and repository-scoped,
turn-only switch in [commit-permission.md](commit-permission.md). An ON hook status permits ordinary
staged commits for that grant, overriding the default developer-only commit rule. Push and amend remain forbidden.

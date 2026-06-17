# Template — `wow-two-ws/PLANNING.md` (entry board)

*Last updated: 2026-06-17*

> The single link handed to a contributor: who owns what · where each plan lives · how we (don't) gate.
> Fill the `{placeholders}`; full rationale in `system/sessions/onboard-member/session-onboard-member.md`.

---

# wow-two — Planning Board

*Last updated: {YYYY-MM-DD}*

## Board

| Repo | Plan path | Contributor's next | Owner |
|---|---|---|---|
| {repo} | `engineering/planning/backlog.md` | {top item} | {name} |

## Ownership split

- Contributor → app **frontends** (`{slug}.frontend-services/`); consumes libs as packages; no lib/backend edits.
- Owner → beta libs + app backends/infra.
- Live seam: `drydock` frontend ↔ backend **API contract** — coordinate on the status channel.

## Status channel

- {GitHub repo Issues / Telegram thread} — async status, questions, lib requests, API-seam changes. No standup.

## No branch protection

Single trusted contributor → fix-forward + CI-green signal, not gates. See SOP → *Gates & scaling* for when this changes.

## Dependency map

- `drydock.frontend-services` → `@wow-two-beta/ui` (`^0.0.x`) — owner controls bumps.
- `drydock` frontend → `drydock` backend — the one live API seam.

## Git note

`workbench/` is gitignored; each repo is an independent `.git`. Commit inside the repo, never from the workspace root.

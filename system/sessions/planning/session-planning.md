# Session: wow-two Planning — `pln-w2`

*Last updated: 2026-08-13*

> Handle: `pln-w2` · Chat: `pln - w2 {YYYY-MM-DD}` · ~10 min
> **Task source:** [`system/planning/pln-tasks.md`](../../planning/pln-tasks.md)
> **Output:** none of its own — schedule rows land in the `10x-ws` day log as `ven` / `eng`
> Run inside one chat with the other vectors → `pln-vectors` in `10x-ws`.

Shortest of the three sessions. `w2` has no external clock and no ceremonies — it decides one thing: which item the day's build blocks pull.

---

## Two levels — and one grain rule

| Level | Lives in | Holds | Grain |
|---|---|---|---|
| Active | `system/planning/pln-tasks.md` | what's being worked now, with IDs | **abstract** — a capability, not a step |
| Detail | each repo's `engineering/planning/` | how that capability gets built | concrete file / API changes |

- `pln-tasks.md` states outcomes: *finish codes functionality for forever-pin*. Never sub-steps.
- The repo's own planning breaks it down. This file never mirrors that breakdown.
- Pulling mints a Task ID. No ID → not schedulable, not in a day log.

Same relationship `eis` has between its tasks file and its ticket context docs.

---

## No dated logs

Git is the journal. Version docs (`engineering/versions/v{X.Y}/`) hold per-version detail; `docs/planning.md` § *Log* holds pivots. Timing comes from the `10x-ws` day log.

---

## Process

1. Read `pln-tasks.md` → anything `wip` continues first
2. Nothing `wip`, or a block is free → pull the next capability, mint its ID
3. Score per `pln-vectors`; most `w2` items carry no deadline
4. Tie-break by **track order**, below — this vector's delta from the shared engine
5. Present the pick → user confirms

### Track order

`rough` → `polish` (optional) → `version`. A settled product runs `version` + `polish` only.

Between two undeadlined candidates, the one unblocking a consumer wins. A blocked product fixes the SDK rather than working around it — that rule is `conventions/development/dev-cycle.md` § *Vector completeness*, and it decides ties.

---

## Categories

| Tag | Covers |
|---|---|
| `sdk` | `wow-two-sdk` / `-sdk-beta` package work |
| `plt` | `wow-two-platform` internal infra |
| `app` | products — drydock, secrets-vault |
| `ven` | ventures — forever-pin, micro-saas, TNIS, prism |
| `con` | conventions, standards, ADRs |
| `ws` | workspace / meta — registry, scripts, templates |

Task ID `{cat}-t-{NNN}`, assigned here. Carried into the `10x` day log as `w2:{cat}-t-{NNN}`.

Day-log category: `ven` for ventures, `eng` for everything else.

---

## Commands

- `/w2 next` — top `Backlog` item in `pln-tasks.md`
- `/w2 active` — rows that are `wip`
- `/w2 stale` — rows untouched longest

---

## Rules

- **The backlog is ordered, not version-tagged.** Never pin an item to a future version.
- **An item needs an ID before it can be scheduled.** No ID → it's still backlog.
- **Never mirror a repo's breakdown here.** A sub-step in `pln-tasks.md` is a grain violation.
- **2–3 related repos per session.** Updating a lib → check consumers.
- **Agents never commit or push** — stage and draft the message only (`.claude/hooks/guard-git.py`).
- **Parallel chats share one working tree.** Unexpected changes are another lane's work — stop and ask, never revert.

# Engineering Planning — Convention & Template

*Last updated: 2026-06-10*

Each repo keeps `engineering/planning/planning.md` (roadmap + tracker) plus `engineering/planning/backlog.md`
and `engineering/planning/rules.md` — the durable **roadmap + backlog**, the standing plan that version
docs (`versions/v{X.Y}/v{X.Y}.md`) pull from and return to.
Everything a version doc omits — deferred work, known issues, follow-ups, decisions, history — lives
here. Shape proven on Haven (10 versions shipped).

## Sections

- **Versions** — the roadmap. One row per version: theme · deliverables · status. Deliverables fill in on close. Lists **shipped versions + the single active/next one** — no speculative future rows (plan only the next version; future work is backlog). Carries the bump rule + a pointer to per-version docs.
- **Decisions** — durable platform decisions: decision · rationale. Append-only; survives version churn.
- **Backlog** — everything not in the active version, an **ordered queue** (top = next to pull). Group by theme when it helps; order within each group by priority. A version's leftovers land here; pull items back into an iteration when it's their turn. Strike-through + ✅ kept items (traceability), not deleted.
- **Log** — dated journal of version scope/close events and notable pivots (git holds the rest).
- Repos may add **reference sections** (component tracker, infra/endpoints, troubleshooting) as useful — keep them below the four above.

## Rules

- **Backlog is ordered, not future-version-tagged.** Don't pin items to specific future versions (v1.2, v1.5…) — that predicts next-next versions. Order by pull priority; the next version pulls from the top.
- **The Versions table grows on close.** A planned version is one row (theme + ⏳); fill Deliverables and flip to ✅ when its iterations are done.
- **Durable only.** Per-version task detail lives in version docs; how-to lives in architecture docs.

## Template — copy below the line

---

# {Brand} — Engineering Planning

*Last updated: {YYYY-MM-DD}*

## Versions

Release roadmap. Per-version detail in `versions/v{X.Y}/v{X.Y}.md`. Bump: pre-MVP `+0.1` per
capability; post-MVP minor = feature batch, major = milestone. Timebox: ≤1 week per version.

| Version | Theme | Deliverables | Status |
|---|---|---|---|
| v0.1 | {theme} | {what shipped} | ✅ |
| v1.0 | {theme} | — | ⏳ |

## Decisions

| Decision | Rationale |
|---|---|
| {decision} | {why} |

## Backlog

Anything not in the active version — **ordered, top = next to pull**. Group by theme; order within.
Type: `feature` · `issue` · `check` · `idea`. Strike-through + ✅ when done (kept for traceability).

### {Theme group}

| Item | Type | Notes |
|---|---|---|
| {item} | feature | {note} |

## Log

- **{YYYY-MM-DD}:** {version scoped / closed — deliverables; what moved to backlog}.

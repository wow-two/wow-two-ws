# Version Doc — Convention & Template

*Last updated: 2026-06-10*

A per-version progress doc kept by a product / venture repo at `engineering/versions/`. A
version is a group of **iterations**; each iteration is a one-line **goal** + a few abstract tasks.
Deferred work, known issues, and follow-ups go to the repo's **backlog** in `engineering/planning/backlog.md`
(see [`../engineering-planning/engineering-planning-conventions.md`](../engineering-planning/engineering-planning-conventions.md)) — not here.

## Naming & location

- One folder per version, named exactly the version: `engineering/versions/v{X.Y}/v{X.Y}.md`.
- No brand or `engineering` prefix — the repo is the namespace. The **latest** version folder is the active one (no `current/`).

## Lifecycle

`⏳ Planned` → `🚧 In Progress` → `✅ Complete`. Open when planning the version; close when its iterations' tasks are done (set **Completed**). One active version at a time.

## Cadence

- Pre-MVP: `+0.1` per major capability.
- Post-MVP: the bump reflects the change — minor for a feature batch, larger for a milestone. No fixed step.

## Rules

- **Timebox — one week, max.** A version contains at most a week of work; anything beyond is pushed to the ordered backlog.
- **Plan only the next version.** No version-after-next docs or speculative iterations; future work waits in the ordered backlog until it's next.
- **Tasks stay abstract** — capability one-liners, not implementation. No table/column names, service or class names, or file paths; those live in code + architecture docs, not the version log.
- One sentence per goal; short, outcome-shaped tasks.

## Template — copy below the line

---

# v{X.Y} — {Theme}

*Last updated: {YYYY-MM-DD}*

**Status:** ⏳ Planned · **Started:** {YYYY-MM-DD} · **Completed:** —

### Iteration 1 — Ingest

**Goal:** Scrape and store source listings.

- [ ] Pull new listings from the source on a schedule.
- [ ] Store them, skipping ones already saved.

### Iteration 2 — Classify

**Goal:** Classify listings and flag the ones worth acting on.

- [ ] Classify new listings in batches.
- [ ] Record each result and mark the matches.

### Iteration 3 — Notify

**Goal:** Notify the channel of new matches.

- [ ] Detect newly-matched listings.
- [ ] Send a formatted alert to the channel.

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

## Versioning scheme

- Products **start at `v0.1`** — there is no `v1.0` on day one.
- **Minor increments** per version: `v0.1` → `v0.2` → … → `v0.99` → `v0.100`.
- **Major bump** (→ the next whole number, e.g. `v1.0`) only when the minor counter reaches **`.100`**, OR a **breaking change** ships. `v1.0` is *earned* — a long `v0.x` runway or a deliberate break, not a launch label.
- Timebox still applies: ≤ 1 week per version.

## Two-cycle shipping (a cycle = two versions)

Each development **cycle** spans **two** versions — build, then extract:

- **Deliverable version** — get something done in the app: ship a product feature. Cross-cutting infrastructure is built **inline** to move fast (business logic first).
- **Extraction version** — extract + polish the reusable infra the deliverable produced into the **SDK** + update conventions, then adopt it across the active apps.

So **1 cycle = 2 versions delivered**; then the next cycle's deliverable version starts. Worked example (smart-qr): `v0.1` (product foundation — bespoke migrator built inline) → `v0.2` (migrator extracted to the SDK + adopted across drydock/secrets-vault) → cycle done → `v0.3` next deliverable. Full model: [`../../development/dev-cycle.md`](../../development/dev-cycle.md).

## Rules

- **Timebox — one week, max.** A version contains at most a week of work; anything beyond is pushed to the ordered backlog.
- **Plan only the next version.** No version-after-next docs or speculative iterations; future work waits in the ordered backlog until it's next.
- **Iteration heading carries the goal on one line** — `### Iteration N — {name}: {one-line goal}`. No separate `**Goal:**` line.
- **Each task = a capability the version delivers**, phrased **`Ability to {capability}`** — the feature / user POV, never an implementation step. `Ability to log in as a guest`, not `Mint a guest cookie`.
- **One line, no em-dash clauses.** If you'd append `— detail`, fold it in plainly or split it into another task. Use **`and`**, never `+`. Group only *closely-related* capabilities (`edit and delete your codes`); split *unrelated* ones (generate vs download = two tasks).
- **Capability-grained + abstract** — one bullet per user-facing capability (the `CRUD the entity` level). Never per-endpoint / per-field. No table/column, service/class names, or file paths — those live in code + architecture docs. Don't name a property that isn't itself a feature (an immutable slug is not a task).
- **Verification iteration** (optional, always last) — when a version needs manual sign-off beyond automated tests. Its items are **ordered, concrete check steps**, not capabilities: `[ ] {action} → {expected result}`, run top-to-bottom. The one place specifics are allowed (you're checking the real thing). Sign-off = ticking them + flipping `Status` → `✅`.

## Template — copy below the line

---

# v{X.Y} — {Theme}

*Last updated: {YYYY-MM-DD}*

**Status:** ⏳ Planned · **Started:** {YYYY-MM-DD} · **Completed:** —

### Iteration 1 — Ingest: scrape and store source listings

- [ ] Ability to pull new listings on a schedule, skipping ones already saved.

### Iteration 2 — Classify: flag the listings worth acting on

- [ ] Ability to classify new listings and mark the matches.

### Iteration 3 — Notify: alert the channel of new matches

- [ ] Ability to alert the channel when a new match appears.

### Iteration 4 — Verification: confirm the pipeline end to end

- [ ] Run a scrape → new listings stored, duplicates skipped.
- [ ] Run classify → each listing recorded, matches flagged.
- [ ] Add a matching listing → the channel receives one formatted alert.

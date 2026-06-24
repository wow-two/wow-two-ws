# Version Doc — Convention & Template

*Last updated: 2026-06-24*

A per-version progress doc kept by a product / venture repo at `engineering/versions/`. A
version is a group of **iterations**; each iteration is a **noun naming its focus** + a few abstract tasks.
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

## Version types

Every version is exactly **one** of three types. The type sets the task verb and is declared on the meta line (`**Type:**`, next to `**Status:**`).

| Type | What it does | Task verb |
|---|---|---|
| **Feature** | Product development — a new user-facing capability, or a bug fix. | `Ability to {capability}` · `Fix {behavior}` |
| **Adoption** | SDK extraction + adoption — moves code **to / from** the SDK. | `Extract {thing} → SDK` · `Adopt {SDK thing}` |
| **Polish** | Optimization of what already works **and is already extracted** — system-wide or SDK refine / simplify / harden. **Not** new features, **not** new extraction. | `Optimize {thing}` · `Simplify {thing}` · `Harden {thing}` |

- A **cycle = Feature → Adoption** (build inline, then extract — see [Two-cycle shipping](#two-cycle-shipping-a-cycle--two-versions) below).
- **Polish stands alone** — it isn't half of a cycle; run it on its own when optimization is the version's theme.

## Two-cycle shipping (a cycle = two versions)

Each development **cycle** spans **two** versions — build, then extract. The two halves are the **Feature** then the **Adoption** [version type](#version-types):

- **Deliverable version** (Type: **Feature**) — get something done in the app: ship a product feature. Cross-cutting infrastructure is built **inline** to move fast (business logic first).
- **Extraction version** (Type: **Adoption**) — extract + polish the reusable infra the deliverable produced into the **SDK** + update conventions, then adopt it across the active apps.

So **1 cycle = 2 versions delivered**; then the next cycle's deliverable version starts. A **Polish** version is **not** part of a cycle — it stands alone. Worked example (smart-qr): `v0.1` (product foundation — bespoke migrator built inline) → `v0.2` (migrator extracted to the SDK + adopted across drydock/secrets-vault) → cycle done → `v0.3` next deliverable. Full model: [`../../development/dev-cycle.md`](../../development/dev-cycle.md).

## Rules

- **Timebox — one week, max.** A version contains at most a week of work; anything beyond is pushed to the ordered backlog.
- **Plan only the next version.** No version-after-next docs or speculative iterations; future work waits in the ordered backlog until it's next.
- **Version theme = a noun phrase, no parentheticals.** The `# v{X.Y} — {Theme}` H1 carries a plain noun phrase — `Product foundation`, not `Product foundation (guest-first)`; `SDK adoption`, not `SDK adoption (backend-beta + frontend-beta)`. Don't pack scope detail into the H1; it lives in the iterations.
- **Declare the version Type.** The meta line carries a `**Type:**` field next to `**Status:**` — one of `Feature` · `Adoption` · `Polish` (see [Version types](#version-types)). It sets the task verb.
- **No intro blockquote.** The `# v{X.Y} — {Theme}` H1 title and the `**Status:**` line already carry the theme; don't restate it in a `> …` quote under them.
- **No per-iteration test / green results.** A `Green: …` line (build / unit / E2E / migration counts) does **not** belong on a build iteration — green is recorded only in the (last) Verification iteration, where checking the real thing is the point.
- **Iteration name = a noun naming the iteration's focus / subject — no `: {goal}` clause.** `### Iteration N — Google identity provider`, not `### Iteration N — Sign in: authenticate with a Google account`. The action / goal lives in the task; keep the name short (the noun, not a sentence).
- **No per-iteration status emoji.** No `✅` / `🚧` on iteration headings — the task checkboxes (`[ ]` / `[x]`) carry done-state.
- **Each task = a capability the version delivers**, phrased per the version Type (below) — the feature / user POV, never an implementation step. `Ability to log in as a guest`, not `Mint a guest cookie`.
- **Open the task with the keyword matching the version Type** (see [Version types](#version-types)):
  - **Feature** (new user-facing capability or a bug fix — e.g. `v0.1`, `v0.3`) → **`Ability to {capability}`** (new capability) or **`Fix {behavior}`** (bug). The feature / user POV.
  - **Adoption** (internal architecture; moves code to / from the SDK — e.g. `v0.2`, `v0.4`) → verb-first by direction: **`Adopt {SDK thing}`** (consume an SDK module) or **`Extract {thing} → SDK`** (contribute one). Not `Ability to` — there's no new user capability, so the action itself is the deliverable.
  - **Polish** (optimize what already works and is already extracted) → **`Optimize {thing}`** / **`Simplify {thing}`** / **`Harden {thing}`**. Not a new feature, not a new extraction.
- **One line, no em-dash clauses.** If you'd append `— detail`, fold it in plainly or split it into another task. Use **`and`**, never `+`. Group only *closely-related* capabilities (`edit and delete your codes`); split *unrelated* ones (generate vs download = two tasks).
- **Capability-grained + abstract** — one bullet per user-facing capability (the `CRUD the entity` level). Never per-endpoint / per-field. No table/column, service/class names, or file paths — those live in code + architecture docs. Don't name a property that isn't itself a feature (an immutable slug is not a task).
- **Verification iteration** — optional, but **when present, it is always the final iteration**; no build iteration follows it. Its name is the bare noun **`Verification`** — no description / goal after it (self-evident). Use it when a version needs manual sign-off beyond automated tests, and have it cover the version's final, fully-delivered state. Its items are **ordered, concrete check steps**, not capabilities: `[ ] {action} → {expected result}`, run top-to-bottom. The one place specifics are allowed (you're checking the real thing). Sign-off = ticking them + flipping `Status` → `✅`.
- **No `## Log` section.** Git is the full history — never keep a hand-maintained changelog / journal / per-date log inside a version doc or planning doc. The doc records the version's *current* shape (iterations + tasks + status); how it got there lives in the git log.
- **Meta line is `**Type:** … · **Status:** … · **Started:** … · **Completed:** …` only.** No per-iteration date breakdowns or other parentheticals appended (`*(Iter 1–9: … · Iter 10: …)*`). Per-iteration timing is git's job; the meta line carries only the four fields.
- **`**Type:**` is required** on every version doc's meta line — exactly one of `Feature` · `Adoption` · `Polish` (see [Version types](#version-types)). It is not optional; a version doc without a declared Type is incomplete.
- **A version doc covers ONLY its own app / repo.** Record what *this* app ships in this version — nothing more. Cross-app rollout (e.g. an SDK module extracted here and then adopted by other apps) belongs in **those apps' own version docs**, not here; reference it at most, never enumerate another app's counts / state. A Verification iteration checks **this** app only.

## Iteration spec docs

A per-iteration **temp spec** is a transient planning aid — never a permanent artifact.

- **When an iteration starts**, write a **super-compact plan** to a temp file in the version folder: `engineering/versions/v{X.Y}/{iter-slug}.md`. One-liners only: *what* we'll change + *how* — no prose, no logs.
- **Review + refine it together BEFORE implementing.** Its whole purpose is to lock the plan up front so the version doc itself isn't churned with mid-work edits.
- **Delete it once the iteration is done.** It leaves no trace — the version doc (iterations + tasks) is the only durable record; git carries the history.

## Template — copy below the line

---

# v{X.Y} — {Theme}

*Last updated: {YYYY-MM-DD}*

**Status:** ⏳ Planned · **Type:** {Feature | Adoption | Polish} · **Started:** {YYYY-MM-DD} · **Completed:** —

### Iteration 1 — Listing ingest

- [ ] Ability to pull new listings on a schedule, skipping ones already saved.

### Iteration 2 — Match classification

- [ ] Ability to classify new listings and mark the matches.

### Iteration 3 — Channel alerts

- [ ] Ability to alert the channel when a new match appears.

### Iteration 4 — Verification

- [ ] Run a scrape → new listings stored, duplicates skipped.
- [ ] Run classify → each listing recorded, matches flagged.
- [ ] Add a matching listing → the channel receives one formatted alert.

---

> **Note — no `## Log`.** This template has no log/changelog section by design; git is the history (see [Iteration spec docs](#iteration-spec-docs) for the transient per-iteration `{iter-slug}.md` plan that's written at iteration start and deleted when it's done).

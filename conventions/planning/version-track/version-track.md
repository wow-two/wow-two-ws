# Version Track

*Last updated: 2026-09-29*

The only planning convention: a repository plans with one backlog and one folder per version, the iterations and
capabilities a product ships in that version.

## Planning files [REQUIRED]

A repository plans with exactly two things, both under `engineering/planning/`:

| Path | Holds |
|---|---|
| `backlog.md` | every unbuilt item — feature, fix, engineering work — in grouped tables, top of each group = next; plus the `Features` group |
| `version-track/v{X.Y}/v{X.Y}.md` | one version: its iterations and tasks; the newest folder is the active version |

- must not keep any other planning file: no `planning.md` (engineering or product), no roadmap, no `features.md`,
  no version-track lead doc, no `engineering/versions/`, no second track (rough, polish, vector)
- CI derives the product's `X.Y` from the newest `engineering/planning/version-track/v{X.Y}/` folder, so every
  product repository uses exactly that path
- must move a settled decision that still binds to `product/context.md` (product) or `engineering/architecture/`
  (technical); logs, history and superseded decisions go, since git keeps them
- working rules for agents in the repository live in `engineering/development/rules.md`; analyses and deep-dives live
  in `engineering/research/`
- ecosystem-wide work — an SDK upgrade, an extraction that spans products — lives in the SDK repository's backlog or
  in wow-two-ws, never in a product backlog; a product's own adoption of an SDK capability stays in its backlog

---

## Backlog

- must group items into tables, one `## {Group}` per theme; the top row of each group is the next to pull
- must hold each unbuilt item once, as `Item · Type · Notes`; Type is `feature` · `fix` · `engineering` · `product`
  (a milestone, a validation step or launch work)
- must delete an item when it ships — the version doc records it; no strike-through, no done column
- must not tag an item with a future version — order by pull priority; the next version pulls from the top
- must open with a `Features` group: one compact line per feature of the product, `Feature · State · Spec`, State
  `shipped v{X.Y}` or `planned`, Spec a link to its `product/features/` file while one exists, else `—`
- a version's leftovers land at the top of their group when it closes

---

## Location & naming

- must place each version at `engineering/planning/version-track/v{X.Y}/v{X.Y}.md` — one folder per version, file
  named after its folder; never a flat `v{X.Y}.md`
- must start at `v0.1`; minor-increment `Y`; bump major `X` only at `Y = 100` or a breaking change
- must treat the newest folder as the active one
- the active version's `X.Y` is the product's code version; CI assigns the patch `Z` to each release from `main`
  ([versioning](../../development/repo/versioning/versioning.md))

---

## Scope

- must be exactly one type, declared on the meta line:

| Type | Scope | Task verb |
|---|---|---|
| `Feature` | a new user-facing capability, or a bug fix | `Ability to {capability}` · `Fix {behavior}` |
| `Adoption` | a large or interconnected extraction to / from the SDK (a whole layer / coupled set) | `Extract {thing} → SDK` · `Adopt {SDK thing}` |

- must hold ≤ 1 week of work — overflow goes to `engineering/planning/backlog.md`
- must plan only the next version — future work waits in the backlog
- a cycle is `Feature` → `Adoption`; 1 cycle = 2 versions (full model → `../../development/dev-cycle.md`)
- must number a `Feature` version with an odd minor and an `Adoption` version with an even minor (`v0.5` · `v0.6`)
- may hold `Polish` iterations beside its capability iterations, whatever its type (below)

---

## Structure

- must group `### Iteration {N} — {noun}` → `[ ]` tasks; the iteration name is its focus noun, no `: {goal}` clause
- must write each task as a capability the version delivers — abstract, user-POV: `Ability to log in as a guest`, not `Mint a guest cookie`
- may break a task into indented `- [ ]` **sub-steps** when the how needs itemizing — a sub-step is one concrete action (the *what* + *where*), never a paragraph
- must open each task with the Type verb — `Ability to` / `Fix`; `Extract … → SDK` / `Adopt …`; a Polish task opens with a Polish verb
- must keep one capability per task on one line — no `— detail` clause; join closely-related with `and`, split unrelated
- must follow the **Task form** below
- must stay capability-grained — never per-endpoint, per-field, or naming a table / class / file; Polish tasks excepted
- may close with a `### Verification` iteration — always last, bare noun, ordered `[ ] {action} → {expected}` checks
- must carry meta `**Status:** … · **Type:** … · **Started:** … · **Completed:** …` (those four only); declare a `Type`; title is a plain noun phrase

---

## Polish iterations

Behavior-invariant reshaping of code that already works runs as `Polish` iterations inside a version; there is no
separate polish track and no polish release.

- must not change observable behavior — same inputs, same outputs; the test suite is green before and after
- may reshape at any size inside the app — rename, dedupe, split, move, re-layer, rewrite at parity
- must open each task with one of four verbs — `Refactor` · `Rename` · `Remove` · `Split` — and name the code it
  reshapes (a module, a component, a layer)
- may itemize a task into sub-steps that name the files it touches
- must name the iteration for the area it reshapes, ending in `polish`: `### Iteration 4 — Registry polish`
- must send a behavior change, a bug fix included, to the backlog or a capability iteration — never land it in a
  Polish iteration
- may extract one small component to the SDK as a Polish task; a large or coupled extraction is an `Adoption` version

---

## Task form

- must write each task **verb-first** — a concrete action, never a noun phrase or an `X → Y` mapping. `Move api.ts to integration/`, not `api.ts → integration`.
- must keep **one action per bullet** — split a multi-part change into separate bullets. More bullets is fine; density comes from fewer words per task, not fewer tasks.
- must use the fewest words that name the action + its target; backtick identifiers, drop restatement.
- must cap a task line at **75 characters**, counting the `- [ ] ` marker. A task that will not fit is not one action, or it is carrying detail that belongs elsewhere.
  - over the cap → **split** it into two tasks, or **drop the detail**; move it into the architecture docs only when it is still load-bearing.
  - **detail about work already done gets deleted, not relocated.** The compact task line is the record that the capability shipped; git holds how.
  - relocate only what a *future* reader needs to decide something: an open fork, a constraint that still binds, a rejected option and why. A version number, a test count, or a defect mapping for closed work is history — cut it.
  - never wrap a task across lines to satisfy the cap — the cap measures scope, and wrapping only hides that the scope is wrong.
- must not carry an em-dash clause, a parenthetical rationale, a quote, or a file:line reference in a task line.
- may sit a `- [ ]` **sub-step** under a task, under the same cap, when the *how* needs itemizing.

```markdown
<!-- ❌ Wrong — 4 facts, a rationale, and a file ref on one line -->
- [ ] **Thin `CodePayload` down** *(shifted from Iteration 6)* — drop the `?? string.Empty` fallback once validation guarantees it; rehome `SlugPlaceholder` off the controller

<!-- ✅ Correct — one action each, rationale lives in the architecture docs -->
- [ ] Drop the `CodePayload` empty-string fallback
- [ ] Rehome `SlugPlaceholder` off the controller
```

---

## Prose inside a version doc [REQUIRED]

The task-form rules govern task lines. This governs everything else on the page, which is where residue actually accumulates.

- must keep a **completed** iteration's prose to zero. Its compact task lines are the whole record; a `>` blockquote or a standing paragraph under a done iteration is residue whether it was written last week or at the start.
- must not carry a fact in a version doc that outlives the version. A version doc is time-scoped and gets archived; these are not, and each has a real home:

| Residual fact | Home |
|---|---|
| Design tokens, palettes, type scales | the design system / `@theme`, never a version doc |
| A deferred item and why | `engineering/planning/backlog.md` |
| A known coverage gap or stub | the test suite's own doc, or an open task |
| A dated verification run | the `**Completed:**` meta field, which already holds it |
| An architectural constraint that still binds | `engineering/architecture/` |
| A product decision that still binds | `product/context.md` |

- must not restate meta in the body — a run date, a status, or a completion date belongs in the `**Status:** …` line and nowhere else.
- must not keep **re-scoping history** — no `**Rescoped {date}** — X moved to v0.9`, no note that an item arrived from elsewhere, no record of what a version used to contain. A task moves between iterations and versions many times as priorities shift; each move would leave a note, and the notes outnumber the tasks. **The current task list IS the scope**, and git holds every earlier shape of it. This is the same rule as *must move an item, never leave a forwarding stub*, applied to the version as a whole.
- may keep prose under an **open** iteration when its open tasks need it, and must delete that prose when the iteration closes.

---

## Lifecycle

- `⏳ Planned` → `🚧 In Progress` → `✅ Complete`
- must open a version when planning it and close it when its tasks are done — set `Completed`, flip `Status`; one active at a time
- must not advance to the next version until the current is `✅ Complete` **and** the developer explicitly says to proceed — never pre-declare, queue, or auto-begin the next version (in chat or in the plan); finish, report, and stop
- must **verify completion with the developer** before marking a version / iteration complete — never self-declare it
- must treat a `Verification` iteration's checks as the **developer's manual pass** — they tick on the developer's word, not on evidence in the tree; every other task ticks only on shipped code
- must **move an unshipped task to the next version** when closing a version — a closed version's task list describes only what shipped. Carry it to the iteration whose focus it fits, or open a new one named for that focus; never name the new iteration after where the task came from, and never leave a note that it moved
- must not apply that rule **within** an open version — a closed iteration inside an in-progress version may sit beside open ones, since iterations are not worked in order
- must **strip a completed iteration's sub-steps** once verified — a sub-step itemizes *how* to build something already built, so it is spent the moment the iteration closes; git holds it
- must leave the completed iteration's **tasks** in place, one compact line each, as the record of what the version delivered — rewrite any that were never compact rather than carrying the sprawl forward
- may drop the tasks too once the whole version is `✅ Complete`, keeping the bare `### Iteration N — Name` heading

---

## Rules

- must write a transient plan at `engineering/planning/version-track/v{X.Y}/{iter-slug}.md` at iteration start (what + how), review before implementing, delete when done
- a handoff between chats follows the handoff rule in [agentic-workflow.md](../../agentic-workflow/agentic-workflow.md#handoff-docs--write-once-read-once-delete); the version doc outranks it
- must record green (build / test counts) only in the `Verification` iteration — never on a build iteration
- must not put a status emoji on an iteration heading — the `[ ]` / `[x]` checkboxes carry done-state
- must keep the iteration heading a **bare name** — just the focus noun; no trailing `(done)` / `(final)` / parenthetical / status / version tag
- must not frame or report the work as *closing* / *finalizing* the version — report per iteration (*did X, Y; Z remaining*); a track is open-ended, extend it freely, never push it toward closure
- must cover only this repo — another app's rollout lives in that app's version doc
- must not keep a `## Log` — git is the history
- must **move** an item that changes iteration, never leave a forwarding stub (`→ moved to Iteration N`). The destination line is the record; a stub duplicates state and goes stale the moment the item moves again
- must not name the current iteration in the doc — it is the first one with open boxes. A `(current)` tag is a second source of truth that rots on every advance

---

## Template — version doc, copy below the line

---

# v{X.Y} — {Theme}

*Last updated: {YYYY-MM-DD}*

**Status:** ⏳ Planned · **Type:** {Feature | Adoption} · **Started:** {YYYY-MM-DD} · **Completed:** —

### Iteration 1 — Listing ingest

- [ ] Ability to pull new listings on a schedule, skipping ones already saved.

### Iteration 2 — Match classification

- [ ] Ability to classify new listings and mark the matches.

### Iteration 3 — Classifier polish

- [ ] Split the classifier into rule loading and matching
- [ ] Rename `ListingJob` to `IngestJob`

### Iteration 4 — Verification

- [ ] Run a scrape → new listings stored, duplicates skipped.
- [ ] Run classify → each listing recorded, matches flagged.

---

## Template — backlog, copy below the line

---

# {Brand} — Backlog

*Last updated: {YYYY-MM-DD}*

Every unbuilt item, grouped; top of each group = next. Shipped work lives in [`version-track/`](version-track/).

## Features

| Feature | State | Spec |
|---|---|---|
| Guest login | shipped v0.3 | [guest-login.md](../../product/features/guest-login.md) |
| Saved searches | planned | — |

## {Group}

| Item | Type | Notes |
|---|---|---|
| {item} | feature | {note} |

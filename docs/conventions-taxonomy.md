# Conventions Taxonomy — product-vs-SDK reorg

*Last updated: 2026-09-29*

A proposal for reshaping `conventions/development/` so it serves both repo archetypes (product/venture vs SDK/library) cleanly and stays coherent as the convention set grows. Read-only analysis — no file has moved; the owner reviews before any restructure.

## Problem

- `conventions/development/` splits into `repo/` · `backend/` · `frontend/`. That worked when every repo was a product with one .NET backend + one React frontend.
- The new `repo/sdk-structure.md` is **repo-shape** convention but for the **SDK/library** archetype. It has no clean home:
  - putting it in `frontend/` is wrong — `frontend/` is **code style**, this is **repo shape** (and the archetype covers backend SDKs too, not just the UI lib);
  - leaving it flat in `repo/` beside `repo-structure.md` **conflates two archetypes** — a reader can't tell which shape applies to which repo kind.
- Splitting `repo/` by **stack** (backend-repo vs frontend-repo) breaks the **product** archetype: a product is ONE repo holding BOTH stacks (`engineering/codebase/{slug}.backend-services` + `{slug}.frontend-services`). Stack is the wrong axis for repo shape.
- Net: the tree is stranded between two archetypes — **SDK repo** (single-stack, one package) vs **product repo** (multi-stack, one repo) — and the current folders encode neither.

## Axes a clean taxonomy must separate

Three independent axes. Today's tree collapses them, which is why placement is ambiguous.

| Axis | Values | Governs | Keyed by |
|---|---|---|---|
| **Archetype** | product/venture · SDK/library | repo **SHAPE** — folders + names on disk | the repo kind |
| **Stack** | backend (.NET) · frontend (React) | **CODE STYLE** — idioms, naming, docs | the language, not the repo |
| **Concern** | repo-shape · code-style · planning · cross-cutting | which folder a doc belongs to at all | what the doc is about |

The load-bearing observation:

- **Repo shape is archetype-keyed.** Product shape (`product/` + `engineering/`, two code dirs, single-host serving) ≠ SDK shape (no `product/`, one package under `engineering/codebase/{slug}/`, dist-only publish). `repo-structure.md` and `sdk-structure.md` are the two halves.
- **Code style is stack-keyed and archetype-agnostic.** The `backend/` rules apply to a product's backend AND to `WoW.Two.Sdk.Backend.Beta`; the `frontend/` rules apply to a product's frontend AND to `@wow-two-beta/ui`. This is already codified — `backend-conventions.md` / `frontend-conventions.md` say "every backend/frontend repo," and `conventions.md` §Precedence says naming + docs conventions "apply to the backend-beta SDK too." So code style must NOT nest under an archetype — that would duplicate it.
- **The two axes are orthogonal and must never nest inside each other.** Shape splits by archetype; style splits by stack; a product repo draws from one archetype-shape + both stack-styles; an SDK repo draws from one archetype-shape + one stack-style.

That principle is the north star for every option below.

## Current tree (annotated)

```
conventions/
├── conventions.md                         ← root index + authoring rules
├── development/                            ← ★ the reorg target
│   ├── development-conventions.md          ← area index
│   ├── dev-cycle.md                        [cross-cutting] app↔SDK 2-cycle rhythm
│   ├── sdk-extraction.md                   [cross-cutting] extract / keep / remove decision
│   ├── swappable-modules.md                [cross-cutting] engine-wrapping SDK modules
│   ├── repo/                               ← concern: repo SHAPE (+ shared setup)
│   │   ├── repo-conventions.md             ← index
│   │   ├── repo-structure.md               [shape · PRODUCT archetype]
│   │   ├── sdk-structure.md                [shape · SDK archetype]  ← the misfit
│   │   ├── single-host-serving.md          [shape · PRODUCT · multi-stack seam]
│   │   ├── tech-stack.md                   [shared setup — names both stacks]
│   │   ├── ports.md                        [shared setup — dev-port ledger]
│   │   └── git.md                          [shared setup — commit format]
│   ├── backend/                            ← concern: CODE STYLE · stack .NET (archetype-agnostic)
│   │   ├── backend-conventions.md
│   │   └── build/ code-style/ architecture/ persistence/ presentation/
│   │       runtime/ foundation/ integrations/ testing/ messaging/ identity/
│   └── frontend/                           ← concern: CODE STYLE · stack React (archetype-agnostic)
│       ├── frontend-conventions.md
│       └── code-style/ architecture/ presentation/
├── planning/            [sibling domain] version-track (backlog + versions)
├── agentic-workflow/    [sibling domain] parallel-chat lanes
├── marketing/           [sibling domain] naming · GTM · channels
└── design/              [sibling domain] variant-driven design exploration
```

- Sibling domains (`planning/` `agentic-workflow/` `marketing/` `design/`) are **out of scope** — they're stable and orthogonal to the archetype tension. The reorg touches `development/` only.
- Everything inside `backend/**` and `frontend/**` is code style; their internal sub-domain structure is sound and stays intact under every option.
- Misfits to resolve: `sdk-structure.md` (headline) · `single-host-serving.md` (product-only, spans both stacks) · the three shared-setup docs (which archetype, if any).

---

## Option A — concern-first, both axes named at the top

Label the concern at the top level: `repo/` = shape (split by archetype), `code/` = style (split by stack). The two axes become self-documenting.

```
development/
├── development-conventions.md
├── dev-cycle.md · sdk-extraction.md · swappable-modules.md     ← cross-cutting root docs
├── repo/                               ← CONCERN: repo SHAPE
│   ├── repo-conventions.md
│   ├── shared/                         ← archetype-agnostic setup
│   │   ├── tech-stack.md · ports.md · git.md
│   ├── product/                        ← ARCHETYPE: product / venture
│   │   ├── product-repo.md  (lead)
│   │   ├── repo-structure.md
│   │   └── single-host-serving.md
│   └── sdk/                            ← ARCHETYPE: SDK / library
│       ├── sdk-repo.md  (lead)
│       └── sdk-structure.md
└── code/                               ← CONCERN: CODE STYLE
    ├── code-conventions.md
    ├── backend/                        ← STACK: .NET  (all existing subfolders unchanged)
    └── frontend/                       ← STACK: React (all existing subfolders unchanged)
```

| Doc | Lands at |
|---|---|
| `repo-structure.md` | `repo/product/repo-structure.md` |
| `single-host-serving.md` | `repo/product/single-host-serving.md` |
| `sdk-structure.md` | `repo/sdk/sdk-structure.md` |
| `tech-stack.md` · `ports.md` · `git.md` | `repo/shared/` |
| `backend/**` | `code/backend/**` |
| `frontend/**` | `code/frontend/**` |
| `dev-cycle` · `sdk-extraction` · `swappable-modules` | `development/` root (unchanged) |

- **Pros:** both axes named at the top — "shape or style?" then "which archetype / which stack?" resolves every doc. Most self-documenting; maximally future-proof (new archetype → `repo/{x}/`; new stack → `code/{x}/`; the axes never cross). Code style authored once, shared across archetypes.
- **Cons:** largest migration — every `backend/**` + `frontend/**` file moves under `code/`, and every inbound `../backend/…` / `../../repo/…` cross-link re-paths (dozens across the tree + `conventions.md` + root `CLAUDE.md` + `create-repo` skill). Adds a nesting level to the deepest trees (`code/backend/persistence/migrations/…`) and a `repo/shared/` folder for 3 docs.

## Option B — archetype split inside `repo/`, code stays at root (RECOMMENDED)

Fix only what's broken. `repo/` gains the archetype split; `backend/` + `frontend/` stay exactly where they are (they're already unambiguous as code-style-by-stack, and nothing about them is wrong).

```
development/
├── development-conventions.md
├── dev-cycle.md · sdk-extraction.md · swappable-modules.md     ← cross-cutting root docs
├── repo/                               ← repo SHAPE (split by ARCHETYPE) + shared setup
│   ├── repo-conventions.md
│   ├── product/                        ← ARCHETYPE: product / venture (multi-stack, one repo)
│   │   ├── product-repo.md  (lead)
│   │   ├── repo-structure.md
│   │   └── single-host-serving.md
│   ├── sdk/                            ← ARCHETYPE: SDK / library (single-stack, one package)
│   │   ├── sdk-repo.md  (lead)
│   │   └── sdk-structure.md
│   ├── tech-stack.md                   ← shared setup (flat at repo/ root)
│   ├── ports.md
│   └── git.md
├── backend/                            ← CODE STYLE · .NET   (unchanged)
└── frontend/                           ← CODE STYLE · React  (unchanged)
```

| Doc | Lands at |
|---|---|
| `repo-structure.md` | `repo/product/repo-structure.md` |
| `single-host-serving.md` | `repo/product/single-host-serving.md` |
| `sdk-structure.md` | `repo/sdk/sdk-structure.md` |
| `tech-stack.md` · `ports.md` · `git.md` | `repo/` root (shared, unchanged) |
| `backend/**` · `frontend/**` | unchanged |
| `dev-cycle` · `sdk-extraction` · `swappable-modules` | `development/` root (unchanged) |

- **Pros:** solves the exact stated problem with proportionate churn — the archetype axis (product vs SDK) now governs repo shape, which is precisely what was missing. `sdk-structure.md` gets a clean, parallel home; product keeps its two shape docs together; `backend/`+`frontend/` and all their inbound links are untouched. Future-proof on both axes (add `repo/{archetype}/`; add a sibling stack folder at root). Shared setup stays flat — no `shared/` folder for 3 docs.
- **Cons:** the concern label (shape vs style) is implicit — `backend/`+`frontend/` sit as peers of `repo/` rather than under a named `code/`. Mild asymmetry: archetype docs nest (`repo/product/…`) while shared setup is flat at `repo/` root — the `repo-conventions.md` index must call out that `tech-stack`/`ports`/`git` are cross-archetype.
- **Growth path:** B is the front half of A. If the doc count later justifies naming the concern, wrap `backend/`+`frontend/` in `code/` and lift the 3 shared docs into `repo/shared/` — the archetype split done here carries over with zero rework.

## Option C — minimal change: shared `repo/` + one `archetypes/` subfolder

Least disruption. Keep `repo/` as the single repo folder; corral only the two archetype-shape docs into `repo/archetypes/`. Leave the rest of `repo/` flat.

```
development/
├── development-conventions.md
├── dev-cycle.md · sdk-extraction.md · swappable-modules.md
├── repo/
│   ├── repo-conventions.md
│   ├── archetypes/                     ← the only new folder
│   │   ├── archetypes.md  (lead — the product-vs-SDK table, lifted from repo-structure §1)
│   │   ├── product-structure.md        ← was repo-structure.md
│   │   └── sdk-structure.md            ← moved in
│   ├── single-host-serving.md          ← stays flat (product-only — leaks out of archetypes/)
│   ├── tech-stack.md · ports.md · git.md
├── backend/   (unchanged)
└── frontend/  (unchanged)
```

| Doc | Lands at |
|---|---|
| `repo-structure.md` | `repo/archetypes/product-structure.md` (rename) |
| `sdk-structure.md` | `repo/archetypes/sdk-structure.md` |
| `single-host-serving.md` | `repo/` root (unchanged — the leak) |
| `tech-stack.md` · `ports.md` · `git.md` | `repo/` root (unchanged) |
| `backend/**` · `frontend/**` | unchanged |

- **Pros:** smallest footprint — one new folder, two docs moved, a lead doc added. Directly de-conflates the two archetype shapes (they're explicit siblings under `archetypes/`) without touching code style.
- **Cons:** **incomplete** — `single-host-serving.md` is product-archetype-only yet stays outside `archetypes/`, so the grouping leaks; moving it drifts C toward B anyway. `archetypes/` lumps both archetypes in one folder, giving neither room to grow its own multi-doc set (product already wants shape + single-host + more). Cheaper than B by only ~3 inbound links (moving `repo-structure.md` re-paths its ~12 refs under any option), so C buys little over B while scaling worse.

---

## Recommendation — Option B

- Encodes the missing axis exactly where it belongs: **repo shape splits by archetype** (`repo/product/` vs `repo/sdk/`), never by stack — which is the precise error the owner flagged.
- **Proportionate churn:** touches 3 repo docs + their inbound links; leaves the ~60-file `backend/`+`frontend/` trees and their links alone (they aren't the problem). C saves only ~3 links over B yet scales worse; A's `code/` relabel is a large migration for a naming benefit, not a functional fix.
- **Future-proof both ways:** new archetype (CLI tool, browser extension, pure-infra platform lib) → a new `repo/{archetype}/`; new stack (Rust/Python tool) → a sibling folder at `development/` root. The orthogonal axes never collide.
- **Clean growth path to A:** adopt B now; promote to A later by wrapping `backend/`+`frontend/` in `code/` and lifting shared setup into `repo/shared/`, with no rework of the archetype split. Recommend B now, revisit the `code/` relabel only if the concern ambiguity actually bites.

### Migration for B (proposal — do NOT execute)

**Files moved (3):**
- `repo/repo-structure.md` → `repo/product/repo-structure.md`
- `repo/single-host-serving.md` → `repo/product/single-host-serving.md`
- `repo/sdk-structure.md` → `repo/sdk/sdk-structure.md`

**New lead docs (2):** `repo/product/product-repo.md` · `repo/sdk/sdk-repo.md` — each a short index for its archetype (lift the product-vs-SDK archetype table from `repo-structure.md` §1 into whichever lead reads cleanest, cross-link the other).

**Unchanged:** `tech-stack.md` · `ports.md` · `git.md` (flat in `repo/`) · all of `backend/**` · `frontend/**` · the three cross-cutting root docs.

**Indexes / links to update:**
- `conventions.md` — repo/ table: re-path `repo-structure` → `repo/product/…`, `single-host-serving` → `repo/product/…`; **add a row for `sdk-structure`** (`repo/sdk/…`) — it is currently missing from the root index entirely.
- `development/repo/repo-conventions.md` — re-path all three; regroup the table under **product / sdk / shared**.
- `development/development-conventions.md` — repo/ row note.
- `development/backend/backend-conventions.md` (line 7 + Notes) · `development/frontend/frontend-conventions.md` (lines 7–8) — `../repo/repo-structure.md` → `../repo/product/repo-structure.md`.
- `development/backend/code-style/code-organization.md` (§3 ref) · `build/build.md` (§5 ref) · `build/directory-build-props.md` (§13 + single-host-serving refs) — re-path to `repo/product/…`.
- Moved docs' own internal links: `sdk-structure.md` `repo-structure.md` → `../product/repo-structure.md`; `repo-structure.md` §1 `sdk-structure.md` → `../sdk/sdk-structure.md`; `single-host-serving.md` §10 ref → `product/repo-structure.md` (now a sibling).
- Repo root `wow-two-ws/CLAUDE.md` — `conventions/development/repo/repo-structure.md` (§3 no-README, §5) → `repo/product/repo-structure.md`.
- `.claude/skills/create-repo/SKILL.md` — `repo-structure.md` ref → `repo/product/repo-structure.md`.

## Open calls

- **Hardest placement — `single-host-serving.md`.** It sits at the crossing of all three axes: multi-stack (the backend↔frontend `wwwroot` seam), concern-ambiguous (build/serve wiring, not C#/React idioms → not clearly "code style"), yet product-archetype-only. The **archetype axis wins** — it exists only because a product co-locates both stacks in one deployable — so it lands in `repo/product/`, not `code/`. Every other misfit resolves trivially once the archetype axis exists; this is the one genuinely torn doc.
- **Runner-up — `tech-stack.md`.** Names both stacks + the beta SDKs and is cited by product AND SDK code (`directory-build-props` reads `net10.0` from it). Treated as **shared** (`repo/` root), not product-only, despite its "product/venture" self-description — an SDK repo runs the same React/Vite/.NET floor.
- **Optional rename for symmetry:** `repo/product/repo-structure.md` → `product-structure.md` to pair with `sdk-structure.md`. Deferred — `repo-structure.md` is a widely-referenced known name; the `product/` folder already disambiguates, so the rename's link-churn isn't worth it now.

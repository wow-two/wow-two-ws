# WoW 2.0 — One version track

*Last updated: 2026-09-29*

> Consolidates the planning tracks into one authoritative version-track standard and moves every product repo onto
> it. Analysis pool; each decided point lands in [version-track.md](../conventions/planning/version-track/version-track.md)
> and the other conventions it names. Trigger: the developer dropped polish releases (2026-09-29), and CI now reads
> `X.Y` from the newest `engineering/planning/version-track/v{X.Y}/` folder, so that path must hold in every repo.

## Inventory (2026-09-29)

| Source | Says | Problem |
|---|---|---|
| `conventions/planning/version-track/version-track.md` | `engineering/planning/version-track/v{X.Y}/v{X.Y}.md`; Feature / Adoption types | the standard |
| `conventions/planning/polish-track/polish-track.md` | separate `p{X.Y}` track for behavior-invariant cleanup | dropped by decision |
| `conventions/planning/rough-track/rough-track.md` | `r{X.Y}` first build before any version | a second numbering before `v0.1` |
| `conventions/planning/vector-track/vector-track.md` | subject lanes running rough, version or polish inside | names the retired tracks |
| `conventions/planning/planning-conventions.md` | track order `rough` → `polish` → `version`; plans in `engineering/versions/` | old order and path |
| `conventions/planning/engineering-planning/engineering-planning-conventions.md` | per-version detail in `versions/v{X.Y}/v{X.Y}.md` | old path |
| `conventions/development/repo/structure/repo-structure.md` | layout lists `polish-track/`; §4 cites `versions/` | retired track, old path |
| `conventions/development/repo/structure/sdk-structure.md` | `version-track/` + `polish-track/`; one `v0.1.md` flat file | retired track, flat file |
| `conventions/development/dev-cycle.md` | cycle = Feature then Adoption version | stays; references need no change |
| `conventions/conventions.md`, `docs/conventions-taxonomy.md` | index rows for rough, version, polish | retired rows |
| `docs/versioning-strategy.md` | apps link `conventions/planning/version-planning/version-docs.md` | dead link |
| Product template `engineering/versions/versions.md` | old path, dead convention link | every new repo inherits it |
| `create-repo` skill | scaffolds `versions/ versions.md` | same |

| Repos | State |
|---|---|
| ForeverPin, TranscriptForge | polish tracks (3 and 2 iterations) beside their version tracks |
| pose-coach | rough track |
| 20 repos, the product template among them | old `engineering/versions/`; 6 of them also have `version-track/` |

---

## Points

- [x] V1 — Polish inside versions
- [x] V2 — Rough track
- [x] V3 — Canonical path, template and scaffold
- [x] V4 — Retire duplicate rules
- [x] V6 — One backlog file
- [x] V7 — Per-feature spec files
- [ ] V5 — Repo migration

---

### V1 — Polish inside versions

Decided 2026-09-29: no polish releases and no polish track; polish work becomes iterations inside version docs.

- Built 2026-09-29: version-track.md § *Polish iterations* — behavior-invariant, verbs `Refactor` · `Rename` ·
  `Remove` · `Split`, named `{Area} polish`; the Feature / Adoption types stay.

### V2 — Rough track

Decided 2026-09-29: the rough track goes too. A rough track's tasks merge into ordinary version-track versions; no
special version type.

### V3 — Canonical path, template and scaffold

Built 2026-09-29: `engineering/planning/backlog.md` + `version-track/v{X.Y}/v{X.Y}.md` only (V6 removed the lead
doc); no `engineering/versions/`, no flat `v0.1.md`. The product template now ships `backlog.md`,
`version-track/v0.1/v0.1.md` and `engineering/development/rules.md`; the `create-repo` skill's layout matches.

### V4 — Retire duplicate rules

Decided 2026-09-29: version-track is the only planning convention left. Delete polish-track, rough-track,
vector-track, engineering-planning and the planning index (`planning-conventions.md`).

- Built 2026-09-29: the five files are deleted; the task form lives in version-track.md, the handoff rule in
  agentic-workflow.md; the conventions index, taxonomy, repo and SDK structure, dev-cycle and versioning-strategy
  cite version-track.md.
- Deferred work lives in `backlog.md` (V6 superseded the lead-doc `Backlog` section); ecosystem-wide work goes to
  wow-two-ws or the SDK repository's backlog.

### V5 — Repo migration

- One agent per repository: move old paths, fold polish, rough and vector tracks into version docs, merge
  `planning.md`, product planning, `features.md` and roadmap files into `backlog.md` (V6) and delete them, keep
  history in git, commit per repository under its commit flag.
- Scope: 31 repositories under `workbench/` with `engineering/` or `product/`; Wheelhouse migrates itself; ocharo-ws
  repositories wait until the developer says the other chat has left.
- Done 2026-09-29 for 30 repositories plus the template, one subagent each
  ([brief](../system/sessions/version-track-consolidation/repo-agent-brief.md)):

| Outcome | Repositories |
|---|---|
| Committed | Haven `b1f6a6b` · ForeverPin `44da868` · TranscriptForge `50f0543` · ListingShelf `2a66e95` · TNIS `c3d42e4` · backend SDK `1299540` |
| Committed with the other lanes' pending work, in cohesive batches (developer greenlight, 2026-09-29) | UI SDK `306601d` · PRISM `54ed9c6` · Museums Gallery `3bfe7d0` · Secrets Vault `6b549aa` · Whiteout `546d721` · Hijinx `c960fbe` |
| Staged, left by the developer's call | TNIS-mintrans · TransportBrain |
| Untracked repositories, nothing to stage | the ten first-batch ventures · Arcade · Sift · PbnStudio · PoseCoach · home-reno · product template |
| No planning files | tbs.demo |

- Folded tracks: ForeverPin polish → Polish iterations in v0.7, v0.9, v0.11; TranscriptForge polish → v0.4, v0.8;
  PoseCoach rough → v0.1; TNIS vector lanes → v0.1–v0.3; UI SDK Vue port and sweep → v0.1 iterations 9–14.
- Ecosystem gaps the products raised went to the SDK backlogs (`Product-reported gaps`) and to the wow-two-ws task
  backlog (conventions, product template).
- Needs: V2, V3, V4.

### V6 — One backlog file

Decided 2026-09-29: a repository plans with exactly `engineering/planning/backlog.md` and
`engineering/planning/version-track/v{X.Y}/v{X.Y}.md`; the newest folder is the active version.

- Merge into the backlog, then delete: `engineering/planning/planning.md` (35 repositories), `product/planning/planning.md`
  (32), `product/features/features.md` (30), any roadmap file, and the version-track lead doc `version-track.md`.
- The backlog holds every unbuilt item (feature, fix, engineering work) in grouped tables, top of each group = next;
  shipped work lives in the version docs.
- Settled decisions that still bind move to `product/context.md` (product) or `engineering/architecture/` (technical);
  logs and history go, since git keeps them.
- `engineering/planning/rules.md` (32) is not planning: it moves to `engineering/development/rules.md`.
- Planning-folder analyses (the backend SDK's `data-pipeline/`, `messaging/`, `identity/`, …) move to
  `engineering/research/`.
- Unchanged: `product/product.md`, `product/context.md`, `product/flows/`, `product/marketing/`, `product/research/`.

### V7 — Per-feature spec files

Decided 2026-09-29: keep existing feature files for now; the developer deletes them later.

- `backlog.md` gets a `Features` group: one compact line per feature from `features.md` and every per-feature file,
  with its state (`shipped vX.Y` or `planned`) and, while the file exists, a link to it.

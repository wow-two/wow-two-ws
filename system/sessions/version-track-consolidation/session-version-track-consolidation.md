# Session — one version track

*Last updated: 2026-09-29*

> Brief for the chat that consolidates wow-two planning onto one version-track standard and migrates every product
> repository onto it. Inventory and points: [docs/version-track-consolidation.md](../../../docs/version-track-consolidation.md).
> State: [context.md](context.md).

## Decided

- Version-track is the only planning convention left. Delete polish-track, rough-track, vector-track,
  engineering-planning and the planning index `conventions/planning/planning-conventions.md`.
- Polish work becomes iterations inside version docs: add a `Polish` iteration kind to
  `conventions/planning/version-track/version-track.md` (behavior-invariant; verbs `Refactor`, `Rename`, `Remove`,
  `Split`). The Feature / Adoption types stay. A rough track's tasks merge into ordinary versions.
- The shared task form moves into version-track.md; the handoff-doc rule moves to
  `conventions/agentic-workflow/agentic-workflow.md`.
- A repository plans with exactly two things: `engineering/planning/backlog.md` (every unbuilt item — feature, fix,
  engineering work — in grouped tables, top of each group = next) and `engineering/planning/version-track/v{X.Y}/v{X.Y}.md`
  (the newest folder is the active version). No planning file, roadmap file, features list or lead doc.
- Merge into the backlog, then delete: `engineering/planning/planning.md`, `product/planning/planning.md`,
  `product/features/features.md`, any roadmap file, and the version-track lead doc `version-track.md`.
- Settled decisions that still bind move to `product/context.md` (product) or `engineering/architecture/` (technical);
  logs and history go, since git keeps them.
- `engineering/planning/rules.md` moves to `engineering/development/rules.md`; planning-folder analyses (the backend
  SDK's `data-pipeline/`, `messaging/`, `identity/`, …) move to `engineering/research/`.
- Ecosystem-wide engineering (SDK upgrades, extractions across products) goes to wow-two-ws or the SDK repository's
  own backlog.
- Per-feature spec files (`product/features/<feature>.md`, feature subfolders) stay for now; the developer deletes
  them later. `backlog.md` gets a `Features` group: one compact line per feature from `features.md` and every
  per-feature file, with its state (`shipped vX.Y` or `planned`) and, while the file exists, a link to it.
- Unchanged: `product/product.md`, `product/context.md`, `product/flows/`, `product/marketing/`, `product/research/`.
- CI derives a product's `X.Y` from the newest `engineering/planning/version-track/v{X.Y}/` folder, so every product
  repository must use exactly that path.

## Work

1. Conventions: delete `conventions/planning/` `polish-track/`, `rough-track/`, `vector-track/`,
   `engineering-planning/` and `planning-conventions.md`; update version-track.md, agentic-workflow.md, the
   conventions index `conventions/conventions.md`, `docs/conventions-taxonomy.md`,
   `conventions/development/repo/structure/repo-structure.md` (canonical layout: `product/features/`,
   `product/planning/`, `engineering/planning/planning.md` and `rules.md`; §4 `versions/`),
   `conventions/development/repo/structure/sdk-structure.md` (polish-track, flat `v0.1.md`),
   `conventions/development/dev-cycle.md` if it cites a retired track, and the dead link in
   `docs/versioning-strategy.md`.
2. Template and scaffold: `workbench/wow-two-sdk-beta/wow-two-sdk-beta.product-template` (`engineering/versions/`
   → the canonical layout) and the `create-repo` skill (`.claude/skills/create-repo/SKILL.md`, `scaffold.sh`, any
   `.agents/skills` copy).
3. Repositories, one Agent-tool subagent per repository: every Git repository under `workbench/` that has an
   `engineering/` or `product/` folder — ventures, platform repositories such as secrets-vault, and the SDK
   repositories among them. Leave `workbench/ocharo-hq/` for last: another chat works there. When every other
   repository is done, ask the developer whether ocharo-ws is free, then migrate its repositories. Per repository:
   move `engineering/versions/*` into `engineering/planning/version-track/` (merge where both exist); fold polish
   iterations (ForeverPin 3, TranscriptForge 2), rough-track tasks (pose-coach) and vector-track lanes
   (ventures.tnis) into version docs; merge planning, roadmap and feature-list files into `backlog.md` per the rules
   above, then delete them; move `rules.md` and planning-folder analyses; fix the repository's own `CLAUDE.md` and
   file-reference paths; keep history (`mv` + `git add`, or `git mv`).
4. Skip `workbench/wow-two-platform/wow-two-platform.wheelhouse`: another chat works in it and migrates it itself.

## Rules

- Chats share working trees: check `git status` first, never revert another lane's change, stage only your paths.
- Commit a repository only with `git -C <abs-repo> commit -m "subject"` while its commit flag is ON (subject only,
  50–70 characters, `{type}: {past-tense verb} ...`); otherwise stage it and list it for the developer.
- wow-two-ws's index holds other lanes' staged files: leave wow-two-ws uncommitted and list your paths.
- Update the inventory doc and `context.md` as points close.

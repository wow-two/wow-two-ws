# One version track — context

*Last updated: 2026-09-29*

## State

- Built: version-track.md is the only planning convention (planning files, backlog + `Features` group, Polish
  iterations, task form); polish, rough, vector, engineering-planning and the planning index deleted; handoff rule
  in agentic-workflow.md; index, taxonomy, repo and SDK structure, dev-cycle, versioning-strategy and onboarding
  templates cite it.
- Built: product template (`backlog.md`, `version-track/v0.1/`, `development/rules.md`) and the `create-repo` layout.
- Migrated: 30 repositories, one subagent each with [repo-agent-brief.md](repo-agent-brief.md); outcomes per
  repository in [docs/version-track-consolidation.md](../../../docs/version-track-consolidation.md) § V5.
- Committed after the developer's greenlight: PRISM, Museums Gallery, Secrets Vault, Whiteout, Hijinx and the UI SDK,
  each split into cohesive commits with the migration last (planned read-only first, trees verified).
- Left by the developer's call: TNIS-mintrans and TransportBrain stay staged; fifteen untracked repositories keep no
  first commit yet.
- Left out on purpose: Whiteout's 11 unreferenced source PNGs (7–10 MB) and `crate-material-handoff.md`; Museums'
  edited `handoff.md` and untracked `broad-places-idea.md`.
- For the developer's call: Whiteout's newest folder `v0.9` is a draft of type `Polish`, so CI reads 0.9; Museums
  Gallery, TNIS-mintrans, TransportBrain, home-reno and four first-batch ventures have no version doc, so CI reads
  0.0; ForeverPin runs v0.10 and v0.11 at once by owner decision; Haven v1.1/v1.2 and Sift v0.2 break the odd/even
  rule; Whiteout's zone-builder keeps a `planning/` folder under `engineering/codebase/`.
- Deferred: ocharo-ws repositories, until the developer says the other chat has left (asked 2026-09-29: not yet);
  Wheelhouse migrates itself.
- Procedure: [session-version-track-consolidation.md](session-version-track-consolidation.md).

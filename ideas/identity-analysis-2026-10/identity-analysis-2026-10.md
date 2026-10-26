# Identity analysis — hub tracks

*Last updated: 2026-10-26*

> The part of the Identity analysis batch that stays in the hub: T5, T8 and T9 cover domain repos and release
> automation in general. The Identity-specific batch — index, decision queue, T1–T4, T6, T7, T10 — moved into the
> repo: [identity analysis](https://github.com/wow-two-sdk-beta/wow-two-sdk-beta.identity/blob/main/engineering/research/identity-analysis-2026-10/identity-analysis-2026-10.md).
> The spec is the repo's [product.md](https://github.com/wow-two-sdk-beta/wow-two-sdk-beta.identity/blob/main/product/product.md).

## Tracks

| # | Track | File | State |
|---|---|---|---|
| T5 | SDK split: Identity as the first per-domain repo (be + fe library, service, Docker) | [t5-sdk-breakdown.md](t5-sdk-breakdown.md) | ✅ |
| T8 | Domain library repo template and the rollout checklist | [t8-library-template.md](t8-library-template.md) | ✅ |
| T9 | Release automation: repo creation, NuGet and npm first publish, rollout an agent can run | [t9-release-automation.md](t9-release-automation.md) | ✅ |

- T1–T4, T6, T7 and T10 live in the repo's `engineering/research/identity-analysis-2026-10/`, same file names.

---

## Points

The hub's share of the decision queue; queues A–F and I are in the repo's index.

### G · Library repo and template

- [x] Q35 (developer 2026-10-26: confirmed) template: `wow-two-sdk-beta.domain-template`, a separate repo; `create-repo` gains `SHAPE=domain` → yes (T8)
- [x] Q36 (developer 2026-10-25: confirmed, as a wow2 convention every new library follows) docs: the spec moves to the repo's `product/product.md`, analysis to `engineering/research/`; the hub keeps
  the catalog entry, platform-apps row and cross-capability decisions → yes (T8)
- [x] Q37 (developer 2026-10-26: confirmed with Q1d) packages publish from a repo-local workflow, versions from tags, no release commit; images via shared
  `delivery.yml` → yes (T5, T8)
- [x] Q38 (developer 2026-10-26: confirmed with Q1d) compat job: nightly and on dispatch, against the latest core release → yes (T5, T8)
- [ ] Q39 strip provider and region names from T6 before the docs move into a public repo → yes (T8); done in the 2026-10-26 move, awaiting review

### H · Release automation

- [x] Q40 (developer 2026-10-26: confirmed; unavoidable hand steps stay the developer's, the rest is automated) one entry point: a `create-library` skill over `scripts/release/library.py`, dry run first, resumable; it
  prints every GitHub write for the agent to run as its own guarded command → yes (T9)
- [x] Q41 (developer 2026-10-26: confirmed) guard hole: a `gh` write to a repo not cloned locally reads the hub's push flag (ON) → unmatched targets read
  OFF; `gh repo create` reads the flag of the folder it clones into (P2) (T9)
- [x] Q42 (developer 2026-10-26: confirmed; the agent edits the guard) one flag directive per folder, `workbench/wow-two-sdk-beta/*`, covering repos created later (P1) (T9)
- [x] Q43 (developer 2026-10-26: confirmed) clone counts as safe; a push must name a configured remote, never a URL (P3) (T9)
- [ ] Q44 [parked 2026-10-26, low priority → `system/planning/pln-tasks.md` § Backlog] uninstall the Codex GitHub App: write access on 3 orgs, Codex dropped 2026-10-23 → developer, once (T9)
- [ ] Q45 consumer re-pins: an agent sweep (`repin.py`), since no wow2 org has Renovate installed → sweep (T9)

### Self-served

- ⬜ release residue: npm ≥ 11.15.0 for `npm trust` (local 11.6.1); stale `NUGET_API_KEY` and `NPM_TOKEN` repo secrets in the sdks (T9)
- ✅ `catalog.yml` carries the Identity entry (rollout step 11, [T8 § 6](t8-library-template.md#6--rollout-checklist))

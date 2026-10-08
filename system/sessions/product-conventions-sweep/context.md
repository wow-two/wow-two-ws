# Product conventions sweep

*Last updated: 2026-10-01*

## Scope

- Developer order, 2026-10-01: analyse the product conventions, fix and improve them, add the missing ones, then
  sweep the products and write a gap handoff for each.
- Conventions root: `conventions/`. The audit list:
  [product conformance](../../../conventions/development/repo/structure/product-conformance.md).
- Points, applied defaults, open decisions and the product matrix: [analysis](analysis.md).

---

## State

- Phase 1, conventions: first pass complete on 2026-10-01 — 17 fixes, 7 additions, 12 applied defaults.
- Phase 1 is uncommitted. The tree holds another lane's staged `.claude/launch.json` and
  `conventions/deployment/hosting/ports.md`, so the commit waits for the developer's answer to the lane check.
- Phase 2, products: `ventures.tnis` audited and fixed in place on 2026-10-01, uncommitted — evidence in its
  `engineering/architecture/research/project-audit.md` § *Conformance*, open rows in its backlog's *Shell & design*
  and *Repo & delivery* groups. Every other product: not started; the matrix is the starting evidence.

---

## Resume

1. Settle the open points in [analysis](analysis.md) § *Open* with the developer, one batch per reply.
2. Commit phase 1 once the lane question is answered — `conventions/`, `CLAUDE.md` and this session folder only.
3. Start phase 2 with the product template and the `create-repo` skill, then the platform apps, then ventures.
4. Audit each repo against the conformance list; a matrix cell is a lead, not a verdict.

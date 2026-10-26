# Breaking changes

*Last updated: 2026-10-26*

> When an infrastructure change may break the SDKs, domain repos, products, their data or their deployments.
> Use case — a redesign that improves structure, governance or safety and breaks its consumers on the way.

## Rule

- may make any infrastructure change in the SDKs, domain repos and products, breaking ones included, when it
  improves something for us.
- must name the improvement in the change's analysis or decision; a break with no gain stays out.
- must build the target design, never a workaround that only avoids the break.
- must not keep a compatibility shim, a dual path or a data-preserving migration only for users who do not exist.

---

## Scope

- applies to every product with no external users — all of them on 2026-10-26.
- must give a product with external users a data migration and a cut-over for each breaking change; its consumers
  in the SDKs stay free to break.
- must record a product's first external users in its `catalog.yml` status, so this scope can be read off the hub.

---

## Data

- may convert, reset or drop a product's data when the new design needs it.
- may move a product to a new schema, database or service without a zero-copy path.
- must copy data only when the copy is cheaper than recreating it.

---

## Process

- must update every named consumer in the same pass ([dev-cycle](dev-cycle.md) § Cycle 2).
- must state the break in the commit subject of the repository that breaks.
- must keep the lane rules of [agentic workflow](../agentic-workflow/agentic-workflow.md) while consumers move.

---

## Precedent

- Identity, 2026-10-26: products move to Identity's one schema and a database per instance; their own identity
  tables (Desk, Haven, ForeverPin, the pilots' SQLite) are converted or reset, with no takeover path.

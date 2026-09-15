*Last updated: 2026-08-24*

# Tasks

> Single source of truth for active `wow-two` work. Scored + pulled by [`session-planning.md`](../sessions/planning/session-planning.md) (`pln-w2`).
> **Grain: abstract.** A row states a capability — *finish codes functionality for forever-pin* — never its sub-steps. The breakdown lives in that repo's `engineering/planning/`.
> Calendar slots are not tracked here.

**Columns:** `Task ID` = `{cat}-t-{NNN}` · `Priority` = `high` 0.5 / normal 1.0 / `low` 2.0 · `Status` = `todo` / `wip` / `blocked` / `done` · `Repo` = owning repo, or `-` for workspace-level

Categories: `sdk` · `plt` · `app` · `ven` · `con` · `ws`

---

## Ventures

| Task ID | Task | Deadline | Priority | Status | Repo | Notes |
|---|---|---|---|---|---|---|
| `ven-t-001` | Record the ministry outcome + agreed next steps | `-` | `high` | `todo` | `ventures.tnis` | Presentation `2026-08-12`, 1:45–4 PM. Written nowhere yet. Home: `product/context.md` |
| `ven-t-002` | Advance `TNIS` per `follow-up-roadmap.md` | `-` | `high` | `wip` | `ventures.tnis` | ~6h15m `08-12`, brainstorms `08-13`. Roadmap holds the breakdown |
| `ven-t-003` | Name the active Micro-SaaS candidate | `-` | normal | `todo` | `-` | One block `08-12`. `10x-ws` tracks a matching task to give Micro SaaS a section there |
| `ven-t-004` | Finish the Mintrans demo solution and share it | `2026-08-23` | `high` | `todo` | `ventures.tnis-mintrans` | Added `2026-08-17`. The deliverable sent to Mintrans — distinct from the venture (`ventures.tnis`) and from the hackathon demo, which lives in Yandex org. Gates `ven-t-005` |
| `ven-t-005` | Complete the Mintrans integration | `2026-09-06` | `high` | `todo` | `ventures.tnis-mintrans` | Added `2026-08-17`. Breakdown belongs in the repo’s `engineering/planning/`, not here |
| `ven-t-006` | Advance forever-pin per its `engineering/planning/` | `-` | `high` | `wip` | `forever-pin` | Added `2026-08-17`. 10h across `08-15`–`08-16`, the heaviest venture thread this month |
| `ven-t-007` | Complete the ForeverPin rebrand | `-` | normal | `done` | `forever-pin` | Local source, projects, docs, product/promo folders renamed 2026-09-13. Full suites pass. GitHub rename and both remote URLs verified. Corrected hero still/video exported under native approval. Product rebrand, verification tooling, and docs committed. |

---

## Conventions

| Task ID | Task | Deadline | Priority | Status | Repo | Notes |
|---|---|---|---|---|---|---|
| `con-t-001` | Close the presentation-layer convention | `-` | `high` | `wip` | `-` | Current owners: backend `core/mla/domains/api/` and `shapes/service/platform/responses/`; closure in audit `BC04` and `BC07` |
| `con-t-002` | Land the Dto-vs-`Response` naming cleanup | `-` | normal | `todo` | `-` | Convention states it; renaming is per-app work |
| `con-t-003` | Complete the backend convention sweep before the SDK release | `-` | `high` | `wip` | `wow-two-ws` | Mechanical repairs complete; 19/25 grouped convention tasks closed. [Audit and remaining decisions](../sessions/backend-beta-build/conventions-audit.md); [repair evidence](../sessions/backend-beta-build/conventions-resolution.md). SDK consequences added as C14–C25; settle decisions before SDK implementation/release |

---

## Workspace

| Task ID | Task | Deadline | Priority | Status | Repo | Notes |
|---|---|---|---|---|---|---|
| — | — | — | — | — | — | — |

---

## Backlog

Not started, ordered, top = next. Pulling one promotes it above and mints its ID.

### → beta SDK (`wow-two-sdk.backend.beta`)

| Item | Type | Notes |
|---|---|---|
| `IClock` + `DateTimeOffset` clock → `Foundation.Time` | feature | adopting = a pure delete in products |
| `FailureCategory` union (`+402` / `+503`) → canonical enum | feature | bake at extract time |
| `ApiResponse<T>` envelope → `Web.Contracts` | feature | products drop the inline copy |
| Remaining v0.2 extract items | feature | 13-item list, detail in drydock's backlog |
| `ToCommand` / `ApiRequest` support | idea | evaluate once apps adopt the convention |

### Conventions

| Item | Type | Notes |
|---|---|---|
| Reconcile controller and message examples | issue | Backend audit `BC07` and `BC13`; current construct owner is `controller.md`, not the removed `controllers.md` |
| Apply the current convention authoring rules | check | Backend audit `BC20`; directive rules and single ownership per `conventions/conventions.md` |

---

## Detail pointers

Not tasks — where a promoted capability gets broken down.

| Source | Holds |
|---|---|
| `workbench/{org}/{repo}/engineering/planning/` | that repo's roadmap, backlog, versions |
| `workbench/ventures/ventures.tnis/follow-up-roadmap.md` | `TNIS` venture breakdown |
| `workbench/ventures/ventures.tnis-mintrans/` | the Mintrans deliverable — demo + integration |
| `workbench/wow-two/wow-two.refinement` | live ecosystem state + roadmap |

---

## Done

Completions land here, ID preserved so day-log references keep resolving. Pruned once a version doc or git carries them.

| Task ID | Task | Outcome |
|---|---|---|
| `ven-t-008` | Send the Mintrans project requirements | ✅ `2026-08-19` — prepared 9:00 AM + 3:00 PM, sent 3:30 PM. Precedes `ven-t-004` |

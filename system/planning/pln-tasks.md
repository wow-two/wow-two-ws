*Last updated: 2026-10-05*

# Tasks

> Single source of truth for active `wow-two` work. Scored + pulled by [`session-planning.md`](../sessions/planning/session-planning.md) (`pln-w2`).
> **Grain: abstract.** A row states a capability — *finish codes functionality for forever-pin* — never its sub-steps. The breakdown lives in that repo's `engineering/planning/`.
> Calendar slots are not tracked here.

**Columns:** `Task ID` = `{cat}-t-{NNN}` · `Priority` = `high` 0.5 / normal 1.0 / `low` 2.0 · `Status` = `todo` / `wip` / `blocked` / `done` · `Repo` = owning repo, or `-` for workspace-level

Categories: `sdk` · `plt` · `app` · `ven` · `con` · `ws`

---

## Venture product order

**Current: ForeverPin. Following product: Pose Coach.** User-confirmed on `2026-10-05`.

| Position | Product | Task | Outcome |
|---|---|---|---|
| 1 — current | [ForeverPin](../../workbench/ventures/10x-venture-forever-pin/) | `ven-t-006` | Complete a reliable release and verify the paid subscription path |
| 2 — queued | [Pose Coach](../../workbench/ventures/ventures.pose-coach/) | `ven-t-009` | Validate the photo-director experience and deliver a paid release |
| 3 — queued | [Transcript Forge](../../workbench/ventures/10x-ventures-transcript-forge/) | `ven-t-010` | Deliver a paid transcript workflow for repeat users |
| 4 — queued | [Hijinx](../../workbench/ventures/ventures.hijinx/) | `ven-t-011` | Validate repeat host use and deliver a paid release |

This is the execution order for venture product work, including consumer and entertainment products, ordered to reach subscription revenue (MRR) sooner. The [subscription-speed assessment](../../ideas/saas-research-2026-10/subscription-speed.md) holds each product's remaining path and what blocks charging. Continue the current product until its release outcome is complete or the user explicitly parks it; the next queued product becomes current. Each repository's `engineering/planning/` owns its implementation breakdown and release evidence. Dates are unassigned.

The [100-product research](../../ideas/saas-research-2026-10/decision-report.md) remains an options catalog; its research ranking does not replace this order. Existing platform-app and SDK work remains in its own track, with concrete dependencies resolved when they block the current product.

---

## Apps

| Task ID | Task | Deadline | Priority | Status | Repo | Notes |
|---|---|---|---|---|---|---|
| `app-t-001` | Finish wheelhouse for a reliable release | `-` | `high` | `todo` | `wow-two-platform.wheelhouse` | Added `2026-09-29`: first release target, with `app-t-002` and `ven-t-006`, ahead of TNIS. Breakdown in the repo's `engineering/planning/` |
| `app-t-002` | Finish secrets-vault for a reliable release | `-` | `high` | `todo` | `wow-two-platform.secrets-vault` | Added `2026-09-29`: same release push as `app-t-001` and `ven-t-006` |

---

## Ventures

| Task ID | Task | Deadline | Priority | Status | Repo | Notes |
|---|---|---|---|---|---|---|
| `ven-t-001` | Record the ministry outcome + agreed next steps | `-` | `high` | `todo` | `ventures.tnis` | Presentation `2026-08-12`, 1:45–4 PM. Written nowhere yet. Home: `product/context.md` |
| `ven-t-002` | Advance `TNIS` per its follow-up backlog | `-` | `high` | `todo` | `ventures.tnis` | Deferred `2026-09-29` until wheelhouse, secrets-vault and forever-pin reach a reliable release — maybe the mid-October vacation. ~6h15m `08-12`, brainstorms `08-13`. Roadmap holds the breakdown |
| `ven-t-003` | Choose the active venture sequence | `-` | normal | `done` | `-` | Resolved `2026-10-05`: user chose the [venture product order](#venture-product-order). The fresh SaaS catalog remains research, not an additional build queue |
| `ven-t-004` | Finish the Mintrans demo solution and share it | `-` | `high` | `todo` | `ventures.tnis-mintrans` | Deadline removed `2026-09-29`: the hackathon was paid, so finishing is the user's call; deferred with `ven-t-002`. Added `2026-08-17`. The deliverable sent to Mintrans — distinct from the venture (`ventures.tnis`) and from the hackathon demo, which lives in Yandex org. Gates `ven-t-005` |
| `ven-t-005` | Complete the Mintrans integration | `-` | `high` | `todo` | `ventures.tnis-mintrans` | Deadline removed `2026-09-29`: the hackathon was paid, so finishing is the user's call; deferred with `ven-t-002`. Added `2026-08-17`. Breakdown belongs in the repo’s `engineering/planning/`, not here |
| `ven-t-006` | Finish forever-pin for a reliable release | `-` | `high` | `wip` | `forever-pin` | Current product in the [venture product order](#venture-product-order), confirmed `2026-10-05`; includes verifying its paid subscription path. Breakdown in its `engineering/planning/`. Platform release work remains under `app-t-001` and `app-t-002` |
| `ven-t-007` | Complete the ForeverPin rebrand | `-` | normal | `done` | `forever-pin` | Local source, projects, docs, product/promo folders renamed 2026-09-13. Full suites pass. GitHub rename and both remote URLs verified. Corrected hero still/video exported under native approval. Product rebrand, verification tooling, and docs committed. |
| `ven-t-009` | Deliver a paid Pose Coach release | `-` | `high` | `todo` | `ventures.pose-coach` | Queued by the user `2026-10-05`; position follows the [venture product order](#venture-product-order). Real-device validation and implementation belong in its `engineering/planning/` |
| `ven-t-010` | Deliver a paid Transcript Forge release | `-` | normal | `todo` | `10x-ventures-transcript-forge` | Queued by the user `2026-10-05`; position follows the [venture product order](#venture-product-order). Repeat-use scope and implementation belong in its `engineering/planning/` |
| `ven-t-011` | Deliver a paid Hijinx release | `-` | normal | `todo` | `ventures.hijinx` | Queued by the user `2026-10-05`; position follows the [venture product order](#venture-product-order). Repeat-host validation and implementation belong in its `engineering/planning/` |

---

## Conventions

| Task ID | Task | Deadline | Priority | Status | Repo | Notes |
|---|---|---|---|---|---|---|
| `con-t-001` | Close the presentation-layer convention | `-` | `high` | `wip` | `-` | Current owners: backend `core/mla/domains/api/` and `shapes/service/platform/responses/`; closure in audit `BC04` and `BC07` |
| `con-t-002` | Land the Dto-vs-`Response` naming cleanup | `-` | normal | `todo` | `-` | Convention states it; renaming is per-app work |
| `con-t-003` | Complete the backend convention sweep before the SDK release | `-` | `high` | `done` | `wow-two-ws` | Completed 2026-09-15: 25/25 convention tasks closed, all naming decisions settled. [Final acceptance](../sessions/backend-beta-build/naming-final-acceptance.md): 159 docs, 1,050 local links/fragments pass. SDK implementation and release remain in their own sweep. |
| `con-t-004` | Refactor remaining product controllers to block bodies | `-` | normal | `todo` | `wow-two-ws` | Non-Ocharo products; preserve routes, response contracts and delegates. Rule: [controller member content](../../conventions/development/backend/dotnet/core/mla/constructs/behavior/controller.md#member-content). |
| `con-t-005` | Adopt complete HTTP ProblemDetails contracts across remaining products | `-` | `high` | `todo` | `wow-two-ws` | Non-Ocharo APIs and development proxies; adopt shared SDK pipeline, cover endpoint/framework/middleware errors and preserve headers. Rule: [wire contract](../../conventions/development/backend/dotnet/shapes/service/platform/responses/problem-details.md#wire-contract). |
| `con-t-006` | Align remaining product request feedback and first paint | `-` | normal | `todo` | `wow-two-ws` | Non-Ocharo frontends; safe deduplicated toasts, neutral retry states, settled skeletons, retained last good content, matching early theme backgrounds. Rules: [state and data](../../conventions/development/frontend/core/mla/domains/data/state-and-data.md#error-adaptation), [first paint](../../conventions/development/frontend/shapes/app/platform/document.md#first-paint). |
| `con-t-007` | Adopt confirmed mutation and independent read lifecycles across remaining products | `-` | `high` | `todo` | `wow-two-ws` | Non-Ocharo frontend/backend products; pending controls before acknowledgement, durable backend completion, separate projection refresh after success, no optimistic persisted updates. Migrate success contracts with consumers. Rules: [commands and reads](../../conventions/development/backend/dotnet/core/mla/domains/api/api.md#commands-and-reads), [mutations](../../conventions/development/frontend/core/mla/domains/data/state-and-data.md#mutations). |
| `con-t-009` | Group remaining product host configuration by capability | `-` | normal | `todo` | `wow-two-ws` | Non-Ocharo APIs and workers; host-owned capability registrations, shared resources, explicit assembly anchors and awaited initialization. Preserve lifetimes, configuration precedence and middleware order. Rule: [domain registration](../../conventions/development/backend/dotnet/shapes/service/platform/startup/host-configuration.md#domain-registration). |

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
| Remaining v0.2 extract items | feature | 13-item list, detail in wheelhouse's backlog |
| `ToCommand` / `ApiRequest` support | idea | evaluate once apps adopt the convention |

### Conventions

| Item | Type | Notes |
|---|---|---|
| Reconcile controller and message examples | issue | Backend audit `BC07` and `BC13`; current construct owner is `controller.md`, not the removed `controllers.md` |
| Apply the current convention authoring rules | check | Backend audit `BC20`; directive rules and single ownership per `conventions/conventions.md` |
| Align result, validation and ProblemDetails conventions with `AppError` | check | From the backend SDK's errors research §6; verify what already landed |
| Settle explicit `IQuery` / `ICommand` markers in `mediator.md` | check | From the backend SDK's mediator research, decision 2; verify first |
| Resolve `Provides mapping for` vs `Extends` in XML-doc summaries | issue | TNIS: `request-models.md:82` against `documentation/summary.md:83` |
| Name grouped controls and input suffixes; prefer gaps and separators to borders | feature | ForeverPin polish findings (`ShapeControls` vs `ShapeControlsGroup`) |
| Document the derived component-catalog pattern in `sdk-structure.md` | feature | UI SDK v0.1 iteration 3 |
| Move shipped facts from the UI SDK vector analyses into conventions | check | UI SDK content audit |

### → product template (`wow-two-sdk-beta.product-template`)

| Item | Type | Notes |
|---|---|---|
| Stop `vue/html-self-closing` fighting Prettier on void elements | issue | PbnStudio; `eslint.config.mjs` lacks the override |
| Serve `vite preview` over http without the mkcert `server.https` | issue | Hijinx: http previews and E2E get empty responses |
| Stamp `src/form.ts` into new repos | feature | UI SDK forms row, deferred |

### → SDK repos (`wow-two-sdk.backend.beta` · `wow-two-sdk-beta.ui`)

| Item | Type | Notes |
|---|---|---|
| Rename the SDK repos: `wow-two-sdk.backend.beta` → `wow-two-sdk.be.beta`, `wow-two-sdk-beta.ui` → `wow-two-sdk.fe.beta` | chore | Added `2026-09-29`, not a priority. Spans the GitHub renames, local folders + remotes, `package.json` `repository`/`homepage`, the Pages URL, registry, `CLAUDE.md` files, conventions, launch configs. Package ids stay. Open: the registry wants repo prefix = org name (`wow-two-sdk-beta`) |

---

## Detail pointers

Not tasks — where a promoted capability gets broken down.

| Source | Holds |
|---|---|
| `workbench/{org}/{repo}/engineering/planning/` | that repo's backlog and version track (`conventions/planning/version-track/version-track.md`) |
| `workbench/ventures/ventures.tnis-mintrans/engineering/planning/backlog.md` | `TNIS` follow-up breakdown (the former follow-up roadmap) |
| `workbench/ventures/ventures.tnis-mintrans/` | the Mintrans deliverable — demo + integration |
| `workbench/wow-two/wow-two.refinement` | live ecosystem state + roadmap |

---

## Done

Completions land here, ID preserved so day-log references keep resolving. Pruned once a version doc or git carries them.

| Task ID | Task | Outcome |
|---|---|---|
| `ven-t-008` | Send the Mintrans project requirements | ✅ `2026-08-19` — prepared 9:00 AM + 3:00 PM, sent 3:30 PM. Precedes `ven-t-004` |

*Last updated: 2026-10-23*

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
| 1 — current | [ForeverPin](../../workbench/maxs-projects/ventures/saas/10x-venture-forever-pin/) | `ven-t-006` | Complete a reliable release and verify the paid subscription path |
| 2 — local changes ready for review | [Pose Coach](../../workbench/maxs-projects/ventures/consumer/ventures.pose-coach/) | `ven-t-009` | Validate the photo-director experience and deliver a paid release |
| 3 — local changes ready for review | [Transcript Forge](../../workbench/maxs-projects/ventures/saas/10x-ventures-transcript-forge/) | `ven-t-010` | Deliver a paid transcript workflow for repeat users |
| 4 — local changes ready for review | [Hijinx](../../workbench/maxs-projects/ventures/consumer/ventures.hijinx/) | `ven-t-011` | Validate repeat host use and deliver a paid release |
| 5 — selected, definition pending | Kids Curiosity | `ven-t-013` | Deliver a guided question-to-discovery experience with repeat family use and a tested paid boundary |

This is the execution order for venture product work, including consumer and entertainment products, ordered to reach subscription revenue (MRR) sooner. The [subscription-speed assessment](../../ideas/saas-research-2026-10/subscription-speed.md) holds each product's remaining path and what blocks charging. Continue the current product until its release outcome is complete or the user explicitly parks it; the next queued product becomes current. Each repository's `engineering/planning/` owns its implementation breakdown and release evidence. Explicit user targets are recorded in the task deadlines below.

**Parallel release work, authorized `2026-10-09`:** ForeverPin and Pose Coach remain in their existing chats.
The next two products are Transcript Forge and Hijinx; this lane prioritizes Hijinx's web/mobile reliability,
game rules and UI, alongside Transcript Forge's workflow reliability. The user targets `2026-10-31`.
Hijinx's first realtime mode is confirmed: one same-room host screen with player phones. The room service
and client are implemented; all 48 multi-device browser scenarios passed. Installed offline
acceptance passed on iOS and Android.
This target is not a paid-launch guarantee: realtime acceptance, payment acceptance, native distribution and
repeat-user validation remain explicit release gates. Repository backlogs and active version tracks own the work.
Both products share browser scenarios across phone, tablet and desktop layouts; `pnpm verify:release` repeats
their local quality checks. [Hijinx verification](../../workbench/maxs-projects/ventures/consumer/ventures.hijinx/engineering/research/release-readiness-2026-10.md#verification)
and [Transcript Forge verification](../../workbench/maxs-projects/ventures/saas/10x-ventures-transcript-forge/engineering/research/release-readiness-2026-10.md#verification)
separate automated coverage from remaining device, provider and release acceptance.

The [October 5 B2B research](../../ideas/saas-research-2026-10/decision-report.md) remains an options catalog; its research ranking does not replace this order. On `2026-10-09`, the user selected Kids Curiosity. The [rebuilt self-serve 100-candidate assessment](../../ideas/self-serve-research-2026-10/self-serve-research-2026-10.md) confirms that the previous catalog's multi-role business-workflow requirement excluded the preferred product shape. Kids Curiosity is the next selected additional product. Existing platform-app and SDK work remains in its own track, with concrete dependencies resolved when they block the current product.

**Additional-product research priorities, `2026-10-09`:** these prepare options beyond the four active releases; Kids Curiosity remains selected. On `2026-10-10`, the user accepted Fiction Scene and Continuity for later work and selected Surface Pattern for immediate venture analysis and implementation. The other entries remain research recommendations. All proposed prices and recurring demand remain unvalidated.

| Research priority | Product | Decision to prove |
|---|---|---|
| 1 — user-selected | Kids Curiosity (`E001`) | Families independently complete and revisit reviewed investigations, with a useful paid continuation |
| 2 — recommended | Formula Drill Gym (`E002`) | Error-based practice earns paid returns rather than only a finite course purchase |
| 3 — accepted, deferred | Fiction Scene and Continuity Studio (`E040`) | Writers repeatedly resume real scenes more effectively than in existing tools |
| 4 — selected, implementation active | Surface-Pattern Studio (`E031`) | Regular makers prefer and pay for repeated collection production over existing tools |
| 5 — recommended | Hifz Revision Companion (`E003`) | Trusted self-assessed revision remains useful through missed days and earns payment |

**Surface Pattern implementation, authorized `2026-10-10`:** `ven-t-014` owns the new [venture](../../workbench/maxs-projects/ventures/saas/ventures.surface-pattern/). Its first increment is a guided repeat studio, physical-scale surface previews, browser collections and SVG/PNG exports. This is additional local implementation; existing release chats retain their ownership. Paid demand, personal-artwork workflow and physical print acceptance remain unverified.

The [five-product analysis](../../ideas/self-serve-research-2026-10/self-serve-research-2026-10.md#five-research-priorities) records competitors, content/compute burdens and stop rules. Guided Drawing is the nearest reserve; Arcade's current cosmetic transactions, finite courses and packs contribute no assumed subscription MRR.

**Haven** joins after venture revenue reaches a stable $2K MRR; it takes no queue position before then (user, `2026-10-08`).

**Before ForeverPin (user, `2026-10-15`):** a few Wheelhouse iterations first (logic review, UI layout, mobile responsiveness), then the Ocharo projects, then ForeverPin resumes its place in this order.

**Parallel preparation, authorized `2026-10-06`:** ForeverPin is handled in a separate chat. The initial implementation sweep and expanded feature increment are complete for local review: Pose Coach live framing/voice and 15 languages; Transcript Forge persistent queue controls; Hijinx 15-language UI, translated starter content and reusable host playlists. [Outcomes, checks and running review targets](../sessions/saas-research-2026-10/implementation-review.md). Their release priority stays as listed; physical-device, native editorial, provider and paid-release acceptance remain open. This preparation does not establish paid launch or release completion.

---

## Apps

| Task ID | Task | Deadline | Priority | Status | Repo | Notes |
|---|---|---|---|---|---|---|
| `app-t-001` | Finish wheelhouse for a reliable release | `-` | `high` | `todo` | `wow-two-platform.wheelhouse` | Added `2026-09-29`: first release target, with `app-t-002` and `ven-t-006`, ahead of TNIS. Breakdown in the repo's `engineering/planning/` |
| `app-t-002` | Finish secrets-vault for a reliable release | `-` | `high` | `todo` | `wow-two-platform.secrets-vault` | Added `2026-09-29`: same release push as `app-t-001` and `ven-t-006` |
| `app-t-003` | Set up a reliable off-provider backup flow for the platform VPS | `-` | `high` | `todo` | `wow-two-platform.wheelhouse` | Added `2026-10-14` by the user: encrypted backups of both Wheelhouse databases, cookie keys, runner state and host config, with a tested restore; OVH's daily backup is the only copy today. Multi-cloud replication is on the table. Breakdown in the Wheelhouse backlog § Hosting |
| `app-t-004` | Buy a second VPS for Ocharo (Contabo or OVH) | `-` | `high` | `todo` | `-` | Added `2026-10-17` by the user: Ocharo is the first product to deploy and gets its own host. The purchase is the user's; Wheelhouse registers it as a server. Deploying waits for `app-t-005` |
| `app-t-005` | Build Wheelhouse's essential modules before the first Ocharo deploy | `-` | `high` | `todo` | `wow-two-platform.wheelhouse` | Added `2026-10-17` by the user: logs and the other important modules land before Ocharo goes live. Module list and breakdown in the Wheelhouse backlog |
| `app-t-006` | Build Almanac, the calendar view app, to its v1 ship gate | `2026-11-15` | `-` | `todo` | `wow-two-apps.almanac` | Added `2026-10-23` by the user: a readable read-only calendar for the built-in browser pane, run in Docker locally, deployed through Wheelhouse later. Google Calendar stays in use until then. Adds the calendar vector to the fe sdk. [Spec](../../ideas/calendar-spec.md) |

---

## Ventures

| Task ID | Task | Deadline | Priority | Status | Repo | Notes |
|---|---|---|---|---|---|---|
| `ven-t-001` | Record the ministry outcome + agreed next steps | `-` | `high` | `todo` | `ventures.tnis` | Presentation `2026-08-12`, 1:45–4 PM. Written nowhere yet. Home: `product/context.md` |
| `ven-t-002` | Advance `TNIS` per its follow-up backlog | `-` | `high` | `todo` | `ventures.tnis` | Deferred `2026-09-29` until wheelhouse, secrets-vault and forever-pin reach a reliable release — maybe the mid-October vacation. ~6h15m `08-12`, brainstorms `08-13`. Roadmap holds the breakdown |
| `ven-t-003` | Choose the active venture sequence | `-` | normal | `done` | `-` | Resolved `2026-10-05`: user chose the [venture product order](#venture-product-order). The fresh SaaS catalog remains research, not an additional build queue |
| `ven-t-004` | Finish the Mintrans demo solution and share it | `-` | `high` | `todo` | `ventures.tnis-mintrans` | Deadline removed `2026-09-29`: the hackathon was paid, so finishing is the user's call; deferred with `ven-t-002`. Added `2026-08-17`. The deliverable sent to Mintrans — distinct from the venture (`ventures.tnis`) and from the hackathon demo, which lives in Yandex org. Gates `ven-t-005` |
| `ven-t-005` | Complete the Mintrans integration | `-` | `high` | `todo` | `ventures.tnis-mintrans` | Deadline removed `2026-09-29`: the hackathon was paid, so finishing is the user's call; deferred with `ven-t-002`. Added `2026-08-17`. Breakdown belongs in the repo’s `engineering/planning/`, not here |
| `ven-t-006` | Finish forever-pin for a reliable release | `-` | `high` | `wip` | `forever-pin` | Current product in the [venture product order](#venture-product-order), confirmed `2026-10-05`; includes verifying its paid subscription path. Breakdown in its `engineering/planning/`. Platform release work remains under `app-t-001` and `app-t-002`. Live Stripe billing depends on `ven-t-012` |
| `ven-t-007` | Complete the ForeverPin rebrand | `-` | normal | `done` | `forever-pin` | Local source, projects, docs, product/promo folders renamed 2026-09-13. Full suites pass. GitHub rename and both remote URLs verified. Corrected hero still/video exported under native approval. Product rebrand, verification tooling, and docs committed. |
| `ven-t-009` | Deliver a paid Pose Coach release | `-` | `high` | `wip` | `ventures.pose-coach` | Live framing/voice and 15-language increment locally implemented `2026-10-06`; physical camera/speech and paid-release acceptance remain open. The [venture product order](#venture-product-order) retains release priority; details belong in its `engineering/planning/` |
| `ven-t-010` | Deliver a paid Transcript Forge release | `2026-10-31` | `high` | `wip` | `10x-ventures-transcript-forge` | User target `2026-10-09`; draft/retry and provider-cost reliability fixes passed local verification. Reliable local Release 1 and provider acceptance precede hosted billing. Details belong in its `engineering/planning/` |
| `ven-t-011` | Deliver a paid Hijinx release | `2026-10-31` | `high` | `wip` | `ventures.hijinx` | User target `2026-10-09`; offline browser and installed iOS/Android game checks passed. Selected same-room host/player mode is implemented with all 48 multi-device browser scenarios passing; physical-device/editorial acceptance and paid-release gates remain open. Details belong in its `engineering/planning/` |
| `ven-t-012` | Set up the parent company for Stripe and app-store sales | `-` | `high` | `todo` | `-` | Added `2026-10-08`: Stripe does not onboard Uzbekistan sellers, so ForeverPin's live billing needs a Stripe-supported entity; the user wants one parent company to serve every later product. [Structure analysis](../../ideas/parent-company-2026-10/parent-company-2026-10.md). Gates live billing under `ven-t-006` |
| `ven-t-013` | Define and deliver Kids Curiosity as a self-serve learning product | `-` | `high` | `todo` | `-` | Selected by the user `2026-10-09`; predict → explore a reviewed investigation → explain. Start one coherent question cluster; qualified content review, family repeat use and a tested paid boundary precede release. No repository or implementation is created by the research task. [Selection and gates](../../ideas/self-serve-research-2026-10/self-serve-research-2026-10.md#kids-curiosity-selected-with-an-editorial-gate) |

| `ven-t-014` | Build and validate Surface Pattern as a maker venture | `-` | `high` | `wip` | `ventures.surface-pattern` | Selected `2026-10-10`; WOW2 Vue/.NET studio with deterministic repeats, surface previews and print exports. Local implementation and verification in [v0.1](../../workbench/maxs-projects/ventures/saas/ventures.surface-pattern/engineering/planning/version-track/v0.1/v0.1.md); recurring demand and physical print acceptance remain open. |

---

## Conventions

| Task ID | Task | Deadline | Priority | Status | Repo | Notes |
|---|---|---|---|---|---|---|
| `con-t-001` | Close the presentation-layer convention | `-` | `high` | `wip` | `-` | Current owners: backend `core/mla/domains/api/` and `shapes/service/platform/responses/`; closure in audit `BC04` and `BC07` |
| `con-t-002` | Land the Dto-vs-`Response` naming cleanup | `-` | normal | `todo` | `-` | Convention states it; renaming is per-app work |
| `con-t-003` | Complete the backend convention sweep before the SDK release | `-` | `high` | `done` | `wow-two-ws` | Completed 2026-09-15: 25/25 convention tasks closed, all naming decisions settled. [Final acceptance](../sessions/backend-beta-build/naming-final-acceptance.md): 159 docs, 1,050 local links/fragments pass. SDK implementation and release remain in their own sweep. |
| `con-t-004` | Refactor remaining product controllers to block bodies | `-` | normal | `todo` | `wow-two-ws` | Non-Ocharo products; preserve routes, response contracts and delegates. Rule: [controller member content](../../conventions/development/backend/dotnet/core/mla/constructs/behavior/controller.md#member-content). |
| `con-t-005` | Adopt complete HTTP ProblemDetails contracts across remaining products | `-` | `high` | `todo` | `wow-two-ws` | Non-Ocharo APIs and development proxies; adopt shared SDK pipeline, cover endpoint/framework/middleware errors and preserve headers. Rule: [wire contract](../../conventions/development/backend/dotnet/shapes/service/platform/responses/problem-details.md#wire-contract). |
| `con-t-006` | Align remaining product request feedback and first paint | `-` | normal | `todo` | `wow-two-ws` | Non-Ocharo frontends; safe deduplicated toasts, plain centered empty labels, persistent toolbar refresh, matched stable skeletons, retained last good content, matching early theme backgrounds. Rules: [state and data](../../conventions/development/frontend/core/mla/domains/data/state-and-data.md#error-adaptation), [first paint](../../conventions/development/frontend/shapes/app/platform/document.md#first-paint). |
| `con-t-007` | Adopt confirmed mutation and independent read lifecycles across remaining products | `-` | `high` | `todo` | `wow-two-ws` | Non-Ocharo frontend/backend products; pending controls before acknowledgement, durable backend completion, separate projection refresh after success, no optimistic persisted updates. Migrate success contracts with consumers. Rules: [commands and reads](../../conventions/development/backend/dotnet/core/mla/domains/api/api.md#commands-and-reads), [mutations](../../conventions/development/frontend/core/mla/domains/data/state-and-data.md#mutations). |
| `con-t-008` | Adopt shared notification lifecycles across remaining products | `-` | normal | `todo` | `wow-two-ws` | Non-Ocharo frontends; top-right severity toasts, explicit retained history, close/delete distinction and typed actions. Rules: [toast viewport](../../conventions/development/frontend/core/mla/components/feedback/toastHost.md#values), [notification center](../../conventions/development/frontend/core/mla/components/feedback/notificationCenterGroup.md#values). |
| `con-t-009` | Group remaining product host configuration by capability | `-` | normal | `todo` | `wow-two-ws` | Non-Ocharo APIs and workers; host-owned capability registrations, shared resources, explicit assembly anchors and awaited initialization. Preserve lifetimes, configuration precedence and middleware order. Rule: [domain registration](../../conventions/development/backend/dotnet/shapes/service/platform/startup/host-configuration.md#domain-registration). |
| `con-t-010` | Settle repository license conventions | `-` | normal | `todo` | `wow-two-ws` | Added `2026-10-14` by the user: analyze license options, choose our templates and write the exact conditions for picking one when a repo is created |
| `con-t-011` | Require an app icon, version tag and environment tag in every app | `-` | normal | `todo` | `wow-two-ws` | Added `2026-10-14`: the design is proved in Wheelhouse first (a separate env pill beside the version; try a vertical stack on desktop), then fixed as a convention |
| `con-t-012` | Write the zero-disruption deployment contract every app adopts | `-` | `high` | `todo` | `wow-two-ws` | Added `2026-10-15` by the user: request drain and maintenance pages, a busy signal for idle-aware and scheduled deploys, frontend refresh onto a new version before writes, migration dry runs. Wheelhouse and the canary prove it; then the SDK halves and the convention |
| `con-t-013` | Write responsive design and mobile interaction conventions | `-` | normal | `wip` | `wow-two-ws` | Added `2026-10-15` by the user. Draft `2026-10-16`: settled rules in [responsive](../../conventions/development/frontend/shapes/app/responsive/responsive.md) (bottom bar, stacked tables, phone dialogs, list and detail, motion; skeletons in [loading](../../conventions/development/frontend/core/mla/domains/data/state-and-data.md#loading)); open drafts, including swipe row actions and full-page versus modal dialogs, in [responsive proposals](../../conventions/development/frontend/shapes/app/responsive/responsive-proposals.md). The owner reviews them in Wheelhouse v0.5 |

---

## Workspace

| Task ID | Task | Deadline | Priority | Status | Repo | Notes |
|---|---|---|---|---|---|---|
| `wks-t-001` | Give every app a correct public identity: logo, description and homepage | `-` | normal | `todo` | `-` | Added `2026-10-13` by the user. Covers each product and platform app, its GitHub repository About, packages and GitHub OAuth/GitHub App registrations (first: Wheelhouse's `wheelhouse-dev` OAuth app). Inventory every surface, then fix per app |
| `wks-t-002` | Review the `product.json` manifest and the icon variant set together, then roll both out | `-` | normal | `todo` | `-` | Added `2026-10-15` by the user: decide the required variants (monochrome is missing everywhere, including Wheelhouse), then add `product/product.json` and `product/brand/icons/` to ForeverPin and the product template. Conventions: `design/identity/` |
| `wks-t-003` | Rename both SDKs to `wow-two-sdk-beta.be` and `wow-two-sdk-beta.fe`, packages and namespaces included | `-` | `high` | `done` | `-` | Decided `2026-10-16` by the user: repos, local folders and remotes; NuGet `WoW2.Sdk.Backend.Beta*` → `WoW2.Sdk.Beta.Be*` and namespace `WoW.Two.Sdk.Backend.Beta` → `WoW.Two.Sdk.Beta.Be`; npm `@wow-two-beta/ui-vue` → `@wow-two-beta/fe`. Consumers are frozen; Wheelhouse moves now, the rest on their next upgrade. Starts once running SDK work lands. Done `2026-10-17`: both SDKs publish under the new names (`@wow-two-beta/fe` 0.0.20, `WoW2.Sdk.Beta.Be` 10.0.68-beta) and Wheelhouse uses them; npm's old names are deprecated, NuGet's wait in the backlog; other consumers move on their next upgrade |
| `wks-t-004` | Remove material that should not be public from `wow-two-ws` | `-` | normal | `todo` | `wow-two-ws` | Added `2026-10-20` by the user: the repo stays public because wow2 is a public community. Inventory and move out personal business material — e.g. `ideas/parent-company-2026-10/` (tax, banking), client names, private venture plans. Removed files stay in git history; decide whether to rewrite it |
| `wks-t-005` | Ask Anthropic, via `/feedback` in the Claude desktop app, for a permanent JavaScript grant in the built-in browser | `-` | low | `todo` | `-` | Added `2026-10-21` by the user: on Wheelhouse's tailnet console host the pane says site-level permissions are disabled and offers only Allow once, so every JavaScript check asks again. Agents use JavaScript there when it is more accurate than screenshots |

---

## Backlog

Not started, ordered, top = next. Pulling one promotes it above and mints its ID.

### → be sdk (`wow-two-sdk-beta.be`)

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
| Align result, validation and ProblemDetails conventions with `AppError` | check | From the be sdk's errors research §6; verify what already landed |
| Settle explicit `IQuery` / `ICommand` markers in `mediator.md` | check | From the be sdk's mediator research, decision 2; verify first |
| Resolve `Provides mapping for` vs `Extends` in XML-doc summaries | issue | TNIS: `request-models.md:82` against `documentation/summary.md:83` |
| Name grouped controls and input suffixes; prefer gaps and separators to borders | feature | ForeverPin polish findings (`ShapeControls` vs `ShapeControlsGroup`) |
| Document the derived component-catalog pattern in `sdk-structure.md` | feature | fe sdk v0.1 iteration 3 |
| Move shipped facts from the fe sdk vector analyses into conventions | check | fe sdk content audit |

### → product template (`wow-two-sdk-beta.product-template`)

| Item | Type | Notes |
|---|---|---|
| Stop `vue/html-self-closing` fighting Prettier on void elements | issue | PbnStudio; `eslint.config.mjs` lacks the override |
| Serve `vite preview` over http without the mkcert `server.https` | issue | Hijinx: http previews and E2E get empty responses |
| Stamp `src/form.ts` into new repos | feature | fe sdk forms row, deferred |

### → SDK repos (`wow-two-sdk-beta.be` · `wow-two-sdk-beta.fe`)

| Item | Type | Notes |
|---|---|---|
| Deprecate the old be sdk packages on NuGet | chore | Added `2026-10-16`; npm half done `2026-10-17` (`@wow-two-beta/ui-vue` and `@wow-two-beta/ui` point at `@wow-two-beta/fe`). NuGet has no CLI deprecation: per package on nuget.org, Manage › Deprecation › all versions › Legacy, alternate = the `WoW2.Sdk.Beta.Be*` twin, for the 7 `WoW2.Sdk.Backend.Beta*` packages |

### → CI outside Wheelhouse and Ocharo (audit `2026-10-19`; shared `delivery.yml` is pipelines `v0.9.0`)

| Item | Type | Notes |
|---|---|---|
| Move Secrets Vault to shared delivery with its tests in CI | issue | Legacy release-triggered publish; Integration and Migrations tests exist but never run; no job timeouts |
| Move Haven to shared delivery and descriptor 2 | issue | Legacy release matrix x6, no descriptor; its only CI run failed (Images); 25 commits unpushed |
| Move ForeverPin to shared delivery | issue | Legacy publish pinned to drydock and not gated on its CI |
| Push TNIS and prove its CI | issue | CI never ran: 41 commits unpushed; browser script not in CI |
| Add CI to the hub repos | feature | `wow-two-ws`, `10x-ventures`, `ocharo-ws` hold the catalogs Wheelhouse reads; no schema or link check |
| Stamp the delivery caller into the product template | feature | `create-repo` stamps no workflows, so new repos start without CI |
| Give the be sdk a path filter, a job timeout and a separate NuGet wait | issue | Docs pushes release NuGet versions; no timeout (one 528-min run); 7-12 min of each run waits on NuGet |
| Retarget the fe sdk `test.yml` to the live package | issue | It tests the parked React package; `pnpm test \|\| pnpm test` hides a vite race |

---

## Detail pointers

Not tasks — where a promoted capability gets broken down.

| Source | Holds |
|---|---|
| `workbench/{org}/{repo}/engineering/planning/` | that repo's backlog and version track (`conventions/planning/version-track/version-track.md`) |
| `workbench/maxs-projects/clients/mintrans/ventures.tnis-mintrans/engineering/planning/backlog.md` | `TNIS` follow-up breakdown (the former follow-up roadmap) |
| `workbench/maxs-projects/clients/mintrans/ventures.tnis-mintrans/` | the Mintrans deliverable — demo + integration |
| `workbench/wow-two/wow-two.refinement` | live ecosystem state + roadmap |

---

## Done

Completions land here, ID preserved so day-log references keep resolving. Pruned once a version doc or git carries them.

| Task ID | Task | Outcome |
|---|---|---|
| `ven-t-008` | Send the Mintrans project requirements | ✅ `2026-08-19` — prepared 9:00 AM + 3:00 PM, sent 3:30 PM. Precedes `ven-t-004` |

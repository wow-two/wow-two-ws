# Next tasks: Ocharo services, Ocharo release, fe sdk, AI, Events server

*Written 2026-11-16 from the repos as they stand (read-only check). Scope: outside SCFD's internals and the
SCFD → Events → Ocharo Events path. Ordered by pull priority inside each group.*

## How to use this list

Repo paths, all under `wow-two-ws/workbench/`:

| Short name | Path |
|---|---|
| `ocharo-platform` | `mfts-projects/ventures/ocharo-hq/ocharo-ws/workbench/ocharo-platform` |
| `ocharo-marketing` | `mfts-projects/ventures/ocharo-hq/ocharo-ws/workbench/ocharo-marketing` |
| `ocharo-studio` | `mfts-projects/ventures/ocharo-hq/ocharo-ws/workbench/ocharo-studio` |
| `wow-two-sdk-beta.fe` | `wow-two-sdk-beta/wow-two-sdk-beta.fe` (code in `engineering/codebase/wow-two-sdk-beta-fe`) |
| `wow-two-sdk-beta.ai` | `wow-two-sdk-beta/wow-two-sdk-beta.ai` |
| `wow-two-sdk-beta.events` | `wow-two-sdk-beta/wow-two-sdk-beta.events` |
| `wow-two-sdk-beta.harvest` | `wow-two-sdk-beta/wow-two-sdk-beta.harvest` (SCFD) |

Rules for every task:

- Read the repo's own `CLAUDE.md` first; record the work in the repo's active version track in the commit that
  builds it (`ocharo-platform` opens `engineering/planning/version-track/v0.4/v0.4.md` for the extractions).
- `#N` points cite wow-two-ws `system/sessions/events-integration/events-integration.md`; `E2`–`E7` cite `ocharo-ws`
  `docs/app-boundaries.md`.
- One-time data moves are agent-run statements on the target, counted before and after and recorded in the version
  track; no migration reads another service's schema (#52).
- An fe sdk change ships through wow-two-ws `conventions/development/dev-cycle.md` § SDK change loop and § SDK release
  sync: gates, one commit, push when the repo's push flag is ON, wait for CI's release commit, `git pull --ff-only`.
- Commit and push only as the repo's git flags allow; never force, never commit a package version.
- No secrets, host addresses or personal data in any repo.
- Each Ocharo extraction follows the Events app's two-release pattern (`ocharo-platform`
  `engineering/research/events-app.md`): R1 adds the service, app, Identity client and deploy entry; R2, after a
  dev read-back, removes Desk's slice and adds the app to every Ocharo app's menu.

---

## Ocharo services

### O01 Sourcing service and app out of Desk (R1)
- Repo: `ocharo-platform` · Area: services/sourcing · Type: engineering
- Why: #61's order puts Sourcing next after the Events app; the supplier CRM becomes an Ocharo service of its own (E2).
- Do:
  - Scaffold `engineering/codebase/ocharo-sourcing.backend-services/` (`OcharoSourcing.{Api,Application,Domain,Infrastructure,Persistence}`, unit and E2E tests) and `ocharo-sourcing.frontend-services/` (pnpm workspace, app `apps/web` on `AppFrame`) by copying the host shape of `ocharo-events.*`: BFF session, session cache schema `ocharo_sourcing_cache`, Data Protection keys, `/health`, `/api/system/status`, `/api/runtime-config`, `migrate` and `config check` verbs.
  - Move Desk's Sourcing slice with its wire unchanged: `brand-workspace.backend-services/BrandWorkspace.Api/Sourcing/**` (`SourcingController` at `api/organizations/{organizationId}/sourcing`, `SourcingImportVerb`, `SourcingUploadReader`, models) and `BrandWorkspace.{Application,Domain,Infrastructure,Persistence}/Sourcing/**`; the frontend's `apps/web/src/presentation/sourcing` and `application/sourcing` with their tests.
  - Adopt schema `sourcing` in place, no data move: `OcharoSourcing.Persistence/Migrations/001-baseline` creates `sourcing.suppliers`, `people`, `contact_routes`, `media_contents` and `media` with `CREATE TABLE IF NOT EXISTS`, column for column as Desk's `007-sourcing` plus the Files `file_id` columns Desk added (follow `OcharoCatalogue.Persistence/Migrations/001-baseline` for the idempotent style).
  - `engineering/deployment/deploy.yml`: service and site `sourcing`, image `deployment/sourcing/Dockerfile`, `migrate` and `configCheck` items, `Files:BaseUrl` linked to `Identity:Server:Resources:2:Uri`; Identity client 12 `ocharo-sourcing` (`authorization_code` + `token_exchange` to `files`, namespace `sourcing`, URIs typed per environment like client 11); roles: owner, admin and editor `sourcing:read` + `sourcing:edit`, viewer `sourcing:read`.
  - Design note `engineering/research/sourcing-service.md` in the shape of `events-app.md`; v0.4 Iteration 1.
- Done when: `dotnet test` in `ocharo-sourcing.backend-services` passes with E2E cases for 401 without a session, 404 for another organization's route, 403 for a viewer's write; on dev the Sourcing app lists, for the owner, the same supplier count and media Desk lists.
- Depends: —

### O02 Desk's Sourcing slice leaves; every app links Sourcing (R2)
- Repo: `ocharo-platform` (+ `ocharo-marketing`, `ocharo-studio`) · Area: services/desk · Type: engineering
- Why: one writer per schema; Desk keeps nothing of Sourcing once the app reads back on dev.
- Do:
  - Remove Desk's Sourcing controller, verb, reader, slice, frontend pages and tests; drop the sourcing tables from `BrandWorkspace.Infrastructure/Files/Services/DeskFilesBackfill.cs` and `IDeskFileIdRepository`; Desk's old sourcing address redirects to the Sourcing app.
  - Desk's `007-sourcing` stays applied history; Desk adds no further sourcing migration.
  - Add `OcharoApps:Sourcing` (`from: Sites:sourcing:Url`, or `{ repository: platform, key: Sites:sourcing:Url }` outside this repo) to every app's runtime-config menu: Desk, Brand, Catalogue and Events here; Marketing and Editorial in `ocharo-marketing`; Studio in `ocharo-studio` (`OcharoAppsSettingsExtensions.cs`, `UseOcharoApps.ts`).
  - Mark the Sourcing row built in `ocharo-ws` `docs/app-boundaries.md`; v0.4 Iteration 2.
- Done when: on dev `GET /api/organizations/{id}/sourcing/suppliers` on Desk answers 404, the Sourcing app still lists every supplier, and each app's menu shows Sourcing; all suites pass in the three repos.
- Depends: O01

### O03 Image service: background-removal relay out of Desk
- Repo: `ocharo-platform` · Area: services/image · Type: engineering
- Why: #61 makes Desk's relay a small service of its own now, a proper image worker later; Editorial is its only caller.
- Do:
  - Move the Python worker into `engineering/codebase/ocharo-image.backend-services/worker/` (update `image-worker`'s build `context`, `paths` and `deployment/image-worker/Dockerfile`) and add the .NET relay beside it: `OcharoImage.BackendServices.slnx`, `OcharoImage.Api` with unit and E2E tests, API only.
  - Move Desk's relay with its route and wire unchanged: `BrandWorkspace.Api/MediaProcessing/**` (`BackgroundRemovalController` at `api/integrations/media/background-removal`, `ImageBodyReader`, `MediaProcessingPolicy`), `BrandWorkspace.Application/MediaProcessing/**`, `BrandWorkspace.Infrastructure/MediaProcessing/**`.
  - `deploy.yml`: service and site `image` with `ImageProcessing:WorkerBaseUrl` and `ImageProcessing:WorkerKey` (moved from Desk), `Identity:Resource:*`, a `configCheck` item; Identity resource 5 `image` (scope `image.remove-background`, `Uri` from `Sites:image:Url`); client 4 `editorial` gains resource `image` and that scope beside its current `desk.remove-background` until O04.
- Done when: `dotnet test` in `ocharo-image.backend-services` passes with E2E cases for 401 without a token, 403 for a token lacking `image.remove-background`, and a PNG answer from a scripted worker; on dev `GET …/background-removal/capabilities` on the image site answers 200 to Editorial's service token.
- Depends: —

### O04 Editorial calls the Image service; Desk drops its relay
- Repo: `ocharo-marketing` (+ `ocharo-platform`) · Area: editorial/media · Type: engineering
- Why: closes the last outside call into Desk (app-boundaries § Cross-app flows).
- Do:
  - `ocharo-blog.backend-services`: rename `Blog:DeskBaseUrl` to `Blog:ImageBaseUrl` in `BlogOptions.cs`, `EditorialImageWorker.cs` (`DeskOrigin` → `ImageOrigin`) and `OcharoBlog.Api/Configurations/HostConfiguration.Extensions.cs:224` (the token `Resource`); `engineering/deployment/deploy.yml` links it `{ from: { repository: platform, key: Sites:image:Url } }`.
  - Adjust `apps/editorial` tests (`MediaEditingApi.test.ts`, `MediaEditing.test.ts`) only where names changed.
  - `ocharo-platform`: remove Desk's MediaProcessing slice, its `ImageProcessing:*` keys, and client 4's `desk` resource and `desk.remove-background` scope; resource 0 `desk` keeps its other uses.
- Done when: on dev an Editorial cover image's background removal returns a PNG through the Image service, and Desk's `api/integrations/media/background-removal` answers 404; Blog's and Desk's suites pass.
- Depends: O03

### O05 Brand takes the brands list and business cards
- Repo: `ocharo-platform` · Area: services/brand · Type: engineering
- Why: #61's map: Brand owns brand identity and the brands list; business-card designs have no catalogue home.
- Do:
  - `ocharo-brand.backend-services`: `OcharoBrand.Persistence/Migrations/002-brands-and-cards` adds `brand.brands` (id, organization, name, slug, saved by and at) and card designs with revisions shaped like Desk's `design_documents.documents` / `revisions` of kind `business-card`; routes `api/brand/brands` and `api/brand/cards` (reads by membership, writes `brand:edit`).
  - Brand app: a Brands page and the business-card designer, moved from Desk's `presentation/brands` and `presentation/design` (`CardTools.vue` and the card pages; not `design/catalogue`).
  - Copy dev's rows by hand (#52): count `preparation.brands` and `design_documents.documents WHERE kind = 'business-card'`, insert them with the same ids, record the counts.
  - Desk: brand create and the card pages redirect to Brand; `preparation.brands` stays, read-only, while `commerce.*` holds foreign keys to it (until O12).
- Done when: Brand's backend and app tests pass; on dev the Brand app lists the same brand ids and business cards Desk listed, and a card saved in Brand reopens at its revision.
- Depends: —

### O06 Catalogue: release gate for the public product feed
- Repo: `ocharo-platform` · Area: services/catalogue · Type: feature
- Why: E3 port: Desk serves its product feed only from a published release (`commerce.releases`); the Catalogue app's `api/public/catalogue` serves live products.
- Do:
  - `OcharoCatalogue.Persistence/Migrations/002-product-releases`: `catalogue.product_releases` (id, revision, immutable snapshot `jsonb`, note, published by and at, withdrawn by, at and reason), mirroring Desk's `005-commerce` `releases`.
  - Routes `GET|POST api/catalogue/releases` and `POST api/catalogue/releases/{id}/withdraw` (`catalogue:approve`), as `CommerceController`'s `releases` routes.
  - `Catalogue/Publishing/Controllers/PublicFeedsController.cs` serves only the active release's snapshot; a Releases page in `ocharo-catalogue.frontend-services` (publish with a note, withdraw with a reason, history).
  - Before the gated build reaches dev, publish release 1 from the current products by an agent-run call, so Marketing and Blog keep reading the same products.
- Done when: E2E: an edit after a publish leaves `GET api/public/catalogue` unchanged until the next release, a withdraw removes the release from the feed, and a member without `catalogue:approve` gets 403; existing Catalogue tests pass.
- Depends: —

### O07 Catalogue: per-image rights approval
- Repo: `ocharo-platform` · Area: services/catalogue · Type: feature
- Why: E3 port: Desk publishes an image only with an approval and its provenance (`BrandWorkspace.Domain/Commerce/Models/MediaApproval.cs`).
- Do:
  - Catalogue product images carry `MediaApproval`'s fields per SHA-256: kind, approved for publication, source URL, credit, rights; plus approved by and at (`OcharoCatalogue.Persistence/Migrations/003-image-rights`).
  - Releases (O06) and the public feed include only approved images and expose their provenance, as Desk's `PublicProjection.cs` does.
  - The product editor's image group gets the approval fields; withdrawing approval affects the next release only.
- Done when: E2E: a release snapshot leaves out an unapproved image and holds it after approval with its credit; a released snapshot never changes after a later revocation.
- Depends: O06

### O08 Catalogue: who saved and who published
- Repo: `ocharo-platform` · Area: services/catalogue · Type: feature
- Why: E3 port: Desk records an actor on every revision, release and withdrawal; Catalogue's tables record none.
- Do:
  - `OcharoCatalogue.Persistence/Migrations/004-authorship`: nullable saved-by (Identity `sub` plus display name) on product and design revisions, published-by on design releases and product releases; old rows stay null.
  - Fill them from the BFF session in the save, publish and withdraw handlers.
  - Show them in product history, design history and Releases (null reads "unknown").
- Done when: E2E: a save and a publish by a signed-in member read back with that member's `sub` and name; history renders old rows as unknown.
- Depends: O06

### O09 Catalogue receives Studio's creative imports (E6)
- Repo: `ocharo-platform` (+ `ocharo-studio`, `ocharo-marketing`) · Area: services/catalogue · Type: engineering
- Why: E6 is decided: Catalogue is the one receiver; Desk (`commerce.creative_imports`) and Marketing (`api/marketing/creative-imports`) both receive today.
- Do:
  - Catalogue: `POST|GET api/catalogue/creative-imports` (snapshot `jsonb`, actor, time), shaped after Desk's `CommerceController` routes `creative-imports` and Marketing's `CreativeImportsController`; a Studio imports page in the Catalogue app.
  - `ocharo-studio`: point `apps/web/src/integration/studio/clients/CreativeHandoff.ts` at Catalogue, its URL linked from `Sites:catalogue:Url`.
  - After the dev read-back, remove Desk's and Marketing's receivers and pages; copy their dev rows by hand (#52) if any exist.
- Done when: on dev a Studio handoff lands in Catalogue's imports page, and Desk's and Marketing's creative-import routes answer 404; Studio's `creative-handoff.test.ts` passes.
- Depends: —

### O10 One public catalogue feed for Marketing and Blog (E4)
- Repo: `ocharo-marketing` · Area: marketing/catalogue-feed · Type: engineering
- Why: E4 pick: Catalogue owns the one feed; Marketing and Blog still carry a `PlatformBaseUrl` branch for Desk's feed shape.
- Do:
  - Remove `PlatformBaseUrl` from `OcharoMarketing.Infrastructure/Core/MarketingOptions.cs`, `Automation/CatalogueSyncService.cs`, `Inquiries/PublishedProductVerifier.cs`, `OcharoMarketing.Api/Configurations/HostConfiguration.Extensions.cs`, and from Blog's `BlogOptions.cs`, `CatalogueFeed.cs`, `BrandKit.cs`; read only `CatalogueBaseUrl` / `BrandBaseUrl`.
  - Drop the Desk-shape decoding; read the release-gated feed (O06) with image provenance (O07).
  - Close the open E4 line in Marketing's version track and tick E4 in `docs/app-boundaries.md`.
- Done when: `grep -rn PlatformBaseUrl engineering/codebase` in `ocharo-marketing` finds nothing; Marketing's sync and enquiry checks and Blog's catalogue pages pass their E2E against a Catalogue feed fixture; on dev both show the released products.
- Depends: O06, O07

### O11 Post drafts move from Desk to Marketing
- Repo: `ocharo-marketing` (+ `ocharo-platform`) · Area: marketing/drafts · Type: engineering
- Why: #61: Desk's content draft is a post draft, and Marketing already has drafts, approval and export.
- Do:
  - Compare Desk's `PreparationController` drafts routes (`drafts`, `request-review`, `approve`, `revoke-approval`, `exports`, `exports/{id}/download`) and its draft content (brand, title, caption, language, destination, source notes, media) with Marketing's `Posts/Controllers/DraftsController.cs` (`drafts`, `approve`, `schedule`, `export`); add what Marketing lacks in `OcharoMarketing.Persistence/Migrations/003-desk-drafts`.
  - Approval binds the exact revision: an edit after approval drops it; media are Files ids, never bytes.
  - Copy dev's drafts, revisions, approvals and exports by hand (#52) with the same ids; record counts.
  - Remove Desk's content pages (`presentation/content`), drafts routes and the related approval and export code.
- Done when: Marketing E2E: a draft with media goes request-review → approve → export ZIP, and an edit after approval clears it; on dev Marketing's draft count equals Desk's.
- Depends: —

### O12 Remove Desk; organization switch moves to the frame
- Repo: `ocharo-platform` (+ `ocharo-marketing`, `ocharo-studio`, `ocharo-assets`) · Area: services/desk · Type: engineering
- Why: Desk has no job once the extractions land, so it is removed last (#61).
- Do:
  - Every app passes the session's memberships to `AppFrame`'s account menu (`organizations`, `v-model:organization`; the fe sdk's `AccountMenu` switches at two or more), replacing Desk's organization chooser.
  - Retire Desk's Commerce, DesignDocuments (catalogue kind), `CatalogueWebDesigner.vue`, `LegacyCommerceReader` and `PublicBrandsController` (`api/public/v1/brands/{slug}`); move any job still scheduled in `BrandWorkspace.Worker` to its new owner first.
  - `deploy.yml`: remove services `desk` and `jobs`, site `desk`, client 0 and resource 0 (indexes kept as gaps, like client 9), every `OcharoApps:Desk` key and the `desk:*` role permissions.
  - Last Desk release: a forward-only migration drops schemas `preparation`, `design_documents` and `commerce` after counts prove every row moved; `access` (the old sign-in tables) only after prod's Identity cutover.
- Done when: on dev no service, site, Identity client or menu entry named Desk remains, every app switches organization from its account menu, and all suites pass in the four Ocharo repos.
- Depends: O02, O04, O05, O08, O09, O10, O11

---

## Ocharo release

### O13 Prod promotion audit for Ocharo's Events app
- Repo: `ocharo-platform` · Area: deployment/prod · Type: engineering
- Why: the Events app and client 11 run only on dev; prod runs an older platform release (Desk's migrations stop at `010`), so the promotion jumps many releases.
- Do:
  - Write `engineering/research/prod-promotion.md`: every required, typed, linked and generated key `deploy.yml` declares at the tag to promote, per service (identity, desk, jobs, image-worker, brand, catalogue, events), against what prod's target holds (read-only, Wheelhouse prod console).
  - List the migrations prod would run (`012-files`, `013-identity-cutover`, `014-events-retire`, the pilots' and Events app's sets) and confirm `014` drops an empty `events.showcase_events` (0 rows read 2026-11-10).
  - Name each prerequisite with its owner: Ocharo Identity on prod (G3, parked by the owner, `engineering/research/identity-cutover.md` #51), Files tenant `ocharo` on prod (`files-adoption.md` #2, parked), the Events prod target (O14), and resource 4 `harvest` and client 8, which have no SCFD on prod (typed values or a dev-only declaration).
- Done when: the doc lists every key with its source and status and every blocker with its owner, and a check of `deploy.yml` at the promoted tag finds no required key missing from it.
- Depends: —

### O14 WoW2 Events prod target `events-prod`
- Repo: `wow-two-sdk-beta.events` (operated in the Wheelhouse prod console) · Area: deployment · Type: engineering
- Why: `Events:BaseUrl` on prod links to resource 3's `Uri`, so Ocharo's Events app needs a WoW2 Events on prod.
- Do:
  - Target `events-prod` on Ocharo's prod server, database `events_prod`, site `app`; type `Events:Auth:*` with prod Ocharo Identity's issuer exactly as tokens' `iss` (trailing slash kept) and resource 3's prod `Uri` as audience; `Events:Console:ClientSecret` through the owner link from client 10; leave `Events:Intake:Sources:*` untyped, so intake stays off (no SCFD on prod, #50).
  - Run through Wheelhouse Run: `catalog ensure ocharo-fashion --owner-org {prod Ocharo organization id} --name "Ocharo fashion"`, then `workflow put` with the 8 stages used on dev.
  - Record the target in the events repo's `engineering/deployment/deployment.md` (names only, no host addresses).
- Done when: on `events-prod` `/health` answers 200, `/api/system/status` shows the deployed version with `intake` `off`, `GET /api/events/v1/catalogs` answers 401 without a token, and both host verbs exit 0.
- Depends: O13

### O15 Ocharo prod Identity keys for Events
- Repo: `ocharo-platform` · Area: deployment/prod · Type: engineering
- Why: Identity refuses to boot when a declared client or resource lacks its URIs, and the Events app signs in as client 11.
- Do:
  - On prod's `identity`: type resource 3's `Uri` and `SignalUrl` (the `events-prod` site), client 10's redirect, sign-out and signal URIs, and client 11's (`{Url}api/identity/callback`, `{Url}`, `{Url}api/identity/signal` of prod's `events` site), plus the resource 4 and client 8 answer from O13.
  - Finish the G3 steps the owner releases: Ocharo's organization and the owner's membership on prod.
  - Confirm the Files tenant `ocharo` on prod, since every platform release from `v0.1.34` stores media in Files.
- Done when: a readiness check of the promoted release on prod reports no missing required key, and Identity's `config check` reads consistent.
- Depends: O13, O14

### O16 Promote Ocharo's Events app to prod and read back
- Repo: `ocharo-platform` (+ `ocharo-marketing`, `ocharo-studio`) · Area: deployment/prod · Type: engineering
- Why: closes "Not promoted to prod" for the `events` service and client 11 (#62).
- Do:
  - On the owner's go, promote `ocharo-platform` (`v0.3.12` or later), `ocharo-marketing` (`v0.1.18` or later) and `ocharo-studio` (`v0.1.24` or later) through Wheelhouse's prod promotion (dev-proven releases only).
  - Only on the owner's yes, seed prod's catalog: `import --dry-run`, then `import`, with the kept `wow2.events-import.v1` bundle (outside git; sha256 starts `308deb17`).
  - Record the read-back in v0.4's verification list.
- Done when: on prod the Events app signs in through `ocharo-events`, lists the catalog through its own origin, a tracking save answers 200, another organization's path answers 404, the bar reads 56 px, and Desk's old Events address redirects to the app.
- Depends: O15

---

## fe sdk

F01–F04 finish the toast work a ChatGPT (Codex) session left uncommitted; start them only after that session stops
writing in the tree. F05–F10 lift the SCFD console's `sdk-candidate` items (harvest
`engineering/planning/version-track/v0.2/v0.2.md` entries 6–24), each checked against the fe sdk at `fe-v0.0.48`; the
console's adoption of each is the SCFD lane's.

### F01 Toast work: fold features.md into backlog and track
- Repo: `wow-two-sdk-beta.fe` · Area: docs, playground · Type: engineering
- Why: `engineering/features.md` breaks wow-two-ws `conventions/planning/version-track/version-track.md:17`, the backlog lost `Feedback bus`, and the playground carries product names.
- Do:
  - Delete `engineering/features.md` and its link in `engineering/engineering.md`; restore `Feedback bus | shipped v0.1 | —` in `engineering/planning/backlog.md` § Features and add `Toast notifications | implemented, release pending | [toast-notifications.md](../architecture/analysis/toast-notifications.md)`.
  - Replace the link-only `## Toast notifications` in `version-track/v0.1/v0.1.md` with an iteration entry, one checkbox per capability: priority, deadlines, pin, remind later, grouping, overflow, motion presets, safe-area insets.
  - Remove the product rollout rows (SCFD, Ocharo Catalogue pilot, other products) from the backlog's `## Notifications`; keep the SDK-wide upgrade row.
  - Playground: replace `apps/playground/src/toastLab/ScfdPostsPreview.vue`, the copied SCFD logo and favicon, the afisha links and the Ocharo previews with neutral samples.
- Done when: `engineering/features.md` is gone; `grep -rniE "scfd|afisha|ocharo" engineering/codebase/wow-two-sdk-beta-fe/apps/playground engineering/planning/backlog.md` prints nothing; `node apps/playground/tests/gallery-smoke.mjs` passes.
- Depends: —

### F02 Toast API: string enum values and an SFC action
- Repo: `wow-two-sdk-beta.fe` · Area: feedback · Type: fix
- Why: the new public enums break wow-two-ws `conventions/development/frontend/core/lla/components/enums.md` §3 and would freeze at release; `RemindLaterAction` uses `h()` where a template fits (`conventions/development/frontend/core/lla/constructs/vue/composition.md`).
- Do:
  - `src/feedback/FeedbackBus.ts`: `NoticePriority` values `low`, `normal`, `high`, `urgent`, plus an exported `NoticePriorityRank` map the host's sort reads; doc line `Defines …`, members `Refers to …`.
  - `src/presentation/feedback/toastHost/ToastHost.vue`: `ToastMotion` values `sideSlide`, `shortSlide`, `edgeSlide`, `slideAndSettle`; `ToastTimer.CloseRing` value `closeRing`; `Defines …` / `Refers to …` doc lines on `ToastMotion` and `ToastGroupMotion`; update every `data-toast-timer` selector, `styles.css`, the specs and `scripts/check-package.mjs` that read these values.
  - Move `RemindLaterAction` (`FeedbackToastHost.vue:74`, `defineComponent` + `h()`) into `feedbackToastHost/RemindLaterAction.vue`; the grouped `h(TransitionGroup)` list may stay.
- Done when: `pnpm typecheck`, `pnpm lint` (0 errors) and `pnpm test` pass; a unit test proves `urgent > high > normal > low` with delivery order on ties; no member of `NoticePriority`, `ToastTimer`, `ToastMotion` or `ToastGroupMotion` has a numeric or kebab-case value.
- Depends: —

### F03 Split ToastHost into composables and test its untested paths
- Repo: `wow-two-sdk-beta.fe` · Area: feedback · Type: engineering
- Why: `ToastHost.vue` grew to ~1,490 lines holding the store, clocks, capacity, motion, overflow and highlights; overflow, merge motion, compact rows and the details disclosure have only the playground smoke test.
- Do:
  - Extract into `src/presentation/feedback/toastHost/`: `UseToastClock.ts` (deadlines, pause, pin and unpin clocks), `UseToastCapacity.ts` (`max`, viewport-height capacity, overflow count), `UseToastGroupMotion.ts` (merge and count highlight); the SFC keeps the template and wiring.
  - Fix the `max-len` warnings at `toast/ToastContent.vue:29` and `ToastHost.vue:1444`.
  - DOM tests under `tests/unit/presentation/feedback/` for "Show N more notifications", group merge, compact rows and the details disclosure.
- Done when: `pnpm lint` shows no warning in the toast files, `pnpm test` passes with the new cases, and `ToastHost.vue` holds no clock, capacity or motion state of its own.
- Depends: F02

### F04 Release the toast overhaul
- Repo: `wow-two-sdk-beta.fe` · Area: release · Type: engineering
- Why: Pin, overflow and the honoured `position` reach every consumer on re-pin, so the release must say so.
- Do:
  - Commit `engineering/development/rules.md` (Vue gotchas, unrelated to the toasts) on its own first.
  - Add a `MIGRATION.md` entry: Pin on every timed toast (`canPin` defaults to `true`), the "Show N more notifications" overflow, `position` honoured again (`bottom-right` moves), the card layout through `ToastContent`.
  - From `engineering/codebase/wow-two-sdk-beta-fe`: `pnpm typecheck`, `pnpm lint`, `pnpm format:check`, `pnpm test` (Firefox runs in CI), `pnpm build`, `pnpm --filter playground build`, `node apps/playground/tests/gallery-smoke.mjs`, `pnpm check:package --install`; then commit, push, wait for the release commit, `git pull --ff-only`.
- Done when: `npm view @wow-two-beta/fe version` shows the new version, and its tarball's CSS holds `--toast-motion-transform` and `--toast-available-height`.
- Depends: F01, F02, F03

### F05 Grid: auto-fill columns by minimum width
- Repo: `wow-two-sdk-beta.fe` · Area: presentation/layout · Type: feature
- Why: harvest v0.2 #7: a card gallery steps 4 → 3 → 2 → 1 columns by the width it has; `Grid` takes only fixed counts per viewport breakpoint.
- Do:
  - `src/presentation/layout/grid/Grid.vue` and `Grid.variants.ts`: prop `minColumnWidth` (a CSS length); when set, a static class `grid-cols-[repeat(auto-fill,minmax(min(100%,var(--grid-min-column)),1fr))]` plus the inline variable replaces `columns`.
  - `Grid.spec.md`, the playground fixture `apps/playground/src/gallery/fixtures/LayoutExamples.ts`, tests.
- Done when: a browser test with `minColumnWidth="16rem"` and `gap="3"` renders 4, 3, 2 and 1 columns at container widths 1100, 900, 700 and 520 px.
- Depends: —

### F06 MediaCard: image-first card with a faded glass panel
- Repo: `wow-two-sdk-beta.fe` · Area: presentation/display · Type: feature
- Why: harvest v0.2 #6, #9, #10, #11, #22: an image card that keeps its ratio as columns change, a blur that fades upward over a dark gradient, and a link over the whole card; `Card` and `FeatureCard` are text-first.
- Do:
  - New `src/presentation/display/mediaCard/` (`MediaCard.vue`, `MediaCard.spec.md`, `index.ts`, exported from `presentation/display`): props `ratio` (default `4/5`), `href` (a stretched link over the card, router-aware like `CardLink`), `isDimmed` (grayscale), `panelHeight` (default `8.5rem`); slots `media` (an image or a `Carousel`), `fallback` (a soft tile with no media), `default` (the text panel), `topStart`, `topCenter`, `topEnd`.
  - The panel: a blur layer over the lower 60 %, masked `linear-gradient(to top, black 50%, transparent)`, a dark gradient under white text; the media zooms slightly on hover, not under reduced motion.
  - Controls in the top slots sit above the stretched link; the spec shows `topCenter` holding a glass pill around `DotsIndicator`.
- Done when: DOM tests: a click on the media follows `href`, a click on a `topEnd` button does not; the measured aspect ratio holds in 1, 2 and 4 columns; the playground fixture renders in light and dark.
- Depends: —

### F07 Button: unavailable state for glass icon buttons
- Repo: `wow-two-sdk-beta.fe` · Area: presentation/actions · Type: feature
- Why: harvest v0.2 #13: an open-original button with no link stays visible, dashed and dimmed with a slash and a reason; `Button` has `glass` / `glass-surface` and `shape="circle"` but only `isDisabled`.
- Do:
  - `src/presentation/actions/button/Button.vue` and `Button.variants.ts`: `isUnavailable` keeps the button focusable with `aria-disabled="true"`, swallows press, draws a dashed border at reduced opacity and a diagonal slash over the icon for `circle` and `square` shapes.
  - `unavailableLabel` shows through the SDK `Tooltip` and becomes the accessible description.
  - Spec, a playground fixture beside the glass variants, DOM tests.
- Done when: DOM tests: Tab reaches the button, click and Enter emit no `press`, `aria-disabled` reads `true`, the label is its accessible description; existing `isDisabled` tests pass unchanged.
- Depends: —

### F08 Badge: glass tones and a shrinkable label
- Repo: `wow-two-sdk-beta.fe` · Area: presentation/display · Type: feature
- Why: harvest v0.2 #9, #14, #16 (`HarvestPill`, `PillIcon`): glyph pills in glass tones over images, cut with an ellipsis in a row that never wraps; `Badge` already has the `leading` slot and dashed borders, but no glass tone or truncation.
- Do:
  - `src/presentation/display/badge/Badge.variants.ts`: `BadgeVariant.Glass` (`glass`) and `BadgeVariant.GlassSuccess` (`glassSuccess`) for use over imagery.
  - `Badge.vue`: `isShrinkable` truncates the label and lets the pill shrink (`min-w-0`), keeping the `leading` glyph.
  - The glyph table stays in the app (harvest's `PostGlyphs.ts` maps SCFD kinds and sections); the spec shows a `leading` glyph through `Icon`.
- Done when: a DOM test puts a shrinkable badge in a 120 px row and finds the ellipsis with the glyph kept; both glass variants render in light and dark in the playground; existing Badge tests pass.
- Depends: —

### F09 Carousel: hover-only glass arrows and touch swipe
- Repo: `wow-two-sdk-beta.fe` · Area: presentation/display · Type: feature
- Why: harvest v0.2 #19–#21: the card carousel hand-builds hover-only glass arrows, arrows dimmed for one image, and swipe, since `Carousel` has none of them.
- Do:
  - `src/presentation/display/carousel/Carousel.vue`, `CarouselPrev.vue`, `CarouselNext.vue`: `controls` `'always' | 'hover'` (hover: shown on hover or focus-within, always under `(hover: none)`); `variant="glass"` on the arrows; with one slide the arrows are disabled, dimmed and inert, so a click falls through to the card's link.
  - `CarouselViewport.vue`: a horizontal pointer swipe moves one slide, without capturing on press (see backlog row "Fix `useDrag` and `usePinch` capturing on press").
  - Specs, fixtures, DOM and browser tests.
- Done when: browser tests: with `controls="hover"` the arrows stay hidden until hover, a swipe moves exactly one slide, a tap on a link inside a slide still navigates, and a one-slide carousel's arrows are disabled.
- Depends: —

### F10 MetaInlineText: icon-led items with spoken text
- Repo: `wow-two-sdk-beta.fe` · Area: presentation/display · Type: feature
- Why: harvest v0.2 #24: a card's last line shows items behind icons (event dates, posted age) with a fuller phrase for screen readers and a tone; `MetaInlineText` takes bare slot content.
- Do:
  - New `src/presentation/display/metaInlineText/MetaInlineItem.vue`: slot `icon`, default slot (the visible text, `aria-hidden` when `label` is set), `label` (a visually hidden phrase), `tone` `'default' | 'success' | 'muted'`, truncation.
  - Export it with `MetaInlineText`; spec, fixture, tests.
- Done when: a DOM test reads the `label` as the item's text for assistive technology and maps each tone to its class; existing `MetaInlineText` tests pass.
- Depends: —

---

## AI

Every A task: owner `ev-ai` lane (resumes 2026-11-18); the AI layer's design is wow-two-ws `ideas/ai-layer-analysis.md`
#15.

### A01 Make queued eval runs repeatable
- Repo: `wow-two-sdk-beta.ai` · owner: `ev-ai` lane · Area: evals · Type: fix
- Why: `004-eval-run-queue` blocks writes while it builds 3 indexes (the migration lint test fails), and a queued run re-selects its sample and prompt at worker start.
- Do:
  - Review the uncommitted Iteration 2 diff against `aaab511` first (`EvalRunRequest` sample fields, `EvalSampler`, `EvalRunQueue`, `EvalQueueSignal`, `AiEvalWorker`, `IAiProviderCatalog`).
  - `packages/Module/Migrations/004-eval-run-queue/Apply.sql`: build `ix_ai_eval_runs_queued`, `ix_ai_eval_runs_running` and `ix_ai_eval_runs_batch` with `CREATE INDEX CONCURRENTLY` outside the migration transaction, dropping an invalid index left by an interrupted build; a test upgrading from `003` with eval history.
  - `packages/Module/Evals/ModuleEvalsBroker.cs`: pin at enqueue the selected item ids, the label and scoring revision, and each cell's resolved prompt hash, parameters and schema; a changed or purged pinned input fails that run explicitly; refuse queues on `rewrite`-mode prompts.
- Done when: `Ai.Tests.Migrations` passes 16 of 16, and an integration test proves the worker runs exactly the pinned items and prompt hash after a prompt edit.
- Depends: —

### A02 First eval on `afisha-10` from the bench
- Repo: `wow-two-sdk-beta.ai` · owner: `ev-ai` lane · Area: evals · Type: product
- Why: #55 step 2: the first eval on 10 real posts gates the model pick; the bench is ready, only the keys are missing.
- Do:
  - After the developer sets `Ai:Providers:anthropic:ApiKey` and `Ai:Providers:openai:ApiKey` in `Ai.Api`'s user-secrets, confirm each route returns a schema-valid answer.
  - `ai eval run --set afisha-10 --fresh --version 1 --model anthropic/claude-haiku-5-5,anthropic/claude-sonnet-5-5,openai/gpt-6-luna`, then GPT on version 2; `ai eval report --set afisha-10 --format md`.
  - Confirm the draft labels with the developer and add one confirmed must-catch post (a TITF post on Afisha when one exists); hard negatives and non-Russian posts go to a separate holdout set.
  - Record per run only prompt version, model, accuracy, relevant misses, false accepts, invalid output, cost per post and p95 latency against `ocharo-fashion-v1`; post text and answers stay in the bench database (#50).
- Done when: v0.1 Iteration 3's two open boxes are checked with the summary table, and the recorded spend is under $0.05.
- Depends: —

### A03 First HTTP slice: providers, queue, status, cancel, report
- Repo: `wow-two-sdk-beta.ai` · owner: `ev-ai` lane · Area: hosting · Type: feature
- Why: the developer wants REST over the CLI on deployed hosts (v0.1 Iteration 2); the Client package ships only `AddAiClient`.
- Do:
  - `packages/Hosting`: `AddAiApi` / `MapAiApi` under `api/ai/`: `GET providers` (configured providers and live model ids), `POST evals/runs` (202 with batch and run ids), `GET evals/runs/{id}`, `POST evals/runs/{id}/cancel`, `GET evals/runs/{id}/report?format=json|csv|md`; scopes `ai.read`, `ai.run`, `ai.evals-manage`; auth off only in Development.
  - `service/Ai.Api` composes the API and `AiEvalWorker`; verbs `ai eval queue|status|cancel` and `ai providers [--live]`; `eval run` takes `--count --seed --tags --items`.
  - Bound model × sample size and worker concurrency; the report tells completed from usable results, new spend from cached, a missing price from zero cost; prompt editing, import and export stay out.
- Done when: E2E: 401 without a token, 403 without the scope, `202` → report through `ScriptedAiModelCaller`; integration: one sample across all cells, no double claim, cancel, stale-heartbeat recovery, all-provider failure.
- Depends: A01

### A04 Publish the AI packages and image
- Repo: `wow-two-sdk-beta.ai` · owner: `ev-ai` lane · Area: release · Type: engineering
- Why: SCFD and Events can reference the layer only once `WoW2.Sdk.Beta.Be.Ai.*` is on nuget.org (v0.1 Iteration 4).
- Do:
  - Run wow-two-ws `scripts/release/library.py plan wow-two-sdk-beta.ai --brand Ai` and the commands it prints, one at a time.
  - Hand the developer's steps over in one batch: the `main-guard` ruleset, nuget.org trusted publishing for `WoW2.Sdk.Beta.Be.Ai.*`, npm's first `@wow-two-beta/fe-ai` (2FA).
  - Arm `PUBLISH_PACKAGES`; tag the first `be-v*` and `fe-v*`; release the first image.
- Done when: nuget.org lists `Abstractions`, `Module`, `Providers`, `Client` and `Testing` at the first version, npm lists `@wow-two-beta/fe-ai`, and the image release exists on GitHub.
- Depends: A01, A03

### A05 SCFD relevance pass in shadow on one Afisha pipeline
- Repo: `wow-two-sdk-beta.harvest` · owner: `ev-ai` lane · Area: engine/ai · Type: feature
- Why: #55: Afisha through AI inference, Claude first with GPT as fallback; SCFD's own Process stage calls OpenAI directly (#65).
- Do:
  - `service/HarvestSources.Api`: reference the published `WoW2.Sdk.Beta.Be.Ai.Module` and `.Providers`; replace the direct `OpenAIClient` wiring in `Configurations/PipelineStageConfiguration.cs` and the keyed `IChatClient` in `packages/Module/Engine/ProcessingStore.cs` with the runner's `RunAsync("ocharo-relevance", …)`.
  - Wire an explicit pilot opt-in through `packages/Module/Engine/HarvestEngine.cs` (hardcodes `AiMode.Off`) and `sources/Module/Ocharo/OcharoSourceProvisioner.cs` (resets the mode); shadow only.
  - Classify persisted normalized post revisions outside the capture lease, keyed by tenant, container, post revision and classifier configuration; skip completed work on replay; stamp inference id, provider, model and prompt version and hash; an unavailable or invalid call stays undecided while harvesting and delivery go on.
  - Live Events delivery keeps `ocharo-fashion-v1`; a purge removes the post's text from eval inputs and stored answers.
- Done when: tests prove a replay skips finished work, a provider timeout leaves the post undecided and delivered unchanged, a purge clears stored answers, and with `AiMode.Off` the golden pages under `tests/Contract/wow2.event.v1/` come out byte for byte as before.
- Depends: A04

### A06 Budget caps and the weekly shadow comparison
- Repo: `wow-two-sdk-beta.ai` · owner: `ev-ai` lane · Area: runner · Type: feature
- Why: cost and latency limits come before more volume (SCFD gate G5), and promotion needs a weekly shadow comparison.
- Do:
  - Per use case, monthly USD soft and hard caps computed from the inference log; past the hard cap the runner refuses with a classified `budgetExceeded` error and makes no provider call; the soft cap logs a warning.
  - A verb `ai shadow report --use-case ocharo-relevance --week {iso-week}` prints AI against the rule filter: relevant misses, false accepts, cost per post, p95 latency (aggregates only).
  - Settings `Ai:Budgets:{useCase}:SoftUsd` and `HardUsd`, documented in `engineering/deployment/deployment.md`.
- Done when: an integration test proves the hard cap stops the call before any provider request, and the report verb prints the comparison for a seeded week.
- Depends: A03

### A07 Events takes SCFD's AI classification
- Repo: `wow-two-sdk-beta.events` · owner: `ev-ai` lane · Area: intake/classification · Type: engineering
- Why: #53, #54: Events' `payload` classifier is built and waits for SCFD's `classification`; a model stamp would be cut at 64 characters.
- Do:
  - Widen the mapping version past 64 characters (`packages/Module/Intake/ScfdEventMapper.cs` `MaxMappingVersionLength`, its column, a new migration).
  - Rehearse `Events:Intake:Sources:N:Classifier = payload` with `MinConfidence = 0.5` on an isolated subscription and catalog on dev; SCFD's delivery filter lets AI-positive posts the rules miss reach that subscription only.
  - Switch `afisha-fashion` and `afisha-exhibitions` only after a shadow week inside the agreed limits (A06) and the developer's word.
- Done when: on dev the rehearsal catalog publishes an AI-relevant post the rule filter rejected, holds an irrelevant one, and `intake check` reads `subscription=ok`; a unit test stores a 200-character mapping version intact.
- Depends: A05, A06

### A08 Core be sdk drops its LLM folders
- Repo: `wow-two-sdk-beta.be` · owner: `ev-ai` lane · Area: Ai · Type: engineering
- Why: the AI layer's backlog moves providers out of core after the first publish; core keeps MCP hosting (OQ-5).
- Do:
  - Remove the provider folders under `engineering/codebase/wow-two-sdk-beta-be/src/Ai/` that `Ai.Providers` replaces (`Anthropic`, `AzureOpenAi`, `Bedrock`, `Gemini`, `Llama`, `Ollama`, `OpenAi`); judge `Core`, `KernelMemory`, `SemanticKernel`, `Tokenizers` and `Vector` one by one against `Ai.Providers` and record each verdict in `src/Ai/Ai.md`; keep `Mcp` and what it needs.
  - Re-pin each consumer of the removed APIs (sift's `AddOllamaChatClient`) to `WoW2.Sdk.Beta.Be.Ai.Providers`; grep every wow-two repo for the removed namespaces first.
  - A breaking-change note in the be sdk release and its version track.
- Done when: the be sdk builds and tests pass without the folders, `AiRegistrationTests` covers MCP only, and every former consumer builds on `Ai.Providers`.
- Depends: A04

---

## Events server

### V01 Review console on AppFrame and the SDK session
- Repo: `wow-two-sdk-beta.events` · Area: console · Type: engineering
- Why: #59, #60: every console renders through the shared frame; the console keeps a local shell on fe `0.0.42` and its own BFF session reader, a backlog row unblocked by fe `0.0.44`.
- Do:
  - Re-pin `@wow-two-beta/fe` to the newest published version in `engineering/codebase/events.frontend-services/apps/web/package.json` and `packages/fe-events/package.json` (exact dev pin, peer `>=… <0.1.0`).
  - Render `apps/web` through `AppFrame`: review, observations, events, intake and imports in the sidebar, the account menu with the session's organization, `VersionBadge` from `/api/system/status` (fe sdk `engineering/architecture/app-frame-migration.md`).
  - Replace the decoding in `src/integration/session/SessionApi.ts` and `src/domain/session/ConsoleSession.ts` with the fe sdk's BFF session strategy.
  - Close v0.1 (every box is checked, status still "In progress") and open v0.2 for this task and the P2 rows below.
- Done when: the console's typecheck, lint, tests and build pass; locally the bar reads 56 px in light and dark and the badge shows the served version; on `events-dev` a reviewer signs in and the review queue loads.
- Depends: —

### V02 Places and organizers as deduplicated entities
- Repo: `wow-two-sdk-beta.events` · Area: catalog · Type: feature
- Why: P2's first catalog row: P1 embeds place and organizer in each event, so one venue repeats per event and source.
- Do:
  - Contract (`packages/Abstractions`): `Place` (name, city, country, address, geo) and `Organizer` (name, website) with ids per catalog; events reference them; the Module's migration adds the tables.
  - Match by normalized name plus city (places) and name or website (organizers); a host verb `places rebuild --catalog {c}` derives them from existing events and reruns after a rule change.
  - Reviewers merge or split places and organizers in the console; the Client, conformance suite and `fe-events` mirrors follow; embedded fields stay readable for one release.
- Done when: conformance passes for Module and Client; replaying the golden contract pages yields one place per repeated venue text; another organization's read of a private catalog's places answers 404.
- Depends: —

### V03 Cross-source match proposals
- Repo: `wow-two-sdk-beta.events` · Area: catalog/review · Type: feature
- Why: P1 matches by source identity only; once several sources feed one catalog (the 100-source goal, #51), one edition arrives twice.
- Do:
  - On intake and import, score a new candidate against published events of its catalog by title similarity (`pg_trgm`, enabled by the migration), place and date overlap; above a threshold store a match proposal beside the candidate.
  - Review console: a "Possible duplicate" panel with accept (merge: sources and evidence move, the candidate archives) and dismiss; a dismissed pair never re-proposes.
  - Contract, conformance and `fe-events` mirrors.
- Done when: an integration test with two sources delivering one event (title variant, same place and start) yields one published event plus one proposal; accepting merges the evidence; after a dismiss, a replay proposes nothing.
- Depends: V02

### V04 Custom field schemas per workflow
- Repo: `wow-two-sdk-beta.events` · Area: tracking · Type: feature
- Why: P2's first tracking row: workflow fields are free JSON (`WorkflowModel.Fields`, `WorkflowSpec.Fields`), so nothing validates tracking writes.
- Do:
  - Field schema per workflow: key, localized label, type (`text`, `number`, `date`, `select`, `url`), options, required.
  - Tracking writes validate against it and answer 400 with per-field errors; fields stored without a schema stay readable.
  - Console and `fe-events` render typed inputs; contract, conformance, migration.
- Done when: E2E: a tracking write with a wrong type answers 400 naming the field, a valid one round-trips, and a workflow with no schema behaves as today.
- Depends: —

### V05 Webhooks for published, changed, cancelled and deadline events
- Repo: `wow-two-sdk-beta.events` · Area: integrations · Type: feature
- Why: P2 integrations row: consumers learn about changes only by polling.
- Do:
  - Per organization `POST|GET|DELETE …/webhooks` (`events.admin`); events `event.published`, `event.changed`, `event.cancelled`, `deadline.approaching`.
  - An outbox written in the same transaction as the change; signed deliveries (HMAC-SHA256 over timestamp and body), retries with backoff, a delivery log.
  - `deadline.approaching` from a daily job at configurable lead days, once per event, deadline and lead.
- Done when: integration tests: a publish emits one `event.published` per subscription after commit and none on rollback, a receiver answering 500 gets retried, the signature verifies, and the deadline job emits once per event, deadline and lead.
- Depends: —

### V06 Calendar export with VTIMEZONE blocks
- Repo: `wow-two-sdk-beta.events` · Area: calendar · Type: fix
- Why: P2 tracking row: `events.ics` writes `TZID` with no `VTIMEZONE`, which strict clients reject.
- Do:
  - `packages/Module/Calendar/CalendarWriter.cs`: one `VTIMEZONE` per `TZID` used, with `STANDARD` / `DAYLIGHT` rules covering the exported range, from the IANA zone.
  - Tests in `tests/Events.Tests.Unit/Calendar/CalendarWriterTests.cs`.
- Done when: a unit test exporting `Asia/Tashkent` and `Europe/Paris` events finds exactly one `VTIMEZONE` per zone with the right offsets and transitions for the range; existing calendar tests pass.
- Depends: —

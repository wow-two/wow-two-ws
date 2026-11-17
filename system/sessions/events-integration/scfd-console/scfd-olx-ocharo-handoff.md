# SCFD commit preparation and Claude handoff

Prepared 2026-11-17. The user asked to prepare all completed work, hand SCFD/Ocharo completion to Claude, and
resume Haven after that work closes. This handoff does not authorize a new production rollout or AI feed promotion.
No commit or push was made during this preparation.
Updated with the Instagram lane's November 18 status and the user's clarified source-per-account and shared-feed
requirements. The latest source identity correction supersedes any earlier single shared Instagram source design.

## Start here

Take ownership of the SCFD working tree after reviewing its staged diff. Preserve the existing pipeline/gallery
work and the OLX/shared-AI patch. Finish the current Ocharo integration and its acceptance checks, reconcile its
tracks, and close that lane with exact commits, release/CI evidence and remaining explicit holds. Complete shared
subscription and processed-delivery acceptance before resuming Instagram acceptance or Haven.
Use the [integration coordinator](../events-integration.md), [SCFD tasks](../tasks/tasks-scfd.md) and existing
events-integration build chat for the current task decisions; this document transfers the Codex changes into that work.

Workspace: `/Users/max/Projects/10x-ws/workbench/career/engineering/wow-two/wow-two-ws`.
SCFD repo: `workbench/wow-two-sdk-beta/wow-two-sdk-beta.harvest`, branch `main`.
The original tested baseline was `695de44`. Current handoff HEAD is
`27cef5565a4ec8e14533b86f6db39725ee636404`, after Instagram post limits and private image storage.
All 58 staged SCFD paths remain present; no unstaged or untracked Harvest files were present at this check.
Recheck HEAD and the index before committing: the checkout is shared. Preparation is staged, not committed.

## Completed Instagram Posts-per-run and Files slice

The Instagram lane committed and pushed `81655d6..27cef55`. Local HEAD and the committed operator runbook confirm
the completed slice; its tests and live checks below are lane-reported evidence. Its temporary reservations on
`RunPlanner.cs`, `HarvestEngine.cs`, `HarvestConsole.ts` and `CreateHarvestClient.ts` are released.
Preserve the original staged AI changes when continuing shared work.

- **Posts per run** persists as `maxItems`; pagination is internal, with the correct item/page stop reason.
- Official-API images copy to private Files storage, up to twenty per post. Unchanged captures refresh expiring
  media references without a content revision or duplicate delivery; existing saved posts can recover missing copies.
- API-key and cookie consoles load images through the authenticated client and render view-owned blob URLs.
  Local acceptance covered all fifteen Fest photos plus the Store photo; authorized asset reads returned image
  bytes, anonymous reads returned 401, and photo fifteen rendered from a private blob in Chrome.
- The test Meta grant was renewed with the same permissions. Both Teplo sources then made one request, returned
  one unchanged post, zero new/failed posts, and stopped with `itemLimit`. Schedules remained off.
- Validation reported: 125 focused backend tests, 170 frontend tests, all six frontend gates and a clean source-host
  publish. These are not a claim that the entire backend suite was rerun for this commit.
- Acceptance used isolated local API/console/Files services. No DevQA or production configuration changed.
  Release/deployment status for `27cef55` is not established by this completion notice.
- Canonical media URLs remain source evidence. The source-post projection exposes private asset routes:
  AI and consumers needing durable image bytes must use authorized asset access rather than depend on expiring CDN URLs.

Remaining work is owned as recorded in SCFD `engineering/deployment/instagram.md`: shared Capture/cadence API/UI
and scheduled-run proof; S09 subscriptions across publishers; S14–S17 extraction/relevance and filtered
Events/Desk delivery; then Instagram DevQA end-to-end acceptance. Historical backfill remains deferred.

## Commit batches

| Repository | Prepared scope | Suggested commit |
|---|---|---|
| SCFD | Shared Process admission and evidence API, opt-in OLX v2 host/processor, console/client, regressions and runbook/track | `feat: added audited OLX processing through the shared AI SDK` |
| wow-two-ws | Dropdown conventions, AI publisher inventory, analysis refresh and this handoff | `docs: recorded SCFD handoff and shared dropdown conventions` |

The SCFD patch is one coordinated backend/client/console feature; committing those contracts together avoids an
intermediate broken consumer. [Exact SCFD path manifest](scfd-commit-paths.txt) identifies the reviewed batch.
The workspace batch is limited to:

- `conventions/development/frontend/core/lla/constructs/html/forms.md`
- `conventions/development/frontend/core/mla/components/forms/selectPicker.md`
- `docs/package-registries.md`
- `ideas/ai-layer-analysis.md`
- this handoff and `scfd-commit-paths.txt`

Do not sweep other dirt into either commit. Excluded lanes: AI queued eval/provider catalog/migration 004; FE SDK
notification docs; Haven intake/research edits; workspace repo-registry, feedback/toast conventions, planning tasks
and `ideas/10x-os-domains-analysis.md`. No secrets, private prompts or captured post text belong in these commits.

## Already committed: keep and build on it

- `5d75ebd`: staged collection engine, schedules and master controls.
- `fac5f69`: source controls and separate pipeline/stage/run views, step canvas/results, logs, inline schedule
  controls, source activity chart and capture/gallery presentation. Run now stays on the current page.
  Discovery traversal belongs to source registries; the console does not offer a Discover batch-size control.
- Capture records are source/registry-owned; consumer listing presentation belongs to Haven or another product.
  Gallery preview, overflow tile and lightbox are implemented; shared gallery/pipeline extraction remains backlog.
- `925d93a`, `77ee974`, `ccee7fd`, `e28e184`: newer Ocharo/SCFD compatibility, permission, Afisha crawl and
  review fixes are already in the baseline. Current dirty engine hunks preserve those changes.
- The FE SDK pin and peer floor are `0.0.51` at `a4c4a33` / `695de44`.
- `a81e309` adds the Instagram collector and persisted profile controls, released as `v0.2.12`.
  `5e15364` records its Phase 1 boundary and deferred history requirements in
  `engineering/deployment/instagram.md` and the Engine backlog. The Instagram lane reports healthy
  `harvest-dev` on that release plus a local real capture and repeat deduplication. Test Meta credentials remain
  local only; the release does not establish a configured dev connection, scheduled capture or production activation.
- `7649b9b` records the remaining Instagram Capture/cadence console task. The Instagram lane reports another
  completed local manual capture at 21:54 Tashkent on November 17: one provider request, one unchanged post,
  no duplicate. This is lane-reported manual-run evidence, not scheduled or processed-delivery acceptance.
- `8798687` commits and pushes the per-account source correction: Teplo Fest and Teplo Store have separate
  declared sources sharing provider transport and host pacing. Source **Pipelines** now owns manual Capture and
  saved limits; redundant availability text is removed. The IG lane reports local UI acceptance of both:
  Fest returned one unchanged post, Store saved one new post, each with one request/page and schedules off.
  Credentials remain local; no test token was deployed to DevQA or production.
  Released as [v0.2.13](https://github.com/wow-two-sdk-beta/wow-two-sdk-beta.harvest/releases/tag/v0.2.13)
  from `8798687`. Independently verified successful
  [image publishing](https://github.com/wow-two-sdk-beta/wow-two-sdk-beta.harvest/actions/runs/44137592047),
  [CodeQL](https://github.com/wow-two-sdk-beta/wow-two-sdk-beta.harvest/actions/runs/44137591039) and
  [published-image conformance](https://github.com/wow-two-sdk-beta/wow-two-sdk-beta.harvest/actions/runs/44138491704).
  Package publishing remained intentionally skipped/unarmed. Dev deployment is unverified: the workflow does not
  establish the target's running version. No test token was deployed.
- AI `d71898b` is already pushed and released as `be-v10.0.0-beta`; all five NuGet packages are public.
  [Publish run 44042733179](https://github.com/wow-two-sdk-beta/wow-two-sdk-beta.ai/actions/runs/44042733179)
  succeeded. A separate clean public-NuGet consumer restored all five, built and passed a smoke check.
  The trusted publisher is push-only. The AI repo's remaining dirty eval work was not released.

## What the staged SCFD feature does

- Composes shared AI only on the internal source host, behind `Harvest:Processing:Ai:Enabled` (default false).
  `rental-terms@2` interprets saved OLX descriptions using `IAiRunner`, versioned database prompts and a pinned
  provider/model route. The legacy v1 processor remains available.
- Checks source AI permission, processor readiness, route and prompt pin at queue admission and worker execution.
  Successful capture/configuration pairs are not repeated. Model/evidence failures require review and a new pin
  before automatic retry; failures before a model call remain eligible once configuration is fixed.
- Persists typed rental-term evidence separately from canonical facts and delivery schemas. A read-only
  `GET /api/posts/{postId}/processing?containerId=...&limit=50&sourceId=...` exposes authorized results.
  Optional source filtering happens before the limit so merged posts do not hide that source's history.
- Adds source AI permission, server processor labels, model/prompt readiness and processing evidence to the console.
  Clients lacking the optional results method, including the demo, omit the results panel.
- Review fixes protect evidence from a number/qualifier truncated at the 12,000-character input boundary,
  keep the source filter before the result limit, and align fallback processor labels with the backend.

Runbook: SCFD `engineering/development/olx-ai.md`. No Claude API key was supplied or live model call made in this
lane. Configure any needed key privately; keep prompt drafts and captured/model input text outside git.
The AI package reference no longer needs a local feed or `AiSdkVersion` override.

Compatibility: new backend record/interface members require compiled consumers to rebuild with the released
contracts. The FE results method is optional for older embedded clients. This patch has no new SCFD database
migration; enabling AI applies its own keyed `ai` migrations through the existing host migration procedure.
Managed activation still needs AI enable/route/provider/secret settings added to the deployment configuration.
Verify the released migration manifest includes the `ai` set before enabling it.

## Verification

The original `695de44` baseline plus the prepared feature was tested in an isolated full-tree copy, preserving
deployment fixtures, with public package pins. The counts below predate the Instagram commits through `27cef55`;
they are not a new combined-tree test claim.
Snapshot and logs are temporary: `/private/tmp/scfd-commit-prep.vpclhid6`. No ignored local configuration was copied.

| Check | Final outcome |
|---|---|
| Backend, SDK 10.0.300, public AI 10.0.0-beta | 974 passed, 0 failed |
| FE package / app tests, Node 24.11.0, pnpm 10.33.2, SDK 0.0.51 | 109 / 37 passed |
| FE typecheck, ESLint, Prettier, package/app production builds | passed |
| FE packed consumer | passed, 88 files and 3 exports |
| Live browser, deployed console, real provider, Ocharo end-to-end | not performed by this preparation |

For `8798687`, the Instagram lane reports aggregate **1,006 backend and 160 frontend tests passed**, final package
validation passed, and local real captures for both declared Teplo sources. These are that lane's verification
results, not a rerun by this handoff update. The committed Instagram release checks passed as linked above.
The shared AI feature remains staged and is not part of that released commit; deployed target verification and
end-to-end AI-filtered delivery acceptance remain open.

Backend command, from `engineering/codebase/harvest.backend-services`:

```sh
dotnet test SCFD.BackendServices.slnx -m:1 -p:BuildSpa=false --no-restore
```

Run restore first on a fresh checkout. The verification snapshot used a normal public package restore.
The final log is `backend-final-tests-2.log`, with eight TRX files in `final-results-2/`.
An earlier parallel run hit one robots regex timeout; the final serial run passed that unchanged test.
A source-filter parameter naming collision was fixed before this final pass. Vite still reports a non-fatal
main-chunk size warning. None of these local checks establishes a deployment or measured model accuracy.

Frontend commands, from `engineering/codebase/harvest.frontend-services` with the pinned Node/pnpm:

```sh
pnpm install --frozen-lockfile
pnpm test
pnpm typecheck
pnpm lint
pnpm format:check
pnpm build
pnpm check:package
```

## Finish Ocharo and close the lane

1. Review and commit the prepared feature under the repository's commit/release rules; verify CI before consuming
   newly published packages. Let CI create versions/tags. The old S35 instruction to push tags is superseded by
   the repository's CI-managed release rules.
2. Finish S36's tenant-private stage-editor permission path and a dedicated UI gate regression. The backend routes
   already enforce `pipelines:manage`, and this patch consumes `processorLabels`; the card still also requires
   operator access. S39 still needs the restricted-source `RequiresGrant` / `AwaitingSourceAccess` cleanup and
   the Settings wording "Harvested by stages". Those clean files were not silently changed during this prep.
3. Reconcile the already shipped Ocharo SCFD/Events/Identity/app changes against the current build lane. The
   coordinator #69 records releases and a started dev rollout, not overall acceptance. S18 needs actual approved
   ANONS/Uzexpocentre/CAEx provisioning/readback. Preserve the Craftfair challenge-detector hold.
4. Implement the shared feed and processed-delivery prerequisites below, then prove accepted, rejected and
   unresolved cases through SCFD → Events → Ocharo/Desk, including repeat delivery and restart.
   Include authorized intake, golden replay E28, dev smoke E29, correct tenant/cursor behavior and a user-visible
   accepted record. Healthy E00 polling with no new matching Afisha event is not transport failure.
   Verify Telegram digest delivery separately if that path is in the active rollout.
5. Finish S33 console acceptance on the intended dev target: root page, `/api/system/status`, deep-link refresh and
   operator sign-in. A local build and backend-only image do not satisfy this.
6. S14 is partial: shared host composition is available, but Ocharo's relevance processor, evaluation subject source
   and configured prompts/routes are separate. S15 must first run shadow with reviewed samples, recording accuracy,
   misses, invalid outputs, latency and priced cost. Keep current rule-based delivery while shadowing.
   S16 promotion still needs its explicit acceptance/approval gate. Do not repurpose the OLX prompt for Ocharo.
7. The user has clarified the Instagram requirement under decision #68: one feed across separately declared
   account sources and their pipelines, filtered to subscriber interests after AI analysis.
   Use that requirement for S09 rather than imposing
   subscriptions per publisher. The broader selector representation and any remaining E01/E02/S10/S11 decisions
   still need reconciliation with the coordinator; do not mark that entire design closed from the IG clarification.
   Other explicit holds may remain deferred with ownership stated; closing the active lane must not erase them.
8. Update tracks/backlogs with exact completion evidence, commits, CI/release links, deployed versions and open
   holds. Leave owned changes committed or deliberately handed over, preserve unrelated dirt, and report the
   Ocharo acceptance result. Do not begin the 700-source expansion or Haven in this completion pass.

## Shared delivery prerequisites for Instagram Phase 1

The user clarified this in the Instagram chat: Instagram is the reusable provider, and every publisher/account
has its own registry-declared source. Under the **Teplo Store** group, register both **Teplo Fest** (`@teplofest`) and
**Teplo Store** (`@teplostore_2022`) as separate sources. Collection sources and their pipelines remain independent
of subscriber interests: one broad Instagram subscription may receive relevant events across them after AI analysis.
Separate subscriptions per publisher are not required.

The Instagram lane committed the source identity, registry and UI correction (S25) in `8798687`; preserve it when
committing the staged AI feature. Source URLs resolve through the adapter declaration, and shared provider host
pacing is separate from username identity; both accounts reuse the provider reader. One `instagram.com` source row
is no longer the intended design. Legacy domain sources remain readable; a mixed-account legacy source must not
be renamed to one publisher without reconciling its historical provenance.
The user authorized test collection for both Teplo accounts, including the Store. Production credentials and
deployment activation remain separate. The Instagram lane completed the additional controls/media slice above;
Ocharo's shared S09 subscription and S14–S17 AI/delivery closure remain prerequisites for full consumer acceptance.

Verified code at `5e15364` plus the preserved staged feature:

- `packages/Abstractions/Delivery/SubscriptionDeclaration.cs` still requires one `PipelineId`.
  `packages/Module/Delivery/DeliveryEventWriter.cs` restricts first deliveries from a capture run to that pipeline.
  S09 must apply the declared multi-pipeline scope consistently to future captures and stored-post replay.
- `packages/Module/Posts/ModulePostBroker.cs` emits `post.new` / `post.changed` while saving capture results.
  `packages/Module/Engine/ProcessingStore.cs` persists separate AI results without emitting `post.extracted`.
  S14–S17 must connect completed extraction/relevance to consumer delivery before requested event filters run.
  Preserve raw capture facts and audit results separately; storing evidence alone does not finish this flow.
- Acceptance must cover accepted, rejected and unresolved AI outcomes through Events/Desk, with repeat and restart
  checks. Preserve existing live rules during shadow and the explicit AI-promotion/production approval boundaries.

Generic Capture/cadence console work remains a separate shared SCFD Phase 1 pipeline slice, outside the completed IG work:

- The generic pipeline screen shows Discover/Harvest/Process and omits Instagram's supported Capture operation.
  Instagram has neither the discovery catalog nor the Detail step required by Discover/Harvest, so those
  unavailable states are correct. Process uses saved captures; it does not fetch Instagram posts.
- Source **Pipelines → Capture now** and saved bounds are implemented in `8798687`.
  The engine accepts `kind=capture` schedules through ordinary pipeline updates; generic stage-settings API/UI
  support for Capture and its cadence remains open. Posts-per-run and private image loading are complete in
  `27cef55`; neither supplies the missing generic Capture schedule controls.
- Keep Capture/cadence alongside the remaining shared SCFD/Ocharo work; assign its implementation explicitly.
  Shared subscription and AI-filtered delivery closure still precede full consumer acceptance.
  Separate per-publisher subscriptions and historical backfill remain outside the Phase 1 prerequisites.
  The per-account source identity implementation is already committed; its release status is recorded above.

The Instagram lane can then configure its approved test connection privately on `harvest-dev`, verify the separate
Teplo account sources and enable their chosen schedules. It verifies scheduled
capture, deduplication and the full processed consumer flow. Keys, production activation and grant renewal remain
separate. The committed `engineering/deployment/instagram.md` is the owner of the Phase 1 acceptance procedure.

Historical provider backfill remains deferred in the Engine backlog, outside Phase 1. An admin enables it and
chooses the oldest publication date; initialize the cutoff to three calendar months before activation and persist
that fixed date. There is no hardcoded two-year or other duration ceiling. A separate service prioritizes feeds
and dispatches small background batches; durable checkpoints survive limits and restarts. AI owns event-date
extraction and recurrence. Existing subscription replay of saved posts is not historical provider collection.

Known follow-up: the scheduler currently advances `last_queued_at` for due work even when queue preflight rejects
it. This predates the new admission checks; it was left for a focused scheduler follow-up, with no change to
scheduling semantics during commit preparation.

After Claude closes the Ocharo lane, the Instagram lane resumes its Phase 1 acceptance and the Haven lane can
resume its SCFD feed rollout. For Haven, shared-AI classifier adoption follows as a separate consumer change with
its own accuracy/cost/latency comparison and rollout decision.

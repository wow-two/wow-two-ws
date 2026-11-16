# SCFD for Ocharo: remaining tasks

*Written 2026-11-16 from harvest `main` `2dd33d6` (`v0.2.6`) plus the uncommitted Codex tree (111 files modified, 66 untracked), the events-integration track (#1-#65), `scfd-console-analysis.md` and the Codex review.*

These tasks cover SCFD's own side: sources, harvesting, matching, delivery, the console and releases. The Events intake mapping and Ocharo's Events app belong to other lists. Where a task changes the `wow2.event.v1` wire, the Events repo adopts the change in its own work.

## Conventions for every task

- Paths:
  - `be/` = `engineering/codebase/harvest.backend-services/`
  - `fe/` = `engineering/codebase/harvest.frontend-services/`
  - Docs paths are relative to the repo root.
- Checks:
  - Backend: `dotnet test be/SCFD.BackendServices.slnx`. Run it inside `mcr.microsoft.com/dotnet/sdk:10.0.403` when the host SDK is older than `global.json`'s 10.0.400. Docker must be running for Testcontainers.
  - Frontend, from `fe/`: `pnpm typecheck && pnpm -r test && pnpm lint && pnpm format:check && pnpm check:package`.
- Public repo:
  - Code, docs and fixtures must hold no host addresses, IPs, tokens, phone numbers, emails or personal names. Replace fixture contacts with synthetic values.
  - The developer sets secrets in user-secrets or Wheelhouse. They never go in chat, code or `deploy.yml` defaults.
- Sourcing posture (#50, #63):
  - Internal tracking only. Nothing collected is republished.
  - Read with an identified user agent, inside `robots.txt`, on one paced connection per host. A challenge, block or rate limit pauses the source.
  - No logins, CAPTCHA solving or rotating proxy pools. A dedicated outgoing server per source is allowed.
- Git:
  - Commit subject: `{type}: {past-tense verb} {what}`, 50-70 characters, subject only.
  - Stage explicit paths and check `git diff --cached --name-only` before each commit.
  - Never `stash`, `reset --hard`, `checkout --`, `restore`, a worktree or a force push.
  - Before committing, check that `git var GIT_AUTHOR_IDENT` shows the personal identity.
- Releases:
  - Every push to `main` releases image `v0.2.N` and Wheelhouse deploys it to `harvest-dev` automatically.
  - After each push, wait for CI's release, then `git pull --ff-only`.
- Records:
  - Record each change in `engineering/planning/version-track/v0.2/v0.2.md`.
  - In the same commit, remove or adjust its row in `engineering/planning/backlog.md`.
  - Migrations go in the next free `be/packages/Module/Migrations/NNN-name/{Apply,Rollback}.sql`. Never edit an applied migration.
- Pull order across groups: S01-S07, S08-S09, S18, S10, S19, S20, S11-S13, S21-S26 and S27-S32. Take S14-S17 once the AI repo has released, and S33-S35 when a console target or package consumer is needed.

---

## Finish ChatGPT's work

### S01 Fix StoreBootTests and add ListingReplay to the solution
- Repo: wow-two-sdk-beta.harvest · Area: backend · Type: fix
- Why: one failing backend test blocks every commit, including Ocharo's Afisha changes in the same tree.
- Do:
  - `be/tests/Harvest.Tests.Integration/Store/StoreBootTests.cs:18`: append `"008-pipeline-stages"` to the expected list. `MigrationTests.cs` already lists 008.
  - Grep `be/tests` for other hard-coded lists that end at `"007-source-assets"` and align them.
  - Add `tools/ListingReplay/ListingReplay.csproj` to `be/SCFD.BackendServices.slnx` under a `/Tools/` folder. It is not packable by default (`Directory.Build.props:15`).
- Done when:
  - `dotnet test be/tests/Harvest.Tests.Integration` passes 59 of 59.
  - `dotnet build be/SCFD.BackendServices.slnx` builds ListingReplay with 0 warnings and 0 errors.
- Depends: —

### S02 Clear fe-harvest lint errors and Prettier drift
- Repo: wow-two-sdk-beta.harvest · Area: console · Type: fix
- Why: CI's `pnpm lint` gate fails (`publish-packages.yml:199`, `core-latest.yml:94`), so no console change can ship.
- Do:
  - `fe/packages/fe-harvest/src/admin/harvestConsole/PipelineStageCard.vue:49`: remove or use the unused `_id` and `_next`.
  - `PipelineFlow.vue:48`: replace the self-closing element with an explicit closing tag.
  - `fe/packages/fe-harvest/tests/HarvestConsole.test.ts:466`: change `let followup` to `const followup`.
  - In `fe/packages/fe-harvest`, run `pnpm exec prettier --write src tests`. It reformats `HarvestConsole.ts`, `contracts/index.ts`, `RegistrationEnums.ts`, `CreateHarvestClient.ts` and the test file.
  - Re-run the formatter after any later edit to `SourceHeader.vue`, `SourceIcon.vue` or `SourcePostsTab.vue`.
- Done when: the frontend check line exits 0 with 0 lint errors and 0 unformatted files.
- Depends: —

### S03 Move the rental-terms prompt out of the generic engine
- Repo: wow-two-sdk-beta.harvest · Area: backend · Type: engineering
- Why: Ocharo's relevance pass (S15) needs a pluggable Process step. Today `be/packages/Module/Engine/ProcessingStore.cs:115-133` hard-codes a Haven lease-terms prompt and calls `IChatClient` inside the NuGet engine package.
- Do:
  - Add `ICaptureProcessor` to `be/packages/Abstractions/Steps/`:
    - members: `string Key` and `Task<CaptureProcessResult> ProcessAsync(CaptureProcessInput, CancellationToken)`
    - the input carries the container, source, post, link, capture, and the saved reading's title, text, language and extras
  - Add `PipelineStageOptions.Processor` (default `saved-reading@1`). `RegistrationRules.cs`, near :162, allows it only on `Process`, up to 100 characters, and only for a registered key.
  - `ProcessingStore.ProcessAsync` resolves `GetKeyedService<ICaptureProcessor>(stage.Processor)` and keeps only the model-free `saved-reading@1` summary. Remove `Microsoft.Extensions.AI` from `be/packages/Module`.
  - Move the prompt and its verbatim-evidence check to `be/sources/Module/Marketplace/RentalTermsProcessor.cs` (key `rental-terms@1`), registered by `AddHarvestListingSources`. Until S14, it keeps using `PipelineStageConfiguration.cs`'s keyed client.
  - `GET /api/pipelines/{id}/stages` lists the available processor keys. `PipelineStageSettings.vue` offers them as a choice.
- Done when:
  - `grep -rn "IChatClient\|deposit" be/packages` finds nothing.
  - A new integration test runs `rental-terms@1` with a scripted `IChatClient` and stores only evidence-checked terms in `harvest_processing_results`.
  - All tiers pass.
- Depends: S01

### S04 Give each section one schedule path
- Repo: wow-two-sdk-beta.harvest · Area: backend · Type: fix
- Why: a section can run Settings' capture and the Pipelines page's discover and harvest stages at once, and both provisioners (`OcharoSourceProvisioner.cs:216`, `MarketplaceProvisioner.cs:240`) drop `Stage` when re-enabling schedules, so `ocharo setup --schedules` resets a tuned stage.
- Do:
  - `be/packages/Module/Registration/RegistrationRules.cs`, in the schedule loop near :155: refuse an enabled `Capture` row beside an enabled `Discover` or `Harvest` row. Message: "A section runs either capture or the discover and harvest stages." `Check` and `Process` combine with either path.
  - Copy `Stage = row.Stage` in both provisioners' `EnabledCadence`. `--schedules` never enables `Capture` on a pipeline whose stages are on.
  - `fe/.../SourceSettingsTab.vue`: when Discover or Harvest is on, replace the capture-interval control with "Harvested by stages" and a link to `/sources/:id/pipelines`. `saveSectionSchedule` in `HarvestConsole.ts` shows the server's refusal as a toast.
  - In `v0.2.md`, note that the Pipelines sidebar entry Codex added differs from #42's operator menu (Home, Sources, Subscribers, Access) and waits for the developer.
- Done when:
  - A unit test `ScheduleSet_ShouldRefuseCaptureBesideHarvestStages` passes.
  - An integration test proves `ocharo setup --schedules` keeps an existing stage's `BatchSize`.
  - A console test shows the stages notice on Settings.
- Depends: S01

### S05 Test stage validation, discoveries and the run audit
- Repo: wow-two-sdk-beta.harvest · Area: backend · Type: engineering
- Why: the staged engine every Ocharo pipeline now runs on has no dedicated tests for `DiscoveryStore`, `PipelineStages` validation or `GET /api/runs/{id}/audit`.
- Do:
  - Integration tests for `be/packages/Module/Engine/DiscoveryStore.cs`:
    - a repeated `external_key` raises `revision` and does not insert a second row
    - a gone detail sets `detail_state='gone'`
    - two pipelines share one discovery through `harvest_discovery_scopes`
  - Unit tests for the stage rules in `RegistrationRules.cs`:
    - `CatalogUrl` is refused
    - batch caps per kind
    - `TitleContains`, `PublishedSinceUtc` and `Model` are refused outside `Process`
  - E2E in `be/tests/Harvest.Tests.E2E` for `GET /api/runs/{id}/audit`:
    - one row per attempt, with HTTP status and retry time
    - a tenant caller gets 404 for another tenant's run
- Done when: the new tests pass by name in `dotnet test be/SCFD.BackendServices.slnx`.
- Depends: S03

### S06 Record Codex's work in the docs
- Repo: wow-two-sdk-beta.harvest · Area: docs · Type: engineering
- Why: `v0.2.md` stops at the 11-15 BirBir entry, and `contract.md` does not document the five new routes.
- Do:
  - In `engineering/planning/version-track/v0.2/v0.2.md`, add an iteration "Source stages and catalogs":
    - stages, migration 008, the Pipelines pages and the run audit
    - the server-side posts query with facets and paging
    - registry section catalogs, with no typed URL
    - Afisha harvested in Russian only
    - Joymee, `wow2.listing.v1`, ListingReplay and the "Active only" filter
    - the four decisions the developer reversed, each with his words from the Codex review
  - In `engineering/architecture/contract.md`, add these routes with their scopes and shapes:
    - `GET|PUT /api/pipelines/{id}/stages`
    - `GET /api/pipelines/{id}/discoveries`
    - `GET /api/runs/{id}/audit`
    - `POST /api/sources/{id}/posts/query`
  - Make the BirBir statements in `contract.md:269-272`, `engineering/deployment/deployment.md` and `v0.2.md` say what the code does: `MarketplaceSetup.cs:59` `AwaitingSourceAccess`.
  - Describe `Processor` (S03) in `deployment.md` § Source stages.
- Done when:
  - `grep -c "stages\|/audit\|discoveries\|posts/query" engineering/architecture/contract.md` finds all five routes.
  - No doc claims a BirBir grant gate the code lacks.
- Depends: S04, S05

### S07 Commit the work in slices and verify v0.2.7 on dev
- Repo: wow-two-sdk-beta.harvest · Area: release · Type: engineering
- Why: Codex's work is uncommitted and Codex may still be writing. Nothing for Ocharo ships until the tree is clean and released.
- Do:
  - Precondition: no file under `engineering/` has changed for 10 minutes, and no Codex session is open on the tree.
  - Scan the staged files for tokens, `+998` phone numbers, emails and IPs. `engineering/research/housing-listing-analysis-2026-11/` must hold aggregates only.
  - Commit one cohesive slice per commit:
    - the stage engine, migration 008, its routes and tests
    - the section catalogs in the readers
    - the server-side posts query and console paging
    - the listing model, BirBir, Joymee, OLX fields, the marketplace import, ListingReplay and the research
    - Afisha Russian-only and the registry JSON
    - the console Pipelines pages
    - the docs
  - Run `git pull --ff-only` and `git push`. CI releases `v0.2.7` and Wheelhouse deploys it to `harvest-dev`.
  - On dev, check by hand that Afisha's Uzbek passive pipelines from the old catalog stay paused. This is a manual step with no code (#52).
- Done when:
  - `gh release view v0.2.7 --repo wow-two-sdk-beta/wow-two-sdk-beta.harvest` succeeds.
  - `harvest-dev` reports `0.2.7` at `/api/system/status`, with migration history ending at `008-pipeline-stages`.
  - `ocharo status --group afisha` (Wheelhouse Run) still shows the 6-hour capture and daily check.
  - Events' `intake check` reads `subscription=ok` for `afisha-fashion` and `afisha-exhibitions`.
- Depends: S01, S02, S03, S04, S05, S06

## Matching and delivery

### S08 Carry Ocharo's filter key in the golden contract pages
- Repo: wow-two-sdk-beta.harvest · Area: backend · Type: fix
- Why: the golden `be/tests/Contract/wow2.event.v1/subscription.json` has no `filterKey`, while Events refuses a source whose subscription lacks its `Filter` and Ocharo's subscriptions carry `ocharo-fashion-v1`.
- Do:
  - `be/tests/Harvest.Tests.E2E/Contract/EventContractPagesTests.cs`: subscribe with `FilterKey = "ocharo-fashion-v1"` and context `catalog=ocharo-fashion`.
  - Add a case where a post the filter rejects never appears.
  - Regenerate `subscription.json`, the pages and `manifest.json` with each page's sha256.
  - In `v0.2.md`, note that Events must copy the folder again.
- Done when:
  - `jq -r .data.filterKey be/tests/Contract/wow2.event.v1/subscription.json` prints `ocharo-fashion-v1`.
  - The E2E tier passes with matching manifest hashes.
- Depends: S07

### S09 Let one subscription follow many sections
- Repo: wow-two-sdk-beta.harvest · Area: backend · Type: feature
- Why: a subscription follows one pipeline (`ck_harvest_subscriptions_channel`) and Events binds one intake source per subscription (`Events:Intake:Sources:N:SubscriptionId`), so each new Ocharo channel costs an Events deploy entry, while 100 sources need one cursor.
- Do:
  - Migration `009-subscription-sections`:
    - a table `harvest_subscription_pipelines(subscription_id, container_id, pipeline_id, added_at)` with primary key (subscription_id, pipeline_id)
    - kind check adds `sections`
    - `sections` requires a null `pipeline_id`
  - Contract: add `SubscriptionKind.Sections`, `SubscriptionDeclaration.PipelineIds` and `PUT /api/subscriptions/{id}/pipelines` with `{ add: [], remove: [] }` under scope `subscriptions:manage`, and document them in `contract.md`. A section added later delivers from then on.
  - `be/packages/Module/Delivery/DeliveryEventWriter.cs:17`: include `sections` subscriptions through the join table, with the same filter, lifecycle and `withinSection` rules as `channel`.
  - Implement the kind in Module, `Client` and `FakeDeliveryBroker`, with conformance tests in `be/packages/Testing`.
  - `OcharoSourceProvisioner.EnsureAsync` creates or reuses one `sections` subscription for tenant `ocharo`:
    - filter `ocharo-fashion-v1`, schema `wow2.event.v1`, context `catalog=ocharo-fashion`
    - it follows every provisioned pipeline, and `ocharo setup` prints its id
    - the two Afisha per-pipeline subscriptions Events reads stay as they are
- Done when:
  - Conformance `Sections_ShouldDeliverEveryFollowedPipelineOnOneCursor` passes against Module, Client and Fake.
  - Running `ocharo setup --group afisha --group anons` twice prints the same `sectionsSubscriptionId`.
- Depends: S07

### S10 Ocharo filter regression set over every reader's fixtures
- Repo: wow-two-sdk-beta.harvest · Area: backend · Type: engineering
- Why: Ocharo's catalog fills only from posts that `ocharo-fashion-v1` passes. New readers (S19-S26) must not let concerts in or drop fashion fairs unnoticed.
- Do:
  - New theory `be/tests/HarvestAdapters.Tests.Unit/Ocharo/OcharoFilterFixturesTests.cs`. It takes each event fixture of Afisha, Anons, Caex, Craftfair and Uzexpocentre through its reader, `RulesPostExtractor` and `OcharoFashionFilter.Matches`, and compares the result with `ocharo-filter-expectations.json` (fixture, expected verdict, reason).
  - Add trimmed fixtures where missing. Expected false: a concert found through Exhibitions, a comedy show under Concerts, a cancellation notice, an editorial fashion report. Expected true: TITF, Texworld, CAEx Baraka Friday, a Craft Fair call. The cases come from `scfd-console-analysis.md` § Event topics.
  - If CAEx captures carry `recordKind`, add `caex` to the editorial-article guard at `OcharoFashionFilter.cs:22`.
- Done when: `dotnet test be/tests/HarvestAdapters.Tests.Unit --filter OcharoFilterFixtures` passes at least 20 cases, and every event fixture is listed.
- Depends: S07

### S11 Emit item-level publisher categories as source tags
- Repo: wow-two-sdk-beta.harvest · Area: source reader · Type: feature
- Why: a section mislabels posts; Afisha's Exhibitions section lists a concert. The item's own category lets the filter, Events and the console tell fashion from concerts.
- Do:
  - `be/sources/Afisha/AfishaCaptureReader.cs`: take the category from the article path (`/ru/{category}/{yyyy}/{mm}/{dd}/{slug}`) or its breadcrumb, and emit `SourceTags` `afisha:{category}`.
  - `AnonsCaptureReader.cs`: emit the event card's category the same way.
  - Codex's read-time `ReadPostFilter` in `AfishaSourceAdapter.cs` reads the stored tag instead of re-parsing URLs.
  - `OcharoFashionFilter.cs`: a `fashion` tag counts as subject evidence, and a `concerts` or `theatre` tag alone never does.
  - After release, run `ocharo setup --group afisha --refresh` on dev by hand.
- Done when:
  - Afisha fixture tests assert `afisha:fashion` and `afisha:exhibitions`.
  - `07-afisha-place.json` is regenerated with `sourceTags`.
  - S10's set still passes.
- Depends: S10

### S12 Record each subscription's pull lag
- Repo: wow-two-sdk-beta.harvest · Area: backend · Type: feature
- Why: Home has no delivery data (#4), and nobody sees when Events stops pulling Ocharo's events.
- Do:
  - In the handler behind `GET /api/subscriptions/{id}/events` (`be/packages/Hosting/Delivery/Controllers/SubscriptionsController.cs:58`):
    - write `harvest_subscriptions.last_read_at` (it exists since `001-baseline` and nothing writes it)
    - store the decoded cursor position in a new column (next free migration)
  - `SubscriptionModel` gains `LastReadAtUtc`, `Pending` (events after the last read position) and `OldestPendingAtUtc`, returned by both subscription reads.
  - `be/sources/Module/Ocharo/OcharoStatus.cs`: the `ocharo status` line adds each subscription's `pending` and `lastReadAt` and stays under 500 characters.
- Done when:
  - An integration test shows `pending` at 0 after a pull, 1 after a new matching post, and `lastReadAtUtc` set.
  - `ocharo status` prints one JSON line under 500 characters.
- Depends: S09

### S13 Typed application deadlines in wow2.event.v1
- Repo: wow-two-sdk-beta.harvest · Area: backend · Type: feature
- Why: Ocharo applies to artisan fairs and trade shows by deadline. Craftfair (`CraftfairCaptureReader.cs:52-66`) and Afisha (`AfishaEventProjector.cs:211`) capture deadline evidence, but none reaches the wire (#18 P2).
- Do:
  - `be/packages/Module/Extraction/RulesPostExtractor.cs`: map reader evidence `applicationDeadline` to `PostDate { Role = Deadline }`, keeping precision and raw text. The call status (`open`, `closed` or `unknown`) becomes a typed field.
  - `EventSchemaMapper.cs` emits `deadlines: [{ kind: "application", value, precision, raw, status }]` only when stated.
  - Document it as additive in `contract.md` § `wow2.event.v1`.
  - Add golden page `09-deadline.json` and its manifest entry under `be/tests/Contract/wow2.event.v1/`.
- Done when:
  - A Craftfair fixture test reads a closed call's deadline with `status=closed`.
  - The contract pages regenerate with the new page and hashes.
- Depends: S08

### S14 Embed the shared AI layer in the source host
- Repo: wow-two-sdk-beta.harvest · Area: backend · Type: engineering
- Why: #54, #55 and #64 put Ocharo's relevance pass on Claude, with GPT as fallback, through `wow-two-sdk-beta.ai`. Harvest must call that layer instead of its own OpenAI client.
- Do:
  - Precondition: the AI repo has published its first `be-v*` NuGet release of `WoW2.Sdk.Beta.Be.Ai.{Abstractions,Providers,Module,Testing}`. It has no tags today.
  - Pin the packages in `be/Directory.Packages.props` and reference them only from `be/service/HarvestSources.Api/HarvestSources.Api.csproj`. Register `AddAiProviders(configuration)` and `AddAi()` in `HostConfiguration.cs`; the host's `migrate` verb applies the AI module's migrations.
  - Delete the `Harvest:Processing:OpenAi` client in `PipelineStageConfiguration.cs` and the `Microsoft.Extensions.AI.OpenAI` 10.8.3 pin. `RentalTermsProcessor` (S03) calls `IAiRunner` under use case `rental-terms`.
  - Implement `IEvalSubjectSource` for `harvest:post:{id}@{rev}` (title, text and language from that revision). A post purge clears what it served.
  - Add to `deploy.yml`:
    - `Ai:Providers:anthropic:Kind`, plus `ApiKey` as a secret
    - `Ai:Providers:openai:Kind`, plus `ApiKey` as a secret
    - `Ai:Routes:ocharo-relevance`, default `["anthropic/claude-haiku-5-5","openai/gpt-6-luna"]`
- Done when:
  - All tiers pass with `Ai.Testing`'s scripted client.
  - `dotnet HarvestSources.Api.dll config check` passes with no AI key set, and the host boots with AI unavailable.
- Depends: S03, S07

### S15 Run Ocharo relevance in shadow on Afisha
- Repo: wow-two-sdk-beta.harvest · Area: backend · Type: feature
- Why: #55's next step is to compare a model's verdicts with `ocharo-fashion-v1` on real Afisha posts for a week before switching anything (#54).
- Do:
  - Add `be/sources/Module/Ocharo/OcharoRelevanceProcessor.cs`, an `ICaptureProcessor` with key `ocharo-relevance@1`:
    - it calls `IAiRunner` with use case `ocharo-relevance` and input `{ title, text, language }`
    - the answer is `{ relevance: close|loose|none, kind, reason }`; prompt version 1 is seeded once
    - an invalid or unavailable answer stays undecided and retries
  - `ocharo setup --relevance-shadow` (`OcharoSetupVerb.cs`) sets the selected Afisha sources to `AiAllowed=true` and adds a Process stage: every 6 hours, batch 20, processor `ocharo-relevance@1`. The AI-posture conflicts at `OcharoSourceProvisioner.cs:90` and `:134` relax only under this flag.
  - Delivery stays on `ocharo-fashion-v1`, and no new events are delivered.
  - `ocharo relevance report [--since <date>]` prints counts only:
    - rules yes against model close, loose or none, and rules no against each
    - invalid answers
    - cost per post and p95 latency, read from the AI inference log
    - no post text
- Done when: an integration test with a scripted client passes:
  - verdicts are stored
  - a replay skips finished captures
  - a failure leaves the capture undecided
  - `harvest_subscription_event` gains no rows
  - the report verb prints one JSON line
- Depends: S14

### S16 Promote AI relevance into Ocharo's delivery
- Repo: wow-two-sdk-beta.harvest · Area: backend · Type: product
- Why: after the shadow week meets the agreed miss, cost and latency limits, the posts the model accepts and the rules miss must reach Ocharo with `classification`, which Events' `payload` classifier reads.
- Do:
  - On a verdict change, write `PostClassification` into the post's resolved envelope as a new revision (`post.changed`):
    - classifier `model:{model}@ocharo-relevance:{version}`
    - close becomes relevant 0.9, loose becomes relevant 0.6, none becomes irrelevant 0.9 (#54)
    - `kind` comes from the answer
  - New filter `be/sources/Module/Ocharo/OcharoRelevanceFilter.cs` with key `ocharo-relevance-v1`: it passes what the rules pass plus a `relevant` verdict at 0.5 or above.
  - `ocharo setup --relevance-live` creates a new `sections` subscription (S09) on that filter. The old ones stay until Events switches.
  - Gate: the developer approves after reading S15's report.
- Done when:
  - An integration test shows a rules-rejected, model-`close` post on the new subscription with `classification.verdict=relevant`, and not on the `ocharo-fashion-v1` one.
  - Turning the AI step off restores rules-only output.
- Depends: S15, S09

### S17 Estimate event dates from the AI pass
- Repo: wow-two-sdk-beta.harvest · Area: backend · Type: feature
- Why: undated posts cannot be placed on Ocharo's timeline; v0.2 entry 27 needs an estimated date.
- Do:
  - The S15 answer gains `starts`, `ends` and `evidence`. The evidence must appear verbatim in the input, checked the way rental terms are.
  - `be/packages/Abstractions/Extraction/PostDate.cs` gains `Certainty` (`stated` or `estimated`). A stated date always wins.
  - `EventSchemaMapper.cs` emits `starts.certainty` and `ends.certainty` (#18 P2).
  - Add the field to `contract.md` and a golden page `10-estimated.json`.
- Done when:
  - An integration test shows an undated post getting `starts.certainty=estimated`, then replaced by a later stated date.
  - The contract pages regenerate.
- Depends: S16

## Sources for Ocharo

### S18 Run ANONS, Craftfair, Uzexpocentre and CAEx for Ocharo
- Repo: wow-two-sdk-beta.harvest · Area: source reader · Type: product
- Why: only Afisha feeds Ocharo (`ocharo setup --group afisha` is the only setup run on dev); four compiled collectors in registry `harvest` mode have never run there (backlog: "Live event-source coverage").
- Do:
  - Locally, on the Compose stack: `dotnet HarvestSources.Api.dll ocharo setup --group anons --group hunarmand --group uzexpocentre --group caex --run`.
  - Review each run's dates, deadlines and closed calls against the page (`v0.1-sources.md` Iteration 1 boxes).
  - Fix what the review finds in `be/sources/{Anons,Craftfair,Uzexpocentre,Caex}`, each with a fixture test.
  - On `harvest-dev`, run the same verb with `--schedules` through Wheelhouse Run. The pipelines join S09's sections subscription.
  - Close the matching `v0.1-sources.md` boxes in `v0.2.md`.
- Done when:
  - `ocharo status --group anons --group hunarmand --group uzexpocentre --group caex` on dev lists every pipeline with a capture schedule.
  - Each latest run is `ok` or `partial/page_limit` with 0 failed.
  - The sections subscription holds at least 1 `wow2.event.v1` record from a source other than Afisha.
- Depends: S07, S09

### S19 Read trade-fair edition pages (TITF, Texworld, TFT Expo)
- Repo: wow-two-sdk-beta.harvest · Area: source reader · Type: feature
- Why: the fairs Ocharo sources from and exhibits at each publish an edition page, and none is read. TITF is the must-catch item for the first AI eval (#55).
- Do:
  - New reader `be/sources/Editions/` (`EditionPageCaptureReader`, `EditionPageSourceAdapter`, key `edition-page`, family `site`):
    - one capture per edition page
    - schema.org `Event` JSON-LD when present, otherwise the labelled date range, venue, city, edition name and year
    - visitor, exhibitor and buyer routes kept as links, never as admission facts
  - Registry `ocharo-event-sources.json`: switch these channels to `mode: harvest`, `adapterKey: edition-page`, `setup: selected`:
    - `iteca-uz/titf-programme`, `iteca-uz/textileexpo-programme`, `iteca-uz/caitme-programme`
    - `bmca-uz/primary`, `tft-expo/primary`, `catexpo/primary`
  - `OcharoSourceRegistry.cs`: add the profile, and give `CollectionProfile` a per-profile capture interval (weekly here) instead of the provisioner's fixed 6 hours.
  - Add fixtures of trimmed live markup with synthetic contacts under `be/tests/HarvestAdapters.Tests.Unit/Sources/Editions/`.
  - `iteca.uz/calendar` stays manual, since it served a browser challenge. A challenge on any microsite pauses only that source.
- Done when:
  - Unit tests parse each fixture into one event with start, end, venue and city.
  - `OcharoRegistryTests` passes.
  - A bounded local `ocharo setup --group iteca-uz --group bmca-uz --group tft-expo --group catexpo --run` captures at least 1 dated edition per reachable site.
  - S10 marks each edition `true`.
- Depends: S10

### S20 Keep one size of each Afisha picture
- Repo: wow-two-sdk-beta.harvest · Area: source reader · Type: fix
- Why: Afisha lists each picture twice (`..._l.webp` from `og:image`, `..._m.webp` in the page), so every Ocharo post sends duplicate media to Events and the console (v0.2 entry 21).
- Do:
  - In `Images` (`be/sources/Afisha/AfishaCaptureReader.cs:183`), group URLs by path without the `_l`, `_m` or `_s` size suffix. Keep the largest size, in first-appearance order.
  - Add a unit test over the existing Afisha fixtures.
  - After release, run `ocharo setup --group afisha --refresh` on dev by hand.
- Done when:
  - `dotnet test be/tests/HarvestAdapters.Tests.Unit --filter Afisha` passes with the new test.
  - A refreshed dev post's `imageUrls` holds no `_m` twin of an `_l` image.
- Depends: S07

### S21 Route registry channels to the generic readers
- Repo: wow-two-sdk-beta.harvest · Area: source reader · Type: feature
- Why: 6 of the registry's 188 channels are harvested, and channels with RSS, Atom, ICS, schema.org Event pages or a sitemap need only a route to the generic readers in `be/packages/Module/Readers/`, not a reader each (#51).
- Do:
  - `OcharoSourceRegistry.cs` `Profiles`: add `generic-feed`, `generic-structured` and `generic-site` with their family and check policy. `OcharoSourceProvisioner` registers them like the named readers.
  - By hand, with no new code (#52), probe each P1 `planned` channel with one paced GET inside `robots.txt`. Record in the channel's `note` which of RSS, ICS, JSON-LD Event or sitemap it offers, and update `reviewedOn`.
  - Switch the confirmed channels to `mode: harvest` with the generic `adapterKey` and `setup: selected`.
- Done when:
  - `OcharoRegistryTests` covers a generic route.
  - At least 1 channel moves to `harvest` with a passing fixture test.
  - Every P1 `planned` channel carries a probe note.
- Depends: S19

### S22 Read Hunarmand association calls
- Repo: wow-two-sdk-beta.harvest · Area: source reader · Type: feature
- Why: the national artisan association, rank 1 in the registry, posts calls with application windows. These are the opportunities Ocharo's artisan line applies to.
- Do:
  - New reader `be/sources/Hunarmand/` (key `hunarmand-uz`) for the `hunarmand/association-calls` channel: a news index, then each detail page. Keep the publication date and the close date apart; the text is in Uzbek.
  - Registry: set that channel to `mode: harvest` and `setup: selected`, and add its profile in `OcharoSourceRegistry.cs`.
  - The deadline lands as `DateRole.Deadline` (S13). Fixture contacts are synthetic.
- Done when:
  - Unit tests read one call with its publication date and deadline.
  - A bounded local run captures at least 1 call.
  - S10 marks a craft call `true`.
- Depends: S13

### S23 Read regional tourism news on gov.uz
- Repo: wow-two-sdk-beta.harvest · Area: source reader · Type: feature
- Why: five P1 regional authorities (Fergana, Khorezm, Bukhara, Samarkand, Namangan) announce atlas, adras and craft festivals on one platform, so one reader covers all five.
- Do:
  - New reader `be/sources/GovUz/` (key `gov-uz`): each region's news index, then article detail.
    - Event dates stay unresolved unless the text states them.
    - One `gov.uz` source holds each region as a section, grouped as "Regional authorities".
    - One paced connection serves the whole host.
  - Registry: set the five regional `primary` news-index channels to `mode: harvest` and `setup: selected`. `uz-tourism/primary` stays manual, since its index is empty.
- Done when:
  - Fixture tests pass for each regional layout.
  - A bounded local run over two regions captures at least 1 article each with `postedAt`.
  - S10 marks an atlas festival `true`.
- Depends: S21

### S24 Read public Telegram channels through t.me/s
- Repo: wow-two-sdk-beta.harvest · Area: source reader · Type: feature
- Why: 18 registry channels are on Telegram, and no publisher will add a bot (developer, 2026-11-16). The public web preview needs no account.
- Do:
  - New reader `be/sources/Telegram/` (`TelegramPreviewCaptureReader`, `TelegramSourceAdapter`, key `telegram-preview`, family `Telegram`):
    - fetch `https://t.me/s/{username}`, then page with `?before={id}`
    - one capture per message, keyed by (username, message id)
    - text, `postedAt` from the message time, and photos as media URLs; an edit becomes a revision
  - `be/packages/Module/Engine/RunPlanner.cs:196` `InScope`: map a `Telegram` source's handle `tg:{username}` to host `t.me` and path `/s/{username}`. Put the family-to-host map in one helper that S25 reuses.
  - Registry: switch the `manual-social` `t.me/s/*` channels that showed dated evidence to `mode: harvest`, `adapterKey: telegram-preview`, `setup: selected`.
  - No login, session, bot or proxy.
  - Pace: 1 request per 10 seconds, `MaxPages` 3. A 429 or a challenge pauses the source. `t.me/robots.txt` answered 404 on 2026-11-16, so the robots gate allows the fetch.
- Done when:
  - Unit tests over trimmed preview HTML, using a synthetic channel, read ids, times and an edit as a revision.
  - A bounded local run captures at least 1 dated post from one registry channel.
- Depends: S21

### S25 Fix Instagram paging and file each profile under its publisher
- Repo: wow-two-sdk-beta.harvest · Area: source reader · Type: fix
- Why: Teplo, Visa Fashion Week Tashkent and Human House post first-hand runway and market notices, but the reader stops after page 1 when Meta sends only a cursor, and all profiles share one source and the first publisher's group.
- Do:
  - `be/sources/Instagram/InstagramBusinessDiscoveryClient.cs:94-101`: continue on `paging.cursors.after` when `next` is absent, and stop when the cursor repeats.
  - Give each publisher its own source:
    - handle = username
    - `InstagramSourceAdapter.Serves` (:35) accepts any handle for family `Instagram`
    - S24's helper maps it to `https://www.instagram.com/{handle}/`
    - `OcharoSourceProvisioner` finds sources by family and handle, per channel
  - `ocharo setup` gains `--instagram`; `OcharoSetupVerb.cs:58` hard-codes `includeInstagram: false` today.
  - `deploy.yml` adds `HarvestInstagram:AccessToken` (secret), `ProfessionalAccountId`, `ApiVersion` and `AllowedUsernames:0..3`. The developer creates the SCFD-owned Business account and types the token in Wheelhouse.
- Done when:
  - A client test where page 1 carries only `cursors.after` reads page 2.
  - The `OcharoPipelineTests` fixture shows four Instagram sources in four groups.
  - `config check` passes with Instagram disabled.
- Depends: S24

### S26 Read iTicket and ShowGo event listings
- Repo: wow-two-sdk-beta.harvest · Area: source reader · Type: feature
- Why: ShowGo sold the Fashion Show Line runway tickets, and iTicket lists Tashkent's cultural events with prices. Both add admission and price facts to Ocharo's events.
- Do:
  - New readers `be/sources/ITicket/` (channel `iticket/primary`) and `be/sources/ShowGo/` (channel `showgo/primary`):
    - category cards, then event or offer pages
    - dates, venue, and price as `PostPrice` with currency
    - seller and runway access stay unknown
  - Registry: set both channels to `mode: harvest` and `setup: selected`, and add their profiles in `OcharoSourceRegistry.cs`.
  - An event seen on Afisha and on a ticket site merges into one post with two links. Add a test.
- Done when:
  - Fixture tests pass for each site.
  - Bounded local runs capture at least 1 dated event each.
  - The merge test passes.
- Depends: S21

## Console

### S27 Stop counting page-limit harvests as failures
- Repo: wow-two-sdk-beta.harvest · Area: console · Type: fix
- Why: Home and Activity count Afisha's normal page-limit harvests as failures (#51), so a real failure on an Ocharo source goes unnoticed.
- Do:
  - `fe/packages/fe-harvest/src/admin/harvestConsole/ConsoleFormat.ts:9` `isFailedRun`: a `partial` run whose `completionReason` is `page_limit` or `item_limit` is complete. Failed, interrupted and other partial runs still count.
  - `HomePanel.vue`: the failed count and its helper text follow the new rule.
  - Add a Delivery card on Home: each subscription's `pending` and `lastReadAtUtc` (S12), amber after two poll intervals without a read.
  - `SourceActivityTab.vue`: the "Needs attention" chip uses the same rule.
- Done when: `HarvestConsole.test.ts` passes these cases:
  - a `partial/page_limit` run is not in Needs attention
  - a `failed` run is
  - Home shows a pending count from the demo client
- Depends: S12

### S28 Let adapters declare each section's topic
- Repo: wow-two-sdk-beta.harvest · Area: backend · Type: engineering
- Why: the console guesses topics from section names (`PostGlyphs.ts:43-52`). v0.2 entry 16 asks adapters to declare them; the language is already declared through `Locale`.
- Do:
  - `SourceSectionDefinition` in `be/packages/Abstractions/Sources/ISourceSectionCatalog.cs` gains `Topic` (`fashion|exhibition|concert|theatre|event|listing|other`). `SourceScopeSchemas.Catalog` serializes it.
  - Every catalog adapter declares it: Afisha, Anons, Caex, Craftfair, Uzexpocentre, Domtut, Olx and Joymee.
  - `fe/.../SourceSections.ts` and `PostGlyphs.ts` read `topic`, and fall back to the name only for schemas saved before.
- Done when:
  - A unit test asserts topics on Afisha's three sections.
  - A console test shows the fashion glyph for a section named "Мода" with `topic: fashion`.
- Depends: S07

### S29 Show an event's place on cards and the post page
- Repo: wow-two-sdk-beta.harvest · Area: console · Type: feature
- Why: Ocharo's reviewers need the venue and city at a glance. The list read carries no place, and the post page shows none for events (backlog: "Post card place line").
- Do:
  - `be/packages/Abstractions/Sources/SourcePostModel.cs` gains `Place { Venue, City }`, built from the stored envelope's `location.mentions`.
    - Fill it in `ModuleSourceOverviewBroker.cs` and `FakeSourceOverviewBroker.cs`, with conformance tests.
    - The city comes only from a `city` mention.
  - Show `venue · city` behind a pin glyph in the `SourcePostsTab.vue` card footer and Rows details.
  - `PostPanel.vue` gains a Place section for events.
  - Add `place` to the key list in `SourceConsoleEndpointTests`.
- Done when:
  - Conformance and E2E pass.
  - A console test shows "Дворец творчества молодёжи · Ташкент" on the Afisha card.
- Depends: S07

### S30 Event timing and an event-date sort for every source
- Repo: wow-two-sdk-beta.harvest · Area: console · Type: feature
- Why: only Afisha offers Upcoming, Ongoing and Finished (`AfishaSourceAdapter.ReadPostFilter`), and posts sort by harvest time, so the new event sources (S18-S26) get neither the timing filter nor a sort by event date.
- Do:
  - Move the event-timing facet into the engine's posts query for every `PostKind.Event` post. The time zone comes from the adapter, default `Asia/Tashkent`.
  - `SourcePostQuery.Sort` takes one of two values, and the cursor carries the sort:
    - `newest`: by `postedAt`, then first seen
    - `eventDate`: ongoing posts by soonest end, then upcoming by soonest start, then undated posts above the upcoming block by newest posted (the developer's lean, v0.2 entry 27), then finished posts by latest end
  - Add a sort control beside Cards and Rows. Choosing the timing filter switches the sort to `eventDate`.
- Done when:
  - An integration test orders 6 fixed posts correctly under both sorts across two pages.
  - A console test switches the sort and keeps the facets.
- Depends: S07

### S31 Give Ocharo a client view with Sources and Following
- Repo: wow-two-sdk-beta.harvest · Area: console · Type: feature
- Why: under #32, #33 and #58, Ocharo's people sign in as a client, pick the sections Ocharo follows and read the matched posts, and no operator chooses for them.
- Do:
  - `fe/apps/web/src/presentation/shell/ConsoleDestinations.ts`, `ConsoleNav.vue` and `Routes.ts`: a tenant caller gets Sources and Following, never Access or Subscribers. `CallerResolver` already maps an organization to a tenant.
  - Following lists the tenant's `sections` subscription (S09), with follow and unfollow per section through `PUT /api/subscriptions/{id}/pipelines`.
  - A followed source's Posts tab:
    - shows matched posts by default, with a `Matched | All` switch
    - dims unmatched posts with the reason (#47)
    - keeps the other filters behind an expandable panel (#52)
  - Reference: the wow-two-ws mocks at `system/sessions/events-integration/scfd-console/mocks/iter-2/`.
- Done when:
  - Console tests pass for the client menu and for follow and unfollow.
  - Locally, an account mapped to tenant `ocharo` sees only Sources and Following.
  - The owner, editor and viewer roles behave as `v0.1-sources.md` Iteration 4 lists.
- Depends: S09

### S32 Let an operator grant a restricted source
- Repo: wow-two-sdk-beta.harvest · Area: backend · Type: feature
- Why: a `restricted` source keeps its sections pending and nothing can grant it (#51). This blocks registry sources whose terms ask for permission.
- Do:
  - `be/packages/Abstractions/Sources/SourceUpdate.cs` gains `Permission` (`granted|denied|restricted`) and a required `Reason`, operator-only under `sources:manage`. Store the reason in a new nullable `harvest_sources.permission_reason` (next free migration).
  - `PUT /api/sources/{id}` accepts it. `SourceSettingsTab.vue` gets a Permission row that shows the reason.
  - A grant turns on the schedules of the source's pending pipelines as registered.
  - Implement it in Module, Client and Fake, with conformance tests.
- Done when:
  - Conformance `Grant_ShouldScheduleARestrictedSourcesSections` passes.
  - A tenant caller gets 403.
- Depends: S07

## Release

### S33 Serve the console on harvest-dev
- Repo: wow-two-sdk-beta.harvest · Area: release · Type: engineering
- Why: Ocharo's operator and client views (S31) run only on a local stack. `deploy.yml` routes `sites.app.paths: [/api]`, and the image builds no console.
- Do:
  - Build the console into the image: a Node stage in `engineering/deployment/Dockerfile` runs `pnpm --filter web build` into `HarvestSources.Api/wwwroot`.
  - `deploy.yml`: site `app` paths `[/, /api]`.
  - Add these keys to `deploy.yml`:
    - `Harvest:Console:IsIdentityEnabled`
    - `Harvest:Console:OperatorSubjectIds:0`
    - `Harvest:Console:OrganizationTenants:*`
    - `Identity:Client:ClientId`
    - `Identity:Client:ClientSecret` (secret)
    - `DataProtection:KeysPath`, with a `keys` volume
  - Deep links such as `/sources/:id/posts/:postId` fall back to `index.html`, and `/api/*` never does (the iteration-1 bug).
  - Precondition, outside this repo: Ocharo's Identity registers a confidential console client with callback `{origin}/api/identity/callback`.
- Done when:
  - On `harvest-dev`, `/` and `/api/system/status` answer 200.
  - A deep link reloads.
  - The developer's sign-in reaches the operator view.
- Depends: S07

### S34 Drop IP-lease pools and CAPTCHA solving from the image
- Repo: wow-two-sdk-beta.harvest · Area: release · Type: engineering
- Why: #50 and #63 allow a dedicated outgoing server per source, but not rotating pools or bypassing challenges. The public image still ships both, switched off.
- Do:
  - Remove the IP-lease route (`be/sources/Integrations/Proxy/IpLeaseBrokerOptions.cs` and its `Routing/` use) and `Captcha/`, with their tests (`IntegrationFetchLeaseTests.cs`, `TwoCaptchaSolverTests.cs`).
  - Remove the OLX residential-pool keys (`HarvestIntegrations:OlxProxy:*`, `OlxProxyProfile`, `Captcha:*`) from `deploy.yml`, `docker-compose.yml` and `.env.example`.
  - Keep the fixed-proxy route per exact host and its tests.
  - Update `be/sources/Integrations/integrations.md` and `engineering/research/integration-providers.md`.
- Done when:
  - `grep -rniE "captcha|iplease" engineering --include=*.cs --include=*.yml` finds nothing.
  - All tiers and `config check` pass.
- Depends: S07

### S35 Publish the Harvest NuGet and npm family
- Repo: wow-two-sdk-beta.harvest · Area: release · Type: engineering
- Why: Events still parses SCFD's wire with its own reader (#43). A published `Harvest.Client` and `Harvest.Testing` would let Events and Ocharo test against SCFD's own contract.
- Do:
  - Set the repo variable `PUBLISH_PACKAGES`.
  - Developer steps:
    - add nuget.org trusted publishing for `publish-packages.yml` (passkey)
    - make the first npm publish of `@wow-two-beta/fe-harvest` (2FA), per `engineering/development/development.md:31`
  - Push tags `be-v*` and `fe-v*`. Never commit a version.
  - Record the published versions in `v0.2.md` and `engineering/architecture/package-registry.md`.
- Done when: `WoW2.Sdk.Beta.Be.Harvest.Client` resolves on nuget.org, and `@wow-two-beta/fe-harvest` on npm, at the tagged versions.
- Depends: S09

# Events integration

*Last updated: 2026-11-10*

WoW2's events server (Events, the new domain repo `wow-two-sdk-beta.events`) runs with Ocharo's Identity, takes SCFD's
Afisha records into review and serves Ocharo Desk's Events page, deployed by Wheelhouse. This is the goal's cross-lane
track: vectors, lanes, order, contracts, decisions and done-when. The orchestrator chat writes it; each lane keeps its
own backlog and version track in its own repos, and never edits this file.

Sources: [the Events spec](../../../ideas/events-service-spec.md) (2026-10-27, written before pull delivery),
`ideas/events-infrastructure-next.md` (the 2026-11-05 review: pull consumer, Desk migration, operating controls;
uncommitted, another chat's), [the Files track](../../../workbench/wow-two-sdk-beta/wow-two-sdk-beta.files/engineering/planning/files-integration.md)
(the pattern: #29 issuer, #32 registration split), [api-communication](../../../conventions/development/backend/dotnet/core/hla/api-communication.md)
(the settled auth rules), [capability forms](../../../conventions/development/capability-forms.md), `ocharo-ws`
`docs/app-boundaries.md` (E1).

## Status

- ✅ M1 analysis (#12): four lanes started 2026-11-10; each verified its snapshot slice first (#34)
  - ✅ events #34, 2026-11-10: the slice holds; `workbench/wow-two-sdk-beta/*` has commit and push ON, so repo creation runs; the `catalog.yml` `events` row's `purpose` line carries #39's uncommitted SCFD hunk (`:272`), so the lane's #41 hunk comes with context against `HEAD`
  - ✅ scfd #34, 2026-11-10, read-only (#39 hold kept): harvest's tags reach `v0.1.9` (`bc0c8ac`) on GitHub, unfetched locally; `d77daf6` (harvest) and `18b083a`, `1b58b9d` (adapters) are local only, unpushed and unreleased; harvest's NuGet family `WoW2.Sdk.Beta.Be.Harvest.*` and npm `@wow-two-beta/fe-harvest` were never published (#43); the registry keeps colon scopes (`events:read`) and `CallerResolver` maps a token's dot names onto them, so Ocharo's Identity would carry `events.read` (#16); `api/subscriptions` needs `subscriptions:manage`, `…/{id}` and `…/{id}/events` need `events:read` (#15); mapper audit 7 yes, 15 partial, 11 no of 33 fields (`scfd-mapper-audit.md`, #18); the adapters pin be sdk `10.0.106-beta` and build harvest from source
  - ✅ platform #34, 2026-11-10, read-only: dev's `events.showcase_events` exists (`008-events` applied) with 0 rows; local Desk on the Mac holds all 68 rows, 1 organization `Ocharo`, from 3 bundle imports (2026-10-08, 10-13, 10-30), none edited in Desk; stages 64 candidate, 1 applying, 3 skipped; precision day 35, month 5, estimated 18 (all first-of-month), unknown 10; titles Latin-script, mostly English, none Uzbek-only; notes on all 68, source URL 51, website 46, deadline 9; the source bundles are not under `~/Projects`; Desk's own bundle is `ocharo.events-import.v1`; `EventImportService` skips existing keys at `:35`; `b2cb4e3` sits one commit past `v0.2.9`, untagged; the lane opens v0.3 for this work (#44)
  - ✅ wheelhouse #34, 2026-11-10: Wheelhouse `v0.14.9` runs, tree clean; every product's dev target (`ocharo-dev`, `files-dev`) sits in the prod console, which holds no Events, SCFD or SCFD Adapters product; the adapters image builds `HarvestSources.Api` from adapters source plus public SCFD at `bc0c8ac` (`v0.1.9`), one container with its own database, so Afisha records exist only on product `harvestadapters` (#45); private release reads work through the GitHub App, but a private image pull needs the control host's classic `read:packages` token file, and no product has pulled a private image yet (#46); released SCFD bundles (harvest `v0.1.9`, adapters `v0.1.1`) predate service access, so #13 (a) needs new SCFD releases, behind #39; Wheelhouse imports a product only from a catalog entry with `deploy: wheelhouse`, a repository, and a slug equal to the bundle prefix: `wow-two-ws` `2f7b151` added `harvestadapters` (#41); `events` gets `deploy: wheelhouse` with the events lane's #41 hunk
- 🔄 M2 build (#13)
- ✅ #39 answered by the developer, 2026-11-10: "no chat is working in scfd so commit is yours"; the scfd lane commits the SCFD repos' work, and the orchestrator committed the hub's SCFD hunks (`wow-two-ws` `98c4c1e`)
- ✅ events repo `wow-two-sdk-beta/wow-two-sdk-beta.events` created and scaffolded (`fccf9ad`), private as `create-library` leaves it; be sdk pinned `10.0.111-beta` (the template's pin failed restore on NU1902), fe `0.0.32` as FSS; hub hunks committed (`wow-two-ws` `5ba6ccb`, `events` `deploy: wheelhouse`, ports 8410–8414)
- ✅ The developer made `wow-two-sdk-beta.events` public, 2026-11-10 (checked: `PUBLIC`, description "an internal event catalog fed by SCFD…"), unblocking its `main-guard` ruleset, npm provenance and the registries
- ✅ platform: the export reshaped onto Events' `wow2.events-import.v1` (`ocharo-platform` `2495a08`, on origin): 68 rows, 68 unique `legacyId`s, 35 day values, 23 `yyyy-MM` month values (18 estimated), 10 unknown, no end before its start, `tracking` and `recordedAtUtc` equal to the rows, `legacy` complete; 142 unit and 180 E2E tests pass. Desk's create maps to `POST …/candidates`; old fact `PUT`/`DELETE` answer 410 `EventsMoved`; the import runs through Desk as an Ocharo admin after `PUT workflow`, dry run first
- ✅ scfd M2: harvest `ffccfa6` (the `harvest.*` scopes, client credentials, organizer, `postedAt`, mapping stamp, capture, `pipelineId`; 442 backend tests) and adapters `b4193c2` (re-pinned to `ffccfa6`, be sdk `10.0.111`) on origin, checked; adapters `v0.1.3` being cut. Provisioning is the host verb `dotnet HarvestSources.Api.dll ocharo setup --group afisha [--run]` in adapters `v0.1.4`, run through Wheelhouse Run: idempotent tenant `ocharo`, container `ocharo-events`, one pipeline and subscription per Afisha channel (fashion, exhibitions), so Events pulls 2 subscriptions; no operator secret on `harvestadapters-dev`; `--run` queues one bounded capture per pipeline, the Afisha acceptance sample
- ✅ Developer approval, 2026-11-10 ("yes of course"): the events lane adds nuget.org's trusted-publishing policy for `wow-two-sdk-beta.events` (owner `wow-two-sdk-beta`, workflow `publish-packages.yml`, packages `WoW2.Sdk.Beta.Be.Events.*`) in the `wow2` profile, the developer tapping the passkey; it unblocks `PUBLISH_PACKAGES` and the Client NuGet Desk needs. The npm first version (2FA) follows as a Warp step once `fe-events` is built. Events' `main-guard` ruleset is active; image `v0.1.0` is the template sample, so `events-dev` waits for the M2 image
- ✅ wheelhouse: client 10's three keys typed on `ocharo-dev` (platform pushes client 10 next); the owner link pushed as Wheelhouse `32352f2` (54 settings E2E, 34 migration and 385 frontend tests pass), shipping as `v0.15.0`; automation deployed adapters `v0.1.3` (the `harvest.*` dot scopes) to `harvestadapters-dev`, dev check passed. Events' keys are typed in its M2 release's deploy dialog. Events reads both Afisha subscriptions as sources `afisha-fashion` and `afisha-exhibitions` (`ffb7411`), source 1 taking source 0's endpoint and client with `from`
- ✅ scfd M2 released (checked): harvest `v0.1.11` (`ffccfa6`: #16, #18, #19, client credentials), adapters `v0.1.3` (`b4193c2`, the first to accept `harvest.events-read`); adapters `1954d35` building as `v0.1.4` with the `ocharo setup` verb (13 E2E tests). #50 done: GitHub descriptions now read "SCFD (Source Collection and Feed Delivery): … pull delivery to subscribing products" and "SCFD Adapters: private source readers that collect public event listings for internal tracking (Ocharo); nothing is republished"; adapters `product.md` § Use and harvest `product.md` § Source posture carry the rule; no CAPTCHA, proxy or session provider configured. Closing checks for #13 (a), run by Events' status verb on `events-dev`: subscription read 200 with at least 1 record, `GET /api/tenants` 403, another tenant's subscription 404 (hidden on purpose). SCFD's be-v NuGet publish is deferred, since Events P1 needs no package
- ✅ platform: client 10 `events-console` live on `ocharo-dev` (`ab99164`, `v0.3.3`, CI green incl. Deployment composition; identity, desk and jobs healthy ~07:19Z, 0 ERR/FTL lines): a code-flow request with its typed callback answers 302 to `/sign-in`, an unknown client 400. Platform now waits only on Events' first Client release
- ✅ wheelhouse, 2026-11-10: Wheelhouse prod console on `v0.15.0` (owner links), promoted 12:22 local; adapters `v0.1.4` on `harvestadapters-dev`, dev check passed; `ocharo setup --group afisha --run` exit 0 in 7 s (Wheelhouse Run job `76a1956e`): tenant `01a1c45b-3e9f-72a5-be66-7244f2f02489`, fashion subscription `01a1c45b-4609-760a-a7b7-52f3cb4334ef` (pipeline `01a1c45b-448c-…`), exhibitions subscription `01a1c45b-4655-7191-8e9f-da7becd0a65b` (pipeline `01a1c45b-464b-…`), one capture queued per pipeline; `ClientGrantsJson` holds `harvest-operator` plus `events` → that tenant; both subscription ids kept for Events' deploy dialog. Platform `v0.3.2` had stopped at Identity's config check, since client 10's typed keys arrived before its `ClientId`; `v0.3.3` fixed it
- ✅ events M2 build pushed (`fccf9ad..65459ad`, checked on origin; image run in progress): backend E2E 38, unit 45, integration 66, conformance 108, migrations 4; fe-events 42, console 15; #13 (d)'s tests pass by name: `Intake_ShouldStoreEachDeliveryOnce_WhenAPageIsReplayed`, `Intake_ShouldKeepTheHighestRevision_WhenRevisionsArriveOutOfOrder`, `Intake_ShouldCommitNothing_WhenItCrashesBeforeTheCursorCommit` and `…ResumeFromTheCommittedCursor_AfterACrash`, `Intake_ShouldQuarantineAMalformedRecord_WithoutBlockingThePage`, `GetAsync_ShouldNotFindTheCatalog_WhenAnotherOrganizationReadsAPrivateCatalog`, `ListAsync_ShouldNotShowAnotherOrganizationsTracking_WhenTwoOrganizationsTrackOneEvent` (lane's local run; CI to confirm). New deploy keys: volume `keys`, `DataProtection:*`; the `intake check` verb prints SCFD statuses only. npm `fe-events-0.0.1.tgz` built (61 files, exports `./contracts`, `./kit`, `./admin`), first publish is the developer's 2FA step
- ✅ scfd Afisha acceptance on `harvestadapters-dev` (read-only): both runs `partial / page_limit` within the 5-page budget, 0 failed; fashion discovered 23, captured 4; exhibitions 26, 4; 8 posts, 2 of them events. The fashion subscription holds 1 `wow2.event.v1` record ("Показ мод The Fashion Show Line 2026", starts `2026-11-21T17:00+05:00`, `postedAt` `2026-10-14`, place with geo, 1 offer, mapping stamp, capture, organizer null); exhibitions holds 0, its one event past and filtered out. Contract fix underway: enums inside the mapped event become camelCase strings (harvest `v0.1.12`, adapters `v0.1.5`). Client 7's secret checked unchanged (vault history: one version, the developer's Files save; the "1 second ago" came from a stale console tab). The cross-tenant check needs a second tenant on `harvestadapters-dev`, asked of scfd
- ✅ (was blocked ~07:15Z, the developer confirmed `wow2` signed in) the `wow2` Chrome profile's Claude extension dropped off, holding Wheelhouse's confirmation of the `v0.15.0` prod promotion, the secret links and SCFD's setup run; the events lane will not submit the nuget.org policy on a relayed yes, so the developer fills it or says "go" in the events lane's chat
- All four lanes' turns ended on a network error (ENOTFOUND) around 11:00 local; each was resumed with its open items once the API answered again
- ✅ M1 picks, 2026-11-10: every contract #14–#33 and #43 carries a pick in the Contracts table; events (backlog § Integration picks, `product/product.md`), platform (`ocharo-platform` `94fd5a7`), wheelhouse (`b4cae16`); scfd writes its backlog rows with its first commits after #39. Open between lanes: #49. No developer decision came out of M1
- 🔄 M2 build: events builds contract first; scfd commits #39's work, then the #47 release order; platform builds `export events` and the dry run; wheelhouse builds the cross-product owner link
  - ✅ platform: Desk verb `export events` (`ocharo-platform` `866b097`, on `origin/main`); the local dry run writes 68 of 68 rows to `wow2.events-import.v1` (68 unique source ids, 18 estimated → month + estimated, 5 month, 10 undated, tracking and provenance equal to the rows); 141 unit and 180 E2E tests pass (platform lane); the draft shape `EventExportBundle.cs` went to the events lane for #26
  - ✅ wheelhouse #46: the private adapters image pulls ("Registry access: Passed, GHCR images read with the token file"); `harvestadapters` imported from the catalog, environment `harvestadapters-dev` on the Ocharo host with site `app`; readiness passes for `v0.1.1` but the database string, which placement fills; nothing deployed until an adapters release carries service access (#47)
  - ✅ scfd, 2026-11-10: #39's work reviewed, committed and pushed with the lane's fixes; harvest `origin/main` `a608d01` (`d77daf6`, `c1e68a0` rename, `49c6f79` browser sign-in beside service access, `864dc6e` tag filters, `00d0987` shellcheck), 436 backend and 35 frontend tests pass; adapters `origin/main` `6d4f391` (`18b083a`, `1b58b9d`, `a28f840`, `ea12e67`, `6d4f391` re-pinning `publicHarvestRef` to `864dc6e`), 214 tests pass; both backlogs cite `events-integration #N`; harvest v0.1 iteration 12 and adapters v0.1 iteration 7 record it (#42). The image run on `6d4f391` carries `Harvest:ServiceAccess:*` but not yet the `harvest.*` scope names, so it can prove health; Events' 200/403 check waits on the M2 release
  - ✅ wheelhouse, 2026-11-10: typed on `ocharo-dev` (saved, not applied) resource 3's `Uri` and `SignalUrl` (the `events-dev` `app` site) and resource 4's `Uri` (the `harvestadapters-dev` `app` site), the same strings as Events' and SCFD's audiences; `events-dev` and `harvestadapters-dev` with their databases are ready, each deploy waiting on its release. Until platform's set lands, an `ocharo-dev` deploy would fail on resources without `Name` (`OidcServerOptionsValidator.cs:92`), so platform pushes now without client 10 `events-console`, whose redirect, sign-out and signal keys wait on the events lane's paths
  - ✅ platform: registrations released as `ocharo-platform` `v0.3.1` (`34f08dc`, image run green, checked): resources 3 `events` and 4 `harvest`, clients 8 `events` and 9 `harvest-operator` with generated secrets, Desk's exchange grant, the `events:*` roles; client 10 left out. `v0.3.1` auto-deployed to `ocharo-dev`: Identity and Desk healthy at 05:43Z, Identity started with no validator refusal, the rendered target carries resources 3 and 4 and clients 8 and 9 with generated secrets (platform lane); wheelhouse links clients 8 and 9's secrets to `events-dev` and `harvestadapters-dev` next
  - ✅ wheelhouse read-back: automation deployed `v0.3.1` at 10:42 local; Identity's config check passed, boot validated, health 200, the discovery issuer keeps its slash and publishes the 5 `events.*` and 11 `harvest.*` scopes; 10 of 10 services healthy, 7 of 7 sites 200. The `v0.3.0` deploy at 10:37 had stopped at Identity's config check (30 findings), since the typed `Uri`s arrived before their names; no service restarted. Secret links wait on Wheelhouse's owner link (`v0.15` iteration 1): client 8 → `events-dev`; client 9's home follows SCFD's provisioning verb, since SCFD itself needs only issuer, audience and grants
  - ✅ events, 2026-11-10 (`75938db`, local until the first image is ready; GitHub description set): client 10 `events-console` paths relative to resource 3's `Uri`: redirect `api/identity/callback`, post-sign-out the site root, client `SignalUrl` `api/identity/signal`; members propose candidates through `POST api/events/v1/catalogs/{c}/candidates` (`events.track` + `events:track`, owner organization only, published only on a reviewer's accept), so Desk's create maps there and needs no 410; the #26 schema lives in the events repo's `engineering/architecture/contract.md` § Imports (`legacyId`, `facts.*`, month values `yyyy-MM`, no organization in the bundle, the workflow `PUT` first, run as an Ocharo admin through Desk's exchange); `deploy.yml` keys `Events:Auth:*`, `Events:Console:*`, `Events:Intake:Sources:0:*`, intake off until `BaseUrl` and `SubscriptionId` are typed; intake never copies sourced media (#50). Order for client 10: wheelhouse types its 3 keys, then platform pushes it
  - ✅ wheelhouse: SCFD Adapters `v0.1.2` (`6d4f391`) runs on `harvestadapters-dev`, deploy `e706dba0` at 10:52 local: the private image pulled, migrations 0 → 5, config check consistent, healthy; outside, `/api/system/status` 200 and `/api/subscriptions` 401 without a token; typed `Authority` and `Audience`; `ClientGrantsJson` holds `harvest-operator` only, since SCFD refuses an empty map; `events` joins with its tenant id after provisioning. Waiting on scfd: the provisioning route and the M2 dot-scope release. Wheelhouse's owner link is built, shipping as `v0.15.x`
- Every lane records what it builds in its repos' active version track (#42)
- Findings outside the lanes, 2026-11-10:
  - ⬜ fe sdk: an empty leftover folder `presentation/display/eventCalendar/` (2026-09-10) beside `eventCalendarViewer/` (events lane)

## Goal

| # | Milestone | Done when |
|---|---|---|
| #12 | M1 analysis | the Events spec is reconciled with what is built (pull delivery, service tokens, evidence, migration); every contract #14–#33 and #43 has a verdict (provided, change, add or drop) and a phase; each lane has written its picks into its backlog and this doc |
| #13 | M2 build | each lane's P1 rows built, released and deployed to dev, and on dev: (a) a live Afisha record pulled from SCFD becomes a review candidate in Events, and nothing publishes unreviewed; (b) an accepted event shows on Desk's Events page, which calls Events through Desk's backend; (c) every `events.showcase_events` row is imported with a stable id map, its stage, priority, notes, provenance and date precision kept, and Desk's old writer frozen; (d) Events' tests cover replay, out-of-order revisions, a crash around the cursor commit, a malformed record and a cross-organization read |

- Pass/fail for M1: each of #14–#33 shows the owning lane's pick in the Contracts table's `Confirmed` column, and each
  lane's backlog cites the `events-integration #N` points it owns.
- Pass/fail for M2: the owning lane reads (a)–(d) back on dev and reports the evidence (request, status, ids, test
  names and counts); the orchestrator records it in Status.
- A lane builds as soon as its picks are written; only work tied to an open decision waits (#9).

## Lanes

| Lane | Session | Writes only | Slice |
|---|---|---|---|
| events | `ev-events`, `local_ebd5acbd-e3b1-4fe8-b9dc-8ccb0cbe9466` | `workbench/wow-two-sdk-beta/wow-two-sdk-beta.events`, created with the `create-library` skill | #35 |
| scfd | `ev-scfd`, `local_5fcf8705-55eb-4154-ac09-8cebe12c8852` | `workbench/wow-two-sdk-beta/wow-two-sdk-beta.harvest` and `…/wow-two-sdk-beta.harvest-adapters`, one product, work in series | #36 |
| platform | `ev-platform`, `local_017f2bcd-6de5-41e8-93aa-14530829cbde` | `workbench/mfts-projects/ventures/ocharo-hq/ocharo-ws/workbench/ocharo-platform` | #37 |
| wheelhouse | `ev-wheelhouse`, `local_31ee8aa4-c16a-48e1-a4b8-03be478bdb3b` | `workbench/wow-two-platform/wow-two-platform.wheelhouse` | #38 |

- The orchestrator is `ocharo - events server` (`local_4597465c-ca6d-445b-b4f1-77546f8511b4`); it writes this file and
  its own `wow-two-ws` hunks (#41), and no lane's code.
- The developer writes only to the orchestrator; lanes send their decisions there by `SendMessage`.
- No identity, be sdk or fe sdk lane at start (#40).

## Order

1. Each lane verifies its slice of the snapshot against its repos and reports the deltas (#34).
2. Each lane gives a verdict and a phase for the contracts it owns; the orchestrator asks the developer only the open
   decisions, one per turn.
3. Picks go into each lane's backlog and this doc: M1 closes per lane, and its M2 build starts.
4. M2 critical path: scfd renames its scopes (#16) and closes the mapper gaps the first candidate needs (#18) →
   events ships module, client, service and the pull consumer, then releases NuGet, npm and image → platform registers
   Events and SCFD in Ocharo's Identity (#21, #22) and builds the import and the proxy → wheelhouse deploys SCFD, SCFD
   Adapters and Events on dev → platform imports `showcase_events` and freezes the old writer → each lane reads back
   its part of #13.
5. A downstream lane starts on the last published versions and re-pins on the next release.
6. Close: #13 verified end to end, plus a fresh reviewer agent checking the diffs against this doc for correctness gaps.

## Settled

Developer, 2026-10-24 to 2026-11-10; not reopened.

- #1 Events owns the catalog and tracking; Desk owns its page, its organization authorization and references to Ocharo
  entities (E1, `ocharo-ws` `docs/app-boundaries.md`, 2026-10-24).
- #2 One domain repo, `wow-two-sdk-beta.events`, ships the module, client, service and fe package (capability forms;
  FSS shipped this way). Desk calls the service in P1; the catalog row moves from `wow-two-platform.events`.
- #3 The auth rules of `api-communication.md` (2026-11-05): audience-bound tokens verified offline, client credentials
  for a service as itself, token exchange for a person, scopes `{service}.{action}`, revocation through the two signed
  signals, API keys only for callers outside Identity.
- #4 No WoW2 Identity instance: Events and SCFD trust Ocharo's Identity on dev, as FSS does (Files #29, 2026-11-08:
  "it's the least priority").
- #5 Registrations split as Files #32: `ocharo-platform` `engineering/deployment/deploy.yml` holds each resource and
  Desk's grants; Wheelhouse types the per-target URIs.
- #6 SCFD delivers by pull; webhook push waits for a consumer that needs it. Nothing publishes unreviewed.
- #7 `ocharo-fashion` starts private (EV1 default), and stays private under #50.
- #8 Order: Identity closed 2026-11-08, Files (FSS) closed 2026-11-10, Events now (2026-11-05).
- #9 The developer answers only the decisions the goal needs and reviews the built result at the end (Files #33).
- #10 SDK doctrine: Events' need triggers the vector, and the whole vector gets built (`CLAUDE.md` § SDK doctrine,
  `conventions/development/dev-cycle.md` § Vector completeness).
- #50 Sourcing is for internal use only (developer, 2026-11-10: "I only ever use this sourcing for internal use, like
  to track events for ocharo and not post them anywhere else"). Records SCFD collects serve their owner's internal
  tracking; a catalog fed by SCFD stays private to its owner organization; captures stay review evidence; nothing
  sourced is republished. Reading stays polite and open: identified user agent, `robots.txt`, one paced connection per
  host, a challenge or block pauses the source. This goal configures no CAPTCHA, proxy or account-session provider.
- #51 Order (developer, 2026-11-10): "our target was to integrate 100 sources - but that's after we integrate scfd
  itself to ocharo". The 100-source push is the goal after this one. #39's work came from a ChatGPT chat, whose
  handover (the private SCFD console's first account on the local preview) went to the scfd lane, local only.
- #11 Out of scope: Ocharo prod; Haven's OLX intake through SCFD; reminders, webhooks, AI extraction and translation
  (EV4, P2); a second product tracking events; CodeQL on the private adapters repo. After this goal: FSS's
  whole-vector pass.

## Contracts

Lead verdicts come from the 2026-11-10 snapshot and a read-only check by the orchestrator, and stay leads until the
owning lane verifies them. `Confirmed` holds the owning lane's verified pick.

| # | Contract | Lead phase | Lead verdict | Repo that changes | Confirmed |
|---|---|---|---|---|---|
| #14 | Spec reconciled with what is built | P1 | change: the spec's intake `POST /harvest/items` (webhook) becomes a pull consumer over SCFD's `IDeliveryBroker` (#6); its `wow-two-platform.events` host becomes the service in `wow-two-sdk-beta.events` (#2); interim API keys become Identity tokens (#3); the review's § Events intake and review and § Desk migration rules join the spec | events: the reconciled spec lands as the repo's `product/` docs | events 2026-11-10: change, P1. `product/product.md` in the events repo covers pull intake, Identity tokens, evidence per observation and the Desk import; webhook intake, API keys for our own callers and the `wow-two-platform.events` host dropped. Picks in `engineering/planning/backlog.md` § Integration picks |
| #15 | SCFD pull subscription | P1 | provided (lead): `api/subscriptions`, `api/subscriptions/{id}/events`; `DeliveryEvent` carries `EventId` (dedup), `ItemId` (content), `PostId` and `Revision` (highest wins); no global order | scfd confirms shape and cursor semantics; events consumes | scfd 2026-11-10: provided, P1. The SCFD Client gains client credentials through be sdk `Http.Auth.OAuth2ClientCredentials`. `GET api/subscriptions/{id}/events?cursor=&limit=100` answers `{data, next, hasMore}`; the cursor is opaque and client-held, an empty poll returns the same cursor, an older cursor replays the same `eventId`s; honour `post.purged`. Events only reads; the operator creates the subscription through adapters `POST api/ocharo/sources/setup`. events: polls with a client-credentials token; the subscription id arrives as setting `Events:Intake:Scfd:SubscriptionId`; page and cursor commit in one transaction, dedup on (subscription, `EventId`), highest `Revision` per `PostId` |
| #16 | SCFD scope names | P1 | change: SCFD documents `tenants.manage`, `sources.manage` and `events.read` (`harvest` `engineering/deployment/deployment.md:36`), outside `{service}.{action}` (#3); `events.read` collides with Events' own scopes in the same Ocharo Identity | scfd renames them under its resource; platform registers the new names | scfd: change, P1. Resource `harvest`, as FSS kept `files`; 11 scopes `harvest.{noun}-{verb}`, two segments as Ocharo's Identity requires: `tenants-manage`, `containers-manage`, `sources-manage`, `pipelines-read`, `pipelines-run`, `pipelines-manage`, `subscriptions-manage`, `events-read`, `links-submit`, `entries-write`, `posts-read`; the registry and API keys keep colon names, `CallerResolver` maps them; SCFD accepts the dot names once its M2 rename ships. Operator client `harvest-operator` holds all 11; Events' client `events` holds `harvest.events-read` |
| #17 | SCFD's issuer | P1 | change: the 2026-11-05 review gives SCFD its own issuer; #4 puts SCFD on Ocharo's Identity on dev | scfd's docs; wheelhouse types issuer and audience | scfd: change, P1, docs only; the code trusts any issuer through `ServiceAccess:Authority` and `Audience`. wheelhouse: `Authority` is Ocharo dev Identity's issuer exactly as tokens' `iss`, trailing slash included (FSS's 401); `Audience` is the same string typed as the `harvest` resource's `Uri`; Events' issuer and audience the same way |
| #18 | `wow2.event.v1` coverage | P1 for the first candidate, P2 the rest | change: `EventSchemaMapper` maps dates, place, offers, contacts and source tags, not every deadline, participation or contact-ownership field | scfd fixes generic gaps upstream, Afisha readings in the adapters | scfd: change. P1: organizer only from a schema.org organizer (today it falls back to the article's author, Afisha's journalist), plus `postedAt`. P2: certainty, time zone, deadlines, participation, contact ownership, structured place and country |
| #19 | Evidence per observation | P1 | unverified: Events keeps source instance, pipeline, post and revision, original link, capture reference, observed time, source fields and mapping version; whether `DeliveryEvent` carries the capture reference and the mapping version is unchecked | scfd adds what is missing; events stores it | scfd: change, P1. `wow2.event.v1` gains a mapping stamp `{schema, norm, rules, parser}` and `capture {captureId, capturedAtUtc, url}`; `DeliveryEvent` gains `pipelineId`; Events keeps the source instance in its own source registration. events: stores per observation each link's URL, source id, capture id, capture time and source fields, the `EventId`, `ItemId`, `PostId`, `Revision`, the occurred time and the raw payload |
| #20 | Afisha into an Events subscription | P1 | provided (lead): adapters `v0.1.1` ships the Afisha adapter, `OcharoFashionFilter`, subscriptions in `wow2.event.v1` with filter `ocharo-fashion-v1` and catalog `ocharo-fashion`; the Afisha acceptance run is open | scfd (adapters) | scfd: provided, P1; the acceptance run takes a bounded live sample in M2 |
| #21 | Events in Ocharo's Identity | P1 | add: no `events` resource; Events' scopes and organization permissions named by the events lane | events names them; platform `deploy.yml` registers (#5); wheelhouse types `Uri` and `SignalUrl` | platform 2026-11-10 (`ocharo-platform` `94fd5a7`): add, P1. Resource 3 `events`, namespace `events`, with `SignalUrl` (exchanged tokens carry `sid` and `org_id`); Desk's client 0 gets `ExchangeResources: events` only. events: `Uri` `https://events.{domain}/`, `SignalUrl` `{Uri}signals/identity`; scopes `events.read`, `events.track`, `events.review`, `events.import`, `events.admin`; organization permissions `events:read`, `events:track`, `events:review`, `events:admin`; Desk's backend gets `events.read events.track events.import` by token exchange |
| #22 | SCFD in Ocharo's Identity | P1 | add: no SCFD resource; a `client_credentials` client for Events as SCFD's consumer and one for SCFD's operator, each mapped in `Harvest:ServiceAccess:ClientGrantsJson` | platform registers; wheelhouse types URIs, secrets and the grant mapping | platform: add, P1. Resource 4 `harvest` (no namespace, no `SignalUrl`: service tokens only); client 8 `events` (`harvest.events-read`) and client 9, SCFD's operator (all 11 scopes), both client credentials with typed secrets, since `from` links only inside one product. scfd: `ClientGrantsJson` is `{clientId: {isOperator, tenantId?, scopes: [colon names]}}` |
| #23 | Desk → Events for a person | P1 | add: token exchange with `act` (#3; Ocharo's Identity provides it, Files #13); Desk's backend checks membership; Events checks a scope plus an organization permission, never a scope alone (Files #23) | platform: Desk's grant and the permissions on Ocharo's roles; events: the policies | platform: add, P1. Desk's membership filter plus Identity.Client's route-organization check (404) before the exchange; roles: owner and admin all `events:*`, editor read and track, viewer read, billing none. events: a person's call needs the scope plus its permission, a service's the scope alone; tracking keys on the caller's (`iss`, `org_id`), another organization's route answers 404; a private catalog is readable by its owner organization only; review and imports need the owner organization |
| #24 | Service token acquisition | P1 | unverified: Events → SCFD by client credentials and Desk → Events by token exchange need a token handler; whether Identity's `packages/Client` ships both is unchecked | identity, only if missing (a blocker, #40) | platform and scfd: provided, no Identity change. be sdk `10.0.109-beta` ships `OAuth2ClientCredentialsHandler` and `OAuth2TokenExchangeHandler`; Identity.Client `10.0.30-beta` ships `BffSubjectTokenSource` |
| #25 | `IEventsClient` and the fe package | P1 | add: be `Client` package and npm package, released from tags | events → platform | events: change, P1. `IEventsClient` becomes the broker family in `Events.Abstractions`; `AddEventsClient()` takes the be sdk's `AddOAuth2TokenExchange` for a person or `AddOAuth2ClientCredentials` for a service; npm `@wow-two-beta/fe-events` holds the components and client |
| #26 | Import bundle | P1 | add: `wow2.events-import.v1` with `dryRun` and a stable old → new id map; keeps stage, priority, notes, provenance, language and date precision (a stored first-of-month stays month precision; `estimated` never becomes confirmed); titles not assumed Uzbek | events defines and imports; platform produces it from `showcase_events` | platform producer, P1: read-only Desk verb `export events` → `wow2.events-import.v1`; per record `sourceId` (Desk id) and `key` for the map, provenance (source organization, created by and at, revision, source URL), titles `und`, precision day → day, month → month, estimated → month with `certainty: estimated`, unknown → no dates, and the whole Desk row as `legacy`. events: add, P1. `POST …/catalogs/{c}/imports` with `dryRun`, idempotent on (catalog, organization, `legacyId`), so a rerun returns the same id map; month and estimated precision kept; language per row, `und` when unknown; status, priority, notes, participation and cost go to tracking; the exact schema comes with the first Client release |
| #27 | Desk cutover | P1 | change: `EventsController`, `EventImportService` (skips existing keys, `:35`) and the Vue screens under `apps/web/src/presentation/events` move onto the Events contract through Desk's proxy; the old writer frozen; export and rollback kept until reconciliation passes | platform | platform: change, P1. `Events:BaseUrl`, linked from resource 3's `Uri`, turns Desk's reads and one tracking route into a proxy on `IEventsClient`; old POST, PUT and DELETE answer 410 `EventsMoved`; `import events` refuses; the table stays as rollback until counts and fields reconcile; the Vue screens read the Events contract |
| #28 | Events deploy | P1 | add: `deploy.yml` with service, PostgreSQL database, settings, secrets, signal URL and the review console | events → wheelhouse | events: add, P1. Service `events` on PostgreSQL, site `app` (API plus console), typed issuer, audience, SCFD base URL, token endpoint, client id and secret, subscription id; release asset `events-release.tar.gz`. wheelhouse (Wheelhouse `b4cae16`): product `events`, target `events-dev` beside `files-dev`, database `events_dev`; a private `console` site would need a tailnet node, so the console stays on `app` behind sign-in |
| #29 | SCFD and SCFD Adapters on dev | P1 | add: neither console holds an Events, SCFD or SCFD Adapters product; P1 runs `harvestadapters` only (#45); the private image pull rests on #46; the released bundles predate service access | wheelhouse; scfd releases first | wheelhouse: add, P1. Target `harvestadapters-dev` (database `harvestadapters_dev`) is the SCFD Events pulls from (#45); no `harvest-dev` (#45 over the brief's done-when); release reads through the GitHub App, the image through the control host's machine-account token file (#46). Code gap built in P1: an owner link carries a secret generated on `ocharo-dev` to another product's target key, same environment, never shown. scfd: two catalog entries stay, since `harvest` is a library with its own releases (#47) |
| #30 | Review console | P1 | add: reviewers accept, merge or reject candidates; who signs in through which Identity (#4) is the events lane's proposal | events; platform registers the console's client | events: add, P1. The console is Events' own pages; reviewers sign in through Ocharo's Identity with Identity's BFF as confidential client `events-console` and need `events:review` in the catalog's owner organization; platform registers the client, wheelhouse types its redirect URI and secret |
| #31 | Event images | open | the spec puts images in WoW2's own Files instance, which does not exist; FSS on `files-dev` holds only tenant `ocharo` | events proposes, with platform and wheelhouse input | inputs: platform, P2 from Desk's side (`showcase_events` has no image field), catalog images stay out of Ocharo's FSS tenant, client 8 could reach `files` as a stopgap; scfd, Afisha's photos are not reusable (#32); wheelhouse, one FSS on dev, tenant `ocharo` only, no second instance. events: P1 keeps image references only (URL, SCFD link and capture, attribution), no bytes; P2 home open (#48) |
| #32 | EV2 Afisha intake route and terms of use | open | provider API, HTTP capture or a feed; the terms of use | scfd proposes | scfd: HTTP capture of public category and article pages inside `robots.txt`; no public API or feed. Afisha's terms ask written permission from Afisha Media to use site materials, and attribution. For this goal captures stay internal review evidence in the private catalog (#7); anything shown carries facts plus an attributed link, never Afisha's text or photos. `ocharo-fashion` stays private (#50), so no public plan needs Afisha's permission |
| #33 | Operating controls | P1 minimal, P2 the rest | change: request budgets in transport, retention purge, freshness and consumer lag, pause, resume, replay (review § Operation before expansion) | scfd; events exposes its cursor lag and quarantine | scfd: provided, P1 minimal as built: pipeline pause and resume, cursor replay, step-boundary budgets, a refusal pausing its lane, `pipeline.run` and `pipeline.health` events, `MaxStaleness`. P2: budgets reserved in transport, the retention purge, a lag and freshness readout, resync |
| #43 | SCFD packages for Events | P1 | add: `WoW2.Sdk.Beta.Be.Harvest.*` and `@wow-two-beta/fe-harvest` were never published; `publish-packages.yml` waits on the repo variable `PUBLISH_PACKAGES` and a nuget.org trusted-publishing policy (scfd lane, 2026-11-10) | scfd publishes the family, or events calls SCFD's HTTP API with no package | scfd: add, P1. `WoW2.Sdk.Beta.Be.Harvest.Abstractions`, `.Client` (`AddHarvestDataClient` → `IDeliveryBroker`) and `.Testing` (`FakeDeliveryBroker`, conformance) publish first in M2 with #16; adding the nuget.org trusted-publishing policy takes one developer passkey tap, asked then. events: P1 reads the wire with its own reader and swaps to `Harvest.Client` once published (P2), so P1 needs no SCFD package |

## Lane slices

- #34 First step of every lane: verify its slice of the snapshot in its brief against its repos and report the deltas
  to the orchestrator before any analysis.
- #35 events: #14, the consumer side of #15 and #19, the names in #21, the policies in #23, #25, #26's contract, #28,
  #30, #31; then the whole vector: module, client, service, fe package, review console, imports, ICS, conformance suite,
  `deploy.yml`.
- #36 scfd: #15–#20, #32 and #33 on SCFD's side; Afisha into Events in `wow2.event.v1`; service access on dev.
- #37 platform: #21–#23 registrations and permissions, #26's producer, #27 cutover.
- #38 wheelhouse: #28 and #29 deployed on dev; the per-target URIs, secrets and keys for #21 and #22.

## Open

- #39 Uncommitted SCFD work, answered by the developer 2026-11-10 ("no chat is working in scfd so commit is yours"): `harvest` holds 80 changed paths (61 modified, 18 new,
  1 deleted) and `harvest-adapters` 43 (29, 13, 1), edited from 2026-11-09 13:42 (the `SCFD.*.slnx` rename,
  `DeliveryTagFilter`, `packages/Caex`) to 2026-11-10 07:24 local (Hosting access, `SubscriptionsController`, Identity
  configuration, console pages, `deployment.md`). `wow-two-ws` holds matching hunks in `catalog.yml` and
  `docs/platform-apps.md`. No desktop transcript names `CallerResolver` or `HostConfiguration.Identity`. The scfd lane
  writes nothing in either repo until the developer says whose it is. Its content (scfd lane, 2026-11-10): the brand
  rename Harvest → SCFD in docs, descriptor, solutions and brand assets, the product id kept `harvest`; in harvest, the
  console's browser sign-in that `d77daf6` removed, back as an Identity authorization-code BFF beside service access,
  with `CallerResolver` mapping sessions through operator subjects and an organization → tenant map, plus
  `DeliveryTagFilter`, `PipelineScope` and a console source picker; in adapters, a CAEx venue-calendar reader
  (`packages/Caex`), a JSON source registry replacing the Ocharo presets, Afisha URL fixes, host Identity configuration
  and E2E tests. None of it touches `EventSchemaMapper` or the payload renderer.
- #40 No lane writes Identity, the be sdk or the fe sdk. A change a lane needs there goes to the orchestrator as a
  blocker, and the orchestrator starts a lane for that repo then (Files #31).
- #41 `wow-two-ws`: the events lane hands `create-library`'s `catalog.yml` and `scripts/active.sh` changes to the
  orchestrator, which commits only those hunks (`git apply --cached`), since other chats hold edits in both files.
- #42 Every lane records what it builds in its repos' active version track, in the commit that builds it. Its turn-end
  recap reaches the orchestrator cut to ~400 characters, so the report leads it.
- #44 #13 (c) reads local Desk's 68 rows, since dev's `showcase_events` holds none: the producer exports them into the
  bundle and imports them into Events on dev; dev Desk's empty table needs no reconciliation, and its writer is frozen
  all the same (platform lane pick, orchestrator accepted 2026-11-10 under #9).
- #45 SCFD on dev for this goal is product `harvestadapters` alone: its image carries the public SCFD engine plus the
  Afisha readers, so Events' subscription lives there. Public `harvest` keeps `deploy: none` until a consumer needs the
  engine without private sources (Haven, out of scope #11). Whether SCFD and SCFD Adapters merge into one catalog
  product (catalog § Products of several repositories) is the scfd lane's M1 call (orchestrator pick 2026-11-10 under
  #9, from the wheelhouse lane's #34).
- #47 SCFD stays two catalog entries: `harvest` is a domain library with its own NuGet, npm and image releases, so a
  merged entry would deploy a second engine beside the adapters host (scfd lane, 2026-11-10, under #45). Release order
  for #13 (a): push harvest's `d77daf6` plus the M2 rename and gaps (#16, #18, #19, client credentials) → re-pin the
  adapters' `harvest-runtime.json` `publicHarvestRef` to that commit (the image build downloads it, so an adapters
  build fails until it is pushed) → push the adapters and release `v0.1.2`, image and bundle carrying ServiceAccess.
  The deploy needs no harvest release; a harvest `be-v` release only serves NuGet consumers, which Events' P1 is not.
- #48 P2, outside this goal: where a published event's image lives. The events lane proposes a copy into FSS under
  the owner's tenant (`ocharo`); the platform lane would keep catalog images out of Ocharo's tenant; one FSS runs on
  dev. Settled when P2 opens.
- #49 Settled 2026-11-10 (platform lane, checked by the orchestrator): a resource needs no `SignalUrl`.
  `OidcResourceOptions.SignalUrl` is `string?` (Identity `OidcResourceOptions.cs:29`), and
  `OidcServerOptionsValidator.CheckSignalUrls` checks only the URLs a resource or client names; `harvest` carries none,
  since only service tokens reach it. Platform's draft registrations: resource 3 `events` (5 scopes, namespace,
  `SignalUrl`), resource 4 `harvest` (11 scopes), client 8 `events`, client 9 `harvest-operator`, client 10
  `events-console` (code flow), Desk's client 0 exchanging to `events.read events.track events.import`; clients 8–10
  `generate` their secrets; they push once wheelhouse has typed resource 3's `Uri` and `SignalUrl`, resource 4's `Uri`,
  and client 10's redirect, sign-out redirect and `SignalUrl`.
- #46 Settled 2026-11-10: the private `harvestadapters` image pulls with the control host's token file (Registry access
  passed); no developer step.

## Cross-lane contracts

| From | To | What | When |
|---|---|---|---|
| scfd | events | the subscription shape, cursor and `DeliveryEvent` fields (#15, #19), and the package Events references for them | M1 |
| scfd | platform, wheelhouse | SCFD's resource name, URI form, scope names (#16) and the grant mapping's shape (#22) | M1 |
| events | platform, wheelhouse | Events' resource name, URI form, scopes and organization permissions (#21, #23) | M1 |
| events | platform | `IEventsClient` NuGet and npm versions, the `wow2.events-import.v1` schema (#25, #26) | M2 |
| events | wheelhouse | `deploy.yml` and the published image (#28) | M2 |
| scfd | wheelhouse | SCFD's and the adapters' `deploy.yml`, images, and the Events tenant and subscription to provision (#29, #20) | M2 |
| platform | wheelhouse | Events' and SCFD's registrations in `ocharo-platform` `deploy.yml` before Wheelhouse types them: a required untyped key refuses every Identity deploy (Files) | M2 |
| wheelhouse | events, scfd, platform | the dev targets' names, typed URIs and linked secrets, never host addresses in repos | M2 |

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

- 🔄 M1 analysis (#12): four lanes started 2026-11-10; each verifies its snapshot slice first (#34)
  - ✅ events #34, 2026-11-10: the slice holds; `workbench/wow-two-sdk-beta/*` has commit and push ON, so repo creation runs; the `catalog.yml` `events` row's `purpose` line carries #39's uncommitted SCFD hunk (`:272`), so the lane's #41 hunk comes with context against `HEAD`
  - ✅ scfd #34, 2026-11-10, read-only (#39 hold kept): harvest's tags reach `v0.1.9` (`bc0c8ac`) on GitHub, unfetched locally; `d77daf6` (harvest) and `18b083a`, `1b58b9d` (adapters) are local only, unpushed and unreleased; harvest's NuGet family `WoW2.Sdk.Beta.Be.Harvest.*` and npm `@wow-two-beta/fe-harvest` were never published (#43); the registry keeps colon scopes (`events:read`) and `CallerResolver` maps a token's dot names onto them, so Ocharo's Identity would carry `events.read` (#16); `api/subscriptions` needs `subscriptions:manage`, `…/{id}` and `…/{id}/events` need `events:read` (#15); mapper audit 7 yes, 15 partial, 11 no of 33 fields (`scfd-mapper-audit.md`, #18); the adapters pin be sdk `10.0.106-beta` and build harvest from source
  - ✅ platform #34, 2026-11-10, read-only: dev's `events.showcase_events` exists (`008-events` applied) with 0 rows; local Desk on the Mac holds all 68 rows, 1 organization `Ocharo`, from 3 bundle imports (2026-10-08, 10-13, 10-30), none edited in Desk; stages 64 candidate, 1 applying, 3 skipped; precision day 35, month 5, estimated 18 (all first-of-month), unknown 10; titles Latin-script, mostly English, none Uzbek-only; notes on all 68, source URL 51, website 46, deadline 9; the source bundles are not under `~/Projects`; Desk's own bundle is `ocharo.events-import.v1`; `EventImportService` skips existing keys at `:35`; `b2cb4e3` sits one commit past `v0.2.9`, untagged; the lane opens v0.3 for this work (#44)
- ⬜ M2 build (#13)
- ⬜ Asked of the developer 2026-11-10: whose is the uncommitted SCFD work (#39)
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
- #7 `ocharo-fashion` starts private (EV1 default).
- #8 Order: Identity closed 2026-11-08, Files (FSS) closed 2026-11-10, Events now (2026-11-05).
- #9 The developer answers only the decisions the goal needs and reviews the built result at the end (Files #33).
- #10 SDK doctrine: Events' need triggers the vector, and the whole vector gets built (`CLAUDE.md` § SDK doctrine,
  `conventions/development/dev-cycle.md` § Vector completeness).
- #11 Out of scope: Ocharo prod; Haven's OLX intake through SCFD; reminders, webhooks, AI extraction and translation
  (EV4, P2); a second product tracking events; CodeQL on the private adapters repo. After this goal: FSS's
  whole-vector pass.

## Contracts

Lead verdicts come from the 2026-11-10 snapshot and a read-only check by the orchestrator, and stay leads until the
owning lane verifies them. `Confirmed` holds the owning lane's verified pick.

| # | Contract | Lead phase | Lead verdict | Repo that changes | Confirmed |
|---|---|---|---|---|---|
| #14 | Spec reconciled with what is built | P1 | change: the spec's intake `POST /harvest/items` (webhook) becomes a pull consumer over SCFD's `IDeliveryBroker` (#6); its `wow-two-platform.events` host becomes the service in `wow-two-sdk-beta.events` (#2); interim API keys become Identity tokens (#3); the review's § Events intake and review and § Desk migration rules join the spec | events: the reconciled spec lands as the repo's `product/` docs | — |
| #15 | SCFD pull subscription | P1 | provided (lead): `api/subscriptions`, `api/subscriptions/{id}/events`; `DeliveryEvent` carries `EventId` (dedup), `ItemId` (content), `PostId` and `Revision` (highest wins); no global order | scfd confirms shape and cursor semantics; events consumes | — |
| #16 | SCFD scope names | P1 | change: SCFD documents `tenants.manage`, `sources.manage` and `events.read` (`harvest` `engineering/deployment/deployment.md:36`), outside `{service}.{action}` (#3); `events.read` collides with Events' own scopes in the same Ocharo Identity | scfd renames them under its resource; platform registers the new names | — |
| #17 | SCFD's issuer | P1 | change: the 2026-11-05 review gives SCFD its own issuer; #4 puts SCFD on Ocharo's Identity on dev | scfd's docs; wheelhouse types issuer and audience | — |
| #18 | `wow2.event.v1` coverage | P1 for the first candidate, P2 the rest | change: `EventSchemaMapper` maps dates, place, offers, contacts and source tags, not every deadline, participation or contact-ownership field | scfd fixes generic gaps upstream, Afisha readings in the adapters | — |
| #19 | Evidence per observation | P1 | unverified: Events keeps source instance, pipeline, post and revision, original link, capture reference, observed time, source fields and mapping version; whether `DeliveryEvent` carries the capture reference and the mapping version is unchecked | scfd adds what is missing; events stores it | — |
| #20 | Afisha into an Events subscription | P1 | provided (lead): adapters `v0.1.1` ships the Afisha adapter, `OcharoFashionFilter`, subscriptions in `wow2.event.v1` with filter `ocharo-fashion-v1` and catalog `ocharo-fashion`; the Afisha acceptance run is open | scfd (adapters) | — |
| #21 | Events in Ocharo's Identity | P1 | add: no `events` resource; Events' scopes and organization permissions named by the events lane | events names them; platform `deploy.yml` registers (#5); wheelhouse types `Uri` and `SignalUrl` | — |
| #22 | SCFD in Ocharo's Identity | P1 | add: no SCFD resource; a `client_credentials` client for Events as SCFD's consumer and one for SCFD's operator, each mapped in `Harvest:ServiceAccess:ClientGrantsJson` | platform registers; wheelhouse types URIs, secrets and the grant mapping | — |
| #23 | Desk → Events for a person | P1 | add: token exchange with `act` (#3; Ocharo's Identity provides it, Files #13); Desk's backend checks membership; Events checks a scope plus an organization permission, never a scope alone (Files #23) | platform: Desk's grant and the permissions on Ocharo's roles; events: the policies | — |
| #24 | Service token acquisition | P1 | unverified: Events → SCFD by client credentials and Desk → Events by token exchange need a token handler; whether Identity's `packages/Client` ships both is unchecked | identity, only if missing (a blocker, #40) | — |
| #25 | `IEventsClient` and the fe package | P1 | add: be `Client` package and npm package, released from tags | events → platform | — |
| #26 | Import bundle | P1 | add: `wow2.events-import.v1` with `dryRun` and a stable old → new id map; keeps stage, priority, notes, provenance, language and date precision (a stored first-of-month stays month precision; `estimated` never becomes confirmed); titles not assumed Uzbek | events defines and imports; platform produces it from `showcase_events` | — |
| #27 | Desk cutover | P1 | change: `EventsController`, `EventImportService` (skips existing keys, `:35`) and the Vue screens under `apps/web/src/presentation/events` move onto the Events contract through Desk's proxy; the old writer frozen; export and rollback kept until reconciliation passes | platform | — |
| #28 | Events deploy | P1 | add: `deploy.yml` with service, PostgreSQL database, settings, secrets, signal URL and the review console | events → wheelhouse | — |
| #29 | SCFD and SCFD Adapters on dev | P1 | unverified: Wheelhouse's repo docs name no Events or SCFD product; targets live in Wheelhouse's store; which images run (the adapters host reuses public SCFD) and the private image pull are unchecked | wheelhouse | — |
| #30 | Review console | P1 | add: reviewers accept, merge or reject candidates; who signs in through which Identity (#4) is the events lane's proposal | events; platform registers the console's client | — |
| #31 | Event images | open | the spec puts images in WoW2's own Files instance, which does not exist; FSS on `files-dev` holds only tenant `ocharo` | events proposes, with platform and wheelhouse input | — |
| #32 | EV2 Afisha intake route and terms of use | open | provider API, HTTP capture or a feed; the terms of use | scfd proposes | — |
| #33 | Operating controls | P1 minimal, P2 the rest | change: request budgets in transport, retention purge, freshness and consumer lag, pause, resume, replay (review § Operation before expansion) | scfd; events exposes its cursor lag and quarantine | — |
| #43 | SCFD packages for Events | P1 | add: `WoW2.Sdk.Beta.Be.Harvest.*` and `@wow-two-beta/fe-harvest` were never published; `publish-packages.yml` waits on the repo variable `PUBLISH_PACKAGES` and a nuget.org trusted-publishing policy (scfd lane, 2026-11-10) | scfd publishes the family, or events calls SCFD's HTTP API with no package | — |

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

- #39 Uncommitted SCFD work, asked of the developer 2026-11-10: `harvest` holds 80 changed paths (61 modified, 18 new,
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

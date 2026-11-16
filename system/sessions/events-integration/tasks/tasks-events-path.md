# SCFD → WoW2 Events → Ocharo Events: end-to-end gaps and tasks

*Checked 2026-11-16, code level and local tests only (no deployed hosts).*

Code read: `wow-two-sdk-beta.harvest` working tree (HEAD `2dd33d6` plus another lane's uncommitted work; the
delivery code below is unchanged by it), `wow-two-sdk-beta.events` `v0.1.11` (`934d5b5`), `ocharo-platform` `ae752d8`
(the Ocharo Events app, `v0.3.11` / `v0.3.12`). Path roots used below:

- `{harvest-be}` = `engineering/codebase/harvest.backend-services` in `wow-two-sdk-beta.harvest`
- `{events-be}` = `engineering/codebase/events.backend-services` in `wow-two-sdk-beta.events`
- `{oe-be}` = `engineering/codebase/ocharo-events.backend-services` in `ocharo-platform`
- `{oe-fe}` = `engineering/codebase/ocharo-events.frontend-services/apps/web` in `ocharo-platform`

The path: SCFD stores a post → `DeliveryEventWriter` appends it to each matching subscription (filter
`ocharo-fashion-v1`) → `GET api/subscriptions/{id}/events` renders `wow2.event.v1` (`EventSchemaMapper` +
`ModuleDeliveryBroker.RenderPayload`) → Events' `IntakeProcessor` maps it (`ScfdEventMapper`) into catalog
`ocharo-fashion` and, under `Review: auto` + `Classifier: filter`, publishes every record → Ocharo's Events app reads
the catalog through the tracking broker (`EventsServiceRepository`) and maps each event onto Desk's old
`ShowcaseEvent` wire (`EventsServiceMapper`), which the Vue page renders.

## Field map

| Field | SCFD (`wow2.event.v1`) | Events (facts / model) | Ocharo app (`ShowcaseEvent` / UI) | Gap |
|---|---|---|---|---|
| Title | `title` + `language {code, script}` | `Title{"ru-Cyrl": …}`, cut to 200 | `title`; picks keys `und, en, uz, ru` then any (`EventsServiceMapper.cs:22`) | Keys are `ru-Cyrl` / `uz-Latn`, so the preference list never matches; UI locale ignored; language never shown (E25) |
| Description | `description` (article text) | dropped by design (#50, `Summary` empty) | none | By design (#32: Afisha text never shown); only the source link explains the event |
| Start | `starts {value "2026-12-05T19:00:00+05:00", precision}` | `Starts` `yyyy-MM-ddTHH:mm`, offset dropped, `TimeZone` never set (`ScfdEventMapper.cs:377`) | `startsOn` date only; minute → `day`, year → `unknown` | Time of day and zone lost; year-only shows "not announced" (E08, E10) |
| End | `ends` (schema.org `endDate`) | `Ends` | `endsOn`, only when a start exists and end ≥ start | OK; Afisha's extra schedules collapse to the first one in the reader (sibling scope) |
| Undated | `starts: null` | `Starts` unknown | "Dates not announced", grouped last, always listed | OK |
| Application deadline | not top-level; only in the reader namespace `schemaOrg.{craftfair,uzexpocentre}.applicationDeadline`, `schemaOrg.afisha.applicationDeadlineEvidence {raw, date}` | never read; `Deadlines` empty for every sourced event | `applicationDeadline` null → "Deadlines first" never lists a sourced event | Dropped at SCFD's projection and at Events (E07, E08) |
| Venue | `place.mentions[venue]`, `schemaOrg.location.name` | `Place.Venue` | `venue` on detail; card shows city · country | OK |
| Address, region, geo | mentions `street`/`address`/`region`, `geo` | `Place.Address/Region/Latitude/Longitude` | dropped | Address never shown (E10) |
| City | mentions `city`, `schemaOrg…addressLocality` | `Place.City` | `city` | OK since adapters `v0.1.7` |
| Country | `schemaOrg…addressCountry` (rare) | else the source's `DefaultCountry` `UZ` for every record (`IntakeProcessor.cs:508`) | `country` + derived `scope` (UZ → local) | A foreign city announced on a UZ source becomes country UZ, scope "local" (E11) |
| Price | `offers[] {amount, min, max, currency, free, raw, role}` | `Offers[]` (raw, per, negotiable dropped) | none; `cost` is Ocharo's own tracking field | A ticketed event reads "Cost not stated" (E09) |
| Ticket link | `contentLinks[kind=ticket]` | `TicketUrl` | dropped | (E09) |
| Organizer | `organizer {name, url}` only from a schema.org organizer | `Organizer {Name, Website}` | `organizer` name only | Organizer website dropped (E10) |
| Website | `contentLinks[kind=site]`: every in-page link is `site` (`RulesPostExtractor.cs:42`) | first `site` link (`ScfdEventMapper.cs:130`); the golden test pins Afisha's venue page as the website | `website`, shown as "Website" | Wrong: the aggregator's own page shows as the event's website (E06) |
| Original link | `links[].url` (post links, `role: primary`) | `Sources[].Url` + observation links | `sourceUrl` = first source URL | OK |
| Source name | `links[].sourceId` (UUID); subscription `context.sourceGroup/sourceChannel` | `Sources[] {Kind scfd, Id "{instance}/{postId}"}`; context not stored | none | No "via Afisha"; Ocharo can't tell sources apart (E15, E16) |
| Images | `media[] {url, width, height}` (sizes null in fixtures) | dropped by design (`Images` empty, #31, #50) | none | By design for Afisha (#32); no per-source policy (E32) |
| Language | `language {code, script, mixed, confidence}` | `Languages ["ru-Cyrl"]` | none | (E25) |
| Posted | `postedAt {value, precision, timeZone}` | ignored | none | Can't order or triage by announcement time (E15, E31) |
| Contacts | `contacts[]` | ignored (#18 P2, contact ownership) | none | By design for now |
| Kind / format | `kind` = AI classification kind, null without AI | `Kind` `other` unless a classifier sets it | `format` `other` for every sourced event | Format badge and filter carry no information (E12; AI kind is the AI lane's) |
| Status | `schemaOrg.eventStatus` | `Status` Cancelled / Postponed / Rescheduled / MovedOnline | dropped | A cancelled event looks live (E05) |
| Attendance | `schemaOrg.eventAttendanceMode` | `Attendance` | dropped | Online events look physical (E05) |
| Relevance | filter `ocharo-fashion-v1` decides delivery; `classification` null | `Classifier: filter` → every delivered record published | listed as "New — review" | Filter passes off-topic events (Silk Road marathon, UX designer meetup, interior design expo) (E02) |
| Coverage | `ocharo setup` creates 5 default subscriptions (craftfair, afisha ×2, anons, uzexpocentre) | `deploy.yml` pulls 2 (afisha fashion, exhibitions) | — | 3 of 5 default subscriptions never reach Ocharo (E01, E19, E20) |
| Revision | `revision` per post; newer wins | classifier-published events follow the source in place | `revision` = tracking revision + 1; facts changes don't move it | A stage change on a page read before an SCFD revision answers 410 "moved", not 409 (E13) |
| Post gone | `state: gone` | untracked, unended event held as candidate → leaves the list; tracked stays | no signal | Tracked events show no "listing removed" (E15, E16) |
| Post merged | `post.merged` + `mergedInto` | duplicate held unless any organization tracks it (`IntakeProcessor.cs:451`) | tracked duplicate stays listed twice | Tracking not carried to the survivor (E18) |
| Cross-source duplicate | separate posts (dedup needs equal URL, declared origin or near-equal text) | one event per post | listed twice | No cross-source match (E17) |
| Stops matching filter | nothing delivered (`DeliveryEventWriter.cs:36-38`) | stays published | stays listed | Stale off-topic events never leave (E03, E04) |
| Purged | `post.purged` | payload and link `sourceFields` cleared, facts kept | unchanged | OK |
| Stage, priority, notes, participation, cost | — | `Tracking` (+ `Fields` JSON) | `status`, `priority`, `notes`, `participation`, `cost` | OK; but every quick stage change re-sends and re-validates all facts (E13) |

## Live check on dev (2026-11-16)

Ocharo Events dev `0.3.11`, signed in as the owner, read through the app's own API from its page:

- 71 events: 69 came from Desk's import on 11-10, only 3 from SCFD (Afisha, created 11-10, 11-12, 11-13); none
  arrived after 11-13 (E00).
- The 3 SCFD events are in Russian: titles and the city `Ташкент`, while curated events say `Tashkent` (E25, E33).
- All 3 have format `other`, a fashion show included; participation, notes and organizer are empty (E12, E10).
- No image field exists in the list or detail reads, so SCFD's pictures never reach Ocharo (E32).
- The list read omits `venue` and `sourceUrl`, which the detail read has; nothing marks an event as sourced
  (E15, E16).

## Intake coverage and relevance

### E00 Find why no SCFD event reached Ocharo dev after 11-13
- Repo: wow-two-sdk-beta.events · Area: intake operations · Type: fix
- Why: Ocharo dev holds 3 SCFD events, the last created 11-13; either SCFD stopped harvesting, the filter matches
  nothing new, or Events stopped pulling.
- Do:
  - On `harvest-dev`, read the Afisha sections' last runs and the two Ocharo subscriptions' delivered counts and
    cursors (`ocharo status`, run audit); on `events-dev`, run `intake check` and read the intake cursors.
  - Name the stage that stopped (harvest, match, delivery or intake) and fix it, or record that no new Afisha post
    matched `ocharo-fashion-v1` since 11-13 with the run evidence.
  - Record the finding in `wow-two-sdk-beta.events` `engineering/planning/version-track/v0.1/` or the current track.
- Done when: a new matching Afisha post appears in Ocharo dev within one harvest interval, or the record shows
  every stage healthy with zero new matches.
- Depends: —

### E01 Pull all five default Ocharo SCFD subscriptions into Events
- Repo: wow-two-sdk-beta.events · Area: intake config · Type: fix
- Why: `deploy.yml` wires only afisha fashion and exhibitions; craftfair, anons and uzexpocentre records never reach Ocharo.
- Do:
  - In `engineering/deployment/deploy.yml` (Intake block, `Events:Intake:Sources:0..1`), add `Sources:2..4` named `craftfair-all`, `anons-events`, `uzexpocentre-exhibitions`, each `from` source 0 for `BaseUrl`, token settings, `Review`, `Classifier`, `Filter`, `OwnerOrg`, with its own untyped `SubscriptionId`.
  - Leave `DefaultCountry` `UZ` for all three (each registry group covers Uzbekistan); add a comment that CAEx `calendar` is `setup: selected` and joins when provisioned.
  - Update `engineering/deployment/deployment.md` § Intake with the five sources and the `ocharo status` verb that prints their subscription ids.
  - Extend `{events-be}/tests/Events.Tests.Unit/Intake/EventsIntakeOptionsValidatorTests.cs` with a five-source configuration.
- Done when: `dotnet Events.Api.dll intake check` against a configuration with five sources prints five `subscription=ok|…` lines, and the validator test passes.
- Depends: —

### E02 Tighten ocharo-fashion-v1 against off-topic event matches
- Repo: wow-two-sdk-beta.harvest · Area: delivery filter · Type: fix
- Why: under `Classifier: filter` every match auto-publishes; `silk`, `ipak`, `designer`, `dizayn`, `accessor` plus any "event/show/expo" word pass off-topic posts.
- Do:
  - In `{harvest-be}/sources/Module/Ocharo/OcharoFashionFilter.cs`, add an exclusion regex checked after `Subject()`: `silk road`, `шёлков\w* пут`, `ipak yo['‘’ʻ]?li`, `interior`, `интерьер`, `mebel|мебел`, `auto|авто`, `UX|UI|graphic|web\s+design`, `marathon|марафон`, unless `NamedOpportunity()` also matches.
  - Narrow `accessor` and `jewel` to fashion context (`fashion|moda|мод|kiyim|одежд` within the same text).
  - Add negative `InlineData` rows to `{harvest-be}/tests/HarvestAdapters.Tests.Unit/Ocharo/OcharoSourcesTests.cs` `Filter_requires_subject_and_opportunity`: "Silk Road Samarkand Marathon", "Ipak yo'li xalqaro festivali", "UX Designer Meetup", "Auto accessories exhibition", "Interior dizayn ko'rgazmasi"; keep every existing positive row passing.
  - Bump `FilterKey` to `ocharo-fashion-v2` only if the change must not re-judge history; otherwise keep `v1` and note the change in `engineering/architecture/contract.md` § Source host.
- Done when: `dotnet test tests/HarvestAdapters.Tests.Unit --filter FullyQualifiedName~Ocharo` passes with the five new negative rows (all five return `true` today).
- Depends: —

### E03 Deliver post.unmatched when a seen post stops matching
- Repo: wow-two-sdk-beta.harvest · Area: delivery · Type: fix
- Why: a post that matched once and no longer matches (re-extracted, reclassified as article) sends nothing, so Events keeps it published.
- Do:
  - Add `DeliveryEventTypes.PostUnmatched = "post.unmatched"` in `{harvest-be}/packages/Abstractions/Delivery/DeliveryEventTypes.cs` and list it in `DeliveryPostFilters.IsLifecycle`.
  - In `{harvest-be}/packages/Module/Delivery/DeliveryEventWriter.cs:34-38`, when `subscription.Seen`, the previous record was not `post.unmatched`, and `filters.Matches` is now false, append one `post.unmatched` record with the post's identity and revision; a later match appends `post.changed` as today.
  - Mirror it in `{harvest-be}/packages/Testing/Delivery/FakeDeliveryBroker.cs` and `PostDeliveryBrokerConformance`.
  - Add golden page `{harvest-be}/tests/Contract/wow2.event.v1/10-unmatched.json` to the manifest and `engineering/architecture/contract.md` § Runs, posts and pull delivery.
- Done when: a `PullDeliveryTests` case (match → re-extract to an article → pull) yields `post.new` then `post.unmatched`, in both module and fake conformance runs.
- Depends: —

### E04 Hold events whose SCFD post stopped matching
- Repo: wow-two-sdk-beta.events · Area: intake · Type: fix
- Why: Events must drop an off-topic event from Ocharo's list when SCFD says its post no longer matches.
- Do:
  - In `{events-be}/packages/Module/Intake/IntakeProcessor.cs` `RecordAsync`/`ApplyLifecycleAsync`, treat `post.unmatched` like `gone`: an automatically reviewed, untracked event goes back to `Candidate` with `ReviewedBy = source:{instance}` and a new `UnmatchedReason`.
  - A later `post.changed` that passes the filter releases the hold (same branch as a `live` relist).
  - For a tracked event, keep it published and record the reason on its source row (surfaced by E15).
  - Add `IntakeLifecycleTests` cases for untracked, tracked and re-matched posts.
- Done when: `dotnet test tests/Events.Tests.Integration --filter FullyQualifiedName~IntakeLifecycle` passes with the three new cases.
- Depends: E03

## Facts shown wrong or missing

### E05 Show cancelled, postponed and online events as such
- Repo: ocharo-platform · Area: Events app · Type: fix
- Why: Events maps schema.org `eventStatus` and attendance, but Ocharo drops both, so a cancelled event looks live.
- Do:
  - Add `EventStatus` (`scheduled|cancelled|postponed|rescheduled|moved-online`) and `Attendance` (`offline|online|mixed`) to `{oe-be}/OcharoEvents.Domain/Events/Models/ShowcaseEvent.cs` and fill them in `EventsServiceMapper.ToShowcaseEvent` from `facts.Status` / `facts.Attendance`; keep them out of `HasSameFacts`.
  - Add both to `{oe-fe}/src/domain/events/Events.ts` (`ShowcaseEvent`, labels) and to the decoder in `{oe-fe}/src/integration/events/EventsApi.ts` (unknown values decode as `scheduled` / `offline`, never a protocol failure).
  - `EventCard.vue` and `EventDetail.vue`: a danger badge "Cancelled" (title struck through), a warning badge "Postponed"/"Rescheduled", an "Online" badge.
  - Exclude cancelled events from `EventsServiceRepository.GetSummaryAsync` upcoming deadlines.
- Done when: a unit test maps `EventStatus.Cancelled` + `EventAttendance.Online` to `cancelled`/`online`, and a vitest renders the Cancelled badge.
- Depends: —

### E06 Stop taking aggregator pages as the event website
- Repo: wow-two-sdk-beta.events · Area: intake mapping · Type: fix
- Why: SCFD marks every in-page link `site`, so `Website` becomes the aggregator's venue page (pinned by the golden test).
- Do:
  - In `{events-be}/packages/Module/Intake/ScfdEventMapper.cs:130`, take `Website` only from a `site` content link whose host differs from every `links[].url` host of the payload and is not a social, messenger or map host; otherwise leave it null.
  - Update `{events-be}/tests/Events.Tests.Unit/Intake/Contract/ScfdContractPagesTests.cs` `NewPost_ShouldMapEveryFactEventsReads` to expect `Website` null for `01-new.json`, and add a unit case where an external organizer site maps.
  - Rely on `ReviewBacklogAsync` to re-map stored auto-reviewed events; assert its `Remapped` count in an `IntakeAutoReviewTests` case.
- Done when: the contract-page and auto-review tests pass with the aggregator link rejected and an external site kept.
- Depends: —

### E07 Project application deadlines into wow2.event.v1
- Repo: wow-two-sdk-beta.harvest · Area: delivery projection · Type: feature
- Why: readers record deadlines only inside their `schemaOrg.{reader}` namespace, which no consumer reads.
- Do:
  - In `{harvest-be}/packages/Module/Extraction/EventSchemaMapper.cs`, add a top-level `deadlines` array `[{kind: "application", value, precision, raw}]` from `DateRole.Deadline` dates and from `schemaOrg.craftfair.applicationDeadline`, `schemaOrg.uzexpocentre.applicationDeadline` and `schemaOrg.afisha.applicationDeadlineEvidence.date` (ISO day; skip null).
  - Keep the reader namespace untouched; the projection only copies.
  - Add `{harvest-be}/tests/Contract/wow2.event.v1/09-deadline.json` (a Craftfair-shaped post) to the manifest; document the field in `engineering/architecture/contract.md` § Source host.
  - Unit test in `{harvest-be}/tests/Harvest.Tests.Unit/Extraction/` for each of the three reader shapes.
- Done when: the new unit test and `Harvest.Tests.E2E` `EventContractPages` pass with `deadlines` present on page 09.
- Depends: —

### E08 Map SCFD deadlines and time zones into event facts
- Repo: wow-two-sdk-beta.events · Area: intake mapping · Type: feature
- Why: with deadlines and zones mapped, Ocharo's "Deadlines first" lists sourced events and start times keep their zone.
- Do:
  - In `ScfdEventMapper.TryMap`, read `deadlines[]` into `facts.Deadlines` (`DeadlineKind.Application`, `EventWhen` with the given precision), at most `EventsConstants.MaxListLength`.
  - Add `DefaultTimeZone` (IANA, e.g. `Asia/Tashkent`) to `EventsIntakeSourceOptions`; set `facts.TimeZone` when the start value's offset equals that zone's offset on that date; otherwise leave it null.
  - Add the option to `deploy.yml` for every source (E01), default `Asia/Tashkent`.
  - Re-copy harvest's contract pages at the tag carrying E07 (`source.json`, `manifest.json`) and assert page 09's deadline in `ScfdContractPagesTests`.
- Done when: `Events.Tests.Unit --filter FullyQualifiedName~Intake` passes with page 09 mapping one application deadline and `01-new.json` mapping `TimeZone` `Asia/Tashkent`.
- Depends: E07

### E09 Show sourced ticket prices and ticket links
- Repo: ocharo-platform · Area: Events app · Type: feature
- Why: Events holds `Offers` and `TicketUrl`, but the card says "Cost not stated" for a ticketed event.
- Do:
  - Add `Tickets` (`{minPrice, maxPrice, currency, free}` from the first `OfferKind.Ticket` offer, else first offer) and `TicketUrl` to `ShowcaseEvent` and `EventsServiceMapper.ToShowcaseEvent`.
  - Keep Ocharo's `cost` (its own participation cost) separate; label it "Ocharo's cost" on the card.
  - `EventCard.vue`: a "Tickets" line ("from 150 000 UZS", "Free"); `EventDetail.vue`: the ticket link through `safeEventUrl`.
  - Extend the fe decoder and `EventsModel.test.ts`.
- Done when: a unit test maps a 150000 UZS ticket offer and a vitest renders "Tickets" with the amount while `cost` stays null.
- Depends: —

### E10 Show start time, address and organizer link on detail
- Repo: ocharo-platform · Area: Events app · Type: feature
- Why: minute-precision starts, addresses and organizer sites arrive from SCFD but Ocharo shows dates only.
- Do:
  - Add `StartsAt` (local `HH:mm` when `facts.Starts.Precision` is `Minute`), `TimeZone`, `Address` and `OrganizerWebsite` to `ShowcaseEvent` and the mapper.
  - `formatEventDates` in `{oe-fe}/src/domain/events/Events.ts`: append "19:00" (and the zone's short name when it differs from the browser's) for day-precision events with `startsAt`.
  - `EventDetail.vue`: address under the venue; organizer name links to `organizerWebsite` through `safeEventUrl`.
  - `EventCalendar.ts`: export a timed ICS event when `startsAt` exists.
- Done when: vitest shows "5 Dec 2026, 19:00" for the golden jazz event's facts and the ICS export carries `DTSTART;TZID=Asia/Tashkent:20261205T190000`.
- Depends: E08

### E11 Keep foreign cities out of the default country
- Repo: wow-two-sdk-beta.events · Area: intake mapping · Type: fix
- Why: `DefaultCountry` `UZ` stamps every record, so a foreign fair announced on a UZ source reads as a local event.
- Do:
  - Add `DefaultCities` (names in ru, uz Latin, uz Cyrillic and en) to `EventsIntakeSourceOptions`, validated in `EventsIntakeOptionsValidator`.
  - In `IntakeProcessor.TryFacts` (`IntakeProcessor.cs:508`), apply `DefaultCountry` only when the city is null or matches `DefaultCities` (case- and apostrophe-insensitive); otherwise leave the country null.
  - Ship a list of Uzbekistan's regional centres in `deploy.yml` defaults (Tashkent, Samarkand, Bukhara, Khiva, Namangan, Andijan, Fergana, Margilan, Kokand, Nukus, Karshi, Termez, Navoi, Jizzakh, Gulistan, Urgench), each spelling.
- Done when: a unit case maps `addressLocality` "Париж" to country null and "Ташкент" / "Toshkent" to `UZ`.
- Depends: —

### E12 Give sourced events a kind from their subscription
- Repo: wow-two-sdk-beta.events · Area: intake mapping · Type: feature
- Why: without AI every sourced event is `other`, so Ocharo's format badge and filter say nothing.
- Do:
  - Add `DefaultKind` to `EventsIntakeSourceOptions`; in `TryFacts` apply it when the mapped kind is `other`, no classifier kind is given, and the catalog's taxonomy contains it.
  - Set defaults in `deploy.yml`: `afisha-exhibitions` → `exhibition`, `uzexpocentre-exhibitions` → `trade-fair`, `craftfair-all` → `market`; leave `afisha-fashion` and `anons-events` unset.
  - A classifier's `kind` (the AI lane's `payload` classifier) keeps precedence; document the order in `product/product.md` § Intake.
- Done when: an `IntakeAutoReviewTests` case maps a kind-less record from a source with `DefaultKind: exhibition` to `exhibition`, and a payload `kind: runway` still wins.
- Depends: —

### E33 Show sourced city names in the app's script
- Repo: wow-two-sdk-beta.events · Area: intake mapping · Type: fix
- Why: Afisha's city arrives as `Ташкент` while curated events say `Tashkent`, so Ocharo's city filter and grouping
  split one city in two.
- Do:
  - Map known Uzbek city names from Cyrillic and Russian spellings to one canonical Latin name in `ScfdEventMapper`
    (`Place.City`), keeping the source spelling in the record's raw facts.
  - Keep a small table of the cities seen in SCFD fixtures and Ocharo's curated events; unknown names pass through.
  - Cover `Ташкент`, `Самарканд`, `Бухара` and an unknown city in `ScfdEventMapperTests`.
- Done when: the mapper tests pass and Ocharo dev shows one `Tashkent` group for curated and sourced events.
- Depends: —

## Edits, revisions and lifecycle in Ocharo

### E13 Stop stage changes answering 410 after SCFD revisions
- Repo: ocharo-platform · Area: Events app · Type: fix
- Why: Ocharo's revision tracks only its tracking row; after SCFD updates facts, a stale page's Shortlist gets 410 "moved".
- Do:
  - Add `PUT /api/organizations/{organizationId}/events/{eventId}/tracking` (`status`, `priority`, `notes`, `participation`, `cost`, `expectedRevision`) in `{oe-be}/OcharoEvents.Api/Events/Controllers/EventsController.cs`, a command and handler, and `EventsServiceRepository.UpdateTrackingAsync` that validates tracking fields only and never calls `HasSameFacts`.
  - Point `patchEvent` in `{oe-fe}/src/application/events/UseEvents.ts` and the tracking part of `EventDetail.vue` at the new route.
  - Add `EventRevision` (Events' `EventModel.Revision`) to `ShowcaseEvent`; the full `PUT` answers 409 when it differs from the page's, and 410 only for a real fact change.
  - Map 410 in `failureMessage` (`{oe-fe}/src/application/events/UseEventsAccess.ts:12`) and refresh the event on 410 as on 409.
- Done when: a unit test (fake bumps the event's facts after the page read, then Shortlist) answers 200, and a stale full `PUT` answers 409, not 410.
- Depends: —

### E14 Remove dead fact-edit and delete actions from the page
- Repo: ocharo-platform · Area: Events app · Type: fix
- Why: "Edit details" offers every fact and "Delete event" warns of deletion, but the backend answers 410 for both.
- Do:
  - In `{oe-fe}/src/presentation/events/EventDetail.vue:320-327`, drop "Delete event" and its `remove()`; "Edit details" opens a tracking-only form (status, priority, participation, cost, notes).
  - Split `EventForm.vue` so the create form (a member proposal) keeps the fact fields, and align its limits with the server's (`organizer` and `city` 200, from `eventLimits`).
  - Remove `DELETE …/events/{eventId}` from `EventsController` and `deleteEvent` from `EventsApi.ts`, or keep the route answering 410 with a test.
  - Update `EventsPage.test.ts` for the new actions.
- Done when: vitest finds no "Delete event" button and the edit form has no title or date fields for an existing event.
- Depends: E13

### E15 Expose source name, state and posted time on events
- Repo: wow-two-sdk-beta.events · Area: catalog model · Type: feature
- Why: Ocharo can't show "via Afisha", a removed listing or announcement time; Events drops context, state and `postedAt`.
- Do:
  - Add `Name`, `State` (`live|suspect|gone|unmatched`) and `PostedAtUtc` to `{events-be}/packages/Abstractions/CatalogEvents/EventSourceModel.cs` and columns to `EventSourceEntity` with a migration.
  - In `IntakeProcessor.ApplyPostAsync` / `ApplyLifecycleAsync`, fill `Name` from the record's `Context["sourceName"]` else `Context["sourceGroup"]` else the intake source's name, `State` from the payload `state` (and E04's unmatched), `PostedAtUtc` from `postedAt`.
  - Load them in `{events-be}/packages/Module/Tracking/EventModels.cs` and serialize through the client; extend `EventTrackingBrokerConformance`.
- Done when: replaying `05-lifecycle.json` leaves the post's event source with `State` `gone`, and conformance passes for module and client.
- Depends: E04

### E16 Show source attribution and listing state on cards
- Repo: ocharo-platform · Area: Events app · Type: feature
- Why: members need to know where an event came from and when its listing disappeared or changed.
- Do:
  - Add `Sources: [{name, url, state}]` and `SourceUpdatedAt` (event `UpdatedAtUtc` when later than the tracking's) to `ShowcaseEvent` and the mapper; re-pin `WoW2.Sdk.Beta.Be.Events.*` in `{oe-be}/Directory.Packages.props`.
  - `EventCard.vue`: "via {name}" linking the original; a warning badge "Listing removed at source" when every source is `gone` or `unmatched`.
  - `EventDetail.vue`: a sources list, and "Updated by source on {date}" for a tracked event.
  - Decoder and vitest updates.
- Done when: vitest renders "via Afisha Uzbekistan" and the removed-listing badge for an all-`gone` event.
- Depends: E15

## Duplicates

### E17 Attach cross-source duplicates to one event on intake
- Repo: wow-two-sdk-beta.events · Area: intake · Type: feature
- Why: once five sources flow, one fair (TITF on Afisha and Uzexpocentre) becomes two events in Ocharo.
- Do:
  - In `IntakeProcessor.ApplyPostAsync`, before `CreateCandidateAsync` (`IntakeProcessor.cs:338`), look for a published or candidate event in the catalog with a normalized equal title (case, punctuation, year and quotes stripped, or token overlap ≥ 0.8), overlapping `[StartsMin, EndsMax]` and the same city (or both null).
  - On a match, set `post.EventId` to it and add an `EventSourceEntity` with `MatchedBy = "rule:title-date-city"`; facts stay the first source's under automatic review.
  - Add a review action "split source" in the console and `IEventReviewBroker` that moves one source to a new candidate and records keep-apart.
  - Move the backlog row "Cross-source match proposals" in `engineering/planning/backlog.md` § Catalog to built.
- Done when: an integration test with two sources delivering "TITF 2026" on overlapping dates in Tashkent yields one event with two sources; a different city yields two events; split restores two.
- Depends: E01

### E18 Move tracking to the survivor when SCFD merges posts
- Repo: wow-two-sdk-beta.events · Area: intake lifecycle · Type: fix
- Why: a tracked duplicate stays published after SCFD merges its post, so Ocharo lists the event twice.
- Do:
  - In `ApplyLifecycleAsync` (`IntakeProcessor.cs:451`), on `mergedInto`, find the survivor post's event; for each organization tracking the duplicate, copy the tracking to the survivor when it has none there, else keep the later stage and append notes; write a tracking history entry.
  - Then hold the duplicate as today, tracked or not.
  - On unmerge, release the hold; leave copied tracking on the survivor and note it in `product/product.md` § Intake.
  - Add `IntakeLifecycleTests` cases for untracked, tracked-once and tracked-on-both.
- Done when: the tracked-duplicate case leaves one listed event with stage `shortlisted` in `IEventTrackingBroker.ListAsync`.
- Depends: —

## Scale and states

### E19 Let a subscriber list its tenant's subscriptions
- Repo: wow-two-sdk-beta.harvest · Area: delivery API · Type: feature
- Why: Events' service token (`harvest.events-read`) can't list subscriptions, so each new channel needs a deploy edit.
- Do:
  - In `{harvest-be}/packages/Hosting/Delivery/Controllers/SubscriptionsController.cs:31-45`, allow a service caller holding `events-read` to `GET api/subscriptions` for its own tenant only (from `ClientGrantsJson`), with an optional `context.catalog` query filter.
  - `OcharoSourceProvisioner` writes `sourceName` (group display name) and `country` (ISO-2 from the group's coverage, when one country) into new subscriptions' context; `ocharo setup --refresh` backfills existing ones.
  - Document both in `engineering/architecture/contract.md` § Runs, posts and pull delivery and § Source host.
- Done when: an E2E test lists exactly its tenant's five Ocharo subscriptions with an `events-read` client-credentials token, each with `sourceName`, and another tenant's are absent.
- Depends: —

### E20 Discover intake subscriptions instead of per-index settings
- Repo: wow-two-sdk-beta.events · Area: intake · Type: feature
- Why: the 100-source goal (#51) can't run on one `Events:Intake:Sources:N` block and deploy per subscription.
- Do:
  - Add `Events:Intake:Discovery:N` (`Name`, `BaseUrl`, token settings, `Catalog`, `ContextCatalog`, `OwnerOrg`, `Review`, `Classifier`, `Filter`, `DefaultTimeZone`) to `EventsIntakeOptions` and its validator.
  - `IntakePoller` lists the tenant's subscriptions each poll, derives one runtime source per subscription (`{discovery}/{subscriptionId}`, its own cursor row), `DefaultCountry` from context `country`, `DefaultKind` from a `KindByChannel` map; static sources keep working.
  - `intake check` prints one line per discovered subscription; `/api/system/status` lists them.
  - Move the backlog row "Several SCFD subscriptions per catalog" to built.
- Done when: an integration test with a fake listing of three subscriptions pulls all three with separate cursors, and a fourth that appears is pulled on the next poll without a restart.
- Depends: E19

### E21 Add country lists and untracked counts to tracking reads
- Repo: wow-two-sdk-beta.events · Area: tracking API · Type: feature
- Why: Ocharo's scope filter needs country sets and its summary needs an untracked count to stop scanning the catalog.
- Do:
  - Add `Countries`, `ExcludeCountries` and `IncludeUnknownCountry` to `{events-be}/packages/Abstractions/Tracking/TrackingQuery.cs`; apply them in `EventListQuery.Filter`.
  - Add `Untracked` (published events with no tracking for the caller's organization) to `TrackingSummaryModel`.
  - Carry both through the client's query string and `EventTrackingBrokerConformance`.
- Done when: `dotnet test tests/Events.Tests.Conformance` passes for module and client with the new filter and count cases.
- Depends: —

### E22 Filter, page and summarize in Events, not in memory
- Repo: ocharo-platform · Area: Events app · Type: engineering
- Why: each page load reads the whole catalog twice and fails past 10,000 events (`MaximumPages` 50 × 200).
- Do:
  - `EventsServiceRepository.GetEventsAsync` sends one `TrackingQuery` (`Text`, `From`, `To`, `Kind`, `Stage`, scope → `Countries`/`ExcludeCountries`, `Cursor`, `Limit`) instead of `LoadAsync` + `Matches`.
  - `GetSummaryAsync` uses `IEventTrackingBroker` summary (by stage, upcoming deadlines, `Untracked` as `candidate`).
  - Replace `offset` with a `cursor` on `GET …/events`; `{oe-fe}/src/application/events/UseEvents.ts` `useEventList` loads more pages ("Show more") instead of the 200-row cap note in `EventsFeed.vue`.
  - Drop `MaximumPages` and the "more pages than this service reads" error.
- Done when: an E2E test with a fake of 1,000 events makes one Events call per list request and one per summary, and the second page arrives by cursor.
- Depends: E21

### E23 Let catalog members read intake freshness
- Repo: wow-two-sdk-beta.events · Area: intake API · Type: feature
- Why: Ocharo members can't tell a quiet day from a stalled SCFD pull; intake status needs `events.admin`.
- Do:
  - Add `GET api/events/v1/catalogs/{catalog}/freshness` (`events.read` + `events:read` in the owner organization) answering `{lastReceivedAtUtc, newestObservedAtUtc, failingSources}` over the catalog's intake cursors; no cursor values or error text.
  - Add it to `IEventIntakeBroker` (or a new broker), the client and `EventIntakeBrokerConformance`.
  - Another organization's call answers 404, as for catalogs.
- Done when: conformance passes and an E2E test shows a member token reading freshness while another organization gets 404.
- Depends: —

### E24 Show error, empty and stale states with retry
- Repo: ocharo-platform · Area: Events app · Type: fix
- Why: a failed list shows only a toast over an empty page; an unconfigured or unreachable Events gives the generic message.
- Do:
  - `{oe-fe}/src/presentation/events/EventsFeed.vue`: when `list.error` and no rows, an inline panel with a status-specific message (503 "Events isn't configured for this service", 502/504 "WoW2 Events is unreachable") and a Retry button calling `list.refetch`.
  - Add `GET /api/organizations/{organizationId}/events/freshness` in the Ocharo API over E23; show "Sources updated {relative time}" under the page title, and a warning when older than 24 hours or any source fails.
  - Empty state for a catalog with no events: "No sourced events yet; sources sync every few minutes."
  - Vitest cases for error-without-data, 503 and stale freshness.
- Done when: the three vitest cases pass and Retry re-issues the list request.
- Depends: E23

### E25 Prefer UI-locale titles and show the title language
- Repo: ocharo-platform · Area: Events app · Type: feature
- Why: titles arrive keyed `ru-Cyrl` / `uz-Latn`; Ocharo's `und, en, uz, ru` order never matches them.
- Do:
  - `EventsServiceMapper.Title` takes the request's UI locale (`Accept-Language` from `{oe-fe}/src/application/shared/UseUiLocale.ts`) and matches by language prefix (`uz` → `uz-Latn`, then `uz-Cyrl`), then `und`, `en`, then any.
  - Add `TitleLanguage` and `Languages` to `ShowcaseEvent`; `EventCard.vue` shows a small "RU"/"UZ" tag when the title's language differs from the UI's.
  - Unit and vitest cases.
- Done when: a unit test with titles `{ru-Cyrl, uz-Latn}` returns the `uz-Latn` title for UI `uz` and `TitleLanguage` `uz-Latn`.
- Depends: —

## Tests and verification

### E26 Ship a conformance-tested in-memory Events fake
- Repo: wow-two-sdk-beta.events · Area: testing package · Type: engineering
- Why: consumers hand-write fakes (Ocharo's `FakeEventsService`) that no conformance suite checks.
- Do:
  - Add `InMemoryEventsBrokers` to `{events-be}/packages/Testing` implementing `ICatalogEventsBroker` and `IEventTrackingBroker` (review states, cursors, tracking revisions, organization scoping).
  - Run `CatalogEventsBrokerConformance` and `EventTrackingBrokerConformance` against it in `tests/Events.Tests.Conformance`.
  - Publish it with the next NuGet release; note it in `engineering/architecture/contract.md`.
- Done when: `dotnet test tests/Events.Tests.Conformance` passes for module, client and in-memory.
- Depends: —

### E27 Pin Ocharo's mapper to SCFD-shaped Events records
- Repo: ocharo-platform · Area: Events app tests · Type: engineering
- Why: Ocharo's 61 unit tests use hand-made events; none has a `ru-Cyrl` title, minute start, offer or cancelled status.
- Do:
  - Add `{oe-be}/tests/OcharoEvents.Tests.Unit/ScfdShapedEventsTests.cs` building `TrackedEventModel`s from the facts Events maps for its golden pages `01-new.json` and `07-afisha-place.json`, plus a cancelled variant, asserting every `ShowcaseEvent` field.
  - Replace `tests/OcharoEvents.Tests.Unit/FakeEventsService.cs` and `tests/OcharoEvents.Tests.E2E/Harness/FakeEventsService.cs` with E26's in-memory brokers; re-pin `WoW2.Sdk.Beta.Be.Events.*`.
- Done when: `dotnet test tests/OcharoEvents.Tests.Unit` and `tests/OcharoEvents.Tests.E2E` pass with both hand-written fakes deleted.
- Depends: E26

### E28 Replay SCFD's new golden pages in Events
- Repo: wow-two-sdk-beta.events · Area: intake tests · Type: engineering
- Why: Events' contract pages stop at harvest `v0.1.14`; deadlines and `post.unmatched` need pinned wire pages.
- Do:
  - Re-copy `{harvest-be}/tests/Contract/wow2.event.v1` at the harvest tag carrying E03 and E07 into `{events-be}/tests/Events.Tests.Unit/Intake/Contract/`, updating `source.json`.
  - Extend `ScfdContractPagesTests` and `Events.Tests.Integration/Intake/ScfdContractReplayTests.cs` for pages 09 (deadline) and 10 (unmatched → held).
- Done when: `Manifest_ShouldMatchEveryCopiedFile_ByteForByte` and the replay test pass at the new tag.
- Depends: E03, E07

### E29 Run a local SCFD → Events → Ocharo smoke
- Repo: ocharo-platform · Area: verification · Type: engineering
- Why: no test drives one record through all three services; each repo stops at its own fake or golden page.
- Do:
  - Add `engineering/scripts/events-e2e-smoke.sh` starting local builds of the SCFD host, Events and the Ocharo Events app with the platform's local Identity from `engineering/deployment/docker-compose.yml`, on the local PostgreSQL.
  - Run `ocharo setup --group afisha` on SCFD, ingest one fixture capture through the operator capture route, run Events' `intake poll`, then read `GET /api/organizations/{id}/events` with a signed-in test session.
  - Assert title, start date, city, source link and `status` `candidate`; stop every container it started, by name.
  - Document it in `engineering/deployment/deployment.md` § Checks.
- Done when: the script exits 0 and prints the event's title, dates, city and source link, with no container left running.
- Depends: E01

### E30 Run harvest tests on the workspace SDK
- Repo: wow-two-sdk-beta.harvest · Area: build · Type: engineering
- Why: `global.json` pins SDK `10.0.400`; with `10.0.300` installed, `dotnet test` in the repo fails before building.
- Do:
  - Lower `{harvest-be}/global.json` to `10.0.300` with `rollForward: latestFeature` (Events pins `10.0.300`); the delivery, adapter and contract tests built and passed on `10.0.300` when run from outside the repo.
  - If `10.0.400` is required, record why and the install step in `engineering/development/development.md`.
- Done when: `dotnet test tests/Harvest.Tests.Unit` run from `{harvest-be}` on a machine with only SDK `10.0.300` builds and passes.
- Depends: —

## Product

### E31 Add a triage view for untracked sourced events
- Repo: ocharo-platform · Area: Events app · Type: product
- Why: at five-plus sources, every published record lands as "New — review" in one long feed.
- Do:
  - Add a "New" view (`/organizations/{id}/events?view=new`) listing untracked published events, newest `postedAt` first, with a count badge in the nav.
  - Bulk Shortlist / Skip through E13's tracking route; keyboard shortcuts S / K.
  - Remember each member's last triage time in Ocharo's own schema (`ocharo_events`), migration `002-triage`.
- Done when: vitest selects three events, presses Skip, and the three leave the view after one bulk request each.
- Depends: E13, E15, E22

### E32 Decide a per-source policy for event thumbnails
- Repo: wow-two-sdk-beta.events · Area: intake policy · Type: product
- Why: images are dropped for every source, though only Afisha's terms forbid showing them (#32); organizer sites may allow it.
- Do:
  - Add `MediaPolicy` (`none` default, `reference`) to `EventsIntakeSourceOptions`; under `reference`, map `media[kind=image]` to `facts.Images` as `{Url, SourceUrl, Attribution}` with no bytes copied.
  - Record the policy and which sources may use `reference` in `product/product.md` § Intake (never Afisha); keep `none` for all sources until the owner picks.
  - Ocharo shows a thumbnail with attribution when `Images` is non-empty (follow-up in `ocharo-platform`).
- Done when: a unit test maps a Craftfair-shaped page to one image reference under `reference` and `01-new.json` to none under `none`.
- Depends: —

## Appendix: local test runs (2026-11-16)

| Repo | Command (from the repo's backend root unless noted) | Result |
|---|---|---|
| events | `dotnet test tests/Events.Tests.Unit --filter FullyQualifiedName~Intake` | 37 passed |
| events | `dotnet test tests/Events.Tests.Integration --filter FullyQualifiedName~Intake` | 43 passed |
| ocharo-platform | `dotnet test tests/OcharoEvents.Tests.Unit` | 61 passed |
| ocharo-platform | `dotnet test tests/OcharoEvents.Tests.E2E --filter "FullyQualifiedName~EventsServiceRoute\|FullyQualifiedName~Access"` | 13 passed |
| ocharo-platform | `pnpm exec vitest run` in `{oe-fe}` | 7 files, 73 passed |
| harvest | `dotnet test tests/Harvest.Tests.Unit --filter "FullyQualifiedName~Delivery\|FullyQualifiedName~EventSchema\|FullyQualifiedName~RulesPostExtractor"` (run outside the repo, SDK `10.0.300`) | 24 passed |
| harvest | `dotnet test tests/HarvestAdapters.Tests.Unit --filter FullyQualifiedName~Ocharo` (same) | 29 passed |
| harvest | `dotnet test tests/Harvest.Tests.Integration --filter FullyQualifiedName~PullDelivery` (same) | 8 passed |
| harvest | `dotnet test tests/Harvest.Tests.E2E --filter FullyQualifiedName~EventContractPages` (same) | 1 passed |

- Inside the harvest repo, every `dotnet test` stops on "compatible SDK not found" (`global.json` `10.0.400`), E30.
- Events' golden pages match harvest's current `tests/Contract/wow2.event.v1` byte for byte (copied from `v0.1.14`).
- The filter probe (E02) ran the `ocharo-fashion-v1` regexes in Python: all five off-topic titles matched.
- Missing coverage: no test crosses two repos at runtime (E29); Ocharo's fakes are unchecked (E26, E27); no golden page
  covers deadlines, `post.unmatched` or cross-source duplicates (E17, E28).

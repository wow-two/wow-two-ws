# Ocharo events logic: read-only review

*2026-11-19. Read-only: code at `ocharo-platform` `e01da3c` (`v0.3.17`), `wow-two-sdk-beta.events` `3597efc`
(`v0.1.17`, NuGet `10.0.11-beta`, `fe-events` `0.0.6`), `wow-two-sdk-beta.harvest` `bbda3c2` (`v0.2.28`, plus another
lane's uncommitted Sources work, not read). Dev data: read-only `SELECT`s on `events_dev`, `harvest_dev` and `ocharo_dev`
through the dev host's product PostgreSQL. No edits, commits or deploys.*

Path roots:

- `{oe-be}` = `ocharo-platform` `engineering/codebase/ocharo-events.backend-services`
- `{oe-fe}` = `ocharo-platform` `engineering/codebase/ocharo-events.frontend-services/apps/web/src`
- `{ev}` = `wow-two-sdk-beta.events` `engineering/codebase/events.backend-services/packages`
- `{h}` = `wow-two-sdk-beta.harvest` `engineering/codebase/harvest.backend-services/packages`
- `tasks/` = `wow-two-ws` `system/sessions/events-integration/tasks/`

## Verdict

The display layer caught up fast (E05, E09, E10, E13, E14, E16, E25, E33, O17 all shipped since 11-16). The logic around
it still has three gaps that a member of Ocharo's team would notice first:

1. **Relevance runs backwards.** SCFD's AI already rates 3 of the 4 sourced events on dev `irrelevant` (0.90–0.95),
   but Events publishes on `Classifier: filter` and ignores that verdict. One of them, CAEx Build & Co (a construction
   expo), went out in the 11-17 Telegram digest. At the same time, 13 posts that passed `ocharo-fashion-v1` on the anons,
   caex and uzexpocentre subscriptions never reach Ocharo, because Events pulls only the two Afisha subscriptions. Those
   13 include Visa Fashion Week SS'27, TFT Expo, Texworld, Apparel Sourcing Tashkent, UZCHARMEXPO and Viza Fashion
   Week.
2. **The team can neither add nor remove an event.**
   - "Add event" creates an Events candidate. The tracking list returns only published events, and no Ocharo role can
     accept a candidate inside the app. So the new event never appears in the feed.
   - "Skip" changes only Ocharo's stage. A skipped event stays in the feed and stays eligible for the Telegram digest.
3. **SCFD's event entities have no way into Ocharo.**
   - `wow2.event.v1` carries no entity id.
   - Entity reads need `posts:read`, but Events' client holds only `harvest.events-read`.
   - Events has no series or occurrence model.
   - So the 9 fashion entities on dev never reach Ocharo. That includes TFT Expo (semiannual, next edition predicted
     2027-01-25) and Uzbekistan Fashion Week (bound across afisha and uzexpocentre). The 18 curated events with
     `estimated` dates cannot be confirmed by them.

A further gate applies before any of this reaches the team: on dev, Ocharo has one member (the owner, one Telegram link),
and prod has no Events app at all (`events_prod` holds no tables; O13–O16 are parked with the developer).

## Dev snapshot (2026-11-19, read-only)

| Fact | Value |
|---|---|
| Events catalog `ocharo-fashion` | 72 published, 0 candidates, 0 rejected; 68 imported, 4 sourced (all Afisha) |
| Kinds | trade-fair 24, runway 16, competition 9, exhibition 9, festival 9, market 5 (no `other` left) |
| Dates | 50 upcoming, 8 past, 10 undated, 4 others still running |
| Tracking (68 rows, all imports) | stage `candidate` 64 (of which high 5, normal 38, low 21), `applying` 1, `skipped` 3; the 4 sourced events are untracked |
| Deadlines | 9 in the catalog, 3 still open |
| Member proposals | 0 (`events_event_sources` kinds: `import` 68, `scfd` 4) |
| Newest sourced event | created 11-16 (CAEx Build & Co); both intake cursors were updated 11-19 16:50Z; observations accepted up to 11-19 15:50Z |
| SCFD AI verdict in the payloads Events stores | Fashion Show Line `relevant` 0.92 (`runway`); Tsereteli exhibition `irrelevant` 0.90; Yalt-Yult museum `irrelevant` 0.90; CAEx Build `irrelevant` 0.95; all four published by `classifier:filter:ocharo-fashion-v1` |
| Digest | one: "Ocharo tadbirlari", `uz-Latn`, Monday 09:00 Tashkent, new + starting ≤ 30 days + deadline ≤ 14 days, `role:member`, next run 11-23 04:00Z; one manual run 11-17: 10 events, 2 of them sourced (CAEx Build included); deliveries `sent` 1, `not_linked` 1 |
| SCFD subscriptions with `ocharo-fashion-v1` on harvest-dev | afisha fashion and exhibitions (pulled by Events); anons events-ru, uzexpocentre exhibitions, caex calendar (no consumer) |
| `post.new` that passed the filter | afisha/exhibitions-ru 3, afisha/fashion 1, anons 4, caex 3, uzexpocentre 6 |
| SCFD event entities | 9, one container, all `style-fashion/*`; cadence semiannual 1, unknown 8; 10 real occurrences, 0 predicted rows |
| Ocharo Identity on dev | 1 organization, 1 membership (owner), 1 Telegram link |

The 17 posts that passed the filter, with SCFD's English title and AI primary domain:

- **Relevant, never reached Ocharo:**
  - Visa Fashion Week SS'27 (anons, `style-fashion`; already curated, so it would duplicate)
  - TFT EXPO (caex)
  - Texworld Tashkent (uzexpocentre, apparel industry)
  - Apparel Sourcing Tashkent (uzexpocentre)
  - UZCHARMEXPO EURASIA (uzexpocentre, beauty)
  - Viza Fashion Week (uzexpocentre)
  - Textile Equipment exhibition (uzexpocentre)
  - Heimtextil Uzbekistan (uzexpocentre, interior)
- **Off-topic, which the regex would also pass if E01 went live alone:**
  - circus festival "Great Silk Road" (anons)
  - furniture sale at Artikul32 (anons)
  - Tourism on the Silk Road fair (caex)
  - CAEx Baraka Friday (caex)
- **Off-topic, already in Ocharo:** Tsereteli exhibition, Yalt-Yult museum exhibition, CAEx Build & Co (all afisha
  exhibitions-ru).

## 1. How an event enters Ocharo

### Works

- **Curated imports:** the 68 Desk-era events came in through Events' `import` host verb on 11-10 and reconcile 68 of
  68. `events_import_map` keeps every legacy id (events-integration #13 (c)).
- **Sourced pull:** Events pulls two SCFD subscriptions every 5 minutes, deduplicates each delivery, keeps a post's
  highest revision and commits its cursor in one transaction. Sourced events are keyed by (instance, catalog, post)
  (`{ev}/Module/Intake/IntakeProcessor.cs:328-352`).
- **Review policy:** `auto` with `filter` publishes every delivered record (`{ev}/Module/Intake/IntakeVerdict.cs:34-35`;
  events `engineering/deployment/deploy.yml:88-90`).
- **Lifecycle:** a post that goes `gone` before its event, is merged, or is `unmatched` sends an untracked,
  auto-reviewed event back to `candidate`, and it leaves the feed (E04 `aa86028`). Tracked events stay published.
- **Mapping fixes shipped:** E06 (aggregator website), E08 (deadlines, time zone), E11 (foreign city), E12
  (`DefaultKind`), E33 (Latin city names), E15 (source name, state, posted time), and SCFD's `estimated` certainty
  (`3597efc`).

### Broken, missing or inconsistent

- **SCFD's AI verdict is ignored.**
  - Every sourced payload now carries `classification` from `model:anthropic/claude-haiku-5-5@post-tags:1`.
  - The `filter` classifier still counts every record as relevant (`IntakeVerdict.cs:34-35`).
  - Result: 3 of 4 published sourced events are AI-irrelevant (dev snapshot).
  - The regex never "un-matches" them either, because E03's `post.unmatched` fires only when a post's own revision
    stops matching. So E04 never removes them.
  - Covered by: A07 (switch to `payload`, gated on a shadow week and the developer's word; `tasks/tasks-platform.md`
    A07). The subscription selector design changes A07 to "Events stays on filter" (`subscription-modes.md` §4). E02
    (regex stopgap, still open in harvest's backlog) does not touch history.
- **Three provisioned subscriptions have no consumer.**
  - anons, uzexpocentre and caex subscriptions exist on harvest-dev, but Events' `deploy.yml` binds only
    `Sources:0..1` (events `deploy.yml:72-155`).
  - Uzexpocentre and craftfair are also where SCFD finds application deadlines (E07), so the "Deadlines first" panel
    stays nearly empty: 3 open deadlines.
  - Covered by: E01, held behind #68 and superseded by the selector design (§2.8). E20 is mostly superseded too.
- **Member proposals become invisible.**
  - `CreateEventAsync` proposes a candidate (`{oe-be}/OcharoEvents.Infrastructure/Events/Services/EventsServiceRepository.cs:89-105`
    calls `ICatalogEventsBroker.ProposeAsync`, which enters `Candidate`: `{ev}/Module/CatalogEvents/ModuleCatalogEventsBroker.cs:74-75`).
  - The tracking list reads `PublishedEvents` only (`{ev}/Module/Tracking/ModuleTrackingBroker.cs:45`).
  - The proposal therefore shows on its detail page (owner `GetAsync`) and never in the feed.
  - Client 11 holds `events.read`, `events.track` and `events.admin` but not `events.review`
    (`ocharo-platform` `engineering/deployment/deploy.yml:452-454`). Only the separate Events console can accept the
    proposal. Events' rule: "publishes only when a reviewer accepts it" (events `product/product.md:140-141`).
  - Ocharo's `IsVisible` accepts `Candidate` (`EventsServiceMapper.cs:33-34`), which only the single-event read can
    hit.
  - Latent: 0 proposals on dev so far. Covered by: none.
- **No cross-source or curated-vs-sourced dedup.**
  - Identity is the SCFD post only. A curated event and its sourced twin, such as Visa Fashion Week SS'27 (curated,
    and posted on anons), become two events once anons is pulled.
  - SCFD's entity layer already binds posts across sources (Uzbekistan Fashion Week: afisha + uzexpocentre; The
    Fashion Show Line: afisha + anons), but nothing reaches Events.
  - Covered by: E17 (title-date-city rule; depends on E01), V03 (proposals, depends on V02), E18 (tracking moves on
    SCFD merge).
- **No path for SCFD's entities.**
  - `wow2.event.v1` carries no entity id: `EventSchemaMapper.cs` and `Module/Delivery` have no entity field.
  - Entity routes need `posts:read` (`{h}/Hosting/Entities/Controllers/EntitiesController.cs:30`, `:48`, `:68`, `:89`,
    `:112`; `{h}/Abstractions/Tenants/HarvestScopeConstants.cs:28`, `:37`), and client 8 holds only
    `harvest.events-read` (`ocharo-platform` `deploy.yml:406`).
  - Entities are per SCFD container and their change feed is container-wide (`{h}/Module/Migrations/014-entities`).
    "A subscription choosing posts, entities or both waits for S09" (harvest `engineering/planning/backlog.md:117`).
  - Events has no series or occurrence model (P2 in events `product/product.md:206-208`).
  - Covered by: none. Entity model #7 (event identity) and #8 (two feeds) are still proposed.

## 2. Lifecycle and Ocharo's workflow

### Works

- **Stages:** 8 Ocharo stages (`candidate` … `rejected`) in Events' workflow (`{oe-be}/…/EventValidationService.cs:19-20`).
  An untracked event reads as `candidate` (`EventsServiceMapper.cs:80`).
- **Stage writes:** stage, priority, notes, participation and cost go through the tracking-only route, so an SCFD
  revision no longer refuses a stage change (E13 `bb86d1f`). The dead fact-edit and delete actions left the page (E14).
- **Cancellations:** cancelled, postponed and online events are badged; a cancelled title is struck through and leaves
  "upcoming deadlines" (E05, `EventsServiceRepository.cs:66-68`).
- **Deadlines:** the summary lists the 5 nearest open application deadlines with days left.

### Broken, missing or inconsistent

- **"Candidate" means two things.** Events' review `candidate` is held and invisible; Ocharo's stage `candidate` is
  "untracked or untriaged" and is labelled "New — review" (`{oe-fe}/presentation/events/EventCard.vue:86`). So 64
  imports from 11-10 still read "New — review".
  - Covered by: E31 (triage view; needs the developer).
- **Skip never removes anything.**
  - The feed shows every stage by default (`{oe-fe}/presentation/events/EventsFeed.vue:72-78`).
  - The digest selects on Events' event `Status` (scheduled, cancelled …), not on the organization's tracking stage
    (`{ev}/Module/Digests/DigestDrafter.cs:83-87`, `:101-106`), so a skipped event still goes out.
  - Covered by: none.
- **No reminders tied to Ocharo's own work.** Nothing reminds about a shortlisted or applying event's deadline, apart
  from the weekly digest's `deadlineWithinDays` 14, which ignores stage. Empty digest runs already send nothing
  (`{ev}/Module/Digests/DigestRunner.cs:222-224`), so a daily reminder digest is cheap once stages filter.
  - Covered by: V05 (`deadline.approaching` webhooks, for products, not people). Otherwise none.
- **No assignee.** Events tracking has `assignee` (`{ev}/Module/Tracking/TrackingRules.cs`); Ocharo never sends or
  shows it.
  - Covered by: none.
- **Past events never close.** 8 past events keep their stage; the feed hides them unless "Show past events" is on.
  Nothing prompts attended or skipped.
  - Covered by: none.
- **Custom fields are free JSON.** Participation and cost live in free JSON `fields`; V04 would validate them.

## 3. What the app shows

### Works

- Month-grouped feed with undated events last; search over title, organizer, city, venue, country and key; scope chips;
  format and status filters with counts; a past-events toggle.
- **Dates:** honest precision ("≈ March 2027 (expected)" for estimates), the start time with its zone, ICS export (E10).
- **Facts:** ticket price and link apart from Ocharo's cost (E09); address and organizer link (E10).
- **Source:** "via {source}" on cards, a per-source state list, and "Listing removed at source" (E16).
- **Language:** titles follow the UI locale by language prefix, with a title-language badge (E25). Cities read in one
  Latin spelling (E33).

### Broken, missing or inconsistent

- **Sourced titles are Russian Cyrillic only.**
  - SCFD's tagging pass writes an English title (`harvest_post_tags.title_en`), but `wow2.event.v1` does not carry it
    (no `titleEn` in Events' stored payloads).
  - Ocharo's `uz` and `en` readers, and the `uz-Latn` digest, show Russian.
  - The digest's title fallback tries `uz-Latn`, `uz`, `und`, `en`, `ru`, then any (`{ev}/Module/Digests/DigestText.cs:49-58`),
    so `ru-Cyrl` is reached only as "any".
  - Covered by: none. E25 and E33 handle keys and cities, not translation.
- **Source label shows the group handle.** Cards read "via afisha", not a display name; the source name falls back to
  the subscription's `sourceGroup`.
  - Covered by: E19, which the selector design changes (provenance into the payload).
- **No images or description.** By design: #32, #50, `ScfdEventMapper.cs:11`. The per-source thumbnail policy waits
  for the developer (E32).
- **Sorting is fixed.** Start date, then title (`EventsServiceRepository.cs:50-54`). There is no "recently added", "by
  deadline" or "by priority" sort.
- **Filters are missing.** No priority, city, source (curated or sourced), has-deadline or tracked/untracked filter.
  - Covered by: E21 and E22 (server-side filters), partly. E31 covers "new".
- **Scope is inconsistent.**
  - It is derived from country: no country reads `international` (`EventsServiceMapper.cs:174-179`).
  - The create form asks for a scope (`{oe-fe}/presentation/events/EventForm.vue:105`), but `ToFacts` drops it
    (`EventsServiceMapper.cs:96-114`). A proposal marked "local" with no country reads "international".
  - Covered by: none.
- **Paging is capped in memory.**
  - The list reads the whole catalog twice per page load, filters in memory, caps at 200 ("Showing the first 200",
    `EventsFeed.vue:260-262`), and fails past 50 × 200 (`EventsServiceRepository.cs:33`, `:176-198`).
  - There is no error panel or freshness line.
  - Covered by: E22 (paging), E23 and E24 (freshness, error states).

## 4. Delivery

### Works

- **Digests (V07 + O17):** organization admins edit digests in the app through the fe-events `DigestsPanel`, mirrored
  under the organization (`{oe-be}/OcharoEvents.Api/Delivery/Controllers/DigestsController.cs:20`, admin check
  `:74-75`).
- **Defaults:** weekly Monday 09:00 Tashkent; new since the last run, plus starting within 30 days, plus a deadline
  within 14 days; `uz-Latn`; `role:member` (`{oe-fe}/domain/delivery/TelegramDelivery.ts:45`).
- **Runs:** each occurrence runs once; empty runs send nothing; deliveries go through Identity's notices with
  `sent`/`not_linked`/`muted`/`failed`.
- **Read-back:** the 11-17 manual run on dev delivered one message.

### Broken, missing or inconsistent

- The digest cannot leave out events Ocharo skipped or rejected, and cannot pick stages (`DigestDrafter.cs:83-106`).
  So a weekly digest repeats skipped events, and a deadline reminder for shortlisted or applying events is not
  expressible.
- Off-topic sourced events go out. The 11-17 run sent CAEx Build & Co: root cause in #1.
- Titles in the `uz-Latn` digest are Russian for sourced events (#3).
- Nothing else notifies: no in-app notices, email or webhooks (V05 open).
- Recipients on dev: one member. The team is not on dev, and prod has no Events (O13–O16 parked).

## 5. Organization scoping, permissions and the wire

### Works

- **Access filter:** the route's organization must be the session's active one, with `events:read`. Anything else
  answers 404 (`{oe-be}/OcharoEvents.Api/Access/Filters/OrganizationAccessFilter.cs:45-52`).
- **Tracking writes:** need `events:track` (`EventService.cs:106-109`); digests need `events:admin`.
- **Token exchange:** every Events call exchanges the person's token, so Events re-checks scope and permission and
  keys tracking by (issuer, organization).
- **Catalog and intake:** the catalog is private to Ocharo's organization, and each intake source pins `OwnerOrg`.
- **Roles:** owner and admin hold `events:read/track/review/admin`; editor holds read and track; viewer holds read
  (`ocharo-platform` `deploy.yml:271-281`).

### Broken, missing or inconsistent

- **Reviewer permission without a route.** `events:review` is granted to owner and admin, but client 11 cannot carry
  it (no `events.review` scope). In-app, nobody can accept a proposal or reject an event; only Events' own console can.
- **The app still reads through the Desk-era wire.**
  - The controller keeps "the routes and wire Desk served" (`EventsController.cs:14`).
  - `EventsServiceMapper` maps each `TrackedEventModel` to `ShowcaseEvent`.
  - The page revision is the tracking revision + 1 (`EventsServiceMapper.cs:89-93`).
  - `offset` paging and in-memory filters remain.
  - The source link is read from the import's tracking JSON (`EventsServiceMapper.cs:76`).
  - A full `PUT …/events/{id}` with a `HasSameFacts` check, unused by the UI, still exists
    (`EventsController.cs:95-112`, `EventsServiceRepository.cs:112-139`); `DELETE` answers 410
    (`EventsController.cs:134-150`).
  - Every new fact so far needed four edits: `ShowcaseEvent`, the mapper, the fe decoder and `Events.ts` (commits
    `13d535f`, `565ce12`, `755b5c7`, `eec660d`).
  - Meanwhile fe-events `kit` ships `EventsFeed`, `EventCard`, `EventDetail`, `TrackingForm`, `EventProposalForm`,
    `EventsDeadlines` and `FailureNotice`. The digest page already embeds fe-events through a pass-through mirror.
    Events-adoption #8 recorded the intent: "The fe package replaces the screens only once it matches the month feed,
    deadlines, detail and tracking form".
  - Covered by: none as a task. E22 and E27 touch parts.
- **The feature doc is stale.** `ocharo-platform` `product/features/events.md` (2026-10-08) still describes "Desk
  Events" and "Feed import".

## Coverage check of shipped and specced tasks

- **Shipped since 11-16:**
  - Events: E00, E04, E06, E08, E11, E12, E15, E33, V07.
  - Harvest: E03, E07, S-tasks per #69.
  - Ocharo: E05, E09, E10, E13, E14, E16, E25, O17.
  - Identity: I01.
- **Open and still right:** E17, E18, E21, E22, E23, E24, E26, E27, E28/E29, V02–V06, O13.
- **Open and held:**
  - E01, E19, E20 (selector #68).
  - A07 (shadow week + the developer).
  - E31, E32 (the developer).
  - O14–O16 (prod, the developer).
- **E02 (harvest):** a regex stopgap; it re-judges no history. OE01 below makes it unnecessary for Ocharo.

## Proposed tasks, ranked by user value for Ocharo's team

New ids use `OE` (Ocharo events). Existing specced tasks appear in the ranking by id, with any amendment. Hold marks:
**[held: selector]** waits on the subscription selector design (#68, point 1); **[held: entities]** waits on the
entity model (`ideas/scfd-entity-model.md` #7/#8); **[developer]** needs the developer's word.

Ranking:

| # | Task | Repo | Hold |
|---|---|---|---|
| 1 | OE01 Hold sourced events SCFD's AI marks irrelevant | events | [developer] (A07's switch gate) |
| 2 | OE02 Pull the three Ocharo subscriptions already provisioned on dev | events | [held: selector], ask to un-hold as interim |
| 3 | E17 Attach cross-source duplicates (amended: before OE02 goes live) | events | — |
| 4 | OE03 Show a member's proposal in the feed at once | events | orchestrator pick; reverses `product.md:140` |
| 5 | OE04 Select digest events by the organization's tracking stage | events | — |
| 6 | OE05 Leave skipped events out of the feed and digest; add a deadline reminder | ocharo-platform | — |
| 7 | OE06 Carry SCFD's English title to Events and Ocharo | harvest + events | — |
| 8 | E23 + E24 Freshness and error states (re-ranked up) | events, ocharo-platform | — |
| 9 | OE07 Read Events through fe-events; retire the Desk-era wire | ocharo-platform (+ events for kit gaps) | — |
| 10 | OE08 Stop discarding the scope picked for a new event | ocharo-platform | — |
| 11 | OE09 Bind sourced events to SCFD's event entity | harvest + events | [held: entities] |
| 12 | OE10 Show the expected next edition from SCFD's cadence | events + ocharo-platform | [held: entities] [held: selector] |
| 13 | E31 Triage view (minimal slice: "new since my last visit") | ocharo-platform | [developer] |
| 14 | OE11 Assign a teammate to a tracked event | ocharo-platform | — |
| 15 | OE12 Close out past events | ocharo-platform | — |

Gate above all of these, for the developer: the team sees nothing until members join Ocharo on dev or O13 → O16 runs
(prod). O13 (the read-only audit) needs no decision and can run now.

### OE01 Hold sourced events SCFD's AI marks irrelevant
- Repo: `wow-two-sdk-beta.events` · Area: intake/classification · Type: fix
- Why: under `Classifier: filter` every delivered record publishes (`IntakeVerdict.cs:34-35`). On dev, SCFD's own AI
  rates the Tsereteli exhibition, the Yalt-Yult museum exhibition and CAEx Build & Co `irrelevant` (0.90–0.95). They
  still sit published in Ocharo's feed, and CAEx Build went out in the 11-17 Telegram digest. The one relevant post
  (Fashion Show Line, 0.92) is rated correctly.
- Do:
  - Add classifier `filter+payload` to `EventsIntakeSourceOptions` and `IntakeVerdict.Of`. A record is relevant when
    SCFD delivered it (the filter) and its `classification.verdict` is not `irrelevant` at or above `MinConfidence`. A
    missing or `uncertain` verdict leaves the filter's decision. The actor reads `classifier:filter+payload:{filter}`
    and the reason quotes the AI verdict.
  - In `ReviewBacklogAsync`, a published, untracked event that a classifier reviewed, and whose latest payload is now
    irrelevant, goes back to `candidate` with the AI reason. A tracked event stays published, with the verdict recorded
    on its source row (surfaced like E16's state).
  - Validator: `filter+payload` needs `Filter` like `filter`. `intake check` prints the mode.
  - `deploy.yml`: allow the new value; keep the default `filter` until the developer's word, then set `Sources:0..1`.
  - Note in events `product/product.md` § Intake that this is an interim until the selector's tags become the filter
    (`subscription-modes.md` §2.9 step 4).
- Done when:
  - `IntakeAutoReviewTests` pass for: filter + relevant → published; filter + irrelevant 0.95 → held; filter +
    uncertain → published; tracked + irrelevant → stays published.
  - On dev after the switch, Ocharo's feed lists the Fashion Show Line and none of the three off-topic events, and
    `intake check` reads `subscription=ok`.
- Depends: the developer's word (A07 gate). The evidence above is the shadow read: 4 of 4 verdicts right on dev.

### OE02 Pull the three Ocharo subscriptions already provisioned on dev
- Repo: `wow-two-sdk-beta.events` (operated through Wheelhouse) · Area: intake config · Type: fix
- Why: harvest-dev holds `ocharo-fashion-v1` subscriptions for anons events-ru, uzexpocentre exhibitions and caex
  calendar, which no consumer reads. Their 13 matched posts include Visa Fashion Week SS'27, TFT EXPO, Texworld,
  Apparel Sourcing Tashkent, UZCHARMEXPO and Viza Fashion Week. Uzexpocentre also carries the application deadlines
  "Deadlines first" lacks.
- Do:
  - `deploy.yml`: `Events:Intake:Sources:2..4` (`anons-events`, `uzexpocentre-exhibitions`, `caex-calendar`), each
    `from` source 0 for endpoint, token settings, `Review`, `Classifier`, `Filter`, `OwnerOrg`, `DefaultCountry`,
    `DefaultCities` and `DefaultTimeZone`. Each has its own untyped `SubscriptionId`. `DefaultKind`: uzexpocentre →
    `trade-fair`, caex → `exhibition`, anons unset.
  - Wheelhouse: type the three subscription ids that `ocharo status --group <id>` prints on harvest-dev.
  - Mark the entries as interim in events `deployment.md` § Intake: the selector's migration (`subscription-modes.md`
    §2.9 step 2) re-points `Sources:0` and drops them.
- Done when: `intake check` on events-dev prints five `subscription=ok` lines, and Ocharo dev lists TFT EXPO, Apparel
  Sourcing Tashkent and UZCHARMEXPO with no second Visa Fashion Week row.
- Depends: OE01 on, so the circus festival, furniture sale, tourism fair and Baraka Friday stay out; E17, so curated
  Visa Fashion Week absorbs its anons twin. **[held: selector]**: E01 is superseded by #68. Ask the developer to un-hold
  it as an interim, since the selector has no date.

### E17 Attach cross-source duplicates to one event on intake (existing spec, amended)
- Amendment: run it before OE02 goes live, and match against imported (curated) events too. The spec's "published or
  candidate event in the catalog" already includes them; add a test with the curated "Visa Fashion Week Tashkent SS27"
  against anons' "Visa Fashion Week Tashkent SS'27".
- Once OE09 lands, an SCFD entity id outranks the title rule for sourced-vs-sourced matches.

### OE03 Show a member's proposal in the feed at once
- Repo: `wow-two-sdk-beta.events` · Area: catalog events · Type: fix
- Why: Ocharo's "Add event" calls `ProposeAsync`, which creates a `candidate`
  (`ModuleCatalogEventsBroker.cs:74-75`). The tracking list returns published events only
  (`ModuleTrackingBroker.cs:45`), and client 11 carries no `events.review`. So the event an editor adds disappears from
  the feed, and only Events' separate console can publish it. The catalog is private to Ocharo (#50), and #53 removed
  human acceptance for sourced events.
- Do:
  - In `ProposeAsync`, when the catalog is private and the caller's organization owns it, enter the event as
    `published`, reviewed by the proposer (`person:{sub}`, reason "owner-organization proposal in a private catalog").
    Shared or public catalogs keep `candidate`.
  - Update events `product/product.md` § Review (`:140-141`) and the contract doc.
  - Conformance case for Module and Client.
- Done when:
  - An integration test shows an owner-organization proposal in a private catalog listed by `IEventTrackingBroker.ListAsync`
    and a non-owner's proposal still `candidate`.
  - Ocharo's E2E creates an event and finds it in `GET …/events`.
- Depends: —. Orchestrator pick; it reverses a documented rule, so it is stated to the developer in one line.
  Alternative if refused: client 11 gains `events.review` and the detail page gets Accept and Reject for owners and
  admins.

### OE04 Select digest events by the organization's tracking stage
- Repo: `wow-two-sdk-beta.events` · Area: digests · Type: feature
- Why: `DigestSelection` filters on Events' event status and `TrackedOnly` only (`DigestDrafter.cs:83-106`). A digest
  cannot leave out what the team skipped or rejected, nor target "shortlisted or applying" for a deadline reminder.
- Do:
  - Add `Stages` (include) and `ExcludeStages` to `DigestSelection` and `DigestSpecValidator`. Both match the digest
    organization's tracking stage. `ExcludeStages` also drops untracked events only when it names the workflow's
    default stage.
  - Apply them in `DigestDrafter.Select` with the same (issuer, organization) join as `TrackedOnly`.
  - fe-events `DigestsPanel`: a stage multi-select from the organization's workflow (labels from `WorkflowModel`).
  - Contract, conformance and a migration-free JSON field (`selection` is `jsonb`).
- Done when: integration tests on a fake clock show a skipped event left out under `ExcludeStages: [skipped]`, and a
  `Stages: [shortlisted, applying]` + `DeadlineWithinDays: 7` digest listing only those events, running `Empty` when
  none match.
- Depends: —

### OE05 Leave skipped events out of the feed and digest, and add a deadline reminder
- Repo: `ocharo-platform` · Area: Events app · Type: feature
- Why: "Skip" leaves an event in the feed (`EventsFeed.vue:72-78`, every stage by default) and in the digest. Nothing
  reminds the team of deadlines for events it is pursuing.
- Do:
  - Feed: hide `skipped` and `rejected` by default, with a "Show skipped" toggle beside "Show past events"; the status
    filter still selects them. Summary counts are unchanged.
  - Default digest (`{oe-fe}/domain/delivery/TelegramDelivery.ts:45`): `excludeStages: [skipped, rejected]`.
  - Second preset in the Telegram delivery page, "Deadline reminders": daily 09:00 Tashkent, stages `shortlisted`,
    `applying`, `applied`, deadline within 7 days, `role:member`, created disabled for the admin to switch on.
  - Re-pin `fe-events` and the Events Client to the release carrying OE04.
- Done when: vitest hides a skipped event by default and shows it with the toggle; on dev, a preview of the default
  digest leaves a skipped event out and the reminder preset previews only shortlisted or applying events with a deadline
  within 7 days.
- Depends: OE04
- Changed (developer, 2026-11-20): the "Deadline reminders" preset is dropped; reminders move to a scheduled reminder
  system with selectable channels and configurations (track doc #74). The feed and default-digest parts stay.

### OE06 Carry SCFD's English title to Events and Ocharo
- Repo: `wow-two-sdk-beta.harvest`, then `wow-two-sdk-beta.events` · Area: delivery projection, intake mapping · Type: feature
- Why: sourced titles reach Ocharo only as `ru-Cyrl`. SCFD's tagging pass already writes an English title per post
  (`harvest_post_tags.title_en`, such as "CAEx Build & Co 2026 Exhibition"), but `wow2.event.v1` omits it. Ocharo's
  `en` and `uz` readers, and its `uz-Latn` digest, show Russian.
- Do:
  - Harvest: `EventSchemaMapper` adds `titles: [{ text, language: "en", machine: true }]` from the latest tag revision's
    `title_en`, when present. Add a golden page and a § Source host note in `contract.md`.
  - Events: `ScfdEventMapper` maps it to `Title["en"]` beside the source title, and records the machine origin on the
    observation's source fields. `DigestText.Title` matches by language prefix (`ru` finds `ru-Cyrl`), the same rule as
    Ocharo's mapper.
  - Re-copy harvest's contract pages into Events (`source.json`).
- Done when: Events' contract test maps a page with `title_en` to titles `{ru-Cyrl, en}`, and on dev Ocharo's `en` UI
  reads "CAEx Build & Co 2026 Exhibition" with the `RU` badge gone.
- Depends: —

### OE07 Read Events through fe-events and retire the Desk-era wire
- Repo: `ocharo-platform` (+ `wow-two-sdk-beta.events` for any kit gap) · Area: Events app · Type: engineering
- Why: the app still serves Desk's routes and `ShowcaseEvent` wire (`EventsController.cs:14`) through
  `EventsServiceMapper`. That means a revision hack (`:89-93`), in-memory filters with a 200 cap and a 10,000 ceiling
  (`EventsServiceRepository.cs:33`, `:45-58`), a dead full `PUT` and `DELETE`, and four edits per new fact.
  fe-events `kit` already ships the feed, card, detail, tracking form, proposal form, deadlines and failure notice, and
  the digest page already embeds fe-events through a pass-through mirror (`DigestsController.cs:20`).
- Do:
  - Parity check first: fe-events kit against the current page (month groups, deadlines panel, detail, tracking form,
    scope chips, title-language badge, source list, Ocharo's cost and participation fields). File each gap as an
    Events task.
  - Mirror Events' tracking, catalog-event and calendar routes under `api/organizations/{organizationId}/events-api/…`,
    as `DigestsController` does. Render the page from the kit.
  - Delete `ShowcaseEvent`, `EventsServiceMapper`, `EventsServiceRepository`, the full `PUT`, the `DELETE`, the
    hand-written fakes and the fe decoder.
  - Move participation and cost to workflow fields once V04 exists; until then keep them in `fields`.
  - Update `product/features/events.md` (still "Desk Events", 2026-10-08) and `research/events-app.md` #3.
- Done when: the page renders from fe-events with no `ShowcaseEvent` left (`rg ShowcaseEvent` finds nothing), a list
  request makes one Events call with server-side filters and a cursor, all app tests pass, and on dev the feed, detail,
  tracking save and digest page read back.
- Depends: E21 (country lists for the scope chips), fe-events parity gaps. Supersedes E22 and E27's Ocharo half, and
  absorbs E24's error panel.

### OE08 Stop discarding the scope picked for a new event
- Repo: `ocharo-platform` · Area: Events app · Type: fix
- Why: the create form asks for a scope (`EventForm.vue:105`), but `ToFacts` drops it (`EventsServiceMapper.cs:96-114`).
  Scope is derived from country, and no country reads `international` (`:174-179`). A proposal marked "local" with no
  country lists as international.
- Do:
  - Drop the scope field from the create form; show the derived scope under the country field ("Local: Uzbekistan").
  - A missing country derives no scope: add `unknown` to the read model and labels, and keep it out of the three scope
    chips.
  - Unit test for `Scope(null)`; vitest for the form.
- Done when: the form has no scope field, and an event with no country reads scope `unknown` in the list and detail.
- Depends: —. It can ride with OE07.

### OE09 Bind sourced events to SCFD's event entity
- Repo: `wow-two-sdk-beta.harvest`, then `wow-two-sdk-beta.events` · Area: delivery projection, intake identity · Type: feature
- Why: SCFD resolves one entity per real event and one occurrence per edition across sources (dev: Uzbekistan Fashion
  Week from afisha and uzexpocentre; The Fashion Show Line from afisha and anons). Events still creates one event per
  post, so OE02 would list each edition once per source. Entity reads need `posts:read`, which Events' client lacks.
- Do:
  - Harvest: each `wow2.event.v1` record carries
    `entity { id, type, occurrenceId, occurrenceLabel, role }` from `harvest_entity_relations` (`role` per
    scfd-entity-model #3.1). This is additive, with no new scope, and a golden page.
  - Events: when a record names an `occurrenceId`, the catalog's event for that occurrence is the post's event. A new
    post of a known occurrence attaches as another source (`MatchedBy = "scfd:entity"`) instead of a new candidate. An
    `entity.merged` or split arrives as the post's next revision. Key: (instance, catalog, occurrence).
  - A `mention` or `report` post attaches as a source without changing facts.
- Done when: replaying two posts of one occurrence from two sources yields one event with two sources; a different
  occurrence of the same entity yields a second event; contract pages pass in both repos.
- Depends: **[held: entities]**: #7 (event identity: edition and series match) settles. Feeds into E17 for
  curated-vs-sourced.

### OE10 Show the expected next edition from SCFD's cadence
- Repo: `wow-two-sdk-beta.events` + `ocharo-platform` · Area: series, Events app · Type: feature
- Why: 18 curated events carry `estimated` dates "from earlier editions". SCFD predicts next editions from cadence
  (TFT Expo, semiannual: 2027-01-25). The developer wants "one entity / one source of truth for events", with history by
  year.
- Do:
  - Events: a series per SCFD entity (P2's "series, occurrences"). It reads the entity change feed for the catalog's
    bound entities: `occurrence.predicted` sets an estimated next event, and `occurrence.confirmed` turns it announced.
    A reviewer or member links a curated event to a series once.
  - Ocharo: the detail page shows "Next edition expected {month}" and past editions by year; the feed groups an
    estimated edition under its month, as today.
- Done when: an integration test replays `occurrence.predicted` then `occurrence.confirmed` and the linked event moves
  from estimated to announced; Ocharo's vitest renders the past-editions list.
- Depends: OE09; **[held: entities]** (#8, two feeds); **[held: selector]**: a subscription choosing entities waits
  for S09 (harvest `backlog.md:117`).

### E31 Add a triage view for untracked sourced events (existing spec; needs the developer)
- Recommendation: a minimal first slice. A "New since your last visit" count and filter over events published after
  the member's last visit (`published_at`), and "New — review" renamed "Not triaged". 64 month-old imports read "New —
  review" today (`EventCard.vue:86`). Bulk Shortlist and Skip can follow.

### OE11 Assign a teammate to a tracked event
- Repo: `ocharo-platform` · Area: Events app · Type: feature
- Why: Events tracking stores `assignee`, but Ocharo never sends or shows it. A team pursuing several applications
  needs to know who owns each.
- Do:
  - Read the organization's members through Identity's member list (client 11 grant `identity.members.read`, as client
    8 has it). The detail page gets an "Owner" select; the card shows initials. A feed filter "Mine" uses Events'
    tracking query (assignee filter added if missing).
  - Tracking route accepts `assignee` (a `sub` of a member).
- Done when: vitest sets and shows an assignee; an E2E test refuses a `sub` outside the organization.
- Depends: —. Low value while dev has one member.

### OE12 Close out past events
- Repo: `ocharo-platform` · Area: Events app · Type: feature
- Why: 8 past events keep their stage forever; an `applying` or `confirmed` event that has ended asks nothing.
- Do: a "Past, not closed" strip on the feed for ended events in `shortlisted`, `applying`, `applied` or `confirmed`,
  with one-click Attended or Skipped through the tracking route. Ended untracked events need no action.
- Done when: vitest lists an ended `confirmed` event in the strip, and Attended moves it out with one tracking write.
- Depends: OE07 is preferred (server-side `To` filter).

## Notes for the orchestrator

- The 3 off-topic events will not leave on their own. E03 and E04 shipped, but no revision un-matches them, so OE01
  (or the selector's switch) is the only path.
- OE02 without OE01 roughly doubles off-topic noise: 4 of the 13 new matches are off-topic.
- `events_prod` exists on the dev host's PostgreSQL with no tables. O14 has not run.

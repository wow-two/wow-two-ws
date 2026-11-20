# Ocharo events UI — display, search and the event and post entities

*Written 2026-11-20 · read-only analysis, no repo changed, dev not queried*

> How Ocharo's Events app shows events today, and the refinement plan: page shell, cards, search and filters, and
> the event entity with its source posts.
> Asked (developer, 2026-11-20): "work on ocharo itself to refine a few things - first how events are displayed there,
> search filtering, favoring event entity and post entity".
> Added (developer, 2026-11-20): "for the events page - need similar cards design that we did in scfd posts page,
> remove any unnecessary stuff at the top, analyze how to improve page design since we'll have calendar of events with
> day ,month, year view and a feed of events that just scrolls to see all events posts from different sources, and
> scheduled reminder settings page, if side navigation like in wheelhouse works - let's go and implement it".

Code read at: `ocharo-platform` `0f7bbf5` (`v0.3.25`; the Events app pins fe `0.0.51`, fe-events `0.0.11`);
`wow-two-sdk-beta.events` `4deb80c` (`v0.1.29`, `be-v10.0.20-beta`); `wow-two-sdk-beta.harvest` `0b1d92c` (`v0.2.42`);
`wow-two-sdk-beta.fe` `d6ddfbd7` (`fe-v0.0.52`, plus another lane's uncommitted Year view in
`EventCalendarViewerTypes.ts`); `wow-two-platform.wheelhouse` `9bc4b81`.

## Path prefixes

All paths are relative to the `wow-two-ws` root.

| Prefix | Path |
|---|---|
| `{pl}` | `workbench/mfts-projects/ventures/ocharo-hq/ocharo-ws/workbench/ocharo-platform` |
| `{oe-fe}` / `{oe-be}` | `{pl}/engineering/codebase/ocharo-events.frontend-services/apps/web/src` / `…/ocharo-events.backend-services` |
| `{ev}` | `workbench/wow-two-sdk-beta/wow-two-sdk-beta.events/engineering/codebase/events.backend-services` |
| `{kit}` | `workbench/wow-two-sdk-beta/wow-two-sdk-beta.events/engineering/codebase/events.frontend-services/packages/fe-events/src` |
| `{h}` | `workbench/wow-two-sdk-beta/wow-two-sdk-beta.harvest/engineering/codebase/harvest.backend-services/packages` |
| `{hc}` | `workbench/wow-two-sdk-beta/wow-two-sdk-beta.harvest/engineering/codebase/harvest.frontend-services/packages/fe-harvest/src/admin/harvestConsole` |
| `{fe}` | `workbench/wow-two-sdk-beta/wow-two-sdk-beta.fe/engineering/codebase/wow-two-sdk-beta-fe/src` |
| `{wh}` | `workbench/wow-two-platform/wow-two-platform.wheelhouse/engineering/codebase/wheelhouse.frontend-services/apps/web/src` |

---

## Verdict

- The page already renders WoW2 Events' own screens from the fe-events kit (OE07, `{oe-fe}/presentation/events/pages/EventsPage.vue:29-37`).
  Most of the refinement therefore lands in the fe sdk, the kit and the Events server; the Ocharo app keeps its
  configuration, shell and routes (SDK doctrine).
- Three gaps a team member sees first:
  - Layout: six blocks stand above the first card (eyebrow, title, freshness, a 40-word description, deadlines panel,
    past strip), then a second "Events" heading, a five-control toolbar and a chip row; cards run up to 11 text lines.
  - Search and filters: search covers titles, organizer, city, venue, key and notes; city, source, priority, date
    range and sort are missing; stage counts ignore every other filter.
  - Entities: an Ocharo event is keyed by its SCFD post and joined across sources by a title rule (E17); a source
    shows only its name, state and seen times. SCFD's entity (editions by year, cadence, posts with roles) never reaches
    Events, because `wow2.event.v1` carries no entity id.
- Recommended shape:
  - side navigation through the fe sdk `AppFrame` `nav` slot, as Ocharo's Brand, Desk, Marketing, Studio and Catalogue
    already do: Feed, Calendar, Reminders, Telegram delivery;
  - a feed of image-first `MediaCard` event cards (the SCFD posts card, already lifted into the fe sdk), a date tile
    where no curated image exists, infinite scroll;
  - a facet bar with server-side counts;
  - one card per edition, its source posts shown as evidence on the card and the event page;
  - series and editions by year once entity model #7 settles (OE09, OE10).
- First slice: UI01-UI06 (shell, cards, facet bar with counts, city and source filters, sort, infinite scroll).

---

## 1. Today

### Places and what each shows

| Place | Shows | Evidence |
|---|---|---|
| Routes | two places: `organizations/:id/events/:view*` (feed or one event) and `…/telegram-delivery`; `/` opens the session's organization | `{oe-fe}/bootstrap/EventsRouter.ts:37-72` |
| Frame | the fe sdk `AppFrame` with no `nav` slot: "It has one place, so it gives the frame no sidebar" | `{oe-fe}/bootstrap/AppLayout.vue:24-25`, `:33-37`, `:113-128` |
| Page header | eyebrow "Showcase events", Telegram delivery link (admins), h1 "Events", "Sources updated …", a description paragraph | `EventsPage.vue:99-119`; `{oe-fe}/presentation/events/SourcesFreshness.vue:10-15` |
| Deadlines panel | the 5 nearest open application deadlines, untracked events included, lost stages left out | `EventsPage.vue:122-132`; `{kit}/kit/presentation/EventsDeadlines.vue:14-18` |
| Past, not closed (OE12) | ended events still `shortlisted`…`confirmed`, closed with Attended or Skipped | `EventsPage.vue:133-143`; `{oe-fe}/presentation/events/PastEventsStrip.vue:18-23` |
| Feed header | h2 "Events", Download calendar, Propose an event | `{kit}/kit/presentation/EventsFeed.vue:307-325` |
| Feed controls | search, stage select with counts, kind select, show past, show skipped and rejected | `EventsFeed.vue:358-396` |
| Scope chips | All, Local, Regional, International, from Ocharo's country sets | `EventsFeed.vue:397-419`; `{oe-fe}/domain/events/Events.ts:197-203` |
| List | month groups, undated last, 50 a page behind a Load more button | `EventsFeed.vue:89`, `:445-486` |
| Detail | badges, title, images, dates with one-event ICS, fields, deadlines, offers, links, sources, tracking form | `{kit}/kit/presentation/EventDetail.vue:192-390` |
| Telegram delivery | fe-events `DigestsPanel` and a "Deadline reminders" preset button | `{oe-fe}/presentation/delivery/pages/TelegramDeliveryPage.vue:13-18` |
| Wire | kit → the app's mirror `api/organizations/{id}/events-api/api/events/v1/…` → Events' tracking list | `{oe-be}/OcharoEvents.Api/Events/Controllers/EventsApiController.cs:29-137`; `{ev}/packages/Module/Tracking/ModuleTrackingBroker.cs:29-113` |

### The card (`EventCard.vue`)

| Line | Shows | Evidence (`{kit}/kit/presentation/EventCard.vue`) |
|---|---|---|
| image | an 80px thumbnail, curated `facts.images` only; sourced media never reaches it | `:30-35`, `:98-101`, `:151-157` |
| marker | "New — review" on every untracked event | `:161-163` |
| title | locale title, a language tag when the title is in another language | `:164-176` |
| organizer, place, source | three lines; the source reads "via {source}" | `:177-186` |
| dates | honest precision, "≈ March 2027 (expected)" for estimates | `:192` |
| badges | review, kind, scope, status, online, removed, stage, high priority | `:188-216` |
| deadline, tickets | next open deadline with days left; ticket price | `:217-233` |
| fields | Ocharo's cost, "Cost not stated" when empty | `:234-239`; `Events.ts:206-208` |
| actions | Shortlist and Skip as two outline buttons on an untracked card | `:240-251`; `Events.ts:98` |

### Gaps and rough edges

- The first card sits below six header blocks and a second toolbar; the screenshot shows the scope chips, month
  headers and tall cards the developer named.
- "Events" is a heading twice: the page's h1 (`EventsPage.vue:110`) and the feed's h2 (`EventsFeed.vue:308`).
- "New — review" marks 64 imports from 11-10 on dev (review doc's 11-19 snapshot); "Cost not stated" prints on
  every card without a cost; two buttons sit on every untracked card.
- The source line shows a group handle ("afisha orqali"), not a display name (E19, changed by the selector design to
  per-post provenance).
- Stage counts come from the summary, unaffected by search, kind or scope (`EventsFeed.vue:145-155`): a chip can read
  "Shortlisted (5)" over a list of one.
- Kind and stage are single selects; no multi-select.
- The tracking list drops the city and status filters it already supports (`ModuleTrackingBroker.cs:53-55` passes
  `null`; the filter exists at `{ev}/packages/Module/Tracking/EventListQuery.cs:56-59`).
- No source, priority, date-range, open-deadline or "new" filter; the order is fixed to start ascending
  (`ModuleTrackingBroker.cs:97-99`).
- Search is a substring over titles in every language (SCFD's English machine title included since OE06), organizer,
  city, venue and key (`{ev}/packages/Module/Shared/EventRows.cs:22-28`), plus tracking notes
  (`ModuleTrackingBroker.cs:88-95`); source names, SCFD topics and entity aliases are not searchable.
- The list loads with a button, not on scroll (`EventsFeed.vue:484-486`).
- The detail lists sources by name, state and first and last seen only (`EventDetail.vue:358-378`); a source post's
  own title, language, posted date and role are not shown. Observations, which hold them, are readable only with
  `events.review` (`{ev}/service/Events.Api/Review/Controllers/ReviewController.cs:15`, `:114-124`).
- Images: Ocharo shows curated images only; Afisha's terms keep its photos out (track #32), and the per-source
  thumbnail policy (E32) waits for the developer. Most events have no image, so an image-first card mostly shows its
  fallback.
- No design spec declares the Events app's screens: `{pl}/engineering/research/design-research/design-research.md:5-8`
  covers Catalogue only, and responsive work needs declared targets
  ([responsive](../../../../conventions/development/frontend/shapes/app/responsive/responsive.md)). Digest links open
  event pages on phones, so phone is a real target.

---

## 2. Event entity and post entity

### Reading

- Event entity: one real event across sources and years (entity model #2,
  [scfd-entity-model.md](../../../../ideas/scfd-entity-model.md)). In Ocharo it splits in two:
  - an edition: one run with its dates, what a team applies to and attends; one Events catalog event per edition;
  - a series: the event across years, with its cadence and a predicted next edition; one SCFD entity.
- Post entity: what a source published about an edition, with its role (`announcement`, `update`, `report`,
  `mention`, `{h}/Abstractions/Entities/EntityRoles.cs`), source, posted date, own title and link. Ocharo shows it as
  evidence, never its text or photos (track #32).
- On the page:
  - the feed lists editions, one card each, deduplicated across sources; the card names its sources;
  - the event page shows the edition, its posts by source, and the series' editions by year with the predicted next.

### What each layer carries

| Piece | SCFD | Events | Ocharo shows | Gap |
|---|---|---|---|---|
| Edition across sources | occurrences, with posts bound by role (`{h}/Module/Entities/entities.md`) | one event per post, joined by E17's title-date-city rule (`{ev}/packages/Module/Intake/IntakeProcessor.cs:21`), moved on SCFD merges (E18) | one card per Events event | `wow2.event.v1` carries no entity or occurrence id (`{h}/Module/Extraction/EventSchemaMapper.cs:28-55`) → OE09 |
| Series, years, cadence, predicted next | `EntitySummaryModel` years, cadence, predicted; `OccurrenceModel.Predicted`; change feed with `occurrence.predicted` (`{h}/Abstractions/Entities/IEntitiesBroker.cs:23`, `:66`) | none (Events P2) | none | OE10, plus feed access: entity routes need `posts:read` (`{h}/Hosting/Entities/Controllers/EntitiesController.cs:29-112`), Events' client holds `harvest.events-read` |
| Posts per edition | `EntityPostModel`: role, changes, year, title, link, source, posted (`{h}/Abstractions/Entities/EntityPostModel.cs`) | `EventSourceModel`: kind, id, url, name, state, posted, `matchedBy`, seen times (`{kit}/contracts/EventModel.ts:16-33`); full payloads under review scope | name, state, seen times | no title, language or role on a source; no member read |
| Post tags: domains, topics, timeframe | `harvest_post_tags` (`{h}/Module/Migrations/012-post-tags/Apply.sql:4-24`); delivery `match.clauses` name only the deciding clauses (`{h}/Abstractions/Delivery/SubscriptionMatch.cs:5-18`) | `facts.tags` exists, never filled (`{kit}/contracts/EventFacts.ts:85`; `{ev}/packages/Module/Intake/ScfdEventMapper.cs:169-184`) | none | payload `tags`, an Events column and filter |
| Source display name | groups and sources with names | `EventSourceModel.Name`, the group handle as fallback | "via afisha" | per-post provenance in the payload (E19 as changed) |
| English title | `titleEn` | machine title beside the source title (`ScfdEventMapper.cs:155-162`) | in the `en` UI | shipped (OE06) |

### Missing end to end, in build order

1. harvest: `wow2.event.v1` gains `entity { id, occurrenceId, occurrenceLabel, role }` (OE09), `tags { primaryDomain,
   domains[], topics[] }` and `source { group, name }`, all additive with golden pages.
2. Events: sources gain `title`, `language` and `role`; an event's source posts become readable under `events.read`,
   without text or media.
3. Events: a sourced event keys on its occurrence when one is named, so a second source joins it (OE09); E17's title
   rule stays for curated events and posts without an entity.
4. Events: a series read model from SCFD's entity change feed (OE10), needing a harvest scope for Events' client or
   entity model #8's entity feed in the subscription.
5. fe-events: the card names its sources; the event page gains Posts and Editions sections.
6. Ocharo: re-pin, and mirror each new Events route in `EventsApiController.cs`.

---

## 3. Search and filtering

### Facets

| Facet | Value for Ocharo | Computed in | Today | Change |
|---|---|---|---|---|
| Text | high | Events `search` column, substring | 5 fact fields + notes | add source names; aliases after OE09; topics after tags |
| Date range | high; the calendar shares it | Events `from`/`to` | "show past" toggle | presets: upcoming (default), this month, next 3 months, this year, past, custom (`DateRangePicker`) |
| Scope | high | app config → Events `countries`/`excludeCountries` (E21) | chips | chips with counts |
| City | medium (Tashkent, Samarkand, Bukhara) | Events `city` | not passed by tracking | `cities[]` with counts |
| Kind (format) | high | Events `kind` | single select | `kinds[]`, chips with counts |
| Stage | high | Events `stages`/`excludeStages` | select, summary counts | chips with counts that follow the filters; the hidden-stage toggle stays |
| Priority | medium | Events `priority` | none | "High priority" toggle |
| Source | high once the selector switch brings 4 more publishers | Events, over `events_event_sources` | none | `sources[]`: each source name, plus `curated` for import and manual entries |
| Open deadline | high ("Deadlines first") | Events `deadlineBefore` | panel only | "Deadline within 30 days" toggle |
| New | high (E31) | Events `publishedSince`; the visit marker per person | "New — review" on untracked | OQ-4 |
| SCFD subdomain, topic | medium (jewelry, textile, womenswear) | harvest tags → Events column | none | full set, after the payload carries tags |
| Expected or recurring | medium | Events series (OE10) and date certainty | "≈ (expected)" dates | full set, after OE10 |
| Sort | high | Events | start ascending only | `starts` (default), `added` (newest published), `deadline` (nearest open) |

- Counts: one Events read returns counts per facet value for the list's query, each facet counted without its own
  selection — the SCFD console's chip rule (`../scfd-console/scfd-console-analysis.md:209`). The console counts loaded
  rows only (`:236`); Events counts server-side, since the feed scrolls and never holds the whole catalog.
- Size: 72 published events on dev (review doc's snapshot); a substring scan stays cheap, so a `pg_trgm` index waits
  until a catalog passes ~5,000 events.
- Month dividers: kept under the `starts` sort, where they help scanning by date; dropped under `added` and
  `deadline`.

### API changes

- `TrackingQuery` (`{ev}/packages/Abstractions/Tracking/TrackingQuery.cs`): `cities[]`, `kinds[]`, `sources[]`,
  `publishedSince`, `sort`; pass the existing `city` and `status` through (`ModuleTrackingBroker.cs:53-55`).
- New `GET api/events/v1/catalogs/{catalog}/tracking/facets` with the list's query: counts for scope countries, city,
  kind, stage (untracked as the default stage), priority, source, open deadline.
- `EventSourceModel` gains `title`, `language`, `role`; contract, module and Client conformance.
- fe-events `EventsClient` gains `getTrackingFacets`; the kit's query types mirror the new fields.
- Ocharo mirrors the facets route beside the tracking routes (`EventsApiController.cs:39-47`).

---

## 4. Layering

| Piece | Lives in | State |
|---|---|---|
| Side navigation: sidebar, rail, drawer, phone bar | fe sdk `AppFrame` `nav`, `nav-footer` and `phone-nav` slots (`{fe}/presentation/layout/appFrame/AppFrame.vue:99-100`, `:223-245`) with `SidebarMenu` and `BottomNavMenu` | exists; 5 Ocharo apps use the `nav` slot; Wheelhouse composes the same `SidebarMenu` under `AppShellSidebar` (`{wh}/bootstrap/AppLayout.vue:187-189`, `{wh}/presentation/shell/components/ConsoleNav.vue:42-60`) |
| Nav items, routes, labels, the top cleanup | Ocharo app `AppLayout.vue`, `EventsRouter.ts`, `EventsPage.vue` | new |
| Image-first card with glass pills | fe sdk `MediaCard` (`{fe}/presentation/display/mediaCard/MediaCard.spec.md`), `Badge` `glass` (`{fe}/presentation/display/badge/Badge.spec.md:24-25`), `CardLink` | exists since fe `0.0.51`, lifted from the SCFD posts card; no product uses it yet |
| Filter chips with counts and icons | fe sdk `ToggleGroup` items gain `count` and `icon` | lift from `{hc}/FilterToggleGroup.vue` |
| Facet bar: search, inline facets, "Filters" popover, selected chips, match count | fe sdk, a composite | lift from `{hc}/SourcePostsTab.vue:224-300`; SCFD's console adopts it back |
| Infinite, windowed list with prefetch | fe sdk `foundation/virtualization` | lift `{hc}/UseAdaptiveList.ts:10-11` |
| Event card content | fe-events kit `EventMediaCard` over `MediaCard` | new; `EventCard` retires (breaking is fine, beta) |
| Feed: facets, sort, scroll, grid | fe-events kit `EventsFeed` | change |
| Event page: Posts, Editions, tracking panel | fe-events kit `EventDetail` | change |
| Calendar views | fe sdk `EventCalendarViewer` (Year view in progress, uncommitted) + a kit adapter | calendar lane ([calendar analysis](../calendar/ocharo-calendar-analysis.md) CAL02, CAL05) |
| Queries, facets, sort, source posts, occurrence keys, series | Events server | change |
| Entity, tags, provenance in `wow2.event.v1`; an entity scope | harvest | change |
| Ocharo's catalog, stages, regions, quick stages, cost field | app `Events.ts` | exists |
| Reminder settings | reminders analysis (`reminders/ocharo-reminders-analysis.md`, being written) | pending |

### Page design

```text
sidebar           Feed · Calendar · Reminders · Telegram delivery (admins)       foot: Sources updated 3h
Feed              [12 of 72] [search……………] [all|local|regional|intl] [kind chips] [Filters] [sort] [+ Add]
                  [3 deadlines in 14 days] [2 past to close]          ← shown only when non-zero; each expands
                  ── March 2027 ──────────────────────────────────── ← under the `starts` sort only
                  [card][card][card][card]                            ← auto-fill ≥ 17rem, 4/3/2/1 columns
                  …scrolls; the next page loads ahead of the reader
Event             header (pills, title, dates, place) · facts · deadlines · Posts by source · Editions by year
                  tracking form as a side panel from `lg`, below the facts on phones
Calendar          day · week · month · year · agenda over the same filters (calendar lane)
Reminders         the reminder system's settings (reminders analysis)
```

- Top cleanup (orchestrator's pick; the developer: "remove any unnecessary stuff at the top"):
  - drop the eyebrow (`EventsPage.vue:101`), the description (`:112-118`) and the feed's second heading;
  - move the Telegram delivery link into the sidebar;
  - move "Sources updated …" to the sidebar foot, keeping its warning tone;
  - fold the deadlines panel and the past strip into the two attention pills; deadlines also show in the calendar
    (CAL02);
  - move Download calendar into an overflow menu beside Add event.
- Card, in the SCFD posts card's look (`{hc}/SourcePostsTab.vue:386-396`; the developer's likes:
  "whole-card clickable, glass style over images, lower-case pills, icons with short text, relative ages without
  `ago`, no clutter on cards", `../scfd-console/scfd-console-live-edits-handoff.md:44`):

| Zone | Shows |
|---|---|
| media | the curated image; else a date tile: day and month large, the kind glyph, on the brand gradient |
| top start | lower-case glass pills: kind, stage when tracked, cancelled / postponed / online, removed |
| top end | a menu with the quick stages (Shortlist, Skip); a high-priority mark |
| panel | title in 2 lines; dates · city; next deadline "apply by 3 Mar · 5d" in the urgent tone, else the sources "afisha · uzexpocentre" |
| state | dimmed when cancelled, removed or past |
| left out | organizer, scope (the chips filter it), "Cost not stated", the review badge, the title-language tag (kept on the event page) |

---

## 5. Slices

- First slice (UI01-UI06): a member opening Events on dev sees the sidebar, the first cards above the fold, image-first
  cards with date tiles, a facet bar whose counts follow the search, city and source filters, a "recently added" sort,
  and a feed that scrolls without a button.
- Full set (UI07-UI14): source posts on the card and the event page, SCFD tags as facets, editions by year and the
  predicted next edition, the "new since your last visit" marker, and the calendar's filter contract.
- Lanes: the page-shell lane builds UI02, UI03 and UI06; an fe sdk lane UI01; the events lane UI04, UI05, UI07,
  UI08, UI10, UI11's Events half, UI12 and UI14; harvest UI09 and UI11's harvest half; the calendar lane consumes UI14.

---

## 6. Open decisions

### OQ-1 What one feed card stands for

The developer's "a feed of events that just scrolls to see all events posts from different sources" reads two ways.

- (a) One card per edition: duplicates merged; the card names its sources; the posts sit on the event page.
- (b) One card per source post, newest first, as SCFD's Posts tab shows them: every source's word on its own card, but
  Visa Fashion Week appears once per publisher.
- (c) (a) as the feed, plus an "Updates" view: the newest source posts (announced, dates changed, cancelled), each
  linking to its edition.
- Pick: (a) now; (c)'s Updates view once OE09 brings each post's role.

### OQ-2 Card media while sourced images stay out

The SCFD card is image-first, but Ocharo shows only curated images: Afisha's terms ask written permission for its
photos (track #32), and E32 (which sources' thumbnails Ocharo may show) is still open.

- (a) `MediaCard` with a date tile wherever no curated image exists; E32 stays held.
- (b) Decide E32 now and show sourced thumbnails for the sources whose terms allow them.
- (c) A text card in the SCFD pill style, with no media zone.
- Pick: (a): the SCFD look without a rights question, and a curated image still fills the card.

### OQ-3 Event identity: one Events event per SCFD edition

Entity model #7 (how editions and series are identified) is still proposed; OE09 and OE10 wait on it.

- (a) Settle it: an Events catalog event is one SCFD occurrence (edition) and a series is one SCFD entity. OE09 keys
  sourced events by occurrence; a curated event links to its series once, by hand or by E17's rule.
- (b) Keep post keys and E17's title rule until entity model #7 and #8 (the entity feed) both settle.
- Pick: (a): it uses what SCFD already resolves (Uzbekistan Fashion Week across afisha and uzexpocentre). OE10's
  predicted editions still need #8 or an entity scope for Events' client.

### OQ-4 What "new" means on a card (E31)

E31 (the triage view) waits for the developer; today "New — review" marks every untracked event, the 64 month-old
imports included.

- (a) "New since your last visit", stored per person; the default stage's label becomes "Not triaged" and leaves the
  card.
- (b) Keep the untracked marker.
- (c) No marker; the "recently added" sort covers it.
- Pick: (a): it marks only what changed for this reader, and the visit marker sends nothing (GWDNBM).

---

## 7. Tasks

| # | Repo | What | Depends | Build |
|---|---|---|---|---|
| UI01 | `wow-two-sdk-beta.fe` | filter chips with counts, facet bar, adaptive list | — | Sonnet `xhigh` |
| UI02 | `ocharo-platform` | sidebar shell, routes, top cleanup, screens declared | — | Sonnet `medium` |
| UI03 | `wow-two-sdk-beta.events` (fe-events) | `EventMediaCard` on `MediaCard` | OQ-2 | Sonnet `xhigh` |
| UI04 | `wow-two-sdk-beta.events` | query fields, facets route, sort | — | Sonnet `xhigh` |
| UI05 | `wow-two-sdk-beta.events` (fe-events) | feed v2: facet bar, counts, sort, scroll, grid | UI01, UI03, UI04 | Sonnet `xhigh` |
| UI06 | `ocharo-platform` | adopt UI03-UI05, mirror the facets route | UI02, UI05 | Sonnet `medium` |
| UI07 | `wow-two-sdk-beta.events` | source posts on events: title, language, role | — | Sonnet `xhigh` |
| UI08 | `wow-two-sdk-beta.events` (fe-events), `ocharo-platform` | event page v2: Posts section, tracking panel; card source line | UI07, UI05 | Sonnet `xhigh` |
| UI09 | `wow-two-sdk-beta.harvest` | `tags` and `source` provenance in `wow2.event.v1` | — | Sonnet `medium` |
| UI10 | `wow-two-sdk-beta.events` (+ fe-events) | store tags; `tags[]` filter and facet; display source names | UI09, UI04 | Sonnet `xhigh` |
| UI11 | `wow-two-sdk-beta.harvest`, then events | OE09: entity in the payload, events keyed by occurrence | OQ-3 | Opus plans, Sonnet `xhigh` |
| UI12 | `wow-two-sdk-beta.events` (+ fe-events), `ocharo-platform` | OE10: series, editions by year, predicted next | UI11, entity model #8 or a scope | Opus plans, Sonnet `xhigh` |
| UI13 | `wow-two-sdk-beta.events` (+ fe-events), `ocharo-platform` | E31: new since your last visit | OQ-4, UI04 | Sonnet `xhigh` |
| UI14 | `wow-two-sdk-beta.events` (fe-events) | calendar filter contract: the facet bar and query over a date window | UI04, UI05 | Sonnet `medium` |

### UI01 Filtered card feed primitives in the fe sdk

- Do: `ToggleGroup` items take `count` and `icon`; a facet bar composite (search, inline facets, a "Filters" popover
  with pickers, removable chips for selected popover facets, a live match-count pill); `useAdaptiveList` into
  `foundation/virtualization`; specs, stories, playground entries.
- Done when: vitest covers a count rendering and updating, a popover facet becoming a removable chip, the match pill
  announcing through `aria-live`, and the list calling `load` before the end is reached; `fe-v` released.
- Depends: —. SCFD's console swapping to them is a follow-up in harvest's lane.

### UI02 Ocharo Events shell and top cleanup

- Do:
  - `AppLayout.vue` fills the `nav` slot with `SidebarMenu`: Feed, Calendar, Reminders, Telegram delivery (admins);
    `phone-nav` with `BottomNavMenu`, at most 5 destinations; "Sources updated …" in `nav-footer`.
  - Routes `events`, `events/{id}`, `calendar`, `reminders`; a destination stays out of the menu until its page ships.
  - `EventsPage.vue` drops the eyebrow, the description and the Telegram link.
  - Declare the Events app's `## Screens` in `engineering/research/design-research/design-research.md`: desktop
    primary, phone declared.
- Done when: vitest renders the menu with the active item per route and the phone bar below `md`; on dev at
  1440 × 900 the first event card sits above the fold; `rg "Showcase events" {oe-fe}` finds nothing.
- Depends: —

### UI03 Event card on `MediaCard`

- Do: `EventMediaCard` in the kit per #4's card table; the date tile when no curated image; quick stages in a top-end
  menu; dimmed state; `EventCard` removed from the feed.
- Done when: vitest covers untracked, tracked, cancelled, removed, past, no image, a curated image, an urgent deadline
  and a long title; a story shows the grid at 4, 3, 2 and 1 columns (1440, 1024, 768, 390 wide).
- Depends: OQ-2

### UI04 Events queries, facets and sort

- Do: #3's `TrackingQuery` fields; city and status passed through; a source filter over `events_event_sources`;
  `GET …/tracking/facets`; `sort`; contract, module and Client conformance; `IEventsClient` and the npm client.
- Done when: integration tests show each facet counted without its own selection, `sources: [afisha]` listing only
  events with an Afisha source, `sources: [curated]` the imported ones, `cities: [tashkent]` working, and `sort: added`
  ordering by newest published.
- Depends: —

### UI05 Feed v2 in fe-events

- Do: `EventsFeed` renders the UI01 facet bar with UI04 counts, the sort, date presets, the UI03 grid with month
  dividers under `starts`, infinite scroll through `useAdaptiveList`, and the attention pills (deadlines, past to
  close) with slots so a consumer supplies its own strip.
- Done when: vitest shows the next cursor loading on scroll with no button, stage counts changing with the search,
  pills hidden at zero; the kit's E2E fake runs it; `fe-events` released.
- Depends: UI01, UI03, UI04

### UI06 Ocharo adopts the feed

- Do: re-pin fe sdk and fe-events; mirror the facets route in `EventsApiController.cs`; pass Ocharo's past-events
  strip into the attention slot; remove `EventsDeadlines` and `PastEventsStrip` from the top.
- Done when: on dev the feed shows the facet bar whose counts change with a search, scrolls past 50 events without a
  button, and filters by source and city; app tests pass.
- Depends: UI02, UI05

### UI07 Source posts on an event

- Do: `EventSourceModel` gains `title`, `language` and `role` (null until UI11), written from the latest observation
  per source; no text, no media; the event read returns them under `events.read`.
- Done when: an integration test lists an event with two sources, each with its own title and posted date, read by
  a member without `events.review`.
- Depends: —

### UI08 Event page v2

- Do: `EventDetail` gains a Posts section (source, own title, language, posted, role, "open at source") and puts the
  tracking form in a side panel from `lg`; the card's panel names its sources.
- Done when: vitest renders two posts with their sources and links; on dev an event with an Afisha and an Uzexpocentre
  source shows both.
- Depends: UI07, UI05

### UI09 Tags and provenance in `wow2.event.v1`

- Do: `EventSchemaMapper` adds `tags { primaryDomain, domains[], topics[] }` from the latest done tag row and
  `source { group, name }` from the title link's source; golden pages; `contract.md`.
- Done when: a golden page carries both blocks, and a post with no tags renders its earlier bytes.
- Depends: —

### UI10 Tags as Events facets

- Do: Events stores the tags (`facts.tags` or a tag table), filters on `tags[]`, counts them in the facets read, and
  shows source display names from the provenance.
- Done when: an integration test filters `tags: [style-fashion/jewelry]`; on dev a card reads "afisha" by its display
  name.
- Depends: UI09, UI04

### UI11 OE09: one Events event per SCFD edition

- Do: OE09 as specced (`../tasks/tasks-ocharo-events.md:478-494`); sources take `role` from the payload; search adds
  entity aliases.
- Done when: OE09's done-when, plus a search for an alias finding its event.
- Depends: OQ-3

### UI12 OE10: series and editions by year

- Do: OE10 as specced (`../tasks/tasks-ocharo-events.md:496-510`); the kit adds an Editions section and "next edition
  expected {month}" on the card; facet "Expected".
- Done when: OE10's done-when, plus vitest rendering past editions by year.
- Depends: UI11; entity model #8 or a harvest entity scope for Events' client

### UI13 E31: new since your last visit

- Do: a per-person visit marker in Events (organization, person, catalog, seen-at); the `publishedSince` filter; a
  "New" chip and a quiet card pill; the default stage labelled "Not triaged".
- Done when: an integration test shows an event published after the marker listed as new and older ones not; on dev
  the 64 imports no longer read as new.
- Depends: OQ-4, UI04

### UI14 Calendar filter contract

- Do: the kit exposes the facet bar state and the tracking query for a date window, so the calendar page reuses the
  feed's filters; month- and year-precision events pass through with their precision for the calendar's strip
  (CAL05).
- Done when: vitest shows a filter set in the feed carried into a window query with `from`/`to`.
- Depends: UI04, UI05. The views themselves stay with the calendar lane.

- OE11 (assign a teammate) rides on UI04 later: an `assignee` filter and a "Mine" chip, once dev has more than one
  member.

# Ocharo platform calendar — design analysis

*Written: 2026-11-20 · read-only analysis, no repo changed*

> Where to build one calendar that pulls everything scheduled across Ocharo, and whether to build one shared
> calendar or separate calendars per service.
> Asked (developer, 2026-11-20): "need to analyze where we can build overall calendar - like a calendar that can pull
> all scheduled stuff across the whole ocharo platform, events will be just part of it - like seeing overall scheduled
> events, but we'll be albe to see one main calendar with everything scheduled as well - for marketing etc for example -
> analyze if we should build one calendar and use it across services or build separate calendars for style and
> customization".

## Verdict

- **Option (b), federated:** each service keeps its scheduled items and answers one shared schedule-feed contract.
  One SDK calendar component serves every app, and one Ocharo calendar app shows them together.
- Reason: each service already owns its dates, permissions and write rules. A shared contract and component give one
  main calendar plus per-service styling, and nothing is copied into a second store.
- First slice: one feed contract in the be sdk; one feed route each in Events and Marketing; one thin `ocharo-calendar`
  host that fans out to both and renders the existing `EventCalendarViewer`. No fe sdk change is needed for it.

## Path prefixes

All paths are relative to the `wow-two-ws` root.

| Prefix | Path |
|---|---|
| `{oc}` | `workbench/mfts-projects/ventures/ocharo-hq/ocharo-ws/workbench` |
| `{mkt}` | `{oc}/ocharo-marketing/engineering/codebase/ocharo-marketing.backend-services` |
| `{mkt-fe}` | `{oc}/ocharo-marketing/engineering/codebase/ocharo-marketing.frontend-services/apps/web/src` |
| `{blog}` | `{oc}/ocharo-marketing/engineering/codebase/ocharo-blog.backend-services` |
| `{pl}` | `{oc}/ocharo-platform/engineering/codebase` |
| `{oe}` / `{oe-fe}` | `{pl}/ocharo-events.backend-services` / `{pl}/ocharo-events.frontend-services/apps/web/src` |
| `{ev}` / `{fe-ev}` | `workbench/wow-two-sdk-beta/wow-two-sdk-beta.events/engineering/codebase/events.backend-services` / `…/events.frontend-services/packages/fe-events/src` |
| `{hv}` | `workbench/wow-two-sdk-beta/wow-two-sdk-beta.harvest/engineering/codebase/harvest.backend-services` |
| `{fe}` | `workbench/wow-two-sdk-beta/wow-two-sdk-beta.fe/engineering/codebase/wow-two-sdk-beta-fe` |
| `{be}` | `workbench/wow-two-sdk-beta/wow-two-sdk-beta.be/engineering/codebase/wow-two-sdk-beta-be/src` |
| `{id}` | `workbench/wow-two-sdk-beta/wow-two-sdk-beta.identity/engineering/codebase/identity.backend-services` |

---

## 1. What is scheduled today

### Dated items

| Item | Owner | Model (evidence) | Recurs | Feed / ICS / API today |
|---|---|---|---|---|
| Catalog event: start, end, zone | WoW2 Events (`wow-two-sdk-beta.events`), read by Ocharo Events | `EventFacts.Starts/Ends/TimeZone` `{ev}/packages/Abstractions/CatalogEvents/EventFacts.cs:39-45`; honest precision and certainty `EventWhen.cs:4-14` (`2026`, `2026-03`, `2026-03-14`, `2026-03-14T19:00`) | no | list API with `From`/`To` window `EventQuery.cs:9-12`; ICS `GET …/catalogs/{catalog}/events.ics` `{ev}/service/Events.Api/Calendar/Controllers/CalendarController.cs:26-29` (bearer, `events.read`); mirrored by Ocharo Events `{oe}/OcharoEvents.Api/Events/Controllers/EventsApiController.cs:119` |
| Event deadline: application, registration, early bird, submission, payment | WoW2 Events | `EventDeadline.cs:4-16`, `DeadlineKind.cs:4-22`, list `EventFacts.cs:48` | no | `EventQuery.DeadlineBefore` `EventQuery.cs:33`; tracking summary's `UpcomingDeadlines` with stage `TrackingSummaryModel.cs:12-13`, `UpcomingDeadlineModel.cs:6-22`; exact deadlines export as all-day ICS entries `IEventCalendarBroker.cs:7-9` |
| Tracking (stage, priority, assignee) | WoW2 Events, private per organization | `{ev}/packages/Abstractions/Tracking/TrackingModel.cs:6-30`; holds no date of its own | — | `GET …/tracking`, `…/tracking/summary` mirrored at `EventsApiController.cs:39,47` |
| Events digest: Telegram delivery | WoW2 Events (V07), set by Ocharo Events (O17) | `DigestSchedule.cs:6-15` (days, `HH:mm` times, IANA zone); `DigestModel.NextRunAtUtc` `DigestModel.cs:39-40` | weekly / daily | digests CRUD + runs `{oe}/OcharoEvents.Api/Delivery/Controllers/DigestsController.cs:20`; Ocharo defaults: Monday 09:00 Tashkent `{oe-fe}/domain/delivery/TelegramDelivery.ts:52`, daily deadline reminders `:76-78` |
| Marketing post plan per channel | Ocharo Marketing (`ocharo-marketing`) | `ScheduleModel(…, Channel, ScheduledAt, Status, …)` `{mkt}/OcharoMarketing.Application/Posts/Models/ScheduleModel.cs:4-13`; channels `instagram`, `telegram`, `whatsapp`, `x` `{mkt}/OcharoMarketing.Infrastructure/Posts/Services/MarketingService.cs:19` | no | create `POST drafts/{id}/schedule` `{mkt}/OcharoMarketing.Api/Posts/Controllers/DraftsController.cs:53`; cancel / queue `{mkt}/OcharoMarketing.Api/Deliveries/Controllers/DeliveryController.cs:25,35`; read only inside `GET workspace` (all plans, no window) `{mkt}/OcharoMarketing.Persistence/Core/Repositories/MarketingRepository.cs:40-46`; no ICS |
| Publication operation (queued send) | Ocharo Marketing | `PublicationOperationModel.DueAt` `{mkt}/OcharoMarketing.Application/Deliveries/Models/PublicationOperationModel.cs:14` | no | `GET schedules/{id}/publication` `DeliveryController.cs:49`; live send only Telegram and X, Instagram and WhatsApp stay manual `{mkt-fe}/domain/marketing/OperationsExtensions.ts:49-52` |
| Posting slot (rhythm) | Ocharo Marketing | `PostingSlotModel(Channel, Days, Time)` "in the brand's timezone (Asia/Tashkent)" `{mkt}/OcharoMarketing.Application/Automation/Models/AutomationModels.cs:5-6`; slots fill plans `AutoFillDays` `:17` | weekly | `GET automation` `{mkt}/OcharoMarketing.Api/Automation/Controllers/AutomationController.cs:35` |
| Lead follow-up | Ocharo Marketing (Inquiries) | `InquiryFollowUp(AssignedTo, FollowUpAt, NextStep)` `{mkt}/OcharoMarketing.Application/Inquiries/InquiryModels.cs:28-30`; `due` / `scheduled` filters `InquiryService.cs:95-98` | no | `GET api/marketing/inquiries` `{mkt}/OcharoMarketing.Api/Inquiries/Controllers/InquiriesController.cs:33` |
| Blog / Editorial story publish time | Ocharo Blog (in `ocharo-marketing`) | `ArticleRecord.PublishAt/PublishedAt` `{blog}/OcharoBlog.Domain/Blog/BlogRecords.cs:10-11`; `ScheduledPublisher` publishes when due `{blog}/OcharoBlog.Infrastructure/Blog/ScheduledPublisher.cs:6-17` | no | `POST articles/{id}/schedule` with `ExpectedRevision` + `PublishAt` `{blog}/OcharoBlog.Api/Blog/Controllers/ArticlesController.cs:77-89`; list filters by status, no date window `:16-36` |
| Brand appearance (seasonal logo, accent, event badge) | Ocharo Brand (`ocharo-platform`) | `BrandAppearance.StartsAt/EndsAt/Status` `{pl}/ocharo-brand.backend-services/OcharoBrand.Domain/Brand/BrandAppearance.cs:7-29`; statuses `scheduled`, `cancelled` `AppearanceStatus.cs:5-6`; Blog reads it as `BrandEvent` `{blog}/OcharoBlog.Application/Blog/Services/Ports.cs:81` | no | `GET/POST appearances`, cancel `{pl}/ocharo-brand.backend-services/OcharoBrand.Api/Brand/Controllers/BrandsController.cs:93,100,119` |
| Predicted event occurrences | SCFD (`wow-two-sdk-beta.harvest`) | `OccurrenceModel` with precision, certainty, `Predicted` `{hv}/packages/Abstractions/Entities/OccurrenceModel.cs:13-28`; entry `EntityCalendarEntryModel.cs:4-25` | by cadence | `CalendarAsync(container, from, to)` `IEntitiesBroker.cs:46-54`, route `calendar` `EntityRouteConstants.cs:13`, window ≤ 366 days `:64` (commit `ed3f2f4`); not Ocharo-facing — Ocharo gets SCFD events through Events intake |

### Nothing scheduled yet

- Desk tasks: no task or due-date model in `brand-workspace`; Desk's overview lists "Scheduling — Planned"
  (`{pl}/brand-workspace.frontend-services/apps/web/src/presentation/common/pages/OverviewPage.vue:225`).
- Studio drafts: no due date; `OcharoStudio.Domain/Greetings/Entities` is empty.
- Catalogue drops: a release publishes when written, with no future publish time
  (`{pl}/ocharo-catalogue.backend-services/OcharoCatalogue.Domain/Catalogue/Entities/CatalogueReleaseRecord.cs:12-13`).
- Each of these joins the calendar by answering the feed once it gains a date.

### Context the calendar must respect

- Brand time zone is stored per brand: `Brand(…, TimeZone)` in
  `{pl}/brand-workspace.backend-services/BrandWorkspace.Domain/Preparation/Models/Brand.cs:4`.
- Org scoping differs per service:
  - Marketing serves one bound organization (`MarketingAccessOptions.cs:3-11`).
  - Events keeps tracking per organization, under `api/organizations/{organizationId}/…` (`EventsApiController.cs:29`).
- Every Ocharo app is an Identity BFF with cookie sessions (`AddIdentityBff`):
  - Ocharo Events reaches WoW2 Events through the client's person-flow token exchange
    (`{oe}/OcharoEvents.Infrastructure/Events/Services/EventsApiService.cs:15`).
  - Marketing accepts no bearer token today (`{mkt}/OcharoMarketing.Api/Configurations/HostConfiguration.Access.cs:30`).
  - Blog and Desk already accept bearer tokens (`{blog}/OcharoBlog.Api/Configurations/HostConfiguration.Access.cs:36`,
    `{pl}/brand-workspace.backend-services/BrandWorkspace.Api/Configurations/HostConfiguration.Extensions.cs:231`).
- Planned is not published: Marketing's operations model says so (`OperationsModels.cs:47`), and the calendar must
  show the status as the owner reports it.

---

## 2. Calendar pieces that exist

| Piece | Where | What it does | Gaps for a platform calendar |
|---|---|---|---|
| `EventCalendarViewer` (month, week, day, agenda) | `{fe}/src/presentation/display/eventCalendarViewer/` | Temporal `ZonedDateTime` items with `id`, `title`, `start`, `end`, `color`, `isAllDay` (`EventCalendarViewerTypes.ts:15-36`); zone-correct projection, DST, keyboard slots, `event-click`, `slot-click` (spec) | no item slot (spec: "Slots: None declared"); title is a scalar; "Drag-edit, recurrence, and '+N more' overflow are deferred" (`EventCalendarViewer.vue:57-62`); no source legend or filter; no month- or year-precision items; no product uses it (grep across `workbench/`) |
| `ScheduleView` | `{fe}/src/presentation/display/scheduleView/` | one day, one row per resource, `booking` / `resource` slots, `onSlotClick` | a single day only; fits per-channel or per-person rows later |
| `RecurrenceEditor` | `{fe}/src/presentation/forms/recurrenceEditor/RecurrenceEditor.vue` | visual RRULE editor, serialises `RRULE:` (`:115`) | the occurrence expander `nextOccurrence` (`:125`) is private to the component |
| Date inputs and grids | `{fe}/src/presentation/forms/{datePicker,calendarPicker,rangeCalendar,rangeCalendarPicker,calendar}`, `display/{heatmapCalendarGrid,ganttTimeline,timeline,activityTimeline}` | pickers, a heatmap grid (Wheelhouse deployments), Gantt | none blocks this work; week start per locale is open (`{fe}/../../planning/backlog.md:125`) |
| Events ICS export (be) | `{ev}/packages/Module/Calendar/CalendarWriter.cs`, broker `IEventCalendarBroker.cs:10-17` | RFC 5545 file; stable UID `{id}@events`, SEQUENCE from revision; minute starts in local time with `TZID`; dates all-day; exact deadlines as their own all-day entries | writes `TZID` without `VTIMEZONE` (`CalendarWriter.cs:12`; task V06 open); bearer-only, so a phone cannot subscribe; events only |
| Events ICS export (fe) | `{fe-ev}/kit/calendar/EventCalendar.ts:88,194`, `DownloadEventsCalendar.ts:22` | one-event download, and the catalog's file | a second ICS writer, beside the be one |
| Events deadline list | `{fe-ev}/kit/presentation/EventsDeadlines.vue` | the tracked deadlines widget | list only |
| SCFD entity calendar | `{hv}/packages/Abstractions/Entities/IEntitiesBroker.cs:46-54` | windowed occurrences, predicted ones marked | per container, harvest roles; serves the SCFD console |
| Marketing week calendar | `{mkt-fe}/presentation/delivery/pages/CalendarPage.vue:18-43` | a hand-built 7-day grid plus agenda, Tashkent days through `Intl` | a local rebuild of what the SDK viewer does; plans only |
| be sdk time and jobs | `{be}/Foundation/Time/Parsers/CronExpressionParser.cs`, `{be}/Jobs/Hangfire/` | cron parsing, Hangfire jobs | no ICS writer, no RRULE expansion, no schedule contract |
| Identity API keys | `{id}/packages/Auth/ApiKeys/ApiKeyOptions.cs:3-16` | hashed, URL-safe product secrets with a check suffix | can carry a per-person ICS feed token |
| Second consumer of a calendar UI | `ideas/calendar-spec.md` (Almanac, `app-t-006`) | a readable day calendar over Google Calendar | spec only; together with Ocharo, two products need the calendar vector |

---

## 3. Design options

### (a) One calendar domain

A WoW2 Calendar service (`wow-two-sdk-beta.calendar`) stores items. Each service publishes its items into it.

- Shape:
  - a domain repo, NuGet family, image and migrations (domain structure);
  - every owner publishes create, change and cancel;
  - the calendar store answers every read.
- Needs a change feed from every owner:
  - SCFD has one (`IEntitiesBroker.cs:57-66`);
  - Events webhooks (V05) are not built;
  - Marketing, Blog and Brand have none.
- Cost: L.
  - domain template, service, deploy;
  - a publisher and an outbox in 5 services;
  - a reconcile job for missed changes;
  - permission rules copied from every owner;
  - a write-back path to each owner.
- Fits [capability forms](../conventions/development/capability-forms.md) only by owning copies. The state it would
  "own" is derived from other services' state.

### (b) Federated feed

Each service keeps its items and answers one schedule-feed contract. One Ocharo calendar app aggregates the feeds.
The fe sdk ships one calendar that every app embeds, with its own filters, colours and item renderers.

- Shape:
  - a contract in the be sdk;
  - one windowed route per owner;
  - a stateless aggregator in Ocharo;
  - the fe calendar extended in the SDK.
- Cost: M.
  - contract and conformance suite;
  - 5 small routes (Events, Marketing, Blog, Brand, later Desk);
  - one thin host;
  - the fe component's second generation, needed for drag and renderers, not for slice 1.
- Fits [capability forms](../conventions/development/capability-forms.md) `:13-14`: the aggregator owns no state, so
  it is an SDK module plus an app, not a domain repo.

### (c) Separate calendars per service

Each app builds its own calendar with its own components.

- This is the state today: Marketing's hand-built `CalendarPage.vue`; Events has only ICS and lists.
- Cost: S for each app, paid again in every app. The zone, grid, accessibility and drag work repeats.
- It never yields one main calendar without (b)'s contract anyway.
- It breaks [SDK extraction](../conventions/development/sdk-extraction.md) `:19-22`: a generic piece goes to the SDK.

### Concerns compared

| Concern | (a) Calendar domain | (b) Federated feed | (c) Separate |
|---|---|---|---|
| Per-service styling, renderers, actions | items carry every field any renderer needs; one central renderer set | the SDK component takes per-source colour, icon and an item slot; each app passes its own renderer and actions | free per app; each re-implements the grid |
| Permissions, org scoping | the store must copy each owner's rules (Marketing bound org + roles, Events `events:read`/`events:track`, Blog editorial); a leak on drift | each owner checks the exchanged token; the aggregator never widens access; a hidden item never leaves its owner | per app |
| Recurring items | the store materialises or re-implements each rule (slots, digests) | each owner expands its rule inside the window; items carry `seriesId` and an RRULE for ICS | per app |
| Time zones (`Asia/Tashkent`) | one place | the contract fixes two forms: an instant (UTC) with its IANA zone, or a local date with precision (`day`/`month`/`year`); the viewer zone defaults to the brand's `TimeZone` | per app; Marketing hard-codes Tashkent (`CalendarPage.vue:18`) |
| Drag to reschedule | the store's write must sync back to the owner: a two-phase write, with conflicts | the item lists its `actions` and `revision`; the calendar calls the owner's verb; the owner validates (Marketing: a future time, `planned` only; Blog: `ExpectedRevision`) | per app |
| ICS subscribe for phones | one store, one file | the aggregator writes one ICS from the fan-out behind a per-person feed token; the ICS writer lives in the be sdk | one subscription per service on each phone |
| Performance | one indexed query | N parallel windowed calls; window ≤ 92 days; per-source timeout; partial answer naming the failed source; a short cache per org and window | — |
| Events digests and deadlines | copied in; `NextRunAtUtc` recomputed on each change | the Events feed emits deadlines (all-day, with stage) and digest runs (recurring markers, a layer that starts hidden) | Events app only |
| Sources of truth | two | one per item | one per item, N different UIs |
| Build cost | L | M | S × N, no main view |

### When (a) earns its place

- When a product needs calendar-native state: bookings and availability, shared team calendars with attendees, entries
  no service owns, or a Google Calendar sync (Almanac).
- Then a WoW2 Calendar domain owns *those* items and answers the same feed. It becomes one more source, not the
  aggregator.

---

## 4. Recommendation

- **(b) Federated:** one feed contract and one SDK calendar, used by every service. Each service keeps its data, its
  permission checks and its write verbs.
- Per-service styling comes from the component's renderer slot, colours and actions, not from separate calendars.

| Piece | Lives in | Notes |
|---|---|---|
| Schedule feed contract: item model, window query, broker, route constant, conformance suite | be sdk `wow-two-sdk-beta.be` (a module, plus `Testing`) | stateless, so a module, not a domain repo (`capability-forms.md:14`) |
| ICS writer with `VTIMEZONE`, RRULE expansion helper | be sdk | lifted from `{ev}/packages/Module/Calendar/CalendarWriter.cs` (folds in V06); Events then uses the shared writer |
| Calendar component, second generation: item slot, source legend and filter, precision strip, "+N more", drag/resize intent, recurrence markers, week start per locale | fe sdk `wow-two-sdk-beta.fe` (`EventCalendarViewer`) | built as a whole vector (`dev-cycle.md:38-50`); Almanac is the second consumer |
| Feed client and `ScheduleItem` → viewer mapping | fe sdk | one helper, so each app does not re-map |
| Events feed: events, deadlines, digest runs | domain repo `wow-two-sdk-beta.events` | Events' precision, certainty and stage rules stay in Events |
| SCFD occurrences feed (predicted layer) | domain repo `wow-two-sdk-beta.harvest` | later; maps `EntityCalendarEntryModel` |
| Marketing feed: plans, slot previews, follow-ups; reschedule verb | `ocharo-marketing` | plus bearer audience for exchanged tokens |
| Blog feed: stories' `PublishAt` | `ocharo-marketing` (Blog) | bearer already present; reschedule goes through the existing `schedule` verb |
| Brand feed: appearances | `ocharo-platform` (Brand) | |
| Main calendar: aggregator BFF, page, ICS subscribe, per-person filters | `ocharo-platform`, new `ocharo-calendar` host | shaped like `ocharo-events`: a BFF that keeps only Data Protection keys and sessions (`{oe}/ocharo-events.backend-services.md:6-9`) |
| Per-app calendars (Marketing, Events) | each app, embedding the SDK component with its own renderers | Marketing's `CalendarPage.vue` moves onto the SDK viewer |
| `calendar` key in the apps menu | 6 copies of `OcharoApps.ts` (Brand, Desk, Events, Catalogue, Studio, Marketing `connect`) | the copies are a cost in their own right; one shared source would remove it |

### Feed item sketch

```text
ScheduleItem
  id         "{source}:{kind}:{ownerId}[:{occurrenceKey}]"   stable; doubles as the ICS UID
  source     events | marketing | blog | brand | scfd | desk
  kind       event | deadline | digest | post | follow-up | story | appearance
  title      text per locale
  start/end  { at: UTC instant, zone: IANA }  or  { date: YYYY[-MM[-DD]], precision: day|month|year }
  allDay     bool
  status     owner's word: planned | queued | published | scheduled | cancelled | tentative …
  certainty  announced | estimated            (Events, SCFD)
  seriesId   + rrule?                         set when the owner expanded a recurring rule
  url        deep link into the owner app
  revision   for write-back
  actions    [reschedule, cancel]             what this caller may do, after the owner's check
ScheduleQuery  from, to (DateOnly, ≤ 92 days), kinds?, sources?
```

---

## 5. First slice — one main calendar with Events and Marketing

Smallest build: a feed contract, two feed routes, one thin host. It uses `EventCalendarViewer` as it ships today:
month, week and agenda views, colour per source, click opens the owner app. Drag, renderers and ICS come later.

### CAL01 Schedule feed contract
- Repo: `wow-two-sdk-beta.be`
- Why: one wire that every owner answers and every calendar reads; without it, the aggregator invents a private wire.
- Do:
  - module with `ScheduleItemModel`, `ScheduleWhen` (instant + zone, or date + precision), `ScheduleQuery`
    (`from`, `to`, ≤ 92 days, `kinds`), `IScheduleFeedBroker.ListAsync`, route constant `schedule`;
  - conformance suite in `Testing`: exclusive end instants, all-day versus instant, ascending start order, refusal
    past the window cap, stable ids across calls.
- Done when: the suite runs green against an in-memory fake; the package is published.
- Depends: —

### CAL02 Events schedule feed
- Repo: `wow-two-sdk-beta.events`
- Why: events and deadlines are the first layer, and their precision and stage rules belong to Events.
- Do:
  - `GET api/events/v1/catalogs/{catalog}/schedule?from&to` (`events.read`, owner organization).
    It returns published events overlapping the window as `event` items: a minute start becomes an instant in its
    zone, a day start becomes all-day, and month or year precision is left off the grid with a count.
  - Open exact deadlines in the window become all-day `deadline` items, with stage and tracked flag. Stages
    `skipped` and `rejected` stay out (OE05).
  - Add the Client method; run CAL01's suite against the module and the image.
- Done when:
  - the suite is green in both forms;
  - an integration test lists a Tashkent 19:00 event at its UTC instant and its exact deadline as all-day;
  - the test leaves a month-precision event off the grid.
- Depends: CAL01

### CAL03 Marketing schedule feed
- Repo: `ocharo-marketing`
- Why: post plans are the marketing layer. The main calendar reads them with the person's exchanged token, and
  Marketing accepts only cookie sessions today.
- Do:
  - `GET api/marketing/schedule?from&to` returns one `post` item per plan, with channel and the owner's status.
    It reads through the `(Status, ScheduledAt)` index (`OcharoMarketingDbContext.cs:80`), not the full read in
    `MarketingRepository.cs:40-46`.
  - Add bearer authentication with Marketing's resource audience, following Blog's recipe. Admit a token only when
    its organization is `Marketing:OrganizationId`.
  - Run CAL01's suite.
- Done when: an integration test answers 403 to another organization's token; the window returns only plans inside
  it; the suite is green.
- Depends: CAL01

### CAL04 Ocharo main calendar
- Repo: `ocharo-platform` (+ Wheelhouse dev settings, Identity declaration)
- Why: one place to see everything scheduled, with nothing stored twice.
- Do:
  - `ocharo-calendar.{backend,frontend}-services`, shaped like `ocharo-events`: Identity BFF, Data Protection keys
    and sessions only.
  - Fan out to Events (catalog `ocharo-fashion`) and Marketing through person-flow token exchange, in parallel, with
    a per-source timeout. A partial answer names the failed source.
  - Page with `EventCalendarViewer` in month, week and agenda views, zone `Asia/Tashkent`, colour per source and
    source toggles. A click opens the owner app's page.
  - Add a `calendar` key to the 6 `OcharoApps.ts` copies, plus `deploy.yml` on dev.
- Done when:
  - on dev, an Ocharo member's month view shows an Events event, an exact deadline and a planned Marketing post on
    their Tashkent days;
  - turning Marketing off hides the posts;
  - with Marketing stopped, the page still shows Events and names Marketing as unavailable.
- Depends: CAL02 and CAL03 released; Identity client for the host and a resource entry for Marketing

### Later slices

| # | Slice | Repo |
|---|---|---|
| CAL05 | Calendar second generation: item slot, legend and filters, precision strip, "+N more", drag/resize intent with a constraint callback, recurrence markers, week start per locale; RRULE expander lifted out of `RecurrenceEditor.vue:125`; `engineering/research/calendar-completeness.md` inventory | `wow-two-sdk-beta.fe` |
| CAL06 | Marketing embeds CAL05 in `CalendarPage.vue` (retires the hand-built grid); `PUT schedules/{id}` reschedule (`planned` only, future time, expected revision); drag on the main calendar calls it | `ocharo-marketing`, `ocharo-platform` |
| CAL07 | Blog and Brand feeds: stories' `PublishAt` (reschedule through `articles/{id}/schedule`) and appearance windows | `ocharo-marketing`, `ocharo-platform` |
| CAL08 | ICS subscribe: the be sdk ICS writer with `VTIMEZONE` (absorbs V06), a per-person revocable feed token on Identity's API-key scheme, `GET …/feed/{token}.ics` on the calendar host; Events moves to the shared writer | `wow-two-sdk-beta.be`, `wow-two-sdk-beta.events`, `ocharo-platform` |
| CAL09 | Recurring layers: Marketing posting slots as `tentative` previews, Events digest runs from `NextRunAtUtc`, inquiry follow-ups visible to their assignee | `ocharo-marketing`, `wow-two-sdk-beta.events` |

---

## 6. Open decisions

- Ad-hoc items: campaign launches or shoot days that no service owns.
  - Recommended: Marketing owns "milestones" and answers them in its feed.
  - Alternative: a small store in the calendar host, which grows it toward (a).
- Main calendar's home:
  - Recommended: a new `ocharo-calendar` host.
  - Alternatives: a page in Desk (its overview already plans "Scheduling") or in Marketing. Either avoids a new host
    but ties the main calendar to one app's release cycle.
- Reminders: the calendar sends none of its own (GWDNBM). Events digests stay the reminder engine; ICS `VALARM` is opt-in
  per feed token.

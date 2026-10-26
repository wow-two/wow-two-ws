# WoW Two Events — Shared Event Catalog and Tracking for Every Product

*Last updated: 2026-10-25*

> `wow-two-platform.events`: a catalog of dated happenings — fairs, fashion weeks, exhibitions, concerts,
> competitions, conferences — fed by sources through [Harvest](#harvest-seam) and curated by reviewers, plus private
> tracking per organization. Shipped in the [capability forms](../conventions/development/capability-forms.md).
> First consumer: Ocharo Desk's Events feed.
>
> **Status:** design 2026-10-25. The developer chose on 2026-10-24 to move Events out of Desk (E1 in
> [Ocharo app boundaries](../workbench/mfts-projects/ventures/ocharo-hq/ocharo-ws/docs/app-boundaries.md)); the
> service is built in a WoW2 chat, then Desk integrates through its clients. Defaults below marked *default* are
> recommendations the build chat may revisit; open ones are listed under [Points](#points).

## Problem

- Desk's Events answers what is coming, what must be decided before a deadline, and where the brand stands.
- The expensive half is unbuilt and fully generic: sources, scheduled discovery, extraction, dedup, reminders.
- Building that half inside Desk means building it again for the next product that tracks events.

---

## Concepts

| Concept | Is | Scope |
|---|---|---|
| catalog | a curated namespace of events with its own taxonomy, sources and reviewers | shared: one catalog may serve many organizations |
| event | something that happens at a time and place, once or as one edition of a series | catalog |
| occurrence | one session of an event: a showtime, a day of a fair | event |
| series | a recurring event brand, such as a fashion week; its editions are events | catalog |
| place · organizer | deduplicated venues and organizers | catalog |
| source | where events come from: a Harvest pipeline, an ICS or RSS feed, manual entry, an import | catalog |
| observation | one extracted record from a source, with provenance, waiting to match or be reviewed | catalog |
| pipeline (tracking) | the stages and custom fields one organization tracks events with | organization |
| tracking | one organization's record about one event: stage, priority, notes, fields, references | organization |

- an event exists whoever tracks it; tracking is private and never changes the event.
- the service knows no product's vocabulary: kinds, stages and custom fields are configuration.
- product entities (products, catalogue editions, campaigns) attach to tracking by opaque reference only.

---

## Entities

### Event

| Field | Type | Rule |
|---|---|---|
| `id` | UUID v7 | |
| `catalog` | slug | owning catalog |
| `key` | slug, optional | import key `^[a-z0-9][a-z0-9-]{0,63}$`, unique per catalog |
| `title` | localized text | 1–200 per locale; at least one locale |
| `summary` | localized text, optional | ≤ 2,000 per locale |
| `kind` | taxonomy key | from the catalog's taxonomy, such as `fashion.runway`, `trade-fair`, `concert` |
| `tags` | string[] | free, lowercase |
| `series` · `edition` | id, label — optional | `edition` such as `2026` or `SS27` |
| `parent` | event id, optional | a festival's sub-event |
| `organizer` · `place` | ids, optional | `place` null for online-only |
| `attendance` | enum | `offline` · `online` · `mixed` |
| `audience` | enum | `public` · `trade` · `invite-only` |
| `status` | enum | `scheduled` · `postponed` · `rescheduled` · `cancelled` · `moved-online` |
| `starts` · `ends` | [When](#when) | `ends` optional and never before `starts` |
| `timeZone` | IANA | defaults to the place's |
| `occurrences` | Occurrence[] | empty when the event is one continuous span |
| `deadlines` | Deadline[] | |
| `offers` | Offer[] | tickets, exhibitor terms, fees |
| `website` · `ticketUrl` · `onlineUrl` | URLs, optional | http(s) ≤ 2,048 |
| `images` | file references | in WoW2's File Storage instance — [Media](#media) |
| `languages` | locale[] | languages the event runs in |
| `externalIds` | map source → id | dedup by source identity |
| `provenance` | SourceRef[] | every source that reported it: source, URL, observed at |
| `review` | enum | `candidate` · `published` · `rejected` · `archived`; consumers see `published` |
| `confidence` | 0–1, optional | from extraction; null when entered by hand |
| `revision` · `createdAt` · `updatedAt` · `publishedAt` | | optimistic concurrency on `revision` |

### When

Dates are honest: an unknown day is never invented.

| Field | Values |
|---|---|
| `value` | `2026-03-14T19:00` · `2026-03-14` · `2026-03` · `2026` · null |
| `precision` | `minute` · `day` · `month` · `year` · `unknown` — must match `value` |
| `certainty` | `confirmed` · `announced` · `estimated` (predicted from earlier editions) |

- filters treat a month or year value as its whole span; sorting puts unknown last.

### Parts

- **Occurrence** — `id`, `starts`, `ends`, `place` override, `status`, `ticketUrl`.
- **Deadline** — `kind` (`application` · `registration` · `early-bird` · `submission` · `payment` · `other`),
  `at` (When), `label`, `url`.
- **Offer** — `kind` (`ticket` · `exhibitor` · `sponsorship` · `submission` · `other`), `name`, `price`
  (`min`, `max`, ISO 4217 `currency`; null when unknown, never 0), `free`, `terms` text, `url`, `availableFrom/To`.
- **Place** — `id`, localized `name`, `address`, `city`, `region`, ISO-2 `country`, `geo` (lat, lng), `website`.
- **Organizer** — `id`, `name`, `website`, `contact`.
- **Series** — `id`, localized `name`, `organizer`, `cadence` (`annual` · `biannual` · `seasonal` · `irregular`),
  `usualMonths`, `website`; the next edition is predicted as an `estimated` event.
- **Catalog** — `slug`, `name`, owner organization, `visibility` (`private` · `shared` · `public`), `locales`,
  taxonomy (key, localized label, parent), reviewers.

### Tracking

- **Pipeline** — per organization: `stages` (key, localized label, class `open` · `active` · `won` · `lost`),
  `defaultStage`, and a JSON Schema for custom `fields`.
- **Tracking** — `organization`, `event`, `stage`, `priority` (`high` · `normal` · `low`), `assignee`, `notes`
  (≤ 8,000), `fields`, `refs` (type and id pairs), `revision`, timestamps.
- **History** — every stage change with actor and time.
- **Scope** — derived per organization from its home country and region: `local` · `regional` · `international`.
- **Feed subscription** — a token URL serving ICS for a saved filter (`webcal://`).

---

## API

Version `v1`, `{ data }` envelopes, ProblemDetails failures, cursor paging, `Accept-Language` for localized text.

| Area | Endpoints |
|---|---|
| read | `GET /catalogs/{c}/events` (filters: `from`, `to`, `kind`, `country`, `city`, `q`, `status`, `deadlineBefore`, `includeUndated`), `GET …/events/{id}`, `GET …/series`, `GET …/places` |
| write | `POST` · `PUT` · `DELETE …/events/{id}` (curators), `POST …/imports` (bundle `wow2.events-import.v1`, `dryRun`) |
| review | `GET …/review` (candidates and observations), `POST …/review/{id}/accept` · `merge` · `reject` |
| sources | `GET` · `POST` · `PUT …/sources`, `POST …/sources/{id}/run` |
| tracking | `GET /organizations/{o}/tracking` (joined with events), `GET …/summary` (per stage, nearest deadlines), `PUT …/tracking/{eventId}`, `GET …/tracking/{eventId}/history`, `GET` · `PUT …/pipeline` |
| feeds | `GET …/events.ics?filter`, `GET /feeds/{token}.ics` |
| intake | `POST /harvest/items` — signed deliveries from Harvest |
| agents | read-only MCP tools: list, get, summary |
| out | webhooks `event.published`, `event.changed`, `event.cancelled`, `deadline.approaching` (P2) |

- *default*: consuming apps call with an API key scoped to catalogs and organizations until Identity lands;
  then OIDC client credentials. The app enforces its own users' membership before calling.
- *default*: browsers never call the service directly; the host app's backend proxies the routes its UI needs.

---

## Clients

- **be SDK** — `IEventsClient`: typed calls for read, tracking, review and imports; one registration with base URL
  and key; the same contract when the module runs in-process.
- **fe SDK** — feed components (month feed, deadline panel, event card, detail, tracking form, date-precision
  formatting, ICS export) calling the host app's proxy routes; texts in `uz`, `ru`, `en`.

---

## Harvest seam

[Harvest](harvest-service-spec.md) is the separate 24/7 harvester: it runs scheduled pipelines over sources, captures pages and posts, extracts
records into a schema the consumer names, and delivers them. It grows from ListingShelf's pipelines, runs and
captures; Events is one consumer of many.

- Events registers a Harvest pipeline per source: sources, schedule, schema `wow2.event.v1`, extraction
  instructions (such as "fashion events in Central Asia"), and its delivery URL.
- Harvest delivers items at least once: pipeline, item id, capture URL, captured at, content hash, schema version,
  model, prompt version, confidence, and the event-shaped payload.
- Events stores each item as an observation, idempotent on item id, then matches it: external id, then key, then
  fuzzy title, dates and city within the series or place.
- a match updates the event and records provenance; no match creates a `candidate`; nothing is published unreviewed.
- extraction runs once per content hash and prompt version; the model (DeepSeek, OpenAI) is Harvest's configuration
  through the AI gateway.

---

## Ocharo integration

- catalog `ocharo-fashion`, owned by Ocharo, `private` until sharing is decided; kinds: `runway`, `trade-fair`,
  `market`, `exhibition`, `competition`, `festival`, `conference`, `other`.
- pipeline: stages `candidate` · `shortlisted` · `applying` · `applied` · `confirmed` · `attended` (won) ·
  `skipped` · `rejected` (lost); fields `participation`, `cost`, `route` as text.
- home `UZ`; region: the Central Asian neighbours; scope derived, no longer stored.
- Desk keeps the Events page in its shell from the fe SDK components, proxies the routes, enforces membership, and
  attaches references to products, catalogue editions and Marketing campaigns.
- sources: Afisha first, then the nine reviewed directory links, each as a Harvest pipeline.

### Migration from `events.showcase_events`

| Desk field | Becomes |
|---|---|
| `title`, `organizer`, `website`, `sourceUrl` | event `title` (`uz`), organizer, `website`, provenance |
| `format` | `kind` |
| `country`, `city`, `venue` | place |
| `startsOn`, `endsOn`, `datePrecision` | `starts`, `ends` with precision; `estimated` → `certainty: estimated` |
| `applicationDeadline` | deadline `application` |
| `participation`, `cost` | tracking fields; `cost` also an exhibitor offer's `terms` when stated |
| `status`, `priority`, `notes` | tracking stage, priority, notes |
| `scope` | dropped: derived |
| `key` | event `key` |

---

## Media

Decided 2026-10-25 — [instances per owner](https://github.com/wow-two-sdk-beta/wow-two-sdk-beta.files/blob/main/product/product.md#instances-per-owner).

- event images live in WoW2's own File Storage instance, the one Harvest writes its captures to.
- an event references the capture's file instead of copying it; the reference keeps the file after Harvest prunes
  the capture.
- reviewers' uploads and replacements go to the same instance, owned by the catalog, never an organization.
- a consuming product's own files about an event, such as Ocharo's booth photos, stay in that product's instance and
  attach to its tracking by reference.

---

## Placement

- **Form 1 · library** — catalog, tracking and intake modules in the be SDK; components in the fe SDK.
- **Form 2 · self-hosted service** — `wow-two-platform.events`, hosting the module with a review console.
- **Form 3 · provided service** — one shared catalog per domain that many products subscribe to.

---

## Points

- [ ] EV1 — catalog sharing: Ocharo's catalog private, shared with chosen organizations, or public
- [ ] EV2 — Afisha intake: provider API, HTTP capture or a feed; terms of use; what Afisha lists for fashion
- [ ] EV3 — Harvest's repository: tracked as H1 in the [Harvest spec](harvest-service-spec.md)
- [ ] EV4 — reminders: through Notifications or a Telegram message from the service until Notifications exists

---

## Sequencing

1. Build the service in a WoW2 chat: entities, API, review, ICS, imports, `IEventsClient`, fe components, tests,
   deploy through Wheelhouse.
2. Ocharo: migrate `showcase_events` by bundle import, switch the Events page to the components, retire the table.
3. Harvest: pipelines for Afisha and the directory links; deliveries into review.
4. P2: reminders, webhooks, subscribed feeds, translations.

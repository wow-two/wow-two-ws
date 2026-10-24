# WoW Two Events — Shared Event Catalog and Tracking for Every Product

*Last updated: 2026-10-25*

> `wow-two-platform.events`: a catalog of dated opportunities — fairs, fashion weeks, exhibitions, competitions,
> conferences — that sources feed and reviewers curate, plus private tracking per organization. Shipped in the
> [capability forms](../conventions/development/capability-forms.md). First consumer: Ocharo Desk's Events feed.
>
> **Status:** the developer chose on 2026-10-24 to move Events into the SDK now (E1 in
> [Ocharo app boundaries](../workbench/mfts-projects/ventures/ocharo-hq/ocharo-ws/docs/app-boundaries.md)); the
> entity, sources and harvesting design comes next.

## Problem

- Desk's Events answers what is coming, what must be decided before a deadline, and where the brand stands.
- The expensive half is unbuilt and fully generic: sources, scheduled discovery, observations, dedup, reminders.
- Building that half inside Desk means building it again for the next product that tracks events.

---

## Two layers

| Layer | Holds | Scope |
|---|---|---|
| catalog | events, editions, sources, observations, review queue | shared knowledge: an event exists whoever tracks it |
| tracking | one record per organization and event: status, priority, notes, product fields | private to the organization |

- the catalog may serve many organizations at once; one curated fashion-event catalog serves every fashion brand.
- tracking statuses come from a pipeline each product configures; the service knows no product's vocabulary.
- product entities (products, catalogue editions, campaigns) attach to tracking by opaque reference only.

---

## Placement

- **Form 1 · library** — an `Events/` module in the be SDK (catalog, tracking, ingestion, ICS) and feed components
  in the fe SDK (month feed, deadline panel, event card, date-precision formatting, calendar export).
- **Form 2 · self-hosted service** — the module hosted as the `wow-two-platform.events` image, with a review console.
- **Form 3 · provided service** — one shared catalog per domain that many products and organizations subscribe to.
- Desk starts on Form 1; Form 2 waits for a second product that needs events.

---

## From Desk's code

Desk's Events is about 816 backend and 1,623 frontend lines, with 17 backend and 40 frontend test methods.

| Piece | Goes to | Why |
|---|---|---|
| event record, honest date precision, validation | SDK catalog | no Ocharo meaning |
| keyed bundle import (`ocharo.events-import.v1`) | SDK, renamed `wow2.events-import.v1` | idempotent import is generic |
| list, filters, summary of nearest deadlines | SDK | generic queries |
| ICS builder (RFC 5545 escaping, folding) | fe SDK | generic; `PRODID` becomes configuration |
| review step (candidate → shortlist or skip) | SDK tracking | generic triage |
| month feed, deadline panel, card, detail, form | fe SDK components | Desk composes them in its shell |
| read-only MCP tools | SDK | every product's agent reads events the same way |
| exhibitor statuses, `participation`, `cost`, route | Ocharo pipeline config + tracking fields | Ocharo's decision vocabulary |
| `scope` relative to Uzbekistan | SDK, computed from the organization's home country | generic once relative to a home |
| fashion `format` values, seed sources | Ocharo catalog config and data | domain content |
| links to products, editions, campaigns | Desk | Ocharo's entities |
| the rule that Desk never applies or pays | Desk | product policy |

---

## Features

P1 is what Ocharo needs next; P2 completes the vector; P3 waits on a named consumer.

### Catalog

- event: title, organizer, kind from a configured taxonomy, place (country, city, venue, coordinates), dates
  with precision, typed deadlines (application, registration, early bird), website, source links (P1).
- editions: one recurring event, one edition per year; next edition predicted from the last (P1).
- translations of title and description per locale (P2).
- search and filters by date, place, kind and deadline; ranking by deadline nearness (P1).

### Ingestion

- sources registry: ICS, RSS, web page, provider API, Telegram channel; schedule and reliability per source (P1).
- scheduled discovery: each source fetched on its schedule into observations with provenance (P1).
- observations → candidate or update; fuzzy dedup on title, dates and city; merge with history (P1).
- review queue: accept, merge, reject; nothing reaches the catalog unreviewed (P1).
- AI extraction from free text through the AI gateway, always into review (P2).
- keyed bundle import for bulk seeding (exists in Desk).

### Tracking

- per-organization record: status from the product's pipeline, priority, notes, assignee, product fields (P1).
- activity history per record (P2).
- reminders before each deadline through Notifications: Telegram first, email later (P2).
- links to product entities by opaque reference (P1).

### Distribution

- list and summary API; read-only MCP tools (exist in Desk) (P1).
- ICS download (exists) and a subscribed `webcal` feed per filter (P2).
- webhooks on new and changed events (P2); public catalog page per domain (P3).

---

## Sequencing

1. be SDK: catalog and tracking modules from Desk's code, renamed and configured; ICS to the fe SDK.
2. be SDK: sources, observations, dedup and review queue; scheduled discovery on the SDK jobs.
3. Desk: consume the module; keep the exhibitor pipeline, fields, seed sources and product links.
4. P2 across the vector; Form 2 when a second product tracks events.

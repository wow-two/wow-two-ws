# SCFD entity model — entity types over the collector

*Started: 2026-11-18. Settles point by point with the developer in `ev-ai`. Task: wow2 `pln-tasks.md` `app-t-010`,
deadline 2026-11-30. Builds on [scfd-ai-layers](scfd-ai-layers.md) (two AI layers) and the subscription selector design
(`system/sessions/events-integration/subscription-modes/subscription-modes.md`).*

## Status

- ✅ #1 entity-type architecture: a basic collector with entity-type modules on top (developer, 2026-11-18)
- ✅ #2 events become one record per real event, with history by year and a predicted next edition (developer, 2026-11-18)
- ⬜ #3 posts and entities are two things, joined by a relation — proposed
- ⬜ #4 the entity-type list — proposed
- ⬜ #5 the post-form list — proposed
- ⬜ #6 domains and subdomains — proposed
- ⬜ #7 event identity: editions, series, cadence — proposed
- ⬜ #8 two feeds: posts and entities — proposed

## #1 Architecture

- The developer: "we'll have a basic scfd where it just collects entities from given sources with pipelines and other
  components or maybe completely other sources wrapped on top of scfd - this helps us process everything accordingly
  with the logic they need".
- Core: sources, pipelines, captures, posts, dedup, link checks, the two AI layers. It knows nothing about any entity
  type.
- Entity-type modules sit on top, one per type, each with its own logic:
  - events: connect the dots across sources and years, one event record, past editions bound to it
  - marketplace: dedup across sites, market price research
  - news: its own components, later
- Other sources may wrap SCFD and feed the same modules.

## #2 Events as one source of truth

- One record per real event; every post or article about it binds to it (developer: "one entity / one source of truth
  for events we need").
- History: a subscriber searching fashion events gets Visa Fashion Week Tashkent with the years it ran, then every
  source's posts for a chosen year.
- Prediction: a new event in November is recorded once, with a predicted next edition; a second edition a month later
  makes the cadence monthly or quarterly.
- Uses: analyze events on a calendar, predict the next one, audit recurring events.

## #3 Posts and entities (proposed)

- A post is what a source published; an entity is the real-world thing it is about. Many posts, many sources, one
  entity.
- A relation joins them, with a role:

| Role | The post… | Example |
|---|---|---|
| `announces` | names a future edition: dates, place, how to take part | "Visa Fashion Week Tashkent 2026 will unite…" |
| `reports` | describes an edition that happened | "First day of TFT Expo 2026. Photos" |
| `mentions` | is about something else, or about the entity without dates | "Met Gala 2027 theme announced" |
| `lists` | is the entity's own offer | an OLX rental listing |
| `calls` | opens applications or a deadline | "Applications open for the XI Tashkent Biennale" |

- The Met Gala case: the post is news that `mentions` the Met Gala 2027 edition. Whether Ocharo cares is a question
  about the entity (an event Ocharo cannot attend), not about the post; the post stays in the post feed as context.

## #4 Entity types (proposed)

| Type | What it is | Sources seen |
|---|---|---|
| `event` | one edition of a happening, with dates and a place | Afisha, iTicket, ShowGo, expo sites, Instagram |
| `event-series` | the recurring event its editions belong to | derived from editions (#7) |
| `listing` | an offer: a good, a property, a vehicle, a service or a job, with its own subtype | OLX, BirBir, Joymee, Domtut |
| `organization` | an organizer, brand, venue operator or publisher | named by events and listings |
| `place` | a venue or address | named by events and listings |
| `opportunity` | a call, competition entry, grant or tender with a deadline | Hunarmand calls, contests, biennale calls |

- News has no entity of its own: an article is a post that `mentions` or `reports` entities.

## #5 Post forms (proposed)

- `announcement`, `report`, `news`, `listing`, `call`, `schedule`, `review`, `promo`, `interview`, `gallery`
- The tagging pass (layer 1) gives the form; the relation role (#3) follows from form plus entity.

## #6 Domains (proposed)

- Domains reuse the selector design's 14 subject areas (category → sub-category) so one vocabulary serves tags,
  subscriptions and entities: fashion and crafts, arts and culture, music, business and trade, tech, medicine and
  health, education, food, sport, real estate, auto, tourism, kids and family, other.
- Fashion's subdomains: apparel, textile, accessories and jewelry, handmade and crafts, design, beauty.

## #7 Event identity (proposed)

- Edition match: the same normalized name (Russian, Uzbek and English forms, translit), an overlapping date window
  and the same city make one edition across sources.
- Series match: the edition's name without its year or ordinal ("9th", "2026") plus organizer or venue names the
  series.
- Cadence: from two or more edition dates — annual, semiannual, quarterly, monthly — with a confidence; the next
  edition is the last date plus the cadence, marked predicted until a source announces it.

## #8 Two feeds (proposed)

- The post feed stays as today: every collected post with its tags.
- The entity feed carries entity changes: created, edition added, dates confirmed, predicted, merged.
- A subscription chooses posts, entities or both; Ocharo's calendar reads the entity feed.

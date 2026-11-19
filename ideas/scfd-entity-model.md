# SCFD entity model — entity types over the collector

*Started: 2026-11-18. Settles point by point with the developer in `ev-ai`. Task: wow2 `pln-tasks.md` `app-t-010`,
deadline 2026-11-30. Builds on [scfd-ai-layers](scfd-ai-layers.md) (two AI layers) and the subscription selector design
(`system/sessions/events-integration/subscription-modes/subscription-modes.md`).*

## Status

- ✅ #1 entity-type architecture: a basic collector with entity-type modules on top (developer, 2026-11-18)
- ✅ #2 events become one record per real event, with history by year and a predicted next edition (developer, 2026-11-18)
- ✅ #3 posts and entities are two things, joined by a relation (developer, 2026-11-18: "looks perfect to me")
- ✅ #3.1 the relation's role: four roles, cancellations inside `update` (developer, 2026-11-19: "great")
- ✅ #9 every AI-chosen value has an unsure way out that flags the post for a prompt or enum fix (developer, 2026-11-19)
- ✅ #4 entity types: `event` and `listing` now; `opportunity` later with job boards (developer, 2026-11-19)
- ✗ #5 a separate post-form field: dropped, since the relation's role plus the entity type say what a post is
- ✅ #6 domains: one list for every entity type, built on IAB Content Taxonomy 3.1 tier 1 with our own labels (developer, 2026-11-19: "confirmed one list of iab with different labels")
- ✅ #6.1 34 of IAB's 37 tier-1 entries are domains; `Events`, `Genres` and `Sensitive Topics` are not (developer, 2026-11-19: "yes correct")
- 🔄 #6.2 subdomains and exact searches such as textile — proposal under review
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

## #3 Posts and entities

- A post is what a source published; an entity is the real-world thing it is about. Many posts, many sources, one
  entity (developer, 2026-11-18: "looks perfect to me").
- The Met Gala case: the post is news that mentions the Met Gala 2027 edition; whether Ocharo cares is a question about
  the entity, and the post stays in the post feed as context for it (developer: "100% agreed").
- The relation's role is refined field by field, one per iteration (developer: "we'll work in a few iterations, mark it
  complete then work on other fields").

### #3.1 Role

Iteration 2 listed 15 roles. The developer asked to merge them: "one for first announcement, one for any update including
cancellations, mentions only mention like not announcement yet". Four roles cover every entity type:

| Role | The post… | Effect on the entity | Folds in from iteration 2 |
|---|---|---|---|
| `announcement` | states the entity's facts: an edition's dates and place, an offer's terms, a call's deadline | the earliest one creates the entity or confirms a predicted one; a later one with the same facts changes nothing | `announcement`, `listing`, `reminder`, `promotion` when it carries the facts |
| `update` | changes a fact already known | applies each change in `changes`, keeping the old value in history | `program`, `registration`, `postponement`, `cancellation`, `extension`, `result`, `withdrawal` |
| `report` | covers an edition while or after it happens | marks the edition held | `report`, `review` of a held edition |
| `mention` | refers to the entity without its facts, often before any announcement | none; attaches as context | `mention`, `promotion` or `review` without facts |

- An `update` relation names what changed, one or more of: `dates` (a postponement), `place`, `price`, `program`,
  `registration`, `deadline`, `results`, `status` (`cancelled`, `postponed`, `sold-out`, `withdrawn`).
- "First announcement" is computed, not tagged: the earliest `announcement` relation of an entity.
- A digest post holds one relation per entity it lists.
- A source's own lifecycle signals, such as an OLX link going gone or relisted, stay link states.
- `report` keeps its name; `coverage` was weighed and found vaguer (developer, 2026-11-19: "we can stick to report").
- The same author's later ad or edit is an `update`; another author's ad is an `announcement` (developer, 2026-11-19:
  "from the same author - update, from others - announcement").
- A second ad for the same listing, by another author or on another site, is another `announcement`; deduplication is
  the binding, not a role. Each announcement keeps its own author, price and link, so the listing shows every offer and
  its price spread; the earliest is the first announcement.
- Listings use `announcement` (the ad) and `update` (a new price or terms, a "sold" post); `mention` is rare and
  `report` never applies, since a listing is not held. A re-captured ad whose price changed is an `update` read from the
  revision diff, with no model call.

## #4 Entity types

- Two now (developer, 2026-11-19: "I can only see 2 value things here - event and listing"):
  - `event`: something organized, with dates and a place. A recurring event is one record; each run of it is an
    occurrence inside that record (#7), so the history by year needs no second type.
  - `listing`: an offer of a good, a property, a vehicle or a service. Like an event, it is one record across sources
    (developer, 2026-11-19: "we'll need a single entity just like events for dedup here as well"): every ad for the same
    flat or item, by any author on any site, binds to it.
- `opportunity` (jobs, calls, grants) comes later, with job-board sources (developer: "we can source collect job boards
  for this but I don't need this right now").
- News is not an entity type: an article is a post that announces, updates, covers or mentions entities.

## #5 Post forms (dropped)

- `announcement`, `report`, `news`, `listing`, `call`, `schedule`, `review`, `promo`, `interview`, `gallery`
- The tagging pass (layer 1) gives the form; the relation role (#3) follows from form plus entity.

## #6 Domains

- One list serves events and listings alike: a `fashion` domain holds fashion weeks and clothing ads, so Ocharo can
  follow both. Type-specific detail, such as OLX's category path or an event's format, is a later field of its type.
- Basis: IAB Tech Lab Content Taxonomy 3.1 tier 1 (37 entries, [IAB file](https://github.com/InteractiveAdvertisingBureau/Taxonomies/blob/main/Content%20Taxonomies/Content%20Taxonomy%203.1.tsv)),
  each domain keyed by our own slug, carrying the IAB ID, with labels in ru, uz and en.

### #6.1 Which entries are domains

- Keep 34: Attractions, Automotive, Books and Literature, Business and Finance, Careers, Communication, Crime, Disasters,
  Education, Entertainment, Family and Relationships, Fine Art, Food & Drink, Healthy Living, Hobbies & Interests,
  Holidays, Home & Garden, Law, Medical Health, Personal Celebrations & Life Events, Personal Finance, Pets, Politics,
  Pop Culture, Real Estate, Religion & Spirituality, Science, Shopping, Sports, Style & Fashion, Technology & Computing,
  Travel, Video Gaming, War and Conflicts.
- Leave out 3 that are not subjects: `Events` (our entity type), `Genres` (media genres), `Sensitive Topics` (a
  brand-safety flag).

### #6.2 Subdomains and exact searches (proposed)

The developer: "how one subscriber can search for textile exactly?" IAB has no textile node: the closest are
Business and Finance › Industries › Apparel Industry (`113`, the trade) and Hobbies & Interests › Arts and Crafts ›
Needlework (`253`, the craft). Three layers answer it:

| Layer | What it is | Textile example |
|---|---|---|
| category | closed tree: IAB tiers 1-4 plus our own extension nodes, each with an ID and ru, uz, en labels; a post or entity carries a primary and secondary categories | our node Style & Fashion › Textiles (fabrics, yarn, weaving, atlas and ikat), beside IAB `113` for a textile trade fair |
| topic | open tags the tagging pass writes in normalized form, merging ru, uz and en words | `textile` from "текстиль", "ткань", "to'qimachilik", "atlas" |
| prompt | a subscriber's sentence compiled once into categories and topics (selector design) | "textile trade fairs in Central Asia" |

- A subscriber picks the Textiles node and gets exactly that; a topic catches what no node names yet.
- Topics that recur under no node become proposed extension nodes in the unsure-flag review (#9).
- IAB itself marks rows with an `Extension` column, so our nodes sit in the same table under our own IDs.

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

## #9 Unsure flags

- The developer: "if unsure - we need a way to just flag the post so that we can fix the prompt, add a new enum if
  needed".
- Every value the AI picks from a list (role, entity type, post form, domain, change kind) allows `unsure`, with a short
  reason and, when it fits, a proposed new value.
- A flagged post still gets its other fields; only the unsure field waits.
- Flags gather in a review list per use case and field, counted by proposed value, so a value proposed often becomes a
  new enum entry and a new prompt version, checked by an eval before it ships.
- Where it lives: the AI library keeps the flags beside the inference log, so every product's prompts get the same loop
  (proposed; built with the first SCFD use case that needs it).

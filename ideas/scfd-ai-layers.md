# SCFD AI layers — how SCFD classifies and parses what it collects

*Started: 2026-11-17; last updated 2026-11-17. Settles point by point with the developer in `ev-ai`. AI library: `wow-two-sdk-beta.ai`
([analysis](ai-layer-analysis.md)); first consumers: Ocharo's events, Haven's rent listings.*

## Status

- ✅ #1 two layers, both inside SCFD (developer, 2026-11-17)
- ✅ #2 triage runs on every post with a small prompt on a cheap model (developer, 2026-11-17)
- ✅ #3 extraction prompts per domain and type, never per source (developer, 2026-11-17, correcting an earlier
  per-source pick)
- ✅ #4 extraction runs only for triage results a subscription wants; a new subscriber backfills (developer, 2026-11-17)
- ✅ #5 one use case per layer, category and kind, each with its own eval sets (developer, 2026-11-18: "yes I think it fits - we'll later analyze what other prompts we'll need for ocharo based on that harvested data")
- ✅ #6 triage fields beyond the two taxonomy axes, plus an English title (developer, 2026-11-17: "confirmed extra fields, can also add a translated title as well - for english translations")
- ⬜ #8 one vocabulary with the subscription selector design (orchestrator `ocharo - scfd integration`, 2026-11-17) — adopted here, its taxonomy decisions sit with the developer there
- ⬜ #7 one canonical shape per kind and category: a base type shape plus a category extension — proposed; waits on the selector design's taxonomy decision (#8)

## #1 Two layers

- Layer 1, triage: what the post is — type and subtype (listing › apartment rent, listing › car, event › fashion
  show), language and topic tags; product-neutral.
- Layer 2, extraction: the fields of that type, parsed as exactly as the source allows — for a listing, owner or
  agent, deposit, utilities; for an event, organizer, dates, fees, deadlines.
- A per-product layer is rare and lives in the product (developer: "layer 3 will be useful but extremely rare plus
  mostly will be on the product side itself"). SCFD answers what products need with no work of theirs ("it's priceless
  intel service that boosts other services because those services can get all the data they need with 0 effort").
- Relevance such as "a fashion event" is a triage subtype or topic, not a product verdict: Ocharo subscribes to
  `event` with topic `fashion`.

## #2 Triage on every post

- A small prompt on the cheapest model (Haiku 5.5) types every post, because a source's own category is too coarse:
  OLX mixes rentals, sales and cars, and Afisha's "events" section does not say which are fashion events (developer:
  "parsing cars with a big prompt that's meant for apartments will cost us more").
- The source's own category, when the page states one (OLX breadcrumbs, an Afisha section), rides into the prompt
  as a hint.

## #3 Prompts per domain and type

- An extraction prompt belongs to a domain (with an optional subdomain) and a content type: fashion events, apartment
  rentals, fashion articles (developer: "we use prompt based on use case - for haven it's apartments, for ocharo it's
  fashion events - article etc").
- One prompt serves every source carrying that domain and type; a source's specifics, such as OLX's fixed value
  sets for listing fields, ride in as a variable, never as a prompt of its own.

## #4 Demand-driven extraction

- Extraction runs on a post only when an active subscription's filter wants its triage result; a car listing nobody
  subscribes to costs one triage call and stops there.
- A new subscription backfills: stored posts whose triage matches its filter get extracted then.

## #5 Use cases and evals

- One AI use case per layer, domain and type: `triage`, `extract-fashion-event`, `extract-realestate-rental`,
  `extract-fashion-article`; SCFD routes a triaged post to the use case of its domain and type.
- Eval sets belong to a use case; every use case serves many sources, so its report slices accuracy by `source:{key}`
  tags, which shows where one source's posts parse worse.

## #6 Triage fields

| Field | Why |
|---|---|
| category → sub-category | the selector's subject axis (`category:fashion-craft/fashion`, `category:real-estate/residential`); routes to the extraction prompt |
| kind → format | the selector's type axis (`type:event/trade-fair`, `type:listing/rent`, `type:news/report`) |
| `about` | what it describes: an event, a listing, an organization, a product — a photo report is an article about an event |
| `language` | picks prompts and checks Uzbek coverage |
| `region` | country and city, so a Tashkent-only subscription skips Samarkand posts before extraction |
| `timeframe` | upcoming, ongoing, past or evergreen; a past report still tracks a recurring series |
| `items` | how many events or listings the post holds, so a digest splits into one extraction each |
| `confidence` | below a bar, a stronger model re-triages before extraction spends |
| `titleEn` | the title in English; an English title passes through unchanged, so every product can show and search one language |

- The taxonomy is SCFD's operator-owned, versioned one from the selector design (#8), cached in the system prompt;
  every post gets tags whether or not a subscription wants them, so previews and counts stay honest. Geography stays a
  location filter, not a tag.

## #8 One vocabulary with the selector design

- The selector design (orchestrator `ocharo - scfd integration`) adds one `selector` subscription over two taxonomy axes
  and one AI tagging pass per post (`post-tags`). Layer 1 here is that pass; its axes replace "domain" and "type".
- Selector matching gates Layer 2 (#4); a per-subscription verdict stays on that subscription's delivery event.

## #7 Canonical shapes (proposed)

- Every type has a base shape (`wow2.event.v1` for events, `wow2.listing.v1` for listings); a domain adds an
  extension block (`fashion`: garment categories, exhibitor or visitor terms, fees, deadlines).
- Any product reads the same fashion-event shape (developer: "fashion events will be parsed in one absolute data shape
  anyone may ever need - regardless if it is ocharo or different product").

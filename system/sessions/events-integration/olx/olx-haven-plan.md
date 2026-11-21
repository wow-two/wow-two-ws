# OLX listings for Haven, AI-processed in SCFD

*Written 2026-11-21 by the `ocharo - sources and ai processing` lane from two read-only analyses (SCFD's AI path; Haven's
classification). Lane builds from it; the orchestrator and the developer own the decisions. Code pins: harvest
`4487070`, Haven `2ec543b8`.*

Developer, 2026-11-21: "we'll just add olx for haven, haven had used a lot last time, so analyze how we implemented ai for
afisha, then implmenet for olx based on haven's prompts - can improve the prompts, ran evals as well - make sure olx
source is ready for haven's integration after that, we had around 100K posts from olx for apartments a month so pretty
sure we can use it". Standing decision (ai `product/context.md:28`): SCFD does the work; Haven is untouched and later
consumes SCFD like any product.

## Status

- Moved 2026-11-21: from B3 onward this plan belongs to the `haven - scfd` orchestrator and its lane (developer: "this
  chat is an orchestrator for scfd for haven"); B1 and B2 shipped here, B3 was stopped before any edit.

- ✅ O1 Dev state: OLX blocked on dev since 2026-11-13 (apartments 46 ads, then "fetch blocked"; houses and daily rent
  0; capture off); `site/www.olx.uz` `auto` → `manual` on 2026-11-21; `extract-listing` never ran (all zeros)
- ✅ O2 Listing extraction v2 (B1): harvest `d21cab0`; `extract-listing@2` in place, `{{attributes}}` / `{{seller}}`
  (OLX) and `{{section}}`, attribute lines back evidence, phone scrub on every pass incl. bare Uzbek mobiles; checker
  passed, all tiers green
- ✅ O3 Prompts: `v4-haven-base` (35.9K chars) and `v5` (17.4K, 48% of v4) with `schema-v2.json` in the notes folder
  `ai-evals/extract-listing/`; listing v2 is housing-only (`item` nests unit facts, no `service` offer); quotes may
  come from `{{attributes}}`; no provider structured output (41 nullable unions). Render check waits on B1.
- ⬜ O4 Listing route: no Layer 1 for OLX, Haven's demand, delivery to Haven (B2)
- ⬜ O5 Spend guard across Ocharo and OLX (B3)
- ⬜ O6 Evals: labelled OLX set, accuracy per field, cost per listing (B4)
- ⬜ O7 Dev rollout and Haven read-back; routing decision to the developer
- ⬜ D1 Egress for volume (developer)

## Verdict

- Path: Afisha's Layer 2, `extract-listing`, demand-driven, with the evidence check and listing entities; `rental-terms@2`
  folds into it and retires after parity (its 22 evidence tests stay as regression).
- Layer 1 (`post-tags`) is skipped for OLX: the section already says listing + real estate, so a code rule writes those
  tags. It halves calls, and Sonnet tagging (SR08) never touches listings.
- Haven's prompt v0.5 is the base, not the shape: SCFD keeps a code-owned schema with quoted evidence and no contacts.
- Volume sets the model: at ~100K listings a month Haiku 5.5 costs about $60-100 (estimate), Sonnet 5.5 about $1.5-2K.
  OLX runs on Haiku; Sonnet re-runs only flagged answers, inside the guard.
- A monthly spend guard (none exists) keeps Ocharo + OLX at or under ~$195 of the $200 credit.
- Haven gets the answers inside its existing delivery as `post.extracted` with `extras.listingAi`; its client already
  treats `post.extracted` as a capture.

## 1. What exists

| Piece | State | Evidence |
|---|---|---|
| OLX reader | apartments, houses, daily rent; newest first; 2 s pace; `olx.ad.v1` fields | `sources/Olx/OlxSourceAdapter.cs:13-19,56` |
| Haven profile | tenant `haven`, container `haven-listings`; 3 OLX searches + Joymee, BirBir ×2, Domtut; capture 2 h; 60 items a run | `sources/Module/Marketplace/MarketplaceProfiles.cs:13-38`, `MarketplaceProfile.cs:34-48` |
| Delivery | one `wow2.post.v1` subscription per search, filter `marketplace-listing-v1`; key `haven-supply` `events:read`; deterministic `extras.listing` (`housing-listing@1`) | `deployment.md:212-225`, `ListingSchemaMapper.cs:23-45` |
| `extract-listing` | schema with offer, price + period, location, item hints, `author.kind` (no contacts), `rentalTerms` with quotes; no prompt registered; answers reach no subscriber | `extraction.md:85-111`, `contract.md:189-192` |
| Dev | OLX blocked houses and daily rent on 2026-11-18; local pull works | `v0.2.md:333-335` |
| Egress | fixed proxy route `olx-ip-server` and its keys exist; S34 plans to delete them | `ConfiguredFetchTransportFactory.cs:36-49`, `deploy.yml:61-66` |
| Spend guard | none in harvest or the AI module | AI `backlog.md:25,32` |
| Haven's prompt | v0.5, 47.6K chars, ~45 fields, 5 listings a call, Haiku 5.5 → Sonnet 5.5 on failure; no labelled evals | Haven `Classification/Prompts/classify-prompt.md`, `Models/ClassificationOutputSchema.cs:7-152` |

## 2. Listing extraction v2 (O2, task B1)

**Inputs** (new prompt variables beside today's):

- `{{attributes}}`: the OLX dropdown attributes as `label: value` lines, Russian labels kept.
- `{{section}}`: the source section (`apartments-rent`, `houses-rent`, `daily-rent`), so a rent with no period keyword
  reads the section's period.
- `{{seller}}`: `business` · `private` · `unknown` from OLX's seller category when `olx.ad.v1` carries it.
- `{{title}}` and `{{text}}` are phone-scrubbed in code before rendering (`[phone]`); the evidence check runs on the same
  scrubbed text. No author name, phone or registration date enters a prompt.

**Schema** (code-owned; `extract-listing@2`): today's fields, plus Haven's that are not contacts:

| Group | Fields |
|---|---|
| Kind | `propertyKind` `apartment` · `house` · `room` · `bed-space` · `commercial` · `land` · `unsure`; `invalid` `not-a-property` · `multi-listing` · `null` |
| Offer | `offerType` `rent` · `sale` · `rent-or-sale` · `exchange` · `rent-to-own` · `unsure` |
| Price | `amount`, `currency` `usd` · `uzs` · `unsure`, `period` (adds `hour`), `negotiable`, evidence |
| Building | `propertyType` `new-build` · `secondary` · `unsure`, `buildingType` `brick` · `panel` · `monolithic` · `block` · `wooden` · `unsure`, `yearBuilt` |
| Unit | `rooms`, `layout` (Haven's enum), `areaM2` `{total, living, kitchen}`, `floor`, `floors`, `ceilingM`, `bathrooms` `{count, type}`, `renovation` (Haven's enum) |
| Furnish | `furnished` `yes` · `partly` · `no` · `unknown`; `apartmentAmenities[]`, `nearbyAmenities[]` (slugs) |
| Terms | `rentalTerms`: `deposit`, `advanceRent`, `utilities`, `minimumStay`, plus `commission`; each `{status: unknown · absent · present · conflict, claims: [{evidence, value}]}`, so "no commission" is `absent`, not unknown |
| Tenants | `acceptedTenants[]`, `excludedTenants[]` (Haven's enum) |
| Author | `author.kind` `owner` · `agent` · `agency` · `developer` · `management-company` · `unknown`; `noAgents` |
| Place | `location` `{district, city, address}`; `landmarks[]` `{type, name, evidence}` |
| Urgency | `urgent` |

- Attributes win for unit facts unless the text contradicts them; a contradiction is a flag, not a pick.
- No invented defaults: deposit without an amount is `present` with no value; dates never fall back to capture time.
- Currency stays as written; the rent/sale price thresholds move to code with a rate setting.
- Structured outputs on the provider call where the AI module supports it; a `max_tokens` stop is a retryable failure.

## 3. Prompts (O3, task P1)

- v1, Haven baseline: Haven v0.5's rules mapped onto the v2 schema, contacts removed, examples made synthetic.
- v2, improved: Haven's weak spots fixed -- currency, period by section, `absent` vs unknown, no invented defaults,
  property kind, dialect (Uzbek Latin and Cyrillic, ~15-20% of OLX), marketing terms (`евродвушка`) kept as text, not
  rooms; keyword lists trimmed where attributes carry the fact.
- Drafts live outside every repo, beside SCFD's earlier `extract-listing` v1-v3 drafts and their 10-item eval sets: the
  orchestrator's notes folder `ai-evals/extract-listing/` (`v4-haven-base.prompt.json`, `v5.prompt.json`); registered
  on dev with `extract prompt --use-case listing --file …`.

## 4. Listing route (O4, task B2)

- OLX sections imply tags: a section declared `listing` + its real-estate node writes `type:listing` and `domain:` tags in
  code with tier `Rule`, and queues extraction directly; no `post-tags` call.
- Haven's demand: `Harvest:Processing:Extraction:Wanted:1` = `listing` + `real-estate` (`deploy.yml` declares `:1`).
- `marketplace setup --model-processing off|manual|auto`, as `ocharo setup` has.
- Delivery: a done listing answer raises `post.extracted` on the post's subscriptions, carrying `extras.listingAi`
  `{schema: "extract-listing@2", promptVersion, model, costMicroUsd, captureId, answer, flags}`. Haven's key stays
  `events:read`. Tag-only revisions raise nothing for marketplace subscriptions.
- Contract: `contract.md` § Listing delivery and `deployment.md` § Haven, written for Haven's later integration.
- Rental terms: `rental-terms@2` stays until the evals show `extract-listing@2` at parity on its 22 cases, then retires.

## 5. Spend guard (O5, task B3)

- Settings: `Harvest:Processing:Budget:MonthlyUsd` (hard cap; none = off), `:SoftShare` (default 0.8),
  `:CycleStartDay` (credit cycle start, 25 for the cycle ending on the 24th).
- Month-to-date cost comes from the AI inference log for the cycle, all use cases.
- Below soft: every route as configured, flagged-answer escalation to Sonnet allowed.
- Soft to hard: the workers use each use case's last route only (Haiku); no escalation.
- At hard: the workers stop claiming; queued work waits for the next cycle or a raised cap. `processing budget` prints
  cycle, spend, projection and state.
- It moves to the AI service's budgets once that service deploys (ai `context.md:27`).

## 6. Evals (O6, task B4)

- Set `olx-listings-v1`: 80 OLX listings, stratified by section and language (ru, uz-Latin, uz-Cyrillic), phone-scrubbed;
  from stored dev posts when OLX fetches there, else from a bounded local capture.
- Labels: attributes give the gold for unit fields; for text fields a reference answer from Opus 5.5, then a field-by-
  field review against the quoted evidence by a fresh agent; reviewed items lose `unreviewed`.
- Matrix: prompts v1 and v2 × Haiku 5.5 and Sonnet 5.5; report accuracy per field, invalid and failure rates, tokens,
  p95, cost per listing; plus `rental-terms@2`'s 22 cases on v2.
- Pass bar for v2 on Haiku: ≥ 90% on offer, period, price, rooms, author kind; ≥ 80% on terms and tenants; no contact
  in any output.

## 7. Routing and spend (decision for the developer, after O6)

| Use | Volume a month | Route | Estimate |
|---|---|---|---|
| Ocharo `post-tags` | ~450-3,000 posts (grows by wave) | Sonnet 5.5 → Haiku | $20-110 |
| Ocharo `extract-event` | ~10% of posts | Haiku 5.5 | < $1 |
| OLX `extract-listing@2` | up to ~100K listings | Haiku 5.5 | $60-100 |
| OLX escalation | flagged answers, ~5% | Sonnet 5.5 | ~$50-75, guard-capped |
| Guard | | hard $195, soft 80% | |

- Every figure is an estimate until O6 and O7 measure it; the measured row replaces it.

## 8. Order and tasks

| Id | What | Done when | Depends |
|---|---|---|---|
| O1 | Read `marketplace status --profile haven`; Haven sources `auto` → `manual` | outputs recorded; no Haven source `auto` | — |
| B1 | Listing extraction v2 (#2) | unit tests: schema, variables, scrub (no phone survives), normalizer; build passes | — |
| P1 | Prompt drafts v1, v2 (#3) | both drafts render against B1's variables; no real contact in examples | B1 schema |
| B2 | Listing route (#4) | tests: OLX post skips `post-tags` and queues extraction; `post.extracted` carries `extras.listingAi`; E2E passes | B1 |
| B3 | Spend guard (#5) | tests: soft drops escalation, hard stops claiming; `processing budget` prints state | B2 |
| B4 | Eval set and labels (#6) | 80 items, gold reviewed, no contact in items | B1, O1 |
| O7 | Release; register prompts on dev; run the matrix; Haven profile `manual` → `auto`; Haven key pulls `post.extracted` | eval report in the version track; measured cost per listing; a Haven pull shows `extras.listingAi` | B2, B3, B4, P1 |
| D1 | Egress: a dedicated outgoing server for OLX (allowed; rotating pools are not) | the developer's pick; then secrets by `wow2` CLI and the bounded acceptance | — |

- One builder writes harvest at a time: tests share the solution's build output.
- Sourcing rules bind: paced, inside `robots.txt`, no challenge solving; contacts stay out of prompts, evals, fixtures
  and reports.

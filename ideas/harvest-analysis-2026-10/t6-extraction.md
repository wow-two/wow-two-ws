# T6 — Extraction and classification

*Last updated: 2026-10-26*

> What Harvest extracts from a capture, in what order, at what cost, and how the shared pool gets tags. Harvest keeps one
> small base envelope, `wow2.post.v1`, filled by a five-tier cascade: deterministic parsers, rules, embeddings, a small
> LLM, a large LLM. Tiers D and R always run; E, S and L run only when a pipeline switch, a per-source `ai_allowed` gate,
> the host's content signal and a budget all allow it. Structured sources (JSON-LD `Event`, OLX price text) fill most fields
> with no model, so a consumer schema such as `wow2.event.v1` becomes a declared mapping first and an LLM call only for
> gaps. At modest scale the whole AI line is about $20–50 a month; the larger costs sit in Haven's own 48-field
> classifier and in provider fees, not in tags. For Uzbek, PostgreSQL has no text-search configuration: the measured
> setup is `simple` plus prefix queries, apostrophe normalisation, Cyrillic-to-Latin transliteration and trigrams, in a
> database created with a UTF-8 locale.

Legend: **(U)** = could not verify. Tiers: **D** deterministic · **R** rules · **E** embeddings · **S** small LLM ·
**L** large LLM. Gates: **G1–G5** (section 2.2). Prices read 2026-10-26 from the providers' pages (section 5.1); Haven's
figures from `ai-cost-analysis.md` (2026-03-05). **Own measurements:** a throwaway PostgreSQL 17.4 cluster on the
developer's Mac, two databases (`en_US.UTF-8` and `C`), removed afterwards; PostgreSQL 18 not tested. Volumes
marked (U) have no measurement behind them. T5 owns tables and dedup, T7 pipelines and delivery, T8 placement.

---

## 1. The base envelope `wow2.post.v1`

Every capture yields exactly one envelope, whatever the source. Nothing in it needs a model; a model may fill gaps and
is always recorded. Identity, canonical URL, capture time and content hashes are T5's; the rows below are T6's.

### 1.1 Fields

| Field | Shape | Rule |
|---|---|---|
| `kind` | enum `event` · `listing` · `offer` · `news` · `promo` · `discussion` · `other` | source default first (an `Event` node, an OLX category), then rules, then S |
| `title` | text or null | verbatim; null for channel posts; never generated |
| `text` | text | verbatim, Unicode NFC; HTML flattened, anchors kept in `links` |
| `author` | `{name, handle, url}` | API or markup; a phone number as the name moves to `contacts` (52 of 1,416 OLX listings) |
| `postedAt` | `{value, precision, tz}` | publish time of the post, not the event's; relative text ("Сегодня в 10:15", "N days ago") parsed by rules |
| `language` | `{code, script, mixed, conf}` | `uz` · `ru` · `en` · `other` · `und`; script `Latn` · `Cyrl`; section 4.3 |
| `media[]` | `{type, url, fileRef, hash, w, h, role}` | source URLs always; `fileRef` once fetched into File Storage (T5) |
| `links[]` | `{url, kind, text}` | `kind` by host table: ticket · social · messenger · map · site · other |
| `location` | `{mentions[]: {text, kind, geo?}, geo?}` | raw mention text, `kind` city · region · district · street · venue · address; coordinates only when the source gives them |
| `prices[]` | `{amount or min/max, currency, per, negotiable, free, raw, role}` | amount as published; `null` unknown, never 0; `free` is its own flag; `role` listed · ticket · mentioned |
| `dates[]` | `{role, value, end, precision, raw, yearInferred}` | `value` ISO partial: `2026-03-14T19:00` · `2026-03-14` · `2026-03` · `2026` · `--03-14` (no year); `role` start · end · deadline · posted · mentioned |
| `contacts[]` | `{kind, value, raw}` | phone as `+998XXXXXXXXX`, handle, email, URL |
| `tags[]` | `{tag, score, tier, v}` | section 4 |
| `engagement` | `{views, reactions, comments, shares, at}` | a snapshot series outside the capture hash (T1-P10); hidden counts (Instagram `-1`) become null |
| `extras` | one namespace per source family | section 1.2 |
| `fieldSources` | map field → `{tier, rule or parser id}` | provenance per field; T3 asked for it |
| `flags[]` | strings | `low_confidence` · `dialect_unverified` · `date_precision_guess` · `tier_disagree:{field}` · `ai_refused` · `ai_skipped:{gate}` |
| `extraction` | `{normVersion, rulesVersion, tiersRun[], ai?: {model, promptVersion, at, tokens}}` | what ran, with versions |

- every field except identity is nullable; a missing value is `null`, never a default.
- `text` stays in the source language; Harvest translates nothing and generates no summary (AI-only fields stay out
  of the base).
- dates keep their honesty: "September" is `2026-09` at `month` precision, not 1 September (Ocharo's rule, T4 §2).

### 1.2 Per-family extras

| Namespace | Holds | Evidence |
|---|---|---|
| `telegram` | `chat`, `messageId`, `forwardOrigin {kind, chat, messageId, authorSignature}`, `isAutomaticForward`, `mediaGroupId`, `edited`, `replyTo`, `threadId`, `hasProtectedContent` | T1 §2.2, §4; forward origin is the dedup key where present (T1-P10) |
| `schemaOrg` | every node by `@type` with `@id` resolved: for `Event` — `startDate`, `endDate`, `previousStartDate`, `eventStatus`, `eventAttendanceMode`, `location` (`Place`, address, `geo`), `offers`, `performer`, `organizer`, `subEvent` / `superEvent`; also `Product`, `Article`, `LocalBusiness` | T3 §2.2; lets a consumer map to its schema with no LLM |
| `openGraph` | `og:*`, `article:published_time`, oEmbed type | T3 §2.7 |
| `listing` | the page's attributes verbatim, in captured order, labels untouched (OLX `parameters`, MOQ text, bed type) | ListingShelf schema 1.0 `attributes`; Sourcing and Haven break these down |
| `social` | `hashtags[]`, `mentions[]`, `placeId`, platform counters, `canceled`, `going` / `interested` counts (Facebook events) | T2 §5.1 |
| `feed` | RSS `guid`, `categories`; ICS `uid`, `sequence`, `status`, `rrule`, `lastModified` | T3 §2.6 |

- `extras` shapes are versioned per family and may gain fields in a minor version; a product must not depend on a key
  the family schema does not list.

### 1.3 Which tier fills what, by source family

`D` = deterministic from API fields, structured data or a per-source parser · `R` = rules (regex, lexicon, gazetteer) ·
`S` = needs an LLM when the source gives nothing structured · `–` = not applicable.

| Field | Telegram channel | Marketplace (OLX, Domtut) | Structured page (Afisha, mstar) | Brochure page (Tilda, Joomla) | Social (provider or API) | Feed (ICS, RSS) | Link intake (OG, oEmbed) |
|---|---|---|---|---|---|---|---|
| `title` | – | D | D (`name`) | D (`h1`, `og:title`) | – (D: Facebook events, YouTube) | D | D |
| `text` | D | D | D | D (main content) | D | D | D (description only) |
| `author` | D (channel, signature) | D, R (phone-as-name) | D (organizer) | R / S | D | D | D (oEmbed) |
| `postedAt` | D | R (relative text) | – (sitemap `lastmod` is not a publish date) | – | D | D | D (`published_time`) |
| `language` | R | R | D (`html lang`) + R | D + R | R | R | R |
| `media` | D | D | D | D | D | D | D (`og:image`) |
| `links` | D (entities) + R | R | D | D | D | D | D |
| `location` | R (D: venue message) | D (`location` text) | D (`Place`, `geo`) | R / S | D (events, place) / R | D (`LOCATION`, `GEO`) | – |
| `prices` | R | D (97.0% `NUMBER у.е.`) | D (`offers`); R when only in text | R / S | R | – | – |
| `dates` | R / S | – | D (`startDate`…) | R / S | D (Facebook events) / R | D (`DTSTART`…) | – |
| `contacts` | R | R (description text) | D (organizer) / R | R | R | R | – |
| `kind` | R from channel default, S if mixed | D (source default) | D (`@type`) | D (source default) | D (events) / R / S | D | D (`og:type`) / S |

- the 97.0% is 1,374 of 1,416 OLX listings reading `NUMBER у.е.` (Haven data report); Haven's own prompt parses
  `postedAtText` with the model today, which rules can take.
- Event nodes exist on 3 of the 16 sites T3 profiled (afisha.uz, mstar.uz, voyage.uz); the other 13 take R and S.
- T3's traps are parser rules, not model work: afisha.uz bucket dates are publish dates; uzexpocentre.uz dates omit the
  year (`yearInferred`); voyage.uz date-only events arrive as midnight UTC, so precision comes from the raw string.

### 1.4 Where Harvest stops and a product starts

Haven's 48 output fields (T4 §5) and `wow2.event.v1` (Events spec) draw the line.

| Group | Fields | Lives in |
|---|---|---|
| Haven, source-agnostic (6) | post ref, `AuthorName`, `PhoneNumbers`, `PostedAt`, `PriceAmount`, `PriceCurrency` | envelope: `externalId`, `author`, `contacts`, `postedAt`, `prices` |
| Haven, borderline (5) | `PricePeriod`, `PriceIsNegotiable` | `prices[].per`, `prices[].negotiable` |
| | `IsUrgent` | rule tag `urgent` ("срочно", "shoshilinch") |
| | `LocationSignals` | `location.mentions[]` raw text; landmark and district resolution stays Haven's |
| | `InvalidReason` (relevance) | not in the pooled post: relevance depends on one pipeline's instructions, so it is a pipeline verdict (section 3) |
| Haven, real estate (37) | property, rent terms, seller and deal readings, quality flags | Haven |
| Events, deterministic | `title`, `summary`, `starts` / `ends`, place text, `offers`, `website` / `ticketUrl`, `images`, `languages`, `externalIds`, `provenance` | envelope + `extras.schemaOrg.event`; a mapping, no LLM |
| Events, interpretation | `kind` against the catalog taxonomy, `status`, `attendance`, `audience`, `deadlines`, `series` / `edition`, `occurrences`, `certainty`, place and organizer matching | Events (mapping rules or its consumer-schema pass) |
| Sourcing | model, bed type, gauge, delivered price, lead time, FX conversion | Sourcing |

---

## 2. Tiers, gates and the AI switch

### 2.1 The cascade

Order is fixed: D → R → E → S → L. A later tier reads the earlier tiers' output as known facts and fills only what is
missing. S escalates to L only when its output fails validation after one repair or its confidence is under the
schema's threshold; L never escalates automatically (Opus-class is for gold-set labelling).

| Tier | What it does | Catches | Cost per post | Skipped when |
|---|---|---|---|---|
| **D** | API fields, JSON-LD / microdata / OpenGraph, per-source selectors, ICS / RSS | all envelope fields on structured sources; marketplace title, text, price, location, attributes | CPU only | never; a failed parser raises `unrecognized` (T3) |
| **R** | regex, lexicons, gazetteer, script and language rules; versioned, with test vectors | prices (`у.е.`, сум / so'm / сўм, млн / mln, ranges, "договорная" / "kelishiladi"), phones (`+998…`, 9-digit local), dates in uz / ru / en with month names in both Uzbek scripts, urgent, negotiable, free, link kinds, region / city mentions, keyword tags | CPU only | never |
| **E** | one multilingual vector per canonical post; nearest-centroid tags; kind for free text | tags and kind for posts whose words miss the lexicons; the vector also serves "similar" reads | $0.008 per 1,000 posts (text-embedding-3-small, 400 tokens) | G1–G5 deny; text under ~30 characters; same text hash already embedded |
| **S** | zero-shot tags on the remainder; gap-fill of base fields from free text; simple consumer schemas | date roles, prices and places in prose, tags E abstained on | ~$0.12 per 1,000 (Haiku 5.5) | gates deny; D / R / E left nothing missing at confidence ≥ τ; pipeline `ai=off`; budget hit; post judged out of scope by R / E |
| **L** | consumer schemas with many fields or hard reading | Haven-sized schemas, offers with terms, events from brochure prose | ~$5.7 per 1,000 (moderate schema) to ~$11.3 (48 fields), Sonnet 5.5 | as S, or S already produced a valid, confident item |

- expected share of posts that never reach S or L: all structured-source posts, almost all marketplace posts, all
  gated posts. Only free-text posts from AI-enabled pipelines on allowed sources get a model call.
- R and D run on every post even where AI is off; "Harvest always delivers captures" (developer, 2026-10-26) extends to
  "and the deterministic envelope".

### 2.2 Gates

Five checks decide the tier ceiling for one post: `ceiling = min(G1, G2, G3, G4, G5)`. D and R are never gated.

| Gate | Decides | Default | Waits on |
|---|---|---|---|
| **G1** pipeline switch `ai` | `off` (D, R only) · `gaps` (E / S / L only for what D and R left missing or low-confidence) · `full` (E / S / L on every in-scope post) | `off`; Haven's pipelines `off` (T4-8); Events' `gaps` | developer, per pipeline |
| **G2** source `ai_allowed` | `yes` · `no` · `unreviewed` (acts as `no` for E / S / L) | by family, table below | P3, T1-P1, S1 |
| **G3** host content signal | `ai-input=no` in `Content-Signal` blocks E, S, L for that host; blank means no preference; `ai-train=no` needs no action | read from `robots.txt` per host | W5 |
| **G4** data class | public pool vs a consumer's private container; each class has a provider allow-list | public: Anthropic, OpenAI; private: the consumer's list; DeepSeek only if a consumer opts in | developer; provider terms (U) |
| **G5** budget | monthly USD cap per pipeline and per provider; soft warning at 80%, hard stop (S7) | section 5.4 | T7 mechanism |

- G3 reading: the signal defines `ai-input` as inputting content into one or more AI models, so an embedding call and a
  self-hosted model count the same as an LLM call. The policy does not mention extraction or classification, so W5's
  rule stands and rests on the definition's plain words (U on enforcement).
- Harvest trains and fine-tunes nothing on captured content, v1 and later; centroids are means of curated examples, not
  training. That answers the `ai-train` half of every signal and the "train, fine-tune" half of Telegram §1.5.
- E counts as AI everywhere. The Telegram clause bars "development, enhancement or deployment" of AI; embedding Telegram
  text is inside that wording (conservative reading, T1 §2.6).

Defaults for G2 (the gate is a per-source field, so a decision moves one value, not code):

| Source | `ai_allowed` | Waits on |
|---|---|---|
| Open web, `permission` open or granted | `yes` | W5 for hosts with a signal |
| Restricted site (Afisha today) | not scheduled | W1 |
| Telegram public channel, group, comments, private chat (routes W, M) | `no` | P3 / T1-P1 — counsel on API Terms §1.5 |
| Telegram owner-installed bot, consented intake | `yes` | T1-P1: whether owner consent covers AI use (U) |
| WhatsApp intake (user forwards) | `yes`, with the consent notice | T1-P9 |
| Instagram, Facebook, TikTok through a licensed provider (Route B) | `unreviewed` | P3, S1, P4 |
| Meta official routes (business discovery, Page Public Content) | `unreviewed` | S1, S11 |
| X official, YouTube API | `unreviewed` | P3 (X Developer Policy not read, T2) |
| Link intake in a private container | `yes` (the submitter's act), unless G3 | W4, W5 |
| Hand-typed entry | `yes` | — |
| Consumer-owned credentialed source (RFQ inbox) | the consumer decides, provider list from G4 | T4-4 |

- consequence while P3 is open: Telegram posts get source-level and lexicon tags only; Meta-route posts get D and R
  until S1 resolves. The design runs end to end on D and R alone, so no Point blocks the build.

### 2.3 What the switch means for the pool

- a post's tags say how it was tagged: `extraction.tiersRun` lists the tiers; a subscriber reading tag `real-estate.rent`
  sees rule-tagged posts from AI-off pipelines at lower recall than embedding-tagged ones.
- the AI pass runs once per canonical post and is charged to the pipeline that enabled it (T5, T7). Another product
  that wants embedding tags on a channel whose pipeline has AI off joins or creates a pipeline with AI on; a keyword
  or tag subscription never triggers model calls (T6-5).

---

## 3. The optional consumer-schema pass

### 3.1 Registration

A consumer (Events, Sourcing) registers once per version, immutable:

- `schemaId` + `version` (`wow2.event.v1`) and the JSON Schema.
- `instructions`: scope sentence ("fashion events in Central Asia"), field notes, ≤8 examples; versioned with the
  schema. `promptVersion` = the instructions' label + SHA-256 of the rendered prompt, Harvest's fixed preamble included.
- `mapping` (optional): a declarative map from envelope and `extras` paths to schema fields, with a closed function
  set (`first`, `join`, `date`, `money`, `enum`); no scripting.
- `tierMin` / `tierMax`, `needsContacts` (default false: phones are masked before any model sees the text).

### 3.2 How Harvest runs it

1. Resolve gates (section 2.2).
2. Apply the mapping to the envelope. For a JSON-LD `Event` page this fills most of `wow2.event.v1` with no model.
3. Validate with a full JSON Schema validator. Complete and valid → item with `extractor: mapper`, done.
4. Missing fields and gates allow → one model request: Harvest preamble + instructions + schema as the stable prefix;
   user part = text plus the envelope's known fields, so the model fills gaps instead of re-deriving. The schema goes in
   `output_config.format` (structured outputs, supported on Haiku 5.5, Sonnet 5.5 and Opus 5.5).
5. Validate again. Claude's structured outputs reject numeric bounds, string-length bounds, array bounds beyond
   `minItems` 0 or 1 and recursion, and restrict regex patterns, so Harvest enforces those after generation; one repair request quotes the validator's
   errors; a second failure stores `invalid` (not retried until the version changes).
6. Store the item with per-field confidence and flags; deliver (T7).

- out of scope: the pass returns `scope: out` and no payload. The verdict is cached so the post is not asked again, and
  it is not delivered (spec § Extraction: out-of-scope posts yield no item).
- a refusal (`stop_reason: refusal`) is a status, `ai_refused`, never a blind retry (U on category handling).
- model batching: group the queue by `promptVersion` so the prefix caches; 5–20 posts per request (Haven runs 5 listings
  of ~2,000 tokens); validate per post so one bad post never fails the request.

### 3.3 Cache

- key: `(inputHash, schemaId, schemaVersion, promptVersion)`. `inputHash` hashes exactly what the model would see — the
  normalised text and known-fields block — not the raw page, so a changed view counter or timestamp never re-extracts.
- the model, tier and token usage are recorded on the item and are not in the key; switching providers does not
  invalidate items. An explicit `reextract` (with reason) replays under a newer model.
- changed capture → new `inputHash` → new extraction; unchanged → items reused (spec § Extraction).
- two consumers share an item only when schema, version and instructions are identical; private containers never share.
- the effort level is fixed per route: Claude's cache is keyed on the resolved effort and on `output_config.format`, so
  changing either mid-stream drops the cached prefix.

### 3.4 Why Haven keeps its own classifier

- its prompt (`classify-prompt.md`, 47,562 characters) takes Haven's district and landmark lists from its Location
  service on every request (`EnrichWithLandmarks`); a registered schema carries static instructions and has no slot for
  per-request context from the consumer's own data.
- 37 of its 48 fields are real-estate readings with domain rules (contact type from "Бизнес" and author names, negation
  such as "маклерам не звонить", the dialect fallback of v1.7), tuned against Haven's evaluation checklist and agent
  corrections, which are Haven's data (T4 §5).
- no cost gain: the same tokens go through the same model class; Harvest would add a hop and a second prompt
  version to reason about.
- Harvest serves it with captures and the deterministic envelope (price, phones, `postedAt`, location text, language,
  `urgent`). Whether Haven's prompt drops those fields is Haven's call.
- reopen when Harvest can accept per-request consumer context blocks (T6-12).

---

## 4. Classification for the shared pool

### 4.1 Who owns the taxonomy

| Layer | Owner | Shape | Notes |
|---|---|---|---|
| `kind` | Harvest, closed | 7 values (section 1.1) | in the envelope, not a tag |
| `topic` tags | Harvest, curated | hierarchical dotted keys, ~40 nodes at launch: `real-estate.{rent,sale,new-build,commercial}`, `events.{concert,theatre,fashion,fair,market,exhibition,conference,sport,kids}`, `commerce.{textile,machinery,apparel}`, `jobs`, `news` … | seeded from the known consumers; labels in uz / ru / en; versioned `taxonomy@N` with an alias map for renames |
| consumer tags | the registering consumer | `c:{consumer}:{key}` + description, keywords per language, 20 positive and negative examples | visible only to that consumer's subscriptions; a curator may promote one into the global layer, merging synonyms |
| keywords | nobody | a saved query, not a stored label | section 4.5 |

- Events keeps its own per-catalog `kind` taxonomy (`fashion.runway`, `trade-fair`); Harvest's `events.*` topics are
  coarser and exist for pool reads. A catalog maps from topics, not the reverse.
- a consumer tag applies only to the public pool, never to another consumer's private container.

### 4.2 How a post gets tags

Ordered, cheapest first; each result is stored as `{tag, score, tier, taxonomyVersion}`.

1. **Source-inherited** (D): the source's declared topics (`@afishauz` → `events`; Domtut's channel → `real-estate.new-build`).
   Score 0.9, the declaration's confidence. This is the only tier a gated Telegram post gets beyond rules.
2. **Lexicon rules** (R): curated keyword lists per tag in uz-Latn, uz-Cyrl, ru, en. Prefix matching for Uzbek suffixes,
   word boundaries for Russian, a negation window, weights per term. Precision-first: a lexicon hit alone yields a tag;
   a miss means "unknown", not "no".
3. **Nearest centroid** (E): each tag has a centroid from its curated examples; assign when cosine ≥ θ(tag) and the
   margin over the runner-up is wide enough; multi-label by threshold; abstain otherwise. A new tag backfills history by
   comparing against stored vectors, with no LLM over old posts.
4. **Zero-shot small LLM** (S): only for abstained posts. Prompt = candidate tags with descriptions (stable prefix,
   cached), post text; output = tags with scores. Expected to see 10–25% of E-eligible posts (U).

- thresholds θ per tag are calibrated on the evaluation set (section 6); until then tags below 0.6 are not published.
- Haven's `dialect_unverified` precedent: a post in Uzbek-Latin phonetic Russian ("Kansaner" for кондиционер; ~15–20% of
  OLX listings by Haven's estimate, Feb 2026) gets `flags: dialect_unverified` and falls to S rather than being
  dropped. Its dictionary (Haven plans one at 50 examples) feeds the lexicons.

### 4.3 Uzbek, Russian, English: normalisation, language, script

- **Normalisation (D, versioned `norm@N`, run before every index):** NFC; lowercase; Uzbek apostrophes unified —
  ASCII `'`, `‘`, `’`, `` ` ``, `´` after `o` / `g` become `ʻ` (U+02BB), elsewhere `ʼ` (U+02BC); `ё` → `е` for Russian;
  zero-width characters removed. The raw `text` is untouched; a `searchText` column holds the normalised form.
- **Script:** count letter scripts per post and per token (`Latn` / `Cyrl` / mixed). Uzbek Cyrillic carries ў қ ғ ҳ,
  which separate it from Russian without a model.
- **Language:** `uz` vs `ru` vs `en` from script, the Uzbek-only letters and digraphs (`oʻ`, `gʻ`), then fastText
  `lid.176` (has `uz` and `ru`; `.ftz` 917 kB, `.bin` 126 MB; model licence CC BY-SA 3.0) through the MIT .NET wrapper
  `Panlingo.LanguageIdentification.FastText` 0.8.1 (net6–net10, 2026-09-06). Lingua (lingua-py, 75 languages) has no
  Uzbek, so it is out. Short Latin text is the weak case (U); keep `conf` and a `und` value.
- **Transliteration:** Uzbek Cyrillic → Latin is deterministic apart from a few contextual letters (е / э, ц, ъ), so
  `searchText` canonicalises Uzbek to Latin; Latin → Cyrillic is lossy (`sh`, `ch`, `yo`) and is never used for storage.
  Russian stays Cyrillic. Port the mapping from the MIT-licensed UzTransliterator (Python, three scripts; the README
  reports no accuracy figure); the 1995 alphabet and its `ʻ` / `ʼ` letters are the target.
- **Stemming:** Snowball has no Uzbek (the algorithm page lists Turkish and Russian, not Uzbek, Kazakh or Kyrgyz).
  Python Uzbek morphology tools exist — UzMorphAnalyser (paper reports >91% word-level accuracy on 5.3K words, licence
  not stated), UzLemmatizer, uznltk, devon (MIT) — none in .NET and none shown to handle both scripts. Not in v1.

### 4.4 PostgreSQL search — what it supports, measured

PostgreSQL 17.4 ships 29 text-search configurations: `russian`, `turkish` and `simple` among them; none for Uzbek,
Kazakh or Kyrgyz. Snowball stemmers are the only built-in stemming; a language not built in needs an Ispell or Hunspell
dictionary in UTF-8, and no Uzbek dictionary file turned up. Results of the local tests:

| Test | Result | Reading |
|---|---|---|
| `russian`: "сдаётся" vs query "сдается" | match | `ё` folded |
| `russian`: "две комнаты" vs "комната" | match | plural stems |
| `russian`: "сдаю квартиру" vs "сдается" | no match | stemmer, not lemmatizer: verb forms with different stems stay apart |
| `simple`, Uzbek Latin: "kvartiralar" vs `kvartira` | no match | no stemming |
| `simple`: "kvartiralar" vs `kvartira:*` | match | prefix queries work for suffixing Uzbek |
| `turkish` on Uzbek Latin | unreliable | document "kvartiralar" → `kvartira`, but query "kvartira & xona" → `kvartir` & `xo`: no match; it also turns final `i` into `ı` |
| tokens of "o'zbek" and "o‘zbek" (ASCII `'`, U+2018) | split into `o` + `zbek` | normalise first |
| tokens of "oʻzbek" (U+02BB) and "oʼzbek" (U+02BC) | one token | the canonical form |
| `unaccent("oʻzbek")` | `o'zbek` | `unaccent` turns U+02BB into ASCII `'`, which then splits: never run it after normalisation |
| phone "+998 90 123-45-67" | tokens `+998`, `90`, `123`, `-45`, `-67` | phones need their own normalised column (D / R), not FTS |
| `similarity('kvartira','квартира')`, `('ijaraga','ижарага')` | 0, 0 | trigrams do not cross scripts: transliterate before indexing |
| `word_similarity('ijrga', 'kvartira ijaraga beriladi')` | 0.33 | under the 0.6 default `word_similarity_threshold`; typo recall needs a tuned threshold |
| database `C` locale: `show_trgm('кичик квартира')` | empty set | no Cyrillic trigrams |
| database `C` locale: `similarity('КВАРТИРА','квартира')` | 0 (1 in `en_US.UTF-8`) | Cyrillic is not case-folded |
| database `C` locale: `to_tsvector('russian','Сдаётся…')` | lexeme `Сдает` keeps its capital | queries in lower case will miss it |

- pick: Harvest's database is created with a UTF-8 locale (or ICU collation), and boots with a self-test —
  `show_trgm('привет')` must be non-empty and `lower` must fold Cyrillic. A `C`-locale database silently breaks Cyrillic
  search (T5, T7, T8 touch database creation).
- search vector per post: `to_tsvector('russian', searchText) || to_tsvector('simple', searchText)` under one GIN index,
  plus a `gin_trgm_ops` index on the title and the first ~300 characters; `pg_trgm` GIN supports `LIKE` / `ILIKE`;
  ordered nearest-neighbour needs GiST.
- `platform-apps.md` defers Meilisearch until an app outgrows Postgres full-text; nothing in this track reaches that.

### 4.5 Keyword subscriptions

- a keyword subscription is a saved query `{terms, mode any|all|phrase, negative terms, languages, scope: channels / tags}`,
  compiled to a `tsquery`. The consumer types one form; Harvest expands it: Latin and Cyrillic spellings for Uzbek
  terms (via the transliteration table), `:*` prefixes for Uzbek, the `russian` configuration for Russian terms.
- matching is per new post at ingest (`post.searchVec @@ sub.tsq`), which scales to hundreds of subscriptions (U) before
  a different structure is needed; T7 owns delivery.
- a keyword reads only what pipelines harvest (T4 §3): Haven's Tashkent real-estate OLX pipeline holds no machines. T4-6
  stands: a keyword may propose a pipeline, never create one.
- semantic subscriptions ("posts like this") read the stored vectors; v1.1, and only over posts E was allowed to see.

### 4.6 Embedding model and storage

| Option | Price per 1M tokens (read 2026-10-26) | Dimensions | Notes |
|---|---|---|---|
| OpenAI `text-embedding-3-small` | $0.02 | 1,536 | pick until the eval says otherwise |
| OpenAI `text-embedding-3-large` | $0.13 | 3,072 | 6.5× the price |
| Voyage `voyage-4-lite` | $0.02; first 200M tokens free | (U) | `voyage-multilingual-2` $0.12 |
| Gemini `gemini-embedding-2` | $0.20; batch $0.10 | 128–3,072 (768 / 1,536 / 3,072 recommended), 8,192 tokens | "over 100 languages", Uzbek not named |
| `BAAI/bge-m3` (self-host) | $0 + a service | 1,024; 8,192 tokens; MIT | "more than 100 working languages", Uzbek not named |
| `multilingual-e5-large` (self-host) | $0 + a service | 1,024; 512 tokens; MIT | "100 languages from xlm-roberta"; the card warns low-resource languages degrade |

- no Uzbek retrieval benchmark turned up for any of them (search 2026-10-26); the choice needs a 300-post Uzbek
  evaluation (T6-8). The embedding model is a configuration value stored beside each vector (`embedModel`), so a switch
  re-embeds at the prices above (about $0.01 per 1,000 posts with the cheap models).
- storage: pgvector `halfvec` columns with HNSW (`vector` indexes up to 2,000 dimensions, `halfvec` up to 4,000); a
  1,024-dimension `halfvec` is ~2 KB a post. Pool reads are filtered (channel, tag, date), and approximate indexes filter
  after the scan, so set `hnsw.iterative_scan` (pgvector ≥ 0.8).
- a self-hosted model does not escape the gates (section 2.2); it only changes where the text goes.

---

## 5. Cost model

### 5.1 Prices read on 2026-10-26

| Model | Input | 5-min cache write | Cache read | Output | Batch (in / out) |
|---|---|---|---|---|---|
| Claude Haiku 5.5 (prompts ≤100K) | $0.10 | $0.125 | $0.01 | $0.50 | $0.05 / $0.25 |
| Claude Sonnet 5.5 | $2 | $2.50 | $0.10 | $10 | $1 / $5 |
| Claude Opus 5.5 | $4 | $5 | $0.20 | $20 | $2 / $10 |
| DeepSeek `deepseek-flash` (off-peak / peak) | $0.15 / $0.30 miss | — | $0.003 / $0.006 | $0.60 / $1.20 | — |

- per million tokens. Haiku 5.5 prompts over 100K tokens cost $0.50 / $2.50; no Harvest prompt is near that.
- cache: minimum 512 tokens on all three Claude models; 5-minute default life, refreshed free on each use; a 1-hour option
  at 2× write price pays after two reads.
- Batch API: 50% off input and output, stacks with caching; results arrive asynchronously.
- thinking is billed as output tokens (`usage.output_tokens_details.thinking_tokens` reports it); effort is the lever,
  set once per route.
- DeepSeek at off-peak costs about the same as Haiku 5.5 per post (~$0.15 per 1,000 vs ~$0.12), so it earns a place as a
  second provider, not as a saving; its data-handling terms are unread (U).
- Haven's test configuration (build output) still names `claude-sonnet-4-6` at $3 / $15 (production config unread, U);
  the 5.5 prices are a third lower.

### 5.2 Unit costs

Token counts are assumptions marked on each row; Haven's rows use its measured per-request tokens (March 2026).
All rows assume cache hits on the stable prefix.

| Route | Tokens (uncached in / cached in / out) | Per post | Per 1,000 posts |
|---|---|---|---|
| E, text-embedding-3-small | 400 / — / — | $0.000008 | $0.008 |
| S, Haiku 5.5 (zero-shot tags, gap-fill) | 400 / 800 / 150 | $0.000123 | $0.12 (batch $0.06) |
| L, Sonnet 5.5, moderate schema (events, offers) | 800 / 900 / 400 | $0.00569 | $5.7 (batch ~$2.9) |
| L, Sonnet 5.5, Haven's 48 fields, cached | 2,000 / 3,060 / 700 | $0.0113 | $11.3 |
| L, Sonnet 5.5, same, prompt uncached | 2,000 + 3,060 / — / 700 | $0.0171 | $17.1 |
| L, Opus 5.5, same, cached | 2,000 / 3,060 / 700 | $0.0226 | $22.6 |
| Haven measured, Sonnet 4.6 (Mar 2026) | 10,000 + 9,500 per 5 listings / — / 3,500 | $0.022 uncached | $13 cached (first run) – $22 |

- Haven's 3,060 cached tokens per listing = a 15.3K-token prompt shared by 5 listings; the 15.3K is the current 47,562
  characters at the March ratio of 3.1 characters per token (29,471 characters ≈ 9,500 tokens). The Claude 5 tokenizers
  may count more tokens than the March one (U); measure with the free token-count endpoint before the numbers are used.
- thinking adds output tokens on every row above; the rows exclude it. Measure `thinking_tokens` per route at effort
  `low` (U).
- Uzbek and Russian text probably costs more tokens per character than English; no measurement (U). Part of the spike.

### 5.3 Levers

- **Cascade (the main one):** D and R take structured and marketplace posts to zero model cost; gates take Telegram and
  unreviewed sources out entirely.
- **Prompt caching:** stable prefix = Harvest preamble + instructions + schema; sort the queue by `promptVersion` so
  consecutive calls share the 5-minute cache. Haven measured a 90% hit rate with 1 s between batches.
- **Batching in the request:** 5–20 posts per call amortises the prefix; per-post validation.
- **Batch API:** whole-site night sweeps, backfills, re-extraction on a version bump, evaluation runs. Not for link
  intake. Halves every row above.
- **Effort:** `low` on extraction routes; keep it constant (a change invalidates the cache).
- **Classify once per canonical post** (T5): cross-posts and language twins cost one call. Haven's backlog defers
  cross-source dedup (`standard-listings-optimization.md`), so the saving there is unmeasured.
- **Not worth it now:** shrinking prompts (quality risk, Haven's own finding), Opus for routine extraction (2× Sonnet).

### 5.4 The AI gateway route

`platform-apps.md` row 15 (AI Gateway, `wow-two-platform.templates.ai`) is an empty .NET skeleton (`Class1.cs` files
only). The be SDK `Ai` folder already holds the `Microsoft.Extensions.AI` seam (`IChatClient`,
`IEmbeddingGenerator`, an OpenTelemetry-and-function-calling pipeline, Ollama and tiktoken); its Anthropic and OpenAI
registrations are listed as pending. Haven's `Haven.Platform.Ai` already routes provider × tier (`Lite` · `Core` · `Pro`;
Anthropic, OpenAI, DeepSeek, Google) with per-tier pricing in configuration; it is the nearest working code for the gateway.

- Harvest needs five things from "the gateway": keys from the vault, routing by tier with a fallback order, provider
  prompt-cache passthrough (`cache_control` kept intact), Batch API submission as a first-class async route, and metering
  tagged by `{consumer, pipeline, tier, promptVersion}` for the cost ledger and caps.
- Harvest keeps the extraction cache, the cascade, batching policy and evaluation; the gateway does not cache responses,
  or Harvest and the gateway would duplicate each other.
- route by tier name (`embed`, `lite`, `core`, `pro`), never by model id; the model map is gateway configuration, so
  Haiku 5.5 → a successor is one edit.
- build the seam first: Harvest takes `IChatClient` / `IEmbeddingGenerator` with provider registrations in-process
  (Form 1); the gateway service (Form 3) is extracted when a second app needs shared keys. This removes the row 15
  dependency from Harvest's "Needs" column (T6-11).
- Form 2 (self-hosted): provider keys per tenant (S3); Form 3: WoW2's keys with a budget per consumer.

### 5.5 Monthly budget at modest scale

Scenario A uses stated figures: Haven 3,000 listings a month (the cost analysis's top projection), T2's modest social
basket (Instagram 10k + Facebook groups 5k + Facebook events 1k), Telegram 10 channels at ~5 a day. Scenario B is a
tenfold Haven and 2.5× social (U). Haven's and Telegram's posts get no Harvest AI.

| Line | A: volume | A: $ | B: volume | B: $ |
|---|---|---|---|---|
| E on social, Ocharo web, Sourcing | 16,500 posts | 0.13 | 42,000 | 0.34 |
| S on 25% of those | 4,125 | 0.5 – 1.0 | 10,500 | 1.3 – 2.6 |
| L, consumer schemas (events-like social posts 5%, Ocharo non-structured pages 60%, Sourcing offers) | 1,220 | 6.9 – 9.7 | 3,600 | 20.5 – 28.7 |
| Re-extraction, one version bump a quarter, Batch API | 3,660 stored items | 3.5 | 10,800 | 10.2 |
| Evaluation, 4 runs of a 600-item set, Batch API | 600 | 6.8 | 600 | 6.8 |
| **Harvest AI total** | | **~18 – 21** | | **~39 – 49** |
| Reference: Haven's own classifier at Sonnet 5.5, cached – uncached | 3,000 listings | 34 – 51 | 30,000 | 339 – 514 |
| Reference: sources, T2 modest basket on Apify | | ~55 | | (U) |

- the high end is ×2 on the S row and ×1.4 on the L row, for thinking tokens and retries.
- proposed caps: global AI $30 hard in A (soft $24), $60 in B; per pipeline $10; Opus 5.5 only for gold-set labelling,
  one-off ~600 items ≈ $7–14 (twice the Sonnet rows).
- the AI line is smaller than the source line in A; the dominant AI cost in the ecosystem is Haven's classifier, which
  stays on Haven's bill.

---

## 6. Quality

### 6.1 Confidence

- every field has `{tier, conf}`: API field 1.0; JSON-LD / microdata 0.95; a rule carries its calibrated precision from
  the evaluation set (e.g. `NUMBER у.е.` 0.98); embedding tags carry the cosine margin; LLM output carries a score that
  is **not** trusted raw.
- item confidence = the minimum over required fields; `wow2.event.v1`'s `confidence` takes it.
- agreement beats self-report: a rule and an LLM that disagree on price, phone or date lower confidence and set
  `tier_disagree:{field}`; a model value for a field the text does not mention is dropped (the source of Haven's
  "hallucinated signals" failure pattern).
- low confidence still delivers, flagged (spec § Extraction). Flags: `low_confidence`, `dialect_unverified`,
  `date_precision_guess`, `tier_disagree:*`, `invalid`, `ai_refused`.

### 6.2 Prompt and rule versions

- `promptVersion` (section 3.1) and `rulesVersion` / `normVersion` / `taxonomyVersion` are stored on every item and tag.
- repository layout: Harvest preamble and rule tables in the repo with test vectors; consumer instructions in the
  schema registry, immutable per version.
- a version bump never silently rewrites history. Re-extraction policies per schema: `lazy` (default; next capture
  change), `eager` (backfill through the Batch API, only after a cost preview — posts × unit price from section 5.2),
  `none`. Haven's `PromptVersion` ("changing it reclassifies every candidate once") is the precedent; Harvest adds the
  preview.

### 6.3 Evaluation sets, one per source family

| Family | Set | Labels from |
|---|---|---|
| Structured pages | 100 pages from afisha.uz, mstar.uz, voyage.uz with the JSON-LD masked | the JSON-LD itself: free ground truth for the text-only path |
| Marketplace listings | 100 OLX / Domtut listings, 30 of them Uzbek-Latin dialect | Haven's 1,416-listing dataset and its `dialect_unverified` queue |
| Telegram posts (rules and lexicons only until P3) | 150: 50 each uz-Latn, uz-Cyrl, ru | human, pre-labelled by Opus 5.5 and corrected |
| Brochure pages | 20 pages from Ocharo's nine reviewed links | human |
| Social captions and Facebook events | 60 + 30 | human; provider data |
| Feeds and ICS | 20 | the feed fields |
| Link cards | 30 URLs | human |

- ~600 items; the Uzbek-literate labeller is the scarce resource (~45 s per item after pre-labelling ≈ 8 h, an
  estimate). Tag evaluation is per tag: precision and recall at θ, per language and script.
- metrics: exact match for amounts, currencies and phone sets; date accuracy including precision; kind F1; per-tag P / R;
  validation-failure and refusal rates; cost per post.
- gate: a rule, lexicon, taxonomy or prompt change merges only if no field's score drops by more than a set margin on
  its family's set (T6-13 sets it); the run uses the Batch API (~$1.7 for 600 items on Sonnet 5.5, moderate schema).
- monitoring: fill rate per field and family per week; a JSON-LD coverage drop or a rise in `unrecognized` (T3) is a
  parser regression alert.
- the review queue is flags on delivered items; Harvest's console lists them, the product decides (Events already
  holds `candidate` review).

---

## 7. What a product receives, and what it must never expect

### 7.1 Receives

- **Captures, always:** immutable, dated, hashed, with media references (T5). Nothing else is conditional on a gate.
- **The base envelope, always:** D and R fields, with `fieldSources` and `flags`.
- **Tags:** source-inherited and lexicon tags always; embedding and LLM tags when G1–G5 allowed, marked by `tiersRun`.
- **Consumer-schema items** for the pipelines it registered, with `extractor` (`mapper` · `llm`), model, `promptVersion`,
  per-field confidence and flags; out-of-scope posts produce none.
- **Source state events** (`live` · `gone` · `relisted`, T4-2) from T5 and T7.
- **Contacts:** raw values to the pipeline's owner; the pool shows a keyed HMAC of the last nine digits only. A plain
  hash would fall to a 10⁹-value brute force. (T4-7; T5 stores it.)

### 7.2 Never expect

- a populated field: every envelope field except identity is nullable; check `fieldSources`.
- an AI value: `ai=off` pipelines and gated sources carry none; `extraction.tiersRun` says what ran.
- the same tags over time: `taxonomyVersion` changes; aliases cover renames.
- translation, summaries, sentiment, entity resolution (venue, organizer, district, landmark), geocoding, currency
  conversion (`у.е.` stays "USD, as published"), dates more precise than the source's, or image understanding.
- contact numbers behind a login, or raw contacts for a pipeline it does not own.
- a stable `extras` shape beyond its family schema version.
- extraction under one model: items record their model; a provider switch leaves old items in place.
- deletion certainty beyond the state machine (T5): `gone` is a hint plus evidence.
- permanence of derived data: items, tags and embeddings die with their capture's retention class (YouTube ≤30 days,
  Meta delete-on-request, X compliance events, T2 S4); an embedding is not anonymous.

---

## Findings that change the spec

1. **Replace "extract into the consumer's schema" with a cascade that always yields a base envelope.** Spec § Extraction
   describes one LLM step per capture. The result is `wow2.post.v1` from D and R on every capture, then E, S, L only
   when allowed. Reason: 97.0% of OLX prices, all of a JSON-LD `Event`, every Telegram timestamp and every ICS field
   need no model (sections 1.3, 2.1).
2. **A consumer schema is a mapping first.** Three of 16 profiled sites carry `Event` nodes; `extras.schemaOrg` preserves
   them, so `wow2.event.v1` for those sources is a declared map with no LLM, and the LLM sees only gaps. Spec §
   Concepts: add `mapping` to a schema's registration (section 3).
3. **Four AI gates exist before the budget, and embeddings are inside them.** `ai_allowed` per source (Telegram `no`,
   Meta-route and X `unreviewed`), the host's `ai-input` signal, the pipeline switch and a data-class provider list;
   Harvest fine-tunes nothing. Telegram posts therefore get lexicon and source tags only until P3 (section 2.2).
4. **PostgreSQL has no Uzbek text-search configuration, and a `C`-locale database breaks Cyrillic.** Measured: no
   `uzbek`; `turkish` gives inconsistent stems; `simple` with prefix queries works; ASCII and U+2018 apostrophes split
   `oʻzbek`; trigrams do not cross scripts; a `C` database yields empty Cyrillic trigrams and uncased lexemes. Spec §
   Storage must require a UTF-8 locale and a boot self-test, and `searchText` normalisation before every index (section 4.4).
5. **The AI line is small; the gateway service is not a prerequisite.** Per 1,000 posts: $0.008 (embedding), $0.12
   (Haiku 5.5), $5.7–11.3 (Sonnet 5.5); about $20–50 a month for Harvest at modest scale. Harvest needs the existing
   `IChatClient` / `IEmbeddingGenerator` seam with tier routing and metering, not the row 15 service; its "Needs" column
   in `platform-apps.md` can read the be SDK `Ai` module instead (sections 5.2–5.5).
6. **Version bumps need a cost preview.** Re-extraction defaults to `lazy`; `eager` runs through the Batch API after a
   preview of posts × unit price (section 6.2).
7. **Derived data inherits retention.** Embeddings, tags and items die with the capture's retention class; the spec's
   "immutable capture" does not extend to derived records on YouTube, Meta or X routes (section 7).
8. Claude structured outputs cannot carry numeric or string-length bounds, so Harvest validates consumer
   schemas after generation; changing effort or the output format invalidates the cache, so both are fixed per route.

---

## Points

Open questions; each ends in a provisional pick.

- [ ] **T6-1** envelope name and strictness → `wow2.post.v1`; every field except identity nullable; `extras` namespaced
  and versioned per family (T5 stores)
- [ ] **T6-2** `kind` set → seven values (`event` · `listing` · `offer` · `news` · `promo` · `discussion` · `other`);
  rent vs sale is a tag, not a kind
- [ ] **T6-3** mapping dialect for the deterministic consumer pass → JSON-pointer paths plus a closed function set;
  no JSONata or scripting
- [ ] **T6-4** AI switch semantics and defaults → `off` · `gaps` · `full`; default `off`; Haven's pipelines `off`;
  Events `gaps` (T7)
- [ ] **T6-5** who pays for pool enrichment → the pipeline that enabled AI; a tag or keyword subscription never
  triggers model calls; a product wanting embedding tags joins or creates a pipeline with AI on (T7)
- [ ] **T6-6** does an embedding count as AI use for the Telegram clause → yes; E, S and L all gated by `ai_allowed`;
  counsel reads API Terms §1.5 and Content Licensing (P3, T1-P1)
- [ ] **T6-7** G2 defaults → table in section 2.2: Telegram `no`; Meta-route, X, YouTube `unreviewed`; open web `yes`;
  waits on P3, S1, W5
- [ ] **T6-8** embedding model → `text-embedding-3-small` in `halfvec`, with `embedModel` per vector; replace after a
  300-post Uzbek evaluation of it against `voyage-4-lite`, `gemini-embedding-2` and self-hosted `bge-m3`
- [ ] **T6-9** taxonomy → Harvest-curated ~40-node global topics, consumer private tags with curator promotion,
  `taxonomy@N` with aliases; the developer approves the seed list
- [ ] **T6-10** Uzbek stemming → none in v1; measure keyword-subscription recall first, then port a stemmer to .NET if
  low
- [ ] **T6-11** AI gateway → build on the be SDK `Ai` seam with tier names and metering; extract the service when a
  second app needs shared keys; drop row 15 from Harvest's "Needs" (T8)
- [ ] **T6-12** per-request consumer context blocks (Haven's lists) → not in v1; Haven keeps its classifier
- [ ] **T6-13** evaluation sets → ~600 items as in section 6.3; an Uzbek-literate labeller is needed; merge-gate margin
  set from the first run; who has the hours is the open part
- [ ] **T6-14** database locale and boot self-test → mandatory UTF-8 locale; test `show_trgm('привет')` at startup
  (T5, T7, T8)
- [ ] **T6-15** contact exposure → keyed HMAC of the last nine digits in the pool, raw to pipeline owners; phones masked
  before any model sees text unless the schema sets `needsContacts` (T5, S12; cross-border transfer under the 2026
  amendment to the personal-data law is unread, U)
- [ ] **T6-16** re-extraction → `lazy` default; `eager` only after a cost preview, through the Batch API (T7)
- [ ] **T6-17** first-slice scope → D and R for all families, the Events mapping, source and lexicon tags; E, S, L land
  after the evaluation set exists

---

## Sources

Pricing and Claude API (read 2026-10-26):

- https://platform.claude.com/docs/en/about-claude/pricing — Haiku 5.5, Sonnet 5.5, Opus 5.5 prices; cache multipliers (0.05× on Sonnet 5.5 and Opus 5.5); Batch API 50%; Haiku 5.5 long-prompt tier
- https://platform.claude.com/docs/en/build-with-claude/prompt-caching — 512-token minimum for the three models; 5-minute default; 1-hour option
- https://platform.claude.com/docs/en/build-with-claude/structured-outputs — `output_config.format`; unsupported constraints; cache invalidation on format change; 24-hour grammar cache
- https://platform.claude.com/docs/en/build-with-claude/thinking-steering-and-cost — effort levels, thinking billed as output, effort change invalidates cache
- Claude API skill reference bundled with the session (cached 2026-10-06) — model ids, effort defaults, refusal stop reason (not re-read at the provider)

Other providers:

- https://developers.openai.com/api/docs/pricing — `text-embedding-3-small` $0.02, `-large` $0.13
- https://docs.voyageai.com/docs/pricing — `voyage-4-lite` $0.02, `voyage-multilingual-2` $0.12, free allowances
- https://ai.google.dev/gemini-api/docs/pricing · https://ai.google.dev/gemini-api/docs/embeddings — `gemini-embedding-2` $0.20 / $0.10 batch; dimensions; 8,192 tokens
- https://api-docs.deepseek.com/quick_start/pricing — `deepseek-flash` prices, off-peak halving

PostgreSQL and search:

- https://www.postgresql.org/docs/current/textsearch-dictionaries.html — simple, synonym, thesaurus, ispell, snowball; Hunspell loading, UTF-8
- https://www.postgresql.org/docs/current/textsearch-psql.html — `\dF` (built-in `russian` configuration)
- https://www.postgresql.org/docs/current/pgtrgm.html — trigram operators, thresholds (0.3 / 0.6 / 0.5), GIN and GiST, `LIKE` support
- https://snowballstem.org/algorithms/ — stemmer list (Russian, Turkish; no Uzbek, Kazakh, Kyrgyz)
- https://github.com/pgvector/pgvector — dimension limits, HNSW, iterative scans (0.8)
- own measurements 2026-10-26: PostgreSQL 17.4 (EDB install), databases `en_US.UTF-8` and `C`, `pg_trgm`, `unaccent`, configurations `russian` / `simple` / `turkish`; cluster deleted afterwards

Uzbek and language tooling:

- https://github.com/elmurod1202/UzTransliterator · https://ceur-ws.org/Vol-3315/paper05.pdf — Cyrillic / Latin / New Latin transliteration, MIT, no accuracy figure on the README
- https://arxiv.org/abs/2405.14179 — UzMorphAnalyser, >91% word-level accuracy on 5.3K words
- https://pypi.org/project/UzLemmatizer · https://pypi.org/project/uznltk/ · https://pypi.org/project/devon — Uzbek stemmers and lemmatizers (Python)
- https://fasttext.cc/docs/en/language-identification.html — `lid.176` (`uz`, `ru`), CC BY-SA 3.0
- https://www.nuget.org/packages/Panlingo.LanguageIdentification.FastText — .NET wrapper 0.8.1, MIT, net6–net10
- https://github.com/pemistahl/lingua-py — 75 languages, no Uzbek
- https://huggingface.co/BAAI/bge-m3 · https://huggingface.co/intfloat/multilingual-e5-large — model cards (languages, dimensions, licence)
- https://blog.cloudflare.com/content-signals-policy/ — `search`, `ai-input`, `ai-train` definitions; absent signal means no preference
- https://kun.uz/en/news/2026/03/27/uzbekistan-amends-personal-data-law-to-facilitate-global-payment-systems · https://www.legal500.com/developments/thought-leadership/legislative-updates-in-the-field-of-artificial-intelligence-and-personal-data-regulation-uzbekistan/ — Law No. 1125 (2026-03-26), localisation narrowed (secondary; T6-15)

Workspace:

- `workbench/maxs-projects/ventures/saas/10x-ven-haven/engineering/research/classification/` — `ai-cost-analysis.md`, `classification-evaluation.md`, `dialect-classification-failure.md`, `olx-listing-data-report.md`, `standard-listings-optimization.md`
- Haven `Haven.Supply.Infrastructure/Classification/` (`ClassificationSettings.cs`, `Prompts/classify-prompt.md`) and `Haven.Platform.Ai/Models/` (`AiModelTier`, `AiProvider`)
- be SDK `src/Ai/Ai.md`; `workbench/wow-two-platform/wow-two-platform.templates.ai/src/` (skeleton)
- [T1](t1-messaging-sources.md) (Telegram terms, extras) · [T2](t2-social-sources.md) (fields, retention) · [T3](t3-web-sources.md) (extraction ladder, traps, W5) · [T4](t4-consumers-and-social.md) (volumes, 48-field split)
- [harvest-service-spec.md](../harvest-service-spec.md) · [events-service-spec.md](../events-service-spec.md) · [analysis index](harvest-analysis-2026-10.md)

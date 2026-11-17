# SCFD console analysis

*Last updated: 2026-11-17*

First full analysis of the SCFD console as built in iteration 1 (harvest `v0.1.14`, `d0aedb5`), read from its 9 pages.
It feeds the mocks in [`mocks/`](mocks/), which are iterated in the orchestrator chat and saved per iteration. Lanes
build only from a saved final iteration. Developer inputs: `events-integration` #56, #58, #62.

## Status

- ✅ Pages read: 9 of 9, light mode, screenshots in [`iter-1-built/`](iter-1-built/)
- ✅ Mocks, iteration 1, final for the operator's Sources area (developer, 2026-11-10: "if you think sources are ready for this iteration - can update the site itself and we'll do aother iteration"): Sources (cards, rows), a source's Overview, Posts (rows, cards, a post opened), Activity and Settings
- ⬜ Decisions #26–#29 and #37–#39 settle on the mocks, one per turn; #23–#25 and #30–#36 are settled
- 🔄 Mocks, iteration 2, the client's view: Sources, a followed source's Posts in both modes; Overview and Following not mocked yet
- ✅ Built from iteration 1 by the scfd lane, 2026-11-10: harvest `v0.1.15` (`0ed89cf`), adapters `v0.1.13` (`1693c79`), tags checked on GitHub; 11 pages in [`built-from-mock-1/`](built-from-mock-1/) (demo build, light); the orchestrator read Sources, a source and a post against the mocks
- ⬜ The developer's review of the built console at `https://localhost:8400/`, once the lane's local harvest fills it

---

## What the developer asked

- "the layout needs a lot of work", "make it similar to wheelhouse ui", "missing account icon at the top, layout lines
  like we have in wheelhouse, navbar height" (#56).
- "I didn't say it must be mapped, I said it must be clean separation, like we did in wheelhouse, but this is a
  separate service" (#56).
- "I want us to add sources ourselves ... instead of typing the source url etc - we allow the subscriber just choose a
  source - later we'll add tags based on the source classification we do with ai models" (#58).
- "let's first finish our first full analysis, then we'll share ot to the implementation lanes"; "we'll generate mocks
  here, iterate on them and save as iteration final" (#62).

---

## Data in the screenshots

- #1 The 1440×900 screenshots come from the console's `demo` build: `AppRoot.vue` switches on
  `import.meta.env.MODE === 'demo'` and `UseDemoConsole` serves in-memory records, with no backend and no adapter.
  No working adapter is disabled.
- #2 The real readers live in the private `harvest-adapters` repo, one package each: `Afisha`, `Uzexpocentre`, `Olx`,
  `Caex`, `Craftfair`, `Anons`, `Instagram`. On `harvestadapters-dev` Afisha's 2 pipelines capture every 6 hours.
  The local stack registers one source, `www.afisha.uz` (adapter `afisha-uz`), with 2 pipelines, Fashion and
  Concerts; the host compiles the other readers, yet none is registered as a source there (scfd lane, 2026-11-10).
- #3 A mock uses the real source names, so a page is judged on the content it will hold. The 6 sources beside Afisha
  in `mocks/iter-1/sources` are compiled readers shown as if registered.

---

## Findings by page

| # | Page | Shows today | Gap |
|---|---|---|---|
| #4 | [Home](iter-1-built/home.png) | 4 counters, latest runs, host lanes | delivery lag has no data; nothing says which source needs attention or what was delivered today |
| #5 | [Sources](iter-1-built/sources.png) | a card per source with adapter name, operations, section chips | leads with adapter internals (`site · filtered · ownFetch`, `capture, discover, refresh, check`); no health, last capture or post count; cards do not scale to 100 sources |
| #6 | [Pipelines](iter-1-built/pipelines.png) | 2 rows: name, host, section, cadence, last-run badge | no next run, no post or subscriber count; duplicates what a source's sections say |
| #7 | [Pipeline](iter-1-built/pipeline.png) | state, source, section, cadence, a configuration form, a schedule form per work kind | the starting URL is typed by hand, against #58; the adapter's scope schema and operations are shown raw; the schedule form asks for mode, time zone and minutes before saying what runs when |
| #8 | [Runs](iter-1-built/runs.png) | a list filtered by pipeline | the error kind and its message run together (`timeout The synthetic listing host ...`); a run links to nothing: not its source, its posts or the pause it caused |
| #9 | [Posts](iter-1-built/posts.png) | a list and an evidence pane | no filter by source, kind or date, no search; `1 source links` |
| #10 | [Subscriptions](iter-1-built/subscriptions.png) | subscriptions and a "Subscribe a tenant" form | the subscriber picks a pipeline and types an exact tag, against #58; the main button is a debugging action, `Pull next events` |
| #11 | [Hosts](iter-1-built/hosts.png) | each host's queue, failures and pause | `fetch lane` is engine language; the pause reason trails unlabelled; it sits under System though it is a source's health |
| #12 | [Access](iter-1-built/access.png) | the session's scopes, tenants, containers | scopes are raw names (`pipelines:read`); tenants are the subscribers and belong with delivery; containers are never explained |

---

## Findings across pages

- #13 The frame is right and incomplete: 5 groups, a 56 px bar, a collapse control, a breadcrumb, a container switch
  and an account menu, yet no glass edges and no version badge, and the account shows initials only. The shared
  `AppFrame` (fe `0.0.45`) brings all three.
- #14 The pages speak the engine's language: `fetch lane`, `ownFetch`, `Available operations`, `Saved scope schema`,
  colon scope names, `tenant`, `container`. An operator needs source, section, schedule, subscriber.
- #15 Two pages contradict #58: a pipeline's typed URL (#7) and a subscription made from a pipeline and a typed tag
  (#10).
- #16 The lists hold too little to act on: no next run, counts, filters or search (#5, #6, #9). At 100 sources the
  card grid of #5 and the flat lists stop working.
- #17 Related things do not link: a failed run, the host pause it caused, the source it belongs to and the posts it
  captured sit on 4 pages with no path between them.
- #18 The grouping follows the engine's tables, not the operator's questions: Pipelines and Hosts are separate pages
  for what is one question, "is this source being read, and is it healthy?".

---

## Proposed structure

Orchestrator's picks. Each settles on the mocks, then becomes the page map the scfd lane builds.

| # | Group | Page | Answers | Replaces |
|---|---|---|---|---|
| #19 | Overview | Home | what needs attention, what was captured and delivered today | Home |
| #20 | Collect | Sources | a gallery of sources by group, as Wheelhouse shows products: the groups first with pills and a trend, then each group's sources as cards or rows (one switch), each with result pills and a 14-day chart at the bottom right; search and filters for 100 sources | Sources, Pipelines, Hosts |
| #20 | Collect | a source page | result pills under the name, then tabs: Overview (sections with schedule, last and next capture, posts, subscribers; health; the chart), Posts (every post with its result and evidence), Activity, Settings | Pipeline, Hosts, Posts |
| #21 | Collect | Activity | every run across sources, with a path to its source and posts | Runs |
| #22 | Deliver | Subscriptions | who receives which source and section; made by choosing subscriber, source, sections | Subscriptions |
| #22 | Deliver | Subscribers | the products that receive posts | Access's tenants |
| #22 | System | Access | the session's permissions in words, containers explained | Access |

- Developer, 2026-11-10: "we def need to remove posts in the menu - it must be part of sourves page instead"; "show
  the sources like a gallery - like wheelhouse does ... group the sources like wheelhouse grouping the products, and
  have grid and list view here as well"; "for each source we can then add their statistics chart in the bottom right
  for quick look and pills for the results". The Content group leaves the menu.
- A section a subscriber follows is a pipeline underneath; the word stays in the engine and leaves the pages.
- A schedule reads as a sentence, `captures every 6 hours, checks daily`, with the form behind an edit action.
- Tags appear on a subscription as a later, disabled choice until AI classification exists (#58).

---

## Open decisions

- #23 Settled 2026-11-10: Collect is sources first, as a grouped gallery, with posts inside a source (#20).
- #24 Deliver: Subscribers and Subscriptions as 2 pages, or one page.
- #25 Hosts: folded into a source's health (#20), or kept as a page.
- #26 Words: `subscriber` for tenant, `section` for a pipeline's scope, and what a container is called.
- #27 Home: which 3 or 4 questions it answers first.
- #28 Who may add a source: operators only, through an adapter release (#58), with the console read-only for the
  catalog.
- #29 Where the console runs: local only today; a deployed target needs a site route beside `/api`.
- #30 Settled 2026-11-10: a group is a publisher whose channels or branches are its sources (developer: "group is
  like afisha has telegram, instagram, website - it's this, or like teplo store has multiple branches in it - we just
  group them under teplo"). The operator names groups; a source's icon says how it is read (site, Telegram,
  Instagram, branch), and no place is shown, since one site carries events from many cities.
- #31 Settled 2026-11-10: a card carries one pill, what the last harvest found (`4 new of 23 found · partial`), the
  last and next harvest under the name, and the 14-day chart of new posts; no section pills and no delivery figures
  (developer: "what the last harvest found - within the last harvest pill should be enough").

- #32 Settled 2026-11-10, client access: client login, not a client page inside the operator's console (developer:
  "we either need to allow client logins or show sources at a client page - because admin seeing all deliveries is not
  needed imo ... I think client login fits this"). #58 has the subscriber choose a source, which needs the subscriber
  signed in; the console's sign-in already maps a person's organization to a tenant (`events-integration` #39); a
  client page would keep the operator choosing for every client and reading every delivery.
- #33 One console, 2 menus (#32). Operator: Home, Sources, Activity, Clients, Access. Client: Sources, Following. The
  operator sees how many clients follow a section, never who received which post; deliveries show only to the client.
  #24 and #25 close with it: Subscriptions leaves the operator's menu, Hosts folds into a source's health.
- #34 Settled 2026-11-10: the Sources page follows Wheelhouse's Products page: group tiles first (name, count,
  description, a pill, a trend), then a collapsible section per group with a rule beside its name; Cards shows a
  3-column grid, Rows a bordered list per group (developer: "gropuing page looks off - look how wheelhouse looks").
- #35 Settled 2026-11-10: a source's Overview lists only the sections being harvested and folds the rest into one
  closed line; it shows no posts, which have their own tab (developer: "need to somehow hide not following channels",
  "latest posts - remove from overview").
- #36 Posts have a Cards and a Rows view (developer). Orchestrator's pick for the switch: the top bar, shown only on
  pages with a gallery (Sources, a source's Posts), one remembered choice for both; the bar stays in view while a long
  gallery scrolls, and the shared `AppFrame` gives every console the same place for it (`bar-end`).
- #37 Settled 2026-11-10: a client gets Sources and Following and no feed page; its posts sit inside each source it
  follows, as an operator's do (developer: "it shouldn't be one feed page, but more like sources -> posts", "a feed
  included inside each source they are following").
- #47 Iteration 2, a client's Posts tab inside a followed source: matched posts by default, and a `Matched | All`
  switch that adds the rest to the same list, dimmed, each saying why it did not match (developer, 2026-11-10: "only
  matched and can switch to all ... maybe in the same panel but with dimmed ?"). One list, no second panel: the
  contrast shows what the filter dropped. Confirmed by the developer ("yes").
- #52 Iteration 2, filters: the search and the `Matched | All` switch stay visible; section, kind and, later, tag
  filters fold behind an expandable Filters panel, on the operator's Posts tab too (developer, 2026-11-10: "for the
  other tags - hide with extendable panel is better I think"; read as the other filters, to be corrected if he
  meant something else).
- #38 Open: the operator's Clients page and a source's Settings and Activity tabs.
- #39 Open: the word for a part of a source the developer called category and channel, here `section`.

- #40 Settled 2026-11-10: a post opens over the page in a modal with no route of its own, since SCFD is not a place to
  read posts; revisions show inside it, never in the list (developer: "revisions - do we really need to show it in the
  posts page ? or maybe inside a post when user clicks it ?").
- #41 Settled 2026-11-10: the Pipelines, Runs, Hosts, Posts and Subscriptions pages go. A source's Settings tab, for
  operators only, holds what Pipelines held (each section on or off, how often it is harvested and checked, the page
  limit, the reading pace, AI on or off); its Activity tab holds the runs; its Health card holds what Hosts showed
  (developer: "pipelines and sources now clash in the name, I think all those configurations must be be part of
  sources then", "runs - this should be part of pipelines as well", "hosts. - not sure why we need this").
- #42 Settled 2026-11-10, the menus: an operator gets Home, Sources, Subscribers and Access; a client gets Sources and
  Following and never Access (developer: "this will be subscribers page on the menu when admin logs in", "access -
  won't be available for client login").
- #43 The pool keeps posts of every kind; a subscriber receives only its matches, so Ocharo sees events only
  (developer, 2026-11-10).
- #44 Settled 2026-11-10 (developer: "with subscriber's smallest we lose events I think, so we setting is the best
  imo"): the operator sets how often a section is harvested. The reasoning: the operator, per source section, from how
  often the source changes and how politely it can be read; never the smallest interval a subscriber asks for, which
  would let one client drive load on a source. A subscriber's own schedule is how it receives: it pulls its matches,
  and a webhook ping to its server can tell it to pull now; SignalR fits a browser page, not a service.
- #46 Settled 2026-11-10: a post's view shows its images, in the opened post and as the first image on a card
  (developer: "images are part of the harvest - so we should def show them"). The engine models them (`PostMedia`,
  `CaptureMedia`, the `Media` step that copies images into file storage). They show inside SCFD only; what a
  subscriber's public page may show stays under `events-integration` #32 and #50.
- #45 Later, not in iteration 1: a choice of outgoing server per source once a second server exists (no proxy pools,
  `events-integration` #50); AI use per source (#54, #55); Home; Subscribers; the client's Following page (#37).

- #48 Built differently from the mocks, the lane's choices nearest Wheelhouse, open to the developer's review:
  `workspace` for the engine's container, with the switch shown only for 2 or more; sources with no group last under
  `Other`; the registry's publisher name as the group name (`Afisha Uzbekistan`); a section an adapter lists in 2
  languages reads `Fashion · Russian`; Subscribers makes a subscription from subscriber, source and section, with no
  typed tag; the account trigger shows initials only, as Wheelhouse's does.
- #49 Not built, with the lane's reasons: `See the capture` (a post link carries a capture id and no route shows a
  capture); the branch icon (no `branch` source family yet); naming a run the first harvest (runs cannot prove it).
- #50 Images on dev: 14 of 14 Afisha posts hold image links; no step stores copies. The post view shows the links,
  loaded with no referrer, inside SCFD only.
- #51 The local console holds real data since 2026-11-10 (scfd lane): Fashion · Russian and Exhibitions · Russian
  turned on through Settings, harvests of 4 new of 17 and 4 new of 26 found, 10 posts, 9 with image links, both
  sections harvesting every 6 hours while the stack runs. Found on the way, held for the developer's review: no
  console, API or host verb grants a restricted source (the lane opened `afisha.uz` by hand on the local database;
  an operator grant is in harvest's backlog); the post modal's Place shows the venue without the city; Home and
  Activity count a harvest that stopped at its page limit as failed or needing attention.

---

## Posts page review, 2026-11-14

The operator's Posts tab at [the Docker review URL](https://localhost:8400/sources/01a1c0cc-c04b-70ab-97f9-94dba2e37e06/posts)
uses the real Afisha workspace. This pass read the live API and exercised the current UI in Docker Chromium with
synthetic posts, including a long date range and a fixed publication age. The date fixes are recorded in the
[Harvest version track](../../../../workbench/wow-two-sdk-beta/wow-two-sdk-beta.harvest/engineering/planning/version-track/v0.2/v0.2.md).

### Layout and interactions

| Area | Observed | Review |
|---|---|---|
| Source header and tabs | The header carries source state, the last and next harvest, and actions. The shared app bar holds the remembered Cards and Rows switch. | Review the shared source header after the card. |
| Search and chips | Search matches titles. Section and kind chips count within the loaded results and the other selected facet. All clears both chips and keeps the search. | Preserve these interactions during card refactoring. |
| Cards | The grid fits tracks of at least 17rem. Images cover a 4:5 tile with a fading scrim. The footer shows category pills, a two-line title and date metadata. | Give the full event range priority in the footer. Let the age use a second line when the pair would clip. Preserve room for both title lines and the image. |
| Rows | Rows show the same posts and ranges. At 390 px, the visible columns are Post and Kind. Section and Posted appear at wider widths. | Keep publication units and event date formatting consistent across both views. |
| Links | Clicking the image opened the SCFD detail route. The separate upper-right link targets the publisher in a new tab. | Use the post title as the primary named link. Keep the publisher link and image controls individually operable. |
| Carousel | Chromium confirmed keyboard activation changes the slide and the indicator. The current tab order is previous, next, original, post title. | Put the post title first in the card's reading and tab order. Verify keyboard focus and touch targets as part of the card review. |
| Missing or removed content | No image uses the source-icon tile. One image has dimmed, disabled arrows. Removed posts have a disabled original link and grayscale images. A valid image URL that fails to load leaves a blank slide. | Review fallback behavior for failed image loads. Include long titles and several pills in the browser fixtures. |

### Dates

- [SourceWords](../../../../workbench/wow-two-sdk-beta/wow-two-sdk-beta.harvest/engineering/codebase/harvest.frontend-services/packages/fe-harvest/src/admin/harvestConsole/SourceWords.ts#L83) currently formats ages in minutes, hours, days and years. Cards, their accessible
  text, and Rows use the same formatter. Afisha's Messika post supplies a publication timestamp of 21 July 2026. At the
  screenshot's 14 November time, Chromium reproduced `115 days` from that timestamp. The queued wording is `3 months`.
- [SourcePostsTab](../../../../workbench/wow-two-sdk-beta/wow-two-sdk-beta.harvest/engineering/codebase/harvest.frontend-services/packages/fe-harvest/src/admin/harvestConsole/SourcePostsTab.vue#L351) gives a fixed-width age priority over a truncating range. At a 320 px
  viewport, Chromium measured 146 px available for a 152 px date label. `5 Mar 2026 – 10 Jun 2027` was clipped even
  though the formatter returned the full range. Preserve both endpoints and give the date its own line when needed.
- The [SDK relative time helper](../../../../workbench/wow-two-sdk-beta/wow-two-sdk-beta.fe/engineering/codebase/wow-two-sdk-beta-fe/src/foundation/i18n/RelativeTimeParts.ts#L35) uses rounded units and includes weeks.
  On the pinned build, 115 days resolves to four months. A compact elapsed format that uses completed units and
  skips weeks can extend the existing SDK helper during extraction. Keep the shared rounding contract for its callers.
- Event ranges preserve source calendar dates. The status helper parses those values separately as instants and
  treats a date-only end as UTC midnight plus one day. Include day-only values and different viewer time zones when
  reviewing ongoing and finished states.

### Data and loading

- Local Afisha returned 37 posts, including one without a section. The tab badge uses the section sum of 36. A future
  source total should count the same post population as the list, including posts without a section.
- The [list API](../../../../workbench/wow-two-sdk-beta/wow-two-sdk-beta.harvest/engineering/codebase/harvest.backend-services/packages/Module/Sources/ModuleSourceOverviewBroker.cs#L73) orders
  by first capture. The frontend asks for 200 rows without a cursor. Search and chip counts cover those loaded rows.
- Each workspace poll returns a fresh source object. The Posts watcher returns a fresh tuple and requests the same
  list again even when the source ID and harvest values are unchanged. Chromium observed a repeat after five seconds.
  Compare stable watch values during the list refactor and verify one reload when a harvest actually changes.
- The post detail fetches the full record and separately fetches the capped source list to find the post's section,
  dates and fallback link. Older direct links can lose that supplemental data after the post leaves the list window.
- The [Docker demo](http://localhost:8410/sources/00000000-0000-4000-8000-000000000200/posts) now includes publication
  timestamps and two synthetic dates for footer review. Demo entries exist in memory.

### Card composition and frontend SDK

| Part | Where it belongs |
|---|---|
| Post card | SCFD owns the layout while it is being refined. Separate the card's presentation and carousel state from fetching, search, chip counts and Rows in `SourcePostsTab`. |
| Whole-card navigation and media | Adopt the SDK [CardLink](../../../../workbench/wow-two-sdk-beta/wow-two-sdk-beta.fe/engineering/codebase/wow-two-sdk-beta-fe/src/presentation/display/card/CardLink.spec.md) where it preserves the stretched hit area and independent controls. The card already uses SDK Carousel and DotsIndicator. |
| Image scrim and action overlay | Candidates for the next SDK extraction after the card settles. Check existing Card and Button APIs before adding variants. Cover focus, touch, contrast and reduced transparency. |
| Category pills | SDK Badge already covers leading icons, tones and truncation. Evaluate a treatment for badges over imagery. SCFD owns kind, section, language and removed-state meanings. |
| Responsive columns | Keep the grid CSS during card review. Consider an auto-fill minimum in the SDK's existing [Grid](../../../../workbench/wow-two-sdk-beta/wow-two-sdk-beta.fe/engineering/codebase/wow-two-sdk-beta-fe/src/presentation/layout/grid/Grid.spec.md) alongside its breakpoint column options. |
| Date and age labels | Evaluate reusable elapsed formatting and calendar range formatting in the SDK. SCFD owns the choice of when to show an event date, publication age and lifecycle status. |

### Footer review at the card minimum

- Each card starts with a one-line footer. At 272 px, `18 Nov 2025 · 1 year` and `31 Dec – 2 Jan 2027 · 3 months`
  each fit in one line. The full `5 Mar 2026 – 10 Jun 2027` range takes its own line and `3 months` moves below it.
- At 288.5 px the full range and age fit together. In a mixed row at 272 px, the card that wraps starts its
  title about 17 px higher. Both cards keep the same bottom inset.

### Afisha card acceptance

- Chrome follows the post title with the carousel arrows and then the publisher link. The title stays at the bottom
  of the card. The image area opens the post and the carousel arrows have their own click targets.
- A failed slide shows Lucide `ImageOff`. The carousel test verifies the other image and slide controls still work.
- Afisha badges use the publisher category. Harvest section remains a separate filter.

### Event topics and formats

[PostPills](../../../../workbench/wow-two-sdk-beta/wow-two-sdk-beta.harvest/engineering/codebase/harvest.frontend-services/packages/fe-harvest/src/admin/harvestConsole/PostPills.vue#L44) and
[SourcePostsTab](../../../../workbench/wow-two-sdk-beta/wow-two-sdk-beta.harvest/engineering/codebase/harvest.frontend-services/packages/fe-harvest/src/admin/harvestConsole/SourcePostsTab.vue#L98) derive the badge and section filter from the
[first capture pipeline](../../../../workbench/wow-two-sdk-beta/wow-two-sdk-beta.harvest/engineering/codebase/harvest.backend-services/packages/Abstractions/Sources/SourcePostModel.cs#L31).
Afisha's Russian Exhibitions pipeline found the 18 November concert, so SCFD shows `exhibitions` on it.
The item itself describes an opera-soloist concert. Afisha also files a comedy performance under Concerts and
publishes a cancellation article there. A publisher's section alone cannot determine the occurrence or its subject.
[Concert](https://www.afisha.uz/ru/concerts/2026/11/11/zhelaem),
[comedy performance](https://www.afisha.uz/ru/concerts/2026/09/25/karen-avanesyan),
[cancellation notice](https://www.afisha.uz/ru/concerts/2026/09/04/cancellation).

Use **subject** for what the event covers and **format** for how it happens. A fashion trade expo can have fashion
and business subjects and an expo format. Keep attendance mode, access, eligibility, schedule, status, language,
location and the harvest section as their own fields. A report, recap or call for applications can describe an
event or milestone using a related record. Eventbrite exposes separate types and categories, Ticketmaster exposes
classifications with identifiers, and Schema.org covers status, scheduling and attendance as properties.
[Eventbrite](https://www.eventbrite.com/help/en-gb/articles/193464/set-up-an-event-with-multiple-dates-without-an-event-schedule/),
[Ticketmaster](https://developer.ticketmaster.com/products-and-docs/apis/discovery-api/v2/),
[Schema.org Event](https://schema.org/Event).

| Subject areas | Example formats |
| --- | --- |
| Music and nightlife | Concert, recital, festival, club night |
| Theatre, dance and comedy | Play, ballet, stand-up, mixed performance |
| Visual arts, design, fashion and craft | Exhibition, opening, runway show, demonstration |
| Film, media and literature | Screening, premiere, reading, book launch |
| Sport, fitness, recreation and gaming | Match, race, tournament, class, esports competition |
| Business, industry and careers | Trade show, job fair, conference, networking meetup |
| Science, technology and education | Talk, workshop, seminar, hackathon, webinar |
| Food, drink and retail | Tasting, cooking class, market, pop-up |
| Civic, political and legal | Public hearing, election, council meeting, protest |
| Community, family and charity | Community gathering, fundraiser, volunteer day, support group |
| Culture, heritage and faith | Festival, guided tour, commemoration, religious service |
| Health and wellbeing | Clinic, appointment, screening, retreat |
| Nature, outdoors and travel | Hike, expedition, conservation day, tour |
| Personal occasions | Wedding, reception, birthday, memorial |

Use extensible identifiers, translated labels and aliases, and optional primary and secondary subjects. Formats can
appear in multiple subject areas. [W3C SKOS](https://www.w3.org/TR/skos-reference/#labels).

1. Use item-level classifications from the selected source's URL and locale. Next use a supported subtype of the
   primary structured event, then an adapter-validated breadcrumb or exact native tag. Use a supported broader
   subject or leave the badge absent when finer evidence is missing.
2. Read from the saved [link reading](../../../../workbench/wow-two-sdk-beta/wow-two-sdk-beta.harvest/engineering/codebase/harvest.backend-services/packages/Module/Posts/ModulePostBroker.cs#L108).
   [AfishaCaptureReader](../../../../workbench/wow-two-sdk-beta/wow-two-sdk-beta.harvest/engineering/codebase/harvest.backend-services/sources/Afisha/AfishaCaptureReader.cs#L69) already retains source evidence.
   Expose additive display fields and resolve the same values for cards, rows, detail and topic counts.
3. Retain pipeline provenance and the existing subscriber semantics.
   [DeliveryTagFilter](../../../../workbench/wow-two-sdk-beta/wow-two-sdk-beta.harvest/engineering/codebase/harvest.backend-services/packages/Abstractions/Delivery/DeliveryTagFilter.cs#L19) matches current tags
   and source tags. Check concerts discovered through Exhibitions, comedy under Concerts, cancellation notices,
   multilingual URLs and older posts without item-level evidence before adopting the display fields.

### Events and listings in the Posts table

SCFD uses the same identity, revision, source link and availability model for events, listings and general posts.
`harvest_posts` uses a container-scoped kind index. It stores the resolved `wow2.post.v1` envelope,
while each source link keeps its own reading and evidence. Ocharo subscribes to the `wow2.event.v1` projection.
Haven subscribes to `wow2.post.v1` filtered to listings. The console can add its own summary fields to the existing
source-post read. [Post storage](../../../../workbench/wow-two-sdk-beta/wow-two-sdk-beta.harvest/engineering/codebase/harvest.backend-services/packages/Module/Migrations/001-baseline/Apply.sql#L529),
[Ocharo subscription](../../../../workbench/wow-two-sdk-beta/wow-two-sdk-beta.harvest/engineering/codebase/harvest.backend-services/sources/Module/Ocharo/OcharoSourceProvisioner.cs#L152),
[Haven subscription](../../../../workbench/wow-two-sdk-beta/wow-two-sdk-beta.harvest/engineering/codebase/harvest.backend-services/sources/Module/Marketplace/MarketplaceProvisioner.cs#L94).

The current [Rows view](../../../../workbench/wow-two-sdk-beta/wow-two-sdk-beta.harvest/engineering/codebase/harvest.frontend-services/packages/fe-harvest/src/admin/harvestConsole/SourcePostsTab.vue#L237) shows Post, Kind, Section and Posted. It adds a date
under the title when there is an event date. The [list response](../../../../workbench/wow-two-sdk-beta/wow-two-sdk-beta.harvest/engineering/codebase/harvest.backend-services/packages/Abstractions/Sources/SourcePostModel.cs)
has event dates and images but omits price and place. The OLX reader already retains native attributes and price
evidence. In the local development databases on 15 November, all 10 OLX listings had a listed amount, currency and
location. The normalized prices had no billing period. Afisha had 36 events and 43 posts with no extracted kind.
35 of those events had a location.
[OLX reader](../../../../workbench/wow-two-sdk-beta/wow-two-sdk-beta.harvest/engineering/codebase/harvest.backend-services/sources/Olx/OlxCaptureReader.cs#L84).

Use **Post**, **Type**, **Details** and **Posted** as the shared columns. Keep the source section available as
harvest context and add a Source column when the table spans multiple sources in the open workspace. Render the
Details field beneath the title at narrow widths. Use the same summary fields on cards and the detail page.

| Type | Details in the table | In the post |
| --- | --- | --- |
| Event | Date or range, venue if present | Full schedule, venue and access or ticket information |
| Rental listing | Stated price and currency, billing period if known, district and rooms as space allows | Price terms, property type, rooms, area and source attributes |
| Article or unknown kind | Publisher topic if available | Source text and supporting links |

Add optional structured summaries by kind to the source-post read using the selected source's reading. Use
published event date precision and the stated currency and billing period. An absent period stays absent, and a
negotiable price stays distinct from a numeric zero or missing price. A rental is a listing with rental terms.
Keep publication age, event dates, listing terms and source availability independent. Two ads for the same address
can represent distinct offers with different terms.

Review an Afisha event, an OLX rental and a general post through Rows, Cards and a direct detail link. Include a
listing with missing terms and a post outside the first page of results. Use the existing storage for this slice.
If operators need date range or price filters across all posts, add typed indexes or a read projection alongside
server-side filters and pagination. The current console caps the list at 200 posts before filtering.
[Current query](../../../../workbench/wow-two-sdk-beta/wow-two-sdk-beta.harvest/engineering/codebase/harvest.backend-services/packages/Module/Sources/ModuleSourceOverviewBroker.cs#L75).

---

## Sources review — 17 November 2026

**Status:** R01–R18 were approved by the developer and implemented locally in the Sources review pass below.
The original observations and recommendations remain here as the dated review record. Final frontend and browser
verification is pending; this status does not assert deployment or release acceptance.

Read-only critique of the source detail page in the developer's screenshot, the Sources index, and their current implementation. Three independent agents reviewed the index, detail operations, and Posts behavior. Chrome observations covered the real local Sources list, Afisha Posts, and Afisha Overview. Error injection, split-permission accounts, mixed-pipeline mutations and narrow-screen interaction were not exercised; findings about those cases come from the code. The running tab reports a local-version mismatch, so current checkout findings are not claims that every change is deployed. No product code or source state was changed by this review.

The post-card visual design and segmented Enabled/Disabled control can remain. The next visual pass should resolve the source header's layout and operational language. Correctness work below should be completed before accepting the whole Sources area. These were review-time proposals; subsequent approval and local implementation are recorded below.

### Source header layout

Keep the existing theme, source logo, website pill, compact times and segmented control.

- First row: source logo and name on the left; the action group on the right. Keep Enabled/Disabled together and at the same height as the buttons. Make the manual harvest action the primary action when available.
- Second row spans the full card: source type and source group on the left; paired last/next activity pills on the right. The present metadata is inside the title column, so the action column reduces its usable width while space beneath the actions stays empty.
- At narrow widths, actions take their own row; metadata and the time pair wrap as coherent units. Avoid giving long names or group names an artificially narrow column.
- After that structural change, reduce unnecessary vertical gaps between header, tabs and filters. Keep the current card density and carousel design.

Evidence at review time: [SourceHeader.vue:108](../../../../workbench/wow-two-sdk-beta/wow-two-sdk-beta.harvest/engineering/codebase/harvest.frontend-services/packages/fe-harvest/src/admin/harvestConsole/SourceHeader.vue#L108). The read-only review recommended the full-width metadata row; the implementation record below supersedes its pending status.

### Behavior and correctness

| # | Priority | Finding | Recommended behavior and evidence |
|---|---|---|---|
| R01 | High | Source summaries and the main harvest action still assume the legacy capture path. An enabled pipeline using discover/harvest stages can appear idle and have Harvest now disabled. | Derive health, harvested sections, last activity and manual execution from the configured path. The header already reads stage schedules for the next-run pill; finish the remaining summary/action paths rather than replacing that work. [SourceOverviewRules.cs:58](../../../../workbench/wow-two-sdk-beta/wow-two-sdk-beta.harvest/engineering/codebase/harvest.backend-services/packages/Module/Sources/SourceOverviewRules.cs#L58), [ModuleSourceOverviewBroker.cs:300](../../../../workbench/wow-two-sdk-beta/wow-two-sdk-beta.harvest/engineering/codebase/harvest.backend-services/packages/Module/Sources/ModuleSourceOverviewBroker.cs#L300), [SourceHeader.vue:56](../../../../workbench/wow-two-sdk-beta/wow-two-sdk-beta.harvest/engineering/codebase/harvest.frontend-services/packages/fe-harvest/src/admin/harvestConsole/SourceHeader.vue#L56), [HarvestConsole.ts:765](../../../../workbench/wow-two-sdk-beta/wow-two-sdk-beta.harvest/engineering/codebase/harvest.frontend-services/packages/fe-harvest/src/admin/harvestConsole/HarvestConsole.ts#L765). |
| R02 | High | The source-wide toggle overwrites individual section pauses. Sequential updates can partially succeed, then fail without refreshing the UI. | Treat the source control as a master pause that preserves section choices, or explicitly define and expose its all-sections behavior. Always reconcile actual state after a partial failure. A mixed set of enabled and paused sections must not silently become all enabled after a disable/enable cycle. [HarvestConsole.ts:776](../../../../workbench/wow-two-sdk-beta/wow-two-sdk-beta.harvest/engineering/codebase/harvest.frontend-services/packages/fe-harvest/src/admin/harvestConsole/HarvestConsole.ts#L776), [HarvestConsole.ts:564](../../../../workbench/wow-two-sdk-beta/wow-two-sdk-beta.harvest/engineering/codebase/harvest.frontend-services/packages/fe-harvest/src/admin/harvestConsole/HarvestConsole.ts#L564), [SourceHeader.vue:54](../../../../workbench/wow-two-sdk-beta/wow-two-sdk-beta.harvest/engineering/codebase/harvest.frontend-services/packages/fe-harvest/src/admin/harvestConsole/SourceHeader.vue#L54). |
| R03 | High | Failed reads can look like legitimate empty states. Overview failure becomes Source not found; failed run reads become No harvests yet; capability failure can remain Reading sections indefinitely; source-list failure can cause No source matches. | Separate loading, empty, unavailable and stale data. Retain successful snapshots, retry failed capabilities and provide scoped Retry controls. [SourcePanel.vue:87](../../../../workbench/wow-two-sdk-beta/wow-two-sdk-beta.harvest/engineering/codebase/harvest.frontend-services/packages/fe-harvest/src/admin/harvestConsole/SourcePanel.vue#L87), [HarvestConsole.ts:329](../../../../workbench/wow-two-sdk-beta/wow-two-sdk-beta.harvest/engineering/codebase/harvest.frontend-services/packages/fe-harvest/src/admin/harvestConsole/HarvestConsole.ts#L329), [HarvestConsole.ts:359](../../../../workbench/wow-two-sdk-beta/wow-two-sdk-beta.harvest/engineering/codebase/harvest.frontend-services/packages/fe-harvest/src/admin/harvestConsole/HarvestConsole.ts#L359), [SourcesGallery.vue:50](../../../../workbench/wow-two-sdk-beta/wow-two-sdk-beta.harvest/engineering/codebase/harvest.frontend-services/packages/fe-harvest/src/admin/harvestConsole/SourcesGallery.vue#L50). |
| R04 | High | Settings uses one pipeline-management permission gate, although name, group and reading pace require source-management permission. | Gate sections and actions by their own permission and allow operators to reach whichever settings they can manage. [SourcePanel.vue:34](../../../../workbench/wow-two-sdk-beta/wow-two-sdk-beta.harvest/engineering/codebase/harvest.frontend-services/packages/fe-harvest/src/admin/harvestConsole/SourcePanel.vue#L34), [SourceSettingsTab.vue:248](../../../../workbench/wow-two-sdk-beta/wow-two-sdk-beta.harvest/engineering/codebase/harvest.frontend-services/packages/fe-harvest/src/admin/harvestConsole/SourceSettingsTab.vue#L248), [SourcesController.cs:44](../../../../workbench/wow-two-sdk-beta/wow-two-sdk-beta.harvest/engineering/codebase/harvest.backend-services/packages/Hosting/Registration/Controllers/SourcesController.cs#L44), [RunsController.cs:106](../../../../workbench/wow-two-sdk-beta/wow-two-sdk-beta.harvest/engineering/codebase/harvest.backend-services/packages/Hosting/Runs/Controllers/RunsController.cs#L106). |
| R05 | Medium | Opening a post or source and returning loses search/filter context; group collapse state also lives only in the listing component. | Preserve query, filters, loaded position and scroll per source/list. Use route state for shareable choices and remembered view state for position. [UseSourcePostPages.ts:8](../../../../workbench/wow-two-sdk-beta/wow-two-sdk-beta.harvest/engineering/codebase/harvest.frontend-services/packages/fe-harvest/src/admin/harvestConsole/UseSourcePostPages.ts#L8), [SourcesGallery.vue:51](../../../../workbench/wow-two-sdk-beta/wow-two-sdk-beta.harvest/engineering/codebase/harvest.frontend-services/packages/fe-harvest/src/admin/harvestConsole/SourcesGallery.vue#L51). |
| R06 | Medium | Search replaces the entire grid with Loading posts before the debounce expires. Loading more sets a flag that suppresses every later refresh. | Keep existing results while updating. Preserve list position after loading more, but offer New or updated posts available or an explicit refresh action. Announce the completed result count. [UseSourcePostPages.ts:45](../../../../workbench/wow-two-sdk-beta/wow-two-sdk-beta.harvest/engineering/codebase/harvest.frontend-services/packages/fe-harvest/src/admin/harvestConsole/UseSourcePostPages.ts#L45), [UseSourcePostPages.ts:65](../../../../workbench/wow-two-sdk-beta/wow-two-sdk-beta.harvest/engineering/codebase/harvest.frontend-services/packages/fe-harvest/src/admin/harvestConsole/UseSourcePostPages.ts#L65), [UseSourcePostPages.ts:102](../../../../workbench/wow-two-sdk-beta/wow-two-sdk-beta.harvest/engineering/codebase/harvest.frontend-services/packages/fe-harvest/src/admin/harvestConsole/UseSourcePostPages.ts#L102), [SourcePostsTab.vue:222](../../../../workbench/wow-two-sdk-beta/wow-two-sdk-beta.harvest/engineering/codebase/harvest.frontend-services/packages/fe-harvest/src/admin/harvestConsole/SourcePostsTab.vue#L222). |
| R07 | Medium | Rows omit the removed state shown on cards. | Keep source availability consistent across Cards, Rows and details; changing view must not hide that a post was removed. [SourcePostsTab.vue:259](../../../../workbench/wow-two-sdk-beta/wow-two-sdk-beta.harvest/engineering/codebase/harvest.frontend-services/packages/fe-harvest/src/admin/harvestConsole/SourcePostsTab.vue#L259), [SourcePostsTab.vue:298](../../../../workbench/wow-two-sdk-beta/wow-two-sdk-beta.harvest/engineering/codebase/harvest.frontend-services/packages/fe-harvest/src/admin/harvestConsole/SourcePostsTab.vue#L298). |
| R08 | Medium | Activity displays a count derived from the latest 50 runs per pipeline as though it were complete history. Entries do not lead to the existing run audit. | Mark the view/count as recent until pagination is supported; link each run to its audit and its pipeline. [RunsController.cs:37](../../../../workbench/wow-two-sdk-beta/wow-two-sdk-beta.harvest/engineering/codebase/harvest.backend-services/packages/Hosting/Runs/Controllers/RunsController.cs#L37), [SourcePanel.vue:38](../../../../workbench/wow-two-sdk-beta/wow-two-sdk-beta.harvest/engineering/codebase/harvest.frontend-services/packages/fe-harvest/src/admin/harvestConsole/SourcePanel.vue#L38), [SourceActivityTab.vue:78](../../../../workbench/wow-two-sdk-beta/wow-two-sdk-beta.harvest/engineering/codebase/harvest.frontend-services/packages/fe-harvest/src/admin/harvestConsole/SourceActivityTab.vue#L78). |

### Visual clarity and consistency

| # | Priority | Finding | Recommended behavior and evidence |
|---|---|---|---|
| R09 | First visual pass | Metadata is constrained by the action column. | Apply the two-row header layout described above. [SourceHeader.vue:108](../../../../workbench/wow-two-sdk-beta/wow-two-sdk-beta.harvest/engineering/codebase/harvest.frontend-services/packages/fe-harvest/src/admin/harvestConsole/SourceHeader.vue#L108). |
| R10 | First visual pass | Active, Enabled, Harvesting, idle and Paused refer to different layers without explaining the differences. The Sources filter Harvesting also includes healthy sources. | Separate configured enablement, current work and host health. Keep Enabled/Disabled as the control. Use Idle only for enabled work waiting to run; explain disabled/manual/no-schedule states accurately. Rename Active only to reflect its registration/access filter or change its behavior to match the source control. The live Overview shows Disabled in the header and Paused: no under Health; label that field Host pause. Give unavailable Harvest now a nearby or focus-accessible reason. [SourcesGallery.vue:20](../../../../workbench/wow-two-sdk-beta/wow-two-sdk-beta.harvest/engineering/codebase/harvest.frontend-services/packages/fe-harvest/src/admin/harvestConsole/SourcesGallery.vue#L20), [SourcesGallery.vue:57](../../../../workbench/wow-two-sdk-beta/wow-two-sdk-beta.harvest/engineering/codebase/harvest.frontend-services/packages/fe-harvest/src/admin/harvestConsole/SourcesGallery.vue#L57), [SourceOverviewTab.vue:245](../../../../workbench/wow-two-sdk-beta/wow-two-sdk-beta.harvest/engineering/codebase/harvest.frontend-services/packages/fe-harvest/src/admin/harvestConsole/SourceOverviewTab.vue#L245), [SourceHeader.vue:184](../../../../workbench/wow-two-sdk-beta/wow-two-sdk-beta.harvest/engineering/codebase/harvest.frontend-services/packages/fe-harvest/src/admin/harvestConsole/SourceHeader.vue#L184). |
| R11 | Medium | Source cards and rows use a favicon but omit visible source type; the group symbol differs between the sidebar and header. | Retain the publisher logo and add compact Website/Telegram/Instagram metadata where sources are listed. Use one group glyph throughout. A source group is a container's set of sources, typically a publisher's channels or branches; it does not own schedules or merge posts. A small grouped-channel motif fits that meaning better than a folder. Explore its SVG separately as previously requested. [SourceCard.vue:24](../../../../workbench/wow-two-sdk-beta/wow-two-sdk-beta.harvest/engineering/codebase/harvest.frontend-services/packages/fe-harvest/src/admin/harvestConsole/SourceCard.vue#L24), [SourceRow.vue:20](../../../../workbench/wow-two-sdk-beta/wow-two-sdk-beta.harvest/engineering/codebase/harvest.frontend-services/packages/fe-harvest/src/admin/harvestConsole/SourceRow.vue#L20), [SourceGroupModel.cs:3](../../../../workbench/wow-two-sdk-beta/wow-two-sdk-beta.harvest/engineering/codebase/harvest.backend-services/packages/Abstractions/Sources/SourceGroupModel.cs#L3). |
| R12 | Medium | Advanced filters show only a number, hiding which constraints are active. Category and content-kind controls visually run together. | Keep the circular quick filters. Show selected advanced constraints as removable pills and a visible matched count; visually distinguish categories from content kinds with spacing or a subtle separator. Keep server-side facets and the existing timing filter. [SourcePostsTab.vue:74](../../../../workbench/wow-two-sdk-beta/wow-two-sdk-beta.harvest/engineering/codebase/harvest.frontend-services/packages/fe-harvest/src/admin/harvestConsole/SourcePostsTab.vue#L74), [SourcePostsTab.vue:194](../../../../workbench/wow-two-sdk-beta/wow-two-sdk-beta.harvest/engineering/codebase/harvest.frontend-services/packages/fe-harvest/src/admin/harvestConsole/SourcePostsTab.vue#L194). |
| R13 | Medium | The source-list last-harvest pill is verbose and differs from the compact detail header. | Use the same age units everywhere. Keep the most useful result visible, such as 0 new; move found counts and full timing into a custom tooltip or the activity details. A partial/failed result should lead to its audit rather than leave the operator guessing. [LastHarvestPill.vue:19](../../../../workbench/wow-two-sdk-beta/wow-two-sdk-beta.harvest/engineering/codebase/harvest.frontend-services/packages/fe-harvest/src/admin/harvestConsole/LastHarvestPill.vue#L19), [SourceWords.ts:293](../../../../workbench/wow-two-sdk-beta/wow-two-sdk-beta.harvest/engineering/codebase/harvest.frontend-services/packages/fe-harvest/src/admin/harvestConsole/SourceWords.ts#L293). |
| R14 | Medium | Browser title tooltips remain on source icons, last harvest, group tiles, truncated Activity text, the original-post link and language pills. | Complete the shared themed Tooltip migration, including keyboard access. Keep essential error explanations visible. Existing filter-pill tooltips already use the custom component and should remain. [SourceIcon.vue:58](../../../../workbench/wow-two-sdk-beta/wow-two-sdk-beta.harvest/engineering/codebase/harvest.frontend-services/packages/fe-harvest/src/admin/harvestConsole/SourceIcon.vue#L58), [LastHarvestPill.vue:27](../../../../workbench/wow-two-sdk-beta/wow-two-sdk-beta.harvest/engineering/codebase/harvest.frontend-services/packages/fe-harvest/src/admin/harvestConsole/LastHarvestPill.vue#L27), [SourceGroupTile.vue:32](../../../../workbench/wow-two-sdk-beta/wow-two-sdk-beta.harvest/engineering/codebase/harvest.frontend-services/packages/fe-harvest/src/admin/harvestConsole/SourceGroupTile.vue#L32), [SourceActivityTab.vue:92](../../../../workbench/wow-two-sdk-beta/wow-two-sdk-beta.harvest/engineering/codebase/harvest.frontend-services/packages/fe-harvest/src/admin/harvestConsole/SourceActivityTab.vue#L92), [SourcePostsTab.vue:407](../../../../workbench/wow-two-sdk-beta/wow-two-sdk-beta.harvest/engineering/codebase/harvest.frontend-services/packages/fe-harvest/src/admin/harvestConsole/SourcePostsTab.vue#L407), [PostPills.vue:65](../../../../workbench/wow-two-sdk-beta/wow-two-sdk-beta.harvest/engineering/codebase/harvest.frontend-services/packages/fe-harvest/src/admin/harvestConsole/PostPills.vue#L65). |
| R15 | Optional polish | Uniformly Russian results repeat ru on every card; past/ongoing event labels are only explicit to screen readers. | Suppress redundant language pills when the source/result context already states the single language, keeping language in detail. Clarify ambiguous event timing with a compact visible label or custom tooltip. Keep publication age distinct from the event date. [SourcePostsTab.vue:103](../../../../workbench/wow-two-sdk-beta/wow-two-sdk-beta.harvest/engineering/codebase/harvest.frontend-services/packages/fe-harvest/src/admin/harvestConsole/SourcePostsTab.vue#L103), [SourcePostsTab.vue:324](../../../../workbench/wow-two-sdk-beta/wow-two-sdk-beta.harvest/engineering/codebase/harvest.frontend-services/packages/fe-harvest/src/admin/harvestConsole/SourcePostsTab.vue#L324), [PostPills.vue:65](../../../../workbench/wow-two-sdk-beta/wow-two-sdk-beta.harvest/engineering/codebase/harvest.frontend-services/packages/fe-harvest/src/admin/harvestConsole/PostPills.vue#L65). |

### Groups, responsive behavior and accessibility

| # | Priority | Finding | Recommended behavior and evidence |
|---|---|---|---|
| R16 | Medium | Group tiles show full counts/trends while filtered sections show only matching sources. Collapse buttons remain visible while filtering forces sections open. | Show matching/total counts when narrowed. Keep group-wide trends explicitly scoped. Honor collapse or remove the nonfunctional control during filtering. [SourcesGallery.vue:94](../../../../workbench/wow-two-sdk-beta/wow-two-sdk-beta.harvest/engineering/codebase/harvest.frontend-services/packages/fe-harvest/src/admin/harvestConsole/SourcesGallery.vue#L94), [SourcesGallery.vue:172](../../../../workbench/wow-two-sdk-beta/wow-two-sdk-beta.harvest/engineering/codebase/harvest.frontend-services/packages/fe-harvest/src/admin/harvestConsole/SourcesGallery.vue#L172), [SourcesGallery.vue:189](../../../../workbench/wow-two-sdk-beta/wow-two-sdk-beta.harvest/engineering/codebase/harvest.frontend-services/packages/fe-harvest/src/admin/harvestConsole/SourcesGallery.vue#L189). |
| R17 | Medium | Narrow source rows hide the entire last-harvest summary; Settings retains a 44rem table and fixed label columns. | Preserve essential status/time in a wrapping secondary row. Stack Settings fields at narrow widths, following the existing Overview/Activity approach. Verify long names, groups, no data, failure, mixed enablement and both themes before acceptance. This is code-based responsive review, not a completed mobile test. [SourceRow.vue:17](../../../../workbench/wow-two-sdk-beta/wow-two-sdk-beta.harvest/engineering/codebase/harvest.frontend-services/packages/fe-harvest/src/admin/harvestConsole/SourceRow.vue#L17), [SourceSettingsTab.vue:164](../../../../workbench/wow-two-sdk-beta/wow-two-sdk-beta.harvest/engineering/codebase/harvest.frontend-services/packages/fe-harvest/src/admin/harvestConsole/SourceSettingsTab.vue#L164), [SourceSettingsTab.vue:251](../../../../workbench/wow-two-sdk-beta/wow-two-sdk-beta.harvest/engineering/codebase/harvest.frontend-services/packages/fe-harvest/src/admin/harvestConsole/SourceSettingsTab.vue#L251). |
| R18 | Low | Group navigation scrolls without moving keyboard focus, always smooth-scrolls, and the single-group section references an absent heading. | Focus the destination heading, respect reduced motion, and give bare single-group sections a valid accessible name. [SourcesGallery.vue:115](../../../../workbench/wow-two-sdk-beta/wow-two-sdk-beta.harvest/engineering/codebase/harvest.frontend-services/packages/fe-harvest/src/admin/harvestConsole/SourcesGallery.vue#L115), [SourceGroupSection.vue:28](../../../../workbench/wow-two-sdk-beta/wow-two-sdk-beta.harvest/engineering/codebase/harvest.frontend-services/packages/fe-harvest/src/admin/harvestConsole/SourceGroupSection.vue#L28). |

### Preserve and sequence

Already present in the current code: segmented source control, website metadata pill, compact header times, title-first post links, centered per-slide ImageOff fallback, usable remaining slides, circular filter targets, touch labels, themed quick-filter tooltips, server-side post search/facets and cursor paging. The one-language toolbar filter is hidden. These are retained decisions, not new work.

Suggested order: R09–R10 for the next visible pass; R01–R04 before operational acceptance; R05–R08 and R12 for browsing; then R11 and R13–R18 for consistency and edge cases. Some stage-related implementation overlaps the listings integration lane, so coordinate that ownership before edits. Image compaction remains a separate Files/SCFD backlog concern and does not require another post-card design.

### Implementation record — 17 November 2026

The developer approved all 18 findings. The following changes are implemented in the local Harvest checkout,
preserving the accepted post-card design and segmented Enabled/Disabled control.

| Item | Implemented scope |
|---|---|
| R01 | Source summaries include legacy Capture and staged Discover, Harvest and Process work. They expose the last work kind, earliest eligible next schedule and configured manual action. Manual stage actions remain available when their automation is off. |
| R02 | The source control writes one persisted master pause through `PUT /api/sources/{id}` with `paused`. It preserves every pipeline's own pause and schedule choices. Scheduler/manual-run gates share the pause transaction lock; paused sources also block new queued-work claims. |
| R03 | Sources, source detail, capabilities and Activity distinguish initial loading, unavailable reads and stale snapshots, with scoped Retry actions. Successful data remains visible during refresh failures. |
| R04 | Source naming, grouping, reading pace and master pause use source-management permission; section actions use their pipeline permission. Settings is accessible for the scopes the caller actually holds. |
| R05 | Source-list and per-source browsing restore search, filters, expanded/collapsed groups, loaded posts and scroll within the console session. Stored views are isolated by client/connection and container. |
| R06 | Search keeps the existing results while updating. Continued browsing can detect changed posts and offer refresh without discarding the current position automatically; completed result counts are announced. |
| R07 | Removed posts remain identifiable in Rows as well as Cards and post detail. |
| R08 | Activity is explicitly recent, with links to run audits and pipelines. Its count describes the loaded recent runs. |
| R09 | Header metadata spans a full second row, with source type/group and paired compact activity times. At narrow widths, actions occupy their own row. |
| R10 | Copy separates Disabled, Idle, Running, Manual, availability/access restrictions and host pause. Unavailable manual actions have an explanation. Enabling cannot reset unavailable or retired source states. |
| R11 | Source cards and rows show their Website/Telegram/Instagram channel metadata alongside the publisher icon. Source-group surfaces share the existing Group glyph. |
| R12 | Selected advanced constraints appear as removable pills with a matched count. Category and content-kind controls have distinct spacing; server-side facets remain the authority. |
| R13 | Last-harvest summaries use compact ages, keep useful new-post counts visible and put detailed timing/found counts in a custom tooltip. Problem results link to their audit. |
| R14 | The reviewed Sources surfaces use the shared themed Tooltip for icons, metadata, truncated Activity text, original-post actions and language labels, with keyboard access. Existing quick-filter tooltips remain. |
| R15 | A uniform result language is stated in the result context instead of repeated on every card; post detail retains language. Event timing is explicit while publication age remains separate. |
| R16 | Filtered groups show matching/total counts, group-wide trends retain their scope, and collapse controls work while filtering. |
| R17 | Narrow source rows retain status and activity metadata. Settings fields and section rows adapt to narrow containers. |
| R18 | Explicit group navigation unfolds and focuses the destination heading, respects reduced motion and runs once. Single-group sections have a valid accessible heading. |

Scope limits:

- R05 restores session-local browsing; shareable search/filter URL queries are not implemented.
- R08 still reads the latest 50 runs per pipeline. Full history pagination is not implemented.
- R11 uses a provisional existing Group glyph. A source group is a container's set of sources, commonly a
  publisher's channels or branches; it does not own schedules or merge posts. The custom grouped-channel SVG
  remains a separate design task.
- R02 reuses the existing source-state column. Already executing requests may finish; the pause blocks new
  work. Ocharo/Marketplace setup preserves the stored pause and individual pipeline choices.
  Older servers that omit `sourceState` from the overview cannot receive master-pause writes: the control is
  disabled with an explanation. Registry refresh recovery does not manufacture this support indicator.
- This pass adds no migration and performs no release. Image compaction remains in the separate Files/SCFD backlog.

Live runtime boundary, checked read-only on 17 November: `https://localhost:8400` still uses backend container
`scfd-internal-local-harvest-1`, image `harvest:scfd-afisha-ru`, reporting
`0.0.0-dev+afisha-ru-local`. Docker health is `healthy`, but the running Abstractions assembly does not contain
the new `SourceHarvestSelection` type. The backend has no application-code or assembly mounts, so the new master
source control is **not deployed or accepted on 8400**. The console's `/` route proxies to `http://$scfd_live`, and
the source-mounted `scfd-console-live-vite` container is running; frontend outputs may be ahead of the backend.
No image rebuild or service recreation was
performed: the shared dirty tree also contains the listings lane and stage dependencies, so a whole-tree image
build would include more than this Sources review. A frontend-only preview is not evidence that the live source
pause is persisted by the old API.

The metadata-only migration check reads `public.harvest_migration_history`; its newest recorded name is
`source-assets` (the checkout's `007-source-assets` set), preceded by `source-groups` and `subscription-filter`.
The running database is therefore not at the required `009-step-operations` release check. Any later backend
update must account for the pending stage/audit schema rather than treating this as a frontend-only refresh.

Backend verification completed in an isolated working-tree snapshot using Docker and .NET SDK `10.0.403`:

| Suite | Passed | Failed | Skipped |
|---|---:|---:|---:|
| `Harvest.Tests.Unit` | 211 | 0 | 0 |
| `Harvest.Tests.Conformance` | 207 | 0 | 0 |
| `Harvest.Tests.Integration` | 70 | 0 | 0 |
| `Harvest.Tests.E2E` | 60 | 0 | 0 |
| **Affected backend suites** | **548** | **0** | **0** |

These checks cover module/client/fake contract parity, persisted pause/resume, preservation of mixed pipeline
choices, scheduler and manual-run refusal, queued-work claims, source-availability protection, stage summaries,
and the API's field/null-omission shape. The existing Discover batch-size theory was aligned with its documented
contract: discovery ignores that field; Harvest and Process retain their bounds. The test snapshot includes the
deployment descriptor needed by the existing host-filtering E2E check. `git diff --check` passes. This is the four
affected backend suites, not a new run of all eight suites recorded in the earlier S03–S05 work.

Implementation pointers: [source pause](../../../../workbench/wow-two-sdk-beta/wow-two-sdk-beta.harvest/engineering/codebase/harvest.backend-services/packages/Module/Registration/ModuleRegistrationBroker.cs),
[stage selection](../../../../workbench/wow-two-sdk-beta/wow-two-sdk-beta.harvest/engineering/codebase/harvest.backend-services/packages/Abstractions/Sources/SourceHarvestSelection.cs),
[source-control integration tests](../../../../workbench/wow-two-sdk-beta/wow-two-sdk-beta.harvest/engineering/codebase/harvest.backend-services/tests/Harvest.Tests.Integration/Engine/SourceControlTests.cs).
Final frontend verification: **139 passed** (`fe-harvest` 102, web app 37), with the original test timeouts and
concurrency. Package build, workspace typecheck, compilation of all 17 app Vue SFCs, workspace ESLint and
Prettier checks pass. The packed consumer check verified **86 files and 3 exports**. The architecture test now
loads ESLint configuration before timing its rule assertions; no timeout was increased. Two pipeline-stage
components received formatter-only cleanup. The final suite includes stale-overview reconciliation and both
session/UI regressions that prevent master-pause writes to an older server.

Browser evidence is narrower: the earlier desktop demo check observed source search, matching group counts,
collapse during filtering, the full-width metadata row and synthetic master-pause behavior. The final browser
session repeatedly timed out, so the final responsive/theme pass and current real-data visual acceptance are
not complete. This must not be treated as acceptance of the old backend on port 8400. The local demo review
build is served at `http://127.0.0.1:8468/sources`; it uses synthetic data and no real source mutations.

---

## Publication and next checks

*17 November 2026 — changes pushed and backend v0.2.7 published; target acceptance remains open.*

The [Harvest v0.2 track](../../../../workbench/wow-two-sdk-beta/wow-two-sdk-beta.harvest/engineering/planning/version-track/v0.2/v0.2.md)
is the canonical change list and release record. Backend release CI passed all 863 tests; the final console re-pin
passed 139 frontend tests. The shared tooltip SDK is published as `0.0.49`. Harvest's own package publication was
skipped, and its image contains only the backend; console hosting remains S33. No deployment or migration was
verified in this publication pass. Preserve unrelated listings and toast work in their owning lanes.

1. Finish S07 target checks: the released backend, migrations 008/009, Afisha's Russian
   schedules with old Uzbek pipelines still paused, and Events' two Afisha subscription checks.
   Upgrade local port 8400 separately before accepting the source Enabled/Disabled control there.
2. Finish the responsive/theme and real-data Sources review against the updated backend, including source
   pause/resume persistence and preservation of individual section schedules.
3. Run E00 to locate the stage at which new Ocharo events stopped arriving: harvest, match, delivery or intake.
   Keep the possible healthy-zero-new-matches result distinct from a failed integration.
4. Follow E01, S08 and S09 before S18: complete the five-subscription intake, golden filter contract and
   multi-section subscription, then verify the additional live event sources. S09 must use the next free migration
   ordinal; 009 is already reserved for the run audit.
5. Continue event correctness and the end-to-end consumer checks from the
   [task order](../tasks/tasks.md). Image compaction and the custom source-group SVG remain separate backlog/design
   work; the post-card visual iteration needs no further expansion to perform these integration checks.

Current checkout check, 17 November: the Events repo is clean at `4446026`, and its deployment descriptor still
defines only Afisha Fashion and Exhibitions. Craftfair, ANONS and Uzexpocentre have no configured intake entries.
Ocharo's existing Events integration is recorded in its v0.3 track at checkout `6badf4f`; this is a repair and
acceptance pass, not a new integration. The older report of three sourced events with no arrivals after 13 November
was observed on 16 November and has not been re-checked live in this publication pass.

Cross-repository publication: Files backlog commit `2e8f248` is pushed. Its documentation delivery run
`44024924066` passed without publishing a new image. Conformance run `44024958750` failed during restore on
`Microsoft.AspNetCore.SignalR.StackExchangeRedis` 10.0.3 (`NU1903`, `GHSA-wr8v-9x5q-ggcm`); the same failure is
present in the preceding run `43863078391`. The tooltip fix is pushed as FE SDK commit `b73b0b91`, released as
`0.0.49` at `6168acdf`, and re-pinned in Harvest at `3fb024a`. FE SDK release CI passed 4,921 tests with 216
skipped. Commit/release links and the backend image digest are recorded in the Harvest version track.

---

## Mocks

- [`mocks/iter-1/`](mocks/iter-1/) holds iteration 1: `sources` (cards), `sources-rows`, `source-afisha` (Overview),
  `source-afisha-posts` (rows), `source-afisha-posts-cards`, `source-afisha-post` (a post opened),
  `source-afisha-activity`, `source-afisha-settings` and `client-sources` (a preview of iteration 2), each an `.html`
  with its `.png`. `build.py` writes the pages from one
  frame; `render-html.sh` renders each at 1440 px.
- [`mocks/iter-2/`](mocks/iter-2/) starts iteration 2 from a copy of iteration 1 and adds a client's view:
  `client-sources`, `client-source-posts` (matched), `client-source-posts-all` (all, the rest dimmed) and
  `client-source-posts-filters` (the Filters panel open).
- An iteration is final when the developer says so; the next one copies it into `mocks/iter-N/` before changing it.

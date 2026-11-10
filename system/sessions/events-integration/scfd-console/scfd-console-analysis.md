# SCFD console analysis

*Last updated: 2026-11-10 11:10 PM*

First full analysis of the SCFD console as built in iteration 1 (harvest `v0.1.14`, `d0aedb5`), read from its 9 pages.
It feeds the mocks in [`mocks/`](mocks/), which are iterated in the orchestrator chat and saved per iteration. Lanes
build only from a saved final iteration. Developer inputs: `events-integration` #56, #58, #62.

## Status

- ✅ Pages read: 9 of 9, light mode, screenshots in [`iter-1-built/`](iter-1-built/)
- 🔄 Mocks: iteration 1 covers the operator's Sources (cards, rows), a source's Overview and Posts (rows, cards), and a client's Sources
- ⬜ Decisions #26–#29 and #37–#39 settle on the mocks, one per turn; #23–#25 and #30–#36 are settled
- ⬜ Hand-over to the scfd lane after the final iteration is saved

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
- #37 Open: a client's pages beyond Sources and Following, such as a feed of delivered posts.
- #38 Open: the operator's Clients page and a source's Settings and Activity tabs.
- #39 Open: the word for a part of a source the developer called category and channel, here `section`.

---

## Mocks

- [`mocks/iter-1/`](mocks/iter-1/) holds iteration 1: `sources` (cards), `sources-rows`, `source-afisha` (Overview),
  `source-afisha-posts` (rows), `source-afisha-posts-cards` and `client-sources`, each an `.html` with its `.png`. `build.py` writes the pages from one
  frame; `render-html.sh` renders each at 1440 px.
- An iteration is final when the developer says so; the next one copies it into `mocks/iter-N/` before changing it.

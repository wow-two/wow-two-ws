# SCFD console analysis

*Last updated: 2026-11-10 09:10 PM*

First full analysis of the SCFD console as built in iteration 1 (harvest `v0.1.14`, `d0aedb5`), read from its 9 pages.
It feeds the mocks in [`mocks/`](mocks/), which are iterated in the orchestrator chat and saved per iteration. Lanes
build only from a saved final iteration. Developer inputs: `events-integration` #56, #58, #62.

## Status

- ✅ Pages read: 9 of 9, light mode, screenshots in [`iter-1-built/`](iter-1-built/)
- 🔄 Mocks: iteration 1 covers Sources, a source page and Subscriptions
- ⬜ Decisions #23–#29 settle on the mocks, one per turn
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
- #3 A mock uses the real source names, so a page is judged on the content it will hold.

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
| #20 | Collect | Sources | which sources exist, which are followed, which are unhealthy; search and filters for 100 rows | Sources, Pipelines, Hosts |
| #20 | Collect | a source page | its sections, each followed or not, with schedule, last and next capture, posts, subscribers; the source's pacing and pauses | Pipeline, Hosts |
| #21 | Collect | Activity | every run across sources, with a path to its source and posts | Runs |
| #22 | Content | Posts | what was captured, filtered by source, section, kind and date, with evidence | Posts |
| #22 | Deliver | Subscriptions | who receives which source and section; made by choosing subscriber, source, sections | Subscriptions |
| #22 | Deliver | Subscribers | the products that receive posts | Access's tenants |
| #22 | System | Access | the session's permissions in words, containers explained | Access |

- A section a subscriber follows is a pipeline underneath; the word stays in the engine and leaves the pages.
- A schedule reads as a sentence, `captures every 6 hours, checks daily`, with the form behind an edit action.
- Tags appear on a subscription as a later, disabled choice until AI classification exists (#58).

---

## Open decisions

- #23 Collect: sources first with no Pipelines page (#20), or Pipelines kept beside Sources.
- #24 Deliver: Subscribers and Subscriptions as 2 pages, or one page.
- #25 Hosts: folded into a source's health (#20), or kept as a page.
- #26 Words: `subscriber` for tenant, `section` for a pipeline's scope, and what a container is called.
- #27 Home: which 3 or 4 questions it answers first.
- #28 Who may add a source: operators only, through an adapter release (#58), with the console read-only for the
  catalog.
- #29 Where the console runs: local only today; a deployed target needs a site route beside `/api`.

---

## Mocks

- [`mocks/iter-1/`](mocks/iter-1/) holds iteration 1: `sources`, `source-afisha` and `subscriptions`, each an `.html`
  with its `.png`, rendered by `render-html.sh` at 1440 px.
- An iteration is final when the developer says so; the next one copies it into `mocks/iter-N/` before changing it.

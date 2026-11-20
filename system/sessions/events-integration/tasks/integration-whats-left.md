# SCFD → WoW2 Events → Ocharo Events: what's left

*2026-11-20, read-only. Specs: wow-two-ws `system/sessions/events-integration/tasks/` (S01-S39, E00-E33,
O01-O17, F01-F11, A01-A08, V01-V07, I01, B01, W01, OE01-OE12), track #60-#72, `subscription-modes.md` § 4.
Evidence: each repo's `backlog.md` `## Specced next`, its active version track and `git log` at:
harvest `d2959ec` (`v0.2.40`), events `b3472f9` (`v0.1.24`, NuGet `be-v10.0.17-beta`, npm `fe-v0.0.9`),
ocharo-platform `fe0accb` (`v0.3.25`), identity `05bccc6`, fe `9e8748a8` (`fe-v0.0.51`), be `86f7f67`,
ai `24330fe` (`be-v10.0.5-beta`), ocharo-marketing `1d565d1`. No edits, commits or deploys.*

## Summary

| Status | Ids |
|---|---|
| Shipped | 60 |
| In flight | 0 ids; the work in flight is the selector (SL1-SL9) and the Afisha/ANONS source-health fixes |
| Open | 56 |
| Superseded or obsolete | 15: 11 by the in-flight selector, 3 by OE07 (E22, E24, E27), 1 by the AI layer (A05) |
| Total | 131 |

- Group (a), must finish for Ocharo's integration, ranked: E17, E23 (+ E24's stale half), E18, E29, then the three
  dev read-backs OE03 / OE05 / OE06 owe.
- Stale backlog rows: 22 (14 superseded but listed, 8 shipped but listed; 1 of the 8 is probable).
- Open ids with no backlog row anywhere: OE09, OE10, OE11, W01, and E24's stale-state half.

## In flight (not task ids)

| Work | State | Evidence |
|---|---|---|
| Subscription selector (SL1-SL9) | built: harvest v0.2 Iteration 21 (`38181c8`..`cefb5c8`, `v0.2.36`-`v0.2.40`); Events SL8a binds one intake source to `selector:{name}` (`d74b1b6`, `v0.1.24`, NuGet `10.0.17-beta`), SL8b replays the golden selector pages (`b3472f9`, unreleased). Left: ≥ 3 daily shadow rows (day 0 on 2026-11-20: 7 both, 10 filter-only, 2 selector-only, 0 pending), the developer's switch (point 13), `adopt`, Events `Sources:0` re-pointed on dev, channel subscriptions archived, `ocharo-fashion-v1` and `ocharo-relevance-v1` retired | `subscription-modes/selector-shadow.md`; harvest `development/subscription-selectors.md` § Provisioning and switching |
| Afisha and ANONS source health | planner, ANONS pacing and console labels (#72); Afisha has read no new post since S37; nothing committed yet (harvest tree clean) | track #72 |

- Check at the switch: the 3 off-topic events already published (Tsereteli, Yalt-Yult, CAEx Build & Co) leave only if
  `adopt` emits `post.unmatched` for them under the selector; E04's hold then takes them out of the feed.

---

## 1. Every task id

Groups for open ids: (a) Ocharo integration · (b) SCFD-only · (c) Ocharo refinements · (d) the developer ·
(e) outside this integration (Ocharo services, Events P2, SDK cleanup).

### SCFD (`tasks-scfd.md`)

| Id | Task | Status | Evidence | Why / group |
|---|---|---|---|---|
| S01 | StoreBootTests, ListingReplay | shipped | harvest row deleted `76eec2d`; `v0.2.7`; track #67 | |
| S02 | fe-harvest lint and Prettier | shipped | `76eec2d`; `v0.2.7`; #67 | |
| S03 | rental-terms prompt out of the engine | shipped | `76eec2d`; leftovers `925d93a` | |
| S04 | one schedule path per section | shipped | `76eec2d`; v0.2 Iteration 6 | |
| S05 | stage validation, discoveries, run audit tests | shipped | `76eec2d`; #67 | |
| S06 | record Codex's work in the docs | shipped | `76eec2d`; #67 | |
| S07 | commit in slices, verify `v0.2.7` on dev | open | harvest row: commits accepted, dev acceptance runs as v0.2 Verification; 4 Haven checks open (OLX, BirBir, `rental-terms@2`, Teplo Fest) | (b), rides the v0.2 close |
| S08 | filter key in golden pages | shipped | `6fde53b`; Iteration 4 | |
| S09 | one subscription, many sections | superseded | harvest Iteration 21 | the selector follows sources and tags in one container; Instagram's cross-pipeline need is met by `sources.include` |
| S10 | `ocharo-fashion-v1` regression set | superseded | Iteration 20 `relevance --filter` (`8f0ea10`), selector `diff` (`bc2b192`) | the rule retires at the switch; its fixtures become tagging eval cases (b) |
| S11 | publisher categories as source tags | superseded | Iteration 10 (`51ae0da`) | Layer 1 tags every post with type, domain and topic, which the selector reads; a publisher-category mapping is optional now |
| S12 | per-subscription pull lag | open | harvest row | (b) |
| S13 | typed application deadlines | shipped | `89fe25d`; Iteration 4 | |
| S14 | shared AI layer in the source host | shipped | Iterations 10-19 (`51ae0da`..`1c65b34`); AI on for harvest-dev (#71) | row still says partial |
| S15 | Ocharo relevance in shadow | superseded | rebuilt on `post-tags` in `174d3cd` | the shadow that gates the switch is now the selector diff (`selector-shadow.md`) |
| S16 | promote AI relevance into delivery | superseded | `subscription-modes.md` § 4; Iteration 20 | the selector switch replaces `ocharo-relevance-v1` |
| S17 | estimated dates from the AI pass | shipped | `174d3cd` (`v0.2.22`); Events reads `starts.certainty` (E34 `3597efc`); Ocharo `e01da3c` | row still says Events must read certainty |
| S18 | ANONS, Craftfair, Uzexpocentre, CAEx | open | ANONS, Uzexpocentre, CAEx on dev on schedule (Iteration 4, `b748364`); Craftfair row waits on the challenge posture | (d), Craftfair only |
| S19 | trade-fair edition pages | open | harvest row | (b) |
| S20 | one size per Afisha picture | open | harvest row | (b); Events copies no sourced media |
| S21 | registry channels to generic readers | open | harvest row | (b), registries |
| S22 | Hunarmand association calls | open | harvest row | (b), registries |
| S23 | gov.uz regional tourism news | open | harvest row | (b), registries |
| S24 | Telegram channels via `t.me/s` | open | harvest row | (b), registries |
| S25 | Instagram paging, one source per publisher | shipped | Iteration 7 (`a81e309`, `8798687`, `27cef55`); row deleted `5e15364` | dev target acceptance sits in the Sources row "Instagram Phase 1 target acceptance" |
| S26 | iTicket and ShowGo listings | open | harvest row | (b), registries |
| S27 | page-limit harvests not failures | open | harvest row | (b); may overlap the in-flight console labels, check before dispatch |
| S28 | section topics from adapters | open | harvest row | (b); § 4 changed it to a taxonomy node per section |
| S29 | event place on cards and post page | open | harvest row | (b), console |
| S30 | event timing, event-date sort | open | harvest row | (b), console |
| S31 | Ocharo client view, Sources and Following | open | harvest row | (b); § 4 makes Following the selector editor |
| S32 | operator grants a restricted source | open | harvest row | (b) |
| S33 | console on harvest-dev | shipped | `3746c26`; Iteration 20; Verification "Open harvest-dev's `/`" checked | row still listed |
| S34 | drop IP-lease pools and CAPTCHA solving | open | harvest row | (d) |
| S35 | publish the Harvest NuGet and npm family | open | harvest row | (b); Events reads the wire with its own reader |
| S36 | stage settings, one permission | shipped | `77ee974`, `af6a2ee` | |
| S37 | Afisha crawl inside section and page limit | shipped | `ccee7fd`; Verification "≤ 5 pages" checked | |
| S38 | what marketplace collectors keep about people | open | harvest row | (d) |
| S39 | v0.2.7 review's small findings | shipped | `e28e184`, `d538e2c`, `bb25457` | |

### Events path (`tasks-events-path.md`)

| Id | Task | Status | Evidence | Why / group |
|---|---|---|---|---|
| E00 | why no event reached dev after 11-13 | shipped | events `64fdf5e` (record only) | |
| E01 | pull all five Ocharo subscriptions | superseded | Events SL8a `d74b1b6` | one intake source on `ocharo-events` |
| E02 | tighten `ocharo-fashion-v1` | superseded | shadow day 0 holds the 5 filter false positives | the selector replaces the rule |
| E03 | deliver `post.unmatched` | shipped | harvest `5bbdabc` | |
| E04 | hold events whose post stopped matching | shipped | events `aa86028` (`v0.1.13`) | |
| E05 | cancelled, postponed, online | shipped | platform `13d535f` (`v0.3.13`) | |
| E06 | no aggregator page as website | shipped | events `2bba84e` | |
| E07 | deadlines in `wow2.event.v1` | shipped | harvest `89fe25d` | |
| E08 | deadlines and time zones into facts | shipped | events `703f093` | |
| E09 | ticket prices and links | shipped | platform `565ce12` | |
| E10 | start time, address, organizer link | shipped | platform `755b5c7` | |
| E11 | foreign cities out of the default country | shipped | events `065c648` | |
| E12 | kind from the subscription | shipped | events `e73a199`; SL8a takes the kind from payload `context` | |
| E13 | stage changes survive revisions | shipped | platform `bb86d1f` | |
| E14 | dead fact-edit and delete actions removed | shipped | platform `318b3bb` | |
| E15 | source name, state, posted time | shipped | events `979cfca` | |
| E16 | source attribution on cards | shipped | platform `eec660d` | |
| E17 | cross-source duplicates to one event | open | events row | (a) |
| E18 | tracking moves to the survivor on merge | open | events row | (a) |
| E19 | subscriber lists its tenant's subscriptions | open | harvest row; `SubscriptionsController.List` still refuses a client-credentials `events-read` token | (b); not needed for one Ocharo subscription |
| E20 | discover intake subscriptions | superseded | § 4 "mostly superseded" | one subscription per catalog |
| E21 | country lists, untracked counts | shipped | events `6463aea` (`v0.1.21`) | |
| E22 | filter and page in Events | superseded | platform `1a7fdf5` (OE07) deleted the row | OE07's mirror runs filters and the cursor in Events |
| E23 | members read intake freshness | open | events row | (a) |
| E24 | error, empty, stale states with retry | superseded | `1a7fdf5` deleted the row ("absorbs E24's error panel") | the kit's failure notice covers errors; the stale-state half still needs E23 and has no row |
| E25 | UI-locale titles | shipped | platform `4cca614` | |
| E26 | in-memory Events fake | open | events row | (e); Ocharo moved to a pass-through recorder |
| E27 | pin Ocharo's mapper | obsolete | `1a7fdf5` deleted `EventsServiceMapper` and the row | no mapper left to pin |
| E28 | replay SCFD's new golden pages | shipped | events `703f093` ("E08 (covers E28)") | |
| E29 | local SCFD → Events → Ocharo smoke | open | platform row | (a); its E01 dependency now reads the selector |
| E30 | harvest tests on the workspace SDK | shipped | harvest `559c7e2` | |
| E31 | triage view for untracked events | open | platform row | (c), needs the developer |
| E32 | per-source thumbnail policy | superseded | events row | Superseded (developer, 2026-11-20): SCFD copies every image to Files and any subscriber reads it with a read-only key; see #75 |
| E33 | city names in the app's script | shipped | events `a848026` | |
| E34 | (extra id) SCFD date certainty | shipped | events `3597efc`; Ocharo `e01da3c` | not counted |

### Platform (`tasks-platform.md`)

| Id | Task | Status | Evidence | Why / group |
|---|---|---|---|---|
| O01 | Sourcing service out of Desk | open | platform row | (e) |
| O02 | Desk's Sourcing slice leaves | open | platform row | (e) |
| O03 | Image service relay | open | platform row | (e) |
| O04 | Editorial calls the Image service | open | marketing row | (e) |
| O05 | Brand takes brands and cards | open | platform row | (e) |
| O06 | Catalogue release gate | open | platform row | (e) |
| O07 | per-image rights approval | open | platform row | (e) |
| O08 | who saved and published | open | platform row | (e) |
| O09 | Studio's creative imports | open | platform row | (e) |
| O10 | one public catalogue feed | open | marketing row | (e) |
| O11 | post drafts to Marketing | open | marketing row | (e) |
| O12 | remove Desk | open | platform row | (e) |
| O13 | prod promotion audit | open | platform row; `events_prod` holds no tables | (d); read-only, can run without a decision |
| O14 | `events-prod` target | open | events row | (d) |
| O15 | prod Identity keys for Events | open | platform row | (d) |
| O16 | promote Events app to prod | open | platform row | (d) |
| O17 | Telegram delivery on Ocharo's schedule | shipped | platform `e46c4a0`, `bae0006`, `d6f9aa8`; dev read `b3a6615` | |
| F01 | toast docs into backlog and track | shipped | fe `9e8748a8` (features.md dropped); Iteration 25 | |
| F02 | toast string enums, SFC action | shipped | fe `0.0.50` (`c2462e60`) | |
| F03 | ToastHost composables and tests | shipped | fe `0.0.50` | |
| F04 | release the toast overhaul | shipped | fe `0.0.50` | |
| F05 | Grid auto-fill | shipped | fe `0.0.50` | |
| F06 | MediaCard | shipped | fe `0.0.51` (`12216987`) | |
| F07 | Button unavailable state | shipped | fe `0.0.51` | |
| F08 | Badge glass tones | shipped | fe `0.0.51` | |
| F09 | Carousel glass arrows, swipe | shipped | fe `0.0.51` | |
| F10 | MetaInlineText | shipped | fe `0.0.51` | |
| F11 | Escape keeps a tooltip closed | shipped | fe Iteration 27, in `0.0.50` | |
| A01 | repeatable queued evals | shipped | ai `cc972d0` (v0.2 Iteration 1) | |
| A02 | first eval on `afisha-10` | shipped | ai `11826eb` (v0.3 "First live eval", 2026-11-18: Haiku and Sonnet 90 %, $0.036) | draft labels still unconfirmed by the developer |
| A03 | first HTTP slice | shipped | ai `cc972d0` (v0.2 Iterations 3-4) | |
| A04 | publish AI packages and image | open | NuGet `be-v10.0.0`..`5-beta` and images `v0.2.0`..`v0.3.3` exist; no `fe-v*` tag, so npm `@wow-two-beta/fe-ai` is unpublished; v0.2 Iteration 5 unticked | (b), npm half only |
| A05 | SCFD relevance shadow on Afisha | superseded | harvest composes published AI (Iterations 10-19) | the relevance shadow became the selector shadow |
| A06 | budget caps, weekly shadow comparison | open | ai row | (b); the shadow-comparison half is now the selector diff, budget caps remain |
| A07 | Events takes SCFD's AI classification | superseded | § 4; SL8a `d74b1b6` | Events stays on `filter`, and the selector is the filter |
| A08 | core be sdk drops LLM folders | open | be row; `src/Ai/` still holds 7 provider folders | (e) |
| V01 | review console on AppFrame | open | events row | (e) |
| V02 | places and organizers as entities | open | events row | (c) |
| V03 | cross-source match proposals | open | events row | (e); E17 and OE09 cover Ocharo's case |
| V04 | custom field schemas per workflow | open | events row | (c); OE07 keeps participation and cost in `fields` until it lands |
| V05 | webhooks | open | events row | (e) |
| V06 | `VTIMEZONE` in `events.ics` | open | events row; `CalendarWriter.cs:12` still writes none | (e); the kit's one-event file has it since OE07 PG17 |
| V07 | scheduled digests with a delivery seam | shipped | events `d64bdac`, `4d3b322`, `5ff82e9`, `5623324` | |
| I01 | Identity sends notices to Telegram | shipped | identity `709f82b`, released `v0.5.22` (`37e06b2`) | |
| B01 | SignalR Redis past NU1903 | shipped | be `c49ab23` (`10.0.112-beta`); Events `32bfffa` | |
| W01 | console review's convention edits | open | no row; the live-edits hand-off doc still holds a personal email | (d) for the two `must`s' scope; the email and verdict fixes need no decision |

### Ocharo events (`tasks-ocharo-events.md`)

| Id | Task | Status | Evidence | Why / group |
|---|---|---|---|---|
| OE01 | hold events SCFD's AI marks irrelevant | superseded | #72 "folded into the selector" | the selector holds no-subject posts at the source (shadow day 0) |
| OE02 | pull the three provisioned subscriptions | superseded | `selector-shadow.md` setup: `--group afisha --group anons --group caex --group uzexpocentre --selector` | the three sources join `ocharo-events` by group |
| OE03 | a member's proposal in the feed at once | shipped | events `db92f53` (`v0.1.19`); Ocharo `bb29f37` | not yet read on dev |
| OE04 | digest by tracking stage | shipped | events `3aca62b` | |
| OE05 | skipped out of feed and digest; reminders | shipped | Ocharo `d8b42ab`, `01ea8ae`, `8e58c45`; dev read 2026-11-20 | reminder preset not yet created on dev |
| OE06 | SCFD's English title to Events and Ocharo | shipped | harvest `dd66b28` (`v0.2.30`); events `c78546f` (`v0.1.20`); Ocharo through OE07's kit | the spec's dev check (`en` UI reads the English title) is not recorded |
| OE07 | read Events through fe-events | shipped | Ocharo `1a7fdf5`; events `a70e9df`, `509ab76`; dev read 2026-11-20 | |
| OE08 | keep the scope picked for a new event | shipped | Ocharo `6b19d87` | |
| OE09 | bind sourced events to SCFD's entity | open | no row | (c); held on entity model #7 and #8 (still proposed) |
| OE10 | expected next edition from cadence | open | no row | (c); held on OE09 and #8 |
| OE11 | assign a teammate | open | no row | (c); low value with one dev member |
| OE12 | close out past events | shipped | Ocharo `a3d0129`; dev read 2026-11-20 | |

---

## 2. Open tasks, grouped

### (a) Must finish for Ocharo's integration — ranked

| Rank | Task | Repo | Why now |
|---|---|---|---|
| 1 | E17 cross-source duplicates to one event, matching curated events too (OE review amendment) | events | the selector switch brings ANONS, CAEx and Uzexpocentre into one subscription, so Visa Fashion Week, The Fashion Show Line and Uzbekistan Fashion Week each arrive twice; OE09's entity id outranks the title rule later |
| 2 | E23 members read intake freshness, plus E24's stale-state half (no row since `1a7fdf5`) | events, then ocharo-platform | Afisha has read no new post since S37, and Ocharo's team cannot tell a quiet week from a stalled pull |
| 3 | E18 tracking moves to the survivor when SCFD merges posts | events | a tracked duplicate stays listed twice after a merge |
| 4 | E29 local SCFD → Events → Ocharo smoke, re-based on `selector:ocharo-events` | ocharo-platform | no test drives one record through all three services; run it after the switch |
| 5 | Dev read-backs the shipped OE tasks owe: OE03 (add an event as an editor on dev), OE05 (create the reminder preset), OE06 (`en` UI shows the English title) | ocharo-platform, events | each "Done when" names a dev check that is not recorded |

### (b) SCFD-only, for a later SCFD orchestrator

- Close v0.2: S07 (its dev acceptance is the v0.2 Verification; 4 Haven checks open).
- Sources and the ~700 registries: S19, S20, S21, S22, S23, S24, S26; Instagram Phase 1 dev acceptance (Sources row).
- Console: S27, S28, S29, S30, S31 (now the selector editor), S32; adopt the fe `0.0.51` lifts (Console row).
- Delivery and release: S12, S35, E19 (list read only; Ocharo needs it no longer).
- AI: A06 budget caps; A04's npm `@wow-two-beta/fe-ai`; AI evals and stats console pages (Engine row, developer
  2026-11-19); `post-tags` and extraction measured on labelled samples (Iterations 10-11, labels from the developer);
  entity change feed retention; native structured output; split AI processing per entity type.

### (c) Ocharo refinements the developer named next

- Event entity and post entity:
  - OE09 bind sourced events to SCFD's event entity — held on entity model #7 (identity) and #8 (two feeds).
  - OE10 expected next edition and past editions by year — after OE09.
  - Gap, no spec yet: show an event's posts from every source by year in Ocharo; SCFD serves them under
    `posts:read`, which Events' client lacks.
- How events are displayed:
  - E31 triage view, minimal slice "new since your last visit" — needs the developer.
  - V04 custom field schemas, so participation and cost leave `fields`.
  - V02 places and organizers as entities (place and organizer filters, dedup).
  - OE11 assign a teammate — low value while dev has one member.
- Search and filtering: no open spec beyond the shipped E21, PG02 and PG18 (country lists, stage lists, two-letter
  country search); a search spec (entity, year, organizer, place) is missing.

### (d) Parked on the developer

- Prod: O13 (read-only audit, runnable now), O14, O15, O16.
- S34 IP-lease pools and CAPTCHA solving; S38 what marketplace collectors keep about people.
- W01 scope of the two `must`s; its email and verdict fixes are mechanical.
- Craftfair: the challenge-detector posture, then S18's Craftfair half.
- Not task ids: the selector switch (point 13), prompt-mode subscriptions (point 7), entity model #7 and #8, A02's
  labels, and members joining Ocharo on dev (the team sees nothing until then).

### (e) Outside this integration

- Ocharo services: O01-O12 (Desk split, Catalogue, Marketing).
- Events P2: V01, V03, V05, V06, E26.
- be sdk: A08.

---

## 3. Stale backlog rows

Shipped but still listed (8):

| Repo | Row | Evidence |
|---|---|---|
| harvest | `S33 Serve the console on harvest-dev` | `3746c26`, Iteration 20 |
| harvest | `S14 Embed the shared AI layer in the source host` ("partial … Ocharo's relevance use case and deployed configuration remain") | Iterations 10-19, AI on for harvest-dev |
| harvest | `S17 Estimate event dates from the AI pass` ("Events' reader still marks every date Announced") | Events `3597efc` reads `starts.certainty` |
| harvest | `Classification writer` (§ Events integration: "no step writes it yet") | Iteration 15: the tag revision sets `PostClassification` |
| events | `Reminders on deadlines` (§ Tracking) — probable | OE04 stage selection + OE05's "Deadline reminders" preset |
| ocharo-platform | `Events on WoW2 Events` ("Done 2026-11-10") | v0.3 Iterations 1-5 |
| ocharo-platform | `Events app` ("Done 2026-11-10") | v0.3 Iteration 8 |
| ai | `A02 First eval on afisha-10 from the bench` | `11826eb`; narrow it to the label confirmation |

- A04 is partial, not stale: its row should say only the npm half is left.

Superseded but still listed (14):

| Repo | Row | Superseded by |
|---|---|---|
| harvest | `S09 Let one subscription follow many sections` | selector, Iteration 21 |
| harvest | `S10 Ocharo filter regression set over every reader's fixtures` | selector; fixtures → eval set |
| harvest | `S11 Emit item-level publisher categories as source tags` | Layer 1 tags + selector |
| harvest | `S15 Run Ocharo relevance in shadow on Afisha` | selector shadow |
| harvest | `S16 Promote AI relevance into Ocharo's delivery` | selector switch |
| harvest | `E02 Tighten ocharo-fashion-v1 against off-topic event matches` | selector |
| harvest | `A05 SCFD relevance pass in shadow on one Afisha pipeline` | Iterations 10-19 + selector shadow |
| harvest | `Tag and keyword subscriptions` (§ Features, "planned") | selector (keyword dropped, § 4) |
| events | `E01 Pull all five default Ocharo SCFD subscriptions into Events` | SL8a |
| events | `E20 Discover intake subscriptions instead of per-index settings` | one subscription per catalog |
| events | `A07 Events takes SCFD's AI classification` | stays on `filter`; the selector is the filter |
| events | `Switch a source's Classifier to payload` (§ Intake) | same as A07 |
| ocharo-platform | `Event editions and candidates` and `Feed or provider adapter` (§ Desk sourcing and event integrations, both "moved") | Events owns them since v0.3 (2 rows) |

Softer findings, not counted:

- Rows whose scope changed under § 4 but keep the old text: harvest `E19`, `S28`, `S31`.
- Pointers to S09 that should name the selector or entity model #8: harvest § Features `Entity layer` and § Engine
  `Event entities after AI classification`.
- harvest `Afisha participation readings` (§ Events integration) is probably covered by `extract-event` v4's
  participation roles (Iteration 19).
- The retired `wow-two-sdk-beta.harvest-adapters` repo (merged into harvest, #63) keeps a backlog frozen at 2026-11-10,
  with `Console on a target` shipped by S33 and `Afisha deadline … readings` shipped by S13.
- Open ids with no row: OE09, OE10, OE11 (events / ocharo-platform), W01 (wow-two-ws), E24's stale-state half.

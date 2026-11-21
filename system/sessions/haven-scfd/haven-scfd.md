# SCFD for Haven

*Last updated: 2026-11-21*

The orchestrator chat `haven - scfd` writes this track; lanes keep their own version tracks in their repos and never
edit it. Plan source: [olx-haven-plan.md](../events-integration/olx/olx-haven-plan.md) (O1-O7, B1-B4, D1; written
2026-11-21 by the `ocharo - sources and ai processing` lane).

Developer, 2026-11-21: "this chat is an orchestrator for scfd for haven · we not gonna integrate haven now · just
configure scfd with identity in ocharo's vps · configure olx pipelines, copy antrophic key from scfd for ocharo there,
run the service and monitor processing of olx posts there, improve prompts etc · basically have $200 limit of credits so
want to start evals with haiku, goal is to classify like 10K listings · so we gonna integrate bir bir and other
apartment listing platforms along the way as well".

## Status

- ✅ #1 Snapshot (orchestrator, 2026-11-21): `harvest-dev` runs on `ocharo-vps` with Ocharo's dev Identity sign-in
  (v0.2) and an Anthropic key in its vault (Wheelhouse v0.15 it. 4, vault v1); harvest HEAD `8469f53` = B1 + B2
  pushed; B3 spend guard not in the tree; the `haven` marketplace profile (OLX ×3, Joymee, BirBir, Domtut) is in code
- ✅ #2 Instance: Haven gets its own SCFD, Identity and Files on `ocharo-vps`, separate from Ocharo's (developer,
  2026-11-21: "like a separate identity server, file server and scfd - all separate from what ocharo already has in
  the vps should be perfect imo"); supersedes the same day's `harvest-dev` `haven` tenant pick; `harvest-dev` gets no
  Haven provisioning
- 🔄 #3 OLX reach from `ocharo-vps`: probe 2026-11-21 reached OLX, then HTTP 403 after ~40 requests at a 2 s pace (the
  Mac took 189 with no refusal); 15 s pace picked (developer, 2026-11-21: "yeah let's go with this then"), ~5.7K ads a day; only
  `harvest-prod` fetches OLX, since both instances share the VPS address; still refused → egress (plan D1), the
  developer's pick; `harvest-prod` run `01a1fb56` on `v0.2.57` (2026-11-21) was blocked after 10 requests at 15 s
  (8 new posts), so the VPS address is refused whatever the pace; the orchestrator's "OLX idle until D1" was
  wrong -- harvesting pipelines stay on while blocked (developer, 2026-11-21: "them blocking us doesn't stop us -
  even that info would have helped us"; `conventions/development/dev-cycle.md` § *Harvesting pipelines stay on in
  development*): OLX captures every 1 h at 15 s, BirBir at its stored interval; D1: the developer buys an IP server
  billed per GB, one sticky exit, never rotation (#14); from the Mac's home IP OLX's `robots.txt` also answers a
  CloudFront 403 to harvest's UA and to curl, so the block may key on the client, not only the address
- ✅ #4 Spend guard (plan B3): harvest `98aff1a`, checker pass, backend suite green; settings
  `Harvest:Processing:Budget:{LimitUsd, SoftShare, CycleStartDay, SinceUtc}`, read by `processing budget`; dev values
  set once its release reaches `harvest-dev`
- 🔄 #5 Eval set and Haiku evals (plan B4, O6): `olx-listings-v1`, 80 OLX ads, labels from Claude Code agents; v7 on
  Haiku 5.5 is Haven's prompt (`harvest-prod` `extract-listing` version 2): offer 0.988, period 0.950, price 0.912,
  rooms 0.988, terms 0.963, tenants 0.812, author kind 0.600 strict / 0.713 rule 12 / 0.850 coarse (bar 0.90), 0 leaks,
  1/80 schema-invalid, $0.00061 an ad; v8 scored lower; next round reads `harvest-prod` volume answers; evals spent
  $0.28; next set `joymee-listings-v1` (~100 Joymee ads captured from the Mac, agent gold labels, contacts scrubbed),
  since Joymee is the volume source and v7's author rules lean on OLX fields; a version reaches `harvest-prod` only
  when it beats v7 on both sets and on a held-out ~40-ad Joymee set (orchestrator, 2026-11-21); v7 on
  `joymee-listings-v1` (80 ads, `harvest-dev` run `01a1fbe2`): offer 1.000, period 0.988, price 0.988, terms 0.982,
  tenants 0.875, rooms 0.850 and author 0.775 under the bar, 0 invalid, 0 leaks, $0.00052 an ad; misses are rule
  gaps (`2/4/12` as floors, Uzbek fee wording, "без маклера" owner cues, agency voice) that v9 targets; Joymee's
  structured attributes and `advertiser_type` never reached the prompt (`PostExtractionContent` read `olx.ad.v1`
  only): harvest fix reads `joymee.ad.v1` attributes and renders Joymee's own account type into `{{seller}}`
  (`advertiser_type` 1 → `owner`, 2 → `agent`, else `unknown`; OLX's `private`/`business` unchanged, since OLX
  `business` stays unknown under rule 12); held-out 40 gold: type 2 agent 26, unknown 12, owner 0; gold rule 15 takes the account type as the poster's statement unless the text says otherwise, like
  OLX rule 12 (orchestrator, 2026-11-21); harvest `2f3a673` (v0.2 Iteration 41) lifts v7 on `joymee-listings-v2`
  (inputs as rendered, gold rules 1 + 15), two runs: author 0.950 / 0.925, rooms 1.000 / 0.975, floor 1.000 / 0.975,
  every bar field passing; v10 ties v7 on both Joymee sets and gains only OLX author (0.771 vs 0.700), so
  `harvest-prod` keeps v7 and v10 is revisited when OLX runs; v7 swings ±3-4 points a field across runs
- 🔄 #6 Provisioned on `harvest-prod` 2026-11-21 (`manual`, 7 searches, v5 as prompt version 1, no key issued, no
  schedules); `pipelines pace|run|schedule|show` host verbs committed harvest `60cef0b` (all tiers green), eval record `8d2f28e`;
  `v0.2.57` promoted to `harvest-prod` by hand 2026-11-21 (migrate 18 → 19, probe 200, data snapshotted first; dev
  auto-deploys, prod is promoted); on it the lane sets the 15 s pace, `marketplace setup --profile haven
  --model-processing auto` and one bounded apartments-rent capture, with schedules after the `24002e8` release. Plan: `--model-processing manual`, a ~50-listing sanity batch, then `auto`;
  volume does not wait for #5 -- prompt iterations draw on the volume answers and the eval set
- 🔄 #7 (2026-11-21: `harvest-prod` on `v0.2.61` = `d961ea9`; Joymee capture every 2 h, run `01a1fb82-7211`
  58 new posts, 0 failed; BirBir answers a challenge on its first request from the VPS, schedule off, folded into
  D1; OLX idle; 66 `extract-listing` answers, 0 invalid, $0.0378, $0.00057 a listing; Joymee capture reads only its
  newest ~58, so `pipelines run|schedule --kind discover|harvest` reach the catalog, harvest `be193fc` (v0.2
  Iteration 40, every tier green), live on `harvest-prod` `v0.2.62`: one cycle took Joymee from 58 to 178 posts, no
  challenge; discover every 30 m, harvest every 15 m; 185 answers, 0 invalid, $0.1021; BirBir schedule off on prod)
  Schedules and AI `auto` on every Haven collection source (OLX ×3, Joymee, BirBir), then improve prompts and
  sources from the volume answers (developer, 2026-11-21: "set the schedules, set the ai processing in all sources and
  work on improving them"); after the scheduler UTC hotfix reaches `harvest-prod`
- 🔄 #8 BirBir, Joymee, Domtut on the same listing route: BirBir and Joymee `apartments-rent` imply `listing` +
  `real-estate/apartments`, harvest `50840fb` (v0.2 Iteration 36, every tier green)
- ⬜ #9 10K listings classified on Haiku 5.5, measured spend inside the cap
- ✅ #15 Available sources: the instance turns registered sources on in its database; Sources shows only those, a
  separate Available page lists the rest (developer, 2026-11-21: "instance itself will be able to configure which
  sources will be ever turned on - saved in db"); off = disabled, never removed ("like disable not completely
  remove"); Haven's instance turns on listing sources only, Ocharo's `harvest-dev` keeps its four; design harvest
  `fb6a5d2` (`source-catalog.md`, v0.2 iteration 32); unit = publisher group or marketplace site; turning on from
  Available provisions with schedules and model processing off (orchestrator, derived); committed harvest `b27a1f6` 2026-11-21 (checker 14/15, the gap test-only; all tiers green), the gap closed by
  `8d975ce` (7 gate tests);
  `harvest-prod` and `harvest-dev` run `v0.2.57` (= `631c636`, holds #15 and the image copies, not the scheduler fix
  `24002e8`); checks recorded harvest `152ac92`: `harvest-prod` Sources shows Haven's 4 sites, Available shows the 27
  Ocharo groups (nothing toggled there); a `harvest-dev` on/off/on toggle survived reloads and a redeploy; evidence
  in [available-sources/](available-sources/); open backlog row: the Available page shows its lead line twice
- ✅ #16 Haven's stack: SCFD target first (credit cycle ends 2026-11-24), then Identity with console sign-in, then
  Files; per-instance `LimitUsd` caps summing ≤ $195
  - ✅ `harvest-prod` healthy 2026-11-21 (`0.2.54+748d5cd`, own database): Haven takes the `prod` environment names on
    `ocharo-vps` (Wheelhouse names by `<product>-<env>` per server); `files_prod` was placed for Ocharo prod in
    Wheelhouse v0.14, so Ocharo prod there needs instance-suffix work or another server
  - ✅ Anthropic key on `harvest-prod`, vault v2 (developer, 2026-11-21); the first Haiku batch proves it
  - ✅ Identity `identity-prod` and Files `files-prod` healthy; the developer signed in to the Haven SCFD console as
    operator 2026-11-21 through `@haven_agents_dev_bot` (the stored token is the dev bot's)
  - ⬜ (history) Identity `identity-prod`: `deploy.yml:113-115` certificate keys gain `generate` (identity repo, one release);
    admin signs in by Telegram with one of Haven's Agents bots (developer, 2026-11-21: "we have tg bot for haven
    as well - we'll reuse that"; Haven `telegram.md:11-16`), provided no running Haven.Auth loses its updates
  - ⬜ Files `files-prod`
- ✅ #17 (2026-11-21: `assets report` on `v0.2.61`: OLX 46 of 46 images copied, no fetch refusal from
  `olxcdn.com`; Joymee posts with a phone 28 of 58; the OLX phone share waits on D1, read by the olx lane) OLX images and phones (design 2026-11-21, `haven-browser-17.md` in the lane's notes):
  - images: harvest's `SourceAssetWorker` copies OLX photos from adapter-declared CDN hosts into Haven's Files, first
    6 per post, own ≥2 s pace, no browser and no separate service; Haven's old browser service is gone (Haven
    `f0a10453`) -- v0.2 Iteration 35 committed harvest `631c636` (8 tiers, 2,214 tests green); console read of
    `harvest-prod` run `01a1fb56` (2026-11-21): copies work, 3 of 16 images copied (JPEG, 525 px, ~52 KB each),
    13 wait while the OLX host is paused, by design; ~0.3 MB a post at 6 photos; size stays OLX's default until
    Haven's UI needs larger (`;s=1280x960`, ~3–4× the bytes; orchestrator pick, backlog row)
  - phones: automated reveal through OLX's CAPTCHA gate is not built -- the lane declined it as bot-detection
    circumvention to collect private sellers' phones, and auto mode refused the reveal probe; phones written in the
    ad go into the post's contacts field as plain text, no manual reveal field (developer, 2026-11-21: "we just
    harvest from olx and store here as plain text man")
  - phone coverage on the Mac capture `harvest-b4`: 29 of 180 OLX posts (16%) -- 27 in the seller display name, 2 as
    `tel:` links, 1 in the ad text; v0.2 Iteration 38, harvest `b42f8de` (8 tiers, 2,325 tests green, spec
    checker pass), adds the seller name and attributes to the E.164 `contacts` rule (`e164-and-email@3`); no prompt
    renders a phone and Haven's delivery stays contact-free; Iteration 37 is Ocharo's Telegram reader `4c10883`;
    counts come from the read-only host verb `assets report` (v0.2 Iteration 39, harvest `d961ea9`, 8 tiers green;
    migration `020-asset-outcomes` records each copy's outcome and bytes), since auto mode refused SSH to
    `ocharo-vps` (2026-11-21, orchestrator pick); 13 of the run's OLX images stayed uncopied after the pause
    lifted, cause read from `byOutcome` once the release is on `harvest-prod`; the real
    coverage is read from `harvest-prod`'s first OLX capture

## Decisions

- #10 Haven is not integrated now: no Haven repo change, no `haven-supply` key issued (developer, 2026-11-21)
- #11 Haiku 5.5 runs evals and volume; Sonnet only re-runs flagged answers inside the guard, Opus never on API credits
- #12 Credit cap: the $200 monthly Claude Console credit, cycle 25th to 24th, unused credit expires
  (`ocharo-sources-plan.md:7-8`); the guard counts one instance, so caps split per instance: Haven 135, Ocharo
  `harvest-dev` 60 once Haven's target is live (195 until then), `SoftShare 0.8`, `CycleStartDay 25`; harvest-dev MTD
  $0.24 on 2026-11-21; under the developer's "it's ok to spend all on anything just smth useful" (AI `context.md:27`)
- #13 Gold labels come from Claude Code agents (subscription), never from API calls
- #14 Sourcing rules bind: paced, inside `robots.txt`, no rotating proxy pools; contacts stay out of prompts, evals,
  fixtures, reports and logs; the developer allowed CAPTCHA solving for OLX phone reveal (2026-11-21), but it is not built (#17)
- #18 Haven runs one SCFD, `harvest-prod`: `prod` is only the name (`dev` names on `ocharo-vps` are Ocharo's); it takes
  promoted releases only (it served `0.2.54` while `harvest-dev` took `0.2.55`); the olx lane promotes
- #19 Browser steps in this goal run in Chrome profile `wow2` only (developer, 2026-11-21: "let's stick to use wow2
  chrome profile only")

## Lanes

| Lane | Session | Repos | Owns |
|---|---|---|---|
| `haven - scfd olx listings` | `haven-scfd-olx` `local_cbde7205-874e-42c0-8229-52d3a276f286` | `wow-two-sdk-beta.harvest`; `harvest-dev` settings via `wow2` and Wheelhouse | #3-#9 |
| `haven - scfd available sources` | `scfd-available-sources` `local_2744267d-65cb-4b24-af2d-2f77b0e48b8e` | `wow-two-sdk-beta.harvest` (console + backend) | #15 (done, archived 2026-11-21) |
| `haven - separate platform stack` | `haven-stack` `local_0f62fb9b-4cc8-4aae-83e7-9b25e566cf48` | Wheelhouse targets for `harvest`, `identity`, `files` on `ocharo-vps` | #16 (done, archived 2026-11-21) |
| `haven - scfd browser and phone reveal` | `haven-browser` `local_10fe89ba-28f5-4147-90a3-b63cd3f9a2a1` | harvest seam; a browser service if separate | #17 (done, archived 2026-11-21; the OLX phone share moved to the olx lane) |

- Other chats on harvest: `ocharo - sources and ai processing` (Ocharo sources), `ocharo - scfd integration build`;
  the OLX slice (plan B3 onward) moved here on 2026-11-21; B3 handed over with no edits at `8469f53`
- Harvest builds run one at a time: `ocharo - sources and ai processing` keeps SR05, SR06; each build start goes
  through the orchestrator to the other lane
- Prompt drafts v4, v5, `schema-v2.json`: `~/Library/Application Support/Claude/side-session-notes/local_4597465c-ca6d-445b-b4f1-77546f8511b4/ai-evals/extract-listing/`

## Done when

- 10K OLX apartment listings carry an `extract-listing@2` answer on Haiku 5.5 on Haven's SCFD
- Eval report: per-field accuracy against the plan's bar (#6 of the plan), invalid and failure rates, cost per listing
- Measured month-to-date spend under the #12 cap; the guard reads its state with `processing budget`
- BirBir and at least one more apartment platform answer on the same route

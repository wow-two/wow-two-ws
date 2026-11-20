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
  developer's pick
- ✅ #4 Spend guard (plan B3): harvest `98aff1a`, checker pass, backend suite green; settings
  `Harvest:Processing:Budget:{LimitUsd, SoftShare, CycleStartDay, SinceUtc}`, read by `processing budget`; dev values
  set once its release reaches `harvest-dev`
- ⬜ #5 Eval set and Haiku evals (plan B4, O6): labels from Claude Code agents, API spend only on Haiku runs
- 🔄 #6 Provisioned on `harvest-prod` 2026-11-21 (`manual`, 7 searches, v5 as prompt version 1, no key issued, no
  schedules); OLX pace and single runs wait on two host verbs (next harvest slot after #15), since `harvest-prod` has no
  operator route yet. Plan: `--model-processing manual`, a ~50-listing sanity batch, then `auto`;
  volume does not wait for #5 -- prompt iterations draw on the volume answers and the eval set
- ⬜ #7 Monitor processing and iterate prompts: per-field accuracy, invalid rate, cost per listing
- ⬜ #8 BirBir, Joymee, Domtut on the same listing route
- ⬜ #9 10K listings classified on Haiku 5.5, measured spend inside the cap
- ⬜ #15 Available sources: the instance turns registered sources on in its database; Sources shows only those, a
  separate Available page lists the rest (developer, 2026-11-21: "instance itself will be able to configure which
  sources will be ever turned on - saved in db"); off = disabled, never removed ("like disable not completely
  remove"); Haven's instance turns on listing sources only, Ocharo's `harvest-dev` keeps its four; design harvest
  `fb6a5d2` (`source-catalog.md`, v0.2 iteration 32); unit = publisher group or marketplace site; turning on from
  Available provisions with schedules and model processing off (orchestrator, derived); building since 2026-11-21
- 🔄 #16 Haven's stack: SCFD target first (credit cycle ends 2026-11-24), then Identity with console sign-in, then
  Files; per-instance `LimitUsd` caps summing ≤ $195
  - ✅ `harvest-prod` healthy 2026-11-21 (`0.2.54+748d5cd`, own database): Haven takes the `prod` environment names on
    `ocharo-vps` (Wheelhouse names by `<product>-<env>` per server); `files_prod` was placed for Ocharo prod in
    Wheelhouse v0.14, so Ocharo prod there needs instance-suffix work or another server
  - ✅ Anthropic key on `harvest-prod`, vault v2 (developer, 2026-11-21); the first Haiku batch proves it
  - ⬜ Identity `identity-prod`: `deploy.yml:113-115` certificate keys gain `generate` (identity repo, one release);
    admin signs in by Telegram with one of Haven's Agents bots (developer, 2026-11-21: "we have tg bot for haven
    as well - we'll reuse that"; Haven `telegram.md:11-16`), provided no running Haven.Auth loses its updates
  - ⬜ Files `files-prod`
- ⬜ #17 OLX phone reveal and images: browser rendering and CAPTCHA solving where needed; in SCFD or a separate
  service, Haven's old browser service or new -- the lane analyses and decides (developer, 2026-11-21: "captcha solve
  doesn't cost us much except the browser rendering ... so analyze and decide"); build after the design summary

## Decisions

- #10 Haven is not integrated now: no Haven repo change, no `haven-supply` key issued (developer, 2026-11-21)
- #11 Haiku 5.5 runs evals and volume; Sonnet only re-runs flagged answers inside the guard, Opus never on API credits
- #12 Credit cap: the $200 monthly Claude Console credit, cycle 25th to 24th, unused credit expires
  (`ocharo-sources-plan.md:7-8`); the guard counts one instance, so caps split per instance: Haven 135, Ocharo
  `harvest-dev` 60 once Haven's target is live (195 until then), `SoftShare 0.8`, `CycleStartDay 25`; harvest-dev MTD
  $0.24 on 2026-11-21; under the developer's "it's ok to spend all on anything just smth useful" (AI `context.md:27`)
- #13 Gold labels come from Claude Code agents (subscription), never from API calls
- #14 Sourcing rules bind: paced, inside `robots.txt`, no rotating proxy pools; contacts stay out of prompts, evals,
  fixtures, reports and logs; CAPTCHA solving allowed for OLX phone reveal only (#17, developer, 2026-11-21, reversing
  events-integration #50 for this use)
- #18 Haven runs one SCFD, `harvest-prod`: `prod` is only the name (`dev` names on `ocharo-vps` are Ocharo's); it takes
  each harvest release by auto-promote once `harvest-dev`'s dev check passes

## Lanes

| Lane | Session | Repos | Owns |
|---|---|---|---|
| `haven - scfd olx listings` | `haven-scfd-olx` `local_cbde7205-874e-42c0-8229-52d3a276f286` | `wow-two-sdk-beta.harvest`; `harvest-dev` settings via `wow2` and Wheelhouse | #3-#9 |
| `haven - scfd available sources` | `scfd-available-sources` `local_2744267d-65cb-4b24-af2d-2f77b0e48b8e` | `wow-two-sdk-beta.harvest` (console + backend) | #15 |
| `haven - separate platform stack` | `haven-stack` `local_0f62fb9b-4cc8-4aae-83e7-9b25e566cf48` | Wheelhouse targets for `harvest`, `identity`, `files` on `ocharo-vps` | #16 |
| `haven - scfd browser and phone reveal` | `haven-browser` `local_10fe89ba-28f5-4147-90a3-b63cd3f9a2a1` | harvest seam; a browser service if separate | #17 |

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

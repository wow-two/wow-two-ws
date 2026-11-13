# Haven restart — OLX supply through SCFD

*Last updated: 2026-11-14*

Orchestrator: `10x - haven restart` (`local_6d9157de-9c87-4550-9ba2-a02f36d1ffc3`). Lanes message it; the developer
talks only to it.

## Goal

Haven runs in production on fresh OLX listings that SCFD collects into a private Haven container, classified by Claude
on the Ultra API credit before that credit's cycle ends on 2026-11-24.

Done when:

- SCFD holds a Haven tenant with a private container, OLX Tashkent residential-rent sources, scheduled pipelines and a
  `wow2.post.v1` subscription; a bounded run on the deployed host delivers to that subscription.
- Haven production runs the current stack (v1.2 or later), its OLX intake reads the SCFD subscription, the cursor
  advances after storage, and gone/relisted links update the listing.
- Haven's classifier runs on Claude through a key of the Console org `WoW 2.0`, which the Ultra credit funds.

---

## #1 OLX registration today

| Layer | State | Evidence |
|---|---|---|
| Haven production | v1.0 on the VPS with its own scraper; v1.1 and v1.2 never reached production | Haven `backlog.md` § Launch, `v1.2.md` "Next" |
| Haven code (`main`) | two OLX intake paths behind `HARVEST_OLX_ENABLED`, default `false`: ListingShelf (default) and Harvest delivery | Haven `aa83078a` |
| Haven Harvest client | pulls `GET api/subscriptions/{id}/events` with OAuth client credentials (`HarvestOlx:*`); keeps `post.new` / `post.changed` / `post.extracted` whose `base.kind` is `listing` and whose link carries `olx.ad.v1`; throws on `post.purged`; ignores `link.state` and `post.merged` | `HarvestOlxClient.cs`, `HarvestOlxIntakePipeline.cs` |
| SCFD reader | the OLX reader ships in the image (`AddHarvestListingSources`, composed in `HarvestSources.Api`); one bounded local live run delivered 2 events; no contact reveal | `sources/Olx/olx.md`, `research/olx-source-review.md` |
| SCFD registration | nothing for Haven: no tenant, container, source, pipeline or subscription; repeatable setup exists only for Ocharo (`ocharo setup`, `/api/ocharo/sources/setup`); `haven-supply` appears only as a sample grant | `contract.md` § Source host, `deployment.md` § Service access |
| SCFD egress | the OLX proxy route is built and unconfigured; GeoNode, then Decodo, ranked first | `research/olx-egress-options.md` |
| ListingShelf | v0.2 built, verification pending, not deployed; still the only Domtut collector | `.claude/repo-registry.md` |

Deltas the lanes verify first:

- Scope name: Haven's `deployment.md` asks for an `events.read` Identity scope; SCFD registers `harvest.events-read`.
- Auth form: Haven's client speaks OAuth client credentials against SCFD's issuer (on dev, Ocharo's Identity); SCFD
  also accepts tenant API keys (`hv_…`), which need no Identity client.
- Event types: `DeliveryEventTypes.cs` carries `link.state` (live, suspect, gone, relisted) and `post.merged`, which
  Haven drops today, so a rented flat stays live in Haven.

Haven lane, verified 2026-11-14:

- Scope: SCFD's `events:read` maps to Identity `harvest.events-read` (`HarvestScopeConstants.ToIdentityScope`);
  Haven's `events.read` is stale, fixed in Haven's doc. Haven's settings accept OAuth only; a tenant API key needs a
  settings branch in Haven.
- Wire: `link.state` carries the whole post with `linkId`; a `post.merged` loser has `mergedInto` and no links, the
  survivor follows as `post.changed`; `post.unmerged` ships too. Haven keys listings by OLX `externalKey`, so merges
  need acknowledgement only.
- `external_listings.external_status` (active/deleted) exists, never written; classification filters on it, search
  and publishing do not — gone/relisted write it, and those two filters follow.
- Classifier on `main`: Anthropic `claude-sonnet-4-6`, fallback OpenAI `gpt-5.4`; the move is model IDs plus the key.
  Production v1.0's config is not in the repo; the 2026-03 record says Sonnet 4.6 with a DeepSeek fallback.

---

## #2 What to build

### SCFD lane

1. Haven provisioning: a product-neutral marketplace setup (host verb plus operator route), idempotent like
   `ocharo setup` — tenant `haven`, a private container, OLX sources for Tashkent residential rent, pipelines with
   schedules and link checks, a `wow2.post.v1` subscription filtered to OLX listings, the consumer credential; it
   prints the IDs.
2. OLX egress from the deployed host: a bounded direct probe first; a proxy profile only after a refusal.
3. Release and provision Haven on dev; a production SCFD target follows Haven's go-live.
4. A Domtut reader, so ListingShelf retires — after 1-3.

### Haven lane

1. Intake against current SCFD: envelope, scope name, auth form (#1 deltas); handle `link.state` gone/relisted and
   `post.merged`.
2. Local end-to-end run against `HarvestSources.Api` provisioned by the SCFD lane's setup.
3. Close v1.2 (the real-group pass), then upgrade production from v1.0 (`deployment.md` § Upgrading v1.0
   production), backup first.
4. Classifier on Claude through the credit-funded key; reclassify the stored backlog where it improves triage.
5. Cutover: production OLX intake reads SCFD.

---

## #3 Lanes

| Lane | Session | Repo | Owns |
|---|---|---|---|
| scfd | `hv-scfd`, `local_df774994-fb45-4e75-9631-598a8f5dd82b`, started 2026-11-14, Opus 5.5 `xhigh` | `workbench/wow-two-sdk-beta/wow-two-sdk-beta.harvest` | `sources/Module/Marketplace/`, `sources/Olx/`, a new `sources/Domtut/`, the marketplace verb and routes in `service/HarvestSources.Api`, their tests, `deployment.md` § Haven |
| haven | `hv-haven`, `local_e82be65b-fc8f-42ae-a5e5-2c15d5d72100`, started 2026-11-14, Opus 5.5 `xhigh` | `workbench/maxs-projects/ventures/saas/10x-ven-haven` | the whole repo |

Other writers in the SCFD repo, from the `ocharo - scfd integration` goal (`system/sessions/events-integration`):
`ev-scfd` (engine), `ev-ai` (relevance step in the engine), `ev-scfd-live` (`harvest.frontend-services/` only).

---

## #4 Cross-lane contract

- Delivery: `wow2.post.v1`, types per `packages/Abstractions/Delivery/DeliveryEventTypes.cs`, pages as
  `{ data: { data, next, hasMore } }`.
- Credential (SCFD lane, 2026-11-14): a tenant API key as `X-Api-Key`, `events:read` only, revocable — OAuth on dev
  needs an `ocharo-platform` Identity release and prod has no issuer yet. Haven adds an API-key mode.
- Subscriptions are one per pipeline (`SubscriptionDeclaration.PipelineId`): setup prints one per OLX search URL, and
  Haven's settings hold a list with one cursor each.
- Scope (`rent-res`, Haven `product.md`: monthly, daily, weekly): apartments and houses on long-term rent
  (`.../arenda-dolgosrochnaya/tashkent/`), apartments on daily rent, newest first. v1.0 read
  `nedvizhimost/kvartiry/tashkent/` (sale and rent).
- A relist arrives as `link.state` `relisted`; `post.relisted` is reserved. `post.unmerged`, `pipeline.run` and
  `pipeline.health` need no handling in Haven.
- Setup output (tenant, container, subscription IDs, the key) → Haven's target settings (`HARVEST_OLX_*`); the key
  goes to the vault, never to chat or git.

---

## #5 Decisions

- #5.1 "A separate container of SCFD" reads as a private SCFD container for Haven's tenant inside the shared SCFD
  deployment, not a second SCFD instance (orchestrator default, 2026-11-14; open to the developer's correction).
- #5.2 Haven moves onto the AI layer (`wow-two-sdk-beta.ai`) only after `ev-ai` finishes; the developer says so in
  the orchestrator chat. Until then Haven keeps `Haven.Platform.Ai`.
- #5.3 Open: events-integration #50 keeps SCFD sourcing internal ("nothing sourced is republished", no proxy), while
  Haven publishes listings to its Telegram group.

---

## #6 Asks held for the developer

- An OLX proxy credential, only if the direct probe is refused.
- An Anthropic key in the Console org `WoW 2.0` (`haven-classifier`), in Haven's gitignored
  `engineering/deployment/.env` as `ANTHROPIC_API_KEY` — asked 2026-11-14.
- The go-ahead for the production upgrade on Haven's VPS, in the runbook's order (`upgrade-v1.0.md`, Haven
  `e199eff0`): read-only pre-flight (H1–H6 shell, Q1–Q10 database, Cloudflare SSL mode) → a v1.0 dump for a local
  rehearsal → publishing `v1.2.0` so images exist → the upgrade day. Asked 2026-11-14.
- Tailscale connected on the Mac — the SCFD lane's dev Run needs the Wheelhouse console. Asked 2026-11-14.

---

## #7 Built

- Haven `a564b342`: a gone link hides the listing from search, publishing and alerts; a relist restores it; stale
  events are ignored. Its push carried the developer's unpushed `aa83078a`.
- Haven `e0ef191d`: classification on Claude Haiku 5.5 (`Lite`) with Sonnet 5.5 (`Core`) as fallback; OpenAI left
  the route. 198 tests pass (lane report).
- Haven `c0f4a031`: the tenant key in `HARVEST_OLX_API_KEY` as `X-Api-Key` (OAuth stays the second mode), a
  comma-separated `HARVEST_OLX_SUBSCRIPTION_IDS` with one cursor each, relist through `link.state`. 203 tests pass
  (lane report). The local end-to-end run waits on the SCFD lane's local base URL, subscription IDs and key location.
- SCFD `8128bc4`, `e73d03d`: the marketplace setup verb and routes with Haven's profile, delivered counts in
  status; three subscriptions (apartments-rent, houses-rent, daily-rent). A local live run pulled 5 OLX listings in
  the shape `HarvestOlxClient` parses. The dev Run waits on Tailscale (stopped on the Mac, 2026-11-14).
- Haven `e199eff0`: the v1.0 upgrade rewritten as a checked runbook. Migrations `002`–`016` drop, truncate or delete
  nothing; `001` equals v1.0's baseline. Fixed blockers: no published images (private repo, so a `ghcr.io` login on
  the VPS), v1.0's `haven-caddy` on :80, compose's fixed `Host=postgres`, write loss in the old order. New flow:
  freeze writers, dump, restore into compose Postgres; rollback restarts v1.0. Open risk: production must hold exactly
  one `1 · baseline` journal row (Q1). SCFD's OLX `externalKey` matches v1.0's `-ID…` token, so intake updates rows.
- Credit (Haven lane estimate: 18K cached prompt tokens, 5 listings a call): Haiku 5.5 ≈ $1 per 1,000 listings,
  Sonnet 5.5 ≈ $26 per 1,000. Plan: a 50-listing paired sample on both (≈ $1.40, approved by the orchestrator as
  inside the goal), then the stored backlog on Haiku after the production upgrade, Sonnet only for agent-queued
  reclassifications.

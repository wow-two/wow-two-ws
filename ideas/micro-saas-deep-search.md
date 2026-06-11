# Micro SaaS Deep Search

*Created: 2026-05-22*
*Last updated: 2026-05-22*

Deep search across the micro SaaS landscape, filtered through a tightened constraint set after Haven pause.

Builds on [market-analysis.md](./market-analysis.md) — same scoring framework + audience tiers + demand categories, narrower lens.

---

## Constraints reset (2026-05-22)

| Constraint | Value | Implication |
|---|---|---|
| Budget per project | **$20–50** | No expensive AI per request; no data licensing |
| Launch target | **20–30** (revised from 50–100) | One per week cadence after template |
| Hit-rate target | 1–5 working out | Each idea must clear a 4-week first-revenue gate, else kill |
| Haven status | **Paused** | IP-blocked scraping + ~$1K Claude budget unavailable |
| Existing infra | wow-two backend SDK (52 pkgs), UI lib (227 components) | Incremental build cost much lower than typical indie — template gets you 80% to launch |
| GWDNBM | Mandatory | No ads, no spam, no engagement bait |

**Real per-product cost breakdown:**

| Item | Cost |
|---|---|
| Domain (`.fyi/.app/.tools`) | $10–20/yr |
| Hosting | ~$0 (single shared Hetzner box, ~$5/mo for ALL 20–30 products via subdomain or domain mapping) |
| Database | ~$0 (Postgres on same box, or Supabase free tier per project) |
| Email | ~$0 (Resend free 100/day shared) |
| SSL | $0 (Cloudflare) |
| Payments | $0 fixed (Stripe % only) |
| **Per-product total** | **~$15–25 first year** |

$20–50 budget is genuinely fine **IF** the product doesn't burn AI or scraping costs. That's the filter.

---

## Cost-of-operation tiers

| Tier | Marginal cost/request | Examples | Strategy share |
|---|---|---|---|
| **0** | $0 | Cron, webhooks, monitors, generators, calculators, directories | **~70% of portfolio** |
| **1** | cents (Haiku / Groq / 4o-mini, single short call) | Narrow extraction, single classification | **~30% of portfolio** — *only if priced to pass cost through* |
| **2** | dollars (Opus / Sonnet / GPT-4 / heavy image gen) | Long-context analysis, image generation | **0% of portfolio** until cash flow exists |

**Rule:** if a product would lose money on 100 free signups, kill it. Either Tier 0 (no AI) or Tier 1 with pay-per-use pricing that exceeds API cost by 3–5×.

---

## Killed-by-budget categories

Skip these even if they're attractive in absolute terms:

- **Long-context LLM products** — contract analysis, deep summarization, multi-file Q&A
- **Image generation products** — Midjourney-clone economics burn cash fast
- **Heavy scraping plays** — IP blocks (Haven lesson), proxies $50+/mo
- **Audio/video at scale** — Whisper / transcription costs add up at any volume
- **Custom-trained ML models** — training costs + ops overhead
- **Marketplaces / social** — need critical mass; bootstrap is brutal
- **Anything requiring paid data licensing** — court records APIs, financial data APIs

---

## Candidate bank — 60 ideas across 7 buckets

### Bucket A — Pure compute, $0 marginal (preferred)

| # | Idea | Model | Audience | Notes |
|---|---|---|---|---|
| A1 | Cron-as-a-service | sub $9/mo | devs | Daemon + DB rows; <1 wk build |
| A2 | Webhook debugger / relay | sub $9–19/mo | devs | Receive → store → replay |
| A3 | Static-site form handler | sub $5–15/mo | devs/designers | Formspree alt; win on no-spam |
| A4 | Status page hosting | sub $5/mo per page | SaaS owners | Tiny build |
| A5 | SSL + domain expiry monitor | sub $3 per 10 items | devs/agencies | Daily cron |
| A6 | Uptime monitor (privacy-first) | sub $5/mo | devs | Saturated; differentiate on GWDNBM |
| A7 | DNS history tracker | pay $1/lookup | security/devs | Free APIs exist; aggregate + cache |
| A8 | WHOIS history reporter | pay $1–3/lookup | legal/security | API-driven |
| A9 | Subdomain finder | pay/sub | security | API-driven |
| A10 | HTTP header inspector API | pay-per-call | devs | Tiny |
| A11 | CSV cleaner (dedupe, validate) | $5/file or $9/mo | analysts | Pure compute |
| A12 | Open Graph image generator (templated) | pay $0.10/img or $9/mo | marketers | No AI — templates + canvas |
| A13 | QR code w/ analytics | sub $5/mo | physical biz | Sticky |
| A14 | Niche short URL + analytics | sub $5–15/mo | specific verticals | Industry-niched wins |
| A15 | Sitemap generator/validator | one-shot $9 | SEO teams | Run once per audit |
| A16 | Robots.txt tester / linter | freemium → $5/mo | SEO | SEO long-tail magnet |
| A17 | OG / Twitter card debugger | sub $5/mo | marketers | Embeddable widget |
| A18 | CORS tester / playground | free w/ pro $5/mo | devs | SEO + dev tool |
| A19 | Cron expression visualizer | $5/mo for save/share | devs | Free version exists; charge for team |
| A20 | Regex tester w/ named library | $5/mo for save/share | devs | Same pattern |
| A21 | Color palette extractor API | pay $0.05/img | designers | No AI |
| A22 | Favicon generator (all platforms) | one-shot $5 | devs | Templates |
| A23 | Sitemap → SEO landing-page audit | $19 one-shot | SEO | Programmatic |
| A24 | Schema.org markup generator | $9 one-shot | SEO | Templated |
| A25 | Lighthouse-on-demand audit | $5 one-shot or $19/mo | devs | Free CLI, charge for hosted |

### Bucket B — Cheap AI per-request, pass-through pricing

| # | Idea | Model | Audience | Marginal |
|---|---|---|---|---|
| B1 | Receipt → CSV | $0.20/doc or $15/mo | accountants | Haiku Vision ~$0.005/img |
| B2 | Business card → vCard / CRM | $0.10/card or $9/mo | sales/networking | Haiku ~$0.002 |
| B3 | Invoice → structured data API | $0.30/doc | accounting / B2B | Haiku |
| B4 | Resume → ATS-friendly JSON | $0.20/doc | recruiters | Haiku |
| B5 | Email signature parser | $0.05/sig | sales tools | Haiku |
| B6 | Bank statement → CSV (per bank format) | $0.50/page | freelancers / SMB | Haiku |
| B7 | Handwriting → markdown | $0.50/page | students/researchers | Haiku Vision |
| B8 | Subtitle / caption cleaner | $9/mo | YouTubers | Haiku on text only |
| B9 | Podcast chapter timestamps from transcript | $5/episode | podcasters | Haiku on text |
| B10 | Newsletter spam-checker (will it land?) | $0.10/check or $9/mo | newsletter writers | Haiku |

### Bucket C — Niche directories / aggregators (zero AI, SEO play)

| # | Idea | Model | Distribution |
|---|---|---|---|
| C1 | Niche job board (one specific industry) | listing fees $99/post or $29/mo | SEO + community |
| C2 | Tool comparison directory (programmatic SEO) | affiliate + sponsored listings | SEO long-tail |
| C3 | Conference/event aggregator for one industry | $9/mo for alerts | SEO |
| C4 | Niche API directory (e.g. real-estate APIs, gov APIs) | sponsored listings | SEO |
| C5 | Niche prompt directory (e.g. legal AI prompts) | $5/mo paid library | SEO + creator share |

### Bucket D — Notifications / alerts (sticky recurring)

| # | Idea | Model | Audience |
|---|---|---|---|
| D1 | License renewal reminder (CME for doctors, bar for lawyers) | $5/mo | high-WTP pros |
| D2 | Trademark filing watcher | $10/mo per term | legal / brand owners |
| D3 | Domain availability watcher (alert when frees up) | $3/mo per domain | brand owners / devs |
| D4 | GitHub release watcher (custom alerts beyond stars) | $5/mo | devs |
| D5 | Price drop tracker for narrow category | $5/mo | hobbyists / B2B buyers |
| D6 | Auction lot alerts (generalized NT/UZ play) | $5–10/mo per query | RE investors UZ |
| D7 | Court case tracker (specific jurisdiction) | $19/mo | legal / journalists |
| D8 | Local gov public notice alerts | $5/mo | RE / legal / citizens |

### Bucket E — Compliance / legal one-shots (high WTP)

| # | Idea | Model | Price |
|---|---|---|---|
| E1 | Privacy policy generator | one-shot | $29 |
| E2 | Terms generator | one-shot | $19 |
| E3 | Cookie banner customizer (embeddable) | sub | $5/mo |
| E4 | DPA generator | one-shot | $29 |
| E5 | GDPR data-request handler (DSAR portal) | sub | $19/mo |
| E6 | Vendor security questionnaire generator | one-shot | $49 |
| E7 | Accessibility (WCAG) audit + monitoring | hybrid | $39 + $19/mo |
| E8 | SOC2 evidence-collection helper (light) | sub | $29/mo |

### Bucket F — Creator tools (Tier B audience, viral)

| # | Idea | Model | Notes |
|---|---|---|---|
| F1 | Subtitle / caption cleaner | $9/mo | (also in B8) |
| F2 | Podcast clip extractor (transcript → snippets) | $9/mo | text only — cheap |
| F3 | Tweet thread → blog post | $5/use | text |
| F4 | Course outline generator from transcript | $5/use | text |
| F5 | YouTube end-card / thumbnail layout templates | $5/mo | templated; no AI |
| F6 | Lyric video generator (templated) | $5/use | no AI |

### Bucket G — UZ local edge (low/no competition)

| # | Idea | Model | Notes |
|---|---|---|---|
| G1 | NT (Sharq Bahori etc.) auction lot tracker | $5/query/mo | your existing personal tool |
| G2 | UZ business registry lookup API | $0.10/query | B2B |
| G3 | UZ mortgage tracker (bank-agnostic) | $3/mo | your own use case |
| G4 | UZ tax calculator (freelancer / employee / IE) | one-shot $5 | SEO long-tail |
| G5 | UZ Telegram channel analytics | $9/mo | content creators |
| G6 | UZ gov form auto-filler | $5/form | citizens / SMB |
| G7 | UZ real-estate market reports (monthly) | $9/mo | RE investors |

---

## Top 15 finalists (scored)

Filter: Tier 0 OR Tier 1-with-passthrough · clear distribution path · GWDNBM-natural · build ≤1 wk · WTP ≥ $5/mo or $9 one-shot.

| Rank | Idea | Bucket | WTP | Build | Marginal | Distribution loop | Score |
|---|---|---|---|---|---|---|---|
| 1 | Privacy policy generator | E1 | $29 one-shot | 1 wk | $0 | SEO long-tail per jurisdiction | ★★★★★ |
| 2 | UZ NT auction tracker | G1 | $5–10/mo | 3–5 d | $0 (already built for personal) | Telegram UZ RE groups | ★★★★★ |
| 3 | Receipt → CSV | B1 | $15/mo | 1 wk | $0.005/req (passthrough) | Accountant subreddits + LinkedIn | ★★★★ |
| 4 | Accessibility audit | E7 | $39 + $19/mo | 1 wk | $0 (axe-core does it) | SEO long-tail ADA + dev tools | ★★★★ |
| 5 | OG image generator (templated) | A12 | $0.10/img or $9/mo | 3–5 d | $0 | Embeddable + dev SEO | ★★★★ |
| 6 | Cron-as-a-service | A1 | $9/mo | 1 wk | $0 | HN, IH, dev SEO | ★★★★ |
| 7 | Webhook debugger / relay | A2 | $9–19/mo | 1 wk | $0 | HN, IH, dev SEO | ★★★★ |
| 8 | License renewal reminder (CME / bar) | D1 | $5/mo | 3–5 d | $0 (cron + email) | Doctor/lawyer FB groups | ★★★★ |
| 9 | SSL + domain expiry monitor | A5 | $3/10 items | 2–3 d | $0 | Dev SEO + bundle w/ Cron | ★★★ |
| 10 | UZ business registry API | G2 | $0.10/query | 1 wk | $0 | UZ dev/SMB channels | ★★★ |
| 11 | Trademark filing watcher | D2 | $10/mo per term | 1 wk | data source TBD | Legal/brand groups | ★★★ |
| 12 | Niche short URL + analytics | A14 | $5/mo | 3 d | $0 | Pick one vertical, dominate | ★★★ |
| 13 | Cookie banner customizer | E3 | $5/mo | 3–5 d | $0 | Embed = SEO + virality | ★★★ |
| 14 | Sitemap → SEO landing-page audit | A23 | $19 one-shot | 1 wk | $0 | SEO meta-play (audit other people's SEO) | ★★★ |
| 15 | Podcast chapter generator | F2 | $9/mo | 5 d | $0.01/episode (passthrough) | Podcaster communities + viral | ★★★ |

---

## Distribution-first picks (built-in growth loops)

Without paid ads, distribution is the bottleneck. Products with native growth loops beat blind launches:

| Loop type | Picks from top 15 | How the loop works |
|---|---|---|
| **Embed = backlinks** | Cookie banner customizer · Status page · OG image API | Customer's site shows "Powered by X" → backlink → SEO + traffic |
| **Shared output** | OG image generator · Privacy policy · Sitemap audit | User gets PDF/image with subtle attribution → recipient sees brand |
| **Programmatic SEO** | Privacy policy (per-jurisdiction landing pages) · Accessibility audit (per-framework landing pages) · OG image (per-template landing pages) | One product → 100+ landing pages targeting long-tail searches |
| **Dev API ecosystem** | Cron · Webhook · OG image · WHOIS · UZ registry | Devs integrate → blog about it → other devs find it |
| **Niche community virality** | UZ NT tracker (Telegram) · CME renewal (doctor FB) · Podcast chapter (podcaster groups) | Tight community → word-of-mouth in 1 thread |
| **Pure SEO long-tail** | "convert X to Y" · "validate X" · "audit X" | Programmatic landing pages compounding over months |

**Pattern**: every product in batch 1 should hit ≥1 loop. Picks without a loop need paid ads, which doesn't fit the budget.

---

## Volume strategy for 20–30 launches

### Phase 0 — Foundation (week 1–2, one-time)

Build the **template repo** once. Every future launch forks it. Estimated 1–2 weeks:

- Auth: passwordless email link (Resend free tier)
- Payments: Stripe Checkout + Customer Portal (one-shot + subscription modes wired)
- UZ-products extension: Click/Payme adapter slot
- Hosting: Hetzner shared box behind Cloudflare; multi-tenant by domain
- Landing page template (1 hero + 1 features + 1 pricing + 1 CTA)
- Docs template (for dev infra products)
- Programmatic SEO generator (for products with many landing pages)
- "Delete my data" page baked in (GWDNBM proof)
- Receipt email template
- Status page

Reuse: wow-two backend SDK packages where they fit (identity, JWT, OTP). UI library `@wow-two-beta/ui` for everything visual.

### Phase 1 — First 5 launches (week 3–7, one per week)

Pick 5 from top 15 with mixed distribution loops:

| Wk | Product | Loop |
|---|---|---|
| 3 | Privacy policy generator | Programmatic SEO + shared output |
| 4 | UZ NT auction tracker | Niche community (Telegram) |
| 5 | OG image generator | Embed backlinks + dev API |
| 6 | Cron-as-a-service | Dev API ecosystem |
| 7 | License renewal reminder (one profession — pick highest-WTP) | Niche community |

Each launch = fork template, swap landing copy, swap core logic, deploy, post to 1 channel.

### Phase 2 — Cadence (week 8–26, one per week ≈ 20 more launches)

Run validation playbook (from market-analysis.md) on remaining top-15 + new candidates from YT audit. Ship one per week. Kill any at 4-week mark with zero revenue.

### Phase 3 — Double down (week 27+)

Whichever 1–5 hit revenue thresholds get focused work; rest stay on autopilot.

---

## "Hit" definition — kill gates

A product is **kept** if it crosses milestones; **killed** if not.

| Gate | Milestone | Action if missed |
|---|---|---|
| **G1** (week 2 post-launch) | 1 paying customer | Pause marketing; if 4 wks no buyer, kill |
| **G2** (month 3) | $100 MRR (or $300 one-shot rev) | Continue but no new effort |
| **G3** (month 6) | $500 MRR (or $1500 cumulative one-shot) | Active product — double down |
| **G4** (month 12) | $2000 MRR or $10K cumulative | "Hit" — graduate to focused product |

Goal: of 25 launches by EOY, 1–5 cross G3 = success.

---

## Updated batch 1 (cost-aware, replaces market-analysis.md picks)

| # | Product | Bucket | Tier | Build | First-rev gate |
|---|---|---|---|---|---|
| 1 | **Privacy policy generator** | E1 | 0 | 1 wk | 4 wks |
| 2 | **UZ NT auction tracker** | G1 | 0 | 3–5 d (mostly built) | 4 wks |
| 3 | **OG image generator (templated)** | A12 | 0 | 3–5 d | 4 wks |
| 4 | **Cron-as-a-service** | A1 | 0 | 1 wk | 4 wks |
| 5 | **Accessibility audit (axe-core wrapper)** | E7 | 0 | 1 wk | 4 wks |

**Changes from prior batch 1:**

| Old pick | Status | Why |
|---|---|---|
| Privacy policy generator | KEEP | Tier 0, high WTP, programmatic SEO |
| UZ NT auction tracker | KEEP | Tier 0, local edge, partially built |
| Receipt → CSV | **MOVED to batch 2** | Tier 1 — pricing must be perfect; do this after a Tier 0 win to fund margin tests |
| Accessibility audit | KEEP | Tier 0 (axe-core free) |
| Subtitle cleaner | **REPLACED with OG image generator + Cron** | Subtitle cleaning needs transcription input ($$); OG image + Cron are pure Tier 0 |

5 Tier-0 picks → marginal cost on user volume = $0 → can run at break-even or free trials safely.

---

## What to actively avoid

- **"AI assistant for X"** without a sharp single job — bleeds money + commoditized by next model release
- **Big-LLM-context products** (legal contract review, long-doc analysis) — costs run away
- **Image generation products** — Midjourney economics
- **Anything requiring paid data licensing** (court records, financial data, MLS) — fixed costs kill margin
- **Social/network products** — bootstrap problem
- **Heavy scraping plays** — Haven lesson, plus proxy costs
- **Marketplaces** — chicken-and-egg + payment splits
- **Anything where the buyer is "students" or "broke creators"** — WTP floor

---

## Open questions (carry-over)

1. **YouTube channel for app mining** — fill `youtube-apps-audit.md` (separate chat)
2. **Single brand vs N brands** — leaning N (each domain independent)
3. **UZ-first vs global-first per product** — case-by-case: products 1, 3, 4, 5 = global; product 2 = UZ-only
4. **Validation playbook (4-step) on each pick before build** — recommended; 1 day per product

---

## User feedback pass — 2026-05-22

User reviewed enriched candidates (info biz + creator tools + entertainment). Decisions:

### Endorsed (good picks)

- **VC deals / acquisitions tracker w/ visual ownership tree** — strong concept, data source is the constraint (Crunchbase $$$, SEC EDGAR free US-only). Defer to phase-2 after first wins.
- **Court case tracker** — keep (US first via CourtListener)
- **Trademark filing watcher** — **LOCKED for batch 1 build** (chat spawned)
- **Patent filing watcher** — keep (same shape as TM)
- **Gov spending tracker (UZ angle)** — keep, local-startup-friendly
- **Domain history (WHOIS + DNS)** — keep, bundle with reverse-IP
- **Reverse IP** — keep, bundle
- **QR code w/ redirect rules** — **LOCKED for batch 1 build** (chat spawned)
- **Code snippet share** — keep but lower priority (saturated by free)

### Killed by user

- **Newsletter / RSS aggregator** — saturated, commodity

### Concerns resolved

- **Flight deal alerts**: no AI needed, polling-only. Real constraint = data source (Skyscanner / Kiwi / Travelpayouts affiliate APIs are gated but free for affiliates → could run free-for-users on affiliate revenue). Tier 0 feasible.
- **Real estate tracking**: no AI for user-submits-URL daily re-fetch model. Tier 0. AI only enters if you want market summaries or similar-listing recs.
- **Tech stack detection**: backend is opaque (~30–50% accuracy via Wappalyzer-style). **Drop or scope to frontend-only.**

### Locked for batch 1 build (chats spawned 2026-05-22)

| Product | Category | Pricing | Chat |
|---|---|---|---|
| **Trademark filing watcher** | Info biz | $10/mo per keyword | Spawned |
| **Smart QR code (redirect rules + analytics)** | Creator tool | $5/mo Solo, $15/mo Pro | Spawned |

Each carries deliverable order: product brief → tech architecture → MVP code → landing copy → distribution plan. No coding before brief sign-off.

### Deferred to backlog

- **SaaS-wish curated directory** ("wish.com for micro SaaS") — user-proposed 2026-05-22. Marketplace shape (contradicts portfolio "no marketplaces" rule). Recommended reframe = curated directory (no UGC at launch; you seed wishes; visitors upvote without login; SEO long-tail landing pages per wish; builders pay $9/mo to claim wishes). Deferred until at least one of TM watcher / Smart QR clears G1 (1 paying customer by wk 4). Has hidden value: doubles as portfolio idea-pipeline + cross-promo hub for other launches.

---

## Related

- [Market analysis](./market-analysis.md) — scoring framework, audience tiers, demand categories
- [YouTube apps audit](./youtube-apps-audit.md) — stub for channel-sourced ideas
- [Telegram features](./telegram-features.md)
- [Transcript Forge spec](./transcript-forge-spec.md)
- [Transcript Forge backend libs spec](./transcript-forge-backend-libs-spec.md)

# Own ideas review: the founder's product ideas scored like the 100 researched SaaS products

*Last updated: 2026-10-09*

**Method and scope.** This applies the [research protocol](../saas-research-2026-10/research-protocol.md) (8 dimensions 1-5, weights pain 20, recurrence 15, budget 15, distribution 15, wedge 15, feasibility 10, global 5, cost 5; challenge penalty 0-20; final = base - penalty) to **89 own ideas**, so they can be read against [ranked-100](../saas-research-2026-10/ranked-100.md) and the [subscription-speed](../saas-research-2026-10/subscription-speed.md) lens. Sources: product-idea docs in `ideas/`, the judged picks in `workbench/ventures/10x-ventures/products-final.md` (Tier A, Tier B upper and the portfolio anchors), the top 15 and batch 1 of `micro-saas-deep-search.md`, and the root `CLAUDE.md` / `product/` files of every repo under `workbench/ventures/`. Existing code earns no score bonus; it appears in the "built state" column and the speed tier. ForeverPin, Pose Coach, Transcript Forge and Hijinx are scored only as calibration rows ("in order"); the [venture order](../../system/planning/pln-tasks.md#venture-product-order) is untouched. Prices are analyst hypotheses unless a source doc states them; competitor prices were observed on official pages on 2026-10-09 (evidence table). Single analyst pass: no independent challenge round, so penalties are self-applied (mean 10.5 here vs 5.9 in the research) and differences under 5 points are not meaningful. Payment rails follow [parent-company](../parent-company-2026-10/parent-company-2026-10.md): global products bill through Stripe via the planned US LLC (not yet formed), Uzbekistan-local products would use Click/Payme through a Uzbek IE/LLC, iOS digital goods go through the App Store.

## Decision summary

- **No own idea reaches the research Validate band.** The research Validate set scores 66-76; the best own ideas score 61 (O71 grant pipeline), 60 (O05 UZ geocoder) and 59 (O01 ForeverPin, in order). None scores 70 or more. Only 21 of 89 reach 50, against 91 of 100 researched products; median final is 45 against 60.5.
- **Why they trail.** The own set is mostly consumer, one-off or single-role: 21 rows sell one-off, 8 have no payer, and 38 of 71 priced rows cost $19 or less. Mean penalty is 10.5 against 5.9 in the research. Price is the sharpest gap: median accounts for $5K MRR is 264 against 34, and only 3 own ideas price at $99 or more.
- **The ordered four on the same scale.** ForeverPin 59 (method status Reserve) is the only one near the research Reserve line; Transcript Forge 53, Hijinx 45, Pose Coach 39. The three consumer/entertainment products need 173-835 accounts and lack the multi-role record the protocol rewards. The order was chosen for speed to MRR, not score; the speed lens supports that for ForeverPin only.
- **Fastest to a subscription:** ForeverPin (2-4 builder-weeks, already ordered). Next are thin developer utilities, cron-as-a-service, webhook relay and accessibility audit (2-4 weeks, finals 50-52, price $9-19, free or cheap incumbents in the evidence table), then the built first-ten prototypes at 3-6 weeks: Training Seats 58, File Watch 56, Podcast Readiness 55, Retainer Balance 55. The prototypes are single-user workspaces and need team access, sponsor/guest sign-in and billing before they can be charged.
- **Best candidates to carry forward as Reserve:** O71 grant pipeline, O05 UZ geocoder, O83 Training Seats, O68 vault.guardian, O88 Podcast Readiness, O79 Retainer Balance. None is a stronger version of a researched product; P111, Procedure Review, Customer Promises and the newsletter storefront are narrower, cheaper cuts of S086, S080, S083/S084 and S039, while Training Seats and Podcast Readiness are sharper but smaller slices into S026/S029 and S042 (cross-check below).
- **Uzbekistan-local:** 14 ideas, best is the geocoder (60); the rest score 49 or lower (Haven, gated, 49). All 12 UZ-rail rows wait for a Uzbek IE/LLC and Click/Payme; the 67 rows billed through Stripe (one also via the App Store) wait for the US LLC, whose formation is itself gated by three written answers.
- **Cost envelope.** The AI-per-document decoders (manuscript, illustrator, bid referee, medical bill, HOA/IEP), Gaussian-splat and image-generation ideas break the $20-50 pilot cost or need pass-through pricing; those rows finish at 36-47 after penalties.
- **23 ideas score Drop** (final below 40 or a broken founder constraint: physical fulfilment, licence breach, marketplace, no payer), including Arcade (39), Museums Gallery (32), Whiteout (29) and the Spotify-dependent music apps.

## Ranked table (all 89 scored ideas)

Spd = speed tier to a chargeable subscription or paid product (1 = at most 4 builder-weeks, 2 = at most 8, 3 = at most 12, 4 = at most 18, 5 = more, or blocked by an external gate or missing payer; upper bound of the estimate decides). Accts $5K = ceil(5000 / price), before churn, fees and discounts; one-off rows show sales per month instead. `[UZ]` = Uzbekistan-local. Ties broken by distribution, wedge, ID.

| # | ID | Idea | Source(s) | Built state | Final | Spd | Price hypothesis | Accts $5K | Rail | Status |
|--:|---|---|---|---|--:|:-:|---|--:|---|---|
| 1 | O71 | Small-nonprofit grant pipeline (P111) | products-final Tier B (66); P111 | Not built | 61 | 3 | H $49/mo | 103 | Stripe | Reserve |
| 2 | O05 | [UZ] geocoder / address normalisation API | uz-geocoder-spec; cadastre-agency-analysis; uz-govtech-demand-map (P1) | Spec only; nothing built | 60 | 4 | $99/mo Startup (50k req); Business ~$499 (H) | 51 | Click/Payme (UZ) | Reserve |
| 3 | O01 | ForeverPin (programmable QR + link router) | forever-pin-spec; 10x-venture-forever-pin; micro-saas A13/A14 | Built: codes, redirects, exports, analytics, Stripe code; pre-launch | 59 | 1 | $15/mo Pro (tiers $5/$15/$39) | 334 | Stripe | in order (method: Reserve) |
| 4 | O83 | Training Seats (first-ten, W0289) | ventures.training-seats | Built: local v0.1 (agreements, reservation, substitution, statements) | 58 | 2 | $59/mo/provider | 85 | Stripe | Reserve |
| 5 | O68 | vault.guardian (Notion backup + version history) | 10x-ventures/specs/vault.md; products-final on-deck | Spec only; parked at validation gate | 57 | 3 | H $9/mo (rivals $6-89) | 556 | Stripe | Reserve |
| 6 | O81 | File Watch (first-ten, W0031) | ventures.file-watch | Built: local v0.1 collector + exceptions | 56 | 2 | $39/mo | 129 | Stripe | Defer |
| 7 | O88 | Podcast Readiness (first-ten, W0507) | ventures.podcast-readiness | Built: local v0.1 (guest packets, readiness) | 55 | 2 | $29/mo | 173 | Stripe | Reserve |
| 8 | O79 | Retainer Balance (first-ten, W0252) | ventures.retainer-balance; startup-research-2026-09 | Built: local v0.1 (CSV import to statement); personal workspace only | 55 | 2 | $39/mo/company | 129 | Stripe | Reserve |
| 9 | O65 | Golf society engine | products-final Tier B (68); P120 | Not built | 54 | 3 | H $19/mo | 264 | Stripe | Defer |
| 10 | O52 | KDP ads ROI tracker (royalty-aware ACOS) | products-final Tier B (70); P135 | Not built | 54 | 2 | H $15/mo | 334 | Stripe | Defer |
| 11 | O03 | Transcript Forge (creator repurposing suite) | transcript-forge-spec; transcript-forge-backend-libs-spec; 10x-ventures-transcript-forge | Built: local engine, projects, jobs, search, exports, API keys, MCP; Release 1 open | 53 | 3 | $29-39/mo (use $29) | 173 | Stripe | in order (method: Defer) |
| 12 | O85 | Customer Promises (first-ten, W0276) | ventures.customer-promises | Built: local v0.1 (ledger, digest) | 53 | 2 | $59/mo | 85 | Stripe | Defer |
| 13 | O33 | Cron-as-a-service | micro-saas-deep-search (A1) | Not built | 52 | 1 | $9/mo | 556 | Stripe | Defer |
| 14 | O43 | PDF tool suite (Bates stamp, redact, title page, watermark) | pdf-editor; micro-saas family | Built: 12-project PDF engine POC + test API; SDK media tools extracted | 51 | 2 | $19/mo (H) | 264 | Stripe | Defer |
| 15 | O34 | Webhook debugger / relay | micro-saas-deep-search (A2) | Not built | 51 | 1 | $9-19/mo | 334 | Stripe | Defer |
| 16 | O50 | Faraid (Islamic inheritance) calculator | products-final Tier B (70); P056 | Not built | 50 | 2 | $29 per estate (H) | n/a (173 sales/mo) | Stripe | Defer |
| 17 | O48 | Non-US FIRE planner | products-final Tier B (70); P015 | Not built | 50 | 3 | $9/mo (H) | 556 | Stripe | Defer |
| 18 | O31 | Accessibility audit (axe-core wrapper) | micro-saas-deep-search (E7) | Not built | 50 | 1 | $39 + $19/mo | 264 | Stripe | Defer |
| 19 | O86 | Vendor Renewals (first-ten, W0261) | ventures.vendor-renewals | Built: local v0.1 | 50 | 2 | $29/mo/team | 173 | Stripe | Defer |
| 20 | O72 | Newsletter sponsor storefront (P088) | products-final Tier B (65); P088 | Not built | 50 | 3 | H $39/mo | 129 | Stripe | Defer |
| 21 | O82 | Procedure Review (first-ten, W0263) | ventures.procedure-review | Built: local v0.1 | 50 | 2 | $29/mo/team | 173 | Stripe | Defer |
| 22 | O89 | [UZ] Haven (Tashkent real-estate platform) | 10x-ven-haven; product.md; reference notes | Built: supply pipeline, CRM, channels, map (v0.9+); paused; gated | 49 | 3 | H realtor subscription $49 | 103 | Click/Payme (UZ) | gated (method: Defer) |
| 23 | O26 | AI menu translator for restaurants | passive-income-automation-spec (M1) | Spec only | 49 | 2 | $20-50/restaurant/mo (spec); use $29 | 173 | Stripe | Defer |
| 24 | O16 | Gaussian splats: annotation and collaboration tool | gaussian-splatting-spec (#2) | Spec only | 49 | 3 | $20-50/team/mo (spec); use $39 | 129 | Stripe | Defer |
| 25 | O38 | Trademark filing watcher (US/EU) | micro-saas-deep-search (D2, locked batch 1); trademark-watcher-poc | Built: USPTO/EUIPO clients, matching, tests (POC); idle | 49 | 3 | $10/mo per keyword | 500 | Stripe | Defer |
| 26 | O56 | LEGO collection value tracker | products-final Tier B (69); app:lego-tracker | Not built | 48 | 2 | H $5/mo | 1000 | Stripe | Defer |
| 27 | O77 | PRISM (parametric renovation modeler) | 10x-ventures-prism; ventures.home-renovation (empty) | Built: v0.15 shipped, engine rewrite in progress; client-side | 48 | 3 | H $12/mo | 417 | Stripe | Defer |
| 28 | O45 | Parent IEP command center | products-final Tier A (72); P025 | Not built | 47 | 3 | $15-29/mo (use $19) | 264 | Stripe | Defer |
| 29 | O53 | Decodable-text generator | products-final Tier B (69); P034 | Not built | 47 | 3 | H $9/mo | 556 | Stripe | Defer |
| 30 | O44 | Paint-by-numbers + diamond-painting kit generator | products-final Tier A (73/72); ventures.pbn-studio | Built: client-side v0.1 engine + studio; never browser-checked | 47 | 2 | Per-kit; seller plan $19/mo (H) | 264 | Stripe | Defer |
| 31 | O69 | Kids-curiosity chapters (P140) | products-final anchor; P140 | Banked; self-scored 18 | 47 | 3 | H $9/mo | 556 | Stripe | Defer |
| 32 | O30 | Receipt-to-CSV | micro-saas-deep-search (B1) | Not built | 47 | 2 | $15/mo or $0.20/doc | 334 | Stripe | Defer |
| 33 | O20 | Gaussian splats: construction progress tracker | gaussian-splatting-spec (#6) | Spec only | 47 | 5 | $200-500/site/mo (spec); use $299 | 17 | Stripe | Defer |
| 34 | O87 | Config Checker (first-ten, W0034) | ventures.config-checker | Built: local v0.1 (HMAC manifests) | 47 | 2 | $39/mo | 129 | Stripe | Defer |
| 35 | O35 | License-renewal reminder (CME/bar) | micro-saas-deep-search (D1) | Not built | 46 | 1 | $5/mo | 1000 | Stripe | Defer |
| 36 | O58 | Digital-planner generator | products-final Tier B (68); P040 | Not built | 46 | 2 | H $9/yr rebuy | n/a (556 sales/mo) | Stripe | Defer |
| 37 | O80 | Documentation Checker (first-ten, W0012) | ventures.documentation-checker | Built: local v0.1; JS syntax only | 46 | 2 | $39/mo | 129 | Stripe | Defer |
| 38 | O06 | [UZ] rejection pre-check (tax/VAT refund, social, cadastre) | uz-govtech-demand-map (P6, 4.5) | Research only | 46 | 4 | $59/mo (H) | 85 | Click/Payme (UZ) | Defer |
| 39 | O37 | [UZ] business-registry lookup API | micro-saas-deep-search (G2) | Not built | 46 | 2 | $0.10/query (H sub $20) | 250 | Click/Payme (UZ) | Defer |
| 40 | O84 | EPUB Review (first-ten, W0521) | ventures.epub-review | Built: local v0.1 (Ace import + checks) | 46 | 2 | $39/mo | 129 | Stripe | Defer |
| 41 | O51 | Picture-book illustrator for KDP authors | products-final Tier B (70); P066 | Not built | 45 | 4 | H $29/book | n/a (173 sales/mo) | Stripe | Defer |
| 42 | O66 | Milestone-event command center | products-final Tier B (68); P123 | Not built | 45 | 3 | H $29/event | n/a (173 sales/mo) | Stripe | Defer |
| 43 | O04 | Hijinx (party-game PWA + packs; fun-vault content) | ventures.hijinx; ventures.fun-vault | Built: web/PWA/iOS shell, 49 free packs, 15 locales; nothing in a store | 45 | 2 | Packs $5-9 / bundles $15-25 one-off; host plan $19-29/mo (untested; use $29) | 173 | Stripe + App Store | in order (method: Defer) |
| 44 | O63 | Lawn quote from satellite | products-final Tier B (68); P099 | Not built | 45 | 4 | H $99/mo | 51 | Stripe | Defer |
| 45 | O67 | String-art generator (locked engine proof) | products-final Tier B (65, locked) | Locked; judged standalone only | 45 | 2 | per-gen (H) | n/a (556 sales/mo) | Stripe | Defer |
| 46 | O32 | OG-image generator (templated) | micro-saas-deep-search (A12) | Not built | 45 | 1 | $9/mo or $0.10/img | 556 | Stripe | Defer |
| 47 | O59 | Executor's companion | products-final Tier B (68); P061 | Not built | 44 | 3 | H $29 | n/a (173 sales/mo) | Stripe | Defer |
| 48 | O29 | [UZ] NT auction-lot tracker | micro-saas-deep-search (G1); 10x-fin-nt | Built: scraper pipeline + lots data; dormant personal tool | 44 | 1 | $5-10/query/mo (H $7) | 715 | Click/Payme (UZ) | Defer |
| 49 | O49 | Custody evidence binder | products-final Tier B (70); P024 | Not built | 44 | 3 | H $19/mo | 264 | Stripe | Defer |
| 50 | O74 | sift (curated YouTube feed with density ranking) | sift | Built: v0.1 shell + v0.2 ingest on fixtures; no live API key | 44 | 3 | H $5/mo | 1000 | Stripe | Defer |
| 51 | O36 | SSL and domain-expiry monitor | micro-saas-deep-search (A5) | Not built | 43 | 1 | $3 per 10 items | 1667 | Stripe | Defer |
| 52 | O07 | [UZ] emission-telemetry integration adapters | uz-govtech-demand-map (4.3) | Research only | 43 | 5 | Per-site integration fee (H) | n/a | Click/Payme (UZ) | Defer |
| 53 | O64 | Hunt club and lease command center | products-final Tier B (68); P113 | Not built | 43 | 3 | H $10/mo (CampKeeper sells $119.99/yr per club) | 500 | Stripe | Defer |
| 54 | O47 | Bank-statement to categorised CSV | products-final Tier B (71); BF-12 | Not built | 43 | 2 | Metered $0.50/page or $19/mo | 264 | Stripe | Defer |
| 55 | O28 | Privacy-policy generator | micro-saas-deep-search (E1, rank 1) | Not built | 42 | 1 | $29 one-shot | n/a (173 sales/mo) | Stripe | Defer |
| 56 | O61 | Medical-bill auditor | products-final Tier B (68); P079 | Not built | 42 | 3 | H $29/bill | n/a (173 sales/mo) | Stripe | Defer |
| 57 | O41 | Podcast chapter generator | micro-saas-deep-search (F2) | Not built | 42 | 2 | $9/mo | 556 | Stripe | Defer |
| 58 | O08 | [UZ] registry crosswalk / address-to-mahalla resolver | uz-govtech-demand-map (P3, 4.4) | Research only | 42 | 5 | Subcontract / contract fee | n/a | Click/Payme (UZ) | Defer |
| 59 | O19 | Gaussian splats: Shopify 3D product viewer | gaussian-splatting-spec (#5) | Spec only | 41 | 4 | $10-30/mo (spec); use $19 | 264 | Stripe | Defer |
| 60 | O46 | HOA resale-package X-ray | products-final Tier A (72); P076 | Not built | 41 | 3 | Per-report; agent tier $49/mo (H) | n/a (103 sales/mo) | Stripe | Defer |
| 61 | O73 | [UZ] ListingShelf (OLX/Domtut listing archive) | ventures.listing-shelf | Built: OLX + Domtut capture, archive, JSON export, schedules; verified on live pages | 41 | 2 | H $15/mo | 334 | Click/Payme (UZ) | Defer |
| 62 | O24 | AI garden/landscape visualizer | passive-income-automation-spec (S1) | Spec only | 40 | 4 | $9.99-29.99/mo (spec); use $19 | 264 | Stripe | Defer |
| 63 | O57 | Divorce financial-disclosure organizer | products-final Tier B (68); P030 | Not built | 40 | 4 | H $29/mo | 173 | Stripe | Defer |
| 64 | O60 | Contractor bid referee | products-final Tier B (68); P078 | Not built | 40 | 2 | H $19/project | n/a (264 sales/mo) | Stripe | Defer |
| 65 | O42 | Ownership-graph / acquisitions tracker | micro-saas-deep-search (user-endorsed); acquisition-explorer-poc | Built: graph components (frontend POC); no data | 40 | 4 | $29-99/mo (H $49) | 103 | Stripe | Defer |
| 66 | O55 | Home-inspection report triage | products-final Tier B (69); P077 | Not built | 39 | 3 | Per-report / agent tier (H) | n/a (103 sales/mo) | Stripe | Drop |
| 67 | O62 | Manuscript X-ray | products-final Tier B (68); P085 | Not built | 39 | 3 | H $29/manuscript | n/a (173 sales/mo) | Stripe | Drop |
| 68 | O75 | Arcade (Telegram Mini-App games) | ventures.arcade; specs/arcade.md | Built: 15 games in launcher, en/uz/ru; 0 commits, no remote | 39 | 1 | Cosmetic micro-purchases | n/a | Telegram Stars | Drop |
| 69 | O02 | Pose Coach (duo photo director, iPhone) | pose-coach-spec; ai-photo-director-market-analysis; ventures.pose-coach | Built: duo-collage flow + live coach; simulator-verified, no device test, no products | 39 | 2 | $5.99/mo or $39.99/yr (tests) | 835 | App Store | in order (method: Defer) |
| 70 | O09 | [UZ] B2G packages: field-capture, municipal GIS, master-plan vectorisation | uz-govtech-demand-map (P7, P4, 4.1, 4.2); cadastre-agency-analysis | Research only | 39 | 5 | Project contracts ($0.5-27M packages named) | n/a | other | Drop |
| 71 | O15 | Gaussian splats: real-estate splat-as-a-service API | gaussian-splatting-spec (#1) | Spec only | 38 | 4 | $5-15/scan (spec); sub H $29 | 500 | Stripe | Drop |
| 72 | O39 | Cookie-banner customiser | micro-saas-deep-search (E3) | Not built | 36 | 1 | $5/mo | 1000 | Stripe | Drop |
| 73 | O54 | Cake concept studio | products-final Tier B (69); P069 | Not built | 36 | 4 | H $19/mo | 264 | Stripe | Drop |
| 74 | O11 | [UZ] Activity Matcher (Tashkent, time-aware) | activity-matcher-spec | Spec only; 150-row catalogue exists | 36 | 5 | None defined | n/a | Click/Payme (UZ) | Drop |
| 75 | O40 | Sitemap-to-SEO landing-page audit | micro-saas-deep-search (A23) | Not built | 35 | 1 | $19 one-shot | n/a (264 sales/mo) | Stripe | Drop |
| 76 | O70 | Survey / quiz-storage engine (enabler) | products-final anchor; OS-08 | Legacy id | 34 | 5 | none | n/a | Stripe | Drop |
| 77 | O27 | [UZ] 3D-print physical products (gearbox demonstrators etc.) | 3d-print-products-analysis | Paused; nothing built | 33 | 5 | $45-500/unit | n/a | Click/Payme (UZ) | Drop |
| 78 | O12 | Route Vibe Player (route-scored music) | route-vibe-player-spec | Spec only | 32 | 5 | $5/mo (H) | 1000 | App Store | Drop |
| 79 | O76 | [UZ] Museums Gallery (UZ) | ventures.museums-gallery | Built: frontend v1.1 on 58-museum seed; data unverified | 32 | 5 | None defined | n/a | Click/Payme (UZ) | Drop |
| 80 | O13 | Spotify Mood Queue | spotify-mood-queue-project | Spec only | 31 | 5 | None defined | n/a | App Store | Drop |
| 81 | O23 | Ambient content channels (ADHD music, cat/baby/senior calm) | passive-income-automation-spec (P1-P4) | Spec only | 31 | 5 | AdSense/Spotify | n/a | other | Drop |
| 82 | O22 | Air-pollutant timeline map | air-pollutant-timeline-map-research | Research only | 31 | 5 | None defined | n/a | other | Drop |
| 83 | O17 | Gaussian splats: asset marketplace | gaussian-splatting-spec (#3) | Spec only | 30 | 5 | 15-30% commission | n/a | Stripe | Drop |
| 84 | O18 | [UZ] Gaussian splats: Central Asia heritage scanner | gaussian-splatting-spec (#4) | Spec only | 29 | 5 | Project fees | n/a | other | Drop |
| 85 | O25 | AI cultural-dress virtual try-on | passive-income-automation-spec (S2) | Spec only | 29 | 5 | Per-render (H) | n/a | Stripe | Drop |
| 86 | O78 | Whiteout (WebGPU sniper FPS) + presets library | whiteout; 10x-venture-whiteout-presets | Built: engine + game v0.5, material lab; asset presets | 29 | 5 | Premium/one-off (H) | n/a | Stripe | Drop |
| 87 | O10 | [UZ] valuation appeal / AVM / property due diligence | cadastre-agency-analysis; uz-govtech-demand-map (P5) | Research only | 27 | 5 | Per-report (H) | n/a | Click/Payme (UZ) | Drop |
| 88 | O14 | Icon scraper (DX tool) | icon-scraper-spec | Spec only | 27 | 5 | None | n/a | other | Drop |
| 89 | O21 | Gaussian splats: moonshots (4D event capture, game level editor) | gaussian-splatting-spec (#7, #8) | Spec only | 17 | 5 | None | n/a | other | Drop |

**Status rules (mine, mirroring the research):** Validate = final 66 or more and passes the qualification gate (persistent record, 3+ connected stages, 2+ roles); none qualify. Reserve = final 55 or more and passes the gate. Defer = final 40-54, or fails the gate or a cost/feasibility limit. Drop = final below 40, or breaks a founder constraint (physical fulfilment, licence breach, marketplace, no payer). "In order" rows show what the method would say in brackets; the order itself is not re-ranked.

## Per-idea notes (top 15 by final score)

**1. O71 Small-nonprofit grant pipeline (P111), final 61, Reserve**
- Source: products-final Tier B (66). Grant list + org profile to LOI, application, award and report deadlines; $49/mo hypothesis, 103 accounts for $5K.
- It is the lighter, cheaper twin of researched S086 (72, $129): same buyer and record, but without S086's post-award wedge, plus an AI-drafting add-on that breaks the cost envelope. Treat it as input to the S086 test, not a separate bet.
- Evidence: Instrumentl $299-$999/mo, Grantseeker $19.99-$51.99/mo, so $49 lands in Grantseeker's prospecting band. 8-12 builder-weeks.

**2. O05 [UZ] UZ geocoder, final 60, Reserve**
- Source: uz-geocoder-spec, cadastre-agency-analysis, uz-govtech-demand-map (P1). Fills a real gap (no national geocoder; five address spellings); usage-priced API. $99/mo for 50k requests is about $2 per 1,000 against Google's $5.00 per 1,000 (10,000 free per month) and Yandex's $2,000+/yr minimums.
- Ceiling is local: global = 1, the state address register is funded for ~2030, World Bank address packages (~$1.8M) are already under procurement, the cadastral data licence is unresolved, and no competitor was tested on Uzbek addresses. The demand map itself demoted it from #1 to #3 (an engine inside a registry crosswalk).
- Gates from the spec: 85% house-level accuracy on a Tashkent gold set, 60% on a regional one. Needs a Uzbek entity and Click/Payme; can be tested earlier without either.

**3. O01 ForeverPin (in order, method: Reserve), final 59**
- Highest-scoring ordered product and the fastest to a subscription (2-4 weeks). Persistent redirect record plus analytics gives recurrence 4; the $5-15 price holds budget at 2 and needs 334 accounts at $15.
- Penalty 8: crowded commodity, solo buyer, and a source-inspection finding that a canceled subscription can keep paid creation capacity. Evidence: Uniqode $9/$49 per month (annual-only) and QR Tiger $7/$16/$37; Uniqode states dynamic codes become inactive on cancellation, which supports the never-expire position, a pricing stance rather than a workflow moat.
- Blockers: entitlement fix, live Stripe/OAuth verification, US LLC for Stripe.

**4. O83 Training Seats (first-ten W0289), final 58, Reserve**
- Built local v0.1: sponsor agreement, capacity-safe reservation and substitution, attendance, sponsor statement. The rule "purchased - reserved - attended = available" is concrete and testable; $59/mo/provider, 85 accounts.
- Related to researched S026 (67) and S029 (70, Validate). Arlo charges $118-$132 per administrator plus per-registration fees; none of the pages opened shows seat substitution or sponsor statements. The prototype is a single-user workspace with no sponsor sign-in.
- 3-6 weeks to charge once teams, sponsor access and billing exist.

**5. O68 vault.guardian (Notion backup), final 57, Reserve**
- Source: vault spec. Data-loss pain is recurring (scheduled backups, history). Evidence: ProBackup $25-$86/mo, Notion Backups $6-$89/mo, Rewind on a waitlist; the $9/mo hypothesis sits at the low end, 556 accounts.
- The stated wedge, lossless restore into vault's own format, needs `vault.desk`, which is unbuilt; Notion Backups itself says a complete restore into Notion is impossible because of API limits. Standalone, it competes on price.
- 8-12 weeks; Notion API fidelity is the technical risk.

**6. O81 File Watch (first-ten W0031), final 56, Defer**
- Highest recurrence among the prototypes (daily expected arrivals, collector health, exceptions). $39/mo, 129 accounts.
- Monitor shape: Healthchecks.io ($5-$80/mo) and Cronitor ($2 per monitor + $5 per user) substitute, and the roles are thin (ops owner plus a partner whose files are only observed). Fails the gate, hence Defer.
- 3-6 weeks: teams, notification delivery, billing.

**7. O88 Podcast Readiness (first-ten W0507), final 55, Reserve**
- Producer and guest roles, expiring scoped guest links, readiness derived from four requirements, reminder drafts; $29/mo, 173 accounts.
- No direct competitor with a public price was found; scheduling tools (Calendly $10-$16/seat, Acuity $16-$49) and PodMatch's release form are partial substitutes. A narrow slice of researched S042 (69, $129); the low price is a bigger problem than the workflow.
- 3-6 weeks: email sending, calendar, billing.

**8. O79 Retainer Balance (first-ten W0252), final 55, Reserve**
- CSV time import, reconciliation, approved extra allowance with external evidence, immutable statements; $39/mo/company, 129 accounts. Clear budget owner (agency principal), repeated monthly.
- Harvest ($9-$14/seat) does not mention retainers on its pricing page; Productive lists recurring retainer budgets from its Professional plan. The wedge is the evidence-backed statement. Single personal workspace today.

**9. O65 Golf society engine (P120), final 54, Defer**
- Multi-role seasonal ledger (secretary, members, money) with World Handicap System rules; $19/mo, 264 accounts.
- Golfify sells organiser plans at $48-$549/yr and Golf Genius is contact-sales; secretary turnover and low budgets.

**10. O52 KDP ads ROI tracker (P135), final 54, Defer**
- Monthly-use tracker for self-publishers; $15/mo, 334 accounts. Single-role record, so it fails the 2-role gate.
- Evidence cut the wedge: ScribeCount ($5.99-$34.99/mo) already lists ad spend vs royalty comparison and ROI calculators; Book Report ($19-$99/mo) has an Ads feature. Amazon data access is the other risk.

**11. O03 Transcript Forge (in order, method: Defer), final 53**
- Weekly-use story for creators, but transcripts are commodity and the layers above are crowded: Descript $16-$65/person/mo, Castmagic $19-$139/mo (annual), Opus Clip $15-$29/mo. Hosted STT and LLM cost break the $20-50 envelope unless priced as pass-through.
- 6-10 weeks after local Release 1; multi-tenant isolation first. 173 accounts at $29.

**12. O85 Customer Promises (first-ten W0276), final 53, Defer**
- Commitment ledger with owner confirmation and approved account digests; $59/mo, 85 accounts. A fragment of researched S083/S084 (73 and 72); no client sign-in, so "confirmation" is operator-entered.
- Rocketlane charges $49-$69 per member (minimum 5) and Dock $350/mo for five seats.

**13. O33 Cron-as-a-service, final 52, Defer**
- Highly recurring (every job is a standing record), $9/mo, 556 accounts, 2-4 weeks. Free cron-job.org (donations) and EasyCron at $24-$240/yr, plus Cronitor monitoring, leave no wedge; reliability expectations are high for a $9 product.

**14. O43 PDF tool suite (pdf-editor), final 51, Defer**
- 12-project PDF engine POC (Bates, redaction, watermark, title page, merge) and SDK media tools exist; $19/mo hypothesis, 264 accounts. Cost is CPU only.
- iLovePDF Premium is $4-$7/mo, PDF24 is free and Acrobat Pro $19.99+; Bates numbering is the one gap the pages did not list. Works only as one buyer (litigation support) with one workflow.

**15. O34 Webhook debugger/relay, final 51, Defer**
- $15/mo, 334 accounts, 2-4 weeks. Hookdeck (free tier; Team from $39/mo) and Webhook.site ($9-$69/mo) cover it; differentiation is price only.

**Calibration rows outside the top 15**
- **O04 Hijinx** (#43, 45): pack sales are one-off and the host subscription needs a repeat-use workflow that does not exist yet; cheap to run (static delivery, 15 locales built), so the risk is demand, not cost. Needs 173 hosts at $29/mo for $5K.
- **O02 Pose Coach** (#69, 39): scores low on pain, recurrence and budget (consumer, occasional use, rivals at $4.99/wk to $9.99/mo already listed in the October 5 assessment); on-device processing keeps cost at 5. Needs 835 subscribers at $5.99/mo.

**Remaining ideas, one line each**

- **O50** Faraid (Islamic inheritance) calculator (#16, 50, Defer): Real wedge in correct math, but calculators are free and paid Islamic wills sell once at $89-$199.
- **O48** Non-US FIRE planner (#17, 50, Defer): Consumer planner; ProjectionLab lists international planning ($129/yr) and a free UK planner exists.
- **O31** Accessibility audit (axe-core wrapper) (#18, 50, Defer): Easy build, no wedge: free axe extension, Pope Tech from $25/mo, WAVE API credits.
- **O86** Vendor Renewals (first-ten, W0261) (#19, 50, Defer): A renewal calendar with a record; Cledara bundles renewal alerts from GBP 100/mo.
- **O72** Newsletter sponsor storefront (P088) (#20, 50, Defer): Weaker than researched S039; Passionfroot's creator side is free and Letterhead covers inventory.
- **O82** Procedure Review (first-ten, W0263) (#21, 50, Defer): Narrow slice of S080; SweetProcess lists $82.50/mo for 10 members, Process Street is contact-sales.
- **O89** [UZ] Haven (Tashkent real-estate platform) (#22, 49, gated): Scored for comparison only; gated by the founder.
- **O26** AI menu translator for restaurants (#23, 49, Defer): Cheap to build, thin wedge.
- **O16** Gaussian splats: annotation and collaboration tool (#24, 49, Defer): Only splat idea with a team record, but capture apps already bundle team seats and comments at $20-$33/user/mo.
- **O38** Trademark filing watcher (US/EU) (#25, 49, Defer): Real recurring pain, thin wedge.
- **O56** LEGO collection value tracker (#26, 48, Defer): Low budget collector niche.
- **O77** PRISM (parametric renovation modeler) (#27, 48, Defer): Deep tool built around the founder's own renovation.
- **O45** Parent IEP command center (#28, 47, Defer): Real parent pain, US-only legal surface.
- **O53** Decodable-text generator (#29, 47, Defer): Niche educational generator.
- **O44** Paint-by-numbers + diamond-painting kit generator (#30, 47, Defer): Cheapest-to-run own idea, but free generators already cover the digital output; paid offers online are physical kits.
- **O69** Kids-curiosity chapters (P140) (#31, 47, Defer): Consumer subscription with LLM cost.
- **O30** Receipt-to-CSV (#32, 47, Defer): Cost-passthrough utility.
- **O20** Gaussian splats: construction progress tracker (#33, 47, Defer): Strong budget owner but infeasible for a small team.
- **O87** Config Checker (first-ten, W0034) (#34, 47, Defer): Interesting privacy model, narrow job.
- **O35** License-renewal reminder (CME/bar) (#35, 46, Defer): A reminder is a feature, not a product.
- **O58** Digital-planner generator (#36, 46, Defer): Annual rebuy, not MRR.
- **O80** Documentation Checker (first-ten, W0012) (#37, 46, Defer): A checker needs a bigger record to be a product.
- **O06** [UZ] rejection pre-check (tax/VAT refund, social, cadastre) (#38, 46, Defer): Tender-free buyers and recurring filings, but unverified demand and heavy rule upkeep.
- **O37** [UZ] business-registry lookup API (#39, 46, Defer): Narrow UZ data API.
- **O84** EPUB Review (first-ten, W0521) (#40, 46, Defer): Niche with a compliance tailwind (unverified).
- **O51** Picture-book illustrator for KDP authors (#41, 45, Defer): Cost model fails the envelope.
- **O66** Milestone-event command center (#42, 45, Defer): Episodic.
- **O04** Hijinx (party-game PWA + packs; fun-vault content) (#43, 45, in order): Cheap to run; revenue shape is packs first, subscription only if repeat-host workflow proves out.
- **O63** Lawn quote from satellite (#44, 45, Defer): Imagery cost.
- **O67** String-art generator (locked engine proof) (#45, 45, Defer): Engine sibling of the kit generator.
- **O32** OG-image generator (templated) (#46, 45, Defer): A feature.
- **O59** Executor's companion (#47, 44, Defer): One-shot.
- **O29** [UZ] NT auction-lot tracker (#48, 44, Defer): Useful personal tool; MRR ceiling tiny.
- **O49** Custody evidence binder (#49, 44, Defer): Painful, sensitive, US-specific.
- **O74** sift (curated YouTube feed with density ranking) (#50, 44, Defer): Personal-first anti-engagement feed.
- **O36** SSL and domain-expiry monitor (#51, 43, Defer): Free-tier territory.
- **O07** [UZ] emission-telemetry integration adapters (#52, 43, Defer): Penalty-priced buyers are real, but it sells as projects.
- **O64** Hunt club and lease command center (#53, 43, Defer): Real club record, but an App Store competitor already sells the same feature set per club.
- **O47** Bank-statement to categorised CSV (#54, 43, Defer): Metered utility.
- **O28** Privacy-policy generator (#55, 42, Defer): Fast to ship, never reaches MRR.
- **O61** Medical-bill auditor (#56, 42, Defer): Crowding fast.
- **O41** Podcast chapter generator (#57, 42, Defer): A feature of hosts.
- **O08** [UZ] registry crosswalk / address-to-mahalla resolver (#58, 42, Defer): Largest stated demand in the map, but not a subscription product.
- **O19** Gaussian splats: Shopify 3D product viewer (#59, 41, Defer): Weak quality and cost fit.
- **O46** HOA resale-package X-ray (#60, 41, Defer): Whitespace wedge, no recurrence.
- **O73** [UZ] ListingShelf (OLX/Domtut listing archive) (#61, 41, Defer): Feeds Haven; standalone market unvalidated.
- **O24** AI garden/landscape visualizer (#62, 40, Defer): Image generation economics fail the envelope.
- **O57** Divorce financial-disclosure organizer (#63, 40, Defer): Legal risk dominates.
- **O60** Contractor bid referee (#64, 40, Defer): Episodic.
- **O42** Ownership-graph / acquisitions tracker (#65, 40, Defer): Visual layer without a data supply.
- **O55** Home-inspection report triage (#66, 39, Drop): Episodic.
- **O62** Manuscript X-ray (#67, 39, Drop): Cost fails.
- **O75** Arcade (Telegram Mini-App games) (#68, 39, Drop): Cheap distribution loop, tiny ARPU.
- **O02** Pose Coach (duo photo director, iPhone) (#69, 39, in order): Concrete demo result but weak retention; direct subscription rivals already priced at $4.99-$9.99.
- **O09** [UZ] B2G packages: field-capture, municipal GIS, master-plan vectorisation (#70, 39, Drop): Big funded lines but a services business, not a SaaS.
- **O15** Gaussian splats: real-estate splat-as-a-service API (#71, 38, Drop): Per-scan GPU economics clash with the $20-50 envelope.
- **O39** Cookie-banner customiser (#72, 36, Drop): Crowded.
- **O54** Cake concept studio (#73, 36, Drop): Cost and price mismatch.
- **O11** [UZ] Activity Matcher (Tashkent, time-aware) (#74, 36, Drop): Personal discovery tool, not a business.
- **O40** Sitemap-to-SEO landing-page audit (#75, 35, Drop): Utility.
- **O70** Survey / quiz-storage engine (enabler) (#76, 34, Drop): Keep as engine only.
- **O27** [UZ] 3D-print physical products (gearbox demonstrators etc.) (#77, 33, Drop): Hardware business; paused by its own analysis.
- **O12** Route Vibe Player (route-scored music) (#78, 32, Drop): Novel but platform-dependent consumer toy.
- **O76** [UZ] Museums Gallery (UZ) (#79, 32, Drop): Public good without a payer.
- **O13** Spotify Mood Queue (#80, 31, Drop): Superseded by Route Vibe as its picker module; neither has a payer.
- **O23** Ambient content channels (ADHD music, cat/baby/senior calm) (#81, 31, Drop): Content business; outside SaaS constraints.
- **O22** Air-pollutant timeline map (#82, 31, Drop): Visualisation concept without a payer.
- **O17** Gaussian splats: asset marketplace (#83, 30, Drop): Marketplaces are excluded by protocol.
- **O18** [UZ] Gaussian splats: Central Asia heritage scanner (#84, 29, Drop): Project services.
- **O25** AI cultural-dress virtual try-on (#85, 29, Drop): Episodic and costly.
- **O78** Whiteout (WebGPU sniper FPS) + presets library (#86, 29, Drop): Engine value, not a SaaS revenue line.
- **O10** [UZ] valuation appeal / AVM / property due diligence (#87, 27, Drop): Dropped by its own source report on demand.
- **O14** Icon scraper (DX tool) (#88, 27, Drop): Free-source aggregation is a feature; Pro scraping is not viable.
- **O21** Gaussian splats: moonshots (4D event capture, game level editor) (#89, 17, Drop): Tech demos.

## Competitor evidence (every idea with base 60 or more)

Observed 2026-10-09 on the vendor's own pages by a research pass (WebFetch / search); prices are as displayed, with billing basis where shown. "Not verified" means the page showed no price or loaded it dynamically. A paid competitor shows a commercial category, not demand for our version.

Coverage: every idea with base 60 or more has at least one official competitor page above (O71, O05, O01, O83, O68, O81, O88, O79, O65, O52, O03, O85, O33, O43, O34, O50, O48, O31, O86, O72, O82, O89); pages were also opened for O16, O44, O64 and the Spotify-dependent O12/O13. Two gaps: O88 Podcast Readiness has no direct competitor with a public price (scheduling tools shown as partial substitutes) and O89 Haven has no verified official realtor price (OLX.uz and Uybor.uz show none). Pages were read through a page-summarising fetch tool, so figures are as extracted, not verbatim captures; where a page showed conflicting or unlabelled numbers it is marked not verified.

| ID | Idea | Competitor | URL opened | Observed price and facts (as displayed; vendor claims are the vendor's) | Date |
|---|---|---|---|---|---|
| O01 | ForeverPin | Uniqode | https://www.uniqode.com/pricing | Basic "$9/month", Core "$49/month" (FAQ: annual plans only, so per-month figures look annual-billed); other tiers show no price; custom domain add-on on Plus "$2000 per domain per year"; vendor says dynamic codes "become inactive" on cancellation or trial expiry | 2026-10-09 |
| O01 | ForeverPin | QR Tiger | https://www.qrcode-tiger.com/payment | Regular "US$7Month" (12 dynamic codes), Advanced "US$16Month" (200), Premium "US$37Month" (600); paid plans unlimited scans; billing basis not stated; its own pages disagree on which plan has multi-URL redirect and custom domain; dynamic codes "require a paid plan to keep them active" | 2026-10-09 |
| O01 | ForeverPin | Flowcode | https://www.flowcode.com/pricing | Free "$0" (2 codes, 500 scans); Pro Plus "$25" per month billed annually (50 codes, 6,000 scans); Growth "$250" annual only, unit not stated; routing/custom-domain ticks did not load (not verified) | 2026-10-09 |
| O01 | ForeverPin | QR Code Generator | https://www.qr-code-generator.com/pricing/ | Amounts not verified (placeholders, EUR ex-VAT); Advanced and Professional annual only; auto-renews, 30-day cancellation notice | 2026-10-09 |
| O03 | Transcript Forge | Descript | https://www.descript.com/pricing | Per person / month: Free $0 (1 media hour); Hobbyist $16 or $24 (10 h); Creator $24 or $35 (30 h); Business $50 or $65 (40 h); toggle monthly/annual, lower figure probably annual (inferred) | 2026-10-09 |
| O03 | Transcript Forge | Castmagic | https://www.castmagic.io/pricing | Hobby $19/mo billed annually ($239/yr, 30 h); Starter $48/mo billed annually ($579/yr, 100 h, API); Team $139/mo billed annually ($1,669/yr, 400 h); Business & Scale "From $699/mo"; monthly-billing prices not shown | 2026-10-09 |
| O03 | Transcript Forge | Opus Clip | https://www.opus.pro/pricing | Free $0; Starter $15/mo; Pro $29/mo; Business custom; minute allotments not stated | 2026-10-09 |
| O05 | UZ geocoder | Google Maps Platform Geocoding | https://developers.google.com/maps/billing-and-pricing/pricing | USD per 1,000 requests, pay-as-you-go: 10,000 free per month; to 100,000 at $5.00; 100,001-500,000 at $4.00; 500,001-1M at $3.00; plan bundles Starter $100/mo for 50,000 calls, Essentials $275/mo for 100,000 (billing basis not stated); Uzbek address quality not tested | 2026-10-09 |
| O05 | UZ geocoder | Yandex Geocoder (standalone) | https://yandex.com/dev/tariffs/doc/en/geocoder/prices/index.md | Annual prepaid, 1-year term: 1,000 queries/day $2,000 minimum (or $10,000 with data saving), 10,000/day $6,000 / $14,000, then $1-3 per 1,000 extra; non-refundable minimum; no free tier on this page | 2026-10-09 |
| O05 | UZ geocoder | Geoapify | https://www.geoapify.com/pricing/ | Billed monthly (USD): Free 3,000 credits/day; API 10 $59 (10,000/day); API 25 $109; API 50 $179; API 100 $299; geocode request = 1 credit; annual prices not loaded | 2026-10-09 |
| O12/O13 | Spotify-dependent music apps | Spotify for Developers (official) | https://developer.spotify.com/blog/2024-11-27-changes-to-the-web-api ; https://developer.spotify.com/documentation/web-api/concepts/quota-modes | Verified: since 2024-11-27, apps registered on or after that date lose Related Artists, Recommendations, Audio Features, Audio Analysis and some playlist endpoints; extended access (May 2025) needs a registered organisation, an active launched service and about 250k MAUs; development mode: 5 users, Premium owner | 2026-10-09 |
| O16 | Gaussian-splat annotation | Polycam | https://poly.cam/pricing | USD: Basic $150/yr ($30 monthly); Business $400/yr per user (shared team library); Enterprise $1,200/yr per user, 3-user minimum; splats on all tiers; only "comments on captures" listed | 2026-10-09 |
| O16 | Gaussian-splat annotation | Niantic Spatial / Scaniverse | https://www.nianticspatial.com/pricing | Free (5 seats); Plus $20/mo or $200/yr (10 seats); Pro $50/mo or $500/yr (25 seats); splats on all tiers; no annotation features mentioned | 2026-10-09 |
| O16 | Gaussian-splat annotation | PlayCanvas | https://playcanvas.com/plans | Free; Personal $15/mo; Organization $50/seat/mo billed monthly; SuperSplat annotation hotspots known only from a search snippet (not verified) | 2026-10-09 |
| O31 | Accessibility audit | Deque axe DevTools / Monitor | https://www.deque.com/axe/devtools/pricing/ | No list price shown; Free and Pro-trial extension; bundle and Monitor "talk to a sales rep" (contact sales) | 2026-10-09 |
| O31 | Accessibility audit | Pope Tech (WAVE engine) | https://pope.tech/pricing | Free $0 (1-25 pages); Team "$25/mo" (billed annually; $30 monthly); Business Plus "$225/mo" annual ($270 monthly) | 2026-10-09 |
| O31 | Accessibility audit | WAVE API (WebAIM) | https://wave.webaim.org/api/ | Prepaid credits $.04 to $.025 per credit; minimum purchase 250 credits ($10); not a subscription | 2026-10-09 |
| O33 | Cron-as-a-service | cron-job.org | https://cron-job.org/en/ | Free, "financed entirely by voluntary donations"; up to 60 executions per hour | 2026-10-09 |
| O33 | Cron-as-a-service | EasyCron | https://easycron.com/pricing | Free (200 EPDs, 20-min interval); Individual $24 / $60 / $120 / $240 per year; Enterprise $120 to $1,200 per year; "$" with no currency code; billed yearly | 2026-10-09 |
| O33 | Cron-as-a-service | Cronitor | https://cronitor.io/pricing | Hacker $0 (5 monitors); Business "$2/mo per monitor + $5/mo per user"; monitors your own jobs rather than hosting execution | 2026-10-09 |
| O34 | Webhook debugger/relay | Hookdeck | https://www.hookdeck.com/pricing | Developer $0 (10,000 events/mo, 3-day retention); Team "starts at" $39/mo; Growth "starts at" $499/mo; $3.00 per 100k events above included; included-event figure per tier not cross-checked | 2026-10-09 |
| O34 | Webhook debugger/relay | Webhook.site | https://docs.webhook.site/pro.html | USD ex-VAT: $9/mo or $90/yr; $27/mo or $270/yr; $69/mo or $699/yr (plan-to-price mapping by column order, inferred); Free tier 50 requests per URL | 2026-10-09 |
| O43 | PDF tool suite | iLovePDF | https://www.ilovepdf.com/pricing | Premium US$7 monthly or US$4/month billed annually (US$48/yr); Basic free; Business "Let's talk"; merge, split, watermark, redact, page numbers on paid tools; Bates numbering not listed | 2026-10-09 |
| O43 | PDF tool suite | Adobe Acrobat | https://www.adobe.com/acrobat/pricing.html | US$: Standard $14.99/mo annual commitment ($24.99 month-to-month); Pro $19.99/mo annual ($29.99 month-to-month); Studio $24.99/mo annual; redaction on Pro and Studio only; Bates and watermark not mentioned | 2026-10-09 |
| O43 | PDF tool suite | PDF24 | https://tools.pdf24.org/en/ | "100% free of charge", ad-funded; merge, split, watermark, page numbers, redact; Bates not listed | 2026-10-09 |
| O44 | Paint-by-numbers generator | PBNify | https://pbnify.com | Print-at-home files free (preview, numbered canvas PDF, colour guide, up to 60 colours); physical custom kit price not shown | 2026-10-09 |
| O44 | Paint-by-numbers generator | PaintByNumbers.NET | https://paintbynumbers.net | Free, in-browser, no account; printable PDF; links to a separate physical-kit site without prices | 2026-10-09 |
| O48 | Non-US FIRE planner | ProjectionLab | https://projectionlab.com/pricing | Basic $0/yr; Premium $129/yr (annual billing, no monthly shown); Pro $549/yr; "$" currency not stated; Premium lists "International Planning" (no UK ISA/SIPP wording) | 2026-10-09 |
| O48 | Non-US FIRE planner | Boldin | http://www.boldin.com/retirement/pricing/ | Basic free; PlannerPlus $144/yr (rising to $168 on 10/15); no UK/EU features mentioned | 2026-10-09 |
| O48 | Non-US FIRE planner | Compare Drawdown (UK) | https://comparedrawdown.co.uk/retirement-planner | Vendor says free tool; models UK State Pension, DB/DC pensions, ISAs, 2026/27 tax; optional-account cost not verified | 2026-10-09 |
| O50 | Faraid calculator (P056) | HalalWallet / Sharia Wiz calculators | https://www.halalwallet.us/tools/faraid-calculator ; https://www.shariawiz.com | Calculators are free (vendor statements) | 2026-10-09 |
| O50 | Faraid calculator (P056) | Sharia Wiz wills | https://www.shariawiz.com | Last Will and Testament $199; Health Care Directive $59; Power of Attorney $39; bundle $250 ($, currency not stated) | 2026-10-09 |
| O50 | Faraid calculator (P056) | IFG Wills (UK) | https://www.islamicfinanceguru.com/islamic-wills | Islamic Will GBP 98 one-time; Trust Based Will GBP 348 one-time; amendments GBP 10/yr | 2026-10-09 |
| O50 | Faraid calculator (P056) | Wasiyyah (Australia) | https://wasiyyah.com.au | "Just $89" (currency not named) including Shariah and Australian-law review | 2026-10-09 |
| O52 | KDP ads ROI tracker (P135) | ScribeCount | https://scribecount.com/pricing | Tier One $5.99/mo (income under $500/mo) to Tier Four $34.99/mo (over $2,500); lists "Ad spend vs royalty comparison" and ROI calculators; ACOS not mentioned | 2026-10-09 |
| O52 | KDP ads ROI tracker (P135) | Book Report | https://www.getbookreport.com/docs/pricing | Free under $1,000/mo earnings; Core $19/mo to Business $99/mo, Enterprise $249; Amazon Ads feature shows ad-spend impact; plan not stated | 2026-10-09 |
| O52 | KDP ads ROI tracker (P135) | Publisher Rocket | https://publisherrocket.com | One-time $199 (struck through $299), currency not stated; keyword/category research, no ad tracking shown | 2026-10-09 |
| O64 | Hunt club (P113) | CampKeeper: Deer Club Manager (App Store) | https://apps.apple.com/app/id6792546790 | "Club - Annual $119.99" ($119.99/year for the whole club); stand-reservation grid, harvest log, dues tracking; no monthly option shown | 2026-10-09 |
| O64 | Hunt club (P113) | The Hunt Club App (App Store) | https://apps.apple.com/app/id6760369151 | Free, no IAPs; stand reservations and harvest log | 2026-10-09 |
| O64 | Hunt club (P113) | Wild Apricot | https://www.wildapricot.com/pricing | 100 contacts $66.00/mo monthly, $59.40/mo on 1-year prepay; larger tiers did not load; dues renewals and event registration, no stand booking | 2026-10-09 |
| O65 | Golf society engine (P120) | Golfify | https://golfify.io (pricing section) | Per year, organiser pays only: solo Free (8 players), Lite $48, Basic $129, Plus $249, Pro $449; club Lite $99 to Pro $549; USD/GBP/EUR/AUD switch; handicaps/skins not verified | 2026-10-09 |
| O65 | Golf society engine (P120) | Golf Genius | https://www.golfgenius.com | No public price (pricing path redirects to a 404); contact sales; third-party figure of about $3,500-$4,200/yr not verified | 2026-10-09 |
| O65 | Golf society engine (P120) | RiddyGolf (App Store) | https://apps.apple.com/mx/app/riddygolf/id6736896294 | Free download, no in-app purchases listed; green-fee payments and leaderboard; HowDidiDo pricing 404 | 2026-10-09 |
| O68 | vault.guardian | ProBackup | https://www.probackup.io/backup/notion | Per workspace, "$" currency not named: Plus $25/mo annual ($31 monthly), 10 GB, 6 months history; Pro $38 ($47); Premium $69 ($86); daily backups, one-click restore (no lossless claim) | 2026-10-09 |
| O68 | vault.guardian | Notion Backups | https://notionbackups.com/ | Lite $6, Starter $11, Pro $28, Enterprise $89 per month (basis unclear); vendor: "A complete restore is not possible due to Notion's API limitations" | 2026-10-09 |
| O68 | vault.guardian | Notion (native history) | https://www.notion.com/pricing | Free 7 days of page history; Plus $10 (30 days); Business $20 (90 days) per member per month; billing mode not verified | 2026-10-09 |
| O68 | vault.guardian | Rewind Backups for Notion | https://rewind.com/products/backups/notion/ | No price; waitlist label; claims daily backups and 365-day retention | 2026-10-09 |
| O71 | Grant pipeline (P111) | Instrumentl | https://www.instrumentl.com/pricing | Discover $299/mo paid annually upfront ($326 monthly), 3 users; Pre-Award $499 ($579); Full Lifecycle $999 ($1,159), 15 users; currency not stated; 14-day trial | 2026-10-09 |
| O71 | Grant pipeline (P111) | Grantseeker | https://grantseeker.io/pricing | Classic Premium $19.99/mo; Prospecting $51.99/mo (monthly vs annual billing state not verified); Pro formula-based, demo only; grant tracking, deadlines, reports on Premium | 2026-10-09 |
| O72 | Newsletter sponsor storefront (P088) | Letterhead (Studio Revenue) | https://www.tryletterhead.com/pricing | No public price: quote driven by number of newsletters and audience size; sponsorship slots, calendar view and proof-of-publication tearsheets (vendor claim) | 2026-10-09 |
| O72 | Newsletter sponsor storefront (P088) | Passionfroot | https://www.passionfroot.me/creator-pricing | Creator plan free ("$", currency not stated); 2% fee per transaction paid by the brand; 15% fee when Passionfroot matches a brand; storefront, booking forms, slot calendar, invoicing (vendor claim) | 2026-10-09 |
| O79 | Retainer Balance | Harvest | https://www.getharvest.com/pricing | Teams $9/seat/mo billed annually ($11 monthly); Enterprise $14/seat/mo annual ($17.50 monthly); Free $0 (1 seat, 2 projects); USD; page lists time & materials and fixed-fee projects, no mention of retainers | 2026-10-09 |
| O79 | Retainer Balance | Productive | https://www.productive.io/pricing/ | Essential "$10/month" monthly toggle, "$12" yearly toggle (and "$9 billed yearly" elsewhere); Professional "$25/month"; Ultimate "Let's talk"; minimum 3 seats; page contradicts itself on figures (not verified); vendor lists "recurring budgets to automate retainer management" under Professional | 2026-10-09 |
| O79 | Retainer Balance | Accelo | https://www.accelo.com/pricing | No prices, custom quote; vendor says it runs fixed-fee projects and retainers side by side | 2026-10-09 |
| O81 | File Watch | Cronitor | https://cronitor.io/pricing | Hacker $0 (5 monitors); Business "$2 per monitor + $5 per user", monthly, 14-day trial; Enterprise from $6,000/yr | 2026-10-09 |
| O81 | File Watch | Healthchecks.io | https://healthchecks.io/pricing/ | Hobbyist $0 (20 jobs); Supporter $5/mo (20 jobs); Business $20/mo or $192/yr (100 jobs); Business Plus $80/mo or $768/yr (1,000 jobs) | 2026-10-09 |
| O82 | Procedure Review | Process Street | https://www.process.st/pricing/ | No prices shown, contact sales on Startup, Pro, Enterprise (Startup: under 15 employees, min 5 users); approvals and role assignments on all plans | 2026-10-09 |
| O82 | Procedure Review | SweetProcess | https://www.sweetprocess.com/ (pricing anchor) | $82.50/mo for up to 10 members billed yearly, +$4.17/mo per extra member; unlabelled "$99" and "$5" also shown (probably monthly rates, not verified); version history and manager approval | 2026-10-09 |
| O83 | Training Seats | Arlo | https://www.arlo.co/pricing | Per administrator: Simple "$118" or "$132"; Professional "$204" or "$227"; Enterprise "$271" or "$302" (annual vs monthly mapping not verified); plus $2.15 per paid registration; cancellations/transfers/refunds listed | 2026-10-09 |
| O83 | Training Seats | TalentLMS | http://www.talentlms.com/prices | Free $0 (5 users); Core from $119/mo; Grow from $229/mo; Pro from $449/mo; USD; priced by monthly logins; no reserved-seat feature seen | 2026-10-09 |
| O83 | Training Seats | Thinkific | https://thinkific.com/pricing/ | Basic $54/mo ($40 annual); Start $109 ($82); Grow $219 ($164); group orders and B2B bulk seats from Grow | 2026-10-09 |
| O85 | Customer Promises | Rocketlane | https://www.rocketlane.com/pricing | Standard $49 per team member/mo billed annually, min 5; Premium $69 per member/mo billed annually, min 5; no monthly option shown; customer portal and approvals | 2026-10-09 |
| O85 | Customer Promises | Dock | https://www.dock.us/pricing | Free $0 (10 workspaces); Standard $350/mo (5 internal seats); Premium $1,000/mo billed annually; extra seats $50/mo | 2026-10-09 |
| O86 | Vendor Renewals | Cledara | https://www.cledara.com/pricing | Basic £100/month (GBP view), yearly "Save 16%"; renewal alerts; quote-only tiers above | 2026-10-09 |
| O86 | Vendor Renewals | Contractbook | https://www.contractbook.com/pricing | Essential $399/month billed annually (1 user); other tiers conflicting or quote-only (not verified) | 2026-10-09 |
| O88 | Podcast Readiness | Calendly | https://calendly.com/pricing | Standard $10/seat/mo (yearly view); Teams $16/seat/mo (yearly view); Free $0; USD | 2026-10-09 |
| O88 | Podcast Readiness | Acuity Scheduling | https://acuityscheduling.com/pricing | Starter $16 (annual) / $20 (monthly); Standard $27 / $34; Premium $49 / $61; USD ex-tax; custom intake forms and reminders | 2026-10-09 |
| O88 | Podcast Readiness | PodMatch | https://podmatch.com/pricing | Amounts did not render (not verified); lists an interview release form and production-management workflows | 2026-10-09 |
| O89 | Haven | OLX.uz business / Uybor.uz | https://business.olx.uz ; https://uybor.uz | No official realtor price shown on either site (lead form; tariffs page 404); only a secondary news report (everyday.uz, 2026-09-04): 4-listing package 64,000 UZS, 1,000-listing Premium 12,990,000 UZS per 30 days; not verified from the vendor | 2026-10-09 |

## Cross-check: own top 5 against the research top 10

Own top 5 by final score against the research top 10 (S094 76, S081 75, S052 74, S083 73, S086 72, S080 72, S085 72, S090 72, S084 72, S055 71). The gap is 10 to 19 points: own top 5 sit at 57-61.

| Own idea (final) | Nearest researched product | Relationship |
|---|---|---|
| O71 Grant pipeline, P111 (61) | **S086** Grant portfolio operations, #5, 72, Reserve, $129 | Same buyer and record. S086 is the stronger version: it adds a post-award responsibility wedge and bring-your-own sources; P111 is a lighter pipeline at a lower price ($49) with an AI-drafting add-on that breaks the cost envelope. Fold P111 into the S086 test. |
| O05 UZ geocoder (60) | none | Outside the research by design (global dimension; regional dependence). Competes with Google Geocoding and Yandex; see evidence. |
| O01 ForeverPin (59, in order) | none | QR/redirect tooling is not a qualifying SaaS under the protocol (no multi-role workflow). No researched record is adjacent. |
| O83 Training Seats (58) | **S026** Independent training-provider operations (#22, 67, Reserve, $149); **S029** B2B course-license account operations (#13, 70, Validate, $199) | Narrower but sharper rule: purchased - reserved - attended = available, with substitution history and sponsor statements, which is the same seat/entitlement problem S029 tests across LMSs. Arlo already prices administrator licences at $118-$132 (evidence), above this prototype's $59. A candidate wedge for S026/S029, not a stronger product. |
| O68 vault.guardian (57) | none | Dev/data-safety lane is outside the researched pool; Notion backup is a priced category (ProBackup $25-$86/mo, Notion Backups $6-$89/mo). No researched record covers it. |

**Other overlaps (outside own top 5)**
- O82 Procedure Review (50) is a thinner slice of **S080** (#6, 72, Validate): S080 already includes policy version, control run and evidence export.
- O85 Customer Promises (53) is a fragment of **S083** (#4, 73) and **S084** (#9, 72).
- O88 Podcast Readiness (55) is a producer-side slice of **S042** (#15, 69); Transistor and Podbean network plans were its researched competitors.
- O72 Newsletter sponsor storefront (50) is weaker than **S039** (#11, 71, Validate): Letterhead and Passionfroot already cover inventory and booking.
- O86 Vendor Renewals (50) is adjacent to **S081** (#2, 75) and S060: buyer-side notice windows against S081's purchasing approvals.
- O79 Retainer Balance (55) sits near S001 fixed-fee consulting operations (#61, 58, Reserve); Productive already lists recurring retainer budgets (evidence).

**Where an own idea is a stronger version of a researched one:** none at score level. The only sharper mechanics are Training Seats' seat conservation (into S026/S029) and the evidence-bound attestation in Procedure Review (already inside S080's workflow). Own advantages are speed (built v0.1 prototypes: 3-6 weeks to charge) and founder access to the Uzbek market, neither of which the score counts.

## Excluded and out of scope

**Internal platform/SDK** (excluded once, reason "internal platform/SDK"): validation-wrapper-analysis, exceptions-analysis, logging-analysis, nullability-and-fixtures-analysis, constructs-taxonomy-analysis, mla-components-discovery, frontend-sdk-vue-port-analysis, shared-validation-spec, wow-two-sdk-modular-library-system-spec, api-endpoint-documentation-analysis, self-host-supabase-guide, currency-sdk-spec, identity-service-spec, feedbacks-spec, wheelhouse-spec, flowdeck-spec, nth26-map-vector-analysis (map layer as SDK vector).

**Not a product or no ideas**

| Item | Why excluded |
|---|---|
| interactive-3d-web-experiences-spec | Skills and tech-stack vision, no buyer or product |
| city-vision / ventures.city-vision | Speculative city design; documents and drawings only |
| youtube-apps-audit | Empty stub; no apps audited |
| telegram-features | Feature catalogue; names no product (Arcade is its only product use) |
| market-analysis | Method context only (scoring framework, audience tiers) |
| 10x-ventures/specs/idea-forge | Self-declared personal tool, "not a revenue bet" |
| your-pocket-doctor | Registry marks it a third-party clone; prism-wt-c is a leftover worktree |
| wow-two-apps.home-atlas, med-text-fab, meme-world; labs/*; projects/nasiya-finance; ocharo-hq | Outside `workbench/ventures`: private workbench, client work or a separate business |

**Government project, out of SaaS scope:** ventures.tnis, ventures.tnis-mintrans, track-2-transportbrain, tbs.demo. One named public buyer (YHTEM / ministries), sold as a pilot or project; no self-serve subscription shape found, so unscored.

**Merged into another row:** fun-vault into Hijinx; forever-pin-promo and the smart-qr name into ForeverPin; whiteout-presets into Whiteout; 10x-fin-nt into the NT auction tracker; ventures.home-renovation (empty README) into PRISM; micro-saas A13/A14 (QR with analytics, niche short URL) into ForeverPin; diamond-painting into the paint-by-numbers row.

**Not individually scored (kept in their source files):** 123 lower-tier ids of `products-final.md` (48 Tier B mid/lower, 71 Tier C, 4 killed); micro-saas-deep-search candidates outside its top 15 (court-case, patent and gov-spending trackers, domain history, flight deals, real-estate tracking, SaaS-wish directory); the remaining ~45 bank items in that file.

## Appendix A: scoring detail (P pain, R recurrence, B budget, D distribution, W wedge, F feasibility, G global, C cost)

| ID | Idea | P | R | B | D | W | F | G | C | Base | Pen | Final | Penalty reason |
|---|---|-:|-:|-:|-:|-:|-:|-:|-:|--:|--:|--:|---|
| O71 | Small-nonprofit grant pipeline (P111) | 4 | 4 | 3 | 3 | 2 | 4 | 4 | 4 | 68 | 7 | 61 | Lighter-scope version of researched S086; Grantseeker and Instrumentl already serve it |
| O05 | [UZ] geocoder / address normalisation API | 4 | 5 | 3 | 3 | 4 | 3 | 1 | 4 | 72 | 12 | 60 | UZ-only; state register due ~2030 and WB packages under procurement; cadastre data licence unresolved; UZ banks may demand on-prem |
| O01 | ForeverPin (programmable QR + link router) | 3 | 4 | 2 | 3 | 3 | 5 | 5 | 4 | 67 | 8 | 59 | Crowded commodity category; solo operator buyer, no multi-role workflow; entitlement bug lets canceled plans keep capacity |
| O83 | Training Seats (first-ten, W0289) | 3 | 4 | 3 | 2 | 3 | 4 | 5 | 5 | 66 | 8 | 58 | Narrow seat-conservation rule; related to researched S026 |
| O68 | vault.guardian (Notion backup + version history) | 4 | 4 | 2 | 3 | 3 | 3 | 5 | 4 | 67 | 10 | 57 | Restore-into-own-format wedge needs vault.desk (unbuilt); Notion could ship native backup; Notion API limits |
| O81 | File Watch (first-ten, W0031) | 3 | 5 | 3 | 2 | 2 | 4 | 5 | 5 | 66 | 10 | 56 | Monitor/reminder shape; cron monitors substitute |
| O88 | Podcast Readiness (first-ten, W0507) | 3 | 4 | 2 | 3 | 2 | 4 | 5 | 5 | 63 | 8 | 55 | Narrow slice of researched podcast production ops (S042) |
| O79 | Retainer Balance (first-ten, W0252) | 3 | 4 | 3 | 2 | 2 | 4 | 5 | 5 | 63 | 8 | 55 | Retainer budgets exist in time-tracking/PSA tools; personal workspace, no teams |
| O65 | Golf society engine | 3 | 4 | 2 | 3 | 3 | 3 | 3 | 5 | 62 | 8 | 54 | Secretary turnover; HowDidiDo/Golf Genius adjacent |
| O52 | KDP ads ROI tracker (royalty-aware ACOS) | 3 | 4 | 3 | 3 | 2 | 3 | 4 | 4 | 62 | 8 | 54 | Amazon report/API churn and native-feature risk; ScribeCount and Book Report already track ad spend vs royalty at $5.99-$34.99/mo |
| O03 | Transcript Forge (creator repurposing suite) | 3 | 4 | 3 | 3 | 2 | 3 | 5 | 2 | 61 | 8 | 53 | Transcripts are commodity; layers 2-3 crowded; hosted STT/LLM cost breaks the $20-50 envelope without pass-through |
| O85 | Customer Promises (first-ten, W0276) | 3 | 4 | 3 | 2 | 2 | 4 | 5 | 5 | 63 | 10 | 53 | Overlaps researched customer-implementation/CS ops (S083/S084); no client sign-in |
| O33 | Cron-as-a-service | 3 | 5 | 2 | 3 | 1 | 5 | 5 | 4 | 64 | 12 | 52 | Isolated utility; free cron-job.org and monitors; reliability SLA expectation |
| O43 | PDF tool suite (Bates stamp, redact, title page, watermark) | 3 | 3 | 2 | 3 | 2 | 5 | 5 | 4 | 61 | 10 | 51 | Isolated utilities; iLovePDF Premium $4-7/mo, PDF24 free and Acrobat Pro $19.99+ already cover most tools; Bates numbering is the open niche |
| O34 | Webhook debugger / relay | 3 | 4 | 2 | 3 | 1 | 5 | 5 | 4 | 61 | 10 | 51 | Hookdeck, webhook.site, ngrok cover this; free tiers |
| O50 | Faraid (Islamic inheritance) calculator | 3 | 1 | 2 | 4 | 4 | 4 | 4 | 5 | 62 | 12 | 50 | Event-driven one-shot; correctness liability across madhhabs; free crude calculators |
| O48 | Non-US FIRE planner | 3 | 3 | 3 | 3 | 2 | 3 | 4 | 5 | 60 | 10 | 50 | Financial-advice liability; per-country rule upkeep; ProjectionLab lists international planning and a free UK planner exists |
| O31 | Accessibility audit (axe-core wrapper) | 3 | 3 | 3 | 3 | 1 | 5 | 4 | 4 | 60 | 10 | 50 | Free axe/WAVE/Lighthouse; monitoring vendors well funded |
| O86 | Vendor Renewals (first-ten, W0261) | 3 | 4 | 2 | 3 | 1 | 5 | 5 | 5 | 62 | 12 | 50 | Reminder/tracker; spend-management vendors |
| O72 | Newsletter sponsor storefront (P088) | 3 | 4 | 2 | 2 | 2 | 4 | 5 | 5 | 60 | 10 | 50 | Two-sided element; Passionfroot creator side is free (2% brand-paid fee) and Letterhead covers inventory; overlaps researched S039 |
| O82 | Procedure Review (first-ten, W0263) | 3 | 4 | 2 | 2 | 2 | 4 | 5 | 5 | 60 | 10 | 50 | Weaker version of researched S080 (policy and control ops) |
| O89 | [UZ] Haven (Tashkent real-estate platform) | 4 | 4 | 3 | 3 | 3 | 3 | 1 | 2 | 64 | 15 | 49 | Brokerage rules change 2026-11-08 (ZRU-1163); seller, price and bot scope open; scraping upkeep |
| O26 | AI menu translator for restaurants | 3 | 2 | 3 | 3 | 2 | 4 | 4 | 3 | 57 | 8 | 49 | QR-menu vendors already bundle translation |
| O16 | Gaussian splats: annotation and collaboration tool | 3 | 4 | 3 | 2 | 2 | 3 | 5 | 3 | 59 | 10 | 49 | Splat workflows are rare; Polycam, Niantic and PlayCanvas bundle viewers and team seats at $20-$50/user/mo; large-file storage |
| O38 | Trademark filing watcher (US/EU) | 3 | 4 | 3 | 2 | 2 | 3 | 4 | 4 | 59 | 10 | 49 | Free registry alerts and bundled watch services; needs distribution to legal/brand owners |
| O56 | LEGO collection value tracker | 2 | 4 | 2 | 3 | 2 | 4 | 5 | 4 | 58 | 10 | 48 | BrickEconomy free incumbent; collector price points |
| O77 | PRISM (parametric renovation modeler) | 3 | 2 | 3 | 2 | 3 | 3 | 5 | 5 | 58 | 10 | 48 | Crowded consumer planners (SketchUp-class, Floorplanner); project-based use; no accounts or billing yet |
| O45 | Parent IEP command center | 4 | 3 | 2 | 3 | 3 | 3 | 1 | 3 | 59 | 12 | 47 | US special-education law only; children's data; district tools exist; school-year seasonality |
| O53 | Decodable-text generator | 3 | 3 | 2 | 3 | 3 | 3 | 3 | 3 | 57 | 10 | 47 | Teacher budgets; edtech gold rush |
| O44 | Paint-by-numbers + diamond-painting kit generator | 3 | 2 | 2 | 3 | 2 | 4 | 5 | 5 | 57 | 10 | 47 | Generator = feature; one-off kits; PBNify and PaintByNumbers.NET already give free printable numbered canvases |
| O69 | Kids-curiosity chapters (P140) | 2 | 4 | 3 | 3 | 2 | 3 | 5 | 2 | 57 | 10 | 47 | ChatGPT/Khanmigo free; kids' data; per-chapter LLM cost |
| O30 | Receipt-to-CSV | 3 | 4 | 2 | 3 | 1 | 4 | 4 | 3 | 57 | 10 | 47 | LLM-commodity extraction; Dext/Expensify class bundle it |
| O20 | Gaussian splats: construction progress tracker | 4 | 4 | 4 | 2 | 2 | 1 | 4 | 1 | 59 | 12 | 47 | Drones, outdoor splat quality, GPU cost; OpenSpace-class incumbents |
| O87 | Config Checker (first-ten, W0034) | 3 | 3 | 2 | 2 | 2 | 4 | 5 | 5 | 57 | 10 | 47 | Checker; secrets managers and CI diffs substitute |
| O35 | License-renewal reminder (CME/bar) | 3 | 3 | 1 | 3 | 2 | 5 | 2 | 5 | 56 | 10 | 46 | Reminder, jurisdiction-specific rules, $5 price |
| O58 | Digital-planner generator | 2 | 3 | 2 | 3 | 2 | 4 | 5 | 5 | 56 | 10 | 46 | Seasonal; $10 Etsy anchors |
| O80 | Documentation Checker (first-ten, W0012) | 2 | 3 | 2 | 3 | 2 | 4 | 5 | 5 | 56 | 10 | 46 | Checker; free local linters; JS only |
| O06 | [UZ] rejection pre-check (tax/VAT refund, social, cadastre) | 4 | 3 | 3 | 2 | 3 | 2 | 1 | 4 | 58 | 12 | 46 | Rejection-rate figures are derived; 9 of 14 strong signals in the same report were refuted; legal-advice liability; small private buyer pool |
| O37 | [UZ] business-registry lookup API | 3 | 4 | 2 | 2 | 3 | 3 | 1 | 4 | 56 | 10 | 46 | Data source terms unclear; UZ-only |
| O84 | EPUB Review (first-ten, W0521) | 2 | 3 | 2 | 2 | 3 | 4 | 5 | 5 | 56 | 10 | 46 | Tiny niche; operator-entered client review |
| O51 | Picture-book illustrator for KDP authors | 3 | 2 | 3 | 3 | 3 | 2 | 5 | 1 | 55 | 10 | 45 | Image-gen cost per page; character consistency |
| O66 | Milestone-event command center | 3 | 1 | 3 | 3 | 3 | 3 | 2 | 5 | 55 | 10 | 45 | One-shot events; Zola/Partiful stretch |
| O04 | Hijinx (party-game PWA + packs; fun-vault content) | 2 | 2 | 2 | 3 | 2 | 4 | 5 | 5 | 53 | 8 | 45 | Entertainment content; pack sales are one-off, not MRR; no multi-role record |
| O63 | Lawn quote from satellite | 3 | 4 | 3 | 3 | 2 | 2 | 1 | 2 | 55 | 10 | 45 | US-only imagery licence; DeepLawn-class incumbent |
| O67 | String-art generator (locked engine proof) | 2 | 2 | 2 | 3 | 2 | 4 | 5 | 5 | 53 | 8 | 45 | Generator = feature; one-off |
| O32 | OG-image generator (templated) | 2 | 3 | 2 | 3 | 1 | 5 | 5 | 5 | 55 | 10 | 45 | Vercel OG, Bannerbear, free tools |
| O59 | Executor's companion | 4 | 1 | 3 | 3 | 2 | 3 | 1 | 4 | 54 | 10 | 44 | One-time life event; EstateExec/Atticus sell it |
| O29 | [UZ] NT auction-lot tracker | 3 | 3 | 1 | 2 | 3 | 5 | 1 | 4 | 54 | 10 | 44 | Tiny UZ audience; source-site scraping risk; personal-use tool |
| O49 | Custody evidence binder | 4 | 2 | 3 | 2 | 3 | 3 | 1 | 3 | 56 | 12 | 44 | Adversarial, US family-court specifics; support burden |
| O74 | sift (curated YouTube feed with density ranking) | 2 | 4 | 2 | 2 | 3 | 3 | 5 | 2 | 54 | 10 | 44 | Consumer, single-user; per-video LLM cost; YouTube quota |
| O36 | SSL and domain-expiry monitor | 2 | 4 | 1 | 3 | 1 | 5 | 5 | 5 | 55 | 12 | 43 | Free monitors cover it |
| O07 | [UZ] emission-telemetry integration adapters | 4 | 3 | 4 | 2 | 3 | 1 | 1 | 3 | 58 | 15 | 43 | Integration project per site, not self-serve SaaS; deadlines already lapsed; decree-priced ROI unverified |
| O64 | Hunt club and lease command center | 3 | 3 | 2 | 2 | 2 | 3 | 1 | 5 | 51 | 8 | 43 | US-only; seasonal; CampKeeper Deer Club Manager already sells stand booking, harvest log and dues at $119.99/yr per club |
| O47 | Bank-statement to categorised CSV | 3 | 3 | 3 | 2 | 1 | 4 | 3 | 3 | 53 | 10 | 43 | LLM commoditisation; contested SEO |
| O28 | Privacy-policy generator | 3 | 1 | 2 | 4 | 1 | 5 | 3 | 5 | 54 | 12 | 42 | Isolated generator, one-off, legal liability; Termly/iubenda/free generators |
| O61 | Medical-bill auditor | 4 | 1 | 3 | 3 | 3 | 2 | 1 | 3 | 54 | 12 | 42 | CPT data licensing, US-only, dispute-support drag |
| O41 | Podcast chapter generator | 2 | 3 | 2 | 3 | 1 | 4 | 5 | 4 | 52 | 10 | 42 | Hosts and editors bundle auto-chapters |
| O08 | [UZ] registry crosswalk / address-to-mahalla resolver | 4 | 4 | 3 | 1 | 3 | 2 | 1 | 3 | 57 | 15 | 42 | B2G integration with no procurement seam; in-house operator assigned; sold as subcontract |
| O19 | Gaussian splats: Shopify 3D product viewer | 2 | 3 | 2 | 3 | 2 | 2 | 5 | 2 | 49 | 8 | 41 | Competitive Shopify category; small-object splat quality unreliable |
| O46 | HOA resale-package X-ray | 3 | 1 | 3 | 2 | 4 | 3 | 1 | 2 | 51 | 10 | 41 | One-shot at purchase; US-only; liability optics; long-document LLM cost |
| O73 | [UZ] ListingShelf (OLX/Domtut listing archive) | 2 | 4 | 2 | 2 | 3 | 4 | 1 | 3 | 53 | 12 | 41 | Scraping/IP-block risk; personal-utility hypothesis; UZ-only |
| O24 | AI garden/landscape visualizer | 2 | 2 | 3 | 3 | 2 | 3 | 5 | 1 | 50 | 10 | 40 | Image-generation cost per render; many AI design apps |
| O57 | Divorce financial-disclosure organizer | 4 | 2 | 3 | 2 | 3 | 2 | 1 | 3 | 54 | 14 | 40 | Adversarial, UPL optics, US-specific, episodic |
| O60 | Contractor bid referee | 3 | 1 | 3 | 2 | 3 | 3 | 2 | 3 | 50 | 10 | 40 | Per-project one-shot; ChatGPT handles passably |
| O42 | Ownership-graph / acquisitions tracker | 3 | 3 | 3 | 2 | 2 | 2 | 4 | 2 | 52 | 12 | 40 | Company data licensing (Crunchbase paid, EDGAR US-only); frontend POC only |
| O55 | Home-inspection report triage | 3 | 1 | 3 | 3 | 2 | 3 | 1 | 3 | 49 | 10 | 39 | One-shot; RepairPricer incumbent; US-only |
| O62 | Manuscript X-ray | 3 | 2 | 2 | 3 | 2 | 2 | 5 | 1 | 49 | 10 | 39 | 120k-word LLM runs break the envelope; ProWritingAid scale |
| O75 | Arcade (Telegram Mini-App games) | 1 | 3 | 1 | 3 | 2 | 4 | 4 | 4 | 47 | 8 | 39 | Games with cosmetic Stars; no MRR; platform payout path unverified |
| O02 | Pose Coach (duo photo director, iPhone) | 2 | 2 | 2 | 2 | 2 | 3 | 4 | 5 | 47 | 8 | 39 | Consumer app, not a qualifying SaaS record; occasional use; free and paid direct competitors |
| O09 | [UZ] B2G packages: field-capture, municipal GIS, master-plan vectorisation | 4 | 2 | 5 | 1 | 2 | 2 | 1 | 3 | 54 | 15 | 39 | Project-based; needs prime contractor or JV; no PPP clause found; firm-level track record required |
| O15 | Gaussian splats: real-estate splat-as-a-service API | 3 | 2 | 3 | 2 | 2 | 2 | 4 | 1 | 48 | 10 | 38 | Per-scan GPU training cost; Polycam/Luma/Matterport capture-and-share already exist |
| O39 | Cookie-banner customiser | 2 | 3 | 1 | 3 | 1 | 4 | 3 | 5 | 48 | 12 | 36 | Cookiebot/CookieYes free tiers |
| O54 | Cake concept studio | 2 | 3 | 2 | 2 | 3 | 2 | 3 | 1 | 46 | 10 | 36 | Photoreal render cost; sub-$30 price |
| O11 | [UZ] Activity Matcher (Tashkent, time-aware) | 2 | 3 | 1 | 2 | 2 | 5 | 1 | 5 | 48 | 12 | 36 | No payer defined (monetisation is an open question); ads excluded by principle; local data upkeep |
| O40 | Sitemap-to-SEO landing-page audit | 2 | 1 | 2 | 3 | 1 | 4 | 5 | 5 | 47 | 12 | 35 | One-shot audit; SEO tools bundle it |
| O70 | Survey / quiz-storage engine (enabler) | 2 | 3 | 2 | 1 | 1 | 4 | 5 | 4 | 46 | 12 | 34 | Google/Microsoft Forms-shaped; an enabler, not a market |
| O27 | [UZ] 3D-print physical products (gearbox demonstrators etc.) | 2 | 2 | 3 | 2 | 3 | 3 | 1 | 3 | 48 | 15 | 33 | Physical fulfilment; Etsy/Payoneer unavailable from UZ; violates the no-physical-fulfilment constraint |
| O12 | Route Vibe Player (route-scored music) | 1 | 2 | 2 | 2 | 3 | 2 | 4 | 3 | 42 | 10 | 32 | Spotify removed Audio Features/Recommendations for apps registered after 2024-11-27 (official blog); extended access needs a registered organisation and ~250k MAUs; trip-limited use |
| O76 | [UZ] Museums Gallery (UZ) | 1 | 2 | 1 | 2 | 3 | 4 | 1 | 5 | 42 | 10 | 32 | No payer; agreements with state organisations gate monetisation; unverified seed data |
| O13 | Spotify Mood Queue | 1 | 3 | 1 | 2 | 2 | 3 | 4 | 3 | 41 | 10 | 31 | Same Spotify restriction (verified 2026-10-09); ChatGPT and Spotify cover mood playlists free |
| O23 | Ambient content channels (ADHD music, cat/baby/senior calm) | 1 | 3 | 2 | 2 | 1 | 4 | 5 | 2 | 43 | 12 | 31 | Ad/streaming revenue, not SaaS; $140-270/mo cost vs $20-50 envelope; YouTube AI-content policy risk |
| O22 | Air-pollutant timeline map | 2 | 2 | 2 | 1 | 2 | 3 | 5 | 3 | 43 | 12 | 31 | No buyer named; NASA Worldview and Sentinel browsers are free |
| O17 | Gaussian splats: asset marketplace | 2 | 2 | 2 | 1 | 2 | 2 | 4 | 3 | 40 | 10 | 30 | Two-sided marketplace with supply cold-start |
| O18 | [UZ] Gaussian splats: Central Asia heritage scanner | 2 | 1 | 2 | 2 | 3 | 2 | 1 | 2 | 39 | 10 | 29 | Government/tourism projects, not subscription; UZ-only |
| O25 | AI cultural-dress virtual try-on | 2 | 1 | 2 | 2 | 3 | 2 | 2 | 1 | 39 | 10 | 29 | ML pipeline cost; episodic wedding use |
| O78 | Whiteout (WebGPU sniper FPS) + presets library | 1 | 2 | 2 | 2 | 2 | 1 | 5 | 4 | 39 | 10 | 29 | A game; one-off sale; huge content scope |
| O10 | [UZ] valuation appeal / AVM / property due diligence | 2 | 1 | 2 | 2 | 2 | 2 | 1 | 3 | 37 | 10 | 27 | The demand map itself dropped it: two buyers found, no funded mass-valuation buyer |
| O14 | Icon scraper (DX tool) | 1 | 2 | 1 | 2 | 1 | 5 | 5 | 5 | 42 | 15 | 27 | Scraping Font Awesome Pro is a licence breach; free aggregators already exist |
| O21 | Gaussian splats: moonshots (4D event capture, game level editor) | 1 | 1 | 1 | 1 | 2 | 1 | 4 | 2 | 27 | 10 | 17 | No monetisation defined |

## Appendix B: buyer, revenue shape, builder-weeks and blocker

Weeks assume one experienced full-time builder, include billing and hosting on the existing product template, and exclude acquisition, store review and entity or Stripe set-up (the US LLC is gated by three written answers in the parent-company note). Tiers here are absolute; the research's tiers in subscription-speed.md ranked ten finalists against each other (S055 at 6-10 weeks was tier 1 there, tier 2-3 on this scale).

| ID | Idea | Target buyer | Revenue shape | Weeks | Spd | Main blocker |
|---|---|---|---|---|:-:|---|
| O71 | Small-nonprofit grant pipeline (P111) | Small nonprofits' grant writers | recurring | 8-12 | 3 | Wedge vs Instrumentl/Grantseeker |
| O05 | [UZ] geocoder / address normalisation API | UZ marketplaces, couriers, banks, insurers, utilities | usage | 8-14 | 4 | 85% house-level gold-set accuracy gate; data licence; UZ entity for invoices |
| O01 | ForeverPin (programmable QR + link router) | SMB/solo operators with printed surfaces; marketers; devs | recurring | 2-4 | 1 | Entitlement fix + live Stripe/OAuth verification; US LLC for Stripe |
| O83 | Training Seats (first-ten, W0289) | Independent training providers with sponsors | recurring | 3-6 | 2 | Teams, sponsor sign-in, billing |
| O68 | vault.guardian (Notion backup + version history) | Notion-heavy teams and freelancers | recurring | 8-12 | 3 | Notion API fidelity; destination product absent |
| O81 | File Watch (first-ten, W0031) | Ops owners expecting partner files | recurring | 3-6 | 2 | Teams, notification delivery, billing |
| O88 | Podcast Readiness (first-ten, W0507) | Podcast producers | recurring | 3-6 | 2 | Email sending, calendar, billing |
| O79 | Retainer Balance (first-ten, W0252) | Agencies/consultancies on retainers | recurring | 3-6 | 2 | Team workspaces, billing, hosting, backup |
| O65 | Golf society engine | Golf society secretaries (UK/US) | recurring | 6-10 | 3 | Handicap rules |
| O52 | KDP ads ROI tracker (royalty-aware ACOS) | KDP self-publishers running ads | recurring | 4-8 | 2 | Amazon Ads data access |
| O03 | Transcript Forge (creator repurposing suite) | Mid-tier creators (10k-500k subs), podcasters | recurring | 6-10 after Release 1 | 3 | Local Release 1 first; multi-tenant isolation, quotas, STT cost control |
| O85 | Customer Promises (first-ten, W0276) | Small service firms | recurring | 4-8 | 2 | Authenticated client confirmations |
| O33 | Cron-as-a-service | Developers | recurring | 2-4 | 1 | Reliability reputation |
| O43 | PDF tool suite (Bates stamp, redact, title page, watermark) | Paralegals, small law firms, admins | recurring | 4-8 | 2 | Per-tool landing pages and billing; wedge per tool |
| O34 | Webhook debugger / relay | Developers | recurring | 2-4 | 1 | Differentiation |
| O50 | Faraid (Islamic inheritance) calculator | Muslim diaspora families, imams, will writers | one-off | 3-5 | 2 | Scholarly review of rules |
| O48 | Non-US FIRE planner | UK/EU early-retirement planners | recurring | 8-12 | 3 | Rule upkeep per country |
| O31 | Accessibility audit (axe-core wrapper) | Dev teams, agencies | mixed | 2-4 | 1 | Differentiation vs free scanners |
| O86 | Vendor Renewals (first-ten, W0261) | Small teams with SaaS contracts | recurring | 3-5 | 2 | Teams, notifications |
| O72 | Newsletter sponsor storefront (P088) | Newsletter publishers | recurring | 8-12 | 3 | Advertiser supply |
| O82 | Procedure Review (first-ten, W0263) | Small ops teams needing attestations | recurring | 3-6 | 2 | Team assignment, notifications |
| O89 | [UZ] Haven (Tashkent real-estate platform) | UZ realtors | recurring | n/a (gated) | 3 | User gate: stable $2K MRR first |
| O26 | AI menu translator for restaurants | Restaurants in tourist areas | recurring | 4-6 | 2 | Distribution to restaurants one by one |
| O16 | Gaussian splats: annotation and collaboration tool | Construction, architecture, insurance teams with scans | recurring | 8-12 | 3 | Buyer with splat captures not identified |
| O38 | Trademark filing watcher (US/EU) | Small brands, solo IP counsel | recurring | 6-10 | 3 | Registry API limits; matching quality |
| O56 | LEGO collection value tracker | LEGO collectors | recurring | 3-5 | 2 | Free incumbent |
| O77 | PRISM (parametric renovation modeler) | Renovators, interior designers | recurring | 6-10 | 3 | Accounts/billing/hosting; engine rewrite |
| O45 | Parent IEP command center | US parents of IEP students | recurring | 8-12 | 3 | Child-data trust; LLM cost per PDF |
| O53 | Decodable-text generator | Teachers, tutors | recurring | 6-10 | 3 | Phoneme validator quality |
| O44 | Paint-by-numbers + diamond-painting kit generator | Etsy kit sellers, pet-photo kit buyers | mixed | 4-6 | 2 | Segmentation quality; unproven buyer |
| O69 | Kids-curiosity chapters (P140) | Parents of curious children | recurring | 6-10 | 3 | Child-data trust |
| O30 | Receipt-to-CSV | Freelancers, bookkeepers | usage | 3-5 | 2 | Pass-through pricing must beat commodity |
| O20 | Gaussian splats: construction progress tracker | Construction PMs | recurring | 20+ | 5 | Drone capture pipeline, GPU cost |
| O87 | Config Checker (first-ten, W0034) | Small engineering teams | recurring | 4-8 | 2 | CLI distribution, machine tokens |
| O35 | License-renewal reminder (CME/bar) | Doctors, lawyers | recurring | 2-3 | 1 | Rules per jurisdiction |
| O58 | Digital-planner generator | GoodNotes users | one-off | 3-5 | 2 | Etsy price anchors |
| O80 | Documentation Checker (first-ten, W0012) | API/SDK doc maintainers | recurring | 4-8 | 2 | More language adapters; billing |
| O06 | [UZ] rejection pre-check (tax/VAT refund, social, cadastre) | UZ tax advisors, accountants, property-heavy corporates | recurring | 10-16 | 4 | Rule corpus + registry lookups need legal expertise and data access |
| O37 | [UZ] business-registry lookup API | UZ SMB tools, fintech | usage | 3-5 | 2 | Official data access |
| O84 | EPUB Review (first-ten, W0521) | EPUB production vendors | recurring | 4-6 | 2 | Buyer reach |
| O51 | Picture-book illustrator for KDP authors | Self-pub authors | one-off | 10-16 | 4 | Consistency quality; GPU cost |
| O66 | Milestone-event command center | Quince/mitzvah hosts | one-off | 6-10 | 3 | Culture-specific content |
| O04 | Hijinx (party-game PWA + packs; fun-vault content) | Frequent hosts, families, teams (icebreakers) | mixed | 3-5 (packs, incl. QA) | 2 | Free-release QA; entitlement/restore model for paid packs; subscription needs new repeat-host workflow (+3-6 wks) |
| O63 | Lawn quote from satellite | US lawn-care operators | recurring | 10-16 | 4 | Imagery licence |
| O67 | String-art generator (locked engine proof) | Craft hobbyists | one-off | 3-5 | 2 | None |
| O32 | OG-image generator (templated) | Marketers, devs | mixed | 2-3 | 1 | Commodity |
| O59 | Executor's companion | US executors | one-off | 6-10 | 3 | State checklists |
| O29 | [UZ] NT auction-lot tracker | UZ real-estate investors | recurring | 2-4 | 1 | UZ entity and Click/Payme; source stability |
| O49 | Custody evidence binder | US pro-se parents | recurring | 6-10 | 3 | Court formats per state |
| O74 | sift (curated YouTube feed with density ranking) | Learners who use YouTube heavily | recurring | 8-12 | 3 | YouTube API key, TL;DR cost |
| O36 | SSL and domain-expiry monitor | Devs, agencies | recurring | 2-3 | 1 | None; no wedge |
| O07 | [UZ] emission-telemetry integration adapters | Category I/II industrial enterprises facing 5x/10x penalties | one-off | 14-22 | 5 | Hardware/telemetry integration per site; enterprise sales |
| O64 | Hunt club and lease command center | US hunt clubs | recurring | 8-12 | 3 | Reaching clubs |
| O47 | Bank-statement to categorised CSV | Freelancers, SMB bookkeepers | usage | 3-5 | 2 | Commodity |
| O28 | Privacy-policy generator | Small site owners | one-off | 2-3 | 1 | Jurisdiction accuracy; no recurring revenue |
| O61 | Medical-bill auditor | US patients | one-off | 8-12 | 3 | Fee-schedule data |
| O41 | Podcast chapter generator | Podcasters | recurring | 3-5 | 2 | Commoditised |
| O08 | [UZ] registry crosswalk / address-to-mahalla resolver | ~24 UZ government bodies (via primes) | one-off | 16-24 | 5 | No visible procurement route; prime contractor required |
| O19 | Gaussian splats: Shopify 3D product viewer | Shopify merchants | recurring | 12-18 | 4 | Splat quality for small objects; GPU cost |
| O46 | HOA resale-package X-ray | US home buyers, agents | one-off | 6-10 | 3 | Reaching buyers in 3-day window |
| O73 | [UZ] ListingShelf (OLX/Domtut listing archive) | UZ realtors, investors | recurring | 4-6 | 2 | UZ entity and Click/Payme; source stability |
| O24 | AI garden/landscape visualizer | Homeowners, landscapers | recurring | 10-16 | 4 | Per-render GPU cost |
| O57 | Divorce financial-disclosure organizer | US divorcing parties | recurring | 10-14 | 4 | Legal exposure |
| O60 | Contractor bid referee | Homeowners | one-off | 5-8 | 2 | Free LLM substitute |
| O42 | Ownership-graph / acquisitions tracker | Analysts, journalists, M&A researchers | recurring | 10-16 | 4 | Data source |
| O55 | Home-inspection report triage | US home buyers, agents | one-off | 6-10 | 3 | Cost-accuracy credibility |
| O62 | Manuscript X-ray | Indie novelists | one-off | 8-12 | 3 | LLM cost |
| O75 | Arcade (Telegram Mini-App games) | Telegram chat groups | one-off | 2-4 | 1 | Stars payout path for a UZ-resident founder |
| O02 | Pose Coach (duo photo director, iPhone) | Friends/couples making social photos | recurring | 4-8 | 2 | Physical-iPhone quality, StoreKit products, App Store review, Apple W-8/W-9 for the LLC |
| O09 | [UZ] B2G packages: field-capture, municipal GIS, master-plan vectorisation | UZ utilities, Urbanization Center, municipalities | one-off | 20+ | 5 | Sub-consultant status to an international prime; UZ entity |
| O15 | Gaussian splats: real-estate splat-as-a-service API | Independent agents, small brokerages | usage | 12-18 | 4 | GPU training cost per scan; quality on phone video |
| O39 | Cookie-banner customiser | Site owners | recurring | 3-4 | 1 | Differentiation |
| O54 | Cake concept studio | Home bakers | recurring | 10-14 | 4 | Render cost |
| O11 | [UZ] Activity Matcher (Tashkent, time-aware) | Tashkent residents | none/ads | n/a (no payer) | 5 | No revenue model; venue data upkeep |
| O40 | Sitemap-to-SEO landing-page audit | SEO freelancers | one-off | 2-3 | 1 | No recurrence |
| O70 | Survey / quiz-storage engine (enabler) | Internal | recurring | n/a | 5 | No standalone buyer |
| O27 | [UZ] 3D-print physical products (gearbox demonstrators etc.) | UZ vocational schools, engineers | one-off | n/a | 5 | Payout and shipping wall |
| O12 | Route Vibe Player (route-scored music) | Road-trippers | recurring | 10-16 | 5 | Streaming-provider API terms; background GPS audio |
| O76 | [UZ] Museums Gallery (UZ) | Tourists, museum operators | none/ads | n/a | 5 | No revenue model |
| O13 | Spotify Mood Queue | Spotify listeners | none/ads | 4-8 | 5 | Spotify API terms; no payer |
| O23 | Ambient content channels (ADHD music, cat/baby/senior calm) | Passive viewers | none/ads | 8-12 | 5 | Monetisation threshold, policy risk |
| O22 | Air-pollutant timeline map | Researchers, agencies | none/ads | 8-12 | 5 | No buyer |
| O17 | Gaussian splats: asset marketplace | Game devs, filmmakers | none/ads | 12+ | 5 | Marketplace cold start |
| O18 | [UZ] Gaussian splats: Central Asia heritage scanner | Museums, tourism boards | one-off | n/a | 5 | Public-sector contracts |
| O25 | AI cultural-dress virtual try-on | Brides, bridal shops | usage | 14-20 | 5 | Dataset and model cost |
| O78 | Whiteout (WebGPU sniper FPS) + presets library | PC browser gamers | one-off | 40+ | 5 | Content scope |
| O10 | [UZ] valuation appeal / AVM / property due diligence | UZ valuers, tax advisors | one-off | 8-14 | 5 | Valuation-result feed unavailable |
| O14 | Icon scraper (DX tool) | Developers | none/ads | n/a | 5 | Licence |
| O21 | Gaussian splats: moonshots (4D event capture, game level editor) | Event hosts, game creators | none/ads | n/a | 5 | Hardware rigs, immature pipeline |

## Sources

**Method and comparison**
- [research-protocol](../saas-research-2026-10/research-protocol.md), [ranked-100](../saas-research-2026-10/ranked-100.md), [decision-report](../saas-research-2026-10/decision-report.md), [subscription-speed](../saas-research-2026-10/subscription-speed.md), [products.json](../saas-research-2026-10/products.json) (dimension scores used to calibrate)
- [Venture product order](../../system/planning/pln-tasks.md#venture-product-order) (read only), [parent-company-2026-10](../parent-company-2026-10/parent-company-2026-10.md) (payment rails)

**Idea docs in `ideas/`**
[forever-pin-spec](../forever-pin-spec.md) · [pose-coach-spec](../pose-coach-spec.md) · [ai-photo-director-market-analysis](../ai-photo-director-market-analysis.md) · [transcript-forge-spec](../transcript-forge-spec.md) · [transcript-forge-backend-libs-spec](../transcript-forge-backend-libs-spec.md) · [activity-matcher-spec](../activity-matcher-spec.md) · [route-vibe-player-spec](../route-vibe-player-spec.md) · [spotify-mood-queue-project](../spotify-mood-queue-project.md) · [icon-scraper-spec](../icon-scraper-spec.md) · [gaussian-splatting-spec](../gaussian-splatting-spec.md) · [interactive-3d-web-experiences-spec](../interactive-3d-web-experiences-spec.md) · [uz-geocoder-spec](../uz-geocoder-spec.md) · [cadastre-agency-analysis](../cadastre-agency-analysis.md) · [uz-govtech-demand-map](../uz-govtech-demand-map.md) · [air-pollutant-timeline-map-research](../air-pollutant-timeline-map-research.md) · [passive-income-automation-spec](../passive-income-automation-spec.md) · [city-vision](../city-vision.md) · [3d-print-products-analysis](../3d-print-products-analysis.md) · [nth26-map-vector-analysis](../nth26-map-vector-analysis.md) · [youtube-apps-audit](../youtube-apps-audit.md) · [telegram-features](../telegram-features.md) · [micro-saas-deep-search](../micro-saas-deep-search.md) · [market-analysis](../market-analysis.md) · [startup-research-2026-09 shortlist](../startup-research-2026-09/shortlist-100.md) (origin of the first-ten W-IDs)

**Venture portfolio** (`workbench/ventures/`)
[products-final](../../workbench/ventures/10x-ventures/products-final.md) · [product-ideas](../../workbench/ventures/10x-ventures/product-ideas.md) · [registry README](../../workbench/ventures/10x-ventures/README.md) · [vault spec](../../workbench/ventures/10x-ventures/specs/vault.md) · [idea-forge spec](../../workbench/ventures/10x-ventures/specs/idea-forge.md) · [first-ten](../../workbench/ventures/first-ten.md) · repo files read (first ~40 lines): `product/context.md` or `product/product.md` of ForeverPin, Pose Coach, Transcript Forge, Hijinx, ListingShelf, PBN Studio, Arcade, Museums Gallery, PRISM, sift, Haven, TNIS, TNIS-Mintrans and the ten first-ten repos; `CLAUDE.md` of Whiteout presets, track-2-transportbrain, city-vision; `README.md` of fun-vault, pdf-editor, trademark-watcher-poc, acquisition-explorer-poc, forever-pin-promo, tbs.demo, 10x-fin-nt.

**Web (observed 2026-10-09):** the 70 vendor and platform URLs in the competitor-evidence table above (pricing pages, app-store listings, Spotify developer documentation). Unverified third-party figures are noted there as such and not used in scores.

## Points

- [ ] Should any own idea join the venture order after the four? Nothing scores in the research Validate band (best 61 vs 66-76), so the options are: keep the queue as it is, or run the research's 10-interview / 5-artifact / 3-paid-pilot test on one own slice first (Training Seats as a slice of S026/S029, or the grant pipeline as a slice of S086) before any build.
- [ ] Are Pose Coach (39) and Hijinx (45) kept in the order on speed-to-MRR alone, given they need 835 and 173 paying accounts against 34 for a $149 B2B product? If yes, set a stop rule per product (for example, pack sales or returning-pair counts by a date) so they do not stay current by default.
- [ ] Which of the 23 Drop rows get closed for good (Arcade, Museums Gallery, Whiteout, the Spotify music apps, 3D-print products, ambient channels, Gaussian-splat moonshots, icon scraper)? Closing means no further research or doc upkeep, not deleting repos.
- [ ] Which first-ten prototypes graduate with team workspaces as seeds for researched families (Training Seats, Podcast Readiness, Procedure Review, Customer Promises) and which are archived (Documentation Checker, Config Checker, Vendor Renewals, EPUB Review)?
- [ ] Do the Uzbek-local ideas (geocoder 60, NT auction tracker 44, registry API 46, ListingShelf 41) wait for a Uzbek IE/LLC and Click/Payme, or does the founder open that entity track after the US LLC? The geocoder's 85%-accuracy gold-set gate can be tested without any entity.
- [ ] Ship the 2-4-week developer utilities (cron, webhook relay, accessibility audit, OG image, SSL monitor) at all, for example as free acquisition tools for ForeverPin, or skip them because the evidence shows free and low-cost incumbents and finals of 43-52?
- [ ] Apply the $20-50 cost rule strictly to LLM-per-document ideas (decoders, manuscript, illustrator, splats) and drop them, or allow metered pass-through pricing as the micro-SaaS deep search permitted?
- [ ] Keep Haven gated until a stable $2K MRR (scored 49 here) and keep ListingShelf only as Haven's supply tool, not a standalone product?

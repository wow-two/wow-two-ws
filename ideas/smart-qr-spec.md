# Smart QR — Programmable Codes & Link Router

*Last updated: 2026-05-31*

> Micro-SaaS portfolio product **#002** (`ven-msaas-context.md` → Active). Working name: **Smart QR**.
> Brandable alternatives: **Permacode** ("your code never dies" angle), **RouteQR**, **Scanforge**, **QRForge**, **Codeway**.

## Section 0: Brief Answers (the questions that spawned this)

- **What is it?** A dynamic QR + barcode + short-link builder where each code carries a **programmable routing layer** — the owner defines rules (device, location, time, scan count, language, password, A/B split) and one printed code resolves to different destinations per scan. Core mechanic = link forwarder with a rules engine in front of the redirect.
- **How do we generate the QR?** Pure-C# library **QRCoder** (MIT, zero-dep). Use the `SvgQRCode` and `PngByteQRCode` renderers — both cross-platform, **no `System.Drawing`** (critical, we host on Linux). Barcodes via **ZXing.Net** (QR, Data Matrix, PDF417, Aztec, Code128, EAN/UPC…). Logos/styling composited with **SkiaSharp** or **ImageSharp**. See §6.
- **Do we need to cache the QR? Can it get heavy?** Generation is **cheap and one-time** — microseconds of CPU, a few KB output, produced once at create/edit, never per scan. The **printed image is immutable** → push to object storage + CDN, cache forever. What actually "gets heavy" is the **scan→redirect hot path and analytics ingestion**, not generation. Cache the *routing config* (Redis), not the picture. See §7.
- **What other code/link functionality is useful?** Barcodes (1D + 2D), password-locked links, expiring / scan-capped / one-time links, vCard digital business cards, WiFi codes, app-store routers, menu/PDF hosting, link-in-bio multi-link, GS1 Digital Link (retail, 2027 sunrise), bulk/serialized generation + API. See §5 and §8.

## Section 1: Problem

QR codes went mainstream — 1T+ scans in 2025, ~100M US scanners — and the tooling is a **mature, crowded commodity**: dozens of generators (QR Tiger, Uniqode, Bitly, Flowcode, QRCodeChimp, hovercode…). On the surface there is nothing left to build.

But the category has three persistent, **emotionally-charged** pains that the incumbents *cause* rather than solve:

1. **Codes held hostage.** You print 10,000 flyers / a storefront window / product packaging, then the vendor raises the price, caps your scans, or **deactivates the code when you downgrade** — bricking physical assets you already paid to print. This is the #1 one-star-review theme across the category. A QR code is infrastructure; treating it as a hostage is the original sin of the market.
2. **Smart routing is buried and metered.** The genuinely useful feature — *one code, many destinations by context* — is gated into $30+/mo tiers, hidden behind "Premium," and scan-capped. Most users never reach it.
3. **Five tools for one job.** QR generator + barcode tool + short-link service + digital-business-card app + password-link tool are five subscriptions for what is fundamentally *one primitive: a programmable redirect with a scannable front-end.*

The opportunity is not "another QR generator." It's a **calm, flat-priced, programmable redirect platform** that refuses to brick your codes — the GWDNBM cut of a commodity category.

## Section 2: Market Landscape

### Market size & momentum

- QR market **$13.0B (2025) → $15.2B (2026) → $33.1B (2031)**, ~16.8–20.5% CAGR.
- **Dynamic codes = ~65% share**; ~79% of businesses use dynamic. Editability + analytics is the paid wedge.
- ~99.5M US scanners (2025), ~102.6M projected 2026; usage +323% 2021→2025.
- QR payments trending toward **$3T** annual spend (mostly a payments-rail story, not ours — but signals normalization).
- **GS1 "Sunrise 2027"**: retail migrating 1D barcodes → GS1-powered 2D QR by 2027. A real forward tailwind for a tool that speaks GS1 Digital Link.

### Competitor / pricing map

| Tool | Position | Entry price | Notable gating |
|---|---|---|---|
| QR Tiger | Mature, agency-friendly, 31 solutions | $7/mo (12 codes) | Geo/multi-URL → $37/mo premium |
| Uniqode (ex-Beaconstac) | Enterprise governance, SOC2, SSO | $5/mo | Smart rules + teams up-tier |
| Bitly | Link-mgmt first, QR secondary | ~$8–35/mo | QR is a bolt-on |
| Flowcode | Design-forward, US consumer brands | Free (2 codes) → $5 → $25 → $250 | Code count caps per tier |
| QRCodeChimp / hovercode / QR.io | Mid-market generators | $5–15/mo | Custom domain, API up-tier |
| QRTRAC | **White-label, unlimited scans/users** | custom | Reseller-oriented |
| Scanova, me-qr, QRCodeKIT | Long-tail SEO players | $5–15/mo | Feature-metered |

**Pattern:** entry $5–7/mo, but the three things people actually want — **smart routing, custom domain, unlimited un-capped scans** — are consistently pushed to $25–37+/mo, and several vendors **expire codes on downgrade**. Bulk/API sits at ~$0.23–0.50/code.

### The actual gap

Nobody owns the position **"programmable routing as the headline, on flat pricing, with codes that never die."** Incumbents optimize for tiered up-sell; the GWDNBM thesis says do the opposite and let the calmness *be* the marketing.

## Section 3: Concept

**One scannable code → a programmable redirect you fully control. Print it once; reprogram it forever; it never expires on you.**

The product is a thin, fast **redirect engine** with three surfaces stacked on top:

1. **The front-end code** — QR (styled, logo'd), or any barcode type, or a plain short link. Immutable once printed.
2. **The routing layer (the soul)** — an ordered rule set the owner programs: *if device/location/time/language/scan-count/referrer/A-B-bucket matches → go here; else fallback.* No-code visual builder, with a JSON + API escape hatch for developers.
3. **The analytics layer** — every scan logged (time, geo, device, OS, unique vs repeat) into a calm dashboard. No engagement nags, just the data.

Mental model: **"Cloudflare-Workers-for-physical-codes, minus the complexity"** — but the pitch to a normal user is *"a QR code that's smart enough to do the right thing for whoever scans it, and that you'll never have to reprint."*

## Section 4: Target Users

**Primary — SMBs & solo operators with physical surfaces:**
- Restaurants/cafés (menu by time-of-day; review-gating), retail, real-estate signage, event organizers, gyms, clinics.
- They print once and need *edit-after-print* + *never-expires* far more than they need 40 features.

**Secondary:**
- **Developers / indie makers** — want an API + custom domain + flat price without enterprise sales. Underserved sweet spot.
- **Marketers / small agencies** — A/B routing, UTM injection, per-campaign analytics, white-label for clients.
- **App publishers** — one "Download" code that routes iOS→App Store, Android→Play, desktop→landing.

**Not the target (v1):**
- Enterprise governance buyers (SSO/SOC2/audit) — Uniqode owns it; long sales cycles.
- Pure payments QR (bank/PSP rail) — regulated, different game.
- Free-only consumers generating one static code — no WTP; serve them as funnel, not customers.

## Section 5: Features

### MVP — the programmable redirect (Month 1)

- Create a **dynamic QR** → short URL on our domain → editable destination (change after print, no reprint).
- **Styled output**: colors, error-correction level, **center logo**, rounded modules; export SVG + PNG (and PDF).
- **Routing rules v1**: device/OS, country (IP-geo), time-of-day/day-of-week, fallback. Top-down, first-match-wins, visual builder.
- **Short links** (same engine, no code) + **password-locked links** (interstitial gate).
- **Scan analytics**: total/unique, time series, by country/device/OS, top hours.
- **Custom domain** support from a cheap tier (CNAME `qr.brand.com`) — *not* gated to enterprise.
- Account, billing (Stripe), "export everything / delete everything."
- **Promise baked in: codes never expire and never deactivate on downgrade.** (Free codes keep redirecting; you just lose editing/analytics if you stop paying — you never lose the redirect.)

### V2 — code & content breadth (Month 2–3)

- **Barcode types** via ZXing.Net: Code128, EAN-13/UPC-A, Data Matrix, PDF417, Aztec.
- **Content-type templates** (QRCoder payloads): vCard digital business card, WiFi join, geo, email/SMS, calendar event, app-store router, "menu/PDF" hosting.
- **Link-in-bio / multi-link** landing page (one code → mini link hub).
- **Expiring / scan-capped / one-time (self-destruct) links.**
- **Bulk generation** (CSV in → ZIP of codes out) + serialized data (unique payload per row).

### V3 — routing power + reach (Month 4–6)

- **Advanced rules**: language (Accept-Language), AND/OR condition groups, scheduled windows, **A/B split with % weighting**, unique-vs-repeat-scanner, referrer/UTM rules, retargeting-pixel injection.
- **Public REST API** + API keys (developer tier) — generate, update destination, read analytics.
- **White-label** (agency tier): client workspaces, custom-domain per client, branded interstitials.
- **GS1 Digital Link** generator (retail/CPG; rides the 2027 sunrise).
- Webhooks on scan (Zapier/Make-style integrations, calm digest export).

### Future / aspirational

- Geofenced rules at city/radius granularity; weather/inventory-driven routing (data-source dependent).
- NFC tag pairing (same routing engine, tap instead of scan).
- Self-host / Docker edition (wow-two dogfood; appeals to dev segment + privacy buyers).

## Section 5b: The Routing Engine (the differentiator — deep dive)

A code owns: `rules[] (ordered)` + `fallbackUrl` + optional `password`, `expiry`, `maxScans`.

**Rule** = `{ when: Condition[], then: destinationUrl, weight? }`. Conditions evaluated **top-to-bottom, first full match wins**; if none match → `fallbackUrl` (the safety net so *every* scan resolves somewhere).

| Dimension | Source (server-side, no app/GPS prompt) | Example |
|---|---|---|
| Device / OS | `User-Agent` parse | iOS→App Store, Android→Play, desktop→web |
| Country / region / city | IP-geo (local MaxMind GeoLite2 DB) | route to nearest store / localized site |
| Language | `Accept-Language` header | EN/RU/UZ landing variants |
| Time / day | server clock + code timezone | lunch menu <16:00, dinner after |
| Scan count / sequence | counter in config store | first 100 scans → "early-bird coupon" |
| Unique vs repeat | first-party cookie | new visitor → intro; repeat → loyalty |
| Referrer / UTM | request headers / query | per-channel attribution split |
| A/B bucket | weighted random, sticky by cookie | 50/50 landing test |
| Password | interstitial challenge | gated PDF / private link |

**Two UX modes:** *Simple* (one-click presets: "App Store Router," "Menu by Time," "Geo Store Finder," "A/B Test") and *Advanced* (full visual rule builder). **Dev escape hatch:** the same rule set is just JSON, settable via API — this is the wedge for the developer segment incumbents ignore.

> This is what the user meant by *"conditions built-in so users can program different things."* It is the headline, not a hidden premium toggle.

## Section 5c: Styling, Logos & Animation

The visual layer — a design-forward differentiator (Flowcode competes here; animation leapfrogs it). Reference: a Telegram contact QR — gradient rounded modules, center logo in a knockout, frame + caption.

**Static styling (MVP+ — center-logo compositing already built in the POC `SmartQr.Codes`):**
- **Center logo / pfp** in a cleared **circular knockout** (+ optional white ring) so an avatar reads cleanly — what Telegram does. EC level H so the matrix survives occlusion. Source: upload **or** pull-from-URL (their avatar).
- Module shape (square / rounded / dots), foreground gradient, custom or transparent background.
- **Frames + caption** — border, top badge, bottom CTA/handle ("@handle", "Scan me").
- **Sanitize uploads** — re-encode raster + strip EXIF; never trust uploaded SVG (XSS, see §6).

**Animated codes / GIF export (V2–V3, paid gate — the viral angle):**
- **Animate the logo / background / frame; keep the matrix static** so it always scans (the Telegram model). Draw-on/settle intros OK if they hold on a valid resting frame. **Frame 1 must be a fully valid code** (some platforms show only the first GIF frame). Use **EC level H** + a contrast floor; test across native iOS/Android + 3rd-party scanners.
- Formats: **GIF** (universal, native via ImageSharp — already a dependency), **animated WebP / APNG** (smaller, full color — verify encoder support), **MP4/WebM** later via FFmpeg (smallest for complex), **animated SVG / Lottie** for web embeds. Always emit a **static PNG/SVG fallback**.
- Use cases: stories/chat (Telegram, WhatsApp, Slack), email signatures, digital signage, video intros — "use your QR as a GIF anywhere."

**Performance:** animated generation is the **first genuinely heavy op** (static QR is ~free). Render **async/queued** (never block the request), **generate-once → object storage → CDN**, cap frames/dimensions/duration, gate behind Pro. Still **Tier 0** (no AI — pure CPU), just "heavy Tier 0."

## Section 6: Technical Architecture

### Stack (wow-two-aligned)

| Layer | Tech | Notes |
|---|---|---|
| API / app backend | **.NET 9**, Clean Architecture, MediatR | `wow-two-apps.smart-qr` |
| **Redirect service** | Separate slim ASP.NET Core minimal-API process | Stateless, horizontally scalable, the only hot path |
| QR generation | **QRCoder** (MIT, zero-dep) — `SvgQRCode`, `PngByteQRCode` | **No System.Drawing** → Linux-safe |
| Barcodes | **ZXing.Net** (QR, DataMatrix, PDF417, Aztec, Code128, EAN/UPC) | SkiaSharp/ImageSharp bindings |
| Styling / logo compositing | **SkiaSharp** or **ImageSharp** | overlay logo, rounded modules, gradients |
| Config store (hot) | **Redis** — slug → {rules, fallback, flags} | O(1) redirect, no DB on hot path |
| Primary DB | **Postgres** (codes, users, rules, billing) | platform `data.relational` |
| Analytics store | append-only events → **ClickHouse** *or* partitioned Postgres | decoupled from redirect |
| IP-geo | **MaxMind GeoLite2** loaded in-memory | never an external call on hot path |
| Image storage / CDN | Object storage (R2/S3/Blob) behind **Cloudflare CDN** | immutable images cached at edge |
| Frontend | **React** + Tailwind + shadcn/ui; visual rule builder + analytics dash | `wow-two-apps.smart-qr` |
| Auth / billing | Own accounts + **Stripe** (UZ later: Click/Payme adapter) | standard |
| Queue / jobs | platform `comms.infra`; bulk gen on worker | CSV→ZIP, webhooks |

### Generation, concretely (answers "how do we generate the QR?")

```csharp
// QR → SVG (scalable, tiny, Linux-safe, no System.Drawing)
using var gen = new QRCodeGenerator();
var data = gen.CreateQrCode(shortUrl, QRCodeGenerator.ECCLevel.Q); // Q = 25% EC, room for a logo
string svg = new SvgQRCode(data).GetGraphic(20);

// QR → PNG bytes (raster, also Linux-safe)
byte[] png = new PngByteQRCode(data).GetGraphic(20);
// Logo overlay → composite `png` with SkiaSharp over the center (EC level Q/H tolerates occlusion)
```

- **Vector-first pipeline.** Canonical source of truth = the QR **matrix** (boolean grid, derivable from the slug) — *not* an image. From one matrix, render SVG / PNG / PDF on demand (`SvgQRCode` / `PngByteQRCode` / `PdfByteQRCode`). "Investing in SVG" is therefore near-free — it's a render choice, not a separate build.
  - **SVG = the working/design format**: infinite print scale (card→billboard, generate once), ~1–10 KB, and **live re-style in the React builder** (background, foreground "filler" color, gradient, transparent bg, dot/rounded modules, logo) with zero regeneration — the core builder UX *and* a classic paid-tier export gate.
  - **Still ship raster + print formats**: PNG/JPG (many platforms / POS / label printers reject SVG) and PDF/EPS for print shops. Emit SVG as a single merged `<path>` (not per-module `<rect>`) to keep it tiny; **sanitize any user-uploaded logo SVG** (XML → `<script>`/XXE = XSS risk); convert frame/CTA fonts to paths. Note: **format ≠ scannability** — quiet zone, contrast, EC level, and min module size govern that; SVG only preserves fidelity at scale.
- **Error correction level Q or H** when a center logo is present (higher EC = more redundancy = logo can occlude the middle and it still scans).
- Barcodes: `new BarcodeWriterSvg { Format = BarcodeFormat.DATA_MATRIX, ... }.Write(payload)` etc.
- QRCoder ships **23+ payload generators** (URL, WiFi, vCard/MeCard, geo, email, SMS, calendar, crypto, payment, OTP) — covers most content-type templates for free.

### Redirect hot path (the only thing that scales)

```
[Scan] → GET r.smartqr.app/{slug}
   → Redis lookup {slug} (rules + fallback)        ~sub-ms, no DB
   → evaluate rules (UA parse, in-mem geo, clock)  ~µs
   → emit scan event to queue/buffer (fire-&-forget, non-blocking)
   → 302 → destination                              total < ~10ms
```

The redirect process holds **no business logic beyond resolve+log**. It can be replicated cheaply and even pushed to the edge (Cloudflare Worker shim) later. Analytics writes **never** block the 302.

### Data model (sketch)

- `Code` — slug, owner_id, type (qr/barcode/link), image_ref, style, created_at, **never_expires=true**
- `Rule` — code_id, order, conditions(jsonb), destination, weight
- `CodeConfig` (Redis mirror) — slug → {rules, fallback, password_hash?, expiry?, max_scans?}
- `ScanEvent` — code_id, ts, ip_country, device, os, ua_hash, is_unique, referrer (append-only, analytics store)
- `User`, `Workspace`, `ApiKey`, `Subscription`

## Section 7: Performance & Caching (the user's explicit question)

**Does generation get heavy? No.** A QR matrix is built in microseconds; rendering to SVG/PNG is sub-ms to low-single-digit ms; output is a few KB. It happens **once** at create/edit time, never per scan. So:

- **Don't cache to save generation CPU — there's nothing to save.** Cache because the **image is immutable**: a printed code's slug never changes, so the rendered PNG/SVG is a perfect static asset → store once in object storage, serve via **CDN, `Cache-Control: immutable, max-age=1y`**. Origin generates each image exactly once in its life.

**What actually gets heavy** is the **scan→redirect path and analytics ingestion** — and it can spike *violently*. A code on TV, a billboard, or packaging can do millions of scans in minutes (cf. Coinbase's bouncing-QR Super Bowl ad melting their app). Engineering follows from that:

| Concern | Risk | Mitigation |
|---|---|---|
| Redirect throughput | every scan = a request; viral burst | **Redis-cached config**, stateless redirect workers behind LB, horizontal autoscale; optional edge worker |
| DB on hot path | per-scan DB read = bottleneck | never read primary DB on redirect — Redis only; DB is write-behind for config edits |
| Geo lookup latency | external geo API = +100ms + cost + dependency | **local MaxMind GeoLite2 in memory** |
| Analytics writes | per-scan synchronous insert = write storm | **fire-and-forget to queue / ring buffer**, batch-flush to ClickHouse/partitioned Postgres; redirect returns before the write lands |
| Hot "viral" key | one slug, millions of hits | Redis handles it; counters via atomic INCR or approximate (HLL) for unique counts |
| Image bandwidth | re-serving images | CDN edge cache, immutable; origin barely touched |

**One-liner for the user:** *generation is free and one-time → CDN the static image; the redirect + analytics is the real load → cache the routing config in Redis and make analytics async. Cache the decision, not the picture.*

## Section 8: Code & Content Types (the "what else" catalog)

### Code formats (one tool, every symbology)

| Format | Class | Primary use | Lib |
|---|---|---|---|
| QR | 2D | marketing, links, payments, everything | QRCoder |
| Data Matrix | 2D | industrial / pharma / small-part marking, GS1 | ZXing.Net |
| PDF417 | 2D | IDs, driver licenses, boarding/tickets (1.1KB data) | ZXing.Net |
| Aztec | 2D | transport tickets (no quiet zone, robust low-res) | ZXing.Net |
| Code128 / Code39 | 1D | logistics, asset/inventory labels | ZXing.Net |
| EAN-13 / UPC-A | 1D | retail products | ZXing.Net |
| **GS1 Digital Link** | 2D (QR) | retail/CPG — POS + traceability + consumer in one code | QRCoder + GS1 URI builder |

### Content types (QR payload templates — mostly free via QRCoder)

URL · **vCard digital business card** · **WiFi join** · app-store router · menu/PDF host · geo location · email / SMS · calendar event · **link-in-bio multi-link** · coupon · payment (EPC/PayNow/UPI) · crypto · OTP/2FA · feedback form.

### Link primitives (the "link forwarder" surface, no code required)

Short link · **password-locked link** · **expiring link** · **scan/click-capped link** · **one-time self-destruct link** · UTM-injecting link · geo/device-routed link (same engine as QR).

> vCard digital business cards (Popl/HiHello/Blinq are whole companies) and password/expiring links (Password.link, SPRL) are each standalone SaaS categories. Folding them in makes Smart QR a **unified redirect platform**, not a single-trick generator — and each is a separate SEO/long-tail acquisition surface.

## Section 9: Economics

### Tier policy: **Tier 0** (zero AI cost)

Pure compute + storage + bandwidth. No LLM in the hot path → fat margins, fits the portfolio's ~70% Tier-0 lane.

### Unit cost (effectively nil)

| Item | Cost |
|---|---|
| Generate a code (one-time) | ~0 (µs CPU, KBs) |
| Store + CDN-serve image | fractions of a cent/code/mo |
| Redirect + log per scan | ~0 (Redis + async write); amortized box share |
| Marginal cost per customer | dominated by Stripe fees, not infra |

Shared infra = the existing single Hetzner box behind Cloudflare, multi-tenant by domain (per portfolio convention). Per-product budget $20–50 (domain + box share).

### Pricing (refines dashboard anchor $5 Solo / $15 Pro)

| Plan | Price | For | Includes |
|---|---|---|---|
| Free | $0 | funnel / tinkerers | 3 dynamic codes, **unlimited scans**, basic analytics, **codes never expire** |
| Solo | **$5/mo** | SMB / solo | 25 codes, smart routing, custom domain, full analytics |
| Pro | **$15/mo** | marketers / power | 200 codes, A/B + advanced rules, bulk gen, all code/content types |
| Dev/Agency | **$39–49/mo** | devs / agencies | API, white-label, client workspaces, webhooks |

**Deliberate anti-incumbent moves:** unlimited scans on *every* tier (incl. free); custom domain + smart routing from the **$5** tier (not $30+); **codes never deactivate on downgrade.** These are the marketing.

### Projection (micro-SaaS pace, conservative)

| Milestone | Timeline | MRR | Kill-gate |
|---|---|---|---|
| MVP + 1 paying customer | Wk 4 | ~$5–15 | **G1** |
| ~20 paying | Mo 3 | ~$150 | **G2** ($100) |
| ~70 paying | Mo 6 | ~$600 | **G3** ($500) |
| ~250 paying + a few agency | Mo 12 | ~$2.5K | **G4** ("hit") |

Margins ~95%+ given Tier-0 costs; the constraint is **distribution in a crowded market**, not unit economics (see §10).

## Section 10: Risks & Mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| **Commoditized, crowded, SEO-moated market** | **High** | Don't fight on "QR generator." Win on a *position*: programmable-routing-first + never-expire + flat price. Long-tail SEO via content-type sub-pages (vCard, WiFi, GS1…). Dev segment via API (incumbents weak here). |
| Low WTP at the bottom | Medium | Free tier is funnel only; monetize routing/custom-domain/API. Anchor on "never reprint" cost-avoidance, not feature count. |
| Incumbent free tiers | Medium | Our free tier's *unlimited scans + never-expire* is already better than most paid tiers' fine print — that contrast is the hook. |
| Trust on a no-name redirect domain (phishing assoc.) | Medium | Custom domains, branded interstitials, abuse scanning (Safe Browsing API), clear ToS, fast takedown. |
| Abuse: malware/phishing redirects | **High (ops)** | Destination scanning, rate limits, report flow, KYC on volume. Non-negotiable for a redirect business. |
| Big player bundles it (Cloudflare/Bitly/Google) | Medium | Stay niche-deep (routing UX + never-expire promise + UZ payments); switching cost via printed-asset lock-in *to the customer's benefit*, not ours. |
| Slug/short-domain reputation blocklisting | Medium | Multiple redirect domains, custom-domain-first, monitor blocklists. |
| GDPR (IP/geo logging) | Medium | IP hashed not stored raw, configurable retention, cookie-less mode, "delete everything." |

## Section 11: Wow-Two Integration

### New repo

| Repo | Org | Purpose |
|---|---|---|
| `wow-two-apps.smart-qr` | wow-two-apps | Full product — .NET backend (app API + redirect service) + React frontend |

### Candidate extractable SDK libs (beta)

- `Wow.Two.Sdk.Beta.Codes` — thin façade over QRCoder + ZXing.Net (unified `ICodeRenderer` for QR/barcode/SVG/PNG, logo compositing). Reusable across future products.
- `Wow.Two.Sdk.Beta.Routing` — the rule-evaluation engine (conditions → destination), framework-agnostic.

### Reuses existing wow-two packages

- `wow-two-platform.comms.infra` — MediatR pipelines, bulk-gen jobs
- `wow-two-platform.data.relational` — EF Core (Postgres)
- `wow-two-platform.storage.cache` — Redis config cache
- `wow-two-platform.storage.file` — image object storage
- `wow-two-platform.pipelines` — CI/CD

### Strategic fit

Second consumer-facing product on the stack (with TranscriptForge). **Pure Tier-0** → proves the wow-two stack can ship a lean, high-margin SaaS with no AI dependency. The redirect service is a clean reference impl of "slim hot-path microservice on the platform."

## Section 12: Competitive Differentiation

| Dimension | Smart QR | QR Tiger | Uniqode | Bitly | Flowcode |
|---|---|---|---|---|---|
| Programmable routing as headline | ✅ core | up-tier | up-tier | limited | limited |
| Smart rules + custom domain from $5 | ✅ | ❌ ($37) | partial | ❌ | ❌ |
| **Codes never expire / deactivate** | ✅ promise | ❌ | ❌ | ❌ | code-cap |
| Unlimited scans on free tier | ✅ | ❌ | ❌ | ❌ | ✅ |
| Developer API + flat price (no sales) | ✅ | partial | enterprise | partial | ❌ |
| All code types (1D+2D+GS1) + links | ✅ | partial | partial | links-first | ❌ |
| vCard / password / expiring links unified | ✅ | partial | partial | partial | ❌ |
| Logo/pfp knockout + frames | ✅ | partial | partial | ❌ | ✅ |
| Animated / GIF code export | ✅ (V2) | ❌ | ❌ | ❌ | partial |
| GWDNBM (no caps-as-hostage, no nags) | ✅ | ❌ | ❌ | ❌ | ❌ |
| Enterprise governance (SSO/SOC2) | ❌ (later) | partial | ✅ | partial | partial |

**Positioning line:** *"A QR code smart enough to route every scan to the right place — and that you'll never have to reprint. Programmable routing, every code type, one flat price. Your codes, forever."*

## Section 13: Open Questions

1. **Name** — lead with literal "Smart QR" (SEO-honest) or a brand (**Permacode** leans hard into the never-expire wedge, which is the most defensible angle)?
2. **Wedge feature for launch** — is "never-expire + smart routing from $5" enough, or do we need one viral content-type (vCard cards? GS1?) as the SEO spear-tip?
3. **Redirect domain strategy** — single branded short domain vs custom-domain-first from day 1 (better trust, more setup friction)?
4. **UZ or global first?** Routing/never-expire is global; but UZ payments (Click/Payme) + local SEO could be an easier first beachhead. Portfolio leans "global for this one."
5. **Abuse tolerance** — how much moderation infra before launch? (A redirect service *will* attract phishing; under-investing here is reputational ruin.)
6. **Edge redirect now or later?** Start with a .NET redirect service on the box; move hot path to a Cloudflare Worker only if a viral code forces it.
7. **Self-host edition** — ship a Docker edition early for the dev/privacy segment, or keep hosted-only until G3?

## Section 14: Adheres to GWDNBM

Aligned with [GWDNBM principle](../../../../../.claude/projects/-Users-max-Projects-10x-ws-workbench-career-engineering-wow-two-wow-two-ws/memory/principle_gwdnbm.md) — and here it's not just compliance, it's the **core differentiator**:

- **No hostage codes** — codes never deactivate or expire on downgrade; the redirect keeps working even on a lapsed account. The opposite of every incumbent.
- No scan caps used as a paywall lever (the industry's quiet tax).
- No ad emails, no "you got a scan!" engagement nags — analytics is opt-in pull, calm dashboard only.
- Transparent flat pricing on signup; cancel anytime, export everything, delete everything.

## Section 15: Status & Next Steps

**Status:** `building` (portfolio #002). Backend POC scaffolded **2026-06-03** at `workbench/ventures/smart-qr-poc/` — full Haven-style Clean Arch (6 projects + tests, 98 files), builds clean, **8 unit tests green** (QR/barcode generation + routing engine). Chose **POC-first** over the shared template repo (validate the crowded-market wedge before sinking time into shared infra).

### Done (POC, 2026-06-03)

- ✅ **Clean Arch backend** mirroring Haven: `SmartQr.Common` (mediator/result/ApiResponse), `.Common.Domain` (entities+enums), `.Common.Persistence` (EF Core + Npgsql, snake_case, enums-as-text), `.Codes` (generation lib), `.Api` (management CQRS API), `.Redirect` (minimal-API hot path), `.Tests`.
- ✅ **Generation proven** — QRCoder `SvgQRCode`+`PngByteQRCode` (cross-platform, no System.Drawing), ZXing.Net barcodes → SVG, ImageSharp logo overlay. Unit-tested (valid SVG markup + PNG signature).
- ✅ **Routing engine** — ordered rules (device/country/language/time-of-day), first-match-wins, fallback, never-expire override, 404/410 gating. Unit-tested.
- ✅ **Hot-path design** — `IRedirectConfigStore` (in-memory cache default / Redis production), pure `RoutingEvaluator`, async `ChannelScanRecorder` + batched flush worker (302 never waits on a DB write).
- ✅ **Data path integration-tested** — SQLite in-memory covers persistence (`CodeRepository`), the create-command path, and redirect resolution (config store → evaluator). **16 tests green**; both services boot + serve `/health`.
- ✅ **Frontend MVP** (2026-06-03) — Create-Code builder (React 19 + Tailwind v4 on `@wow-two-beta/ui`); the Api serves the built SPA at its root.
- ✅ **Runtime DB + live end-to-end** (2026-06-09) — startup auto-creates the Postgres DB + schema; **verified create → persist → SVG/PNG render against real Postgres.**

### Next steps

1. ✅ **DB schema** — runtime bootstrap (`EnsureCreated`, enums-as-text) auto-creates DB + tables; verified vs Postgres. Move to **EF Migrations** when the schema starts evolving.
2. **Validate the wedge** — confirm "never-expire + cheap smart routing" resonates vs incumbents (scan r/smallbusiness, r/restaurateur, IndieHackers for hostage-code complaint volume).
3. **Redirect load test** — synthetic burst (100k scans/min) against the cached redirect to validate the §7 architecture; wire the Redis config-writer side in the API.
4. **Geo** — swap `NoopGeoResolver` for a MaxMind GeoLite2 in-memory lookup to activate country rules.
5. ✅ **Frontend MVP** — Create-Code builder (React + `@wow-two-beta/ui`, Api-served). **Next:** name + domain (`Permacode`?), more screens (codes list, scan analytics).
6. Hold barcodes/GS1/API/white-label polish for V2+ — MVP is *one programmable QR that never dies*.

---

### Research sources (2026-05-31)

- Market size & stats: [Mordor Intelligence](https://www.mordorintelligence.com/industry-reports/qr-codes-market), [Wave Connect](https://wavecnct.com/blogs/qr-code-statistics), [QR-Verse](https://qr-verse.com/en/blog/qr-code-statistics-2026)
- Competitors/pricing: [QR Tiger vs Uniqode](https://www.qrcode-tiger.com/qrtiger-vs-beaconstac), [QR Code Generator pricing](https://www.qr-code-generator.com/pricing/), [Flowcode](https://qrlynx.com/blog/best-dynamic-qr-code-generators), [QRTRAC white-label](https://qrtrac.com/comparisons/fair-pricing-qr-code-generator/)
- Smart routing: [Uniqode smart rules](https://docs.uniqode.com/en/articles/8494786-create-condition-based-qr-codes-using-smart-rules), [QRLynx smart redirect](https://qrlynx.com/smart-redirect-rules-qr-code), [Geotargetly](https://geotargetly.com/blog/qr-code-redirect-guide)
- Redirect architecture: [Delivr 302 mechanics](https://delivr.com/faq/1506/how-is-the-short-url-redirection-made-in-a-dynamic-qr-code), [Supercode tracking](https://www.supercode.com/blog/qr-code-tracking)
- Barcodes/GS1: [Scandit barcode types](https://www.scandit.com/resources/guides/types-of-barcodes-choosing-the-right-barcode/), [Dynamsoft 1D/2D](https://www.dynamsoft.com/blog/insights/the-comprehensive-guide-to-1d-and-2d-barcodes/), [GS1 Digital Link](https://www.gs1.org/standards/gs1-digital-link)
- .NET generation: [QRCoder](https://github.com/Shane32/QRCoder) (MIT), [ZXing.Net](https://github.com/micjahn/ZXing.Net), [Net.Codecrete.QrCodeGenerator](https://www.nuget.org/packages/Net.Codecrete.QrCodeGenerator/)
- Content types: [Supercode QR types](https://www.supercode.com/blog/qr-code-types); password/expiring links: [Password.link](https://password.link/en), [SPRL](https://insprl.com/tools/temporary-link-generator)

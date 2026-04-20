# Passive Income Automation — Multi-Project Spec

*Last updated: 2026-04-20 09:30 PM*

## Section 1: Vision

Build a portfolio of automated passive income projects — content channels + micro-SaaS tools — using code to eliminate manual work. Target: $5-10K/mo combined passive income within 18 months.

### Inspiration

"Relax My Dog" — $1M/year YouTube channel. 2M subs, 800K views/mo, $1K starting cost. Founder: Amman Ahmed (Music For Pets). Started 2017. Fully automated ambient content for anxious dogs.

**Why it works:** evergreen demand, near-zero marginal cost, insane watch time (8-15hr videos), algorithm-friendly, multiple revenue streams (AdSense + Spotify + licensing).

### Core Principle

The value isn't in content quality — it's in **occupying a niche early** with enough volume to become the default. Code automates the volume.

---

## Section 2: Project Portfolio

### Tier 1: Automated Content Channels (Low Risk, Proven Model)

Each channel follows the same pattern: AI-generated audio/visuals → automated upload → passive AdSense.

#### P1: ADHD Focus Music

- **Niche:** Focus/productivity music specifically for ADHD community
- **Why:** Massive underserved community (ADHD content growing 300%+ on YT), high engagement, binaural/lo-fi fully automatable
- **Competition:** Generic "lo-fi" is saturated, but ADHD-specific dedicated channels are few
- **Content:** AI-generated binaural beats, brown noise variations, lo-fi with specific Hz frequencies research shows help ADHD focus
- **Revenue model:** AdSense (long-form = high CPM), Spotify distribution, affiliate (focus apps, supplements)
- **RPM estimate:** $5-8 (health/wellness adjacent)
- **Automation potential:** 95% — music generation + thumbnail + scheduling all scriptable

#### P2: Cat Calming Content

- **Niche:** "Relax My Dog" but for cats — no equivalent exists at scale
- **Why:** 600M+ pet cats worldwide, cat owners search for calming content, zero dominant player
- **Content:** Cat-specific frequencies (25-50Hz purr range), nature visuals, fish/bird TV for cats
- **Revenue model:** AdSense, Spotify, merch (eventually)
- **RPM estimate:** $3-6
- **Automation potential:** 90%

#### P3: Senior Wellness Ambient

- **Niche:** Gentle content for 55+ — memory care, relaxation, nature
- **Why:** 55+ is YouTube's fastest-growing demographic, virtually no dedicated creators, high purchasing power = premium advertisers
- **Content:** Gentle nature sounds, nostalgic ambient (50s-70s era backgrounds), guided gentle movement audio
- **RPM estimate:** $6-12 (senior/health advertisers pay premium)
- **Automation potential:** 85%

#### P4: Baby Sleep (Age-Segmented)

- **Niche:** Sleep sounds segmented by baby age (newborn, 3mo, 6mo, 1yr)
- **Why:** Generic "baby sleep" exists but age-specific is rare — parents search by age
- **Content:** White/pink noise calibrated to developmental stage, heartbeat sounds for newborns
- **RPM estimate:** $4-7
- **Automation potential:** 90%

### Tier 2: AI-Powered SaaS Tools (Higher Upside, More Effort)

#### S1: AI Garden/Landscape Visualizer

- **What:** Upload yard photo → get AI-generated seasonal garden plan with plant recommendations
- **Why:** No serious player exists. Renovation visualizers are crowded (RoomGPT, Remodel AI), but outdoor/garden is empty.
- **Tech:** Image-to-image model (SDXL/Flux) fine-tuned on garden transformations, plant database API, climate zone matching
- **Revenue model:** Freemium SaaS — free 3 renders, $9.99/mo unlimited, $29.99/mo pro (contractor features)
- **Market size:** $100B+ global gardening market, no AI tool serving it well
- **Stack:** .NET backend (wow-two platform), React frontend, Azure AI Services or self-hosted model

#### S2: AI Cultural Dress Virtual Try-On

- **What:** Upload selfie → try on traditional dresses from different cultures (Uzbek, South Asian, Middle Eastern, etc.)
- **Why:** Wedding market in Central/South Asia is massive and completely undigitized. Emotional purchase = high conversion.
- **Tech:** Virtual try-on model (similar to IDM-VTON), cultural dress dataset, body pose estimation
- **Revenue model:** Per-render or subscription. B2B for bridal shops.
- **Stack:** Python ML pipeline, .NET API gateway, React frontend

### Tier 3: Micro-SaaS (Boring but Profitable)

#### M1: AI Menu Translator for Restaurants

- **What:** Restaurant uploads menu → gets multi-language translation with food photos auto-matched
- **Why:** Tourism booming globally, restaurants need this, no good tool exists
- **Revenue:** $20-50/mo per restaurant
- **Automation potential:** High — mostly API orchestration (translation + image matching)

---

## Section 3: Technical Architecture

### Content Automation Pipeline (Tier 1 channels)

```
[Music Generator] → [Visual Generator] → [Compositor] → [Metadata/SEO] → [YouTube Upload API]
     ↓                     ↓                    ↓                ↓
  Suno/Udio API      Stable Diffusion      FFmpeg           Title/desc/tags
  or custom model     + motion effects     assembly          GPT-generated
```

#### Core Components to Build

| Component | Purpose | Tech |
|---|---|---|
| `AudioForge` | Generate ambient tracks (binaural, lo-fi, nature) | Suno API / AudioCraft / custom |
| `VisualFlow` | Generate/animate background visuals | SDXL + motion (Deforum / AnimateDiff) |
| `Compositor` | Combine audio + video + overlays | FFmpeg pipeline |
| `MetaGen` | SEO-optimized titles, descriptions, tags | LLM API (Claude/GPT) |
| `Uploader` | Scheduled YouTube/Spotify uploads | YouTube Data API v3, Spotify for Artists |
| `Analytics` | Track views, revenue, growth per channel | YouTube Analytics API → dashboard |
| `Orchestrator` | Cron-based pipeline runner | .NET worker service or Azure Functions |

#### Pipeline Flow

1. **Generate** — AudioForge creates N tracks per niche per week
2. **Visualize** — VisualFlow generates matching ambient visuals
3. **Compose** — Compositor combines into 1hr-10hr videos
4. **Optimize** — MetaGen generates SEO metadata
5. **Publish** — Uploader schedules across channels
6. **Monitor** — Analytics tracks performance, flags underperforming content

### SaaS Architecture (Tier 2-3)

Standard wow-two stack:
- **Backend:** .NET 8, Clean Architecture, MediatR pipeline, EF Core
- **Frontend:** React + TailwindCSS
- **AI:** Azure AI Services / self-hosted models
- **Infra:** Azure (Functions, Blob Storage, SQL), GitHub Actions CI/CD

---

## Section 4: Execution Plan

### Phase 1: Content Channels MVP (Month 1-2)

- [ ] Build AudioForge — basic ambient track generation
- [ ] Build Compositor — FFmpeg video assembly pipeline
- [ ] Build Uploader — YouTube Data API integration
- [ ] Launch Channel P1 (ADHD Focus) — 30 initial videos
- [ ] Launch Channel P2 (Cat Calming) — 20 initial videos

### Phase 2: Scale Content + Start SaaS (Month 3-4)

- [ ] Automate full pipeline (generate → upload on schedule)
- [ ] Launch P3 (Senior Wellness) and P4 (Baby Sleep)
- [ ] Target: 3-5 videos/week per channel automated
- [ ] Begin S1 (Garden Visualizer) — model fine-tuning + MVP

### Phase 3: Monetize + Expand (Month 5-8)

- [ ] YouTube monetization threshold (1K subs + 4K watch hours per channel)
- [ ] Spotify distribution for all audio content
- [ ] Launch S1 (Garden Visualizer) beta
- [ ] Evaluate which channels are growing — double down, kill underperformers

### Phase 4: Optimize (Month 9-18)

- [ ] Analytics-driven content optimization
- [ ] Multi-platform expansion (TikTok ambient, Spotify playlists)
- [ ] S1 paid launch
- [ ] Evaluate S2 / M1 based on capacity

---

## Section 5: Economics

### Startup Costs

| Item | Monthly Cost |
|---|---|
| AI music generation API | $50-100 |
| Image generation (GPU / API) | $50-100 |
| Cloud hosting (Azure) | $20-50 |
| Domain + misc tools | $20 |
| **Total** | **$140-270/mo** |

### Revenue Projections (Conservative)

| Milestone | Timeline | Monthly Revenue |
|---|---|---|
| 4 channels launched | Month 2 | $0 (pre-monetization) |
| First monetization | Month 6-8 | $200-500 |
| Channels growing | Month 12 | $1,000-2,500 |
| SaaS launched | Month 8-10 | $500-1,000 |
| Portfolio mature | Month 18 | $3,000-8,000 |

### Break-even: Month 8-10

---

## Section 6: Risks & Mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| YouTube AI content policy tightening | High | Add human curation layer, original compositions, unique visual style |
| Niche too small | Medium | Test 4 channels, kill underperformers fast |
| AI music quality insufficient | Medium | Hybrid approach: AI base + manual polish |
| SaaS takes too long to build | Low | Tier 1 channels are the main play; SaaS is bonus |
| Copyright claims on AI audio | Medium | Use models trained on royalty-free data, keep generation logs |

---

## Section 7: wow-two Integration

These projects can be built on the wow-two ecosystem:

- **Orchestrator** → `wow-two-platform.pipelines` patterns
- **API layer** → standard wow-two Clean Architecture
- **SaaS apps** → `wow-two-apps` org (new repos)
- **Shared libs** → reusable components back to `wow-two-sdk`

### Potential New Repos

| Repo | Org | Purpose |
|---|---|---|
| `wow-two-apps.content-forge` | wow-two-apps | Content automation pipeline (AudioForge + Compositor + Uploader) |
| `wow-two-apps.garden-viz` | wow-two-apps | AI Garden Visualizer SaaS |
| `wow-two-apps.cultural-tryon` | wow-two-apps | AI Cultural Dress Try-On SaaS |
| `wow-two-sdk.media.audio` | wow-two-sdk | Audio processing utilities (reusable) |
| `wow-two-sdk.media.video` | wow-two-sdk | Video composition utilities (reusable) |

---

## Open Questions

1. Suno vs AudioCraft vs custom model for music generation — quality vs cost vs control?
2. YouTube's evolving AI content policy — how strict will disclosure requirements get?
3. Self-host GPU (home server) vs cloud API for image/audio generation — cost crossover point?
4. Legal entity needed for multi-channel YouTube operation?
5. Spotify for Artists — can AI-generated music be distributed? TOS implications?

# TranscriptForge — Creator Transcript & Repurposing Suite

*Last updated: 2026-05-19*

> Working name. Could become `ScriptVault`, `ChannelLens`, `ClipMind`, `VidScribe`, etc.

## Section 1: Problem

Content creators sit on a **gold mine of unstructured spoken content** (every video they've ever uploaded) and can't do anything with it without manual transcription, copy-paste, or stitching together 5 different SaaS tools. Repurposing a single 30-min video into a blog post, Twitter thread, LinkedIn post, newsletter, and short-form clips takes hours per video.

The base layer — transcripts — is commoditized and free-ish (open-source libraries, Whisper, YouTube's own captions). But every layer above it (search, repurposing, voice-preserving translation, competitive intel) is fragmented across expensive single-purpose tools.

## Section 2: Market Landscape

### Existing supply

**Pure transcript APIs (developer-facing, crowded):**
- Open source: `youtube-transcript-api` (~12k★), `yt-dlp` — free, scrape-based, break frequently
- Paid: SearchAPI.io, Supadata, Kome, ScrapingDog, RapidAPI listings — $5–50/mo for ~10k transcripts
- Official YouTube Data API v3 — `captions.download` requires OAuth as video owner (useless for arbitrary videos — this is why the gray-market exists)

**Creator-facing tools (where the money is):**
| Tool | Focus | Pricing |
|---|---|---|
| Opus Clip | AI long→short clips | $19–$49/mo |
| Submagic, Captions.ai | Auto-captions for shorts | $20–$50/mo |
| Descript | Transcript-based video editing | $24–$50/mo |
| Castmagic | Podcast → social repurposing | $34–$200/mo |
| Spikes Studio, Vizard | Clip generation | $24+/mo |
| Eightify, NoteGPT, Tactiq | Summarization (consumer) | $5–$15/mo |
| Repurpose.io | Distribution automation | $15–$50/mo |

### Demand signals

- "youtube transcript" — 200k+ searches/mo
- "youtube transcript api" — tens of thousands/mo
- Opus Clip raised $30M (2025), Descript valued >$500M, Castmagic doing 7-figure ARR
- LLM/RAG boom = every AI wrapper needs transcripts as upstream
- 50M+ YouTube channels, ~3M monetized, ~200k+ "creator-economy professionals"

### The actual gap

Existing tools are **per-video, per-feature SaaS**:
- Opus clips your video.
- Submagic captions your short.
- Descript edits one episode.
- Castmagic outputs templates per podcast.

Nothing treats your **channel as the unit** — a continuous, searchable, mine-able knowledge base that auto-flows new uploads into every downstream artifact you care about.

## Section 3: Concept

**Connect your channel once. Every video you've ever made and every video you'll ever make becomes a searchable, repurposable, exportable asset.**

Not "give me the transcript of this URL." More like: *your YouTube library as a queryable database with auto-generated outputs.*

### Three layers

1. **Layer 1 — Transcript ingestion** (commodity, but reliable)
   - Pull every existing video from a channel
   - Auto-process every new upload (channel webhook or polling)
   - Multi-source: YouTube auto-captions → fallback to Whisper → fallback to scraper
   - Output stored in a canonical schema with speaker labels, timestamps, paragraphs

2. **Layer 2 — Intelligence** (the wedge)
   - Semantic search across entire channel ("find every time I talked about X")
   - Topic clustering — "your top-5 themes this quarter"
   - Repeated bit detection — "you've made this joke 12 times"
   - Quote extraction — viral-worthy moments tagged with timestamp
   - Competitor mining — track 5–10 channels in your niche, see trends

3. **Layer 3 — Auto-outputs** (the recurring revenue hook)
   - Per video, auto-drafted: blog post, newsletter section, Twitter thread, LinkedIn post, show notes, chapters, SEO metadata
   - Voice-preserving — uses creator's prior writing samples to keep tone
   - Multi-language repurposing without losing personality
   - Scheduled delivery — "every Tuesday morning, last week's video → newsletter draft in inbox"

## Section 4: Target Users

**Primary:** mid-tier creators — 10k–500k subs, publishing weekly, taking it seriously as a business. Big enough to want efficiency, small enough to not have a team.

**Secondary:**
- Podcasters cross-publishing to YouTube
- Educational creators (courses, deep dives) — high transcript value
- Business creators (newsletters + YouTube) — auto-newsletter is killer wedge
- Agencies managing multiple creator clients

**Not the target:**
- Sub-1k creators (won't pay)
- 1M+ creators (have teams, custom workflows)
- Pure short-form creators (Opus Clip serves them well already)

## Section 5: Features

### MVP — single-channel, single-creator (Month 1–3)

- Connect YouTube channel (OAuth via YouTube Data API for metadata, transcripts via Whisper/scraper)
- Backfill last 50 videos automatically
- Auto-process new uploads (poll channel every 6h via Data API)
- Per-video output: blog post draft, Twitter thread, show notes with chapters
- Web UI: channel library, per-video detail, semantic search across library
- Export everything (Markdown, plain text, JSON)

### V2 — repurposing pipelines (Month 4–6)

- Custom output templates ("my newsletter format", "my LinkedIn voice")
- Voice fine-tuning from existing creator writing
- Scheduled delivery (email digest, Notion, Google Docs)
- Multi-language repurposing
- Clip suggestions with timestamps (text-only; doesn't render video — points creator to moments)

### V3 — channel intelligence (Month 7–10)

- Topic clustering / theme analysis dashboard
- Competitor channel tracking (paid add-on)
- Idea suggestions based on past performance + competitor gaps
- Quote/highlight reel for social
- Audience-question mining from comments (cross-correlated with transcript)

### Future / aspirational

- Agency mode (manage multiple creator workspaces)
- Public API (back to the original "transcript API" play, but powered by mature backend)
- Embeddable widgets (creator's site → searchable video library)
- TikTok / Instagram / podcast support (multi-platform)

## Section 6: Technical Architecture

### Data sources (transcript ingestion)

| Source | When to use | Cost | Reliability |
|---|---|---|---|
| YouTube auto-captions (innertube/scrape) | Default, has captions | Free | Medium (breaks when YT changes) |
| YouTube Data API v3 + OAuth | If creator owns the channel (Premium) | Free (quota) | High — official |
| Groq Whisper-large-v3 | Fallback / no captions | ~$0.04/hr audio | High |
| OpenAI Whisper API | Fallback | ~$0.36/hr | High |
| Self-hosted Whisper.cpp | At scale | ~$0.01/hr (GPU) | High |

**Strategy:** for creators who connect via OAuth, use official API for their own channel (highest quality + legal). For competitor tracking, use Whisper-only mode (sidesteps ToS risk).

### Stack (wow-two-aligned)

| Layer | Tech | Repo |
|---|---|---|
| API backend | .NET 9, Clean Architecture, MediatR | `wow-two-apps.transcript-forge` |
| Transcript pipeline | .NET worker service + queue | same |
| LLM orchestration | wow-two `sdk.ai.semantic-kernel` | existing |
| Caption fetcher | C# wrapper around Whisper.cpp + youtube-dl-style fallback | new lib? `wow-two-sdk.media.transcripts` |
| Storage | Postgres (channels, videos, transcripts) + S3/Blob (raw audio if needed) | platform |
| Search | pgvector for semantic embeddings; full-text via Postgres GIN | platform |
| Frontend | React + Tailwind + shadcn/ui | same |
| Auth | YouTube OAuth + own user accounts | standard |
| Billing | Stripe | standard |
| Webhooks / scheduling | Hangfire or Azure Functions for poll jobs | existing pattern |

### Core pipeline

```
[New video detected]
       ↓
[Fetch captions] ──fail──→ [Download audio] → [Whisper] → [Text]
       ↓                                                     ↓
       └──────────────→ [Canonical transcript schema] ←──────┘
                              ↓
              [Chunk + embed (pgvector)]
                              ↓
              [LLM templates run: blog, thread, notes, ...]
                              ↓
              [Persist outputs] → [Notify user / scheduled delivery]
```

### Data model (sketch)

- `Channel` — youtube_channel_id, owner_user_id, oauth_tokens?, settings
- `Video` — youtube_video_id, channel_id, title, published_at, duration, status
- `Transcript` — video_id, source (`captions`/`whisper`), segments (jsonb with timestamps), embeddings_ref
- `Output` — video_id, template_id, generated_text, status, delivered_at
- `Template` — user_id, type (blog/thread/etc), prompt, voice_samples_ref

## Section 7: Economics

### Unit costs (per video, 15-min average)

| Item | Cost |
|---|---|
| Transcript (Whisper via Groq) | ~$0.01 |
| Embeddings (OpenAI text-embedding-3-small) | ~$0.0001 |
| LLM repurposing (5 outputs, GPT-4o-mini or Claude Haiku) | ~$0.02 |
| Storage / compute amortized | ~$0.005 |
| **Total** | **~$0.04 / video** |

### Pricing tiers

| Plan | Price | Videos/mo | Channels | Outputs/video |
|---|---|---|---|---|
| Free trial | $0 | 5 | 1 | All |
| Hobby | $19/mo | 30 | 1 | All |
| Pro | $49/mo | 100 | 3 | All + scheduling |
| Studio | $149/mo | 500 | 10 | All + competitor tracking |
| Agency | $499+/mo | Custom | Unlimited | All + API access |

**Gross margin:** ~95% at Pro (100 videos = ~$4 cost on $49 revenue).

### Revenue projections (conservative, micro-SaaS pace)

| Milestone | Timeline | MRR |
|---|---|---|
| MVP + 10 paying users | Month 3 | $250 |
| 50 paying users | Month 6 | $1,500 |
| 200 paying users | Month 12 | $7,000 |
| 500 + agency clients | Month 18 | $20,000+ |

Fits the [micro-SaaS portfolio play 2026](../../../../../.claude/projects/-Users-max-Projects-10x-ws-workbench-career-engineering-wow-two-wow-two-ws/memory/project_micro_saas_portfolio.md) thesis — single product, clean surface, recurring revenue.

## Section 8: Risks & Mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| YouTube ToS / cease-and-desist on caption scraping | High | Use official YT Data API for owned channels (OAuth); Whisper-only mode for competitor tracking; never cache & resell raw transcripts |
| Crowded creator-tool market | High | Channel-as-unit positioning + voice-preserving repurposing; not competing head-on with Opus/Descript |
| Margin compression as Whisper costs drop | Medium | Margins already 95%; value is in intelligence layer, not raw transcripts |
| Big player (YouTube, Anthropic, OpenAI) launches native repurposing | Medium | Build deep workflow integrations (Notion, Beehiiv, Substack, Ghost) — switching cost > generic alternative |
| Quality variance across niches (heavy accent, technical, music-heavy) | Medium | Multi-pass with self-correction; let user edit/correct + learn from corrections per channel |
| GDPR / data ownership concerns | Medium | Per-user encryption keys; "delete everything" button; clear data residency policy |

## Section 9: Wow-Two Integration

> **Detailed SDK breakdown:** see [transcript-forge-backend-libs-spec.md](transcript-forge-backend-libs-spec.md) — 10 proposed beta NuGet packages and their decomposition.

### New repos

| Repo | Org | Purpose |
|---|---|---|
| `wow-two-apps.transcript-forge` | wow-two-apps | Full product (backend + frontend) |
| `wow-two-sdk-beta.backend` | wow-two-sdk-beta | Mono-repo hosting all `Wow.Two.Sdk.Beta.*` NuGet libs (Media.Transcripts, Media.Youtube, Ai.SpeechToText, etc.) |

### Reuses existing wow-two packages

- `wow-two-platform.comms.infra` — MediatR pipelines
- `wow-two-platform.data.relational` — EF Core patterns
- `wow-two-platform.storage.cache` — caption/embedding cache
- `wow-two-sdk.ai.semantic-kernel` — LLM orchestration
- `wow-two-platform.pipelines` — CI/CD

### Could become flagship `wow-two-apps` product

First real consumer-facing product on the wow-two stack — proves the ecosystem can ship a real SaaS, not just internal libraries. Same way Cursor/Linear/Vercel "ate their own dogfood" to validate their infra.

## Section 10: Competitive Differentiation Summary

| Dimension | TranscriptForge | Opus Clip | Descript | Castmagic | Tactiq |
|---|---|---|---|---|---|
| Channel-level (vs per-video) | ✅ | ❌ | ❌ | ❌ | ❌ |
| Auto-process new uploads | ✅ | ❌ | ❌ | Partial | ❌ |
| Multi-output repurposing (blog/thread/newsletter) | ✅ | ❌ | ❌ | ✅ | ❌ |
| Voice-preserving generation | ✅ | ❌ | ❌ | Partial | ❌ |
| Channel semantic search | ✅ | ❌ | ❌ | ❌ | ❌ |
| Competitor intelligence | ✅ (V3) | ❌ | ❌ | ❌ | ❌ |
| Video editing | ❌ | ✅ | ✅ | ❌ | ❌ |
| Clip rendering | Suggests only | ✅ | ✅ | ✅ | ❌ |
| Price floor | $19/mo | $19/mo | $24/mo | $34/mo | $5/mo |

**Positioning:** *"Not another clip tool. Your channel as a queryable knowledge base, with every video auto-flowing into your newsletter, blog, and social."*

## Section 11: Open Questions

1. **Ingestion legality** — go all-in on official YT Data API (OAuth-only, owned channels) and skip scraping entirely? Reduces ToS risk but limits competitor-tracking feature
2. **GTM** — direct-to-creator (YouTube ads, Twitter outreach) vs partnership with newsletter platforms (Beehiiv, Substack integrations as wedge)?
3. **Free tier or trial-only** — free forever (5 vids/mo) builds top-of-funnel but raises costs; 14-day trial converts harder but cleaner economics
4. **Hosted LLMs vs API** — at 1000 paying users, self-host Llama-class for repurposing? Cost crossover ~$3k/mo in API spend
5. **Build clip rendering or stay text-only?** — text-only = 80% of value at 20% of effort; clip rendering = competing with Opus directly
6. **Naming** — TranscriptForge feels on-brand for wow-two but generic; ChannelLens is more product-y; user can decide
7. **Standalone product vs wow-two-apps first proof** — does it ship under personal brand for faster iteration or under wow-two for ecosystem legitimacy?

## Section 12: Adheres to GWDNBM

Aligned with [GWDNBM principle](../../../../../.claude/projects/-Users-max-Projects-10x-ws-workbench-career-engineering-wow-two-wow-two-ws/memory/principle_gwdnbm.md):
- No ad emails — only artifacts the creator asked for (blog drafts, newsletter, etc.)
- No engagement bait — daily/weekly digest only on opt-in cadence
- No upsell modals — pricing is transparent on signup
- Cancel anytime, export everything, no friction

## Status

`poc-in-progress` — POC backend scaffolded at `workbench/ventures/yt-transcripts-poc/` (own git repo, codename "yt-scraper" in early chats). Creator validation interviews still pending — building thin slice first to make the demo concrete before reaching out.

### POC state — 2026-05-28

- ✅ Canonical `Transcript` schema (`Yt.Transcripts.Poc.Transcripts`)
- ✅ YouTube caption fetcher (`Yt.Transcripts.Poc.YouTube` — yt-dlp + VTT parser, builds clean)
- ✅ Audio extractor (`Yt.Transcripts.Poc.Audio` — yt-dlp audio extraction, builds clean)
- ⏳ Groq Whisper provider — interfaces only, no impl yet (**next**)
- ⏳ `TranscriptFetcher` orchestrator + DI
- ⏳ `POST /transcripts` endpoint (Program.cs still `Hello World!`)
- ⏳ VttParser unit tests

Full state + resume recipe in the [POC README](../../workbench/ventures/yt-transcripts-poc/README.md). Reason for the standalone README: the previous working chat was accidentally deleted on 2026-05-28 — the README is now the recovery surface.

## Next Steps

1. Finish POC backend end-to-end (Groq provider → orchestrator → API endpoint → known-URL smoke test)
2. Validate with 5–10 mid-tier creators (10k–500k subs) — pain points and current tool stack
3. Build paper prototype of "channel library + auto-blog-post" — single-user demo using POC backend
4. Decide on naming + standalone vs wow-two-apps positioning
5. Prove Whisper-via-Groq pipeline can process 100 videos in <30 min end-to-end

# TranscriptForge — Backend SDK Libraries Breakdown

*Last updated: 2026-05-19*

> Companion to [transcript-forge-spec.md](transcript-forge-spec.md). Drills into the **wow-two-sdk-beta.backend** decomposition: what reusable libraries we extract from TranscriptForge so every piece can power future products.

## Section 1: Goal

Build TranscriptForge **on top of** a set of small, focused NuGet packages — not as a monolith. Each package should:

- Solve **one** problem (caption parsing, STT provider, embeddings, etc.)
- Be useful in **at least 2 future products** (otherwise inline in the app)
- Ship under `Wow.Two.Sdk.Beta.*` NuGet branding inside the planned `wow-two-sdk-beta.backend` mono-repo
- Stay beta-forever — semver flexible, no breaking-change panic, public but Issues/Discussions disabled

Reuse target: when we later build podcast tools, course generators, video search engines, AI assistants over personal libraries — these libs drop in unchanged.

## Section 2: Decomposition Principles

1. **One reason to change per package.** Caption format changes ≠ Whisper provider changes ≠ YouTube API changes. Separate.
2. **Provider abstractions over concrete deps.** `ISpeechToTextProvider` interface; OpenAI/Groq/Azure/local as swappable impls.
3. **Pure where possible.** Captions parsing, chunking, schema = no external services. Easy to test, no API keys.
4. **Composite packages compose, don't reimplement.** `Media.Transcripts` orchestrates `Media.Captions` + `Media.Youtube` + `Ai.SpeechToText` — doesn't reach into HTTP itself.
5. **Defer until proven needed.** Build for TranscriptForge first; extract to lib only if a second product would use it.

## Section 3: Proposed Package Map

Single repo (`wow-two-sdk-beta.backend`), multiple NuGet packages.

| # | Package | Layer | Purpose | Phase |
|---|---|---|---|---|
| 1 | `Wow.Two.Sdk.Beta.Media.Captions` | Pure utility | Parse/emit VTT, SRT, TTML, JSON3 caption formats | MVP |
| 2 | `Wow.Two.Sdk.Beta.Text.Chunking` | Pure utility | Sentence/paragraph/semantic chunking with overlap | MVP |
| 3 | `Wow.Two.Sdk.Beta.Ai.SpeechToText` | Provider abstraction | Whisper provider interface + OpenAI / Groq / Azure / local impls | MVP |
| 4 | `Wow.Two.Sdk.Beta.Media.Youtube` | Source client | YouTube channel/video/captions wrapper (official API + public fallback) | MVP |
| 5 | `Wow.Two.Sdk.Beta.Media.Audio` | Source client | Audio extraction (yt-dlp wrapper) + ffmpeg conversion | MVP |
| 6 | `Wow.Two.Sdk.Beta.Media.Transcripts` | Composite | Strategy-chain transcript fetcher with canonical schema | MVP |
| 7 | `Wow.Two.Sdk.Beta.Ai.Embeddings` | Provider abstraction | Embedding provider interface + OpenAI / Cohere / local impls + cache | V2 |
| 8 | `Wow.Two.Sdk.Beta.Search.Vector` | Storage | pgvector helpers + `IVectorStore<T>` abstraction | V2 |
| 9 | `Wow.Two.Sdk.Beta.Ai.Repurposing` | Application-layer | Template engine for blog/thread/newsletter generation with voice samples | V2 |
| 10 | `Wow.Two.Sdk.Beta.Ops.CostTracking` | Cross-cutting | Per-provider usage/cost metering for billing & quotas | V2 |

**MVP set (6 packages):** 1, 2, 3, 4, 5, 6
**V2 set (4 packages):** 7, 8, 9, 10

## Section 4: Per-Package Detail

### 4.1 `Media.Captions` — Caption Format I/O

**Purpose:** Pure parsing/serialization for caption formats. Zero network deps.

**Public API:**
```csharp
public interface ICaptionParser {
    CaptionTrack Parse(string input, CaptionFormat format);
    string Serialize(CaptionTrack track, CaptionFormat format);
}

public record CaptionTrack(
    string Language,
    IReadOnlyList<CaptionSegment> Segments
);

public record CaptionSegment(
    TimeSpan Start,
    TimeSpan End,
    string Text,
    string? Speaker = null
);

public enum CaptionFormat { Vtt, Srt, Ttml, Json3, Plain }
```

**Reuse beyond TF:** any subtitle/caption work — accessibility tools, video editors, language learning apps.

**Effort:** 2–3 days. Mostly straightforward parsing; VTT has weird edge cases.

---

### 4.2 `Text.Chunking` — Text Splitting

**Purpose:** Chunking strategies for RAG / embeddings / LLM context windows.

**Public API:**
```csharp
public interface ITextChunker {
    IReadOnlyList<TextChunk> Chunk(string text, ChunkOptions options);
}

public record ChunkOptions(
    int MaxTokens = 512,
    int OverlapTokens = 64,
    ChunkStrategy Strategy = ChunkStrategy.SentenceAware
);

public enum ChunkStrategy { FixedSize, SentenceAware, ParagraphAware, Semantic }

public record TextChunk(
    string Content,
    int StartOffset,
    int EndOffset,
    int TokenCount,
    IReadOnlyDictionary<string, object>? Metadata = null
);
```

**Reuse beyond TF:** every LLM/RAG product. This is foundational.

**Effort:** 1–2 days for first 3 strategies; `Semantic` needs LLM judge (deferred).

---

### 4.3 `Ai.SpeechToText` — STT Provider Abstraction

**Purpose:** Pluggable Whisper / STT providers behind one interface.

**Public API:**
```csharp
public interface ISpeechToTextProvider {
    string Name { get; }
    Task<TranscriptionResult> TranscribeAsync(
        Stream audio,
        TranscriptionOptions options,
        CancellationToken ct = default);
}

public record TranscriptionOptions(
    string? Language = null,        // null = auto-detect
    bool IncludeWordTimestamps = false,
    string? Prompt = null            // domain hints
);

public record TranscriptionResult(
    string Text,
    string Language,
    IReadOnlyList<TranscribedSegment> Segments,
    decimal CostUsd                   // self-reported by provider
);

public record TranscribedSegment(
    TimeSpan Start,
    TimeSpan End,
    string Text,
    double? Confidence = null,
    IReadOnlyList<TranscribedWord>? Words = null
);
```

**Implementations shipped:**
- `OpenAiWhisperProvider`
- `GroqWhisperProvider` (cheapest at scale)
- `AzureSpeechProvider`
- `LocalWhisperCppProvider` (via process — whisper.cpp binary)

DI registration: `services.AddSpeechToText().AddGroq(opts).AddOpenAi(opts).WithFallback();`

**Reuse beyond TF:** podcast tools, voice memos, meeting transcribers, accessibility apps.

**Effort:** 4–5 days (4 providers + retry/fallback + tests).

---

### 4.4 `Media.Youtube` — YouTube Client Wrapper

**Purpose:** YouTube channel/video/captions access with both official (OAuth) and public (no-auth) modes.

**Public API:**
```csharp
public interface IYouTubeClient {
    Task<YouTubeChannel> GetChannelAsync(string channelId, CancellationToken ct = default);
    IAsyncEnumerable<YouTubeVideo> ListVideosAsync(string channelId, ListVideosOptions options, CancellationToken ct = default);
    Task<YouTubeVideo> GetVideoAsync(string videoId, CancellationToken ct = default);
    Task<CaptionTrack?> GetCaptionsAsync(string videoId, string? language = null, CancellationToken ct = default);
}

public record YouTubeChannel(string Id, string Title, string Handle, long SubscriberCount, long VideoCount, ...);
public record YouTubeVideo(string Id, string ChannelId, string Title, string Description, TimeSpan Duration, DateTimeOffset PublishedAt, ...);
```

**Two impls:**
- `OfficialYouTubeClient` — uses `Google.Apis.YouTube.v3`, requires API key or OAuth
- `PublicYouTubeClient` — uses innertube / public endpoints (brittle, no auth, gray-area)

**Strategy:** product code picks impl based on whether OAuth token exists for the channel.

**Reuse beyond TF:** any product touching YouTube — analytics tools, link-in-bio, content alerts.

**Effort:** 5–7 days (official client wrapping is straightforward; public fallback needs reverse-engineered endpoints + protection against breakage).

---

### 4.5 `Media.Audio` — Audio Extraction & Conversion

**Purpose:** Pull audio out of video URLs, convert formats.

**Public API:**
```csharp
public interface IAudioExtractor {
    Task<AudioStream> ExtractAsync(string videoUrl, AudioExtractOptions options, CancellationToken ct = default);
}

public record AudioExtractOptions(
    AudioFormat Format = AudioFormat.Mp3,
    int? SampleRate = null,
    int? BitrateKbps = null
);

public enum AudioFormat { Mp3, Wav, Ogg, Flac, M4a }
```

**Impl:** wraps `yt-dlp` and `ffmpeg` as child processes. Configurable binary paths.

**Reuse beyond TF:** podcast tools, music apps, video processors.

**Effort:** 3–4 days (process wrangling + temp file management + tests with sample fixtures).

---

### 4.6 `Media.Transcripts` — Orchestrator (THE CORE)

**Purpose:** Single entry point: *"give me a transcript for this video URL."* Internally chains caption fetch → STT fallback.

**Public API:**
```csharp
public interface ITranscriptFetcher {
    Task<Transcript> FetchAsync(TranscriptRequest request, CancellationToken ct = default);
}

public record TranscriptRequest(
    string SourceUrl,
    string? PreferredLanguage = null,
    TranscriptStrategy Strategy = TranscriptStrategy.CaptionsFirst,
    bool RequireWordTimestamps = false
);

public enum TranscriptStrategy {
    CaptionsOnly,        // fail if no captions
    SttOnly,             // ignore captions, always Whisper
    CaptionsFirst,       // try captions, fall back to STT
    HighestQuality       // STT if no human captions available
}

public record Transcript(
    string SourceUrl,
    TranscriptSource Source,         // Captions | Stt
    string Language,
    string FullText,
    IReadOnlyList<TranscriptSegment> Segments,
    TranscriptMetadata Metadata
);

public record TranscriptSegment(
    TimeSpan Start,
    TimeSpan End,
    string Text,
    string? Speaker = null,
    double? Confidence = null
);

public record TranscriptMetadata(
    string ProviderName,
    decimal CostUsd,
    TimeSpan ProcessingDuration,
    DateTimeOffset FetchedAt
);
```

**DI:**
```csharp
services
    .AddTranscriptFetcher()
    .AddSource<YouTubeTranscriptSource>()     // from Media.Youtube
    .AddFallback<SttTranscriptSource>();      // from Ai.SpeechToText + Media.Audio
```

**Reuse beyond TF:** EVERY future audio/video AI product touches this. The crown jewel.

**Effort:** 4–6 days (orchestration logic, retry, partial-failure handling, canonical schema mapping).

---

### 4.7 `Ai.Embeddings` — Embedding Provider Abstraction (V2)

**Purpose:** Same pattern as STT — one interface, many providers + caching.

**Public API:**
```csharp
public interface IEmbeddingProvider {
    string Name { get; }
    int Dimensions { get; }
    Task<IReadOnlyList<float[]>> EmbedAsync(IReadOnlyList<string> texts, CancellationToken ct = default);
}
```

**Impls:** `OpenAiEmbeddingProvider`, `CohereEmbeddingProvider`, `LocalSentenceTransformerProvider`.

**Cache layer:** content-hash → vector, backed by `wow-two-platform.storage.cache`. Avoids re-embedding identical chunks.

**Effort:** 3 days.

---

### 4.8 `Search.Vector` — Vector Storage (V2)

**Purpose:** Abstract vector store; pgvector primary, in-memory for tests.

**Public API:**
```csharp
public interface IVectorStore<TItem> where TItem : class {
    Task UpsertAsync(IEnumerable<VectorEntry<TItem>> entries, CancellationToken ct = default);
    Task<IReadOnlyList<VectorSearchResult<TItem>>> SearchAsync(float[] queryVector, int topK, VectorFilter? filter = null, CancellationToken ct = default);
}
```

**Effort:** 4 days (pgvector EF integration + filter builder + tests).

---

### 4.9 `Ai.Repurposing` — Templated Generation (V2)

**Purpose:** Run prompt templates against transcripts, with voice-preserving few-shot.

**Public API:**
```csharp
public interface IRepurposer {
    Task<RepurposeResult> RunAsync(RepurposeRequest request, CancellationToken ct = default);
}

public record RepurposeRequest(
    Transcript Source,
    RepurposeTemplate Template,
    IReadOnlyList<string>? VoiceSamples = null
);

public record RepurposeTemplate(
    string Name,                        // "BlogPost", "TwitterThread", "Newsletter"
    string SystemPrompt,
    string OutputFormat                  // markdown | plain | json
);
```

Built-in templates shipped: `BlogPost`, `TwitterThread`, `LinkedInPost`, `Newsletter`, `ShowNotes`, `Chapters`.

**Effort:** 4–5 days (templates + prompt engineering + voice few-shot logic).

---

### 4.10 `Ops.CostTracking` — Usage Metering (V2)

**Purpose:** Track per-call provider costs for billing/quota enforcement.

**Public API:**
```csharp
public interface ICostTracker {
    Task RecordAsync(CostEvent evt, CancellationToken ct = default);
    Task<UsageReport> GetUsageAsync(string scopeId, DateRange range, CancellationToken ct = default);
}

public record CostEvent(
    string ScopeId,                     // user/tenant
    string Provider,
    string Operation,
    decimal CostUsd,
    IReadOnlyDictionary<string, object> Tags
);
```

Persistence pluggable — default to EF Core via `wow-two-platform.data.relational`.

**Effort:** 3 days.

## Section 5: Dependency Graph

```
                 ┌──────────────────────────────────┐
                 │   App: TranscriptForge           │
                 │   (wow-two-apps.transcript-forge)│
                 └──────────────────────────────────┘
                                 │
        ┌────────────────────────┼─────────────────────────┐
        ▼                        ▼                         ▼
  Media.Transcripts       Ai.Repurposing            Search.Vector
        │                        │                         │
   ┌────┼────────────┐           ▼                         ▼
   ▼    ▼            ▼     Ai.Embeddings ───────► (used standalone too)
Media. Media.    Ai.SpeechToText        ▲
Youtube Captions  + Media.Audio          │
                                  Text.Chunking
                                         ▲
                                         │
                              (used everywhere doing LLM work)

  Cross-cutting: Ops.CostTracking → recorded by SpeechToText, Embeddings, Repurposing
```

Leaf packages (no internal deps): `Media.Captions`, `Text.Chunking`, `Ops.CostTracking`
Composite: `Media.Transcripts` (depends on 3 leaves), `Ai.Repurposing` (depends on 2 leaves)

## Section 6: Build Order

**Sprint 1 (Week 1–2): Leaves**
1. `Media.Captions` — 2-3 days
2. `Text.Chunking` — 1-2 days

→ Already useful for tests/fixtures; no external deps to break on.

**Sprint 2 (Week 3): STT abstraction**
3. `Ai.SpeechToText` — 4-5 days (with 4 providers)

→ Can be demoed standalone: feed audio file, get text.

**Sprint 3 (Week 4–5): YouTube + Audio**
4. `Media.Youtube` — 5-7 days
5. `Media.Audio` — 3-4 days (parallel-able with 4)

**Sprint 4 (Week 6): Orchestrator**
6. `Media.Transcripts` — 4-6 days

→ MVP libs complete. TranscriptForge app build starts.

**Sprint 5 (Week 7–8): App MVP**
- Build `wow-two-apps.transcript-forge` consuming all 6 libs
- Channel connect → transcript backfill → first repurposing output (hardcoded prompts, no `Ai.Repurposing` lib yet)

**Sprint 6 onward: V2 libs**
7. `Ai.Embeddings`
8. `Search.Vector`
9. `Ai.Repurposing` (extract from hardcoded prompts in app)
10. `Ops.CostTracking`

**Total time to TranscriptForge MVP:** ~8 weeks part-time, ~4 weeks full-time.

## Section 7: Versioning & Publishing Strategy

Per `wow-two-sdk-beta` convention:
- **Beta-forever** — all packages stay `0.x.y` indefinitely. No semver-major panic.
- **Independent versioning** per package (mono-repo with per-project version bumps), not lockstep.
- **CI publishing** via `wow-two-platform.pipelines` — push to `main` → version bump → NuGet publish to nuget.org.
- **Public NuGet, public source.** No Issues/Discussions (matching `wow-two-sdk-beta.ui` pattern).
- **No xml-doc enforcement initially**, but README per package with quickstart example.

### NuGet package naming

| Repo path | NuGet ID |
|---|---|
| `src/Media.Captions/` | `Wow.Two.Sdk.Beta.Media.Captions` |
| `src/Text.Chunking/` | `Wow.Two.Sdk.Beta.Text.Chunking` |
| `src/Ai.SpeechToText/` | `Wow.Two.Sdk.Beta.Ai.SpeechToText` |
| ... | ... |

## Section 8: What Stays in the App (not extracted to libs)

These belong to TranscriptForge specifically:
- Channel polling/cron logic (too YouTube-specific until other platforms added)
- User accounts, OAuth UX, billing flow
- Stripe integration (use platform-level package later if multiple apps need it)
- Delivery channels (Notion, Substack, Beehiiv) — could become libs once 2+ apps need them
- UI components (React, lives in `sdk-beta.ui` if reused)
- Domain entities (`Channel`, `Video`, `Output`) — app-specific aggregates

Rule of thumb: **extract on the 2nd duplicate, not the 1st reuse.**

## Section 9: Reuse Scenarios (sanity check)

If we build these 10 packages, what future products drop in cleanly?

| Hypothetical product | Packages reused |
|---|---|
| Podcast → newsletter generator | `Media.Captions`, `Ai.SpeechToText`, `Media.Audio`, `Media.Transcripts`, `Text.Chunking`, `Ai.Embeddings`, `Ai.Repurposing` |
| Meeting transcriber + summarizer | `Ai.SpeechToText`, `Text.Chunking`, `Ai.Repurposing`, `Ai.Embeddings`, `Search.Vector` |
| "Chat with my YouTube library" | `Media.Youtube`, `Media.Transcripts`, `Text.Chunking`, `Ai.Embeddings`, `Search.Vector` |
| Course builder from video lectures | `Media.Transcripts`, `Text.Chunking`, `Ai.Repurposing` |
| Voice-memo organizer | `Ai.SpeechToText`, `Text.Chunking`, `Ai.Embeddings`, `Search.Vector` |

Every package gets at least 2 hypothetical reuses. Decomposition justified.

## Section 10: Risks

| Risk | Impact | Mitigation |
|---|---|---|
| Over-engineering before product validation | High | Build TF MVP **first**, extract libs once product proven, not before |
| Premature abstraction (`I*Provider` everywhere) | Medium | Start with concrete classes; extract interface only when 2nd impl appears |
| Beta-forever versioning confuses consumers | Low | README clearly states "beta SDK, breaking changes possible, pin versions" |
| `Media.Youtube` public-mode breaks weekly | Medium | Version-pin YT scrape logic; CI canary test against real YouTube; auto-bump on break |
| Whisper.cpp local impl flaky across platforms | Low | Ship as opt-in with explicit binary path config; tests skipped if binary missing |

## Section 11: Open Questions

1. **Build TF MVP as monolith first, extract libs later?** Safer (lib design driven by real use) but slower (refactor cost). Or build libs first (current plan)?
2. **Do we need `Wow.Two.Sdk.Beta.Media.Audio` or can we shell out to `yt-dlp` directly in app code?** Likely lib — meeting transcribers and podcast tools will need it.
3. **Should `Media.Transcripts` ship its own fallback orchestration, or stay strict (caller composes)?** Lean toward shipping built-in fallback — it's the whole point of the composite.
4. **`Ai.Repurposing` voice-preservation — own templating language, or just structured prompts?** Start with structured prompts; templating language is YAGNI until templates get nested.
5. **Does `Ai.SpeechToText` belong in `sdk-beta` or graduate to `sdk` quickly?** STT abstraction is small + stable enough to graduate after 6 months of TF dogfooding.
6. **Public scraping mode in `Media.Youtube` — include at all, or OAuth-only?** Competitor tracking requires it. Could ship as separate package `Media.Youtube.Public` to make legal/risk boundary explicit.

## Section 12: Decision Needed Before Build

1. Mono-repo confirmed for `sdk-beta.backend` (yes, matches `sdk-beta.ui` pattern)? → **Yes assumed**
2. Build order: leaves-first (current plan) vs end-to-end vertical slice (build app + libs in lockstep)? → **Recommend leaves-first**
3. Hosting: GitHub Actions to nuget.org (free tier sufficient)? → **Yes assumed**
4. Whether to scaffold all 10 package skeletons upfront, or one-at-a-time? → **One at a time, prove pattern with first 2**

## Status

`idea` — decomposition plan ready. Awaits product-side validation from [transcript-forge-spec.md](transcript-forge-spec.md) before starting any code.

## Next Steps

1. User confirms decomposition makes sense / wants to revise
2. Pick first package to scaffold (`Media.Captions` recommended — pure, no external deps, fast win)
3. Create `wow-two-sdk-beta.backend` repo + solution structure
4. Establish CI/CD template for one package (copy to others as we go)
5. Build first package end-to-end (code + tests + README + NuGet publish) as the template

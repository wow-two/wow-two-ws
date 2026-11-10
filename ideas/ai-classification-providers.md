# AI providers for event classification

*Reviewed: 2026-11-10. Prices read from vendor pages on 2026-11-10; re-check a price before committing money. Scope: SCFD's per-post relevance pass for Ocharo, and Ocharo's later precise classification. Track doc: [events-integration](../system/sessions/events-integration/events-integration.md) (#50, #51, #53).*

## Recommendation

| Workload | Default | Fallback | Off-Anthropic reserve | Month at base volume |
|---|---|---|---|---|
| W1 relevance pass (summary + close / loose / none + reason) | `claude-haiku-5-5`, `effort: low` with thinking disabled, structured output, synchronous | `claude-sonnet-5-5` for the whole profile, `effort: low`, structured output, batch | `gpt-6-luna` (same price, strict JSON schema) | $11.78 paid-equivalent; **$0 paid** under the monthly credit |
| W2 precise classification (route, exhibitor vs visitor, fees, deadlines, garment categories) | `claude-sonnet-5-5`, adaptive thinking at `effort: medium`, structured output, Batch API | `claude-opus-5-5`, only where the eval shows Sonnet below the bar on fees, deadlines or route | `gpt-6.1-terra` ($1 / $5) or `mistral-large-4-0` ($0.70 / $2.10) | $38.20 paid-equivalent; **$0 paid** under the credit |

- Anthropic wins on value: the $200 monthly Console credit (org `WoW 2.0`) prices both workloads at $0 until it runs out, and unused credit expires.
- Haiku 5.5 costs $0.10 / $0.50 per 1M tokens, matching the cheapest closed models (`gpt-6-luna`, `gemini-2.5-flash-lite`). Paying cash would not undercut it by more than ~$10 a month.
- Anthropic and OpenAI need no new account: the credit org exists, and Haven already pays for GPT (developer, 2026-11-10). Every other provider's billing from Uzbekistan is unverified (#8).
- Haiku 5.5 and `gpt-6-luna` cost the same per token (#11), so the credit decides between them. OpenAI stays the ready reserve.
- Uzbek quality is unproven for every current model, Haiku 5.5 included (#6). The shadow week on real data confirms the default (#10); the fallback is the same vendor one tier up, so a failed eval changes a model id, not the integration.
- Run the relevance pass on every event-kind post (`AiMode.Full`) instead of only the keyword filter's gaps. At base volume, full mode costs $11.78 a month against $4.71 for gaps mode, and it catches the posts `ocharo-fashion-v1`'s lexicon misses.
- Both workloads together at base volume cost $50 a month paid-equivalent: a quarter of the credit, which other product AI (Haven's classification) shares.

## Workloads and volume

### #1 Assumptions

| Input | Value | Basis |
|---|---|---|
| Sources | 100 | the next goal's target (#51) |
| New or changed posts per source per day | low 3, base 10, high 30 | assumption; Afisha's 5-page acceptance sample found 23 fashion and 26 exhibition links, mostly older posts. Telegram-style channels post more, expo sites less |
| Posts per month | low 9,000, base 30,000, high 90,000 | sources × posts × 30 |
| Share reaching the model in `gaps` mode | 40% | assumption: posts the keyword filter neither names (`NamedOpportunity`, `TradeAndRetailFamily`) nor rules out |
| Share in `full` mode | 100% | every event-kind post |
| Re-runs | +10% | changed captures re-run; the spec caches on `(inputHash, schemaId, schemaVersion, promptVersion)` |
| W1 tokens per call | 2,500 page text + 700 rubric prefix (cacheable) in, 200 JSON out | brief: 1–4k input per post |
| W2 share and tokens | 10% of posts (those marked close or loose); 4,000 page + 1,500 rubric in, 1,500 out including reasoning | assumption; W2's fields are decided later |

W1 calls a month at base volume: 13,200 in `gaps` mode and 33,000 in `full` mode; 99,000 at high volume in `full` mode. W2: 3,300 at base, 9,900 at high.

### #2 Monthly cost: credit-funded vs paid

| Scenario | W1 | W2 | Paid-equivalent | Paid after the $200 credit |
|---|---|---|---|---|
| Base, recommended: Haiku full sync + Sonnet batch | $11.78 | $38.20 | $49.98 | $0 |
| Base, gaps mode | $4.71 | $38.20 | $42.91 | $0 |
| Base, fallback: Sonnet W1 batch + Sonnet W2 batch | $116.66 | $38.20 | $154.86 | $0 |
| Base, Opus for W2 batch | $11.78 | $76.40 | $88.18 | $0 |
| High, recommended | $35.34 | $114.60 | $149.94 | $0, if Events' share of the credit reaches $150 |
| High, fallback with Opus W2: Sonnet W1 batch + Opus W2 batch | $349.97 | $229.20 | $579.17 | $379.17 |

- The credit stops covering this workload only on the fallback path at high volume.
- Move W1 to the Batch API once paid spend starts: batch halves every Anthropic price ([pricing](https://platform.claude.com/docs/en/about-claude/pricing)).
- Set SCFD's G5 budget for the Ocharo subscription at a $25 soft / $30 hard monthly cap for W1 at base volume, so a runaway source cannot eat Haven's share of the credit.

## Comparison

### #3 Prices and cost per workload

Prices in USD per 1M tokens. "Disc." is the Batch API discount, or DeepSeek's off-peak price. W1 and W2 columns apply #1 and include the cached-prefix price where one is stated. Monthly W1 is base volume, full mode, standard / discounted.

| Provider | Model id | In | Cached in | Out | Disc. | W1 $ per 1k posts | W1 month | W2 month | Source |
|---|---|---|---|---|---|---|---|---|---|
| Anthropic | `claude-haiku-5-5` | 0.10 | 0.01 | 0.50 | batch −50% | 0.36 | 11.78 / 5.89 | 3.84 / 1.92 | [pricing](https://platform.claude.com/docs/en/about-claude/pricing) |
| Anthropic | `claude-sonnet-5-5` | 2.00 | 0.10 | 10.00 | batch −50% | 7.07 | 233.31 / 116.66 | 76.40 / 38.20 | same |
| Anthropic | `claude-opus-5-5` | 4.00 | 0.20 | 20.00 | batch −50% | 14.14 | 466.62 / 233.31 | 152.79 / 76.40 | same |
| OpenAI | `gpt-6-luna` | 0.10 | 0.01 | 0.50 | batch or flex −50% | 0.36 | 11.78 / 5.89 | 3.84 / 1.92 | [pricing](https://developers.openai.com/api/docs/pricing), [model](https://developers.openai.com/api/docs/models/gpt-6-luna) |
| OpenAI | `gpt-6.1-terra` | 1.00 | 0.05 | 5.00 | −50% | 3.54 | 116.66 / 58.33 | 38.20 / 19.10 | [model](https://developers.openai.com/api/docs/models/gpt-6.1-terra) |
| OpenAI | `gpt-6.1-sol` | 2.00 | 0.10 | 10.00 | −50% | 7.07 | 233.31 / 116.66 | 76.40 / 38.20 | [model](https://developers.openai.com/api/docs/models/gpt-6.1-sol) |
| Google | `gemini-2.5-flash-lite` (older generation; thinking can be off) | 0.10 | 0.01 | 0.40 | batch −50% | 0.34 | 11.12 / 5.56 | 3.35 / 1.67 | [pricing](https://ai.google.dev/gemini-api/docs/pricing) |
| Google | `gemini-3.1-flash-lite` | 0.25 | 0.025 | 1.50 | −50% | 0.94 + thinking | 31.10 / 15.55 | 10.85 / 5.42 | same |
| Google | `gemini-3.8-flash` (price doubles 2027-01-01) | 0.75 → 1.50 | 0.075 → 0.15 | 3.75 → 7.50 | −50% | 2.68 → 5.36 | 88.36 → 176.72 | 28.83 → 57.67 | same |
| Google | `gemini-3.1-pro-preview` | 2.00 | 0.20 | 12.00 | −50% | 7.54 | 248.82 / 124.41 | 86.79 / 43.40 | same |
| DeepSeek | `deepseek-flash` | 0.30 | 0.006 | 1.20 | off-peak −50% | 0.99 | 32.81 / 16.40 | 9.93 / 4.96 | [pricing](https://api-docs.deepseek.com/quick_start/pricing) |
| DeepSeek | `deepseek-v4-pro` | 1.32 | 0.044 | 3.96 | off-peak −50% | 4.12 | 136.05 / 68.03 | 37.24 / 18.62 | same |
| Moonshot | `kimi-k3.1-pro` (no cheap current tier) | 2.00 | 0.20 | 10.00 | batch −40% | 7.14 | 235.62 / 141.37 | 76.89 / 46.13 | [ids, batch](https://platform.kimi.ai/docs/pricing/chat); prices via [benchlm](https://benchlm.ai/moonshot/api-pricing), secondary |
| Alibaba | `qwen3.7-flash` (Singapore; ≤32K requests) | 0.03 | 0.003 | 0.13 | batch −50% | 0.10 | 3.40 / 1.70 | 1.05 / 0.53 | [pricing](https://www.alibabacloud.com/help/en/model-studio/model-pricing) |
| Alibaba | `qwen3.8-flash` | 0.15 | not stated | 0.47 | none listed | 0.57 | 18.94 | 5.05 | same |
| Alibaba | `qwen3.8-max` | 2.00 | not stated | 6.00 | none listed | 7.60 | 250.80 | 66.00 | same |
| xAI | `grok-4.3` (effort `none`) | 1.25 | 0.20 | 2.50 | batch −20% | 3.77 | 124.25 / 99.40 | 29.87 / 23.89 | [models](https://docs.x.ai/developers/models/grok-4.3) |
| xAI | `grok-4.7` | 2.00 | 0.50 | 6.00 | −20% | 6.55 + reasoning | 216.15 / 172.92 | 58.58 / 46.86 | [models](https://docs.x.ai/developers/models/grok-4.7) |
| Mistral | `ministral-8b-2512` | 0.15 | 0.015 | 0.15 | batch −50% | 0.42 | 13.71 / 6.86 | 2.80 / 1.40 | [pricing](https://docs.mistral.ai/inference/pricing) |
| Mistral | `mistral-small-2603` (reasoning `none`) | 0.15 | 0.015 | 0.60 | −50% | 0.51 | 16.68 / 8.34 | 5.02 / 2.51 | same |
| Mistral | `mistral-large-4-0` | 0.70 | 0.07 | 2.10 | −50% | 2.22 | 73.23 / 36.61 | 19.98 / 9.99 | [card](https://docs.mistral.ai/models/mistral-large-4-0) |
| Groq | `openai/gpt-oss-20b` | 0.075 | not stated | 0.30 | batch −50% | 0.30 | 9.90 / 4.95 | 2.85 / 1.42 | [models](https://console.groq.com/docs/models) |
| Groq | `openai/gpt-oss-120b` | 0.15 | not stated | 0.60 | −50% | 0.60 | 19.80 / 9.90 | 5.69 / 2.85 | same |
| Groq | `qwen/qwen3.8-27b` (preview) | 0.80 | not stated | 4.00 | not on the batch list | 3.36 | 110.88 | 34.32 | same |
| Fireworks | Nemotron 3.5 Lightning 30B-A3B (id inferred) | 0.05 | 0.01 | 0.20 | batch −50% | 0.17 | 5.68 / 2.84 | 1.70 / 0.85 | [pricing](https://docs.fireworks.ai/serverless/pricing) |
| Ollama, local | `qwen3.8:27b` or Gemma 4 31B | 0 | 0 | 0 | — | 0, hardware only | 0 | 0 | [structured outputs](https://docs.ollama.com/capabilities/structured-outputs) |

- Together serves `Qwen/Qwen3.8-Flash` at the same $0.15 / $0.47 as Alibaba ([pricing](https://www.together.ai/pricing)); OpenRouter passes through upstream prices and adds a ~5.5% fee on card top-ups (secondary source).
- Vendor pages were read through summarising fetches. Model names newer than June 2026 (`gpt-6-luna`, `gemini-3.8-flash`, `qwen3.8-*`) come from those pages, not from memory.
- Gemini 3.x and Kimi cannot switch reasoning off, so their W1 output grows by the reasoning tokens. `gemini-2.5-flash-lite`, `grok-4.3` at effort `none`, `mistral-small-2603` at reasoning `none`, Ministral, Haiku 5.5 (`disabled`) and Sonnet 5.5 (`between_tools`) can.
- The cheapest rows (`qwen3.7-flash`, Nemotron, `gpt-oss-20b`) save at most ~$10 a month against Haiku at base volume, and none has any Uzbek evidence.
- Ollama fits only as an eval baseline: a 27B model takes ~10–15 s per post on a 32–64 GB Apple Silicon Mac (estimate), and 1–2 min per post on a CPU-only VPS, too slow for 1,000 posts a day.

### #11 Claude vs GPT

Same cost model as #3: prices per 1M tokens; W1 at base volume in full mode, W2 at base volume; monthly figures standard / batch. Claude's figures are paid-equivalent: the $200 credit pays them, while GPT is paid in cash on Haven's OpenAI account.

| Tier | Model id | In | Cached in | Out | W1 $ per 1k posts | W1 month | W2 month | Reasoning off | Context | Uzbek or Russian evidence |
|---|---|---|---|---|---|---|---|---|---|---|
| Small | `claude-haiku-5-5` | 0.10 | 0.01 | 0.50 | 0.36 | 11.78 / 5.89 | 3.84 / 1.92 | yes, `disabled` at effort `high` or below | 1M; prompts over 100K tokens cost 5x | Global-MMLU per language, without Russian or Uzbek; weakest of the three Claude tiers on low-resource languages |
| Small | `gpt-6-luna` | 0.10 | 0.01 | 0.50 | 0.36 | 11.78 / 5.89 | 3.84 / 1.92 | low effort; reasoning tokens bill as output | 1.05M | none published |
| Mid | `gpt-6.1-terra` | 1.00 | 0.05 | 5.00 | 3.54 | 116.66 / 58.33 | 38.20 / 19.10 | low effort | 1.05M | none published |
| Mid | `claude-sonnet-5-5` | 2.00 | 0.10 | 10.00 | 7.07 | 233.31 / 116.66 | 76.40 / 38.20 | yes, `between_tools` | 1M | Global-MMLU, as for Haiku |
| Mid | `gpt-6.1-sol` | 2.00 | 0.10 | 10.00 | 7.07 | 233.31 / 116.66 | 76.40 / 38.20 | low effort | 1.05M | none published |
| Top | `claude-opus-5-5` | 4.00 | 0.20 | 20.00 | 14.14 | 466.62 / 233.31 | 152.79 / 76.40 | no; effort `low` is the floor | 1M | Global-MMLU, as for Haiku |
| Top | `gpt-6-astra` | 10.00 | 1.00 | 50.00 | 35.70 | 1,178.10 / 589.05 | 384.45 / 192.23 | not read | not read | none published |
| Haven today | `gpt-5-mini` (Haven Supply's Lite tier) | 0.25 | 0.025 | 2.00 | 1.04 | 34.40 / 17.20 | 13.32 / 6.66 | — | — | — |

- Both vendors take a 50% batch discount, cache reads at 0.1x or below, and cache writes at 1.25x. Neither trains on API inputs by default.
- At the small tier the two match per token, so the credit makes Haiku free and Luna cash.
- At the mid tier `gpt-6.1-terra` costs half of Sonnet 5.5 and has no Claude counterpart. Terra is the cheaper W2 option once the credit runs out, if the eval shows equal quality.
- Opus 5.5 costs 40% of `gpt-6-astra`.
- `gpt-6-luna` costs 40% of Haven's `gpt-5-mini` on input and 25% on output.
- Sources: [Anthropic pricing](https://platform.claude.com/docs/en/about-claude/pricing) and [OpenAI pricing](https://developers.openai.com/api/docs/pricing); Haven's tiers from `Haven.Supply.Api/appsettings.json`.

### #4 Provider facts

| Provider | Training on API inputs | Retention | Structured output | Uzbekistan: availability and billing | .NET route |
|---|---|---|---|---|---|
| Anthropic | no, under the [Commercial Terms](https://www.anthropic.com/legal/commercial-terms) | deleted within 30 days ([privacy center](https://privacy.claude.com/en/articles/7996866-how-long-do-you-store-my-organization-s-data), dated 2026-07-01); ZDR by agreement | `output_config.format` JSON schema | listed for the API ([supported regions](https://www.anthropic.com/supported-countries)); org `WoW 2.0` already billed | official NuGet `Anthropic`, with an `IChatClient` integration |
| OpenAI | no, unless opted in ([your data](https://developers.openai.com/api/docs/guides/your-data)) | abuse logs up to 30 days; Batch not ZDR-eligible | strict JSON schema | listed ([supported countries](https://developers.openai.com/api/docs/supported-countries)); billing works, since Haven already pays for GPT (developer, 2026-11-10) | NuGet `OpenAI` 2.15.0 + `Microsoft.Extensions.AI.OpenAI` |
| Google | paid tier no; **free tier yes, with human review** ([terms](https://ai.google.dev/gemini-api/terms)) | abuse logging, period not stated | JSON schema | API region listed ([regions](https://ai.google.dev/gemini-api/docs/available-regions)); Uzbekistan missing from the Cloud Billing country table, so paying is unverified | NuGet `Google.GenAI`, `AsIChatClient()`; OpenAI-compatible endpoint in beta |
| DeepSeek | not stated for the API; terms allow broad use | stored in the PRC, no period stated; PRC law ([terms](https://cdn.deepseek.com/policies/en-US/deepseek-open-platform-terms-of-service.html)) | `json_object` only | not stated | OpenAI-compatible |
| Moonshot (Kimi) | content "helps optimize our models", no opt-out in the policy | Singapore, no period stated | `json_object` only | not stated | OpenAI-compatible, `https://api.moonshot.ai/v1` |
| Alibaba (Qwen) | no, without consent ([retention](https://www.alibabacloud.com/help/en/model-studio/data-retention-policy)) | up to 30 days | `json_schema`, but not yet in the Singapore region | not stated | OpenAI-compatible, workspace-specific URL |
| xAI | no, without permission ([security FAQ](https://docs.x.ai/developers/faq/security)) | 30 days; ZDR disables batch | JSON schema | not stated | OpenAI-compatible, `https://api.x.ai/v1` |
| Mistral | no under the [commercial terms](https://legal.mistral.ai/terms/commercial-terms-of-service) § 4.2, except preview models; free plans train unless opted out ([help](https://help.mistral.ai/en/articles/455207-can-i-opt-out-of-my-input-or-output-data-being-used-for-training)) | not stated; ZDR disables batch | JSON schema | only sanctioned areas excluded; billing unverified | community NuGet packages or OpenAI-style endpoint |
| Groq, Together, Fireworks | no for Groq and Together by policy; Fireworks not stated | Groq up to 30 days unless ZDR, US storage | strict schema on Groq `gpt-oss`; Fireworks enforces schema | not stated for any of the three | OpenAI-compatible |

- The texts are public listings used internally (#50), and SCFD masks contact values before any model sees text unless a schema sets `needsContacts` (spec T6-15). No provider is ruled out on data grounds alone.
- Free tiers that train on inputs (Google, Mistral) stay off this workload. DeepSeek (PRC storage, unclear training) and Kimi (content improves models) stay out of the default and the reserve.

### #5 Latency and rate limits

- Nobody waits on a W1 result: Events polls SCFD every minute, and event deadlines run weeks out. A synchronous call adds seconds per post; a batch can take up to 24 hours.
- Base volume is ~1,100 W1 calls a day. Every provider's lowest paid tier allows far more: OpenAI's Build tier allows 5,000 RPM for `gpt-6-luna`, Groq's Developer plan 1,000 RPM, and xAI's Tier 1 50 RPS for `grok-4.3`.

### #6 Quality evidence for Russian and Uzbek

- No published Uzbek score exists for any current model: not Claude 5.x, GPT-6.x, Gemini 3.x, DeepSeek, Kimi, Grok or Mistral.
- The newest closed-model Uzbek numbers are from 2024–25 ([TUMLU](https://arxiv.org/html/2502.11020v2)): Claude 3.5 Sonnet 69.1, GPT-4o 65.4, Gemini 1.5 Pro 65.1.
- On that test the cheap tiers fell 13–19 points: Gemini 1.5 Flash scored 52.1, Claude 3.5 Haiku 50.3. The risk for this workload sits with the cheapest tier on Uzbek.
- Anthropic's [multilingual page](https://platform.claude.com/docs/en/build-with-claude/multilingual-support) lists neither Russian nor Uzbek. Its low-resource rows show Haiku 5.5 losing the most: Yoruba at 87.0% of its English score, against 96.3% for Opus 5.5.
- Open models: Gemma 4 31B and Qwen3.6 27B lead [IdrockBench](https://github.com/azizkayumov/IdrockBench/blob/main/LEADERBOARD.md) for Uzbek at ~52 composite. Models under ~10B fall to 20–30, and Qwen 0.8–2B collapse.
- Russian is saturated for frontier models: the best model in [Global PIQA](https://arxiv.org/html/2510.24081v2) scores 99% on Russian and 94–98% on Northern Uzbek.
- Uzbek Latin and Cyrillic scripts differ by about 1 point (TUMLU). Mixed Russian-Uzbek text has no published evidence.
- The task is easier than exam knowledge: topic recognition plus a short summary. Published evidence still cannot pick a model, so #10's eval decides.

### #7 Fit with the be sdk `Ai` seam

All be sdk links pin [`bd1d317`](https://github.com/wow-two-sdk-beta/wow-two-sdk-beta.be/commit/bd1d3173e4f82cbac39aa53835716ae546344018).

- The seam is `Microsoft.Extensions.AI` 10.8.3: brokers register an `IChatClient` and terminate with [`ChatExtensions.Apply`](https://github.com/wow-two-sdk-beta/wow-two-sdk-beta.be/blob/bd1d3173e4f82cbac39aa53835716ae546344018/engineering/codebase/wow-two-sdk-beta-be/src/Ai/Core/ChatExtensions.cs#L20-L32), which adds function invocation and OpenTelemetry.
- Only Ollama ships ([`AddOllamaChatClient`](https://github.com/wow-two-sdk-beta/wow-two-sdk-beta.be/blob/bd1d3173e4f82cbac39aa53835716ae546344018/engineering/codebase/wow-two-sdk-beta-be/src/Ai/Ollama/OllamaChatClientServiceCollectionExtensions.cs#L17-L28)). [`Ai.md`](https://github.com/wow-two-sdk-beta/wow-two-sdk-beta.be/blob/bd1d3173e4f82cbac39aa53835716ae546344018/engineering/codebase/wow-two-sdk-beta-be/src/Ai/Ai.md#L36-L44) lists Anthropic, OpenAI and Azure OpenAI as pending; the `OpenAi/` and `AzureOpenAi/` folders are empty.
- [`Directory.Packages.props`](https://github.com/wow-two-sdk-beta/wow-two-sdk-beta.be/blob/bd1d3173e4f82cbac39aa53835716ae546344018/engineering/codebase/wow-two-sdk-beta-be/src/Directory.Packages.props#L224) pins the community `Anthropic.SDK` 5.1.0, which no project references. The official NuGet `Anthropic` replaces it.
- Two brokers cover every provider in #3:
  - `AddAnthropicChatClient(apiKey, model)` on the official `Anthropic` package's `IChatClient`.
  - `AddOpenAiCompatibleChatClient(baseUrl, apiKey, model)` on `OpenAI` + `Microsoft.Extensions.AI.OpenAI`. One base URL each reaches OpenAI, DeepSeek, Kimi, Qwen, xAI, Mistral, Groq, Together, Fireworks, OpenRouter, Gemini's compatibility endpoint and Ollama's `/v1`.
- `IChatClient` leaves gaps the brokers fill:
  - Batch APIs are provider-specific. Add Anthropic Message Batches only when paid spend starts (#2).
  - Verify that the official Anthropic `IChatClient` maps `ChatResponseFormat.ForJsonSchema` to `output_config.format`. If it does not, the W1 path calls the native client.
  - Thinking and effort ride `ChatOptions.AdditionalProperties` or the raw-request hook.
  - `UsageDetails` feeds SCFD's `AiStamp.Tokens` and the G5 budget.
- Haven already holds both brokers: [`Haven.Platform.Ai`](https://github.com/sulton-max/10x-ven-haven/tree/9bc72ec0707203906cc4f871fbf4cba28cafde99/engineering/codebase/haven.backend-services/Haven.Platform/Haven.Platform.Ai) routes Anthropic and OpenAI-compatible (OpenAI, Gemini, DeepSeek) calls over raw HTTP, with model tiers, per-token pricing and strict-schema cleanup. Its `AiCompletionService` names itself the extraction candidate for the SDK providers, so the be sdk pass extracts it instead of starting fresh.
- Per the SDK doctrine, both brokers land in the be sdk as one vector pass, never inside SCFD.

## Integration

### #8 Access before building

- Anthropic needs nothing new: the key comes from the `WoW 2.0` Console org that holds the credit.
- OpenAI needs nothing new either: Haven's account already pays for GPT (developer, 2026-11-10), so `gpt-6-luna` and `gpt-6.1-terra` are a key away.
- Every other reserve needs an account and a card that works from Uzbekistan, unverified for all of them.

### #9 Plugging into SCFD and Events

SCFD links pin harvest [`6254896`](https://github.com/wow-two-sdk-beta/wow-two-sdk-beta.harvest/commit/625489670aa4074da826ef2cb026c7d1bab6bcbe) and adapters [`4110b99`](https://github.com/wow-two-sdk-beta/wow-two-sdk-beta.harvest-adapters/commit/4110b99978ee90086a1a2dead40ee8e89848fa64); Events links pin [`1d14977`](https://github.com/wow-two-sdk-beta/wow-two-sdk-beta.events/commit/1d14977c1ad2be0ba17183ea93b8038bd6d8e7db).

1. **Subscription AI config (SCFD, public).** [`AiMode`](https://github.com/wow-two-sdk-beta/wow-two-sdk-beta.harvest/blob/625489670aa4074da826ef2cb026c7d1bab6bcbe/engineering/codebase/harvest.backend-services/packages/Abstractions/Pipelines/AiMode.cs#L4-L14) (`Off`, `Gaps`, `Full`) already exists; extraction today answers `ai_skipped:capability_unavailable`. Add to the subscription a profile key, provider, model and monthly USD cap, as the [service spec](harvest-service-spec.md) plans under *AI gates*.
2. **Tier S extractor (SCFD, public).** It runs after D and R, behind gates G1–G5, and resolves `IChatClient` from the be sdk. It masks contacts, calls once per `(inputHash, profile, promptVersion)`, and stamps [`AiStamp`](https://github.com/wow-two-sdk-beta/wow-two-sdk-beta.harvest/blob/625489670aa4074da826ef2cb026c7d1bab6bcbe/engineering/codebase/harvest.backend-services/packages/Abstractions/Extraction/AiStamp.cs#L4-L16) with model, prompt version and tokens.
3. **Profile `ocharo-relevance@1` (adapters, private).** The rubric, few-shot examples and JSON schema live beside [`OcharoFashionFilter`](https://github.com/wow-two-sdk-beta/wow-two-sdk-beta.harvest-adapters/blob/4110b99978ee90086a1a2dead40ee8e89848fa64/engineering/codebase/harvest-adapters.backend-services/packages/Module/Ocharo/OcharoFashionFilter.cs#L17-L35), since Ocharo policy stays private. Schema: `{ summary, relevance: close | loose | none, reason, language }`; the summary is in English, 1–2 sentences.
4. **Wider candidate filter.** The model can only recover what reaches it. In `full` mode the Ocharo subscription delivers every event-kind post with the profile's verdict, not only what `ocharo-fashion-v1` passes. The keyword filter stays as the classifier for sources without AI.
5. **Delivered verdict.** The record carries Events' existing `classification` object, read by [`IntakeVerdict.FromPayload`](https://github.com/wow-two-sdk-beta/wow-two-sdk-beta.events/blob/1d14977c1ad2be0ba17183ea93b8038bd6d8e7db/engineering/codebase/events.backend-services/packages/Module/Intake/IntakeVerdict.cs#L36-L55): `{ classifier: "ocharo-relevance@1", verdict, confidence, reason }`.
   - `close` maps to `relevant` at confidence 0.9, `loose` to `relevant` at 0.6, `none` to `irrelevant` at 0.9.
   - Fixed confidences per label replace the model's self-reported number, which is poorly calibrated.
   - A failed, refused or over-budget call omits `classification`, so Events holds the record as a candidate.
6. **Events auto review (#53).** The intake source sets [`Review = auto`, `Classifier = payload`](https://github.com/wow-two-sdk-beta/wow-two-sdk-beta.events/blob/1d14977c1ad2be0ba17183ea93b8038bd6d8e7db/engineering/codebase/events.backend-services/packages/Module/Intake/EventsIntakeSourceOptions.cs#L49-L74) and `MinConfidence = 0.5`, which publishes close and loose. Raising it to 0.75 publishes close only, with no code change.
7. **Shadow first.** For one week SCFD writes `classification` while Events keeps `Classifier = filter`. Compare the two verdicts per record, then switch.
8. **W2 later.** Precise fields run as tier L under the Ocharo subscription's consumer schema, mapping first, with the model filling gaps (spec T6 § 3). They run only on records W1 marked close or loose.

## Eval

### #10 Plan

The eval runs on real data after the integration (developer, 2026-11-10), with no offline run first. The shadow week in #9 step 7 produces the items: Haiku 5.5 classifies live SCFD deliveries while Events keeps the filter classifier. An agent then labels a sample, and Sonnet 5.5 re-runs the same captures as the ceiling. The re-runs cost under $10 and draw on the credit.

| Slice | Items | Source | Expected label |
|---|---|---|---|
| Desk positives | 40 | captures of 40 of the 51 Desk events that carry a `sourceUrl` in the 68-row import bundle (`ocharo-desk-events-2026-11-10.json`), stratified by kind: trade fair 10, runway 8, festival 6, competition 6, exhibition 5, market 5 | close, or loose where the page only mentions a textile segment |
| Afisha mixed | 30 | captures on `harvestadapters-dev` from both Afisha channels, through a deeper bounded run than the 5-page acceptance sample | labeled per the rubric |
| Clear negatives | 20 | concerts, IT, food, sport, auto, children's events | none |
| Near misses | 10 | craft beer fairs, "в моде" idioms, jewelry crime news, textile factory news, beauty contests | none or loose per the rubric |

- Languages: at least 50 Russian, 25 Uzbek (10 or more each of Latin and Cyrillic) and 15 English items. Afisha is mostly Russian, so Uzbek items come from Uzbek pages of the Desk sources (expo centres, Uzbek news and Telegram channels).
- Inputs are the SCFD capture text, never Desk's curated English facts, so the eval sees what production sees. The developer's 68 curated events anchor the positives in human judgment.
- Labels: an agent session labels by hand against the rubric (#52's manual work); the developer settles only the disputed items, about 10.
- The set lives in the private adapters repo beside the profile, since captures stay internal (#50).

Metrics and pass bars:

| Metric | Bar |
|---|---|
| Publish recall (close or loose found) | ≥ 0.95 overall, ≥ 0.90 on the Uzbek slice |
| Publish precision | ≥ 0.90, since a false positive shows on Desk |
| Severe errors (close ↔ none) | ≤ 2 of 100 |
| Schema-valid JSON | 100% |
| Label flips across 2 runs | ≤ 3% |
| Summary faithfulness, 20 sampled | ≥ 19 of 20 |
| Baseline | beat `ocharo-fashion-v1`'s recall on the same set at equal or better precision |

- Run order: Haiku 5.5 live, then Sonnet 5.5 and Opus 5.5 on the same captures as the ceiling.
- Pick the cheapest model that clears every bar; on a tie, pick the credit-funded one.
- Add `gpt-6-luna` through Haven's OpenAI account if Haiku fails the Uzbek slice; it costs the same per token.
- W2's eval waits for its fields. It reuses the 40 Desk positives, whose `facts` (kind, organizer, place, deadlines) are the expected values.

## Sources

Read 2026-11-10 unless marked. Per-provider notes with every figure and gap sit outside the repo in the orchestrator's shared notes folder, under `ai-providers/`; the links above carry the primary sources.

- Anthropic: [pricing](https://platform.claude.com/docs/en/about-claude/pricing), [multilingual support](https://platform.claude.com/docs/en/build-with-claude/multilingual-support), [retention](https://privacy.claude.com/en/articles/7996866-how-long-do-you-store-my-organization-s-data), [supported regions](https://www.anthropic.com/supported-countries), [commercial terms](https://www.anthropic.com/legal/commercial-terms).
- Evals: [TUMLU](https://arxiv.org/html/2502.11020v2), [Global PIQA](https://arxiv.org/html/2510.24081v2), [IdrockBench](https://github.com/azizkayumov/IdrockBench/blob/main/LEADERBOARD.md), [INCLUDE](https://arxiv.org/html/2411.19799).
- Gaps still open:
  - Uzbek card acceptance at every non-Anthropic provider.
  - Kimi's official price table, which rendered empty.
  - Per-model rate limits at Google and Mistral.
  - Global PIQA's per-language data for current small models, which sits on the authors' GitHub, unread.

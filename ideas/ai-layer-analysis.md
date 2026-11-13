# AI layer: analysis and target design

*Reviewed: 2026-11-13. Scope: the be sdk's AI code, Haven's AI layer, every other AI consumer, and a target design for providers, prompt versions, an inference log with prices, and a generic eval layer that SCFD uses first. Track doc: [events-integration](../system/sessions/events-integration/events-integration.md) (#54, #55, #64). Provider pick: [ai-classification-providers](ai-classification-providers.md). be sdk links pin [`bd1d317`](https://github.com/wow-two-sdk-beta/wow-two-sdk-beta.be/commit/bd1d3173e4f82cbac39aa53835716ae546344018); Haven links pin [`9bc72ec`](https://github.com/sulton-max/10x-ven-haven/commit/9bc72ec0707203906cc4f871fbf4cba28cafde99).*

## Status

- ✅ OQ-1 home of the AI layer: (a), one domain repo `wow-two-sdk-beta.ai` (developer, 2026-11-13: "yes let's extract it and let's get it working")
- ✅ #7 prompts live in tables only, one table for both modes (developer, 2026-11-13)
- ✅ #9–#11 evals as proposed (developer, 2026-11-13: "great")
- ✅ #14 steps 1–4: repo `wow-two-sdk-beta.ai` built and pushed (`aaab511`); its version track v0.1 holds the state
- 🔄 HTTP API with queued eval runs (developer, 2026-11-14), paused 2026-11-14 for the weekly usage limit; resumes 2026-11-18
- ⬜ #14 step 5: the first 10-post eval, then SCFD's relevance step

## Findings

### #1 be sdk today

- Real LLM code is ~165 lines: [`ChatExtensions.Apply`](https://github.com/wow-two-sdk-beta/wow-two-sdk-beta.be/blob/bd1d3173e4f82cbac39aa53835716ae546344018/engineering/codebase/wow-two-sdk-beta-be/src/Ai/Core/ChatExtensions.cs#L20-L32) (function invocation + OpenTelemetry), `AddOllamaChatClient`, `AddOllamaEmbeddingGenerator`, and `AddTiktokenTokenCounter`.
- `Ai/Mcp` (~395 lines) hosts product tools over MCP (`AddStatelessMcpServer`, `MapAuthenticatedMcp`); it is web hosting, not an LLM client.
- 15 folders are empty: `Anthropic`, `OpenAi`, `AzureOpenAi`, `Gemini`, `Bedrock`, `Llama`, `SemanticKernel`, `KernelMemory` and all 7 `Vector/*`.
- `Directory.Packages.props` pins unused packages: `Anthropic.SDK` 5.1.0, Semantic Kernel 1.30.0 with 2 connectors, `KernelMemory.Core`, `LLamaSharp` 0.19.0.
- The csproj comment at the AI item group still describes M.E.AI `9.0.0-preview.9`; 10.8.3 is pinned.
- Tests: 19 MCP tests and 1 Ollama resolve test; nothing covers `Apply` or the token counter.
- Missing entirely: structured JSON output, provider fallback, retries, usage and cost capture, named providers chosen by config, prompt storage, eval runs.
- Consumers: sift (one Ollama call, `LlmVideoAssessor`), wheelhouse and transcript-forge (MCP hosting only); the token counter has none.

### #2 Haven today

- [`Haven.Platform.Ai`](https://github.com/sulton-max/10x-ven-haven/tree/9bc72ec0707203906cc4f871fbf4cba28cafde99/engineering/codebase/haven.backend-services/Haven.Platform/Haven.Platform.Ai) holds raw-HTTP brokers for Anthropic and OpenAI-compatible APIs, `AiCompletionService` (primary route, retries, fallback route), `AiAttempt`, `AiErrorKind`, model tiers, per-model prices in config and strict-schema cleanup (`AiJsonSchemas`).
- Prompt versions are not a registry: 1 embedded file, `classify-prompt.md`, plus a config string `Classification:PromptVersion` (`0.5`) bumped by hand; nothing ties the string to the file's content.
- Results keep history per version: `listing_classification_results` is unique on (listing, prompt version) and stores attempts as JSONB plus `ai_estimated_cost_micro_usd`.
- Prices live only in `appsettings.json` (`Ai:Providers:{provider}:Tiers:{tier}:Pricing`), with no history.
- Evals are manual: a checklist doc, a cost audit and sample batches under `engineering/research/classification/`; the backlog plans "fixed set, judge model, trend per prompt".
- 1 consumer: `ListingClassifier.ClassifyBatchAsync` (Supply), Anthropic Core with an OpenAI Pro fallback, 5 listings per call.
- Liftable as is: brokers, routing, error kinds, micro-USD cost, schema cleanup. New in the shared layer: prompt registry, inference log, response cache, eval harness.

### #3 Other consumers

- transcript-forge calls Groq Whisper over raw `HttpClient` for speech to text, not an LLM.
- your-pocket-doctor (legacy lab) has its own OpenAI code, off the SDK.
- Planned only: harvest's `AiMode`, `AiStamp` and `PostClassification` (no provider call), the harvest spec's AI gates G1–G5, and AI tiers in several venture specs.

### #4 Building blocks

| Block | Fact (read 2026-11-13) | Use here |
|---|---|---|
| `Anthropic` NuGet 13.8.0 | `client.AsIChatClient(model, maxTokens, thinkingMode)`; a JSON-schema `ResponseFormat` maps to `output_config.format`; `ChatOptions.Reasoning.Effort` maps to effort; cache control rides content `AdditionalProperties`; needs M.E.AI.Abstractions ≥ 10.5.1 | Anthropic provider, replacing Haven's raw HTTP |
| `Microsoft.Extensions.AI.OpenAI` 10.8.3 / 11.0.0 over `OpenAI` 2.15.0 | strict JSON schema; `OpenAIClientOptions.Endpoint` reaches any OpenAI-compatible host | OpenAI, Groq, DeepSeek, Ollama `/v1` |
| `UsageDetails` | input, output, cached input, reasoning tokens, `AdditionalCounts`; Anthropic puts cache writes in `AdditionalCounts` | cost per call |
| `Microsoft.Extensions.AI.Evaluation` 11.0.0 | `IEvaluator` with numeric, boolean and string metrics; scenario runs per `ExecutionName`; records latency, model and usage per turn; disk JSON store and an HTML report; no dataset object; needs M.E.AI.Abstractions ≥ 11.0 | optional LLM-judge scorers later (OQ-4); its store does not join our prices |
| OpenTelemetry GenAI conventions | `gen_ai.request.model`, `gen_ai.usage.*`, `gen_ai.prompt.name`, `gen_ai.prompt.version`, `gen_ai.evaluation.*` (status Development) | span attributes on every call |
| Langfuse prompt management | immutable versions, movable labels (`production`), trace linked to the version | the registry's model (#7) |
| Prompty | one file: YAML front matter (model, inputs) plus the template | its fields map to a prompt row's columns (#7); no files |

## Target design

### #5 Repo and packages

- One domain repo, `wow-two-sdk-beta.ai`, holds every AI piece (OQ-1 (a)); NuGet `WoW2.Sdk.Beta.Be.Ai.*`, namespace `WoW.Two.Sdk.Beta.Be.Ai` kept.
- It qualifies under [capability forms](../conventions/development/capability-forms.md): it owns state (prompts, inference log, prices, evals) and secrets (provider keys), and serves Haven, SCFD, sift and later Ocharo.
- The [domain-structure](../conventions/development/repo/structure/domain-structure.md) rule "AI providers stay in core as a companion package" predates a stateful AI layer; providers move with the domain, so one release carries a provider fix, its usage capture and its eval.

| Package | Holds |
|---|---|
| `Ai.Abstractions` | the contract: `IAiRunner`, `IPromptSource`, `IInferenceLog`, `IEvalBroker`, records for prompt versions, inferences, prices, eval sets, runs and scores |
| `Ai.Providers` | named `IChatClient` providers (Anthropic, OpenAI-compatible, Ollama), the router with fallback and retries, usage-to-cost |
| `Ai.Module` | Form 1: PostgreSQL tables and migrations (#8), the prompt registry, the inference log, the eval runner and report, host verbs |
| `Ai.Testing` | a scripted fake `IChatClient`, the conformance suite |
| `service/Ai.Api` | the image: Hosting plus Module; the local eval bench first (#11), a provided AI service later (OQ-2) |

- Core keeps `Ai/Mcp` (OQ-5) and drops every LLM folder, the unused pins and the stale comment; sift re-pins to `Ai.Providers`.
- The token counter moves to `Ai.Providers` for pre-call budget checks.

### #6 Providers and routing

- `AddAiProviders(configuration)` registers one keyed `IChatClient` per `Ai:Providers:{name}` section that has a key: `Kind` (`anthropic`, `openai`, `ollama`), `BaseUrl`, `ApiKey`, `Timeout`.
- A route is an ordered model list per use case, `Ai:Routes:{useCase}` = `["anthropic/claude-haiku-5-5", "openai/gpt-6-luna"]`; the router retries transient failures, then moves to the next entry on failure, refusal or a schema-invalid answer.
- Every call records an inference (#8) per attempt, fallbacks included, and sets the OpenTelemetry GenAI attributes with `gen_ai.prompt.name` and `gen_ai.prompt.version`.
- Product code calls one typed method; the result carries the value and the inference:

```csharp
var answer = await ai.RunAsync<RelevanceAnswer>(
    "ocharo-relevance", new { title, text, language }, subject: $"harvest:post:{postId}@{revision}", ct);
// answer.Value, answer.Outcome, answer.Inference: id, prompt version, provider, model, tokens, costMicroUsd, latencyMs
```

- The output schema comes from the answer type (Haven's strict-schema cleanup); a JSON parse failure is outcome `schema_invalid`, never an exception.

### #7 Prompts: one table, two modes

- Prompts live in tables only, never in files or code (developer, 2026-11-13); `IPromptSource` resolves (use case, model) to a prompt row: system and user templates, parameters (temperature, max tokens, effort), version, content hash.
- Rewrite mode, no audit: a change updates the row in place and its `version` stays as it is; the content hash changes, so the inference log still tells two texts apart.
- Versioned mode, audited: a change inserts a new row with the next `version`; rows are never updated; labels (`production`, `candidate`) point at a version and move, so switching a label switches the prompt with no rewrite and no deploy; every label move is kept.
- The mode is a column on the use case (`ai_use_cases.prompt_mode`); both modes share `ai_prompts`, and the `version` column costs 4 bytes a row.
- Per-model variants: a prompt row may carry a model match (`claude-*`, `gpt-6-luna`); resolution takes the most specific match for the routed model, else the generic row.
- Seeding: a product ships its first prompt as a seed the module inserts once when the use case has no row; later edits happen in the table (verb, API, console).

### #8 Tables

`Ai.Module` adds these to the product's own database (Form 1); every price and token count sits in the main tables, and the report (#10) joins them.

| Table | Holds | Key columns |
|---|---|---|
| `ai_use_cases` | one row per use case | `key`, `description`, `prompt_mode` (`rewrite`, `versioned`), `output_schema`, `route` |
| `ai_prompts` | prompt texts for both modes | `use_case`, `model_match`, `version`, `system_template`, `user_template`, `params`, `content_hash`, `note`, `created_at`, `updated_at`, `created_by` |
| `ai_prompt_labels` | movable pointers for versioned mode, with a move history | `use_case`, `label`, `version`, `moved_at`, `moved_by` |
| `ai_model_prices` | per-model prices with history | `provider`, `model`, `effective_from`, input, output, cache-write and cache-read micro-USD per 1M tokens, `batch_discount` |
| `ai_inferences` | every call | `id`, `at`, `use_case`, `prompt_version`, `label`, `provider`, `model`, `attempt`, `subject_ref`, `input_hash`, input, output, cache-read, cache-write and reasoning tokens, `cost_micro_usd`, `latency_ms`, `outcome`, `error_kind`, `output`, `eval_run_id` |
| `ai_eval_sets` | a named item list per use case | `key`, `use_case`, `note` |
| `ai_eval_items` | a frozen input with its expected answer | `set_key`, `subject_ref`, `input` (the template variables), `expected`, `tags` (`lang:ru`, `slice:positive`), `labelled_by` |
| `ai_eval_runs` | one cell of the matrix | `id`, `set_key`, `prompt_version`, `content_hash`, `provider`, `model`, `started_at`, `finished_at`, `note` |
| `ai_eval_scores` | one item in one run | `run_id`, `item_id`, `inference_id`, `correct`, `score`, `metrics`, `rating` (1–5), `rated_by`, `comment` |

- Cost is computed at call time from the price row in effect and stored; a later price change never rewrites history.
- `ai_inferences` caches on (`use_case`, `prompt_version`, `model`, `input_hash`): a repeat call with the same input reuses the stored answer unless the caller asks for a fresh one.
- A subject purge (SCFD's `post.purged`) clears `output` on its inferences and its eval items' `input`.

### #9 Evals

- An eval set freezes each item's input when the item is added: the product's `IEvalSubjectSource` turns a subject (`harvest:post:{id}@{rev}`) into template variables once; runs never call the product again.
- A run is one prompt version × one model over a set; a matrix command starts several runs at once.
- Scoring: the default scorer compares named fields of the answer with `expected` (`relevance`, `kind`); a severe miss is configurable (close ↔ none); a product adds a scorer only when it needs one.
- Ratings: Claude or the developer rates any (run, item) 1–5 with a comment; mean rating sits beside accuracy.
- LLM-judge scorers from `Microsoft.Extensions.AI.Evaluation.Quality` plug in later as scorers (OQ-4).

### #10 The combined report

- One query, `ai_eval_report`, joins runs, scores, inferences and prices into one row per run and one row per (run, item).

| Per run | Per item |
|---|---|
| prompt version, model, items, accuracy, severe misses, schema-valid share, fallbacks, failures, total cost, cost per item, p50 and p95 latency, input, output and cached tokens, mean rating | subject ref, expected, answer fields, correct, cost, latency, outcome, rating |

- `ai eval report {set} --format json|csv|md` exports it; JSON carries the answer fields only on request (`--with-output`), never the input text.

### #11 The Claude Code eval loop

1. Pick items from the product's store (read-only) and add them to a set with expected labels: `ai eval set add afisha-10 --subject harvest:post:{id}@{rev} --expected '{"relevance":"close","kind":"runway"}'`.
2. Run the matrix: `ai eval run afisha-10 --prompt ocharo-relevance@1,@2 --model anthropic/claude-haiku-5-5,openai/gpt-6-luna,anthropic/claude-sonnet-5-5`.
3. Read the report as JSON, rate items, add the changed prompt as a new version, rerun.
4. Move the `production` label to the winner (versioned mode), or rewrite the row to the winner's text (rewrite mode).

- The bench is local: `service/Ai.Api` in Compose with its own PostgreSQL, keys in user-secrets; a set exported from a product database (`ai eval set export`) imports there, so evals need no product host.

### #12 What stays out of git (#50)

- Item inputs, model answers and post text live only in a database (product or local bench), never in a repo.
- A repo may record the summary only: per run, prompt version, model, accuracy, severe misses, cost per item and latency.

### #13 Consumers

| Consumer | Change |
|---|---|
| SCFD (`wow-two-sdk-beta.harvest`) | tier S calls `RunAsync("ocharo-relevance", …)` under `AiMode`; `AiStamp` gains the inference id and prompt version; `PostClassification` carries the verdict to Events |
| Events | `Classifier = payload` after the eval; W2 precise classification later on the same layer |
| Haven | `Haven.Platform.Ai` retires; `ListingClassifier` moves to `RunAsync` and the registry; its own result tables stay (Haven's work, its own chat) |
| sift | re-pins `AddOllamaChatClient` to `Ai.Providers` |
| wheelhouse, transcript-forge | none, while MCP stays in core |

### #14 Build order

1. Create the repo with `create-library`; the developer's hand steps arm NuGet and npm.
2. `Ai.Providers` with the router and prices; core drops its LLM folders in the same pass; sift re-pins.
3. Prompts (both modes) and the inference log.
4. Eval sets, runs, scores, the report and the verbs; the local bench.
5. SCFD's relevance step on the layer, then the first 10-post eval (#55).
6. Haven moves to the layer, in Haven's own chat.
7. Later: the provided service and console pages, budgets (gate G5), batch APIs, LLM-judge scorers.

## Open questions

- OQ-1 Home: (a) one domain repo for providers and the stateful layer, MCP stays in core; (b) providers stay in core, the stateful layer becomes a domain repo; (c) everything stays in core. Proposed (a): one release loop per AI change, and the domain rule's "stateless providers" premise no longer holds.
- OQ-2 The provided AI service (Form 3) with keys and budgets in one place: later; the bench image comes first.
- OQ-3 M.E.AI 11: the new repo starts on 11.0.0, since `Microsoft.Extensions.AI.Evaluation` 11 needs it; core's MCP package must resolve against it.
- OQ-4 Scorers: own `IEvalScorer` with exact-field match first; M.E.AI.Evaluation judges wrap into it later.
- OQ-5 MCP hosting stays in core under `Ai/Mcp`, or moves to `Web/Mcp` with the LLM folders gone.
- OQ-6 Model answers in `ai_inferences.output`: kept in production too, in the product's database only, cleared on purge.

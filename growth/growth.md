# Growth Roadmap

*Last updated: 2026-07-02*

> Personal career growth — self-directed learning and skill-building. Distinct from employer-assigned work (EPAM / EBSCO project).
>
> **Staging file.** One giant doc for now — iterate and refine here, add/cut/reorder tracks freely. Once a track stabilizes, extract it into its own file/folder under `growth/` (mirrors `explore/explore.md` → `explore/platforms/{vendor}.md`).

## Tracks

| Track | Focus | Mode | Priority | Status |
|---|---|---|---|---|
| [C# Deep Mastery](#1-c-deep-mastery) | Language/runtime internals, performance | Dedicated study | high | `todo` |
| [wow-two SDK Building](#2-wow-two-sdk-building) | Platform/SDK architecture, API design, packaging | Learning-by-building | high | `active` |
| [Startups](#3-startups) | Idea validation, GTM, indie-hacker execution | Learning-by-building | normal | `active` |
| [Tool Building](#4-tool-building) | CLI/dev-tool craft, DX, distribution | Learning-by-building | normal | `active` |
| [Learning Tools](#5-learning-tools) | Rider full mastery (+ others TBD) | Dedicated study | normal | `todo` |

*(Priorities are a starting proposal — overwrite freely.)*

---

## 1. C# Deep Mastery

**Why:** app-level C# is solid; the gap is runtime/language internals — the stuff that shows up in perf-critical code, SDK design, and senior-level interviews.

**Current level:** production-proficient, not internals-proficient.

### Memory & GC
- [ ] GC generations, workstation vs server GC, concurrent/background modes
- [ ] LOH (Large Object Heap), fragmentation, `GCSettings`
- [ ] `Span<T>` / `Memory<T>` / `ReadOnlySpan<T>` — when and why
- [ ] `stackalloc`, `ref struct`, ref fields (C# 11+)
- [ ] Boxing/unboxing costs, `ArrayPool<T>`, `ObjectPool<T>`

### Concurrency
- [ ] `Task` internals — state machine, continuations, `TaskScheduler`
- [ ] `ValueTask` — when it actually saves allocations
- [ ] `SynchronizationContext` deep dive — why `ConfigureAwait(false)` matters where
- [ ] `System.Threading.Channels` for producer/consumer
- [ ] Lock-free structures, `Interlocked`, `Volatile`, memory model basics

### JIT & compilation
- [ ] Tiered compilation, ReadyToRun, Native AOT — tradeoffs
- [ ] IL basics — read the IL for a hot method, understand what the JIT does with it
- [ ] Roslyn source generators (ties into [SDK track](#2-wow-two-sdk-building) — migrator/analyzer work already touches this)

### Performance measurement
- [ ] BenchmarkDotNet — write real benchmarks, not guesses
- [ ] `dotnet-trace`, `dotnet-counters`, `dotnet-dump` — diagnose one real perf issue end to end
- [ ] SIMD via `System.Numerics` / `Vector<T>` — one real use case

### Advanced language
- [ ] Generic variance (`in`/`out`) — where it actually matters
- [ ] Expression trees — build one, understand what LINQ providers do with them
- [ ] Reflection emit vs source generators — when each wins

### Resources (seed — verify/expand)
- *C# in Depth* (Jon Skeet) — language design rationale
- *Writing High-Performance .NET Code* (Ben Watson) — GC/perf from a practitioner
- `dotnet/runtime` source on GitHub — read real implementations, not just docs
- Microsoft Learn — GC / JIT internals docs

---

## 2. wow-two SDK Building

**Why:** the primary learn-by-shipping track — `wow-two-sdk`, `wow-two-sdk-beta`, `wow-two-platform` are real packages with real consumers (drydock, secrets-vault, forever-pin, …). Every design decision is a forcing function for API design, versioning discipline, and backward-compat thinking.

**Current level:** actively building — identity baseline shipped, messaging layer scaffolded, errors-layer redesign in progress, Testing.Data companion adopted across all 3 apps.

### Topics
- [ ] API design — what makes a public surface hard to evolve later (case study: the errors-layer two-model problem)
- [ ] SemVer discipline in practice — when a change actually needs a major bump
- [ ] Package composition — mono-lib vs companion packages (the `FrameworkReference` DI-downgrade gotcha already hit once — codify the lesson)
- [ ] NuGet publishing pipeline — beta channel vs stable, `wow-two-platform.pipelines` templates
- [ ] Cross-repo dependency management — updating a lib without breaking N consumers
- [ ] Writing SDKs people other than you can onboard to (XML docs, README, samples)
- [ ] Infra-extracts-to-SDK discipline — products stay business-logic-only; infra built inline first, extracted to beta SDK in the `+0.1`

### Active/ongoing work already driving this track
- Errors/results/exceptions redesign (ErrorOr-style target)
- Messaging layer (clean-room abstraction, in-memory transport, routing-slip saga)
- Identity SPA gaps (CORS, cookie modes)

### Next deliberate step
- [ ] TBD — pick one lesson from the errors-layer investigation and write it up (turns learning-by-doing into retained knowledge)

---

## 3. Startups

**Why:** the micro-SaaS portfolio play (3–5 first batch, 50–100 launches target by EOY 2026) is itself the curriculum — the skill to build is *fast validated shipping*, not any single product.

**Current level:** multiple ventures in flight (forever-pin, Whiteout, Hijinx/fun-vault, string-art, LumenCrystal).

### Topics
- [ ] Idea → validation loop — how fast can an idea go from spec to "worth continuing"
- [ ] Positioning & pricing — one-liner + price point before writing code
- [ ] Distribution channels that don't require an existing audience (SEO, communities, cold outreach, marketplaces)
- [ ] Metrics that matter pre-revenue (activation, retention proxies) vs vanity metrics
- [ ] Kill criteria — codify when to stop a venture (ties into the micro-SaaS portfolio kill gates)
- [ ] GWDNBM as a product filter (Get The Work Done & Never Bother Me — no ads, no engagement bait) — formalize into a pre-launch checklist

### Resources (seed — verify/expand)
- *The Mom Test* (Rob Fitzpatrick) — validation without leading the witness
- Indie Hackers case studies — pattern-match against what's already working for the portfolio

---

## 4. Tool Building

**Why:** internal tools (migrators, CLIs, scrapers) are smaller-scoped than the SDK but teach DX and distribution — designing for a user who is future-you or a teammate, not an end customer.

**Current level:** shipped `forever-pin-migrate` CLI, package-analyzer, yt-scraper POC.

### Topics
- [ ] CLI design — `System.CommandLine`, argument/option ergonomics, good `--help` output
- [ ] Tool distribution — `dotnet tool install`, npm global installs, single-binary AOT publish
- [ ] Idempotency & dry-run patterns for anything that mutates state (migrator precedent)
- [ ] Config/secrets handling for tools that aren't web apps
- [ ] When to extract a one-off script into a real reusable tool vs. leave it a script

### Next deliberate step
- [ ] TBD — candidate: generalize the forever-pin SQL migrator into the backend-beta SDK migrator (proving ground already validated 2026-06-11)

---

## 5. Learning Tools

**Why:** the IDE is where most of the day happens — marginal fluency gains compound daily. Currently using Rider day to day but not deliberately mastering it.

### 5.1 Rider — full mastery
- [ ] Debugger — conditional breakpoints, tracepoints, Evaluate & Log, Smart Step Into
- [ ] Profiling — dotTrace (CPU/timeline) and dotMemory (allocations, leaks)
- [ ] Refactorings — full catalog beyond rename/extract (Move to Namespace, Change Signature, Safe Delete, Type Migration)
- [ ] Live Templates & File Templates — custom ones for repeated wow-two patterns (e.g. new CQRS handler scaffold)
- [ ] Structural Search & Replace — pattern-based refactors across a solution
- [ ] Database tools — connect directly to the Postgres instances behind drydock/secrets-vault in-IDE
- [ ] HTTP Client (`.http` files) — replace ad-hoc curl/Postman for API testing
- [ ] Docker/container tools integration
- [ ] Keymap — commit to one scheme, learn it cold for the top ~20 actions
- [ ] Settings Sync + `.editorconfig` enforcement across all wow-two repos

### 5.2 Other tools (TBD)
- [ ] *(add here — Rider was the only one named so far)*

---

## Open Questions

- Sequencing — which track gets dedicated time first? SDK / Tools / Startups run "ongoing" by default since they're driven by active work; C# Deep and Rider need carved-out time to happen at all.
- `10x-ws`'s `domain-career.md` routes personal career growth to `career/growth/` in the 10x-ws context tree. This file lives in `wow-two-ws` instead (deliberate — engineering-heavy content, closer to where the work happens). Worth a thin pointer from the 10x-ws side later, or fine to leave this as the sole source?
- Split trigger — extract a track into its own file when its checklist is mostly checked off, or once it just gets long?

## Next Steps

1. React to this draft — cut what's wrong, reorder priority, call out anything missing.
2. Once a track stabilizes, extract its `##` section into `growth/{track}/` (mirrors `explore/explore.md` → `explore/platforms/`).

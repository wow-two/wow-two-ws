# WoW 2.0 — Refinement & Roadmap

> **Goal**: Get the project "on rails" so we can iterate and build. No more scattered Notion docs — everything lives in repos with Claude-powered workflows.

---

## Vision

**WoW 2.0** (Way of Web 2.0) is a full-stack developer ecosystem for building production apps with .NET + React. It provides plug-and-play libraries, pre-built clients, Docker images, and hosted APIs — backed by a wiki of real-world knowledge (usage patterns, gotchas, solutions) for every piece of technology used. Built first for the internal team, designed to scale worldwide.

### Audience

- **Phase 1**: Internal team — standardize how we build
- **Phase 2**: Open-source community — anyone can adopt the ecosystem

### What developers get

| Format | Example |
|--------|---------|
| **NuGet/npm library** | `sdk.storage.cache` — add to project, configure, done |
| **Pluggable client** | Pre-built API client with typed contracts |
| **Docker image** | `docker run wow-cache` — run locally or host |
| **Hosted API** | Managed service for select tools |
| **Wiki + knowledge base** | Real issues, patterns, decisions — not just API docs |

### Community phasing

1. **GitHub-only** — issues, discussions, PRs, code-focused
2. **Short-form content** — YT usage videos, quick demos for exposure
3. **Full presence** — podcasts, developer support, events

### WoW 2.0 → 3.0 transition

WoW 2.0 is "done" when the core .NET + React stack has full coverage (libs + docs + templates). WoW 3.0 makes AI a first-class citizen — not an add-on but baked into every template and workflow.

---

## Current State (Feb 2026)

### What exists

| Area | Status | Notes |
|------|--------|-------|
| **Backbone** (18 NuGet libs) | ~60% done | Time, enums, LINQ, serialization, caching, DI, comms (MediatR+MassTransit), AI (SemanticKernel, NLP). Published packages exist. |
| **Backend** (22 learning repos) | Stale | LLA/ILA/HLA modules — concurrency, generics, data access, security, middleware. Last updates ~2024. |
| **Wiki** | Sparse | Backend arch docs, HttpClient, MediatR examples, Azure AI. Mostly stubs. |
| **Projects** (8 apps) | Mixed | Feedback.Analyzer most complete. DDLParser, StudyMate, AirBnb clone exist. |
| **Core tools** | 1 tool | PackageAnalyzer — batch repo/package management. |
| **Pipelines** | Exists | GitHub Actions for NuGet publish (pre-release + release). |
| **Frontend** | Missing | No React ecosystem despite being in the vision. |
| **CLI** | Missing | No scaffolding/DX tooling. |
| **Claude setup** | ✅ Root done | Workspace CLAUDE.md + .claude/rules/ created. Child repo CLAUDE.md templates needed. |
| **PM** | Empty | No roadmap, milestones, or contribution guidelines. |
| **Docs site** | Missing | No unified documentation portal. |

### What's broken

- Definitions written in Notion years ago — not in repos, not versioned
- No Claude setup in any repo — can't leverage AI for development
- Last meaningful updates were months ago
- No clear onboarding path for new contributors
- Backend learning repos vs Backbone production libs boundary is unclear
- No frontend story at all

---

## Tasks

### T1: Define WoW 2.0 Concept & Approach

**Analyze the vision, tools, DX, and community strategy.**

- [x] Define WoW 2.0 in one paragraph — see Vision section above
- [x] Clarify the layer model — platform (infra) → sdk (public libs) → kb (knowledge) → apps (products)
- [ ] Define "DX platform" scope: libs + templates + CLI + docs + community
- [ ] List all tools/libs to build with priority (P0/P1/P2)
- [x] Define community touchpoints — GitHub → YT short-form → podcasts/events
- [x] Decide: both — internal-first tooling org + public teaching/knowledge platform
- [ ] Write the "WoW Way" — opinionated decisions (why EF Core, why MediatR, why Clean Arch)
- [x] Define WoW 3.0 transition criteria — full .NET + React coverage = done, then AI-native

### T2: Claude Setup for Project Management

**Analyze how we integrate Claude across the ecosystem.**

- [x] Create root `CLAUDE.md` — workspace-level context, layout, tech stack, working rules
- [x] Create `.claude/rules/repo-registry.md` — full index of all repos across all orgs
- [x] Create `.claude/rules/behavior-rules.md` — lookup rules, cross-repo workflow, naming conventions
- [x] Create `.gitignore` — meta repo tracks only Claude config, ignores child repos
- [ ] Create `CLAUDE.md` templates for each repo type (platform lib, sdk package, kb module, app)
- [ ] Define Claude workflows: code review, PR descriptions, changelog generation, issue triage
- [ ] Setup Claude for documentation generation from code
- [ ] Define prompt templates for common tasks (new sdk package, new kb entry)
- [ ] Create a "Claude onboarding" doc — how contributors use Claude with WoW repos
- [ ] Evaluate Claude Code + GitHub Actions integration for CI

**Architecture decision**: workspace root = `wow-two` meta git repo. Child repo folders are git-ignored. Claude opens the workspace root and lazy-loads child repos on demand. Each child repo will have its own `CLAUDE.md` that overrides root rules.

### T3: Repo Structure & Indexing

**Analyze how repos are organized and what role each plays.**

- [x] Create a repo registry — done in `.claude/rules/repo-registry.md`
- [x] Define repo naming convention — `{category}.{domain}`, lowercase, dot-separated. See Org Structure section.
- [x] Categorize repos into 5 orgs: wow-two, wow-two-platform, wow-two-sdk, wow-two-kb, wow-two-apps
- [ ] Decide: monorepo vs multi-repo per area (currently multi-repo — is that right?)
- [ ] Define repo lifecycle: draft → active → stable → archived
- [ ] Add `CLAUDE.md` + `README.md` + `.github/` templates to every repo
- [ ] Setup GitHub org labels, milestones, and project boards
- [ ] Create dependency graph — which Backbone packages depend on which
- [ ] Define versioning strategy (SemVer + pre-release conventions)

### T4: Pre-Build Foundations (Do Before Writing Code)

**What else needs to happen before we start building new tools.**

- [ ] Migrate all Notion definitions into repo markdown files
- [ ] Audit existing Backbone packages — which are production-ready, which need work
- [ ] Define .NET version policy (.NET 8 LTS? .NET 9? Multi-target?)
- [ ] Define React stack decisions — Vite? Next.js? State management? Component lib?
- [ ] Create project templates (dotnet new + create-react-app equivalents)
- [ ] Setup unified CI/CD — extend existing Backbone.Pipelines to all repo types
- [ ] Create contribution guidelines (CONTRIBUTING.md, PR template, issue templates)
- [ ] Define package publishing workflow (local dev → pre-release → stable NuGet)
- [ ] Cleanup stale repos — archive or update Backend modules that haven't been touched
- [ ] Create a "Getting Started" guide — zero to working app in 15 minutes

---

## Priority Order

```
Phase 0 — Foundation (now)
├── T1: Define the concept (so we know what we're building)
├── T3: Repo structure (so we know where things go)
├── T2: Claude setup (so AI helps us from day one)
└── T4: Pre-build cleanup (so we start from a clean state)

Phase 1 — Core DX
├── Backbone package audit + updates
├── CLI scaffolding tool
├── Unified docs site
└── React ecosystem kickoff

Phase 2 — Community
├── Contribution guidelines + onboarding
├── Social events / meetups / content
└── Public launch

Phase 3 → WoW 3.0
├── AI-native templates
├── LLM-integrated development patterns
└── AI copilot patterns as first-class citizens
```

---

## GitHub Org Structure (Decided)

### Orgs

| Org | Link | Role |
|-----|------|------|
| **wow-two** | [github.com/wow-two](https://github.com/wow-two) | Entry point, meta, roadmap, org-wide CLAUDE.md & templates |
| **wow-two-platform** | [github.com/wow-two-platform](https://github.com/wow-two-platform) | Internal infra — pipelines, DI, internal APIs. Not used by outsiders. |
| **wow-two-sdk** | [github.com/wow-two-sdk](https://github.com/wow-two-sdk) | Public ecosystem — libs, tools, clients, Docker images. |
| **wow-two-kb** | [github.com/wow-two-kb](https://github.com/wow-two-kb) | Knowledge base — code samples + runnable demos. The "bible." |
| **wow-two-apps** | [github.com/wow-two-apps](https://github.com/wow-two-apps) | Community-driven real products. |

### Old orgs (transfer complete)

| Old | Target | Status |
|-----|--------|--------|
| `WoW-2-0` | wow-two + wow-two-kb | ✅ Done |
| `WoW-2-0-Backbone` | wow-two-platform + wow-two-sdk | ✅ Done |
| `WoW-2-0-Core` | wow-two-sdk + wow-two-kb | ✅ Done |
| `WoW-2-0-Wiki` | wow-two-kb | ✅ Done |
| `WoW-2-0-Projects` | *(staying as-is — mentee repos)* | Skipped |
| `WoW-2-0-Intelli-Flow` | *(archive)* | Skipped |

### Org boundaries

```
wow-two              "what is WoW 2.0?"
├── wow-two-platform "what powers it internally?"      (private)
├── wow-two-sdk      "what can I install and use?"      (public)
├── wow-two-kb       "how does X technology work?"      (public, code + docs)
└── wow-two-apps     "what's been built with it?"       (public, community)
```

### Two knowledge tracks

1. **wow-two-kb** — existing tech (EF Core, MediatR, React hooks, etc.) — code samples + docs. Static reference.
2. **wow-two-sdk docs** — WoW ecosystem docs live *inside each sdk repo*. Each component owns its own documentation.
3. **Interactive learning platform** — future app (lives in wow-two-apps or wow-two-sdk) built on top of kb content.

### Current repo distribution (post-migration)

| Org | ~Repos | Examples (new names) |
|-----|--------|---------|
| wow-two | ~6 | `refinement`, `roadmap`, `career-strategies` |
| wow-two-platform | ~17 | `platform.pipelines`, `platform.core.di`, `platform.comms.infra` |
| wow-two-sdk | ~7 | `sdk.language.core`, `sdk.package-analyzer`, `sdk.ai.semantic-kernel` |
| wow-two-kb | ~25 | `kb.dotnet.efcore`, `kb.dotnet.concurrency`, `kb.azure.ai-services` |
| wow-two-apps | — | *(staying in old WoW-2-0-Projects org)* |

### Repo naming convention (Decided)

**Format**: `{category}.{domain}` — lowercase, dot-separated, no org prefix in repo name.

```
Repo name:    platform.pipelines          (short, clean in org context)
NuGet name:   WoW.Two.Platform.Pipelines  (branded, globally unique)
Full path:    wow-two-platform/platform.pipelines
```

**Rules:**
- Lowercase everything
- Dots for hierarchy: `sdk.language.core`, `platform.storage.cache`
- Multi-word domains use hyphens: `platform.design-patterns`
- Drop old prefixes (Backbone.*, Backend.*)
- Repo name ≠ NuGet name — repos are short, packages are branded

**Categories per org:**
- `wow-two-platform` repos → `platform.*`
- `wow-two-sdk` repos → `sdk.*`
- `wow-two-kb` repos → `kb.*`
- `wow-two-apps` repos → `app.*`
- `wow-two` repos → no prefix (meta repos)

### Migration checklist

- [x] Create new GitHub orgs (wow-two, wow-two-platform, wow-two-sdk, wow-two-kb, wow-two-apps)
- [x] Transfer repos from old orgs to new orgs
- [x] Rename all repos to new `{category}.{domain}` convention
- [x] Categorize Backend repos → wow-two-kb (learning material)
- [ ] Update all repo references, links, package sources
- [ ] Archive old orgs (WoW-2-0, WoW-2-0-Backbone, WoW-2-0-Core, WoW-2-0-Wiki)
- [ ] Archive wow-two-0-intelli-flow
- [ ] Create `wow-two/workspace` repo — Claude orchestration hub (CLAUDE.md, .claude/rules/, .gitignore)
- [ ] Clone all repos into workspace folder, organized by org subfolder

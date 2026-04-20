# WoW 2.0 — Modular Library System Analysis

> **Goal**: Build the backbone and first libraries for wow-two-sdk to create a modular, reusable library system for both .NET backend and React frontend stacks.
>
> **Context**: Analysis of current workbench state, Haven venture patterns, and proposed architecture.

---

## 1. Current State Summary

### What Exists

| Layer | Repos | State | Notes |
|-------|-------|-------|-------|
| **SDK** (7 repos) | language.core, language.linq, language.serialization, resilience-patterns, package-analyzer, ai.semantic-kernel, ai.nlp | Mixed | Core/serialization have real code on feature branches; linq is empty; resilience-patterns is examples-only |
| **Platform** (16 repos) | core.di, core.app, core.exceptions, core.validations, comms.infra, data.relational, etc. | Mostly stubs | Architecture defined, naming done, but most repos are skeleton/placeholder |
| **KB** (21 repos) | dotnet.efcore, dotnet.mediatr, dotnet.di, etc. | Stale | Learning modules from 2024, code samples + docs |
| **Apps** (1 repo) | meme-world | Early | Single community app |
| **Ventures** (3) | 10x-ven-haven, 10x-fin-nt, your-pocket-doctor | Active | Haven is the most mature — full-stack .NET 9 + React 19 |

### Key Findings

**SDK packages that have real code (on feature/dev branches):**
- `language.core` — Enum extensions, time providers, type abstractions (.NET 9, benchmarked, tested)
- `language.serialization` — JSON abstractions + System.Text.Json + Newtonsoft implementations (.NET 9, feature-complete)
- `resilience-patterns` — Polly v8 example suite (comprehensive, but examples-only — not a library)

**Critical gaps:**
- No `Directory.Build.props` or `Directory.Packages.props` (no centralized build/version management)
- No CI/CD for SDK packages (pipeline templates exist in platform.pipelines but aren't wired)
- Version inconsistency: some packages target .NET 8, others .NET 9
- Naming inconsistency: `Backbone.*` vs `WoW2.Backbone.*` vs `WoW2.Sdk.*`
- No frontend SDK exists at all

### Haven as a Pattern Source

Haven (10x-ven-haven) is the most mature project in the workspace and demonstrates **proven patterns** we should extract:

**Backend (.NET 9):**
- 5 microservices + 5 shared common libraries
- Clean separation: Domain → Common → Common.Persistence → per-service layers
- Patterns: pipeline executor, Supabase client, LLM batch integration, phone normalization, config factories

**Frontend (React 19 + Vite + pnpm):**
- 5 apps + 3 shared packages (`@haven/common`, `@haven/ui`, `@haven/domain`)
- Workspace monorepo with pnpm
- Shared Vite config factory, TypeScript base configs, ESLint base config
- Radix UI + Tailwind CSS + CVA for component system
- Subpath exports for tree-shaking

---

## 2. .NET Backend — Modular Library Strategy

### 2.1 Proposed Package Hierarchy

```
WoW.Two.Sdk                              ← root namespace
├── Language                              ← language-level extensions (no framework deps)
│   ├── Core                              ← primitives: enums, time, types
│   │   ├── WoW.Two.Sdk.Language.Core.Enums
│   │   ├── WoW.Two.Sdk.Language.Core.Time
│   │   └── WoW.Two.Sdk.Language.Core.Types
│   ├── Linq                              ← LINQ extensions
│   │   └── WoW.Two.Sdk.Language.Linq
│   └── Serialization                     ← JSON abstractions + impls
│       ├── WoW.Two.Sdk.Language.Serialization.Abstractions
│       ├── WoW.Two.Sdk.Language.Serialization.SystemTextJson
│       └── WoW.Two.Sdk.Language.Serialization.Newtonsoft
│
├── Http                                  ← HTTP client patterns
│   ├── WoW.Two.Sdk.Http.Abstractions
│   ├── WoW.Two.Sdk.Http.Resilience       ← Polly integration
│   └── WoW.Two.Sdk.Http.TypedClients
│
├── Data                                  ← data access
│   ├── WoW.Two.Sdk.Data.Abstractions     ← IRepository, IUnitOfWork
│   ├── WoW.Two.Sdk.Data.EfCore           ← EF Core implementations
│   └── WoW.Two.Sdk.Data.Auditing         ← created_at/updated_at patterns
│
├── Messaging                             ← in-process + distributed
│   ├── WoW.Two.Sdk.Messaging.Abstractions
│   ├── WoW.Two.Sdk.Messaging.MediatR
│   └── WoW.Two.Sdk.Messaging.MassTransit
│
├── Validation                            ← input validation
│   ├── WoW.Two.Sdk.Validation.Abstractions
│   └── WoW.Two.Sdk.Validation.FluentValidation
│
├── Storage                               ← caching + files
│   ├── WoW.Two.Sdk.Storage.Cache.Abstractions
│   ├── WoW.Two.Sdk.Storage.Cache.InMemory
│   └── WoW.Two.Sdk.Storage.File
│
├── Hosting                               ← app bootstrapping
│   ├── WoW.Two.Sdk.Hosting.Core          ← DI, config, error handling
│   └── WoW.Two.Sdk.Hosting.WebApi        ← ASP.NET Core setup
│
└── AI                                    ← AI capabilities
    ├── WoW.Two.Sdk.AI.Abstractions
    ├── WoW.Two.Sdk.AI.SemanticKernel
    └── WoW.Two.Sdk.AI.ChatCompletion
```

### 2.2 Design Principles

1. **Abstractions-first**: Every domain has an `Abstractions` package with zero framework dependencies. Implementations are separate packages.

2. **DI extension pattern**: Each implementation ships a `.DependencyInjection` extension method (e.g., `services.AddWoWJsonSerialization()`). This is a separate package or included in the impl package.

3. **Granular packages**: Small, focused packages over monolithic ones. A user wanting only enum extensions shouldn't pull in EF Core.

4. **Consistent layering**:
   ```
   Abstractions (interfaces, contracts) → 0 deps
   Implementation (concrete classes)    → depends on Abstractions + framework
   DependencyInjection (registration)   → depends on Implementation + MS.DI
   ```

5. **Version alignment**: All packages target the same .NET version (recommend .NET 9, with .NET 8 LTS multi-target for sdk packages).

### 2.3 Build Infrastructure (Priority 0)

Before any new library, establish the foundation:

```
wow-two-sdk/                        ← new monorepo or shared config repo
├── Directory.Build.props           ← shared MSBuild properties
├── Directory.Packages.props        ← centralized package versions (CPM)
├── global.json                     ← .NET SDK version pin
├── .editorconfig                   ← code style rules
├── nuget.config                    ← package source config
├── version.json                    ← Nerdbank.GitVersioning
└── eng/
    ├── ci-build.yml                ← GitHub Actions build template
    ├── ci-publish.yml              ← NuGet publish template
    └── test.yml                    ← test + coverage template
```

**Key `Directory.Build.props` settings:**
```xml
<PropertyGroup>
  <TargetFrameworks>net9.0;net8.0</TargetFrameworks>
  <ImplicitUsings>enable</ImplicitUsings>
  <Nullable>enable</Nullable>
  <TreatWarningsAsErrors>true</TreatWarningsAsErrors>
  <GenerateDocumentationFile>true</GenerateDocumentationFile>
  <Authors>WoW 2.0 Team</Authors>
  <PackageLicenseExpression>MIT</PackageLicenseExpression>
  <RepositoryType>git</RepositoryType>
</PropertyGroup>
```

### 2.4 First Libraries to Build (Priority Order)

| # | Package | Why First | Effort |
|---|---------|-----------|--------|
| 1 | `Language.Core.Enums` | Already written, just needs merge + rename + publish | S |
| 2 | `Language.Core.Time` | Already written, same situation | S |
| 3 | `Language.Serialization.Abstractions` | Already on dev branch, pilot for standardization | S |
| 4 | `Language.Serialization.SystemTextJson` | Most common serializer, pairs with abstractions | M |
| 5 | `Language.Linq` | Empty but high value — every project uses LINQ extensions | M |
| 6 | `Data.Abstractions` | IRepository/IUnitOfWork — Haven already has this pattern | M |
| 7 | `Hosting.Core` | DI + config + exception handling — bootstrap any app | L |
| 8 | `Http.Resilience` | Extract from resilience-patterns examples into library | L |

### 2.5 Monorepo vs Multi-Repo Decision

**Recommendation: Hybrid approach**

- **Monorepo per domain** (e.g., one repo for `Language.*`, one for `Data.*`, one for `Messaging.*`)
- **Each domain repo** contains multiple projects/packages with shared `Directory.Build.props`
- **Cross-domain** dependencies managed via NuGet package references (not project references)

This balances:
- ✅ Atomic commits within a domain (Language.Core + Language.Serialization evolve together)
- ✅ Independent versioning across domains
- ✅ Manageable CI/CD (one pipeline per domain repo)
- ✅ Avoids the "100 repos with 1 file each" problem

**Example:**
```
wow-two-sdk.language/                ← single git repo
├── src/
│   ├── WoW.Two.Sdk.Language.Core.Enums/
│   ├── WoW.Two.Sdk.Language.Core.Time/
│   ├── WoW.Two.Sdk.Language.Core.Types/
│   ├── WoW.Two.Sdk.Language.Linq/
│   ├── WoW.Two.Sdk.Language.Serialization.Abstractions/
│   ├── WoW.Two.Sdk.Language.Serialization.SystemTextJson/
│   └── WoW.Two.Sdk.Language.Serialization.Newtonsoft/
├── tests/
│   ├── WoW.Two.Sdk.Language.Core.Tests/
│   ├── WoW.Two.Sdk.Language.Linq.Tests/
│   └── WoW.Two.Sdk.Language.Serialization.Tests/
├── Directory.Build.props
├── Directory.Packages.props
├── WoW.Two.Sdk.Language.sln
├── CLAUDE.md
├── README.md
└── CHANGELOG.md
```

---

## 3. React Frontend — Modular Library Strategy

### 3.1 Current Frontend Reality

Haven's frontend demonstrates a **working pnpm workspace monorepo** with 3 shared packages. This is the pattern to generalize.

**What Haven already solved:**
- pnpm workspace with `workspace:*` linking
- Shared Vite config factory (`vite.base.ts`)
- Shared TypeScript configs (`tsconfig.base.app.json`, `tsconfig.base.node.json`)
- Shared ESLint flat config (`eslint.config.base.js`)
- Subpath exports for tree-shaking
- Presentational component library with Radix UI + Tailwind + CVA
- Domain type mirroring (TS enums ↔ C# enums)
- Context-based state management (no Redux)

### 3.2 Proposed Package Hierarchy

```
@wow-two/                                 ← npm scope
├── core                                  ← language-level utilities
│   ├── @wow-two/core                     ← type guards, result types, date utils
│   └── @wow-two/core/validators          ← runtime validation helpers
│
├── react                                 ← React-specific
│   ├── @wow-two/react-hooks              ← reusable hooks (useAsync, useDebounce, useLocalStorage)
│   ├── @wow-two/react-auth               ← auth provider, guards, token mgmt
│   ├── @wow-two/react-query              ← API client patterns (TanStack Query wrappers)
│   ├── @wow-two/react-forms              ← form state + validation (react-hook-form wrappers)
│   └── @wow-two/react-i18n               ← i18n setup patterns
│
├── ui                                    ← component library
│   ├── @wow-two/ui-primitives            ← headless Radix UI wrappers + Tailwind + CVA
│   ├── @wow-two/ui-layout                ← AppShell, Sidebar, PageHeader, etc.
│   ├── @wow-two/ui-data                  ← DataTable, Filters, Pagination
│   └── @wow-two/ui-theme                 ← theme provider, dark mode, design tokens
│
├── tooling                               ← DX/build tools
│   ├── @wow-two/vite-config              ← shared Vite config factory
│   ├── @wow-two/tsconfig                 ← shared TypeScript configs
│   ├── @wow-two/eslint-config            ← shared ESLint flat config
│   └── @wow-two/tailwind-preset          ← shared Tailwind theme/preset
│
└── domain                                ← domain utilities
    ├── @wow-two/api-client               ← typed HTTP client generator
    └── @wow-two/domain-types             ← shared type patterns (Result<T>, PagedList<T>)
```

### 3.3 Design Principles

1. **Extract from Haven first**: Don't build from scratch — generalize what's already working in Haven.

2. **Subpath exports everywhere**: Every package uses `package.json` exports map for tree-shaking:
   ```json
   {
     "exports": {
       ".": "./src/index.ts",
       "./hooks": "./src/hooks/index.ts",
       "./utils": "./src/utils/index.ts"
     }
   }
   ```

3. **Framework-agnostic core**: `@wow-two/core` has zero React dependencies. React-specific packages are separate.

4. **Headless-first UI**: Components provide behavior + accessibility (via Radix UI), styling is opt-in via Tailwind/CVA.

5. **TypeScript-strict**: All packages use strict mode, no `any`, exported types for everything.

6. **Peer dependencies for React**: All `@wow-two/react-*` packages list React 18/19 as peer deps.

### 3.4 Build Infrastructure

```
wow-two-sdk.react/                   ← single git repo (monorepo)
├── packages/
│   ├── core/                        ← @wow-two/core
│   ├── react-hooks/                 ← @wow-two/react-hooks
│   ├── ui-primitives/               ← @wow-two/ui-primitives
│   ├── ui-layout/                   ← @wow-two/ui-layout
│   ├── vite-config/                 ← @wow-two/vite-config
│   ├── tsconfig/                    ← @wow-two/tsconfig
│   └── eslint-config/               ← @wow-two/eslint-config
├── apps/
│   └── docs/                        ← Storybook or docs site
├── pnpm-workspace.yaml
├── package.json                     ← workspace root
├── tsconfig.base.json
├── turbo.json                       ← Turborepo for build orchestration
├── CLAUDE.md
└── README.md
```

**Tooling choices:**
- **pnpm** — workspace management (proven in Haven)
- **Turborepo** — build orchestration, caching, parallel builds
- **Changesets** — versioning + changelog generation for npm packages
- **Vite** — bundling (library mode for packages)
- **Vitest** — testing (Vite-native, fast)
- **Storybook** — component documentation

### 3.5 First Packages to Build (Priority Order)

| # | Package | Source | Effort |
|---|---------|--------|--------|
| 1 | `@wow-two/vite-config` | Extract from Haven's `vite.base.ts` | S |
| 2 | `@wow-two/tsconfig` | Extract from Haven's `tsconfig.base.*.json` | S |
| 3 | `@wow-two/eslint-config` | Extract from Haven's `eslint.config.base.js` | S |
| 4 | `@wow-two/core` | New — type guards, Result<T>, date utils | M |
| 5 | `@wow-two/react-hooks` | Extract from Haven's `@haven/common/hooks` | M |
| 6 | `@wow-two/ui-primitives` | Extract from Haven's `@haven/ui` + generalize | L |
| 7 | `@wow-two/ui-layout` | Extract AppShell, Sidebar patterns from Haven | M |
| 8 | `@wow-two/react-auth` | Extract from Haven's `@haven/common/identity` | L |

### 3.6 Haven Migration Path

Once SDK packages exist, Haven migrates from local packages to published ones:

```
Before:  @haven/common  → packages/common/src  (local workspace link)
After:   @haven/common  → depends on @wow-two/react-hooks, @wow-two/core
         @haven/ui      → depends on @wow-two/ui-primitives, @wow-two/ui-layout
```

Haven-specific logic (Telegram auth, Supabase client) stays in `@haven/*`. Generic patterns move to `@wow-two/*`.

---

## 4. Cross-Stack Alignment

### 4.1 Backend ↔ Frontend Mirroring

Haven already mirrors C# enums to TypeScript. Generalize this:

| .NET Package | React Package | Shared Concept |
|---|---|---|
| `Sdk.Language.Core.Enums` | `@wow-two/core` | Enum utility patterns |
| `Sdk.Language.Serialization` | `@wow-two/api-client` | JSON contracts, naming policies |
| `Sdk.Data.Abstractions` | `@wow-two/domain-types` | PagedList<T>, Result<T>, SortField |
| `Sdk.Validation` | `@wow-two/core/validators` | Validation rules (shared logic) |
| `Sdk.Hosting.WebApi` | `@wow-two/api-client` | API endpoint contracts |

### 4.2 Shared Conventions

- **Naming**: `WoW.Two.Sdk.*` (.NET) ↔ `@wow-two/*` (npm)
- **Versioning**: SemVer on both sides, pre-release via `-alpha.N` / `-beta.N`
- **Testing**: xUnit (.NET) ↔ Vitest (React), both with coverage gates
- **CI/CD**: GitHub Actions for both, reusable workflow templates
- **Docs**: XML docs (.NET) → DocFX site | TSDoc (React) → Storybook/TypeDoc

---

## 5. Implementation Roadmap

### Phase 0 — Build Infrastructure (Week 1-2)

- [ ] Create `wow-two-sdk.language` monorepo with `Directory.Build.props`, `Directory.Packages.props`, `global.json`
- [ ] Create `wow-two-sdk.react` monorepo with pnpm workspace, Turborepo, Changesets
- [ ] Set up GitHub Actions CI for both repos (build + test + lint)
- [ ] Standardize naming: `WoW.Two.Sdk.*` (NuGet), `@wow-two/*` (npm)
- [ ] Create NuGet + npm org/scope ownership

### Phase 1 — First .NET Libraries (Week 2-4)

- [ ] Merge `language.core` feature branch → consolidate into `wow-two-sdk.language` monorepo
- [ ] Merge `language.serialization` dev branch → same monorepo
- [ ] Publish first alpha packages: `WoW.Two.Sdk.Language.Core.Enums`, `.Time`, `.Serialization.Abstractions`
- [ ] Write tests (target 80%+ coverage)
- [ ] Create README + usage examples for each package

### Phase 2 — First React Libraries (Week 3-5)

- [ ] Extract Haven tooling configs → `@wow-two/vite-config`, `@wow-two/tsconfig`, `@wow-two/eslint-config`
- [ ] Build `@wow-two/core` (type guards, Result<T>, utility functions)
- [ ] Extract Haven hooks → `@wow-two/react-hooks`
- [ ] Publish to npm (private or public based on readiness)

### Phase 3 — Integration (Week 5-7)

- [ ] Haven backend adopts `WoW.Two.Sdk.Language.*` packages
- [ ] Haven frontend adopts `@wow-two/*` packages (replace local @haven equivalents)
- [ ] Validate: does the SDK work for a real product?
- [ ] Iterate based on friction points

### Phase 4 — Expand (Week 7+)

- [ ] `Sdk.Data.Abstractions` + `Sdk.Data.EfCore`
- [ ] `Sdk.Messaging.Abstractions` + MediatR/MassTransit impls
- [ ] `@wow-two/ui-primitives` + `@wow-two/ui-layout`
- [ ] `@wow-two/react-auth` (generalize from Haven's Telegram auth)

---

## 6. Key Decisions Needed

| Decision | Options | Recommendation |
|---|---|---|
| **Repo strategy** | Multi-repo (current) vs domain monorepos | Domain monorepos (see §2.5) |
| **.NET version** | .NET 8 LTS only / .NET 9 only / multi-target | Multi-target `net9.0;net8.0` for SDK |
| **NuGet naming** | `WoW2.Backbone.*` (current) vs `WoW.Two.Sdk.*` (proposed) | `WoW.Two.Sdk.*` — clean break |
| **npm scope** | `@wow-two` vs `@wow2` vs unscoped | `@wow-two` — matches org name |
| **React state** | Context (Haven) vs Zustand vs Jotai | Context for SDK, app decides beyond that |
| **Component styling** | Tailwind-only vs CSS-in-JS vs both | Tailwind + CVA (proven in Haven) |
| **Build orchestrator** | Turborepo vs Nx vs Lerna | Turborepo (lighter, sufficient) |
| **Versioning tool** | Changesets vs semantic-release vs manual | Changesets (explicit, PR-based) |
| **Platform ↔ SDK split** | Keep separate or merge | Keep separate — platform is internal, SDK is public |

---

## 7. Risk Assessment

| Risk | Impact | Mitigation |
|---|---|---|
| Naming migration breaks existing consumers | High | Publish under new names, keep old as deprecated aliases for 1 release |
| Over-abstraction (too many tiny packages) | Medium | Start with domain monorepos; split only when justified by real consumer needs |
| Haven diverges from SDK | Medium | Haven is the first consumer — if SDK doesn't work for Haven, it doesn't work |
| No contributors beyond Max | Low (for now) | Focus on personal productivity first, community second |
| .NET 9 → 10 migration overhead | Low | Multi-target from day 1, upgrade LTS target annually |

---

*Last updated: 2026-03-24*

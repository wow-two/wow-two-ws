# WoW 2.0 SDK — Modular Library System Spec

> **Status**: Spec  
> **Created**: 2026-04-20  
> **Goal**: Build the backbone and first libraries for wow-two-sdk — a modular, reusable library system for .NET backend and React frontend.

---

## 1. Problem Statement

The WoW 2.0 ecosystem has ~40 repos across 5 GitHub orgs, but most are stubs or have code stuck on unmerged feature branches. There's no shared build infrastructure, no consistent naming, no CI/CD for SDK packages, and no frontend SDK at all. Meanwhile, Haven (10x-ven-haven) has organically built proven patterns for both .NET and React that should be extracted and generalized.

### What's broken today

- **Naming chaos**: `Backbone.*`, `WoW2.Backbone.*`, `WoW2.Sdk.*` — three naming generations coexist
- **Version fragmentation**: some packages target .NET 8, others .NET 9; versions range from `8.0.0-alpha.0` to `9.0.0-alpha.1`
- **No build infra**: no `Directory.Build.props`, no centralized package management, no CI/CD wired to SDK repos
- **Code on branches**: language.core and language.serialization have real, tested code — but only on unmerged feature/dev branches
- **100+ repo sprawl risk**: current 1-repo-per-package approach will become unmanageable
- **No frontend story**: React ecosystem mentioned in vision but zero packages exist
- **Haven is isolated**: Haven's proven patterns (pnpm workspace, shared configs, component library) aren't reusable by other projects

---

## 2. Current State — What Exists

### 2.1 SDK Repos (7)

| Repo | Real Code? | Branch | .NET | Maturity |
|------|-----------|--------|------|----------|
| `language.core` | ✅ Enums, Time providers, Type abstractions | `feature/#5_core-types-enum-description` | 9.0 | Early production — benchmarked, tested |
| `language.serialization` | ✅ JSON abstractions + STJ + Newtonsoft | `dev` | 9.0 | Feature-complete, has TASKS.md roadmap |
| `language.linq` | ❌ Empty stub | `main` | — | Planned only |
| `resilience-patterns` | ✅ Polly v8 examples (6 pattern areas) | `main` | 9.0 | Complete — but examples, not a library |
| `package-analyzer` | ✅ Clean Arch backend service | `dev` | 8.0 | In-progress service, consumes ~10 platform packages |
| `ai.semantic-kernel` | ⚠️ Minimal settings abstractions | `merged feature/#1` | 8.0 | Early abstractions |
| `ai.nlp` | ⚠️ Chat completion interfaces | `merged feature/#2` | 8.0 | Early abstractions |

### 2.2 Platform Repos (16)

Mostly stubs with architecture defined. Key ones that have some code: `core.di`, `core.app`, `core.exceptions`, `core.validations`, `comms.infra`, `data.relational`. All target .NET 8.

### 2.3 Haven Patterns Worth Extracting

**Backend (.NET 9, 12 projects):**

| Pattern | Where in Haven | Generalization Value |
|---------|---------------|---------------------|
| Config factory (env-based) | `Haven.Common` | High — every app needs this |
| DB context factory | `Haven.Common.Persistence` | High — EF Core bootstrapping |
| Pipeline executor (batch processing) | `Haven.Channels.Common` | Medium — specific to data pipelines |
| Phone normalization | `Haven.Common` | Low — Uzbekistan-specific |
| Supabase client wrapper | `Haven.Channels.Common` | Low — Supabase-specific |
| LLM batch client (Claude) | `Haven.Channels.Common` | Medium — reusable AI patterns |
| CORS setup helpers | `Haven.Common` | High — every API needs this |
| Audit columns (created_at/updated_at) | All 11 DB tables | High — universal pattern |

**Frontend (React 19, pnpm workspace, 5 apps + 3 packages):**

| Pattern | Where in Haven | Generalization Value |
|---------|---------------|---------------------|
| Vite config factory | `vite.base.ts` | High — every app needs this |
| TypeScript base configs | `tsconfig.base.app.json`, `tsconfig.base.node.json` | High |
| ESLint flat config base | `eslint.config.base.js` | High |
| Context-based service locator | `@haven/common/context` | High |
| Auth provider + guards | `@haven/common/identity` | High (needs generalization) |
| Theme hook (light/dark) | `@haven/common/hooks` | High |
| Hash router hook | `@haven/common/hooks` | Medium |
| UI state persistence | `@haven/common/hooks` | Medium |
| Presentational components (AppShell, Sidebar) | `@haven/ui` | High |
| `cn()` utility (clsx + tailwind-merge) | `@haven/common/lib` | High |
| Domain type mirroring (TS ↔ C#) | `@haven/domain` | High — pattern, not code |
| Subpath exports pattern | All packages | High — convention to replicate |

**Haven's tech choices (validated in production):**
- React 19 + Vite 7 + pnpm workspaces
- Tailwind CSS v4 + Radix UI + CVA (class-variance-authority)
- TypeScript 5.9 strict mode
- ESLint 9 flat config
- lucide-react for icons
- No Redux/Zustand — React Context is sufficient for app state

---

## 3. Proposed Architecture

### 3.1 .NET Backend — Package Hierarchy

```
WoW.Two.Sdk                              ← NuGet package prefix
│
├── Language                              ← zero-framework-dependency extensions
│   ├── WoW.Two.Sdk.Language.Core.Enums           ← [Description] helpers, TryGetDescription
│   ├── WoW.Two.Sdk.Language.Core.Time             ← ITimeProvider, BasicTimeProvider, DI
│   ├── WoW.Two.Sdk.Language.Core.Types            ← type abstractions
│   ├── WoW.Two.Sdk.Language.Linq                  ← LINQ extensions
│   ├── WoW.Two.Sdk.Language.Serialization.Abstractions  ← IJsonSerializer, IAsyncJsonSerializer
│   ├── WoW.Two.Sdk.Language.Serialization.SystemTextJson
│   └── WoW.Two.Sdk.Language.Serialization.Newtonsoft
│
├── Http                                  ← HTTP client patterns
│   ├── WoW.Two.Sdk.Http.Abstractions
│   ├── WoW.Two.Sdk.Http.Resilience       ← Polly integration
│   └── WoW.Two.Sdk.Http.TypedClients
│
├── Data                                  ← data access
│   ├── WoW.Two.Sdk.Data.Abstractions     ← IRepository<T>, IUnitOfWork
│   ├── WoW.Two.Sdk.Data.EfCore           ← EF Core implementations
│   └── WoW.Two.Sdk.Data.Auditing         ← created_at/updated_at/created_by patterns
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
│   ├── WoW.Two.Sdk.Hosting.Core          ← DI, config, exception handling, CORS
│   └── WoW.Two.Sdk.Hosting.WebApi        ← ASP.NET Core setup, Swagger, middleware
│
└── AI                                    ← AI capabilities
    ├── WoW.Two.Sdk.AI.Abstractions
    ├── WoW.Two.Sdk.AI.SemanticKernel
    └── WoW.Two.Sdk.AI.ChatCompletion
```

### 3.2 React Frontend — Package Hierarchy

```
@wow-two/                                 ← npm scope
│
├── Tooling (DX)
│   ├── @wow-two/vite-config              ← createViteConfig(port, appDir) factory
│   ├── @wow-two/tsconfig                 ← base app + node TypeScript configs
│   ├── @wow-two/eslint-config            ← ESLint 9 flat config base
│   └── @wow-two/tailwind-preset          ← shared Tailwind theme/design tokens
│
├── Core (framework-agnostic)
│   ├── @wow-two/core                     ← type guards, Result<T>, PagedList<T>, cn(), date utils
│   └── @wow-two/core/validators          ← runtime validation helpers
│
├── React
│   ├── @wow-two/react-hooks              ← useAsync, useDebounce, useTheme, useLocalStorage
│   ├── @wow-two/react-auth               ← AuthProvider, AuthGate, useAuth, token management
│   ├── @wow-two/react-query              ← TanStack Query wrappers, API client patterns
│   ├── @wow-two/react-forms              ← react-hook-form wrappers
│   └── @wow-two/react-i18n               ← i18next setup patterns
│
├── UI (component library)
│   ├── @wow-two/ui-primitives            ← Radix UI + Tailwind + CVA (Button, Input, Dialog, etc.)
│   ├── @wow-two/ui-layout                ← AppShell, Sidebar, SidebarNavItem, PageHeader
│   ├── @wow-two/ui-data                  ← DataTable, Filters, Pagination (TanStack Table)
│   └── @wow-two/ui-theme                 ← ThemeProvider, dark mode toggle, design tokens
│
└── Domain
    ├── @wow-two/api-client               ← typed HTTP client, error handling, interceptors
    └── @wow-two/domain-types             ← Result<T>, PagedList<T>, SortField, enum patterns
```

---

## 4. Design Principles

### 4.1 .NET

1. **Abstractions-first**: Every domain has a zero-dep `Abstractions` package. Implementations are separate.
2. **DI extension pattern**: Each impl ships `services.AddWoW{Feature}()` extension methods.
3. **Layering**:
   ```
   Abstractions (interfaces)  → 0 dependencies
   Implementation (classes)   → Abstractions + framework lib
   DependencyInjection (ext)  → Implementation + MS.Extensions.DI
   ```
4. **Multi-target**: All SDK packages target `net9.0;net8.0`.
5. **Granular**: A user wanting only enum extensions shouldn't pull in EF Core.

### 4.2 React

1. **Extract from Haven**: Don't build from scratch — generalize proven patterns.
2. **Subpath exports everywhere**: Tree-shakeable, fine-grained imports.
3. **Framework-agnostic core**: `@wow-two/core` has zero React deps.
4. **Headless-first UI**: Behavior + accessibility via Radix UI; styling via Tailwind/CVA.
5. **Peer deps for React**: All `@wow-two/react-*` list React 18/19 as peer deps.

### 4.3 Cross-Stack

1. **Haven = first consumer**: If the SDK doesn't work for Haven, it doesn't work.
2. **Domain mirroring**: C# enums ↔ TypeScript enums (pattern already proven in Haven).
3. **Consistent naming**: `WoW.Two.Sdk.*` (NuGet) ↔ `@wow-two/*` (npm).
4. **SemVer**: Both stacks follow strict semantic versioning.

---

## 5. Repo Strategy — Domain Monorepos

**Decision: Hybrid monorepo per domain** (not 1 repo per package, not 1 giant monorepo).

### .NET repos

| Repo | Contains | Packages |
|------|----------|----------|
| `wow-two-sdk.language` | Language-level extensions | Core.Enums, Core.Time, Core.Types, Linq, Serialization.* |
| `wow-two-sdk.data` | Data access patterns | Data.Abstractions, Data.EfCore, Data.Auditing |
| `wow-two-sdk.messaging` | Messaging abstractions | Messaging.Abstractions, .MediatR, .MassTransit |
| `wow-two-sdk.hosting` | App bootstrapping | Hosting.Core, Hosting.WebApi |
| `wow-two-sdk.http` | HTTP client patterns | Http.Abstractions, .Resilience, .TypedClients |
| `wow-two-sdk.storage` | Caching + files | Storage.Cache.*, Storage.File |
| `wow-two-sdk.validation` | Input validation | Validation.Abstractions, .FluentValidation |
| `wow-two-sdk.ai` | AI capabilities | AI.Abstractions, .SemanticKernel, .ChatCompletion |

**Each domain repo structure:**
```
wow-two-sdk.language/
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
│   └── WoW.Two.Sdk.Language.Serialization.Tests/
├── Directory.Build.props
├── Directory.Packages.props
├── global.json
├── .editorconfig
├── nuget.config
├── WoW.Two.Sdk.Language.sln
├── CLAUDE.md
├── README.md
└── CHANGELOG.md
```

### React repo (single monorepo)

```
wow-two-sdk.react/
├── packages/
│   ├── core/                    ← @wow-two/core
│   ├── react-hooks/             ← @wow-two/react-hooks
│   ├── react-auth/              ← @wow-two/react-auth
│   ├── ui-primitives/           ← @wow-two/ui-primitives
│   ├── ui-layout/               ← @wow-two/ui-layout
│   ├── ui-data/                 ← @wow-two/ui-data
│   ├── ui-theme/                ← @wow-two/ui-theme
│   ├── vite-config/             ← @wow-two/vite-config
│   ├── tsconfig/                ← @wow-two/tsconfig
│   ├── eslint-config/           ← @wow-two/eslint-config
│   └── tailwind-preset/         ← @wow-two/tailwind-preset
├── apps/
│   └── docs/                    ← Storybook / docs site
├── pnpm-workspace.yaml
├── turbo.json
├── package.json
├── CLAUDE.md
└── README.md
```

### Why domain monorepos?

- ✅ Atomic commits within a domain (Enums + Serialization evolve together)
- ✅ Shared `Directory.Build.props` / `Directory.Packages.props` per domain
- ✅ One CI pipeline per domain repo
- ✅ Independent versioning across domains
- ✅ Avoids "100 repos with 1 file each" sprawl
- ✅ Cross-domain deps managed via published NuGet refs (not project refs)

---

## 6. Build Infrastructure

### 6.1 .NET — Shared Build Config

**`Directory.Build.props`** (per domain repo):
```xml
<Project>
  <PropertyGroup>
    <TargetFrameworks>net9.0;net8.0</TargetFrameworks>
    <ImplicitUsings>enable</ImplicitUsings>
    <Nullable>enable</Nullable>
    <LangVersion>latest</LangVersion>
    <TreatWarningsAsErrors>true</TreatWarningsAsErrors>
    <GenerateDocumentationFile>true</GenerateDocumentationFile>
    <EnablePackageValidation>true</EnablePackageValidation>

    <!-- Package metadata -->
    <Authors>WoW 2.0 Team</Authors>
    <Company>WoW 2.0</Company>
    <PackageLicenseExpression>MIT</PackageLicenseExpression>
    <PackageProjectUrl>https://github.com/wow-two-sdk</PackageProjectUrl>
    <RepositoryType>git</RepositoryType>

    <!-- Source Link -->
    <PublishRepositoryUrl>true</PublishRepositoryUrl>
    <EmbedUntrackedSources>true</EmbedUntrackedSources>
    <IncludeSymbols>true</IncludeSymbols>
    <SymbolPackageFormat>snupkg</SymbolPackageFormat>
  </PropertyGroup>
</Project>
```

**`Directory.Packages.props`** (centralized package management):
```xml
<Project>
  <PropertyGroup>
    <ManagePackageVersionsCentrally>true</ManagePackageVersionsCentrally>
  </PropertyGroup>
  <ItemGroup>
    <!-- Framework -->
    <PackageVersion Include="Microsoft.Extensions.DependencyInjection.Abstractions" Version="9.0.0" />
    <PackageVersion Include="Microsoft.Extensions.Options" Version="9.0.0" />
    <!-- Serialization -->
    <PackageVersion Include="Newtonsoft.Json" Version="13.0.3" />
    <!-- Testing -->
    <PackageVersion Include="xunit" Version="2.9.3" />
    <PackageVersion Include="FluentAssertions" Version="7.0.0" />
    <PackageVersion Include="Moq" Version="4.20.72" />
    <!-- Source Link -->
    <PackageVersion Include="Microsoft.SourceLink.GitHub" Version="8.0.0" />
  </ItemGroup>
</Project>
```

**`global.json`**:
```json
{
  "sdk": {
    "version": "9.0.200",
    "rollForward": "latestFeature"
  }
}
```

### 6.2 React — Tooling Config

**`turbo.json`**:
```json
{
  "$schema": "https://turbo.build/schema.json",
  "tasks": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": ["dist/**"]
    },
    "lint": {},
    "test": {
      "dependsOn": ["^build"]
    },
    "typecheck": {
      "dependsOn": ["^build"]
    }
  }
}
```

**Versioning**: Changesets for explicit, PR-based version bumps + changelog generation.

**Testing**: Vitest (Vite-native, fast, compatible with React Testing Library).

### 6.3 CI/CD — GitHub Actions

**Reusable workflows** (stored in `wow-two-platform.pipelines`):

| Workflow | Trigger | Steps |
|----------|---------|-------|
| `dotnet-ci.yml` | Push/PR to SDK repos | Restore → Build → Test → Coverage → Pack |
| `dotnet-publish.yml` | Tag push (`v*`) | Build → Test → Pack → Push to NuGet.org |
| `dotnet-prerelease.yml` | Push to `dev` branch | Build → Test → Pack → Push to GitHub Packages |
| `react-ci.yml` | Push/PR to react repo | Install → Typecheck → Lint → Test → Build |
| `react-publish.yml` | Changeset merge to main | Build → Changesets version → Publish to npm |

---

## 7. Migration Plan — Existing Code

### 7.1 language.core (feature branch → monorepo)

**Source**: `wow-two-sdk.language.core` branch `feature/#5_core-types-enum-description`

**What exists (33 C# files):**
- `Backbone.Language.Core.Extensions.Enums` — `GetDescription()`, `TryGetDescription()`, `GetDescriptionOrValue()`
- `Backbone.Language.Core.Time.Extensions` — `DayCalculationExtensions`, `DateTimeOffsetExtensions`
- `Backbone.Language.Core.Time.Provider.Abstractions` — `ITimeProvider`
- `Backbone.Language.Core.Time.Provider.Basic` — `BasicTimeProvider`
- `Backbone.Language.Core.Time.Provider.Basic.DependencyInjection` — `AddBasicTimeProvider()`
- UnitTests project, Benchmarks project

**Migration steps:**
1. Create `wow-two-sdk.language` repo
2. Copy code from feature branch
3. Rename namespaces: `Backbone.*` → `WoW.Two.Sdk.Language.*`
4. Rename NuGet package IDs: `WoW2.Backbone.*` → `WoW.Two.Sdk.Language.*`
5. Update .NET target: `net9.0;net8.0` (multi-target)
6. Add `Directory.Build.props`, `Directory.Packages.props`
7. Verify tests pass
8. Publish alpha to GitHub Packages

### 7.2 language.serialization (dev branch → monorepo)

**Source**: `wow-two-sdk.language.serialization` branch `dev`

**What exists (21 C# files):**
- `WoW2.Sdk.Language.Serialization.Json.Abstractions` — `IJsonSerializer`, `IAsyncJsonSerializer`
- `WoW2.Sdk.Language.Serialization.Json.System` — System.Text.Json implementation
- `WoW2.Sdk.Language.Serialization.Json.Newtonsoft` — Newtonsoft.Json implementation
- DI extension packages for both
- Custom converters (enum description, interface-to-concrete)

**Known issues (from TASKS.md):**
- Version mismatch: System.DI at `8.0.0-alpha.1`, others at `9.0.0-alpha.*`
- Namespace ≠ PackageId inconsistency
- Missing: tests, Source Link, README, CI/CD
- Newtonsoft lacks `IAsyncJsonSerializer` implementation

**Migration steps:**
1. Move into `wow-two-sdk.language` repo alongside Core packages
2. Rename to `WoW.Two.Sdk.Language.Serialization.*`
3. Fix version alignment
4. Add async support to Newtonsoft impl
5. Add tests
6. Update converter dependency: `Core.Enums` (now local project ref, not NuGet)

### 7.3 Haven frontend → @wow-two packages

**Phase 1 — Extract tooling (zero breaking changes to Haven):**
1. Copy `vite.base.ts` → `@wow-two/vite-config`
2. Copy `tsconfig.base.*.json` → `@wow-two/tsconfig`
3. Copy `eslint.config.base.js` → `@wow-two/eslint-config`
4. Haven then imports from `@wow-two/*` instead of local files

**Phase 2 — Extract core utilities:**
1. Extract `cn()` → `@wow-two/core`
2. Extract `useTheme`, `useUIState` → `@wow-two/react-hooks`
3. Haven's `@haven/common` now depends on `@wow-two/react-hooks` + `@wow-two/core`

**Phase 3 — Extract UI components:**
1. Generalize AppShell, Sidebar → `@wow-two/ui-layout`
2. Haven's `@haven/ui` depends on `@wow-two/ui-layout`
3. Haven-specific components stay in `@haven/ui`

**Phase 4 — Extract auth (requires generalization):**
1. Abstract Telegram-specific auth out of `@haven/common/identity`
2. Create `@wow-two/react-auth` with pluggable auth strategies
3. Haven creates `@haven/auth-telegram` that implements the strategy

---

## 8. Priority & Sequencing

### Phase 0 — Build Infrastructure (Week 1-2)

| Task | Effort |
|------|--------|
| Create `wow-two-sdk.language` repo with build infra (Directory.Build.props, CPM, global.json, editorconfig, nuget.config) | M |
| Create `wow-two-sdk.react` repo with pnpm workspace, Turborepo, Changesets | M |
| Set up GitHub Actions CI for both repos (build + test + lint) | M |
| Register NuGet `WoW.Two.Sdk` prefix + npm `@wow-two` scope | S |

### Phase 1 — First .NET Libraries (Week 2-4)

| Task | Effort | Source |
|------|--------|--------|
| Migrate `language.core` → `wow-two-sdk.language` | M | Existing feature branch |
| Migrate `language.serialization` → same repo | M | Existing dev branch |
| Implement `Language.Linq` | M | New code |
| Write tests (target 80%+ coverage) | M | New |
| Publish first alpha packages to GitHub Packages | S | — |
| README + usage examples for each package | S | — |

### Phase 2 — First React Libraries (Week 3-5)

| Task | Effort | Source |
|------|--------|--------|
| `@wow-two/vite-config` | S | Extract from Haven |
| `@wow-two/tsconfig` | S | Extract from Haven |
| `@wow-two/eslint-config` | S | Extract from Haven |
| `@wow-two/core` (type guards, Result<T>, cn()) | M | New + Haven extract |
| `@wow-two/react-hooks` | M | Extract from Haven |
| Publish to npm (private or public) | S | — |

### Phase 3 — Integration & Validation (Week 5-7)

| Task | Effort |
|------|--------|
| Haven backend adopts `WoW.Two.Sdk.Language.*` packages | M |
| Haven frontend adopts `@wow-two/*` tooling packages | M |
| Validate: friction points, missing APIs, ergonomics | — |
| Iterate based on real usage | — |

### Phase 4 — Expand (Week 7+)

| Task | Effort |
|------|--------|
| `wow-two-sdk.data` — Abstractions + EF Core + Auditing | L |
| `wow-two-sdk.messaging` — Abstractions + MediatR + MassTransit | L |
| `wow-two-sdk.hosting` — Core + WebApi bootstrapping | L |
| `@wow-two/ui-primitives` — Radix UI + Tailwind + CVA | L |
| `@wow-two/ui-layout` — AppShell, Sidebar from Haven | M |
| `@wow-two/react-auth` — generalized auth provider | L |

---

## 9. Decisions Needed

| # | Decision | Options | Recommendation | Notes |
|---|----------|---------|----------------|-------|
| D1 | Repo strategy | Multi-repo (current) / domain monorepos / single monorepo | **Domain monorepos** | Balance between cohesion and independence |
| D2 | .NET version | .NET 8 only / .NET 9 only / multi-target | **Multi-target net9.0;net8.0** | SDK needs to support LTS consumers |
| D3 | NuGet naming | `WoW2.Backbone.*` / `WoW.Two.Sdk.*` | **`WoW.Two.Sdk.*`** | Clean break, consistent with org |
| D4 | npm scope | `@wow-two` / `@wow2` / unscoped | **`@wow-two`** | Matches GitHub org name |
| D5 | React state mgmt | Context / Zustand / Jotai | **Context in SDK** | App can use whatever; SDK stays minimal |
| D6 | Component styling | Tailwind-only / CSS-in-JS / both | **Tailwind + CVA** | Proven in Haven, tree-shakeable |
| D7 | React build orchestrator | Turborepo / Nx / Lerna | **Turborepo** | Lighter, sufficient for scope |
| D8 | Versioning tool (React) | Changesets / semantic-release / manual | **Changesets** | Explicit, PR-based, good changelog |
| D9 | platform ↔ SDK split | Keep separate / merge | **Keep separate** | Platform = internal, SDK = public |
| D10 | What to do with existing single-package repos | Archive / redirect / keep parallel | **Archive after migration** | Add deprecation notice pointing to new monorepo |

---

## 10. Dependency Graph

### .NET packages (planned)

```
Language.Core.Enums         ← 0 deps
Language.Core.Time          ← MS.Extensions.DI.Abstractions
Language.Core.Types         ← 0 deps
Language.Linq               ← 0 deps
Language.Serialization.Abstractions  ← 0 deps
Language.Serialization.STJ  ← Serialization.Abstractions
Language.Serialization.Newtonsoft ← Serialization.Abstractions + Newtonsoft.Json

Data.Abstractions           ← 0 deps
Data.EfCore                 ← Data.Abstractions + EF Core
Data.Auditing               ← Data.Abstractions

Messaging.Abstractions      ← 0 deps
Messaging.MediatR           ← Messaging.Abstractions + MediatR
Messaging.MassTransit       ← Messaging.Abstractions + MassTransit

Hosting.Core                ← Language.Core.* + Validation.Abstractions
Hosting.WebApi              ← Hosting.Core + ASP.NET Core

AI.Abstractions             ← 0 deps
AI.SemanticKernel           ← AI.Abstractions + Semantic Kernel
AI.ChatCompletion           ← AI.Abstractions
```

### React packages (planned)

```
@wow-two/core               ← 0 deps (framework-agnostic)
@wow-two/vite-config        ← vite, @vitejs/plugin-react, @tailwindcss/vite
@wow-two/tsconfig           ← 0 deps (config files only)
@wow-two/eslint-config      ← eslint, typescript-eslint, eslint-plugin-react-*
@wow-two/tailwind-preset    ← tailwindcss

@wow-two/react-hooks        ← react (peer), @wow-two/core
@wow-two/react-auth         ← react (peer), @wow-two/core
@wow-two/react-query        ← react (peer), @tanstack/react-query
@wow-two/react-forms        ← react (peer), react-hook-form

@wow-two/ui-primitives      ← react (peer), @radix-ui/*, tailwindcss, cva, @wow-two/core
@wow-two/ui-layout          ← react (peer), @wow-two/ui-primitives, lucide-react
@wow-two/ui-data            ← react (peer), @tanstack/react-table, @wow-two/ui-primitives
@wow-two/ui-theme           ← react (peer), @wow-two/core
```

---

## 11. Success Criteria

| Metric | Target |
|--------|--------|
| First .NET alpha published | Week 3 |
| First npm package published | Week 5 |
| Haven backend consuming SDK packages | Week 6 |
| Haven frontend consuming @wow-two packages | Week 6 |
| 80%+ test coverage on SDK packages | Week 7 |
| CI/CD fully automated (push → test → publish) | Week 4 |
| Zero naming inconsistencies across all packages | Phase 0 |

---

## 12. Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Naming migration breaks existing consumers | High | Publish under new names, add deprecation notice to old packages for 1 release cycle |
| Over-abstraction (too many tiny packages) | Medium | Start with domain monorepos; split only when justified by real consumer needs |
| Haven diverges from SDK patterns | Medium | Haven is first consumer — SDK must work for Haven or it doesn't ship |
| No contributors beyond Max | Low (now) | Focus on personal velocity first, community second |
| .NET 9 → 10 upgrade | Low | Multi-target from day 1, upgrade LTS target annually |
| React ecosystem moves fast | Medium | Pin to React 18/19 peer deps; upgrade yearly |
| Scope creep — building packages nobody uses | Medium | Only build what Haven actually needs; everything else is backlog |

---

*Ready for implementation in a new chat session.*

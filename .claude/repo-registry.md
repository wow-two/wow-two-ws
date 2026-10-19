> **Generated** from the hubs' `catalog.yml` files (wow2's, then each hub its `hubs` lists) by `scripts/gen-repo-registry.py` — edit the owning hub's catalog, then regenerate.
>
> **Usage:** This is a lookup table. Do NOT read these files or repos proactively.
> Only access a repo when the current task specifically requires it.
>
> **Path:** wow2 repos live under `workbench/{org}/` — e.g. `workbench/wow-two-sdk/wow-two-sdk.language.core/`; folder name = org name (1:1). Ventures, client work and Ocharo sit in the owner folders `workbench/maxs-projects/` and `workbench/mfts-projects/` at each entry's `local` — [workbench layout](../conventions/development/repo/layout/workbench-layout.md).

# Repo Registry

*Last updated: 2026-10-19*

All repos use the naming convention: `{org}.{domain}[.{subdomain}]`, lowercase, dot-separated. Repo prefix matches org name exactly.

## wow-two (core)

Org: [github.com/wow-two](https://github.com/wow-two) — core identity: vision, roadmap, standards, org-wide GitHub config.

| Repo | Purpose | Status |
|------|---------|--------|
| `wow-two.refinement` | Refinement doc, vision, current state | Active |
| `wow-two.roadmap` | Project roadmap and milestones | Active |
| `wow-two.standards` | Ecosystem-wide enforceable standards + ADRs | Active |
| `.github` | Org-wide GitHub config (templates, profiles) | Active |

Also under `workbench/wow-two/`: `wow-two-modular-library-analysis.md` — historical analysis, loose file awaiting a future home repo.

## wow-two-meta (off-ecosystem)

Org: [github.com/wow-two-meta](https://github.com/wow-two-meta) — docs adjacent to but not part of the wow-two ecosystem: personal career strategy, legacy archives.

| Repo | Purpose | Status |
|------|---------|--------|
| `wow-two-meta.career-strategies` | Career strategy docs (personal, not ecosystem) | Active |
| `wow-two-meta.legacy.core` | Legacy core code (pre-migration) | Archive |
| `wow-two-meta.legacy.old-core` | Old core, formerly `WOW2.Core---Old` | Archive |

## wow-two-platform (internal infra)

Org: [github.com/wow-two-platform](https://github.com/wow-two-platform) — pipelines, DI, comms, data access. Not for external consumers.

| Repo | Purpose | Status |
|------|---------|--------|
| `wow-two-platform.pipelines` | Shared GitHub Actions: every product's reusable build-and-publish workflow and the release generator ([delivery pipeline](../docs/delivery-pipeline.md) D7) | Active |
| `wow-two-platform.core.di` | DI configuration helpers | Active |
| `wow-two-platform.core.app` | Base application setup | Active |
| `wow-two-platform.core.exceptions` | Exception handling patterns | Active |
| `wow-two-platform.core.validations` | Validation utilities | Active |
| `wow-two-platform.comms.infra` | MediatR (in-process) + MassTransit (distributed) — don't confuse them | Active |
| `wow-two-platform.data.relational` | Relational DB patterns (EF Core) | Active |
| `wow-two-platform.data.transport` | Data transportation | Draft |
| `wow-two-platform.storage.cache` | Caching abstractions | Active |
| `wow-two-platform.storage.file` | File system operations | Active |
| `wow-two-platform.docs.api` | API documentation generation | Draft |
| `wow-two-platform.templates.ai` | AI capability templates | Draft |
| `wow-two-platform.main` | Main platform assembly | Active |
| `wow-two-platform.design-patterns` | Common design patterns | Active |
| `wow-two-platform.contrimap` | POCO mapping | POC |
| `wow-two-platform.wheelhouse` | Product ops & deploy control plane (Clean-Arch .NET 10 + Vue) | Active |
| `wow-two-platform.secrets-vault` | Secrets vault — envelope-encrypted store + management UI | Active |
| `wow-two-platform.wheelhouse-canary` | Sample Vue + .NET + PostgreSQL app Wheelhouse deploys to dev and prod to prove every deployment flow | v0.1 built; awaiting first deploy |
| `.github` | Org-wide GitHub config | Active |

## wow-two-sdk (public libs & tools)

Org: [github.com/wow-two-sdk](https://github.com/wow-two-sdk) — installable packages, tools, clients.

| Repo | Purpose | Status |
|------|---------|--------|
| `wow-two-sdk.language.core` | Time providers, enum extensions, type abstractions | Published |
| `wow-two-sdk.language.linq` | LINQ extensions | Published |
| `wow-two-sdk.language.serialization` | JSON/object serialization | Published |
| `wow-two-sdk.ai.semantic-kernel` | Semantic Kernel integration | Active |
| `wow-two-sdk.ai.nlp` | NLP utilities | Active |
| `wow-two-sdk.package-analyzer` | Batch repo/package management across orgs | v1.0 |
| `wow-two-sdk.resilience-patterns` | Resilience and retry patterns | Active |

## wow-two-sdk-beta (beta SDK packages)

Org: [github.com/wow-two-sdk-beta](https://github.com/wow-two-sdk-beta) — beta-forever packages. Mirror of `wow-two-sdk` for unstable / iterating libs. Repos are **public** (Pages requirement on free tier) but Issues/Discussions disabled to keep contributor surface minimal.

| Repo | Purpose | Status |
|------|---------|--------|
| `wow-two-sdk-beta.be` | be sdk — `WoW2.Sdk.Beta.Be[.X]` (nuget.org), namespace `WoW.Two.Sdk.Beta.Be[.X]`; mono-lib: hosting, observability, web, mediator, identity, data. Code: `engineering/codebase/wow-two-sdk-beta-be/` | Active (beta) |
| `wow-two-sdk-beta.fe` | fe sdk — `@wow-two-beta/fe` (npm), Vue 3 components, application adapters, browser capabilities. Code: `engineering/codebase/wow-two-sdk-beta-fe/`; the parked React `@wow-two-beta/ui` sits in `engineering/codebase/wow-two-front-beta-sdk/` | Active (beta) |
| `wow-two-sdk-beta.product-template` | Copyable product-repo template — the canonical conformant structure `create-repo` stamps out (a template, not a package) | Active |

## wow-two-kb (knowledge base)

Org: [github.com/wow-two-kb](https://github.com/wow-two-kb) — code samples, runnable demos, real-world docs.

| Repo | Purpose | Status |
|------|---------|--------|
| `wow-two-kb.welcome` | Welcome page / index | Stub |
| `wow-two-kb.dotnet.efcore` | EF Core ORM patterns | Has code |
| `wow-two-kb.dotnet.efcore.issues` | EF Core common issues & solutions | Has docs |
| `wow-two-kb.dotnet.mediatr` | MediatR examples (Messages, Streams, PipelineBehavior) | Has code |
| `wow-two-kb.dotnet.httpclient` | HttpClient REST docs | Has docs |
| `wow-two-kb.dotnet.concurrency` | Async/concurrent patterns | Has code |
| `wow-two-kb.dotnet.generics` | Generic programming | Has code |
| `wow-two-kb.dotnet.di` | IoC/DI container patterns | Has code |
| `wow-two-kb.dotnet.security.identity` | Identity & auth | Has code |
| `wow-two-kb.dotnet.security.base` | Base security framework | Has code |
| `wow-two-kb.dotnet.webapi` | ASP.NET Core Web API helpers | Has code |
| `wow-two-kb.dotnet.api.rest` | HTTP/REST communication patterns | Has code |
| `wow-two-kb.dotnet.notifications` | Event-based notifications | Has code |
| `wow-two-kb.dotnet.notifications.framework` | Notifications framework | Has code |
| `wow-two-kb.dotnet.optimization.general` | Performance optimization | Has code |
| `wow-two-kb.dotnet.optimization.db` | DB & memory optimization | Has code |
| `wow-two-kb.dotnet.mapping` | AutoMapper patterns | Has code |
| `wow-two-kb.dotnet.files` | File I/O | Has code |
| `wow-two-kb.dotnet.data.abstractions` | Data access abstractions | Has code |
| `wow-two-kb.dotnet.jobs` | Background jobs & scheduling | Has code |
| `wow-two-kb.dotnet.framework` | .NET framework patterns | Has code |

## wow-two-apps (community products)

Org: [github.com/wow-two-apps](https://github.com/wow-two-apps) — no public repos yet.

| Repo | Purpose | Status |
|------|---------|--------|
| `wow-two-apps.med-text-fab` | DS3-150 bandage machine parameter analysis and Vue/.NET educational 3D simulator | Local repository; uncalibrated model; no version track |
| `wow-two-apps.home-atlas` | Private home reference mapping and layered Vue/.NET 3D renovation workbench | Local repository; mapping under review; no version track |

> **Note**: Apps like Feedback.Analyzer, DDLParser, StudyMate etc. are still in the old `WoW-2-0-Projects` org and haven't been migrated yet.

## 10x Ventures

Hub: [sulton-max/10x-ventures](https://github.com/sulton-max/10x-ventures) — The owner's venture portfolio from idea to live, and ventures and client work run for others.

| Repo / local folder | Purpose | Status |
|---|---|---|
| `sulton-max/10x-venture-forever-pin` · `workbench/maxs-projects/ventures/10x-venture-forever-pin` | ForeverPin QR and programmable links | Active, v0.9 |
| `sulton-max/10x-ven-haven` · `workbench/maxs-projects/ventures/10x-ven-haven` | Haven: real estate platform for Tashkent; agents classify, triage and publish ListingShelf listings | Active; v1.1 and v1.2 in progress |
| `ventures.surface-pattern` · `workbench/maxs-projects/ventures/ventures.surface-pattern` | Surface Pattern: local repeat-pattern studio, surface previews and print exports | v0.1 local studio built; demand and physical print validation pending |
| `sulton-max/ventures.listing-shelf` · `workbench/maxs-projects/ventures/ventures.listing-shelf` | ListingShelf: listing/post crawler and archive; OLX and Domtut initial adapters, no social media | v0.2 built (Vue shelf console, SDK 10.0.59); verification pending |
| `ventures.pose-coach` · `workbench/maxs-projects/ventures/ventures.pose-coach` | PoseCoach: iPhone photo director (Swift/SwiftUI) with a .NET API and Vue console | v0.1 duo collage flow built locally (pattern check, alignment, collage, eye screens); iPhone verification pending |
| `ventures.retainer-balance` · `workbench/maxs-projects/ventures/ventures.retainer-balance` | Retainer Balance — first-ten SaaS pilot | Local v0.1 implemented and tested; authenticated Vue/.NET pilot; launch gates remain |
| `ventures.documentation-checker` · `workbench/maxs-projects/ventures/ventures.documentation-checker` | Documentation Checker — first-ten SaaS pilot | Local v0.1 implemented and tested; authenticated Vue/.NET pilot; launch gates remain |
| `ventures.file-watch` · `workbench/maxs-projects/ventures/ventures.file-watch` | File Watch — first-ten SaaS pilot | Local v0.1 implemented and tested; authenticated Vue/.NET pilot; launch gates remain |
| `ventures.procedure-review` · `workbench/maxs-projects/ventures/ventures.procedure-review` | Procedure Review — first-ten SaaS pilot | Local v0.1 implemented and tested; authenticated Vue/.NET pilot; launch gates remain |
| `ventures.training-seats` · `workbench/maxs-projects/ventures/ventures.training-seats` | Training Seats — first-ten SaaS pilot | Local v0.1 implemented and tested; authenticated Vue/.NET pilot; launch gates remain |
| `ventures.epub-review` · `workbench/maxs-projects/ventures/ventures.epub-review` | Epub Review — first-ten SaaS pilot | Local v0.1 implemented and tested; authenticated Vue/.NET pilot; launch gates remain |
| `ventures.customer-promises` · `workbench/maxs-projects/ventures/ventures.customer-promises` | Customer Promises — first-ten SaaS pilot | Local v0.1 implemented and tested; authenticated Vue/.NET pilot; launch gates remain |
| `ventures.vendor-renewals` · `workbench/maxs-projects/ventures/ventures.vendor-renewals` | Vendor Renewals — first-ten SaaS pilot | Local v0.1 implemented and tested; authenticated Vue/.NET pilot; launch gates remain |
| `ventures.config-checker` · `workbench/maxs-projects/ventures/ventures.config-checker` | Config Checker — first-ten SaaS pilot | Local v0.1 implemented and tested; authenticated Vue/.NET pilot; launch gates remain |
| `ventures.podcast-readiness` · `workbench/maxs-projects/ventures/ventures.podcast-readiness` | Podcast Readiness — first-ten SaaS pilot | Local v0.1 implemented and tested; authenticated Vue/.NET pilot; launch gates remain |
| `sulton-max/10x-ventures-prism` · `workbench/maxs-projects/ventures/10x-ventures-prism` | PRISM: browser parametric room and interior modeler — 2D plan editor and live 3D | v0.15 shipped; v0.16 parked for the engine rewrite; v0.17 planned |
| `sulton-max/10x-ventures-whiteout` · `workbench/maxs-projects/ventures/whiteout` | Whiteout: browser tactical sniper FPS on WebGPU (React Three Fiber); the presets repository holds its Blender asset library | v0.7 in progress (crate hero asset); v0.8 and v0.9 drafted |
| `sulton-max/10x-ventures-transcript-forge` · `workbench/maxs-projects/ventures/10x-ventures-transcript-forge` | TranscriptForge: YouTube transcription engine (captions first, Whisper fallback) under a creator repurposing suite | v0.8 in progress |
| `ventures.hijinx` · `workbench/maxs-projects/ventures/ventures.hijinx` | Hijinx: web-first party and fun apps (web, PWA and native shells) fed by Fun Vault packs | v0.1 in progress; no remote |
| `ventures.fun-vault` · `workbench/maxs-projects/ventures/ventures.fun-vault` | Fun Vault: curated fun-content library (pranks, party games, icebreakers) that Hijinx and Arcade consume as packs | Usable content library; no remote |
| `ventures.arcade` · `workbench/maxs-projects/ventures/ventures.arcade` | Arcade: Telegram Mini App games collection (Vue on a .NET host), monetized with Telegram Stars cosmetics | v0.1 in progress (15 games in the launcher); no remote |
| `sift` · `workbench/maxs-projects/ventures/sift` | Sift: curated anti-brainrot YouTube feed ranked by information density | v0.2 in progress; no remote |
| `ventures.pbn-studio` · `workbench/maxs-projects/ventures/ventures.pbn-studio` | PbnStudio: photo to custom paint-by-numbers kit generator | v0.1 in progress; no remote |
| `sulton-max/10x-ventures.museums-gallery` · `workbench/maxs-projects/ventures/ventures.museums-gallery` | Museums Gallery: desktop-first gallery of Uzbekistan's museums and heritage sites | v0.1 frontend-only; seed data unverified |
| `sulton-max/ventures.tnis` · `workbench/maxs-projects/ventures/ventures.tnis` | TNIS: transport network impact simulation, continued as a product after the National Transport Hackathon 2026 | v0.3 in progress |
| `ventures.city-vision` · `workbench/maxs-projects/ventures/ventures.city-vision` | City Vision: speculative circular city with six satellites — vision, domains and baseline parameters | Documentation and drawings; no application code; no remote |
| `sulton-max/trademark-watcher-poc` · `workbench/maxs-projects/ventures/trademark-watcher-poc` | Trademark Watcher: filing watcher that ranks recent registry filings by similarity to a keyword | POC scaffold; idle since 2026-05 |
| `sulton-max/acquisition-explorer-poc` · `workbench/maxs-projects/ventures/acquisition-explorer-poc` | Acquisition Explorer: company and M&A ownership graph | Frontend scaffold; idle since 2026-05 |
| `sulton-max/pdf-editor` · `workbench/maxs-projects/ventures/pdf-editor` | PDF Editor: PDF editing tool | Scaffold; scope undefined; idle since 2026-05 |
| `sulton-max/10x-fin-nt` · `workbench/maxs-projects/ventures/10x-fin-nt` | NT auction tracker for Uzbekistan | Dormant; kept as a personal tool |
| `10x-venture-forever-pin-promo` · `workbench/maxs-projects/ventures/10x-venture-forever-pin-promo` | ForeverPin promo and hero videos (Remotion) | Usable; local only |
| `airfryer-3d` · `workbench/maxs-projects/ventures/airfryer-3d` | Scroll-driven 3D product ad page (procedural Three.js model, GSAP choreography) | Usable concept page; local only |
| `sulton-max/ventures.tnis-mintrans` · `workbench/maxs-projects/clients/mintrans/ventures.tnis-mintrans` | TNIS Mintrans: the ministry handoff cut of TNIS, implemented by the ministry's own team | Handoff cut for Mintrans UZ: technical document, reference implementation and data request |
| `National-transport-hackathon/track-2-transportbrain` · `workbench/maxs-projects/clients/mintrans/track-2-transportbrain` | Transport Brain Studio: Track 2 hackathon submission; the jury demo lives in sulton-max/tbs.demo | National Transport Hackathon 2026 submission; organisers own its IP |

## ocharo-hq (brand workspace)

Org: [github.com/ocharo-hq](https://github.com/ocharo-hq) — Ocharo's brand organization: platform, studio, marketing and assets, independent of WoW2.

Six main repositories plus the `.github` profile repository belong to Ocharo. Blog, Brand and Catalogue are adopted components, not additional repository targets. Current paths: [Ocharo repository map](../workbench/mfts-projects/ventures/ocharo-hq/ocharo-ws/docs/repositories.md).

- `workbench/mfts-projects/ventures/ocharo-hq/ocharo-ws/` owns Ocharo setup and repository navigation.
- Its Git history and GitHub organization remain independent of WoW2.
- Its managed repositories sit directly under its own ignored `workbench/`.
- Coding chats use the WoW2 root for existing shared hooks and engineering conventions.

| Repo / local folder | Purpose | Status |
|---|---|---|
| `ocharo-platform` · `workbench/mfts-projects/ventures/ocharo-hq/ocharo-ws/workbench/ocharo-platform` | Ocharo Platform: brand identity, catalogue and business management; adopted Brand Workspace | Brand/Catalogue sources adopted; application integration pending |
| `ocharo-studio` · `workbench/mfts-projects/ventures/ocharo-hq/ocharo-ws/workbench/ocharo-studio` | Ocharo Studio: 3D mannequin and per-part textile creative studio | Existing Studio implementation retained; integration deferred |
| `ocharo-marketing` · `workbench/mfts-projects/ventures/ocharo-hq/ocharo-ws/workbench/ocharo-marketing` | Ocharo Marketing: operator desk, editorial/public app container, distribution and lead capture | Both Blog sources adopted; broader public apps/integration pending |
| `ocharo-assets` · `workbench/mfts-projects/ventures/ocharo-hq/ocharo-ws/workbench/ocharo-assets` | Ocharo Assets: asset creation and motion research; Ocharo Motion runtime retained | Garment library adopted; runtime integration deferred |
| `ocharo-hq` · `workbench/mfts-projects/ventures/ocharo-hq/ocharo-ws/workbench/ocharo-hq` | Main brand overview and public portfolio README | Published, private; public visibility recommended |
| `.github` · `workbench/mfts-projects/ventures/ocharo-hq/ocharo-ws/workbench/.github` | GitHub organization profile at profile/README.md | Public; organization profile published |

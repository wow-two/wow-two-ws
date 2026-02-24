> **Usage:** This is a lookup table. Do NOT read these files or repos proactively.
> Only access a repo when the current task specifically requires it.
>
> **Path:** All repos live under `workbench/` — e.g. `workbench/sdk/wow-two-sdk.language.core/`, `workbench/meta/wow-two.refinement/`.

# Repo Registry

*Last updated: 2026-02-24 06:00 PM*

All repos use the naming convention: `{org}.{domain}[.{subdomain}]`, lowercase, dot-separated. Repo prefix matches org name exactly.

## wow-two (meta)

Org: [github.com/wow-two](https://github.com/wow-two) — entry point, roadmap, org-wide config.

| Repo | Purpose | Status |
|------|---------|--------|
| `wow-two.refinement` | Refinement doc, roadmap, vision | Active |
| `wow-two.roadmap` | Project roadmap and milestones | Active |
| `wow-two.career-strategies` | Career strategy docs | Active |
| `.github` | Org-wide GitHub config (templates, profiles) | Active |
| `legacy.core` | Legacy core code (pre-migration) | Archive |
| `WOW2.Core---Old` | Old core (pre-migration) | Archive |

## wow-two-platform (internal infra)

Org: [github.com/wow-two-platform](https://github.com/wow-two-platform) — pipelines, DI, comms, data access. Not for external consumers.

| Repo | Purpose | Status |
|------|---------|--------|
| `wow-two-platform.pipelines` | CI/CD pipeline templates (GitHub Actions, NuGet publish) | Active |
| `wow-two-platform.core.di` | DI configuration helpers | Active |
| `wow-two-platform.core.app` | Base application setup | Active |
| `wow-two-platform.core.exceptions` | Exception handling patterns | Active |
| `wow-two-platform.core.validations` | Validation utilities | Active |
| `wow-two-platform.comms.infra` | MediatR + MassTransit communication | Active |
| `wow-two-platform.data.relational` | Relational DB patterns (EF Core) | Active |
| `wow-two-platform.data.transport` | Data transportation | Draft |
| `wow-two-platform.storage.cache` | Caching abstractions | Active |
| `wow-two-platform.storage.file` | File system operations | Active |
| `wow-two-platform.docs.api` | API documentation generation | Draft |
| `wow-two-platform.templates.ai` | AI capability templates | Draft |
| `wow-two-platform.main` | Main platform assembly | Active |
| `wow-two-platform.design-patterns` | Common design patterns | Active |
| `wow-two-platform.contrimap` | POCO mapping | POC |
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

> **Note**: Apps like Feedback.Analyzer, DDLParser, StudyMate etc. are still in the old `WoW-2-0-Projects` org and haven't been migrated yet.

> **Usage:** This is a lookup table. Do NOT read these files or repos proactively.
> Only access a repo when the current task specifically requires it.

# Repo Registry

All repos use the post-migration naming convention: `{category}.{domain}`, lowercase, dot-separated.

## wow-two (meta)

Org: [github.com/wow-two](https://github.com/wow-two) — entry point, roadmap, org-wide config.

| Repo | Purpose | Status |
|------|---------|--------|
| `refinement` | Refinement doc, roadmap, vision | Active |
| `roadmap` | Project roadmap and milestones | Active |
| `career-strategies` | Career strategy docs | Active |
| `.github` | Org-wide GitHub config (templates, profiles) | Active |
| `legacy.core` | Legacy core code (pre-migration) | Archive |
| `WOW2.Core---Old` | Old core (pre-migration) | Archive |

## wow-two-platform (internal infra)

Org: [github.com/wow-two-platform](https://github.com/wow-two-platform) — pipelines, DI, comms, data access. Not for external consumers.

| Repo | Purpose | Status |
|------|---------|--------|
| `platform.pipelines` | CI/CD pipeline templates (GitHub Actions, NuGet publish) | Active |
| `platform.core.di` | DI configuration helpers | Active |
| `platform.core.app` | Base application setup | Active |
| `platform.core.exceptions` | Exception handling patterns | Active |
| `platform.core.validations` | Validation utilities | Active |
| `platform.comms.infra` | MediatR + MassTransit communication | Active |
| `platform.data.relational` | Relational DB patterns (EF Core) | Active |
| `platform.data.transport` | Data transportation | Draft |
| `platform.storage.cache` | Caching abstractions | Active |
| `platform.storage.file` | File system operations | Active |
| `platform.docs.api` | API documentation generation | Draft |
| `platform.templates.ai` | AI capability templates | Draft |
| `platform.main` | Main platform assembly | Active |
| `platform.design-patterns` | Common design patterns | Active |
| `platform.contrimap` | POCO mapping | POC |
| `.github` | Org-wide GitHub config | Active |

## wow-two-sdk (public libs & tools)

Org: [github.com/wow-two-sdk](https://github.com/wow-two-sdk) — installable packages, tools, clients.

| Repo | Purpose | Status |
|------|---------|--------|
| `sdk.language.core` | Time providers, enum extensions, type abstractions | Published |
| `sdk.language.linq` | LINQ extensions | Published |
| `sdk.language.serialization` | JSON/object serialization | Published |
| `sdk.ai.semantic-kernel` | Semantic Kernel integration | Active |
| `sdk.ai.nlp` | NLP utilities | Active |
| `sdk.package-analyzer` | Batch repo/package management across orgs | v1.0 |
| `sdk.resilience-patterns` | Resilience and retry patterns | Active |

## wow-two-kb (knowledge base)

Org: [github.com/wow-two-kb](https://github.com/wow-two-kb) — code samples, runnable demos, real-world docs.

| Repo | Purpose | Status |
|------|---------|--------|
| `kb.welcome` | Welcome page / index | Stub |
| `kb.dotnet.efcore` | EF Core ORM patterns | Has code |
| `kb.dotnet.efcore.issues` | EF Core common issues & solutions | Has docs |
| `kb.dotnet.mediatr` | MediatR examples (Messages, Streams, PipelineBehavior) | Has code |
| `kb.dotnet.httpclient` | HttpClient REST docs | Has docs |
| `kb.dotnet.concurrency` | Async/concurrent patterns | Has code |
| `kb.dotnet.generics` | Generic programming | Has code |
| `kb.dotnet.di` | IoC/DI container patterns | Has code |
| `kb.dotnet.security.identity` | Identity & auth | Has code |
| `kb.dotnet.security.base` | Base security framework | Has code |
| `kb.dotnet.webapi` | ASP.NET Core Web API helpers | Has code |
| `kb.dotnet.api.rest` | HTTP/REST communication patterns | Has code |
| `kb.dotnet.notifications` | Event-based notifications | Has code |
| `kb.dotnet.notifications.framework` | Notifications framework | Has code |
| `kb.dotnet.optimization.general` | Performance optimization | Has code |
| `kb.dotnet.optimization.db` | DB & memory optimization | Has code |
| `kb.dotnet.mapping` | AutoMapper patterns | Has code |
| `kb.dotnet.files` | File I/O | Has code |
| `kb.dotnet.data.abstractions` | Data access abstractions | Has code |
| `kb.dotnet.jobs` | Background jobs & scheduling | Has code |
| `kb.dotnet.framework` | .NET framework patterns | Has code |

## wow-two-apps (community products)

Org: [github.com/wow-two-apps](https://github.com/wow-two-apps) — no public repos yet.

> **Note**: Apps like Feedback.Analyzer, DDLParser, StudyMate etc. are still in the old `WoW-2-0-Projects` org and haven't been migrated yet.

# WoW 2.0 — Workspace Root

## Important: Lazy Loading

- Do NOT pre-read or scan files at conversation start
- Only open a file when the current question or task specifically requires its content
- The repo registry in `.claude/rules/repo-registry.md` is a lookup table, not a reading list
- Answer from what you already know first, then read files only if needed
- When a task requires context, read the minimum number of files necessary

## What is this

WoW 2.0 (Way of Web 2.0) is a full-stack developer ecosystem for building production apps with .NET + React. It provides plug-and-play libraries, pre-built clients, Docker images, and hosted APIs — backed by a knowledge base of real-world patterns, gotchas, and solutions.

This workspace (`wow-two-ws`) is a meta-repo tracking workspace-level config only. All managed repos are independent git repos living inside `workbench/`, which is gitignored as a whole.

## Workspace layout

```
.                                 ← you are here (wow-two-ws root)
├── CLAUDE.md                     ← this file
├── .claude/rules/                ← auto-loaded rules
│   ├── repo-registry.md          ← full index of all repos
│   ├── behavior-rules.md         ← lookup rules, workflows, conventions
│   └── templates/                ← CLAUDE.md templates per repo type
├── docs/                         ← ecosystem-wide strategy & standards
├── ideas/                        ← project specs & proposals
├── scripts/                      ← workspace automation (clone, setup)
└── workbench/                    ← all managed repos (gitignored)
    ├── meta/                     ← wow-two org repos (roadmap, docs, refinement)
    ├── platform/                 ← wow-two-platform org repos (internal infra)
    ├── sdk/                      ← wow-two-sdk org repos (public libs/tools)
    ├── kb/                       ← wow-two-kb org repos (tech knowledge base)
    ├── apps/                     ← wow-two-apps org repos (community products)
    └── ...                       ← any additional repos (ventures, products, experiments)
```

## GitHub orgs

| Org | Link | Role |
|-----|------|------|
| **wow-two** | [github.com/wow-two](https://github.com/wow-two) | Entry point, meta, roadmap |
| **wow-two-platform** | [github.com/wow-two-platform](https://github.com/wow-two-platform) | Internal infra — pipelines, DI, comms |
| **wow-two-sdk** | [github.com/wow-two-sdk](https://github.com/wow-two-sdk) | Public libs, tools, clients |
| **wow-two-kb** | [github.com/wow-two-kb](https://github.com/wow-two-kb) | Knowledge base — code samples + docs |
| **wow-two-apps** | [github.com/wow-two-apps](https://github.com/wow-two-apps) | Community products |

## Working rules

- **Parallel sessions**: typically 2-3 related repos per chat session
- **Cross-repo changes**: when updating a lib, check its consumers for breaking changes
- **Each repo has its own CLAUDE.md**: child CLAUDE.md overrides this root for repo-specific rules
- **Passive language only**: describe where things are, never instruct to pre-read
- **Commit style**: conventional commits (`feat:`, `fix:`, `docs:`, `refactor:`)
- **All repos live in `workbench/`**: org repos, ventures, products, experiments — everything managed by this workspace

## Tech stack

- Backend: .NET 8/9, ASP.NET Core, EF Core, MediatR, MassTransit
- Frontend: React (stack decisions TBD — Vite, state management, etc.)
- CI/CD: GitHub Actions (pipeline templates in `wow-two-platform.pipelines`)
- Packages: NuGet (backend), npm (frontend, future)
- Architecture: Clean Architecture, CQRS, event-driven, DI

## Key files

- `docs/wow-two-refinement.md` — current project state, vision, task list, and roadmap
- `.claude/rules/repo-registry.md` — all repos indexed by org with current names
- `.claude/rules/behavior-rules.md` — lookup and workflow conventions
- `.claude/rules/templates/` — CLAUDE.md templates for each repo type

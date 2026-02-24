# WoW 2.0 — Way of Web 2.0

A full-stack developer ecosystem for building production apps with **.NET + React**.

Plug-and-play libraries, pre-built clients, Docker images, hosted APIs, and a knowledge base of real-world patterns — built first for the internal team, designed to scale to the open-source community.

## Ecosystem structure

```
wow-two                  → meta: roadmap, refinement, org config
├── wow-two-platform     → internal infra: pipelines, DI, comms, data access
├── wow-two-sdk          → public libs: language extensions, AI, tools
├── wow-two-kb           → knowledge base: code samples, demos, docs
├── wow-two-apps         → community products built with the ecosystem
└── (local only)         → ventures/, products/ — not cloned by setup script
```

| Org | Repos | Description |
|-----|-------|-------------|
| [wow-two](https://github.com/wow-two) | 6 | Entry point, roadmap, org-wide config |
| [wow-two-platform](https://github.com/wow-two-platform) | 16 | Internal infra — pipelines, DI, comms, data access |
| [wow-two-sdk](https://github.com/wow-two-sdk) | 7 | Public NuGet packages — language, AI, tools |
| [wow-two-kb](https://github.com/wow-two-kb) | 21 | Knowledge base — .NET code samples & docs |
| [wow-two-apps](https://github.com/wow-two-apps) | 0 | Community products (migration pending) |

## Getting started

One command to clone everything — workspace + all 50 repos:

```bash
curl -sLO https://raw.githubusercontent.com/wow-two/wow-two-workspace/main/setup.sh && bash setup.sh
```

That's it. Use `bash setup.sh --ssh` for SSH, or `bash setup.sh --dry-run` to preview.

<details>
<summary>Manual setup (step by step)</summary>

```bash
# 1. Clone the workspace
git clone https://github.com/wow-two/wow-two-workspace.git
cd wow-two-workspace

# 2. Clone all org repos into the workspace
./scripts/clone-all.sh
```

</details>

Result:

```
wow-two-workspace/
├── meta/          ← wow-two repos
├── platform/      ← wow-two-platform repos
├── sdk/           ← wow-two-sdk repos
├── kb/            ← wow-two-kb repos
├── apps/          ← wow-two-apps repos
├── ventures/      ← your venture repos (local only, not cloned by setup)
└── products/      ← (future) community profit projects
```

Open the workspace root in your editor — Claude auto-picks up `CLAUDE.md` and `.claude/rules/`.

## Tech stack

- **Backend**: .NET 8/9, ASP.NET Core, EF Core, MediatR, MassTransit
- **Frontend**: React (stack decisions TBD)
- **CI/CD**: GitHub Actions (templates in `platform.pipelines`)
- **Packages**: NuGet (backend), npm (frontend, future)
- **Architecture**: Clean Architecture, CQRS, event-driven, DI

## What developers get

| Format | Example |
|--------|---------|
| NuGet/npm library | `sdk.language.core` — add to project, configure, done |
| Pluggable client | Pre-built API client with typed contracts |
| Docker image | `docker run wow-cache` — run locally or host |
| Hosted API | Managed service for select tools |
| Wiki + KB | Real issues, patterns, decisions — not just API docs |

## Project status

**Phase 0 — Foundation** (current): wiring up the workspace, Claude setup, repo structure, clone scripts.

See [`wow-2.0-refinement.md`](wow-2.0-refinement.md) for the full roadmap.

## Contributing

Contribution guidelines coming in Phase 1. For now, work happens through Claude-assisted sessions on this workspace.

## License

TBD

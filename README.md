# wow-two-ws

The workspace orchestrator for the [WoW 2.0](https://github.com/wow-two) ecosystem. This repo manages, clones, and organizes all repos across multiple GitHub orgs into a single local workspace. It tracks only workspace-level config — scripts, docs, Claude setup. All managed repos are independent git repos living inside `workbench/`, which is gitignored as a whole.

## How git works

### Two layers of git

1. **This repo** (`wow-two-ws`) — tracks workspace config, scripts, docs, Claude setup
2. **Child repos** — each is an independent git repo inside `workbench/` with its own remote, branches, and history

The entire `workbench/` folder is gitignored, so `git status` at the workspace root only shows workspace-level changes. Running `git status` inside any child folder (e.g. `workbench/sdk/sdk.language.core/`) shows that repo's own changes. No tangling between layers.

### Workbench structure

The clone script maps each GitHub org to a folder inside `workbench/`:

| GitHub Org | Local Folder | Role |
|---|---|---|
| [wow-two](https://github.com/wow-two) | `workbench/meta/` | Roadmap, org config, legacy |
| [wow-two-platform](https://github.com/wow-two-platform) | `workbench/platform/` | Internal infra — pipelines, DI, comms, data |
| [wow-two-sdk](https://github.com/wow-two-sdk) | `workbench/sdk/` | Public NuGet packages — language, AI, tools |
| [wow-two-kb](https://github.com/wow-two-kb) | `workbench/kb/` | Knowledge base — code samples & docs |
| [wow-two-apps](https://github.com/wow-two-apps) | `workbench/apps/` | Community products |

You can also add your own repos under `workbench/` — for ventures, products, experiments, or anything else you're building with the ecosystem. They'll be gitignored from the workspace automatically.

## Getting started

### Prerequisites

- `git`
- [`gh` CLI](https://cli.github.com/) authenticated via `gh auth login`

### One-command setup

```bash
curl -sLO https://raw.githubusercontent.com/wow-two/wow-two-ws/main/setup.sh && bash setup.sh
```

This clones the workspace repo, then runs `scripts/clone-all.sh` which uses `gh repo list` to discover and clone every repo from every org into `workbench/`.

| Flag | Effect |
|---|---|
| `--ssh` | Use SSH URLs instead of HTTPS |
| `--dry-run` | Preview what would be cloned |

### Manual setup

```bash
git clone https://github.com/wow-two/wow-two-ws.git
cd wow-two-ws
bash scripts/clone-all.sh
```

## How Claude works with this workspace

The workspace is designed for Claude-assisted development. Open the workspace root in your editor — Claude auto-loads `CLAUDE.md` and `.claude/rules/`.

### Architecture

```
CLAUDE.md                                    ← workspace-level instructions (auto-loaded)
.claude/rules/
├── repo-registry.md                         ← index of all repos (lazy-loaded lookup)
├── behavior-rules.md                        ← cross-repo workflows, naming, conventions
└── templates/                               ← CLAUDE.md templates for new repos

workbench/meta/some-repo/CLAUDE.md           ← repo-specific overrides (if present)
workbench/sdk/sdk.language.core/CLAUDE.md    ← repo-specific overrides (if present)
```

### Key principles

- **Lazy loading** — Claude never pre-reads repos or files; the registry is a lookup table, not a reading list
- **Scoped context** — each child repo can have its own `CLAUDE.md` that overrides the workspace root for repo-specific rules
- **No tangling** — `workbench/` is gitignored, so Claude can commit to either layer without cross-contamination
- **Cross-repo awareness** — when updating a library, Claude checks the registry for consumers and coordinates breaking changes
- **Parallel sessions** — typically 2-3 related repos per chat session

### Common workflows

| Task | Claude does |
|---|---|
| Work on a specific repo | Reads its `CLAUDE.md`, follows repo-specific rules |
| Find a repo by topic | Looks up `repo-registry.md`, matches by domain |
| Update a shared library | Identifies consumers in registry, checks for breakage |
| Add a new repo | Clones it into the right folder, creates `CLAUDE.md` from template |

## Key docs

| Doc | What it covers |
|---|---|
| [`wow-2.0-refinement.md`](wow-2.0-refinement.md) | Vision, roadmap, current phase, task list |
| [`branching-strategy.md`](branching-strategy.md) | Trunk-based dev/main flow, CI publish channels |
| [`versioning-strategy.md`](versioning-strategy.md) | .NET-aligned versioning, pre-release suffixes |
| [`.claude/rules/repo-registry.md`](.claude/rules/repo-registry.md) | Full index of all repos by org, purpose, and status |

## Tech stack

- **Backend**: .NET 8/9, ASP.NET Core, EF Core, MediatR, MassTransit
- **Frontend**: React (stack decisions TBD)
- **CI/CD**: GitHub Actions (templates in `platform.pipelines`)
- **Packages**: NuGet (backend), npm (frontend, future)
- **Architecture**: Clean Architecture, CQRS, event-driven, DI

## Project status

**Phase 0 — Foundation** (current): workspace wiring, Claude setup, repo structure, clone scripts. See [Key docs](#key-docs) for the full roadmap.

## Contributing

Contribution guidelines coming in Phase 1. For now, work happens through Claude-assisted sessions on this workspace.

## License

TBD

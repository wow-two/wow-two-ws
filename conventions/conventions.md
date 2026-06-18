# Conventions — wow-two

*Last updated: 2026-06-17*

> **The single index to every convention.** When a task touches *how we build* — code, repo structure,
> naming, versioning — search HERE first, then open only the file(s) you need. Lookup table,
> **not auto-loaded**; do not pre-read the targets. Area indexes are named `{area}-conventions.md`; this is the root.

## How to use

1. Find what the task touches below.
2. Open that ONE file (leaf files live in the area sub-folders).
3. A repo-level rule (`workbench/{repo}/CLAUDE.md` or `.claude/rules/`) **overrides** a convention for that repo.

## Authoring a convention

Every convention doc follows this shape:

```markdown
# {Title}                         ← noun, matches the file name

*Last updated: YYYY-MM-DD*

> {What — one line}.
> Purpose — {why it exists / the problem it solves}.
> Use case — {when / where you reach for it}.

## {Section}

- compact bullet · backtick every `Symbol` and `path/to/file`
- one fact per bullet, no paragraph > 2 lines

---

## {Next section}

- ...
```

Rules:

- **Super-compact by default** — a convention is a *reference, not a tutorial*. Cut every word that doesn't change what the reader does; if a rule fits in
  a table row or a 1-line bullet, it must not be a paragraph.
- **Shape** — `# Title` → `*Last updated:*` → description blockquote → `##` sections. `---` between **every** section. No `## See also` — link inline only
  where load-bearing.
- **Description** — a 3-line blockquote: **What** (one line, what it governs + scope boundary), **Purpose** (the *why* / benefit / problem it solves),
  **Use case** (the *when* / where you reach for it). Purpose ≠ Use case — don't let both collapse to the same phrase. Not "Conventions for X" filler.
- **Density** — super-compact bullets, imperatives, one fact per line. No prose paragraph > 2 lines. Code fence for multi-line only; backticks for every
  identifier.
- **Hard wrap** — wrap prose at **150 cols** (the editor's setting).
- **Tables vs bullets** — tables only for narrow 3+-item × 2+-col data that fits inside 150 cols. If any row would exceed the 150-col hard wrap,
  convert that table to bullet points — a wrapped wide table is unreadable.
- **Citation** — concrete symbols (`IKeyedEntity<TId>`, `AddDatabaseBespokeMigrations`) + file paths, **never namespaces** (they go stale — grep the
  symbol). Verify a symbol exists in source before citing; examples come from real code.
- **No duplication** — reference another convention inline; don't restate it. Supersede a stale note in place rather than stacking.
- **Location** — `{sub-domain}/{name}.md`; a folder's lead doc is `{folder}.md`, `README.md` only at a repo root.

## Domains

| Domain | Covers | Status |
|---|---|---|
| **development** (below) | how we build — repo shape, backend & frontend code style | Active |
| **planning** (below) | how we plan — version docs (grows over time) | Active |
| **agentic-workflow** (below) | how parallel chats / agents share a repo — lanes · no-revert · scope containment | Active |
| deployment | VPS, Docker, Traefik, CI/CD, release | Planned |
| security | secrets handling, auth patterns, threat model | Planned |

---

## development — index: [development/development-conventions.md](development/development-conventions.md)

### repo/ — repo shape & setup · [repo-conventions.md](development/repo/repo-conventions.md)

| Need | File |
|---|---|
| Repo layout · `product/` + `engineering/` · code under `engineering/codebase/{slug}.{backend,frontend}-services` · naming · folder-docs (no README below root) · archetypes · **image-publish contract** (§13) · **audit** | [development/repo/repo-structure.md](development/repo/repo-structure.md) |
| Tech stack — backend + frontend + beta SDKs | [development/repo/tech-stack.md](development/repo/tech-stack.md) |
| Port ledger — allocated dev ports | [development/repo/ports.md](development/repo/ports.md) |

### backend/ — .NET conventions (by sub-domain) · [backend-conventions.md](development/backend/backend-conventions.md)

Meta: `authoring` (cite symbols, not namespaces). Sub-domains:

| Sub-domain | Docs |
|---|---|
| `code-style/` | `documentation` · `code-organization` · `members` · `models` · `idioms` |
| `architecture/` | `service-architecture` · `domain-structuring` · `host-configuration` · `services` |
| **`persistence/`** (focus) | `database` · `entities` · `enums` · `data-access` · `migrations/` (`migrations` · `bespoke-migrations` · `migration-dialects` · `ef-migrations` · `dbup-migrations` · `migration-tooling`) |
| `presentation/` | `controllers` · `controllers-known-endpoints` · `request-models` · `response-models` · `problem-details` |
| `runtime/` | `settings` · `launch-profiles` |
| `foundation/` | `result-pattern` · `validation` · `time` |
| **`integrations/`** (focus) | `clients` |
| `testing/` | `testing` |
| `messaging/` | `mediator` |
| `identity/` | `jwt-auth` |
| `observability/` · `platform/` | proposed — write as built |

### frontend/ — React / TS code style · [frontend-conventions.md](development/frontend/frontend-conventions.md)

`naming` · `documentation` · `code-organization` · `models` · `enums` · `components` · `hooks` · `extensions` · `forms` · `project-structure` · `state-and-data` · `styling`

---

## planning — index: [planning/planning-conventions.md](planning/planning-conventions.md)

| Area | File |
|---|---|
| Version docs — naming, lifecycle, cadence + iteration template | [planning/version-planning/version-docs.md](planning/version-planning/version-docs.md) |
| Engineering planning — repo roadmap + backlog | [planning/engineering-planning/engineering-planning-conventions.md](planning/engineering-planning/engineering-planning-conventions.md) |

## agentic-workflow — index: [agentic-workflow/agentic-workflow.md](agentic-workflow/agentic-workflow.md)

| Need | File |
|---|---|
| Parallel chats on one tree · assume-intentional / no-revert · lane discipline · scope containment · commit discipline | [agentic-workflow/agentic-workflow.md](agentic-workflow/agentic-workflow.md) |

## Scaffolding

- New conformant repo → skill **`create-repo`**. Template repo: `workbench/wow-two-sdk-beta/wow-two-sdk-beta.product-template/`.

## Precedence

A convention applies to **every** repo under `wow-two-ws/`; a repo-level rule overrides for that repo. The SDK's own `docs/conventions/` covers SDK-package concerns (naming, layout, registry) — no overlap.

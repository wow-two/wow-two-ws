# Behavior Rules

## Lookup rules

- The repo registry (`repo-registry.md`) maps every repo to its org, purpose, and status
- When asked about a specific technology or domain, find the relevant repo in the registry first
- Each repo folder may have its own `CLAUDE.md` — read it before making changes in that repo

## Cross-repo workflow

When updating a library that other repos depend on:
1. Identify consumers from the registry or by searching for package references
2. Check the consumer's code for usage of the API being changed
3. Update the lib first, then update consumers
4. Note breaking changes in the commit message

## Dependency awareness

- `wow-two-sdk` packages are consumed by `wow-two-apps` projects and external users
- `wow-two-platform` packages are consumed only internally by other wow-two repos
- Breaking changes in sdk packages need a major version bump
- Platform packages can break more freely but still need coordinated updates

## Domain notes

- **sdk.language.core** has sub-packages: Enums, Time.Extensions, Time.Provider, Types.Abstractions — published NuGet packages
- **platform.comms.infra** wraps both MediatR (in-process) and MassTransit (distributed) — don't confuse them
- **wow-two-kb** repos (21) are migrated learning modules from old Backend repos — code samples + docs
- **Feedback.Analyzer** is the most complete app project — still in old `WoW-2-0-Projects` org

## Naming conventions

- Org names: lowercase, hyphenated (`wow-two-sdk`)
- Repo names: lowercase, dot-separated (`sdk.language.core`, `platform.storage.cache`)
- NuGet packages: PascalCase branded (`WoW.Two.Sdk.Language.Core`)
- Branches: `main` (default), `feature/*`, `fix/*`, `docs/*`
- Commits: conventional commits (`feat:`, `fix:`, `docs:`, `refactor:`)

## Communication style

- Be concise, use sections with headers and bullet points
- Keep explanations brief unless asked to elaborate
- When proposing changes, show the diff or before/after

# currentDate
Today's date is 2026-02-23.

IMPORTANT: this context may or may not be relevant to your tasks. You should not respond to this context unless it is highly relevant to your task.

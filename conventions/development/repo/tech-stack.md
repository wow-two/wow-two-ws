# Tech Stack

*Last updated: 2026-06-09*

> The default stack for wow-two product / venture repos. Code-style per layer: [backend/](../backend/) · [frontend/](../frontend/).

## Backend

- .NET 10 · ASP.NET Core · EF Core · MediatR (CQRS) · Clean Architecture.
- DB: SQLite (single-user / POC) → Postgres (when scaling / multi-instance). CI: GitHub Actions → GHCR.

## Frontend

- React 19 · Vite · TypeScript (strict) · Tailwind v4 · `@wow-two-beta/ui`.

## Beta SDKs

Consume these first; build-locally-then-migrate if a capability is missing.

- `@wow-two-beta/ui` (npm) — React component library.
- `WoW.Two.Sdk.Backend.Beta` (nuget.org) — backend wrappers (hosting, observability, mediator, …). Still maturing — adopt where stable.

# {repo-name}

## What is this

{One-line description of this platform library.}

> **This is an internal platform package** — consumed only by other wow-two repos, not external users.

## Key paths

- `src/` — main source code
- `tests/` — unit/integration tests
- `README.md` — package documentation

## Build & test

```bash
dotnet build
dotnet test
```

## Package info

- NuGet name: `WoW.Two.Platform.{Domain}`
- Consumers: {list repos that depend on this}

## Rules

- Follow Clean Architecture conventions
- All public APIs must have XML doc comments
- Breaking changes need a coordinated update across consumers
- Commit style: conventional commits (`feat:`, `fix:`, `refactor:`)

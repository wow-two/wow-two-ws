# WoW 2.0 — Branching Strategy

> **Scope**: All SDK and Platform library repos (NuGet packages).
> App repos may need a different strategy (with staging/environments) — TBD.

---

## Branch Model: Simplified Trunk-Based

Two long-lived branches only. No staging, no test branches.

```
main ─────●─────●─────●─────●──── stable releases
           \   ↑ PR    \   ↑ PR
dev ────●───●───●───●───●───●──── active development (alpha)
```

---

## Branch Definitions

| Branch | Purpose | Protection | Publishes To |
|--------|---------|------------|-------------|
| `main` | Stable, production-ready code | Protected — merge via PR only, requires CI pass | NuGet.org (stable: `1.0.0`) |
| `dev` | Active development, integration | Default branch for daily work | GitHub Packages (alpha: `1.0.0-alpha.1`) |

### Feature branches (optional, short-lived)

```
dev ────●───────●───────●────
         \     ↑ PR
feature/  ●───●
```

- Branch off `dev`, merge back to `dev` via PR
- Naming: `feature/{description}`, `fix/{description}`, `docs/{description}`
- Delete after merge
- No CI publish — only build + test

---

## Flow: Dev → Alpha → Stable

### Daily development
```
1. Work on dev (or feature branch → PR to dev)
2. Push to dev
3. CI: build + test
4. Auto-publish: alpha package to GitHub Packages
   → WoW2.Sdk.Language.Serialization 1.0.0-alpha.{run_number}
```

### Release to stable
```
1. Create PR: dev → main
2. CI gate: build + test must pass
3. Code review (if team grows)
4. Merge PR
5. Auto-publish: stable package to NuGet.org
   → WoW2.Sdk.Language.Serialization 1.0.0
```

---

## Sequential Dependency Updates (Dev Channel)

When a change in package A requires updates in packages B, C, D... (chain updates):

```
Package A (serialization)
  └→ Package B (depends on A)
       └→ Package C (depends on B)
            └→ Package D (depends on C)
```

### Dev channel flow
1. Push change to A's dev → alpha published to GitHub Packages (~instant)
2. Update B's package reference to A's new alpha → push to B's dev → alpha published
3. Repeat down the chain
4. Each step: GitHub Packages publish is fast (no NuGet.org validation delay)

### Production channel flow
1. Once full chain is validated on dev/alpha:
2. Merge A to main → stable published to NuGet.org
3. Update B's reference to A's stable version → merge B to main
4. Repeat down the chain
5. NuGet.org delay per package (~5-10s) is acceptable here since changes are already validated

### Key insight
- Dev channel (GitHub Packages): fast iteration, chain updates happen frequently
- Prod channel (NuGet.org): batch release, chain is already validated, delay is tolerable

---

## Version Numbering

### Stable (main → NuGet.org)
```
{major}.{minor}.{patch}
Examples: 1.0.0, 1.1.0, 1.1.1, 2.0.0
```

### Prerelease (dev → GitHub Packages)
```
{major}.{minor}.{patch}-alpha.{build_number}
Examples: 1.0.0-alpha.1, 1.0.0-alpha.2, 1.1.0-alpha.1
```

### Version bumping rules
- **Patch** (`1.0.x`): bug fixes, no API changes
- **Minor** (`1.x.0`): new features, backward compatible
- **Major** (`x.0.0`): breaking changes

### Where version lives
- Defined in `.csproj` → `<Version>` / `<VersionPrefix>` property
- Alpha suffix appended by CI pipeline (not hardcoded in .csproj)

---

## Branch Cleanup

### After migration
- Delete `staging` branch
- Delete `test` branch
- Keep only `main` and `dev`

### Ongoing
- Feature branches deleted after merge
- No long-lived branches other than main and dev

---

## Repo-Specific Overrides

This strategy applies to all **library repos** (SDK + Platform). Other repo types may override:

| Repo Type | Strategy | Notes |
|-----------|----------|-------|
| SDK libs (`sdk.*`) | This document | Two branches, dual publish |
| Platform libs (`platform.*`) | This document | Same — internal but same flow |
| Apps (`apps.*`) | TBD | May need staging/env branches |
| KB modules (`kb.*`) | Simplified | Possibly main-only, no packages |
| Meta repos | Main-only | Docs, roadmap — no CI/CD needed |

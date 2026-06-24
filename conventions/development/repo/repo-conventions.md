# Conventions — Development — Repo

*Last updated: 2026-06-21*

> How a repo is shaped, equipped, and allocated. Code style for each layer is in the siblings
> [../backend/](../backend/) + [../frontend/](../frontend/).

| File | Covers |
|---|---|
| [repo-structure.md](repo-structure.md) | Top-level `product/` + `engineering/`, code under `engineering/codebase/{slug}.backend-services` + `engineering/codebase/{slug}.frontend-services`, naming, archetypes, ecosystem naming, + repo audit |
| [tech-stack.md](tech-stack.md) | Default stack — backend + frontend + beta SDKs |
| [ports.md](ports.md) | Port ledger — allocated dev ports (check before picking one) |
| [single-host-serving.md](single-host-serving.md) | Backend serves the SPA from `wwwroot` — vite `outDir` + static-serve/fallback + `BuildSpa` MSBuild target + dev proxy + CORS posture |

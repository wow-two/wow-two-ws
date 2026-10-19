# Conventions — Deployment — Hosting

*Last updated: 2026-10-19*

> Where a product runs and how it is served — the single deployable's serving model, the dev-port ledger and site hosts.

| File | Covers |
|---|---|
| [single-host-serving.md](single-host-serving.md) | Backend serves the SPA from `wwwroot` — vite `outDir` + static-serve/fallback + `BuildSpa` MSBuild target + dev proxy + CORS posture |
| [ports.md](ports.md) | Port ledger — allocated dev ports (check before picking one) |
| [environment-files.md](environment-files.md) | Per-environment files — .NET `appsettings.{Development,Production}.json`, a target's mounted `appsettings.Target.json`, machine-local `appsettings.Local.json` · others `{name}-{environment}.{ext}` |
| [domains.md](domains.md) | Site hosts — bound per environment in Wheelhouse · apex, `www`, product and dev hosts · proxy and tailnet exposure |

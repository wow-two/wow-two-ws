# Project structure

*Last updated: 2026-06-10*

Two shapes, chosen by app count. Both live under a repo's `engineering/codebase/{slug}.frontend-services/` (dot-prefixed with the repo slug, per [../repo/repo-structure.md](../repo/repo-structure.md)). `@{brand}` = the repo's package scope (`@haven`, `@drydock`, …).

## Shape A — single Vite app (default)

One product, one frontend. No workspace, no shared packages.

```
{slug}.frontend-services/     ← the Vite app itself
├── index.html
├── vite.config.ts            ← base '/', HTTPS dev (mkcert), proxy /api → backend HTTP port
├── tsconfig.json · package.json
└── src/
    ├── main.tsx              ← React mount
    ├── App.tsx              ← root layout + (auth gate)
    ├── index.css            ← Tailwind v4 + beta-UI tokens + @source (see styling.md)
    ├── api/                 ← client.ts + types.ts (same-origin /api — see state-and-data.md)
    ├── components/          ← app components (one-component-per-folder)
    ├── hooks/               ← data + UI hooks
    ├── lib/                 ← utils, *Extensions
    ├── types/              ← model + DTO types
    └── config/             ← view defs, field metadata
```

Use this until a second app or genuine cross-app reuse appears. Don't pre-build a workspace.

## Dev server — HTTPS by default

The Vite dev server runs over **HTTPS** via **`vite-plugin-mkcert`** (a locally-trusted cert — no browser warning). The backend serves plain **HTTP** (TLS terminated upstream in prod — see [../backend/launch-profiles.md](../backend/runtime/launch-profiles.md)); the frontend stays HTTPS so `Secure` auth cookies + secure-context keep working and an OAuth redirect doesn't hit a cert interstitial. Proxy `/api` to the backend's **HTTP** port with `changeOrigin: false` so the dev origin (`host:port`) is preserved end-to-end — the OAuth `redirect_uri` + session cookie then stay on the dev origin (register that origin's `/…/callback` with the provider).

```ts
import mkcert from 'vite-plugin-mkcert';

plugins: [react(), tailwindcss(), mkcert()],
server: {
  port: 7025,
  proxy: { '/api': { target: 'http://localhost:<backend-http>', changeOrigin: false, secure: false } },
},
```

First `npm run dev` may prompt once to trust the local CA (keychain) — expected.

## Shape B — pnpm workspace (multi-app)

Multiple apps sharing code. Mirrors the backend's `Common/` pattern; `"workspace:*"` ≈ .NET `<ProjectReference>`.

```
{slug}.frontend-services/
├── package.json              ← workspace root (orchestration scripts)
├── pnpm-workspace.yaml       ← declares members
├── packages/
│   ├── common/               ← @{brand}/common — hooks, identity, utils, types
│   ├── ui/                   ← @{brand}/ui — dumb presentational components
│   └── domain/               ← @{brand}/domain — entities, enums (optional)
├── {app-a}/                  ← lowercase app folder (own port)
└── {app-b}/
```

| .NET | pnpm workspace |
|---|---|
| `.sln` | `pnpm-workspace.yaml` |
| `<ProjectReference>` | `"workspace:*"` in `package.json` |
| `Common/` project | `packages/common/` |
| `dotnet build` (solution) | `pnpm install` (root) |
| `dotnet run --project X` | `pnpm --filter X dev` |

Each app's `vite.config.ts` aliases packages so Vite compiles workspace TS:

```ts
resolve: {
  alias: {
    "@": path.resolve(__dirname, "./src"),
    "@{brand}/common": path.resolve(__dirname, "../packages/common/src"),
    "@{brand}/ui": path.resolve(__dirname, "../packages/ui/src"),
  },
},
```

Each app uses the **same internal `src/` layout** as Shape A.

## Package boundaries (Shape B)

| Package | May use | May NOT use |
|---|---|---|
| `@{brand}/ui` | React, Tailwind, lucide, variants | data fetching, context, localStorage, app types |
| `@{brand}/common` | React, fetch, localStorage, context | app-specific types/components |
| `@{brand}/domain` | pure types/enums | React, side effects |
| Apps | everything + all packages | other apps |

- **`@{brand}/ui` = dumb components** — props in, JSX out. No API calls, no business logic, no context consumers.
- **`@{brand}/common` = shared logic** — hooks, identity, utils; has side effects.
- **Extract to a package only when ≥2 apps need it** — otherwise keep it app-local. Premature extraction adds workspace ceremony for no gain.

## Beta UI relationship

`@wow-two-beta/ui` is the **ecosystem-wide** component library (consumed by every product). A repo's `@{brand}/ui` holds only **product-specific** components not worth upstreaming yet. Build locally → migrate upstream when reusable.

## Per-app file conventions

- **One component per folder**, camelCase folders, PascalCase files — see [components.md](components.md) / [naming.md](naming.md).
- Ports: the backend is a **single HTTP port** (even) per the [launch-profile rule](../backend/runtime/launch-profiles.md); the frontend dev server (HTTPS via mkcert) picks any free port.

## See also

- [../repo/repo-structure.md](../repo/repo-structure.md) — where `engineering/codebase/{slug}.frontend-services/` sits
- [styling.md](styling.md) · [state-and-data.md](state-and-data.md) · [components.md](components.md)

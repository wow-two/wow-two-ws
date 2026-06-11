# State & data

*Last updated: 2026-06-10*

## API client — same-origin `/api`

The SPA is served from the .NET host's `wwwroot` in production, so **all API URLs are relative** (`/api/...`). In dev, Vite proxies `/api` to the backend's HTTP launch profile. No base-URL config, no CORS in prod.

```ts
// vite.config.ts — dev proxy to the backend's HTTP (odd) port
export default defineConfig({
  base: '/',                                   // root-relative assets
  plugins: [react(), tailwindcss()],
  server: {
    proxy: { '/api': { target: 'http://localhost:8211', changeOrigin: true } },
  },
});
```

Pair with the launch-profile rule (HTTPS even / HTTP odd) — the proxy targets the **HTTP odd** port.

## Client shape

A thin `fetch` wrapper in `src/api/`:

- **`client.ts`** — `request<T>()` helper + an `api` object of typed methods (`getStatus`, `listServers`, …). Each method documents its route: `/** GET /api/servers — all registered servers. */`.
- **`types.ts`** — request/response DTOs + `ProblemDetails` (RFC 7807).
- **`ApiError`** — a typed `Error` carrying `status` + parsed `ProblemDetails`; the client throws it on non-2xx and on network failure (status `0`). Components/hooks catch it for messaging.
- Handle `204` / empty bodies (return `undefined as T`); set `Accept: application/json` and `Content-Type` only when there's a body.

```ts
/** Error carrying the server's RFC 7807 detail (or a transport-level message). */
export class ApiError extends Error {
  readonly status: number;
  readonly problem: ProblemDetails | null;
}
```

## State management

| Concern | Choice |
|---|---|
| Local UI state | `useState` / `useReducer` |
| Shared app state | **React Context + hooks** — no Redux/Zustand |
| Server data | a `use{Resource}` data hook owning fetch + mapping (see [hooks.md](hooks.md)) |
| Persistence | `localStorage`, namespaced key `{brand}:{app}:{feature}` |
| View routing | URL hash (lightweight apps) — see gap note on routing in [frontend-conventions.md](frontend-conventions.md) |

- Fetch inside hooks, not components; abort on unmount with `AbortController`.
- Map DTO → domain model at the hook boundary (see [models.md](models.md)); never leak raw DTOs into the view tree.

## See also

- [hooks.md](hooks.md) — data-fetching hooks
- [models.md](models.md) — DTO ↔ domain mapping
- [../backend/api-endpoints.md](../backend/api-endpoints.md) — the `ApiResponse<T>` / `Problem()` shapes this consumes

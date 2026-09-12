# Dev server

*Last updated: 2026-08-19*

> How an app is served in development — the Vite config, its HTTPS certificate, and the `/api` proxy.
> Purpose — the frontend reaches the backend over the same origin in dev as in production, so no code branches.
> Use case — standing up a new app's `vite.config.ts`, or previewing a route behind the auth gate.

## HTTPS

- must serve HTTPS through `vite-plugin-mkcert`, on an even port
  (ledger: [ports](../../../../../deployment/hosting/ports.md)).
- must gate mkcert behind `VITE_HTTPS=false` for a headless HTTP fallback, with a matching `*-http` launch
  config; normal dev stays HTTPS.

---

## The `/api` proxy

The client calls relative URLs and never configures a base URL
([state and data](../../../core/mla/domains/data/state-and-data.md) § *API client*); the proxy is what makes that
true in dev.

- must proxy `/api` to the backend's **HTTPS (even) port** with `secure: false` for loopback development — the .NET dev cert is
  self-signed — never to the HTTP port.
- must set `base: '/'` so assets resolve root-relative, matching the `wwwroot` host in production.

```ts
// vite.config.ts — dev proxy to the backend's HTTPS (even) port
export default defineConfig({
  base: '/',                                   // root-relative assets
  plugins: [vue(), tailwindcss()],
  server: {
    // secure:false → accept the .NET dev self-signed cert
    proxy: { '/api': { target: 'https://localhost:8210', changeOrigin: false, secure: false } },
  },
});
```

---

## Previewing

- must drive an agent preview through that `*-http` config, verify the affected viewport and keyboard states, then stop it — the
  human reviews in their own browser. Mocks and design render inline instead, with no server.
- must run the backend and its database before previewing an app route behind the auth gate.

---

## Neighbours

- [platform](platform.md) — the vector this doc sits in
- [styling](styling.md) — the other half of the Vite config: the Tailwind plugin and the token import
- [state and data](../../../core/mla/domains/data/state-and-data.md) — the client the proxy stands behind

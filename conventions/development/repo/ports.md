# Port Ledger

*Last updated: 2026-06-12*

> Single source of truth for allocated dev ports — **check here before picking one** to avoid collisions.
> Backend rule: **single `http` port** per service (even number; no TLS in dev — terminated upstream in prod) — see [backend/launch-profiles.md](../backend/runtime/launch-profiles.md). Frontend (Vite) = any free port. (Rows below predating this rule list legacy `https`/`http` pairs.)

## Allocated

| Repo | Service | Port(s) |
|---|---|---|
| secrets-vault | API | 8200 https / 8201 http |
| drydock | API | 8210 https / 8211 http |
| drydock | frontend (Vite) | 5174 |
| smart-qr | API · redirect · frontend | 7020 http · 7022 http · 7025 |
| acquisition-explorer | frontend | 7510 |
| haven | backend services | Auth 7001 · Settings 7003 · Channels.Supply 7005 · Location 7007 · Database 7012 · RenderedContentExtractor 7101 |
| haven | frontends (Vite) | 7501–7507 (crm · admin · channels · map) |
| ventures/prism | frontend (Vite) | 5180 |
| product-template (`Sample` example) | API · Vite | 8220 https / 8221 http · 8225 |

**Next free backend even port: 8230.** Append a row whenever you allocate.

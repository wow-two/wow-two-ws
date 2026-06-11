# Port Ledger

*Last updated: 2026-06-09*

> Single source of truth for allocated dev ports — **check here before picking one** to avoid collisions.
> Backend rule: HTTPS = even, HTTP = odd (even+1) — see [backend/launch-profiles.md](../backend/launch-profiles.md). Frontend (Vite) = any free port.

## Allocated

| Repo | Service | Port(s) |
|---|---|---|
| secrets-vault | API | 8200 https / 8201 http |
| drydock | API | 8210 https / 8211 http |
| drydock | frontend (Vite) | 5174 |
| smart-qr | API · frontend | 7021 · 7025 |
| acquisition-explorer | frontend | 7510 |
| haven | backend services | Auth 7001 · Settings 7003 · Channels.Supply 7005 · Location 7007 · Database 7012 · RenderedContentExtractor 7101 |
| haven | frontends (Vite) | 7501–7507 (crm · admin · channels · map) |
| labs/home-modeler | frontend (Vite) | 5180 |

**Next free backend even port: 8220.** Append a row whenever you allocate.

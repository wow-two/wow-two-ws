# Port Ledger

*Last updated: 2026-06-19*

> Single source of truth for allocated dev ports — **check here before picking one** to avoid collisions.
> Backend rule: a **single `https` profile** binds two ports per service — **HTTPS on the even port, HTTP on the adjacent odd port** (`even`, `even + 1`); TLS terminated upstream in prod — see [backend/launch-profiles.md](../backend/runtime/launch-profiles.md). Frontend (Vite) = an **even** port (HTTPS via mkcert).

## Allocated

| Repo | Service | Port(s) |
|---|---|---|
| secrets-vault | API | 8200 https / 8201 http |
| secrets-vault | frontend (Vite) | 5173 |
| drydock | API | 8210 https / 8211 http |
| drydock | frontend (Vite) | 5174 |
| smart-qr | API | 7020 https / 7021 http |
| smart-qr | redirect | 7022 https / 7023 http |
| smart-qr | frontend (Vite) | 7024 |
| acquisition-explorer | frontend | 7510 |
| haven | backend services | Auth 7001 · Settings 7003 · Channels.Supply 7005 · Location 7007 · Database 7012 · RenderedContentExtractor 7101 |
| haven | frontends (Vite) | 7501–7507 (crm · admin · channels · map) |
| ventures/prism | frontend (Vite) | 5180 |
| product-template (`Sample` example) | API · Vite | 8220 https / 8221 http · 8225 |
| sift | API · Vite | 8230 https / 8231 http · 8226 |
| transcript-forge | API · Vite | 8232 https / 8233 http · 8227 |
| arcade | API · Vite | 8234 https / 8235 http · 8228 |

**Next free backend even port: 8236.** Append a row whenever you allocate.

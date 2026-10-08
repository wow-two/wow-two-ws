# Port Ledger

*Last updated: 2026-09-29*

> Single source of truth for allocated dev ports — **check here before picking one** to avoid collisions.
> Backend rule: a **single `https` profile** binds two ports per service — **HTTPS on the even port, HTTP on the adjacent odd port** (`even`, `even + 1`); TLS terminated upstream in prod — see [backend/launch-profiles.md](../../development/backend/dotnet/shapes/service/platform/startup/launch-profiles.md). Frontend (Vite) = an **even** port (HTTPS via mkcert).

## Allocated

| Repo | Service | Port(s) |
|---|---|---|
| secrets-vault | API | 8200 https / 8201 http |
| secrets-vault | frontend (Vite) | 5173 |
| wheelhouse | API | 8210 https / 8211 http |
| wheelhouse | frontend (Vite) · HTTP preview | 5174 · 5175 |
| wheelhouse | local console + rehearsal rig (loopback) | console 18210 · SSH target 2222 · registry 15000 · vault 18201 |
| forever-pin | API | 7020 https / 7021 http |
| forever-pin | redirect | 7022 https / 7023 http |
| forever-pin | frontend (Vite) | 7024 |
| acquisition-explorer | frontend | 7510 |
| haven | backend services | Auth 7010/7011 · Supply 7012/7013 · Location 7014/7015 · Settings 7016/7017 · Database 7018/7019 |
| haven | frontends (Vite) · compose edge | web 7520 · channels 7522 · admin 7524 · map 7526 · landing 7528 · edge 7530 |
| ventures/prism | frontend (Vite) · studio — Vue rewrite (Vite) | 5180 · 8294 |
| wow-two-sdk-beta.ui (Vue) | playground (Vite) · atlas — layouts, patterns, themes (Vite) | 5176 · 5178 |
| product-template (`Sample` example) | API · Vite | 8220 https / 8221 http · 8225 |
| sift | API · Vite | 8230 https / 8231 http · 8226 |
| 10x-ventures-transcript-forge | API · Vite (Vue) · legacy React Vite | 8232 https / 8233 http · 8274 · 8227 |
| arcade | API · Vite | 8234 https / 8235 http · 8228 |
| museums-gallery | API · Vite | 8236 https / 8237 http · 8229 |
| nth26 | API | 8238 https / 8239 http |
| nth26 | field PWA — rider + driver (Vite) | 8240 |
| nth26 | operator console (Vite) | 8242 |
| nth26 | pitch — solution presentation (Vite) | 8244 |
| nth26 | ideas-iterator frontend (Vite) | 5184 |
| pose-coach | API · Vite (console) | 8258 https / 8259 http · 8272 |
| ocharo-studio | API · Vite | 8260 https / 8261 http · 8262 |
| ocharo-marketing | API · Vite | 8276 https / 8277 http · 8358 |
| ocharo-catalogue | API · Vite | 8278 https / 8279 http · 8282 |
| ocharo-blog | API · Vite | 8280 https / 8281 http · 8284 |
| ocharo-brand | API · Vite | 8286 https / 8287 http · 8288 |
| pbn-studio | API · Vite | 8290 https / 8291 http · 8292 |
| ocharo-motion | API · Vite | 8296 https / 8297 http · 8298 |
| retainer-balance | API · Vite | 8300 https / 8301 http · 8332 |
| documentation-checker | API · Vite | 8302 https / 8303 http · 8334 |
| file-watch | API · Vite | 8304 https / 8305 http · 8336 |
| procedure-review | API · Vite | 8306 https / 8307 http · 8338 |
| training-seats | API · Vite | 8308 https / 8309 http · 8310 |
| epub-review | API · Vite | 8312 https / 8313 http · 8314 |
| customer-promises | API · Vite | 8316 https / 8317 http · 8318 |
| vendor-renewals | API · Vite | 8320 https / 8321 http · 8322 |
| config-checker | API · Vite | 8324 https / 8325 http · 8326 |
| podcast-readiness | API · Vite | 8328 https / 8329 http · 8330 |
| med-text-fab | API · Vite | 8362 https / 8363 http · 8242 |
| home-atlas | API · Vite | 8364 https / 8365 http · 8266 |

| transportbrain (hackathon Track 2 submission) | API | 8246 https / 8247 http |
| tbs.demo | demo — jury-facing solution page, own repo + Vercel (Vite) | 8248 |
| transportbrain | Transport Brain Studio — planner console (Vite) | 8249 |
| tnis-mintrans | ministry handoff cut — API · Vite | 8250 https / 8251 http · 8252 |

| listing-shelf | API · Vite | 8254 https / 8255 http · 8256 |

| brand-workspace | API · Vite · Compose API · PostgreSQL | 8264 https / 8265 http · 8266 · 8268 http / 8269 https · 8270 |
| hijinx | frontend-only static SPA — Vite dev · preview (Playwright) | 5186 · 5187 |

| ocharo-platform review | isolated API · Desk frontend | 8340 https / 8341 http · 8342 |
| ocharo-marketing review | operator frontend | 8344 |

| ocharo-platform review | isolated PostgreSQL | 8346 |

| ocharo-studio review | isolated API · frontend | 8348 https / 8349 http · 8356 |
| ocharo-marketing review | isolated Editorial API · editor frontend | 8350 https / 8351 http · 8352 |
| ocharo-marketing review | isolated Marketing API | 8354 https / 8355 http |
| ocharo-platform image worker review | private loopback HTTP worker | 8360 |

**Next free backend even port: 8366.** Append a row whenever you allocate.

Ocharo Marketing Vite moved from the duplicate `8242` allocation to `8358` on 2026-09-29.
Port `8242` remains owned by the nth26 operator console. Isolated review uses `8344`.

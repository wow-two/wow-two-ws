# Drydock — Product Ops & Deploy Control Plane

*Last updated: 2026-06-09*

> Named **Drydock** (chosen 2026-06-09) — a ship is built, serviced, launched, and repaired from drydock; the portfolio is a fleet of small vessels. Internal platform (not a sellable product) — the control plane for the micro-SaaS portfolio (`ven-msaas-context.md`, target 50–100 launches by EOY 2026). Lives at new org `wow-two-ops` → repo `wow-two-ops.drydock`. Names considered: Hangar, Marina, Mission Control, Shipyard, Launchpad.
> One-liner: *a personal Vercel/Heroku for the whole portfolio — one dashboard to deploy front+back to my VPSs, buy+wire domains, and watch everything stay alive.*

## Section 0: Brief Answers (the questions that spawned this)

- **What is it?** A single dashboard + .NET API that holds every product, every VPS, every domain, and every secret — and turns "ship this product to that server on this domain" into a few clicks. Replaces the pile of manual SSH + registrar tabs + scattered `.env` files that 50–100 products would otherwise need.
- **Push front/back to a VPS?** Yes. Each VPS runs **Docker + Traefik** (reverse proxy, auto-SSL, label-based routing). GitHub Actions builds images → **GHCR**; Launchpad SSHes in (SSH.NET), drops a generated `docker-compose.yml`, runs `docker compose pull && up -d`. Front (React→nginx/static) and back (.NET) are two containers in one stack. Live logs stream to the dashboard. Rollback = re-pin previous image tag. See §3.
- **Search / buy / assign domains in a few clicks?** Yes, via API. **Porkbun** (cleanest buy/search/pricing API, cheap) for registration; **Cloudflare** for DNS + SSL. Flow: search → buy → set nameservers to Cloudflare → create A-record → VPS IP → Traefik picks up the host rule and issues the cert. Caveat: registrar account must be **pre-funded** — "a few clicks" = an API purchase against balance, not a new checkout each time. See §4.
- **Build vs. buy?** Recommend **bespoke** (Docker + Traefik + SSH.NET + GHCR) as primary — it fits the wow-two stack, gives full control, and is itself a flagship internal .NET build. Fast-lane fallback: wrap **Coolify** (open-source self-hosted Vercel; has an API) and make Drydock a thin registry+domains+dashboard layer on top. See §8.

## Section 1: What it manages (5 core domains)

| Domain | Holds | Key actions |
|---|---|---|
| **Products** | name, slug, front/back repo, stack, status, owner, envs | register, scaffold, archive/kill |
| **Servers (VPS)** | host/IP, SSH key ref, Docker info, capacity, what's deployed | add, test connection, health, capacity view |
| **Deployments** | product × server × env, image tags, status, logs, who/when | deploy, rollback, restart, teardown |
| **Domains** | name, registrar, expiry, DNS provider, assigned product | search, buy, point DNS, assign, renew-alert |
| **Secrets** | scope (global/server/product/env), key, encrypted value | set, inject at deploy, rotate, audit |

## Section 2: Architecture & stack

```
┌───────────────────── Drydock control plane ─────────────────────┐
│  React dashboard ──HTTP/SignalR──▶ .NET 9 API (Clean Arch / CQRS)│
│   (@wow-two-beta/ui, Vite)          ├─ Products/Servers/Domains  │
│                                     ├─ Hangfire (deploy jobs)    │
│                                     ├─ Secrets vault (AES@rest)  │
│                                     └─ Postgres                  │
└─────────┬──────────────────┬───────────────────┬────────────────┘
          │ SSH (SSH.NET)    │ REST              │ REST
          ▼                  ▼                   ▼
 ┌────────────────┐  ┌────────────────┐  ┌────────────────┐
 │ VPS (n)        │  │ Registrar API  │  │ Cloudflare API │
 │ Docker+Traefik │  │ (Porkbun)      │  │ DNS + SSL      │
 │ product stacks │  │ search/buy     │  │ A-rec → VPS IP │
 └──────▲─────────┘  └────────────────┘  └────────────────┘
        │ docker pull
 ┌──────┴─────────┐
 │ GHCR images    │◀── GitHub Actions (build on push to main)
 └────────────────┘
```

| Layer | Choice | Why |
|---|---|---|
| Control-plane API | .NET 9, Clean Arch, CQRS (their conventions) | dogfoods wow-two stack |
| Jobs | **Hangfire** (`wow-two-kb.dotnet.jobs`) | deploys are long-running, need retry + dashboard |
| Live logs | **SignalR** | stream stdout of deploy/build to the console widget |
| Remote exec | **SSH.NET** (Renci.SshNet) | run `docker compose`, scp files; transparent + loggable |
| Per-VPS runtime | **Docker + Traefik** | multi-product/host, label routing, auto Let's Encrypt SSL |
| Images | **GHCR** + GitHub Actions | reuse `wow-two-platform.pipelines`; platform orchestrates, doesn't build |
| DB | **Postgres** | registry + deploy history + audit |
| Dashboard | **React + Vite + `@wow-two-beta/ui`** | their beta UI lib |
| Domains | **Porkbun API** (buy) + **Cloudflare API** (DNS/SSL) | best programmatic registrar + free DNS w/ great API |

**Ecosystem fit:** its own repo `wow-two-ops.drydock` under new org `wow-two-ops` (it manages the other repos, so it sits above them). Split `.drydock.api` / `.drydock.web` later. Not a `platform.*` lib — it's an app.

## Section 3: Deploy flow (the core mechanic)

1. Push to `main` → GitHub Actions builds `…-web` + `…-api` images → GHCR (tag = git SHA).
2. Action calls Drydock webhook *(or* user clicks **Deploy** in dashboard*)*.
3. Drydock queues a Hangfire job for `product × server × env`.
4. Job: render `docker-compose.yml` from template (image tags, Traefik labels with the assigned domain, injected secrets as env) → scp to VPS → `docker compose pull && up -d`.
5. Traefik auto-detects the new container's host label → routes the domain → issues/renews SSL.
6. Health check hits `/health`; status + streamed logs land in the dashboard. **Rollback** = redeploy previous SHA tag (one click).

**Per-product compose stack:** `web` (static React behind nginx or Traefik) + `api` (.NET) + optional `db`/`redis`. All labelled for Traefik. Per-product datastores provisioned as containers or a DB-per-product on a shared Postgres (see §7).

## Section 4: Domain flow

1. **Search** — Porkbun `domain/check` (availability + price) from the dashboard search box.
2. **Buy** — Porkbun register against pre-funded balance; record name, cost, expiry in Domains.
3. **DNS** — set nameservers → Cloudflare; Cloudflare API creates **A-record → VPS IP** (and `www` CNAME).
4. **Assign** — link domain → product/env; next deploy writes the Traefik `Host()` rule; Traefik issues the cert. Live in ~1–2 min (DNS prop).
5. **Renew/expiry** — track expiry, auto-renew flag, alert N days out (§7).

SSL options: **Traefik + Let's Encrypt** (DNS-only / grey-cloud Cloudflare) is simplest. Upgrade to Cloudflare proxied (CDN/DDoS) with DNS-01 challenge later.

## Section 5: Data model (entities)

| Entity | Key fields |
|---|---|
| `Product` | id, slug, name, repoWeb, repoApi, stack, status(active/paused/killed), createdAt |
| `Server` | id, name, host, ip, sshUser, sshKey→`Secret`, dockerVersion, cpu/ram, region |
| `Environment` | id, productId, name(prod/staging), domainId, vars[] |
| `Deployment` | id, productId, serverId, envId, imageWebTag, imageApiTag, status, log, triggeredBy, at |
| `Domain` | id, name, registrar, purchasedAt, expiresAt, autoRenew, dnsProvider, assignedEnvId, status |
| `Secret` | id, scope(global/server/product/env), refId, key, valueEnc, updatedAt |
| `AuditEntry` | id, actor, action, target, at |

## Section 6: Secrets & security (this box holds the keys to the kingdom)

- Stores **VPS root SSH keys, registrar billing API, Cloudflare token, GHCR PAT** → highest-value target in the whole portfolio. Treat accordingly.
- **At rest:** AES column encryption (EF Core value converter), key from env/user-secrets → upgrade to **Infisical / Doppler / Vault**.
- **SSH:** keys not passwords; least-privilege deploy user on each VPS (not root) where possible.
- **Scoped tokens:** Cloudflare token limited to the zones it manages; GitHub token scoped to GHCR read + repo.
- **Platform exposure:** do **not** put the dashboard on the public internet. Behind **Tailscale** / Cloudflare Access / IP allowlist + single-admin GitHub OAuth.
- **Audit log** on every deploy, secret change, domain purchase.

## Section 7: Feature backlog (what else we need)

| # | Feature | Tier | Note |
|---|---|---|---|
| 1 | Deploy front+back to VPS + rollback | **must** | core ask #1 |
| 2 | Domain search/buy/assign | **must** | core ask #2 |
| 3 | Secrets vault + env injection | **must** | unblocks 1 & 2 |
| 4 | Live deploy/build logs (SignalR) | **must** | trust the box did what you clicked |
| 5 | Health/uptime monitoring + **Telegram alerts** | should | ties to `telegram-features.md`; calm ops |
| 6 | Domain + SSL **expiry alerts** | should | a dead domain = a dead product |
| 7 | Per-product **managed datastores** (Postgres/Redis) + scheduled **backups** | should | every SaaS needs a DB + backups |
| 8 | **Cost per product** (domain + VPS share) | should | feeds kill-gates + financial domain |
| 9 | **0→live scaffold** — template repo → GitHub API create repo → CI → domain → first deploy | should | the portfolio accelerator for 50–100 launches |
| 10 | **Teardown/kill** — stop stack, final backup, archive repo, release/expire domain | should | executes the micro-SaaS **kill gates** cleanly |
| 11 | Capacity/placement view — which VPS has room | later | bin-pack products across servers |
| 12 | **VPS provisioning** — **Hetzner Cloud API** spin-up + **cloud-init** bootstrap (Docker+Traefik on first boot) | later | one-click new server — Hetzner makes it a single API call |
| 13 | Privacy-friendly **analytics** auto-wire (Plausible/Umami) | later | fits **GWDNBM** — no creepy tracking |
| 14 | Staging/preview environments per product | later | branch deploys |
| 15 | Stack **presets** (React+.NET+Postgres defined once, reused) | later | consistency across the portfolio |

## Section 8: Build vs. wrap

| | **Bespoke** (recommended) | **Wrap Coolify/Dokku** (fast lane) |
|---|---|---|
| Deploy substrate | Docker + Traefik + SSH.NET, you own it | Coolify owns deploy/SSL/DBs; you call its API |
| Effort to v1 | higher | much lower |
| Control / learning | full; flagship .NET build | limited to what the API exposes |
| Verdict | go here for the real platform | use to validate flow / as fallback if §3 stalls |

Either way, the **registry + domain-buying + unified dashboard + cost/kill-gate layer is bespoke** — that's the actual value-add; deployment is the commodity underneath.

## Section 9: Phasing

- **P0 — Foundations:** Product + Server registries, Secrets vault, "add VPS → test SSH/Docker."
- **P1 — Deploy (ask #1):** Docker+Traefik runtime, GHCR pull, one-click deploy front+back, live logs, rollback.
- **P2 — Domains (ask #2):** Porkbun buy/search + Cloudflare DNS + assign → Traefik route + SSL.
- **P3 — Ops:** uptime + Telegram alerts, expiry alerts, datastores + backups, cost tracking.
- **P4 — Accelerate:** 0→live scaffold, teardown/kill-gate automation, capacity view, VPS provisioning.

## Section 10: Open questions

1. **Name** — ✅ **Drydock** (chosen 2026-06-09).
2. **Registrar** — Porkbun (best API) vs Namecheap (familiar, stricter API: IP whitelist + min spend)?
3. **Build vs wrap** — bespoke Docker+Traefik (own it) vs Coolify-as-substrate (ship faster)?
4. **VPS reality** — provider = **Hetzner Cloud** ✅ (full REST API + cloud-init provisioning, §7 #12). Open: how many servers now? Decides multi-server priority.
5. **One big VPS vs one-per-product** — bin-pack many products per host (cheaper, Traefik shines) vs isolation per product?
6. **CI ownership** — build in GitHub Actions (recommended, reuse pipelines) vs build inside Drydock on a runner?

# Self-Host Supabase — Quick Start

*Last updated: 2026-03-01 12:00 PM*

## 1. Get a VPS

Any $10-20/mo box works — Hetzner, DigitalOcean, Contabo. Minimum 2GB RAM, 2 vCPU.

## 2. Clone & Configure

```bash
git clone --depth 1 https://github.com/supabase/supabase
cd supabase/docker
cp .env.example .env
```

## 3. Edit `.env` — Change These

```env
POSTGRES_PASSWORD=<strong-password>
JWT_SECRET=<random-40-char-string>
ANON_KEY=<generate-from-jwt-secret>
SERVICE_ROLE_KEY=<generate-from-jwt-secret>
DASHBOARD_USERNAME=admin
DASHBOARD_PASSWORD=<strong-password>
```

Generate JWT keys at `https://supabase.com/docs/guides/self-hosting#api-keys`

## 4. Launch

```bash
docker compose up -d
```

- Studio dashboard → `http://your-ip:8000`
- API → `http://your-ip:8000/rest/v1/`

## 5. Multiple Projects Strategy

Since one instance = one Postgres, use schemas for isolation:

```sql
CREATE SCHEMA project_alpha;
CREATE SCHEMA project_beta;
```

Each schema gets its own tables, RLS policies, and PostgREST exposure.

## 6. Maintenance Cheat Sheet

| Task | Command |
|---|---|
| Update | `git pull && docker compose pull && docker compose up -d` |
| Backup | `docker exec supabase-db pg_dumpall -U postgres > backup.sql` |
| Logs | `docker compose logs -f` |
| Stop | `docker compose down` |

## Key Gotcha

Schema-based isolation shares one auth system. If you need separate auth per project, run multiple Supabase instances on different ports — but that eats more RAM (~500MB per instance).

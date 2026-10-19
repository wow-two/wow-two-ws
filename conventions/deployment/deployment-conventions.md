# Conventions — Deployment

*Last updated: 2026-10-19*

> How we ship & host what we build — the runtime home of a deployable. Lookup table, not auto-loaded.
> Currently: hosting (serving model, dev-port ledger, domains), server lifecycle and the deployment descriptor.

| Area | Covers |
|---|---|
| [hosting/](hosting/hosting.md) | How a product is served & where it binds — single-host SPA-in-backend serving · dev-port ledger · environment files · domains |
| [servers/](servers/server-lifecycle.md) | A VPS from purchase to retirement — order · bootstrap · tailnet · runner key · platform · products · backups · move · retire |
| [descriptor/](descriptor/deploy-descriptor.md) | What a product deploys — `deploy.yml` services, per-service builds and change paths, sites, service versions, candidate builds, release flow (`main` → dev → prod) · [JSON Schema](descriptor/deploy.schema.json) |

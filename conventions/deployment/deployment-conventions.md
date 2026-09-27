# Conventions — Deployment

*Last updated: 2026-09-27*

> How we ship & host what we build — the runtime home of a deployable. Lookup table, not auto-loaded.
> Currently: hosting (serving model + dev-port ledger) and the deployment descriptor (services, builds, sites, versions).

| Area | Covers |
|---|---|
| [hosting/](hosting/hosting.md) | How a product is served & where it binds — single-host SPA-in-backend serving · dev-port ledger |
| [descriptor/](descriptor/deploy-descriptor.md) | What a product deploys — `deploy.yml` services, per-service builds and change paths, sites, service versions, candidate builds · [JSON Schema](descriptor/deploy.schema.json) |

# Deployment descriptor — rationale

*Last updated: 2026-10-01*

> Why `deploy.yml` is a house format rather than an adopted one. The rules live in the
> [deployment descriptor](deploy-descriptor.md).

## Formats compared

| Format | Covers | Misses for us |
|---|---|---|
| Docker Compose (+ `x-` keys) | service runtime, builds, volumes, networks | change paths, named sites, versions |
| Kamal `deploy.yml` | builder, proxy host and port, accessories | one app image per file; hosts and secrets inside |
| Render `render.yaml` | many services, build filter paths, health path, domains | platform runtime; domains beside the code |
| Fly `fly.toml` | build, internal port, checks, mounts | one app per file |
| Score `score.yaml` | platform-neutral workload and resource dependencies | one workload per file; no builds or change paths |

---

## Sources

- per-service build recipe — Kamal.
- change paths — Render's build filters.
- declared dependencies — Score.
- runtime vocabulary — Compose; the generator writes Compose from the descriptor, so no product hand-writes the
  deployed `compose.json`.

# Deployment descriptor — rationale

*Last updated: 2026-10-28*

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

---

## Migrate step

Reasoning per point in the [migrations analysis](../../../ideas/migrations-analysis-2026-10/migrations-analysis-2026-10.md).

- a product-level `migrate:` list, not a key per service: a set may be read by several services and hosted by one
  image, so the step belongs to sets, not to one service's wave (M9, M43).
- every item before the first wave: a sibling reading the same set never restarts onto a pending schema (M14).
- a pinned image as a service: a per-product instance shares the product's database, snapshot and release (M77).
- `extensions:` in the descriptor: an untrusted extension needs a superuser, which only placement has (M41).

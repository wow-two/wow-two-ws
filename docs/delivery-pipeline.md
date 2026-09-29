# WoW 2.0 — Delivery pipeline

*Last updated: 2026-09-29*

> How every product goes from a push to a deployable, versioned build: the version shape, the planning tracks, the
> build trigger, the artifact store and the shared CI. Analysis with open points, ordered parent before child: a later
> point assumes the earlier answers. Each decided point moves into its convention; this doc keeps only what is open.
> Related: [platform apps](platform-apps.md) (Wheelhouse #1, Pipelines #7) ·
> [deploy descriptor](../conventions/deployment/descriptor/deploy-descriptor.md) ·
> [versioning](../conventions/development/repo/versioning/versioning.md) ·
> [version track](../conventions/planning/version-track/version-track.md).

## Today

| Concern | State on 2026-09-29 |
|---|---|
| Version source | `v{X.Y}` version docs (Feature odd, Adoption even); code carries `X.Y.Z` in `Directory.Build.props` and `package.json`, `Z` bumped by hand |
| Other tracks | Rough `r{X.Y}` and polish `p{X.Y}` number themselves; neither number reaches code or images |
| Release | A published `vX.Y.Z` GitHub release builds the changed services, tags them `X.Y.Z` and attaches the bundle |
| Candidate | Every push builds the changed services as `sha-<commit>`, shown as `<last release>+<commit>`; the bundle is a 14-day Actions artifact |
| Service version | The release in which the service last changed, derived by `release.py` from change paths |
| Registry | GHCR, one repository per service (`ghcr.io/<owner>/<repo>/<service>`); free under GitHub's current policy |
| Generator | `release.py` lives in Wheelhouse; each product's workflow fetches it by git blob and SHA-256 |
| Shared CI | None: every product copies its workflow; `wow-two-platform.pipelines` is an empty public repository |
| SDKs | Beta-forever: CI bumps the patch on every push to `main` and publishes |

---

## Points

- [x] D1 — Version shape
- [x] D2 — One track
- [x] D3 — Release trigger and branch builds
- [x] D4 — Version source
- [x] D5 — Artifact store
- [x] D6 — Bundles and retention
- [x] D7 — Shared CI home
- [ ] D8 — Access and visibility
- [ ] D9 — Build runners and platforms
- [ ] D10 — Supply chain
- [ ] D11 — Rollout order
- [ ] D12 — Base image refresh

---

### D1 — Version shape

Decided 2026-09-29: `X.Y.Z`; CI assigns `Z`; each service keeps the version it last changed in.
Now in [versioning](../conventions/development/repo/versioning/versioning.md).

### D2 — One track

Decided 2026-09-29: no polish releases; polish iterations fold into version docs, and the polish track convention
goes. Worked out in [one version track](version-track-consolidation.md).

### D3 — Release trigger and branch builds

Decided 2026-09-29: `main` releases; optional `dev` / `test` branches replace their builds under `dev-latest` /
`test-latest`; other branches build 14-day candidates. Now in the
[deploy descriptor](../conventions/deployment/descriptor/deploy-descriptor.md) § *Builds and versions* and the
[branching strategy](branching-strategy.md#product-repos).

### D4 — Version source

Decided 2026-09-29: `X.Y` comes from the newest `version-track/v{X.Y}/` folder; CI injects `X.Y.Z` into every build;
local builds report `dev`. Now in [versioning](../conventions/development/repo/versioning/versioning.md).
Hand-declared versions had drifted: ForeverPin v0.11 vs `package.json` `0.0.0`, Haven v1.2 vs `1.1.0`,
TranscriptForge v0.8 vs `0.7.0`.

### D5 — Artifact store

Decided 2026-09-29: GHCR stays the registry; our own code owns the catalog, versions and retention. Now in the
[deploy descriptor](../conventions/deployment/descriptor/deploy-descriptor.md) § *Artifacts and retention*.

- Deferred: a self-hosted registry (Zot first; Harbor if scanning and RBAC matter). Triggers: GHCR billing notice,
  private images across many targets, pull latency.
- Sizing for that day, measured on ForeverPin `sha-a4d8490`: ~175 MB per service image, ~100 MB of it the shared .NET
  base, ~75 MB the app layer each rebuild replaces; 10 releases × 100 services ≈ 75 GB.

### D6 — Bundles and retention

Decided 2026-09-29: bundles kept for good; deployed digests, rollback sets and the last 10 releases per service kept;
`dev` / `test` keep their newest build; candidates expire after 14 days; Wheelhouse owns deletion. Now in the
[deploy descriptor](../conventions/deployment/descriptor/deploy-descriptor.md) § *Artifacts and retention*.

- Open in implementation: bundles as OCI artifacts beside the images, and a dependency image layer so a rebuild
  adds a few MB instead of ~75 MB.

### D7 — Shared CI home

Decided 2026-09-29: `wow-two-platform.pipelines` holds the reusable publish workflow and, moved from Wheelhouse, the
release generator; each product keeps a small caller pinned to a pipelines tag. It serves every Docker setup,
because each product's `deploy.yml` names its services' Dockerfiles, targets, arguments and build contexts.

### D8 — Access and visibility

- Public or private product repositories, per product.
- Image visibility and target pull credentials, which depend on D5.
- Which tokens Wheelhouse holds: catalog read, build dispatch, registry pull.
- Needs: D5, D7.

### D9 — Build runners and platforms

- GitHub-hosted `linux/amd64` runners are free for public repositories; private ones spend the free minutes.
- `linux/arm64` hosts (cheaper Hetzner CAX) need arm64 runners or emulated builds.
- A self-hosted runner on the control host, never on a target host.
- Needs: D7.

### D10 — Supply chain

- Image signing (cosign), SBOM (syft) and vulnerability scanning (Trivy) in the shared workflow.
- Defer until a trigger: the first product that holds paying customers' data.
- Needs: D7.

### D11 — Rollout order

- ForeverPin, then Wheelhouse, then Secrets Vault, then every product through `create-repo`.
- Retire each product's copied workflow once it calls the shared one.
- Needs: D1–D9.

### D12 — Base image refresh

- Changed-only builds leave an unchanged service on its old base image, so it misses .NET runtime patches.
- Pin base images by digest; a bump (by hand, Dependabot or Renovate) changes the Dockerfile, which rebuilds every
  service that uses it.
- Or rebuild every service on a schedule, which releases services that did not change.
- Needs: D7.

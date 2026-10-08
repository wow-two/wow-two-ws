# Deployment descriptor

*Last updated: 2026-10-01*

> One file per product repo, `engineering/deployment/deploy.yml`, declaring its deployable services: how each
> builds, which paths change it, how it runs, which sites it serves and what it needs.
> Purpose — one source for CI, the release generator and Wheelhouse; environments, hosts and secrets stay out.
> Use case — every product repo deployed through Wheelhouse; the product template ships one.

Why a custom format → [rationale](deploy-descriptor-rationale.md).

---

## Rules

- must place the file at `engineering/deployment/deploy.yml`, one per product repo.
- must hold only product-owned facts. Hostnames, secrets, servers and environments belong to Wheelhouse targets.
- must build every image environment-free: no environment values at build time.
- must let an SPA read its public settings at runtime, never from build-time variables
  ([known endpoints](../../development/backend/dotnet/shapes/service/platform/responses/known-endpoints.md)
  § *Runtime config*).
- a settings change is a commit, so it builds a new image; an operator setting changes only the target.
- must give every service a health check; the runner refuses a service without one.
- must point a backend service's health check at the boot bundle's `/health`
  ([startup defaults](../../development/backend/dotnet/shapes/service/platform/startup/startup-defaults.md#health)).
- must list the paths that change each service; a `shared` path rebuilds every service.
- must declare public entry points as named `sites`; every other port stays internal.
- must not publish host ports; the ingress routes each site by hostname.
- should publish one image per service at `ghcr.io/<owner>/<repo>/<service>`; `image` overrides a legacy name.
- must keep the product slug equal to the Wheelhouse runner product (`foreverpin`, not `forever-pin`).

---

## Format

Paths are relative to the repo's `engineering/` folder. `**` crosses folders; `*` and `?` stay inside one.

```yaml
# yaml-language-server: $schema=<path to wow-two-ws>/conventions/deployment/descriptor/deploy.schema.json
descriptor: 1                         # format version
product: haven                        # runner product slug
platform: linux/amd64                 # default; or linux/arm64
shared:                               # a change here rebuilds every service
  - codebase/haven.backend-services/Directory.*.props
  - deployment/backend.Dockerfile
services:
  auth:                               # service slug = Compose service = image name
    build:
      dockerfile: deployment/backend.Dockerfile
      context: codebase               # default
      # target: <stage>               # optional multi-stage target
      args: { SERVICE: Auth }         # optional
      contexts: { deployment: deployment }   # optional named build contexts
    paths:
      - codebase/haven.backend-services/Haven.Auth/**
    port: 8080                        # default 8080
    health: /health                   # HTTP path probed with curl inside the container
    memory: 512m                      # default 512m
    stopGrace: 30s                    # default 30s
    settings:                         # the service's private settings file, filled per environment
      file: /app/appsettings.Local.json   # default
      required: [DatabaseOptions:ConnectionString, AllowedHosts]
    volumes:
      keys: /data/keys                # named volume → mount path, scoped to the environment
    needs: [postgres]                 # postgres | valkey | broker
  edge:
    build: { dockerfile: deployment/edge.Dockerfile, contexts: { deployment: deployment } }
    paths: [codebase/haven.frontend-services/**, deployment/edge/**]
    port: 80
    health: { command: [wget, -q, -O-, http://localhost/healthz] }   # when the image has no curl
    capabilities: [NET_BIND_SERVICE]  # added back after the default drop of all capabilities
    sites:
      landing: {}                     # port defaults to the service port, path to /
      crm: { path: / }
      admin: { exposure: private }    # answers only on the private network
```

| Key | Default | Meaning |
|---|---|---|
| `descriptor` | — | Format version; `1` |
| `product` | — | Runner product slug |
| `platform` | `linux/amd64` | Build and run platform |
| `shared` | `[]` | Paths whose change rebuilds every service |
| `services.<name>.image` | `<registry>/<name>` | Image repository without a tag, for a legacy name |
| `services.<name>.build` | — | `dockerfile` (required), `context`, `target`, `args`, `contexts` |
| `services.<name>.paths` | — | Paths whose change rebuilds this service; its Dockerfile always counts |
| `services.<name>.port` | `8080` | The port the service listens on |
| `services.<name>.health` | — | An HTTP path, or `{ command: [...] }` |
| `services.<name>.memory` · `stopGrace` | `512m` · `30s` | Container memory limit and stop grace |
| `services.<name>.settings` | none | `file` mount target and the `required` keys the runner checks before deploying |
| `services.<name>.volumes` | `{}` | Named volume → absolute mount path |
| `services.<name>.sites` | `{}` | Site name → `port`, `path` prefix, `exposure` (`public` \| `private`) |
| `services.<name>.needs` | `[]` | Platform services consumed: `postgres`, `valkey`, `broker` |
| `services.<name>.capabilities` | `[]` | Linux capabilities added back after `cap_drop: ALL` |

- Two services may share a site name only with different path prefixes; the longer prefix wins.
- Every service runs with `no-new-privileges`, all capabilities dropped, an init process, bounded logs and a restart policy.
- Each service answers on the platform network as `<product>-<environment>-<service>`; the ingress routes sites there.
- Wheelhouse targets map site names to hostnames: prod names each one, dev and test follow a host pattern.

---

## Builds and versions

A product version is `X.Y.Z`: `X.Y` is the newest version-track folder
([versioning](../../development/repo/versioning/versioning.md)); CI assigns `Z`. A service carries the product
version in which it last changed, so services version independently and an old version means no change since.

| Built from | Version | Image tags | Deploys to | Kept |
|---|---|---|---|---|
| `main` | `X.Y.Z`, the next `Z` | `X.Y.Z`, `latest` | dev, test, prod | for good: a release |
| `test` | `X.Y.(Z+1)-test.<n>` | `test-latest` | dev, test | until the next `test` build |
| `dev` | `X.Y.(Z+1)-dev.<n>` | `dev-latest` | dev | until the next `dev` build |
| any other branch, or a dispatched commit | `X.Y.(Z+1)-<branch>.<n>` | `sha-<commit>` | dev | 14 days |

- `Z` is the highest `vX.Y.*` tag plus one, so no version-bump commit lands in history; `Z` restarts at 0 on a new `X.Y`.
- A `main` build releases only when a service or the descriptor changed; a docs-only push releases nothing.
- A descriptor-only change releases a new bundle that reuses every image.
- `<n>` counts the branch's commits since it left `main`, so one commit always gets the same version.
- `<branch>` is the branch name made tag-safe (`feat/login` → `feat-login`); a pre-release sorts below its release.
- A service changed when a path in its `paths`, `shared` or its Dockerfile differs from the previous release's commit.
- Moving tags (`latest`, `test-latest`, `dev-latest`) name the newest build of their branch, never what an environment
  runs; Wheelhouse records that, and deploys only digest-pinned images.
- dev, test and prod are environments; `dev` and `test` branches are optional, and a product without them builds
  every other branch as a candidate.
- The release generator is `generator/release.py` in `wow-two-platform.pipelines`; it needs Python 3.9+ with
  PyYAML, Git and Docker Buildx.
- `release.py plan` prints what builds and every service's version; `release.py build` builds, pushes and writes
  the bundle.
- CI checks out the full history (`fetch-depth: 0`), so the generator can diff against the previous release.

---

## Artifacts and retention

- Images live in GHCR, one repository per service; container storage and bandwidth are free under GitHub's current
  policy, with a month's notice before any change.
- A self-hosted registry waits for a trigger: GHCR billing, private images across many targets, or pull latency.
- A bundle is about 2 KB, so every release bundle is kept for good.
- Keep every deployed digest and each target's rollback set, and the last 10 release images per service.
- Keep only the newest `dev` and `test` builds; other candidates expire after 14 days.
- Wheelhouse owns deletion, because only it knows what each target runs.

---

## CI workflow

- must keep `.github/workflows/publish-docker-image.yml` as the marker file Wheelhouse detects.
- must call the shared `publish.yml` workflow of `wow-two-platform.pipelines` from it, pinned to a tag.
- must trigger it on every push and on `workflow_dispatch` with a `commit` input.
- must not copy the publish steps or the release generator into a product repo.

```yaml
jobs:
  publish:
    uses: wow-two-platform/wow-two-platform.pipelines/.github/workflows/publish.yml@v0.1.0
    with:
      commit: ${{ inputs.commit }}
```

The shared workflow:

- builds on every push: `main` releases, `dev` and `test` replace their builds, other branches build candidates;
- builds a dispatched commit that has no build yet (Wheelhouse's Build action);
- builds each changed service from `deploy.yml`, whatever its Dockerfile, target, arguments or build contexts;
- tags and publishes images and the bundle per the table above, and moves the branch's tag last.

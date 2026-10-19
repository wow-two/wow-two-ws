# Deployment descriptor

*Last updated: 2026-10-19*

> One file per product repo, `engineering/deployment/deploy.yml`, declaring its deployable services: how each
> builds, which paths change it, how it runs, which site paths it serves and what it needs.
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
- must list every setting a service needs under `settings.required`, or as `required` under `settings.keys`; the
  runner refuses a deploy missing one. Wheelhouse derives some and asks for the rest on a first deploy
  ([settings at deploy](#settings-at-deploy)).
- should type its keys under `settings.keys` ([typed keys](#typed-keys)): Wheelhouse checks each value against its type
  when the owner saves it, offers a choice's values, and keeps a `secret` in its vault.
- should name a secret setting so its last part reads as one (`Key`, `Secret`, `Password`, `Token`,
  `ConnectionString`), or declare it `secret: true`: Wheelhouse then keeps its value in its vault, never in its settings
  store, and refuses it as a plain setting unless the owner confirms.
- must give every service a health check; the runner refuses a service without one.
- must point a backend service's health check at the boot bundle's `/health`
  ([startup defaults](../../development/backend/dotnet/shapes/service/platform/startup/startup-defaults.md#health)).
- must list the paths that change each service; a `shared` path rebuilds every service.
- should use `descriptor: 2`; descriptor 1 is deprecated and still reads ([descriptor 1](#descriptor-1-deprecated)).
- must declare the product's entry points as named `sites` and the paths each service serves on each
  ([sites and routing](#sites-and-routing)); every other port stays internal.
- must not name a host, zone, address or proxy setting; Wheelhouse binds each site to one host per environment.
- must not publish host ports; the ingress routes each site by host and path.
- should publish one image per service at `ghcr.io/<owner>/<repo>/<service>`; `image` overrides a legacy name.
- must keep the product slug equal to the Wheelhouse runner product (`foreverpin`, not `forever-pin`).
- should set `dotnetEnvironment: true` once every .NET service's `appsettings.Development.json` holds defaults only
  ([environment files](../hosting/environment-files.md) § *Settings*); the runner then runs dev as `Development`.
- may declare a `verify` check; a product that auto-promotes should, so a release reaches prod only after it.
- may declare `dependsOn` for a service that cannot start before another service of the product is healthy; a
  platform service (postgres, valkey, broker) goes under `needs`, never `dependsOn`.
- a service restarts only when its own image or settings change; a dependency's update never restarts it
  ([rollouts](#rollouts)).

---

## Format

Paths are relative to the repo's `engineering/` folder. `**` crosses folders; `*` and `?` stay inside one.

```yaml
# yaml-language-server: $schema=<path to wow-two-ws>/conventions/deployment/descriptor/deploy.schema.json
descriptor: 2                         # format version
product: haven                        # runner product slug
platform: linux/amd64                 # default; or linux/arm64
shared:                               # a change here rebuilds every service
  - codebase/haven.backend-services/Directory.*.props
  - deployment/backend.Dockerfile
dotnetEnvironment: true               # dev runs as .NET Development, prod as Production
verify:                               # the end-to-end check after a dev rollout
  service: auth                       # whose release image runs it
  command: [sh, -c, 'curl --fail --silent --header "Host: localhost" "$VERIFY_SERVICE_AUTH/health"']
  timeout: 5m                         # default 5m; 10s-30m
sites:                                # host roles; Wheelhouse binds each to one host per environment
  crm: { primary: true }              # the front door; public by default
  landing: {}
  admin: { exposure: private }        # answers only on the private network
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
      file: /app/appsettings.Target.json  # default
      required: [DatabaseOptions:ConnectionString, AllowedHosts]
      keys:                           # typed keys (pipelines v0.10.0); a required one joins `required`
        Billing:Mode: { type: choice, values: [test, live], default: test }
        Stripe:ApiKey: { secret: true, required: true }
        Jobs:Cleanup: { type: cron, default: "0 3 * * *" }
    volumes:
      keys: /data/keys                # named volume → mount path, scoped to the environment
    needs: [postgres]                 # postgres | valkey | broker
    sites:
      crm: { paths: [/api, /hubs] }   # the API under the product's own host
      admin: { paths: [/api] }
  edge:
    build: { dockerfile: deployment/edge.Dockerfile, contexts: { deployment: deployment } }
    paths: [codebase/haven.frontend-services/**, deployment/edge/**]
    dependsOn: [auth]                 # starts once auth is healthy; an auth update never restarts it
    port: 80
    health: { command: [wget, -q, -O-, http://localhost/healthz] }   # when the image has no curl
    capabilities: [NET_BIND_SERVICE]  # added back after the default drop of all capabilities
    sites:
      landing: {}                     # paths default to [/], port to the service port
      crm: { paths: [/] }
      admin: {}
```

| Key | Default | Meaning |
|---|---|---|
| `descriptor` | — | Format version: `2`; `1` is deprecated |
| `product` | — | Runner product slug |
| `platform` | `linux/amd64` | Build and run platform |
| `shared` | `[]` | Paths whose change rebuilds every service |
| `dotnetEnvironment` | `false` | The runner sets `ASPNETCORE_ENVIRONMENT` and `DOTNET_ENVIRONMENT`: dev `Development`, prod `Production` |
| `verify` | none | `service`, `command` and `timeout` of the end-to-end check after a dev rollout ([below](#dev-check)) |
| `sites.<site>` | `{}` | A host role; Wheelhouse binds it to one host per environment |
| `sites.<site>.exposure` | `public` | `public` (internet) or `private` (private network) |
| `sites.<site>.primary` | the first site | The front door: Open site, the apex proposal; at most one |
| `sites.<site>.environments` | `[dev, prod]` | The environments that publish the site |
| `services.<name>.image` | `<registry>/<name>` | Image repository without a tag, for a legacy name |
| `services.<name>.build` | — | `dockerfile` (required), `context`, `target`, `args`, `contexts` |
| `services.<name>.paths` | — | Paths whose change rebuilds this service; its Dockerfile always counts |
| `services.<name>.port` | `8080` | The port the service listens on |
| `services.<name>.health` | — | An HTTP path, or `{ command: [...] }` |
| `services.<name>.memory` · `stopGrace` | `512m` · `30s` | Container memory limit and stop grace |
| `services.<name>.settings` | none | `file` mount target (default `/app/appsettings.Target.json`; `/app/appsettings.Local.json` before v0.7.0), the `required` keys the runner checks before deploying, and typed `keys` ([below](#typed-keys)) |
| `services.<name>.volumes` | `{}` | Named volume → absolute mount path |
| `services.<name>.sites.<site>.paths` | `[/]` | The path prefixes the service serves on that site |
| `services.<name>.sites.<site>.port` | the service port | The container port the site reaches |
| `services.<name>.needs` | `[]` | Platform services consumed: `postgres`, `valkey`, `broker` |
| `services.<name>.dependsOn` | `[]` | Services of this product it starts after, once each is healthy; no cycle |
| `services.<name>.capabilities` | `[]` | Linux capabilities added back after `cap_drop: ALL` |

- Every service runs with `no-new-privileges`, all capabilities dropped, an init process, bounded logs and a restart policy.
- Each service answers on the platform network as `<product>-<environment>-<service>`; the ingress routes sites there.
- Every service receives `DEPLOY_ENVIRONMENT` (`dev` or `prod`) from the runner, declared or not.

---

## Sites and routing

A site is a host role: one host per environment, bound by Wheelhouse. The descriptor owns roles, paths and exposure;
Wheelhouse owns hosts, zones and proxying.

- One product per host; a product's API lives under its own host's `/api`.
- Each site path has exactly one service: one service serves `/` per site, and the generator refuses a second claim.
- A path is `/` or `/a/b`: letters, digits and `. _ ~ -` between slashes, no trailing slash, no `.` or `..`.
- The longest prefix wins; `/api` serves `/api` and `/api/…`, never `/apiary`.
- A service may serve several paths of one site; a site may list paths of several services.
- A site without `/` answers 404 outside its paths; `release.py validate` warns.
- A site's `environments` leave it unpublished elsewhere: `environments: [prod]` routes nothing on dev.
- A Wheelhouse binding may narrow a site's exposure (public to private), never widen it.
- Today a target names each site's host, or dev follows the server's host pattern; domain bindings replace both.

How the runner renders them, after a verified rollout, into `<root>/ingress/<product>-<environment>.yml`:

| Site path | Traefik rule | Priority |
|---|---|---|
| `/` | `` Host(`h`) `` | 101 |
| `/api` | `` Host(`h`) && (Path(`/api`) \|\| PathPrefix(`/api/`)) `` | 104 |
| `/api/docs` | `` Host(`h`) && (Path(`/api/docs`) \|\| PathPrefix(`/api/docs/`)) `` | 109 |

- One router per site path, priority 100 plus the path's length, whatever the rule's length.
- Public sites attach to the public entry points, private sites to the private ones.
- Every path of a service shares one upstream, `<product>-<environment>-<service>:<port>`.
- Each service site publishes the URL of its shortest path and is probed there; a site's root comes first.
- `release.json` schema 2 carries `sites` (the roles) and `routes` (each service's `port` and `paths` per site).

### Descriptor 1 (deprecated)

Descriptor 1 declares one path per service site, with its own exposure, and no top-level `sites`:

```yaml
descriptor: 1
services:
  edge:
    sites:
      app: { path: /, exposure: private }   # port defaults to the service port, path to /
```

- It still reads, and its bundles stay `release.json` schema 1, byte for byte.
- The runner routes it the same way: `path: /x` routes as `paths: [/x]`, with that entry's exposure.
- To move: set `descriptor: 2`, list each site under `sites` with its `exposure`, and turn `path: /x` into
  `paths: [/x]`. Pin pipelines `v0.8.0` first.

---

## Rollouts

How Wheelhouse applies a release to a target, service by service.

- `dependsOn` renders as Compose `depends_on` with `condition: service_healthy`, never `restart: true`.
- The runner compares each service with what the target runs: `added`, its `image`, its Compose `definition` (memory,
  health check, mounts), or its `settings` (the settings file's contents, the environment the runner gives it or the
  target's variables). A `dependsOn` change alone changes nothing.
- Only changed services restart, each alone, in dependency waves: a wave starts once the waves it depends on are
  healthy, and an unchanged service keeps running even when a dependency it uses restarts.
- A failing service stops the rollout: later waves never start, and a release that declares `rollbackCompatible`
  rolls back whole, so a target always runs exactly one release.

---

## Settings at deploy

Wheelhouse renders each service's settings file at every deploy, in layers, the last winning:

| Layer | Holds |
|---|---|
| Host file | A file the target still names; the render keeps it as its bottom layer |
| Wheelhouse | The environment's stored settings and its built-in vault secrets |
| Derived | `AllowedHosts` (the hosts of the sites the service serves, its platform name `<product>-<environment>-<service>`, `localhost`), `Sites:<site>:Url` (each published site's origin) and `Deployment:TrustedProxies` (the ingress's address) |
| Database | A required connection key no other layer sets (`ConnectionStrings:<name>`, `<Section>:ConnectionString`), from the target's own database, for a service that `needs: [postgres]` |

- A derived key may sit under `settings.required`; nobody fills it in.
- Every other required key the first deploy asks for, and a deploy waits until each has a value.
- A value goes to each service that requires its key; a key no service requires goes to every service.

### Typed keys

`settings.keys` maps each configuration path to its declaration; every field is optional (`Key: {}` or `Key:` is a
plain text key).

| Field | Default | Meaning |
|---|---|---|
| `type` | `text` | `text`, `number` (`42`, `-0.5`), `boolean` (`true`/`false`), `choice`, `url` (absolute http or https), `cron` (five fields, six with seconds first, or `@daily` and the like), `date`, `email` |
| `required` | `false` | A deploy waits until a layer sets it; it joins `settings.required` |
| `secret` | `false` | Its values live in Wheelhouse's vault, never its settings store |
| `default` | none | An optional plain key's value when no layer sets one; checked against `type`; refused on a secret or a required key |
| `values` | — | A `choice`'s values, 1–50; refused on other types |
| `format` | `yyyy-MM-dd` | A `date`'s format: `yyyy`, `MM`, `dd`, `HH`, `mm`, `ss` and `- . / : T` or space; refused on other types |

- must pin pipelines `v0.10.0` or later to declare `keys`; an older generator refuses it, and the bundle reaches a
  Wheelhouse runner from v0.5 (`settings.<service>.types`), which an older runner refuses.
- A descriptor without `keys` builds bundles byte for byte as before.
- Owners may add keys of their own per product in Wheelhouse's console, typed the same way; a release's declaration
  wins over one the owner added.
- Wheelhouse checks a value against its type on every save, field by field; a deploy applies what is saved.

### Snapshots of file databases

A prod deploy first snapshots the product's PostgreSQL databases and named volumes. A volume holding a file database is
archived while the product's containers that mount it are paused, so the copy is consistent; other volumes are archived
live. No descriptor key marks it: the runner finds a SQLite file by its header, whatever its name, and another embedded
database by its file name (`*.db`, `*.db3`, `*.sqlite`, `*.sqlite3`, `*.litedb`, `*.mdb`, `*.duckdb`, `*.realm`, `*.wt`,
`*.bdb`), so name such files that way.

---

## Dev check

The `verify` check proves a release end to end on dev before it may auto-promote.

- runs once a dev rollout succeeds: the `command` in a one-off container from the `service`'s release image, on the
  platform network, as the image's user, with all capabilities dropped and 512 MB of memory;
- gets `DEPLOY_ENVIRONMENT`, `VERIFY_RELEASE`, `VERIFY_SITES` (a JSON list of `name`, `service`, `exposure`, `url`
  per published service site), `VERIFY_SITE_<SITE>` per published site (its root, else its shortest path) and
  `VERIFY_SERVICE_<SERVICE>` per service (`http://<product>-dev-<service>:<port>`);
  no settings file and no secret;
- must send `Host: localhost` on a `VERIFY_SERVICE_<SERVICE>` request: a service URL's host is the container
  name, which a hand-written `AllowedHosts` may leave out and answer with 400;
- passes on exit 0; any other exit, a run past `timeout` or a check that cannot start fails it;
- must not print a secret: the deployment keeps the check's last output line;
- never changes the rollout's outcome: a failure is a warning on the deployment, and auto-promote holds the release;
- prod never runs it; a manual promote shows its result.

---

## Builds and versions

A product version is `X.Y.Z`: `X.Y` is the newest version-track folder
([versioning](../../development/repo/versioning/versioning.md)); CI assigns `Z`. A service carries the product
version in which it last changed, so services version independently and an old version means no change since.

| Built from | Version | Image tags | Deploys to | Kept |
|---|---|---|---|---|
| `main` | `X.Y.Z`, the next `Z` | `X.Y.Z`, `latest` | dev, then prod | for good: a release |
| any other branch, or a dispatched commit | `X.Y.(Z+1)-<branch>.<n>` | `sha-<commit>` | dev, by hand | 14 days |

- `Z` is the highest `vX.Y.*` tag plus one, so no version-bump commit lands in history; `Z` restarts at 0 on a new `X.Y`.
- A `main` build releases only when a service or the descriptor changed; a docs-only push releases nothing.
- A descriptor-only change releases a new bundle that reuses every image.
- A base release whose source commit left the history (a rewrite) rebuilds every service; the notes warn about it.
- `<n>` counts the branch's commits since it left `main`, so one commit always gets the same version.
- `<branch>` is the branch name made tag-safe (`feat/login` → `feat-login`); a pre-release sorts below its release.
- A service changed when a path in its `paths`, `shared` or its Dockerfile differs from the previous release's commit.
- The moving tag `latest` names the newest release, never what an environment runs; Wheelhouse records that, and
  deploys only digest-pinned images.
- The release generator is `generator/release.py` in `wow-two-platform.pipelines`; it needs Python 3.9+ with
  PyYAML, Git and Docker Buildx.
- `release.py plan` prints what builds and every service's version; `release.py build` builds, pushes and writes
  the bundle.
- CI checks out the full history (`fetch-depth: 0`), so the generator can diff against the previous release.

---

## Release flow

- must work on `main` only and fix forward; no long-lived branch, no `dev` or `test` branch.
- may push a short-lived branch; it builds a candidate that reaches dev only by hand.
- must run two environments per product: `dev` and `prod`.
- must deploy every `main` release to dev automatically.
- must promote that same release to prod by digest; prod never rebuilds and never takes a candidate.
- must refuse a prod deploy of a release that has not succeeded on dev; typing the target's ID overrides.

---

## Artifacts and retention

- Images live in GHCR, one repository per service; container storage and bandwidth are free under GitHub's current
  policy, with a month's notice before any change.
- A self-hosted registry waits for a trigger: GHCR billing, private images across many targets, or pull latency.
- A bundle is about 2 KB, so every release bundle is kept for good.
- Keep every deployed digest and each target's rollback set, and the last 10 release images per service.
- Candidates expire after 14 days.
- Wheelhouse owns deletion, because only it knows what each target runs.

---

## CI workflow

- must keep `.github/workflows/publish-docker-image.yml` as the marker file Wheelhouse detects; it is the product's
  one CI file.
- must call the shared `delivery.yml` workflow of `wow-two-platform.pipelines` from it, pinned to a tag (`v0.9.0` or
  later), and declare the product's checks there; no product `ci.yml` or `verify.yml`. Before `v0.9.0` it called
  `publish.yml` behind its own CI.
- must pin `v0.5.0` or later to declare `dotnetEnvironment` or `verify`, and `v0.6.0` or later to declare
  `dependsOn`; an older generator refuses each key.
- must move to `v0.7.0` together with a be sdk that reads `appsettings.Target.json`: from `v0.7.0` the settings file
  mounts there, not at `/app/appsettings.Local.json`
  ([host configuration](../../development/backend/dotnet/shapes/service/platform/startup/host-configuration.md) § *Settings files*).
- must pin `v0.8.0` or later to declare `descriptor: 2`; an older generator refuses it, and a Wheelhouse runner older
  than descriptor 2 refuses a schema 2 bundle.
- must pin `v0.10.0` or later to type its settings under `settings.keys`; an older generator refuses the key.
- should move the pin to each new pipelines tag; every workflow of a repo that names the generator names one tag.
- must trigger it on every push except `renovate/**` branches, on pull requests, and on `workflow_dispatch` with a
  `commit` input.
- must queue `main` runs in one concurrency group (`queue: max`) and cancel superseded runs on other refs.
- must not copy the publish steps, the CI steps or the release generator into a product repo.
- must give a check `paths` only when every path it reads is listed; a path no check owns runs every check.

```yaml
jobs:
  delivery:
    uses: wow-two-platform/wow-two-platform.pipelines/.github/workflows/delivery.yml@v0.9.0
    with:
      commit: ${{ inputs.commit }}
      backends: |
        [{"name": "Backend", "dotnet": "engineering/codebase/pilot.backend-services/global.json",
          "run": "dotnet test engineering/codebase/pilot.backend-services/Pilot.BackendServices.slnx"}]
```

Full caller and check keys: the pipelines `README.md`. The shared workflow:

- skips a `main` push a newer push has replaced, and builds, tests and publishes nothing for a push that changes only
  docs, planning or markdown since the last delivered commit; its `gate` check still passes;
- runs each declared check whose paths changed, then publishes once they pass; a pull request runs the checks only;
- builds on every code push: `main` releases, every other branch builds a candidate;
- builds a dispatched commit that has no build yet (Wheelhouse's Build action);
- builds each changed service from `deploy.yml`, whatever its Dockerfile, target, arguments or build contexts;
- fetches the Git LFS files under `engineering/` first, so images carry real assets instead of pointer files;
- passes every build `APP_VERSION` (the build's version) and `VCS_REF` (the full commit SHA it was built from);
- tags and publishes images and the bundle per the table above, and moves `latest` last on a release.

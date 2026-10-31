# Deployment descriptor

*Last updated: 2026-10-31*

> One file per product repo, `engineering/deployment/deploy.yml`, declaring the product's identity and its deployable
> services: what the product is called, how each service builds, which paths change it, how it runs, which site paths
> it serves, what it needs and which images migrate its sets.
> Purpose — one source for CI, the release generator and Wheelhouse; environments, hosts and secrets stay out.
> Use case — every product repo deployed through Wheelhouse; the product template ships one.

Why a custom format → [rationale](deploy-descriptor-rationale.md). Point ids (`M9`) cite the
[migrations analysis](../../../ideas/migrations-analysis-2026-10/migrations-analysis-2026-10.md).

---

## Rules

- must place the file at `engineering/deployment/deploy.yml`, one per product repo.
- must hold only product-owned facts. Hostnames, secrets, servers and environments belong to Wheelhouse targets.
- should declare the product's identity: `name`, `description`, and `homepage` when it has a public address
  ([identity](#identity)); it replaced `product/product.json` on 2026-10-27.
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
- may run another repository's published image as a service, pinned by tag ([pinned images](#pinned-images), M77).
- must declare a `migrate:` item for every image that hosts a migration set ([migrate](#migrate), M9).
- must keep the product slug equal to the Wheelhouse runner product (`foreverpin`, not `forever-pin`); every repository
  of a product built from several names that product's slug ([below](#products-of-several-repositories)).
- should set `dotnetEnvironment: true` once every .NET service's `appsettings.Development.json` holds defaults only
  ([environment files](../hosting/environment-files.md) § *Settings*); the runner then runs dev as `Development`.
- may declare a `verify` check; a product that auto-promotes should, so a release reaches prod only after it.
- may declare `dependsOn` for a service that cannot start before another service of the product is healthy; a
  backing service the server provides (postgres, valkey, broker) goes under `needs`, never `dependsOn`.
- a service restarts only when its own image or settings change; a dependency's update never restarts it
  ([rollouts](#rollouts)).

---

## Format

Paths are relative to the repo's `engineering/` folder. `**` crosses folders; `*` and `?` stay inside one.

```yaml
# yaml-language-server: $schema=<path to wow-two-ws>/conventions/deployment/descriptor/deploy.schema.json
descriptor: 2                         # format version
product: haven                        # runner product slug
name: Haven                           # display name (identity, pipelines v0.11.0)
description: Listings, leads and clients for a realtor.
homepage: https://haven.example       # optional public address
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
    name: Accounts                    # optional display name and one line (identity)
    description: Sign-in and accounts.
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
| `name` · `description` | none | The product's display name (1–80 characters) and one line on what it does (1–200), declared together ([identity](#identity)) |
| `homepage` | none | The product's public `http` or `https` address, at most 300 characters |
| `platform` | `linux/amd64` | Build and run platform |
| `shared` | `[]` | Paths whose change rebuilds every service |
| `dotnetEnvironment` | `false` | The runner sets `ASPNETCORE_ENVIRONMENT` and `DOTNET_ENVIRONMENT`: dev `Development`, prod `Production` |
| `verify` | none | `service`, `command` and `timeout` of the end-to-end check after a dev rollout ([below](#dev-check)) |
| `migrate` | none | One `service`, `command` and `timeout` per image that hosts a set ([below](#migrate)) |
| `extensions` | `[]` | Untrusted PostgreSQL extensions Wheelhouse creates when it places the database ([below](#migrate)) |
| `sites.<site>` | `{}` | A host role; Wheelhouse binds it to one host per environment |
| `sites.<site>.exposure` | `public` | `public` (internet) or `private` (private network) |
| `sites.<site>.primary` | the first site | The front door: Open site, the apex proposal; at most one |
| `sites.<site>.environments` | `[dev, prod]` | The environments that publish the site |
| `services.<name>.name` · `description` | none | The service's display name and one line, same limits; a console shows the service key without them |
| `services.<name>.image` | `<registry>/<name>` | Without a tag: a legacy repository name. With a tag: a [pinned image](#pinned-images) |
| `services.<name>.build` | — | `dockerfile` (required), `context`, `target`, `args`, `contexts`; none on a pinned image |
| `services.<name>.paths` | — | Paths whose change rebuilds this service; its Dockerfile always counts; none on a pinned image |
| `services.<name>.port` | `8080` | The port the service listens on |
| `services.<name>.health` | — | An HTTP path, or `{ command: [...] }` |
| `services.<name>.memory` · `stopGrace` | `512m` · `30s` | Container memory limit and stop grace |
| `services.<name>.settings` | none | `file` mount target (default `/app/appsettings.Target.json`; `/app/appsettings.Local.json` before v0.7.0), the `required` keys the runner checks before deploying, and typed `keys` ([below](#typed-keys)) |
| `services.<name>.volumes` | `{}` | Named volume → absolute mount path |
| `services.<name>.sites.<site>.paths` | `[/]` | The path prefixes the service serves on that site |
| `services.<name>.sites.<site>.port` | the service port | The container port the site reaches |
| `services.<name>.needs` | `[]` | Backing services the server provides: `postgres`, `valkey`, `broker` |
| `services.<name>.dependsOn` | `[]` | Services of this product it starts after, once each is healthy; no cycle |
| `services.<name>.capabilities` | `[]` | Linux capabilities added back after `cap_drop: ALL` |

- Every service runs with `no-new-privileges`, all capabilities dropped, an init process, bounded logs and a restart policy.
- Each service answers on the platform network as `<product>-<environment>-<service>`; the ingress routes sites there.
- Every service receives `DEPLOY_ENVIRONMENT` (`dev` or `prod`) from the runner, declared or not.

### Pinned images

A service may run another repository's published image, such as a per-product instance of a platform service (M77).

```yaml
services:
  identity:                           # a per-product Identity instance
    image: ghcr.io/wow-two-sdk-beta/wow-two-sdk-beta.identity/identity:0.3.0
    health: /health
    settings:
      keys:
        DatabaseSettings:ConnectionString: { required: true }
        # … the instance's own keys, generated or linked: § Generated and linked keys
    needs: [postgres]
```

- must give a pinned image a release tag, never `latest`, and no `build` or `paths` (M77).
- must pin only a public package: a platform service's image is public on GHCR, so every Wheelhouse pulls it without a
  registry login (owner 2026-10-31). Every wow2 organization allows public package creation (owner 2026-10-31); the
  flip itself is a package settings click, since GitHub has no API for it.
- must declare its health, settings and `needs` like any service's (M77).
- must change the tag in the descriptor to upgrade it; a tag change is a descriptor change (M77).
- Renovate pushes each newer tag to its `renovate/pinned-images` branch through the pipelines preset, with no pull
  request: the branch push runs the product's checks, and Renovate fast-forwards `main` once they pass, opening a pull
  request only when they fail (owner 2026-10-29: "ci doing it without a pr is preferred"). The `main` push releases a
  bundle, and Wheelhouse deploys it to dev like any release.
- The generator resolves the tag to a digest at release and versions the service by its tag.
- Wheelhouse pulls and deploys it like any service; the product's services reach it on the platform network.

---

## Identity

What the product calls itself. The repository owns it; a console shows a cached copy and never edits it. It moved
here from `product/product.json` on 2026-10-27 (Wheelhouse decision 7, format A); that file is
[retired](../../design/identity/product-manifest.md).

- must declare `name` and `description` together; `homepage` needs both. Pipelines `v0.11.0` or later checks them
  and refuses a broken one.
- must name the product as people say it (`Forever Pin`), not by its slug (`foreverpin`).
- must write the description as one line on what the product does for whom (`QR codes that outlive the print.`),
  never how it is built or what it is built on.
- must write every text as one line: no control characters, no leading or trailing space. Quote a text YAML would
  read as something else: `"{{Brand}}"`, `"Yes"`, `"2048"`.
- must not put credentials in `homepage`; a product with no public address leaves it out.
- may name and describe a service under its own key (`services.<name>.name`, `description`); a console shows the
  service key for one without.
- must keep icons as files, never descriptor keys ([product icons](../../design/identity/product-icons.md#paths)).
- must keep slug, repository, lifecycle, release source and environments out of the identity: `product` is the slug,
  and Wheelhouse owns the rest.
- A product of several repositories takes its name and description from its
  [catalog entry](../../development/repo/catalog/catalog.md#products-of-several-repositories); Wheelhouse ignores its
  repositories' identity keys.
- The release bundle never carries the identity. An identity change alone is a descriptor change: it releases a
  bundle that reuses every image.

How a console reads it:

- must read the descriptor at a commit of the product's default branch, and key what it keeps by that commit; must
  not expire it on a timer.
- must replace a kept copy only with one read at a newer commit.
- must drop the kept copy when a newer commit declares no identity; the product then falls back to its recorded
  values.
- must ignore an invalid identity: keep the last valid copy and show the operator the reason.
- must not fail a request because the identity is invalid, missing or unreachable.
- must show every field as text; must not interpret markup in it.
- may read a retired `product/product.json` while the descriptor declares no identity, and must then tell the
  operator to move it ([retired manifest](../../design/identity/product-manifest.md#existing-files)).

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

### Products of several repositories

A product may span several repositories (Wheelhouse decision 70): one brand, one domain, one set of environments,
listed together in its [catalog entry](../../development/repo/catalog/catalog.md#products-of-several-repositories).
Each repository keeps its own `deploy.yml`, CI, `vX.Y.Z` tags and version track; Wheelhouse composes the product's
releases from theirs.

| Fact | Rule |
|---|---|
| `product` | the product's slug in every repository (`ocharo`), never the repository's own name; the bundle, its asset (`ocharo-release.tar.gz`) and every service's platform name (`ocharo-<environment>-<service>`) carry it |
| Services | unique across the product's repositories; Wheelhouse refuses a release set that repeats one, naming both repositories |
| Images | each repository's own: `ghcr.io/<owner>/<repo>/<service>`, unchanged |
| Sites | host roles of the one product, so unique across its repositories: each repository names its own (`desk`, `studio`, `motion`) and Wheelhouse refuses a clash |
| Front door | the primary repository's primary site; another repository's primary site is an ordinary one |
| Named volumes | unique across its repositories too (`studio-data`, `motion-data`): one volume is one product's storage, so Wheelhouse refuses a clash rather than share or rename one |
| `dependsOn` | may name another repository's service once the shared generator accepts it; Wheelhouse checks the whole product when it composes a release, and refuses an unknown service or a cycle |
| `dotnetEnvironment`, `verify` | per repository: .NET environment names apply to the services of the repositories that opt in; the first repository's dev check runs for the set |
| `migrate`, `extensions` | per repository, for its own images and sets; Wheelhouse merges them for the release set ([migrate](#migrate)) |

- A release set is one release of each repository, composed by Wheelhouse into one bundle: it deploys, rolls back
  release-wide and promotes like a single repository's release, and only its changed services restart.
- A set's label names each repository's release by its short name (the repository's name without the owner's or the
  product's prefix), joined by `_`: `platform-v0.1.8_studio-v0.1.6_assets-v0.1.0`; its bundle ID is
  `<product>-set-<12 hex>`, a digest of its components, so the same components always make the same set.
- Every repository release makes a new set with every other repository's newest release; a commit build of one
  repository makes a candidate set for dev. A product has no set until each of its deploying repositories has published
  a release.
- Prod takes the very set dev proved; the changelog before a promotion compares each repository that changed.

---

## Migrate

The step that brings every migration set to the release's level before any service restarts. Set, verb and
compatibility rules → [migrations](../../development/backend/dotnet/core/mla/domains/persistence/migrations/migrations.md).

```yaml
migrate:                              # one item per image that hosts a set
  - service: identity                 # a pinned per-product instance, before the sets that key into it
    command: [dotnet, Identity.Api.dll, migrate]
  - service: management               # hosts every set this repository owns
    command: [dotnet, ForeverPin.Api.dll, migrate]
    timeout: 10m                      # default 10m; 10s-60m
extensions: [postgres_fdw]            # untrusted extensions only; a set creates trusted ones
```

- must declare one item per image that hosts a set, never one per service that reads a set (M9, M43).
- must name a service of this descriptor; its release image runs `command` as the entrypoint (M9).
- must give `command` as the program and its arguments, ending in the bare `migrate` verb (M9, M51).
- may set `timeout`: default `10m`, from `10s` to `60m` (M9).
- must list a pinned per-product instance before every item whose sets reference its set (M28, M77).
- must list the untrusted extensions the product's sets need under `extensions` (M41).

How the runner runs it:

- on every forward deploy, dev and prod, after the pull and before the first wave (M13, M14).
- in list order within a repository, every set after the sets it depends on (M14, M28).
- across a release set's repositories, by the sets' `DependsOn` from the manifest, then catalog order (M28, M43).
- each item in a one-off container: the item's release image, `--pull never`, the command as entrypoint, the
  service's environment, volumes and memory, the platform network, all capabilities dropped, the image's user (M8).
- connected through `Migrations:ConnectionString`, filled from the target's database beside the service's rendered
  settings; the runtime role in v1 ([settings at deploy](#settings-at-deploy), M8).
- after the prod snapshot, under the target's deployment lock for the whole job; the dev run is the rehearsal (M18).
- any failure stops the job before any restart: exit `1` or `2`, a crash, the timeout (M14).
- an exit `3` retries once, then fails "busy"; a timeout stops the container (M17).
- records per item `status` (`applied` · `current` · `refused` · `failed` · `busy` · `timed out`), `exitCode`,
  `seconds`, and per set the levels, applied labels with kind, rollback floor, background migrations and lock waits
  from the `migrate-result` line (M37).
- keeps the database's history the only history; Wheelhouse keeps job records beside it (M36, M38).
- shows per environment and set the level and newest label from the latest job, and "check now" runs `migrate check`
  from the image the target runs (M36, M38).
- creates the declared `extensions` as superuser when it places the database (M41).

The rollback gate:

- every return to an older release — an operator rollback, the automatic restore, a deploy of an older release —
  runs the older image's `migrate check` first (M15).
- `0` proceeds; anything else refuses and names the snapshot (M15).
- an older release that declares no `migrate:` item falls back to `rollbackCompatible`, with a warning (M15).

The generator:

- runs each item image's `migrate sets --json` and writes every set and its level into the release manifest (M78).
- derives the bundle's `migrations` fact from those levels (M9, M78).

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
  rolls back whole, so a target always runs exactly one release. A release set is rollback-compatible only when every
  repository's release is.

---

## Settings at deploy

Wheelhouse renders each service's settings file at every deploy, in layers, the last winning:

| Layer | Holds |
|---|---|
| Host file | A file the target still names; the render keeps it as its bottom layer |
| Wheelhouse | The environment's stored settings and its built-in vault secrets |
| Derived | `AllowedHosts` (the hosts of the sites the service serves, its platform name `<product>-<environment>-<service>`, `localhost`), `Sites:<site>:Url` (each published site's origin) and `Deployment:TrustedProxies` (the ingress's address) |
| Database | A required connection key no other layer sets (`ConnectionStrings:<name>`, `<Section>:ConnectionString`), from the target's own database, for a service that `needs: [postgres]` |
| Migrate | `Migrations:ConnectionString` from the target's database, in the [migrate](#migrate) container only (M8) |
| Linked | A `from` key's value: its source's value from the layers above ([generated and linked keys](#generated-and-linked-keys)) |

- A derived key may sit under `settings.required`; nobody fills it in.
- Wheelhouse makes a missing `generate` key's value before the deploy; nobody fills it in either.
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
| `generate` | none | How Wheelhouse makes a secret's missing value: [generated and linked keys](#generated-and-linked-keys) |
| `from` | none | Another key whose value this key takes: [generated and linked keys](#generated-and-linked-keys) |

- must pin pipelines `v0.10.0` or later to declare `keys`; an older generator refuses it, and the bundle reaches a
  Wheelhouse runner from v0.5 (`settings.<service>.types`), which an older runner refuses.
- A descriptor without `keys` builds bundles byte for byte as before.
- Owners may add keys of their own per product in Wheelhouse's console, typed the same way; a release's declaration
  wins over one the owner added.
- Wheelhouse checks a value against its type on every save, field by field; a deploy applies what is saved.

### Generated and linked keys

A secret key may say how Wheelhouse makes its value (`generate`), and any key may take another key's value (`from`), so
no secret passes through a person or an agent (owner 2026-10-31). A product pinning Identity declares its keys so:

```yaml
services:
  identity:
    image: ghcr.io/wow-two-sdk-beta/wow-two-sdk-beta.identity/identity:0.3.6
    settings:
      keys:
        Identity:Server:Keys:Signing:0:
          secret: true
          required: true
          generate: { command: [dotnet, Identity.Api.dll, keys, generate, --role, signing] }
        Identity:Server:Clients:0:ClientSecret:
          secret: true
          required: true
          generate: { random: 32 }                      # 32 random bytes, base64url
        Identity:Server:Issuer:
          from: Sites:identity:Url                      # the identity site's origin, per environment
  desk:
    settings:
      keys:
        Auth:ClientSecret:
          from: Identity:Server:Clients:0:ClientSecret  # the same value Identity holds
```

| Field | Form | Value |
|---|---|---|
| `generate` | `{ random: N, encoding: base64url \| hex }` | `N` random bytes, 16–64, `base64url` by default |
| `generate` | `{ command: [argv…], timeout: 2m }` | The command's standard output, run from the service's own release image |
| `from` | a configuration path | Another declared key's value, or a derived key's (`Sites:<site>:Url`) |

`generate`:

- must sit on a `secret: true` text key; refused beside `default` or `from`.
- Wheelhouse makes the value once per environment, before the deploy would wait on it; dev and prod never share one.
- A deploy only fills a missing value and never replaces a stored one; the console's Regenerate adds a new version,
  which the next deploy applies.
- A command runs on the target in a one-off container from the declaring service's release image: no network, no
  settings file, no secret, all capabilities dropped, as the image's user, 512 MB of memory; `timeout` defaults to
  `2m`, at most `10m`.
- must print the value alone to standard output and anything else to standard error. Exit 0 with output stores it,
  without its trailing newline; anything else fails the deploy before a restart, keeping the last standard-error line
  and never standard output.
- A value holding a PEM certificate sets its version's expiry to the certificate's end date (`notAfter`).
- The audit records which deploy generated which key, never the value.

`from`:

- must name one configuration path: a key any service of the same product declares, or a derived key.
- must stand alone on its key: refused beside any other field; the key takes its source's type and secrecy, and a
  deploy waits on it only while its source waits.
- must not name a key that itself has `from`: one hop, so no cycle.
- Wheelhouse renders the source's value for the same environment at every deploy, so a regenerated source reaches
  every linked key in one deploy.
- A secret source's linked value stays in the vault render; it never reaches the settings store or a console read.
- The console shows a linked key read-only, with its source.

- must pin pipelines `v0.14.0` or later to declare `generate` or `from`; an older generator refuses both, and the
  bundle needs a Wheelhouse runner from v0.11.

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
| any other branch but `renovate/**`, or a dispatched commit | `X.Y.(Z+1)-<branch>.<n>` | `sha-<commit>` | dev, by hand | 14 days |

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
- must pin `v0.11.0` or later to declare an identity (`name`, `description`, `homepage`, or a service's `name` or
  `description`); an older generator refuses the keys.
- must pin `v0.12.0` or later to declare `migrate`, `extensions` or a pinned image; an older generator refuses each.
- must pin `v0.13.0` or later to trigger on `renovate/**` pushes: from it such a push runs the checks and publishes
  nothing, and leaves a commit a pull request run verifies to that run; an older tag publishes a candidate for it.
- should move the pin to each new pipelines tag; every workflow of a repo that names the generator names one tag.
- must trigger it on every branch push (`branches: ['**']`), on pull requests, and on `workflow_dispatch` with a
  `commit` input, so Renovate's automerged branches get their checks (owner 2026-10-29); a pin before `v0.13.0` keeps
  `'!renovate/**'` in the push branches.
- must keep one concurrency group per ref (`inputs.commit || github.ref`), queued with `queue: max`, and set no
  `cancel-in-progress`: GitHub rejects `queue: max` with a `cancel-in-progress` that evaluates true, at run start,
  and starts no job. A superseded branch run therefore still builds.
- must prove a workflow change on every event and ref its expressions branch on (a `main` push, a branch push, a pull
  request, a dispatch) before a convention, the pipelines `README.md` or a template carries it; a green `main` run
  proves `main` only.
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
- builds on every code push but a `renovate/**` one, which runs the checks only: `main` releases, every other branch
  builds a candidate;
- builds a dispatched commit that has no build yet (Wheelhouse's Build action);
- builds each changed service from `deploy.yml`, whatever its Dockerfile, target, arguments or build contexts;
- fetches the Git LFS files under `engineering/` first, so images carry real assets instead of pointer files;
- passes every build `APP_VERSION` (the build's version) and `VCS_REF` (the full commit SHA it was built from);
- tags and publishes images and the bundle per the table above, and moves `latest` last on a release.

### Incidents

- 2026-10-27: every branch push and pull request failed at run start with "The combination of 'queue: max' and
  'cancel-in-progress: true' is not allowed", in 26 repositories; `main` stayed green.
  - Cause: the 2026-10-19 rule asked one concurrency block for two behaviors, queue on `main` and cancel elsewhere,
    while `queue` stayed a literal; GitHub's workflow syntax page states the restriction.
  - Why it hid: `cancel-in-progress` evaluates false on `main`, and agents push to `main` only, so no other ref ran
    until cloud sessions pushed `claude/*` branches eight days later.
  - Spread: the rule → the pipelines `README.md` caller → both templates → every scaffolded repository, each proved
    on `main` alone.
  - Fix: no `cancel-in-progress` beside `queue: max`; a change is proved on every path it branches on (rules above).

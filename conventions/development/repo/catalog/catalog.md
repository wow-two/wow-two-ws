# Catalog

*Last updated: 2026-10-24*

> `catalog.yml` at the root of each hub repository: every repository and app the hub owns, one entry per product.
> Purpose — one machine-readable source per owner: Wheelhouse imports from every hub; `.claude/repo-registry.md` renders them all.
> Use case — adding, moving or retiring a repository; starting a hub; reading the portfolio from code.

## Scope

- must give every repository the registry lists an entry in exactly one hub; one entry per product.
- must give a library, KB module or template its own single-repository entry with `deploy: none`.
- must keep hosts, addresses, tailnet names, environments and secrets out of every hub; the registry renders all hubs
  into public `wow-two-ws`.
- must validate each hub's file against [catalog.schema.json](catalog.schema.json); its first line points `$schema` there.

---

## Hubs

A hub is a repository whose root `catalog.yml` indexes one owner's products.

| Hub | Repository | Checkout | Owns | Workspaces |
|---|---|---|---|---|
| `wow2` | `wow-two/wow-two-ws` | the workspace root | the `wow-two*` orgs: core, meta, platform, SDKs, KB, apps; wow2's personal tools | `wow2-platform` · `wow2-backbone` · `wow2-apps` · `personal` |
| `ventures` | `sulton-max/10x-ventures` | `workbench/maxs-projects/ventures/10x-ventures` | the owner's ventures, and ventures and client work run for others | `own-ventures` · `other-ventures` |
| `ocharo` | `ocharo-hq/ocharo-ws` | `workbench/mfts-projects/ventures/ocharo-hq/ocharo-ws` | the `ocharo-hq` org's repositories | `ocharo` |

```text
{hub}/
├── catalog.yml      ← the index: hub, orgs, workspaces, entries
└── …                ← the hub's own docs: portfolio tracking, strategy, setup; they link entries by slug
```

- must keep the index to the one root `catalog.yml`; a hub adds no `catalog/` folder — an entry's plans, tracks and
  specs live in its own repository, so a per-entry folder would repeat them.
- must not re-list an entry's repository, status or purpose in another hub document; link the slug or `catalog.yml`.
- must name the hub in `hub` (`slug`, `name`, `repository`, `description`); the hub repository is never an entry.
- must file an entry in its owner's hub: `wow-two*` repositories in wow2, the owner's and others' ventures in ventures,
  `ocharo-hq` repositories in Ocharo.
- must give each workspace one hub; a workspace slug carries its hub's word — `wow2-*`, `*-ventures`, `ocharo[-*]` —
  except wow2's `personal`.
- must keep entry and workspace slugs unique across hubs; Wheelhouse refuses the later hub's list naming both.
- must keep `local` relative to the `wow-two-ws` root in every hub; each hub checkout sits under it.
- must list each other hub in wow2's `hubs` (`repository`, `local`), in registry order.

### Starting a hub

- must create the repository and its root `catalog.yml` with `hub`, then validate it against the schema.
- must add the hub to wow2's `hubs`, this table and Wheelhouse's `Catalog:Sources`, then regenerate the registry.
- must move entries by deleting them from the old hub in the same pass; the registry rejects a slug in two hubs.

---

## Format

```yaml
catalog: 1
hub:                                    # the hub this file indexes
  slug: wow2
  name: wow2
  repository: wow-two/wow-two-ws
  description: "The wow2 ecosystem: core, platform, SDKs, knowledge base and community apps"
hubs:                                   # wow2 only: the other hubs' checkouts, in registry order
  - repository: sulton-max/10x-ventures
    local: workbench/maxs-projects/ventures/10x-ventures
orgs:                                   # GitHub organizations the hub owns, in registry order; optional
  - slug: wow-two-platform
    url: https://github.com/wow-two-platform
    label: internal infra               # registry only: heading parenthetical
    description: "pipelines, DI, comms, data access. Not for external consumers"
workspaces:
  - slug: wow2-platform
    name: wow2 platform
    description: "Platform apps that deploy and run the portfolio, and their test fixtures"
entries:
  - slug: secrets-vault
    name: Secrets Vault
    workspace: wow2-platform
    kind: platform
    deploy: wheelhouse
    status: "Active"
    purpose: "Secrets vault — envelope-encrypted store + management UI"
    repositories: [wow-two-platform/wow-two-platform.secrets-vault]
```

| Key | Meaning |
|---|---|
| `hub` | the hub's slug, display name, own repository and one-line scope |
| `hubs` | wow2 only: each other hub's repository and checkout path |
| `orgs[].intro` · `notes` | registry only: Markdown blocks before and after the org's table |
| `entries[].repositories` | GitHub `owner/name`, primary first; several make one product ([below](#products-of-several-repositories)) |
| `entries[].replaces` | the slugs of products this entry supersedes; Wheelhouse retires each one nothing ever deployed to |
| `entries[].local` | the primary's checkout path from the `wow-two-ws` root, when not `workbench/{owner}/{name}` |

- must double-quote free text (`description`, `status`, `purpose`); a `: ` or a leading backtick breaks a plain value.
- must keep to block mappings and sequences, flow sequences of scalars, quoted values and `|-` literals.
- must not use flow mappings, anchors or tags; the generator's fallback reader stops at them.

---

## Entries

| Field | Rule |
|---|---|
| `slug` | a deployable's `deploy.yml` `product`; another product's code slug; else the repo name, dots → hyphens |
| `workspace` | one the same hub declares — see [Hubs](#hubs) |
| `kind` | `core` · `meta` · `platform` · `backbone` · `sdk` · `kb` · `app` · `venture` · `template` |
| `deploy` | `wheelhouse` · `ci` · `none` |

- must take a deployable's slug from its [deploy descriptor](../../../deployment/descriptor/deploy-descriptor.md#rules).
- must pick `local` by the [workbench layout](../layout/workbench-layout.md#catalog-mapping).
- must check out an entry's other repositories beside the primary, each under its own name.
- must name a `.github` repository's entry `{owner}-github`.
- must file platform apps and their fixtures under `wow2-platform`; SDKs, libraries, pipelines and templates under
  `wow2-backbone`; community apps under `wow2-apps`; personal tools under `personal`.
- must file the owner's ventures under `own-ventures`, other ventures and client work under `other-ventures`, and
  Ocharo's repositories under `ocharo`.
- must use kind `platform` for a platform app and `backbone` for a platform library, pipeline or org config.
- must set `deploy: wheelhouse` when Wheelhouse deploys the repo, Wheelhouse itself included (it deploys itself since
  2026-10-24), and `ci` when the repository's own CI does.
- must name the canonical GitHub repository, never a redirect alias left in a local `origin`.
- may leave `repositories` empty only while no GitHub repository exists; `local` is then required.
- must not leave `repositories` empty on a deployable.

### Products of several repositories

One brand, one domain and one dependency chain make one product, whatever its repositories (Wheelhouse decision 70):
Ocharo's `ocharo` entry lists Platform, Studio, Marketing and Assets.

- must list every repository of a `deploy: wheelhouse` entry in `repositories`, primary first: Wheelhouse imports them
  as one product with one set of environments, one placement, one secrets space and one redundancy setup.
- must put first the repository whose primary site is the product's front door; its manifest and icons stand for the
  repository only, and the product is named by its entry.
- must name the entry's slug as `product` in every listed repository's `deploy.yml`
  ([descriptor](../../../deployment/descriptor/deploy-descriptor.md#products-of-several-repositories)).
- must keep service, site and named-volume names unique across the product's repositories; Wheelhouse refuses a clash
  and names both repositories.
- may list a repository that deploys nothing yet; it joins the product's releases once its `deploy.yml` names a
  service and it has published a release.
- should name, in `replaces`, the products a merge supersedes (`replaces: [ocharo-platform, ocharo-studio]`); importing
  the entry retires each one nothing ever deployed to, its environments first, and keeps one with deploys on record,
  with a warning.
- must keep a library, KB module or template on its own single-repository entry; several repositories mean one
  deployable product, nothing else.

---

## Adding a repository

- must add the entry to its owner's hub, inside its org's group or the hub's own group; registry rows follow catalog
  order.
- must validate against the schema, then run `python3 scripts/gen-repo-registry.py` in `wow-two-ws`.
- must commit the hub's `catalog.yml` in the hub and `.claude/repo-registry.md` in `wow-two-ws`.

---

## Registry

- must not edit `.claude/repo-registry.md` by hand; the generator rewrites it from wow2's catalog and each hub in `hubs`.
- must have every hub checked out at its `local`; the generator exits 1 naming a missing one.
- may run the generator with `--check`; it exits 1 while the registry is stale.
- section — per hub in `hubs` order, wow2 first: each org the hub declares, then the hub's own section for entries
  whose primary repository no declared org owns.
- org — the primary repository's owner, else the org folder in `local`.
- date line — kept when nothing else changed, else today.

---

## Consumption

- Wheelhouse reads each hub in `Catalog:Sources` at `main` — wow2, ventures, Ocharo — and merges them in that order.
- must ignore keys a reader does not use; `label`, `intro`, `notes`, `hubs`, `status` and `local` serve the registry.
- must skip importing an entry whose `repositories` is empty.
- must import a `deploy: wheelhouse` entry of several repositories as one product, and give an existing product the
  entry's repositories when they changed.

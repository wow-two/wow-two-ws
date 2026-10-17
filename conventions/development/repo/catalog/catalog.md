# Catalog

*Last updated: 2026-10-17*

> `catalog.yml` at the `wow-two-ws` root: every wow2 repository and app, one entry per product.
> Purpose — one machine-readable source: Wheelhouse imports products from it; `.claude/repo-registry.md` is its view.
> Use case — adding, moving or retiring a repository; reading the portfolio from code.

## Scope

- must give every repository the registry lists an entry; one entry per product.
- must give a library, KB module or template its own single-repository entry with `deploy: none`.
- must keep hosts, addresses, tailnet names, environments and secrets out; `wow-two-ws` is public.
- must validate the file against [catalog.schema.json](catalog.schema.json); its first line points `$schema` there.

---

## Format

```yaml
catalog: 1
orgs:                                   # GitHub organizations, in registry order
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
| `orgs[].intro` · `notes` | registry only: Markdown blocks before and after the org's table |
| `entries[].repositories` | GitHub `owner/name`, primary first |
| `entries[].local` | checkout path from the root, when not `workbench/{owner}/{name}` |

- must double-quote free text (`description`, `status`, `purpose`); a `: ` or a leading backtick breaks a plain value.
- must keep to block mappings and sequences, flow sequences of scalars, quoted values and `|-` literals.
- must not use flow mappings, anchors or tags; the generator's fallback reader stops at them.

---

## Entries

| Field | Rule |
|---|---|
| `slug` | a deployable's `deploy.yml` `product`; another product's code slug; else the repo name, dots → hyphens |
| `workspace` | `personal` · `wow2-platform` · `wow2-backbone` · `wow2-apps` · `own-ventures` · `other-ventures` |
| `kind` | `core` · `meta` · `platform` · `backbone` · `sdk` · `kb` · `app` · `venture` · `template` |
| `deploy` | `wheelhouse` · `ci` · `none` |

- must take a deployable's slug from its [deploy descriptor](../../../deployment/descriptor/deploy-descriptor.md#rules).
- must name a `.github` repository's entry `{owner}-github`.
- must file platform apps and their fixtures under `wow2-platform`; SDKs, libraries, pipelines and templates under
  `wow2-backbone`; community apps under `wow2-apps`; personal tools under `personal`.
- must file the owner's ventures under `own-ventures`; ventures and client work for others under `other-ventures`.
- must use kind `platform` for a platform app and `backbone` for a platform library, pipeline or org config.
- must set `deploy: wheelhouse` when Wheelhouse deploys the repo, `ci` when CI does (Wheelhouse itself).
- must name the canonical GitHub repository, never a redirect alias left in a local `origin`.
- may leave `repositories` empty only while no GitHub repository exists; `local` is then required.
- must not leave `repositories` empty on a deployable.

---

## Adding a repository

- must add the entry inside its org's group, or the ventures group; registry rows follow catalog order.
- must validate against the schema, then run `python3 scripts/gen-repo-registry.py`.
- must commit `catalog.yml` and `.claude/repo-registry.md` together.

---

## Registry

- must not edit `.claude/repo-registry.md` by hand; the generator rewrites it.
- may run the generator with `--check`; it exits 1 while the registry is stale.
- section — the primary repository's owner, else the org folder in `local`, else the ventures section.
- section order — the `wow-two*` orgs, then the ventures section, then the remaining orgs.
- date line — kept when nothing else changed, else today.

---

## Consumption

- Wheelhouse reads `catalog.yml` from `wow-two/wow-two-ws` at `main`.
- must ignore keys a reader does not use; `label`, `intro`, `notes` and `local` serve the registry.
- must skip importing an entry whose `repositories` is empty.

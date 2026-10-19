# Workbench Layout

*Last updated: 2026-10-19*

> Where each repository is checked out under `workbench/`: one folder per wow2 org, one folder per owner for the rest.
> Use case — cloning, scaffolding or moving a checkout; choosing a catalog entry's `local`.

## Tree

```text
workbench/
├── wow-two/ · wow-two-meta/ · wow-two-platform/ · wow-two-sdk/ · wow-two-sdk-beta/ · wow-two-kb/ · wow-two-apps/
├── maxs-projects/                     ← the owner's
│   ├── ventures/                      ← own ventures, flat; the 10x-ventures hub
│   ├── clients/{client}/              ← work run for others: nasiya-finance/ · mintrans/
│   └── wom-two-ws/                    ← a workspace of the owner's own
└── mfts-projects/                     ← Maftuna's
    └── ventures/
        └── ocharo-hq/ocharo-ws/       ← the Ocharo hub; its repositories sit in its own workbench/
```

---

## Top level

- must hold only the `wow-two*` org folders and the owner folders `maxs-projects/` and `mfts-projects/`.
- must check out a `wow-two*` repository at `workbench/{org}/{repo}`; the folder name is the org name.

---

## Owner folders

- `{owner}-projects/` — whose work it is: `maxs` the owner, `mfts` Maftuna; never what kind of work.
- must place a venture its owner runs in `ventures/`.
- must keep `ventures/` flat; the hub's `kind` and `status` classify a venture, never a sub-folder.
- must place work run for others in `clients/{client}/`; `{client}` is the client's GitHub org, else its short name.
- must nest a venture with its own GitHub org in a folder named for the org: `ventures/{org}/{repo}`.
- must check out a hub inside its owner's `ventures/`.
- may place a separate workspace of the owner's directly in the owner folder: `{owner}-projects/{workspace}`.

---

## Catalog mapping

| Catalog workspace | Checkout |
|---|---|
| `wow2-*` · `personal` | `workbench/{org}/{repo}` |
| `own-ventures` | `workbench/maxs-projects/ventures/{repo}` |
| `other-ventures` | `workbench/maxs-projects/clients/{client}/{repo}` |
| `ocharo` | `workbench/mfts-projects/ventures/ocharo-hq/ocharo-ws/workbench/{repo}` |

---

## Setup and moves

- may recreate the tree with `scripts/clone-all.sh` — wow2 orgs, owner folders, each hub, then its entries.
- must move a checkout with `mv` and update its `local`, `scripts/active.sh` and `.claude/launch.json` in one pass.
- must re-send `~git_on` for a moved repository; flags are keyed by path → [git](../version-control/git.md#discipline).

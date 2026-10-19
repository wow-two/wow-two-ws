# Workbench Layout

*Last updated: 2026-10-19*

> Where each repository is checked out under `workbench/`: one folder per wow2 org, one folder per owner for the rest.
> Use case — cloning, scaffolding or moving a checkout; choosing a catalog entry's `local`.

## Tree

```text
workbench/
├── wow-two/ · wow-two-meta/ · wow-two-platform/ · wow-two-sdk/ · wow-two-sdk-beta/ · wow-two-kb/ · wow-two-apps/
├── maxs-projects/                     ← the owner's
│   ├── ventures/                      ← own ventures in three groups; the 10x-ventures hub beside them
│   │   ├── saas/                      ← hosted software that accounts or institutions pay for
│   │   ├── consumer/                  ← apps, games and content for play and daily life
│   │   ├── labs/                      ← no buyer by design: research, vision, concepts, personal tools
│   │   └── 10x-ventures/              ← the hub, in no group
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
- must place a venture its owner runs in `ventures/`; `maxs-projects/ventures/` sorts them into [groups](#venture-groups).
- must place work run for others in `clients/{client}/`; `{client}` is the client's GitHub org, else its short name.
- must nest a venture with its own GitHub org in a folder named for the org, beside the groups: `ventures/{org}/{repo}`.
- must check out a hub inside its owner's `ventures/`.
- may place a separate workspace of the owner's directly in the owner folder: `{owner}-projects/{workspace}`.
- may leave an owner's `ventures/` ungrouped while it holds one org's work: `mfts-projects/ventures/` does.

---

## Venture groups

- must place each venture of `maxs-projects/ventures/` in one group, one level deep: `ventures/{group}/{repo}`.
- `saas/` — hosted software that a business, maker, professional or institution pays for: subscription, per use or contract.
- `consumer/` — apps, games and content for play and daily life; free, or paid through cosmetics and unlocks.
- `labs/` — no buyer by design: research, vision, concepts and personal tools.
- must pick the group by who pays, else by who the product is for; never by stage — the hub's `kind` and `status` classify that.
- must place a companion (promo, asset library, worktree) in its parent's group, beside the parent.
- must place a file that indexes a group's ventures in that group.
- must keep the hub at `ventures/10x-ventures`, beside the groups and in none.
- must not add a group for one venture; a venture that fits no group sits in `labs/` until several do.
- must not name an org folder after a group.

---

## Catalog mapping

| Catalog workspace | Checkout |
|---|---|
| `wow2-*` · `personal` | `workbench/{org}/{repo}` |
| `own-ventures` | `workbench/maxs-projects/ventures/{group}/{repo}` |
| `other-ventures` | `workbench/maxs-projects/clients/{client}/{repo}` |
| `ocharo` | `workbench/mfts-projects/ventures/ocharo-hq/ocharo-ws/workbench/{repo}` |

- must carry a venture's group in its `local`; the catalog has no group key, so `local` and the folder cannot disagree.

---

## Setup and moves

- may recreate the tree with `scripts/clone-all.sh` — wow2 orgs, owner folders, venture groups, each hub, then its entries.
- must move a checkout with `mv` and update its `local`, `scripts/active.sh` and `.claude/launch.json` in one pass.
- must re-send `~git_on` for a moved repository; flags are keyed by path → [git](../version-control/git.md#discipline).

---
name: create-library
description: >-
  Take a NEW domain library — an SDK domain repo with its NuGet family, npm package and service image — from the
  domain template all the way to a GitHub repo, published packages, an image, the hub catalog, Wheelhouse and consumer
  re-pins, by running scripts/release/library.py's plan and the exact commands it prints, one Bash call each. Use it
  whenever the user wants to create, set up, release or publish a new library or domain repo end to end ("create
  library identity", "new domain repo for file storage", "publish a new library", "put wow-two-sdk-beta.example-lib on
  GitHub"), or to resume one halfway ("where is the identity library at", "continue the library rollout", "arm the
  publish for identity"). Scaffolding alone, with no GitHub repo, stays with create-repo (SHAPE=domain).
---

# create-library

Carries one domain library from `workbench/wow-two-sdk-beta/wow-two-sdk-beta.domain-template` to a live repo, as
designed in `ideas/identity-analysis-2026-10/t9-release-automation.md` (T9). It automates the 27-step rollout of
`ideas/identity-analysis-2026-10/t8-library-template.md` § 6 except the steps that need 2FA, a secret value, DNS or the
developer's judgment; those come out as one checklist.

- `scripts/release/library.py` only reads: the local folder, `gh api` GETs, nuget.org, npm, the hub and the git flags.
- It prints each phase as done, next or blocked, then the next phase's exact commands.
- It makes no GitHub, registry, commit or push write. You run each printed command as its own Bash call, so the
  git guard (`.claude/hooks/guard-git.py`) judges every write.
- State comes from probes, never a state file: a re-run resumes at the first unfinished step, in any chat.
- The layout, names and releases follow `conventions/development/repo/structure/domain-structure.md`.

## Inputs

| Input | Flag | Default | Identity |
|---|---|---|---|
| repo name | positional | — | `wow-two-sdk-beta.identity` |
| Brand (PascalCase domain) | `--brand` | the repo's last segment, PascalCased | `Identity` |
| org (workbench folder, GitHub owner) | `--org` | `wow-two-sdk-beta` | — |
| slug (code dirs, `fe-{slug}`) | `--slug` | last dot-segment | `identity` |
| product (catalog, deploy, Wheelhouse) | `--product` | lowercased Brand | `identity` |
| be sdk / fe sdk pins | `--core-version` · `--fe-version` | the template's | — |
| GitHub description | `--description` | generated from the names | — |

Ask only for what is missing; confirm `{repo, Brand, org}` before the first write. Run creation in the chat where the
developer asked for the library, not in a relayed subagent: auto mode refused a public push relayed mid-task before
(T9 § 3, unverified whether it still does).

## The loop

```bash
python3 -I scripts/release/library.py plan wow-two-sdk-beta.identity --brand Identity
```

1. Run `plan`. Read the status table, then the `Next:` block.
2. Run each numbered command as its own Bash call, in order, with the absolute paths as printed. Never join two
   writes in one call, never wrap them in a script, never add `cd`.
3. Make each `edit (…)` line with the Edit tool.
4. Stop at the first failure; fix it or report it; never retry a write in another form the guard would not see.
5. Re-run `plan`. It shows the new position, and the next phase's commands.
6. When `Next:` says nothing is runnable, relay the hand-step checklist to the developer and stop.

- `status` prints the table only; `next` prints the commands and the checklist only.
- `--confirmed nuget-policy,wheelhouse,secrets` marks steps no probe can see, once you or the developer checked them.
- `--publish` opens phase 4 while the packages still hold the template's Greetings sample (normally wrong: T9 § 4).
- `--offline` skips GitHub, nuget.org and npm; their steps read `unknown`.

Statuses: `done` · `skip` (does not apply) · `next` (yours to run now) · `pending` (after the named steps) ·
`hand` (the developer's) · `consent` (yours after a chat "yes") · `waiting` (CI or a gate) · `blocked` · `unknown`.

## Phases

| # | Phase | Steps | Done when | Who |
|---|---|---|---|---|
| 0 | Preflight | tools · gh account · template with `INTO=clone` · flags · commit identity · Codex app | probes pass | agent, developer once |
| 1 | GitHub | create (`gh repo create o/n --public`) → clone (`gh repo clone`) → settings → `main-guard` ruleset | `gh api repos/o/n` answers, `origin` = `o/n`, settings and ruleset read back | agent |
| 2 | Scaffold | `SHAPE=domain INTO=clone scaffold.sh` → fill placeholders → verify, commit → push | `product/product.json` exists; `origin/main` has the commit | agent |
| 3 | Hub | catalog entry (`apply-local catalog`) → platform-apps row → registry → hub commit → hub push | `origin/main:catalog.yml` names the repo | agent |
| 4 | Registries | content gate → NuGet policy → npm first version → arm `PUBLISH_PACKAGES` → be and fe published | nuget.org lists the family; npm lists a CI version | consent, developer, agent |
| 5 | Image | first `v*` release from the scaffold push · `wheelhouse-max` on the org | a `v*` release exists | CI, developer once |
| 6 | Wheelhouse | catalog `deploy: wheelhouse` (`apply-local deploy`) → product import → secrets and DNS | `--confirmed wheelhouse,secrets` | agent, developer |
| 7 | Consumers | `repin` each stale consumer → build, test → commit, push per repo | every pin equals the newest version | agent |

- Phase 1 clones before it edits settings: the guard matches a gh write to a checked-out repository's `origin`, and
  reads an uncloned `owner/name` as OFF (G8, P2). T9 § 4 listed settings first.
- Creation reads the push flag of the folder it will be cloned into (`workbench/wow-two-sdk-beta/*`, ON); an occupied
  folder reads OFF, so `plan` blocks creation when the folder already holds something.
- `scaffold.sh` with `INTO=clone` fills the empty clone and keeps its `.git` and `origin`; nobody runs `git remote add`.
- The commit step runs the create-repo verification (`dotnet test`, `pnpm lint/test/build/check:package`,
  `test-next-version.sh`) and `git var GIT_AUTHOR_IDENT` before `git -C <repo> commit -m "…"`.
- Phase 4 waits while `packages/*/Greetings` or `fe-{slug}/src/Greeting*` exist, so no placeholder ships. Between
  phase 3 and phase 4 the domain work lands; for Identity that is T8 steps 12–17 (docs move, code move, core `N+1`).
- Arm only after the NuGet policy: the be job pushes its tag before the publish, so a failed login burns the number.
- The hub is a shared tree: stage only the printed paths, read `git diff --cached --stat`, and stop when it lists a path
  another lane staged.
- Hub writes use the hub's own flags (`.`); with them OFF the commit and push become hand steps for GitKraken.

## Hand steps

`plan` lists each one with what it unblocks, ready ones first, with exact commands once ready.

| Step | When | The developer does | Unblocks |
|---|---|---|---|
| NuGet trusted-publishing consent | per library, after the content gate | says "yes" in chat, and the agent signs in (email, then the developer's passkey tap) and fills nuget.org's form in the `wow2` Chrome profile; or fills it: owner `wow-two-sdk-beta`, repo, `publish-packages.yml`, packages `WoW2.Sdk.Beta.Be.{Brand}.*` | arming `PUBLISH_PACKAGES`; the be publish |
| npm first version and `npm trust` | per library, after the content gate | in Warp, after the agent packs `fe-{slug}-0.0.1.tgz`: `npm publish <tgz> --access public`, then `npm trust github @wow-two-beta/fe-{slug} --file publish-packages.yml --repo o/n --allow-publish` (2FA; npm ≥ 11.15.0) | the fe job; npm drops a trusted publisher with no publish within 2 days, so the agent dispatches right after |
| Wheelhouse product registration | per library, after `deploy: wheelhouse` | imports the product from the wow2 hub, picks its server, binds its sites; the agent can drive the import in the owner's console session on request | dev rollouts of each image |
| Third-party secret values | per product | enters them in Wheelhouse; secrets never pass through an agent | the dev verify check |
| Public DNS | per public site | points DNS and binds the domain | the public site; prod promotion stays the owner's |
| `wheelhouse-max` App on the org | once per org | installs it with all repositories | Wheelhouse pulls GHCR images; T8 step 21 vanishes |
| Codex connector removal | once per org | uninstalls `chatgpt-codex-connector` | closes a dropped app's write access to every new repo |
| Folder flags | once | `~git_on commit,push workbench/wow-two-sdk-beta/*` as one whole message (set 2026-10-26) | every library under the folder |

## Release flow after creation

| Event | Runs | Result |
|---|---|---|
| a push to `main` touching `packages/` | `publish-packages.yml` | tag `be-v10.y.z-beta` → NuGet, tag `fe-v0.0.z` → npm, each line only when its sources changed |
| any push to `main` | `publish-docker-image.yml` → shared `delivery.yml` | image and GitHub Release `vX.Y.Z` (X.Y from the version track) |
| `v*` release | Wheelhouse | dev rollout and verify; prod promotion stays the owner's |
| nightly | `core-latest.yml` | build and test against the newest be sdk and fe sdk; red is a signal, not a gate |
| a published family | `plan` phase 7, `repin` | one commit per consumer repo, pushed under that repo's flags |

- CI creates every tag; an agent never creates or pushes `be-v*`, `fe-v*` or `v*`.
- A failed publish burns its number; rerun with `gh workflow run publish-packages.yml -R o/n --ref main`.
- No release commit, so no release-sync wait or `pull --ff-only` after a domain-repo push.
- Consumers pin the family through one `{Brand}SdkVersion` property beside `BackendSdkVersion`; `repin` rewrites it,
  literal `WoW2.Sdk.Beta.Be.{Brand}.*` versions and `@wow-two-beta/fe-{slug}` pins, dry run without `--write`.

## Files

- `scripts/release/library.py` — probes, plan, `apply-local catalog|deploy`, `repin`; stdlib only, `python3 -I`.
- `scripts/release/main-guard.json` — the `main` ruleset: no deletion, no force push, no review rule.
- `scripts/release/test_library.py` — `python3 -I -m unittest discover -s scripts/release`.
- `.claude/skills/create-repo/scaffold.sh` — the stamp, reused; `INTO=clone` fills an empty clone.

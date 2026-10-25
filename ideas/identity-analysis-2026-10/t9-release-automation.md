# T9 — Library release automation

*Last updated: 2026-10-25*

> One agent-run entry point, `create-library`, carries a domain library from template to published packages, image,
> Wheelhouse product and consumer re-pins; no new stored secret and no new flag kind, three guard fixes, and a
> per-library human residue of one npm 2FA sitting, one chat "yes" for NuGet, and third-party secrets and DNS.

- `W` = workspace root; `(U)` = unverified; step numbers are [T8 § 6](t8-library-template.md#6--rollout-checklist).
- Facts come from reads on 2026-10-25 of the guard, the flag adapter, both SDK workflows, pipelines `publish.yml` and
  `release.py`, Wheelhouse's architecture and deployment docs, `create-repo`, read-only `gh api` GETs, nuget.org's
  registration API, and the registry docs listed in Sources.
- Guard verdicts in § 3 come from feeding each command to `guard-git.py` as hook input; nothing ran, and the harness's
  auto-mode classifier was not simulated.
- Nothing was created, published, configured or committed.

---

## Verdict

- 18 of T8's 27 steps are already the agent's; per library, T9 takes 4 of the 8 hand steps (6, 7, 9, 21) off the
  developer, makes step 18 an agent step behind a chat "yes", and splits step 24.
- The guard already lets `gh repo create owner/name` run: an unmatched slug reads the hub's `push` flag, which is ON.
  The same fallback also lets writes reach any repository not checked out, so the fix is to fail closed (P2).
- Policy needs three narrow changes and no new kind: folder-scope flag overrides (P1), fail-closed `gh` targets with
  creation mapped to the future checkout (P2), and named-remote pushes with clone listed as safe (P3).
- Credentials stay keyless in CI: NuGet trusted publishing already creates brand-new ids, as the 2026-10-16 rename
  proved; npm trusted publishing starts after a hand-published first version; `GITHUB_TOKEN` pushes images; the
  Wheelhouse App pulls them.
- The developer keeps what 2FA, secret values and judgment require: npm's first publish per package, the NuGet form
  consent per repo, third-party secrets, public DNS, decisions, and two one-time org actions.

---

## 1 · Step inventory

| # | Step | T8 owner | What blocks automation today | Route after T9 | Owner after |
|---|---|---|---|---|---|
| 1 | Answer queue A, approve T7's cut | developer | a decision | — | developer |
| 2 | Build `domain-template` | agent | a new local repo has no flag override | P1 folder override covers it | agent |
| 3 | Extend `create-repo`, `SCRATCH=1` proof | agent | none (hub `.` ON) | adds an `INTO=clone` mode (§ 4) | agent |
| 4 | Conventions pass | agent | none | adds § 4's entry point to `dev-cycle.md` | agent |
| 5 | Core `10.0.N` | agent | none (be flags ON) | unchanged | agent |
| 6 | Create the GitHub repo | developer | T8 assumed no flag covers a missing repo; the guard reads `.` (ON) | `gh repo create … --public --disable-wiki --disable-issues`; after P2 it reads the folder override | agent |
| 7 | Repo settings, Renovate access | developer | T8 assumed UI; every setting has a repo API | `gh repo edit`, `PUT …/actions/permissions/workflow`, a `main` ruleset; Renovate dropped (no app on any wow2 org) | agent |
| 8 | Scaffold | agent | `git init` leaves no `origin` | scaffold into the clone (`INTO=clone`) | agent |
| 9 | `git remote add`, `~git_on` | developer | remote writes never run; flags change only by directive | `gh repo clone` writes `origin` (P3); one P1 directive covers every later repo | agent |
| 10 | Verify, commit, push the scaffold | agent | the new repo's flags | P1 | agent |
| 11 | Hub registration | agent | none | `library.py` writes the catalog entry and regenerates the registry | agent |
| 12 | Move spec and analysis | agent | none | unchanged | agent |
| 13–16 | Code move, dry run, core `N+1`, pin | agent | none | unchanged | agent |
| 17 | P1 implementation | agent | none | unchanged | agent |
| 18 | NuGet trusted-publishing policy | developer | nuget.org form, no documented API (U) | agent fills it in the `wow2` Chrome profile after a chat "yes"; glob `WoW2.Sdk.Beta.Be.{Brand}.*` | agent with consent |
| 19 | npm first publish, trusted publisher | developer | the package must exist; every write asks 2FA | agent packs; developer runs `npm-first-publish.sh` in Warp; agent verifies | developer |
| 20 | Arm `PUBLISH_PACKAGES`, first CI publish | agent | the `push` flag | `gh variable set`, `gh workflow run` inside npm's 2-day window; T8's `fe-v0.0.1` tag dropped | agent |
| 21 | GHCR access for Wheelhouse | developer | package settings UI | none per repo: the workflow token links the package, and the org-wide App install reads it | none |
| 22 | Dispatch compat and conformance | agent | the `push` flag | unchanged | agent |
| 23 | Catalog `deploy: wheelhouse` | agent | none | unchanged | agent |
| 24 | Wheelhouse product, settings, secrets, domains | developer | import is session-only; secret values; DNS | agent imports and binds tailnet sites in the owner's console session; developer enters third-party secrets and public DNS | split |
| 25 | Consumer sweep | agent | each consumer's flags | `repin.py` (§ 5) | agent |
| 26 | Ocharo Form 2 cutover | agent + developer | bot, secrets, DNS | unchanged | split |
| 27 | Parallel build loop | agent | — | unchanged | agent |

- T8 counts: 18 agent, 1 decision, 8 hand.
- After T9, per library: 22 agent (step 18 behind a "yes"), 1 decision, 1 hand (19), 2 split (24, 26), 1 gone (21).
- One-time, ever: the P1 directive, `wheelhouse-max` on `wow-two-sdk-beta`, removing the Codex connector (§ 2).
- T8 step 20's `fe-v0.0.1` tag is redundant: `next-version.sh fe` already takes the highest of the tags and the
  registry.

---

## 2 · Credentials model

### What exists and what each one reaches

| Credential | Lives in | Scope | Lifetime, rotation | Used for | Blast radius |
|---|---|---|---|---|---|
| `gh` OAuth token, `sulton-max` | macOS keyring, read per call with `gh auth token -u` | `repo`, `workflow`, `read:org`, `gist` | no expiry (U); revoke in GitHub settings | repo create, edit, clone; variables; dispatch; git pushes through `gh auth git-credential` | every repo in the 15 orgs the account admins; no org secrets, org Actions policy or packages |
| `GITHUB_TOKEN` | each workflow run | per job: `contents: write`, `packages: write`, `id-token: write` | the run | tags, GHCR pushes, OIDC requests | the running repo and the packages it published |
| NuGet temporary key | minted by `NuGet/login@v1` from the run's OIDC token | the policy: GitHub owner, repo, `publish-packages.yml`, package glob | 1 hour; one token, one key | `dotnet nuget push` | packages matching the policy's glob under owner `WoW2.0` |
| npm OIDC token | minted by npm ≥ 11.5.1 in CI | one package, one workflow file | one publish | `npm publish --provenance` | that package |
| npm web session | developer's machine, `npm login --auth-type=web` | the account | session; 2FA on each write | first publish, `npm trust` | developer-held |
| Wheelhouse App key (`wheelhouse-max`) | control-host file | Actions rw, Contents r, Metadata r, Packages r | replace the file | GHCR pulls, release reads | orgs it is installed on; `wow-two-sdk-beta` lacks it today |
| Wheelhouse token file | control host | classic `read:packages` | owner-set expiry | private repos' images | not needed for public domain repos |

- The minimal long-lived set needs nothing new: the developer's `gh` token and the Wheelhouse App key already exist.
- NuGet fence: one policy per repo, its package glob `WoW2.Sdk.Beta.Be.{Brand}.*`, keeps a domain repo off core's
  ids and off other domains' ids.
- Prefix: `WoW2.Sdk.Beta.Be` shows as verified with owner `WoW2.0`, so a reserved prefix already blocks squatters on
  new domain ids (U: which prefix exactly).
- npm fence: a trusted publisher binds one package to one workflow file; one configuration per package.
- GHCR fence: a package pushed with the workflow's token links to that repo and inherits its access.

### Registry facts the design rests on

- NuGet policy fields: repository owner, repository, workflow file name, optional environment.
- NuGet policy scopes choose new packages or new versions, with a glob.
- NuGet new ids are verified in our own record: 7 brand-new `WoW2.Sdk.Beta.Be*` ids first appear at `10.0.67-beta`
  (2026-10-16 18:23 UTC), pushed by be `publish.yml` through `NuGet/login@v1`.
- NuGet policy creation is UI-only in the docs; no API is documented (U).
- NuGet marks a private-repo policy temporarily active for 7 days until a publish; public repos probably activate at
  once (U).
- npm trusted publishers and `npm trust` require the package to exist.
- npm staged publishing can create a new package: it publishes a public `0.0.0-stage` placeholder, and approval asks
  2FA.
- npm expires a new trusted-publisher configuration that sees no successful publish within 2 days.
- npm `trust` needs npm ≥ 11.15.0; this machine has 11.6.1.
- npm granular tokens are created on the website only.
- npm deprecates direct publishing with bypass-2FA tokens, with removal in January 2027.
- npm removed legacy tokens in November 2025.
- GitHub Free: org-level secrets reach public repos only; managing them needs `admin:org`.
- GHCR: a new package is private; visibility changes in the UI only (U for an API).
- Wheelhouse: the App's installation token reads packages of public repos; private repos' packages need the token
  file (Wheelhouse architecture § Registry sign-in).

### Rejected long-lived secrets

| Candidate | Would buy | Cost | Verdict |
|---|---|---|---|
| Org Actions secret: NuGet key, push new, glob `WoW2.Sdk.Beta.*` | first publish without a policy | any workflow in any `wow-two-sdk-beta` repo reads it; 365-day rotation; the glob reaches core's ids | reject: trusted publishing already creates new ids |
| npm granular token, bypass 2FA, scope `@wow-two-beta` | CI first publish | direct publish with it ends January 2027; website-only creation | reject |
| npm stage-only token, scope `@wow-two-beta` | CI stages the first version; developer approves with 2FA | lowest blast radius, yet website-only creation and expiry make rotation recurring hand work for a rare event | defer: revisit if new npm packages become monthly |
| PAT in core for `repository_dispatch` | compat on each core release | stored PAT with repo write | reject, as T8 Open 4 |
| `admin:org` on the agent's `gh` token | org secrets and org Actions defaults by agent | widens every `gh` call to org settings | reject |

### Cleanup the sweep found

- be repo secret `NUGET_API_KEY`: unused since `publish.yml` moved to `NuGet/login`; delete.
- fe repo secret `NPM_TOKEN`: read only by the parked React `release.yml`; npm removed legacy tokens; delete both.
- `chatgpt-codex-connector` sits on `wow-two-sdk-beta`, `wow-two-platform` and `wow-two-apps` with all repositories
  and contents, actions and workflows write; Codex was dropped 2026-10-23.
- That app reaches every new repo the moment it exists; uninstalling it is an org setting, so the developer's.

---

## 3 · Agent permissions

### Guard verdicts today

| Command | Guard | Flag read | Note |
|---|---|---|---|
| `gh repo create o/n --public --disable-wiki -d …` | allow | `.` push (ON) | an unmatched slug falls back to the hub |
| `gh repo create o/n --source … --remote origin` | block | — | never-run list |
| `gh repo edit o/n …`, `gh api -X PUT repos/o/n/actions/permissions/workflow …` | allow | `.` before the clone, the repo's own after | correct only by ordering |
| `gh repo edit wow-two-apps/<not cloned> --visibility public` | allow | `.` push (ON) | the hole: any repo not checked out |
| `gh secret set X --org wow-two-sdk-beta` | allow | `.` push (ON) | GitHub refuses it: no `admin:org` |
| `gh repo clone o/n workbench/o/n`, `git clone <url> <path>` | allow | none | clone passes as an unlisted subcommand, not by decision |
| `git -C <repo> remote add origin …` | block | — | never-run list |
| `git -C <new repo> push -u origin main` | block | new repo push (OFF) | needs a directive today |
| `git -C <be> push -u https://github.com/o/elsewhere.git main` | allow | be push (ON) | ordinary form takes a URL; `-u` writes upstream config |
| `GH_TOKEN=… git -C <repo> push origin main` | block | — | env-prefixed pushes never match the ordinary form |
| `gh variable set …`, `gh workflow run …` on a checked-out repo | allow | that repo's push | as intended |
| `bash scripts/…` that calls `gh` inside | allow | none | the guard sees only the top-level command |

- Env-prefixed pushes are blocked, so pushes rely on the credential helper's active account (`sulton-max`).
- That reliance conflicts with the personal git rule "name the account on every HTTPS push"; the release flow
  uses bare `git -C <repo> push`.
- Auto mode refused a public push to a new remote when the instruction was relayed mid-task (memory, 2026-09-28).
- So creation and the first public push run in the chat where the developer asked for the library, never in a
  relayed subagent (U whether that still holds).

### Policy changes

| # | Change | Narrowest form | Against the personal rule | Pick |
|---|---|---|---|---|
| P1 | Folder-scope overrides | `~git_on commit,push workbench/wow-two-sdk-beta/*` records one override for every repo under the folder, present and future; precedence: repo override, longest folder, default | no new kind; consent stays a whole-message directive; narrower than the `*` default | yes |
| P2 | Fail-closed `gh` targets | an unmatched `owner/name` reads OFF; bare `gh repo create owner/name` and `POST orgs/{owner}/repos` read the flag of `workbench/{owner}/{name}` through P1 | creation stays a `push` write (risky, now used per library and per venture launch) | yes |
| P3 | Clone safe, remotes named | list `git clone` and `gh repo clone` into the workspace as safe; the ordinary push's `<remote>` must be a configured remote name | clone writes only the new repo's own `origin`; a URL push is a remote write in disguise | yes |

- Rejected: a `repo` flag kind, since creation already sits under `push` and a third kind repeats the same consent.
- Rejected: allow-listing a script by path, since the guard cannot see what a script does and a script edit would
  become a policy edit.
- Rejected: agent `git remote add`, since the clone gives `origin` without it.
- Rejected: `*` default ON, since it hands every future repo, products included, both flags.
- Rejected: `admin:org` on the agent token (§ 2).
- Org settings, app installs, repo deletion, forced pushes and pushed-history rewrites stay human, rare and risky.

### Design rule the guard implies

- Scripts make no GitHub, registry, commit or push writes.
- They print each exact command; the agent runs it as its own Bash call, so the guard judges every write.

---

## 4 · Automation design

### Entry point

| Option | For | Against |
|---|---|---|
| `create-library` skill over `scripts/release/library.py` | runs in the chat that holds consent; reuses `scaffold.sh`; resumable | — |
| a `wow` CLI verb | one human command | no such CLI exists (U); the same guard issue |
| Actions `create-library.yml` on dispatch | writes from CI | the template is local-only; needs an org-admin App key stored as a secret |
| Wheelhouse feature #9, "0→live scaffold" | a console click | the App has no Administration permission; later in Wheelhouse's order |

- Pick the skill over a script; Wheelhouse can call the same script once feature #9 arrives.
- The skill's trigger: "create library {name}", "new domain repo", "publish a new library".
- `library.py plan {slug}` is the default: it probes each step and prints a status table and the next exact commands.
- `library.py apply-local {slug}` does only local file work: scaffold, catalog edit, registry, `active.sh`, ports.
- State comes from probes, never a state file; a rerun resumes at the first unfinished step.
- Probes are read-only: `gh api` GETs, `git ls-remote`, the nuget.org flat container, `npm view`, Wheelhouse MCP
  `list_projects`.
- Inputs follow T8 § 5: repo name, Brand, `SLUG`, `PRODUCT`, `CORE_VERSION`, `FE_VERSION`; org defaults to
  `wow-two-sdk-beta`.

### Phases

| Phase | Step | Done when | Action | Runs as | Gate |
|---|---|---|---|---|---|
| 0 Preflight | flags, account, tools | `commit_permission.py status` ON for the folder; npm ≥ 11.15.0 | print the missing directive or upgrade | read | — |
| 1 GitHub | create | `gh api repos/o/n` answers 200 | `gh repo create o/n --public --disable-wiki --disable-issues -d "…"` | agent | push (P2) |
| | settings | repo fields and workflow permissions read back | `gh repo edit o/n --enable-projects=false --enable-discussions=false`; `gh api -X PUT repos/o/n/actions/permissions/workflow -f default_workflow_permissions=read` | agent | push |
| | `main` ruleset | `gh api repos/o/n/rulesets` lists it | `gh api -X POST repos/o/n/rulesets --input main-guard.json`: block force pushes and deletion | agent | push |
| | clone | `workbench/o/n/.git` has `origin` = `o/n` | `gh repo clone o/n workbench/o/n` | agent | none (P3) |
| 2 Scaffold | stamp | `product/product.json` exists | `SHAPE=domain INTO=clone scaffold.sh …` | `apply-local` | — |
| | verify | slnx tests, pnpm build, `test-next-version.sh` green | T8 § 5 commands | agent | — |
| | commit, push | `git ls-remote origin main` shows the commit | ordinary forms | agent | commit, push (P1) |
| 3 Hub | catalog, platform-apps row, registry | `gen-repo-registry.py --check` passes | `apply-local`, then a hub commit and push | agent | `.` flags |
| 4 Registries | NuGet policy | the policy shows on nuget.org | browser form in the `wow2` profile | agent | chat "yes" |
| | npm first version, trust | `npm view @wow-two-beta/fe-{slug}` and `npm trust list` answer | `npm-first-publish.sh` | developer | 2FA |
| | arm and publish | `PUBLISH_PACKAGES` true; run green; feeds list the versions | `gh variable set`; `gh workflow run publish-packages.yml`; `gh run watch` | agent | push |
| 5 Image | first image | delivery run green; release `v0.1.1` exists | none: the scaffold push built it | CI | — |
| 6 Wheelhouse | import, bind | `list_projects` shows the slug | catalog `deploy: wheelhouse`, then console import and tailnet sites | agent | browser rules |
| | secrets, public DNS | the target check passes | console entry | developer | — |
| 7 Consumers | re-pin | each consumer builds on the new pin | `repin.py`, then per-repo commit and push | agent | each repo's flags |

- `INTO=clone` makes `scaffold.sh` accept an empty clone and skip `git init`; every other pass stays.
- `main-guard.json` mirrors the never-run list on GitHub's side, with no review rule, so agent pushes still land.
- `npm-first-publish.sh {slug}`: `npm publish <tgz> --access public`, then
  `npm trust github @wow-two-beta/fe-{slug} --file publish-packages.yml --allow-publish`.
- The same script prints the agent's next command, the arm-and-publish phase, which must land inside npm's 2 days.
- Phase 4 runs when the package has its first screens (T8 step 19), not at creation, so no placeholder ships.
- Wheelhouse backlog item: an integration-key scope `catalog:import`, so phase 6 needs no browser; secrets keep no
  key path.

### Local or GitHub Actions

| Concern | Where | Why |
|---|---|---|
| Scaffold, rebrand, ports, catalog | local | the template is local-only (T8 § 1) |
| Repo create, settings, clone | local agent | needs an org-admin credential; CI holds none |
| Package build, tag, publish | `publish-packages.yml` | the registries trust that workflow's OIDC identity |
| Image | shared `delivery.yml` | pipelines own images; Wheelhouse reads the bundle |
| Compat, conformance | `core-latest.yml`, `conformance.yml` | nightly and on dispatch |
| NuGet policy, npm first version | browser, developer | UI and 2FA |
| Consumer re-pins | local agent | cross-repo writes need each repo's flag; CI has no cross-repo credential |

---

## 5 · Release flow after creation

| Event | Runs | Result | Who |
|---|---|---|---|
| a push to `main` | `publish-packages.yml` plan | job `be` and job `fe` run only for changed paths | agent pushes, CI runs |
| packages changed | job `be` or `fe` | tag `be-v10.y.z-beta` or `fe-v0.0.z` before the publish, then NuGet or npm with provenance | CI |
| code changed | `delivery.yml` | image `vX.Y.Z`, GitHub Release, bundle | CI |
| image released | Wheelhouse | dev rollout and `verify`; prod promotion | Wheelhouse, then the owner |
| nightly | `core-latest.yml` | build and test against the newest core | CI; red is a signal, not a gate |
| package published | `repin.py` | one consumer commit per repo | agent |

- Tags come from CI only; an agent never creates or pushes a release tag.
- A rerun is `gh workflow run publish-packages.yml`; a failed publish burns its number (T8 § 3).
- No release commit means no release-sync wait or `pull --ff-only` after a domain repo push.
- A red compat run surfaces through `gh run list -w core-latest.yml`; the fix lands as a domain-repo commit.
- Renovate is configured but inert: no wow2 org has the Mend app, and wheelhouse, be and pipelines show zero
  Renovate pull requests.
- Products work on `main` with no pull requests, so re-pins are commits, as in the 2026-10-20 sweep of 25 repos.
- `repin.py --package <id or glob> --version <v>` finds consumers through the catalog checkouts and edits
  `Directory.Packages.props` or `package.json`.
- It then builds and tests each one and prints the commit and push; repos with a flag OFF wait for a directive.
- Sweep order follows T8 step 25: pilots, Wheelhouse, Haven, ForeverPin, TranscriptForge; Ocharo in its own chat.
- Prod promotion of a domain service stays the owner's; only Wheelhouse itself is the agent's to promote.

---

## 6 · What stays human

| Residue | When | Why it stays | Cost |
|---|---|---|---|
| Decisions: queue A, package cut | per library | judgment | — |
| P1 directive for `workbench/wow-two-sdk-beta/*` | once | flags change only by directive | one message |
| NuGet policy consent | per repo | an account setting through a UI; consent per action | one "yes", or a minute by hand |
| npm first version and `npm trust` | per new npm package | 2FA on each write; trust needs the package | about 3 minutes in Warp |
| `wheelhouse-max` on `wow-two-sdk-beta`, all repositories | once | an app install grants permissions | a minute |
| Codex connector removal | once | org setting | a minute |
| Third-party secret values | per product | secrets never pass through an agent | varies |
| Public DNS and domain binding | per public site | Wheelhouse domain binding is unbuilt (iteration 11) | varies |
| Prod promotion of the service | per release | other products' prod is the owner's | a typed confirm |

- Never by agent, whatever the flags: forced or deleting pushes, repo deletion, pushed-history rewrites, org settings,
  2FA approvals.

---

## Open

1. Flag scope for new libraries: a folder override (P1), a per-repo `~git_on` each time, or the `*` default ON?
   - Pick P1: one directive, fenced to `workbench/wow-two-sdk-beta/`, products untouched.
2. Guard tightening: apply P2 (fail-closed `gh` targets, creation mapped to the future checkout) and P3 (clone safe,
   named-remote pushes) together?
   - Pick yes: they close two live holes and are what make creation agent-safe.
3. NuGet policy per repo: the agent fills the nuget.org form in the `wow2` Chrome profile after a chat "yes", or the
   developer by hand?
   - Pick the agent with consent; the developer's minute stays the fallback.
4. GHCR pulls for `wow-two-sdk-beta`: install `wheelhouse-max` on the org with all repositories, or make each image
   public?
   - Pick the App install: once per org, no one-way visibility change per package.
5. Consumer re-pins: the agent's `repin.py` sweep, or installing Mend Renovate on the orgs?
   - Pick the sweep: products take commits on `main`, and the private preset waits for the owner's ticks.

---

## Sources

- [T8 — Domain library repo template](t8-library-template.md) — § 3 CI, § 5 `create-repo`, § 6 rollout.
- [Repository git flags adapter](../../.claude/commit-permission.md) and `W/.claude/hooks/guard-git.py`,
  `commit_permission.py` — target mapping, ordinary forms, never-run list.
- [Workspace git protocol](../../conventions/development/repo/version-control/git.md) and
  [personal git conventions](/Users/max/.claude/conventions/git.md#repository-commit-permission).
- [Git flags analysis](../../docs/git-flags.md) — G0–G7.
- `W/workbench/wow-two-sdk-beta/wow-two-sdk-beta.be/.github/workflows/publish.yml` — `NuGet/login@v1`, user `MaxDev`.
- `W/workbench/wow-two-sdk-beta/wow-two-sdk-beta.fe/.github/workflows/release-fe.yml`, `release.yml`.
- `W/workbench/wow-two-platform/wow-two-platform.pipelines/.github/workflows/publish.yml`, `generator/release.py`.
- Wheelhouse `engineering/architecture/architecture.md` (§ Registry sign-in, § Catalog hubs, MCP),
  `engineering/deployment/deployment.md` (§ GitHub access), `engineering/deployment/vps/vps.md` (§ 6),
  `product/context.md`, and [wheelhouse spec](../wheelhouse-spec.md) feature #9.
- `W/.claude/skills/create-repo/` (`SKILL.md`, `scaffold.sh`), `W/scripts/clone-all.sh`, `catalog-checkouts.py`,
  `gen-repo-registry.py`.
- Read-only reads, 2026-10-25: `gh` token scopes; org installations on `wow-two-sdk-beta`, `wow-two-platform`,
  `wow-two-apps`; be repo settings and secrets; fe secrets; Renovate pull requests; `commit_permission.py status`.
- nuget.org: `https://api.nuget.org/v3-flatcontainer/wow2.sdk.beta.be/index.json`, the registration index, and the
  search API's `verified` flag.
- [NuGet Trusted Publishing](https://learn.microsoft.com/en-us/nuget/nuget-org/trusted-publishing).
- [NuGet scoped API keys](https://learn.microsoft.com/en-us/nuget/nuget-org/scoped-api-keys).
- [npm trusted publishers](https://docs.npmjs.com/trusted-publishers).
- [npm trust](https://docs.npmjs.com/cli/v11/commands/npm-trust).
- [npm staged publishing](https://docs.npmjs.com/staged-publishing).
- [npm access tokens](https://docs.npmjs.com/about-access-tokens) and
  [creating tokens](https://docs.npmjs.com/creating-and-viewing-access-tokens).
- [GitHub Actions secrets](https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/use-secrets).
- [GHCR access control and visibility](https://docs.github.com/en/packages/learn-github-packages/configuring-a-packages-access-control-and-visibility)
  and [working with the Container registry](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry).

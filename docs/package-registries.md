# Package registries

*Last updated: 2026-10-27*

> Who may publish what on nuget.org and npm: every trusted-publishing policy and publisher, with enough detail to
> recreate each one after losing a policy, a repository or an account. No secret lives here; workflows publish through
> OIDC, and the accounts sign in with the owner's passkey or 2FA.

## NuGet (nuget.org)

- Account `MaxDev`, a member of the organization `WoW2.0`, which owns every package; the `WoW2.*` prefix is reserved
  to it, so a first push creates a new id with no registry step.
- Sign-in: Sign in with Microsoft, the owner's email, then the owner's passkey; no password and no code
  (`~/.claude/conventions/tools/browser.md` § Claude in Chrome).
- Workflows exchange their OIDC token with `NuGet/login` as `user: MaxDev`.

| Policy | Package owner | Repository | Workflow | Scopes | Globs |
|---|---|---|---|---|---|
| `wow-two-beta-be-publish` | `WoW2.0` | `wow-two-sdk-beta/wow-two-sdk-beta.be` | `publish.yml` | push new packages and versions · unlist or relist | `*` |
| `wow-two-beta-identity-publish` | `WoW2.0` | `wow-two-sdk-beta/wow-two-sdk-beta.identity` | `publish-packages.yml` | push new packages and versions · unlist or relist | `WoW2.Sdk.Beta.Be.Identity.*` |

- Every policy: CI provider GitHub Actions, no environment.
- A domain library adds its row when its policy is created (`create-library` phase 4), then sets the repository
  variable `PUBLISH_PACKAGES=true`; Files and Harvest have neither yet.
- Unlisting runs through each publish workflow's `unlist` input ([domain structure](../conventions/development/repo/structure/domain-structure.md)
  § Releases); relisting is nuget.org's web UI.

### Recreate a policy

1. nuget.org → Trusted Publishing → Create: the row's name, package owner, repository owner and name, workflow file,
   both scopes (push new packages and versions; unlist or relist) and its globs.
2. Editing a policy blanks its globs field: enter the row's globs again before Save.
3. A policy binds the repository's permanent GitHub id, so a repository deleted and created again needs a new policy.

## npm

- Scope `@wow-two-beta`, held by the owner's npm account with 2FA.
- A package's first version is published by hand, then `npm trust github <package> --file <workflow> --repo
  <owner/repo> --allow-publish` (npm ≥ 11.15) adds its trusted publisher; later versions publish from CI with
  provenance. npm drops a trusted publisher that publishes nothing within two days, so CI publishes right after.

| Package | Repository | Workflow | Publishes by | State |
|---|---|---|---|---|
| `@wow-two-beta/fe` | `wow-two-sdk-beta/wow-two-sdk-beta.fe` | `release-fe.yml` | trusted publisher | live, `0.0.33` |
| `@wow-two-beta/ui-vue` | — | — | — | the fe sdk's earlier name, frozen at `0.0.17` |
| `@wow-two-beta/ui` | `wow-two-sdk-beta/wow-two-sdk-beta.fe` | `release.yml` | the stored `NPM_TOKEN` secret | parked React SDK, `0.0.108`; the token is release residue (T9) |
| `@wow-two-beta/fe-identity` | `wow-two-sdk-beta/wow-two-sdk-beta.identity` | `publish-packages.yml` | trusted publisher, after the first version | not published: still the template's sample |
| `@wow-two-beta/fe-files` | `wow-two-sdk-beta/wow-two-sdk-beta.files` | `publish-packages.yml` | trusted publisher, after the first version | not published |
| `@wow-two-beta/fe-harvest` | `wow-two-sdk-beta/wow-two-sdk-beta.harvest` | `publish-packages.yml` | trusted publisher, after the first version | not published |

- The publisher settings above come from the workflow files; `npm trust list <package>` (signed in) confirms them.

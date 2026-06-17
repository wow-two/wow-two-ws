# session: onboard-member

*Last updated: 2026-06-17*

> SOP for inviting, onboarding, and offboarding a volunteer contributor to wow-two — one trusted person at a time, zero team ceremony.
> Purpose — make onboarding repeatable and collision-free, so a second pair of hands speeds delivery instead of adding coordination tax.
> Use case — reach for this whenever adding or removing a contributor on any wow-two org repo.

- State / live roster: [context.md](./context.md) ← read first
- Per-repo plans: `engineering/planning/{planning,backlog,rules}.md` (shape: `conventions/planning/engineering-planning/`)
- Copy-ready templates: `.claude/rules/templates/onboarding-{start-here,planning-board,quickstart}.md`
- **Status channel** (set once): GitHub repo Issues — recommended, co-located + async — or a Telegram thread.
  Async status, lib requests, API-seam coordination land here. No standup.

Recommended chat name: `wow-two - onboard-{member}`.

---

## Philosophy

- **Trust-scaled, not team-scaled.** One known person → no branch protection / RFCs / CODEOWNERS / required reviews.
  Importing team ceremony for one volunteer is the #1 failure mode.
- **Ownership split with ≈zero shared files** beats two devs on one file — each owns a vertical, overlap ≈ 0.
- **Fix-forward.** Break it, you fix it. The net is a CI-green signal + owner-only lib bumps, not gates.

---

## The model — ownership split

| Lane | Owner | Scope |
|---|---|---|
| App **frontends** | Contributor | `engineering/codebase/{slug}.frontend-services/` only |
| App **backends / infra** | You | `{slug}.backend-services/` + deploy/SSH |
| Beta **libs** | You | `wow-two-sdk-beta.ui`, `wow-two-sdk.backend.beta` — incl. version bumps |

- Contributor consumes libs as **published packages**; never edits libs or backends. (Stated once = the collision-free guarantee.)
- **One live seam:** `drydock` frontend ↔ backend **API contract** — coordinate on the status channel.
- **Blocked on a lib?** Contributor posts the needed API on the channel → you change + bump the beta lib → they re-pull.
  Caret-pin (`^0.0.x`) means the bump reaches their app on next install. The wall has a gate; they never edit the lib.
- **Multiplier:** each task = a scoped Claude session on the repo's `CLAUDE.md`. One trusted dev + Claude per vertical ≫ two devs on one file.

---

## Procedure

Read [context.md](./context.md) (live roster) first. Two flows: pre-invite (you) → first session (them).

### Pre-invite checklist — run in order (longest lead first)

1. **Org invite + package read.** Add member to the org holding their repos (`wow-two-platform`); grant package-registry
   **read** only for repos that consume a lib — `drydock` does (`@wow-two-beta/ui` `^0.0.56`), `secrets-vault` doesn't yet.
2. **Seed starter backlogs.** 3–5 scoped one-day items at the **top** of each repo's `backlog.md`.
   `drydock`: swap a hand-rolled component to the beta `ui` lib (dogfoods it).
   `secrets-vault`: a frontend task needing no ui-lib (it doesn't consume one). No starters = no first task.
3. **Establish the status channel** (above) and tell the contributor where it is.
4. **Write entry docs** from templates: `wow-two-ws/PLANNING.md` (board) + paste `## Start here` into each repo's `CLAUDE.md`.
5. **Add build-only CI** to repos with none — `dotnet build` + `test`, no publish.
   `drydock` has no `.github/` at all (create fresh); `secrets-vault` has only `publish-docker-image.yml`.
6. **Fix dangling pointers** in repos they'll read (e.g. the `backend.beta` planning pointer).
7. **Write `wow-two-ws/ONBOARDING.md`** from the quickstart template; **dry-run `scripts/setup.sh`** yourself as the contributor before inviting.

### First session (them)

- They follow `ONBOARDING.md`: `setup.sh` → verify `ls workbench/` → `active.sh` → read `PLANNING.md` →
  pick **top** of their repo `backlog.md`. You pair on the first task end-to-end. After that, async on the channel.

---

## Offboarding — revoke in order

1. **Remove org membership** → kills repo access + package read in one step.
2. **Local clones persist** (revocation doesn't un-clone) → rotate any dev secret/credential they could have seen.
3. If they ever held `secrets-vault` locally → treat all dev-fixture secrets as compromised, rotate.
4. `context.md` roster → Stage = `offboarded` + date.

---

## Gates & scaling

Lean shape holds for **1 trusted dev** (CI-green + owner-only lib bumps = the whole net). When a 2nd untrusted
contributor or external PRs arrive → revisit `docs/branching-strategy.md` for `main` protection + CODEOWNERS.
Don't add gates before the trigger fires.

---

## Workspace gotchas

| Gotcha | Why it bites | Mitigation |
|---|---|---|
| **Two-layer git** | `workbench/` gitignored; each repo own `.git` | Commit inside the repo, never from workspace root |
| **Silent partial clone** | `gh repo list <org>` returns empty (not error) without membership | Verify `ls workbench/` shows their repos |
| **Folder ≠ org** | local folder ≠ remote org (`*.backend.beta` under `wow-two-sdk-beta/`, remote `wow-two-sdk`) | Note before access checks |
| **Secrets material** | `secrets-vault` is a vault | Frontend tasks run on local/dev fixtures only — no prod vault access |

---

## What lives where

| Concern | File | Volatility |
|---|---|---|
| Procedure (this) | `session-onboard-member.md` | Almost never |
| Live roster + prep status | `context.md` | Per-member |
| Entry board · quickstart · start-here | `.claude/rules/templates/onboarding-*.md` → `wow-two-ws/{PLANNING,ONBOARDING}.md`, repo `CLAUDE.md` | Rare |
| Per-repo plan + queue | repo's `engineering/planning/{planning,backlog,rules}.md` (contributor's lane; beta-libs need none) | Frequent |
| Branch / publish model | `docs/branching-strategy.md` | Rare |

---

## context.md scope

**In scope**: current member(s) + repos/lane/stage, prep-artifact status, status channel, open items, last action.
**Out of scope**: the procedure (here), per-task detail (repo backlogs), long reasoning.

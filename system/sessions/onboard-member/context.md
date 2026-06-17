# onboard-member — context

*Last updated: 2026-06-17*

> 30-second snapshot. Procedure + templates in [session-onboard-member.md](./session-onboard-member.md).

## Roster

| Member | Repos (lane) | Stage |
|---|---|---|
| Mentee #1 (TBD) | `secrets-vault` + `drydock` → **frontends only** (`{slug}.frontend-services/`) | Pre-invite |

## Status channel

- TBD — pick GitHub repo Issues (recommended) or a Telegram thread before inviting (SOP step 3).

## Prep status — Mentee #1

Pre-invite checklist (SOP → *Pre-invite checklist*). None executed — SOP authored first.

| # | Step | Status |
|---|---|---|
| 1 | Org invite (`wow-two-platform`) + `@wow-two-beta/ui` read (drydock only — secrets-vault doesn't consume it) | ☐ |
| 2 | Seed 3–5 frontend starters atop `drydock` + `secrets-vault` `backlog.md` | ☐ — both backlogs owner-infra only, no frontend starters |
| 3 | Establish + name the status channel | ☐ |
| 4 | `wow-two-ws/PLANNING.md` board + `## Start here` in both repo `CLAUDE.md` | ☐ |
| 5 | `build.yml` (build+test, no publish) → `drydock` (no `.github/` — create fresh); `secrets-vault` has only `publish-docker-image.yml` | ☐ |
| 6 | Fix `backend.beta` dangling planning pointer | ☐ |
| 7 | `wow-two-ws/ONBOARDING.md` quickstart + dry-run `scripts/setup.sh` as the mentee | ☐ |

Step 1 (org invite) is the owner's to action — longest lead, do first.

## Owned lanes (you)

- Beta libs: `wow-two-sdk-beta.ui`, `wow-two-sdk.backend.beta` — incl. version bumps.
- App backends: `secrets-vault.backend-services`, `drydock.backend-services` + deploy/SSH.

## Live seam

- `drydock` frontend ↔ backend **API contract** — the one interface to coordinate async.

## Open items

- Confirm mentee identity, pick the status channel, and draft the 3–5 frontend starters per repo before running the checklist.
- Decide whether to execute the pre-invite edits (prior session offered steps 2–7) or keep SOP-only.

## Log

- **2026-06-17:** SOP authored + verified (4-reviewer pass, 17 findings folded in: slimmed, templates moved to
  `.claude/rules/templates/`, added offboarding + status channel + lib-escalation, fixed 2 fact errors).
  No product-repo edits — session goal = document as SOP.

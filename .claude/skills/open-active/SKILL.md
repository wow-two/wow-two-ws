---
name: open-active
description: >-
  Open the user's active working set of wow-two projects in the right JetBrains IDE — Rider for
  .NET backends, WebStorm for frontends — by running scripts/active.sh in this workspace. Use this
  whenever the user wants to open, launch, fire up, boot, or "spin up" their active projects /
  working set / "the repos I'm working on" / "everything I'm working on" in their IDEs, or to open
  specific named projects (e.g. "open drydock and smart-qr in the IDEs", "just the frontends", "open
  all my backends in Rider", "list what I'm working on"). Trigger even when the user does NOT say
  "active.sh" or name the IDEs — phrases like "open my projects", "fire up my workspace", "boot up
  everything I'm building" should use this skill. Covers opening all, opening a subset, backend-only
  / frontend-only, listing the set, and dry-running the open plan.
---

# open-active

Opens the active working set in the correct JetBrains IDE (**Rider** for .NET backends, **WebStorm**
for frontends) via the workspace script `scripts/active.sh`.

## Source of truth

`scripts/active.sh` owns the curated registry (`name | backend | frontend`) across all orgs
(`ventures/`, `wow-two-platform/`, `wow-two-sdk-beta/`) and all the launch logic (Toolbox
`rider`/`webstorm` with an `open -na` fallback, skip-missing, staggering). **Do not duplicate the
project list here** — run the script. To change what counts as "active", edit the `PROJECTS` array
at the top of `scripts/active.sh`.

## How to run it

Run from the workspace root. The script resolves its own paths, so the working directory only
affects how you spell the path.

| The user wants… | Command |
|---|---|
| Everything (all backends + frontends) | `scripts/active.sh` |
| Backends only (Rider) | `scripts/active.sh -b` |
| Frontends only (WebStorm) | `scripts/active.sh -f` |
| Specific projects | `scripts/active.sh <name> [<name>…]` |
| Specific projects, one side | combine, e.g. `scripts/active.sh -f drydock smart-qr` |
| See the set + what exists (✓/✗) | `scripts/active.sh -l` |
| Preview, launch nothing | `scripts/active.sh -n` |
| Stagger launches | `DELAY=1 scripts/active.sh` |

Project names are the first column of `scripts/active.sh -l` — currently `drydock`, `secrets-vault`,
`smart-qr`, `trademark-watcher`, `acquisition-explorer`, `yt-scraper`, `pdf-editor`, `backend-beta`,
`frontend-beta`. Map fuzzy references to these (e.g. "the QR thing" → `smart-qr`, "yt scraper" →
`yt-scraper`, "the beta libs" → `backend-beta frontend-beta`).

## Default behavior: preview before the swarm

Opening *all* projects launches ~13 IDE windows. Unless the user clearly says "just open them" (or
asks for a small named subset), **run the dry-run first** (`scripts/active.sh -n`), show the plan,
and confirm before the real launch. The point is to avoid blanketing the dock with IDE windows the
user didn't mean to open. For an explicitly small request ("open drydock", "just smart-qr's
frontend"), skip the preview and run it directly.

## Notes

- Requires Rider + WebStorm installed via JetBrains Toolbox; the script auto-detects the launchers.
- Some projects are one-sided and the script opens whatever exists: `trademark-watcher` and
  `pdf-editor` are backend-only; `acquisition-explorer` and `frontend-beta` are frontend-only.
- After launching, remind the user that each IDE is one app with many project windows
  (WebStorm's frontends share one dock icon) — `⌃→` / Mission Control corrals them.

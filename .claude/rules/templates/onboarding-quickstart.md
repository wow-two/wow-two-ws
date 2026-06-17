# Template — `wow-two-ws/ONBOARDING.md` (contributor quickstart)

*Last updated: 2026-06-17*

> Contributor-facing. Emit to `wow-two-ws/ONBOARDING.md`. Replace `{status channel}` before sending.

---

# Onboarding — wow-two

1. **Prereqs:** git · `gh auth login` · .NET SDK · Node. Confirm org membership (invite email).
2. **Clone everything:** `bash scripts/setup.sh` → clones `10x-ws` + all org repos into `workbench/`.
3. **Verify:** `ls workbench/` shows your repos. Empty = membership/clone issue (not a no-op) — ping owner.
4. **Open IDEs:** `bash scripts/active.sh` → Rider (backends) / WebStorm (frontends).
5. **Orient:** `PLANNING.md` (your lane + board) → your repo's `CLAUDE.md` → `## Start here`.
6. **First task:** top of your repo's `engineering/planning/backlog.md`. Owner pairs with you end-to-end.
7. **Rhythm:** scoped Claude session per task, anchored on the repo's `CLAUDE.md`. Async on {status channel}, no standup.

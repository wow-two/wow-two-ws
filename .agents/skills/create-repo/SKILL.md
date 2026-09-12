---
name: create-repo
description: >-
  Scaffold a NEW conformant product / venture repo for the wow-two workspace — copies the standard
  product-template's example product (a complete Clean-Arch .NET 10 backend + React 19 / Vite frontend
  under engineering/codebase/, single-host serving, Docker) and rebrands it to the new name, then git
  init + registration in scripts/active.sh. Use this whenever the user wants to create / start / spin up
  / bootstrap / set up a new repo, project, product, venture, app, service, or POC in this workspace
  (e.g. "create a new repo for X", "scaffold a new venture", "start a new product repo", "spin up a new
  backend+frontend repo", "bootstrap a conformant repo named foo", "new wow-two-platform repo"). Trigger
  even when the user does NOT name the template, the IDE, or "conformant" — phrases like "make me a new
  repo for a QR tool" should use this skill. Covers single-service (default) and multi-service shapes.
---

# create-repo — Codex entry point

*Last updated: 2026-09-09 06:57 PM*

Read and follow [the shared skill](../../../.claude/skills/create-repo/SKILL.md) when this skill is invoked. Apply instructions addressed to Claude to Codex. Resolve relative references from the shared skill directory; preserve `.claude/` script and template paths.

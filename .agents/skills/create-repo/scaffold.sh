#!/usr/bin/env bash
#
# Codex entry point — the one scaffold lives in .claude/skills/create-repo/scaffold.sh; this wrapper only delegates
# to it, so the two entry points never drift. Same arguments: scaffold.sh <repo-name> <Brand> <org> [single|multi]
set -euo pipefail

exec "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/../../../.claude/skills/create-repo/scaffold.sh" "$@"

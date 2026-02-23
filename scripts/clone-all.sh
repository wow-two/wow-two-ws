#!/usr/bin/env bash
#
# clone-all.sh — Clone all WoW 2.0 repos into the workspace folder structure.
#
# Usage:
#   ./scripts/clone-all.sh              # Clone using HTTPS
#   ./scripts/clone-all.sh --ssh        # Clone using SSH
#   ./scripts/clone-all.sh --dry-run    # Show what would be cloned without doing it
#
# Prerequisites:
#   - git
#   - gh CLI (GitHub CLI) — used to dynamically list repos per org
#     Install: https://cli.github.com/
#   - Authenticated with `gh auth login`

set -euo pipefail

# ── Config ──────────────────────────────────────────────────────────────────

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Org → local folder mapping
declare -A ORG_FOLDERS=(
  ["wow-two"]="meta"
  ["wow-two-platform"]="platform"
  ["wow-two-sdk"]="sdk"
  ["wow-two-kb"]="kb"
  ["wow-two-apps"]="apps"
)

ORGS=("wow-two" "wow-two-platform" "wow-two-sdk" "wow-two-kb" "wow-two-apps")

# ── Parse args ──────────────────────────────────────────────────────────────

USE_SSH=false
DRY_RUN=false

for arg in "$@"; do
  case "$arg" in
    --ssh)     USE_SSH=true ;;
    --dry-run) DRY_RUN=true ;;
    --help|-h)
      echo "Usage: $0 [--ssh] [--dry-run]"
      echo "  --ssh      Use SSH URLs instead of HTTPS"
      echo "  --dry-run  Show what would be cloned without doing it"
      exit 0
      ;;
    *) echo "Unknown option: $arg"; exit 1 ;;
  esac
done

# ── Helpers ─────────────────────────────────────────────────────────────────

log()  { echo "  $1"; }
info() { echo "▸ $1"; }
ok()   { echo "  ✓ $1"; }
skip() { echo "  ⊘ $1 (already exists)"; }
err()  { echo "  ✗ $1" >&2; }

clone_url() {
  local org="$1" repo="$2"
  if $USE_SSH; then
    echo "git@github.com:${org}/${repo}.git"
  else
    echo "https://github.com/${org}/${repo}.git"
  fi
}

# ── Preflight ───────────────────────────────────────────────────────────────

if ! command -v gh &>/dev/null; then
  err "GitHub CLI (gh) not found. Install from https://cli.github.com/"
  exit 1
fi

if ! gh auth status &>/dev/null 2>&1; then
  err "Not authenticated with GitHub CLI. Run: gh auth login"
  exit 1
fi

# ── Main ────────────────────────────────────────────────────────────────────

echo ""
echo "╔══════════════════════════════════════════╗"
echo "║  WoW 2.0 — Clone All Repos              ║"
echo "╚══════════════════════════════════════════╝"
echo ""
echo "Workspace: $WORKSPACE_ROOT"
echo "Protocol:  $($USE_SSH && echo "SSH" || echo "HTTPS")"
$DRY_RUN && echo "Mode:      DRY RUN (no changes)"
echo ""

total_cloned=0
total_skipped=0
total_failed=0

for org in "${ORGS[@]}"; do
  folder="${ORG_FOLDERS[$org]}"
  target_dir="$WORKSPACE_ROOT/$folder"

  info "Organization: $org → $folder/"

  # Create org folder
  if ! $DRY_RUN; then
    mkdir -p "$target_dir"
  fi

  # List all repos in the org
  repos=$(gh repo list "$org" --limit 100 --json name --jq '.[].name' 2>/dev/null || true)

  if [ -z "$repos" ]; then
    log "No repos found (or no access)"
    echo ""
    continue
  fi

  while IFS= read -r repo; do
    repo_path="$target_dir/$repo"
    url=$(clone_url "$org" "$repo")

    if [ -d "$repo_path" ]; then
      skip "$repo"
      ((total_skipped++))
    elif $DRY_RUN; then
      log "Would clone: $url → $folder/$repo"
      ((total_cloned++))
    else
      if git clone --quiet "$url" "$repo_path" 2>/dev/null; then
        ok "$repo"
        ((total_cloned++))
      else
        err "Failed to clone $repo"
        ((total_failed++))
      fi
    fi
  done <<< "$repos"

  echo ""
done

# ── Summary ─────────────────────────────────────────────────────────────────

echo "─────────────────────────────────────────"
echo "Summary:"
echo "  Cloned:  $total_cloned"
echo "  Skipped: $total_skipped"
echo "  Failed:  $total_failed"
echo "─────────────────────────────────────────"
echo ""

if [ "$total_failed" -gt 0 ]; then
  echo "Some repos failed to clone. Check access permissions or run with --ssh."
  exit 1
fi

echo "Done! Open the workspace root in your editor to get started."

#!/usr/bin/env bash
#
# clone-all.sh — Bootstrap the WoW 2.0 workspace.
#
# Clones the workspace repo first (if not already inside it),
# then clones all org repos into the correct folder structure.
#
# Usage:
#   # Standalone (e.g. downloaded via curl):
#   ./clone-all.sh                  # Clone workspace + all repos (HTTPS)
#   ./clone-all.sh --ssh            # Clone using SSH
#   ./clone-all.sh --dry-run        # Preview without cloning
#
#   # From inside the workspace:
#   ./scripts/clone-all.sh          # Only clone org repos
#
# Prerequisites:
#   - git
#   - gh CLI (GitHub CLI) — https://cli.github.com/
#   - Authenticated with `gh auth login`

set -euo pipefail

# ── Config ──────────────────────────────────────────────────────────────────

WORKSPACE_REPO_ORG="wow-two"
WORKSPACE_REPO_NAME="wow-two-workspace"

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

if ! command -v git &>/dev/null; then
  err "git not found. Install git first."
  exit 1
fi

if ! command -v gh &>/dev/null; then
  err "GitHub CLI (gh) not found. Install from https://cli.github.com/"
  exit 1
fi

if ! gh auth status &>/dev/null 2>&1; then
  err "Not authenticated with GitHub CLI. Run: gh auth login"
  exit 1
fi

# ── Step 1: Clone workspace repo (if running standalone) ───────────────────

echo ""
echo "╔══════════════════════════════════════════╗"
echo "║  WoW 2.0 — Clone All Repos              ║"
echo "╚══════════════════════════════════════════╝"
echo ""
echo "Protocol:  $($USE_SSH && echo "SSH" || echo "HTTPS")"
$DRY_RUN && echo "Mode:      DRY RUN (no changes)"
echo ""

# Detect if we're already inside the workspace repo
WORKSPACE_ROOT=""

if [ -f "CLAUDE.md" ] && [ -d ".claude/rules" ]; then
  # Running from workspace root (e.g. ./scripts/clone-all.sh from parent)
  WORKSPACE_ROOT="$(pwd)"
  info "Already inside workspace: $WORKSPACE_ROOT"
elif [ -f "../CLAUDE.md" ] && [ -d "../.claude/rules" ]; then
  # Running from scripts/ folder
  WORKSPACE_ROOT="$(cd .. && pwd)"
  info "Already inside workspace: $WORKSPACE_ROOT"
elif [ -d "$WORKSPACE_REPO_NAME" ] && [ -f "$WORKSPACE_REPO_NAME/CLAUDE.md" ]; then
  # Workspace already cloned next to us
  WORKSPACE_ROOT="$(cd "$WORKSPACE_REPO_NAME" && pwd)"
  skip "Workspace repo $WORKSPACE_REPO_NAME"
else
  # Clone workspace repo
  info "Cloning workspace repo..."
  url=$(clone_url "$WORKSPACE_REPO_ORG" "$WORKSPACE_REPO_NAME")

  if $DRY_RUN; then
    log "Would clone: $url → $WORKSPACE_REPO_NAME/"
    WORKSPACE_ROOT="$(pwd)/$WORKSPACE_REPO_NAME"
  else
    if git clone --quiet "$url" "$WORKSPACE_REPO_NAME"; then
      ok "Workspace repo cloned → $WORKSPACE_REPO_NAME/"
      WORKSPACE_ROOT="$(cd "$WORKSPACE_REPO_NAME" && pwd)"
    else
      err "Failed to clone workspace repo"
      exit 1
    fi
  fi
fi

echo "Workspace: $WORKSPACE_ROOT"
echo ""

# ── Step 2: Clone all org repos ────────────────────────────────────────────

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

  # List all repos in the org (exclude the workspace repo itself)
  repos=$(gh repo list "$org" --limit 100 --json name --jq '.[].name' 2>/dev/null || true)

  if [ -z "$repos" ]; then
    log "No repos found (or no access)"
    echo ""
    continue
  fi

  while IFS= read -r repo; do
    # Skip the workspace repo — it's the parent, not a child
    if [ "$repo" = "$WORKSPACE_REPO_NAME" ]; then
      continue
    fi

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

echo "Done! Open $WORKSPACE_ROOT in your editor to get started."

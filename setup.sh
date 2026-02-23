#!/usr/bin/env bash
# WoW 2.0 — Quick Setup
# Run this anywhere to bootstrap the full workspace.
#
# Usage:
#   curl -sLO https://raw.githubusercontent.com/wow-two/wow-two-workspace/main/setup.sh && bash setup.sh
#   bash setup.sh --ssh        # Use SSH instead of HTTPS
#   bash setup.sh --dry-run    # Preview only

set -euo pipefail

USE_SSH=false
DRY_RUN=false

for arg in "$@"; do
  case "$arg" in
    --ssh)     USE_SSH=true ;;
    --dry-run) DRY_RUN=true ;;
    --help|-h) echo "Usage: $0 [--ssh] [--dry-run]"; exit 0 ;;
    *) echo "Unknown option: $arg"; exit 1 ;;
  esac
done

REPO="wow-two/wow-two-workspace"
DIR="wow-two-workspace"

echo ""
echo "╔══════════════════════════════════════════╗"
echo "║  WoW 2.0 — Quick Setup                  ║"
echo "╚══════════════════════════════════════════╝"
echo ""

# Step 1: Clone workspace repo
if [ -d "$DIR" ] && [ -f "$DIR/CLAUDE.md" ]; then
  echo "⊘ Workspace already exists at ./$DIR"
else
  echo "▸ Cloning workspace repo..."
  if $USE_SSH; then
    url="git@github.com:${REPO}.git"
  else
    url="https://github.com/${REPO}.git"
  fi
  if $DRY_RUN; then
    echo "  Would clone: $url → $DIR/"
  else
    git clone --quiet "$url" "$DIR"
    echo "  ✓ Workspace cloned"
  fi
fi

echo ""

# Step 2: Run the full clone script
if $DRY_RUN; then
  echo "▸ Would run: ./$DIR/scripts/clone-all.sh $*"
else
  cd "$DIR"
  bash scripts/clone-all.sh "$@"
fi

#!/usr/bin/env bash
#
# active.sh — open the current ACTIVE working set in the right JetBrains IDE.
#   Rider    ← .NET backends (.sln / .slnx)
#   WebStorm ← frontends (the package.json folder)
#
# Spans all orgs under workbench/ (ventures + platform + sdk-beta) — unlike
# ventures.sh, which only covers workbench/ventures/. The registry below is the
# curated set of "things I'm working on right now"; edit it as focus shifts.
#
# Usage:
#   active.sh                       open every project (backend + frontend)
#   active.sh -b | --backend        backends only (Rider)
#   active.sh -f | --frontend       frontends only (WebStorm)
#   active.sh -l | --list           show the registry + which targets exist
#   active.sh -n | --dry-run        print what would open, launch nothing
#   active.sh drydock smart-qr      only the named projects (any flag still applies)
#   active.sh -h | --help
#
# Env:
#   DELAY=<secs>   stagger between launches (default 0.4; 0 = fire all at once)
#   RIDER=…/rider  WEBSTORM=…/webstorm   override launcher paths

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WS_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
WB="$WS_DIR/workbench"

JB="$HOME/Library/Application Support/JetBrains/Toolbox/scripts"
RIDER="${RIDER:-$JB/rider}"
WEBSTORM="${WEBSTORM:-$JB/webstorm}"
DELAY="${DELAY:-0.4}"

# Registry — one line per project:  name | backend | frontend
#   backend  = .sln/.slnx path relative to workbench/, or '-' if none
#   frontend = folder (with package.json) relative to workbench/, or '-' if none
PROJECTS=(
  "drydock|wow-two-platform/wow-two-platform.drydock/engineering/codebase/drydock.backend-services/Drydock.slnx|wow-two-platform/wow-two-platform.drydock/engineering/codebase/drydock.frontend-services"
  "secrets-vault|wow-two-platform/wow-two-platform.secrets-vault/engineering/codebase/secrets-vault.backend-services/Wow-Two-Platform.Secrets-Vault.sln|wow-two-platform/wow-two-platform.secrets-vault/engineering/codebase/secrets-vault.frontend-services"
  "smart-qr|ventures/smart-qr-poc/platform/src/backend/SmartQr.sln|ventures/smart-qr-poc/platform/src/frontend"
  "trademark-watcher|ventures/trademark-watcher-poc/platform/src/backend/Trademark.Watcher.sln|-"
  "acquisition-explorer|-|ventures/acquisition-explorer-poc/platform/acquisition-explorer-frontend"
  "yt-scraper|ventures/yt-transcripts-poc/platform/src/backend/Yt.Transcripts.Poc.sln|ventures/yt-transcripts-poc/platform/src/yt-scraper.frontend-services/web"
  "pdf-editor|ventures/pdf-editor/platform/pdf-editor.backend-services/PdfEditor.BackendServices.sln|-"
  "backend-beta|wow-two-sdk-beta/wow-two-sdk.backend.beta/src/WoW.Two.Sdk.Backend.Beta.slnx|-"
  "frontend-beta|-|wow-two-sdk-beta/wow-two-sdk-beta.ui"
  "sift|ventures/sift/engineering/codebase/sift.backend-services/Sift.sln|ventures/sift/engineering/codebase/sift.frontend-services"
  "transcript-forge|ventures/transcript-forge/engineering/codebase/transcript-forge.backend-services/TranscriptForge.sln|ventures/transcript-forge/engineering/codebase/transcript-forge.frontend-services"
  "prism|-|ventures/10x-ventures-prism/engineering/codebase/prism.frontend-services"
)

MODE="both"     # both | backend | frontend
DRY=0
FILTERS=()      # explicit project names; empty = all

while [ $# -gt 0 ]; do
  case "$1" in
    -b|--backend)  MODE="backend" ;;
    -f|--frontend) MODE="frontend" ;;
    -l|--list)     MODE="list" ;;
    -n|--dry-run)  DRY=1 ;;
    -h|--help)     sed -n '2,28p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    -*)            echo "unknown flag: $1" >&2; exit 1 ;;
    *)             FILTERS+=("$1") ;;
  esac
  shift
done

# Is $1 in FILTERS? (true when no filters given)
wanted() {
  [ "${#FILTERS[@]}" -eq 0 ] && return 0
  local f; for f in "${FILTERS[@]}"; do [ "$f" = "$1" ] && return 0; done
  return 1
}

open_rider() {   # $1 = abs path to .sln/.slnx
  if [ -x "$RIDER" ]; then "$RIDER" "$1" >/dev/null 2>&1 &
  elif command -v rider >/dev/null 2>&1; then rider "$1" >/dev/null 2>&1 &
  else open -na "Rider" --args "$1"; fi
}

open_webstorm() {  # $1 = abs path to frontend folder
  if [ -x "$WEBSTORM" ]; then "$WEBSTORM" "$1" >/dev/null 2>&1 &
  elif command -v webstorm >/dev/null 2>&1; then webstorm "$1" >/dev/null 2>&1 &
  else open -na "WebStorm" --args "$1"; fi
}

stagger() { [ "$DELAY" != "0" ] && sleep "$DELAY" || true; }

if [ "$MODE" = "list" ]; then
  printf "%-22s  %-4s  %-4s  %s\n" "PROJECT" "BE" "FE" "PATHS (✓ exists / ✗ missing)"
  printf -- "----------------------------------------------------------------------------------\n"
fi

be_count=0; fe_count=0
for entry in "${PROJECTS[@]}"; do
  IFS='|' read -r name be fe <<< "$entry"
  wanted "$name" || continue

  be_abs=""; fe_abs=""
  [ "$be" != "-" ] && be_abs="$WB/$be"
  [ "$fe" != "-" ] && fe_abs="$WB/$fe"

  if [ "$MODE" = "list" ]; then
    bmark="-"; fmark="-"
    [ -n "$be_abs" ] && { [ -f "$be_abs" ] && bmark="✓" || bmark="✗"; }
    [ -n "$fe_abs" ] && { [ -d "$fe_abs" ] && fmark="✓" || fmark="✗"; }
    printf "%-22s  %-4s  %-4s  %s\n" "$name" "$bmark" "$fmark" "${be#-}${fe:+  |  }${fe#-}"
    continue
  fi

  # backend → Rider
  if [ "$MODE" != "frontend" ] && [ -n "$be_abs" ]; then
    if [ -f "$be_abs" ]; then
      echo "rider     → $name :: $be"
      [ "$DRY" = 0 ] && { open_rider "$be_abs"; stagger; }
      be_count=$((be_count + 1))
    else
      echo "  [skip] backend missing: $be" >&2
    fi
  fi

  # frontend → WebStorm
  if [ "$MODE" != "backend" ] && [ -n "$fe_abs" ]; then
    if [ -d "$fe_abs" ]; then
      echo "webstorm  → $name :: $fe"
      [ "$DRY" = 0 ] && { open_webstorm "$fe_abs"; stagger; }
      fe_count=$((fe_count + 1))
    else
      echo "  [skip] frontend missing: $fe" >&2
    fi
  fi
done

if [ "$MODE" != "list" ]; then
  verb="opened"; [ "$DRY" = 1 ] && verb="would open"
  echo ""
  echo "$verb $be_count backend(s) in Rider, $fe_count frontend(s) in WebStorm."
  disown -a 2>/dev/null || true
fi

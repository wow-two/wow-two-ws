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
#   active.sh wheelhouse forever-pin      only the named projects (any flag still applies)
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
  "tbs|ventures/track-2-transportbrain/engineering/codebase/tbs.backend-services/tbs.backend-services.slnx|ventures/track-2-transportbrain/engineering/codebase/tbs.frontend-services"
  "wheelhouse|wow-two-platform/wow-two-platform.wheelhouse/engineering/codebase/wheelhouse.backend-services/Wheelhouse.BackendServices.slnx|wow-two-platform/wow-two-platform.wheelhouse/engineering/codebase/wheelhouse.frontend-services"
  "secrets-vault|wow-two-platform/wow-two-platform.secrets-vault/engineering/codebase/secrets-vault.backend-services/Wow-Two-Platform.Secrets-Vault.sln|wow-two-platform/wow-two-platform.secrets-vault/engineering/codebase/secrets-vault.frontend-services"
  "forever-pin|ventures/10x-venture-forever-pin/engineering/codebase/forever-pin.backend-services/ForeverPin.BackendServices.slnx|ventures/10x-venture-forever-pin/engineering/codebase/forever-pin.frontend-services"
  "trademark-watcher|ventures/trademark-watcher-poc/platform/src/backend/Trademark.Watcher.sln|-"
  "acquisition-explorer|-|ventures/acquisition-explorer-poc/platform/acquisition-explorer-frontend"
  "transcript-forge|ventures/10x-ventures-transcript-forge/engineering/codebase/transcript-forge.backend-services/TranscriptForge.BackendServices.slnx|ventures/10x-ventures-transcript-forge/engineering/codebase/transcript-forge.frontend-services"
  "pdf-editor|ventures/pdf-editor/platform/pdf-editor.backend-services/PdfEditor.BackendServices.sln|-"
  "backend-beta|wow-two-sdk-beta/wow-two-sdk.backend.beta/engineering/codebase/wow-two-back-beta-sdk/src/WoW.Two.Sdk.Backend.Beta.slnx|-"
  "frontend-beta|-|wow-two-sdk-beta/wow-two-sdk-beta.ui/engineering/codebase/wow-two-front-beta-sdk"
  "sift|ventures/sift/engineering/codebase/sift.backend-services/Sift.sln|ventures/sift/engineering/codebase/sift.frontend-services"
  "prism|-|ventures/10x-ventures-prism/engineering/codebase/prism.frontend-services"
  "arcade|ventures/ventures.arcade/engineering/codebase/arcade.backend-services/Arcade.sln|ventures/ventures.arcade/engineering/codebase/arcade.frontend-services"
  "museums-gallery|ventures/ventures.museums-gallery/engineering/codebase/museums-gallery.backend-services/MuseumsGallery.sln|ventures/ventures.museums-gallery/engineering/codebase/museums-gallery.frontend-services"
  "tnis|ventures/ventures.tnis/engineering/codebase/tnis.backend-services/tnis.backend-services.slnx|ventures/ventures.tnis/engineering/codebase/tnis.frontend-services"
  "tnis-mintrans|ventures/ventures.tnis-mintrans/engineering/codebase/tnis-mintrans.backend-services/TnisMintrans.sln|ventures/ventures.tnis-mintrans/engineering/codebase/tnis-mintrans.frontend-services"
  "listing-shelf|ventures/ventures.listing-shelf/engineering/codebase/listing-shelf.backend-services/ListingShelf.BackendServices.slnx|ventures/ventures.listing-shelf/engineering/codebase/listing-shelf.frontend-services"
  "pose-coach|ventures/ventures.pose-coach/engineering/codebase/pose-coach.backend-services/PoseCoach.BackendServices.slnx|ventures/ventures.pose-coach/engineering/codebase/pose-coach.frontend-services"
  "ocharo-studio|ocharo-hq/ocharo-ws/workbench/ocharo-studio/engineering/codebase/ocharo-studio.backend-services/OcharoStudio.BackendServices.slnx|ocharo-hq/ocharo-ws/workbench/ocharo-studio/engineering/codebase/ocharo-studio.frontend-services"
  "brand-workspace|ocharo-hq/ocharo-ws/workbench/ocharo-platform/engineering/codebase/brand-workspace.backend-services/BrandWorkspace.BackendServices.slnx|ocharo-hq/ocharo-ws/workbench/ocharo-platform/engineering/codebase/brand-workspace.frontend-services"
  "ocharo-marketing|ocharo-hq/ocharo-ws/workbench/ocharo-marketing/engineering/codebase/ocharo-marketing.backend-services/OcharoMarketing.BackendServices.slnx|ocharo-hq/ocharo-ws/workbench/ocharo-marketing/engineering/codebase/ocharo-marketing.frontend-services"
  "ocharo-catalogue|ocharo-hq/ocharo-ws/workbench/ocharo-platform/engineering/codebase/ocharo-catalogue.backend-services/OcharoCatalogue.BackendServices.slnx|ocharo-hq/ocharo-ws/workbench/ocharo-platform/engineering/codebase/ocharo-catalogue.frontend-services"
  "ocharo-blog|ocharo-hq/ocharo-ws/workbench/ocharo-marketing/engineering/codebase/ocharo-blog.backend-services/OcharoBlog.BackendServices.slnx|ocharo-hq/ocharo-ws/workbench/ocharo-marketing/engineering/codebase/ocharo-blog.frontend-services"
  "ocharo-brand|ocharo-hq/ocharo-ws/workbench/ocharo-platform/engineering/codebase/ocharo-brand.backend-services/OcharoBrand.BackendServices.slnx|ocharo-hq/ocharo-ws/workbench/ocharo-platform/engineering/codebase/ocharo-brand.frontend-services"
  "pbn-studio|ventures/ventures.pbn-studio/engineering/codebase/pbn-studio.backend-services/PbnStudio.sln|ventures/ventures.pbn-studio/engineering/codebase/pbn-studio.frontend-services"
  "ocharo-motion|ocharo-hq/ocharo-ws/workbench/ocharo-assets/engineering/codebase/ocharo-motion.backend-services/OcharoMotion.sln|ocharo-hq/ocharo-ws/workbench/ocharo-assets/engineering/codebase/ocharo-motion.frontend-services"
  "retainer-balance|ventures/ventures.retainer-balance/engineering/codebase/retainer-balance.backend-services/RetainerBalance.slnx|ventures/ventures.retainer-balance/engineering/codebase/retainer-balance.frontend-services"
  "documentation-checker|ventures/ventures.documentation-checker/engineering/codebase/documentation-checker.backend-services/DocumentationChecker.slnx|ventures/ventures.documentation-checker/engineering/codebase/documentation-checker.frontend-services"
  "file-watch|ventures/ventures.file-watch/engineering/codebase/file-watch.backend-services/FileWatch.slnx|ventures/ventures.file-watch/engineering/codebase/file-watch.frontend-services"
  "procedure-review|ventures/ventures.procedure-review/engineering/codebase/procedure-review.backend-services/ProcedureReview.slnx|ventures/ventures.procedure-review/engineering/codebase/procedure-review.frontend-services"
  "training-seats|ventures/ventures.training-seats/engineering/codebase/training-seats.backend-services/TrainingSeats.slnx|ventures/ventures.training-seats/engineering/codebase/training-seats.frontend-services"
  "epub-review|ventures/ventures.epub-review/engineering/codebase/epub-review.backend-services/EpubReview.slnx|ventures/ventures.epub-review/engineering/codebase/epub-review.frontend-services"
  "customer-promises|ventures/ventures.customer-promises/engineering/codebase/customer-promises.backend-services/CustomerPromises.slnx|ventures/ventures.customer-promises/engineering/codebase/customer-promises.frontend-services"
  "vendor-renewals|ventures/ventures.vendor-renewals/engineering/codebase/vendor-renewals.backend-services/VendorRenewals.slnx|ventures/ventures.vendor-renewals/engineering/codebase/vendor-renewals.frontend-services"
  "config-checker|ventures/ventures.config-checker/engineering/codebase/config-checker.backend-services/ConfigChecker.slnx|ventures/ventures.config-checker/engineering/codebase/config-checker.frontend-services"
  "podcast-readiness|ventures/ventures.podcast-readiness/engineering/codebase/podcast-readiness.backend-services/PodcastReadiness.slnx|ventures/ventures.podcast-readiness/engineering/codebase/podcast-readiness.frontend-services"
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

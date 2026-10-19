#!/usr/bin/env bash
#
# restructure-workbench.sh — move workbench/ into the owner-folder layout (one-time, idempotent).
#   wow-two-*/ stay · own ventures → maxs-projects/ventures/{saas,consumer,labs}/ · work for others → maxs-projects/clients/{client}/
#   ocharo-hq/ → mfts-projects/ventures/ocharo-hq/ · labs/, apps/, projects/ and ventures/ retire.
# Layout: conventions/development/repo/layout/workbench-layout.md
#
# Moves with `mv` only and never overwrites: while any step's source and target both exist, or a child of
# ventures/ has no group, the run refuses before anything moves. A step already done (source gone, target
# present) is skipped, so a re-run is safe. A retired folder goes with `rmdir` only once empty; a lone
# .DS_Store and the commit-less meme-world stub in apps/ go to ~/.Trash (recoverable). Nothing is deleted.
#
# Usage:
#   scripts/restructure-workbench.sh                  dry run (default): print the plan, move nothing
#   scripts/restructure-workbench.sh --apply          move, retire, verify
#   scripts/restructure-workbench.sh --apply --ignore-running
#                                                     move although processes run inside a moving folder

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WS="$(cd "$SCRIPT_DIR/.." && pwd)"
WB="$WS/workbench"
TRASH="$HOME/.Trash"
STAMP="$(date +%Y%m%d-%H%M%S)"

APPLY=0
IGNORE_RUNNING=0
for arg in "$@"; do
  case "$arg" in
    --apply)          APPLY=1 ;;
    --dry-run)        APPLY=0 ;;
    --ignore-running) IGNORE_RUNNING=1 ;;
    -h|--help)        sed -n '2,17p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *)                echo "unknown option: $arg" >&2; exit 2 ;;
  esac
done

# Venture groups, by who pays (layout convention § Venture groups): every child of ventures/ is named once.
VENTURES_TO="maxs-projects/ventures"
GROUP_SAAS=(
  10x-venture-forever-pin 10x-venture-forever-pin-promo 10x-ven-haven ventures.listing-shelf
  10x-ventures-transcript-forge sift ventures.surface-pattern ventures.pbn-studio
  ventures.retainer-balance ventures.documentation-checker ventures.file-watch ventures.procedure-review
  ventures.training-seats ventures.epub-review ventures.customer-promises ventures.vendor-renewals
  ventures.config-checker ventures.podcast-readiness
  trademark-watcher-poc acquisition-explorer-poc pdf-editor ventures.tnis
  10x-ventures-prism prism-wt-c        # prism-wt-c: leftover worktree of prism
  first-ten.md                         # the index file of the ten pilots, linked to them as siblings
)
GROUP_CONSUMER=(
  ventures.hijinx ventures.fun-vault ventures.arcade
  whiteout 10x-venture-whiteout-presets
  ventures.pose-coach ventures.museums-gallery
)
GROUP_LABS=(
  ventures.city-vision ventures.home-renovation 10x-fin-nt
  your-pocket-doctor                   # third-party clone, not a venture; the hub lists it for removal
)

# source|target, relative to workbench/. Clients and the hub first, then the groups, then labs/ and the rest.
MOVES=(
  "ventures/ventures.tnis-mintrans|maxs-projects/clients/mintrans/ventures.tnis-mintrans"
  "ventures/track-2-transportbrain|maxs-projects/clients/mintrans/track-2-transportbrain"
  "ventures/tbs.demo|maxs-projects/clients/mintrans/tbs.demo"
  "ventures/10x-ventures|$VENTURES_TO/10x-ventures"
)
for name in "${GROUP_SAAS[@]}";     do MOVES+=("ventures/$name|$VENTURES_TO/saas/$name"); done
for name in "${GROUP_CONSUMER[@]}"; do MOVES+=("ventures/$name|$VENTURES_TO/consumer/$name"); done
for name in "${GROUP_LABS[@]}";     do MOVES+=("ventures/$name|$VENTURES_TO/labs/$name"); done
MOVES+=(
  "labs/airfryer-3d|$VENTURES_TO/labs/airfryer-3d"
  "labs/labs.home-reno|$VENTURES_TO/labs/labs.home-reno"
  "projects/nasiya-finance|maxs-projects/clients/nasiya-finance"
  "wom-two-ws|maxs-projects/wom-two-ws"
  "ocharo-hq|mfts-projects/ventures/ocharo-hq"
)
GROUPED_FROM="ventures"                # a child of ventures/ named in no list above is refused, not guessed
STUB="apps/wow-two-apps.meme-world"    # commit-less stub; the repository lives in wow-two-apps/
STUB_REPO="wow-two-apps/wow-two-apps.meme-world"
RETIRE="ventures labs apps projects"
SKELETON="maxs-projects/ventures/saas maxs-projects/ventures/consumer maxs-projects/ventures/labs maxs-projects/clients mfts-projects/ventures"

exists() { [ -e "$1" ] || [ -L "$1" ]; }

map_path() {  # old path under workbench/ → new path, or fail when it does not move
  local rel="$1" step src dst
  for step in "${MOVES[@]}"; do
    src="${step%%|*}"; dst="${step#*|}"
    case "$rel" in
      "$src")   echo "$dst"; return 0 ;;
      "$src"/*) echo "$dst/${rel#"$src"/}"; return 0 ;;
    esac
  done
  return 1
}

dirty_note() {  # uncommitted-file count of a repository, without taking its index lock
  [ -d "$1/.git" ] || return 0
  local n
  n="$(git --no-optional-locks -C "$1" status --porcelain 2>/dev/null | wc -l | tr -d ' ')"
  [ "$n" = 0 ] || echo "  [$n uncommitted, kept]"
}

stub_state() {  # trash | done | keep: <reason>
  local d="$WB/$STUB"
  exists "$d" || { echo "done"; return; }
  [ -d "$WB/$STUB_REPO/.git" ] || { echo "keep: $STUB_REPO is missing"; return; }
  [ "$(ls -A "$d" | wc -l | tr -d ' ')" = 2 ] && [ -d "$d/.git" ] && [ -f "$d/README.md" ] \
    || { echo "keep: holds more than .git and README.md"; return; }
  ! git -C "$d" rev-parse --verify -q HEAD >/dev/null 2>&1 || { echo "keep: has commits"; return; }
  [ "$(wc -l < "$d/README.md" | tr -d ' ')" -le 1 ] || { echo "keep: README.md has content"; return; }
  echo "trash"
}

to_trash() {  # $1 = path under workbench/; prints where it went, fails without aborting the run
  local target="$TRASH/workbench_${1//\//_}-$STAMP"
  exists "$target" && target="$target-$$"
  mv -n "$WB/$1" "$target" 2>/dev/null && ! exists "$WB/$1" && echo "$target"
}

# ── Plan ─────────────────────────────────────────────────────────────────────

PLAN=("${MOVES[@]}")
ungrouped=""                           # newline-separated children of ventures/ that no list names
if [ -d "$WB/$GROUPED_FROM" ]; then
  for path in "$WB/$GROUPED_FROM"/* "$WB/$GROUPED_FROM"/.[!.]*; do
    exists "$path" || continue
    name="${path##*/}"
    [ "$name" = ".DS_Store" ] && continue
    listed=0
    for step in "${MOVES[@]}"; do [ "${step%%|*}" = "$GROUPED_FROM/$name" ] && listed=1; done
    [ "$listed" = 1 ] || ungrouped="$ungrouped$GROUPED_FROM/$name"$'\n'
  done
fi

echo "Workbench: $WB"
echo "Mode:      $([ "$APPLY" = 1 ] && echo APPLY || echo "DRY RUN (pass --apply to move)")"
echo ""
echo "▸ Moves"
todo=0; done_=0; missing=0; conflicts=0
for step in "${PLAN[@]}"; do
  src="${step%%|*}"; dst="${step#*|}"
  if exists "$WB/$src"; then
    if exists "$WB/$dst"; then
      echo "  REFUSE  $src → $dst (target exists)"; conflicts=$((conflicts + 1))
    else
      echo "  mv      $src → $dst$(dirty_note "$WB/$src")"; todo=$((todo + 1))
    fi
  elif exists "$WB/$dst"; then
    echo "  done    $dst"; done_=$((done_ + 1))
  else
    echo "  missing $src (skipped)"; missing=$((missing + 1))
  fi
done
while IFS= read -r path; do
  [ -n "$path" ] || continue
  echo "  REFUSE  $path (no group: add it to a GROUP_ list)"; conflicts=$((conflicts + 1))
done <<< "$ungrouped"
echo "  → $todo to move · $done_ done · $missing missing · $conflicts refused"

echo ""
echo "▸ Merged stub"
stub="$(stub_state)"
case "$stub" in
  trash) echo "  trash   $STUB → ~/.Trash (no commits; the repository is $STUB_REPO)" ;;
  done)  echo "  done    $STUB is gone" ;;
  *)     echo "  KEEP    $STUB — ${stub#keep: }; review it by hand" ;;
esac

echo ""
echo "▸ Retired folders (rmdir once empty; a lone .DS_Store goes to ~/.Trash)"
for dir in $RETIRE; do
  if [ -d "$WB/$dir" ]; then echo "  rmdir   $dir"; else echo "  done    $dir is gone"; fi
done

roots=""
for step in "${PLAN[@]}"; do
  exists "$WB/${step%%|*}" && roots="$roots$WB/${step%%|*}"$'\n'
done
running=""
if [ -n "$roots" ] && command -v lsof >/dev/null 2>&1; then
  running="$(lsof -a -d cwd -F pcn 2>/dev/null | ROOTS="$roots" awk '
    BEGIN { n = split(ENVIRON["ROOTS"], r, "\n") }
    /^p/ { pid = substr($0, 2) }
    /^c/ { cmd = substr($0, 2) }
    /^n/ { cwd = substr($0, 2)
           for (i = 1; i <= n; i++)
             if (r[i] != "" && (cwd == r[i] || index(cwd, r[i] "/") == 1)) { print "  " pid "  " cmd "  " cwd; break } }')"
fi
if [ -n "$running" ]; then
  echo ""
  echo "▸ Processes running inside a moving folder — stop them (chats, dev servers, watchers) first"
  echo "$running"
fi

if [ "$conflicts" -gt 0 ]; then
  echo ""
  echo "Refused: $conflicts step(s) have an existing target or no group. Merge, rename or group them by hand, then re-run." >&2
  exit 1
fi

# ── Apply ────────────────────────────────────────────────────────────────────

if [ "$APPLY" = 1 ]; then
  if [ -n "$running" ] && [ "$IGNORE_RUNNING" = 0 ]; then
    echo "" >&2
    echo "Refused: processes run inside a moving folder. Stop them or pass --ignore-running." >&2
    exit 1
  fi
  echo ""
  echo "▸ Applying"
  for folder in $SKELETON; do mkdir -p "$WB/$folder"; done
  for step in "${PLAN[@]}"; do
    src="${step%%|*}"; dst="${step#*|}"
    exists "$WB/$src" || continue
    if exists "$WB/$dst"; then echo "  REFUSE  $src → $dst (target appeared)" >&2; exit 1; fi
    mkdir -p "$(dirname "$WB/$dst")"
    mv "$WB/$src" "$WB/$dst"
    echo "  moved   $src → $dst"
  done
  if [ "$stub" = trash ]; then
    if went="$(to_trash "$STUB")"; then echo "  trashed $STUB → $went"
    else echo "  KEPT    $STUB — the Trash refused it; move it by hand"; fi
  fi
  for dir in $RETIRE; do
    [ -d "$WB/$dir" ] || continue
    if [ "$(ls -A "$WB/$dir")" = ".DS_Store" ]; then to_trash "$dir/.DS_Store" >/dev/null || true; fi
    if rmdir "$WB/$dir" 2>/dev/null; then
      echo "  rmdir   $dir"
    else
      echo "  KEPT    $dir — still holds: $(ls -A "$WB/$dir" | tr '\n' ' ')"
    fi
  done

  echo ""
  echo "▸ Verify"
  echo "  top level: $(cd "$WB" && ls -d -- */ | tr '\n' ' ')"
  python3 "$WS/scripts/gen-repo-registry.py" --check 2>&1 | sed 's/^/  /' || true
  missing_targets="$("$WS/scripts/active.sh" --list 2>/dev/null | grep -v '^PROJECT' | grep -c '✗' || true)"
  echo "  active.sh: $missing_targets project(s) with a missing target"
fi

# ── Git flags ────────────────────────────────────────────────────────────────
# Flags are keyed by path, so a moved repository reads the default (OFF) until the owner re-sends them.

flag_lines() {  # "<kinds> workbench/<new path>" for each moving repository with a flag ON
  local path flags new kinds
  python3 -B "$1" status --repo '*' 2>/dev/null \
    | sed -n 's/^- \(workbench\/[^:]*\): \(.*\)$/\1|\2/p' \
    | while IFS='|' read -r path flags; do
        new="$(map_path "${path#workbench/}")" || continue
        kinds=""
        case "$flags" in *"commit ON"*) kinds="commit" ;; esac
        case "$flags" in *"push ON"*) kinds="${kinds:+$kinds,}push" ;; esac
        if [ -n "$kinds" ]; then echo "$kinds workbench/$new"; fi
      done
}

helper="$WS/.codex/hooks/commit_permission.py"
if [ -f "$helper" ]; then
  directives="$(flag_lines "$helper" | sort | awk '{ a[$1] = a[$1] " " $2 } END { for (k in a) print "~git_on " k a[k] }')"
  if [ -n "$directives" ]; then
    echo ""
    echo "▸ Git flags to re-send after the move — each line as its own whole message"
    echo "$directives" | sed 's/^/  /'
  fi
fi

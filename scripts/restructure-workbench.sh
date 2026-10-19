#!/usr/bin/env bash
#
# restructure-workbench.sh — move workbench/ into the owner-folder layout (one-time, idempotent).
#   wow-two-*/ stay · own ventures → maxs-projects/ventures/ · work for others → maxs-projects/clients/{client}/
#   ocharo-hq/ → mfts-projects/ventures/ocharo-hq/ · labs/, apps/, projects/ and ventures/ retire.
# Layout: conventions/development/repo/layout/workbench-layout.md
#
# Moves with `mv` only and never overwrites: while any step's source and target both exist, the run
# refuses before anything moves. A step already done (source gone, target present) is skipped, so a
# re-run is safe. A retired folder goes with `rmdir` only once empty; a lone .DS_Store and the
# commit-less meme-world stub in apps/ go to ~/.Trash (recoverable). Nothing is deleted.
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

# source|target, relative to workbench/; the first match wins, so these precede the sweep.
MOVES=(
  "ventures/ventures.tnis-mintrans|maxs-projects/clients/mintrans/ventures.tnis-mintrans"
  "ventures/track-2-transportbrain|maxs-projects/clients/mintrans/track-2-transportbrain"
  "ventures/tbs.demo|maxs-projects/clients/mintrans/tbs.demo"
  "projects/nasiya-finance|maxs-projects/clients/nasiya-finance"
  "labs/airfryer-3d|maxs-projects/ventures/airfryer-3d"
  "labs/labs.home-reno|maxs-projects/ventures/labs.home-reno"
  "wom-two-ws|maxs-projects/wom-two-ws"
  "ocharo-hq|mfts-projects/ventures/ocharo-hq"
)
SWEEP_FROM="ventures"                  # every other child of ventures/ moves here
SWEEP_TO="maxs-projects/ventures"
STUB="apps/wow-two-apps.meme-world"    # commit-less stub; the repository lives in wow-two-apps/
STUB_REPO="wow-two-apps/wow-two-apps.meme-world"
RETIRE="ventures labs apps projects"
SKELETON="maxs-projects/ventures maxs-projects/clients mfts-projects/ventures"

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
  case "$rel" in "$SWEEP_FROM"/*) echo "$SWEEP_TO/${rel#"$SWEEP_FROM"/}"; return 0 ;; esac
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
if [ -d "$WB/$SWEEP_FROM" ]; then
  for path in "$WB/$SWEEP_FROM"/* "$WB/$SWEEP_FROM"/.[!.]*; do
    exists "$path" || continue
    name="${path##*/}"
    [ "$name" = ".DS_Store" ] && continue
    explicit=0
    for step in "${MOVES[@]}"; do [ "${step%%|*}" = "$SWEEP_FROM/$name" ] && explicit=1; done
    [ "$explicit" = 1 ] || PLAN+=("$SWEEP_FROM/$name|$SWEEP_TO/$name")
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
  echo "Refused: $conflicts target(s) already exist. Merge or rename them by hand, then re-run." >&2
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
  missing_targets="$("$WS/scripts/active.sh" --list 2>/dev/null | grep -c '✗' || true)"
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

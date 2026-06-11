#!/usr/bin/env bash
#
# ventures.sh — open / list venture projects under workbench/ventures/
#
# Per-venture manifest: <venture-root>/.venture.sh declares
#   TAGS=(micro-saas backend poc ...)
#   RIDER_TARGETS=(relative/path/to/file.sln  another/folder)
#   WEBSTORM_TARGETS=(relative/path/to/frontend-folder)
# Missing manifest → auto-detect first .sln and first package.json dir.
#
# Usage:
#   ventures.sh list                                # tabular overview
#   ventures.sh open <name|tag|all>                 # open in Rider/WebStorm
#   ventures.sh open trademark-watcher-poc          # one venture
#   ventures.sh open micro-saas                     # all tagged micro-saas
#   ventures.sh open all                            # everything

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WS_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
VENTURES_DIR="$WS_DIR/workbench/ventures"

JB_SCRIPTS="$HOME/Library/Application Support/JetBrains/Toolbox/scripts"
RIDER="$JB_SCRIPTS/rider"
WEBSTORM="$JB_SCRIPTS/webstorm"

# ---------- helpers ----------

discover_ventures() {
    # Print one venture folder name per line, sorted.
    find "$VENTURES_DIR" -mindepth 1 -maxdepth 1 -type d \
        -not -name '.*' \
        -exec basename {} \; | sort
}

# Reset + load a venture's manifest into module-scope arrays.
# Sets: TAGS, RIDER_TARGETS, WEBSTORM_TARGETS (all bash arrays).
load_manifest() {
    local name="$1"
    local dir="$VENTURES_DIR/$name"

    TAGS=()
    RIDER_TARGETS=()
    WEBSTORM_TARGETS=()

    if [[ -f "$dir/.venture.sh" ]]; then
        # shellcheck disable=SC1090
        source "$dir/.venture.sh"
        return
    fi

    # Auto-detect (warn).
    echo "  [warn] $name has no .venture.sh — auto-detecting" >&2
    TAGS=(auto)

    while IFS= read -r sln; do
        [[ -n "$sln" ]] && RIDER_TARGETS+=("${sln#$dir/}")
    done < <(find "$dir" -maxdepth 6 -name '*.sln' \
        -not -path '*/bin/*' -not -path '*/obj/*' \
        -not -path '*/node_modules/*' -not -path '*/.claude/*' \
        2>/dev/null | head -3)

    while IFS= read -r pj; do
        [[ -n "$pj" ]] && WEBSTORM_TARGETS+=("$(dirname "${pj#$dir/}")")
    done < <(find "$dir" -maxdepth 5 -name 'package.json' \
        -not -path '*/node_modules/*' 2>/dev/null | head -3)
}

# Test if $1 is one of the elements of the remaining args.
# Usage: contains "$x" "${arr[@]}"
contains() {
    local needle="$1"; shift
    local item
    for item in "$@"; do
        [[ "$item" == "$needle" ]] && return 0
    done
    return 1
}

# Length of named array, bash-3.2-safe with set -u.
# Usage: array_len ARR_NAME
array_len() {
    local name="$1"
    eval "echo \${#${name}[@]:-0}" 2>/dev/null || echo 0
}

# ---------- commands ----------

cmd_list() {
    printf "%-28s  %-3s  %-3s  %-40s  %s\n" "VENTURE" "BE" "FE" "TAGS" "TARGETS"
    printf -- "------------------------------------------------------------------------------------------------------------------\n"
    local name be fe tags_str targets
    while IFS= read -r name; do
        load_manifest "$name" 2>/dev/null
        be=$(array_len RIDER_TARGETS)
        fe=$(array_len WEBSTORM_TARGETS)
        tags_str="${TAGS[*]:-}"
        targets="${RIDER_TARGETS[*]:-} ${WEBSTORM_TARGETS[*]:-}"
        printf "%-28s  %-3s  %-3s  %-40s  %s\n" "$name" "$be" "$fe" "$tags_str" "$targets"
    done < <(discover_ventures)
}

# Resolve a target (name | tag | "all") to a list of venture names.
resolve_target() {
    local target="$1"
    local matches=()

    if [[ "$target" == "all" ]]; then
        while IFS= read -r n; do matches+=("$n"); done < <(discover_ventures)
    elif [[ -d "$VENTURES_DIR/$target" ]]; then
        matches=("$target")
    else
        # Treat as tag — collect every venture whose manifest contains it.
        local n
        while IFS= read -r n; do
            load_manifest "$n" 2>/dev/null
            if [[ $(array_len TAGS) -gt 0 ]] && contains "$target" "${TAGS[@]}"; then
                matches+=("$n")
            fi
        done < <(discover_ventures)
    fi

    [[ $(array_len matches) -gt 0 ]] && printf '%s\n' "${matches[@]}"
}

cmd_open() {
    local target="${1:-}"
    if [[ -z "$target" ]]; then
        echo "usage: ventures.sh open <name|tag|all>" >&2
        exit 1
    fi

    local matches=()
    while IFS= read -r m; do
        [[ -n "$m" ]] && matches+=("$m")
    done < <(resolve_target "$target")

    if [[ $(array_len matches) -eq 0 ]]; then
        echo "no ventures match '$target'" >&2
        echo "try: ventures.sh list" >&2
        exit 1
    fi

    local name dir t abs
    for name in "${matches[@]}"; do
        dir="$VENTURES_DIR/$name"
        load_manifest "$name"

        if [[ $(array_len RIDER_TARGETS) -gt 0 ]]; then
            for t in "${RIDER_TARGETS[@]}"; do
                abs="$dir/$t"
                if [[ -e "$abs" ]]; then
                    echo "rider     → $name :: $t"
                    "$RIDER" "$abs" >/dev/null 2>&1 &
                else
                    echo "  [skip] rider target missing: $abs" >&2
                fi
            done
        fi

        if [[ $(array_len WEBSTORM_TARGETS) -gt 0 ]]; then
            for t in "${WEBSTORM_TARGETS[@]}"; do
                abs="$dir/$t"
                if [[ -e "$abs" ]]; then
                    echo "webstorm  → $name :: $t"
                    "$WEBSTORM" "$abs" >/dev/null 2>&1 &
                else
                    echo "  [skip] webstorm target missing: $abs" >&2
                fi
            done
        fi
    done
    # Let JetBrains processes detach; don't wait.
    disown -a 2>/dev/null || true
}

cmd_help() {
    cat <<'EOF'
ventures.sh — manage venture projects under workbench/ventures/

Commands:
  list                     Tabular overview of all ventures (parts + tags)
  open <name|tag|all>      Open in Rider (backends) + WebStorm (frontends)
  help                     This message

Examples:
  ventures.sh list
  ventures.sh open trademark-watcher-poc
  ventures.sh open micro-saas
  ventures.sh open all

Per-venture manifest (optional, lives at <venture>/.venture.sh):
  TAGS=(micro-saas backend poc)
  RIDER_TARGETS=(platform/src/backend/Trademark.Watcher.sln)
  WEBSTORM_TARGETS=(platform/frontend)
EOF
}

# ---------- dispatch ----------

case "${1:-help}" in
    list)             cmd_list ;;
    open)             shift; cmd_open "$@" ;;
    help|-h|--help)   cmd_help ;;
    *)                echo "unknown command: $1" >&2; cmd_help >&2; exit 1 ;;
esac

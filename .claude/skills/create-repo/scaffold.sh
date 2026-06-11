#!/usr/bin/env bash
#
# scaffold.sh — deterministic mechanics for the create-repo skill.
#   Creates workbench/{org}/{repo}, copies the product-repo template, fills
#   placeholders, writes a root .gitignore, `git init`s, and registers the repo
#   in scripts/active.sh. It does NOT generate code (the .NET + React files
#   depend on brand/name — the skill's Claude driver writes those) and it does
#   NOT commit (the developer manages git).
#
# Usage:
#   scaffold.sh <repo-name> <Brand> <org> [single|multi]
#     repo-name  e.g. wow-two-platform.foo   (the on-disk + git repo name)
#     Brand      PascalCase  e.g. Foo        (.NET namespace/project prefix)
#     org        wow-two | wow-two-platform | ventures | …  (workbench subfolder)
#     mode       single (default) | multi    (informational — drives the code-gen step, not the mechanics)
#
# Env:
#   NET_VERSION   defaults to 10   (TargetFramework net{N}.0)
#
# Idempotency: refuses to clobber an existing repo dir; appends to active.sh only
# if the project name is not already registered.

set -euo pipefail

# ---- resolve workspace paths (skill lives at .claude/skills/create-repo/) ----
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WS_DIR="$(cd "$SCRIPT_DIR/../../.." && pwd)"     # .claude/skills/create-repo → WS root
WB="$WS_DIR/workbench"
TEMPLATE="$WS_DIR/workbench/wow-two-sdk-beta/wow-two-sdk-beta.product-template"
ACTIVE="$WS_DIR/scripts/active.sh"

# ---- args ----
REPO_NAME="${1:?repo-name required (e.g. wow-two-platform.foo)}"
BRAND="${2:?Brand required (PascalCase, e.g. Foo)}"
ORG="${3:?org required (wow-two | wow-two-platform | ventures | …)}"
MODE="${4:-single}"
NET_VERSION="${NET_VERSION:-10}"

# repo-slug = lowercase repo name, dots/spaces → hyphens (npm package + short name)
REPO_SLUG="$(printf '%s' "$REPO_NAME" | tr '[:upper:]' '[:lower:]' | tr ' .' '--')"
# short name = last dot-segment, slugified (active.sh first column, e.g. "foo")
SHORT_NAME="$(printf '%s' "${REPO_NAME##*.}" | tr '[:upper:]' '[:lower:]' | tr ' .' '--')"
TODAY="$(date +%F)"

REPO_DIR="$WB/$ORG/$REPO_NAME"
CODEBASE="$REPO_DIR/engineering/codebase"
BE_DIR="$CODEBASE/backend-services"
FE_DIR="$CODEBASE/frontend-services"

echo "[scaffold] repo=$REPO_NAME brand=$BRAND org=$ORG mode=$MODE net=$NET_VERSION"
echo "[scaffold] target=$REPO_DIR"

# ---- guardrails ----
[ -d "$TEMPLATE" ] || { echo "[scaffold] template missing: $TEMPLATE" >&2; exit 1; }
[ -e "$REPO_DIR" ] && { echo "[scaffold] refusing to clobber existing: $REPO_DIR" >&2; exit 1; }

# ---- 1. create + copy skeleton ----
mkdir -p "$WB/$ORG"
cp -R "$TEMPLATE" "$REPO_DIR"
# the template ships .gitkeep stubs in the two code dirs; the code-gen step fills them
find "$REPO_DIR" -name '.gitkeep' -path '*/codebase/*' -delete 2>/dev/null || true
mkdir -p "$BE_DIR" "$FE_DIR"

# ---- 2. placeholder replacement across every template doc ----
# {{REPO_NAME}} {{Brand}} {{repo-slug}} {{NET_VERSION}} {{YYYY-MM-DD}}
# (free-text {{ONE_LINE_WHAT_THIS_IS}} etc. are left for the human/Claude to fill)
while IFS= read -r -d '' f; do
  LC_ALL=C sed -i '' \
    -e "s|{{REPO_NAME}}|$REPO_NAME|g" \
    -e "s|{{Brand}}|$BRAND|g" \
    -e "s|{{repo-slug}}|$REPO_SLUG|g" \
    -e "s|{{NET_VERSION}}|$NET_VERSION|g" \
    -e "s|{{YYYY-MM-DD}}|$TODAY|g" \
    "$f"
done < <(find "$REPO_DIR" -type f \( -name '*.md' -o -name '*.json' -o -name '*.txt' \) -print0)

# ---- 3. root .gitignore ----
cat > "$REPO_DIR/.gitignore" <<'EOF'
# Build output
**/bin/
**/obj/
**/dist/
**/.vite/
node_modules/

# Local DB + secrets
*.db
*.db-shm
*.db-wal
**/appsettings.Local.json
.env

# IDE / OS
.idea/
.vs/
.vscode/*
.DS_Store
*.tsbuildinfo
EOF

# ---- 4. git init (NO commit — developer owns git) ----
if [ ! -d "$REPO_DIR/.git" ]; then
  git -C "$REPO_DIR" init -q
  echo "[scaffold] git initialized (no commit made)"
fi

# ---- 5. register in scripts/active.sh PROJECTS array ----
# entry: name|backend-sln(relative to workbench/)|frontend-dir(relative to workbench/)
BE_REL="$ORG/$REPO_NAME/engineering/codebase/backend-services/$BRAND.slnx"
FE_REL="$ORG/$REPO_NAME/engineering/codebase/frontend-services"
ENTRY="  \"$SHORT_NAME|$BE_REL|$FE_REL\""

if grep -q "\"$SHORT_NAME|" "$ACTIVE" 2>/dev/null; then
  echo "[scaffold] active.sh already has '$SHORT_NAME' — skipping registration"
else
  # insert the new entry just before the closing ')' of the PROJECTS=( … ) array
  LC_ALL=C awk -v entry="$ENTRY" '
    /^PROJECTS=\(/ { inarr=1 }
    inarr && /^\)/ { print entry; inarr=0 }
    { print }
  ' "$ACTIVE" > "$ACTIVE.tmp" && mv "$ACTIVE.tmp" "$ACTIVE"
  chmod +x "$ACTIVE"
  echo "[scaffold] registered in active.sh as '$SHORT_NAME'"
fi

# ---- summary for the skill driver ----
cat <<EOF

[scaffold] mechanical scaffold done.
  repo dir   : $REPO_DIR
  backend → : $BE_DIR          (write $BRAND.slnx + $BRAND.{Api,Application,Domain,Infrastructure,Persistence} here)
  frontend →: $FE_DIR          (write the Vite app here; deploy.mjs → backend-services/$BRAND.Api/wwwroot)
  short name : $SHORT_NAME      (scripts/active.sh $SHORT_NAME)
  net        : net$NET_VERSION.0

Next (Claude code-gen): generate the .NET solution + React app per the Drydock pattern,
then verify (dotnet build + npm install/build).
EOF

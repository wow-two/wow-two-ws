#!/usr/bin/env bash
#
# scaffold.sh — deterministic mechanics for the create-repo skill.
#   Creates workbench/{org}/{repo}, COPIES the product-repo template (which now
#   ships a complete working `Sample` example — 5 Clean-Arch projects + tests +
#   a Vite/React frontend + Docker), fills the doc {{placeholders}}, then
#   REBRANDS the example: Sample → Brand across all code/config, renames every
#   Sample* file/dir → Brand*, retargets the two code-dir slug prefixes
#   (sample.{backend,frontend}-services → {repo-slug}.{…}), and re-allocates the
#   template's dev ports to the next-free pair. Writes a root .gitignore, `git
#   init`s, and registers the
#   repo in scripts/active.sh. It does NOT generate code (the example is copied,
#   not authored) and does NOT commit (the developer manages git).
#
# Usage:
#   scaffold.sh <repo-name> <Brand> <org> [single|multi]
#     repo-name  e.g. wow-two-platform.foo   (the on-disk + git repo name)
#     Brand      PascalCase  e.g. Foo        (.NET namespace/project prefix)
#     org        wow-two | wow-two-platform | ventures | …  (workbench subfolder)
#     mode       single (default) | multi    (informational — drives later product work, not the mechanics)
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

# repo-slug = the repo's distinctive name = its LAST dot-segment, slugified
# (wow-two-platform.secrets-vault → "secrets-vault"; keeps the hyphen — NOT the
# lowercased brand "secretsvault"). Used for: the {{repo-slug}} doc placeholder
# AND the two code-dir prefixes ({slug}.backend-services / {slug}.frontend-services).
REPO_SLUG="$(printf '%s' "${REPO_NAME##*.}" | tr '[:upper:]' '[:lower:]' | tr ' .' '--')"
# short name = active.sh first column (e.g. "secrets-vault") — same as the slug.
SHORT_NAME="$REPO_SLUG"
# lowercase brand — for the template's lowercase `sample` tokens (sample.db, sample-data,
# sample-frontend, docker image/container name). Brand is PascalCase → just lowercase it.
BRAND_LC="$(printf '%s' "$BRAND" | tr '[:upper:]' '[:lower:]')"
TODAY="$(date +%F)"

REPO_DIR="$WB/$ORG/$REPO_NAME"
CODEBASE="$REPO_DIR/engineering/codebase"
# the two code dirs carry the repo slug as a dot-prefix (collision-avoidance across
# open IDEs). The template ships them as sample.backend-services / sample.frontend-services;
# the rename pass below retargets the prefix to $REPO_SLUG.
BE_DIR="$CODEBASE/$REPO_SLUG.backend-services"
FE_DIR="$CODEBASE/$REPO_SLUG.frontend-services"

echo "[scaffold] repo=$REPO_NAME brand=$BRAND org=$ORG mode=$MODE net=$NET_VERSION"
echo "[scaffold] target=$REPO_DIR"

# ---- guardrails ----
[ -d "$TEMPLATE" ] || { echo "[scaffold] template missing: $TEMPLATE" >&2; exit 1; }
[ -e "$REPO_DIR" ] && { echo "[scaffold] refusing to clobber existing: $REPO_DIR" >&2; exit 1; }

# ---- 1. create + copy template (incl. the complete `Sample` example) ----
mkdir -p "$WB/$ORG"
cp -R "$TEMPLATE" "$REPO_DIR"
# drop the template's own git history + any build artifacts that rode along in the copy.
rm -rf "$REPO_DIR/.git"
find "$REPO_DIR" -type d \( -name bin -o -name obj -o -name node_modules -o -name dist \) \
  -prune -exec rm -rf {} + 2>/dev/null || true

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

# ---- 2b. BRAND pass: rebrand the copied `Sample` example to `$BRAND` ----
# Files that may carry the Sample/sample token (code + config; docs already handled above,
# but .md is harmless to re-run). Excludes binary/build dirs (already pruned) and .git.
CODE_GLOBS=(-name '*.cs' -o -name '*.csproj' -o -name '*.sln' -o -name '*.props' \
            -o -name '*.json' -o -name '*.ts' -o -name '*.tsx' -o -name '*.mjs' \
            -o -name '*.html' -o -name '*.css' -o -name '*.yml' -o -name '*.yaml' \
            -o -name '*.http' -o -name 'Dockerfile' -o -name '.dockerignore' -o -name '*.md')

# 2b-i. content: Sample → $BRAND (PascalCase: namespaces, usings, types, project names,
#       paths, InternalsVisibleTo, ProjectReference, deploy.mjs Sample.Api, doc comments,
#       launch/appsettings/Dockerfile/compose). Then sample → $BRAND_LC (lowercase tokens:
#       sample.db, sample-data, sample-frontend, docker image/container name).
#       FIRST, though, retarget the two code-dir PREFIX tokens (sample.backend-services /
#       sample.frontend-services) to the repo SLUG — they must keep the hyphenated slug
#       ($REPO_SLUG, e.g. secrets-vault), NOT the lowercased brand. Doing it before the
#       generic `sample`→$BRAND_LC rule means the longer, specific token wins and the bare
#       rule never sees those substrings. (Path refs live in deploy.mjs, Dockerfile,
#       .dockerignore, codebase.md.)
while IFS= read -r -d '' f; do
  LC_ALL=C sed -i '' \
    -e "s|sample\.backend-services|$REPO_SLUG.backend-services|g" \
    -e "s|sample\.frontend-services|$REPO_SLUG.frontend-services|g" \
    -e "s|Sample|$BRAND|g" \
    -e "s|sample|$BRAND_LC|g" \
    "$f"
done < <(find "$REPO_DIR" -type f \( "${CODE_GLOBS[@]}" \) -not -path '*/.git/*' -print0)

# 2b-ii. rename Sample* files and dirs → $BRAND* (deepest paths first so parent renames
#        don't invalidate child paths). Covers Sample.sln, Sample.Api/, Sample.Tests/,
#        SampleDbContext.cs, the 5 Sample.* project dirs + their .csproj, etc.
while IFS= read -r -d '' p; do
  base="$(basename "$p")"
  newbase="${base//Sample/$BRAND}"
  [ "$base" = "$newbase" ] && continue
  mv "$p" "$(dirname "$p")/$newbase"
done < <(find "$REPO_DIR" -depth -name '*Sample*' -not -path '*/.git/*' -print0)

# 2b-iii. rename the two code-DIRS' slug prefix on disk: sample.{backend,frontend}-services
#         → $REPO_SLUG.{backend,frontend}-services (the hyphenated slug, matching the content
#         refs rewritten in 2b-i and the $BE_DIR/$FE_DIR vars). These dirs are lowercase
#         `sample.` so the uppercase-Sample pass above left them untouched.
for kind in backend frontend; do
  src="$CODEBASE/sample.$kind-services"
  dst="$CODEBASE/$REPO_SLUG.$kind-services"
  [ -d "$src" ] && [ "$src" != "$dst" ] && mv "$src" "$dst"
done

# ---- 2c. PORT pass: re-allocate the template's dev ports to the next-free pair ----
# Template binds 8220 (https) / 8221 (http) + 8225 (vite). Pick the next-free even/odd
# backend pair (HTTPS even, HTTP odd = even+1) starting from ports.md's "Next free", and
# a free vite port; scan existing launchSettings + vite configs to avoid collisions.
PORTS_MD="$WS_DIR/conventions/development/repo/ports.md"
TPL_HTTPS=8220; TPL_HTTP=8221; TPL_VITE=8225

# in-use ports across the whole workbench (every launchSettings + vite.config), minus the
# template copy we are about to overwrite (it still reads 8220/8221/8225 at this point).
used_ports() {
  {
    grep -rho -E 'localhost:[0-9]+' "$WB" --include=launchSettings.json 2>/dev/null | grep -o -E '[0-9]+'
    grep -rho -E 'port:[[:space:]]*[0-9]+' "$WB" --include=vite.config.ts 2>/dev/null | grep -o -E '[0-9]+'
  } | sort -un
}
USED="$(used_ports)"
is_free() { ! printf '%s\n' "$USED" | grep -qx "$1"; }

# seed from ports.md "Next free backend even port: N" (fallback 8230); bump to a free even
# whose +1 is also free, skipping the template's own 8220/8221.
SEED="$(grep -oE 'Next free backend even port:[[:space:]]*[0-9]+' "$PORTS_MD" 2>/dev/null | grep -oE '[0-9]+' | head -n1)"
NEW_HTTPS="${SEED:-8230}"
while :; do
  NEW_HTTP=$((NEW_HTTPS + 1))
  if [ "$NEW_HTTPS" != "$TPL_HTTPS" ] && is_free "$NEW_HTTPS" && is_free "$NEW_HTTP"; then break; fi
  NEW_HTTPS=$((NEW_HTTPS + 2))
done
# vite: first free port at/after 8225 that isn't the new backend pair or the template's.
NEW_VITE="$TPL_VITE"
while { [ "$NEW_VITE" = "$TPL_VITE" ] || ! is_free "$NEW_VITE"; } \
      || [ "$NEW_VITE" = "$NEW_HTTPS" ] || [ "$NEW_VITE" = "$NEW_HTTP" ]; do
  NEW_VITE=$((NEW_VITE + 1))
done

# rewrite the three ports across launchSettings, vite proxy, .http, appsettings (ports
# appear only in those files; do http→http first is moot since the values are distinct).
while IFS= read -r -d '' f; do
  LC_ALL=C sed -i '' \
    -e "s|$TPL_HTTPS|$NEW_HTTPS|g" \
    -e "s|$TPL_HTTP|$NEW_HTTP|g" \
    -e "s|$TPL_VITE|$NEW_VITE|g" \
    "$f"
done < <(find "$REPO_DIR" -type f \( -name 'launchSettings.json' -o -name 'vite.config.ts' \
            -o -name '*.http' -o -name 'appsettings*.json' \) -not -path '*/.git/*' -print0)

# append a ports.md row (into the table) + bump "Next free" to the next even after the
# pair we took. The new row is inserted as the last table row — anchored on the blank line
# that precedes the "Next free" line so it lands inside the table, not after it.
if [ -f "$PORTS_MD" ]; then
  NEXT_FREE=$((NEW_HTTPS + 2))
  LC_ALL=C awk -v sn="$SHORT_NAME" -v hs="$NEW_HTTPS" -v ht="$NEW_HTTP" -v vt="$NEW_VITE" -v nf="$NEXT_FREE" '
    # last table row before the trailing blank: emit our row right after it.
    prev ~ /^\| / && $0 == "" && !done {
      print "| " sn " | API · Vite | " hs " https / " ht " http · " vt " |"
      done=1
    }
    /^\*\*Next free backend even port:/ {
      print "**Next free backend even port: " nf ".** Append a row whenever you allocate."
      prev=$0; next
    }
    { print; prev=$0 }
  ' "$PORTS_MD" > "$PORTS_MD.tmp" && mv "$PORTS_MD.tmp" "$PORTS_MD"
fi

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
# the template ships a classic .sln (Sample.sln, rebranded to $BRAND.sln above).
BE_REL="$ORG/$REPO_NAME/engineering/codebase/$REPO_SLUG.backend-services/$BRAND.sln"
FE_REL="$ORG/$REPO_NAME/engineering/codebase/$REPO_SLUG.frontend-services"
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

[scaffold] mechanical scaffold done — template copied + rebranded Sample → $BRAND.
  repo dir   : $REPO_DIR
  backend    : $BE_DIR
               ($BRAND.sln + $BRAND.{Api,Application,Domain,Infrastructure,Persistence} + tests/$BRAND.Tests)
  frontend   : $FE_DIR
               (Vite/React app; deploy.mjs → $REPO_SLUG.backend-services/$BRAND.Api/wwwroot)
  ports      : $NEW_HTTPS https / $NEW_HTTP http · $NEW_VITE vite   (was 8220/8221 · 8225; ports.md row added)
  short name : $SHORT_NAME      (scripts/active.sh $SHORT_NAME)
  net        : net$NET_VERSION.0

Next (Claude): the working example is already in place — verify it builds
(dotnet build "$BE_DIR/$BRAND.sln") and fill the doc {{placeholders}}. No code-gen needed.
EOF

#!/usr/bin/env bash
#
# scaffold.sh — deterministic mechanics for the create-repo skill.
#   Creates workbench/{org}/{repo}, COPIES the product-repo template (which
#   ships a complete working `Sample` example — 5 Clean-Arch projects + unit /
#   E2E / migrations tests, a Vite/Vue frontend workspace, Docker, the deploy
#   descriptor and the CI and publish workflows), fills the doc {{placeholders}}, then
#   REBRANDS the example: Sample → Brand across all code/config, renames every
#   Sample* file/dir → Brand*, retargets the two code-dir slug prefixes
#   (sample.{backend,frontend}-services → {repo-slug}.{…}), and re-allocates the
#   template's dev ports to the next-free pair. Keeps the template's .gitignore,
#   `git init`s, and registers the repo in scripts/active.sh. It does NOT
#   generate code (the example is copied, not authored) and does NOT commit
#   (the developer manages git).
#
# Usage:
#   scaffold.sh <repo-name> <Brand> <org> [single|multi]
#   SHAPE=domain scaffold.sh <repo-name> <Brand> [org]
#     repo-name  e.g. wow-two-platform.foo   (the on-disk + git repo name)
#     Brand      PascalCase  e.g. Foo        (.NET namespace/project prefix; for a domain also the NuGet id part)
#     org        wow-two | wow-two-platform | maxs-projects/ventures/{saas|consumer|labs} | …  (workbench subfolder;
#                a domain defaults to wow-two-sdk-beta)
#     mode       single (default) | multi    (informational — drives later product work, not the mechanics; a domain
#                ignores it)
#
# Env:
#   SHAPE         product (default) | domain — which template: the product template, or the domain library template
#                 (wow-two-sdk-beta.domain-template: be packages, fe package, service, image, tag-derived releases)
#   SLUG          the code-dir prefix and fe package suffix; defaults to the repo name's last dot-segment
#   PRODUCT       the lowercase product/service/catalog slug; defaults to the lowercased Brand
#   CORE_VERSION  domain: the be sdk pin written to BackendSdkVersion (default: the template's)
#   FE_VERSION    domain: the exact @wow-two-beta/fe pin and the fe package's peer floor (default: the template's);
#                 a change refreshes pnpm-lock.yaml (network)
#   SCRATCH=1     scaffold into a temp dir (SCRATCH_DIR, else mktemp): no ports.md row, no active.sh row, no git init —
#                 a template check leaves nothing in the workbench to remove
#   INTO=clone    fill an existing empty clone at the target (`gh repo clone owner/name workbench/{org}/{repo}` of a
#                 repository with no commits) instead of creating the dir: its .git and origin stay, git init is
#                 skipped, every other pass runs. With SCRATCH=1 the clone is SCRATCH_DIR/{repo} (a template check).
#                 The create-library skill drives it: scripts/release/library.py prints the command.
#   NET_VERSION   defaults to 10   (TargetFramework net{N}.0)
#
# Idempotency: refuses to clobber an existing repo dir (with INTO=clone: a clone that holds a commit or any file);
# appends to active.sh only if the project name is not already registered.

set -euo pipefail

# ---- resolve workspace paths (skill lives at .claude/skills/create-repo/) ----
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WS_DIR="$(cd "$SCRIPT_DIR/../../.." && pwd)"     # .claude/skills/create-repo → WS root
WB="$WS_DIR/workbench"
ACTIVE="$WS_DIR/scripts/active.sh"
SHAPE="${SHAPE:-product}"
SCRATCH="${SCRATCH:-0}"
INTO="${INTO:-}"
case "$INTO" in
  ''|clone) ;;
  *) echo "INTO must be clone or unset, not '$INTO'" >&2; exit 2 ;;
esac

# Each shape names its template and the dev ports its example binds (https / http / vite), which the port pass moves.
case "$SHAPE" in
  product)
    TEMPLATE="$WS_DIR/workbench/wow-two-sdk-beta/wow-two-sdk-beta.product-template"
    TPL_HTTPS=8220; TPL_HTTP=8221; TPL_VITE=8224
    DEFAULT_ORG="" ;;
  domain)
    TEMPLATE="$WS_DIR/workbench/wow-two-sdk-beta/wow-two-sdk-beta.domain-template"
    TPL_HTTPS=8384; TPL_HTTP=8385; TPL_VITE=8386
    DEFAULT_ORG="wow-two-sdk-beta" ;;
  *) echo "SHAPE must be product or domain, not '$SHAPE'" >&2; exit 2 ;;
esac
TEMPLATE_NAME="$(basename "$TEMPLATE")"

# ---- args ----
REPO_NAME="${1:?repo-name required (e.g. wow-two-platform.foo)}"
BRAND="${2:?Brand required (PascalCase, e.g. Foo)}"
ORG="${3:-$DEFAULT_ORG}"
[ -n "$ORG" ] || { echo "org required (wow-two | wow-two-platform | maxs-projects/ventures/<saas, consumer or labs> | …)" >&2; exit 2; }
case "${ORG%/}" in
  maxs-projects/ventures) echo "org must name a venture group: maxs-projects/ventures/{saas|consumer|labs}" >&2; exit 2 ;;
esac
MODE="${4:-single}"
NET_VERSION="${NET_VERSION:-10}"

# repo-slug = the repo's distinctive name = its LAST dot-segment, slugified
# (wow-two-platform.secrets-vault → "secrets-vault"; keeps the hyphen — NOT the
# lowercased brand "secretsvault"). Used for: the {{repo-slug}} doc placeholder
# AND the two code-dir prefixes ({slug}.backend-services / {slug}.frontend-services).
REPO_SLUG="${SLUG:-$(printf '%s' "${REPO_NAME##*.}" | tr '[:upper:]' '[:lower:]' | tr ' .' '--')}"
# short name = active.sh first column (e.g. "secrets-vault") — same as the slug.
SHORT_NAME="$REPO_SLUG"
# lowercase brand — for the template's lowercase `sample` tokens (sample.db, sample-data,
# sample-frontend, docker image/container name, the deploy.yml product and service slug).
# Brand is PascalCase → just lowercase it.
BRAND_LC="${PRODUCT:-$(printf '%s' "$BRAND" | tr '[:upper:]' '[:lower:]')}"
# uppercase brand — for the template's `SAMPLE` token (the deploy.yml dev check's VERIFY_SERVICE_SAMPLE variable,
# which the runner derives from the service slug).
BRAND_UC="$(printf '%s' "$BRAND_LC" | tr '[:lower:]-' '[:upper:]_')"
# snake-case product — for SQL identifiers (the domain module's `sample_` table prefix), which refuse a hyphen.
BRAND_SNAKE="$(printf '%s' "$BRAND_LC" | tr '-' '_')"
# the GitHub owner in package metadata URLs: the org folder's last segment (folder name = org name).
OWNER="${ORG##*/}"
TODAY="$(date +%F)"

if [ "$SCRATCH" = 1 ]; then
  SCRATCH_ROOT="${SCRATCH_DIR:-$(mktemp -d "${TMPDIR:-/tmp}/create-repo.XXXXXX")}"
  REPO_DIR="$SCRATCH_ROOT/$REPO_NAME"
else
  REPO_DIR="$WB/$ORG/$REPO_NAME"
fi
CODEBASE="$REPO_DIR/engineering/codebase"
# the two code dirs carry the repo slug as a dot-prefix (collision-avoidance across
# open IDEs). The template ships them as sample.backend-services / sample.frontend-services;
# the rename pass below retargets the prefix to $REPO_SLUG.
BE_DIR="$CODEBASE/$REPO_SLUG.backend-services"
FE_DIR="$CODEBASE/$REPO_SLUG.frontend-services"

echo "[scaffold] shape=$SHAPE repo=$REPO_NAME brand=$BRAND org=$ORG slug=$REPO_SLUG product=$BRAND_LC mode=$MODE net=$NET_VERSION scratch=$SCRATCH into=${INTO:-new}"
echo "[scaffold] target=$REPO_DIR"

# ---- guardrails ----
[ -d "$TEMPLATE" ] || { echo "[scaffold] template missing: $TEMPLATE" >&2; exit 1; }
if [ "$INTO" = clone ]; then
  # An empty clone: a git repository with no commit and nothing beside its .git, so the stamp overwrites nothing.
  [ -d "$REPO_DIR/.git" ] || { echo "[scaffold] INTO=clone needs a clone at $REPO_DIR (gh repo clone owner/name <path>)" >&2; exit 1; }
  if git -C "$REPO_DIR" rev-parse --verify -q 'HEAD^{commit}' >/dev/null; then
    echo "[scaffold] refusing to stamp a clone that already holds a commit: $REPO_DIR" >&2; exit 1
  fi
  if [ -n "$(find "$REPO_DIR" -mindepth 1 -maxdepth 1 ! -name .git -print -quit)" ]; then
    echo "[scaffold] refusing to stamp a clone that already holds files: $REPO_DIR" >&2; exit 1
  fi
  ORIGIN_URL="$(git -C "$REPO_DIR" remote get-url origin 2>/dev/null || true)"
  echo "[scaffold] filling the empty clone (origin: ${ORIGIN_URL:-none})"
else
  [ -e "$REPO_DIR" ] && { echo "[scaffold] refusing to clobber existing: $REPO_DIR" >&2; exit 1; }
fi
# Reject an outdated starter before creating a repository, allocating ports or registering it.
node "$SCRIPT_DIR/validate-frontend.mjs" "$TEMPLATE/engineering/codebase/sample.frontend-services"

# ---- 1. create + copy template (incl. the complete `Sample` example) ----
if [ "$INTO" = clone ]; then
  # copy every top-level entry but the template's .git into the clone, which keeps its own .git and origin.
  find "$TEMPLATE" -mindepth 1 -maxdepth 1 ! -name .git -exec cp -R {} "$REPO_DIR/" \;
else
  mkdir -p "$(dirname "$REPO_DIR")"
  cp -R "$TEMPLATE" "$REPO_DIR"
  # drop the template's own git history.
  rm -rf "$REPO_DIR/.git"
fi
# drop any build artifacts that rode along in the copy; a clone's .git (its logs/ included) stays untouched.
find "$REPO_DIR" -path "$REPO_DIR/.git" -prune -o -type d \( -name bin -o -name obj -o -name node_modules -o -name dist -o -name logs \) \
  -prune -exec rm -rf {} + 2>/dev/null || true
# ... and anything a local run left in the template: the built SPA in wwwroot (only .gitkeep stays), SQLite files
# and this machine's own or a target's settings files.
find "$REPO_DIR" -path "$REPO_DIR/.git" -prune -o -type d -name wwwroot -exec find {} -mindepth 1 -not -name .gitkeep -delete \; 2>/dev/null || true
find "$REPO_DIR" -type f -not -path "$REPO_DIR/.git/*" \( -name '*.db' -o -name '*.db-shm' -o -name '*.db-wal' -o -name '*.nupkg' -o -name '*.snupkg' -o -name '*.tgz' \
  -o -name 'appsettings.Local.json' -o -name 'appsettings.Target.json' -o -name 'appsettings.Machine.json' \) -delete

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
done < <(find "$REPO_DIR" -path "$REPO_DIR/.git" -prune -o -type f \( -name '*.md' -o -name '*.json' -o -name '*.txt' \) -print0)

# ---- 2b. BRAND pass: rebrand the copied `Sample` example to `$BRAND` ----
# Files that may carry the Sample/sample token (code + config; docs already handled above,
# but .md is harmless to re-run). Excludes binary/build dirs (already pruned) and .git.
CODE_GLOBS=(-name '*.cs' -o -name '*.csproj' -o -name '*.sln' -o -name '*.slnx' -o -name '*.props' \
            -o -name '*.json' -o -name '*.ts' -o -name '*.tsx' -o -name '*.vue' -o -name '*.mjs' \
            -o -name '*.html' -o -name '*.css' -o -name '*.yml' -o -name '*.yaml' \
            -o -name '*.http' -o -name 'Dockerfile' -o -name '.dockerignore' -o -name '.gitignore' -o -name '*.md' \
            -o -name '*.sh' -o -name '*.sql')

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
# Domain-only rules run first, so the specific tokens win over the generic `sample`: the template's repo name in the
# package metadata URLs, the fe package `fe-sample` → `fe-{slug}` (the hyphenated slug, which differs from the
# lowercased Brand for names like FileStorage), and the module's `sample_` table prefix → snake case.
DOMAIN_RULES=()
if [ "$SHAPE" = domain ]; then
  DOMAIN_RULES=(
    -e "s|wow-two-sdk-beta/$TEMPLATE_NAME|$OWNER/$REPO_NAME|g"
    -e "s|$TEMPLATE_NAME|$REPO_NAME|g"
    -e "s|fe-sample|fe-$REPO_SLUG|g"
    -e "s|sample_|${BRAND_SNAKE}_|g"
  )
fi
while IFS= read -r -d '' f; do
  LC_ALL=C sed -i '' \
    ${DOMAIN_RULES[@]+"${DOMAIN_RULES[@]}"} \
    -e "s|sample\.backend-services|$REPO_SLUG.backend-services|g" \
    -e "s|sample\.frontend-services|$REPO_SLUG.frontend-services|g" \
    -e "s|Sample|$BRAND|g" \
    -e "s|sample|$BRAND_LC|g" \
    -e "s|SAMPLE|$BRAND_UC|g" \
    "$f"
done < <(find "$REPO_DIR" -type f \( "${CODE_GLOBS[@]}" \) -not -path '*/.git/*' -print0)

# 2b-ii. rename Sample* files and dirs → $BRAND* (deepest paths first so parent renames
#        don't invalidate child paths). Covers Sample.BackendServices.slnx, Sample.Api/, tests/Sample.Tests.*/,
#        SampleDbContext.cs, the 5 Sample.* project dirs + their .csproj, etc.
while IFS= read -r -d '' p; do
  base="$(basename "$p")"
  newbase="${base//Sample/$BRAND}"
  [ "$base" = "$newbase" ] && continue
  mv "$p" "$(dirname "$p")/$newbase"
done < <(find "$REPO_DIR" -depth -name '*Sample*' -not -path '*/.git/*' -print0)

# 2b-ii-b. domain: rename the fe package dir fe-sample → fe-$REPO_SLUG (the content refs were rewritten in 2b-i).
if [ "$SHAPE" = domain ]; then
  while IFS= read -r -d '' p; do
    mv "$p" "$(dirname "$p")/fe-$REPO_SLUG"
  done < <(find "$REPO_DIR" -depth -type d -name 'fe-sample' -not -path '*/.git/*' -print0)
fi

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
# Template binds 8220 (https) / 8221 (http) + 8224 (vite). Pick the next-free even/odd
# backend pair (HTTPS even, HTTP odd = even+1) starting from ports.md's "Next free", and
# a free vite port; scan existing launchSettings + vite configs to avoid collisions.
PORTS_MD="$WS_DIR/conventions/deployment/hosting/ports.md"
# TPL_HTTPS / TPL_HTTP / TPL_VITE come from the shape (top of the script).

# in-use ports across the whole workbench (every launchSettings + vite.config), minus the
# template copy we are about to overwrite (it still reads 8220/8221/8224 at this point).
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
# vite: first free even port after the template's that isn't the new backend pair or the template's.
NEW_VITE="$TPL_VITE"
while { [ "$NEW_VITE" = "$TPL_VITE" ] || ! is_free "$NEW_VITE"; } \
      || [ "$NEW_VITE" = "$NEW_HTTPS" ] || [ "$NEW_VITE" = "$NEW_HTTP" ]; do
  NEW_VITE=$((NEW_VITE + 2))
done

# rewrite the three ports across launchSettings, vite proxy, .http, appsettings, the local compose file and the two
# docs that name them (ports appear only in those files; do http→http first is moot since the values are distinct).
while IFS= read -r -d '' f; do
  LC_ALL=C sed -i '' \
    -e "s|$TPL_HTTPS|$NEW_HTTPS|g" \
    -e "s|$TPL_HTTP|$NEW_HTTP|g" \
    -e "s|$TPL_VITE|$NEW_VITE|g" \
    "$f"
done < <(find "$REPO_DIR" -type f \( -name 'launchSettings.json' -o -name 'vite.config.ts' \
            -o -name '*.http' -o -name 'appsettings*.json' -o -name 'docker-compose.yml' \
            -o -name 'frontend-guidelines.md' -o -name 'deployment.md' \) -not -path '*/.git/*' -print0)

# append a ports.md row (into the table) + bump "Next free" to the next even after the
# pair we took. The new row is inserted as the last table row — anchored on the blank line
# that precedes the "Next free" line so it lands inside the table, not after it.
if [ -f "$PORTS_MD" ] && [ "$SCRATCH" != 1 ]; then
  NEXT_FREE=$((NEW_HTTPS + 2))
  # the Vite port may sit right after the pair (domain repos take it from the same range); skip past it
  if [ "$NEW_VITE" -ge "$NEXT_FREE" ]; then NEXT_FREE=$((NEW_VITE + 2)); fi
  LC_ALL=C awk -v sn="$SHORT_NAME" -v hs="$NEW_HTTPS" -v ht="$NEW_HTTP" -v vt="$NEW_VITE" -v nf="$NEXT_FREE" '
    # last table row before the trailing blank: emit our row right after it.
    prev ~ /^\| / && $0 == "" && !done {
      print "| " sn " | API · Vite | " hs " https / " ht " http · " vt " |"
      done=1
    }
    /^\*\*Next free backend even port:/ {
      print "**Next free backend even port: " nf ".** Append a row whenever you allocate, and move this number past every port the row takes, its Vite port included."
      prev=$0; next
    }
    { print; prev=$0 }
  ' "$PORTS_MD" > "$PORTS_MD.tmp" && mv "$PORTS_MD.tmp" "$PORTS_MD"
fi

# ---- 3. root .gitignore ----
# The template ships its own (rebranded above with the other code/config files: the built wwwroot, settings files and
# SQLite files stay out). Only a template without one gets this fallback.
if [ ! -f "$REPO_DIR/.gitignore" ]; then
  cat > "$REPO_DIR/.gitignore" <<'EOF'
**/bin/
**/obj/
**/dist/
**/logs/
node_modules/
*.db
*.db-shm
*.db-wal
**/appsettings.Local.json
**/appsettings.Target.json
**/appsettings.Machine.json
.env
.idea/
.vs/
.DS_Store
EOF
fi

# ---- 3b. domain pins: core and the fe sdk ----
# CORE_VERSION rewrites the BackendSdkVersion pin (each package's nuspec floor). FE_VERSION rewrites the exact
# @wow-two-beta/fe pin of every workspace manifest and the fe package's peer floor (>=FE_VERSION <0.1.0), then
# refreshes the lockfile, since a frozen install would refuse the changed manifests.
if [ "$SHAPE" = domain ]; then
  TPL_CORE="$(sed -n 's|.*<BackendSdkVersion>\(.*\)</BackendSdkVersion>.*|\1|p' "$BE_DIR/Directory.Packages.props")"
  TPL_FE="$(node -p "require(process.argv[1]).dependencies['@wow-two-beta/fe']" "$FE_DIR/apps/web/package.json")"
  CORE_VERSION="${CORE_VERSION:-$TPL_CORE}"
  FE_VERSION="${FE_VERSION:-$TPL_FE}"
  if [ "$CORE_VERSION" != "$TPL_CORE" ]; then
    LC_ALL=C sed -i '' "s|<BackendSdkVersion>$TPL_CORE</BackendSdkVersion>|<BackendSdkVersion>$CORE_VERSION</BackendSdkVersion>|" \
      "$BE_DIR/Directory.Packages.props"
  fi
  if [ "$FE_VERSION" != "$TPL_FE" ]; then
    while IFS= read -r -d '' f; do
      LC_ALL=C sed -i '' \
        -e "s|\"@wow-two-beta/fe\": \"$TPL_FE\"|\"@wow-two-beta/fe\": \"$FE_VERSION\"|g" \
        -e "s|\"@wow-two-beta/fe\": \">=$TPL_FE <0.1.0\"|\"@wow-two-beta/fe\": \">=$FE_VERSION <0.1.0\"|g" \
        "$f"
    done < <(find "$FE_DIR" -name package.json -not -path '*/node_modules/*' -print0)
    (cd "$FE_DIR" && pnpm install --lockfile-only --silent)
  fi
fi

# Verify the copied/rebranded frontend before registering the result as a usable scaffold.
node "$SCRIPT_DIR/validate-frontend.mjs" "$FE_DIR"

# A scratch scaffold stops here: no git, no active.sh row, no ports row — nothing to clean up in the workbench.
if [ "$SCRATCH" = 1 ]; then
  cat <<EOF

[scaffold] scratch scaffold done — $SHAPE template copied + rebranded Sample → $BRAND (no git, no registration).
  repo dir   : $REPO_DIR
  backend    : $BE_DIR
  frontend   : $FE_DIR
  ports      : $NEW_HTTPS https / $NEW_HTTP http · $NEW_VITE vite   (was $TPL_HTTPS/$TPL_HTTP · $TPL_VITE; no ports.md row)
EOF
  exit 0
fi

# ---- 4. git init (NO commit — developer owns git) ----
if [ ! -d "$REPO_DIR/.git" ]; then
  git -C "$REPO_DIR" init -q -b main
  echo "[scaffold] git initialized on main (no commit made)"
fi

# ---- 5. register in scripts/active.sh PROJECTS array ----
# entry: name|backend-sln(relative to workbench/)|frontend-dir(relative to workbench/)
# the template ships Sample.BackendServices.slnx, rebranded to $BRAND.BackendServices.slnx above.
BE_REL="$ORG/$REPO_NAME/engineering/codebase/$REPO_SLUG.backend-services/$BRAND.BackendServices.slnx"
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
if [ "$SHAPE" = domain ]; then
  BE_SHAPE="$BRAND.BackendServices.slnx: packages/{Abstractions,Module,Client,Testing} (WoW2.Sdk.Beta.Be.$BRAND.*) + service/$BRAND.Api + tests/$BRAND.Tests.{Unit,Integration,E2E,Conformance,Migrations}"
  FE_SHAPE="pnpm workspace: packages/fe-$REPO_SLUG (@wow-two-beta/fe-$REPO_SLUG) + apps/web (hosted pages + console)"
else
  BE_SHAPE="$BRAND.BackendServices.slnx + $BRAND.{Api,Application,Domain,Infrastructure,Persistence} + tests/$BRAND.Tests.{Unit,E2E,Migrations}"
  FE_SHAPE="pnpm workspace; Vue app in apps/web; single-host deployment"
fi
cat <<EOF

[scaffold] mechanical scaffold done — $SHAPE template copied + rebranded Sample → $BRAND.
  repo dir   : $REPO_DIR
  backend    : $BE_DIR
               ($BE_SHAPE)
  frontend   : $FE_DIR
               ($FE_SHAPE)
  ports      : $NEW_HTTPS https / $NEW_HTTP http · $NEW_VITE vite   (was $TPL_HTTPS/$TPL_HTTP · $TPL_VITE; ports.md row added)
  short name : $SHORT_NAME      (scripts/active.sh $SHORT_NAME)
  net        : net$NET_VERSION.0

Next (Claude): the working example is already in place — verify it
(dotnet test "$BE_DIR/$BRAND.BackendServices.slnx") and fill the doc {{placeholders}}. No code-gen needed.
EOF

# Printed, not applied: the catalog entry (free text and quoting rules) and the git-flag directive, which only the
# developer can send, as one whole message.
if [ "$SHAPE" = domain ]; then
  cat <<EOF

Catalog entry for catalog.yml (fill purpose and status, then run scripts/gen-repo-registry.py;
scripts/release/library.py apply-local catalog writes it for the create-library skill):
  - slug: $BRAND_LC
    name: $BRAND
    workspace: wow2-platform
    kind: platform
    deploy: none
    status: "Planned"
    purpose: "{{one line}}"
    repositories: [$OWNER/$REPO_NAME]

Git flags: a folder override (~git_on commit,push workbench/$ORG/*) covers the repo; without one, once the remote
exists, the developer sends this as one whole message:
  ~git_on commit,push workbench/$ORG/$REPO_NAME
EOF
fi

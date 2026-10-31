#!/usr/bin/env python3
"""create-library: carry a new domain library from the domain template to a GitHub repo, published packages, an image,
hub registration and consumer re-pins. Design: ideas/identity-analysis-2026-10/t9-release-automation.md (§ 4 phases);
skill: .claude/skills/create-library/SKILL.md.

The script only reads. It probes the local folder, GitHub (`gh api` GETs), nuget.org, npm and the hub, shows each phase
as done, next or blocked, and prints the next phase's exact commands. It makes no GitHub, registry, commit or push
write: the agent runs each printed command as its own Bash call, so the git guard judges every write. `apply-local`
and `repin` write local files only (the hub catalog entry, consumer pins). State comes from the probes, never from a
state file, so a re-run resumes at the first unfinished step.

Usage (python3 -I, stdlib only):
  library.py plan   <repo> [options]       status by phase, the next phase's commands, the hand-step checklist (default)
  library.py status <repo> [options]       status by phase only
  library.py next   <repo> [options]       the next phase's commands and the hand-step checklist only
  library.py apply-local catalog <repo> --purpose "..."   write the hub catalog entry (deploy: none)
  library.py apply-local deploy  <repo>                   set the catalog entry to deploy: wheelhouse
  library.py repin <repo> --version V [--fe-version V] [--only <path>] [--write]   consumer pins; dry run without --write

Inputs: <repo> as wow-two-sdk-beta.identity; --brand the PascalCase domain (default: the repo's last segment);
--org the workbench folder and GitHub owner (default wow-two-sdk-beta); --slug and --product as scaffold.sh's SLUG and
PRODUCT; --core-version and --fe-version pass to scaffold.sh.
Steps no probe can see take --confirmed nuget-policy,wheelhouse,secrets once checked; --publish opens the registry
phase while the packages still hold the template's Greetings sample; --offline skips network probes.
"""
import argparse
import importlib.util
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SELF = "scripts/release/library.py"
RULESET = "scripts/release/main-guard.json"
SCAFFOLD = ".claude/skills/create-repo/scaffold.sh"
TEMPLATE = "workbench/wow-two-sdk-beta/wow-two-sdk-beta.domain-template"
FLAGS_HELPER = ".claude/hooks/commit_permission.py"
REGISTRY_GEN = "scripts/gen-repo-registry.py"

DEFAULT_ORG = "wow-two-sdk-beta"
ACCOUNT = "sulton-max"                          # personal git rule: every folder outside the EPAM ones
EXPECTED_EMAIL = "sultonbek.rakhimov@gmail.com"  # the commit identity those folders resolve to
PARTS = ("Abstractions", "Module", "Client", "Testing")
FIRST_FE_VERSION = "0.0.1"
NPM_TRUST_MIN = (11, 15, 0)
TOOLS = ("git", "gh", "dotnet", "node", "pnpm", "npm")
REQUIRED_PLACEHOLDERS = ("{{ONE_LINE_WHAT_THIS_IS}}", "{{PLACEHOLDER}}")
HUB_PATHS = ("catalog.yml", ".claude/repo-registry.md", "scripts/active.sh",
             "conventions/deployment/hosting/ports.md", "docs/platform-apps.md")
CONFIRMABLE = ("nuget-policy", "wheelhouse", "secrets")
HUB_INDEX_RULE = ("the hub is a shared tree: when `git diff --cached` lists a path beyond these, or a path holds another "
                  "lane's hunk, stop and ask before the commit")
WHEELHOUSE_APP = "wheelhouse-max"
CODEX_APP = "chatgpt-codex-connector"
TIMEOUT = 25
SKIP_DIRS = {".git", "node_modules", "bin", "obj", "dist", ".venv", "venv", "__pycache__", ".cache", "wwwroot",
             ".idea", ".vs", "coverage", ".vite", ".gradle", "Pods", "DerivedData"}
GITHUB_SLUG = re.compile(r"github\.com[:/]+([^/\s]+)/([^/\s]+?)(?:\.git)?/?$", re.I)
CATALOG_SLUG = re.compile(r"^[a-z][a-z0-9-]{0,47}$")

PHASES = {0: "Preflight", 1: "GitHub", 2: "Scaffold", 3: "Hub", 4: "Registries", 5: "Image", 6: "Wheelhouse",
          7: "Consumers"}
DONE = ("done", "skip")


# ------------------------------------------------------------------------------------------------------------ inputs

def pascal(name):
    return "".join(part[:1].upper() + part[1:] for part in re.split(r"[-_. ]+", name) if part)


@dataclass
class Library:
    repo: str
    brand: str = ""
    org: str = DEFAULT_ORG
    slug: str = ""
    product: str = ""
    account: str = ACCOUNT
    root: Path = ROOT
    core_version: str = ""
    fe_version: str = ""
    description: str = ""

    def __post_init__(self):
        self.org = self.org.strip("/")
        last = self.repo.rsplit(".", 1)[-1]
        self.slug = self.slug or re.sub(r"[ .]", "-", last.lower())
        self.brand = self.brand or pascal(last)
        self.product = self.product or self.brand.lower()
        self.root = Path(self.root)

    @property
    def owner(self):
        return self.org.split("/")[-1]

    @property
    def full(self):
        return f"{self.owner}/{self.repo}"

    @property
    def rel(self):
        return f"workbench/{self.org}/{self.repo}"

    @property
    def path(self):
        return self.root / self.rel

    @property
    def backend(self):
        return self.path / "engineering" / "codebase" / f"{self.slug}.backend-services"

    @property
    def frontend(self):
        return self.path / "engineering" / "codebase" / f"{self.slug}.frontend-services"

    @property
    def slnx(self):
        return self.backend / f"{self.brand}.BackendServices.slnx"

    @property
    def fe_package(self):
        return f"@wow-two-beta/fe-{self.slug}"

    @property
    def fe_dir(self):
        return self.frontend / "packages" / f"fe-{self.slug}"

    @property
    def nuget_ids(self):
        return [f"WoW2.Sdk.Beta.Be.{self.brand}.{part}" for part in PARTS]

    @property
    def nuget_glob(self):
        return f"WoW2.Sdk.Beta.Be.{self.brand}.*"

    @property
    def image_path(self):
        """The GHCR package, as the delivery workflow pushes it: lowercase owner/repo/product."""
        return f"{self.full}/{self.product}".lower()

    @property
    def pin_property(self):
        return f"{self.brand}SdkVersion"

    @property
    def tarball(self):
        return self.path / f"fe-{self.slug}-{FIRST_FE_VERSION}.tgz"

    def problems(self):
        out = []
        if not re.fullmatch(r"[a-z0-9][a-z0-9.-]*", self.repo):
            out.append(f"repo `{self.repo}` must be lowercase, dot-separated")
        if not self.repo.startswith(self.owner + "."):
            out.append(f"repo `{self.repo}` must start with its org `{self.owner}.` (repo naming)")
        if not re.fullmatch(r"[A-Z][A-Za-z0-9]*", self.brand):
            out.append(f"brand `{self.brand}` must be PascalCase")
        if not CATALOG_SLUG.fullmatch(self.product):
            out.append(f"product `{self.product}` must match {CATALOG_SLUG.pattern} (catalog slug)")
        if not re.fullmatch(r"[a-z][a-z0-9-]*", self.slug):
            out.append(f"slug `{self.slug}` must be lowercase with hyphens")
        return out


def q(value):
    return shlex.quote(str(value))


def gh(lib, rest):
    """A gh call that names its account (personal git rule: the folder decides, never the active account)."""
    return f'GH_TOKEN="$(gh auth token -u {lib.account})" gh {rest}'


def me(lib, rest):
    """A call of this script with the same inputs."""
    base = [f"python3 -I {q(lib.root / SELF)}", rest, q(lib.repo), f"--brand {q(lib.brand)}", f"--org {q(lib.org)}"]
    if lib.slug != re.sub(r"[ .]", "-", lib.repo.rsplit(".", 1)[-1].lower()):
        base.append(f"--slug {q(lib.slug)}")
    if lib.product != lib.brand.lower():
        base.append(f"--product {q(lib.product)}")
    return " ".join(base)


# ------------------------------------------------------------------------------------------------------------- state

@dataclass
class Pin:
    file: Path
    repo: Path
    kind: str      # property · package · npm
    name: str
    current: str


@dataclass
class Run:
    status: str = ""       # queued · in_progress · completed
    conclusion: str = ""   # success · failure · cancelled · skipped …
    url: str = ""


@dataclass
class State:
    """Probe results. None means unknown (offline, a failed probe); every field is plain data for tests."""
    tools_missing: list = field(default_factory=list)
    account_ok: object = None
    template_ok: object = True
    scaffold_into: object = True
    flags: object = None             # {"commit": bool, "push": bool, "source": str}
    hub_flags: object = None
    author: object = None            # the commit email the folder resolves to
    npm_version: object = None       # the local npm version, as a tuple
    # local folder
    folder: str = "missing"          # missing · empty · empty-clone · clone · foreign
    origin: object = None
    head: object = None              # local HEAD sha, "" without a commit
    scaffolded: bool = False
    placeholders: list = field(default_factory=list)
    description: str = ""
    sample_content: object = None
    # GitHub
    repo_exists: object = None
    visibility: object = None        # private · public
    settings: object = None          # {"has_issues": …, "has_wiki": …, "has_projects": …, "has_discussions": …}
    workflow: object = None          # {"default_workflow_permissions": …, "can_approve_pull_request_reviews": …}
    actions_enabled: object = None
    rulesets: object = None          # [name]
    remote_main: object = None       # sha, "" when main does not exist
    publish_var: object = None       # the PUBLISH_PACKAGES value, "" when unset
    be_tags: object = None           # versions from be-v* tags
    fe_tags: object = None
    release_tag: object = None       # the newest release's tag, "" when none
    packages_run: object = None      # Run of publish-packages.yml
    image_run: object = None         # Run of publish-docker-image.yml
    image_public: object = None      # True when ghcr.io hands an anonymous pull token for the image, False when private
    org_apps: object = None          # app slugs installed on the org
    # hub
    catalog_entry: object = None     # {"slug", "deploy", "repositories", …} or None
    catalog_mismatch: bool = False   # an entry has the product slug but not this repository
    registry_fresh: object = None
    hub_dirty: list = field(default_factory=list)
    hub_committed: bool = False
    hub_pushed: bool = False
    deploy_worktree: str = ""        # the entry's deploy value in the working tree, HEAD and origin/main
    deploy_head: str = ""
    deploy_origin: str = ""
    platform_row: str = "none"       # none · named · unnamed
    # registries
    nuget_versions: object = None
    npm_versions: object = None
    # consumers
    consumers: object = None         # [Pin]
    consumer_flags: dict = field(default_factory=dict)


def vkey(version):
    """A sort key for 10.0.3-beta and 0.0.12: numeric parts, then a release above its prereleases."""
    core, _, pre = version.partition("-")
    nums = tuple(int(n) if n.isdigit() else 0 for n in core.split("."))
    return nums, pre == "", pre


def newest(versions):
    return max(versions, key=vkey) if versions else ""


# ------------------------------------------------------------------------------------------------------------ probes

def parse_flags(text):
    """{"commit": bool, "push": bool, "source": str} from commit_permission.py status output, or None."""
    match = re.search(r"GIT FLAGS for [^:]+: commit (ON|OFF)(?: \(([^)]*)\))? · push (ON|OFF)(?: \(([^)]*)\))?", text)
    if not match:
        return None
    return {"commit": match.group(1) == "ON", "push": match.group(3) == "ON", "source": match.group(2) or ""}


def origin_slug(config):
    """`owner/name` of the `origin` remote in a .git/config file, the raw URL for a non-GitHub one, else None."""
    try:
        text = Path(config).read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None
    section = None
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("["):
            section = stripped
            continue
        key, sep, value = stripped.partition("=")
        if section == '[remote "origin"]' and sep and key.strip() == "url":
            match = GITHUB_SLUG.search(value.strip())
            return f"{match.group(1)}/{match.group(2)}" if match else value.strip()
    return None


def folder_state(path, full):
    """(state, origin): missing · empty · empty-clone · clone · foreign, and the clone's origin."""
    path = Path(path)
    if not path.exists():
        return "missing", None
    if not path.is_dir():
        return "foreign", None
    names = sorted(entry.name for entry in path.iterdir())
    if not names:
        return "empty", None
    if not (path / ".git").is_dir():
        return "foreign", None
    origin = origin_slug(path / ".git" / "config")
    if not origin or origin.lower() != full.lower():
        return "foreign", origin
    return ("empty-clone" if names == [".git"] else "clone"), origin


def placeholders_in(path):
    """(relative file, token) for each required placeholder left in the repo's docs and manifests."""
    found = []
    path = Path(path)
    for directory, dirs, files in os.walk(path):
        dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS)
        for name in sorted(files):
            if not name.endswith((".md", ".json")):
                continue
            file = Path(directory) / name
            try:
                text = file.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            found += [(str(file.relative_to(path)), token) for token in REQUIRED_PLACEHOLDERS if token in text]
    return found


def has_sample(lib):
    """True while the packages still hold the template's Greetings sample (T9 § 4: no placeholder ships)."""
    packages = lib.backend / "packages"
    be = packages.is_dir() and any((part / "Greetings").is_dir() for part in packages.iterdir() if part.is_dir())
    src = lib.fe_dir / "src"
    fe = src.is_dir() and any(name.startswith("Greeting") for _, _, files in os.walk(src) for name in files)
    return be or fe


def entry_block(text, slug):
    """The catalog text of the entry `- slug: {slug}`, or "" when absent."""
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if re.fullmatch(rf"  - slug: {re.escape(slug)}\s*", line):
            end = i + 1
            while end < len(lines) and lines[end].startswith("    "):
                end += 1
            return "\n".join(lines[i:end])
    return ""


def block_field(block, key):
    match = re.search(rf"^    {re.escape(key)}: *(.*)$", block, re.M)
    return match.group(1).strip().strip('"') if match else ""


def platform_row(text, brand, repo):
    for line in text.splitlines():
        if line.startswith("|") and f"**{brand}**" in line:
            return "named" if f"`{repo}`" in line else "unnamed"
    return "none"


def load_registry(root):
    sys.dont_write_bytecode = True  # a probe leaves no __pycache__ beside the generator
    spec = importlib.util.spec_from_file_location("gen_repo_registry", Path(root) / REGISTRY_GEN)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def catalog_lookup(entries, lib):
    """(entry, mismatch): the entry naming this repository, else one holding the product slug (mismatch)."""
    for entry in entries:
        if lib.full.lower() in [r.lower() for r in entry.get("repositories") or []]:
            return entry, False
    for entry in entries:
        if entry.get("slug") == lib.product:
            return entry, True
    return None, False


def find_consumers(lib):
    """Every pin on this domain's family or npm package outside its own repo, under the workbench."""
    pins = []
    prop = re.compile(rf"<{re.escape(lib.pin_property)}>([^<]+)</{re.escape(lib.pin_property)}>")
    literal = re.compile(rf'<PackageVersion\s+Include="(WoW2\.Sdk\.Beta\.Be\.{re.escape(lib.brand)}\.[A-Za-z0-9.]+)"'
                         rf'\s+Version="([^"$]+)"')
    npm = re.compile(rf'"({re.escape(lib.fe_package)})"\s*:\s*"([^"]+)"')
    own = lib.path.resolve()
    for directory, dirs, files in os.walk(lib.root / "workbench"):
        here = Path(directory)
        if here.resolve() == own:
            dirs[:] = []
            continue
        dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS and not (here / d).is_symlink())
        for name in files:
            if name not in ("Directory.Packages.props", "package.json"):
                continue
            file = here / name
            try:
                text = file.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            repo = repo_root(file)
            if name == "package.json":
                pins += [Pin(file, repo, "npm", m.group(1), m.group(2)) for m in npm.finditer(text)
                         if not m.group(2).startswith(("workspace:", "file:", "link:"))]
                continue
            pins += [Pin(file, repo, "property", lib.pin_property, m.group(1)) for m in prop.finditer(text)]
            pins += [Pin(file, repo, "package", m.group(1), m.group(2)) for m in literal.finditer(text)]
    return pins


def repo_root(file):
    for parent in Path(file).parents:
        if (parent / ".git").exists():
            return parent
    return Path(file).parent


class Probe:
    """Collects a State. Reads only: local files, read-only git, `gh api` GETs, nuget.org and npm GETs."""

    def __init__(self, lib, offline=False):
        self.lib = lib
        self.offline = offline
        self.token = None

    # --- helpers

    def run(self, args, timeout=TIMEOUT, env=None, cwd=None):
        try:
            done = subprocess.run([str(a) for a in args], capture_output=True, text=True, timeout=timeout, env=env,
                                  cwd=cwd)
        except (OSError, subprocess.SubprocessError):
            return None
        return done

    def git(self, *args):
        done = self.run(["git", *args])
        return done.stdout.strip() if done is not None and done.returncode == 0 else None

    def gh_get(self, path):
        """(status, body): 200 with JSON, 404 / 409 with None, (None, None) when the probe cannot tell."""
        if self.offline or not self.token:
            return None, None
        env = {k: v for k, v in os.environ.items() if k not in ("GH_REPO", "GITHUB_TOKEN")}
        env["GH_TOKEN"] = self.token
        done = self.run(["gh", "api", path], env=env)
        if done is None:
            return None, None
        if done.returncode == 0:
            try:
                return 200, json.loads(done.stdout or "null")
            except ValueError:
                return None, None
        match = re.search(r"\(HTTP (\d{3})\)", done.stderr or "")
        code = int(match.group(1)) if match else None
        return (code, None) if code in (404, 409) else (None, None)

    def http_json(self, url, accept="application/json"):
        if self.offline:
            return None, None
        request = urllib.request.Request(url, headers={"Accept": accept, "User-Agent": "wow2-create-library"})
        try:
            with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
                return 200, json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as error:
            return (404, None) if error.code == 404 else (None, None)
        except (urllib.error.URLError, OSError, ValueError):
            return None, None

    def anonymous_pull(self, image):
        """True when ghcr.io answers an anonymous pull-token request 200, False on 401 / 403, else None. No credentials
        go out, and the token in a 200 body is never read."""
        if self.offline:
            return None
        request = urllib.request.Request(f"https://ghcr.io/token?scope=repository:{image}:pull",
                                         headers={"User-Agent": "wow2-create-library"})
        try:
            with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
                return True if response.status == 200 else None
        except urllib.error.HTTPError as error:
            return False if error.code in (401, 403) else None
        except (urllib.error.URLError, OSError):
            return None

    def flags_of(self, target):
        # the helper resolves paths against its working directory, so it runs from the workspace root
        done = self.run([sys.executable, "-B", self.lib.root / FLAGS_HELPER, "status", "--repo", target],
                        cwd=self.lib.root)
        return parse_flags(done.stdout) if done is not None and done.returncode == 0 else None

    def latest_run(self, workflow):
        code, body = self.gh_get(f"repos/{self.lib.full}/actions/workflows/{workflow}/runs?branch=main&per_page=1")
        if code != 200:
            return None if code is None else Run()
        runs = (body or {}).get("workflow_runs") or []
        if not runs:
            return Run()
        return Run(runs[0].get("status") or "", runs[0].get("conclusion") or "", runs[0].get("html_url") or "")

    def tag_versions(self, prefix):
        code, body = self.gh_get(f"repos/{self.lib.full}/git/matching-refs/tags/{prefix}")
        if code in (404, 409):
            return []
        if code != 200:
            return None
        return [ref["ref"].rsplit("/", 1)[-1][len(prefix):] for ref in body or [] if ref.get("ref")]

    # --- collect

    def collect(self):
        lib, st = self.lib, State()
        st.tools_missing = [tool for tool in TOOLS if shutil.which(tool) is None]
        template = lib.root / TEMPLATE
        scaffold = lib.root / SCAFFOLD
        st.template_ok = template.is_dir() and scaffold.is_file()
        try:
            st.scaffold_into = "INTO=clone" in scaffold.read_text(encoding="utf-8")
        except OSError:
            st.scaffold_into = False
        npm = self.run(["npm", "--version"]) if "npm" not in st.tools_missing else None
        if npm is not None and npm.returncode == 0:
            st.npm_version = tuple(int(n) for n in re.findall(r"\d+", npm.stdout.strip().splitlines()[-1])[:3])

        # the local folder
        st.folder, st.origin = folder_state(lib.path, lib.full)
        repo_here = st.folder in ("empty-clone", "clone")
        if repo_here:
            st.head = self.git("-C", lib.path, "rev-parse", "--verify", "-q", "HEAD^{commit}") or ""
        st.scaffolded = (lib.path / "product" / "product.json").is_file() and lib.slnx.is_file()
        if st.scaffolded:
            st.placeholders = placeholders_in(lib.path)
            st.sample_content = has_sample(lib)
            try:
                description = json.loads((lib.path / "product" / "product.json").read_text()).get("description", "")
                st.description = "" if "{{" in description else description
            except (OSError, ValueError):
                pass
        ident = self.git("-C", lib.path if repo_here else template, "var", "GIT_AUTHOR_IDENT")
        if ident:
            match = re.search(r"<([^>]*)>", ident)
            st.author = match.group(1) if match else ""

        # flags: the repo's own once it is checked out, else what a new repo under its folder gets
        st.flags = self.flags_of(lib.rel if repo_here else f"workbench/{lib.org}/*")
        st.hub_flags = self.flags_of(".")

        # GitHub, through the named account
        if not self.offline and "gh" not in st.tools_missing:
            token = self.run(["gh", "auth", "token", "-u", lib.account])
            st.account_ok = token is not None and token.returncode == 0 and bool(token.stdout.strip())
            self.token = token.stdout.strip() if st.account_ok else None
        if self.token:
            code, body = self.gh_get(f"repos/{lib.full}")
            st.repo_exists = None if code is None else code == 200
            if st.repo_exists:
                st.visibility = body.get("visibility") or ("private" if body.get("private") else "public")
                st.settings = {k: body.get(k) for k in ("has_issues", "has_wiki", "has_projects", "has_discussions")}
                code, body = self.gh_get(f"repos/{lib.full}/actions/permissions/workflow")
                st.workflow = body if code == 200 else None
                code, body = self.gh_get(f"repos/{lib.full}/actions/permissions")
                st.actions_enabled = body.get("enabled") if code == 200 else None
                code, body = self.gh_get(f"repos/{lib.full}/rulesets")
                st.rulesets = [r.get("name") for r in body or []] if code == 200 else None
                code, body = self.gh_get(f"repos/{lib.full}/branches/main")
                st.remote_main = (body or {}).get("commit", {}).get("sha", "") if code == 200 else \
                    ("" if code in (404, 409) else None)
                code, body = self.gh_get(f"repos/{lib.full}/actions/variables/PUBLISH_PACKAGES")
                st.publish_var = (body or {}).get("value", "") if code == 200 else ("" if code == 404 else None)
                st.be_tags = self.tag_versions("be-v")
                st.fe_tags = self.tag_versions("fe-v")
                # the image's releases are v*; a be-v or fe-v tag never gets one, so skip any other release
                code, body = self.gh_get(f"repos/{lib.full}/releases?per_page=30")
                tags = [r.get("tag_name") or "" for r in body or []] if code == 200 else None
                st.release_tag = None if tags is None and code not in (404, 409) else \
                    next((t for t in tags or [] if re.fullmatch(r"v\d+\.\d+\.\d+", t)), "")
                st.packages_run = self.latest_run("publish-packages.yml")
                st.image_run = self.latest_run("publish-docker-image.yml")
                if st.release_tag:  # a package that does not exist yet answers 403 like a private one
                    st.image_public = self.anonymous_pull(lib.image_path)
            code, body = self.gh_get(f"orgs/{lib.owner}/installations")
            st.org_apps = [i.get("app_slug") for i in (body or {}).get("installations") or []] if code == 200 else None

        # registries
        code, body = self.http_json(f"https://api.nuget.org/v3-flatcontainer/{lib.nuget_ids[0].lower()}/index.json")
        st.nuget_versions = (body or {}).get("versions", []) if code == 200 else ([] if code == 404 else None)
        name = urllib.parse.quote(lib.fe_package, safe="@")
        code, body = self.http_json(f"https://registry.npmjs.org/{name}", "application/vnd.npm.install-v1+json")
        st.npm_versions = sorted((body or {}).get("versions", {}), key=vkey) if code == 200 else \
            ([] if code == 404 else None)

        # the hub
        try:
            registry = load_registry(lib.root)
            entries = registry.load(str(lib.root / "catalog.yml")).get("entries") or []
            st.catalog_entry, st.catalog_mismatch = catalog_lookup(entries, lib)
        except Exception:  # an unreadable catalog reads as no entry; the registry check below says why
            st.catalog_entry = None
        done = self.run([sys.executable, "-I", lib.root / REGISTRY_GEN, "--check"])
        st.registry_fresh = None if done is None else done.returncode == 0
        dirty = self.git("-C", lib.root, "status", "--porcelain", "--", *HUB_PATHS)
        # `git()` strips the output, so the first line may have lost its leading status space; cut the status field
        st.hub_dirty = [path for line in (dirty or "").splitlines() if (path := re.sub(r"^\s*\S{1,2}\s+", "", line))]
        worktree = (lib.root / "catalog.yml").read_text(encoding="utf-8") if (lib.root / "catalog.yml").is_file() else ""
        head = self.git("-C", lib.root, "show", "HEAD:catalog.yml") or ""
        origin = self.git("-C", lib.root, "show", "origin/main:catalog.yml") or ""
        st.hub_committed = lib.full in head
        st.hub_pushed = lib.full in origin
        st.deploy_worktree = block_field(entry_block(worktree, lib.product), "deploy")
        st.deploy_head = block_field(entry_block(head, lib.product), "deploy")
        st.deploy_origin = block_field(entry_block(origin, lib.product), "deploy")
        try:
            st.platform_row = platform_row((lib.root / "docs" / "platform-apps.md").read_text(encoding="utf-8"),
                                           lib.brand, lib.repo)
        except OSError:
            st.platform_row = "none"

        # consumers, once something is published to pin
        if st.nuget_versions or (st.fe_tags and st.npm_versions):
            st.consumers = find_consumers(lib)
            for repo in sorted({pin.repo for pin in st.consumers}):
                rel = os.path.relpath(repo, lib.root)
                st.consumer_flags[str(repo)] = self.flags_of(rel)
        return st


# -------------------------------------------------------------------------------------------------------- evaluation

@dataclass
class Step:
    id: str
    phase: int
    title: str
    owner: str                 # agent · developer · consent · ci · gate
    needs: tuple = ()
    # done · skip · blocked · unknown · waiting, or todo, which resolve() turns into next · pending · hand · consent
    status: str = "todo"
    note: str = ""
    commands: list = field(default_factory=list)   # the agent's commands, one Bash call each
    edits: list = field(default_factory=list)      # the agent's file edits, in prose
    hand: list = field(default_factory=list)       # the developer's commands or actions
    unblocks: str = ""
    once: bool = False


def tri(value, done):
    """done when `done` holds, unknown when the probe could not tell, else todo."""
    if value is None:
        return "unknown"
    return "done" if done else "todo"


def evaluate(lib, st, confirmed=(), publish=False):
    confirmed = set(confirmed)
    abs_path = lib.path
    hub = lib.root
    steps = []

    def add(step):
        steps.append(step)
        return step

    # 0 · Preflight
    tools = add(Step("tools", 0, "tools on PATH: " + " ".join(TOOLS), "agent"))
    tools.status = "blocked" if st.tools_missing else "done"
    if st.tools_missing:
        tools.note = "missing: " + ", ".join(st.tools_missing)

    account = add(Step("account", 0, f"gh account {lib.account} in the keyring", "developer", once=True,
                       unblocks="every GitHub probe and write"))
    account.status = "done" if st.account_ok else ("unknown" if st.account_ok is None else "todo")
    account.hand = [f"sign {lib.account} into gh's keyring (`gh auth login`); agents never run gh auth login or switch"]

    template = add(Step("template", 0, "domain template and scaffold.sh INTO=clone", "agent"))
    template.status = "done" if st.template_ok and st.scaffold_into else "blocked"
    if template.status == "blocked":
        template.note = f"needs {TEMPLATE} and {SCAFFOLD} with INTO=clone"

    flags = add(Step("flags", 0, f"commit and push flags for {lib.rel}", "developer", once=True,
                     unblocks="repo creation and settings, the scaffold commit and push"))
    if st.flags is None:
        flags.status = "unknown"
        flags.note = "commit_permission.py status could not read them"
    else:
        missing = [kind for kind in ("commit", "push") if not st.flags.get(kind)]
        flags.status = "todo" if missing else "done"
        flags.note = st.flags.get("source", "") if not missing else "OFF: " + ", ".join(missing)
        flags.hand = [f"send as one whole message: ~git_on {','.join(missing or ['commit', 'push'])} "
                      f"workbench/{lib.org}/*   (every repo under the folder, present and future)"]

    author = add(Step("author", 0, "commit identity for the folder", "agent"))
    if st.author is None:
        author.status = "unknown"
    elif st.author.lower() == EXPECTED_EMAIL:
        author.status = "done"
        author.note = st.author
    else:
        author.status = "blocked"
        author.note = (f"git var GIT_AUTHOR_IDENT shows {st.author or 'nothing'}, expected {EXPECTED_EMAIL}: stop, "
                       "the developer owns ~/.gitconfig*")

    codex = add(Step("codex-app", 0, f"dropped Codex app off {lib.owner}", "developer", once=True,
                     unblocks="nothing; it closes the write access a dropped app holds on every new repo (T9 § 2)"))
    codex.status = tri(st.org_apps, st.org_apps is not None and CODEX_APP not in st.org_apps)
    codex.hand = [f"uninstall {CODEX_APP} at github.com/organizations/{lib.owner}/settings/installations"]

    # 1 · GitHub — create private, then clone: the guard matches a gh write to a checkout's origin, so settings follow
    # it; the developer makes the repo public once it holds the scaffold (phase 2), and the ruleset follows that
    create = add(Step("create", 1, f"create {lib.full}, private and empty", "agent",
                      needs=("tools", "account", "template", "flags")))
    occupied = st.folder in ("foreign", "clone", "empty-clone")
    if st.repo_exists:
        create.status = "done"
    elif st.repo_exists is None:
        create.status = "unknown"
    elif occupied:
        create.status = "blocked"
        create.note = (f"{lib.rel} is occupied, so the guard reads creation as OFF: the developer moves it aside")
    description = lib.description or (f"{lib.brand} domain: {lib.nuget_glob} packages, {lib.fe_package} and the "
                                      f"{lib.product} service")
    create.commands = [gh(lib, f"repo create {lib.full} --private --disable-wiki --disable-issues -d {q(description)}")]

    clone = add(Step("clone", 1, f"clone into {lib.rel}", "agent", needs=("create",)))
    if st.folder in ("clone", "empty-clone"):
        clone.status = "done"
    elif st.folder == "foreign":
        clone.status = "blocked"
        clone.note = f"{lib.rel} holds something else (origin {st.origin or 'none'}): the developer moves it aside"
    clone.commands = [gh(lib, f"repo clone {lib.full} {q(abs_path)}")]

    settings = add(Step("settings", 1, "issues, wiki, projects, discussions off; workflow token read-only", "agent",
                        needs=("clone",)))
    wanted = {"has_issues": "--enable-issues=false", "has_wiki": "--enable-wiki=false",
              "has_projects": "--enable-projects=false", "has_discussions": "--enable-discussions=false"}
    edit_flags = [flag for key, flag in wanted.items() if st.settings is None or st.settings.get(key) is not False]
    workflow_ok = (st.workflow is not None and st.workflow.get("default_workflow_permissions") == "read"
                   and st.workflow.get("can_approve_pull_request_reviews") is False)
    if edit_flags:
        settings.commands.append(gh(lib, f"repo edit {lib.full} " + " ".join(edit_flags)))
    if not workflow_ok:
        settings.commands.append(gh(lib, f"api -X PUT repos/{lib.full}/actions/permissions/workflow -f "
                                         "default_workflow_permissions=read -F can_approve_pull_request_reviews=false"))
    if st.actions_enabled is False:
        settings.commands.append(gh(lib, f"api -X PUT repos/{lib.full}/actions/permissions -F enabled=true"))
    if st.repo_exists and st.settings is not None and st.workflow is not None and not settings.commands:
        settings.status = "done"
    elif st.repo_exists and (st.settings is None or st.workflow is None):
        settings.status = "unknown"

    # 2 · Scaffold
    scaffold = add(Step("scaffold", 2, "stamp the domain template into the empty clone", "agent",
                        needs=("clone", "template")))
    if st.scaffolded:
        scaffold.status = "done"
    elif st.folder == "clone":
        scaffold.status = "blocked"
        scaffold.note = "the clone holds files the template did not stamp; scaffold.sh fills an empty clone only"
    env = ["SHAPE=domain", "INTO=clone"]
    if lib.slug != re.sub(r"[ .]", "-", lib.repo.rsplit(".", 1)[-1].lower()):
        env.append(f"SLUG={q(lib.slug)}")
    if lib.product != lib.brand.lower():
        env.append(f"PRODUCT={q(lib.product)}")
    if lib.core_version:
        env.append(f"CORE_VERSION={q(lib.core_version)}")
    if lib.fe_version:
        env.append(f"FE_VERSION={q(lib.fe_version)}")
    scaffold.commands = [" ".join(env) + f" bash {q(lib.root / SCAFFOLD)} {q(lib.repo)} {q(lib.brand)} {q(lib.org)}"]

    fill = add(Step("placeholders", 2, "fill the one-line description placeholders", "agent", needs=("scaffold",)))
    if st.scaffolded and not st.placeholders:
        fill.status = "done"
    files = sorted({file for file, _ in st.placeholders}) or ["README.md", "CLAUDE.md", "product/product.json"]
    fill.edits = [f"replace {' and '.join(REQUIRED_PLACEHOLDERS)} with the domain's one-liner in "
                  + ", ".join(files) + "; product.json's description becomes the catalog purpose"]

    commit = add(Step("commit", 2, "verify the scaffold, then commit it", "agent", needs=("placeholders", "author")))
    if st.head:
        commit.status = "done"
    fe = q(lib.frontend)
    commit.commands = [
        f"dotnet test {q(lib.slnx)}",
        f"pnpm -C {fe} install --frozen-lockfile",
        f"pnpm -C {fe} lint",
        f"pnpm -C {fe} test",
        f"pnpm -C {fe} build",
        f"pnpm -C {fe} check:package",
        f"bash {q(abs_path / 'engineering' / 'scripts' / 'test-next-version.sh')}",
        f"git -C {q(abs_path)} var GIT_AUTHOR_IDENT",
        f"git -C {q(abs_path)} add -A",
        f"git -C {q(abs_path)} status --short",
        f"git -C {q(abs_path)} commit -m {q(f'feat: added the {lib.brand} domain from the domain template')}",
    ]

    push = add(Step("push", 2, "push main; the push starts the image build", "agent", needs=("commit",)))
    if st.remote_main:
        push.status = "done"
        if st.head and st.head != st.remote_main:
            push.note = "local main differs from origin/main"
    elif st.remote_main is None and st.repo_exists is not False and st.head:
        push.status = "unknown"
    push.commands = [f"git -C {q(abs_path)} push origin main"]

    # a public surface is the developer's call: one command, after the repo holds the scaffold
    public = add(Step("public", 2, f"make {lib.full} public", "developer", needs=("push",),
                      unblocks="the main ruleset; the registries (npm provenance needs a public source repo)"))
    if st.visibility == "public":
        public.status = "done"
    elif st.repo_exists and st.visibility is None:
        public.status = "unknown"
    public.hand = ["in Warp: " + gh(lib, f"repo edit {lib.full} --visibility public "
                                         "--accept-visibility-change-consequences")]

    # rulesets on private repos need a paid plan, so main-guard waits for the public flip
    ruleset = add(Step("ruleset", 2, "main ruleset main-guard: no force push, no deletion", "agent",
                       needs=("public",)))
    if st.repo_exists and st.rulesets is None:
        ruleset.status = "unknown"
    elif st.rulesets and "main-guard" in st.rulesets:
        ruleset.status = "done"
    ruleset.commands = [gh(lib, f"api -X POST repos/{lib.full}/rulesets --input {q(lib.root / RULESET)}")]

    # 3 · Hub
    hub_commit_on = bool(st.hub_flags and st.hub_flags.get("commit"))
    hub_push_on = bool(st.hub_flags and st.hub_flags.get("push"))
    catalog = add(Step("catalog", 3, f"catalog entry `{lib.product}`, deploy: none", "agent",
                       needs=("create", "placeholders")))
    if st.catalog_entry and not st.catalog_mismatch:
        catalog.status = "done"
    elif st.catalog_mismatch:
        catalog.edits = [f"add {lib.full} to the `repositories` of the existing `{lib.product}` entry in catalog.yml"]
    else:
        purpose = st.description or "<one line: what the domain does>"
        catalog.commands = [me(lib, "apply-local catalog") + f" --purpose {q(purpose)}"]

    row = add(Step("platform-row", 3, "docs/platform-apps.md row names the repo", "agent", needs=("create",)))
    row.status = {"none": "skip", "named": "done"}.get(st.platform_row, "todo")
    if st.platform_row == "none":
        row.note = f"no **{lib.brand}** row: not a platform app"
    row.edits = [f"set the repo cell of the **{lib.brand}** row in docs/platform-apps.md to `{lib.repo}`"]

    registry = add(Step("registry", 3, ".claude/repo-registry.md regenerated", "agent", needs=("catalog",)))
    if catalog.status == "done":
        registry.status = tri(st.registry_fresh, st.registry_fresh)
    registry.commands = [f"python3 -I {q(hub / REGISTRY_GEN)}"]

    hub_commit = add(Step("hub-commit", 3, "commit the hub registration", "agent" if hub_commit_on else "developer",
                          needs=("catalog", "registry", "platform-row"),
                          unblocks="the hub push and Wheelhouse's catalog import"))
    if st.hub_committed:
        hub_commit.status = "done"
    paths = list(dict.fromkeys(["catalog.yml", ".claude/repo-registry.md"] + list(st.hub_dirty)))
    subject = f"docs: registered the {lib.brand} domain repo in the catalog"
    hub_commit.commands = [f"git -C {q(hub)} add " + " ".join(q(p) for p in paths),
                           f"git -C {q(hub)} diff --cached --stat",
                           f"git -C {q(hub)} commit -m {q(subject)}"]
    hub_commit.edits = [HUB_INDEX_RULE]
    hub_commit.hand = [f"hub commit flag OFF: commit {', '.join(paths)} in GitKraken as `{subject}`"]

    hub_push = add(Step("hub-push", 3, "push the hub", "agent" if hub_push_on else "developer",
                        needs=("hub-commit",), unblocks="Wheelhouse reads the hub at main"))
    if st.hub_pushed:
        hub_push.status = "done"
    hub_push.commands = [f"git -C {q(hub)} push origin main"]
    hub_push.hand = ["hub push flag OFF: push wow-two-ws main in GitKraken"]

    # 4 · Registries — opens with the first real slice; nothing published carries the template's sample
    published = bool(st.nuget_versions) or bool(st.npm_versions)
    content = add(Step("content", 4, "packages hold the first real slice", "gate",
                       needs=("scaffold", "push", "public")))
    ready = publish or (st.scaffolded and st.sample_content is False)
    if published or (ready and st.visibility == "public"):
        content.status = "done"
        content.note = "--publish" if publish and st.sample_content else ""
    elif st.scaffolded and not ready:
        content.note = ("the packages still hold the template's Greetings sample and no placeholder ships (T9 § 4): "
                        "land the first real slice, or pass --publish")

    nuget = add(Step("nuget-policy", 4, "nuget.org trusted-publishing policy for publish-packages.yml", "consent",
                     needs=("content",), unblocks="arming PUBLISH_PACKAGES; the be job's first publish"))
    if "nuget-policy" in confirmed or st.nuget_versions:
        nuget.status = "done"
    nuget.hand = [
        "your chat yes, then the agent fills the form in the wow2 Chrome profile (or you, in a minute):",
        f"nuget.org as MaxDev → Trusted Publishing → add: owner {lib.owner}, repository {lib.repo}, "
        f"workflow publish-packages.yml, no environment; packages {lib.nuget_glob}",
        "then re-run plan with --confirmed nuget-policy",
    ]

    npm = add(Step("npm-first", 4, f"first {lib.fe_package} version by hand, then its trusted publisher",
                   "developer", needs=("content",),
                   unblocks="the fe job; npm drops a trusted publisher with no publish in 2 days, so dispatch next"))
    npm.status = tri(st.npm_versions, bool(st.npm_versions))
    if npm.status == "unknown" and not st.scaffolded:
        npm.status = "todo"
    pkg = q(lib.fe_dir)
    npm.commands = [
        f"pnpm -C {fe} install --frozen-lockfile",
        f"npm --prefix {pkg} version {FIRST_FE_VERSION} --no-git-tag-version",
        f"pnpm -C {fe} --filter {q(lib.fe_package)} build",
        f"node {q(lib.fe_dir / 'scripts' / 'check-package.mjs')} --output {q(lib.tarball)}",
        f"npm --prefix {pkg} version 0.0.0 --no-git-tag-version",
    ]
    old_npm = st.npm_version is not None and st.npm_version < NPM_TRUST_MIN
    npm.hand = ([f"npm install -g npm@^{'.'.join(map(str, NPM_TRUST_MIN))}   "
                 f"(npm {'.'.join(map(str, st.npm_version))} is older than npm trust needs)"] if old_npm else []) + [
        "npm whoami || npm login --auth-type=web",
        f"npm publish {q(lib.tarball)} --access public",
        f"npm trust github {lib.fe_package} --file publish-packages.yml --repo {lib.full} --allow-publish",
    ]

    arm = add(Step("arm", 4, "PUBLISH_PACKAGES=true", "agent", needs=("nuget-policy",)))
    if st.publish_var == "true":
        arm.status = "done"
    elif st.repo_exists and st.publish_var is None:
        arm.status = "unknown"
    arm.commands = [gh(lib, f"variable set PUBLISH_PACKAGES --body true -R {lib.full}")]

    dispatch = [gh(lib, f"workflow run publish-packages.yml -R {lib.full} --ref main"),
                gh(lib, f"run list -R {lib.full} -w publish-packages.yml -L 1"),
                gh(lib, f"run watch <run-id> -R {lib.full} --exit-status")]
    run = st.packages_run

    def publish_status(step, is_done):
        if is_done:
            step.status = "done"
        elif run is not None and run.status in ("queued", "in_progress", "waiting", "pending"):
            step.status = "waiting"
            step.note = f"publish-packages run {run.status}: {run.url}"
        elif run is not None and run.conclusion == "failure" and st.publish_var == "true":
            step.status = "blocked"
            step.note = f"the last publish-packages run failed (a tagged number stays burned): {run.url}"
        step.commands = list(dispatch)

    be_pub = add(Step("be-published", 4, f"{lib.nuget_glob} on nuget.org", "agent", needs=("arm",)))
    publish_status(be_pub, bool(st.nuget_versions))
    if st.nuget_versions:
        be_pub.note = "newest " + newest(st.nuget_versions)
    elif st.nuget_versions is None:
        be_pub.status = "unknown"

    fe_pub = add(Step("fe-published", 4, f"{lib.fe_package} from CI", "agent", needs=("arm", "npm-first")))
    ci_fe = [v for v in st.fe_tags or [] if v in (st.npm_versions or [])]
    publish_status(fe_pub, bool(ci_fe))
    if ci_fe:
        fe_pub.note = "newest " + newest(ci_fe)

    # 5 · Image — the scaffold push built it through the shared delivery workflow
    image = add(Step("image", 5, "first image release v*", "ci", needs=("push",)))
    image.commands = [gh(lib, f"run list -R {lib.full} -w publish-docker-image.yml -L 3")]
    if st.release_tag:
        image.status = "done"
        image.note = st.release_tag
    elif st.repo_exists and st.release_tag is None:
        image.status = "unknown"
    elif st.image_run is not None and st.image_run.conclusion == "failure":
        image.status = "blocked"
        image.note = f"the delivery run failed: {st.image_run.url}"
        image.commands.append(gh(lib, f"run view <run-id> -R {lib.full} --log-failed"))
    elif st.image_run is not None and st.image_run.status:
        image.note = f"delivery run {st.image_run.status}: {st.image_run.url}"

    ghcr = add(Step("ghcr-app", 5, f"{WHEELHOUSE_APP} App on {lib.owner}", "developer", once=True,
                    unblocks="Wheelhouse pulls the image (phase 6); T8 step 21 needs nothing per repo after it"))
    ghcr.status = tri(st.org_apps, st.org_apps is not None and WHEELHOUSE_APP in st.org_apps)
    ghcr.hand = [f"install the {WHEELHOUSE_APP} GitHub App on org {lib.owner}, all repositories"]

    # platform service images are public: any Wheelhouse pulls the pinned image without a registry login. GitHub has no
    # REST endpoint for package visibility, so this stays a UI step; the anonymous token probe reads the result back.
    # Not a `deploy` need: Wheelhouse pulls through its App (ghcr-app), public or not.
    visible = add(Step("image-public", 5, f"package ghcr.io/{lib.image_path} public", "developer", needs=("image",),
                       unblocks="other products pull the image as a pinned service without a registry login"))
    if st.image_public is True:
        visible.status = "done"
    elif st.image_public is None and st.release_tag:
        visible.status = "unknown"
    owner, _, package = lib.image_path.partition("/")
    visible.hand = [
        f"once per org: https://github.com/organizations/{owner}/settings/packages "
        "→ Package creation → tick Public → Save",
        f"per library: https://github.com/orgs/{owner}/packages/container/{package.replace('/', '%2F')}/settings "
        "→ Danger Zone → Change visibility → Public, typing the package name to confirm "
        "(GitHub has no REST endpoint for package visibility)",
    ]

    # 6 · Wheelhouse
    deploy = add(Step("deploy", 6, "catalog entry deploy: wheelhouse, pushed",
                      "agent" if hub_commit_on and hub_push_on else "developer",
                      needs=("image", "ghcr-app", "hub-push")))
    if st.deploy_origin == "wheelhouse":
        deploy.status = "done"
    if st.deploy_worktree != "wheelhouse":
        deploy.commands += [me(lib, "apply-local deploy"), f"python3 -I {q(hub / REGISTRY_GEN)}"]
    deploy_subject = f"docs: set the {lib.brand} catalog entry to deploy through wheelhouse"
    if st.deploy_head != "wheelhouse":
        deploy.commands += [f"git -C {q(hub)} add catalog.yml .claude/repo-registry.md",
                            f"git -C {q(hub)} diff --cached --stat",
                            f"git -C {q(hub)} commit -m {q(deploy_subject)}"]
        deploy.edits = [HUB_INDEX_RULE]
    deploy.commands.append(f"git -C {q(hub)} push origin main")
    deploy.hand = ["hub flags OFF: run the printed catalog edit, then commit and push wow-two-ws in GitKraken"]

    wheelhouse = add(Step("wheelhouse", 6, f"Wheelhouse product `{lib.product}`: import, server, sites", "developer",
                          needs=("deploy",), unblocks="dev rollouts of each image; the secrets step"))
    if "wheelhouse" in confirmed:
        wheelhouse.status = "done"
    wheelhouse.hand = [f"Wheelhouse console: import `{lib.product}` from the wow2 hub, pick its server, bind its sites "
                       "(the agent can drive the import in your console session on request)",
                       "then re-run plan with --confirmed wheelhouse"]

    secrets = add(Step("secrets", 6, "third-party secret values and public DNS", "developer", needs=("wheelhouse",),
                       unblocks="the dev verify check passes; prod promotion stays yours"))
    if "secrets" in confirmed:
        secrets.status = "done"
    secrets.hand = ["enter the product's third-party secret values in Wheelhouse (never through an agent)",
                    "point public DNS at the public site and bind the domain; then re-run plan with --confirmed secrets"]

    # 7 · Consumers
    consumers = add(Step("consumers", 7, "consumer pins follow the published versions", "agent",
                         needs=("be-published",)))
    be_latest = newest(st.nuget_versions or [])
    fe_latest = newest(st.npm_versions or [])
    if st.consumers is not None and be_pub.status == "done":
        stale = [pin for pin in st.consumers
                 if (pin.kind == "npm" and fe_latest and pin.current.lstrip("^~") != fe_latest)
                 or (pin.kind != "npm" and be_latest and pin.current != be_latest)]
        if not st.consumers:
            consumers.status = "skip"
            consumers.note = "no repo pins the family yet; adoption is product work (T8 step 25)"
        elif not stale:
            consumers.status = "done"
        else:
            consumers.note = f"{len({p.repo for p in stale})} repo(s) behind {be_latest or fe_latest}"
            for repo in sorted({str(p.repo) for p in stale}):
                rel = os.path.relpath(repo, lib.root)
                files = sorted({str(p.file.relative_to(repo)) for p in stale if str(p.repo) == repo})
                repin_subject = f"chore: updated the {lib.brand} packages to {be_latest or fe_latest}"
                versions = (f" --version {q(be_latest)}" if be_latest else "") + \
                           (f" --fe-version {q(fe_latest)}" if fe_latest else "")
                consumers.commands += [
                    me(lib, "repin") + versions + f" --only {q(rel)} --write",
                    f"git -C {q(repo)} add " + " ".join(q(f) for f in files),
                    f"git -C {q(repo)} commit -m {q(repin_subject)}",
                    f"git -C {q(repo)} push origin main",
                ]
                flags_here = st.consumer_flags.get(repo)
                off = "" if flags_here and flags_here.get("commit") and flags_here.get("push") else \
                    f" (flags OFF: the developer sends ~git_on commit,push {rel}, or commits it)"
                consumers.edits.append(f"{rel}: build and test per its CLAUDE.md after the repin, before the commit; "
                                       f"a package.json pin also needs `pnpm install` there{off}")

    resolve(steps)
    return steps


def resolve(steps):
    by_id = {step.id: step for step in steps}
    role = {"agent": "next", "developer": "hand", "consent": "consent", "ci": "waiting", "gate": "waiting"}
    for step in steps:
        if step.status != "todo":
            continue
        unmet = [need for need in step.needs if by_id[need].status not in DONE]
        if unmet:
            step.status = "pending"
            step.note = "after " + ", ".join(unmet)
        else:
            step.status = role[step.owner]


def next_phase(steps):
    """(phase, chain): the lowest phase with a runnable agent step, and its agent steps a run in order completes."""
    runnable = [step for step in steps if step.status == "next"]
    if not runnable:
        return None, []
    phase = min(step.phase for step in runnable)
    assumed = {step.id for step in steps if step.status in DONE}
    chain = []
    for step in steps:
        if step.phase != phase or step.owner != "agent" or step.status not in ("next", "pending"):
            continue
        if all(need in assumed for need in step.needs):
            chain.append(step)
            assumed.add(step.id)
    return phase, chain


# ----------------------------------------------------------------------------------------------------------- render

def header(lib):
    return (f"create-library · {lib.full} · brand {lib.brand} · slug {lib.slug} · product {lib.product}\n"
            "dry run: probes only, nothing written")


def render_status(lib, steps):
    out = [header(lib)]
    for phase, name in PHASES.items():
        out.append(f"\n{phase} {name}")
        for step in (s for s in steps if s.phase == phase):
            note = f" — {step.note}" if step.note else ""
            out.append(f"  {step.status:<8} {step.id:<13} {step.title}{note}")
    return "\n".join(out)


def render_next(lib, steps):
    out = []
    phase, chain = next_phase(steps)
    if chain:
        out.append(f"Next: phase {phase} {PHASES[phase]}. Run each command as its own Bash call, in order; stop at the "
                   "first failure; then re-run plan.")
        seen, n = set(), 0
        for step in chain:
            for command in step.commands:
                if command in seen:
                    continue
                seen.add(command)
                n += 1
                out.append(f"  {n}. {command}")
            for edit in step.edits:
                out.append(f"  edit ({step.id}): {edit}")
    else:
        out.append("Next: nothing the agent can run now.")
    waiting = [s for s in steps if s.status in ("waiting", "blocked", "unknown")]
    if waiting:
        out.append("\nWaiting or blocked:")
        for step in waiting:
            watch = f"  (check: {step.commands[0]})" if step.owner == "ci" and step.commands else ""
            out.append(f"  {step.status:<8} {step.id}: {step.note or step.title}{watch}")
    hands = [s for s in steps if s.owner in ("developer", "consent") and s.status not in DONE and s.hand]
    if hands:
        out.append("\nHand steps for the developer, ready first:")
        order = {"hand": 0, "consent": 0, "blocked": 0, "pending": 1, "unknown": 2}
        for step in sorted(hands, key=lambda s: (order.get(s.status, 3), s.phase)):
            when = "ready" if step.status in ("hand", "consent", "blocked") else \
                ("check" if step.status == "unknown" else step.note or "later")
            tag = "once" if step.once else "per library"
            out.append(f"  [{when}] {step.id} ({tag}): {step.title}")
            if when != "ready":  # a later step shows its full commands once it is ready
                if step.unblocks:
                    out.append(f"      unblocks: {step.unblocks}")
                continue
            if step.owner == "developer" and step.commands:
                out.append("      agent first, one Bash call each:")
                out += [f"        {command}" for command in step.commands]
                out.append("      then you, in Warp:")
                out += [f"        {line}" for line in step.hand]
            else:
                out += [f"      {line}" for line in step.hand]
            if step.unblocks:
                out.append(f"      unblocks: {step.unblocks}")
    return "\n".join(out)


# ------------------------------------------------------------------------------------------------------- apply-local

def entry_text(lib, purpose, status="Planned", workspace="wow2-platform", kind="platform", name=""):
    if not purpose or "\n" in purpose or purpose.startswith("<"):
        raise ValueError("--purpose must be one line saying what the domain does")
    quoted = purpose.replace("\\", "\\\\").replace('"', '\\"')
    lines = [f"  - slug: {lib.product}",
             f"    name: {name or lib.brand}",
             f"    workspace: {workspace}",
             f"    kind: {kind}",
             "    deploy: none",
             f'    status: "{status}"',
             f'    purpose: "{quoted}"',
             f"    repositories: [{lib.full}]"]
    if lib.org != lib.owner:
        lines.append(f"    local: {lib.rel}")
    return "\n".join(lines)


def insert_entry(text, lib, block):
    """The catalog text with `block` appended to its org's group (`  # {owner} (…)`), else to the end."""
    if lib.full in text:
        raise ValueError(f"catalog.yml already names {lib.full}")
    if re.search(rf"^  - slug: {re.escape(lib.product)}\s*$", text, re.M):
        raise ValueError(f"catalog.yml already has the slug `{lib.product}`")
    lines = text.split("\n")
    start = next((i for i, line in enumerate(lines) if re.match(rf"  # {re.escape(lib.owner)}( |$)", line)), None)
    if start is None:
        body = text.rstrip("\n")
        return f"{body}\n\n  # {lib.owner}\n{block}\n"
    end = start + 1
    while end < len(lines) and lines[end].strip() != "" and not lines[end].startswith("  # "):
        end += 1
    return "\n".join(lines[:end] + block.split("\n") + lines[end:])


def set_deploy(text, lib, value="wheelhouse"):
    block = entry_block(text, lib.product)
    if not block:
        raise ValueError(f"catalog.yml has no `{lib.product}` entry")
    if not re.search(r"^    deploy: ", block, re.M):
        raise ValueError(f"the `{lib.product}` entry has no deploy field")
    changed = re.sub(r"^    deploy: .*$", f"    deploy: {value}", block, count=1, flags=re.M)
    return text.replace(block, changed, 1)


def check_catalog(lib, text):
    """Parse the new catalog with the registry generator's reader, so a broken edit never lands."""
    registry = load_registry(lib.root)
    with tempfile.NamedTemporaryFile("w", suffix=".yml", delete=False, encoding="utf-8") as handle:
        handle.write(text)
    try:
        entries = registry.load(handle.name).get("entries") or []
    finally:
        os.unlink(handle.name)
    entry, mismatch = catalog_lookup(entries, lib)
    if not entry or mismatch:
        raise ValueError("the edited catalog does not parse back to the new entry")
    return entry


def apply_local(lib, what, args):
    path = lib.root / "catalog.yml"
    text = path.read_text(encoding="utf-8")
    if what == "catalog":
        if lib.full in text:
            print(f"catalog.yml already names {lib.full}; nothing written")
            return 0
        new = insert_entry(text, lib, entry_text(lib, args.purpose, args.status, args.workspace, args.kind, args.name))
    else:
        if block_field(entry_block(text, lib.product), "deploy") == "wheelhouse":
            print(f"the `{lib.product}` entry already deploys through wheelhouse; nothing written")
            return 0
        new = set_deploy(text, lib)
    check_catalog(lib, new)
    path.write_text(new, encoding="utf-8")
    print(f"catalog.yml: {'added the' if what == 'catalog' else 'set deploy: wheelhouse on the'} `{lib.product}` "
          f"entry; next: python3 -I {lib.root / REGISTRY_GEN}")
    return 0


def repin(lib, version, fe_version, only, write, pins=None):
    """Rewrite consumer pins to the given versions; prints each change. Returns the changed files."""
    pins = find_consumers(lib) if pins is None else pins
    if only:
        target = (lib.root / only).resolve()
        pins = [p for p in pins if Path(p.repo).resolve() == target]
    changed = {}
    for pin in pins:
        new = fe_version if pin.kind == "npm" else version
        if not new:
            continue
        text = changed.get(pin.file) or pin.file.read_text(encoding="utf-8")
        if pin.kind == "property":
            updated = text.replace(f"<{pin.name}>{pin.current}</{pin.name}>", f"<{pin.name}>{new}</{pin.name}>")
        elif pin.kind == "package":
            updated = re.sub(rf'(<PackageVersion\s+Include="{re.escape(pin.name)}"\s+Version=")[^"]+(")',
                             rf"\g<1>{new}\g<2>", text)
        else:
            prefix = re.match(r"^[~^]?", pin.current).group(0)
            updated = text.replace(f'"{pin.name}": "{pin.current}"', f'"{pin.name}": "{prefix}{new}"')
        if updated != text:
            changed[pin.file] = updated
            print(f"{'repin' if write else 'would repin'} {os.path.relpath(pin.file, lib.root)}: "
                  f"{pin.name} {pin.current} → {new}")
    if write:
        for file, text in changed.items():
            file.write_text(text, encoding="utf-8")
    if not changed:
        print("no pin to change")
    return sorted(changed)


# -------------------------------------------------------------------------------------------------------------- cli

def parser():
    p = argparse.ArgumentParser(prog="library.py", description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="command")

    def common(sp):
        sp.add_argument("repo", help="e.g. wow-two-sdk-beta.identity")
        sp.add_argument("--brand", default="", help="PascalCase domain; default from the repo's last segment")
        sp.add_argument("--org", default=DEFAULT_ORG, help="workbench folder and GitHub owner")
        sp.add_argument("--slug", default="", help="code-dir prefix and fe-{slug}; default the last dot-segment")
        sp.add_argument("--product", default="", help="catalog, deploy and Wheelhouse slug; default: lowercased brand")
        sp.add_argument("--account", default=ACCOUNT, help="the gh account the folder uses")
        sp.add_argument("--root", default=str(ROOT), help=argparse.SUPPRESS)

    for name in ("plan", "status", "next"):
        sp = sub.add_parser(name)
        common(sp)
        sp.add_argument("--core-version", default="")
        sp.add_argument("--fe-version", default="")
        sp.add_argument("--description", default="", help="the GitHub repo description")
        sp.add_argument("--confirmed", default="", help="comma list: " + ",".join(CONFIRMABLE))
        sp.add_argument("--publish", action="store_true", help="open phase 4 while the Greetings sample remains")
        sp.add_argument("--offline", action="store_true", help="skip GitHub, nuget.org and npm probes")

    sp = sub.add_parser("apply-local")
    sp.add_argument("what", choices=("catalog", "deploy"))
    common(sp)
    sp.add_argument("--purpose", default="")
    sp.add_argument("--status", default="Planned")
    sp.add_argument("--workspace", default="wow2-platform")
    sp.add_argument("--kind", default="platform")
    sp.add_argument("--name", default="")

    sp = sub.add_parser("repin")
    common(sp)
    sp.add_argument("--version", default="", help="the NuGet family version")
    sp.add_argument("--fe-version", dest="fe_pin", default="", help="the npm package version")
    sp.add_argument("--only", default="", help="one consumer repo, relative to the workspace root")
    sp.add_argument("--write", action="store_true")
    return p


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    if argv and argv[0] not in ("plan", "status", "next", "apply-local", "repin", "-h", "--help"):
        argv.insert(0, "plan")
    args = parser().parse_args(argv)
    if not args.command:
        parser().print_help()
        return 2
    lib = Library(args.repo, args.brand, args.org, args.slug, args.product, args.account, Path(args.root),
                  getattr(args, "core_version", ""), getattr(args, "fe_version", ""), getattr(args, "description", ""))
    problems = lib.problems()
    if problems:
        print("library.py: " + "; ".join(problems), file=sys.stderr)
        return 2
    try:
        if args.command == "apply-local":
            return apply_local(lib, args.what, args)
        if args.command == "repin":
            if not args.version and not args.fe_pin:
                print("library.py repin: give --version and/or --fe-version", file=sys.stderr)
                return 2
            repin(lib, args.version, args.fe_pin, args.only, args.write)
            return 0
    except ValueError as error:
        print(f"library.py: {error}", file=sys.stderr)
        return 1
    confirmed = [c.strip() for c in args.confirmed.split(",") if c.strip()]
    unknown = [c for c in confirmed if c not in CONFIRMABLE]
    if unknown:
        print(f"library.py: --confirmed takes {', '.join(CONFIRMABLE)}, not {', '.join(unknown)}", file=sys.stderr)
        return 2
    state = Probe(lib, offline=args.offline).collect()
    steps = evaluate(lib, state, confirmed, args.publish)
    if args.command in ("plan", "status"):
        print(render_status(lib, steps))
    if args.command in ("plan", "next"):
        print(("\n" if args.command == "plan" else "") + render_next(lib, steps))
    return 0


if __name__ == "__main__":
    sys.exit(main())

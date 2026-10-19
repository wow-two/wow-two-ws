#!/usr/bin/env python3
"""Regenerate .claude/repo-registry.md from every hub's catalog.yml.

Reads wow2's catalog.yml, then each hub its `hubs` lists from that hub's local checkout (no network).

Usage:
  python3 scripts/gen-repo-registry.py           rewrite the registry
  python3 scripts/gen-repo-registry.py --check   exit 1 when the registry is stale

Format and rules: conventions/development/repo/catalog/catalog.md.
Uses PyYAML when installed; otherwise a built-in reader for the YAML subset the catalog keeps to.
"""
import datetime
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CATALOG = os.path.join(ROOT, "catalog.yml")
REGISTRY = os.path.join(ROOT, ".claude", "repo-registry.md")
DATE_LINE = re.compile(r"^\*Last updated: (.+)\*$", re.M)

HEADER = """\
> **Generated** from the hubs' `catalog.yml` files (wow2's, then each hub its `hubs` lists) by \
`scripts/gen-repo-registry.py` — edit the owning hub's catalog, then regenerate.
>
> **Usage:** This is a lookup table. Do NOT read these files or repos proactively.
> Only access a repo when the current task specifically requires it.
>
> **Path:** All repos live under `workbench/{org}/` — e.g. `workbench/wow-two-sdk/wow-two-sdk.language.core/`, \
`workbench/wow-two/wow-two.refinement/`. Folder name = org name (1:1).

# Repo Registry

*Last updated: %s*

All repos use the naming convention: `{org}.{domain}[.{subdomain}]`, lowercase, dot-separated. \
Repo prefix matches org name exactly."""


# --- YAML subset reader (fallback when PyYAML is missing) -----------------------------------------
# Block mappings and sequences, `- key: value` items, flow sequences of scalars, quoted and plain
# scalars, `|` / `|-` literals and comments. No flow mappings, anchors, tags or multi-documents.

def _strip_comment(line):
    quote, escaped = None, False
    for i, ch in enumerate(line):
        if quote:
            if escaped:
                escaped = False
            elif ch == "\\" and quote == '"':
                escaped = True
            elif ch == quote:
                quote = None
        elif ch in "\"'" and (i == 0 or line[i - 1] in " [,:"):
            quote = ch
        elif ch == "#" and (i == 0 or line[i - 1] in " \t"):
            return line[:i]
    return line


def _scalar(text):
    if text.startswith('"'):
        return json.loads(text)
    if text.startswith("'"):
        return text[1:-1].replace("''", "'")
    if text.startswith("["):
        inner = text[1:-1].strip()
        return [_scalar(part.strip()) for part in _split_flow(inner)] if inner else []
    if text.startswith("{"):
        raise ValueError("flow mappings are outside the catalog's YAML subset: " + text)
    if re.fullmatch(r"-?\d+", text):
        return int(text)
    return {"true": True, "false": False, "null": None, "~": None}.get(text, text)


def _split_flow(text):
    parts, current, quote = [], "", None
    for ch in text:
        if quote:
            quote = None if ch == quote else quote
        elif ch in "\"'":
            quote = ch
        elif ch == ",":
            parts.append(current)
            current = ""
            continue
        current += ch
    return parts + [current]


class _SubsetReader:
    KEY = re.compile(r"^([A-Za-z_][\w-]*):(?: (.*))?$")

    def __init__(self, text):
        self.lines = text.splitlines()
        self.i = 0

    def peek(self):
        while self.i < len(self.lines):
            body = _strip_comment(self.lines[self.i]).rstrip()
            if body.strip():
                return len(body) - len(body.lstrip(" ")), body.strip()
            self.i += 1
        return None

    def read(self):
        head = self.peek()
        return None if head is None else self.node(head[0])

    def node(self, indent):
        head = self.peek()
        if head[1] == "-" or head[1].startswith("- "):
            return self.sequence(indent)
        return self.mapping(indent)

    def mapping(self, indent):
        result = {}
        while True:
            head = self.peek()
            if head is None or head[0] < indent or head[1].startswith("- "):
                return result
            if head[0] > indent:
                raise ValueError("unexpected indent at line %d" % (self.i + 1))
            match = self.KEY.match(head[1])
            if not match:
                raise ValueError("expected `key: value` at line %d" % (self.i + 1))
            self.i += 1
            result[match.group(1)] = self.value((match.group(2) or "").strip(), indent)

    def value(self, text, indent):
        if text in ("|", "|-"):
            return self.literal(indent, text)
        if text:
            return _scalar(text)
        head = self.peek()
        if head is None:
            return None
        if head[0] > indent:
            return self.node(head[0])
        if head[0] == indent and (head[1] == "-" or head[1].startswith("- ")):
            return self.sequence(indent)
        return None

    def sequence(self, indent):
        result = []
        while True:
            head = self.peek()
            if head is None or head[0] != indent or not (head[1] == "-" or head[1].startswith("- ")):
                return result
            item = head[1][1:].lstrip(" ")
            if self.KEY.match(item):
                inner = indent + len(head[1]) - len(item)
                self.lines[self.i] = " " * inner + item
                result.append(self.mapping(inner))
            else:
                self.i += 1
                result.append(self.value(item, indent))

    def literal(self, indent, style):
        lines, block = [], None
        while self.i < len(self.lines):
            raw = self.lines[self.i].rstrip()
            if raw.strip():
                depth = len(raw) - len(raw.lstrip(" "))
                if depth <= indent or (block is not None and depth < block):
                    break
                block = depth if block is None else block
                lines.append(raw[block:])
            else:
                lines.append("")
            self.i += 1
        while lines and not lines[-1]:
            lines.pop()
        return "\n".join(lines) + ("" if style == "|-" else "\n")


def load(path):
    with open(path, encoding="utf-8") as handle:
        text = handle.read()
    try:
        import yaml
    except ImportError:
        return _SubsetReader(text).read()
    return yaml.safe_load(text)


# --- Registry --------------------------------------------------------------------------------------

def check(catalog, where):
    if not isinstance(catalog.get("hub"), dict):
        sys.exit("%s: `hub` is required" % where)
    workspaces = {w["slug"] for w in catalog["workspaces"]}
    slugs, repositories = set(), set()
    for entry in catalog["entries"]:
        if entry["slug"] in slugs:
            sys.exit("%s: duplicate entry slug: %s" % (where, entry["slug"]))
        if entry["workspace"] not in workspaces:
            sys.exit("%s: %s: unknown workspace %s" % (where, entry["slug"], entry["workspace"]))
        if not entry["repositories"] and not entry.get("local"):
            sys.exit("%s: %s: an entry without a repository needs `local`" % (where, entry["slug"]))
        for repository in entry["repositories"]:
            if repository in repositories:
                sys.exit("%s: repository listed twice: %s" % (where, repository))
            repositories.add(repository)
        slugs.add(entry["slug"])


def check_across(hubs):
    """Every entry slug, workspace slug, repository and org belongs to one hub."""
    owners = {}
    for where, catalog in hubs:
        keys = [("entry", e["slug"]) for e in catalog["entries"]]
        keys += [("workspace", w["slug"]) for w in catalog["workspaces"]]
        keys += [("repository", r) for e in catalog["entries"] for r in e["repositories"]]
        keys += [("org", o["slug"]) for o in catalog.get("orgs") or []]
        for key in keys:
            if key in owners:
                sys.exit("%s %s is in both %s and %s" % (key[0], key[1], owners[key], where))
            owners[key] = where


def load_hubs():
    """wow2's catalog, then each hub its `hubs` lists, read from the hub's local checkout."""
    root = load(CATALOG)
    check(root, "catalog.yml")
    hubs = [("catalog.yml", root)]
    for ref in root.get("hubs") or []:
        where = "%s/catalog.yml" % ref["local"]
        path = os.path.join(ROOT, ref["local"], "catalog.yml")
        if not os.path.exists(path):
            sys.exit("%s is missing: check out %s at %s, then regenerate" % (where, ref["repository"], ref["local"]))
        catalog = load(path)
        check(catalog, where)
        if catalog["hub"]["repository"] != ref["repository"]:
            sys.exit("%s names hub %s, not %s" % (where, catalog["hub"]["repository"], ref["repository"]))
        hubs.append((where, catalog))
    check_across(hubs)
    return [catalog for _, catalog in hubs]


def section_of(entry, orgs):
    """The org whose section lists the entry, or None for the hub's own section."""
    if entry["repositories"]:
        owner = entry["repositories"][0].split("/")[0]
        if owner in orgs:
            return owner
    parts = entry.get("local", "").split("/")
    if len(parts) > 1 and parts[1] in orgs:
        return parts[1]
    return None


def repo_name(entry):
    if entry["repositories"]:
        return entry["repositories"][0].split("/")[1]
    return entry["local"].rstrip("/").split("/")[-1]


def table(rows, wide):
    if wide:
        lines = ["| Repo / local folder | Purpose | Status |", "|---|---|---|"]
    else:
        lines = ["| Repo | Purpose | Status |", "|------|---------|--------|"]
    return "\n".join(lines + ["| %s | %s | %s |" % row for row in rows])


def org_section(org, entries):
    rows, wide = [], False
    for entry in entries:
        name = repo_name(entry)
        cell = "`%s`" % name
        local = entry.get("local")
        if local and local != "workbench/%s/%s" % (org["slug"], name):
            cell += " · `%s`" % local
            wide = True
        rows.append((cell, entry["purpose"], entry["status"]))
    host = org["url"].split("://", 1)[1]
    heading = org["slug"] + (" (%s)" % org["label"] if org.get("label") else "")
    blocks = ["## " + heading, "Org: [%s](%s) — %s." % (host, org["url"], org["description"])]
    blocks += [block.rstrip("\n") for block in org.get("intro", [])]
    blocks.append(table(rows, wide))
    blocks += [block.rstrip("\n") for block in org.get("notes", [])]
    return "\n\n".join(blocks)


def hub_section(hub, entries):
    rows = []
    for entry in entries:
        repository = entry["repositories"][0] if entry["repositories"] else repo_name(entry)
        cell = "`%s`" % repository + (" · `%s`" % entry["local"] if entry.get("local") else "")
        rows.append((cell, entry["purpose"], entry["status"]))
    url = "https://github.com/" + hub["repository"]
    line = "Hub: [%s](%s) — %s." % (hub["repository"], url, hub["description"])
    return "\n\n".join(["## " + hub["name"], line, table(rows, True)])


def render(hubs, date):
    sections = []
    for catalog in hubs:
        orgs = {org["slug"]: org for org in catalog.get("orgs") or []}
        grouped, loose = {slug: [] for slug in orgs}, []
        for entry in catalog["entries"]:
            org = section_of(entry, orgs)
            (grouped[org] if org else loose).append(entry)
        sections += [org_section(org, grouped[org["slug"]]) for org in catalog.get("orgs") or []]
        if loose:
            sections.append(hub_section(catalog["hub"], loose))
    return "\n\n".join([HEADER % date] + sections) + "\n"


def main():
    hubs = load_hubs()
    current = open(REGISTRY, encoding="utf-8").read() if os.path.exists(REGISTRY) else ""
    stamped = DATE_LINE.search(current)
    if stamped and render(hubs, stamped.group(1)) == current:
        print("repo-registry.md is up to date")
        return
    if "--check" in sys.argv[1:]:
        sys.exit("repo-registry.md is stale: run python3 scripts/gen-repo-registry.py")
    with open(REGISTRY, "w", encoding="utf-8") as handle:
        handle.write(render(hubs, datetime.date.today().isoformat()))
    print("wrote .claude/repo-registry.md")


if __name__ == "__main__":
    main()

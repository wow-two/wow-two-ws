#!/usr/bin/env python3
"""Print catalogued checkouts as `owner/name<TAB>path`, the path relative to the wow-two-ws root.

Usage:
  python3 scripts/catalog-checkouts.py hubs      each hub wow2's `hubs` lists, at its `local`
  python3 scripts/catalog-checkouts.py entries   every repository of every other hub's entries

An entry's primary repository checks out at `local`, else `workbench/{owner}/{name}`; its other
repositories check out beside the primary under their own name. wow2's own repositories come from
`gh repo list` per org in scripts/clone-all.sh. A hub not checked out yet is skipped with a warning.
Layout: conventions/development/repo/layout/workbench-layout.md.
"""
import importlib.util
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SPEC = importlib.util.spec_from_file_location("registry", os.path.join(HERE, "gen-repo-registry.py"))
registry = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(registry)


def checkouts(entry):
    repositories = entry["repositories"]
    if not repositories:
        return []
    primary = entry.get("local") or "workbench/" + repositories[0]
    beside = os.path.dirname(primary)
    return [(repositories[0], primary)] + [(r, beside + "/" + r.split("/")[1]) for r in repositories[1:]]


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else ""
    if mode not in ("hubs", "entries"):
        sys.exit(__doc__)
    hubs = registry.load(registry.CATALOG).get("hubs") or []
    if mode == "hubs":
        for hub in hubs:
            print("%s\t%s" % (hub["repository"], hub["local"]))
        return
    local_only = 0
    for hub in hubs:
        path = os.path.join(registry.ROOT, hub["local"], "catalog.yml")
        if not os.path.exists(path):
            print("skipped %s: not checked out at %s" % (hub["repository"], hub["local"]), file=sys.stderr)
            continue
        for entry in registry.load(path)["entries"]:
            local_only += not entry["repositories"]
            for repository, checkout in checkouts(entry):
                print("%s\t%s" % (repository, checkout))
    if local_only:
        print("%d local-only entries have no repository to clone" % local_only, file=sys.stderr)


if __name__ == "__main__":
    main()

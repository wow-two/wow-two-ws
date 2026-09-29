#!/usr/bin/env python3
"""Workspace git guard — PreToolUse hook (Bash + file edits), one engine for every workspace.

Only the CONFIG block differs between workspaces; DOC names the prose policy it enforces.

  allowed    index-only staging/unstaging (`add`, `restore --staged`, path `reset`,
             `rm --cached`) · `mv` and `rm` without force · `apply` unless reversed ·
             `submodule init|update|sync` · `notes` writes · read-only git
             (status log diff show blame describe rev-parse ls-files shortlog
             reflog, `branch --list`, `remote -v`, `stash list|show`) ·
             `git fetch` · read-only gh (`pr view|list|diff|checks|status`,
             `run view|list|watch`, `issue view|list`, `api` GET, `repo view`,
             `auth status`)
  commits    COMMITS decides. "switch": a Claude chat runs exactly
             `git -C <repo> commit -m "subject"` while that repository's commit flag is ON, and
             `git -C <repo> push [-u] [<remote> [<ref>]]` while its push flag is ON. The developer
             flips each with a whole-message `~commit_on <repo>` / `~push_on <repo>`, or sets the
             workspace default with `*`; each flag holds for every chat. `.codex/hooks/commit_permission.py`
             owns the workspace store `.codex/git-flags.json` and the ordinary forms, and `commit-switch.py`
             feeds it Claude prompts. "open": a plain commit runs after the lane check. "never": no commit.
             A Codex chat meets the switch in its adapter, where installed, before this hook.
  flags      two kinds, for commands that are risky AND used often. Where `.codex/hooks/commit_permission.py`
             is installed, each runs while the target repository's flag of its kind is ON
             (`~git_on <kind> <repo>`); otherwise it blocks:
               commit   local history rewrites: `commit --amend` · `rebase` · `cherry-pick` · `revert` ·
                        `merge` · `am` · `subtree` · soft / mixed `reset` to a commit. A rewrite that would
                        replace a commit already on a remote-tracking branch never runs.
               push     every gh write (`pr create|comment|merge|...`, `issue ...`, `release ...`,
                        `workflow run`, `secret set`, `repo create|edit|rename`, `api` writes)
             A gated git command acts on `git -C <repo>`, else the working directory; a `cd`, `pushd`,
             `--git-dir` or `--work-tree` in the same command blocks it, since the target is unknown.
             A gh write acts on `-R owner/name`, a `repos/owner/name` API path, `repo ... owner/name` or
             `--source <path>`, matched to the workspace repository with that origin; an unmatched one
             reads the workspace repository's flag. Without the module each category stays forbidden.
  store      the flag store and its change log (`.codex/git-flags.json|log|lock`) are never edited by a
             tool: a Write / Edit / MultiEdit / NotebookEdit on them, or a shell command naming them, blocks.
  forbidden  risky commands that are rarely needed, whatever the flags: `git push` outside the ordinary
             form (forcing, deleting, mirror, pruning, hook-skipping) · worktree discards (`restore` to
             the worktree, path / `.` / forced `checkout`, forced `switch`, `reset --hard|--merge|--keep`,
             `clean`, forced `rm` / `mv`, reversed `apply`, `checkout-index`) · every `config` write ·
             `remote` and `worktree` writes · `submodule add|deinit|set-url|set-branch|absorbgitdirs` · ref and object
             surgery (`filter-branch`, `filter-repo`, `fast-import`, `update-ref`, `update-index`,
             `replace`, `gc`, `prune`, `reflog` and `symbolic-ref` writes) · `send-email` · `gh repo delete`
  STRICT     also forbids `pull`, branch create / switch, `stash` writes, tag writes and every
             gated category; otherwise they are allowed (a stash is a real ref and shows in GitKraken).
  lane check `pull`, `stash push`, open commits and flagged history rewrites stop
             once, by name, when the tree holds modified / staged files this session never
             wrote — probably a parallel chat's in-flight work on the shared branch. The developer answers in chat and the retry
             goes through (it asks once per file set). "This session wrote it" comes from the
             ledger that the PostToolUse hook `track-touch.py` appends to on every Write /
             Edit; without that hook installed, nothing counts as this session's.

Mechanism: exit 2 with the reason on stderr — the PreToolUse contract for a block;
the reason is fed back to the agent. An internal error exits 0 for a command with no git
or gh call, because a guard that crashes must never block unrelated commands — and 2 for
every git or gh call, so a crash never lets a write through.

Parsing: every git/gh invocation in the shell string is scanned (splits on
&& || ; | & ( ), skips `sudo`/`env` prefixes and git's global opts
`-c key=val` / `-C dir`), so `git status; git -c x=y push` cannot slip by.
"""
import hashlib
import importlib.util
import json
import os
import re
import shlex
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlsplit

# ------------------------------------------------------------------- CONFIG

WORKSPACE = "wow-two-ws"
DOC = "conventions/development/repo/version-control/git.md -> ## Discipline"
STRICT = False          # True -> no pull / branch / stash-write / tag write either
LANE_CHECK = True       # True -> pull / stash-push ask about foreign dirt
COMMITS = "switch"      # "switch": the repository commit switch · "open": plain commits, lane-checked · "never"
ALLOWED_HERE = "index-only staging/unstaging, unforced `git mv` / `git rm`, `git apply`, branch create/switch,\n`git stash`, `git pull`, `git fetch`, read-only git + `gh`, ordinary commits and rewrites of unpushed\ncommits while the repository's `commit` flag is ON, and ordinary pushes and gh writes while its `push` flag is ON."
HANDOVER = "Hand it over by name in chat (`push main to origin`, `discard my edits to Program.cs`)\nand STOP; the developer runs it in GitKraken. A subject-only commit message is welcome."

# ------------------------------------------------------------------- engine

# The repository commit switch; this file sits at `<workspace>/.claude/hooks/`.
SWITCH = Path(__file__).resolve().parents[2] / ".codex" / "hooks" / "commit_permission.py"
COMMIT_FORM = 'git -C <repo> commit -m "subject"'
PUSH_FORM = 'git -C <repo> push [-u] [<remote> [<ref>]]'

# The flag store, its change log and its lock; no tool edits or names them.
STORE_FILES = re.compile(r"git-flags\.(?:json|log|lock)")
EDIT_TOOLS = {"Write", "Edit", "MultiEdit", "NotebookEdit"}

# Session file-touch ledger, written by the PostToolUse hook `track-touch.py`.
# Same `${TMPDIR:-/tmp}` + session-id shape as `style-recharge.sh`'s turn counter.
LEDGER_PREFIX = "claude-git-lane-"

# -------------------------------------------------------------- policy sets

# Read-only git — allowed everywhere, whatever the args.
READ_ONLY = {
    "status", "log", "diff", "show", "blame", "describe", "rev-parse", "ls-files",
    "shortlog", "fetch", "grep", "cat-file", "rev-list", "ls-tree", "ls-remote",
    "show-ref", "show-branch", "diff-tree", "diff-index", "name-rev", "merge-base",
    "check-ignore", "check-attr", "count-objects", "verify-commit", "verify-tag",
    "whatchanged", "range-diff", "cherry", "annotate", "var", "version", "help",
}

# The flag kinds: history rewrites follow `commit`, gh writes follow `push`, each while the target repository's
# flag is ON.
FLAG_KINDS = {"commit", "push"}
# Gated kinds that rewrite the index or the working tree, so they meet the lane check too.
LANE_KINDS = {"commit"}

# Worktree destruction — rarely needed, never run.
# `restore` is NOT here: `--staged` alone is index-only and safe, so it is
# resolved in git_verdict() where the flags are visible.
WORKTREE_KILL = {"clean", "checkout-index"}
RESET_KILL = {"--hard", "--merge", "--keep"}
CHECKOUT_KILL = {"-f", "--force", "--ours", "--theirs"}
SWITCH_KILL = {"-f", "--force", "--discard-changes"}

# Ref and object surgery — rarely needed, never run.
SURGERY = {
    "filter-branch", "filter-repo", "fast-import", "update-ref", "update-index", "replace",
    "gc", "prune",
}

# Never run by an agent, whatever the flags.
NEVER = {"send-email"}

# History rewrites — the `commit` flag. `pull` is NOT here: it is allowed
# outside STRICT workspaces, lane check aside.
HISTORY = {"merge", "rebase", "cherry-pick", "revert", "am", "subtree"}

# Directory changes that hide which repository a later command in the same shell string acts on.
DIRECTORY_CHANGES = {"cd", "pushd", "popd"}

# Ops that touch the working tree with more than this session's own edits, so they
# ask about foreign dirt first (STRICT workspaces forbid them outright).
STASH_PUSH = {"", "push", "save"}

# family -> verbs that WRITE (everything else in the family reads).
WRITE_VERBS = {
    "reflog": {"expire", "delete", "drop", "write"},
    "remote": {"add", "remove", "rm", "rename", "set-url", "set-head", "set-branches",
               "prune", "update"},
    "worktree": {"add", "remove", "move", "prune", "lock", "unlock", "repair"},
    "submodule": {"add", "deinit", "set-url", "set-branch", "absorbgitdirs"},
}
# family -> verbs that READ (everything else in the family, bare included, writes).
READ_VERBS = {"stash": {"list", "show"}}

BRANCH_WRITE_FLAGS = {"-d", "-D", "--delete", "-m", "-M", "--move", "-c", "-C", "--copy",
                      "-f", "--force", "-u", "--set-upstream-to", "--unset-upstream",
                      "--edit-description"}
BRANCH_VALUE_FLAGS = {"--contains", "--no-contains", "--merged", "--no-merged",
                      "--points-at", "--sort", "--format", "--color", "-t", "--track"}
TAG_WRITE_FLAGS = {"-a", "--annotate", "-s", "--sign", "-d", "--delete", "-f", "--force",
                   "-m", "--message", "-F", "--file", "-u", "--local-user"}
TAG_VALUE_FLAGS = {"--contains", "--no-contains", "--points-at", "--merged", "--no-merged",
                   "--sort", "--format", "--color", "-n"}
CONFIG_WRITE_FLAGS = {"--unset", "--unset-all", "--add", "--replace-all", "--edit", "-e",
                      "--remove-section", "--rename-section"}
CONFIG_VALUE_FLAGS = {"--get", "--get-all", "--get-regexp", "--get-urlmatch", "--type",
                      "--default", "-f", "--file", "--blob"}

# gh: (group, verb) pairs that write, plus a verb-level net for the rest.
GH_BLOCKED_PAIRS = {
    ("pr", "create"), ("pr", "comment"), ("pr", "merge"), ("pr", "close"), ("pr", "edit"),
    ("pr", "review"), ("pr", "ready"), ("pr", "reopen"), ("pr", "lock"), ("pr", "unlock"),
    ("issue", "create"), ("issue", "comment"), ("issue", "close"), ("issue", "edit"),
    ("issue", "reopen"), ("issue", "delete"), ("issue", "transfer"), ("issue", "pin"),
    ("release", "create"), ("release", "delete"), ("release", "edit"), ("release", "upload"),
    ("workflow", "run"), ("workflow", "enable"), ("workflow", "disable"),
    ("repo", "create"), ("repo", "delete"), ("repo", "edit"), ("repo", "rename"),
    ("repo", "archive"), ("repo", "unarchive"), ("repo", "sync"), ("repo", "fork"),
    ("run", "rerun"), ("run", "cancel"), ("run", "delete"),
    ("secret", "set"), ("secret", "delete"), ("variable", "set"), ("variable", "delete"),
    ("cache", "delete"), ("gist", "create"), ("gist", "delete"), ("gist", "edit"),
    ("label", "create"), ("label", "delete"), ("label", "edit"), ("label", "clone"),
    ("project", "create"), ("project", "delete"), ("project", "edit"),
}
GH_WRITE_VERBS = {"create", "delete", "edit", "merge", "close", "reopen", "comment",
                  "review", "ready", "sync", "rename", "archive", "unarchive", "set",
                  "add", "remove", "upload", "transfer", "fork", "lock", "unlock",
                  "pin", "unpin", "rerun", "cancel", "import", "revoke"}
GH_API_WRITE_METHODS = {"POST", "PUT", "PATCH", "DELETE"}
# `gh api -f/-F/--field/--raw-field/--input` makes the request a POST with no `-X`.
GH_API_IMPLICIT_POST = {"-f", "-F", "--field", "--raw-field", "--input"}
# gh (group, verb) pairs a workspace blocks on top of these; its CONFIG block may set EXTRA_GH_BLOCKED.
EXTRA_GH_BLOCKED = globals().get("EXTRA_GH_BLOCKED", set())
# gh writes an agent never runs, whatever the flags.
GH_NEVER = {("repo", "delete")}
GH_REPO_FLAGS = {"-R", "--repo"}
# gh flags that take a separate value, so the positional after them is not the endpoint or repository.
GH_VALUE_FLAGS = {"-X", "--method", "-H", "--header", "-f", "-F", "--field", "--raw-field", "--input",
                  "-q", "--jq", "-t", "--template", "--cache", "-p", "--preview", "--hostname",
                  "-R", "--repo", "--source", "--remote", "-d", "--description", "-h", "--homepage",
                  "--visibility", "-b", "--body", "-T", "--title", "--team", "--template-repository",
                  "-l", "--label", "-a", "--assignee", "-m", "--milestone", "--base", "--head",
                  "--ref", "--json", "-e", "--env", "--app", "--org", "-u", "--user"}
GLOBAL_OPTS_WITH_VALUE = {"-c", "-C", "--git-dir", "--work-tree", "--namespace",
                          "--exec-path", "--super-prefix", "--config-env"}
SEPARATORS = {"&&", "||", ";", "|", "&", "(", ")", "{", "}", "\n", "!"}
CMD_PREFIXES = {"sudo", "env", "command", "nohup", "time", "exec", "builtin", "then",
                "do", "else", "elif"}

# ------------------------------------------------------------------ parsing


def tokenize(cmd):
    """Split a shell string into tokens, keeping `&&` / `;` / `|` as their own token."""
    try:
        lex = shlex.shlex(cmd, posix=True, punctuation_chars=True)
        lex.whitespace_split = True
        lex.commenters = ""
        return list(lex)
    except ValueError:  # unbalanced quotes — degrade to a permissive split
        return re.sub(r"(&&|\|\||;|\||&|\(|\))", r" \1 ", cmd).split()


def invocations(cmd, binaries):
    """Yield (binary, subcommand, args, directory, hidden) for each `binary ...` call in a shell string.

    `directory` joins every `git -C <dir>` in order (None without one). `hidden` is True when the
    repository cannot be read from the call itself: an earlier `cd` / `pushd` / `popd` in the same
    string, or a `--git-dir` / `--work-tree` option."""
    toks = tokenize(cmd)
    out, i, expect_cmd, moved = [], 0, True, False
    while i < len(toks):
        t = toks[i]
        if t in SEPARATORS:
            expect_cmd = True
            i += 1
            continue
        if expect_cmd:
            base = t.rsplit("/", 1)[-1]
            if base in CMD_PREFIXES or (("=" in t) and not t.startswith("-")):
                i += 1  # `sudo git push` / `VAR=x git push` — the command is still ahead
                continue
            if base in DIRECTORY_CHANGES:
                moved = True
            if base in binaries:
                j, directory, hidden = i + 1, None, moved
                while j < len(toks):  # skip global options to reach the subcommand
                    a = toks[j]
                    if a in GLOBAL_OPTS_WITH_VALUE:
                        if a == "-C" and j + 1 < len(toks):
                            directory = os.path.join(directory or "", toks[j + 1])
                        elif a in ("--git-dir", "--work-tree"):
                            hidden = True
                        j += 2
                        continue
                    if a.startswith(("--git-dir=", "--work-tree=")):
                        hidden = True
                    if a.startswith("-"):
                        j += 1
                        continue
                    break
                if j < len(toks):
                    end = j + 1
                    while end < len(toks) and toks[end] not in SEPARATORS:
                        end += 1
                    out.append((base, toks[j].lower(), toks[j + 1:end], directory, hidden))
                else:
                    out.append((base, "", [], directory, hidden))
            expect_cmd = False
        i += 1
    return out


def positionals(args, value_flags):
    """Non-flag args, skipping the value of a flag that takes one as a separate token."""
    out, skip = [], False
    for a in args:
        if skip:
            skip = False
            continue
        if a.startswith("-"):
            if a in value_flags:
                skip = True
            continue
        out.append(a)
    return out


def label(binary, sub, args):
    text = " ".join([binary] + ([sub] if sub else []) + list(args)).strip()
    return text if len(text) <= 110 else text[:107] + "..."


# ------------------------------------------------------------------ verdicts
# A verdict is (kind, label): kind is "hard" (never allowed here), "lane" (allowed after
# the lane check) or a FLAG_KINDS category (allowed while the repository's flag is ON).
# None means allowed.


def checkout_discards(args, flags, cwd):
    """Recognize checkout's path form even when its optional `--` is omitted."""
    short = {c for a in args if a.startswith("-") and not a.startswith("--") for c in a[1:]}
    if ("--" in args or "." in args or flags & CHECKOUT_KILL or "p" in short
            or flags & {"--patch", "--pathspec-from-file", "--pathspec-file-nul"}):
        return True
    named = positionals(args, {"-b", "-B", "--orphan", "--conflict"})
    if len(named) > 1:
        return True  # tree-ish + pathspec, not a branch switch
    if not named or flags & {"-b", "-B", "--orphan"}:
        return False
    if cwd is None:
        return True  # a preceding directory change hides the path/branch distinction
    # A branch/ref takes precedence over a same-named file. Otherwise tracked pathspecs
    # select the worktree-discard form, including deleted files and wildcard pathspecs.
    try:
        ref = subprocess.run(["git", "-C", cwd, "rev-parse", "--verify", "--quiet", "--end-of-options",
                              named[0] + "^{commit}"], capture_output=True, timeout=5)
        if ref.returncode == 0:
            return False
        paths = subprocess.run(["git", "-C", cwd, "ls-files", "--error-unmatch", "--", named[0]],
                               capture_output=True, timeout=5)
        return paths.returncode == 0
    except (OSError, subprocess.TimeoutExpired):
        return True


def git_verdict(sub, args, cwd=None):
    options = args[:args.index("--")] if "--" in args else args
    flags = {a.split("=", 1)[0] for a in options if a.startswith("-")}
    text = label("git", sub, args)
    hard, lane = ("hard", text), ("lane", text)

    def gated(kind):
        return hard if STRICT else (kind, text)

    if sub == "push":
        # An ordinary push under the "switch" passes in main() through the flag; every other form, forcing,
        # deleting, mirror, pruning or hook-skipping included, lands here and never runs.
        return hard
    if sub == "restore":
        # `--staged`/`-S` alone rewrites the index; the worktree is untouched, so
        # nothing uncommitted can be lost. Adding `--worktree`/`-W` (or passing no
        # flag at all) overwrites files from the index or HEAD -> destruction.
        short = {c for a in options if a.startswith("-") and not a.startswith("--") for c in a[1:]}
        staged = "--staged" in flags or "S" in short
        worktree = "--worktree" in flags or "W" in short
        return None if (staged and not worktree) else hard
    if sub in WORKTREE_KILL:
        return hard
    if sub in {"rm", "mv"}:
        # `rm` refuses a file with uncommitted changes and `mv` an existing target, unless forced.
        return hard if flags & {"-f", "--force"} else None
    if sub == "apply":
        # A patch applies like an edit and fails rather than overwrite on a conflict; applied in reverse,
        # a `git diff` output discards the worktree's changes.
        return hard if flags & {"-R", "--reverse"} else None
    if sub in NEVER or sub in SURGERY:
        return hard
    if sub == "reset":
        if flags & RESET_KILL:
            return hard
        if "--" in args and args.index("--") < len(args) - 1 and not (flags & {"--soft", "--mixed"}):
            return None  # explicit path reset touches only the index
        return gated("commit")
    if sub == "checkout":
        return hard if STRICT or checkout_discards(args, flags, cwd) else None
    if sub == "switch":
        if flags & SWITCH_KILL:
            return hard
        return hard if STRICT else None
    if sub == "commit":
        # "switch" commits pass in main() through the switch; every other form lands here.
        if "--amend" in flags:
            return gated("commit")
        if COMMITS != "open" or STRICT:
            return hard
        return lane
    if sub == "pull":
        return hard if STRICT else lane  # allowed outside eis-ws, lane check aside
    if sub in HISTORY:
        return gated("commit")
    if sub == "stash":
        verb = next((a for a in args if not a.startswith("-")), "")
        if verb in READ_VERBS["stash"]:
            return None
        if STRICT:
            return hard
        return lane if verb in STASH_PUSH else None  # pop/apply/drop touch only my dirt
    if sub == "branch":
        if not STRICT:
            return None
        if flags & BRANCH_WRITE_FLAGS or positionals(args, BRANCH_VALUE_FLAGS):
            return hard
        return None
    if sub == "tag":
        if not STRICT:
            return None
        if flags & TAG_WRITE_FLAGS or positionals(args, TAG_VALUE_FLAGS):
            return hard
        return None
    if sub == "config":
        named = positionals(args, CONFIG_VALUE_FLAGS)
        verb = named[0] if named else ""
        if flags & CONFIG_WRITE_FLAGS or verb in {"set", "unset", "rename-section", "remove-section", "edit"}:
            return hard
        if verb in {"get", "list"}:
            return None
        return hard if len(named) >= 2 else None
    if sub == "lfs":
        named = positionals(args, set())
        verb = named[0] if named else ""
        # LFS upload is not the documented ordinary `git push` exception. Installation,
        # pruning and migration writes retain their existing human-only restrictions.
        if verb == "migrate":
            return None if len(named) > 1 and named[1] == "info" else hard
        safe = {"", "help", "version", "env", "status", "ls-files", "fetch", "pull", "checkout", "track", "untrack"}
        return None if verb in safe else hard
    if sub == "symbolic-ref":
        if flags & {"-d", "--delete"} or len(positionals(args, set())) >= 2:
            return hard
        return None
    if sub in WRITE_VERBS:
        verb = next((a for a in args if not a.startswith("-")), "")
        return hard if verb in WRITE_VERBS[sub] else None
    if sub in READ_ONLY or sub == "add" or not sub:
        return None
    return None  # unknown subcommand — stay out of the way rather than guess


def gh_verdict(sub, args):
    verb = next((a for a in args if not a.startswith("-")), "").lower()
    text = label("gh", sub, args)
    hard = ("hard", text)
    if (sub, verb) in GH_NEVER:
        return hard
    flags = {a.split("=", 1)[0] for a in args if a.startswith("-")}
    if sub == "repo" and verb == "create" and flags & {"--source", "--remote", "--push"}:
        return hard  # source/remote configure a local remote; push is not an ordinary git push
    gated = hard if STRICT else ("push", text)
    if sub == "api":
        method = ""
        for i, a in enumerate(args):
            if a in ("-X", "--method") and i + 1 < len(args):
                method = args[i + 1].upper()
            elif a.startswith("--method="):
                method = a.split("=", 1)[1].upper()
            elif a.startswith("-X") and len(a) > 2:
                method = a[2:].upper()
        if method == "DELETE" and re.fullmatch(r"/?(?:api/v3/)?repos/[^/]+/[^/]+/?", gh_api_path(args)):
            return hard  # repository deletion stays human-only through REST too
        if method in GH_API_WRITE_METHODS:
            return gated
        if any(a.split("=", 1)[0] in GH_API_IMPLICIT_POST for a in args):
            return gated  # `-f key=val` turns `gh api` into a POST with no `-X`
        return None
    if (sub, verb) in GH_BLOCKED_PAIRS or (sub, verb) in EXTRA_GH_BLOCKED:
        return gated
    if verb in GH_WRITE_VERBS:
        return gated
    return None


# ------------------------------------------------------------ gated targets
# A gated category reads the flag of the repository the command acts on.

WORKSPACE_ROOT = Path(__file__).resolve().parents[2]
GITHUB_SLUG = re.compile(r"github\.com[:/]+([^/\s]+)/([^/\s]+?)(?:\.git)?/?$", re.I)


def git_target(directory, hidden, cwd):
    """The directory a git call acts on, or None when the call hides it."""
    if hidden:
        return None
    base = cwd or os.getcwd()
    return os.path.normpath(os.path.join(base, directory)) if directory else base


def gh_api_path(args):
    named = positionals(args, GH_VALUE_FLAGS)
    return urlsplit(named[0]).path if named else ""


def gh_slug(sub, args):
    """The `owner/name` a gh write names, `("path", dir)` for `repo create --source`, or None."""
    for i, a in enumerate(args):
        if a in GH_REPO_FLAGS and i + 1 < len(args):
            return args[i + 1]
        if a.startswith("--repo="):
            return a.split("=", 1)[1]
        if sub == "repo" and a == "--source" and i + 1 < len(args):
            return ("path", args[i + 1])
        if sub == "repo" and a.startswith("--source="):
            return ("path", a.split("=", 1)[1])
    named = positionals(args, GH_VALUE_FLAGS)
    if sub == "api" and named:
        match = re.match(r"/?(?:api/v3/)?repos/([^/\s]+)/([^/?\s]+)", gh_api_path(args))
        return match.group(1) + "/" + match.group(2) if match else None
    if sub == "repo" and len(named) >= 2 and "/" in named[1]:
        return named[1]
    return None


def repository_configs():
    """Visit managed repositories, descending through nested workbenches without a depth limit.

    Grouping folders may contain repositories at any depth. Once a repository is found, only
    its `workbench` can own nested repositories; dependency/source trees are not searched.
    Directory symlinks are never followed, and Git metadata must remain inside the workspace.
    """
    root = WORKSPACE_ROOT.resolve()
    excluded = {".git", "node_modules", "vendor", ".venv", "venv", "__pycache__", ".cache"}

    def config_for(repo):
        marker = repo / ".git"
        try:
            if marker.is_symlink():
                return None
            if marker.is_file():
                text = marker.read_text(encoding="utf-8").strip()
                if not text.startswith("gitdir:"):
                    return None
                gitdir = (repo / text.split(":", 1)[1].strip()).resolve()
            else:
                gitdir = marker.resolve()
            gitdir.relative_to(root)
            common = (gitdir / "commondir").resolve()
            common.relative_to(root)
            if common.is_file():
                gitdir = (gitdir / common.read_text(encoding="utf-8").strip()).resolve()
                gitdir.relative_to(root)
            config = (gitdir / "config").resolve()
            config.relative_to(root)
            return config if config.is_file() else None
        except (OSError, ValueError):
            return None

    config = config_for(root)
    if config:
        yield root, config
    workbench = root / "workbench"
    if not workbench.is_dir() or workbench.is_symlink():
        return
    for directory, children, _ in os.walk(workbench, followlinks=False):
        repo = Path(directory)
        children[:] = sorted(name for name in children
                             if name not in excluded and not (repo / name).is_symlink())
        if (repo / ".git").exists():
            config = config_for(repo)
            if config:
                yield repo, config
            children[:] = [name for name in children if name == "workbench"]


def local_repository(slug):
    """The workspace repository whose remote points at `owner/name` on GitHub, or None."""
    wanted = "/".join(slug.lower().rstrip("/").removesuffix(".git").split("/")[-2:])
    for repo, config in repository_configs():
        try:
            content = config.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for url in re.findall(r"^\s*url\s*=\s*(\S+)", content, re.M):
            match = GITHUB_SLUG.search(url)
            if match and (match.group(1) + "/" + match.group(2)).lower() == wanted:
                return str(repo)
    return None


def gh_target(sub, args, cwd):
    """The workspace directory whose flag a gh write reads."""
    named = gh_slug(sub, args)
    if isinstance(named, tuple):
        return os.path.normpath(os.path.join(cwd or os.getcwd(), named[1]))
    if named:
        return local_repository(named) or str(WORKSPACE_ROOT)
    return cwd or os.getcwd()


_SWITCH_MODULE = []


def switch_module():
    """The flag module, loaded once; None when this workspace does not install it."""
    if not _SWITCH_MODULE:
        module = None
        if SWITCH.is_file():
            sys.dont_write_bytecode = True
            spec = importlib.util.spec_from_file_location("commit_permission", SWITCH)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
        _SWITCH_MODULE.append(module)
    return _SWITCH_MODULE[0]


def flag_decision(kind, target):
    """(allowed, reason) for a gated category at `target`; None when this workspace has no flags."""
    try:
        module = switch_module()
    except Exception as error:  # a broken flag module never permits a gated command
        return False, "The flag module failed ({}); the command stays blocked.".format(type(error).__name__)
    if module is None or not hasattr(module, "enabled"):
        return None
    if target is None:
        return False, ("The command changes directory or names a Git directory, so the guard cannot tell\n"
                       "which repository it acts on. Name it with `git -C <repo>` in a command of its own.")
    return module.enabled(kind, target)


def assess(cmd, cwd):
    """(block, lanes) for a shell string.

    `block` is the first call that must stop, as (kind, label, subcommand, reason), or None. `lanes`
    lists every passing call that meets the lane check, as (family, label, directory)."""
    lanes = []
    for binary, sub, args, directory, hidden in invocations(cmd, {"git", "gh"}):
        verdict = (gh_verdict(sub, args) if binary == "gh"
                   else git_verdict(sub, args, git_target(directory, hidden, cwd)))
        if not verdict:
            continue
        kind, op = verdict
        if kind == "lane":
            lanes.append((lane_family(sub, args), op, git_target(directory, hidden, cwd) or cwd))
            continue
        if kind not in FLAG_KINDS:
            return (kind, op, sub, None), lanes
        target = gh_target(sub, args, cwd) if binary == "gh" else git_target(directory, hidden, cwd)
        decision = flag_decision(kind, target)
        if decision is None:
            return ("hard", op, sub, None), lanes
        allowed, reason = decision
        if not allowed:
            return (kind, op, sub, reason), lanes
        if binary == "git" and kind == "commit":
            revisions = replaced(sub, args)
            pushed = None if revisions is None else published(target, revisions)
            if pushed is not False:
                return ("rewrite", op, sub, PUSHED if pushed else UNCLEAR), lanes
        if kind in LANE_KINDS and LANE_CHECK:
            lanes.append((kind, op, target))
    return None, lanes


# --------------------------------------------------------- pushed history
# A flagged rewrite never replaces a commit that a remote-tracking branch already holds.

REBASE_VALUE_FLAGS = {"--onto", "-s", "--strategy", "-X", "--strategy-option", "-x", "--exec", "--empty",
                      "--whitespace", "-C"}
REBASE_RESUME = {"--continue", "--abort", "--skip", "--quit", "--edit-todo", "--show-current-patch"}
PUSHED = "It replaces commits a remote-tracking branch already holds; rewriting pushed history stays with the developer."
UNCLEAR = ("The guard cannot tell which commits it replaces. Name the range plainly in a command of its own,\n"
           "such as `git -C <repo> rebase <upstream>` or `git -C <repo> reset --soft <commit>`.")


def replaced(sub, args):
    """Revision arguments naming the commits a rewrite replaces, [] when it replaces none, None when unclear."""
    if sub == "commit":
        return ["HEAD^!"]  # `--amend` replaces HEAD
    options = args[:args.index("--")] if "--" in args else args
    flags = {a.split("=", 1)[0] for a in options if a.startswith("-")}
    if sub == "reset":
        named = positionals(options, {"--pathspec-from-file"})
        return [(named[0] if named else "HEAD") + "..HEAD"] if len(named) <= 1 else None
    if sub == "rebase":
        if flags & REBASE_RESUME:
            return []  # continues or ends a rebase that already started
        named = positionals(options, REBASE_VALUE_FLAGS)
        if len(named) > 2:
            return None
        branch = named[1] if len(named) == 2 else "HEAD"
        if "--root" in flags:
            return [branch]
        return [(named[0] if named else "@{upstream}") + ".." + branch]
    return []  # merge, cherry-pick, revert, am and subtree add commits and replace none


def published(cwd, revisions):
    """True when a commit in `revisions` is on a remote-tracking branch; None when git cannot tell."""
    if not revisions:
        return False
    if cwd is None or any(rev.startswith("-") for rev in revisions):
        return None
    every = git_out(cwd, ["rev-list", "--count"] + revisions + ["--"])
    local = git_out(cwd, ["rev-list", "--count"] + revisions + ["--not", "--remotes", "--"])
    if every is None or local is None:
        return None
    return every.strip() != local.strip()


def lane_family(sub, args):
    """Which lane-checked op this is: 'commit' | 'pull' | 'stash', or '' for none."""
    if not LANE_CHECK:
        return ""
    if sub in ("commit", "pull"):
        return sub
    if sub == "stash":
        verb = next((a for a in args if not a.startswith("-")), "")
        return "stash" if verb in STASH_PUSH else ""
    return ""


# ------------------------------------------------------------ commit switch

def switch_verdict(data, cmd):
    """(allowed, reason) for an ordinary commit or push from a Claude chat under COMMITS "switch"; None otherwise."""
    sid = data.get("session_id")
    # A Codex adapter applies the switch before delegating here; its session ids start with `codex-`.
    if COMMITS != "switch" or not isinstance(sid, str) or not sid or sid.startswith("codex-"):
        return None
    if not SWITCH.is_file():
        return None  # not installed: every commit form falls through to the hard verdict
    if not any(sub in ("commit", "push") for _, sub, *_ in invocations(cmd, {"git"})):
        return None  # only a commit or push consults the switch, so a broken switch cannot block other commands
    try:
        sys.dont_write_bytecode = True
        spec = importlib.util.spec_from_file_location("commit_permission", SWITCH)
        switch = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(switch)
        # Claude chats are recorded as `claude-<session_id>`; the tool call is the native event.
        payload = {"session_id": "claude-" + sid, "turn_id": data.get("tool_use_id") or ""}
        return switch.assess(payload, cmd, data.get("cwd") or str(SWITCH.parents[2]))
    except Exception as error:  # a broken switch never permits a commit
        return False, "Commit blocked: the commit switch failed ({}).".format(type(error).__name__)


# ------------------------------------------------------ lane check (shared tree)
# Several chats edit one working tree on one branch. A modified / staged file this
# session never wrote is probably another lane's work, and `commit` / `pull` /
# `stash push` would sweep it up. The hook cannot know who edited what, so it reads
# the ledger that the PostToolUse hook `track-touch.py` appends to for every
# Write / Edit. No ledger (hook not installed, or no edits yet) = nothing is mine.


def session_dir(session_id):
    """Per-session scratch dir, or None when the id is missing / unusable."""
    if not re.fullmatch(r"[A-Za-z0-9._-]{1,128}", session_id or ""):
        return None
    return Path(os.environ.get("TMPDIR") or "/tmp") / (LEDGER_PREFIX + session_id)


def git_out(cwd, args):
    try:
        p = subprocess.run(["git", "-C", cwd] + args, capture_output=True, text=True,
                           timeout=5)
    except Exception:
        return None
    return p.stdout if p.returncode == 0 else None


def touched(sdir):
    try:
        raw = (sdir / "touched").read_text(encoding="utf-8", errors="replace")
    except OSError:
        return set()
    return {os.path.realpath(line.strip()) for line in raw.splitlines() if line.strip()}


def out_of_lane(cwd, sdir):
    """Modified / staged paths this session never wrote. None -> check not applicable."""
    if not cwd or not os.path.isdir(cwd):
        return None
    root = git_out(cwd, ["rev-parse", "--show-toplevel"])
    status = git_out(cwd, ["status", "--porcelain"])
    if root is None or status is None:
        return None  # not a repo, or git unavailable — never block on that
    root, mine, strays = root.strip(), touched(sdir), []
    for line in status.splitlines():
        if len(line) < 4 or line[0] in "?!" or line[1] in "?!":
            continue  # untracked / ignored — neither modified nor staged
        path = line[3:]
        if " -> " in path:  # rename: the destination is the live path
            path = path.split(" -> ", 1)[1]
        path = path.strip().strip('"')
        if os.path.realpath(os.path.join(root, path)) not in mine:
            strays.append(path)
    return sorted(set(strays))


def already_asked(sdir, family, strays):
    """True if this exact stray set was already raised for this op. Warns once."""
    key = hashlib.sha1("|".join([family] + strays).encode("utf-8")).hexdigest()[:16]
    flag = sdir / ("asked-" + key)
    try:
        if flag.exists():
            return True
        sdir.mkdir(parents=True, exist_ok=True)
        flag.write_text("", encoding="utf-8")
    except OSError:
        return False  # cannot record it -> ask again rather than wave it through
    return False


# ------------------------------------------------------------------ messages

def hard_message(op, sub=""):
    form = {"commit": COMMIT_FORM, "push": PUSH_FORM}.get(sub) if COMMITS == "switch" else None
    force = " Forcing, deleting and mirror pushes never run." if sub == "push" else ""
    commit = ("An ordinary {sub} runs only as `{form}` while the repository's\n"
              "{sub} flag is ON; check it with `~{sub}_status <repo>`.{force}\n"
              ).format(sub=sub, form=form, force=force) if form else ""
    return (
        "BLOCKED — {ws} git policy ({doc}).\n"
        "Operation: `{op}` — no flag permits it in {ws}; Claude never runs it, in any session.\n"
        "{commit}"
        "{handover}\n"
        "Allowed here: {allowed}\n"
        "Approval-shaped questions (\"go ahead\", \"can we push?\") are NOT authorization.\n"
    ).format(ws=WORKSPACE, doc=DOC, op=op, commit=commit, handover=HANDOVER, allowed=ALLOWED_HERE)


def flag_message(op, kind, reason):
    return (
        "BLOCKED — {ws} git flag `{kind}` ({doc}).\n"
        "Operation: `{op}`\n"
        "{reason}\n"
        "The developer turns it on with a whole-message `~git_on {kind} <repo>` (`*` for the workspace\n"
        "default) and reads every flag with `~git_status <repo>`; a tool call can never change a flag.\n"
    ).format(ws=WORKSPACE, doc=DOC, op=op, kind=kind, reason=reason)


def rewrite_message(op, reason):
    return (
        "BLOCKED — {ws} git flag `commit` ({doc}).\n"
        "Operation: `{op}`\n"
        "{reason}\n"
        "{handover}\n"
    ).format(ws=WORKSPACE, doc=DOC, op=op, reason=reason, handover=HANDOVER)


def store_message(target):
    return (
        "BLOCKED — {ws} git flag store ({doc}).\n"
        "`{target}` names the git flag store or its hash-chained change log. Only a whole-message directive\n"
        "changes a flag (`~git_on|off <kind> <repo>`, `*` for the workspace default), and `~git_status *`\n"
        "reads them all; no tool edits, moves or reads the store. Ask the developer in chat.\n"
    ).format(ws=WORKSPACE, doc=DOC, target=target)


def switch_message(reason):
    return (
        "BLOCKED — {ws} commit switch ({doc}).\n"
        "{reason}\n"
        "The developer enables a repository with a whole-message `~commit_on <repo>` (commits)\n"
        "or `~push_on <repo>` (pushes), `*` for the workspace default, and reads each with\n"
        "`~commit_status` / `~push_status`; a tool call can never change them.\n"
    ).format(ws=WORKSPACE, doc=DOC, reason=reason)


def lane_message(op, family, strays):
    shown = strays[:12]
    listing = "\n".join("  - " + s for s in shown)
    if len(strays) > len(shown):
        listing += "\n  - ... and {} more".format(len(strays) - len(shown))
    return (
        "BLOCKED — {ws} lane check ({doc}).\n"
        "Operation: `{op}` — the tree carries {n} modified/staged file(s) this session\n"
        "never wrote. Chats share one working tree on one branch, so `{fam}` would sweep\n"
        "up what is probably another lane's in-flight work:\n"
        "{listing}\n"
        "Ask the developer, in chat, before retrying: is another lane working right now?\n"
        "  yes -> leave those files alone; carve the index to this lane's paths only.\n"
        "  no  -> completed-but-uncommitted work; staging is allowed.\n"
        "This asks once per file set: after the answer, re-run the command and it runs.\n"
    ).format(ws=WORKSPACE, doc=DOC, op=op, n=len(strays), fam=family, listing=listing)


# ---------------------------------------------------------------------- main

def edited_paths(tool_input):
    """Every file path a Write / Edit / MultiEdit / NotebookEdit call names."""
    paths = [tool_input.get(name) for name in ("file_path", "notebook_path")]
    paths += [edit.get("file_path") for edit in tool_input.get("edits") or [] if isinstance(edit, dict)]
    return [path for path in paths if isinstance(path, str) and path]


def protected(path):
    """True for the flag store, its change log or its lock, by name or through a symbolic link."""
    return any(STORE_FILES.fullmatch(os.path.basename(p)) for p in (path, os.path.realpath(path)))


def main():
    cmd = ""
    try:
        data = json.loads(sys.stdin.read())
        tool = data.get("tool_name")
        if tool in EDIT_TOOLS:
            hit = next((p for p in edited_paths(data.get("tool_input") or {}) if protected(p)), None)
            if hit:
                sys.stderr.write(store_message(hit))
                return 2
            return 0
        if tool != "Bash":
            return 0
        cmd = (data.get("tool_input") or {}).get("command") or ""
        named = STORE_FILES.search(cmd)
        if named:
            sys.stderr.write(store_message(named.group(0)))
            return 2
        decision = switch_verdict(data, cmd)
        if decision is not None:
            allowed, reason = decision
            if allowed:
                return 0  # the flag is ON; the switch inspected the exact form
            sys.stderr.write(switch_message(reason))
            return 2
        block, lanes = assess(cmd, data.get("cwd") or "")
        if block:
            kind, op, sub, reason = block
            if kind == "hard":
                sys.stderr.write(hard_message(op, sub))
            elif kind == "rewrite":
                sys.stderr.write(rewrite_message(op, reason))
            else:
                sys.stderr.write(flag_message(op, kind, reason))
            return 2  # exit 2 -> PreToolUse blocks, stderr is fed back to the agent
        sdir = session_dir(data.get("session_id"))
        for family, op, directory in lanes:
            if family and sdir is not None:
                strays = out_of_lane(directory or "", sdir)
                if strays and not already_asked(sdir, family, strays):
                    sys.stderr.write(lane_message(op, family, strays))
                    return 2
        return 0
    except Exception:
        # A broken guard must never block unrelated commands, nor let a git or gh write through.
        return 2 if re.search(r"(^|[\s;&|(])(git|gh)(\s|$)", cmd) else 0


if __name__ == "__main__":
    sys.exit(main())

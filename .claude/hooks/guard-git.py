#!/usr/bin/env python3
"""wow-two-ws git guard — PreToolUse(Bash) hook.

Mechanically enforces `conventions/development/repo/version-control/git.md`
-> ## Discipline. Agents stage; the developer commits and pushes. Publishing and
history rewriting stay the developer's, in GitKraken — except during a rapid-
building session, when the history ops unlock (see `marker` below). `push` is
what leaves the machine, and no session unlocks it.

Shared policy (identical in eis-ws / 10x-ws / wow-two-ws):
  allowed    index-only staging/unstaging (`add`, `restore --staged`, path `reset`,
             `apply --cached`, `rm --cached`) · read-only git
             (status log diff show blame describe rev-parse ls-files shortlog
             reflog, `branch --list`, `remote -v`, `stash list|show`) ·
             `git fetch` · read-only gh (`pr view|list|diff|checks|status`,
             `run view|list|watch`, `issue view|list`, `api` GET, `repo view`,
             `auth status`)
  forbidden  `git commit` in every form, including `--amend`; `git push` in every form (`--force`, `--force-with-lease`, `--tags`,
             and push-by-gh) · worktree destruction (`reset --hard`, `restore` to the worktree,
             `checkout -- <path>`, `checkout .`, `clean`) · every gh write
             (`pr create|comment|merge|close|edit|review|ready`,
             `issue create|comment|close|edit`, `release create`,
             `api -X POST|PUT|PATCH|DELETE`, `workflow run`, `repo create|delete`)
  wow-two    allowed on top of the shared list: `git pull`,
             branch create / switch (`branch <name>`, `switch`,
             `checkout -b`, `checkout <branch>`), `git stash` (every subcommand —
             a stash is a real ref and shows in GitKraken's Stashes panel).
             Gated on a rapid-building session: `merge`, `rebase`,
             `cherry-pick`, `revert`, `reset` soft/mixed. `reset --hard` stays
             forbidden always.
  marker     `.claude/.rapid-build` holds ONE ISO-8601 UTC expiry
             (`2026-08-13T18:30:00Z`); the gated ops unlock only while that expiry
             is in the future. Absent = the default, safe state. Expired or
             malformed = no session, reported as a marker problem rather than as a
             forbidden op — they are different problems. The developer writes the
             marker; this hook only ever reads it.
  lane check `pull` and `stash push` stop once, by name, when the tree
             holds modified / staged files this session never wrote — probably a
             parallel chat's in-flight work on the shared branch. The developer
             answers in chat and the retry goes through (it asks once per file set).
             "This session wrote it" comes from the ledger that the PostToolUse hook
             `track-touch.py` appends to on every Write / Edit; without that hook
             installed, nothing counts as this session's and the check asks once
             per distinct dirty set. `git add` is deliberately NOT lane-checked —
             it only copies into the index; the commit that follows is the risk.

Mechanism: exit 2 with the reason on stderr — the PreToolUse contract for a block;
the reason is fed back to the agent. Any internal error exits 0: a guard that
crashes must never block unrelated commands.

Parsing: every git/gh invocation in the shell string is scanned (splits on
&& || ; | & ( ), skips `sudo`/`env` prefixes and git's global opts
`-c key=val` / `-C dir`), so `git status; git -c x=y push` cannot slip by.
"""
import hashlib
import json
import os
import re
import shlex
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

# ----------------------------------------------------------------- workspace

WORKSPACE = "wow-two-ws"
DOC = "conventions/development/repo/version-control/git.md -> ## Discipline"
STRICT = False          # True -> no commit / branch / stash-write / history op at all
RAPID_BUILD = True      # True -> history ops unlock during a rapid-building session
LANE_CHECK = True       # True -> pull / stash-push ask about foreign dirt
ALLOWED_HERE = "index-only staging/unstaging, branch create/switch, `git stash`,\n`git pull`, `git fetch`, read-only git + `gh`."
HANDOVER = "Hand it over by name in chat (`push main to origin`, `discard my edits to Program.cs`)\nand STOP; the developer runs it in GitKraken. A subject-only commit message is welcome."

# `<workspace>/.claude/.rapid-build` — this file sits at `<workspace>/.claude/hooks/`.
MARKER = Path(__file__).resolve().parents[1] / ".rapid-build"
MARKER_LABEL = ".claude/.rapid-build"

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

# Worktree destruction — forbidden everywhere, no exemption.
# `restore` is NOT here: `--staged` alone is index-only and safe, so it is
# resolved in git_verdict() where the flags are visible.
WORKTREE_KILL = {"clean"}
RESET_KILL = {"--hard", "--merge", "--keep"}
CHECKOUT_KILL = {"-f", "--force", "--ours", "--theirs"}
SWITCH_KILL = {"-f", "--force", "--discard-changes"}

# Ref / history surgery — not named in the policy text, but the same family as
# the ops it forbids (they rewrite or bypass history). Blocked everywhere.
SURGERY = {
    "filter-branch", "filter-repo", "fast-import", "am", "apply", "rm", "mv",
    "update-ref", "update-index", "checkout-index", "replace", "gc", "prune",
    "subtree", "send-email",
}

# Gated in 10x-ws / wow-two-ws (rapid-building marker), forbidden in eis-ws.
# `pull` is NOT here: it is plainly allowed outside eis-ws, lane check aside.
HISTORY = {"merge", "rebase", "cherry-pick", "revert"}

# Ops that touch the working tree with more than this session's own edits, so they
# ask about foreign dirt first (10x-ws / wow-two-ws only — eis-ws forbids all three).
STASH_PUSH = {"", "push", "save"}

# family -> verbs that WRITE (everything else in the family reads).
WRITE_VERBS = {
    "reflog": {"expire", "delete", "drop", "write"},
    "remote": {"add", "remove", "rm", "rename", "set-url", "set-head", "set-branches",
               "prune", "update"},
    "worktree": {"add", "remove", "move", "prune", "lock", "unlock", "repair"},
    "notes": {"add", "append", "copy", "edit", "remove", "prune", "merge"},
    "submodule": {"add", "init", "deinit", "update", "set-url", "set-branch", "sync",
                  "absorbgitdirs"},
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
EXTRA_GH_BLOCKED = set()
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
    """Yield (binary, subcommand, args) for each `binary ...` call in a shell string."""
    toks = tokenize(cmd)
    out, i, expect_cmd = [], 0, True
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
            if base in binaries:
                j = i + 1
                while j < len(toks):  # skip global options to reach the subcommand
                    a = toks[j]
                    if a in GLOBAL_OPTS_WITH_VALUE:
                        j += 2
                        continue
                    if a.startswith("-"):
                        j += 1
                        continue
                    break
                if j < len(toks):
                    end = j + 1
                    while end < len(toks) and toks[end] not in SEPARATORS:
                        end += 1
                    out.append((base, toks[j].lower(), toks[j + 1:end]))
                else:
                    out.append((base, "", []))
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
# A verdict is (kind, label): kind is "hard" (never allowed here) or "gated"
# (allowed only during a rapid-building session). None means allowed.


def git_verdict(sub, args):
    options = args[:args.index("--")] if "--" in args else args
    flags = {a.split("=", 1)[0] for a in options if a.startswith("-")}
    text = label("git", sub, args)
    hard, gated, lane = ("hard", text), ("gated", text), ("lane", text)

    if sub == "push":
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
    if sub in {"apply", "rm"} and "--cached" in flags and "--index" not in flags:
        return None  # index-only patch/removal; working-tree files stay intact
    if sub in SURGERY:
        return hard
    if sub == "reset":
        if flags & RESET_KILL:
            return hard
        if "--" in args and args.index("--") < len(args) - 1 and not (flags & {"--soft", "--mixed"}):
            return None  # explicit path reset touches only the index
        return hard if STRICT else gated
    if sub == "checkout":
        if "--" in args or "." in args or (flags & CHECKOUT_KILL):
            return hard  # path checkout / forced switch = worktree destruction
        return hard if STRICT else None
    if sub == "switch":
        if flags & SWITCH_KILL:
            return hard
        return hard if STRICT else None
    if sub == "commit":
        return hard  # the developer commits; rapid-building never unlocks this
    if sub == "pull":
        return hard if STRICT else lane  # allowed outside eis-ws, lane check aside
    if sub in HISTORY:
        return hard if STRICT else gated
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
        if flags & CONFIG_WRITE_FLAGS or len(positionals(args, CONFIG_VALUE_FLAGS)) >= 2:
            return hard
        return None
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
    hard = ("hard", label("gh", sub, args))
    if sub == "api":
        method = ""
        for i, a in enumerate(args):
            if a in ("-X", "--method") and i + 1 < len(args):
                method = args[i + 1].upper()
            elif a.startswith("--method="):
                method = a.split("=", 1)[1].upper()
            elif a.startswith("-X") and len(a) > 2:
                method = a[2:].upper()
        if method in GH_API_WRITE_METHODS:
            return hard
        if any(a.split("=", 1)[0] in GH_API_IMPLICIT_POST for a in args):
            return hard  # `-f key=val` turns `gh api` into a POST with no `-X`
        return None
    if (sub, verb) in GH_BLOCKED_PAIRS or (sub, verb) in EXTRA_GH_BLOCKED:
        return hard
    if verb in GH_WRITE_VERBS:
        return hard
    return None


def blocked(cmd):
    """First (kind, label, subcommand, args) that is not plainly allowed."""
    for binary, sub, args in invocations(cmd, {"git", "gh"}):
        verdict = gh_verdict(sub, args) if binary == "gh" else git_verdict(sub, args)
        if verdict:
            return verdict[0], verdict[1], sub, args
    return None


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


# ------------------------------------------------- rapid-building marker

def marker_state():
    """('absent'|'active'|'expired'|'malformed', detail). Read-only — never written."""
    try:
        if MARKER.stat().st_size > 4096:
            return ("malformed", "file is not a single timestamp")
        raw = MARKER.read_text(encoding="utf-8", errors="replace").strip()
    except (FileNotFoundError, NotADirectoryError):
        return ("absent", "")
    except OSError:
        return ("malformed", "unreadable")
    if not raw:
        return ("malformed", "empty file")
    stamp = raw.splitlines()[0].strip()
    try:
        expiry = datetime.fromisoformat(re.sub(r"[Zz]$", "+00:00", stamp))
    except ValueError:
        return ("malformed", '"{}"'.format(stamp[:40]))
    if expiry.tzinfo is None:
        expiry = expiry.replace(tzinfo=timezone.utc)
    if expiry <= datetime.now(timezone.utc):
        return ("expired", stamp)
    return ("active", stamp)


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

def hard_message(op):
    return (
        "BLOCKED — {ws} git policy ({doc}).\n"
        "Operation: `{op}` — Claude never runs it in {ws}, in any session.\n"
        "{handover}\n"
        "Allowed here: {allowed}\n"
        "Approval-shaped questions (\"go ahead\", \"can we push?\") are NOT authorization.\n"
    ).format(ws=WORKSPACE, doc=DOC, op=op, handover=HANDOVER, allowed=ALLOWED_HERE)


def gated_message(op, state, detail):
    if state == "expired":
        why = (
            "Rapid-building marker EXPIRED at {d} (now {n}).\n"
            "The op is not forbidden — the session is over. Ask the developer to extend\n"
            "`{m}` (one ISO-8601 UTC expiry, e.g. 2026-08-13T18:30:00Z), or hand the\n"
            "operation over by name. Claude never writes that marker."
        ).format(d=detail, n=datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                 m=MARKER_LABEL)
    elif state == "malformed":
        why = (
            "Rapid-building marker UNREADABLE — `{m}`: {d}.\n"
            "The op is not forbidden — the marker is broken. It must hold one ISO-8601\n"
            "UTC expiry, e.g. 2026-08-13T18:30:00Z. Ask the developer to fix it, or hand\n"
            "the operation over by name. Claude never writes that marker."
        ).format(m=MARKER_LABEL, d=detail)
    else:
        why = (
            "No rapid-building session: `{m}` is absent — the default, safe state.\n"
            "A rapid-building marker would permit this op; it holds one ISO-8601 UTC\n"
            "expiry (e.g. 2026-08-13T18:30:00Z) and the developer writes it, never Claude.\n"
            "Otherwise hand the operation over by name in chat and stop."
        ).format(m=MARKER_LABEL)
    return (
        "BLOCKED — {ws} git policy ({doc}).\n"
        "Operation: `{op}` — a history op, gated on a rapid-building session.\n"
        "{why}\n"
    ).format(ws=WORKSPACE, doc=DOC, op=op, why=why)


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
        "  no  -> completed-but-uncommitted work; staging is allowed, the developer commits.\n"
        "This asks once per file set: after the answer, re-run the command and it runs.\n"
    ).format(ws=WORKSPACE, doc=DOC, op=op, n=len(strays), fam=family, listing=listing)


# ---------------------------------------------------------------------- main

def main():
    try:
        data = json.loads(sys.stdin.read())
        if data.get("tool_name") != "Bash":
            return 0
        cmd = (data.get("tool_input") or {}).get("command") or ""
        verdict = blocked(cmd)
        if not verdict:
            return 0
        kind, op, sub, args = verdict
        if kind == "hard" or (kind == "gated" and not RAPID_BUILD):
            sys.stderr.write(hard_message(op))
            return 2  # exit 2 -> PreToolUse blocks, stderr is fed back to the agent
        if kind == "gated":
            state, detail = marker_state()
            if state != "active":  # no live rapid-building session
                sys.stderr.write(gated_message(op, state, detail))
                return 2
        family = lane_family(sub, args)
        sdir = session_dir(data.get("session_id"))
        if family and sdir is not None:
            strays = out_of_lane(data.get("cwd") or "", sdir)
            if strays and not already_asked(sdir, family, strays):
                sys.stderr.write(lane_message(op, family, strays))
                return 2
        return 0
    except Exception:
        return 0  # a broken guard must never block unrelated commands


if __name__ == "__main__":
    sys.exit(main())

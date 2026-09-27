#!/usr/bin/env python3
"""Workspace git guard — PreToolUse(Bash) hook, one engine for 10x-ws · eis-ws · mft-10x-ws · wow-two-ws.

Only the CONFIG block differs between workspaces; DOC names the prose policy it enforces.

  allowed    index-only staging/unstaging (`add`, `restore --staged`, path `reset`,
             `apply --cached`, `rm --cached`) · read-only git
             (status log diff show blame describe rev-parse ls-files shortlog
             reflog, `branch --list`, `remote -v`, `stash list|show`) ·
             `git fetch` · read-only gh (`pr view|list|diff|checks|status`,
             `run view|list|watch`, `issue view|list`, `api` GET, `repo view`,
             `auth status`)
  commits    COMMITS decides. "switch": a Claude chat runs exactly
             `git -C <repo> commit -m "subject"` while that repository's commit flag is ON, and
             `git -C <repo> push [-u] [<remote> [<ref>]]` while its push flag is ON. The developer
             flips each with a whole-message `~commit_on <repo>` / `~push_on <repo>`; each flag
             holds for every chat. `.codex/hooks/commit_permission.py` owns both records and
             the ordinary forms, and `commit-switch.py` feeds it Claude prompts.
             "open": a plain commit runs after the lane check. "never": no commit.
             `commit --amend` never runs. A Codex chat meets the switch in its adapter,
             where installed, before this hook.
  forbidden  `git push` outside the switch, and every forcing, deleting or mirror push
             (`--force`, `--force-with-lease`, `+ref`, `:ref`, `--delete`, `--mirror`) and
             push-by-gh · history rewrites (`merge`, `rebase`, `cherry-pick`,
             `revert`, soft/mixed `reset`) · worktree destruction (`reset --hard`,
             `restore` to the worktree, `checkout -- <path>`, `checkout .`, `clean`) ·
             ref surgery · every gh write (`pr create|comment|merge|close|edit|review|ready`,
             `issue create|comment|close|edit`, `release create`,
             `api -X POST|PUT|PATCH|DELETE`, `workflow run`, `repo create|delete`)
  STRICT     also forbids `pull`, branch create / switch, `stash` writes and tag writes;
             otherwise they are allowed (a stash is a real ref and shows in GitKraken).
  lane check `pull`, `stash push` and open commits stop once, by name, when the tree holds
             modified / staged files this session never wrote — probably a parallel chat's
             in-flight work on the shared branch. The developer answers in chat and the retry
             goes through (it asks once per file set). "This session wrote it" comes from the
             ledger that the PostToolUse hook `track-touch.py` appends to on every Write /
             Edit; without that hook installed, nothing counts as this session's.

Mechanism: exit 2 with the reason on stderr — the PreToolUse contract for a block;
the reason is fed back to the agent. An internal error exits 0, because a guard that
crashes must never block unrelated commands — but it never lets a commit or push through.

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

# ------------------------------------------------------------------- CONFIG

WORKSPACE = "wow-two-ws"
DOC = "conventions/development/repo/version-control/git.md -> ## Discipline"
STRICT = False          # True -> no pull / branch / stash-write / tag write either
LANE_CHECK = True       # True -> pull / stash-push ask about foreign dirt
COMMITS = "switch"      # "switch": the repository commit switch · "open": plain commits, lane-checked · "never"
ALLOWED_HERE = "index-only staging/unstaging, branch create/switch, `git stash`,\n`git pull`, `git fetch`, read-only git + `gh`,\nan ordinary commit while the commit flag is ON, an ordinary push while the push flag is ON."
HANDOVER = "Hand it over by name in chat (`push main to origin`, `discard my edits to Program.cs`)\nand STOP; the developer runs it in GitKraken. A subject-only commit message is welcome."

# ------------------------------------------------------------------- engine

# The repository commit switch; this file sits at `<workspace>/.claude/hooks/`.
SWITCH = Path(__file__).resolve().parents[2] / ".codex" / "hooks" / "commit_permission.py"
COMMIT_FORM = 'git -C <repo> commit -m "subject"'
PUSH_FORM = 'git -C <repo> push [-u] [<remote> [<ref>]]'

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

# History rewrites — the developer runs them. `pull` is NOT here: it is allowed
# outside STRICT workspaces, lane check aside.
HISTORY = {"merge", "rebase", "cherry-pick", "revert"}

# Ops that touch the working tree with more than this session's own edits, so they
# ask about foreign dirt first (STRICT workspaces forbid them outright).
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
# A verdict is (kind, label): kind is "hard" (never allowed here) or "lane" (allowed
# after the lane check). None means allowed.


def git_verdict(sub, args):
    options = args[:args.index("--")] if "--" in args else args
    flags = {a.split("=", 1)[0] for a in options if a.startswith("-")}
    text = label("git", sub, args)
    hard, lane = ("hard", text), ("lane", text)

    if sub == "push":
        # An ordinary push under the "switch" passes in main() through the flag; every other form lands here.
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
        return hard
    if sub == "checkout":
        if "--" in args or "." in args or (flags & CHECKOUT_KILL):
            return hard  # path checkout / forced switch = worktree destruction
        return hard if STRICT else None
    if sub == "switch":
        if flags & SWITCH_KILL:
            return hard
        return hard if STRICT else None
    if sub == "commit":
        # "switch" commits pass in main() through the switch; every other form lands here.
        if COMMITS != "open" or STRICT or "--amend" in flags:
            return hard
        return lane
    if sub == "pull":
        return hard if STRICT else lane  # allowed outside eis-ws, lane check aside
    if sub in HISTORY:
        return hard
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


# ------------------------------------------------------------ commit switch

def switch_verdict(data, cmd):
    """(allowed, reason) for an ordinary commit or push from a Claude chat under COMMITS "switch"; None otherwise."""
    sid = data.get("session_id")
    # A Codex adapter applies the switch before delegating here; its session ids start with `codex-`.
    if COMMITS != "switch" or not isinstance(sid, str) or not sid or sid.startswith("codex-"):
        return None
    if not SWITCH.is_file():
        return None  # not installed: every commit form falls through to the hard verdict
    if not any(sub in ("commit", "push") for _, sub, _ in invocations(cmd, {"git"})):
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
        "Operation: `{op}` — Claude never runs it in {ws}, in any session.\n"
        "{commit}"
        "{handover}\n"
        "Allowed here: {allowed}\n"
        "Approval-shaped questions (\"go ahead\", \"can we push?\") are NOT authorization.\n"
    ).format(ws=WORKSPACE, doc=DOC, op=op, commit=commit, handover=HANDOVER, allowed=ALLOWED_HERE)


def switch_message(reason):
    return (
        "BLOCKED — {ws} commit switch ({doc}).\n"
        "{reason}\n"
        "The developer enables a repository with a whole-message `~commit_on <repo>` (commits)\n"
        "or `~push_on <repo>` (pushes) and reads each with `~commit_status` / `~push_status`;\n"
        "a tool call can never change them.\n"
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

def main():
    cmd = ""
    try:
        data = json.loads(sys.stdin.read())
        if data.get("tool_name") != "Bash":
            return 0
        cmd = (data.get("tool_input") or {}).get("command") or ""
        decision = switch_verdict(data, cmd)
        if decision is not None:
            allowed, reason = decision
            if allowed:
                return 0  # the flag is ON; the switch inspected the exact form
            sys.stderr.write(switch_message(reason))
            return 2
        verdict = blocked(cmd)
        if not verdict:
            return 0
        kind, op, sub, args = verdict
        if kind == "hard":
            sys.stderr.write(hard_message(op, sub))
            return 2  # exit 2 -> PreToolUse blocks, stderr is fed back to the agent
        family = lane_family(sub, args)
        sdir = session_dir(data.get("session_id"))
        if family and sdir is not None:
            strays = out_of_lane(data.get("cwd") or "", sdir)
            if strays and not already_asked(sdir, family, strays):
                sys.stderr.write(lane_message(op, family, strays))
                return 2
        return 0
    except Exception:
        # A broken guard must never block unrelated commands, nor let a commit or push through.
        return 2 if re.search(r"\bgit\b[^\n]*\b(commit|push)\b", cmd) else 0


if __name__ == "__main__":
    sys.exit(main())

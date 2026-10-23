#!/usr/bin/env python3
"""Session file-touch ledger — PostToolUse(Write|Edit|MultiEdit|NotebookEdit) hook.

Records which files THIS session edited, so `guard-git.py` can tell its own work
from another lane's. Several chats edit one working tree on one branch here; a
modified or staged file that no chat in this session wrote is probably a parallel
lane's in-flight work, and `git commit` / `git pull` / `git stash push` would sweep
it up. A PreToolUse hook sees only a shell string, so the knowledge has to be
accumulated as the session goes.

Ledger: `${TMPDIR:-/tmp}/claude-git-lane-<session_id>/touched` — one absolute
realpath per line, append-only, deliberately never pruned (a file edited early and
reverted later still belongs to this session). Same `${TMPDIR}` + session-id shape
as `check-style.py`'s verdict file. The OS reclaims it; nothing else does.

Always exits 0 — a bookkeeping hook must never fail a tool call that already ran.
"""
import json
import os
import re
import sys
from pathlib import Path

LEDGER_PREFIX = "claude-git-lane-"


def paths_from(tool_input):
    """Every file path this tool wrote, across the Write / Edit / Notebook shapes."""
    out = []
    for key in ("file_path", "notebook_path"):
        value = tool_input.get(key)
        if isinstance(value, str) and value:
            out.append(value)
    for edit in tool_input.get("edits") or []:  # MultiEdit, if it ever carries its own
        if isinstance(edit, dict) and isinstance(edit.get("file_path"), str):
            out.append(edit["file_path"])
    return out


def main():
    try:
        data = json.loads(sys.stdin.read())
        session_id = str(data.get("session_id") or "")
        if not re.fullmatch(r"[A-Za-z0-9._-]{1,128}", session_id):
            return 0  # no usable id -> no ledger; the guard then asks about everything
        paths = paths_from(data.get("tool_input") or {})
        if not paths:
            return 0
        ledger = Path(os.environ.get("TMPDIR") or "/tmp") / (LEDGER_PREFIX + session_id)
        ledger.mkdir(parents=True, exist_ok=True)
        with (ledger / "touched").open("a", encoding="utf-8") as fh:
            for path in paths:
                fh.write(os.path.realpath(path) + "\n")
    except Exception:
        pass  # bookkeeping only — never surface an error into the session
    return 0


if __name__ == "__main__":
    sys.exit(main())

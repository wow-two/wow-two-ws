#!/usr/bin/env python3
"""Claude Code adapter for the repository commit and push switches — SessionStart and UserPromptSubmit.

`.codex/hooks/commit_permission.py` owns both per-repository flags; this file only feeds it Claude events.
Only a prompt that is exactly `~commit_on|off|status <repo>` or `~push_on|off|status <repo>` can change or
read a flag; every other prompt prints nothing. At session start each ON flag of the working repository is
surfaced. `guard-git.py` reads the same records before a commit or push; each flag is final for every chat.

Claude chats are recorded as `claude-<session_id>` in the change evidence only.
Claude Code sends no turn id, so each genuine prompt event gets a fresh one.
Never exits non-zero: exit 2 from a prompt hook would block AND erase the prompt.
"""
import importlib.util
import json
from pathlib import Path
import sys
import uuid

SWITCH = Path(__file__).resolve().parents[2] / ".codex" / "hooks" / "commit_permission.py"


def load():
    sys.dont_write_bytecode = True
    spec = importlib.util.spec_from_file_location("commit_permission", SWITCH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def handle(payload):
    sid = payload.get("session_id")
    if not isinstance(sid, str) or not sid or not SWITCH.is_file():
        return ""
    session = "claude-" + sid
    event = payload.get("hook_event_name")
    switch = load()
    if event == "SessionStart":
        cwd = payload.get("cwd") or switch.ROOT
        try:
            on = [kind for kind in switch.KINDS if (state := switch.read_state(cwd, kind)) and state["enabled"]]
            return "\n".join(switch.status(cwd, session, kind) for kind in on)
        except (ValueError, OSError, switch.subprocess.SubprocessError):
            return ""  # the working directory is no repository of this workspace
    if event != "UserPromptSubmit" or switch.directive(payload.get("prompt")) is None:
        return ""
    return switch.prompt(dict(payload, session_id=session, turn_id=payload.get("turn_id") or uuid.uuid4().hex))


def main():
    try:
        payload = json.loads(sys.stdin.read() or "{}")
        text = handle(payload) if isinstance(payload, dict) else ""
    except Exception as exc:
        text = "COMMIT SWITCH BROKEN: permission unchanged, no grant recorded: " + type(exc).__name__
    if text:
        print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Stop + UserPromptSubmit hook: mechanical shape check of Claude's own last reply.

Two modes, dispatched on the payload's hook_event_name:

  Stop              -- measure the reply, write a verdict file, print nothing.
  UserPromptSubmit  -- read the verdict file, delete it, print it (stdout on this
                       event is appended to the model's context).

Why advisory and not blocking: a Stop hook can only reach the model by BLOCKING
(decision=block / exit 2), which makes Claude emit a second reply the user also
has to read -- the opposite of what the ruleset is for -- and risks a correction
loop. The verdict instead lands before the next reply is written, which is the
only place a style rule can still change anything.

HARD RULE -- NO USER-FACING PROSE IN THIS FILE.
The injected wording and the per-workspace exemption patterns live in
.claude/hooks/check-style.md. Code comments are fine; message text is not.

HARD RULE -- NEVER EXIT NON-ZERO.
UserPromptSubmit treats exit 2 as "block AND erase the prompt", and Stop treats
exit 2 as "block the stop". An internal bug must never do either. Every failure
path reports a loud stdout line and exits 0.
"""

import json
import os
import re
import sys
import tempfile

CAP = 15            # whitespace-separated words per bullet, status excluded
STREAM_LINES = 15   # streamed-reply line cap as the ruleset states it
STREAM_SLACK = 18   # the ruleset says "~15"; only complain past this
PLAN_MIN, PLAN_MAX = 4, 6
PLAN_LINE_EXEMPT = 3          # <=3-line reply needs no Plan block
STATUSES = ("✅", "\U0001f504", "⬜", "✗")
VERBATIM_RUN = 24             # backtick/quote span this long reads as verbatim
MAX_SHOWN = 3                 # never list more than this many over-cap bullets

HERE = os.path.dirname(os.path.abspath(__file__))
CONFIG = os.path.join(HERE, "check-style.md")

BULLET = re.compile(r"^(\s*)([-*+])\s+(.*)$")
FENCE = re.compile(r"^\s*(```|~~~)")
HEADING = re.compile(r"^\s*#{1,6}\s")
PLAN_HDR = re.compile(r"^\s*#{2,4}\s*Plan\s*$", re.I)
QUEUE_HDR = re.compile(r"^\s*(#{2,4}\s*)?Queue\s*$", re.I)
LONG_RUN = re.compile(
    r"`[^`]{%d,}`|\"[^\"]{%d,}\"|'[^']{%d,}'|“[^”]{%d,}”"
    % (VERBATIM_RUN, VERBATIM_RUN, VERBATIM_RUN, VERBATIM_RUN)
)


# ---------------------------------------------------------------- config

def load_config():
    """Parse check-style.md into {section: [lines]}. Missing file is survivable."""
    sections, key = {}, None
    try:
        with open(CONFIG, encoding="utf-8") as fh:
            for raw in fh:
                line = raw.rstrip("\n")
                m = re.match(r"^##\s+([a-z0-9-]+)\s*$", line)
                if m:
                    key = m.group(1)
                    sections[key] = []
                elif key is not None:
                    sections[key].append(line)
    except OSError:
        return {}
    return {k: [x for x in v if x.strip()] for k, v in sections.items()}


def walkthrough_patterns(cfg):
    out = []
    for pat in cfg.get("walkthrough-markers", []):
        try:
            out.append(re.compile(pat))
        except re.error:
            continue
    return out


# ---------------------------------------------------------------- scanning

def classify(lines):
    """Return per-line flags: in_fence, is_table, is_quote."""
    in_fence = False
    flags = []
    for line in lines:
        if FENCE.match(line):
            flags.append((True, False, False))
            in_fence = not in_fence
            continue
        stripped = line.lstrip()
        flags.append((in_fence, stripped.startswith("|"), stripped.startswith(">")))
    return flags


def bullet_text(line):
    m = BULLET.match(line)
    return m.group(3) if m else None


def exempt_bullet(text):
    """Exemptions from the cap, stated in the ruleset. Bias hard toward silence."""
    if LONG_RUN.search(text):      # verbatim quote / error string / long identifier
        return True
    return False


def over_cap(lines, flags):
    hits = []
    for i, (line, (fence, table, quote)) in enumerate(zip(lines, flags), start=1):
        if fence or table or quote:
            continue
        text = bullet_text(line)
        if text is None:
            continue
        text = text.rstrip()
        words = text.split()
        if words and words[0] in STATUSES:
            words = words[1:]
        if len(words) <= CAP or exempt_bullet(text):
            continue
        hits.append((i, len(words), text))
    return hits


def plan_block(lines, flags):
    """Return (start_index, bullet_texts) for the ### Plan block, or (None, [])."""
    start = None
    for i, (line, (fence, _t, _q)) in enumerate(zip(lines, flags)):
        if fence:
            continue
        if PLAN_HDR.match(line):
            start = i
            break
    if start is None:
        return None, []
    bullets = []
    for line in lines[start + 1:]:
        if HEADING.match(line) or line.strip().startswith("---"):
            break
        text = bullet_text(line)
        if text is not None:
            bullets.append(text.rstrip())
    return start, bullets


def has_queue(lines, flags):
    for line, (fence, _t, _q) in zip(lines, flags):
        if not fence and QUEUE_HDR.match(line):
            return True
    return False


def unbulleted_lines(lines, flags):
    """Find chat text outside bullets or approved structural Markdown."""
    hits = []
    for i, (line, (fence, table, quote)) in enumerate(zip(lines, flags), start=1):
        stripped = line.strip()
        if (not stripped or fence or table or quote or HEADING.match(line)
                or bullet_text(line) is not None or stripped.startswith('---')
                or stripped.startswith('::')):
            continue
        hits.append((i, stripped))
    return hits


# ---------------------------------------------------------------- verdict

def measure(reply, cfg):
    lines = reply.split("\n")
    flags = classify(lines)
    nonblank = [l for l, (f, _t, _q) in zip(lines, flags) if l.strip() and not f]
    # A table row is denser than the bullets it replaces, and a `---` rule is free.
    # Counting either against the reading-cost cap punishes the sanctioned format.
    readable = [l for l, (f, t, _q) in zip(lines, flags)
                if l.strip() and not f and not t and not l.strip().startswith("---")]

    queued = has_queue(lines, flags)
    walkthrough = any(p.search(reply) for p in walkthrough_patterns(cfg))

    findings = []

    # A walkthrough turn is exempt from the bullet cap and the line cap by name,
    # "on the same ground as a deliverable". Skip the shape checks, keep the
    # structural ones -- those the ruleset never exempts.
    hits = [] if walkthrough else over_cap(lines, flags)
    if hits:
        detail = ["  L%d  %d words  %s" % (i, n, t[:120] + "…" if len(t) > 120 else t)
                  for i, n, t in hits[:MAX_SHOWN]]
        more = "" if len(hits) <= MAX_SHOWN else "  (+%d more)" % (len(hits) - MAX_SHOWN)
        findings.append("bullet cap %d words: %d bullet(s) over" % (CAP, len(hits)))
        findings.extend(detail)
        if more:
            findings.append(more)

    start, plan_bullets = plan_block(lines, flags)
    if start is None:
        # A `### Queue` may stand in for `### Plan` on a point-surfacing turn.
        if len(nonblank) > PLAN_LINE_EXEMPT and not queued:
            findings.append("`### Plan` block: missing (reply is %d lines)" % len(nonblank))
    else:
        if not (PLAN_MIN <= len(plan_bullets) <= PLAN_MAX):
            findings.append("`### Plan`: %d bullets (rule: %d-%d)"
                            % (len(plan_bullets), PLAN_MIN, PLAN_MAX))
        bad = [b for b in plan_bullets if not b.lstrip().startswith(STATUSES)]
        if bad:
            findings.append("`### Plan`: %d bullet(s) carry no status from %s"
                            % (len(bad), " ".join(STATUSES)))

    if queued and not walkthrough and len(readable) > STREAM_SLACK:
        findings.append("streamed reply: %d lines, tables and fences already excluded (cap ~%d)"
                        % (len(readable), STREAM_LINES))

    plain = unbulleted_lines(lines, flags)
    if plain and not walkthrough:
        findings.append("chat text outside bullets at line(s): %s" %
                        ', '.join(str(i) for i, _ in plain[:MAX_SHOWN]))

    return findings


# ---------------------------------------------------------------- transcript

def reply_from_transcript(path):
    """Fallback when last_assistant_message is absent. Skips subagent sidechains."""
    try:
        with open(path, encoding="utf-8", errors="replace") as fh:
            rows = fh.readlines()
    except OSError:
        return ""
    for raw in reversed(rows[-400:]):
        raw = raw.strip()
        if not raw:
            continue
        try:
            row = json.loads(raw)
        except ValueError:
            continue
        # A JSONL line can legally parse to a bare string / list / number when the
        # path is not a transcript at all. Only a dict is a transcript row.
        if not isinstance(row, dict):
            continue
        if row.get("type") != "assistant" or row.get("isSidechain"):
            continue
        message = row.get("message")
        blocks = message.get("content") if isinstance(message, dict) else None
        if not isinstance(blocks, list):
            continue
        text = "".join(b.get("text", "") for b in blocks
                       if isinstance(b, dict) and b.get("type") == "text")
        if text.strip():
            return text
    return ""


def verdict_path(session_id):
    return os.path.join(tempfile.gettempdir(), "claude-style-verdict-%s" % session_id)


# ---------------------------------------------------------------- modes

def do_stop(payload, cfg):
    if payload.get("stop_hook_active"):
        return   # another Stop hook is already driving a correction; do not pile on
    reply = payload.get("last_assistant_message")
    reply = reply if isinstance(reply, str) else ""
    if not reply.strip():
        reply = reply_from_transcript(payload.get("transcript_path") or "")
    if not reply.strip():
        return
    findings = measure(reply, cfg)
    path = verdict_path(payload.get("session_id") or "global")
    if not findings:
        try:
            os.remove(path)
        except OSError:
            pass
        return
    try:
        with open(path, "w", encoding="utf-8") as fh:
            fh.write("\n".join(findings))
    except OSError:
        print("STYLE CHECK BROKEN: cannot write %s -- shape check OFF this turn." % path)


def do_prompt(payload, cfg):
    path = verdict_path(payload.get("session_id") or "global")
    try:
        with open(path, encoding="utf-8") as fh:
            body = fh.read().strip()
    except OSError:
        return
    try:
        os.remove(path)
    except OSError:
        pass
    if not body:
        return
    header = cfg.get("header", [])
    footer = cfg.get("footer", [])
    if not header:
        print("STYLE CHECK BROKEN: no header in %s -- emitting bare findings." % CONFIG)
    for line in header:
        print(line)
    print(body)
    for line in footer:
        print(line)


def main():
    try:
        raw = sys.stdin.read()
    except Exception:
        raw = ""
    if not raw.strip():
        return
    try:
        payload = json.loads(raw)
    except ValueError:
        print("STYLE CHECK BROKEN: hook payload is not JSON -- shape check OFF this turn.")
        return
    if not isinstance(payload, dict):
        print("STYLE CHECK BROKEN: hook payload is not an object -- shape check OFF this turn.")
        return
    cfg = load_config()
    event = payload.get("hook_event_name")
    if event == "Stop":
        do_stop(payload, cfg)
    elif event == "UserPromptSubmit":
        do_prompt(payload, cfg)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:   # noqa: BLE001 -- a bug here must never wedge a session
        print("STYLE CHECK BROKEN: %s: %s -- shape check OFF this turn."
              % (type(exc).__name__, exc))
    sys.exit(0)

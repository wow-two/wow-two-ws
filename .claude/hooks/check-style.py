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
LINE_TARGET = 15    # per-reply aim from the ruleset's `Length` section
LINE_CAP = 20       # hard cap; only complain past this
PLAN_MIN, PLAN_MAX = 4, 6
STATUSES = ("✅", "\U0001f504", "⬜", "✗")
VERBATIM_RUN = 24             # backtick/quote span this long reads as verbatim
MAX_SHOWN = 3                 # never list more than this many over-cap bullets

HERE = os.path.dirname(os.path.abspath(__file__))
CONFIG = os.path.join(HERE, "check-style.md")

BULLET = re.compile(r"^(\s*)([-*+])\s+(.*)$")
FENCE = re.compile(r"^\s*(```|~~~)")
HEADING = re.compile(r"^\s*#{1,6}\s")
PLAN_HDR = re.compile(r"^\s*#{2,4}\s*Plan\s*$", re.I)
QUEUE_HDR = re.compile(r"^\s*#{2,4}\s*Queue\s*$", re.I)
COUNTER = re.compile(r"^(\d+) / (\d+)(?: \(\+\d+\))? from \S")
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


def over_cap(lines, flags, skip=()):
    hits = []
    for i, (line, (fence, table, quote)) in enumerate(zip(lines, flags), start=1):
        if fence or table or quote or (i - 1) in skip:
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


def heading_block(lines, flags, header):
    """Return (start, end, [(index, bullet_text)]) for a `### X` block, or (None, None, []).

    The block runs from its header to the next heading or `---` rule; `end` is the
    index of that boundary, or len(lines) when the block closes the reply.
    """
    start = None
    for i, (line, (fence, _t, _q)) in enumerate(zip(lines, flags)):
        if fence:
            continue
        if header.match(line):
            start = i
            break
    if start is None:
        return None, None, []
    bullets, end = [], len(lines)
    for i in range(start + 1, len(lines)):
        line = lines[i]
        if HEADING.match(line) or line.strip().startswith("---"):
            end = i
            break
        text = bullet_text(line)
        if text is not None:
            bullets.append((i, text.rstrip()))
    return start, end, bullets


def plan_block(lines, flags):
    """Return (start_index, bullet_texts) for the ### Plan block, or (None, [])."""
    start, _end, bullets = heading_block(lines, flags, PLAN_HDR)
    return start, [t for _i, t in bullets]


def queue_findings(lines, flags):
    """Shape of a rendered ### Queue block, plus the line indices its counters occupy.

    Its absence is never a finding: whether points are held is invisible here.
    """
    start, end, bullets = heading_block(lines, flags, QUEUE_HDR)
    if start is None:
        return [], set()
    findings = []
    if not bullets:
        findings.append("`### Queue`: empty block (rule: render only while points are held)")
    counters = [(i, COUNTER.match(t)) for i, t in bullets]
    bad = [i for i, m in counters if m is None]
    if bad:
        findings.append("`### Queue`: %d line(s) not `{remaining} / {total} from {pool}`" % len(bad))
    if any(m and m.group(1) == "0" for _i, m in counters):
        findings.append("`### Queue`: a pool at 0 rendered (rule: drop it the turn it empties)")
    before = [l for l in lines[:start] if l.strip()]
    if before:
        findings.append("`### Queue`: not the reply's first block (%d line(s) precede it)" % len(before))
    # On a `-plan` turn the Plan block sits between the Queue and the rule.
    if end < len(lines) and PLAN_HDR.match(lines[end]):
        _s, end, _b = heading_block(lines, flags, PLAN_HDR)
    rest = [l for l in lines[end:] if l.strip()]
    if rest and not rest[0].strip().startswith("---"):
        findings.append("`### Queue`: no `---` rule between it and the body")
    return findings, {i for i, m in counters if m is not None}


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
    # A table row is denser than the bullets it replaces, and a `---` rule is free.
    # Counting either against the reading-cost cap punishes the sanctioned format.
    readable = [l for l, (f, t, _q) in zip(lines, flags)
                if l.strip() and not f and not t and not l.strip().startswith("---")]

    walkthrough = any(p.search(reply) for p in walkthrough_patterns(cfg))

    findings = []

    # A counter line is a fixed format, exempt from the word cap like a table cell.
    queue, counters = queue_findings(lines, flags)

    # A walkthrough turn is exempt from the bullet cap and the line cap by name,
    # "on the same ground as a deliverable". Skip the shape checks, keep the
    # structural ones -- those the ruleset never exempts.
    hits = [] if walkthrough else over_cap(lines, flags, counters)
    if hits:
        detail = ["  L%d  %d words  %s" % (i, n, t[:120] + "…" if len(t) > 120 else t)
                  for i, n, t in hits[:MAX_SHOWN]]
        more = "" if len(hits) <= MAX_SHOWN else "  (+%d more)" % (len(hits) - MAX_SHOWN)
        findings.append("bullet cap %d words: %d bullet(s) over" % (CAP, len(hits)))
        findings.extend(detail)
        if more:
            findings.append(more)

    # Plan is hidden by default and rendered only on an asked turn, so its absence
    # is never a finding; a rendered block is still held to its shape.
    start, plan_bullets = plan_block(lines, flags)
    if start is not None:
        if not (PLAN_MIN <= len(plan_bullets) <= PLAN_MAX):
            findings.append("`### Plan`: %d bullets (rule: %d-%d)"
                            % (len(plan_bullets), PLAN_MIN, PLAN_MAX))
        bad = [b for b in plan_bullets if not b.lstrip().startswith(STATUSES)]
        if bad:
            findings.append("`### Plan`: %d bullet(s) carry no status from %s"
                            % (len(bad), " ".join(STATUSES)))

    findings.extend(queue)

    if not walkthrough and len(readable) > LINE_CAP:
        findings.append("reply length: %d lines, tables and fences already excluded (aim %d, cap %d)"
                        % (len(readable), LINE_TARGET, LINE_CAP))

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

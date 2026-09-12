#!/bin/bash
# UserPromptSubmit tail hook: expands chat markers found in the prompt into rule text.
#
# Called by style-recharge.sh with the raw hook payload on stdin, AFTER the style pulse,
# so marker text lands last in the injected block and outranks the rules it overrides.
# One script chain, never a second settings.json entry -- matching hooks run in parallel
# with nondeterministic order, and ordering here is load-bearing.
#
# HARD RULE -- NO PROSE IN THIS FILE.
# Every injected word lives in .claude/hooks/marker-rules.md; this script only selects.
# The vocabulary IS the set of `## @@name` headers in that file. `## BANNER` and
# `## UNKNOWN` are reserved sections holding the remaining prose. The token shape is
# data too -- the `<!-- marker-shape: ... -->` comment near the top of the same file.
#
# Payload field: `prompt` (verified in the claude binary; a docs source claiming
# `user_input` is wrong). When the field is absent the whole raw payload is scanned
# instead, so a future rename degrades to over-matching rather than to silence.
#
# Never exit non-zero: UserPromptSubmit treats exit 2 as "block AND erase the prompt".
# Every failure path prints a loud stdout line and still exits 0.

rules="${CLAUDE_MARKER_RULES:-.claude/hooks/marker-rules.md}"

# Drain stdin FIRST, before any early return: exiting while the parent is still writing
# the payload down the pipe hands it EPIPE, and a signalled parent is exactly the
# non-zero status this hook must never produce.
payload=$(cat)

if [ ! -f "$rules" ]; then
  printf 'MARKER HOOK BROKEN: no "%s" under "%s" -- chat markers OFF this turn.\n' "$rules" "$PWD"
  exit 0
fi

[ -n "$payload" ] || exit 0

tmp=$(mktemp "${TMPDIR:-/tmp}/claude-marker-XXXXXX" 2>/dev/null) || {
  printf 'MARKER HOOK BROKEN: mktemp failed -- chat markers OFF this turn.\n'
  exit 0
}
trap 'rm -f "$tmp" 2>/dev/null' EXIT
printf '%s' "$payload" > "$tmp" 2>/dev/null || {
  printf 'MARKER HOOK BROKEN: cannot buffer the payload -- chat markers OFF this turn.\n'
  exit 0
}

out=$(awk '
function shapeval(s, key,   re, m) {
  re = key "=\"[^\"]*\""
  if (match(s, re)) {
    m = substr(s, RSTART, RLENGTH)
    sub(key "=\"", "", m)
    sub(/"$/, "", m)
    return m
  }
  return ""
}
function trimblank(t) {
  sub(/^\n+/, "", t)
  sub(/\n+$/, "", t)
  return t
}
function jsonstr(s, key,   n, i, j, q, c, d, out, start) {
  n = length(s)
  start = 1
  while (1) {
    q = index(substr(s, start), "\"" key "\"")
    if (q == 0) return ""
    i = start + q - 1 + length(key) + 2
    while (i <= n && substr(s, i, 1) ~ /^[ \t\n\r]$/) i++
    if (substr(s, i, 1) != ":") { start = start + q; continue }
    i++
    while (i <= n && substr(s, i, 1) ~ /^[ \t\n\r]$/) i++
    if (substr(s, i, 1) != "\"") { start = start + q; continue }
    i++
    break
  }
  out = ""
  while (i <= n) {
    c = substr(s, i, 1)
    if (c == "\\") {
      d = substr(s, i + 1, 1)
      if (d == "n") out = out "\n"
      else if (d == "t") out = out "\t"
      else if (d == "r") out = out "\r"
      else if (d == "u") { out = out " "; i += 4 }
      else if (d == "b" || d == "f") out = out " "
      else out = out d
      i += 2
      continue
    }
    if (c == "\"") return out
    out = out c
    i++
  }
  return out
}
function stripfences(t,   m, i, arr, ln, tr, inf, inm, res) {
  # Strips every region a marker must NOT be read from, so only text the human
  # typed this turn can arm a marker. Machine-inserted text reaches the `prompt`
  # field too -- a subagent report, a system reminder, a task notification -- and
  # a marker fired from there changes assistant behaviour with nobody
  # having asked. Bias is one-directional on purpose: a marker that fails to fire
  # costs one retype, while a marker fired from injected text is silent and wrong.
  m = split(t, arr, "\n")
  inf = 0   # inside a fenced code block
  inm = 0   # inside a machine-inserted block
  res = ""
  for (i = 1; i <= m; i++) {
    ln = arr[i]
    tr = ln
    sub(/^[ \t]+/, "", tr)
    if (tr ~ /^(```|~~~)/) { inf = 1 - inf; continue }
    if (inf == 1) continue
    # machine-inserted wrappers: <system-reminder>, <task-notification>,
    # <*-notification>, <cross-session-message ...>, <function_results> ...
    if (tr ~ /^<\/?(system-reminder|[a-z-]*notification|cross-session-message|function_(calls|results)|persisted-output)[ >\/]/ || tr ~ /^<\/?(system-reminder|[a-z-]*notification|cross-session-message|function_(calls|results)|persisted-output)>/) {
      if (tr ~ /^<\//) { inm = 0 } else { inm = 1 }
      continue
    }
    if (inm == 1) continue
    if (tr ~ /^>/) continue                 # quoted / pasted material
    gsub(/`[^`]*`/, " ", ln)                # inline code spans
    res = res ln "\n"
  }
  return res
}
BEGIN { sec = ""; nsec = 0; nrank = 0; nk = 0; nu = 0 }

FNR == NR {
  if (shape == "" && $0 ~ /<!--[ \t]*marker-shape:/) { shape = $0; next }
  if ($0 ~ /^##[ \t]+/) {
    h = $0
    sub(/^##[ \t]+/, "", h)
    sub(/[ \t]+$/, "", h)
    if (h == "BANNER")  { sec = "BANNER";  next }
    if (h == "UNKNOWN") { sec = "UNKNOWN"; next }
    if (h ~ /^@@/) {
      sub(/^@@/, "", h)
      sec = "@" h
      rank[++nrank] = h
      known[h] = 1
      next
    }
    sec = ""
    next
  }
  if (sec != "") body[sec] = body[sec] $0 "\n"
  next
}

{ raw = raw $0 "\n" }

END {
  sigil    = shapeval(shape, "sigil")
  run      = shapeval(shape, "run")
  wordre   = shapeval(shape, "word")
  beforenot = shapeval(shape, "before-not")
  if (sigil == "" || run == "" || wordre == "") {
    printf "MARKER HOOK BROKEN: no usable <!-- marker-shape: --> in the rules file -- chat markers OFF this turn.\n"
    exit 0
  }
  if (nrank == 0) {
    printf "MARKER HOOK BROKEN: the rules file declares no ## @@marker sections -- chat markers OFF this turn.\n"
    exit 0
  }

  text = jsonstr(raw, "prompt")
  if (text == "") {
    text = raw
    gsub(/\\n/, "\n", text)
  }
  text = stripfences(text)

  n = length(text)
  for (i = 1; i <= n; i++) {
    if (substr(text, i, 1) != sigil) continue
    if (i > 1 && beforenot != "" && substr(text, i - 1, 1) ~ ("^" beforenot "$")) continue
    j = i + 1
    w = ""
    while (j <= n && substr(text, j, 1) ~ ("^" run "$")) { w = w substr(text, j, 1); j++ }
    i = j - 1
    if (w == "") continue
    if (w !~ wordre) continue
    if (known[w] == 1) {
      if (seenk[w] != 1) { seenk[w] = 1; nk++ }
    } else {
      if (seenu[w] != 1) { seenu[w] = 1; nu++; ulist[++nu2] = w }
    }
  }

  if (nk == 0 && nu == 0) exit 0

  if (body["BANNER"] != "") print trimblank(body["BANNER"]) "\n"
  for (r = 1; r <= nrank; r++) {
    name = rank[r]
    if (seenk[name] == 1 && body["@" name] != "") print trimblank(body["@" name]) "\n"
  }
  if (nu > 0) {
    if (body["UNKNOWN"] != "") print trimblank(body["UNKNOWN"])
    for (u = 1; u <= nu2; u++) printf "  %s%s\n", sigil, ulist[u]
    printf "\n"
  }
  exit 0
}
' "$rules" "$tmp" 2>/dev/null) || {
  printf 'MARKER HOOK BROKEN: the marker scan failed -- chat markers OFF this turn.\n'
  exit 0
}

[ -n "$out" ] && printf '%s\n' "$out"

exit 0

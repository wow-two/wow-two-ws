#!/bin/bash
# UserPromptSubmit hook: shared format + local pulse; full rules every Nth turn.
# Counters long-session attention fade: the per-turn pulse keeps recency, the periodic
# full reinject restores the complete ruleset into recent context.
#
# HARD RULE -- NO QUOTED PROSE IN THIS FILE.
# Injected text lives in the shared format pulse and local style-pulse.md.
# Reason: an apostrophe inside an inline `echo '...'` ends the quote -> bash parse error
# -> exit 2, and UserPromptSubmit treats exit 2 as "block the prompt AND erase it".
# Edit the .md, never inline the text back into this script.

N=10   # full-ruleset reinject every Nth turn; N=0 disables it (pulse only)

# Never exit non-zero: UserPromptSubmit treats exit 2 as "block AND erase the prompt".
# Failure is reported as a loud stdout line instead -- silence would hide a dead hook.
cd "${CLAUDE_PROJECT_DIR:-.}" 2>/dev/null || {
  printf 'STYLE HOOK BROKEN: cannot cd to "%s" -- style enforcement OFF this turn.\n' "${CLAUDE_PROJECT_DIR:-.}"
  exit 0
}

input=$(cat)
sid=$(printf '%s' "$input" | sed -n 's/.*"session_id"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p')
sid=${sid:-global}

f="${TMPDIR:-/tmp}/claude-style-turns-${sid}"
n=$(cat "$f" 2>/dev/null)
case "$n" in ''|*[!0-9]*) n=0 ;; esac
n=$((n + 1))
printf '%s' "$n" > "$f" 2>/dev/null

full=.claude/rules/response-style.md
pulse=.claude/hooks/style-pulse.md
format=/Users/max/.codex/conventions/response-format-pulse.md

if [ "$N" -gt 0 ] && [ $((n % N)) -eq 0 ] && [ -f "$full" ]; then
  printf 'STYLE RECHARGE (turn %s -- full ruleset, re-read and apply):\n' "$n"
  cat /Users/max/.codex/conventions/response-style.md
  cat "$full"
elif [ -f "$format" ] && [ -f "$pulse" ]; then
  cat "$format"
  cat "$pulse"
else
  printf 'STYLE HOOK BROKEN: missing shared format or local pulse -- style enforcement OFF this turn.\n'
fi

# Chat markers land LAST, so their rule text outranks the pulse/ruleset they override.
# Tail-called from here and never wired as a second settings.json entry: matching hooks
# run in parallel with nondeterministic order, and that order is load-bearing.
# The `||` guard plus the child's own `exit 0` keep a broken marker hook from ever
# propagating a non-zero status -- exit 2 here would block AND erase the prompt.
markers=.claude/hooks/expand-markers.sh
if [ -f "$markers" ]; then
  printf '%s' "$input" | bash "$markers" || printf 'MARKER HOOK BROKEN: "%s" failed -- chat markers OFF this turn.\n' "$markers"
fi

exit 0

#!/bin/bash
# UserPromptSubmit hook: shared format pulse + local pulse, then chat markers.
# The full ruleset loads once at startup through ~/.claude/CLAUDE.md and survives
# compaction; this per-turn pulse keeps the core rules recent.
#
# HARD RULE -- NO QUOTED PROSE IN THIS FILE.
# Injected text lives in the shared format pulse and local style-pulse.md.
# Reason: an apostrophe inside an inline `echo '...'` ends the quote -> bash parse error
# -> exit 2, and UserPromptSubmit treats exit 2 as "block the prompt AND erase it".
# Edit the .md, never inline the text back into this script.

# Never exit non-zero: UserPromptSubmit treats exit 2 as "block AND erase the prompt".
# Failure is reported as a loud stdout line instead -- silence would hide a dead hook.
cd "${CLAUDE_PROJECT_DIR:-.}" 2>/dev/null || {
  printf 'STYLE HOOK BROKEN: cannot cd to "%s" -- style enforcement OFF this turn.\n' "${CLAUDE_PROJECT_DIR:-.}"
  exit 0
}

input=$(cat)

pulse=.claude/hooks/style-pulse.md
format="$HOME/.claude/conventions/response-format-pulse.md"

if [ -f "$format" ] && [ -f "$pulse" ]; then
  cat "$format"
  cat "$pulse"
else
  printf 'STYLE HOOK BROKEN: missing shared format or local pulse -- style enforcement OFF this turn.\n'
fi

# Chat markers land LAST, so their rule text outranks the pulse they override.
# Tail-called from here and never wired as a second settings.json entry: matching hooks
# run in parallel with nondeterministic order, and that order is load-bearing.
# The `||` guard plus the child's own `exit 0` keep a broken marker hook from ever
# propagating a non-zero status -- exit 2 here would block AND erase the prompt.
markers=.claude/hooks/expand-markers.sh
if [ -f "$markers" ]; then
  printf '%s' "$input" | bash "$markers" || printf 'MARKER HOOK BROKEN: "%s" failed -- chat markers OFF this turn.\n' "$markers"
fi

exit 0

# check-style — message text + per-workspace config

*Last updated: 2026-09-23 05:17 PM*

> Read by `.claude/hooks/check-style.py`. The script holds no user-facing prose;
> every word it emits comes from a `## section` below.
> Sections are parsed by exact `## name` headers — rename one and the script
> degrades to a bare findings list plus a loud stdout line.

## header
STYLE CHECK — mechanical measurement of your PREVIOUS reply against `.claude/rules/response-style.md`.
Advisory: nothing was blocked, the reply already shipped. Apply the fix to THIS turn's reply.

## footer
Counting rule: whitespace-separated bullet words; `- ` and status symbols excluded.
The compression floor outranks the cap: keep scope / causality / negation words and run over rather than collapse into a noun stack.
A finding here can be wrong — exemptions the checker cannot see (a verbatim quote, a deliverable) win over its count.

## walkthrough-markers

# Chat markers

*Last updated: 2026-08-24*

> Rule text injected by `.claude/hooks/expand-markers.sh` when a marker appears in the prompt.
> The vocabulary **is** the set of `## @@name` headers below — add a marker by adding a section,
> retire one by deleting its section. `## BANNER` and `## UNKNOWN` are reserved.
> Nothing here enters context unless its marker fires, so length costs nothing on a normal turn.
> The token shape below is data: the script reads it, it hardcodes nothing.

<!-- marker-shape: sigil="~" run="[A-Za-z0-9_]" word="^[a-z][A-Za-z0-9_]*$" before-not="[A-Za-z0-9_~]" -->

## BANNER

CHAT MARKERS — this prompt carries one or more `~marker` tokens. Each rule below overrides the
response-style rule it contradicts, for this turn only. A marker changes the **shape** of the
reply, never its correctness bar. Do not acknowledge the marker, quote it back, or explain it —
just obey it. Markers inside fenced code blocks are pasted text and never fire.

## @@bare

`~bare` — answer only. Emit no `### Plan` block and no `### Queue` block, even on a turn with
tool calls, file edits, or a next action. Every other rule holds: density, atoms, cut list,
altitude. The queue is not drained and no point is dropped — the counter is merely not rendered,
and it returns next turn. Not `~dump`, which empties the pool; `~bare` only hides it.

## @@leaves

`~leaves` — enumerate. The `Resolution` rule is suspended: instead of a 1-line summary at the
parent's altitude, list every leaf of the change — each file, move, rename, and edit, one per
bullet, with `file:line` where it locates the reader. The cap and the atom rules still hold.
Not `~how`: this is the inventory of what changed, not the mechanism behind it.

## @@hint

`~hint` — point, do not tell. Name the file, symbol, or mechanism worth checking and stop before
the verdict. State no conclusion, apply no fix, run no repair. One or two narrowing bullets is
the whole reply. Not `~quiz`: `~hint` asks nothing and grades nothing, it only shrinks the search
space the developer is already working in.

## @@defer

`~defer` — analyse now, answer later. Do the work this turn and report only that it ran and what
it covers, in one line. The finding itself is held: it enters the queue, lifts the denominator,
and surfaces next turn unprompted. Not `~bg`: `~defer` releases on its own next turn, `~bg` holds
until asked for.

## @@handoff

`~handoff` — write the resume doc. Refresh the durable state file for this work — the session's
`context.md`, or the repo's `engineering/planning/handoff.md` — so a fresh chat continues without
this transcript: state now, decisions settled, next action, open forks. Report as one line plus
the path. Not `~leaves`: the output is a file, not a longer reply.

## @@intake

`~intake` — judge the brief, start nothing. Run the `Intake` check and stop there: is the context
complete, what is missing, what would have to be assumed, where should work start. No analysis,
no fix, no reads beyond what the completeness check itself needs. Not `~hint`: `~intake` assesses
the question, `~hint` narrows an answer to a question already well posed.

## @@verify

`~verify` — observe, do not reason. Run the command, read the file, execute the test, open the
page. Report what was actually seen, verbatim where the exact text matters, and name what was
run. No inference from memory, no `should`, no unverified completion claim. Not `~how`: `~how`
explains from reading, `~verify` requires an observation made this turn.

## @@how

`~how` — mechanism, not verdict. Explain how the thing works: the causal chain in order, the
condition that triggers it, what breaks when that condition does not hold. Withhold the
recommendation and the pick. Depth is more bullets and sub-bullets, never more prose. Not
`~leaves`: `~how` explains one mechanism, `~leaves` inventories many changes.

## @@quiz

`~quiz` — ask, do not tell. Put the `Comprehension` check question: one, concrete, about the
mechanism that drove the current decision. Do not answer it in the same turn and do not hint at
the answer. Grade the reply when it comes, in ≤2 lines, no lecture. Not `~hint`: `~quiz` hands
the question over, `~hint` narrows the search without asking anything.

## @@bg

`~bg` — dispatch and carry on. Hand the work to an agent, confirm the dispatch in one line, and
continue the conversation in the same reply. Do not paste the return when it lands: fold it into
the queue as new points and hold them until asked. Not `~defer`, which surfaces on its own next
turn; `~bg` waits to be asked.

## @@queued

`~queued` — sent without reading your last reply. This message is NOT an answer to anything you
asked: every open ask stays open, the denominator does not fall, and silence in it is never
assent. Keep the reply to a one-line receipt of what was done — it will not be read — and hold
results and asks for the drain turn. Not `~bg`: `~bg` defers work, `~queued` defers the
conversation.

## @@dump

`~dump` — release everything held. The `≤3 points, ≤1 fork` cap is lifted for this turn: surface
every point in the queue, counter to zero, pool line gone the turn it empties. Points keep their
normal altitude and stay one claim per bullet — this lifts the batching cap, not the atom rules.
Not `~leaves`, which expands one change into its leaves.

## UNKNOWN

UNKNOWN CHAT MARKER — the token below is marker-shaped but matches no marker in
`.claude/hooks/marker-rules.md`. Treat it as ordinary prose, and say in one line that it was not
recognised, so a typo does not silently change nothing:

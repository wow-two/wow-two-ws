# Diagram Conventions — Excalidraw

*Last updated: 2026-08-12*

> How to author `.excalidraw` diagrams that ship next to a doc. The visual analog of [`response-style.md`](../../../.claude/rules/response-style.md): same density rules, same identifier rules, applied to boxes and labels.

`.excalidraw` is plain JSON, so a diagram is generated, reviewed and diffed like any other artefact. **Generate it from a script, never draw it by hand** — the layout stays reproducible and a later edit is a re-run, not a redraw.

---

## Fonts — one per element, chosen by content

| Content | `fontFamily` | Excalidraw button |
|---|---|---|
| identifiers — file, symbol, config key, endpoint, column | `3` | `</>` |
| prose — labels, explanations, captions | `2` | `A` |
| never | `1` | pencil (hand-drawn) |

- must not use `fontFamily: 1` — the hand-drawn face reads as a sketch, not a reference
- must not mix content kinds inside one text element — split the identifier into a note beside the box
- must use `fontFamily: 3` for anything a reader would backtick in markdown — the same test as the style rule

---

## Font size — four buttons, nothing between

Excalidraw's own size buttons. A raw number that is not one of these renders at a size no one can reproduce by clicking.

| Role | `fontSize` | Button |
|---|---|---|
| diagram title | `36` | `XL` |
| section header inside the diagram | `28` | `L` |
| **normal text** — box labels, notes, subtitles | `20` | `M` |
| caption — arrow labels, footnotes, verdict lines | `16` | `S` |

- must use one of `36` / `28` / `20` / `16` and nothing else
- must set **normal text at `M`** — the floor for anything a reader is meant to read
- must reserve `S` for text annotating other text — an arrow's label, a footnote
- should name the sizes in the generator (`XL, L, M, S = 36, 28, 20, 16`) so a call site reads `size=M`
- must scale layout with the type: a bound label centres at `y + h/2 - size/2`, a two-line note needs `~1.35 × size`

---

## Box size — one height, everywhere

- must give every box the **same height: `90`** — mixed heights read as a hierarchy the diagram does not have
- **entity cards are the one exemption.** A box whose job is to carry a field list — a record shape, a
  table, a message contract — is an *entity card*: it holds a title line and its fields, and its height
  follows its field count. A diagram mixes the two kinds freely, but every card in one diagram uses the
  same width and the same per-field pitch, so the varying height reads as "more fields", never as rank.
  Step boxes in the same diagram stay at `90`.
- must size width to the longest label at `M`, in steps, not per box — `420` for a step in a chain, wider for a lane
- must keep `90` even for a box holding one word; the whitespace is the point
- should define it once in the generator (`BOX_H = 90`) and never pass a literal height
- **why 90** — an `M` label centred in `90` leaves ~35 px of air, which survives 3× export and a zoom-to-fit

Constants that follow: ~`54` px of gap between stacked boxes, a note ~`14` px below its box.

---

## Structure

- must give a box a **plain-language label** — what it is, not what it is called in code
- must put the identifier in a note beside the box, not inside it
- should keep the note to 2 lines: the identifier (`3`), then one prose line (`2`)
- must carry the title and a one-line subtitle at the top — a diagram gets shared without its doc
- must not restate the doc — a diagram earns its place by showing what prose handles badly: nesting, ordering, fan-out
- should tag each step with the **vector that owns it** when the tree runs a vector track — a flow diagram then doubles as the seam map

---

## Colour

Excalidraw's own palette, three roles only:

| Role | Stroke | Background |
|---|---|---|
| ordinary box | `#1e1e1e` | `transparent` |
| the thing the diagram is about | `#2f9e44` | `#b2f2bb` |
| the thing it is confused with | `#1971c2` | `#a5d8ff` |
| a warning or measured cost | `#e03131` | — |

- must colour at most 5 boxes — if everything is highlighted, nothing is
- should reserve the second colour for the item readers conflate with the first; the contrast is the point
- a diagram that legends its colours (provenance, ownership, state) spends the 5 on **one** such scale, never two

---

## Mechanics

- **bound text** — a label belongs to its box: `containerId` on the text, `boundElements: [{id, type: "text"}]` on the rectangle. Unbound text drifts when the box moves
- **roundness** — `{"type": 3}` on rectangles, `{"type": 2}` on arrows, `null` on text
- **arrows — bind BOTH WAYS or the diagram distorts.** Two records, not one:
  - on the arrow: `startBinding` / `endBinding` = `{elementId, focus: 0, gap: 4}`
  - on **each bound shape**: append `{id: arrowId, type: "arrow"}` to its `boundElements`
  - the arrow-side record alone renders correctly, then leaves the arrow behind the first time someone drags the box — Excalidraw finds a shape's arrows through the shape's own `boundElements`, never by scanning arrows
  - a shape carrying a label AND arrows holds a mixed list: `[{id: "b1_t", type: "text"}, {id: "a3", type: "arrow"}]`
  - register the arrow on both endpoints **inside the arrow helper**, so it cannot be forgotten
  - a bound arrow **label** is a third record — `containerId` on the text, plus `{id, type: "text"}` in the arrow's `boundElements`
- **required keys** — every element needs `angle`, `strokeColor`, `backgroundColor`, `fillStyle`, `strokeWidth`, `strokeStyle`, `roughness`, `opacity`, `groupIds`, `frameId`, `seed`, `version`, `versionNonce`, `isDeleted`, `boundElements`, `updated`, `link`, `locked`. A missing key opens the file blank
- **file envelope** — `{"type": "excalidraw", "version": 2, "source": "https://excalidraw.com", "elements": [...], "appState": {...}, "files": {}}`
- **validate before staging** — JSON parse, unique ids, every binding two-way:

```python
import json
d = json.load(open("x.excalidraw")); els = d["elements"]; byid = {e["id"]: e for e in els}
assert len(byid) == len(els), "duplicate ids"
for e in els:
    if e["type"] != "arrow": continue
    for side in ("startBinding", "endBinding"):
        b = e.get(side)
        if b and not any(x.get("id") == e["id"] for x in byid[b["elementId"]].get("boundElements") or []):
            raise SystemExit(f"{e['id']}.{side} is one-way — the box does not know about the arrow")
```

---

## Placement

- must give each documented flow or layer **its own folder**, named for what it shows:

```
{area}/flows/
  flows.md                     ← the index: one row per flow, what each settles
  scripts/{prefix}_draw.py     ← shared builder: fonts, sizes, BOX_H, two-way binding
  001-{flow}/
    {flow}.md                  ← the doc — super-compact, links its diagram
    {flow}.excalidraw          ← the drawing
    scripts/{flow}.py          ← the generator, importing the shared builder
```

- must put the enforceable rules in the **shared builder**, not in each generator — a `box()` that takes no height cannot draw an off-scale box, and a `text()` that rejects `fontFamily: 1` cannot draw a sketch
- must run the two-way binding check inside the builder's `write()` — a validator nobody runs is not a validator

- must name the file for **what it shows**, not for the ticket or the sprint — `bake-to-render.excalidraw`
- must keep the generator beside its output, under the flow's own `scripts/` — a diagram whose script lives elsewhere is redrawn by hand the next time
- must number the folders in reading order — a reader takes them in sequence, and the number is the order
- must not put a `README.md` below a repo root — the folder's lead doc is `{folder}.md` ([repo structure](../repo/structure/repo-structure.md#documents))

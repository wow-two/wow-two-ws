# Text

*Last updated: 2026-09-10*

> The default paragraph — running copy, and the tag it renders is a prop.
> What a display is → [display](../../constructs/visual/display.md).

## Reach for it when

- must render running copy, a description line, or an inline run of words
- must wrap a figure that shares a column with other figures, so digits align
- should carry secondary copy through the `color` role rather than a class

---

## Instead of

| Reach for | When |
|---|---|
| [Heading](heading.md) | the line holds a position in the document outline |
| [Quote](quote.md) | the copy is quoted from somewhere else |
| [Code](code.md) | the run is code rather than prose |
| [Mark](mark.md) | the run is a highlighted match inside other copy |
| [Eyebrow](eyebrow.md) | the line is an uppercase kicker over a block |

---

## Values

- should leave `size` at `md`, `weight` at `normal`, `color` at `default`
- should set `color="muted"` for secondary copy and `subtle` for the faintest tier

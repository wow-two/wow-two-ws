# GradientText

*Last updated: 2026-09-10*

> Decorative gradient-filled words — a marketing display line, not an outline entry.
> What a display is → [display](../../constructs/visual/display.md).

## Reach for it when

- must tint a hero or landing headline across a colour sweep
- must stay decorative — the words carry no state and no outline position
- should wrap only the run that should be tinted, inside a real heading

---

## Instead of

| Reach for | When |
|---|---|
| [Heading](heading.md) | the line is the section's outline entry |
| [Text](text.md) | a single `color` role already says what the copy means |
| [Mark](mark.md) | the tint marks a match rather than decorating a headline |

---

## Values

- should leave `from` at `var(--color-primary)` and `to` at the accent fallback
- should leave `direction` at `r`; a diagonal sweep needs a stated reason

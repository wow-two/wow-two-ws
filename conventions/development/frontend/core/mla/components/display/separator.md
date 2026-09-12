# Separator

*Last updated: 2026-09-10*

> The hairline divider — horizontal by default, vertical inside a row.
> What a display is → [display](../../constructs/visual/display.md).

## Reach for it when

- must split two groups that a gap alone does not separate clearly
- must give a vertical rule an explicit height from its flex or grid parent

---

## Instead of

| Reach for | When |
|---|---|
| [SectionHeader](sectionHeader.md) | the rule belongs under a header it already draws |
| [Card](card.md) | the groups want boxes rather than a rule between them |
| `Stack` | a gap already separates the groups |

---

## Values

- should leave `orientation` at `horizontal` and `isDecorative` at `true`

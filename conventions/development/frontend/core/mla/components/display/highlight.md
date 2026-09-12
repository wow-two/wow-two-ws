# Highlight

*Last updated: 2026-09-10*

> Query-driven highlighting — every match inside a string, wrapped for you.
> What a display is → [display](../../constructs/visual/display.md).

## Reach for it when

- must tint the search term inside a result row, a title, or a snippet
- must hand the copy in as a string; the component tokenises it, so a slot cannot serve
- should pass the whole query list at once — it accepts an array of terms

---

## Instead of

| Reach for | When |
|---|---|
| [Mark](mark.md) | the run to tint is already isolated in the markup |
| [Snippet](snippet.md) | the string is code the reader will copy |

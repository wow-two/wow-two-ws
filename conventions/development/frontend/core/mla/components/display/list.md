# List

*Last updated: 2026-09-10*

> The bulleted, numbered, or checked list — `<ul>` or `<ol>`, with markers as a prop.
> What a display is → [display](../../constructs/visual/display.md).

## Reach for it when

- must render items whose order or membership is the content itself
- must set `isOrdered` when the sequence matters — it picks the `<ol>` tag
- should pair with `ListItem` for a leading-trailing row; a bare `<li>` also works

---

## Instead of

| Reach for | When |
|---|---|
| [DescriptionList](descriptionList.md) | each entry is a label and a value |
| [Table](table.md) | each entry has several fields worth their own columns |
| [Tree](tree.md) | the entries nest and the branches expand |
| [Timeline](timeline.md) | the entries are events on a rail |
| [ActivityFeed](activityFeed.md) | the entries are actor-verb-target sentences |

---

## Values

- should leave `marker` at `none` and `spacing` at `normal`

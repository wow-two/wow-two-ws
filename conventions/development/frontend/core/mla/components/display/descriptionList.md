# DescriptionList

*Last updated: 2026-09-10*

> Many label-value pairs as a semantic `<dl>` — settings panels, property lists.
> What a display is → [display](../../constructs/visual/display.md).

## Reach for it when

- must list the properties of one record — a detail panel, a summary, a receipt
- must hand the pairs in as an `items` array; it renders the whole list
- should switch to `stacked` when the values are long or wrap

---

## Instead of

| Reach for | When |
|---|---|
| [InfoRow](infoRow.md) | there are only one or two pairs |
| [Table](table.md) | the pairs repeat per record and want columns |
| [List](list.md) | the entries are items rather than labelled values |

---

## Values

- should leave `layout` at `inline` and `density` at `md`

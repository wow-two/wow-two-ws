# Pagination

*Last updated: 2026-09-10*

> The numbered pager under a set the server splits into pages.
> What a nav component is → [nav](../../constructs/visual/nav.md).

## Reach for it when

- must step the reader through an ordered set one page at a time
- must offer a jump to a numbered page, not only prev and next
- should keep the page the caller owns — the pager holds no state of its own

---

## Instead of

| Reach for | When |
|---|---|
| [TableOfContents](tableOfContents.md) | the content is one long document rather than a split set |
| [Breadcrumb](breadcrumb.md) | the reader needs position in a hierarchy, not in a sequence |

---

## Values

- should keep `siblings` at the default `1`, so three numbers sit between the ellipses
- should not mount the pager at `total` 1 — it still renders a lone page button

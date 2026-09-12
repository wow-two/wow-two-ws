# TableOfContents

*Last updated: 2026-09-10*

> The in-page outline, with the section currently in view highlighted.
> What a nav component is → [nav](../../constructs/visual/nav.md).

## Reach for it when

- must give a long document a jumpable outline of its headings
- must track the reader's position while scrolling, with no wiring from the caller
- should index one document; the outline empties itself when there is nothing to list

---

## Instead of

| Reach for | When |
|---|---|
| [ScrollSpy](scrollSpy.md) | only the active id is needed and the outline renders elsewhere |
| [Breadcrumb](breadcrumb.md) | the position is the page's place in a tree, not a section in a page |
| [NavItem](navItem.md) | the entries are app destinations kept across routes |

---

## Values

- should pass `source` over a hand-kept `items` list, so the outline cannot drift

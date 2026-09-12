# ScrollSpy

*Last updated: 2026-09-10*

> The headless watcher reporting which section is currently in view.
> What a nav component is → [nav](../../constructs/visual/nav.md).

## Reach for it when

- must highlight something as the reader scrolls past sections
- must drive a highlight no component covers — a rail, a progress dot, a heading
- should render nothing itself; the active id goes to the caller's own markup

---

## Instead of

| Reach for | When |
|---|---|
| [TableOfContents](tableOfContents.md) | the outline itself is what should render |
| `useScrollSpy` | the active id is read in a script rather than bound in a template |

---

## Values

- should keep the default `0px 0px -60% 0px` margin — it biases active to the top

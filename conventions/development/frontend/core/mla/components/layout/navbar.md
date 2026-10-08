# Navbar

*Last updated: 2026-09-29*

> The app's navigation bar — a full-width top bar or a full-height side rail, with start, centre and end regions.
> What a layout is → [layout](../../constructs/visual/layout.md).

## Reach for it when

- must give a page a header bar and none of the rest of an app frame
- must fill `start`, `center` and `end`, or replace all three with the default slot
- should reach for it wherever [AppShell](appShell.md) would overshoot
- must set `orientation` by where it sits: `horizontal` across the top, `vertical` down the side
- must put navigation links in `NavItem`s — they size to their label in a top bar and fill the row in a rail

---

## Instead of

| Reach for | When |
|---|---|
| [AppShell](appShell.md) | the frame also owns a sidebar, a main column and a footer |
| [Section](section.md) | the band is page content rather than a header |
| `Toolbar` | the strip is commands sharing one tab stop |
| [ContainerLayout](containerLayout.md) | no band, height or border is wanted |

---

## Values

- should leave `tone` unset for the `card` fill; a tone applies the `subtle` treatment
- may set `variant: 'glass'` over an ambient page, `transparent` over a hero; `solid` everywhere else

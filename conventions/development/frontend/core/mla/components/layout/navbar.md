# Navbar

*Last updated: 2026-09-10*

> The header bar — a start, centre and end row inside a centred container.
> What a layout is → [layout](../../constructs/visual/layout.md).

## Reach for it when

- must give a page a header bar and none of the rest of an app frame
- must fill `start`, `center` and `end`, or replace all three with the default slot
- should reach for it wherever [AppShell](appShell.md) would overshoot

---

## Instead of

| Reach for | When |
|---|---|
| [AppShell](appShell.md) | the frame also owns a sidebar, a main column and a footer |
| [Section](section.md) | the band is page content rather than a header |
| `Toolbar` | the strip is commands sharing one tab stop |
| [Container](container.md) | no band, height or border is wanted |

---

## Values

- should leave `tone` unset for the `card` fill; a tone applies the `subtle` treatment

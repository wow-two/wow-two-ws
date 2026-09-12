# NavItem

*Last updated: 2026-09-10*

> The standing row in a sidebar or nav rail.
> What a nav component is → [nav](../../constructs/visual/nav.md).

## Reach for it when

- must offer a destination the reader returns to across routes
- must pair a leading icon with a label, and a trailing count or status dot
- should render one row per destination, in a list the caller owns

---

## Instead of

| Reach for | When |
|---|---|
| `NavigationMenuLink` | the destination sits in a horizontal top strip |
| `MenuItem` | the row lives inside a floating menu, not a standing list |
| [Breadcrumb](breadcrumb.md) | the row would report position rather than offer a destination |

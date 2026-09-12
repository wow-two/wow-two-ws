# KeyboardShortcut

*Last updated: 2026-09-10*

> A key sequence — [Kbd](kbd.md) caps with connectors between them.
> What a display is → [display](../../constructs/visual/display.md).

## Reach for it when

- must render a combination — a menu row's accelerator, a help sheet, a hint
- must hand the keys in as an ordered array; it renders the caps itself

---

## Instead of

| Reach for | When |
|---|---|
| [Kbd](kbd.md) | the shortcut is a single key |
| `CommandPalette` | the shortcut is what opens the surface, not what it lists |

---

## Values

- should leave `separator` at `+` for a chord; pass `' '` for keys pressed in turn

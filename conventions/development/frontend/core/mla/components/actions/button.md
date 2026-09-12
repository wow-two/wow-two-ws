# Button

*Last updated: 2026-09-10*

> The default trigger — every command with no more specific button in this folder.
> What an action is → [action](../../constructs/visual/action.md).

## Reach for it when

- must reach for any command no sibling covers — submit, save, cancel, retry
- must reach for it when the trigger sits in the content flow, not pinned over it
- should reach for `asChild` when a router link has to carry a button's weight
- should reach for `shape="square"` or `"circle"` for an icon-only command

---

## Instead of

| Reach for | When |
|---|---|
| [Link](link.md) | the trigger moves to a destination instead of running a command |
| [ToggleButton](toggleButton.md) | the press state persists and is read back as a mode |
| [CopyButton](copyButton.md) | the command is a clipboard write |
| [Fab](fab.md) | the command is the screen's one floating action |
| [Toolbar](toolbar.md) | the buttons share one tab stop with arrow-key movement |

---

## Values

- must use a real submit action only for submitting its owning form.
- must block duplicate in-flight commands through the operation state; debouncing alone does not prevent duplicate writes.

- should set `isLoading` for an in-flight click, `isSkeleton` for an unloaded label
- should size a touch target `sm` or larger — `xs` meets the 24×24 floor exactly

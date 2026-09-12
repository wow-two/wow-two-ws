# Spinner

*Last updated: 2026-09-10*

> The bare indeterminate mark — a spinning ring and a visually hidden label.
> What an indicator is → [indicator](../../constructs/visual/indicator.md).

## Reach for it when

- must report that something is running with no fraction to show
- must stand alone; a mark with copy beside it is an [InlineSpinner](inlineSpinner.md)
- should be reached for inside another component's slot — a button, a cell, an overlay

---

## Instead of

| Reach for | When |
|---|---|
| [InlineSpinner](inlineSpinner.md) | a word belongs beside the mark |
| [LoadingState](loadingState.md) | a whole section is waiting and can be centred |
| [ProgressBar](progressBar.md) | a fraction is known |
| `foundation/icons`' `Spinner` | the mark must scale with surrounding text, em-sized |

---

## Values

- should set `tone` to `current` in a tinted surface — the ring inherits the text
- should leave `size` at `md` and `tone` at `default`

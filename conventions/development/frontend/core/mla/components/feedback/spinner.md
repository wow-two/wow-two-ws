# Spinner

*Last updated: 2026-08-22*

> The bare indeterminate mark — a spinning ring and a visually hidden label.
> What an indicator is → [indicator](../../constructs/visual/indicator.md).
> Its full surface → `Spinner.spec.md`.

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

- must set `label` where the copy has to name the operation; it defaults to `Loading`
- should set `tone` to `current` in a tinted surface — the ring inherits the text
- should leave `size` at `md` and `tone` at `default`
- should pass `class` knowing it lands on the ring itself, never on a wrapper

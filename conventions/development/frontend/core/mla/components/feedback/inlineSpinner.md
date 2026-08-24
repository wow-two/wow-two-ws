# InlineSpinner

*Last updated: 2026-08-23*

> Spinner plus label on one line — the busy mark that drops into a row or a sentence.
> What an indicator is → [indicator](../../constructs/visual/indicator.md).
> Its full surface → `InlineSpinner.spec.md`.

## Reach for it when

- must sit mid-flow — inside a button, a list row, a table cell
- must carry a word beside the mark; a bare mark is a [Spinner](spinner.md)
- should reach for it over a [LoadingState](loadingState.md) when the layout holds

---

## Instead of

| Reach for | When |
|---|---|
| [Spinner](spinner.md) | the mark stands alone and the caller writes its own copy |
| [LoadingState](loadingState.md) | a whole section is waiting and centres its report |
| [Skeleton](skeleton.md) | the unloaded shape is worth drawing rather than labelling |
| [TypingIndicator](typingIndicator.md) | a person is composing, not a request running |

---

## Values

- must override the default slot to change the copy — it falls back to `Loading…`
- should leave `size` at `sm` and `tone` at `default`; both are tuned to body text

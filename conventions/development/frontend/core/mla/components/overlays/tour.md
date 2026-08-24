# Tour

*Last updated: 2026-08-22*

> The guided walk — a mask cut around one target per step, with a tooltip beside it.
> What an overlay is → [overlay](../../constructs/visual/overlay.md).
> Its full surface → `Tour.spec.md`.

## Reach for it when

- must walk the reader through a feature over the live UI, right now
- must spotlight a real element per step — an absent target renders nothing
- should run once, on first arrival, never as a standing help surface

---

## Instead of

| Reach for | When |
|---|---|
| [OnboardingChecklist](../feedback/onboardingChecklist.md) | the tasks are done at the reader's pace, in any order |
| `Tooltip` | one control needs a hint and nothing is sequenced |
| [Callout](../feedback/callout.md) | the guidance belongs in the content, permanently |

---

## Values

- must give every step a `target` — a CSS selector, or a template ref to the element
- must leave `isOpen` unset for uncontrolled use — passing it pins the tour
- must handle `@skip` — it fires on Escape as well as on the Skip button
- should set each step's `placement` — it falls back to `bottom` and never flips
- should leave `padding` at `8` px, so the cutout clears the target's focus ring

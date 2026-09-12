# Tour

*Last updated: 2026-09-10*

> The guided walk — a mask cut around one target per step, with a tooltip beside it.
> What an overlay is → [overlay](../../constructs/visual/overlay.md).

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

- should leave `padding` at `8` px, so the cutout clears the target's focus ring

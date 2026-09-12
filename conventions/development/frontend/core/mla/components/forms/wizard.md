# Wizard

*Last updated: 2026-09-10*

> The multi-step flow root — one step at a time, with a gate before every move forward.
> What a form is → [field](../../constructs/visual/field.md).

## Reach for it when

- must reach for it when one submit is split into steps taken in order
- must mount one `WizardStep` per step and mark the last `isFinal` — its Next is the submit
- must put the submit in `onComplete`; it is awaited, and holds the pending flag while it runs
- should mount `WizardSteps` for the strip and `WizardFooter` for the controls
- should set `canGoBack="false"` when a finished step must not re-open

---

## Instead of

| Reach for | When |
|---|---|
| [Stepper](stepper.md) | the progress is shown and the flow stays the caller's |
| [Fieldset](fieldset.md) per section | every field fits one screen and one submit |
| `Tabs` | the reader picks a section in any order |

# Wizard

*Last updated: 2026-08-24*

> The multi-step flow root — one step at a time, with a gate before every move forward.
> What a form is → [field](../../constructs/visual/field.md).
> Its full surface → `Wizard.spec.md`.

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

---

## Values

- must give every step a stable `id` — `currentStep` carries that id, never an index
- must return a verdict from `validate`; resolving `false` holds the step
- must not expect Next to submit a surrounding `<form>` — the footer's buttons are `type="button"`
- must read `isOptional` as a strip marker only; no Skip control ships
- should leave `canGoBack` at `true`, the shipped default
- must read `Wizard.spec.md` as stale — the Vue step props are `isFinal` and `isOptional`

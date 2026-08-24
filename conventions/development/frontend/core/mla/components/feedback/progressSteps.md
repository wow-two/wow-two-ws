# ProgressSteps

*Last updated: 2026-08-23*

> The named stages of a flow, with the current one marked and the earlier ones complete.
> What an indicator is → [indicator](../../constructs/visual/indicator.md).
> Its full surface → `ProgressSteps.spec.md`.

## Reach for it when

- must show where the reader stands in a flow whose stages have names
- must render every stage at once — a stage that hides is not a step here
- should reach for it where the stage names are the information

---

## Instead of

| Reach for | When |
|---|---|
| [ProgressBar](progressBar.md) | the work is one continuous task with a percentage |
| `Stepper` | the flow owns the inputs and the navigation, not only the marker |
| [OnboardingChecklist](onboardingChecklist.md) | the tasks are done in any order, at any time |

---

## Values

- must pass `current` 0-based — the index of the active step, not the count done
- must set `orientation` to `vertical` once the labels no longer fit one row
- should leave `orientation` at `horizontal` — only it draws the connectors

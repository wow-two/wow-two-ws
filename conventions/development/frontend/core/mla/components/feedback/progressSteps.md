# ProgressSteps

*Last updated: 2026-09-10*

> The named stages of a flow, with the current one marked and the earlier ones complete.
> What an indicator is → [indicator](../../constructs/visual/indicator.md).

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

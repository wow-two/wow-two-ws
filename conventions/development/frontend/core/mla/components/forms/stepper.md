# Stepper

*Last updated: 2026-09-10*

> A flow walked stage by stage — the step strip and the panel it swaps are one component.
> Kind → [display](../../constructs/visual/display.md); the active step is presentation state.

## Reach for it when

- must move a reader through stages that are done in order
- must compose the parts — `StepperList`, `StepperStep`, `StepperPanel`
- should reach for it when each stage collects input, not only when it reports progress

---

## Instead of

| Reach for | When |
|---|---|
| `ProgressSteps` | the stages are only marked and nothing is switched |
| `Tabs` | the panels are alternative views, reachable in any order |
| `Accordion` | the sections stack and more than one may be open |

---

## Values

- should leave `orientation` at `horizontal`; `vertical` once the labels stop fitting a row

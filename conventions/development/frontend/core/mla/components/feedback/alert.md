# Alert

*Last updated: 2026-09-10*

> The section note — a titled report about the region it sits in, with room for actions.
> What a feedback component is → [feedback](../../constructs/visual/feedback.md).

## Reach for it when

- must report on the section it sits in, not on the page as a whole
- must stay until the state it reports changes — a transient one is a [Toast](toast.md)
- should fill icon, title, description or actions — those slots are the reason

---

## Instead of

| Reach for | When |
|---|---|
| [AlertSimple](alertSimple.md) | the body is free-form and the four slots buy nothing |
| [Banner](banner.md) | the condition is app-wide and the strip pins across the top |
| [Callout](callout.md) | the note is a doc-style aside inside prose |
| [Toast](toast.md) | the note is transient and follows an action just taken |
| `FormErrorMessage` | the message belongs to one field |

---

## Values

- should pass the slot, not the same-named prop, when the half carries markup

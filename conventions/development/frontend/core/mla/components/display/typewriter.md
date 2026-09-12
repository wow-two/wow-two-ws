# Typewriter

*Last updated: 2026-09-10*

> Copy typed out character by character, optionally cycling through phrases.
> What a display is → [display](../../constructs/visual/display.md).

## Reach for it when

- must animate a hero line, a tagline, or a rotating list of claims
- must stay decorative — reduced motion drops it straight to the full string
- should keep the copy short; every character costs a tick of reading time

---

## Instead of

| Reach for | When |
|---|---|
| [Text](text.md) | the copy is read rather than performed |
| [CountUp](countUp.md) | the animated value is a number |
| [ScrollReveal](scrollReveal.md) | the whole block should appear on scroll, already typed |

---

## Values

- must provide a persistent pause/stop control for applicable repeating automatic copy.
- must expose readable static content under reduced motion.

- should leave `typeSpeed` at `60` ms and `deleteSpeed` at `40` ms
- should leave `pauseBetween` at `1500` ms — the phrase has to be readable

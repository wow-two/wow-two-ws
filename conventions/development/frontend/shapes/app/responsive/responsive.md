# Responsive

*Last updated: 2026-09-28*

> Which screens an app supports and how it adapts between them — device targets, screen classes, verification.
> Purpose — responsive work is spent only where a product is really used, and done the same way everywhere.
> Use case — scoping a new product's frontend, or adding a page to an app that serves phones and desktops.

## Device targets

- must declare the app's device targets in its design spec (`## Screens`): the classes it serves, and its primary.
- must build responsive layouts only across the declared targets; one declared class means one layout.
- must keep an undeclared class out of scope — no layouts, fixes or verification for it.
- must declare every class a user really reaches: a phone target is declared when people open the app on phones.

---

## Screen classes

| Class | Width | Tailwind / SDK `Breakpoint` | Verify at |
|---|---|---|---|
| phone | < 768px | base styles | 390 × 844 |
| tablet | 768–1023px | `md` | 820 × 1180 |
| desktop | ≥ 1024px | `lg` (`2xl` ≥ 1536 widens it) | 1440 × 900 |

- must treat wide screens (`2xl`) as a desktop enhancement — a width cap or extra columns, never a separate design.
- must use the SDK `Breakpoint` steps and Tailwind's screen variants; no custom pixel breakpoints.
- must read breakpoints in script only through the SDK `useBreakpoint` / `useMediaQuery`, never `window.innerWidth`.

---

## Layout rules

- must write mobile-first when phone is declared: base styles serve the phone, `md:` and `lg:` add to them.
- must keep one place per route at every class ([shapes](../../shapes.md)); a class changes the layout, not the route.
- must keep primary navigation one tap away at every declared class — a tab bar or menu on phones.
- must avoid horizontal page scroll; wide tables become cards on phones or scroll inside their own container.
- must give every hover affordance a touch equivalent on phone and tablet.
- must keep touch targets at least 44 × 44px on phone and tablet.

---

## Verification

- must check every declared class at its verify size before a version closes.
- must test representative flows per class with the app's browser suite ([delivery](../delivery/delivery.md)).

# UI copy

*Last updated: 2026-10-01*

> How many words a product screen carries, and which ones earn their place.
> Purpose — an operator who already knows the product reads extra copy as noise.
> Use case — building or reviewing a screen, a sign-in card, an empty state or a confirm.

## Amount

- must give a screen its name and its essential action; every further line has to change what the reader does.
- must not add an eyebrow, a tagline or a pitch to an operational screen.
- must not restate in a hint what the label, the placeholder or the control already says.
- may keep one short line beside a primary action.
- may keep one line of description under a page or panel title.
- must keep marketing copy on marketing surfaces — a landing page, a pricing page.

---

## Sign-in

- must show the logo, the product name, at most one short line, and the sign-in action.
- must not add a footer, a feature list or a second paragraph.

---

## States

- must say why a region is empty and what to do next
  ([EmptyState](../../development/frontend/core/mla/components/display/emptyState.md)).
- must name the consequence in a confirm's description
  ([AlertModal](../../development/frontend/core/mla/components/overlays/alertModal.md)).
- must name the running task where a bare `Loading…` hides it
  ([LoadingOverlay](../../development/frontend/core/mla/components/feedback/loadingOverlay.md)).
- must show a failure through the app's display-safe mapping, never a raw server body
  ([state and data](../../development/frontend/core/mla/domains/data/state-and-data.md#transport)).

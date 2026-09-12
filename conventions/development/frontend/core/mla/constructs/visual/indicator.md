# Indicator

*Last updated: 2026-09-10*

> A small passive mark that reflects live state it does not control — presence, trend, activity, status.
> Purpose — a mark that only reads state stays free of command and dismissal behavior.
> Use case — an online dot beside an avatar, a trend arrow on a metric, a typing bubble in a thread.

## Gate

- must be **passive** — nothing about it is clickable; an interactive mark is an [action](action.md).
- must reflect state that lives outside it, taken in as a prop.
- must be small enough to sit inside another component's row, cell, or header.
- must carry an accessible name, because a colour alone is not a status.

```txt
✅ PresenceIndicator · StatusIndicator · TrendIndicator · TypingIndicator · NotificationDot · Status
```

---

## Location

### Group

- must live in `presentation/feedback/` in the SDK when it marks system or session state — presence, typing, trend.
- must live in `presentation/display/` in the SDK when it marks a property of the content beside it — a dot, a status.

```txt
✅ presentation/feedback/presenceIndicator/{PresenceIndicator.vue, index.ts}
❌ presentation/feedback/presenceStore/     (the source of the state is not an indicator)
```

---

## Declaration

### Component doc

#### [Renders](../../../lla/notation/documentation/documentation.md)

- must name the state marked, not the styling that marks it.

### Construct

- must render semantic state through tokens; identity or content colors may come from a caller-supplied value.
- must expose the state as a `data-*` attribute so a consumer can style around it.
- must keep any animation decorative and pause it under reduced motion.

### Component name

- must end `*Indicator` — a passive mark of live outside state.
- must admit `*Bar` for magnitude, `*Status` · `*Badge` · `*Tag` for chips, `*Glyph` for a mark,
  and `*Spinner` for an indeterminate ring ([visual kinds](visual.md) § *Shape words*).

---

## Content

### Props

#### [The](../../../lla/notation/documentation/documentation.md)

- must model mutually exclusive states as a closed vocabulary; numeric progress uses a numeric value.
- must take label and description as optional scalars with same-named slots.
- must take a `hasPulse`-style flag only for a live-refresh hint, and default it off.

### Slots

- must support an accessible label; expose rich label content only where the mark renders it.

### Emits

- must declare no emits — a passive mark reports nothing back.

---

## Composition

- may be embedded wherever a passive status mark is needed, including a control or action label.
- must compose nothing but text and an icon — an indicator is a leaf.
- must not mount an [overlay](overlay.md); a mark that explains itself on hover gets a `Tooltip` from its parent.

```txt
✅ DataTable → row cell → StatusIndicator     ·     NavItem → NotificationDot
❌ StatusIndicator → Tooltip → Card           (a leaf growing a surface)
```

---

## Neighbours

- [feedback](../../components/feedback/feedback.md) — which one to reach for, and with what values
- [feedback](feedback.md) — the kind that reports an operation, with copy and dismissal
- [display](display.md) — the surfaces an indicator is embedded in
- [enums](../../../lla/components/enums.md) — the member-per-state modelling a tone prop uses
- [visual kinds](visual.md) — every other kind, and the composition contract

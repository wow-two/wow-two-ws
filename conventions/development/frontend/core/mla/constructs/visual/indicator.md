# Indicator

*Last updated: 2026-08-23*

> A small passive mark that reflects live state it does not control — presence, trend, activity, status.
> Purpose — a mark that only reads state stays free of props for tone, copy, and dismissal it will never use.
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

- must render its state through a token vocabulary — an enum-backed `tone`, never a caller-supplied colour.
- must expose the state as a `data-*` attribute so a consumer can style around it.
- must keep any animation decorative and pause it under reduced motion.

### Component name

- must end `*Indicator` — a passive mark of live outside state.
- must admit `*Bar` for a magnitude strip, `*Status` for its chip form, and `*Spinner` for an
  indeterminate ring ([visual kinds](visual.md) § *Shape words*).

```vue
<script setup lang="ts">
/** Renders a colored dot and label for a system status. */
defineOptions({ name: 'StatusIndicator' });
</script>
```

---

## Content

### Props

#### [The](../../../lla/notation/documentation/documentation.md)

- must take the state as a `tone` or an enum member, never as a boolean pair like `isUp` / `isDown`.
- must take label and description as optional scalars with same-named slots.
- must take a `hasPulse`-style flag only for a live-refresh hint, and default it off.

### Slots

- must expose `label` and `description` so a caller can supply rich content in place of the scalar.

### Emits

- must declare no emits — a passive mark reports nothing back.

```vue
<script setup lang="ts">
defineProps<{ tone?: StatusTone; label?: string; hasPulse?: boolean }>();   // ✅
defineEmits<{ (e: 'click'): void }>();                                      // ❌ passive means passive
</script>
```

---

## Composition

- must be mounted inside a [display](display.md), a [nav](nav.md), or a [feedback](feedback.md) surface.
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
- [visual kinds](visual.md) — every other kind, and the composition ladder

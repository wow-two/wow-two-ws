# Primitive

*Last updated: 2026-09-10*

> Behaviour and accessibility with no look of its own — the layer every visual kind is built on.
> Purpose — focus, portalling, dismissal, and roving navigation are solved once, not once per overlay.
> Use case — building a new overlay, menu, listbox, or anything with keyboard semantics.

## Gate

- must carry **no visual styling** beyond the layout it needs to work.
- must be reusable by two or more unrelated kinds, or it belongs to the one component that needs it.
- must avoid unnecessary wrapper elements; expose child composition when the behavior needs one target element.
- must not know a domain — a primitive that names a subject is a [display](display.md) or a [control](control.md).

```txt
✅ Slot · Portal · Presence · FocusScope · DismissableLayer · AnchoredPositioner · RovingFocusGroup
❌ ColorArea               (it edits a colour — a domain control)
```

---

## Location

### Group

- must live in `foundation/primitives/`, the layer nothing may import upward from.
- must be re-exported through that folder's barrel, which is the whole primitive surface.

```txt
✅ foundation/primitives/focusScope/{FocusScope.vue, index.ts}
❌ presentation/overlays/focusScope/       (behaviour is not presentation)
```

---

## Declaration

### Component doc

#### [Renders](../../../lla/notation/documentation/documentation.md)

- must state the behaviour, not the component that uses it.
- must state the SSR posture when the primitive is inert on the server — a portal is.

### Construct

- must drop to a plain `.ts` module when it only computes, rather than render an empty component.
- must expose `asChild` on any primitive that would otherwise add a wrapper element.
- must implement the APG pattern its behaviour has, and cite the pattern in its spec, not in this convention.

### Component name

- must name the behaviour — `FocusScope`, `DismissableLayer` — never the component that consumes it.
- must take no suffix; the behaviour's own word is the whole name — `Slot` · `Portal` · `Presence`.
- must be a [provider](provider.md) instead when what it supplies is a rendering capability for a subtree.

---

## Content

### Props

#### [The](../../../lla/notation/documentation/documentation.md)

- must require explicit installation of behavior; mounting a named primitive is itself an opt-in.
- must default optional side effects off and preserve required semantics of the explicitly requested behavior.
- must expose cancellable events for per-interaction vetoes and explicit options for persistent behavior policy.

### Slots

- must expose a single `default` slot, merged into the child when `asChild` is set.

### Emits

#### [Fires when](../../../lla/notation/documentation/documentation.md)

- must emit a cancellable `CustomEvent` for a behaviour the consumer may need to pre-empt.

---

## Composition

- must be composed by every visual kind, and compose nothing but another primitive.
- must not import from `presentation/`, `auth/`, `query/`, or any capability module — the boundary is linted.
- must not be re-exported from the package root as a styled component; it ships as a building block.

```txt
✅ Modal → Portal → FocusScope → DismissableLayer → Presence
❌ FocusScope → Button        (a primitive reaching into presentation)
```

---

## Neighbours

- [overlay](overlay.md) — the kind that composes the most primitives
- [provider](provider.md) — the primitives that install a rendering capability rather than wrap one
- [architecture](../../../../shapes/app/architecture/architecture.md) — the boundary it may not import across
- [visual kinds](visual.md) — every other kind, and the composition contract

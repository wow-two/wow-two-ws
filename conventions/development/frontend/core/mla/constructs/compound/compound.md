# Compound components

*Last updated: 2026-08-19*

> A root that owns named subparts — `Modal.Content`, `Table.Row`, `Tabs.Panel` — and how both halves export.
> Purpose — a subpart that only makes sense inside its root reads as part of it, and still imports flat.
> Use case — a component that has grown a second part, or a `Root.Sub` access that will not type-check.

## The root

- must reach for a compound root only when it owns 2+ subparts that exist nowhere else — `Modal.Content` ·
  `Table.Row` · `Tabs.Panel`; a lone add-on stays a flat sibling.
- must keep the root's own role suffix, and name each subpart `Root{Part}`.

---

## The export

- must export each subpart both flat and attached, so `Root.Sub` and the flat name both resolve.
- must type the named export through `Object.assign`, so `import { Modal }` plus `<Modal.Content>` type-checks.
- must not attach the statics by casting the default export — the barrel re-exports the named binding, untyped.

```ts
ModalRoot.displayName = 'Modal';   // plain-fn roots keep the DevTools name; forwardRef roots name the inner fn
export const ModalContent = …;     // flat subparts stay exported
export const Modal = Object.assign(ModalRoot, { Content: ModalContent, Header: ModalHeader, … });
```

---

## Neighbours

- [constructs](../constructs.md) — the authoring pass a compound root still runs end to end
- [panel](../visual/panel.md) — the kind a subpart most often is
- [architecture](../../../../shapes/app/architecture/architecture.md) — the slice a compound folder sits in, in a
  product
- [library](../../../../shapes/library/library.md) — the folder a compound takes in a package

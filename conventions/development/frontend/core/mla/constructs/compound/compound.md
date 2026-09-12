# Compound components

*Last updated: 2026-09-10*

> A root that owns named subparts — `Modal.Content`, `Table.Row`, `Tabs.Panel` — and how both halves export.
> Purpose — a subpart that only makes sense inside its root reads as part of it, and still imports flat.
> Use case — a component that has grown a second part, or a `Root.Sub` access that will not type-check.

## The root

- must reach for a compound root only when it owns 2+ subparts that exist nowhere else — `Modal.Content` ·
  `Table.Row` · `Tabs.Panel`; a lone add-on stays a flat sibling.
- must keep the root's own role suffix, and name each subpart `Root{Part}`.

---

## The export

- must export public subparts as named bindings and keep implementation-only parts private.
- must use flat named component exports for Vue; the parent-child relation is expressed through context and naming.
- may attach named subparts with `Object.assign` for a React compound surface when its declared public API uses statics.
- must preserve the named binding's type; a cast on a different default binding does not type the public export.
- must document the actual export surface beside the code and test consumer imports.

```txt
✅ Vue: Modal, ModalContent, ModalHeader as named exports
❌ A Vue application required to use a React-only Modal.Content spelling
```

---

## Neighbours

- [constructs](../constructs.md) — the authoring pass a compound root still runs end to end
- [panel](../visual/panel.md) — the kind a subpart most often is
- [architecture](../../../../shapes/app/architecture/architecture.md) — the slice a compound folder sits in, in a
  product
- [library](../../../../shapes/library/library.md) — the folder a compound takes in a package

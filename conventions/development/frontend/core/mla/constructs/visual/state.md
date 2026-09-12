# State

*Last updated: 2026-09-10*

> A whole-region stand-in rendered **instead of** content — because there is none, it is still loading, or it failed.
> Purpose — the three non-happy paths get one kind, so every region answers empty, loading, and failed the same way.
> Use case — an empty list, a pending section, a subtree that threw.

## Gate

- must replace unavailable content or mask an existing region during a blocking operation.
- must distinguish a shape-only skeleton from a copy-bearing loading, empty or failure surface.
- must preserve the region's layout where its final dimensions are known.
- must offer a recovery action when one exists, without inventing one for a passive skeleton.
- must use feedback for the completed outcome of an operation.

---

## Location

### Group

- must live in `presentation/display/` in the SDK for the empty case, beside what it replaces.
- must live in `presentation/feedback/` in the SDK for the loading case, and in `router/` for the root error boundary.

```txt
✅ presentation/display/emptyState/{EmptyState.vue, EmptyState.spec.md, index.ts}
❌ presentation/display/noResults/          (the kind is named by its suffix, not by its copy)
```

---

## Declaration

### Component doc

#### [Renders](../../../lla/notation/documentation/documentation.md)

- must name the case it covers — empty, loading, failed.

### Construct

- must let the caller size the state to the region; skeleton geometry follows the replaced content.
- must route loading updates through the owning live region; shape-only skeletons stay decorative.
- must give an empty or failed region meaningful copy at the document's appropriate heading level.
- must catch and render, not swallow, in a boundary — the error goes to the logger seam as well.

### Component name

- must end `*State` — the whole-region stand-in for content that is absent, pending, or failed.
- must end `*Gate` for a conditional-render guard, `*Boundary` for the fallback of a failed subtree.
- must admit `*Overlay` for a stand-in painted over the region it covers — all shape words ([visual
  kinds](visual.md) § *Shape words*).

---

## Content

### Props

#### [The](../../../lla/notation/documentation/documentation.md)

- must support accessible copy for a report surface; a skeleton does not need title or action props.
- must keep a busy mask from disabling its own recovery or cancel action.
- must not take the data it stands in for — the caller has already decided there is none.

### Slots

- must expose replaceable copy and recovery content where the state renders them.

### Emits

- must declare no emits — the way out is an [action](action.md) the caller puts in the `actions` slot.

---

## Composition

- must follow the shared [composition contract](visual.md#composition-order).
- must let the owner choose loading, content, empty and failure at the scope it owns.
- may let a collection render its own empty row while the page owns route-level failure.
- must use actions for recovery; a skeleton does not intercept input or announce every repeated shape.
- must prevent interaction with a masked busy region through keyboard as well as pointer input.

---

## Neighbours

- [display](../../components/display/display.md) · [feedback](../../components/feedback/feedback.md) — which one to
  reach for, and with what values
- [feedback](feedback.md) — the kind that reports an operation instead of standing in for content
- [display](display.md) — the content a state stands in for
- [page](page.md) — the owner that picks between content and stand-in
- [visual kinds](visual.md) — every other kind, and the composition contract

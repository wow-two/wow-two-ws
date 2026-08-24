# State

*Last updated: 2026-08-23*

> A whole-region stand-in rendered **instead of** content — because there is none, it is still loading, or it failed.
> Purpose — the three non-happy paths get one kind, so every region answers empty, loading, and failed the same way.
> Use case — an empty list, a pending section, a subtree that threw.

## Gate

- must **replace** the content of a region, not sit beside it — a companion mark is an [indicator](indicator.md).
- must fill the region it stands in for, so the layout does not jump when the content arrives.
- must offer the way out — a retry, a create action, a cleared filter — or say plainly that there is none.
- must not report a completed operation; that is [feedback](feedback.md).

```txt
✅ EmptyState · LoadingState · AppErrorBoundary · Skeleton
❌ Spinner                 (a mark inside a busy control — feedback, not a region stand-in)
```

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

- must render one centred block sized by a `size` prop, so it fits a card and a full page alike.
- must expose an accessible live region for the loading case, and a heading for the empty case.
- must catch and render, not swallow, in a boundary — the error goes to the logger seam as well.

### Component name

- must end `*State` — the whole-region stand-in for content that is absent, pending, or failed.
- must end `*Gate` for a conditional-render guard, `*Boundary` for the fallback of a failed subtree.
- must admit `*Overlay` for a stand-in painted over the region it covers — all shape words ([visual
  kinds](visual.md) § *Shape words*).

```vue
<script setup lang="ts">
/** Renders the no-results stand-in for an empty region. */
defineOptions({ name: 'EmptyState' });
</script>
```

---

## Content

### Props

#### [The](../../../lla/notation/documentation/documentation.md)

- must take `title` as a required scalar, and `description` as an optional one, each with a same-named slot.
- must take `size` from the shared size vocabulary, so the same component fits any region.
- must not take the data it stands in for — the caller has already decided there is none.

### Slots

- must expose `icon`, `title`, `description`, and `actions`.

### Emits

- must declare no emits — the way out is an [action](action.md) the caller puts in the `actions` slot.

```vue
<script setup lang="ts">
defineProps<{ title: string | number; description?: string | number; size?: Size }>();  // ✅
defineProps<{ items: ReadonlyArray<unknown> }>();                                       // ❌ it has none
</script>
```

---

## Composition

- must be mounted by the [page](page.md), [view](view.md), or [panel](panel.md) that owns the region.
- must compose [display](display.md) and [action](action.md) in its slots — an icon, a heading, a create button.
- must not be mounted by the [display](display.md) it replaces; the owner chooses between them.
- must not mount a [control](control.md) — there is nothing yet to edit.

```txt
✅ CodesListPage → EmptyState → Button("Create a code")
❌ DataTable → EmptyState        (the table deciding it has nothing to show)
```

---

## Neighbours

- [display](../../components/display/display.md) · [feedback](../../components/feedback/feedback.md) — which one to
  reach for, and with what values
- [feedback](feedback.md) — the kind that reports an operation instead of standing in for content
- [display](display.md) — the content a state stands in for
- [page](page.md) — the owner that picks between content and stand-in
- [visual kinds](visual.md) — every other kind, and the composition ladder

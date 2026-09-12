# Components

*Last updated: 2026-09-10*

> Which thing to reach for, and with what values — the application register over the roles `constructs/` defines
> and the surfaces the SDK specs.
> Purpose — the SDK receives a value and applies it; this is where the workspace chooses the value.
> Use case — picking between two shapes that both work, or fixing the value a parameter should carry here.

## The registers [REQUIRED]

| Register | Owns | Lives in |
|---|---|---|
| definition | the role, its declaration, its suffix, its home | [`mla/constructs/`](../constructs/constructs.md) |
| application | which one to reach for, with what values — members, attributes | `mla/components/` — here |
| surface | every prop, slot, emit, option and state one thing exposes | `{Component}.spec.md`, in the SDK repo |

The discriminating pair: the spec says a prop **takes** a timeout; the application register says the preferred
timeout for that operation **is** `N`. The SDK receives and applies; the convention chooses.

`lla` / `mla` / `hla` name the **layers** — how far a rule reaches. A register is a different cut: which half of
one role a doc owns.

---

## The gate [REQUIRED]

- must place a doc here only when it says **which thing to reach for, and with what values**.
- must place it in [`mla/constructs/`](../constructs/constructs.md) when it says **what the thing is** — the role,
  the suffix it takes, the shape of its contract.
- must place it in [`lla/components/`](../../lla/components/components.md) when the thing is a **language form**
  used end to end — a `const` binding, a `const` object value set, a static-helper object.
- must leave one component's props, slots, emits and states to its `{Component}.spec.md` in the SDK repo.
- must not enumerate a parameter here, and must not fix a preferred value in a spec — one half each.
- must not read self-sufficiency or simplicity as the test — every component has a caller, and that sorts nothing.

A kind doc fails the gate — [page](../constructs/visual/page.md) says what a page **is**, so it defines. One
component's prop table fails too — that is its spec's surface. `constants`, `enums` and `extensions` fail on
the third bullet: TypeScript supplies all three, so they are
[lla components](../../lla/components/components.md).

---

## Adding a doc here [REQUIRED]

- must use `Reach for it when`, `Instead of`, and optional `Values` sections for a component selection entry.
- must name a component entry for the component, using the existing lower-camel-case filename.
- must keep group leads plural and use them to index selection entries.
- must keep discovery grouping distinct from semantic kind; the kind contract determines an SDK migration target.
- must keep one canonical entry per selection subject; link it from other groups rather than duplicating its rules.
- must resolve public names and concrete surface details against the selected package's code-adjacent specification.

---

## Reaching for one

- must use the selected framework's SDK surface: `@wow-two-beta/ui-vue` for Vue.
- must apply the [extraction boundary](../../../shapes/app/architecture/boundaries.md) to reusable work.
- must fix a missing or incorrect SDK API through its sweep instead of preserving a product workaround.
- must keep component API details and compatibility aliases in the selected package's specifications.

---

## The groups

One folder per construct folder — the visual groups, plus `behavior/` and `data/`. Each folder's lead indexes
its own members; this table indexes the folders, never the members.

| Group | Construct |
|---|---|
| [behavior](behavior/behavior.md) | [behavior](../constructs/behavior/behavior.md) |
| [data](data/data.md) | [data](../constructs/data/data.md) |
| [actions](actions/actions.md) | [action](../constructs/visual/action.md) |
| [display](display/display.md) | [display](../constructs/visual/display.md) |
| [feedback](feedback/feedback.md) | [feedback](../constructs/visual/feedback.md) |
| [forms](forms/forms.md) | [control](../constructs/visual/control.md) · [field](../constructs/visual/field.md) |
| [layout](layout/layout.md) | [layout](../constructs/visual/layout.md) |
| [nav](nav/nav.md) | [nav](../constructs/visual/nav.md) |
| [overlays](overlays/overlays.md) | [overlay](../constructs/visual/overlay.md) |

---

## Neighbours

- [mla constructs](../constructs/constructs.md) — what each role is, before this register chooses between them
- [lla components](../../lla/components/components.md) — the language forms used end to end, constants onward
- [lla constructs](../../lla/constructs/constructs.md) — the language constructs these kinds are built from
- [notation](../../lla/notation/notation.md) — the defaults a component may override

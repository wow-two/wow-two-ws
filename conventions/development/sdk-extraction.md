# Extract, keep, remove

*Last updated: 2026-10-01*

> Where a component, helper or module lives — a shared SDK, the app, or nowhere.
> Use case — judging a piece already built or about to be built, in app code or in either SDK.

## Decision

- must ask whether the piece is generic or carries this app's domain logic; that decides where it lives.
- must ask why an app-local piece over an SDK primitive exists; avoiding duplication, extending a prop and restyling
  are not reasons.
- must not decide by the amount of logic — a label-only `Field` is SDK, a logic-heavy `ContentView` stays in the app.

---

## Extract

- must extract a generic piece to the SDK — `@wow-two-beta/ui-vue` or `WoW2.Sdk.Backend.Beta`.
- must extract it even when it carries little logic, and even when one app uses it today.
- must treat a generic atom — the lowest-level input or control — as SDK, never app-local.
- must build a missing generic primitive in the SDK first, mirroring its nearest sibling, then consume it.
- must schedule a larger extraction through the [dev cycle](dev-cycle.md); an engine-wrapping module follows
  [swappable modules](swappable-modules.md).

---

## Keep

- must keep a piece carrying app-bound logic in the app.
- may keep it as its own component for encapsulation and readability, not only to avoid duplication.

---

## Remove

- must remove an app-local piece whose only reason is DRY, a prop extension or a restyle over an SDK primitive.
- must extract the extension into the SDK when it is generic, then use the SDK version.
- must delete the wrapper and use the SDK primitive directly when the SDK already covers it.
- may repeat an SDK-primitive composition across call sites; never wrap it in an app-local component for DRY.
- must re-decide a primitive built in the app before the call was clear; a working app-local primitive is not a
  resting state.

---

## Examples

| Piece | Verdict | Because |
|---|---|---|
| `Field` — label and control, almost no logic | extract | a generic primitive |
| `DateTimeField` — Temporal and accessibility logic | extract | generic, though one app uses it |
| `ContentView` — the app's content panel | keep | app-bound logic |
| `SelectField` — app-local, wraps the SDK select | remove | extract a generic extension, else delete it |

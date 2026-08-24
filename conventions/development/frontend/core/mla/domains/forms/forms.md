# Forms

*Last updated: 2026-08-24*

> Form state, validation and control wiring — every form runs on the `@wow-two-beta/ui` `/forms-engine` facade
> (`useAppForm`) composed with the presentation `Field` chrome.
> Use case — building a form, or swapping the engine underneath one.

## Entities

All from `@wow-two-beta/ui/forms-engine` (engine-free) unless the `app` kind marks it as the app's own.

| Entity | Kind | Role |
|---|---|---|
| `useAppForm` | hook | creates the form (`{ defaultValues, schema, onSubmit }`), imported from the app's `@/form` |
| `AppForm` · `AppFieldApi` · `AppFormState` | types | the form / field / state contract types |
| `form.Field` | render-prop | binds one field; composes the presentation `Field` chrome |
| `form.Subscribe` · `form.useFormState` | selector | slice-subscribe (`isSubmitting`, `submitError`, `isDirty`) |
| `useFieldArray<TItem>` | hook | typed row collections (`rows`, `key`, `push` / `remove` / `move`) |
| `StandardSchemaV1` | type | the validation seam (zod 4 default; valibot per-form swap) |
| `{Model}Schema` · `empty{Model}` | app | the whole-form schema and init-values const, in `application/{domain}/` |
| `*ApiRequest` / `*Dto` | app | the shape the form **produces** — bind `defaultValues` to it |
| `AppError` | type | the failure `onSubmit` returns; drives field-error mapping (`foundation/http`) |

---

## Engine pin [REQUIRED]

- must pin the engine once per app — `src/form.ts` re-exports one adapter subpath, `@/form` is the import site.
- must import the contract types from `@wow-two-beta/ui/forms-engine`, the engine-free entry.
- must not import an engine package in app code — native access goes through the adapter's typed `form.engine`.
- must default to `/forms-engine/tanstack`; `/forms-engine/house` is the zero-dependency micro-engine, and
  swapping between them edits the pin line only.

```typescript
// src/form.ts — the only vendor-touching line in the app
export { useAppForm } from '@wow-two-beta/ui/forms-engine/tanstack';
```

---

## Values and schema

- must bind the form to the shape it **produces** — an `*ApiRequest` submitting to the backend, a `*Dto`
  updating a frontend model. No third case exists, so no bespoke `*Values` / `*Draft` type.
- must let fields stay forgiving while editing (`""` for a required string, an enum as `string`).
- must take a row key from `useFieldArray`'s `row.key`, never from a modeled `id`.
- must validate with one whole-form schema behind the `StandardSchemaV1` seam; the provider and its
  version live in [validation](../validation/validation.md).
- may write a **partial** schema covering only the fields the form owns — the backend is the source of truth.
- must name the schema `{Model}Schema` beside the mappers in `application/{domain}/`, the const `empty{Model}`.
- must keep validation messages in the schema, never in the component.

---

## Creation

- must create the form with `useAppForm({ defaultValues, schema, onSubmit })`.
- must keep async edit-prefill on `/query` — render once loaded, or `reset(data)`; never per-field effects.
- must read `reset()` as a return to `defaultValues`, `reset(next)` as a re-seed of values and dirty baseline.
- must call `reset(loadedEntity)` from an edit page's Discard, never bare `reset()`.

---

## Field wiring

- must render every field through `form.Field`, composing the presentation `Field` chrome in the render prop.
- must not hand-wire ids or aria — `FormControlContext` supplies `id` / `aria-describedby` / `aria-invalid` /
  `disabled` / `required` / `readOnly` to every control reading `useFormControl`, plus `Label` targeting and
  the `FormErrorMessage` `role="alert"`.
- must add only `label`, the `value` / `setValue` binding and `onBlur={f.onBlur}` — errors render on their own.
- must put per-mode flags on the chrome (`<Field isDisabled>`), or on `form.Field` for a bare control.
- must expect `f.errors` to merge client and server messages, client first — `Field` renders them all.
- may disable a whole form with `useAppForm({ …, isDisabled })` — it ORs into every control and makes submit
  inert; must not hand-disable each control.
- must import controls from `@wow-two-beta/ui/presentation/forms`, each of which reads `FormControlContext`.
- must look a control up by its [kind](../../constructs/visual/visual.md) and read its own
  `{Control}.spec.md` for props — a convention does not roster components.
- must reach for a `*Field` variant (`CheckboxField`) for a labelled single control, the bare control otherwise.
- must speak `Temporal.PlainDate` / `PlainTime` to date and time controls, never a native `Date`.
- must drive a multi-step form with `Wizard` over one form, gating each step with `form.validate()`.

```tsx
<form.Field name="slug">
  {(f) => (
    <Field label="Slug" isDisabled={isEdit}>
      <TextInput value={f.value} onChange={(e) => f.setValue(e.target.value)} onBlur={f.onBlur} />
    </Field>
  )}
</form.Field>
```

---

## Arrays

- must drive row collections with `useFieldArray<TItem>(form, path)` — reactive `rows`, stable `key`s,
  element-typed `push` / `insert` / `remove` / `swap` / `move`.
- must render a row cell through `<array.Field index={row.index} name="…">`, typed one level deep.
- must not cast `f.value` on a row — that cast is the tax the helper exists to remove.
- must key rows by `row.key`, never the array index — a key follows its row, so focus, local state, errors and
  touched state stay with it.
- may reach for `form.array(path)`, the primitive beneath it, only for ops without rendered rows.

```tsx
const rules = useFieldArray<RuleValues>(form, 'rules');   // rules.push(emptyRule()) · rules.move(from, to)

{rules.rows.map((row) => (
  <rules.Field key={row.key} index={row.index} name="destination">
    {(f) => <Field label="Destination"><TextInput value={f.value} onBlur={f.onBlur} /></Field>}
  </rules.Field>
))}
```

---

## Neighbours

- [submission](submission.md) — submit, server-error mapping, and validation timing
- [state and data](../data/state-and-data.md) — the mutation a form's `onSubmit` calls
- [swappable modules](../../../../../swappable-modules.md) — the contract every engine adapter satisfies

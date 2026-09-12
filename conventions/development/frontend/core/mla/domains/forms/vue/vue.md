# Vue forms

*Last updated: 2026-09-10*

> Vue bindings and engine selection for the form contract.

## Composition

- must inherit the [form contract](../forms.md) and [submission semantics](../submission.md).
- must pin the adapter in `bootstrap/form.ts`; importing code must not name the vendor.
- must use the Vue adapter of the selected engine.
- must bind a control's value and update event through the field binding's declared API.
- must pass reactive disabled state and schema dependencies as refs/getters, not read-once snapshots.
- must release field subscriptions, debounce timers and owned requests with the component scope.
- must read public props/slots from the code-adjacent component spec; do not duplicate a prop inventory here.

---

## Engines

- must keep the vendor dependency optional and isolated to its adapter subpath.
- must use the house adapter only within its declared capability ceiling.
- must select an adapter that supports the form's needed parsing, async validation and field-array semantics.
- must run the same form-engine conformance cases against every advertised adapter.
- must test Vue scope disposal and reactive prop updates in addition to framework-neutral conformance.

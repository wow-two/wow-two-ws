# Submission

*Last updated: 2026-09-10*

> Validation, request races and the visible outcome of a form submission.

## Manual submit

- must validate a value snapshot and submit its parsed output through one pipeline.
- must return the request's failed `Result` through that pipeline; pages do not duplicate error catching/mapping.
- must coalesce repeated manual submits for the same snapshot into one in-flight operation.
- must expose pending, succeeded and failed state separately from editable values.
- must suppress stale completion UI when the form resets, disposes or changes session.
- must keep a failed request's values editable; a failure does not reset the dirty baseline.
- must advance the saved baseline to the confirmed submitted snapshot, preserving any newer edits.
- must treat cancellation as a distinct outcome; it does not prove the server rolled back.

---

## Server errors

- must consume the backend's `errors: [{ property, code, message }]` extension.
- must also accept framework validation `errors: { field: [message] }` through a named decoder.
- must map wire property paths into declared field paths, including nested rows.
- must retain unmapped/global errors as a form-level summary instead of silently discarding them.
- must apply field errors only to fields whose submitted value still matches the current value.
- must keep messages display-safe and preserve codes for localization.
- must focus the first invalid enabled field on a user submit; use the summary when no field can receive focus.
- must announce errors once; coordinate summary and field live regions to avoid duplicate speech.
- must not move focus during background validation or autosave.

---

## Timing

- must default to validation on submit, with touched fields revalidated after an attempted submit.
- may choose blur/change validation when immediate feedback is part of the interaction.
- must discard an asynchronous validator's result when its value generation is stale.
- must validate a wizard's current step against that step's schema or field subset.
- must validate the whole output on final submit, including cross-step constraints.
- must distinguish draft-save validation from final-submit validation explicitly.
- must not bypass a transformation by submitting invalid input as if it were parsed output.

---

## Autosave

- must debounce user-origin changes when configured; reset/prefill never trigger a save.
- must queue the latest dirty snapshot while a save is in flight.
- must run one trailing save when that snapshot differs from the confirmed saved snapshot.
- must coalesce intermediate snapshots, not silently discard the last edit.
- must keep a failed latest snapshot dirty and expose retry without an automatic retry loop.
- must cancel timers and invalidate display callbacks on disposal; cancellation follows the transport contract.
- must guard navigation on unsaved state, including a pending trailing snapshot.

---

## Verification

- must cover transforms, current-step/final validation, duplicate submit and edits during autosave.
- must cover reset/disposal during async work, reordered rows and stale field errors.
- must assert rendered errors and focus in interaction tests; engine conformance verifies shared timing semantics.
- must run form interactions with the pinned framework adapter, even when a house engine is used for fixtures.

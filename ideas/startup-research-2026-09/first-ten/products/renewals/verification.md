# renewals verification

## Final integrated status

Root completed strict compilation, browser workflow/validation checks, actual export inspection, reload persistence, and responsive light/dark checks on 2026-09-29. See [the authoritative suite verification](../../verification.md) for the exact executed subset and limits. Sample state was reset before handover.

## Earlier lane review

The notes below describe the lane review at its original point in time; any pending root checks are superseded by the integrated record above.

Checked 2026-09-29. Local prototype only.

## Executed

- Shared strict check: `node node_modules/vue-tsc/bin/vue-tsc.js --noEmit` passed after final source fixes.
- An isolated Node harness compiled the actual SFC script using the installed Vue SFC compiler and TypeScript, instantiated its setup function with a stub `PrototypeApi`, and invoked the real state-changing methods. No browser or external service was used.
- Assertions passed: Calendar-day notice date; decision blocked before owner acknowledgment; owner reassignment clears acknowledgment; intent and reopened history preserved; impossible date rejected; export explicitly reports no external subscription changes.
- Verified sequence: 2026-10-31 minus 30 days = 2026-10-01, two days from fixed 2026-09-29. Valid new vendor with renewal 2026-12-15 and 30 days notice yields 2026-11-15.
- Export callback contained valid JSON reflecting current state. The deep watcher called `api.save` after mutations.

## Evidence limits

These are state/invariant checks, not DOM interaction or visual tests. The download callback was inspected; an actual browser download was not performed in this lane. The save callback was observed; real browser-storage persistence and reload behavior remain the shared-shell browser check. Native dialogs, focus, keyboard interaction, mobile layout and theme contrast remain root-owned browser checks. The exact-button scenario is in [product analysis](product.md).

No account action, email, external upload, subscription change, payment, deployment, staging or commit occurred.

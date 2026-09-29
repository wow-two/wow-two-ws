# Arrival verification record

## Final integrated status

Root completed strict compilation, browser workflow/validation checks, actual export inspection, reload persistence, and responsive light/dark checks on 2026-09-29. See [the authoritative suite verification](../../verification.md) for the exact executed subset and limits. Sample state was reset before handover.

## Earlier lane review

The notes below describe the lane review at its original point in time; any pending root checks are superseded by the integrated record above.

Date: 2026-09-29. Scope: developer lane source review; root owns combined compilation and browser QA.

## Executed evidence

- Inspected initial model: Sep 29 12:30 UTC has two received occurrences, one beyond grace, one within grace and one upcoming.
- Inspected status precedence: exception, receipt, future/not-due, grace, late. Received counts and the expected denominator derive from those states.
- Inspected mutations: receipt insertion rejects an existing receipt/exception; exception creation rejects an existing receipt/exception; removing an exception restores evaluation; simulation clock caps at 18:00 UTC.
- Strengthened row validation to `Number.isSafeInteger` plus positive count, so imprecise large numbers are rejected.
- Inspected metadata-only export and shared persistence watcher; no file contents, polling or network calls exist in the module.
- Root reported strict Vue TypeScript checking and the combined build succeeded before the safe-integer adjustment. No final post-adjustment build is claimed by this record.

## Browser constraint

The child CUA browser entry point returned `Browser is not available: iab` when opening the local prototype. Root was notified and owns the browser smoke run for `#files`. No browser mutations, downloads, persistence reloads, screenshots or viewport tests were executed in this child session. The exact source-derived expected sequence is in [product.md](./product.md#exact-prototype-smoke-scenario).

# Observability

*Last updated: 2026-09-10*

> Logging, tracing and measurement obligations at an operation boundary, independent of the exporter.

## Contract

- must keep business behavior independent of enabled telemetry listeners and exporters.
- must record one operation failure at its handling boundary; propagating layers do not record it again.
- must distinguish a handled expected failure from a defect when choosing its severity.
- must preserve trace context when work crosses a process or queued-work boundary.
- must not place credentials, complete request bodies or connection strings in telemetry.
- must select stable operation names and bounded metric dimensions; identifiers belong in permitted log or trace fields.
- must configure collection and export at the host; a library emits through its instrumentation seams.
- must require explicit host opt-in for additional sinks and exporters.

---

## Providers

- [serilog](serilog/serilog.md) — host logging, message templates and startup capture.
- [otel](otel/otel.md) — activity and meter ownership, collection and export.

- must keep instance options and sink defaults in the SDK's source-owned documentation.
- must select SDK helpers by their implemented behavior, not by a historical inventory's status.

---

## Verification

- must verify correlation with one operation's trace and log output from the configured sink.
- must verify a returned failure and a thrown failure at their respective handling boundaries.
- must verify business behavior with listeners disabled.
- must verify an exporter outage cannot replace the operation's result.

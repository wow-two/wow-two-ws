# Reporting

*Last updated: 2026-09-29*

> The trail an app keeps of what the user did, the incident it freezes when something fails, and the sink a report leaves by.
> Purpose — a user reports a failure in one click, and the report names the steps, the request and its trace id.
> Use case — offering Report on a failure notice, or filing an incident from app code.

## The contract

- must record nothing until the app wires a tracker or records a step itself.
- must send nothing until a user or the app sends a captured incident.
- must never throw from recording, capture or the recording fetch; the reporter's own failure routes to its handler.
- must freeze the trail, the request, the page and the user at capture; take the note and screenshot at send.
- must deliver an incident once — a repeated send returns the first delivery; only a failed delivery may retry.
- must reject a failed delivery, so the surface can offer a retry.
- must name the request behind a failure from the failure's own endpoint first, its status second.
- must read the trace and request ids from the problem details before the response headers.
- must carry a grouping fingerprint — app, failure kind, code, and the route with its record ids templated.
- must inherit opt-in registration from [domain lifetime](../domains.md#lifetime).

---

## Providers

| Provider | Implements | Reach for it when |
|---|---|---|
| http | posts the report as JSON to an ingest, reads back its reference | production, pointed at the triage app |
| memory | keeps every report | tests, and previewing a report before an ingest exists |
| console | prints each report | local development |
| any sink | the sink seam over a transport | a different ingest or queue |

---

```txt
✅ feedbackQueryErrors(feedbackBus, { reporter })   a failed query's notice carries one-click Report
✅ toast({ severity: 'danger', title, report: reporter.capture(error).send })
❌ a Report button that opens a form first                                 the user retells what the trail holds
❌ Report on a validation failure                                          the user's to fix, not a defect
```

---

## Neighbours

- [domains](../domains.md) — the shape every domain follows
- [feedback](../feedback/feedback.md) — the notice that offers the report
- [observability](../observability/observability.md) — the local record joined by the same trace id
- [data](../data/state-and-data.md) — the failure a report most often carries

---

## Privacy

- must record a request's method, URL, status, duration and ids — never a body or a request header.
- must redact credentials in every URL, and mask credential keys at any depth before storing a field.
- must name a clicked control by its label, never an input's value; `data-report-ignore` drops a subtree.
- must let the app run a last pass over the finished report, failing the send closed when that pass throws.
- must leave screenshot capture to the app — no report carries one unless the app supplies the capture.
- must follow [security](../security/security.md#data) for free text and personal data.

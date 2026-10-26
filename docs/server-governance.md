# WoW 2.0 — Server governance

*Last updated: 2026-10-26*

> A service on every hosted server that owns the server-side work Wheelhouse should not: logs, feedback and, later,
> metrics, backups and failover steps. Wheelhouse shows widgets and forwards each request to the server's service.
> Analysis pool; settled points move to [platform apps](platform-apps.md), [app boundaries](app-boundaries.md) and
> Wheelhouse's backlog.

## Developer input (2026-10-26)

- Logs and Feedbacks become separate modules, not Wheelhouse features.
- A server governance service runs inside each hosted server and hosts those modules.
- Wheelhouse shows widgets and forwards to the server's service whenever the owner works with logs or feedback.
- Reasons: the link needs a secure connection anyway, and searching several products' logs needs compute that
  belongs next to the data.

---

## Verdict

- The direction fits what exists: logs already sit on each products host, every environment of a product runs on
  one server ([redundancy](../conventions/deployment/servers/redundancy.md)), and redundancy's Coordination already
  allows "a service of its own on each server".
- Two constraints shape it: feedback ingest comes from end users' browsers, so it needs a public path; and logs
  carry no trace id yet ([logging analysis](../ideas/logging-analysis.md)), so the Feedbacks → log-lines join waits on
  an SDK fix.

---

## Points

- [ ] G1 — Shape: one governance host per server composing module libraries, or one service per module per server
- [ ] G2 — Wheelhouse's role: widgets, auth and forwarding over the tailnet; no log or feedback data stored in it
- [ ] G3 — Feedback ingest: a public path on each server's ingress, keyed per product, or one central ingest
- [ ] G4 — Log pipeline: collect containers' stdout on the host, then build thin (PostgreSQL / SQLite search) or wrap
  (Vector + Loki)
- [ ] G5 — Delivery: the governance service as a Wheelhouse-deployed product with one environment per server, or
  part of the products-host kit
- [ ] G6 — Module repositories: each module a domain repository (library + service), like Identity
- [ ] G7 — Retention and compute bounds per server, and what happens when a server is full
- [ ] G8 — Later modules: metrics and uptime probes, backups, failover coordination; which join first
- [ ] G9 — SDK prerequisites: trace id in every log line, structured JSON logs, OTLP log export (v0.6 candidates)

---

## Context

- Feedbacks spec: [feedbacks-spec.md](../ideas/feedbacks-spec.md) — ingest API, grouping, inbox; the fe sdk
  `/reporting` client exists.
- Logs: [platform apps](platform-apps.md) #6 — structured store and `/logs` viewer by trace id; the SDK emits OTel
  traces and metrics, not logs.
- Wheelhouse today reads a service's recent log lines over SSH, one container at a time.

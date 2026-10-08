# WoW 2.0 — App boundaries

*Last updated: 2026-09-30*

> Where each capability lives as the platform grows: its own app, a project in a shared repository, or a service
> inside another app, so later apps plug in without an extraction. Analysis pool, queued behind the
> [delivery pipeline](delivery-pipeline.md) points. The apps and their build order: [platform apps](platform-apps.md);
> distribution forms: [platform model](platform-model.md).

## Developer input (2026-09-29)

- A products app may own product information and share it with the other apps.
- A GitHub projects dashboard will follow: automated issue labels, AI sorting and prioritisation.
- Reports, feedback and bugs flow through GitHub issues; their dashboards are not built now, but their seams must be.
- Secrets Vault started as its own repository, so one instance per deployed product stays possible.
- A project in a multi-project repository may keep that option; a service inside Wheelhouse's own host would not.
- Products are served by their own controller, so integrations read products and their metadata without deployment
  concepts; a separate products app stays an option.

---

## Points

- [ ] B1 — Unit of separation: repository, project in a shared repository, or service inside an app
- [ ] B2 — Instance model per app: one shared instance, one per product, or one per environment
- [x] B3 — Product catalog: Wheelhouse owns identity in code (runner `catalog.py`); other apps read
  `/api/products` with a scoped integration key (built 2026-09-30)
- [ ] B4 — Issues hub: the GitHub projects dashboard, label automation and AI triage, and its line with Feedbacks
- [ ] B5 — Feedback intake: product report → Feedbacks → GitHub issue, and who owns the issue
- [ ] B6 — Sign-in across internal apps: the Identity app or per-app GitHub OAuth
- [ ] B7 — Integration style: webhooks and events between apps, or direct API reads
- [ ] B8 — Data ownership: one source of truth per fact, read models elsewhere

---

## Test for each app (draft)

- Deploys on its own cadence, with its own blast radius.
- Runs as more than one instance (per product or per environment).
- Holds data or secrets that need their own boundary.
- Serves more than one app or product.
- Is worked by its own lane without touching another app's files.

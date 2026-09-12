# Banner

*Last updated: 2026-09-10*

> The app-wide strip — one note pinned across the top, above everything routed below it.
> What a feedback component is → [feedback](../../constructs/visual/feedback.md).

## Reach for it when

- must report a condition affecting the whole app — an outage, a trial ending
- must be mounted by the shell, full-width, above the routed content
- should carry its actions on the right; the row is centred, not stacked

---

## Instead of

| Reach for | When |
|---|---|
| [Alert](alert.md) | the condition belongs to one section rather than the app |
| [BannerSimple](bannerSimple.md) | the strip's body is free-form |
| [Toast](toast.md) | the note is transient and follows an action just taken |
| [StatusIndicator](statusIndicator.md) | the report is a health dot and a line, not a strip |

---

## Values

- should keep the copy to one line — `description` sits beside the title, not under it

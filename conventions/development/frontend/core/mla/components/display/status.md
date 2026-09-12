# Status

*Last updated: 2026-09-10*

> A coloured dot with its label beside it — a named state, said plainly.
> Kind → [indicator](../../constructs/visual/indicator.md).

## Reach for it when

- must name a live state — online, degraded, building, failed
- must carry the word beside the dot; colour alone never carries the meaning
- should sit in a [MetaInline](metaInline.md) row beside other meta

---

## Instead of

| Reach for | When |
|---|---|
| [NotificationDot](notificationDot.md) | the dot stands alone with no label |
| [Badge](badge.md) | a filled pill reads better than a dot in that row |
| `Alert` | the state needs an explanation, not a label |

---

## Values

- should leave `size` at `md`
- should set `hasPulse` only while the state is actively changing

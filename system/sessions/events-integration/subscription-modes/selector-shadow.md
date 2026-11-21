# Selector shadow log — `ocharo-events` vs `ocharo-fashion-v1`

*Started 2026-11-20 by `ev-build`. Procedure: harvest `engineering/development/subscription-selectors.md` § Shadow.*

Each run is `subscriptions diff --subscription ocharo-events --tenant ocharo --against ocharo-fashion-v1 …` through
Wheelhouse Run on harvest-dev. The cutover needs at least three daily rows, with pending at 0 or explained.

## Setup

- 2026-11-20 ~01:45Z, harvest-dev `v0.2.40` (`cefb5c8`), migration journal at `018-subscription-selectors`.
- Preconditions held: Afisha, ANONS, CAEx and Uzexpocentre sources read `auto`; all 150 live Ocharo posts carry
  `post-tags@2` SmallModel tags, `timeframe:` included (136 `type:event`, 14 `type:none`).
- `ocharo setup --group afisha --group anons --group caex --group uzexpocentre --selector` exited 0 in 7 s:
  `ocharo-events` subscription `01a1f58e-2a98-72a6-a5ec-d6c41c25ca19`, selector version 1. Its backfill judged 150
  posts: 9 `post.new`, 0 pending.

## Runs

| Date | Since | Posts | Both | Filter only | Selector only | Neither | Pending | Out of scope |
|---|---|---|---|---|---|---|---|---|
| 2026-11-20 | 2026-09-01 | 150 | 7 | 10 | 2 | 131 | 0 | 0 |
| 2026-11-21 | 2026-11-20 | 440 | 4 | 3 | 0 | 433 | 0 | 0 |

### 2026-11-20 (day 0)

Filter only (the old filter passes, the selector holds):

| Title (en) | Clauses | Timeframe | Reading |
|---|---|---|---|
| Zurab Tsereteli exhibition "Bigger than Life" | `no-subject` | upcoming | art show, filter false positive |
| CAEx Build & Co 2026 Exhibition | `no-subject` | upcoming | construction fair, filter false positive |
| 31st Tashkent International Fair "Tourism on the Silk Road" (TITF 2026) | `no-subject` | upcoming | tourism fair, filter false positive |
| CAEx Baraka Friday 2026 | `no-subject` | upcoming | retail sale, filter false positive |
| International Circus Arts Festival "Great Silk Road" | `no-subject` | upcoming | circus, filter false positive |
| 17th Central Asia International Exhibition "Textile Equipment & Technologies" | `exclude-timeframe:past` | past | ran 8-10 Sep 2026 |
| International Exhibition Heimtextil Uzbekistan 2026 | `exclude-timeframe:past` | past | October textile week, no extraction |
| International Exhibition Texworld Tashkent 2026 | `exclude-timeframe:past` | past | ran 12-14 Oct 2026 |
| International Exhibition Apparel Sourcing Tashkent 2026 | `exclude-timeframe:past` | past | ran 12-14 Oct 2026 |
| UZCHARMEXPO EURASIA 2026 | `exclude-timeframe:past` | past | ran 12-14 Oct 2026 |

Selector only (the selector passes, the old filter dropped):

| Title (en) | Clauses | Timeframe |
|---|---|---|
| Family Fashion Day at TRC Riviera | `type:event`, `domain:style-fashion`, `topic:clothing`, `topic:fashion-show` | upcoming |
| 10th International Specialized Exhibition of Motherhood & Childhood (KinderExpo 2026) | `type:event`, `domain:style-fashion`, `topic:clothing` | upcoming |

Delivered by the selector (9): The Fashion Show Line 2026 (two posts), Family Fashion Day at TRC Riviera, the
"Yalt-Yult" exhibition at the ICHKARI museum (`topic:textile`), Viza Fashion Week in Uzbekistan, KinderExpo 2026,
TFT EXPO International Fashion & Textile Exhibition, Visa Fashion Week Tashkent SS'27, and an exclusive furniture
exhibition-sale at Artikul32 (`topic:textile`, `topic:ikat`, `topic:suzani`).

Notes:

- Every beauty expo (Beautyworld Tashkent ×3, the 20th beauty-industry exhibition) sits in "neither": no clothing topic,
  so `except:style-fashion/beauty` holds them, and the old filter dropped them too.
- Texworld is held as a past event (its 2026 edition ended 14 Oct), as D23 intends; the spec's done-when line that
  names Texworld predates that amendment. Visa Fashion Week and TFT Expo deliver; CAEx Build & Co is held.
- To watch: the Artikul32 furniture sale passes only on ikat and suzani topics; it is textile-related, but not fashion.

### 2026-11-21 (day 1)

- ~01:53Z, harvest-dev `v0.2.61`, selector version 3: Wave 1 (25 generic-route channels) and Wave 2 (10 Telegram
  channels) joined the followed publishers through `ocharo setup --selector --selector-reset` on 2026-11-20, so the
  window holds 440 posts against day 0's 150.
- Filter only (3): one idem.uz post, "International Circus Festival. The Great Silk Road", counted three times
  (`no-subject`, upcoming). It is a circus festival, not fashion, so the selector's hold is right and the old filter
  passes a false positive.
- Both (4) are not itemised by the verb; selector only 0; pending 0; filter undecided 0.

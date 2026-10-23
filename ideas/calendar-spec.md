# Almanac — A Readable Day Calendar Beside the Chat

*Last updated: 2026-10-23*

> Proposed `wow-two-apps.almanac` (working name) — a read-only calendar view built for the Claude desktop app's
> built-in browser pane: chat on the left, the day on the right, every block readable at pane width, and the 10x
> system's questions about the calendar answered on screen. Google Calendar stays the source of truth; edits keep
> going through the chat and its Google Calendar connector.
>
> **Deadline:** v1 by `2026-11-15` (user, `2026-10-23`). Built in its own chat from this spec. Until then Google
> Calendar runs in the pane as is. **Order:** outside [platform apps](../docs/platform-apps.md) and the venture
> product order — a personal app, like Home Atlas. Task: `app-t-006`.

## Problem

- Google Calendar in the built-in pane (~800 px wide) is unreadable for this calendar:
  - week view cuts titles after a few letters;
  - day view turns 15-minute blocks into one-line slivers;
  - the evening pile-up of 2026-10-23 (~14 events, 9:15–11:30 PM) renders as fragments: `Work on de`, `Search for`, `Review PR`.
- It knows nothing of the 10x system: categories, tasks, day logs, prayers, overlap load, moved recurring instances.
- Notion Calendar was dropped on 2026-10-23. Edits go through the chat; the missing piece is a view worth reading.

## How the calendar is used today

Paths are relative to `10x-ws` (`~/Projects/10x-ws`).

| Workflow | What it does with the calendar | Where |
|---|---|---|
| Daily multi-vector planning (`pln-10x`) | Places blocks for all four vectors (10x, eis, w2, mft); Claude lists moves, the user approves, Claude applies them through the connector | `system/sessions/multi-vector-planning/` |
| Ventures planning | Decides which venture and task fills each Ventures block | `system/sessions/ventures-planning/` |
| Day logs | Calendar → `draft` log → `final` after the user checks the calendar | `.claude/skills/parse-day/SKILL.md` § Google Calendar source |
| Morning brief | Day terrain, meetings, overlap clusters, hours per category, three acts, tasks, yesterday's log | `system/sessions/morning-brief/` |
| Repair | Notion Calendar moved past recurring instances; a year-wide diff against final logs, via an ICS export, is pending | this chat's backlog |
| Monthly review | Reads the day logs, so indirectly the calendar | `system/sessions/monthly-review/` |

## Calendar conventions the app reads

### Calendars and time

- Calendars: primary (`Sultonbek Rakhimov`), `Family` (shared with family), `Tasks`, `Birthdays`, `Holidays in Uzbekistan`.
- Timezone: `Asia/Samarkand` on the calendar, `Asia/Tashkent` on most events — both GMT+5, no DST.
- Days split at sleep, not at midnight: a block after midnight and before sleep belongs to the previous day
  (2026-10-22 ends with a 11:45 PM–12:30 AM DevQA check).

### Title tags → category

`{title} - {tag}`; the tag is stripped from the displayed title and becomes the category.

| Tag | Category |
|---|---|
| `Project EBSCO` | `car` |
| `Life` | `life` |
| `Finance` | `fin` |
| `Planning` | `pln` |
| `ocharo-ws` | `ven` |
| `10x-{x}` | `{x}` — `gro`, `rel`, `hea`, `eng`, `fam`, `ven` seen |
| none | `life` |

- Title overrides: `Gym session` → `hea`, `Family discussion` → `fam`.
- Source of truth for the mapping: `split_tag()` in `system/sessions/morning-brief/morning-brief-build.py`.
- Tags arrive as typed: match case-insensitively (`LIfe` occurs); a missing space before the dash occurs too (`follow ups- Project EBSCO`).

### Colors (observed 2026-10-23)

| `colorId` | Google name | Used for |
|---|---|---|
| `11` | Tomato | `Project EBSCO` |
| `3` | Grape | `10x-gro`, `10x-rel`, `10x-eng`, `10x-fam` |
| `10` | Basil | `10x-hea` |
| `8` | Graphite | `Life` |
| none | calendar default | meals, ad-hoc events |

The app colors by category; `colorId` is a hint only.

### Block kinds

| Kind | Recognized by |
|---|---|
| Meeting | `conferenceData`, more than one attendee, or titles `DSU`, `Dev Sync`, `BLR`, `Demo`, `Retro`, `1-1 …`, `… meeting …` |
| Prayer | `Fajr`, `Zuhr`, `Asr`, `Maghrib`, `Isha` tagged `10x-rel`; also `Handle missed prayers` |
| Rest | `Have a rest`, `nap`, `sleep` |
| Travel | `On my way to …` |
| Meal | `Breakfast`, `Lunch`, `Dinner` |
| Recurring routine | `Review PRs`, `Prep for next iteration`, `Health treatment`, `Daily multi-vector planning`, `DSU preparation` |

- Descriptions hold HTML bullet lists (pill reminders) and Teams join links.
- Recurring instances carry `recurringEventId` and `originalStartTime`; the Notion Calendar damage shows as an
  instance whose start differs from its series time, edited after its day ended.

## Scope v1 — by 2026-11-15

### Views

1. **Day** (default) — one column tuned for the ~800 px pane. A 15-minute block always shows one full line of
   title. Hour height adjustable. Now line. Rest and sleep stretches collapse to a thin labelled band. The day
   runs from the first block to the sleep split.
2. **Agenda** — a list: time range · title · category · duration; overlapping events grouped under one header.
   The most readable view at narrow width.
3. **3-day** — compact columns; titles wrap to two lines; overlaps past the columns that fit collapse into a cluster.
4. **Week overview** — no blocks: per-day load terrain (the morning brief's ink stroke) and hours per category;
   a click opens that day.

### Readability rules — the core of the app

- Base font 15–16 px; a title gets at least one full line before an ellipsis.
- Overlap layout: column packing with a minimum column width (~160 px). Events that don't fit become a cluster
  chip — `4 at once · 9 events` — that expands in place. Never a sliver.
- Category shown as a color bar plus label, with AA contrast in dark and light themes; the theme follows the system.
- Event drawer: full title, tag, time, duration, recurrence and series time, description as sanitized text and
  bullets, links (https only), last updated.

### 10x overlays

- **Overlap clusters** per day: `9 events, up to 4 at once` — the brief template's maths (sweep with strict `<`,
  peak concurrency), with the worst cluster marked.
- **Moved recurring instances** on past days: start ≠ `originalStartTime` and `updated` after the day ended.
- **Duplicates**: the same recurring title twice on one day (`Prep for next iteration` on 2026-10-23).
- **Missing prayers**: any of the five without an event that day.
- **Hours per category**: planned (calendar) against logged (final day log), per day.
- **Log status** per day: none · `planned` · `draft` · `final`.
- **Tasks**: a block shows the Task ID its log row carries; a side rail lists tasks due today with no block,
  across the four task lists, ranked as the brief ranks them.
- **Brief header**: the day's headline and Needs-attention titles from `brief-YYYY-MM-DD.json`, linking to the page.

### Chat bridge

- **Copy for chat** on any event: `Work on CHLBN-2788 · Fri Oct 23, 5:00–6:30 PM · id 22a63e4b…` for pasting
  into a change request.
- `POST /api/sync`: the chat calls it after an edit (`curl` on localhost), so the change shows within seconds.
- Keyboard: `t` today · `←` `→` day · `1` day · `2` agenda · `3` 3-day · `4` week · `/` search.

### Not in v1

Editing in the app · Outlook / Teams calendar overlay · month view · phone layout · notifications · more than one user.

## Data

### Sources

| Source | What | Path in |
|---|---|---|
| Google Calendar API | events of the five calendars | server-side read-only sync |
| 10x task lists (10x, eis, w2, mft) | open tasks, deadlines, priorities | ingest API |
| 10x day logs | rows, Task IDs, status | ingest API |
| Morning brief JSON | headline, attention, acts | ingest API |

### Google read path — recommended: read-only OAuth on the server

- Scope `https://www.googleapis.com/auth/calendar.readonly`, NuGet `Google.Apis.Calendar.v3`.
- `singleEvents=true` within a window (60 days back, 60 ahead, configurable); keep `recurringEventId`,
  `originalStartTime`, `updated`, `colorId`, `attendees`, `conferenceData`, `description`.
- Incremental sync with a `syncToken` per calendar; poll every 60 s plus `POST /api/sync`; full resync on `410 Gone`.
- The user creates the OAuth client in Google Cloud and runs the one-time consent. The refresh token lives in `.env`
  locally and in the Wheelhouse vault once deployed; Claude never handles it.
- ⚠️ A consent screen left in **Testing** for an external user type issues refresh tokens that expire after 7 days.
  Set it to **In production**; unverified is acceptable for one user, behind a warning screen.

Alternatives considered:

- **Snapshot push** — the chat posts the connector's `list_events` result to `/api/ingest/events`. No OAuth, but
  stale after any phone edit. Kept only as the P0 fixture loader.
- **Secret iCal address** — no OAuth, but no `colorId` and unverified freshness. Rejected.

### 10x overlay path — ingest API

- `POST /api/ingest/{tasks|logs|brief}` with a local token. Shapes reuse the brief builder's outputs: `ranked()`,
  `yesterday_log()` widened to any date, and the brief JSON.
- Exporter: an `export` subcommand in `morning-brief-build.py` (or a sibling script) posts after each brief build
  and after task or log edits. The same path works locally and deployed; no workspace mount.
- The brief JSON carries work mail and Teams text, so the app's data is private by default.

### Storage

SQLite on a named volume (the template's default): event cache, sync tokens, ingested overlays. Rebuildable —
drop the file and resync.

## Architecture

- **Repo:** `wow-two-apps.almanac`, scaffolded from `wow-two-sdk-beta.product-template` by the `create-repo`
  skill. `catalog.yml` entry: `kind: app`, `workspace: wow2-apps`, `deploy: none` until P3.
- **Backend:** .NET Clean Architecture per the template on `WoW2.Sdk.Beta.Be` (hosting, observability, mediator,
  data). Google sync runs as a hosted background service. Endpoints: `GET /api/days/{date}?span=`,
  `GET /api/agenda`, `GET /api/flags/{date}`, `POST /api/sync`, `POST /api/ingest/*`, `GET /api/health`.
- **Frontend:** Vue 3, strict TypeScript, Vite, Tailwind v4, `lucide-vue-next`, `@wow-two-beta/fe`.
- **fe SDK calendar vector** — new; `@wow-two-beta/fe` has no calendar, scheduler or timeline component today.
  - Essential slice for Almanac: `TimeGrid` (day / N-day), `EventBlock`, overlap layout (column packing +
    cluster), `NowLine`, `AgendaList`, time-axis and timezone utilities.
  - Completion pass after v1, per the dev cycle's vector completeness: week and month grids, resource lanes,
    all-day row, drag-create hooks, print. The form conventions `calendarPicker`, `dateInput` and
    `recurrenceEditor` already exist and stay separate.
- **Local run:** `docker compose up -d --build` from `engineering/deployment/`; `restart: unless-stopped`;
  `127.0.0.1:8231` (the template's sample uses 8221).
- **Built-in browser:** an attach-only entry in `10x-ws/.claude/launch.json` —
  `{ "name": "almanac", "url": "http://localhost:8231", "port": 8231 }` — so any 10x chat opens it with
  `preview_start {name: "almanac"}` beside the conversation.
- **Deploy (P3):** a Wheelhouse target once `app-t-001` ships. An auth gate comes first, because the data holds
  work meetings, health notes and brief text: Traefik basic auth or Cloudflare Access as the interim, Identity when
  it ships. Google push notifications (watch channels) become possible once the app has public HTTPS.

## Phasing

| Phase | By | Delivers |
|---|---|---|
| P0 | `2026-10-30` | Repo, Docker, day view from a fixture (a saved `list_events` result), readability rules, overlap layout, now line, `launch.json` entry; open in the built-in pane |
| P1 | `2026-11-08` | Read-only Google sync and `/api/sync`, agenda and 3-day views, event drawer, category legend and hours, overlap list, moved-instance and duplicate flags |
| P2 | `2026-11-15` | Ingest API and exporter; tasks rail, log status, planned-vs-logged hours, missing prayers, brief header; copy for chat; week overview |
| P3 | after v1 | fe SDK completion pass, Wheelhouse deploy behind auth, Outlook overlay, push notifications |

## Ship gate — v1

- At ~800 px, every event of 2026-10-23 (~40 events, the 14-event evening pile-up included) reads without hover.
- A change made in chat shows within 10 s after `POST /api/sync`, and within 60 s without it.
- The container comes back after a laptop restart, and one `preview_start` reopens it in the pane.
- Past days show their moved recurring instances as flags.

## Risks

| Risk | Mitigation |
|---|---|
| Refresh token expires after 7 days | Consent screen In production before first use |
| Evening pile-ups stay unreadable | Cluster chips show the load instead of hiding it; the overlap list names the worst cluster |
| Private data on a public host | Auth gate before any deploy |
| Scope creep into editing | v1 is read-only; edits stay in chat |

## Open questions

1. Name — `Almanac` is a working name: the navigator's time tables, a sibling to Wheelhouse.
2. Read path — read-only OAuth (recommended) or snapshot push only.
3. Editing — chat-only for good, or drag-to-move in a later version?
4. Default calendars — primary, Family and Tasks shown; Birthdays and Holidays as an all-day row?
5. Week overview — load terrain per day, or an hour-by-day heatmap?

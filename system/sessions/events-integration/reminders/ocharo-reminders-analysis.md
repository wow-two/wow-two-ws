# Ocharo reminders — design analysis

*Written: 2026-11-20 · read-only analysis, no repo changed*

> A scheduled reminder system for Ocharo: what exists, the model, where it lives, the first slice and the tasks.
> Asked (developer, 2026-11-20): "we'll build a different system for this, reminder system with a scheduler with
> select channels with configurations". "This" is OE05's "Deadline reminders" preset, dropped the same day
> ([track doc](../events-integration.md) #74).

## Verdict

- **Build Reminders as the first feature of a Notifications domain**, `wow-two-sdk-beta.notifications` (platform
  app #10), deployed as `notifications-dev` the way WoW2 Events runs as `events-dev`.
- A rule is a trigger, a selection, an audience and a list of channels, each channel with its own configuration.
  One scheduler and one once-only ledger serve every Ocharo service.
- Owners keep their items and answer the calendar's schedule feed (calendar CAL01), amended with facets, assignees
  and service-caller reads. Reminders read it at fire time, so a moved deadline or a skipped event needs no event from
  the owner.
- Identity stays the gateway to a person: Telegram today through app notices, email later. Notifications holds no
  address.
- OE05's preset is built (`TelegramDelivery.ts:65-86`) and was never created on dev. Slice 1 (R01–R08) deletes it and
  ships one Ocharo deadline rule through `@ocharo_dev_bot`.
- V07 digests are the `window` trigger kind; they move in after parity (R12), leaving one scheduler, one mute and one
  admin page.
- This replaces the calendar analysis's note that Events digests stay the reminder engine
  ([calendar analysis](../calendar/ocharo-calendar-analysis.md):308).

## Path prefixes and pins

Paths are relative to the `wow-two-ws` root (`dcacb86`); each repo's lines were read at the SHA named.

| Prefix | Path | SHA |
|---|---|---|
| `{ev}` | `workbench/wow-two-sdk-beta/wow-two-sdk-beta.events/engineering/codebase/events.backend-services` | `4deb80c` |
| `{fe-ev}` | `…/wow-two-sdk-beta.events/engineering/codebase/events.frontend-services/packages/fe-events/src` | `4deb80c` |
| `{id}` | `workbench/wow-two-sdk-beta/wow-two-sdk-beta.identity/engineering/codebase/identity.backend-services` | `0e3a085` |
| `{be}` | `workbench/wow-two-sdk-beta/wow-two-sdk-beta.be/engineering/codebase/wow-two-sdk-beta-be/src` | `86f7f67` |
| `{fe}` | `workbench/wow-two-sdk-beta/wow-two-sdk-beta.fe/engineering/codebase/wow-two-sdk-beta-fe` | `d6ddfbd7` |
| `{oc}` | `workbench/mfts-projects/ventures/ocharo-hq/ocharo-ws/workbench` | — |
| `{pl}` | `{oc}/ocharo-platform/engineering/codebase` (repo `ocharo-platform`) | `0f7bbf5` |
| `{oe}` / `{oe-fe}` | `{pl}/ocharo-events.backend-services` / `{pl}/ocharo-events.frontend-services/apps/web/src` | `0f7bbf5` |
| `{mkt}` / `{blog}` | `{oc}/ocharo-marketing/engineering/codebase/ocharo-{marketing,blog}.backend-services` | `1d565d1` |
| `{ci}` | `workbench/wow-two-platform/wow-two-platform.comms.infra` | `9baed6c` |

---

## 1. What exists

### Schedulers and job runners

| Piece | Where | Does | For reminders |
|---|---|---|---|
| Events digest scheduler | `{ev}/packages/Module/Digests/DigestScheduler.cs:13-52`, `DigestSchedulerPass.cs:19-54` | a `BackgroundService` polling every 30 s (`EventDigestsOptions.cs:13`); starts due occurrences, resumes runs whose lease passed | the pattern to reuse; Events items only |
| Occurrence math | `{ev}/packages/Module/Digests/DigestOccurrences.cs:47-111` | days × `HH:mm` in an IANA zone; a DST gap runs after the gap, a repeated hour once | lift to the be sdk (R02) |
| Run claim and ledger | `DigestRunner.cs:13-20`, `:216`, `:269-284`; `{ev}/packages/Module/Migrations/005-digests/Apply.sql:57` | one run per (digest, occurrence) across restarts and hosts; 5 min lease, 5 attempts, 6 h catch-up (`EventDigestsOptions.cs:17-24`) | the fire-ledger shape |
| be sdk periodic jobs | `{be}/Jobs/Core/core.md:1-41`, `WakeableSchedule.cs:40` | in-process interval passes, one process per job | the scheduler's tick |
| be sdk Hangfire | `{be}/Jobs/Hangfire/`; used by Desk's worker (`{pl}/brand-workspace.backend-services/BrandWorkspace.Worker/Configurations/HostConfiguration.Extensions.cs:74`) | durable jobs across replicas | not needed: the ledger gives once-only |
| Cron parser | `{be}/Foundation/Time/Parsers/ICronExpressionParser.cs:8` (Cronos) | 5- and 6-field cron | the `cron` schedule form |
| Ocharo jobs | Blog `{blog}/OcharoBlog.Infrastructure/Blog/ScheduledPublisher.cs:6-17`; Marketing `{mkt}/OcharoMarketing.Infrastructure/Deliveries/BackgroundServices/PublicationWorker.cs:10-11`, `AutomationRunner` (`{mkt}/OcharoMarketing.Api/Configurations/HostConfiguration.Extensions.cs:314`) | publish stories and posts, render drafts | they act on content; none reminds a person |
| Empty shells | `{be}/Jobs/Coravel/`, `{be}/Jobs/NCronJob/`, `{be}/Comms/Core/`; `{ci}` holds only `src/Backbone.Comms.Infra.sln` | nothing | no home |

### Channels and delivery

| Piece | Where | Does | Gap |
|---|---|---|---|
| Identity app notices (I01) | `{id}/packages/Abstractions/Notices/IAppNoticeBroker.cs:19-25`, `AppNotice.cs:6-31`, `AppNoticeConstants.cs:10-16` | one person's linked Telegram chat; HTML ≤ 4,096 characters, ≤ 8 link buttons, once per idempotency key per app; scope `identity.notices.send` | personal chats only |
| Notice mutes | `{id}/packages/Module/Notices/IdentityNoticeMute.cs:3-20`, `AppNoticeService.cs:50-51`, `:118-121` | the mute button mutes the sending client; `/stop` mutes every client | no per-rule mute (R10) |
| Members read | `{id}/packages/Abstractions/Members/IMemberBroker.cs:23`, `MemberModel.cs:6-19` | `sub`, role and `HasTelegramLink` per member; scope `identity.members.read` | — |
| Identity email | `{id}/packages/Module/Core/Emails/EmailDeliverySettings.cs:5-22` | account mail over SMTP | no app route; Ocharo sets no `Identity:Email` (`{oc}/ocharo-platform/engineering/deployment/deploy.yml:162`) |
| Events Telegram adapter | `{ev}/packages/Module/Digests/Telegram/IdentityTelegramDigestDelivery.cs:17-73` | maps notice answers to `sent`, `muted`, `not_linked`, `failed` with `RetryAfter` | Events-only |
| be sdk Comms | `{be}/Comms/Email/IEmailBroker.cs:4` (MailKit, SendGrid, SES, Postmark, Mailgun, ACS), `Comms/Sms/ISmsBroker.cs:7` (Eskiz, Twilio, Vonage, Plivo, ACS), `Comms/Push/IPushBroker.cs:7` (FCM, APNs, WebPush, OneSignal), `Comms/WhatsApp/` | stateless vendor brokers | no orchestration, no Telegram |
| be sdk webhooks | `{be}/Messaging/Webhooks/` (backlog `wow-two-sdk-beta.be/engineering/planning/backlog.md:53`) | signed outbound deliveries, durable subscriptions | — |
| Text templates | `{be}/Localization/MessageTemplateMapper.cs:7-11`; email layout `{be}/Comms/Email/Templates/templates.md:3-4` | `{Name}` and ICU plurals with CLDR rules | — |
| fe sdk notice UI | `{fe}/src/presentation/display/notificationCenterGroup/` (bell, panel, item), `notificationIndicator/`, `{fe}/src/foundation/notifications/Notify.ts` | a bell and panel over a client-side bus, "no storage, account or network wiring" (`NotificationCenterGroup.spec.md:11`); browser notifications | no server inbox |
| fe sdk schedule inputs | `{fe}/src/presentation/forms/cronInput/CronInput.vue`, `recurrenceEditor/RecurrenceEditor.vue:115`, `:125` | cron input with a plain-language preview; RRULE editor | — |

### Delivery configuration today

- A digest names one channel and one language: `{ev}/packages/Abstractions/Digests/DigestSpec.cs:4-37` (`Channel`
  `:13`, `Language` `:25`), with a schedule (`DigestSchedule.cs:6-16`), a selection (`DigestSelection.cs:15-48`) and
  recipients by `sub` or role (`DigestRecipient.cs:7-17`).
- The broker covers create, replace, delete, preview, send now and run history (`IEventDigestsBroker.cs:13-72`).
- Telegram turns on when `Events:Digests:Telegram:Identity` names an instance
  (`{ev}/service/Events.Api/Configurations/HostConfiguration.Digests.cs:16-49`; Events'
  `engineering/deployment/deploy.yml:167-171`).
- `fe-events` ships the editor: `{fe-ev}/admin/presentation/DigestsPanel.vue:24-42` takes defaults and the workflow,
  and `DigestEditor.vue:67-78` hides the channel choice when one is registered.
- Ocharo mirrors the routes for admins (`{oe}/OcharoEvents.Api/Delivery/Controllers/DigestsController.cs:20`, `:74`)
  and sets its weekly default (`{oe-fe}/domain/delivery/TelegramDelivery.ts:47-63`).
- Ocharo's Identity grants client 8 (`events`) `identity.notices.send` and `identity.members.read`
  (`{oc}/ocharo-platform/engineering/deployment/deploy.yml:401-411`, audiences `:206-214`); apps never talk to the bot
  (`{oc}/ocharo-platform/engineering/architecture/telegram-bots.md:5-12`).

### OE05's preset in code

- Built and released in Ocharo `v0.3.25`: `ocharoDeadlineReminder` (`{oe-fe}/domain/delivery/TelegramDelivery.ts:65-86`)
  runs daily at 09:00 Tashkent with `deadlineWithinDays: 7`, stages `shortlisted`, `applying`, `applied` (`:36`),
  `role:member`, `uz-Latn`, and is created switched off.
- The offer lives in `{oe-fe}/application/delivery/UseTelegramDelivery.ts:30-47` and
  `{oe-fe}/presentation/delivery/pages/TelegramDeliveryPage.vue:67-85`; tests in
  `ocharo-events.frontend-services/apps/web/tests/TelegramDelivery.test.ts:58-72`, `:215`.
- It relies on OE04's `Stages` and `ExcludeStages` (`DigestSelection.cs:42`, `:47`), built in Events `3aca62b` and
  pinned at `10.0.13-beta`.
- It was never created on dev, and the read-back is replaced (`ocharo-platform`
  `engineering/planning/version-track/v0.3/v0.3.md:162-168`).
- OE05's other half stays: the feed's "Show skipped and rejected" toggle and the default digest's `excludeStages`.

### Gaps

- No item-relative trigger: a digest fires on clock occurrences only, so "deadline within 7 days" re-lists one event
  every day.
- No per-channel configuration: one channel and one language per digest.
- No service caller reads Events (`wow-two-sdk-beta.events` `engineering/planning/backlog.md:97`), and the schedule feed
  (CAL01) is unbuilt.
- One mute per sending client: every reminder from one client mutes together.
- No in-app inbox; Ocharo collects no email (phone and Telegram sign-in only).
- Marketing's follow-up owner is free text of ≤ 100 characters, so it cannot address a person
  (`{mkt}/OcharoMarketing.Application/Inquiries/InquiryModels.cs:27-30`, `InquiryService.cs:118`).
- Identity stores no person language or time zone (`{id}/packages/Module/Core/IdentityUser.cs:15-72`).

---

## 2. Model

### Rule

```text
ReminderRule                       per organization (issuer, id), as digests are; a revision on every write
  name, enabled
  source        events | marketing | blog | brand          a registered schedule feed (R01)
  container     ocharo-fashion                             the feed's scope (Events: the catalog), when it has one
  kinds         [deadline]                                 feed item kinds: event, deadline, post, follow-up, story
  facets        { stage: [shortlisted, applying, applied] } source filters, listed by the source's descriptor
  estimated     false                                      items with estimated dates stay out
  trigger
    relative    { leads: [P7D, P3D, P1D, P0D], at: 09:00 } day items: (day − lead) at `at`; minute items: start − lead
    window      { schedule, within: P7D, newOnly: false }  one list per occurrence: the digest form
    schedule    { days, times } | { cron }                 read in `zone`
    zone        Asia/Tashkent
  audience      [ { role: member } | { subject } | { assignees, fallback: { role: member } } ]
  channels      [ { channel: telegram, enabled, language: uz-Latn, template?, quietHours?: { from, to } },
                  { channel: in-app, enabled } ]
  itemCap       20
  linkTemplate  https://{app}/organizations/{org}/events/{ownerId}    none: the feed item's url
```

### Trigger kinds

| Kind | Fires | Message | Example |
|---|---|---|---|
| `relative` | per item and lead, once per anchor value | one per person and fire instant, listing every item due then | deadline −7, −3, −1 and 0 days at 09:00 |
| `window` | at each schedule occurrence | one list per person | V07's Monday 09:00 digest |
| `once` (later) | at one instant | one | "remind me about this event tomorrow" from a card |

- An item's anchor is its feed start; a `deadline` item starts at its deadline
  (`{ev}/packages/Abstractions/CatalogEvents/EventDeadline.cs:4-17`).
- A month- or year-precision anchor never fires, since it names no day (`EventWhen.cs:4-15`).
- Reading the feed at fire time keeps rules current: a moved deadline is a new anchor value and fires on its new day,
  and a stage moved to `skipped` falls out of the facet filter.
- A fire inside a channel's quiet hours waits for their end and reads `deferred` meanwhile.

### Selection

- The source is a schedule feed: the windowed list of dated items each service answers
  ([calendar analysis](../calendar/ocharo-calendar-analysis.md) CAL01, `:227`).
- Reminders need 4 additions to CAL01's item sketch (`:201-223`):
  - `facets` per item, and a facet filter in the query (`stage`, `tracked`, `channel`, `status`);
  - a descriptor call listing each facet's key, labels and options, so one editor renders any source's filters;
  - `assignees` per item as Identity `sub`s, such as Events tracking's `Assignee`
    (`{ev}/packages/Abstractions/Tracking/TrackingModel.cs:21`);
  - service-caller reads for a named organization: a client-credentials token whose client the owner binds to
    organizations by configuration.
- `firstListedAtUtc` per item carries V07's "new since the last run" (R12).

### Audience

- `role`: Identity members holding it, `member` for everyone (`IMemberBroker.cs:23`); `HasTelegramLink` skips the
  unlinked before a send.
- `subject`: one person.
- `assignees`: each item's assignees, with a fallback for items that name none.
- A person named twice gets one message; the language falls back from the person to the channel, then `uz-Latn`.
- The rule's zone and the channel's language decide until preferences exist (R15).

### Channels and their configuration

| Channel | Exists | Address held by | Configuration per rule |
|---|---|---|---|
| `telegram` (personal chat) | yes: Identity app notices | Identity: the linked chat | enabled, language, template, quiet hours, open-item button |
| `in-app` | UI only: the fe sdk bell and panel | Notifications: an inbox row | enabled, days kept |
| `email` | Identity's SMTP for account mail; no app route | Identity: the confirmed email | enabled, subject and body templates |
| `telegram-group` | no: notices reach personal chats only | the organization's setting: chat and topic | topic, template |
| `webhook` | be sdk outbound webhooks; Events' V05 unbuilt | the subscriber | subscription, event name |
| `log` | Events' `log` digest channel (`DigestChannelConstants.cs:10`) | — | — |
| push, SMS, WhatsApp | be sdk brokers only | — | deferred to R09's inventory |

- Every channel sits behind one seam, as `IDigestDelivery` does
  (`{ev}/packages/Abstractions/Digests/IDigestDelivery.cs:10-21`); each channel validates its own configuration.
- Templates fill through `MessageTemplateMapper` with `{Title}`, `{Date}`, `{Days, plural, …}`; defaults ship in
  `uz-Latn`, `ru` and `en`.
- Ocharo's prod bot already sits in the workspace group as an admin with Manage topics (`telegram-bots.md:32`), which a
  `telegram-group` channel would use.

### Ledger

```text
reminder_fires        unique (rule, fire_at)              running | completed | partial | empty | missed | failed
reminder_fire_items   unique (rule, item, anchor, lead)   a lead fires once per anchor value
reminder_deliveries   key (fire, subject, channel)        pending | sent | not_linked | muted | deferred | failed
```

- Claims, leases, retries and the catch-up window follow the digests' rules (`DigestRunner.cs:13-20`).
- A delivery's idempotency key is `{fire}:{subject}:{channel}`; Identity sends one key once per app
  (`IAppNoticeBroker.cs:16-17`).
- Preview renders the next 14 days of fires and writes nothing; send test renders now and sends to the caller only.

### V07 digests

- A digest maps onto a `window` rule over the Events feed (`DigestSelection.cs:15-48`, `DigestSpec.cs:4-37`):
  - `NewSinceLastRun` → `newOnly`; `StartingWithinDays` and `DeadlineWithinDays` → `within` per kind;
  - `Stages`, `ExcludeStages`, `Kinds`, `Cities`, `TrackedOnly` → facets; recipients → audience;
  - `Language`, `ItemCap`, `LinkTemplate` → channel and rule fields.
- Kept apart, a person meets two systems: two mute buttons (clients `events` and `notifications`) and two admin pages.
- Folding them in after parity costs R12 (OQ-2).

---

## 3. Where it lives

### Options

| Option | Serves Marketing and the calendar's feeds | Fit | Cost |
|---|---|---|---|
| (a) Inside WoW2 Events: V07 gains item leads and per-channel settings | no: Events items only | Events keeps owning messaging; the developer asked for "a different system" | S |
| (b) Inside Identity's app notices | yes, by reading every feed | Identity owns people, addresses and mutes, but the auth core gains a scheduler and every service's items | M |
| (c) Notifications domain: be sdk feed contract, `wow-two-sdk-beta.notifications` module and service | yes | stateful and used by 2+ products, so a domain repo (`conventions/development/capability-forms.md:13-14`); platform app #10 (`docs/platform-apps.md:35`); D12 "build thin on SDK `Comms/`" (`docs/platform-decisions.md:35-36`) | M–L |
| (d) Per app | each app again | breaks SDK extraction; no rule spans sources | S × N |

### Recommendation

- **(c)**: Notifications decides what, when and to whom; owners answer feeds; Identity delivers to a person.

| Piece | Lives in | Task |
|---|---|---|
| Schedule feed contract: facets, descriptor, assignees, service-caller reads; conformance | be sdk `wow-two-sdk-beta.be` | R01 (CAL01 amended) |
| Zoned weekly schedule | be sdk `Foundation/Time` | R02 |
| Feeds | each owner: Events R03, Marketing R13, Blog and Brand R17 | — |
| Rules, triggers, scheduler, ledger, templates, channel seam, inbox, preferences | `wow-two-sdk-beta.notifications` module; service `notifications-dev` | R04, R05, R11, R15 |
| Personal channels: Telegram, later email | Identity app notices; addresses stay in Identity | R10, R14 |
| Admin parts | `@wow-two-beta/fe-notifications`; each app embeds them with its presets | R06, R08, R13 |
| Vendor adapters for later channels | be sdk `Comms/` | R09 |

### Form

- Start with the service form (Forms 2/3): rules span 2+ owners, so a host that is neither runs the schedule, and
  Ocharo already reaches WoW2 Events and Identity as services.
- Form 1, the module in a product's own process, ships from the same repo (`capability-forms.md:60`); the service
  hosts it (`:77`).
- Alternative: Form 1 inside WoW2 Events' host for slice 1. It skips R03's service caller and R07's new deploy, then
  moves Ocharo's rules out at the second source; Marketing is the developer's next system (#74), so the move comes at
  once.
- Starting app #10 now moves it ahead of #3–#9, which only the developer decides (`docs/platform-apps.md:13-18`);
  OQ-1 records it.

---

## 4. Slices

### Slice 1 — replaces OE05's preset on dev

- R01, R02 and R04 run at once; R03 follows R01; R05 follows R01, R02 and R04; R06 builds on R05's contract;
  R07 follows R03 and R05; R08 closes the slice.
- Lanes: be sdk (R01, R02), Events (R03), Notifications (R04–R06), Ocharo (R07, R08).
- Builders: Sonnet `xhigh` for R01, R03, R05, R06; `medium` for R02, R04, R07, R08.
- The slice is done at R08's dev read-back.

### Full vector

- R09's inventory comes first, per the vector-completeness rule (`conventions/development/dev-cycle.md:38`), then
  R10–R18 in the order it sets.
- OQ-4 orders the channels: R11 in-app, R14 email, R18 team group.
- R12 needs OQ-2; R13 opens with the developer's Marketing work.

---

## 5. Open decisions

### OQ-1 Home of the reminder system

- (a) inside WoW2 Events, the shared events service: its scheduled digests (V07) gain per-deadline leads and settings
  per channel; smallest, Events items only.
- (b) inside Identity's app notices, the route that sends a person a Telegram message through the bot; Identity would
  read every service's items.
- (c) a new Notifications domain repo, `wow-two-sdk-beta.notifications`, with its own service on dev, reading each
  service's schedule feed and sending through Identity; serves Marketing and the calendar's sources, and costs a new
  repo, image and deploy, moving platform app #10 ahead of #3–#9.
- Pick: (c).

### OQ-2 Events digests

- V07 digests are the weekly Telegram messages O17 set up for Ocharo: Monday 09:00, new events and near deadlines.
- (a) move them into the reminder system once its `window` trigger lists events the same way (R12), then delete
  Events' digests: one scheduler, one admin page, one mute button.
- (b) keep them in Events: two systems send Telegram to the same people, each with its own mute.
- Pick: (a).

### OQ-3 Ocharo's default deadline reminder

- It covers events the team marked shortlisted, applying or applied, with an exact deadline.
- (a) per deadline: 7, 3 and 1 days before and on the day, at 09:00 Tashkent, to the event's assignee (the teammate
  a tracked event names, OE11), else every member.
- (b) the dropped preset: every day at 09:00, one list of every deadline within 7 days, to every member.
- (c) both, with (b) created switched off.
- Pick: (a).

### OQ-4 Next channel after personal Telegram

- (a) in-app: a bell in every Ocharo app with a read list; needs no address, and the fe sdk has the bell.
- (b) email: Ocharo signs in by phone through Telegram only and sets no SMTP (`deploy.yml:162`), so it needs a provider
  (platform decision D13) and collected addresses first.
- (c) the team's Telegram group: one message to a topic of Ocharo's workspace group instead of one per person;
  Identity sends to personal chats only, so it needs a group route.
- Pick: (a).

---

## 6. Tasks

### R01 Schedule feed contract with facets and service callers
- Repo: `wow-two-sdk-beta.be`
- What: CAL01 as specced (`ScheduleItemModel`, `ScheduleWhen`, `ScheduleQuery` ≤ 92 days,
  `IScheduleFeedBroker.ListAsync`, route constant `schedule`), plus item `facets`, `assignees`, `ownerId` and `firstListedAtUtc`; a query facet filter
  (keys AND, values OR) and `organizationId` for service callers; `DescribeAsync` answering each facet's key, labels
  per locale and options; the conformance suite in `Testing`. It replaces CAL01: one contract, two readers.
- Done when: the suite passes against an in-memory fake, covering facet filters, the descriptor, the window cap and
  stable ids; a be sdk release carries it.
- Depends: —

### R02 Zoned weekly schedule in the be sdk
- Repo: `wow-two-sdk-beta.be`
- What: `ZonedWeeklySchedule` (days, `HH:mm` times, IANA zone) with `Next` and `Latest` and the DST rules of
  `{ev}/packages/Module/Digests/DigestOccurrences.cs:47-111`, under `Foundation/Time`; a zoned cron `Next` over
  `ICronExpressionParser`. Events keeps its copy until R12 deletes it.
- Done when: the cases of `Events.Tests.Unit/Digests/DigestOccurrencesTests.cs` pass against it (Monday 09:00 Tashkent
  is 04:00 UTC, a DST gap, a repeated hour); a be sdk release carries it.
- Depends: —

### R03 Events schedule feed for reminders
- Repo: `wow-two-sdk-beta.events`
- What: CAL02 as specced, with facets `stage` (the organization's tracking stage; untracked reads the default stage),
  `tracked`, `kind`, `status`, `deadlineKind`, `city`; `assignees` from tracking; `DescribeAsync` with the workflow's
  stage labels; service callers holding a new `events.schedule-read` scope, bound to organizations by
  `Events:ServiceCallers:{clientId}:Organizations` (backlog `:97`); the Client method. Backlog row "Reminders on
  deadlines" (`:88`) points to Notifications.
- Done when: R01's suite passes on the module and the image; an integration test has a client bound to organization A
  read A's feed with `stage: [applying]` and get only applying events' exact deadlines with their assignee, while
  organization B and an unbound client get 403 and a person token still reads.
- Depends: R01

### R04 Scaffold `wow-two-sdk-beta.notifications`
- Repo: new `wow-two-sdk-beta.notifications`; `wow-two-ws` (catalog; `docs/platform-apps.md` row #10 and its
  Decisions list)
- What: the `create-library` skill (`scripts/release/library.py plan`): repo, NuGet family
  `WoW2.Sdk.Beta.Be.Notifications.*`, `@wow-two-beta/fe-notifications`, image, catalog entry, Wheelhouse product
  `notifications-dev`; `product/product.md` from this analysis.
- Done when: the plan shows every step done; the empty packages are published; `notifications-dev` answers `/health`.
- Depends: OQ-1

### R05 Reminders core: rules, scheduler, ledger, Telegram channel
- Repo: `wow-two-sdk-beta.notifications`
- What:
  - contract: `ReminderRuleSpec` and `ReminderRuleModel` (#2), `IReminderRulesBroker` (list, get, create, replace,
    delete, preview, send test, list fires) for the caller's active organization, scope `notifications.admin`;
  - seams: `IReminderChannel` with outcomes `sent`, `not_linked`, `muted`, `deferred`, `failed`; `IReminderSource` over
    R01's client, one per `Notifications:Sources:{name}`; an audience resolver over Identity's `IMemberBroker`;
  - scheduler: a be sdk periodic job using R02; a rule with whole-day leads evaluates at its `at` occurrences, one with
    hour or minute leads every pass over [now − catch-up, now + its longest lead]; leads 0–90 days, at most 8;
  - ledger, claim, lease, retry and catch-up per #2; one message per person, channel and fire;
  - templates through `MessageTemplateMapper` with `uz-Latn`, `ru`, `en` defaults; quiet hours;
  - channels `telegram` (Identity `IAppNoticeBroker`, an open-item button) and `log`;
  - conformance on the Module and the Client, migrations, service routes.
- Done when: integration tests on a fake clock pass:
  - a deadline rule with leads 7, 3, 1, 0 at 09:00 Tashkent fires once per lead at 04:00 UTC and not again after a
    restart;
  - a deadline moved by a day fires on its new day only;
  - an item moved to `skipped` before its fire sends nothing;
  - two items due the same morning reach a person in one message;
  - a fire inside quiet hours goes out at their end;
  - a person without a Telegram link reads `not_linked`;
  - the preview's text equals the sent text.
- Depends: R01, R02, R04

### R06 `fe-notifications` admin parts
- Repo: `wow-two-sdk-beta.notifications` (`notifications.frontend-services`)
- What: `RemindersPanel` (list, enabled toggle, next fire), `ReminderEditor` (source and kinds; facet pickers from the
  descriptor; trigger as leads and time, or a window; audience as roles, people, assignees with a fallback; one tab per
  registered channel with enabled, language, template, quiet hours), `ReminderPreview` (fires of the next 14 days with
  their text), `ReminderFires` (history with each recipient's result); a `presets` prop as `DigestsPanel` takes
  `defaults`; uz, ru, en; one base URL per `capability-forms.md:45`.
- Done when: vitest shows the stage picker built from a described facet, a saved relative rule posting leads
  `[P7D, P3D, P1D, P0D]` at `09:00`, tabs only for registered channels, and the preview listing the fires the API
  returns; typecheck and lint pass; the package is published.
- Depends: R05's contract

### R07 Wire Notifications for Ocharo on dev
- Repo: `ocharo-platform` (Identity declaration, `deploy.yml`), `wow-two-sdk-beta.events` and
  `wow-two-sdk-beta.notifications` (dev settings)
- What: Ocharo's Identity gains resource `notifications` (`notifications.admin`) and client `notifications` with
  `identity.notices.send`, `identity.members.read` and `events.schedule-read`; client 11 (`ocharo-events`) may exchange
  a person's token for the `notifications` resource; Events binds client `notifications` to Ocharo's organization;
  `notifications-dev` takes Ocharo's issuer, its token endpoint and the `events` source's base URL.
- Done when: on dev `config check` passes, a rule preview lists Ocharo's tracked deadlines, and a send test reaches the
  owner's `@ocharo_dev_bot` chat.
- Depends: R03, R05

### R08 Reminders page replaces the preset in Ocharo's Events app
- Repo: `ocharo-platform`
- What: an admin page "Reminders" (`/organizations/{id}/reminders`) embedding `RemindersPanel` through a pass-through
  mirror shaped like `{oe}/OcharoEvents.Api/Delivery/Controllers/DigestsController.cs:20` (admins only, `:74`); the
  preset per OQ-3; delete `ocharoDeadlineReminder`, `ocharoDeadlineReminderName`, the offer
  (`UseTelegramDelivery.ts:30-47`, `TelegramDeliveryPage.vue:67-85`) and its tests; menu entry; version track.
- Done when: vitest finds no reminder offer on the Telegram delivery page and the Reminders page creating the preset
  once; on dev the preset is created and switched on, its preview lists Ocharo's pursued events with exact deadlines in
  the next 7 days on their lead days, a send test arrives with a working link to the Events app, and the next 09:00
  Tashkent fire shows in history with each recipient's result.
- Depends: R06, R07, OQ-3

### R09 Notifications completeness inventory
- Repo: `wow-two-sdk-beta.notifications`
- What: `engineering/research/notifications-completeness.md`: channels (#2's table), preferences, digests, batching,
  snooze and acknowledge, manual "remind me", escalation to a second person, a calendar layer of upcoming fires,
  delivery metrics; each with ship-now, defer with a named trigger, or skip with a reason.
- Done when: every row carries a verdict, and the repo backlog's `Vectors` group lists the vector.
- Depends: R05

### R10 Topic mutes on Identity's app notices
- Repo: `wow-two-sdk-beta.identity`
- What: optional `AppNotice.Topic` (≤ 64 characters); the mute button mutes (client, topic); `/stop` still mutes every
  client; Notifications passes the rule id and name.
- Done when: integration tests with `FakeTelegramBotClient` show a muted topic A leaving topic B and topic-less notices
  arriving, `/stop` muting both, and a bare `/start` lifting both.
- Depends: —

### R11 In-app channel and bell
- Repo: `wow-two-sdk-beta.notifications`; `ocharo-platform` for the embed
- What: an inbox store (person, organization, rule, items, text, link, read time); `GET` and `POST` `me/inbox` with
  `notifications.read`; a push over be sdk `Realtime/Sse`; channel `in-app`; `NotificationsBell` over the fe sdk's
  `NotificationCenterButton` and `NotificationCenterGroup` with a server-backed bus; Ocharo's apps show it in their
  header.
- Done when: an integration test writes one inbox row per person for an `in-app` fire, keeps read state and pushes a new
  row; vitest drops the bell's count on read; on dev the Events app's bell shows a send test.
- Depends: R05, OQ-4

### R12 Digests become reminders
- Repo: `wow-two-sdk-beta.notifications`, `wow-two-sdk-beta.events`, `ocharo-platform`
- What: `window` parity with V07 (`newOnly` from `firstListedAtUtc`, `within` per kind, item cap, list text with dates
  at their precision, city and nearest deadline as `DigestText.cs:8-9`); a one-off verb migrating each Events digest
  into a rule; O17's page embeds `RemindersPanel`; Events deletes `Digests/`, its migration set entry, `fe-events`'
  digest parts and its `identity.notices.send` grant.
- Done when: a parity test renders a migrated digest and Events' preview to the same text on the same clock; on dev the
  migrated Monday 09:00 rule delivers once; Events' packages hold no `Digests/` folder.
- Depends: R05, R08, OQ-2

### R13 Marketing feed and reminders
- Repo: `ocharo-marketing`
- What: CAL03 amended: `post` items with `channel` and `status` facets, `follow-up` items at `FollowUpAt`; the follow-up
  owner becomes an Identity `sub` picked from members; bearer reads for service callers bound to Marketing's
  organization; a Reminders page embedding `RemindersPanel` with Marketing presets (follow-ups due today to their owner,
  tomorrow's planned posts to editors).
- Done when: R01's suite passes; an integration test sends a follow-up due tomorrow to its owner only and refuses
  another organization's token; on dev a Marketing send test arrives.
- Depends: R01, R05, R07

### R14 Email on Identity's app notices
- Repo: `wow-two-sdk-beta.identity`, `wow-two-sdk-beta.notifications`
- What: `AppNotice.Channel` (`telegram` by default, `email`) with a subject and an HTML body, sent over Identity's SMTP
  to the confirmed email; Notifications' `email` channel with subject and body templates in be sdk's email layout.
- Done when: integration tests with a fake SMTP send once per key to a confirmed address, read `not_linked` for an
  unconfirmed one and `muted` for a muted topic.
- Depends: R10, OQ-4; for Ocharo, an SMTP provider (D13) and collected addresses

### R15 Person preferences
- Repo: `wow-two-sdk-beta.notifications`
- What: per person and organization: channels per rule, quiet hours, language, time zone, one daily batch; a "My
  reminders" part; deliveries read them first and record `skipped`.
- Done when: tests show a person who turned Telegram off for rule A getting A in-app only, their quiet hours deferring
  only their copy, and the batch sending one daily message with every rule's items.
- Depends: R11

### R16 Webhook channel
- Repo: `wow-two-sdk-beta.notifications`; `wow-two-ws` (V05's spec)
- What: channel `webhook` over be sdk outbound webhooks; a rule's configuration names a subscription; V05's
  `deadline.approaching` becomes a reminder rule, and V05 keeps change events only.
- Done when: an integration test posts one signed delivery per subscription for a fire, retries a 500 and verifies the
  signature.
- Depends: R05

### R17 Blog and Brand feeds
- Repo: `ocharo-marketing` (Blog), `ocharo-platform` (Brand)
- What: CAL07's feeds answer R01: scheduled stories at `PublishAt`, appearance windows; service-caller reads.
- Done when: R01's suite passes in both; on dev a rule over Blog's scheduled stories previews.
- Depends: R01

### R18 Team Telegram group channel
- Repo: `wow-two-sdk-beta.identity`, `wow-two-sdk-beta.notifications`
- What: an organization registers its workspace group chat and topic in Identity; a notice route to that topic; channel
  `telegram-group`.
- Done when: an integration test with the fake bot delivers a group notice to the registered topic once per key and
  answers 404 for an unregistered chat.
- Depends: OQ-4 (c)

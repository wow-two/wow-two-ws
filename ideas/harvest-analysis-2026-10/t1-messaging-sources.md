# T1 — Messaging sources

*Last updated: 2026-10-26*

> Telegram and WhatsApp as Harvest source families: which source kinds exist, which access route reaches each, what
> each route returns (history, edits, deletions, media, metadata), what it costs and risks, and what Harvest must
> model to run an account pool. Telegram has four read routes (Bot API, MTProto user client, web preview, provider
> API) plus consent-based intake (forward, guest mention). WhatsApp has one official read route that sees only
> chats with our own number, and an unofficial linked-device route. Two findings move the spec most: Telegram's 2026
> terms bar using its data for AI, which collides with LLM extraction; and WhatsApp offers no compliant way to read
> Channels or existing groups.

Legend: **(U)** = could not verify. `[key]` = entry in § Sources. **probe** = my own plain `GET` of a public page on
2026-10-26 (about 45 requests, no account, no client run, no 429 seen). All pages read 2026-10-26; prices as shown
that day. Route codes — Telegram: **B** Bot API · **M** MTProto user client · **W** web preview `t.me/s` · **P**
provider API · **F** forward / mention intake. WhatsApp: **C** Cloud API · **H** public channel web page · **L**
linked-device (unofficial) client · **F** forward intake.

---

## 1. Source kinds

| Kind | What it is | Routes that reach it | Notes |
|---|---|---|---|
| TG public channel | one-way posts at `t.me/{username}` | W · M · P · F; B only if we administer it | `t.me/s/{username}` previews it without an account (probe) |
| TG public group / supergroup | many-to-many chat at `t.me/{username}` | M · F; B only if an admin adds the bot | `t.me/s/{username}` answers `302` to `t.me/{username}`: no history preview (probe, `pythontelegrambotgroup`) |
| TG forum topics | supergroup with topics; General topic `id=1`, others are the thread of their creation message `[tg-forum]` | M · B (in a group where the bot sits) | M: `messages.getForumTopics`; TDLib `getForumTopics` + `getMessageThreadHistory` `[td-schema]`; B: `message_thread_id`, `is_topic_message` `[bot-api]`; W: none |
| TG channel discussion group (comments) | a linked supergroup; each post is auto-forwarded into it and the comments are replies to that copy `[tg-discuss]` | M · B (bot inside the group sees `is_automatic_forward` copies and replies) | M: `messages.getDiscussionMessage`; reading comments needs no membership `[tg-discuss]`; deleting the forwarded copy disables comments; W exposes no comment count (probe, 5 channels) |
| TG private channel / group (invite link) | `t.me/+{hash}`; may require admin approval | M · F; B only if an admin adds the bot | `messages.checkChatInvite` → preview, `importChatInvite` → join; `request_needed` links answer `INVITE_REQUEST_SENT` and wait for an admin `[tg-invites]`; `chatInvitePeek` gives temporary read-only access to some channels `[tg-invites]`; W: `/s/+hash` answers `302` to the invite page, which shows title, description and subscriber count only (probe) |
| WA Channel | one-way broadcast at `whatsapp.com/channel/{id}` | H · L · F | no official read API; Meta Content Library is research-only `[wa-cl]` |
| WA group | invite-link chat | L · F; C only for groups our number created | Groups API: ≤8 participants, no joining existing groups `[wa-groups]` |
| WA Business number | Harvest's own number; users message it | C · F | the only fully official route; inbound is free `[wa-pricing]` |

- A brand can expose one Telegram channel under two links: Domtut's site links an invite URL `t.me/+…`
  (14,676 subscribers on the invite page), and the same channel is public as `@domtutuz` (14.7K, 17 post bubbles
  previewable) (probe). Resolve an invite to a public username before choosing a route; matching is by title and
  subscriber count, a heuristic (U).

---

## 2. Telegram access routes

### 2.1 Reach and history

| Attribute | B · Bot API | M · MTProto user client | W · web preview | P · TGStat API |
|---|---|---|---|---|
| Reads | chats the bot belongs to: channels where it is a member (`channel_post`), groups where it was added, private chats `[bot-faq]` | everything the account can see: public chats by username, joined chats, invite previews | public channels with preview enabled; groups and invites unsupported (probe) | channels in TGStat's catalog (3.18M channels, 8 languages) `[tgstat-api]`; Uzbekistan coverage not itemised on the page (U) |
| Account / session | bot token from BotFather; no phone on our side | phone number + login code (+ 2FA), `api_id`/`api_hash`, a session per account `[api-id]` `[wtc]` | none | tariff token `[tgstat-docs]` |
| History backfill | none: no history method; `getUpdates` keeps unconfirmed updates ≤24 h `[bot-api]` | full: `messages.getHistory` (users only) `[tg-gethist]`; TDLib `getChatHistory`, ≤100 per call `[td-schema]` | whole channel, random access: `?before={id}`, 20 posts per page; `before=1000` returned 2020 posts (probe) | by plan: 3 days (free), 60 (S), 180 (M), 365 (L), full (XL) `[tgstat-api]` |
| Membership | the bot must be added; privacy mode on by default, off for admins `[bot-feat]` | public: not for update polling `[tg-updates]`, history without join (U); private: join, or `chatInvitePeek` | none | none |
| Fit for | channels the consumer owns; intake | groups, topics, comments, private chats, deletion by id | public channels, no account to ban | discovery and stats, not content |

### 2.2 Per-post data

| Attribute | B | M | W | P |
|---|---|---|---|---|
| Edit detection | `edited_channel_post`, `edited_message` push; `edit_date` on `Message` `[bot-api]` | `updateEditChannelMessage` for joined chats `[tg-updates]`; TDLib `updateMessageEdited` + `updateMessageContent`; or re-read by id | `edited` marker without edit time; detect by content hash on re-fetch (probe) | not stated (U) |
| Deletion detectability | no delete update for channels or groups; only `deleted_business_messages` for connected business accounts `[bot-api]`; an existence probe by `copyMessage` into a sink chat works only inside chats the bot belongs to (U) | push: `updateDeleteChannelMessages` (joined) `[tg-updates]`, TDLib `updateDeleteMessages{is_permanent, from_cache}`; by id: `channels.getMessages` returns `messageEmpty` (non-existent message) `[tg-chgetmsg]` `[tg-msgempty]`, TDLib `getMessages` returns `null` per missing id | by id: `t.me/{ch}/{id}?embed=1&mode=tme` answers HTTP 200 with "Post not found" (probe: `durov/549`, `durov/550`); id gaps in a listing are ambiguous (probe below) | Callback API can notify deleted publications `[tgstat-docs]`; freshness (U) |
| Media | `getFile` ≤20 MB; local Bot API server (BSL-1.0): download unlimited, upload 2000 MB `[bot-api]` `[bot-local]` | ≤2 GB per file, 4 GB with Premium (file parts × 512 KB) `[tg-config]`; `file_reference` expires `[tg-fileref]`; download can hit `FLOOD_PREMIUM_WAIT` | photos as CDN URLs in `style`, short videos as `<video src=…mp4?token=…>`, others a placeholder "VIEW IN TELEGRAM" (probe) | not stated |
| Metadata | no `views`, no forward count in `Message` (grep of the API page); reactions only via `message_reaction_count`, admin + `allowed_updates`, delayed up to minutes; `forward_origin` (`MessageOriginChannel{chat, message_id}`), `is_automatic_forward`, `author_signature`, `media_group_id` `[bot-api]` | TDLib `messageInteractionInfo{view_count, forward_count, reply_info, reactions}`, `messageForwardInfo.origin` `[td-schema]`; MTProto message has the same fields | views (abbreviated), per-emoji reaction counts, ISO `datetime`, author signature, forwarded-from name with a link to the origin post when public (`tginfoen` → `t.me/betainfoen/2336`), link preview; no reply count, no polls seen (probe) | reach, views over time, mentions, reposts, subscribers; per-field list not documented (U) |

- Listing gaps are not deletions: `afishauz` ids 34111, 34112, 34118 were missing from the list but exist as members
  of an album (embed answers "found"); `durov` 549/550 answer "Post not found" (probe).
- The embed of a missing id returns the same page for a deleted post and for an unavailable channel; check the
  channel (`/s/{ch}`) before declaring posts gone (probe, U for the private case).

### 2.3 Limits, risk, cost

| Attribute | B | M | W | P |
|---|---|---|---|---|
| Rate limits | send side: ~1 msg/s per chat, 20/min per group, ~30/s broadcast `[bot-faq]`; `getUpdates` ≤100 per call | no numbers published; `FLOOD_WAIT_X`, `FLOOD_PREMIUM_WAIT_X` `[tg-errors]`; joined chats 500 default, 1000 Premium `[tg-config]`; polling non-joined channels ≤10 at once `[tg-updates]` | none published, no `robots.txt` (`404`); ~45 requests without a 429 (U at scale) | monthly request quota per tariff `[tgstat-api]` |
| Ban / restriction | low: bots meet `429`/`401`, not account freezes | real: unofficial-client accounts "automatically put under observation"; flooding or faking counters "banned forever" `[api-id]`; freeze state since 2025-05 `[frozen]`; limits via `@SpamBot`; appeals `recover@telegram.org` | no account; an IP block is possible (U) | none on our side |
| Terms | Bot Developer Terms §4.3 (below) `[bot-terms]` | API Terms §1.4, §1.5, §3.3 + Content Licensing (below) `[api-terms]` `[content-lic]` | Content Licensing: access outside "ordinary use as its user" is prohibited; Telegram tolerates the widget in practice (U) | provider contract; Telegram terms on the data still apply downstream (U) |
| Cost | free | free + one SIM per account; Premium optional | free | Free ₽0 (2 own channels, 50 requests); S ₽2,100 (30 channels, 6,000); M ₽8,190 (500, 100k); L ₽20,370 (2,000, 400k); XL ₽60,900 (10,000, 2M) `[tgstat-api]`, period monthly (U) |
| .NET fit | `Telegram.Bot` `22.10.0.1` already wired in the be sdk, latest 22.10.3.3 `[identity-t1]` | `WTelegramClient` or TDLib (2.5) | plain HTTP + HTML parse | plain HTTP |

- Other providers: Telemetr.io lists Free, Pro $25/month, Advanced $55/month, Team custom; whether an API tier exists
  is unclear (U) `[telemetr]`. Apify actors scrape the same web preview at $0.20–$6 per 1,000 results and state that
  they need channels "with web preview enabled" (U) `[apify]`. Both are resale of routes already covered.

### 2.4 Web preview `t.me/s/{channel}` — what the page exposes

| Item | Exposed | Evidence |
|---|---|---|
| post identity | `data-post="{channel}/{id}"`, link `https://t.me/{channel}/{id}` | probe |
| time | ISO 8601 UTC in `<time datetime>`; list shows only `HH:MM` | probe |
| text | HTML with bold, links, `tg-emoji`; all text of the post | probe |
| views | abbreviated (`1.09M`) | probe |
| reactions | per-emoji counts (`kunuz`, `daryo_uz`, `durov`) | probe |
| edited | `edited` marker; no edit time | probe, `telegram/455` |
| forwarded from | label; name + link to origin post when the origin is public; empty name in one sample (`durov`) | probe, `tginfoen` |
| author signature | `tgme_widget_message_from_author` (`durov`, 20 of 20 posts) | probe |
| photos / albums | CDN URL in `style="background-image"`; an album is one bubble (`tgme_widget_message_grouped`) | probe |
| video | direct `mp4` URL with a `token` query for short clips; others a placeholder; token lifetime (U) | probe |
| channel header | title, `@username`, verified flag, description, counters: subscribers, photos, videos, links, files | probe |
| pagination | `?before={id}` older, 20 per page; `?after=` returned no posts; `?q=` search works (1 query) | probe |
| single post | `/{channel}/{id}?embed=1&mode=tme` | probe |
| not seen | comment/reply counts, polls (5 channels, 20 posts each) | probe |

### 2.5 MTProto libraries for .NET

| Attribute | `WTelegramClient` | TDLib + bindings |
|---|---|---|
| Package | `WTelegramClient` `4.4.9`, 888,809 downloads, MIT `[wtc]` | `TDLib` + `TDLib.Api` `1.8.67` (MIT, from `egramtel/tdsharp`, depends on Newtonsoft.Json), `tdlib.native` `1.8.67` (BSL-1.0, RIDs linux/osx/win × x64/arm64); TDLib on `master` is `1.8.69` `[td-nuget]` `[td-repo]` |
| Shape | managed C#, .NET 5+ / netstandard2.0, MTProto layer 229 | native C++ via P/Invoke, local encrypted database per account |
| Updates | `OnUpdates`, `UpdateManager`, add-on `WTelegramClient.Extensions.Updates` `1.2.2`; gap filling is ours | handles pts and gaps, emits `updateNewMessage`, `updateMessageEdited`, `updateDeleteMessages` `[td-schema]` |
| Session | encrypted file `WTelegram.session`, keyed by `api_hash` or `session_key`; one file per account `[wtc-faq]` | database directory per account + database encryption key |
| Flood | waits <60 s retried automatically (`FloodRetryThreshold`); longer ones throw `RpcException` `[wtc-faq]` | error returned to the caller (U) |
| Maintenance | one maintainer; repo pushed 2026-09-26, 0 open issues `[wtc]` | Telegram's own project; pushed 2026-10-22 `[td-repo]` |
| Pick | first, for scheduled polling with raw control (`Channels_GetMessages`) | fallback when live update streams over many joined chats matter |

- Python/Go/Rust clients are not needed for Telegram: both .NET routes exist. WTelegramClient FAQ: no VoIP numbers,
  disposable numbers may already be flagged, new accounts are scrutinised, use the account passively first
  `[wtc-faq]`.

### 2.6 Telegram terms that bind Harvest

- **API Terms §1.5** (pointing at Content Licensing): no "using, accessing or aggregating" Telegram data to "train,
  fine-tune or otherwise engage in the development, enhancement or deployment" of AI/ML `[api-terms]`.
- **Content Licensing**: access to user content beyond ordinary use as a user is prohibited, with a licence for data
  needed to run a legitimate client, bot or Mini App; AI scraping/use is "firmly" prohibited unless every relevant user
  gives explicit, per-context, continued consent `[content-lic]`. Open Terms Archive logged the change on 2026-02-03
  `[ota]`. No enforcement mechanism is stated.
- **Bot Developer Terms §4.3 "Data Scraping"**: do not collect, store, aggregate or process data beyond what the
  service needs; "always prohibited" is collection for large datasets, ML models and AI products, "such as scraping
  public group or channel contents"; data users submit voluntarily is usable with clear notice and individual,
  explicit, active, revocable consent `[bot-terms]`. §4.2: delete user data on request or when no longer needed.
- **API Terms §1.4**: no hidden read state ("ghost mode"), no suppressing typing or presence. **§3.3**: an app that
  "allows accessing content from Telegram channels" must support official sponsored messages; whether a Harvest
  console that lists extracted items triggers it is open (U). **§4**: 10 days to fix a breach, then API access ends.
- Telegram's general terms (English text, keyword search for scraping, automation, bulk) show no such clause `[tos]`.
- Whether LLM extraction of one post is "deployment of AI" is a legal reading (U); the conservative reading says yes.

---

## 3. WhatsApp access routes

### 3.1 Routes compared

| Attribute | C · Cloud API, DMs to our number | C · Groups API | Meta Content Library | H · channel web page | L · linked-device client |
|---|---|---|---|---|---|
| Reads | messages users send to our business number, `messages` webhook `[wa-hook]` | groups our number created: invite-link join only, ≤8 participants, ≤10,000 groups per number, 1 Cloud API business per group; text and media `[wa-groups]` | public Channel updates, last 30 days, last 1,000 per channel `[wa-cl]` | channel name, description, follower count, latest ~4 updates (probe) | all the paired account sees: chats, groups it is in, Channels it follows `[whatsmeow]` |
| Needs | Meta business account, phone number, HTTPS webhook; verification of a UZ entity (U) | Official Business Account `[wa-groups]` | research access in a Secure Research Environment; eligibility (U) `[wa-cl]` | none | a real number, QR or pairing code |
| History | webhook only | webhook only; no endpoint for past group messages `[unipile]` | 30 days | none beyond ~4 updates, no pagination, no ids (probe) | history sync at pairing claimed by a vendor (U) `[unipile]` |
| Edits / deletions | not documented on the pages read (U) | business cannot edit or delete in groups `[wa-groups]` | (U) | none visible | events exist in the protocol (U) |
| Media | `media.id` → `GET` → URL valid 5 minutes; id valid 7 days; ≤100 MB, else webhook error `131052` `[wa-media]` | text and media | URL only inside the research environment `[wa-cl]` | text only after JS render; audio shows "Download WhatsApp to listen" (probe) | by protocol |
| Cost | inbound free; service replies free up to 1,000/month per number, charged from the 1,001st as of 2026-10-01; UZ is in "Rest of Asia Pacific" `[wa-pricing]` | per message `[wa-groups]` | — | free | free + number |
| Terms / ban | official | official | restricted programme | public page; automated access vs ToS (U) | WhatsApp terms prohibit unauthorized or automated access, unauthorized clients, bulk or auto-messaging; WhatsApp may disable accounts `[wa-tos]` |
| Fit | intake (section 4) | tiny private intake groups, little else | none for production | metadata, last updates, follower count | only route to history, groups, Channels |

- Channel page raw `GET` returns update bodies as empty `<noscript>` placeholders; a browser with JS rendered the text
  of 4 updates, each with day/time and total reactions (probe, built-in browser, `whatsapp.com/channel/0029Va4K0PZ5a245NkngBA2M`).
- No official Cloud API endpoint reads Channels (search found none, 2026-10-26) (U). Channels are described as
  app-only in older partner docs `[360dialog]`.

### 3.2 Unofficial clients

| Library | Language | Licence | State 2026-10-26 | Channels | Own disclaimer |
|---|---|---|---|---|---|
| `whatsmeow` | Go | MPL-2.0 | commits to 2026-10-17 | `GetNewsletterMessages`, `GetNewsletterMessageUpdates`, `NewsletterSubscribeLiveUpdates`, `FollowNewsletter`, `GetNewsletterInfoWithInvite` `[whatsmeow]` | README lists features (groups, receive all messages); no ToS note in the first screen |
| Baileys | TypeScript | MIT | `7.0.0-rc14` (2026-07-29), still a release candidate | none in README | maintainers "do not condone" ToS violations, discourage "stalkerware, bulk or automated messaging" `[baileys]` |
| `whatsapp-web.js` | Node + Puppeteer | Apache-2.0 | `1.34.7` | "Channels" supported in the feature table | WhatsApp "does not allow bots or unofficial clients"; blocks not ruled out `[wwebjs]` |
| .NET ports | C# | — | `Baileys.NET` 1.9.1 (2,113 downloads), `CosmoWhatsapp` 0.1.7 (1,084) | — | tiny and unvetted `[nuget-wa]` |
| Hosted | vendor API (Whapi.Cloud, Unipile) | — | Whapi.Cloud: webhook `POST messages` and `GET /newsletters/{id}/messages` for Channels `[whapi]` | yes | protocol not stated by the vendor; the ban risk stays with our number |

- All mature options are non-.NET: a Go or Node sidecar behind a small internal HTTP/gRPC contract, one process per
  paired number.
- Risk signals: WhatsApp "is already detecting unofficial Web clients in the background" and tests a warning in
  Linked devices (Android beta 2.26.35.1, 2026-09-01) `[wabeta]`; the npm fork `lotusbail` (56,000+ downloads,
  reported 2025-12-22) paired an attacker device to victims' accounts `[lotus]`. No trustworthy ban-rate figure
  exists (search, 2026-10-26).

---

## 4. Compliant intake — users forward or mention

| Attribute | Telegram (Bot API, route F) | WhatsApp (Cloud API, route F) |
|---|---|---|
| Trigger | user forwards a post to the Harvest bot; or mentions `@bot` in any chat or replies to a post with it (**guest mode**, Bot API 10.0, 2026-05-08) `[bot-feat]` `[bot-log]` | user forwards a message, channel update or media to Harvest's number |
| What arrives | `message` with `forward_origin`: `channel` → `chat{id, title, username}` + `message_id` + `author_signature`; `user`, `hidden_user`, `chat` variants; `media_group_id` for albums `[bot-api]`. Guest: a `guest_message` update with the summoning message and the post it replied to; one reply allowed; no history, no later updates `[bot-feat]` | webhook `messages`; `context.forwarded: true` (≤5 forwards) or `context.frequently_forwarded: true` (>5) `[wa-hook]`; no origin chat or message id in the payload (U for a forwarded Channel card) |
| Canonical link | `t.me/{username}/{message_id}` for public origins; private origins give a chat id only | none |
| Blocked by | channels with `has_protected_content` ("can't be forwarded") `[bot-api]`; whether guest mode works in channel comments (U) | — |
| Media | `getFile` ≤20 MB, local server lifts it | URL 5 min, id 7 days, ≤100 MB `[wa-media]` |
| Acknowledgement | bot replies freely | free-form reply only inside the 24-hour window opened by the user's message `[wa-send]`; after 1,000 service messages per number per month each reply is charged `[wa-pricing]` |
| Consent | notice + explicit, active, revocable consent in the bot flow (Bot Terms §4.3); delete on request (§4.2) `[bot-terms]` | notice in the first reply; consent record per sender (U legal basis) |

- Owner-installed bot: the owner of a channel or group adds the Harvest bot as admin → `channel_post`,
  `edited_channel_post`, `message_reaction_count`; consent is the owner's act. No history before the install.
- Intake volume equals what users send; it does not discover sources. It is the cleanest legal basis on both
  platforms and the only one for WhatsApp Channels and groups.

---

## 5. What Harvest must model

### 5.1 Entities

- **Messaging account** (pool member): family (`telegram-user` · `telegram-bot` · `whatsapp-cloud` ·
  `whatsapp-linked`), label, phone (E.164) or bot username, `api_id` reference, session secret reference, state,
  `state_since`, `flood_until`, joined count and cap (500 / 1000), last success, SIM holder, Premium flag.
- **Membership** (account × source): `none` · `peeking` · `join_requested` · `member` · `left` · `banned`; invite hash,
  requested-at, approved-at.
- **Source route list**: per source an ordered list of routes with health, so the adapter can fall back (`W` → `M`).
- **Terms posture** per source: `ai_allowed` (default `false` for Telegram), `consent_basis` (`owner` · `submitter`
  · `none`), retention and deletion-on-request flag.
- **Metric snapshot** apart from the capture: views, forwards, reactions change constantly and must not make every
  poll a `changed` capture (T5).

### 5.2 Sessions as secrets

- A Telegram session (WTelegramClient file or TDLib directory) or a WhatsApp auth state is full control of the
  account; a leaked WhatsApp state lets a third party pair a device. Store envelope-encrypted in Secrets Vault
  (platform app 4), never in captures, logs or exports `[platform-apps]`.
- One worker holds a session at a time (lease): two clients on one auth key give `AUTH_KEY_DUPLICATED` (406)
  `[tg-errors]`. `api_hash` is not public and one `api_id` can serve several accounts `[wtc-faq]`; one `api_id` per
  phone number `[api-id]`.
- Provisioning is a human step: SIM, login code, 2FA password; the worker never receives codes automatically.

### 5.3 Account states and source outcomes

| Condition | Signal | State / outcome | Harvest action |
|---|---|---|---|
| flood wait | `FLOOD_WAIT_X`, `FLOOD_PREMIUM_WAIT_X` `[tg-errors]` | account/method `rate_limited` until now+X | pause that call; reschedule; no retry on another account |
| session dead | `AUTH_KEY_UNREGISTERED`, `AUTH_KEY_INVALID`, `USER_DEACTIVATED`, `SESSION_REVOKED`, `SESSION_EXPIRED` (401) `[tg-errors]` | account `session_lost` or `deactivated` | stop; alert; human re-login |
| frozen | `FROZEN_PARTICIPANT_MISSING` `[tg-chgetmsg]`, `FROZEN_METHOD_INVALID` (U, from Pyrogram's list) | account `frozen` | stop; appeal through `@SpamBot` is human `[frozen]` |
| limited | `PEER_FLOOD`, `@SpamBot` reply (U) | account `limited` | stop writes; reads (U) |
| channel private / gone | `CHANNEL_PRIVATE` (406) `[tg-gethist]`; `/s/` redirect; embed "Post not found" for every id | source `unavailable` | never mark its posts deleted |
| banned in chat | `USER_BANNED_IN_CHANNEL` `[tg-chgetmsg]` | membership `banned` | stop; surface |
| join pending | `INVITE_REQUEST_SENT` `[tg-invites]` | membership `join_requested` | wait; never re-request |
| joined-chat cap | `CHANNELS_TOO_MUCH` (U, name not on pages read) | account `full` | assign sources to another account upfront |
| preview off | `/s/{ch}` redirect | source `preview_unavailable` | use route `M` |
| provider quota | monthly requests spent | source `quota_exhausted` | pause until reset |
| AI barred | terms posture `ai_allowed=false` | item `extraction_skipped` | deliver captures only |
| WA media too big | webhook `131052` | item `media_too_big` | keep text |

### 5.4 Rate limits and budgets (provisional values, tuned on observed waits)

| Scope | Rule |
|---|---|
| per account × method | token bucket; honour `FLOOD_WAIT_X` exactly; never split a limited call across accounts |
| per source | minimum poll interval; newest-page poll of hot channels every 5 minutes (sample channels post ~3 per week to ~20 per day) |
| joins | few per account per day, total ≤400 of the 500 cap; human approval for groups and private chats |
| web preview | ≤1 request/s per host, identifying `User-Agent` with Harvest name and contact URL (spec: "must identify itself"); no proxy or IP rotation |
| provider | monthly quota counter per tariff |
| WhatsApp replies | count per number per month against the 1,000 free service messages |

### 5.5 Join workflow

1. Source submitted (username or invite link) → resolve (`checkChatInvite`, `searchPublicChat`) → kind, size, public
   or private, `request_needed`.
2. Public channel → route `W`, no join. Public group or private chat → state `needs_join`, human approves.
3. Pick an account with free slots; join; on `INVITE_REQUEST_SENT` wait for the admin; on success record membership.
4. Profile of the account names the operator (identification); contact route for admins who object.
5. Leave and `unavailable` are outcomes, not retries.

### 5.6 Deletion checks (scheduled, per spec)

| Route | Check | Caveat |
|---|---|---|
| M | `channels.getMessages(ids)` batch: `messageEmpty` = gone; TDLib `getMessages` → `null` | verify membership first; inaccessible ≠ deleted |
| W | `?embed=1` per id: "Post not found" | one request per id; album members exist under their own ids |
| B | none | owner-installed bots see no deletions |
| F (WA) | none | the sender can delete for everyone; Harvest never sees it (U) |
| P | callback notifications | quota and delay (U) |

- Two levels: source availability first, then post existence. A post is `gone` only when the source is `available`
  and the id answers missing on two checks (provisional).

### 5.7 Media

- Fetch at capture time into File Storage: Telegram `file_reference` expires without a published lifetime
  `[tg-fileref]`, preview video URLs carry a `token` (U lifetime), WhatsApp URLs live 5 minutes `[wa-media]`.
- Per-route size caps: Bot API 20 MB (local server: none), preview short clips only, WhatsApp 100 MB.

---

## 6. Uzbekistan context

- **Telegram dominates**: 70% of Uzbeks name Telegram as the messenger they prefer, 18% WhatsApp, 4% IMO (Central Asia
  Barometer blog dated 2023-12-27; survey year not stated) `[cab]`. A 2025-05-12 article lists Telegram at ~28
  million users without a source (U) `[zamin]`. DataReportal 2026: 33.1M internet users, 89% penetration (late 2025);
  no Telegram or WhatsApp figure `[datareportal]`.
- **Catalog size**: TGStat's homepage lists Uzbekistan at 206,000 channels and 40,400 groups, undated `[tgstat-home]`;
  an Astana Hub repost of Magnetto cites 123,958 channels for July 2026 (U) `[astanahub]`; a 2023 Kun.uz report
  counted 123,000+ channels and ~18,000 groups, second in the world after Russia `[kun-2023]`.
- **Sample sources (probe)**: `@kunuz` (news) 20 posts in ~26 hours; `@afishauz` (events, 33.1K) 16 bubbles in 3 days,
  linked from afisha.uz; `@domtutuz` (new-builds, 14.7K) 17 bubbles in 40 days; `@Uybor` (2.8K) 4 posts between
  2026-05-14 and 2026-09-06. Newest-page polling every few minutes covers all four.
- **Real-estate and events**: portals link their channels from the site (`afisha.uz` → `t.me/afishauz`, `uybor.uz` →
  `t.me/Uybor`, `domtut.uz` → invite URL); real-estate groups are not ranked on any source found (U).
- **WhatsApp** is the minority messenger (18%); Channels and groups of UZ businesses are unmeasured (U).
- **Phone numbers**: Telegram and WhatsApp accounts need a number; WTelegramClient advises against VoIP and
  disposable numbers `[wtc-faq]`. Uzbek SIM sales need a passport and, for foreigners, proof of residence; sources
  are secondary, no regulator text found (U); Ucell opened self-registration for foreigners in its app on
  2026-06-12 `[ucell]`. Which entity's passport or licence holds the SIMs ties to the parent-company question
  (`ven-t-012`).
- **Access risk**: Uzbekistan restricted social media and messengers for days in 2021-11 and reversed it
  (search results only; U) `[rferl]`; no 2025–2026 Telegram block found (search, 2026-10-26). A 2025 draft law on
  online activity would limit blocking to court orders; adoption not found (U) `[zamin]`.
- **Channel mortality**: authorities pressured six Kashkadarya news bloggers to close their channels in 2023 `[rsf]`;
  sources vanish, so `unavailable` is a normal outcome.

---

## 7. First route, fallback, risks per source kind

| Source kind | First route | Fallback | Risks |
|---|---|---|---|
| TG public channel, not ours | W web preview (no account, views + reactions + forward link) | M; P for stats only | Content Licensing / AI clause; preview may be off for a channel; no comments; groups and invites unsupported |
| TG public channel we or a consumer own | B owner-added bot | W for history before the install | no backfill for B; owner consent covers the owner's posts, not comments (U) |
| TG public group / supergroup | M (account joins; human approves) | F; B if an admin adds the bot | strongest terms exposure (user content of non-consenting people), join caps and flood waits, bans of the pool account |
| TG forum topics | M (`getForumTopics`, per-topic thread history) | B in groups the bot sits in | topic ids, closed topics, General topic differs |
| TG channel comments | M (`getDiscussionMessage`, thread replies) | B inside the discussion group | comments are third-party user content; deleting the forwarded copy disables them |
| TG private channel / group (invite) | M (`checkChatInvite` → human-approved `importChatInvite`) | F by members; B if admin adds | invite expiry or revocation, admin approval wait, privacy of closed groups; resolve to a public username first |
| WA Channel | H page snapshot (latest ~4 updates, follower count) | F forward; L sidecar only on an explicit decision | page keeps 4 updates and no ids, so fast channels lose posts; L: ban, ToS, supply chain, non-.NET |
| WA group | F forward by members; C Groups API for our own intake groups (≤8) | L sidecar on an explicit decision | official routes cannot join existing groups; L as above |
| WA Business number (ours) | C Cloud API webhook | second number | Meta business verification for a UZ entity (U); 1,000 free replies per month; templates outside the 24-hour window |

---

## Findings that change the spec

- Telegram's terms bar using platform data for AI "development, enhancement or deployment" (API Terms §1.5, Content
  Licensing, logged 2026-02-03) and bar scraping public channel or group content for datasets (Bot Terms §4.3).
  Harvest's LLM extraction over Telegram captures sits inside that wording; spec § Extraction needs a per-source
  `ai_allowed` gate, default off for Telegram, on for consented sources.
- The Bot API cannot be the channel-reading route: no history, no views or forward count, no delete updates, update
  retention ≤24 h, and the bot must be a member or admin. Spec § Concepts: Bot API serves owner-installed channels
  and intake only.
- Only MTProto reaches groups, topics, comments, private invites, full history and by-id deletion checks. That
  forces an account pool: SIM numbers, sessions as secrets, one holder per session, 500/1000 joined-chat cap, and
  `rate_limited` / `session_lost` / `frozen` / `banned` states. Spec needs `account` and `membership` concepts and a
  "needs account" attribute on source adapters.
- Web preview `t.me/s` is a free, account-less first route for public channels: 20 posts per page, random access by
  `?before=`, views, reactions, edited flag, forward-origin link, mp4 URLs, and a per-id deletion probe via
  `?embed=1`. It does not cover groups, invites or comments, and album id gaps look like deletions.
- Consent-based intake is richer than assumed: forwards carry `forward_origin` (canonical link, dedup key), Bot API
  10.0 guest mode lets a user summon the bot in any chat, and Bot Terms §4.3 allows user-submitted data with notice
  and consent. Spec gains an `intake` source kind with a consent record.
- WhatsApp offers no compliant read route for Channels or existing groups: the Cloud API sees only chats with our
  number, the Groups API is limited to ≤8-participant groups we create, Meta's Content Library is research-only with
  30 days, and the channel web page shows ~4 updates without ids. Everything else is an unofficial linked-device
  client (WhatsApp detects them; non-.NET sidecar). WhatsApp v1 = intake + channel page snapshots.
- "A rate-limited source is an outcome, never bypassed" needs a pool definition: a `FLOOD_WAIT` belongs to the
  (account, method) pair; Harvest does not retry that call on another account or through another IP. Assignment is
  sticky; failover only when an account dies.
- Deletion checks are two-level: source availability first, then post existence. An unavailable channel, a kicked
  account and an album gap all look like missing posts.
- Media must be fetched at capture: Telegram file references expire, preview video URLs carry tokens, WhatsApp media
  URLs live 5 minutes.
- WhatsApp pricing changed 2026-10-01: after 1,000 service messages per number per month each reply is charged;
  inbound stays free. Intake acknowledgements must be sparing.
- Uzbek sample channels post from ~3 per week to ~20 per day; newest-page polling every few minutes is enough, and a
  site's invite link can hide a public channel (Domtut).

---

## Points

- [ ] T1-P1 Telegram AI clause: may LLM extraction run over Telegram captures? → provisional pick: Telegram sources
  default to `ai_allowed=false` (captures delivered, rule-based extraction only); `true` only for owner-installed and
  consented intake sources; ask counsel to read §1.5 before any change (T6)
- [ ] T1-P2 Telegram public channels: preview first or user client first? → provisional pick: web preview first, `M`
  when preview is off or deletion events/comments are needed
- [ ] T1-P3 Account pool start: how many accounts and whose SIMs? → provisional pick: two Telegram user accounts
  (one active, one spare) on UZ SIMs registered to the operator entity, no VoIP, no Premium; none for WhatsApp (T8,
  `ven-t-012`)
- [ ] T1-P4 MTProto library → provisional pick: `WTelegramClient` for scheduled polling; revisit TDLib if live update
  streams over >100 joined chats are needed
- [ ] T1-P5 Failover on `FLOOD_WAIT` → provisional pick: sticky assignment, no reactive failover, no IP rotation;
  failover on account death only (T7)
- [ ] T1-P6 Joining groups and private chats → provisional pick: human approves each join; public channels never need
  a join; the account profile names the operator
- [ ] T1-P7 WhatsApp scope for v1 → provisional pick: Cloud API intake number + channel page snapshots; the unofficial
  sidecar waits for an explicit developer decision
- [ ] T1-P8 Intake identity → provisional pick: one shared Harvest intake bot and one WhatsApp number, products
  attributed by a linking step (`/start` payload; sender number); separate from any notification or publishing bot
  (T4, T7, P1 social connectors)
- [ ] T1-P9 Consent record for intake → provisional pick: store text version, timestamp and sender id per submitter;
  deletion on request removes their captures (T5)
- [ ] T1-P10 Metrics → provisional pick: views, forwards and reactions as a snapshot series outside the capture
  hash; forward origin `(chat, message_id)` is a dedup key where present, WhatsApp has none (T5)
- [ ] T1-P11 Brand linking → provisional pick: a site source and its Telegram channel link as one canonical entity
  (Afisha, Uybor, Domtut) (T3, T5)
- [ ] T1-P12 TGStat → provisional pick: do not buy in v1; use the free catalog pages for UZ channel discovery only (T3)
- [ ] T1-P13 Console and sponsored messages (API Terms §3.3) → provisional pick: the console shows extracted items
  with a link to `t.me`, not channel views, so §3.3 is not triggered (U)
- [ ] T1-P14 WhatsApp onboarding for a UZ entity (Meta verification, billing) → provisional pick: check with the
  parent-company decision before any Cloud API work (U)

---

## Sources

Telegram terms and API
- [api-terms] https://core.telegram.org/api/terms — API Terms §1.4, §1.5, §2, §3.3, §4
- [content-lic] https://telegram.org/tos/content-licensing — AI scraping prohibition, limited exception, consent route
- [bot-terms] https://telegram.org/tos/bot-developers — §4.2 deletion, §4.3 Data Scraping
- [tos] https://telegram.org/tos?setln=en — general terms (no scraping clause found)
- [ota] https://opentermsarchive.org/en/memos/telegram-prohibits-collecting-data-for-ai-use/ — change logged 2026-02-03
- [api-id] https://core.telegram.org/api/obtaining_api_id — one `api_id` per number, observation of unofficial clients, bans, recovery mail
- [bot-api] https://core.telegram.org/bots/api — Update types, `Message`, `forward_origin`, `getUpdates` 24 h, `getFile` 20 MB, local server, `has_protected_content`
- [bot-log] https://core.telegram.org/bots/api-changelog — Bot API 10.3 (2026-08-24), 10.0 guest mode (2026-05-08)
- [bot-faq] https://core.telegram.org/bots/faq — privacy mode, rate limits
- [bot-feat] https://core.telegram.org/bots/features — privacy mode, guest bots
- [bot-local] https://github.com/tdlib/telegram-bot-api — local server, BSL-1.0, `--local` limits
- [tg-errors] https://core.telegram.org/api/errors — 420 flood, 401/406 session errors
- [tg-updates] https://core.telegram.org/api/updates — channel pts, polling of non-joined public channels, delete/edit updates
- [tg-config] https://core.telegram.org/api/config — 500/1000 channel limit, upload size
- [tg-invites] https://core.telegram.org/api/invites — invite formats, `chatInvitePeek`, `INVITE_REQUEST_SENT`
- [tg-discuss] https://core.telegram.org/api/discussion — comments, `messages.getDiscussionMessage`
- [tg-forum] https://core.telegram.org/api/forum — topics
- [tg-gethist] https://core.telegram.org/method/messages.getHistory — users only, `CHANNEL_PRIVATE`
- [tg-chgetmsg] https://core.telegram.org/method/channels.getMessages — users and bots, error list incl. `FROZEN_PARTICIPANT_MISSING`
- [tg-msgempty] https://core.telegram.org/constructor/messageEmpty — non-existent message
- [tg-fileref] https://core.telegram.org/api/file-references — `file_reference` expiry
- [td-schema] https://raw.githubusercontent.com/tdlib/td/master/td/generate/scheme/td_api.tl — `getChatHistory`, `getMessages`, `updateDeleteMessages`, `messageInteractionInfo`, `joinChatByInviteLink`
- [td-repo] https://github.com/tdlib/td — BSL-1.0, 1.8.69 on master (read via raw `CMakeLists.txt`)
- [td-nuget] https://www.nuget.org/packages/TDLib and https://www.nuget.org/packages/tdlib.native — 1.8.67 (via NuGet search and nuspec)
- [wtc] https://github.com/wiz0u/WTelegramClient and https://www.nuget.org/packages/WTelegramClient — MIT, 4.4.9
- [wtc-faq] https://wiz0u.github.io/WTelegramClient/FAQ — bans, flood retry, VoIP, sessions, `api_id`
- [frozen] https://tginfo.me/?p=8786 — frozen accounts since May 2025 (secondary); https://docs.pyrogram.org/faq/the-account-has-been-limited-deactivated
- [tgstat-api] https://tgstat.com/api — plans and prices in ₽
- [tgstat-docs] https://api.tgstat.ru/docs/ru/start/intro.html — methods, callbacks, quotas
- [tgstat-home] https://tgstat.com/en — catalog counts for Uzbekistan
- [telemetr] https://tlmtr.io/en/pricing — plans (search result; API tier unclear)
- [apify] https://apify.com/flash_scraper/telegram-channel-scraper — example actor (search result; prices vary)
- [probe-tme] plain `GET` 2026-10-26: https://t.me/s/telegram · /s/durov · /s/kunuz · /s/daryo_uz · /s/afishauz · /s/Uybor · /s/domtutuz · /s/tginfoen · /s/pythontelegrambotgroup · /s/daryo_uz?before=1000 · /s/daryo_uz?q=kvartira · https://t.me/daryo_uz/2177?embed=1&mode=tme · https://t.me/telegram/99999999?embed=1&mode=tme · https://t.me/durov/549?embed=1&mode=tme · https://t.me/+ekAo9KlbIIwyN2Yy · https://t.me/robots.txt

WhatsApp
- [wa-pricing] https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing.md — per-message pricing since 2025-07-01, inbound free, 1,000 free service messages from 2026-10-01, UZ region
- [wa-groups] https://developers.facebook.com/documentation/business-messaging/whatsapp/groups — Groups API limits
- [unipile] https://www.unipile.com/whatsapp-group-api/ — Groups API summary and linked-account comparison (vendor, August 2026)
- [wa-hook] https://developers.facebook.com/documentation/business-messaging/whatsapp/webhooks/reference/messages/text and …/messages/video — `context.forwarded`, media fields
- [wa-media] https://developers.facebook.com/documentation/business-messaging/whatsapp/business-phone-numbers/media — URL 5 minutes, id 7 days, 100 MB, `131052`
- [wa-send] https://developers.facebook.com/documentation/business-messaging/whatsapp/messages/send-messages — 24-hour window
- [wa-cl] https://developers.facebook.com/docs/content-library-and-api/content-library-api/guides/wa-channel-update — Channel updates, 30 days
- [wa-tos] https://www.whatsapp.com/legal/terms-of-service — automated access, unofficial clients, bulk messaging
- [wa-ch] https://www.whatsapp.com/channel/0029Va4K0PZ5a245NkngBA2M — public channel page (probe, raw `GET` and built-in browser)
- [360dialog] https://docs.360dialog.com/docs/whatsapp-marketing/driving-users-to-your-whatsapp-account/whatsapp-channels — Channels app-only (undated, search result)
- [whatsmeow] https://github.com/tulir/whatsmeow and https://raw.githubusercontent.com/tulir/whatsmeow/main/newsletter.go — MPL-2.0, Channel methods
- [baileys] https://github.com/WhiskeySockets/Baileys — MIT, `7.0.0-rc14`, disclaimer
- [wwebjs] https://github.com/pedroslopez/whatsapp-web.js — Apache-2.0, `1.34.7`, disclaimer
- [nuget-wa] https://www.nuget.org/packages/Baileys.NET and https://www.nuget.org/packages/CosmoWhatsapp — .NET ports (via NuGet search)
- [whapi] https://support.whapi.cloud/help-desk/channels/get-messages-from-channels — hosted Channel reading
- [wabeta] https://wabetainfo.com/whatsapp-is-testing-a-safety-warning-for-unofficial-web-clients/ — detection and warning test, 2026-09-01
- [lotus] https://www.theregister.com/2025/12/22/whatsapp_npm_package_message_steal/ — `lotusbail` fork

Uzbekistan
- [cab] https://ca-barometer.org/en/publications/which-messaging-apps-are-popular-in-uzbekistan-kyrgyzstan-and-kazakhstan — 70% / 18% / 4%
- [datareportal] https://datareportal.com/reports/digital-2026-uzbekistan — internet users, no messenger figures
- [zamin] https://zamin.uz/en/society/149747-ozbekistonda-onlayn-faoliyatni-tartibga-soluvchi-yangi-qonun-ishlab-chiqildi.html — 2025-05-12, ~28M Telegram users (unsourced), draft online-activity law
- [kun-2023] https://kun.uz/en/50659966 — 123,000+ channels, second after Russia (search result summary)
- [astanahub] https://astanahub.com/en/blog/kakie-telegram-kanaly-populiarny-v-tsentralnoi-azii — Magnetto/TGStat July 2026 channel counts (search result; original not found)
- [rsf] https://rsf.org/fa/node/93576 — 2023 channel closures in Kashkadarya
- [rferl] https://rferl.org/a/uzbekistan-social-media-restrictions/31544451.html — 2021 restrictions (search result only)
- [ucell] https://ucell.uz/en/news/plan_works_selfreg1206 — foreigner SIM self-registration (search result)
- sample portals read: https://www.afisha.uz/ru · https://uybor.uz · https://domtut.uz (links to their Telegram channels)

Workspace
- [identity-t1] [t1-integrations.md](../identity-analysis-2026-10/t1-integrations.md) — `Telegram.Bot` wired in the be sdk
- [platform-apps] [platform apps](../../docs/platform-apps.md) — Secrets Vault (4), File Storage (3), Harvest (17)
- [spec] [harvest-service-spec.md](../harvest-service-spec.md) · [analysis index](harvest-analysis-2026-10.md)

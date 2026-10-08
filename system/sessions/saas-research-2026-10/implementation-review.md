# Three-product implementation review

Updated: 2026-10-06. User-authorized scope: sweep Pose Coach, Transcript Forge and Hijinx, implement necessary improvements, and prepare them for review. ForeverPin belongs to a separate chat.

## Review status

**Latest increment complete for local review:** 15-language globalization for both consumer products, Pose Coach live observations/voice/hands-free controls, and Transcript Forge persistent project queue controls. [Scope and store evidence](../../../ideas/saas-research-2026-10/globalization-and-live-coaching.md). This report includes the earlier reliability/host-workflow sweep and the expanded increment. Hands-on device, language-quality and provider acceptance remain open.

The scoped implementation increment is complete and ready for human review. The product directions and release priority remain those in the [central venture order](../../planning/pln-tasks.md#venture-product-order). This report records local changes and executed checks; each repository's planning files own its remaining release work. No product was published or enabled to charge, and no commits were made.

| Product | Review target | First workflow to inspect |
|---|---|---|
| Pose Coach | iPhone 17e simulator; physical camera/voice acceptance remains open | Choose language → pattern → Live coach / Voice → duo-photo collage |
| Transcript Forge | [Local application](https://localhost:8232) | Project → pause queue → add waiting work → clear or resume |
| Hijinx | [Host playlists](https://localhost:5186/host) | Choose language → play a translated starter pack → save/reuse a playlist |

## Pose Coach

**User outcome:** the existing duo-photo coach gains opt-in live framing guidance, visible body/hand landmarks, spoken cues and on-device voice commands, plus a 15-language interface. Interrupted imports and retakes cannot restore an old photo, and saved/shared collages refer to the intended image state.

Live analysis is bounded to three admitted frames per second, drops late frames, and uses the capture session's clock converted to the same host clock as freshness and shutter checks. Guidance covers visible people, head/body/hand geometry, brightness and a plausible phone-shaped prop. It does not claim identity recognition or that a creative pose is correct. Explicitly armed hands-free capture requires fresh stable framing, counts down three seconds and disarms after one shot. Context changes, leaving and backgrounding invalidate pending analysis, commands and captures.

Spoken guidance and voice-command listening are separate modes. Commands use supported on-device speech recognition with explicit microphone/speech permission and no cloud fallback. Available commands arm a photo, cancel, retake or switch cameras. Voice availability depends on the device's installed models/voices; unsupported language/device states retain touch controls. Listening sessions are bounded and can be restarted from the UI.

Each of 15 interface catalogs contains 184 matching keys, including pattern directions, errors and command phrases. All 15 native permission catalogs are bundled; OS prompts follow the system/app language, which can differ from the in-app picker. Arabic text layout stays separate from physical camera directions. Translations are authored drafts awaiting native-speaker review.

The sweep covers bounded photo loading, stale asynchronous work, failed imports/capture, enhancement readiness, save revision tracking and share snapshots. A configurable StoreKit purchase/restore foundation uses verified transactions. The production pilot has no configured paid offer or fulfilled premium benefit, so it cannot charge merely because a product identifier is added. Existing starter patterns stay accessible.

Review route: select a language and pattern, enable Live coach, choose spoken guidance or supported commands, arm/cancel hands-free capture, and switch camera/person. Continue through the two-photo collage, Keep/Retake, adjustment and save/share flow. The simulator has no physical camera; it shows explicit unavailable states rather than simulated recognition success. Physical camera quality, detector accuracy, real speech, Photos/share behavior and App Store transactions need separate device/provider evidence.

Verification: final `xcodebuild test` passed **114 tests across 18 suites**, including 25 additional tests beyond the prior 89-test photo-flow sweep. Coverage includes all catalogs/placeholders, bundled permission strings, locale/script matching, capture-clock conversion, stable/fresh observations, one-shot countdowns, command parsing and stale-generation/startup cancellation. The StoreKit adapter compiled; transaction tests use fixtures. Backend and catalogue console were unchanged, and their earlier checks were not repeated.

The unsigned generic iPhone build also passed, compiling the physical live-analysis path without claiming device execution. The tested app is installed and launched on **iPhone 17e / iOS 27.0**, simulator `3594D30A-3C57-4CBD-AF2B-0741344E82D9`. [English](/tmp/pose-coach-live-review-2026-10-06.png) and [Arabic](/tmp/pose-coach-live-review-ar-2026-10-06.png) menu screenshots were independently inspected; Arabic shows translated RTL navigation and content. The app was restored to its ordinary English launch afterward. Interactive camera-layout review was unavailable while the Mac was locked; no complete manual photo or voice workflow is claimed.

Source of current product and check results: [Pose Coach context](../../../workbench/ventures/ventures.pose-coach/product/context.md), [live coaching, localization, commands and review steps](../../../workbench/ventures/ventures.pose-coach/engineering/research/live-coaching-and-localization-2026-10-06.md), [earlier reliability and purchase foundation](../../../workbench/ventures/ventures.pose-coach/engineering/research/local-implementation-sweep-2026-10-06.md).

## Transcript Forge

**User outcome:** a project owner can pause and resume waiting transcription work across restarts, or clear waiting work while retaining running jobs and previous results. The earlier bounded processing, reuse and local access protections remain in place.

Queue controls are available through the local UI, REST and authenticated MCP. PostgreSQL row locks serialize pause/clear against worker claims. Resume invalidates stale jobs when releasing a paused queue; repeated resume safely republishes the same waiting IDs if an earlier dispatch failed. New automatic work and retries stay held while paused. Failed acknowledgements ask the user to refresh rather than falsely claiming the server stayed unchanged.

The sweep covers bounded processing/admission, exact reuse checks after serialization, project input limits, optional metadata failure, command-process cancellation/output limits, and origin/host/proxy-header protection for local APIs. The local host explicitly disables proxy-header interpretation. Language-name normalization reuses compatible existing transcripts, and short speech estimates apply the provider's minimum duration.

Review route: open a project, pause its queue, add waiting work, reload, clear waiting work or resume. Inspect the counts and retained results. Automated provider tests use stubs; they do not establish live YouTube or paid speech-to-text readiness. This remains a single-installation product. Hosted customer isolation, billing, trusted-proxy deployment and the remaining SDK adoption track are separate work.

Verification: **329 backend tests** passed — 167 unit, 46 PostgreSQL integration and 116 HTTP/MCP E2E. **136 frontend tests**, typecheck, 42 Vue component compilation checks, build, lint and formatting passed. After the final acknowledgement-copy correction, the three queue DOM tests and production build/copy passed again. External transcription brokers are stubbed in tests; no paid provider calls were made.

Review runtime: [https://localhost:8232](https://localhost:8232), with the built UI served by the API. The health endpoint and UI returned HTTP 200 with normal TLS validation. Replacement managed session `83492` uses HTTP/1.1 over TLS for this macOS review run; prior session `40257` stopped cleanly. Migration 009 applied on startup. The final rebuilt queue bundle was independently fetched over trusted HTTPS and contained the updated acknowledgement messages. Existing PostgreSQL and installed tools are used; automatic tool downloads are disabled. No Groq key is configured, so live speech recognition is unavailable in this environment.

Source of current product and check results: [Transcript Forge context](../../../workbench/ventures/10x-ventures-transcript-forge/product/context.md), [queue controls, commands and review steps](../../../workbench/ventures/10x-ventures-transcript-forge/engineering/planning/version-track/v0.8/queue-controls-review.md), [earlier reliability sweep](../../../workbench/ventures/10x-ventures-transcript-forge/engineering/planning/version-track/v0.8/local-reliability-review.md).

## Hijinx

**User outcome:** a host can play localized starter content in 15 interface languages, reuse an ordered playlist, retain its position and avoid previously seen cards. Saved state reports whether durable storage succeeded.

The added globalization covers all interface messages, automatic device-language matching, persisted explicit choice, Arabic RTL, localized counts/dates and language-specific Hot Seat alphabets or sounds. Twelve added languages each receive 95 translated clean starter cards across seven games, generated from 96 local overlays. Stable card IDs preserve repeat history across language switches. Translation coverage is computed from actual required text fields, with draft and source-English fallback labels. Existing packs remain free; native editorial review is still pending.

The sweep covers local playlist creation/editing/reordering, backup/import, seen-card history, explicit exhaustion, storage failure recovery, game-phase focus/scroll, dismissed sharing and editorial-language status. Native writes are ordered so an older save cannot overwrite newer state, and only successful native writes confirm durable saves. Disabling adult content immediately clears an active adult round. Repeated scoring actions cannot duplicate a completed turn. Playlist progress does not promise restoration of an unfinished game's score or timer.

Review route: select a language, play a translated starter pack, inspect an English fallback pack, and return to automatic device language. Create a host playlist, add game/pack choices, play, advance, reload and resume; export/import a backup and inspect behavior after selected content is exhausted. New hosted accounts, online rooms and payments are outside this offline implementation increment.

Verification: final `pnpm verify` passed **174 unit tests**, typecheck, lint, formatting and the production build. **27 targeted browser scenarios** passed, covering 15 locales across 11 phone routes (165 route visits), translated gameplay, source fallback, offline use, host regressions and native-storage adapter flows. Arabic, Japanese, Hindi and German gameplay screenshots were independently inspected: readable with no horizontal overflow. Physical-device behavior and native editorial quality remain open.

After a final selector-width correction, the 17 globalization browser scenarios passed again. The final iOS shell rebuilt, installed and launched on the dedicated iPhone 18 Pro simulator. Its [home screenshot](/private/tmp/hijinx-global-review/ios-home.png) confirms the full automatic-language label; it does not establish native multilingual interaction or persistence across OS language changes.

Review runtime: [https://localhost:5186/host](https://localhost:5186/host), managed session `8102`. Final independent readiness verification returned HTTP 200 with normal TLS validation. Current globalization screenshots: [Arabic](/private/tmp/hijinx-global-review/ar-playing-phone.png), [Japanese](/private/tmp/hijinx-global-review/ja-playing-phone.png), [Hindi](/private/tmp/hijinx-global-review/hi-playing-phone.png), [German](/private/tmp/hijinx-global-review/de-playing-phone.png), [Arabic with English fallback](/private/tmp/hijinx-global-review/ar-english-fallback-phone.png). Native bundle registration includes all 15 supported interface locales.

Source of current product and check results: [Hijinx context](../../../workbench/ventures/ventures.hijinx/product/context.md), [globalization coverage, commands and native limits](../../../workbench/ventures/ventures.hijinx/engineering/research/globalization-2026-10-06.md), [earlier host-workflow review](../../../workbench/ventures/ventures.hijinx/engineering/research/local-review-2026-10-06.md).

## Handoff boundaries

- Pose Coach: real-device camera/voice quality and complete manual workflow, native editorial/accessibility review, a concrete paid benefit, real StoreKit lifecycle and store readiness remain open. Fifteen UI languages do not guarantee fifteen local speech models. The purchase foundation alone is not a sellable release.
- Transcript Forge: remaining SDK adoption, manual/live-provider acceptance and reliable local Release 1 precede hosted accounts, quotas and billing. Admission protection is per process; persistence after provider success is bounded best effort, not an invoice ledger or crash-proof result journal.
- Hijinx: native host workflow and physical-device checks, Android parity, editorial review, paid-content fulfillment and store/public release remain open. Device-local playlists do not sync or merge concurrent browser-tab edits.
- Both web runtimes remain owned by this chat for the forthcoming review. They use existing local dependencies; no new hosting or provider spend was introduced.
- Changes remain uncommitted. Existing unrelated work and the index were preserved, including Pose Coach's pre-existing untracked implementation. ForeverPin and shared SDK source were outside this sweep.

Local tests establish the specific behaviors above. They do not establish production readiness, live payments, customer demand, repeat retention or revenue.

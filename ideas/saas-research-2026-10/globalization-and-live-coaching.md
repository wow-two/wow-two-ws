# Globalization and live coaching

Reviewed: 2026-10-06. Scope: the user-authorized expansion of Hijinx and Pose Coach, plus a coherent local workflow increment in Transcript Forge. Implementation evidence belongs in the three repositories and the [implementation review](../../system/sessions/saas-research-2026-10/implementation-review.md). ForeverPin remains owned by its separate chat.

## Decision

Implement a 15-language interface in both consumer products: English, Uzbek Latin, Russian, Spanish, French, German, Brazilian Portuguese, Italian, Turkish, Arabic, Hindi, Indonesian, Japanese, Korean and Simplified Chinese.

This is an engineering/product judgment, not a measured market-share optimum. Preserve the existing home-market languages; add the frequently observed European set, then cover major Asian scripts and Arabic RTL. A smaller, usable translated experience is preferable to claiming every game card, voice or recognition engine works in every language. The larger competitor counts are evidence that breadth is common, not a target to copy blindly.

For Hijinx, implement all interface messages and a clean starter collection across its playable games in the added languages. Retain source-English content with an explicit fallback label wherever a pack has no translation. Draft status and exact content coverage must come from actual fields, rather than a language code on the store page. Native editorial review remains pending.

For Pose Coach, localize the existing photo workflow, pattern directions and new live/voice controls. UI language support, installed speech-synthesis voices and on-device speech recognition are three different capabilities. Show truthful availability and retain touch controls when voice support is absent.

## Store evidence

App Store counts below are the public listing's language metadata. Google Play counts are explicit developer claims in descriptions or release notes. No competitor binaries were installed or linguistically audited. Sources were read October 6; versions and regional pages can differ.

| Product / listing | Observed language scope | Relevance |
|---|---|---|
| [Picolo, App Store](https://apps.apple.com/us/app/picolo-party-game/id1001473964) | 14: English, Danish, Dutch, Finnish, French, German, Italian, Japanese, Korean, Norwegian Bokmål, Portuguese, Russian, Spanish, Swedish | A broad party-game benchmark, including East Asian languages |
| [Charades — Family & Party Game, App Store](https://apps.apple.com/us/app/charades-family-party-game/id1453837845) | 13: English, Arabic, Danish, Dutch, French, German, Hungarian, Italian, Norwegian Bokmål, Portuguese, Spanish, Turkish, Ukrainian | Supports including Arabic and Turkish; exact current listing differs from older search snapshots |
| [Charades: Word Guessing Games, App Store](https://apps.apple.com/us/app/charades-word-guessing-games/id1452117876) | 33 listed languages, including Arabic, Hindi, Indonesian, Japanese, Korean and both Chinese scripts | Broad coverage is possible; listed languages do not establish editorial quality |
| [Charades, Google Play](https://play.google.com/store/apps/details?id=com.plekhotkindmytro.charades) | Explicitly lists 7: English, Spanish, Ukrainian, Russian, French, German, Portuguese | A narrower Android party-game example; do not infer parity from similarly named iOS apps |
| [Charades: Heads Up Party Game, Google Play](https://play.google.com/store/apps/details?id=com.charadesparty.app&hl=en) | Claims 6: English, French, Spanish, Portuguese, German, Indonesian; claims adapted decks | Content adaptation matters alongside interface translation |
| [Bulu / Charades! Offline Games 2026, Google Play](https://play.google.com/store/apps/details?id=com.yasirkara.bulu&hl=en) | Release notes name 10 added languages: Arabic, Spanish, German, French, Italian, Dutch, Danish, Swedish, Norwegian, Finnish; total unspecified | Explicitly describes both app text and card content; additions are not the total supported count |
| [Vouve, App Store](https://apps.apple.com/ie/app/vouve-ai-pose-coach-cam/id6769137009) | 7: English, French, German, Italian, Portuguese, Spanish, Ukrainian | Direct live-pose competitor; advertises on-device detection, voice coaching and auto-shutter |
| [Pose AI: Photo Guide Camera, App Store](https://apps.apple.com/us/app/pose-ai-photo-guide-camera/id6795681321) | English only in listing metadata | Direct guide apps can start with a narrow language set |
| [UNSCRIPTED Photography Poses, App Store](https://apps.apple.com/us/app/unscripted-photography-poses/id1438843099) | English only in listing metadata | Large pose libraries and business functionality do not imply broad localization |
| [Pose AI: ShePoses, App Store](https://apps.apple.com/us/app/pose-ai-sheposes/id6789862513) | 44 listed languages | Adjacent photo product, not a like-for-like live coach benchmark |
| [Framed: Pose Overlay Camera, Google Play](https://play.google.com/store/apps/details?id=com.framed.app&hl=en) | Release notes claim 19 languages, without enumerating them | A direct photo-overlay competitor with broad claimed coverage |
| [ReCreate: Photo Pose Guide, Google Play](https://play.google.com/store/apps/details?id=com.recreate.photo&hl=en) | Description claims 20 languages, without enumerating them | Another direct overlay-camera comparison |
| [Photography Field Assistant, Google Play](https://play.google.com/store/apps/details?id=com.huawei.photoassistant) | Claims 9: Simplified Chinese, English, Japanese, Korean, Traditional Chinese, Spanish, Brazilian Portuguese, French, German | Supports the selected East Asian and Brazilian Portuguese scope; adjacent toolbox |

### What Google Play can and cannot establish

Google distinguishes store-listing translation from app-string translation and offers automatic listing translations. Merely changing `hl=` or observing a translated description does not prove that the installed app supports that language. [Google's localization guidance](https://support.google.com/googleplay/android-developer/answer/9844778?hl=en).

For example, [Unscripted's Google Play listing](https://play.google.com/store/apps/details?id=com.unscripted.posing.app&hl=en) and localized regional versions were inspected, but no exhaustive in-app language count was established. Picolo's localized Play pages likewise were not counted as supported in-app locales. No downloads, reviews or language counts were converted into revenue or demand claims.

## Product-specific implementation requirements

### Hijinx

- Preserve explicit language choice; support returning to the device's automatic language.
- Resolve supported region/script variants deliberately; use native names in the picker.
- Apply Arabic RTL to interface layout and isolate names, numbers and source-English content correctly.
- Use locale-aware number/plural formatting and keep interpolation placeholders intact.
- Measure card translation completeness from required fields; label source-language fallback during play.
- Translate clean starter content across seven games, with truth and dare as separate packs.
- Adapt Hot Seat answer alphabets/sounds for Cyrillic, Arabic, Devanagari, kana, Hangul and pinyin.
- Keep stable card IDs so switching languages does not reset the host's repeat history.
- Keep generated packs reproducible from local overlays; preserve all existing free content.

### Pose Coach

- Add opt-in on-device live observations with bounded frame processing and explicit unavailable/error states.
- Detect visible body/hand/face landmarks and relevant geometric prop candidates; do not claim identity recognition or semantic understanding beyond the detector.
- Stabilize guidance and ensure auto-capture depends on fresh observations, not an old ready frame.
- Add opt-in spoken guidance and hands-free commands where native on-device recognition is available.
- Separate speech output from command listening so the app cannot trigger itself.
- Cancel active analysis, countdown and audio when capture context changes or the app backgrounds.
- Keep physical camera orientation/mirroring separate from RTL text layout.
- Preserve the still-photo import, retake, collage, save and share workflow.
- Localize pattern directions and UI; use the chosen language's installed voice or disclose unavailability.

Capture timing needs an explicit clock conversion. Apple's [capture synchronization clock documentation](https://developer.apple.com/documentation/avfoundation/avcapturesession/synchronizationclock) states that output timestamps use the session clock; [CoreMedia conversion](https://developer.apple.com/documentation/coremedia/cmsyncconverttime(_:from:to:)) supports conversion to the host clock. The implementation uses this conversion and one host clock for both frame freshness and shutter deadlines, instead of assuming separate clocks share an epoch. Physical-device timing remains part of acceptance.

### Transcript Forge

Add persistent project pause/resume and clear-waiting controls in the local UI, API and MCP. Pausing lets an already running provider call finish and holds new waiting work. Clearing waiting work returns it to Not started without deleting successful results or interrupting active paid work. Persist transitions and reject stale jobs across restarts. Existing retry, search and export features remain in place.

## Evidence boundaries

The user authorized implementation without waiting for manual review. Automated compilation, regression tests and local screenshots still accompany the work. Physical-device camera quality, thermal behavior, real microphones, native speech support, linguistic/editorial review, store submissions and actual payment workflows remain separate verification. No cloud recognition cost or translation-service purchase is introduced by this increment.

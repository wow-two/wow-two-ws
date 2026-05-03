# Route Vibe Player

*Last updated: 2026-04-26 03:24 PM*

> Music player that scores your trip — feeds in the navigator's route, plays tracks that match each segment's vibe (e.g. Enya "Only Time" on the way back, hype on the highway, calm in the mountains).

## Problem

- Driving playlists are static. They don't react to where you are on the trip.
- Apple/Spotify "drive mixes" are mood-blind to *route shape* (climb, descent, return leg, scenic coast, urban gridlock).
- Manual scrubbing during a trip breaks the moment. The "right song" usually arrives by accident.

## Core Idea

Pipe the active **navigation route** + **live GPS** into a vibe engine that picks tracks per segment.

Inputs → Vibe → Music.

| Input | Source | Signal |
|---|---|---|
| Route polyline | Yandex / Google / Apple Maps share-link or screen capture | Shape, distance, ETA |
| Segment classification | OSM tags + elevation API | Highway / mountain / city / coast / forest |
| Live position | Phone GPS | Which segment is "now", time-to-next |
| Trip phase | Computed | Outbound / arrived / return |
| Time + weather | OS APIs | Sunrise drive, night, rain |
| User seed | Prompt | "Enya-style instrumental on return" |

Output: ordered queue with **per-segment cue points** — track swaps trigger when GPS crosses segment boundary.

## Architecture (one pass)

```
Navigator path → Route Parser → Segment Tagger → Vibe Mapper (Claude) → Track Picker (Spotify/Apple) → Cued Queue → GPS Trigger Loop
```

- **Route Parser:** decode polyline (Google `enc:`), Yandex JSON, GPX file.
- **Segment Tagger:** split into N segments by road class + elevation delta + speed limit.
- **Vibe Mapper:** Claude turns `(segment_type, phase, weather, user_seed)` → `(energy, valence, tempo, genre, mood_word)`.
- **Track Picker:** reuses logic from `spotify-mood-queue-project.md` per segment.
- **GPS Trigger:** background watcher on phone; crossfade when entering next segment.

## Differentiation vs `spotify-mood-queue-project.md`

| Aspect | Mood Queue | Route Vibe |
|---|---|---|
| Trigger | User prompt, one-shot | Continuous, geo-triggered |
| Unit | Whole queue | Per segment |
| Context | Mood text only | Route + position + phase + weather |
| UX | Pick once, listen | Set once, drive |

Route Vibe is a **superset** at runtime — Mood Queue becomes the picker module.

## Tech Stack

- **Mobile:** Flutter or React Native (need background GPS + audio session). iOS/Android.
- **Backend:** thin — just route parsing + Claude calls. .NET minimal API or Cloudflare Worker.
- **Music:** Spotify Connect first (largest catalog + audio-feature API), Apple Music v2 follow-up.
- **Maps:** start with Google polyline (most universal share format), add Yandex for UZ.
- **AI:** Claude API for vibe mapping + reranking.
- **Local DB:** SQLite cache of audio features for user library.

## Killer UX Moments

- Paste a Yandex/Google share-link → "Trip will have 4 vibes: city escape → highway run → mountain climb → return descent."
- Crossfade exactly as the road bends out of the city.
- "Almost there" — drops volume, swaps to ambient at last 2 km.
- Return leg auto-detect → switches to softer palette without asking.

## Risks / Open Questions

- **Background audio + GPS** drains battery; iOS background limits are strict.
- **Map app lock-in:** none of the major navigators expose a clean live-route API. Plan B = user shares URL once, we re-poll GPS independently.
- **Music API limits:** Spotify Connect requires a Premium device; Apple Music requires MusicKit token.
- **Vibe taste is personal** — needs a quick "👍 / skip" learning loop per user.
- **Driver attention:** UI must be glanceable / Siri/Assistant-driven. CarPlay & Android Auto integration is a real engineering line item.
- **Offline trips** (mountains, no signal) — pre-cache per segment before departure.

## MVP Scope (4 weekends)

1. Paste Google/Yandex share-link → render segments with vibes (no playback yet).
2. Spotify OAuth + queue per segment from user library.
3. iOS app with background GPS → swap track on segment crossing.
4. One curated "Enya return" template + one "Highway hype" template as defaults.

Skip for v1: CarPlay, Apple Music, learning loop, offline cache.

## Verdict

- **Buildable:** yes, all primitives exist (polyline decode, Spotify SDK, Claude, background GPS).
- **Novel:** yes — no shipping app combines route polyline + AI vibe mapping + per-segment cueing. Closest are static "road trip" playlists.
- **Strategic fit (wow-two):** sits naturally as an **app** layer atop the existing `spotify-mood-queue` picker → reuse, don't rewrite.
- **Recommendation:** park as **next app** after Mood Queue ships. Build Mood Queue's picker as a clean module so Route Vibe wraps it.

## Next Action

- Confirm Mood Queue picker is modularised before starting.
- Spike: decode Yandex share URL → polyline (UZ-specific blocker — verify first).

# PoseCoach — Trending Photo Pose Library + AR/AI Guide

*Last updated: 2026-04-26 12:00 PM*

> Browse a library of trending/iconic photo poses (Follow-Me, candid selfie, jump shot, etc.). Pick one → AR mask overlays the target silhouette on camera → AI coaches you in real time until your pose, framing, and angle match.

## Problem

- Most people freeze when the camera comes out — don't know what poses work, how to stand, where the photographer should be.
- Pinterest/Insta pose boards = inspiration only; no help executing.
- Pro photographers charge for what is mostly a known-pose vocabulary + composition rules.
- Trends evolve monthly (TikTok-driven) — static guides go stale fast.

## Concept

Three layers stacked:

- **Library** — curated, tagged, trending pose catalog (solo / couple / group / kids / pets · indoor/outdoor · vertical/horizontal · style: candid, editorial, golden-hour, mirror-selfie, follow-me).
- **AR mask** — silhouette + framing rectangle overlay on live camera; both subject and photographer get guidance (subject sees self-pose, photographer sees framing).
- **AI coach** — pose-detection model (MediaPipe / Apple Vision / MoveNet) compares user keypoints vs target → live nudges ("rotate shoulder 15°", "chin down", "step left", "lower phone 10cm"). Auto-shutter when match score > threshold.

## Market & Competition

| Player | Overlap | Gap they leave |
|---|---|---|
| PoseCam, PoseMe, Pose | Static silhouette overlay | No AI coaching, no trend feed, no framing for photographer |
| Snapchat / Instagram lenses | AR overlays | Filters, not pose teaching |
| Pinterest pose boards | Discovery | Inspiration only — no execution help |
| TikTok pose trends | Trend signal | No structured library, no how-to |
| ProCam / Halide | Pro camera UX | No pose layer |
| Lensa, Remini | AI photo gen/edit | Post-capture, not in-the-moment |

**True white space:** trend-curated library + real-time bidirectional coaching (subject AND photographer) + auto-capture. No single app does all three.

## Core User Flow

1. Open app → Trending tab (TikTok-style vertical feed of pose examples, looping video/photo).
2. Tap pose → see reference + tags + difficulty + required setup (solo/duo, indoor/outdoor, props).
3. Tap "Try it" → camera opens with silhouette overlay + framing box.
4. Two modes:
   - **Solo** (front cam, mirror): user sees self vs silhouette, AI nudges via voice/haptics.
   - **Duo** (rear cam): photographer holds phone, sees framing guides + subject-pose match score; subject can wear AirPods for audio cues.
5. Match score hits 90%+ → auto-shutter burst (5 frames) → best-frame pick.
6. Save → optional "share to Trends" → community vote feeds back into trending ranking.

## Differentiation

- **Bidirectional coaching** — most pose apps only help the subject; framing for photographer is the unsolved half.
- **Live trend feed** — fresh poses from TikTok/Insta scraped + curated weekly; competitors ship static packs.
- **Auto-capture on match** — removes the "say cheese" timing problem.
- **Skeleton-level AI feedback** — keypoint-vs-keypoint deltas, not just silhouette overlap.

## Tech Stack (MVP)

| Layer | Choice | Reason |
|---|---|---|
| Mobile | React Native + Expo, or native Swift (iOS-first) | iOS users = higher photo-app intent; ARKit + Vision are best-in-class |
| Pose detection | Apple Vision `VNDetectHumanBodyPoseRequest` (iOS), MediaPipe Pose (cross-platform) | On-device, real-time, free |
| AR overlay | ARKit / SceneKit (iOS); ARCore (Android) | Native silhouette compositing |
| Trend ingestion | Scrape TikTok/Reels hashtags → human curator queue → tag → publish | Quality > volume |
| Backend | Supabase (auth + storage + Postgres) | Fast, cheap to start |
| AI nudges | On-device keypoint diff → rule engine ("if shoulder.y delta > X → say 'lower shoulder'") | Latency-critical, no LLM needed for v1 |
| Voice cues | Native TTS | Free, private |

## MVP Scope (8–12 weeks, iOS-only)

- 50 hand-curated trending poses across 5 categories.
- Silhouette overlay (no skeleton-level coaching yet).
- Match-score auto-shutter at threshold.
- Save to Photos + simple share sheet.
- No accounts; no community in v1.

## V2 (post-PMF)

- Skeleton-level coaching with voice nudges.
- Photographer/subject split-screen mode (AirPods audio to subject).
- Community submission + voting → trending algorithm.
- Pose packs (couple, maternity, graduation, wedding).
- Brand/creator partnerships (sponsored pose packs).

## Monetization

- **Freemium** — 10 poses free, full library $4.99/mo or $39.99/yr.
- **Pose packs** — one-time purchase ($1.99 each: maternity, wedding, travel).
- **Creator marketplace** — photographers/influencers publish paid packs, app takes 30%.
- **B2B white-label** — wedding photographers, modeling agencies, real-estate agents.

## Risks & Open Questions

- **AR/pose accuracy across body types & clothing** — dark clothes, loose silhouettes degrade keypoint detection. Need tested fallback.
- **Cold-start trend curation** — who ranks trends? Manual curator for v1, ML clustering later.
- **Permission/UX cost of AR + camera + mic** — onboarding friction; mitigate with "demo mode" before perms ask.
- **Cultural pose variance** — poses trending in US ≠ Asia ≠ MENA; needs regional feeds.
- **Copyright on pose references** — using TikTok stills as previews = grey area; safer to recreate poses with stock models or AI gen.
- **Engagement decay** — pose execution is one-and-done per pose; need fresh trends weekly to retain.
- **Why not just a Snap lens?** — Snap can clone the AR mask in a quarter; moat must be the curated library + coaching IP, not the AR tech.

## Verdict (Quick Read)

- **Promise:** strong — combines three known-good primitives (trends, AR, pose AI) into a flow nobody owns end-to-end.
- **Defensibility:** medium — tech is commodity; moat = curation + brand + creator network. Build community fast or get cloned.
- **Effort to MVP:** low-medium — 1 iOS dev + 1 curator can ship in 8–12 weeks.
- **Most-likely failure mode:** trend feed dies → app becomes static pose library → competes with PoseCam (already exists, low growth).
- **Suggested first test:** ship the trending feed + silhouette overlay only (no AI coaching). If users repeatedly open the trends tab, the moat is real. If not, AI coaching won't save it.

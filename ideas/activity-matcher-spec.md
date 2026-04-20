# ActivityMatcher — Time-Aware Activity Recommendation Platform

*Last updated: 2026-04-20 08:00 PM*

## Section 1: Original Idea (Compact)

### What
Web app that ingests a structured activity catalog (venues, time tags, durations, types) and recommends what to do right now — based on current time, available window, group size, mood/type preference. Tashkent-first, city-expandable.

### Problem
You have 2 free hours on a Tuesday evening. Your brain goes blank. You open Google Maps, scroll aimlessly, give up, stay home. The activities exist — the matching doesn't.

Existing tools fail because: Google Maps = venue search, not activity search. TripAdvisor = tourist-oriented. Telegram groups = scattered, no filtering. Nobody answers "what can I actually do right now with 2 hours and 3 friends?"

### Core Loop
1. User opens app → current time auto-detected (e.g. Tuesday 7:30 PM)
2. App shows: "You have the evening. What are you in the mood for?" → type chips: Producing, Sports, Social, Culture, Active, Relaxation
3. Optional filters: duration (1h / 2h / half-day / full-day), group size (solo / 2–4 / 5–10 / 10+), indoor/outdoor
4. App returns ranked activity list — filtered by time compatibility, sorted by match score
5. Each card: activity name, venue, distance, price range, duration, "open now" badge
6. Tap → venue details, map link, booking link (if available)

### Data Model

```
Activity {
  id: number
  name: string
  venue: string
  category: enum (Active, Producing, Sports, Social, Museums, Galleries, Parks, Theatres, Educational, Cafes)
  subcategory: string          // e.g. "Pottery", "MMA", "Quiz Night"
  type: enum (Indoor, Outdoor, Both)
  bestTime: string[]           // ["M", "A", "E", "N"]
  duration: { min: number, max: number }  // minutes
  groupSize: { min: number, max: number }
  priceEstimate: string
  location: { lat: number, lng: number, address: string }
  links: { maps?: string, website?: string, instagram?: string, booking?: string }
  seasonal: boolean            // true = not year-round
  seasonMonths?: number[]      // [1,2,3] = Jan-Mar only
  tags: string[]               // ["adrenaline", "creative", "cultural", "team", "date-friendly"]
}
```

### Key Value Props
- Answer "what can I do RIGHT NOW?" — not "what exists in my city"
- Time-aware filtering is the killer feature no competitor has
- Data layer already built (activities.md catalog with 150+ entries, time-tagged)
- Expandable: any city can plug in its own activity catalog

---

## Section 2: Revision & Feasibility

### What Works
- **Data already exists**: `activities.md` has 150+ Tashkent activities with Best Time, Duration, Type, Price — ready to convert to JSON
- **Simple matching logic**: filter by time window → filter by category → sort by distance/rating. No ML needed for v1
- **Low infra cost**: static JSON data + client-side filtering = can run on free tier (Vercel/Cloudflare Pages)
- **Clear UX**: Tinder-meets-Google-Maps for activities. Everyone understands swipe/filter
- **Personal dogfooding**: you use this data weekly for weekend planning

### What Doesn't Work (As Described)

| Claim | Problem | Fix |
|-------|---------|-----|
| "Open now badge" | Need real-time venue hours — most Tashkent venues don't have reliable Google hours | v1: use time-of-day tags (M/A/E/N) instead of real hours. v2: crowdsource hours |
| "Distance sorting" | Needs user location permission + geocoded venues | v1: skip distance, group by district. v2: add geolocation |
| "Booking link" | Most venues don't have online booking | v1: show phone number + maps link. v2: integrate iticket.uz for theatres |
| "Any city can plug in" | Multi-city needs admin panel, moderation, content pipeline | v1: Tashkent-only, hardcoded. v2: city config files. v3: admin panel |

### Revised Architecture

**v1 — Static Site (MVP)**

```
React + Vite (or Next.js static export):
├── /data/activities.json          ← converted from activities.md
├── /components
│   ├── TimeSelector               ← auto-detect current time, allow override
│   ├── FilterChips                 ← category, group size, duration, indoor/outdoor
│   ├── ActivityCard                ← name, venue, time badge, price, duration
│   ├── ActivityDetail              ← full info + map embed + links
│   └── QuickMatch                  ← "I have X hours" → instant results
├── /lib
│   ├── matcher.ts                  ← core filtering + scoring logic
│   └── timeUtils.ts               ← M/A/E/N resolution, "is it evening now?"
└── /public
    └── og-image.png               ← social sharing
```

- Zero backend. All filtering runs client-side on a ~50KB JSON file
- Deploy: Vercel free tier or GitHub Pages
- Data updates: edit `activities.json`, redeploy (or pull from a Google Sheet)

**v2 — Dynamic (if traction)**

```
Add:
├── Supabase backend               ← activity CRUD, user favorites, ratings
├── Geolocation                     ← distance-based sorting
├── User accounts                   ← save preferences, history
├── City selector                   ← Tashkent, Samarkand, Bukhara
└── PWA                             ← installable, offline-capable
```

### Matching Algorithm (v1)

```typescript
function matchActivities(
  activities: Activity[],
  now: Date,
  filters: {
    categories?: Category[]
    maxDuration?: number      // minutes
    groupSize?: number
    indoorOnly?: boolean
  }
): Activity[] {
  const timeSlot = getTimeSlot(now)  // M, A, E, or N

  return activities
    .filter(a => a.bestTime.includes(timeSlot))
    .filter(a => !filters.categories?.length || filters.categories.includes(a.category))
    .filter(a => !filters.maxDuration || a.duration.min <= filters.maxDuration)
    .filter(a => !filters.groupSize || (a.groupSize.min <= filters.groupSize && a.groupSize.max >= filters.groupSize))
    .filter(a => !filters.indoorOnly || a.type !== 'Outdoor')
    .filter(a => !a.seasonal || a.seasonMonths?.includes(now.getMonth() + 1))
    .sort((a, b) => scoreActivity(b, now) - scoreActivity(a, now))
}

function scoreActivity(activity: Activity, now: Date): number {
  let score = 0
  // Prefer activities that match the exact time slot vs "any time"
  if (activity.bestTime.length <= 2) score += 10  // specific = higher signal
  // Prefer activities with more info (links, prices)
  if (activity.priceEstimate !== 'TBC') score += 5
  if (activity.links.website) score += 3
  // Slight randomization to avoid always showing same order
  score += Math.random() * 5
  return score
}
```

### Effort Estimate

| Phase | Scope | Effort | Deliverable |
|-------|-------|--------|-------------|
| **v0** | Convert activities.md → JSON | 2 hrs | `activities.json` with 150+ entries |
| **v1** | Static React app with filters | 2–3 days | Deployed on Vercel, shareable URL |
| **v2** | Add geolocation, favorites, PWA | 1–2 weeks | Installable app, user prefs |
| **v3** | Multi-city, admin panel, ratings | 1–2 months | Platform with content pipeline |

### Naming Candidates
- **Nima Qilamiz?** (Uzbek: "What shall we do?") — local, memorable, domain-friendly
- **ActivityMatcher** — generic but clear
- **Qayerga** (Uzbek: "Where to?") — short, catchy
- **Vaqt** (Uzbek: "Time") — ties to the time-matching core feature

### Competitive Landscape (Tashkent)

| Competitor | What it does | Why this is different |
|-----------|-------------|---------------------|
| Google Maps | Venue search by category | No time filtering, no "what can I do now?", no activity taxonomy |
| TripAdvisor | Tourist reviews | Tourist-oriented, not local-first, no time matching |
| iticket.uz | Event tickets | Only ticketed events (theatres, concerts), no activities |
| Telegram channels | Activity recommendations | Scattered, no filtering, no structure, ephemeral |
| Afisha.uz | Event listings | Event-only, no venue activities, no time matching |

### Open Questions
1. **Data maintenance** — who updates venues, prices, hours? Manual vs. scraping vs. community?
2. **Monetization** — featured listings? Premium venues? Or stay free as a personal/community tool?
3. **Scope creep** — should it include day-trip planning (combine multiple activities into a route)?
4. **wow-two fit** — is this a wow-two-apps product or a standalone venture? Depends on tech stack choice (.NET backend for v2 would make it wow-two)

---

## Section 3: Implementation Path

### Step 1: Data Pipeline (v0)
- Write a parser that converts `activities.md` tables → `activities.json`
- Add missing fields: lat/lng (from Yandex Maps links), groupSize estimates
- Validate: every activity has category, bestTime, duration

### Step 2: MVP Build (v1)
- React + Vite + Tailwind
- Single-page: filter panel on left/top, activity cards in main area
- Mobile-first responsive design
- Deploy to Vercel
- Share link in friend group for feedback

### Step 3: Iterate (v1.5)
- Add "Surprise Me" button — random activity matching current time
- Add "Plan My Day" — chain 2–3 activities into a sequence
- Add sharing: "I'm going to X — who's in?" → generates shareable card

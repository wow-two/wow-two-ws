# Mapbox

*Last updated: 2026-05-12*

## What it is

Location platform — maps, navigation, geocoding, and search APIs/SDKs. Alternative to Google Maps with stronger design control, vector tiles, and offline support. Used by BMW, Toyota, Rivian (in-car nav), Strava, AllTrails, Shopify, The Weather Channel.

## Core products

- **Maps SDK** — interactive vector maps (web / iOS / Android / Unity)
- **Navigation SDK** — turn-by-turn routing, traffic, voice guidance, lane assist
- **Search / Geocoding API** — address autocomplete, place lookup, reverse geocoding
- **Studio** — visual style editor (colors, fonts, layers, custom tilesets)
- **Movement & Boundaries** — anonymized traffic data, admin region polygons
- **Vision SDK** — AR overlays, on-device CV for driving
- **MapGPT / AI Assistant** — conversational location search (newer)

## What devs can build

- **Ride-hailing / delivery** — Uber-style apps: live tracking, ETA, dispatch
- **Logistics & fleet** — route optimization, driver dashboards, geofencing
- **Real estate / travel** — property maps, isochrones (drive-time zones), POI search
- **Outdoor / fitness** — trail apps, run trackers with elevation + offline maps
- **Automotive / in-car** — embedded navigation
- **AR / 3D experiences** — 3D terrain (Mapbox GL JS), AR overlays (Vision SDK)
- **Data viz dashboards** — heatmaps, choropleths, store locators, analytics
- **Games** — geo-based gameplay (Pokémon GO uses it for some regions)
- **IoT tracking** — assets, vehicles, pets, shipments — custom-styled maps

## Why pick it

- Full style control via Studio (Google Maps is rigid)
- Offline maps + on-device routing
- Often cheaper at scale, generous free tier
- Vector tiles → smooth zoom, smaller payloads
- Strong React / iOS / Android SDK quality

## When NOT to pick it

- Need Google ecosystem (Places reviews, Street View) → Google Maps
- Pure static map images, low volume → Leaflet + OpenStreetMap is free
- Enterprise GIS / heavy spatial analytics → Esri ArcGIS

## Pricing model (rough)

Pay-as-you-go per API call / tile load / monthly active user. Free tier covers small projects. Map loads, geocoding requests, and directions all metered separately. Check current rates — they shift.

## Links

- Docs: https://docs.mapbox.com
- Pricing: https://www.mapbox.com/pricing
- Studio: https://studio.mapbox.com
- GitHub: https://github.com/mapbox

## Alternatives

- **Google Maps Platform** — broader ecosystem, less customization
- **HERE** — strong automotive, fleet focus
- **TomTom** — navigation-centric
- **MapLibre** — open-source fork of pre-proprietary Mapbox GL (free, self-host)
- **Leaflet + OpenStreetMap** — free, lightweight, no vendor lock-in

## Ideas to revisit

- _Add ideas here as they surface — e.g. "use Mapbox + isochrones for `001-sb` apartment commute analysis"_

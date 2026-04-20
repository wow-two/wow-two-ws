# Gaussian Splatting — App Ideas & Research

*Last updated: 2026-04-20 03:00 PM*

## What is 3D Gaussian Splatting?

Real-time rendering technique that represents 3D scenes using millions of tiny 3D Gaussian primitives instead of triangles/meshes. Introduced by INRIA (2023), now the dominant alternative to NeRFs.

**Pipeline:** 2D photos → Structure-from-Motion → sparse point cloud → optimize 3D Gaussians (position, opacity, color, scale, orientation) → rasterize by projecting to 2D, sorting by depth, blending front-to-back.

**Key wins over NeRFs:** 100+ FPS real-time rendering (vs seconds/frame), no neural network at render time, editable primitives, runs in browsers via WebGL.

## Current Landscape

### Capture Apps (input side — solved)

| App | Platform | Speed | Pricing |
|---|---|---|---|
| Scaniverse (Niantic) | iOS/Android | 5-10 min on-device | Free |
| Polycam | iOS + web | Cloud, LiDAR support | $8/mo |
| Luma AI | Web | 20-60 min cloud | Free tier |
| Postshot | Desktop + cloud | Architecture focus | $15/mo |

### Tooling Layer (output side — wide open)

| Product | What | Gap |
|---|---|---|
| Zillow SkyTours | Internal RE tours | Not available to indie agents |
| Apartments.com (CoStar) | Exterior GS via Matterport | Enterprise-only |
| Gracia AI ($1.7M raised) | 4D GS + VR on Quest 3 | VR-first, no web consumer play |
| Volinga | Enterprise viewer + optimization | No API/developer story |
| Nerfstudio | Open-source training | Dev tool, not product |

### Key Trends (2026)

- **Web delivery** is the breakout: share a URL → view in browser, no app install
- **4D (dynamic)** maturing: capture motion, not just static scenes
- **Mesh extraction** now works (MILo, SIGGRAPH Asia 2025): GS → usable mesh pipeline
- **Pose-free reconstruction**: no camera calibration needed (LongSplat, NoPoSplat)
- **Enterprise adoption**: Zillow, Esri ArcGIS, DJI Terra, Foundry Nuke 17, AWS all shipped GS support

---

## App Ideas

### Tier 1 — High demand, underserved

#### 1. Real Estate Splat-as-a-Service API

> Backend API: agent uploads phone video → returns embeddable 3D tour widget

- **Problem:** Zillow does GS internally, but independent agents / small brokerages have nothing. Matterport is expensive and requires special cameras.
- **Solution:** .NET backend API that accepts video upload, orchestrates GS training (Nerfstudio/gsplat on GPU), returns embeddable `<iframe>` or JS widget.
- **Revenue:** Per-scan pricing ($5-15/scan) or monthly subscription.
- **Tech stack:** .NET API + queue (MassTransit) → GPU worker (Python/gsplat) → CDN-hosted viewer (Three.js/PlayCanvas) → embed widget
- **Moat:** Speed + simplicity. Agents don't want to learn tools — they want to upload a video and get a link.
- **Competitors:** Polycam (capture-focused, no embed story), Matterport (expensive, hardware-locked)

#### 2. GS Annotation & Collaboration Tool

> Figma for 3D splats — teams drop pins, measure, comment inside a GS scene

- **Problem:** Construction, architecture, insurance teams capture 3D scans but have no way to annotate, discuss, or track issues spatially.
- **Solution:** Web app where you upload a .ply/.splat file → navigate the scene → click to pin comments, measure distances, draw markup, tag teammates.
- **Revenue:** Per-seat SaaS ($20-50/mo per team).
- **Tech stack:** React + Three.js viewer → .NET API for annotations, comments, user management → real-time collab via SignalR
- **Moat:** Network effects (team collaboration), sticky workflow integration
- **Natural fit:** Combines wow-two backend strengths (SignalR, Clean Architecture) with the 3D web skills from `interactive-3d-web-experiences-spec.md`

#### 3. GS Asset Marketplace

> "Envato for splats" — creators upload scanned environments, buyers license them

- **Problem:** Game devs, filmmakers, VR creators need realistic environments but photogrammetry is slow. No marketplace exists for GS assets.
- **Solution:** Marketplace where creators upload GS captures (restaurants, parks, offices, landmarks), buyers browse with in-browser 3D preview and license for use.
- **Revenue:** Commission (15-30% per sale) + featured listings.
- **Tech stack:** .NET API + Stripe → React storefront with Three.js preview → CDN for asset delivery
- **Risk:** Chicken-and-egg supply problem. May need to seed with own captures initially.

---

### Tier 2 — Niche but monetizable

#### 4. Cultural Heritage Scanner (Central Asia)

> Partner with museums/historical sites in Uzbekistan — capture → host → embed on tourism sites

- **Angle:** Central Asia has world-class heritage sites (Registan, Ichan-Kala, Bukhara old city) with zero 3D digital presence. Government tourism push + grant money available.
- **Revenue:** Government contracts, tourism board partnerships, embed licensing to travel platforms
- **Differentiation:** Regional expertise + language access no Western startup has

#### 5. E-commerce 3D Product Viewer (Shopify Plugin)

> Merchant uploads phone photos of product → auto-generates 360° GS viewer widget

- **Problem:** Shopify merchants want 3D product views but current solutions (Sketchfab, Spline) require 3D modeling skills.
- **Revenue:** Shopify app subscription ($10-30/mo) + per-scan fees
- **Risk:** Shopify ecosystem is competitive, and GS quality for small objects is still inconsistent

#### 6. Construction Progress Tracker

> Drone footage per week → GS scene → diff visualization showing what changed

- **Problem:** Construction PMs do manual site visits or compare flat drone photos. No spatial diff tool.
- **Solution:** Time-series GS captures with automated change detection and overlay comparison
- **Revenue:** Enterprise SaaS ($200-500/mo per site)
- **Risk:** Requires drone integration, outdoor GS quality still varies

---

### Tier 3 — Experimental / moonshot

#### 7. 4D Event Capture

> Multi-camera rig at weddings/concerts → 4D GS replay, web-first

- Gracia AI does VR playback, but consumer web product doesn't exist
- Hardware setup complexity is high

#### 8. GS Game Level Editor

> Scan real locations with phone → import as playable game levels

- MILo (GS → mesh) pipeline is maturing but not production-ready
- Cool tech demo, unclear monetization

---

## Recommendation

**Start with #1 (Real Estate API) or #2 (Annotation Tool).**

Both play to existing strengths:
- .NET backend, Clean Architecture, MassTransit (wow-two ecosystem)
- Three.js / R3F knowledge (already explored in `interactive-3d-web-experiences-spec.md`)
- SignalR for real-time (already used in FlowDeck concept)

The capture side is commoditized (Scaniverse is free). The **tooling layer on top** is where value accrues — and it's wide open.

## Next Steps

- [ ] Pick one idea to prototype
- [ ] Build minimal .ply/.splat viewer in Three.js (shared foundation for any idea)
- [ ] Test GS training pipeline: phone video → Nerfstudio/gsplat → .ply output
- [ ] Estimate GPU costs for cloud training (Lambda, RunPod, AWS)

---

## Sources

- [Hugging Face — Intro to 3D Gaussian Splatting](https://huggingface.co/blog/gaussian-splatting)
- [Utsubo — Complete Guide (2026)](https://www.utsubo.com/blog/gaussian-splatting-guide)
- [Polyvia3D — Software Comparison 2026](https://www.polyvia3d.com/guides/gaussian-splatting-tools-comparison)
- [Volinga — 2025 Turning Point & 2026 Acceleration](https://web.volinga.ai/2025-turning-point-and-2026-trends-blog/)
- [Radiance Fields — Year End Wrap Up](https://radiancefields.substack.com/p/gaussian-splatting-year-end-wrap)
- [Cybergarden — 7 Open-Source Tools (2026)](https://cybergarden.au/blog/7-cutting-edge-open-source-gaussian-splatting-tools-for-2026)
- [INRIA — Original Paper & Code](https://github.com/graphdeco-inria/gaussian-splatting)
- [MILo — Mesh-In-the-Loop (SIGGRAPH Asia 2025)](https://x.com/antoine_guedon/status/1965013985927082013)
- [Spenser Dickerson on 2026 creative turning point](https://x.com/SpenserFX/status/2002052446646837517)

# Interactive 3D Web Experiences — Vision & Tech Stack

*Last updated: 2026-03-07 08:00 PM*

## Inspiration

**igloo.inc** — portfolio/agency site that nails:
- Cool interactive 3D animations synced to scroll
- HUD & UI-style components with glassy overlays
- Immersive storytelling through camera movement and scene transitions
- Clean, futuristic aesthetic

> "This has everything I love — we have to create such sites, we just have to."

Also see: **messenger.abeto.co** — tiny 3D planet concept (used for Meme World).

## Core Tech Stack

| Layer | Tool | Purpose |
|---|---|---|
| 3D Engine | Three.js / WebGL | Scene rendering, meshes, lights, materials |
| React Binding | @react-three/fiber (R3F) | Declarative Three.js in React |
| Helpers | @react-three/drei | Cameras, controls, text, loaders, shaders |
| Scroll Animation | GSAP + ScrollTrigger | Sync 3D transitions to scroll position |
| Shaders | GLSL (custom) | Distortion, glow, grain, dissolve effects |
| Dev Tweaking | Leva / dat.GUI | Real-time parameter tuning during dev |
| UI Animation | Framer Motion | HUD component enter/exit, hover states |
| Glass Effects | CSS `mix-blend-mode` + `backdrop-filter` | Glassy overlay panels |
| Post-processing | @react-three/postprocessing | Bloom, AO, vignette, film grain |

## Key Techniques

### Scroll-Driven 3D Storytelling
Camera position, object visibility, and UI transitions all keyed to scroll progress. GSAP ScrollTrigger maps scroll % → animation timeline. Each "section" of the page triggers a 3D scene transition.

### Custom Shaders
Fragment shaders for visual effects (noise distortion, chromatic aberration, glow). Vertex shaders for geometry animation (wave, morph, particle displacement).

### HUD-Style UI
Overlaid HTML/CSS components positioned over the 3D canvas. Uses `pointer-events: none` on overlay container, `pointer-events: auto` on interactive elements. Glassmorphism via `backdrop-filter: blur()` + semi-transparent backgrounds.

## Where This Applies

- **Meme World** — 3D game world (current project, using R3F)
- **Portfolio / Agency sites** — igloo.inc style showcases
- **Product landing pages** — immersive product reveals
- **wow-two SDK docs** — interactive API documentation with 3D demos
- **Any future venture** — this is a reusable skill set

## Learning Path

1. **Three.js fundamentals** — scene, camera, renderer, geometry, materials, lights
2. **R3F patterns** — useFrame, useThree, refs, declarative scene graphs
3. **Shaders (GLSL)** — start with ShaderToy, then custom R3F materials
4. **GSAP + ScrollTrigger** — scroll-driven timelines
5. **Post-processing** — bloom, AO, outline, film grain via EffectComposer
6. **Performance** — instancing, LOD, texture compression, draw call optimization

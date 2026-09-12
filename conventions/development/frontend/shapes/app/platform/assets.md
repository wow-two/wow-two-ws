# Assets

*Last updated: 2026-09-10*

> Images, fonts and public files in a built frontend.

## Imports

- must import source-owned assets through the bundler so references follow hashing and deployment base paths.
- must reserve `public/` for files requiring stable names; resolve their URLs against the configured base.
- must not hardcode filesystem paths or development-server URLs into deployed assets.
- must verify externally loaded resources against the host's origin/security policy.

---

## Images

- must declare meaningful alternative text or an explicit decorative empty alternative.
- must reserve layout space with dimensions/aspect ratio to prevent image-driven shifts.
- must provide suitable responsive sources/sizes for images whose rendered size varies.
- must defer offscreen images without deferring the primary visible content image.
- must release object URLs used for previews when replaced or disposed.

---

## Fonts

- must ship only licensed font files and the weights/scripts the app needs.
- must choose a fallback and font-display policy that keeps text available during loading.
- must preload only fonts needed for initial content and verify the preload URL matches the served resource.
- must test fallback and missing-font layout with long localized labels.

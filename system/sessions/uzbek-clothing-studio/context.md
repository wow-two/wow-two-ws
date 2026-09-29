# Ocharo Studio

*Last updated: 2026-09-26*

## Current state

Second iteration and interaction refinement are implemented in `workbench/ocharo-hq/ocharo-ws/workbench/ventures.ocharo-studio` (renamed from `ventures.uzbek-studio`).
Initial history: developer `323b2ed`; first implementation `646000a`. This iteration remains uncommitted.
The installed persistent commit switch reports OFF; no tool may enable it. A genuine standalone user directive
`~commit_on workbench/ocharo-hq/ocharo-ws/workbench/ventures.ocharo-studio` is required by the current workspace hook.

- Two placement anchors, scale/rotation and garment-relative shifts; schema-1 migration into schema 2.
- Amber selected-part outlines and clean exports; coherent authored UVs and demand-driven rendering.
- 46 material definitions, including 36 new catalogue choices from 29 classified products; 21 new texture fields.
- Generated WebP assets with per-product evidence and original PNG provenance; approved brand master copied separately.
- Responsive desktop/tablet/phone islands, contextual panels, corrected actions, combined save state and storybook.
- .NET 10/SQLite snapshot state, atomic revision conflicts, per-tab recovery, offline retry and bounded validation.
- Vue 3/TypeScript/Vite frontend with 21 external-style SFCs; React runtime and SDK dependencies removed.
- Vue SDK owns PointControl, interactive TourPopover, useVisitInvitation, LatestRevisionQueue and storage results; tested local pack adopted.
- PointControl, TourPopover and Modal have direct component/style exports; narrow CSS consumption avoids unrelated SDK styles.
- Editorial landing at `/`, lazy editor at `/studio`, removed canvas headline, native garment renders and catalogue gallery.
- SDK router loading state, draft-safe route navigation and focused-name recovery with one rename undo step.
- 82 frontend tests and 16 backend tests; final packaged production passes all 32 browser scenarios.
- Six responsive viewports, 31 served model/texture assets, texture decoding and container-volume durability verified.
- Residual old folder contained only `.idea/workspace.xml`; removed again after the user closed the IDE, absence verified.
- Approved wordmark and needle favicon, grouped material assignments/movement, New draft preservation and centered document name.
- Animated camera presets, reduced motion, pixel-scroll orbit and full-height framing shared across garments.
- Part dropdown resets inherited no-wrap, shrinks grid tracks, and centers on the toolbar on narrow phones.
- Left/right panels now share dimensions and corners at nine checked widths; inspector header stays fixed above inner scrolling controls.
- Removed canvas caption; current garment is beneath the header name. Removed decorative library footer and 22 dead CSS rules.
- Landing cards use oversized muted numbers; Baska glyph/copy/mesh/export now show waist-only pointed hip panels.
- Stronger amber silhouette and panel boundaries; exports hide selection, then restore it.
- Stable rename target contains focused input in the tour; important labels 13px, helpers 12px; editor marketing copy removed.
- Phone/tablet camera controls, wrapped hint and Guide no longer stretch or overlap; new browser regression verifies bounds.
- Material Studio at `/studio/materials`, alias `/materials`, opens from header Materials or inspector Edit material.
- Shared relative material scale updates draft and previously saved looks; other placement fields stay per part.
- Atomic material metadata persists in SQLite and browser recovery; stale thumbnails are invalidated on material saves.
- Material preview cancellation, dirty navigation, legacy appearances, undo/reset and portable import/export are covered.
- Blurred SDK dialogs replace native confirmations and existing dialog shells; `useConfirmation` is reusable.
- Route-focused workspace outline removed; notification border invariant and phone header hit targets pass regressions.
- GitHub rename is verified at `sulton-max/ventures.ocharo-studio`; account switched to `sulton-max`.
- Local origin still points at the former name. `git remote set-url` is blocked by the workspace Git hook and handed to the user.

## Managed runtimes

- Vite landing: `https://127.0.0.1:8262/`; editor `/studio`, managed exec session `10796`.
- Vite reads existing certificates through `STUDIO_TLS_CERT=/Users/max/.vite-plugin-mkcert/cert.pem` and
  `STUDIO_TLS_KEY=/Users/max/.vite-plugin-mkcert/dev.pem`, bypassing mkcert execution and trust changes.
  An attempted mkcert-based restart was rejected by automatic approval; the direct-certificate restart succeeded.
- API: HTTPS `8260`, HTTP `8261`, managed exec session `80054`.
- Production: `http://127.0.0.1:18260/`, editor `/studio`, materials `/studio/materials`, Docker container `ocharo-studio-review`, managed exec session `83866`.
- Production review database: named volume `ocharo-studio-review-data`.
- Final image: `sha256:9798c4d0f18e5e577e0a1e7fed2787a93686bb78b4d911247bf11f1be510de77`.
- Keep these alive for related review turns; inspect logs before restarting task-owned processes.
- A separate user-owned IPv6 Vite instance may exist; do not stop it. Use the explicit IPv4 review URL above.

## Review artifacts

- Product `engineering/planning/verification.md`: commands, results, runtime, remote-update command and limits.
- Product `engineering/planning/studio-refinement.md`: completed UI checklist, normalized API plan and render decisions.
- Product `engineering/planning/studio-evolution.md`: current logic audit, material ownership/migration and hero proposal.
- Product `engineering/research/brand-and-render-assets.md`: authoritative logo and eight-scene inventory.
- Product `engineering/planning/ocharo-iteration.md`: acceptance checklist and implementation contract.
- Product `engineering/research/catalogue-materials.md`: coverage across all classified catalogue products.
- SDK `engineering/architecture/ocharo-studio-adoption.md`: extracted units and compatibility note.

## Git boundaries

Product changes are owned by this lane except the unstaged `engineering/research/catalogue-evidence.md` edits.
Shared UI SDK contains unrelated AlertModal edits; preserve those. Another lane advanced HEAD to `3295e9f` and release metadata 0.0.7.
The local Ocharo tarball contains unpublished additions beyond that registry release. The shared SDK index was
cleared by another lane; this lane's explicit files were restaged. Unrelated AlertModal changes remain unstaged.
The SDK persistent commit switch is ON for another chat; this chat must not commit using that permission. Only explicit Ocharo SDK paths may be staged. Product uses its checked-in local SDK tarball,
so no SDK publication is necessary for review. External custom StorageBroker implementers need a boolean-return
migration if adopting the changed SDK interface; release policy remains relevant before publication.
Current local pack: `wow-two-beta-ui-vue-0.0.7-ocharo-modal.tgz`, SHA-256
`79abd50c3bbaa30cd10aba3719cc185b73ddefad9ea8371c345575b5da260052`; the obsolete guided-tour pack was removed.
SDK modal changes passed 2 hook tests, 24 overlay DOM tests, typecheck/409 SFC compilation, build and 79 packed exports.

Root registration changes share files with other lanes; keep only Ocharo hunks in this lane. No push, amend, account
transfer, or package publication is authorized. The user owns manual browser QA.

## Remaining review

Garment fidelity, actual touch devices, Safari/Firefox and formal device profiling need human review.
Sizing/length, decoration overlays, free attachments, physical simulation, accounts and cloud collaboration remain deferred.
Maftuna's source workspace remains unchanged.

Render output type and the exact six scene IDs remain pending user answers. The source has eight raster scene
references and a generated adult model baseline, but no rigged character or 3D scenes. The source inventory is
`engineering/research/brand-and-render-assets.md`; normalized API and future capabilities are in
`engineering/planning/studio-refinement.md`. The current backend uses SQLite JSON snapshots, no Redis.

The user confirmed shared-scale updates affect previously saved looks. The dedicated Material Studio is implemented
with a local preview and explicit save, workspace metadata revision stamps, atomic saved-look propagation and recovery.
Relative scale uses the existing mapping; legacy part scales remain until a fabric is explicitly saved. Immutable
material history, variants, metric panel UVs and stable surface attachments remain proposals. Those capabilities
require a mapping/schema migration; existing offsets/anchors and the renderer's vertical repeat factor are preserved.
Landing hero recommendation remains a three-textile sampler with exact design handoff; analyzed only.

Current geometry source is the deterministic Three.js author script, not a Blender-authored master. Baska improved;
source-based shoulder/cloth/cape/sleeve work for the other families remains proposed in the evolution analysis.

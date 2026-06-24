# Design exploration

*Last updated: 2026-06-24*

> What — how we arrive at product UI: render a few in-context variants per decision, pick + lock, cascade into the next round, persist to a per-app spec.
> The method, not the visual style (that lives in each app's design spec).
> Purpose — turn "make it look better" into a sequence of small, attributable, reversible choices; kill bikeshedding + decision-fatigue by comparing real
> rendered options, not prose.
> Use case — any new screen, redesign, or non-trivial component where look-and-feel is undecided; reach for it before writing component code.

## Method — variant-driven (default)

1. anchor on refs — analyze 1–N inspirations; name the moves worth stealing (palette, type, spacing, a signature layout trick).
2. decompose into ordered decisions — split the look into axes; resolve **one axis per round**, never blended.
3. render variants — 3–4 per axis, each the *same* component/screen rendered that way, with a 1-line tradeoff + one marked recommendation.
4. pick + lock — user selects one; restate the locked value (`hex` / token / name) as fixed.
5. cascade — every later round honors all locked decisions (a locked canvas tints all later mocks, etc.).
6. compose — assemble the locked axes into the full screen.
7. derive dark + states — invert tokens for dark; then empty / validation / loading / mobile.
8. persist — write/append the per-app design spec (the durable artifact; chat is not).
9. map to code — translate tokens → theme vars + components; apply across the app's screens.

---

## Decision order

- default funnel — `canvas/colors` → `accent/brand` → `type` → `layout/shape` → `components` → `content states` → `responsive` → `motion`.
- colors-first when the brand color is the emotional anchor (consumer / creator products); start from the canvas tint and build out.
- reorder when the risk is elsewhere — IA/layout-led product → wireframe first (see *Other modes* → progressive fidelity).
- one axis open at a time; close it before opening the next.

---

## Rendering the variants

- in-context, never abstract — a button on the real card beats a naked swatch; density + contrast only read true in situ.
- 3–4 options — fewer is a false binary, more is paralysis.
- hold all else constant — only the axis under test varies, so the choice is attributable.
- steer — each option gets a 1-line tradeoff + one marked **recommended**; the user still overrides.
- real content — real strings (short-links, `hex`, URLs, names); never lorem.
- same scale, side-by-side — comparison is visual, not sequential.

---

## Locking & cascading

- after each pick, restate the winner as a fixed token/value; it joins the running locked set.
- a later variant that violates a lock is invalid — regenerate it, don't renegotiate the lock mid-round.
- the locked set only grows; it *is* the spec-in-progress.

---

## Light → dark

- design light first when brand color leads; derive dark by inverse token mapping — canvas↔ink, surfaces raise, accent brightens for contrast.
- keep brand identity recognizable across modes; functional/literal surfaces (a QR tile, a product photo) may stay fixed in both.
- verify both modes before locking a screen — never lock on light alone.

---

## Persisting the spec

- one per-app spec md — `workbench/{repo}/platform/research/design-research/design-research.md` (or the repo's analogue).
- super-compact — token tables (light + dark) · semantic→`@wow-two-beta/ui` mapping · type · layout/shape · component rules · usage don'ts · iterate-next.
- append per iteration; this doc is what the code / SDK-mapping step consumes.

---

## Other modes

| Mode | What | When |
|---|---|---|
| variant-driven (A/B/n) | a few in-context options per axis → pick → lock | choosing a direction; look-led — **default** |
| reference teardown | extract palette/type/spacing/layout moves from inspirations | starting cold with refs in hand |
| token-first | define semantic tokens + theme vars (light/dark parity) before building | cross-app consistency / design-system work |
| component-state matrix | render *all* states of one component at once | a single complex component |
| progressive fidelity | grayscale wireframe → tokens → hi-fi | layout/IA is the risk; avoid early color bias |
| responsive frames | one screen at mobile / tablet / desktop, side-by-side | layout must hold across breakpoints |
| tournament | many candidates → pairwise elimination | huge space — logo, hero, illustration |
| critique pass | score a comp against a heuristics checklist | before locking / after composing |

- state-matrix covers — `default · hover · focus · active · disabled · loading · error · empty · selected`.
- modes compose — most real work is `reference teardown` → `variant-driven` per axis → `critique pass` → `responsive frames`.

---

## Mode selection

- "pick a direction (color / type / style)" → variant-driven.
- "starting from inspiration" → reference teardown → variant-driven.
- "consistency across apps" → token-first.
- "one tricky component" → component-state matrix.
- "layout / IA uncertain" → progressive fidelity (wireframe first).
- "must work phone + desktop" → responsive frames.
- "enormous option space" → tournament.
- "is it good enough?" → critique pass.

---

## Principles

- show, don't tell — a rendered option beats any description.
- one variable at a time — clean, attributable choices.
- recommend + tradeoff — never dump options without a steer.
- lock & cascade — decided = fixed; it constrains the next round.
- in-context + real content — judge on the real surface with real strings.
- light first, dark derived, both verified.
- the spec is the deliverable — not the chat history.
- small reversible locks — revisit one axis without redoing the rest.

---

## Anti-patterns

- blending axes in one mock (color + layout + type) — the choice isn't attributable.
- naked swatches / lorem — fine in the abstract, breaks in context.
- more than ~4 options — choice paralysis.
- options with no recommendation — dumps the whole load on the user.
- skipping the spec — decisions evaporate into scrollback.
- designing dark independently — drifts from light; derive it.
- locking a screen on the light theme only.

---

## Workflow checklist

- [ ] refs analyzed, moves named
- [ ] axes ordered; one open at a time
- [ ] 3–4 in-context variants + a recommendation each
- [ ] pick locked + restated
- [ ] locks cascaded into later rounds
- [ ] full screen composed
- [ ] dark derived; both modes verified
- [ ] states covered — empty / validation / loading / mobile
- [ ] per-app spec written / appended
- [ ] mapped to theme tokens + applied across screens

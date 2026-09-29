# Logo system

*Last updated: 2026-09-29*

> Logo composition and assets for WoW2 platform apps, SDK families and foundational tools; excludes consumer ventures.

## Scope

- must assign identity to an independently encountered product or family
- must reuse SDK family artwork for individual packages; show package names as ordinary text
- must express versions, channels and environments as text or UI badges
- may give foundational tooling its own identity when independently named and encountered
- must keep consumer ventures outside this family system

---

## Composition

- must choose among these four composition families by surface

| Family | Placement | Requirement |
|---|---|---|
| Primary horizontal | Headers, docs, introductions | Default |
| Standalone symbol | Compact navigation, diagrams, favicon source | Core |
| App tile | Launchers, avatars, square cards | When those surfaces exist |
| Endorsed composition | Introductions needing parent attribution | Optional |

- must build compositions from the same approved symbol and lettering
- may integrate the symbol into the initial letter without repeating that initial
- must treat tile backgrounds as carriers for the approved symbol
- must keep color, resolution and file-format variants outside the composition count
- must keep the ordinary product header unendorsed
- must keep the parent brand free of self-endorsement

---

## Derivatives

- may add a stacked composition when primary and standalone forms cannot serve a real placement
- may use a wordmark alone when the placement calls for lettering without the symbol
- must treat separate lettering as a source component, not another mandatory composition
- may adjust a micro symbol when tested small sizes lose recognition or close negative space
- must preserve the approved silhouette when simplifying micro details
- may add a true one-ink variant for a constrained output surface
- must treat social artwork as a layout containing the logo, not a new identity
- must derive native icon bundles from the target platform's actual packaging requirements

---

## Construction

- must use deliberate corner treatment, readable weight and controlled negative space
- must balance symbols optically beside lettering and within product lists
- must distinguish products by silhouette, not color alone
- must keep product metaphors, exact geometry, lettering and palettes in product brand guides
- must not require every product to repeat the parent's object, initial or palette
- must preserve approved geometry during routine export and composition
- must submit geometry changes for visual review through [design exploration](../research/design-exploration.md)

---

## Lettering

- must start new wordmark studies with [Nunito Sans](https://github.com/google/fonts/tree/main/ofl/nunitosans)
- must retain existing approved lettering until a product-specific revision is selected
- must record the selected font source, weight, casing and tracking in the owning brand guide
- may keep application UI typography separate from the logo's lettering

---

## Internal separators

- must apply this baseline only to intentional gaps in segmented or faceted symbols
- must start gap width near `1/24` of the greater visible width or height, excluding export padding
- may adjust by `±10%` for optical balance; this is a starting tolerance, not automatic approval
- must measure perpendicular to straight gap midbodies, excluding rounded ends and junctions
- must compare equal maximum visible extents, actual navigation slots and placement beside lettering
- must preserve outer contours, rounded ends, intended taper, product metaphor and intentional facet colors
- must keep separators transparent across surface variants
- must record the chosen separator width in the owning brand guide
- must not add separators to an identity that has none
- must not apply this baseline to letterspacing, export padding or symbol-to-text spacing

---

## Endorsement

- must source parent artwork from the [WoW2 brand guide](../../../docs/brand/wow2/brand.md)
- must compose a neutral `by` label with the exact approved WoW2 artwork
- must place the endorsement beneath the product identity
- must keep the parent artwork subordinate to the product identity
- must preserve the parent asset's aspect ratio, internal spacing and approved surface variant
- must compose supplied artwork deterministically; no generated redraw or approximate font replacement
- must reserve `powered by` for an actual technology-dependency relationship
- must omit endorsement when its readable minimum cannot fit; place ownership context elsewhere
- must leave tiny product symbols and app tiles free of parent endorsement

---

## Surfaces

- must pair unfamiliar symbols with a visible product name when space permits
- must provide an accessible product name for standalone navigation controls
- must avoid duplicate accessible names when adjacent text already names the same control
- must review primary and symbol artwork on intended light and dark surfaces
- must inspect symbols at `16`, `20`, `24` and `32` CSS pixels, including square favicon slots
- must record those sizes as review targets until actual results establish a minimum
- must record tested minimums separately for primary, symbol and endorsed compositions
- must test app tiles under their intended platform masks
- must keep logo clear space separate from export padding
- must define clear space and allowed backgrounds in the owning brand guide

---

## Masters

- must keep one brand guide as the owner of approved artwork and product-specific usage values
- must keep original generation output or design source alongside reproducible export inputs
- must distinguish approved design, exported assets and application integration status
- must identify the master as raster or vector in the guide
- must use editable paths for a claimed vector master; an embedded bitmap remains raster
- must preserve editable lettering separately when production lettering is outlined
- must keep counters transparent across surface variants
- must document intentional opaque backgrounds, including app-tile carriers
- must avoid claiming additional detail from raster upscaling

---

## Exports

- must record source hashes, source dimensions, transforms and export dimensions
- must record the exact parent asset and its hash for endorsed exports
- must save a portable export command with its runtime dependencies
- must replay into a separate directory and verify the outputs match the saved exports
- must compare decoded pixels when file metadata prevents byte-identical raster output
- must inspect transparency and alignment on contrasting backgrounds
- must save a review sheet showing the delivered compositions and tested sizes
- must keep rejected explorations separate from the approved asset inventory
- must update the guide and compositor inputs when an approved master changes

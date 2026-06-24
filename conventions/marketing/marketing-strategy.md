# Marketing Strategy

*Last updated: 2026-06-23*

> **What** — the go-to-market playbook for a bootstrapped, low-cost wow-two micro-SaaS: which channels, in what order, with what metrics. Scope: acquisition → activation → retention; not brand naming (see `brand-naming-and-domains.md`).
> **Purpose** — make GTM a repeatable decision (distribution is ~70% of the outcome) instead of a scramble; protect unit economics while growing.
> **Use case** — planning a launch, picking channels, setting pricing/CRO, or instrumenting a funnel for any product.

## Laws

- **distribution ≈ 70% of the outcome** — GTM is the lever, not more features.
- **pick 1-2 primary channels and master them** — not scattershot (the "exactly one" rule is too rigid).
- **for a search-driven category → SEO is primary** — highest-leverage + compounding, but slow (6-12mo to bite).
- **retention-first** — fix the leaky bucket before scaling acquisition; a flat-then-zero curve makes acquisition a treadmill.
- **calm lifecycle** — sparse, useful email only; *more* email can lower DAU/MAU (GWDNBM-native).
- **price for fee-efficiency** — a sub-$3/mo *monthly* plan loses ~33% to Stripe (`$0.30 + 2.9%`) → bill **annually** or bundle.

---

## Channel taxonomy

| Channel | Effort | Payoff lag | ROI | When |
|---|---|---|---|---|
| SEO content + comparison pages | high | 6-12mo | high, compounding | from day 1 (primary if search-driven) |
| Programmatic / long-tail pages | med (templated) | 3-9mo | high **if** ≥500w unique; ~⅓ fail on thin content | after core content proven |
| Launch platforms (IndieHackers · Reddit · Product Hunt) | low-med | days | spiky launch bump | at launch — IH/Reddit before PH |
| Directories (AlternativeTo · G2 · Capterra) | low | weeks | steady BOFU | post-launch |
| Integrations / marketplace (Zapier · Make · Slack) | med-high | weeks-mo | high per integration | when an API/public hooks exist |
| Lifecycle email (calm) | low | immediate | retention, not acquisition | from the first user |
| Referral / word-of-mouth | low | slow | compounding | once retention is solid |
| Paid ads | $$$ | immediate | poor at low ARPU | rarely for bootstrapped |

---

## SEO for a crowded / commodity category

- target **3 intents:** problem-aware/commercial · **comparison** "X vs Y" / "X alternative" (BOFU, ~7.5% convert) · trust tutorials.
- **comparison pages = fastest BOFU win** — and "vs the manual/status-quo" often beats "vs a competitor" for an early product.
- **programmatic SEO** for combinatorial long-tail (use-case × type × feature) — but each page needs **≥500 words + ~30% unique** or risk a thin-content penalty (~⅓ of pSEO craters).
- topical authority = a cluster of genuinely useful pages, not volume; earn a few real backlinks.

---

## Launch sequence

- **pre-launch** (wks −4→0): analytics in · demo GIF/video · seed 3-5 communities · first blog posts · schedule Product Hunt · a lead magnet.
- **launch**: IndieHackers + the subreddits where the pain lives → **Product Hunt** (12:01 PT reset; ask for *comments/visits*, never upvotes) → submit to directories.
- **growth**: review CAC by channel → cut losers, double the winner → pursue integrations / partnerships.

---

## Activation & retention

- define the **aha moment** (first real value) + a **magic number** (an action threshold that correlates with retention); drive onboarding straight to it.
- **retention is the foundation** — measure cohort retention before spending on acquisition.

---

## Pricing & CRO

- **free tier ≈ 70% of paid value**; a free→paid rate **< 2%** signals a PMF problem.
- transparent flat pricing + an **annual option** (fee efficiency + commitment); a higher tier **anchors** the one you want sold.
- pricing page essentials: one clear value-metric · comparison vs incumbents · FAQ · social proof.

---

## Metrics + minimal analytics

- **privacy-respecting analytics** (Plausible-style) — on-brand for a calm product, no cookie banners.
- track the **funnel:** visit → signup/guest → **activation** (first value) → paid → retained. One number per stage.

---

## GTM workflow

1. pick the **value-metric** + the **aha**. 2. ship the **free magnet** + a fast activation path. 3. lay the **SEO foundation** (content-type + comparison pages). 4. **launch** (IH/Reddit → PH → directories). 5. wire a **calm lifecycle**. 6. **measure the funnel**, cut/scale by CAC. 7. add **integrations** once an API exists.

---

## Checklist (before launch)

- [ ] one value-metric · fee-efficient pricing (annual for any sub-$3/mo plan)
- [ ] aha + magic number defined **and** instrumented
- [ ] free magnet live · SEO content-type + comparison pages (≥500w each)
- [ ] launch list ready: IH/Reddit → PH (12:01 PT, comment-asks) → directories
- [ ] calm lifecycle only · privacy-first analytics · full funnel tracked

---

## Confidence & sources

- **practitioner-consensus**, not this-run-verified — the deep-research adversarial-verify phase was **rate-limited both runs**; claims rest on the cited sources + general practice. Re-verify a specific number before betting on it.
- the Stripe-fee math is plain arithmetic (`$0.30 + 2.9%` per charge).

> Sources: a16z (growth/retention) · Search Engine Land (programmatic SEO) · churnkey · Powered by Search (comparison pages) · Passionfruit (pSEO failure rates) · OpenHunts 2024 (IndieHackers vs PH) · Plausible (SEO-only bootstrap case).

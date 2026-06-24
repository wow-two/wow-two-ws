# Brand Naming & Domains

*Last updated: 2026-06-22*

> **What** — how a wow-two product / venture picks a brand name + domain: style taxonomy, a house scoring rubric, a verification runbook, domain strategy. Scope: the name+domain decision only — not visual identity or copy voice.
> **Purpose** — make naming a repeatable, defensible decision (distinctive + legally usable + ownable) instead of a vibe, and dodge the rename / relaunch / legal tax of a bad pick.
> **Use case** — reach for it when naming a new product, venture, or repo — and before buying any domain.

## Laws (non-negotiable)

- distinctiveness **>** description — memorability is the primary objective; forgettable loses. don't describe, differentiate. [Lexicon/Placek]
- trademark-ability is a **gate**, not a nice-to-have — pick "the best name you can *legally use*", not the best name. [Igor]
- USPTO distinctiveness spectrum gates the weak end: `generic` = never registrable · `descriptive` = only with acquired secondary meaning (years of use) · `suggestive`/`arbitrary`/`fanciful` = protectable day one. **aim suggestive-or-stronger.** [USPTO]
- the name carries the **wedge** (your differentiator), never a single feature/format you will outgrow.

---

## Style taxonomy

| Style | What | Wins when | Fails when | Example |
|---|---|---|---|---|
| descriptive / functional | says what it does | brand equity is pushed to the *company* name; SEO-first | crowded category → blends in, weak TM | `Subway` |
| suggestive | hints at the benefit | want clarity **and** protectability | hint too literal → slides to descriptive | `Stripe` |
| evocative | evokes the positioning | rare → strongest differentiator | needs marketing to seed meaning | `Uber`, `Apple` |
| invented / coined | a new word | maximal ownability + TM headroom | empty until marketed; spelling risk | `Sonos` |
| compound | 2 roots fused | wedge + ownable + buyable domain | clunky past ~12 chars | `Facebook` |
| acronym | initialism | only if it spells a pronounceable word | raw consonants → unsayable, untrademarkable | `IKEA` ok / `PQCL` no |
| backronym | coin a word, fit a phrase | pronounceable + tells a story | forced, contrived expansion | `everlode` |
| metaphor | a borrowed image | depth, rewards a second look | obscure reference | `Amazon` |
| eponymous | founder / person | personal brand, agency | impersonal product; exit risk | — |

- wow-two default → **suggestive** or **compound-coined** (distinctive + protectable + domain-buyable). avoid descriptive-primary and raw acronyms.

---

## Scoring rubric (house — opinion-weighted)

Score each finalist `0-10` per axis × weight; compare totals. Weights are a house default — tune per product.

| Axis | Wt | `0-10` anchor |
|---|---|---|
| wedge-carry / distinctiveness | ×3 | evokes the differentiator + stands apart in-category |
| trademark-ability | ×3 | suggestive+ and clears search — **gate** (a 0 kills it) |
| radio test (heard → spelled right) | ×2 | one obvious spelling; no homophones / accent forks |
| pronounceability (seen → said right) | ×2 | ≤3 syllables, one obvious reading |
| expansion room (not tech/format-locked) | ×2 | houses future products; cap at 4 if a feature word is in it |
| tone / sound-symbolism fit | ×1 | phonetics match the promise (see cheatsheet) |
| length / shape | ×1 | ≤~12 chars; one word or a tight 2-root compound |
| domain-ownability | ×2 | clean exact-match on a credible TLD, no forced prefix — **gate** |

- any **gate axis at 0** (trademark / domain) eliminates the name regardless of total.
- Placek's tell: if the team is *comfortable*, it's probably not distinctive enough — pressure-test with *"a competitor just launched as X — your reaction?"*

---

## Sound-symbolism cheatsheet (tone-match — directional)

- trust / reliable / grounded → plosives `b d g k p t` + soft sonorants `m l n r w` (`b` reads most reliable). use for calm / infrastructure / GWDNBM brands.
- speed / sharp / hype → fricatives `f s v z`, `x`, sharp front vowels — *fights* a calm promise; use only for performance/disruption brands.
- small / light / fast → front vowels `i e` · big / solid / premium → back vowels `o u a`.
- match phonetics to the promise — a calm product with a buzzy name self-contradicts. [Yorkston (Stanford) · Lexicon — directional, not law]

---

## Verification runbook (gate before buying)

Run in order; a fail at any **gate** stops the name.

| # | Check | Tool / source | Pass bar |
|---|---|---|---|
| 1 | domain availability | RDAP — `rdap.org/domain/{d}`; `.com` via `rdap.verisign.com/com/v1/domain/{d}` (`404` = free); WHOIS fallback | exact-match free on a credible TLD — **gate** |
| 2 | trademark — US | USPTO Trademark Search `tmsearch.uspto.gov` (replaced TESS, 2023) | no live confusable mark in your class — **gate** |
| 3 | trademark — EU / intl | EUIPO `eSearch plus` · WIPO `Global Brand Database` | no blocking mark in target markets |
| 4 | common-law / web | Google SERP — exact + `"name" + category` | no active same-class company — **gate** |
| 5 | social + code handles | X · Instagram · LinkedIn · GitHub org (Namechk-style sweep) | primary handles free or a close variant |
| 6 | cross-language safety | native check across each target language | no slur / vulgar / negative connotation — **gate** |
| 7 | SEO collision | SERP for the bare name | not buried under a strong unrelated entity |

- trademark search is a **clearance signal, not legal advice** — a serious mark gets a TM attorney's final clearance.

---

## Domain strategy

- **TLD by audience:** `.com` = broadest trust (SMB / consumer) · `.io` = dev/tech-credible · `.app` = Google-backed, HTTPS-forced, "platform" read · `.co` = acceptable `.com` fallback.
- one-word `.com` is **exhausted** — expect to coin/compound or take `.io`/`.co`/`.app`. a clean exact-match on `.io`/`.co` beats a polluted `get-`/`use-` `.com`.
- **exact-match > prefixed** — use `get-`/`try-`/`-hq`/`-app` only as a deliberate fallback. avoid hyphens + number/letter homophones (`2`, `4`, `Q`).
- **brandable-primary + keyword-domain redirect** — own the brand domain *and* a descriptive SEO domain that `301`s to it; brand + SEO, each doing its job.
- **defensive regs** — grab the primary + the obvious typo/TLD variants you can afford (esp. the `.com` if cheap); park → redirect to primary.

---

## Decision workflow

1. **diverge** — generate ≥20 candidates across ≥3 styles (suggestive · compound-coined · one descriptive keeper).
2. **shortlist** — drop anything that names the tech/feature or fails the radio test said out loud.
3. **score** — run the rubric on the top ~8; keep the top 3-4.
4. **verify** — run the runbook on finalists; any gate-fail eliminates.
5. **pressure-test** — competitor test + say it on a call; sit with it 48h (comfort ≠ correct).
6. **register** — buy the primary + defensive variants; lock social + GitHub handles the same day.
7. **record** — log the pick + runner-up + why in the product's `business/` context.

---

## Final checklist (go / no-go before buying)

- [ ] suggestive-or-stronger (not descriptive/generic) · carries the wedge, not a feature
- [ ] passes the radio test out loud · ≤3 syllables · one obvious spelling
- [ ] domain exact-match free on a credible TLD (RDAP-confirmed)
- [ ] no live confusable trademark in-class (USPTO + EUIPO/WIPO)
- [ ] no same-class company (common-law / web) · handles available
- [ ] clean across target languages · phonetics match the promise
- [ ] defensive variants + handles registered the same day

---

## Confidence & sources

- **primary-cited** (high confidence): style taxonomy · descriptive-fails · distinctiveness-first · trademark-gate · USPTO spectrum → Igor Naming Guide, Lexicon/Placek, `uspto.gov/trademarks/basics/strong-trademarks`.
- **house-opinion** (tune freely): the rubric **weights** + the sound-symbolism cheatsheet — synthesized from Placek/Igor + Yorkston + a prior naming workflow; not empirically verified.
- **standard tooling** (stable facts): RDAP/WHOIS · USPTO Trademark Search · EUIPO eSearch plus · WIPO Global Brand Database.
- distilled from a deep-research pass whose adversarial-verify phase was **rate-limited** on the rubric / domain / toolchain axes → those rest on practitioner consensus, not this run's 3-vote check. re-verify before treating weights as gospel.

> Sources: Igor Naming Guide 2022 · `lexiconbranding.com` · `uspto.gov/trademarks/basics/strong-trademarks` · Lenny's Newsletter (Placek) · Stanford `yorkston.pdf` (sound symbolism).

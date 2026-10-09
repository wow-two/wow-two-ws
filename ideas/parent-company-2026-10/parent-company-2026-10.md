# Form one US LLC after three written answers

*Last updated: 2026-10-09 05:14 AM*

*Research date 2026-10-08/09; synthesis of the seven notes in `notes/`. This is research, not legal or tax advice. Unmarked citations are primary sources: statute, regulator, treaty, or a platform's own terms and help pages. (S) marks a secondary source, (A) an anecdotal forum report, and (U) an unverified item or my own inference or arithmetic. USD 1 = UZS 11,809 (CBU rate, 8 Oct 2026).*

Form one single-member US LLC under a neutral legal name, run ForeverPin and every later product inside it as brands with separate Stripe accounts, and move a product into a sister LLC only when a partner, a sale, a risk spike or a distinct App Store seller name demands it. A US company is the only structure Stripe names for founders who live in countries it does not serve, and Uzbekistan is one; Delaware through Stripe Atlas costs about $500 a year and owes no US income tax while nobody works for the business in the US, but its yearly Form 5472 carries a $25,000 penalty if missed. Three written answers gate formation: Stripe's consent to a Tashkent-resident owner; one fintech willing to receive payouts, since Mercury, Revolut, Bluevine and Novo exclude him by rule and Stripe Treasury wants a physical US address for the account representative; and an Uzbek accountant's reading of the offshore list that names Delaware, which decides between Delaware and New Mexico. Uzbekistan, not the US, sets the tax bill: on the Tax Code's most natural reading the LLC is the founder's controlled foreign company, a company run alone from Tashkent risks Uzbek tax residence at 15%, and invoicing the LLC from his own individual-entrepreneur business at 1% of turnover is the cheapest documented route home. EU, UK and Uzbek consumer sales require VAT registration from the first sale, and developers report that Apple shows foreign-owned LLCs only a W-9, which blocks Pose Coach payouts until Apple accepts a W-8.

---

## One neutral LLC, gated by three written answers

| Decision | Pick | Switch when |
|---|---|---|
| Entity | One single-member US LLC with a neutral legal name; each product is a brand inside it | A split trigger fires (see the structure section) |
| State | Delaware, formed through Stripe Atlas as an LLC; Atlas lists the C corporation first | The Uzbek accountant confirms Delaware's offshore listing applies and Stripe confirms a non-Atlas LLC: New Mexico |
| Stripe | One Stripe account per product, all on the LLC's EIN | n/a |
| Payout account | Stripe Treasury if the Dashboard offers it; otherwise the first of Slash, Airwallex or Relay to confirm in writing | Every provider refuses: UAE free-zone company with a residence visa |
| Route home | The founder's individual-entrepreneur (IE) business, taxed at 1% of turnover, invoices the LLC | IE ceiling (UZS 1bn, about $85k a year): IT Park LLC; or plain yearly distributions taxed at 5% |
| Indirect tax | Stripe Tax Basic with threshold monitoring; EU non-Union OSS and UK VAT registered before the first consumer sale there | Block consumer sales in a first-sale market instead |
| App stores | The LLC enrolls with Apple ($99 a year) and Google Play ($25 once) on one D-U-N-S number | Apple keeps forcing a W-9: individual enrollment or a separate app entity, chosen with a CPA |

Before formation, in writing:

1. Stripe will activate live payments for a US LLC whose sole owner and representative live in Tashkent, and names the business address to enter.
2. One fintech (Slash, Airwallex or Relay) accepts that owner and lists the proof of operations it needs.
3. The Uzbek accountant says whether the Tax Code's offshore list names Delaware; the answer picks the state.

Before money moves or apps launch:

4. The Uzbek accountant rules on place-of-effective-management (POEM) residence, the LLC's classification, and IE invoicing versus distributions.
5. Apple accepts a W-8BEN for a foreign-owned single-member LLC; this gates Pose Coach, not ForeverPin.

- Mid-case yearly cost at $5K MRR (U, arithmetic on unit prices cited below): Delaware $500 + Form 5472 prep ~$200 + Apple $99 + four wires $100 + IE tax ~$540 ≈ $1,440, or 2.4% of revenue.
- That excludes adviser fees, Stripe processing, Stripe Tax's 0.5% on registered volume, and VAT collected from customers.

---

## Stripe names one route for a Tashkent founder: a US company

- Uzbekistan is missing from Stripe's supported countries; the US, UK, UAE, Estonia, Lithuania, Ireland, Singapore and Hong Kong are listed ([Stripe global](https://stripe.com/global)).
- Stripe requires everyone tied to an Estonian e-Residency account to live in a supported country, and points others to Stripe Atlas, a US company ([Stripe support](https://support.stripe.com/questions/supporting-companies-that-registered-in-estonia-through-e-residency)).
- No other Stripe page states that residence rule, so its reach to UK or UAE accounts is unknown (U).
- Stripe's sanctions list names Cuba, Iran, North Korea, Syria, Crimea, Donetsk and Luhansk, not Uzbekistan ([Stripe restricted businesses](https://stripe.com/legal/restricted-businesses)).

| Option | Stripe, Tashkent owner | Bank, Tashkent owner | Fixed cost a year | Verdict |
|---|---|---|---|---|
| US LLC | Stripe's named route | Discretionary fintechs | About $500 (DE) or $125–250 (NM), before filing prep | Pick |
| UAE free zone | Passport-only for non-resident owners ([Stripe UAE](https://support.stripe.com/questions/uae-ownership-verification-requirements)); residence rule unconfirmed | Needs a UAE-resident signatory, so a visa ([Wio](https://www.wio.io/support/)) | About $1.5–1.9k; $3.3–3.9k with a visa (S) ([Avyanco](https://avyanco.com/rakez-free-zone-cost/)) | Fallback |
| Estonia OÜ | Blocked by the residence rule | Board member in person | €100–400 address and contact person, plus accounting ([e-Residency](https://www.e-resident.gov.ee/start-a-company/)) | No |
| UK Ltd | Unconfirmed | Unverified | £50 filing ([GOV.UK](https://www.gov.uk/government/news/companies-house-fees-are-changing-from-1-february-2026)) plus £600–3,000 accounts (S) ([Sleek](https://sleek.com/uk/resources/cost-of-running-a-limited-company/)) | No |
| Lithuania, Ireland, Singapore, Hong Kong | Unconfirmed | Unverified | Local director, bond, secretary or audit ([ACRA](https://acra.gov.sg/how-to-guides/setting-up-a-local-company/appointing-directors-company-secretary-and-other-key-personnel), [HK Companies Registry](https://www.cr.gov.hk/en/faq/faq05_b.htm)) | No |

- UAE tax: 0% to AED 375,000 of income and 9% above; Small Business Relief keeps 0% while revenue stays at or under AED 3M, now through 2029 ([FTA guide](https://tax.gov.ae/Datafolder/Files/Guides/CT/Free%20Zone%20Persons%20-%2020%2005%202024%20final%20for%20GCD.pdf), [Khaleej Times](https://www.khaleejtimes.com/business/uae-extends-corporate-tax-relief-for-small-businesses-until-2029) (S)).
- Estonia: the e-Residency card is collected in person, nearest at Astana, Baku, Tbilisi, Ankara or Abu Dhabi, and VAT numbers need an economic connection to Estonia since August 2025 ([pick-up points](https://www.e-resident.gov.ee/pick-up-locations/), [e-Residency](https://www.e-resident.gov.ee/blog/posts/9-things-you-should-know-about-running-an-estonian-company/)).
- UK: 19–25% corporation tax; since the 2018 protocol a company resident in both countries gets no treaty benefits unless the two tax authorities agree ([GOV.UK](https://www.gov.uk/corporation-tax-rates), [treaty protocol](https://treaties.fcdo.gov.uk/data/Library2/pdf/2018-TS0006.pdf)).
- Uzbekistan's offshore list omits the UAE, UK, Estonia and Singapore and includes Hong Kong and Cyprus ([lex.uz Annex 1](https://lex.uz/ru/docs/2186012)).
- Uzbek CFC and POEM rules reach any company run from Tashkent, so Estonia's 0% on retained profit and the UAE's 0% band buy little (U).
- On total burden, a US LLC plus Uzbekistan's 5% dividend tax beats UK 19–25% plus the same 5% (U).

---

## Delaware's place on Uzbekistan's offshore list reopens the state choice

- Annex 1 of Uzbekistan's FX-monitoring regulation lists 68 offshore jurisdictions, including the State of Delaware (No. 120) and the State of Wyoming (No. 112) ([lex.uz Annex 1](https://lex.uz/ru/docs/2186012), [Dec 2025 amendment](https://lex.uz/docs/7889232)).
- New Mexico, Nevada and the US as a country are absent; the list was read through a summarising tool (U).
- If the Tax Code's offshore concept uses that list, which is likely but unconfirmed (U):
  - the CFC "active company" exemption is denied ([Tax Code Art. 204(2), prg.kz mirror](https://prg.kz/m/amp/document/30421027/17/1700000));
  - every deal with a counterparty registered there is a controlled transaction, with no threshold ([Art. 181](https://prg.kz/m/amp/document/30421027/14/1400000));
  - banks give its transfers enhanced oversight (S) ([Mondaq](https://webiis08.mondaq.com/financial-services/1073166/the-list-of-offshore-zones-has-been-updated-in-uzbekistan)).
- The listing costs little if all profit leaves the LLC each year; it bites when profit stays above UZS 300M or when an IE invoices the LLC (U).

| | Delaware via Atlas | New Mexico, self-formed |
|---|---|---|
| Setup | $500 covering the state fee, EIN filing and first-year agent ([Atlas](https://stripe.com/atlas)) | $50 filing plus an agent at about $100–250 (S) ([GlobalSolo](https://www.globalsolo.global/data/formation-costs)) |
| Each year | $400 tax due 1 June plus $100 agent ([Delaware](https://corp.delaware.gov/alt-entitytaxinstructions/)) | $0 state fee (U: possibly $20 every three years) plus the agent |
| Stripe | Atlas opens the account; US card payments start before the EIN ([Atlas docs](https://docs.stripe.com/atlas/signup)) | Direct US account; no Stripe text covers this owner without Atlas |
| Banking | Treasury check in the Atlas Dashboard; Atlas partner Mercury excludes Uzbekistan | Same fintech pool; Slash's checklist names a Delaware good-standing certificate ([Slash](https://www.slash.com/help-center/getting-started/signing-up-for-slash-what-you-ll-need-to-get-started)), and other states' certificates are unconfirmed (U) |
| EIN | Atlas files; 10–30 business days without an SSN | Form SS-4 by fax, about four business days ([IRS](https://www.irs.gov/instructions/iss4)) |
| Uzbek offshore list | Listed | Not listed |

- **Rule: Delaware via Atlas, unless the accountant confirms the listing applies and Stripe confirms in writing that a non-Atlas LLC with this owner can activate; then New Mexico.**
- Wyoming is out: it is listed (No. 112), and the 2026 Apple decline reports involve Wyoming LLCs (A) ([Apple forum](https://developer.apple.com/forums/thread/821586)).
- Delaware's tax is not prorated: a 2026 formation owes $400 on 1 June 2027, and a January 2027 formation moves the first bill to 2028 ([Atlas company types](https://docs.stripe.com/atlas/company-types)).

---

## One LLC holds every product until one of six triggers fires

| | One LLC, products as brands | Holding LLC plus per-product LLCs | Series LLC |
|---|---|---|---|
| Fixed cost at 25 products, mid case (U) | About $725 a year (DE) | About $8k–18k a year | About $725, plus $100 per Delaware registered series |
| Bank, D-U-N-S, Apple tax screen | Once | Once per LLC | Master LLC only |
| Stripe | Many accounts on one EIN | Separate accounts per LLC | Master LLC; series status undocumented |
| Creditor isolation | None | Strong if each LLC runs separately | Statutory; untested outside series states |
| Platform isolation | None | Partial; linked through the owner | None |
| Partner on one product | Awkward | Clean | Untested |

- Each extra LLC repeats the scarce approvals: a bank for a Tashkent owner, a D-U-N-S, Apple's tax screen (U).
- Each also files its own Form 5472 with its own $25,000 exposure; the IRS offers no group filing for disregarded entities ([IRS Form 5472 instructions](https://www.irs.gov/instructions/i5472)).
- A holding layer adds an entity and no tax consolidation for a foreign owner, so a split product's LLC belongs to the founder directly (U).
- Series LLCs: the IRS rule treating each series as its own entity has been proposed since 2010 and never finalised (S) ([Wikipedia](https://en.wikipedia.org/wiki/Series_LLC)), and Stripe ties each account to "the tax ID and legal entity of one business" ([Stripe](https://docs.stripe.com/get-started/account/multiple-accounts)).
- Apple shows the organization's legal name as seller on every app and accepts no DBA ([Apple](https://developer.apple.com/programs/enroll/)), so an LLC named after ForeverPin would sell Pose Coach under that name.
- Brands need no state DBA filing: Delaware makes it optional for LLCs, New Mexico has no general DBA filing (S), and Stripe, Apple and Google ask for none ([Delaware Division of Revenue](https://revenue.delaware.gov/trade-names-faqs/), [Ezel](https://ezel.ai/surveys/assumed-name-registration-requirements/new-mexico)).
- Keep every product separable from day one: its own Stripe account, domain, repository, support address and store listing.

Split a product into a sister LLC when:

1. A partner joins it. Two members make an LLC a partnership: Form 1065 and K-1s by 15 March, $255 per partner per month if late ([IRS Form 1065 instructions](https://www.irs.gov/pub/irs-pdf/i1065.pdf)).
2. A buyer wants the entity rather than assets. Most Acquire.com deals are asset purchases (S) ([FounderPath](https://founderpath.com/blog/saas-acquisitions-lessons-from-500m-in-closed-deals)), so separable accounts usually suffice.
3. Its risk diverges. ForeverPin's redirect abuse makes it the first candidate; a split shields the other products from its creditors, not from Stripe or Google linkage.
4. It needs its own App Store seller name.
5. Apple's tax screen forces corporate status for apps; isolate the apps rather than electing 21% federal tax for the whole LLC (U).
6. It earns about $270–600 MRR, enough that a $325–725 yearly fixed cost stays at or under 10% (U, arithmetic).

---

## Separate Stripe accounts split operations, not liability

Setup:

- Stripe wants separate accounts for independently run projects; one legal entity may reuse its tax ID across them, each with its own public name, website, descriptor and payout account ([Stripe](https://docs.stripe.com/get-started/account/multiple-accounts)).
- Describe only its own product in each account: processing for an undisclosed product, or changing the business model without consent, breaches the terms ([restricted businesses](https://stripe.com/legal/restricted-businesses), [Stripe service terms](https://stripe.com/legal/ssa-service-terms)).
- Statement descriptors run 5–22 Latin characters and must reflect the brand; subscriptions can set one per Product ([Stripe descriptors](https://docs.stripe.com/get-started/account/statement-descriptors)).
- Organizations are optional: up to 75 accounts, whose holders must be affiliates and are jointly and severally liable for Organizations activity ([Stripe](https://docs.stripe.com/get-started/account/orgs/build), [service terms](https://stripe.com/legal/ssa-service-terms)).
- The Atlas terms in force from 28 Sep 2026 make each founder jointly and severally liable with the company for Atlas use ([service terms](https://stripe.com/legal/ssa-service-terms)).

Linkage:

- Stripe's "User Group" covers the user plus anyone Stripe "reasonably determines is associated" with it ([Stripe Services Agreement](https://stripe.com/legal/ssa)).
- Reserves, payout holds and setoff can reach any User Entity's balance and bank account (General Terms 7.2(c), Payments Terms 5.3–5.5) ([agreement](https://stripe.com/legal/ssa), [service terms](https://stripe.com/legal/ssa-service-terms)).
- An unacceptable-risk finding typically pauses payouts for 120 days ([Stripe policy](https://stripe.com/legal/unacceptable-risk-policy)).
- Terminated-merchant files keep the business's and the principal owner's name, address and tax ID for five years, and most processors reject listed owners automatically ([Stripe](https://docs.stripe.com/disputes/match)).
- Ending one agreement does not end the others (General Terms 10.2), and no report of a sibling-account closure was found ([agreement](https://stripe.com/legal/ssa)).
- A separate LLC per product therefore does not shield the founder, whose own details travel with any listing (U).

Product screen against Stripe's list of 22 Sep 2026 (U):

- ForeverPin: QR and redirect services are unlisted; the risks are phishing redirects, file hosting near the cyberlocker restriction, and unclear trial pricing.
- Transcript Forge: transcription is unlisted; fetching third-party video invites the copyright-facilitation clause.
- Hijinx: selling its own packs is allowed; prize-linked play, adult content and third-party sellers are not.
- ForeverPin containment: separate domains, registrar and hosting accounts plus screening of link destinations, since blocklists act per domain (S) ([statichost.eu](https://sh.statichost.eu/blog/google-safe-browsing), [SecurityWeek](https://www.securityweek.com/google-temporarily-flags-bitly-links-malicious/)).

Address:

- Stripe asks for the physical address where most business activity happens and refuses PO boxes ([Stripe](https://support.stripe.com/questions/requirements-for-having-a-us-stripe-account)).
- Atlas says a physical or virtual US address works for payments ([Stripe](https://support.stripe.com/questions/which-address-should-i-use-for-atlas-incorporation)).
- Card networks make the final call on a merchant's location, and acquiring outside network rules is prohibited ([service terms](https://stripe.com/legal/ssa-service-terms), [restricted businesses](https://stripe.com/legal/restricted-businesses)).
- Enter only addresses the founder can document, and settle the Tashkent-versus-US question with Stripe in writing before activation (U).

---

## Payouts hinge on one discretionary fintech

- A standard US Stripe account pays USD only to a US account in the LLC's own name or into a Stripe financial account; Uzbek bank accounts are open only to "cross-border payouts" accounts ([Stripe payouts](https://docs.stripe.com/payouts), [agreement 7.4](https://stripe.com/legal/ssa)).

| Provider | Tashkent-resident owner | Deciding rule |
|---|---|---|
| Mercury | No | Residence-based prohibited list includes Uzbekistan, updated 7 Oct 2026; its cards decline at Uzbek merchants ([list](https://support.mercury.com/hc/en-us/articles/28771710754580-Prohibited-countries), [cards](https://support.mercury.com/hc/en-us/articles/28778487704084-Countries-where-Mercury-cards-are-restricted)) |
| Wise Business | Very likely no | Uzbekistan is not a balance country, and Wise USD details cannot receive SWIFT from Uzbekistan ([Wise](https://wise.com/help/articles/2813542/where-do-i-need-to-live-to-hold-money-with-wise), [SWIFT](https://wise.com/help/articles/3MObHiWysjT2DzDNHTupa4/what-countries-can-i-receive-international-swift-payments-from)) |
| Revolut, Bluevine, Novo | No | Residence lists omit Uzbekistan; Novo serves US residents only ([Revolut](https://help.revolut.com/business/help/setting-up-an-account/is-my-business-eligible/what-country-of-residence-is-eligible-to-open-a-revolut-business-account/), [Bluevine](https://bluevine.com/us-business-banking-for-international-owners), [Novo](https://www.novo.co/help/can-businesses-or-owners-outside-the-us-apply-for-an-account)) |
| Brex | Impractical | US presence plus $50k cash or $500k revenue ([Brex](https://www.brex.com/support/brex-account-requirements)) |
| Stripe Treasury | Unlikely; sources conflict | Physical US address for business and representative ([Stripe](https://support.stripe.com/questions/physical-presence-requirement-faq)) |
| Slash | Open (U) | OFAC-only exclusions; accepts applicants abroad; wants two statements from another institution plus proof of activity ([Slash](https://www.slash.com/help-center/getting-started/signing-up-for-slash-what-you-ll-need-to-get-started)) |
| Airwallex US | Weak (U) | Agreement requires a US principal place of business ([Airwallex](https://www.airwallex.com/us/terms/airwallex-service-agreement)) |
| Relay | Open (U) | Uzbekistan not prohibited; SSN, phone and address wording conflicts; international wires business-to-business only ([Relay](https://relayfi.com/hc/en-us/articles/10239600121748-Prohibited-Countries/), [wires](https://relayfi.com/hc/en-us/articles/30873687634068-Non-Permitted-Activity-for-International-Wires/)) |
| Payoneer | Unverified | No statement on Uzbekistan ([Payoneer](https://www.payoneer.com/payments/uzbekistan/)) |

- Every open provider asks for proof of operations, and Relay and Airwallex for a US presence; first revenue from US customers through Stripe is the natural evidence (U).
- Never claim a US principal place of business that cannot be supported; Mercury lists an "unsupportable geography" among its closure reasons ([Mercury](https://support.mercury.com/hc/en-us/articles/43095394066452-Understanding-account-closures-and-access-restrictions)).
- Apply first wherever the written answer was yes; absent answers, start with Slash, which states it accepts applicants abroad.
- If every provider refuses, the UAE free-zone company is the structural fallback.
- The first payout typically lands 7–14 days after the first live payment ([Stripe payouts](https://docs.stripe.com/payouts)).

### SWIFT carries money home for $15–25 a wire

- Uzbek law lets resident individuals receive foreign currency without restriction and treats payments for services and investment income as free current operations, though banks may demand supporting documents ([Currency Law](https://lex.uz/ru/docs/4562846)).
- Route A, a distribution to a personal USD account: Relay cannot wire business-to-person, and Stripe Global Payouts pays Uzbek individuals in UZS but needs Treasury ([Relay](https://relayfi.com/hc/en-us/articles/30873687634068-Non-Permitted-Activity-for-International-Wires/), [Stripe](https://docs.stripe.com/global-payouts/recipient-requirements)).
- Route B, an IE invoice: the contract goes into the E-kontrakt system and payment must settle through the IE's Uzbek bank account ([Resolution 283](https://lex.uz/ru/docs/4812424)).
- Export proceeds unpaid after 180 days become capital movement, with fines of 5%, then 10%, then 35% as the delay grows ([Currency Law](https://lex.uz/ru/docs/4562846)).
- Outbound wires cost $25 at Slash or Relay and $15–25 at Airwallex; intermediary banks may deduct more ([Slash](https://www.slash.com/pricing), [Relay](https://relayfi.com/pricing/), [Airwallex](https://www.airwallex.com/us/pricing)).
- Inbound, Trustbank credits incoming funds free for companies and IEs, Asia Alliance Bank charges nothing on export proceeds, and Kapitalbank charges 0.5% to withdraw SWIFT-received cash ([Trustbank](https://trustbank.uz/upload/medialibrary/46e/y1u7amycg15xx945xcrwdymokdteto3x/70.Tarif-_-English-_-s-07.11.2025g.-v-e.pdf), [AAB](https://www.aab.uz/en/press_center/question_answer/2992/), [Kapitalbank](https://www.kapital24.uz/upload/medialibrary/109/nffw993eh73nvcqc300n1hj7j59i04c2/Service-Fees-for-Individual-Clients.pdf)).
- Batch transfers: a flat $25 is 2.5% of $1,000 and 0.5% of $5,000 (U, arithmetic).
- If Treasury opens, Global Payouts costs about $35–49 per $1,000 and $75–139 per $5,000, and Uzbekistan's cross-border fee is unpublished (U, arithmetic) ([Stripe pricing](https://docs.stripe.com/global-payouts/pricing)).
- Funding the LLC from Uzbekistan: individuals may invest up to $10,000 a year abroad without a government decision, registered in the FERUz system from mid-September 2026, and US companies are carved out of the cap (S) ([spot.uz](https://www.spot.uz/ru/2026/06/15/investment-outbound/), [Fergana](https://en.fergana.agency/news/144083/)).

---

## US duties cost $600–2,000 a year around one $25,000 filing

| Duty | When | Cost | If missed |
|---|---|---|---|
| Form 5472 with a pro forma Form 1120, fax or mail only | 15 April (Form 7004 extends to 15 October); first for 2026 due 15 April 2027 | $99–1,500 preparation (S) | $25,000, plus $25,000 per 30 days starting 90 days after IRS notice |
| Delaware LLC tax | 1 June; first on 1 June 2027 | $400 | $200 plus 1.5% a month |
| Registered agent | Yearly | $100 (Atlas, from year two) | n/a |
| FinCEN beneficial-ownership report | Not required for US-formed companies | $0 | n/a |
| Federal income tax | Only with a US trade or business | $0 expected | Form 1040-NR due 15 June |

Sources: [IRS Form 5472 instructions](https://www.irs.gov/instructions/i5472), [Delaware](https://corp.delaware.gov/alt-entitytaxinstructions/), [Stripe Atlas](https://stripe.com/atlas), [FinCEN](https://www.fincen.gov/news/news-releases/fincen-permanently-ends-beneficial-ownership-reporting-requirements-millions), [SDO CPA](https://www.sdocpa.com/form-5472-foreign-owned-business-filing/) (S), [IRS Pub 519](https://www.irs.gov/pub/irs-pdf/p519.pdf).

- Form 5472 reports contributions, distributions, loans and payments to the owner; an owner without a US tax number uses a self-assigned reference ID ([IRS](https://www.irs.gov/instructions/i5472)).
- Failing to keep the records Form 5472 needs carries the same $25,000 penalty, so LLC money and personal money stay apart ([IRS](https://www.irs.gov/instructions/i5472)).
- Paying the Atlas fee personally is plausibly a formation contribution, so the first 5472 is likely due even without revenue (U).
- No US income tax is expected because services income is sourced where performed and cloud transactions count as services ([IRS Pub 519](https://www.irs.gov/pub/irs-pdf/p519.pdf), [EY](https://taxnews.ey.com/news/2025-0280-united-states-treasury-releases-guidance-package-on-classifying-and-sourcing-digital-content-and-cloud-transactions) (S)).
- That holds only without a US office, employee or contract-concluding agent ([26 CFR 1.864-7](https://www.law.cornell.edu/cfr/text/26/1.864-7)); hosting outside the US is the conservative choice (U).
- EIN: foreign applicants cannot apply online; fax takes about four business days, or call 267-941-1099; no ITIN is needed ([IRS](https://www.irs.gov/instructions/iss4)).
- A C corporation pays 21% federal tax, and dividends to an Uzbek owner bear 30% withholding, about 44.7% combined; it fits only venture money, equity grants or a real US presence ([26 USC 11](https://www.law.cornell.edu/uscode/text/26/11), [IRS Table 1](https://www.irs.gov/pub/irs-lbi/tax-treaty-table-1.pdf)).

---

## Uzbekistan's CFC and residence rules set the real tax bill

*Tax Code articles were read through a paraphrasing tool on a prg.kz mirror current to 19 Jul 2026; wording needs confirming on [lex.uz](https://lex.uz/ru/docs/4674902) (U).*

- The founder is resident after 183 days and taxed on worldwide income: 12% in general, and 5% on dividends and interest, with no source limit in the text read ([Art. 381](https://prg.kz/m/amp/document/30421027/29/2900000)).
- A foreign company more than 25% controlled by a resident is a CFC ([Arts. 39–40](https://prg.kz/m/amp/document/30421027/4/330000)).
- CFC profit left undistributed above UZS 300M (about $25.4k) a year joins the owner's income at 12%; dividends paid the following year reduce it ([Arts. 203–208](https://prg.kz/m/amp/document/30421027/17/1700000)).
- The UZS 300M figure reads as a cliff, not an allowance (U).
- The relevant exemptions need an "active" company (passive income at or under 20%, denied for offshore-listed locations) or a 15%-plus effective rate in a treaty state ([Arts. 204–206](https://prg.kz/m/amp/document/30421027/17/1700000)).
- A US LLC can therefore be exempt only as active, and only outside Delaware and Wyoming (U).
- SaaS may count as "information-processing services", a passive item under Art. 206 (U).
- Notices: participation within one month of acquiring or changing a foreign holding, a CFC notice by 20 March in years CFC profit counts, and a 20% fine (minimum UZS 10M) on omitted CFC profit ([Art. 209](https://prg.kz/m/amp/document/30421027/17/1700000), [Art. 227](https://prg.kz/m/amp/document/30421027/18/1800000)).
- The annual declaration is due 1 April and the tax 1 June, payable from a foreign account ([Arts. 397–398](https://prg.kz/m/amp/document/30421027/30/3000000)).
- POEM: a foreign company run regularly from Uzbekistan is Uzbek-resident and pays 15% on worldwide profit; the carve-out needs staff and assets abroad plus a treaty, which a solo US LLC lacks ([Arts. 33–34](https://prg.kz/m/amp/document/30421027/3/240000)).
- No foreign jurisdiction removes POEM risk; keeping the LLC's profit small shrinks it (U).
- Foreign tax is creditable only under a treaty ([Art. 342](https://prg.kz/m/amp/document/30421027/26/2600000)).
- No individual duty to report foreign bank accounts was found; the foreign-holding notice is the duty that applies ([Art. 22](https://prg.kz/m/amp/document/30421027/2/120000), [Currency Law](https://lex.uz/ru/docs/4562846)).
- Uzbekistan signed the OECD tax-assistance convention on 15 Jul 2026; ratification and data-exchange timing are unknown (S) ([RegFollower](https://regfollower.com/uzbekistan-signs-multilateral-convention-to-tackle-tax-evasion-and-avoidance/)).

| Route home at $60k revenue, about $54k profit (U) | Uzbek tax | Filings | Main risk |
|---|---|---|---|
| A. Yearly distributions | 5%, about $2.7k; 12%, about $6.5k, if profit stays above the cliff | Notices and declaration | Payouts taxed as 12% income; POEM residence |
| B. IE at 1% of turnover invoices the LLC | About $540 | Monthly IE returns, E-kontrakt, controlled-deal notice if Delaware | UZS 1bn ceiling; related-party pricing; repatriation clock |
| C. IT Park LLC services the LLC | About 1% levy ($540) plus 5% on dividends ($2.6k) | Audit report, quarterly reports | Membership revocation; export test from 2028 |

- IE: 1% turnover tax on revenue up to UZS 1bn from 1 Jan 2026, monthly returns by the 15th and an annual return by 15 February ([Arts. 461–470](https://prg.kz/m/amp/document/30421027/34/3400000)).
- IEs cannot become IT Park residents ([IT Park](https://www.it-park.uz/en/itpark/news/11-frequently-asked-questions-and-answers-when-applying-for-it-park-resident-status)).
- IT Park takes Uzbek LLCs only and gives 0% profit tax, social tax and VAT to 1 Jan 2028, then to 2040 without VAT relief if exports exceed 50% of income ([IT Park](https://www.it-park.uz/en/itpark/news/tax-incentives-for-startups-and-foreign-investors-in-uzbekistan-s-it-sector), [EY](https://www.ey.com/en_uz/technical/tax-alerts/2024/10/ey-uz-decree-on-additional-incentives-to-support-it-park-residents)).
- The IT Park levy is about 1% of income up to UZS 5bn (S) ([buxgalter.uz](https://buxgalter.uz/publish/doc/text212804_kto_lishaetsya_lgot_spisok_krupnyh_nalogoplatelshchikov_i_drugie_izmeneniya_po_pp-388)).
- IT Park revoked 152 memberships in July 2026 for missing audit reports, after 616 earlier in the year ([outsource.gov.uz](https://www.outsource.gov.uz/media/in-july-152-companies-lost-their-it-park-uzbekistan-resident-status)).
- Whether fees from the founder's own foreign LLC count as export is unanswered (U).

---

## VAT starts at the first EU, UK or Uzbek consumer sale

- First-sale regimes for consumer digital services include the EU, UK, Uzbekistan, Kazakhstan and Russia ([EC OSS guide](https://vat-one-stop-shop.ec.europa.eu/document/download/a316a98a-3b2b-4991-a9c0-3b5905d369fc_en?filename=OSS_guidelines_en.pdf), [GOV.UK](https://www.gov.uk/register-for-vat), [Stripe Tax: Uzbekistan](https://docs.stripe.com/tax/supported-countries/asia-pacific/collect-tax.md?tax-jurisdiction-asia-pacific=uzbekistan), [Kazakhstan](https://docs.stripe.com/tax/supported-countries/asia-pacific/collect-tax.md?tax-jurisdiction-asia-pacific=kazakhstan), [Russia](https://docs.stripe.com/tax/supported-countries/europe/collect-tax.md?tax-jurisdiction-europe=russia)).
- Secondary guides add South Korea, India, Turkey, Saudi Arabia, the UAE, Mexico, Chile and Colombia (S) ([Forvis Mazars](https://www.forvismazars.com/kr/en/insights/blog/korea-business-guide/korean-vat-for-foreign-ai-and-saas-businesses), [Anrok](https://www.anrok.com/vat-software-digital-services/united-arab-emirates)).
- Threshold regimes: Norway NOK 50k, Canada CAD 30k, New Zealand NZ$60k, Switzerland CHF 100k with a Swiss representative, Japan JPY 10M, and Australia AUD 75k (Australia via search summary, U) ([Skatteetaten](https://www.skatteetaten.no/en/business-and-organisation/vat-and-duties/vat/foreign/e-commerce-voec/register), [CRA](https://www.canada.ca/en/revenue-agency/services/tax/businesses/topics/gst-hst-businesses/digital-economy-gsthst/find-out-need-register/cross-border-threshold-amounts.html), [IRD](https://www.ird.govt.nz/gst/gst-for-overseas-businesses/supplying-remote-services-into-new-zealand), [ESTV](https://www.estv.admin.ch/en/vat-liability-foreign-companies), [NTA](https://www.nta.go.jp/english/taxes/consumption_tax/PFQA_en_foreign.pdf), [ATO](https://www.ato.gov.au/businesses-and-organisations/international-tax-for-business/gst-for-non-resident-businesses/gst-on-imported-services-and-digital-products)).
- EU: non-EU sellers get no €10,000 allowance; the non-Union OSS works through any member state, with quarterly returns due by the end of the next month, mandatory nil returns and 10-year records ([EC guide](https://vat-one-stop-shop.ec.europa.eu/document/download/a316a98a-3b2b-4991-a9c0-3b5905d369fc_en?filename=OSS_guidelines_en.pdf), [EC](https://vat-one-stop-shop.ec.europa.eu/one-stop-shop/declare-and-pay-oss_en)).
- EU timing trap: registration starts the next quarter unless the member state hears by the 10th of the month after the first sale, and Stripe's registration service cannot backdate ([EC](https://vat-one-stop-shop.ec.europa.eu/one-stop-shop/register-oss_en), [Stripe](https://docs.stripe.com/tax/use-stripe-to-register/outside-united-states.md)).
- EU evidence: two non-contradictory location items; Stripe relies on one address but stores the rest, so capture billing address, card country and IP ([EC notes](https://vat-one-stop-shop.ec.europa.eu/document/download/78103105-cf0c-4949-9162-daab6f5d11d4_en?filename=explanatory_notes_2015_en_0.pdf), [Stripe](https://docs.stripe.com/tax/supported-countries/european-union.md)).
- UK: registration is due from the first UK consumer sale of any value ([GOV.UK](https://www.gov.uk/register-for-vat)).
- EU and UK business buyers with valid VAT numbers are reverse-charged; Stripe applies this on number format alone ([HMRC](https://www.gov.uk/hmrc-internal-manuals/vat-registration-manual/vatreg37200), [Stripe](https://docs.stripe.com/billing/customer/tax-ids.md)).
- US sales tax starts only at a state's economic-nexus test, mostly $100k; about 15 jurisdictions also count 200 transactions, which about 17 monthly subscribers could cross if each charge counts (S, U) ([Kintsugi](https://trykintsugi.com/sales-tax-guides/usa/economic-nexus.md)).
- SaaS is taxable in 21 US jurisdictions (S) ([Anrok](https://www.anrok.com/saas-sales-tax-by-state)).
- Stripe Tax Basic charges 0.5% of volume only where registered and returns zero tax where no registration exists ([Stripe pricing](https://stripe.com/tax/pricing), [Stripe](https://docs.stripe.com/tax/customer-locations.md)).
- Tax Complete starts at $90 a month and adds registration and filing; Stripe-run EU OSS comes to roughly $1,800 a year (U, estimate), while self-filing with Irish Revenue costs only time ([Stripe support](https://support.stripe.com/questions/understanding-stripe-tax-pricing)).
- The seller stays liable; Stripe neither remits nor debits for filings ([Stripe](https://docs.stripe.com/tax/file-with-stripe-outside-us.md)).
- Stripe Tax does not support Uzbekistan as a business location ([Stripe](https://docs.stripe.com/tax/supported-countries.md)).
- Apple collects in about 95 regions, including Uzbekistan whenever the developer is non-resident there ([Apple Exhibit B](https://developer.apple.com/support/downloads/terms/exhibits/Exhibits-to-Schedule-2-and-3-English.pdf)).
- A US LLC enrolled with a US address should count as non-resident in Uzbekistan, keeping Pose Coach's Uzbek VAT with Apple (U).
- Apple leaves Brazil, Argentina, Israel, Pakistan and other unlisted regions to the developer, and Google makes the developer liable by default outside listed countries ([Apple](https://developer.apple.com/support/downloads/terms/exhibits/Exhibits-to-Schedule-2-and-3-English.pdf), [Google](https://play.google/developer-distribution-agreement.html)).

---

## App stores accept the LLC on paper but stall on its tax form

- Apple organization enrollment needs a legal entity (no DBAs), a D-U-N-S under the exact legal name, a website and email on the organization's domain, and $99 a year; it sets no nationality or residence rule ([Apple](https://developer.apple.com/programs/enroll/), [Apple FAQ](https://developer.apple.com/support/enrollment/)).
- D-U-N-S numbers are free; Apple quotes up to 5 business days at D&B and Google up to 30 days, and one record under the LLC's name serves both stores (U) ([Apple](https://developer.apple.com/help/account/membership/D-U-N-S), [Google](https://support.google.com/googleplay/android-developer/answer/13628312)).
- App Store Connect shows foreign-owned single-member LLCs only a W-9, and more than ten developers report unresolved Apple Finance cases from May to September 2026 (A) ([Apple forum](https://developer.apple.com/forums/thread/826739)).
- The IRS says a foreign person may not give a W-9 and that a disregarded entity's form comes from its owner ([IRS](https://www.irs.gov/pub/irs-pdf/iw9.pdf)).
- Apple processes banking only after tax forms, so the defect blocks payouts ([Apple](https://developer.apple.com/help/app-store-connect/manage-banking-information/enter-banking-information/)).
- New solo foreign-owned Wyoming LLCs report unexplained declines in April and August 2026 (A) ([Apple forum](https://developer.apple.com/forums/thread/821586)).
- Fallbacks, chosen with a CPA: escalate citing the IRS instructions; enroll as an individual (W-8BEN, personal name as seller, eligibility from Uzbekistan unverified); or set up a separate corporate-classified app entity (U).
- Google Play organization accounts need a D-U-N-S, a one-time $25 and a payments profile matching D&B; the developer name can change any time ([Google](https://support.google.com/googleplay/android-developer/answer/13628312)).
- Google's tax interview does not say how a foreign-owned disregarded LLC answers, and a missing form means 30% or 24% withholding ([Google](https://support.google.com/paymentscenter/answer/10349995)).
- Google terminates related accounts along with a terminated one ([Google](https://support.google.com/googleplay/android-developer/answer/2491922)).
- Apple's 15% rate counts every associated account's proceeds against $1M, so splitting accounts saves nothing ([Apple](https://developer.apple.com/app-store/small-business-program/)).

---

## Eight source conflicts and what each changes

| Topic | One side | Other side | What it changes |
|---|---|---|---|
| US–Uzbekistan treaty | The IRS applies the 1973 US–USSR treaty to Uzbekistan ([IRS](https://www.irs.gov/businesses/international-businesses/uzbekistan-tax-treaty-documents), [Pub 901](https://www.irs.gov/publications/p901)) | PwC's Uzbek treaty list omits the US, and no Uzbek official source was found (S) ([PwC](https://taxsummaries.pwc.com/republic-of-uzbekistan/individual/foreign-tax-relief-and-tax-treaties)) | Nothing for an LLC that pays no US tax. Without Uzbek recognition there is no treaty carve-out from POEM residence and no credit for a C corporation's 30% dividend withholding. The treaty's "representation" test is a US-side backstop only |
| Delaware LLC tax | $400 from tax year 2026 under HB 400, signed 21 May 2026 ([bill](https://legis.delaware.gov/json/BillDetail/GenerateHtmlDocumentEngrossment?engrossmentId=37900&docTypeId=6), [form instructions](https://corpfiles.delaware.gov/LLC_Forms/LLC%20Formation.pdf)) | $300 on Atlas docs and two Division pages ([Atlas](https://docs.stripe.com/atlas/business-taxes), [Delaware](https://corp.delaware.gov/taxfaq/)) | Budget $400; the first bill falls on 1 June 2027 |
| Treasury for a Tashkent owner | Atlas says apply "if eligible" and that Treasury takes non-US physical addresses ([Atlas](https://docs.stripe.com/atlas/payments-business-bank), [Stripe](https://support.stripe.com/questions/which-address-should-i-use-for-atlas-incorporation)) | The physical-presence rule needs US addresses; the 28 Sep 2026 terms require residence in the US territory; no appeals ([Stripe](https://support.stripe.com/questions/physical-presence-requirement-faq), [terms](https://stripe.com/legal/ssa-service-terms), [eligibility](https://support.stripe.com/questions/treasury-eligibility-and-onboarding)) | Plan without Treasury, which also removes Global Payouts; payouts rest on a fintech |
| EIN without an SSN | 10–30 business days ([Atlas](https://docs.stripe.com/atlas/signup)); 15–50 ([Stripe](https://support.stripe.com/questions/how-to-get-a-us-bank-account)); up to five weeks ([Mercury, 2023](https://mercury.com/blog/mercury-stripe-atlas-partnership)) | About four business days by fax ([IRS](https://www.irs.gov/instructions/iss4)) | Atlas card payments can start first; banks need the EIN, so allow 2–10 weeks |
| Stripe identity and address | Non-US representatives give a national ID; a virtual US address works for payments ([Stripe](https://support.stripe.com/questions/2024-updates-to-us-verification-requirements-faq), [Atlas](https://support.stripe.com/questions/which-address-should-i-use-for-atlas-incorporation)) | An SSN for every individual; the address where most activity happens ([Stripe](https://support.stripe.com/questions/signing-up-for-a-us-stripe-account-without-a-tax-id-or-employer-id-number), [Stripe](https://support.stripe.com/questions/requirements-for-having-a-us-stripe-account)) | Ask Stripe which ID and address; the address drives location-mismatch risk |
| Which offshore list the Tax Code uses | Annex 1 of FX regulation 2467 names Delaware and Wyoming ([lex.uz](https://lex.uz/ru/docs/2186012)) | Art. 181 assigns its list to a different set of signatories ([Art. 181](https://prg.kz/m/amp/document/30421027/14/1400000)); the same list is likely but unconfirmed (U) | Decides Delaware versus New Mexico |
| IE turnover ceiling | UZS 1bn, about $85k, in the Tax Code ([Art. 461](https://prg.kz/m/amp/document/30421027/34/3400000)) | 12,000 BRV, about UZS 4.9–5.3bn, under Decree UP-100; unresolved for 1% IEs (S) ([buxgalter.uz](https://buxgalter.uz/question/36464)) | The IE route tops out at about $85k a year until confirmed |
| Mercury for Uzbek founders | 2024 lists and a doola guide present Mercury as an option (S) ([doola](https://www.doola.com/mercury-guide/how-to-open-a-mercury-account-in-uzbekistan/)) | Mercury's official list, updated 7 Oct 2026, prohibits Uzbekistan residents ([Mercury](https://support.mercury.com/hc/en-us/articles/28771710754580-Prohibited-countries)) | Resolved: Mercury is out |

---

## Get these answers in writing before paying anything

| Ask | Questions | What it gates |
|---|---|---|
| Stripe (Atlas support) | Live payments for a US LLC whose sole owner and representative live in Tashkent? Tashkent or US business address, and does Stripe Tax accept it? Which document proves non-US-taxpayer status? Are Treasury and Global Payouts to the owner open to him? | Everything; the $500 Atlas fee is refunded only if Stripe cannot support the business, not if banks refuse ([Atlas](https://docs.stripe.com/atlas/signup)) |
| Slash, Airwallex, Relay | Eligibility of a Tashkent-resident owner without an SSN or US address? Accepted proof of operations? Wires to the owner or his IE? | Payout account |
| Apple Developer Support | Will App Store Connect take a W-8BEN from the foreign owner of a single-member LLC? | Pose Coach payouts |
| Uzbek bank | Documents needed to credit USD from the LLC as a distribution or as an IE invoice | Route home |

### What the US tax professional must confirm

1. No US trade or business for SaaS run from Tashkent, and how app-store revenue is classified and sourced.
2. Form 5472 scope: owner-paid formation and agent fees, payments to the founder's IE, transactions between sister LLCs, and dormant years.
3. Which form the LLC or its owner gives Stripe, Apple and Google (W-8BEN or W-9), and the response to Apple's W-9-only screen.
4. Whether to claim under the 1973 treaty's "representation" article, and whether Form 8833 applies.
5. Delaware versus New Mexico consequences, including New Mexico's periodic-report status.
6. Admitting a partner: conversion mechanics, Form 1065, and K-1 identification for a foreign partner without an ITIN.
7. Corporate-election economics (21%, or about 14% on foreign-derived income) if Apple or fundraising forces it.
8. US sales-tax nexus for SaaS, including how recurring charges count toward 200-transaction tests.
9. The yearly price for preparing and faxing Form 5472.

### What the Uzbek accountant must confirm

1. Whether the offshore list in Tax Code Arts. 181 and 204(2) is Annex 1 naming Delaware and Wyoming, whether it changed after December 2025, and that New Mexico is safe.
2. Whether a single-member US LLC is a foreign legal entity and a CFC, and whether its payouts are 5% dividends or 12% income.
3. Whether a company directed alone from Tashkent is Uzbek-resident under POEM (Art. 34), which documents help, and whether a home office creates a permanent establishment (Art. 36).
4. CFC mechanics: the UZS 300M cliff, notices in low-profit years, and whether SaaS income is active or passive.
5. The participation-notice form, portal and deadline for each new foreign company.
6. The IE route: the UZS 1bn versus 12,000 BRV ceiling, social contributions, E-kontrakt for services to a related foreign company, the repatriation duty, and whether self-employed status fits.
7. The controlled-transaction notice and pricing support if the LLC is in Delaware.
8. IT Park: whether related-party fees count as export, the levy, audit cost, and coverage of CFC profit.
9. Whether funding the LLC (the Atlas fee, early costs) needs FERUz registration under the September 2026 capital rules.
10. Uzbek VAT (Tax Code chapter 39) on ForeverPin sales to Uzbek consumers, and the effect if the LLC is Uzbek-resident.
11. Whether Uzbekistan applies the 1973 US–USSR treaty.
12. The yearly calendar, and the bank documents for each inbound transfer.

---

## Nineteen steps in four gated phases

Answers, no fees:

1. Send the Stripe, fintech and Apple questions; file the replies.
2. Get the Uzbek accountant's written answers to items 1–3 and 6.
3. Engage a US CPA for Form 5472 and the W-8 question, at a fixed yearly price.
4. Pick the state by the Delaware rule, and the route home (IE invoice or distributions).

Formation, about $500:

5. Choose a neutral legal name and register its domain, email and a public company site; Apple requires all three.
6. Get a US phone number; Atlas accepts a virtual one ([Atlas](https://docs.stripe.com/atlas/signup)).
7. Form the LLC (Atlas with entity type LLC, or New Mexico with an agent) and obtain the EIN.
8. File the Uzbek participation notice within one month.
9. On the IE route, register the IE, open its USD account, sign a services contract with the LLC and enter it in E-kontrakt.
10. Request the LLC's free D-U-N-S number.

ForeverPin live:

11. Activate ForeverPin's Stripe account with a ForeverPin-only description, a brand descriptor and the address Stripe approved.
12. Check the Dashboard for Treasury; otherwise open the fintech that said yes and link it for payouts.
13. Turn on Stripe Tax Basic and monitoring, set the product tax code, and collect billing address and tax ID at checkout.
14. Register EU non-Union OSS and UK VAT, or block consumer sales there; decide on Uzbekistan and the other first-sale markets.
15. Move ForeverPin's redirect domains to their own registrar and hosting accounts.
16. Go live, and send money home quarterly against an invoice or a written distribution record.

Later products:

17. Give each new web product its own Stripe account under the LLC.
18. Enroll the LLC with Apple ($99) and Google Play ($25); launch Pose Coach once App Store Connect accepts its tax form and bank.
19. Re-check the six split triggers at every launch; a split product gets a sister LLC owned by the founder.

| When | Duty | Applies |
|---|---|---|
| Monthly, by the 15th | IE turnover return | IE route |
| Quarterly, by the end of the next month | EU OSS return, nil if no sales | OSS registered |
| Quarterly | UK VAT return | UK registered |
| 15 February | IE annual return | IE route |
| 20 March | Uzbek CFC notice | Years CFC profit counts |
| 1 April | Uzbek income declaration | Every year with foreign income |
| 15 April | Form 5472 with pro forma 1120, or Form 7004 | Any reportable transaction |
| 1 June | Delaware LLC tax; Uzbek tax payment | Delaware; every year |
| With the financial statements | Controlled-transaction notice | Delaware LLC invoiced by the IE |

---

## Conclusion

Stripe has already settled the jurisdiction question for a founder in a country it does not serve, so the remaining risk sits in approvals no formation fee can buy: a written yes from Stripe, a fintech willing to bank a Tashkent owner, and an accountant's reading of one list on lex.uz. That inverts the usual spending order. Advice comes before the $500 Atlas fee, because only those answers can still change the plan, and the UAE fallback costs several times more if they come back negative.

The tax planning that matters happens in Tashkent, not in the choice of a foreign flag. Uzbekistan's POEM and CFC rules reach the company wherever it is registered, so hunting for a lower foreign rate matters far less than deciding how money crosses into Uzbekistan; an IE invoice turns a 5–15% exposure into roughly 1% and gives every transfer the paperwork banks ask for. The same scarcity logic redefines the "parent company": the useful parent is a neutral legal name with cleanly separable accounts, and a new legal entity earns its cost only when a named trigger makes another bank approval and another Apple tax form worth fighting for.

---

## Points

Decision queue for the chat, top first; a point closes only on the founder's explicit answer.

- [ ] Structure: one neutral single-member US LLC, with a sister LLC per product only on the six split triggers
- [ ] Written answers before any fee: Stripe, one fintech (Slash, Airwallex or Relay) and an Uzbek accountant
- [ ] State: Delaware through Atlas versus New Mexico, per the accountant's offshore-list answer
- [ ] Route home: IE invoices at 1% of turnover versus yearly distributions at 5%
- [ ] VAT at launch: register EU non-Union OSS and UK VAT, or block consumer sales there
- [ ] Legal name: a neutral name for the LLC, its domain and its email
- [ ] ForeverPin containment: separate registrar and hosting accounts for its redirect domains
- [ ] Pose Coach payouts: Apple's W-9-only screen — escalate, enroll individually, or use a separate app entity

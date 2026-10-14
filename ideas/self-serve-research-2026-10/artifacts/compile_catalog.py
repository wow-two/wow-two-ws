"""Rebuild the saved research catalog from reviewed lane records; no network or product edits."""
import json
import math
from collections import Counter
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
LANES = ['learning', 'creative', 'play', 'everyday']
WEIGHTS = {
    'base': dict(activation=15, recurrence=20, independence=15, demonstrability=10, paid_value=15, differentiation=15, feasibility=10),
    'recurrence': dict(activation=10, recurrence=30, independence=10, demonstrability=5, paid_value=20, differentiation=15, feasibility=10),
    'discovery': dict(activation=20, recurrence=10, independence=15, demonstrability=20, paid_value=10, differentiation=15, feasibility=10),
}
REQUIRED = set('id name family origin user first_result loop return_trigger paid_value pricing dependencies compute content_burden first_scope acquisition competitors difference risk experiment stop_rule overlap scores rationale disposition confidence'.split())

def read(path):
    return json.loads(path.read_text())

def esc(s):
    return str(s).replace('|', '/').replace('\n', ' ')

def proposed_price(p):
    if p['model'] != 'subscription':
        return f"{p['model']}; {p['basis']}"
    amounts = []
    if p.get('monthly_usd') is not None:
        amounts.append(f"USD {p['monthly_usd']:g}/month")
    if p.get('annual_usd') is not None:
        amounts.append(f"USD {p['annual_usd']:g}/year (USD {p['annual_usd']/12:.2f} normalized monthly)")
    return '; '.join(amounts) + '; hypothesis'

def main():
    products = []
    reviews = {}
    for lane in LANES:
        items = read(ROOT / 'lanes' / f'{lane}.json')
        assert len(items) == 25, (lane, len(items))
        products.extend(items)
        review_items = read(ROOT / 'artifacts' / f'review-{lane}.json')
        assert len(review_items) == 25, (lane, 'review count')
        for r in review_items:
            assert r['id'] not in reviews, r['id']
            reviews[r['id']] = r
    overrides = {r['id']:r for r in read(ROOT / 'artifacts' / 'root-adjudication.json')}
    expected = {f'E{i:03}' for i in range(1, 101)}
    assert len(products) == 100
    assert {p['id'] for p in products} == expected
    assert len({p['name'].casefold() for p in products}) == 100
    assert set(reviews) == expected
    assert all(sum(w.values()) == 100 for w in WEIGHTS.values())
    for p in products:
        assert REQUIRED <= p.keys(), (p['id'], REQUIRED-p.keys())
        assert len(p['loop']) == 4 and len(p['first_scope']) >= 3
        p['author_scores'] = dict(p['scores'])
        p['author_disposition'] = p['disposition']
        p['review'] = reviews[p['id']]
        r = p['review']
        assert r['evidence_sufficient'], (p['id'], 'source gap remains')
        existing_urls = {c['url'] for c in p['competitors']}
        for extra in r.get('additional_evidence', []):
            if extra['url'] not in existing_urls:
                extra = dict(extra)
                extra.setdefault('relation', 'direct')
                p['competitors'].append(extra)
                existing_urls.add(extra['url'])
        p['scores'].update(r.get('proposed_scores') or {})
        if r.get('proposed_disposition'):
            p['disposition'] = r['proposed_disposition']
        p['adjudication'] = overrides.get(p['id'], {'id':p['id'], 'reason':'Accepted the independent review; no additional root correction.'})
        o = p['adjudication']
        p['scores'].update(o.get('scores') or {})
        if o.get('disposition'):
            p['disposition'] = o['disposition']
        for k, value in (o.get('fields') or {}).items():
            assert k not in ['id', 'scores', 'review', 'adjudication']
            p[k] = value
        assert set(p['scores']) == set(WEIGHTS['base'])
        assert all(isinstance(v, int) and 1 <= v <= 5 for v in p['scores'].values())
        assert p['disposition'] in ['shortlist','reserve','defer']
        assert p['competitors']
        for c in p['competitors']:
            assert set(['name','url','accessed','relation','facts','price']) <= c.keys()
            assert urlparse(c['url']).scheme == 'https' and urlparse(c['url']).netloc
            assert c['accessed'] == '2026-10-09' and c['facts'] and c['price']
        pricing = p['pricing']
        if pricing['model'] != 'subscription':
            assert pricing['monthly_usd'] is None and pricing['annual_usd'] is None
        for key in ['monthly_usd','annual_usd']:
            assert pricing.get(key) is None or pricing[key] > 0
        p['score_totals'] = {key:round(sum(w[k]*p['scores'][k]/5 for k in w),1) for key,w in WEIGHTS.items()}
        p['ranks'] = {}
        p['accounts_for_5000_mrr'] = {
            'monthly_plan':math.ceil(5000/pricing['monthly_usd']) if pricing['model']=='subscription' and pricing.get('monthly_usd') else None,
            'annual_plan':math.ceil(5000/(pricing['annual_usd']/12)) if pricing['model']=='subscription' and pricing.get('annual_usd') else None,
        }
    for scenario in WEIGHTS:
        ordered = sorted(products,key=lambda p:(-p['score_totals'][scenario],-p['scores']['paid_value'],-p['scores']['differentiation'],p['id']))
        for rank,p in enumerate(ordered,1):
            p['ranks'][scenario] = rank
    products.sort(key=lambda p:p['id'])
    selection=read(ROOT/'artifacts/roadmap-selection.json')
    assert len(selection)==5 and len({s['id'] for s in selection})==5
    indexed={p['id']:p for p in products}
    shortlist=[]
    for s in selection:
        p=indexed[s['id']]
        assert p['pricing']['model']=='subscription' and len(p['competitors'])>=2
        assert not p.get('consolidated_into')
        p['roadmap_selection']=s
        shortlist.append(p)
    (ROOT/'shortlist-5.json').write_text(json.dumps(shortlist,indent=2,ensure_ascii=False)+'\n')
    (ROOT/'products.json').write_text(json.dumps(products,indent=2,ensure_ascii=False)+'\n')
    catalog = ['# One hundred self-serve product candidates','', '*Research date: 2026-10-09*','',
        'These are assessed candidates, not 100 approved businesses. Scores prioritize experiments; competitor offers do not prove demand for these proposals. Prices marked hypothesis are proposed USD prices. See the [decision report](self-serve-research-2026-10.md), [protocol](research-protocol.md), [ranked comparison](ranked-100.md), and [challenge log](review-log.md).','']
    for p in products:
        catalog.extend([f'<a id="{p["id"].lower()}"></a>',f'## {p["id"]} — {p["name"]}','',
            f"**Origin:** {p['origin']}  |  **Disposition:** {p['disposition']}  |  **Score:** {p['score_totals']['base']:g}/100 (rank {p['ranks']['base']})",'',
            f"**User and first value.** {p['user']} {p['first_result']}",'',
            '**Experience.** '+' → '.join(p['loop'])+'. '+p['return_trigger'],'',
            f"**Paid proposition.** {p['paid_value']} **Price test:** {proposed_price(p['pricing'])}. Free: {p['pricing']['free']}. Paid: {p['pricing']['paid']}.",'',
            '**First complete scope.** '+'; '.join(p['first_scope'])+'.','',
            '**Dependencies and operating burden.** '+'; '.join(p['dependencies'])+'. '+p['compute']+' '+p['content_burden'],'',
            f"**Acquisition experiment.** {p['acquisition']}",'',
            '**Observed alternatives** (opened 2026-10-09):',''])
        for c in p['competitors']:
            catalog.append(f"- [{c['name']}]({c['url']}) ({c['relation']}): {c['facts']} Price: {c['price']}.")
        catalog.extend(['',f"**Proposed distinction.** {p['difference']}",'',f"**Argument against building.** {p['risk']}",'',
            f"**Test and stop rule.** {p['experiment']} {p['stop_rule']}",'',f"**Portfolio boundary.** {p['overlap']}",'',
            f"**Challenge.** {p['review']['rationale']} {p['adjudication']['reason']}",'',
            f"**Evidence confidence.** {p['confidence']}",'','---',''])
    (ROOT/'catalog-100.md').write_text('\n'.join(catalog))
    ranks = ['# Ranked self-serve candidates','', '*Research date: 2026-10-09*','',
        'Scores are judgments, not success probabilities. Differences under five points form one broad tier. Ranking all candidates measures experience attractiveness, including one-time products; it does not automatically select an MRR roadmap. Kids Curiosity is user-selected independently. See the [decision report](self-serve-research-2026-10.md) for the five-product preparation recommendation.','',
        'Base weights: activation 15, recurrence 20, independence 15, demonstrability 10, paid value 15, differentiation 15, feasibility 10. Recurrence-heavy: 10/30/10/5/20/15/10. Discovery-heavy: 20/10/15/20/10/15/10, in the same dimension order. Tie-break: paid value, differentiation, stable ID; tie-breaks are not evidence.','',
        '| Rank | Candidate | Base | Recurrence rank | Discovery rank | Model | Disposition |',
        '|---:|---|---:|---:|---:|---|---|']
    for p in sorted(products,key=lambda p:p['ranks']['base']):
        ranks.append(f"| {p['ranks']['base']} | [{p['id']} {esc(p['name'])}](catalog-100.md#{p['id'].lower()}) | {p['score_totals']['base']:g} | {p['ranks']['recurrence']} | {p['ranks']['discovery']} | {p['pricing']['model']} | {p['disposition']} |")
    ranks.extend(['','## Dimension scores','','| ID | Activation | Recurrence | Independence | Demonstrability | Paid value | Differentiation | Feasibility |','|---|---:|---:|---:|---:|---:|---:|---:|'])
    for p in products:
        ranks.append('| '+p['id']+' | '+' | '.join(str(p['scores'][k]) for k in WEIGHTS['base'])+' |')
    (ROOT/'ranked-100.md').write_text('\n'.join(ranks)+'\n')
    evidence=['# Primary-source evidence register','','*All sources opened 2026-10-09.*','',
        'Source pages establish available offers and documented features, not verified revenue, retention, market size or demand for a new entrant. Developer app listings are primary offer descriptions, not independent outcome verification. Repeated URLs serve different candidate comparisons; counts do not imply independent markets. Unknown or ambiguous prices remain unknown.','',
        '| Candidate | Alternative / relation | Observed fact | Price observation |','|---|---|---|---|']
    for p in products:
        for c in p['competitors']:
            evidence.append(f"| {p['id']} | [{esc(c['name'])}]({c['url']}) / {esc(c['relation'])} | {esc(c['facts'])} | {esc(c['price'])} |")
    (ROOT/'evidence-register.md').write_text('\n'.join(evidence)+'\n')
    log=['# Independent challenge and root adjudication','','*Reviewed 2026-10-09.*','',
        'Learning was challenged by root; creative by the learning researcher; play by the creative researcher; everyday by the play researcher. Root inspected the combined portfolio and resolved scoring, overlap and selection. These are separate analyst passes, not customer validation or independent market research firms.','',
        'Original lane files retain author judgments. `products.json` contains accepted reviewer changes plus root adjudication. Every score change is explicit; no opaque penalty is subtracted.','',
        '| ID | Verdict | Score changes | Final disposition | Challenge and root resolution |','|---|---|---|---|---|']
    for p in products:
        changes=', '.join(f'{k}: {p["author_scores"][k]}→{p["scores"][k]}' for k in WEIGHTS['base'] if p['author_scores'][k]!=p['scores'][k]) or 'none'
        log.append(f"| {p['id']} | {p['review']['verdict']} | {changes} | {p['disposition']} | {esc(p['review']['rationale'])} {esc(p['adjudication']['reason'])} |")
    (ROOT/'review-log.md').write_text('\n'.join(log)+'\n')
    old=read(ROOT.parent/'saas-research-2026-10/products.json')
    stats={
        'product_count':len(products),'unique_ids':len({p['id'] for p in products}),'independently_challenged':len(reviews),
        'primary_source_references':sum(len(p['competitors']) for p in products),
        'unique_primary_urls':len({c['url'] for p in products for c in p['competitors']}),
        'per_lane':dict(Counter(p['family'] for p in products)),
        'models':dict(Counter(p['pricing']['model'] for p in products)),
        'dispositions':dict(Counter(p['disposition'] for p in products)),
        'consolidated_concepts':{p['id']:p['consolidated_into'] for p in products if p.get('consolidated_into')},
        'roadmap_selection':[s['id'] for s in selection],
        'old_catalog_count':len(old),'old_catalog_multi_role_count':sum(len(p['roles'])>=2 for p in old),
        'old_catalog_lanes':dict(Counter(p['research_lane'] for p in old)),
        'weights':WEIGHTS,'schema_and_arithmetic':'passed',
        'limits':'Schema and arithmetic checks do not verify source truth, customer demand, legal readiness, paid conversion or retention. Human-readable source observations and analyst review are the evidence for desk research.'}
    (ROOT/'artifacts/catalog-checks.json').write_text(json.dumps(stats,indent=2)+'\n')
    print(json.dumps(stats,indent=2))

if __name__=='__main__':
    main()

"""Validate the research inventory and reproduce the comparison artifacts. No network writes."""
import collections
import html
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent
WEIGHTS = dict(pain=20, pay=15, reach=20, repeat=15, wedge=10, build=10, margin=5, portability=5)
LANES = ('developer', 'business', 'creator', 'personal')
EXPLORATION = {'W0006', 'W0751', 'W0753', 'W0754', 'W0759', 'W0761', 'W0767', 'W0774', 'W0777', 'W0789'}
# Central risk comments are qualitative to avoid double-counting risks in lane scores.
CENTRAL_REVIEWS = {
    'W0001': 'Strong importer substitutes; require repeat schemas and a cheaper adoption path.',
    'W0003': 'Broad API coverage and false positives can turn monitoring into support work.',
    'W0004': 'Payload privacy and incumbent replay tools weaken a hosted general-purpose offer.',
    'W0005': 'Needs reliable instrumentation of expected callbacks; do not become a delivery proxy.',
    'W0007': 'Restore evidence needs credible execution and privileged integration; start with supplied logs.',
    'W0008': 'Database-specific analysis needs production-like evidence before claiming safety.',
    'W0009': 'Data access and reconciliation edge cases complicate self-service.',
    'W0010': 'Free CI artifacts and existing test systems may absorb the ownership workflow.',
    'W0011': 'Provider billing and job data differ; prove a one-provider saving first.',
    'W0013': 'Language/runtime matrices create recurring maintenance beyond the initial demo.',
    'W0016': 'Free validators exist; charge for ownership and repeat release review only.',
    'W0017': 'Rendering costs and false positives need strict page and locale limits.',
    'W0018': 'Automation cannot establish full accessibility; triage ownership and reviewer history are the paid hypothesis.',
    'W0019': 'Mail delivery and client rendering are hard to guarantee under a cheap flat plan.',
    'W0021': 'Credential metadata is sensitive; do not custody or rotate secrets in the MVP.',
    'W0023': 'Free license scanners and legal interpretation limit differentiated claims.',
    'W0024': 'Cloud account access, billing lag and attribution increase onboarding effort.',
    'W0026': 'Feature-flag vendors may already supply cleanup signals.',
    'W0027': 'Release coordination may be a feature of an existing project tool.',
    'W0029': 'Browser rendering and support impose per-site costs; no unlimited sites.',
    'W0030': 'Free monitoring is substantial; client ownership and handoff must drive payment.',
    'W0034': 'Configuration can contain secrets; prefer local comparison and redacted reports.',
    'W0037': 'Privileged database integration and security review delay small self-service sales.',
    'W0038': 'Expiry metadata may not be available; manual input must still deliver value.',
    'W0256': 'Time and billing integrations can overwhelm a narrow margin-review product.',
    'W0264': 'The record cannot establish legal or security sufficiency.',
    'W0268': 'Control evidence is sensitive and cannot replace independent assurance.',
    'W0269': 'Sensitive hiring data and subjective scoring require a narrow consented workflow.',
    'W0270': 'ATS integration or disciplined manual use is required for dependable reminders.',
    'W0271': 'Sensitive candidate evidence and ATS substitutes weaken a standalone purchase.',
    'W0272': 'Reference collection involves personal data and jurisdiction-specific expectations.',
    'W0273': 'Recruiting platforms already cover shortlist review; avoid replacing an ATS.',
    'W0275': 'Onboarding records create access and privacy obligations.',
    'W0276': 'Commitments may remain in CRM; prove value with supplied exports first.',
    'W0277': 'Support platforms already own escalation; a new inbox risks duplicate work.',
    'W0279': 'Customer onboarding platforms bundle dependency tracking.',
    'W0280': 'Customer-success suites and incomplete outcome data can prevent adoption.',
    'W0282': 'Refund approvals must not execute money movement in the pilot.',
    'W0283': 'Sensitive invoice/customer records need a narrow evidence-only scope.',
    'W0285': 'False duplicate flags and sensitive financial files increase review effort.',
    'W0287': 'Participant identity and consent tracking are personal-data workflows.',
    'W0501': 'Existing sponsor platforms cover much of inventory; test conflict-specific value.',
    'W0503': 'Free checklists and built-in previews are strong substitutes.',
    'W0507': 'Guest scheduling and release collection are already bundled elsewhere.',
    'W0508': 'Free feed validators exist; payment depends on dependable repeated monitoring.',
    'W0511': 'Free subtitle editors solve many checks; the paid handoff must save team time.',
    'W0512': 'Subtitle editing incumbents may already handle revision workflows.',
    'W0516': 'Owner-supplied contract metadata is required; no legal interpretation guarantee.',
    'W0518': 'Correlated with developer localization QA; do not launch both initially.',
    'W0521': 'Free EPUB checking exists; sell scoped review evidence, not compliance certification.',
    'W0523': 'Store and access APIs create platform dependencies; begin with CSV reconciliation.',
    'W0524': 'Royalty rules vary; restrict supported rules and avoid payment custody.',
    'W0526': 'Access revocation requires integrations and mistakes can harm paying customers.',
    'W0527': 'Membership platform APIs and privacy complicate access comparison.',
    'W0530': 'Community platforms bundle onboarding; prove a missing measurable workflow.',
    'W0531': 'Live-event reliability is costly; start with preparation and exported run sheets.',
    'W0535': 'SEO crawlers already cover link audits; demonstrate editorial decisions saved.',
    'W0537': 'Rate limits, destination changes and free link checkers can dominate support.',
    'W0538': 'Permission records do not establish enforceability in every jurisdiction.',
    'W0751': 'Sensitive possession records and infrequent updates weaken subscription retention.',
    'W0753': 'paintRack and free notes are strong substitutes; recipe reuse is untested.',
    'W0754': 'Existing sewing organizers require a clear fit-history advantage.',
    'W0771': 'Source tracing must avoid unsupported correctness claims and uncapped inference.',
    'W0772': 'Review platforms already handle parts of extraction; compare an actual round.',
    'W0773': 'Open retraction data does not imply willingness to pay for alerts.',
    'W0778': 'Participant privacy and free qualitative tools increase adoption friction.',
}
FAMILY_MERGES = {
    'caption-change-management': 'caption-quality-assurance',
    'creative-localization-quality': 'localization-quality',
    'brand-client-handoff': 'client-handoff',
    'agency-handoff': 'client-handoff',
    'creative-asset-handoff': 'client-handoff',
    'agency-acceptance': 'client-deliverable-approval',
    'creative-review-resolution': 'client-deliverable-approval',
    'photo-client-revision': 'client-deliverable-approval',
}
FAMILY_PREFERENCES = {
    # Prefer the explicitly falsified, file-only signoff experiment over another subtitle editor workflow.
    'caption-quality-assurance': 'W0511',
}


def write_json(name, data):
    (ROOT / name).write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n')


def esc(value):
    return str(value).replace('|', '\\|').replace('\n', ' ')


def price(row):
    recurring, once = row.get('price_monthly_usd'), row.get('price_once_usd')
    return (f'${recurring:g}/month' if recurring else '') + (' or ' if recurring and once else '') + (f'${once:g} once' if once else '') or 'Free / unspecified'


def main():
    ideas, sources = [], []
    required = {'id', 'name', 'family', 'buyer', 'job', 'wedge', 'model', 'scores', 'channel', 'risk', 'evidence', 'source_ids', 'evidence_fit', 'decision', 'reason', 'mvp', 'validation'}
    details = {'competitors', 'pricing_test', 'cost_risk', 'global_note', 'kill_test', 'research_note'}
    for lane in LANES:
        data = json.loads((ROOT / f'{lane}.json').read_text())
        assert len(data['ideas']) == 250, lane
        assert len([r for r in data['ideas'] if r['evidence'] == 'desk_researched']) == 40, lane
        sources.extend(data['sources'])
        for original in data['ideas']:
            row = dict(original, lane=lane)
            assert not (required - row.keys()), (row['id'], required - row.keys())
            assert set(row['scores']) == set(WEIGHTS)
            assert all(isinstance(v, int) and 1 <= v <= 5 for v in row['scores'].values())
            assert row['evidence'] in {'screened', 'desk_researched'}
            if row['evidence'] == 'desk_researched':
                assert not (details - row.keys()), (row['id'], details - row.keys())
                assert row['source_ids'] and row['evidence_fit'] in {'direct', 'adjacent'}
            row['raw_score'] = round(sum(WEIGHTS[k] * v / 5 for k, v in row['scores'].items()), 1)
            penalty = 0
            reason = CENTRAL_REVIEWS.get(row['id'], 'Lane score carries the stated risks; no additional central risk comment.')
            row['central_penalty'] = penalty
            row['central_review'] = reason
            row['evidence_penalty'] = 2 if row['evidence_fit'] == 'adjacent' else (8 if row['evidence_fit'] == 'none' else 0)
            row['priority_score'] = row['raw_score'] - penalty - row['evidence_penalty']
            row['portfolio_family'] = FAMILY_MERGES.get(row['family'], row['family'])
            row['customers_for_5000_mrr'] = math.ceil(5000 / row['price_monthly_usd']) if row.get('price_monthly_usd') else None
            row['selection'] = 'screened_out'
            row['selection_reason'] = row['reason']
            ideas.append(row)
    by_id = {r['id']: r for r in ideas}
    by_source = {s['id']: s for s in sources}
    assert len(ideas) == len(by_id) == 1000
    assert set(by_id) == {f'W{i:04}' for i in range(1, 1001)}
    assert len(by_source) == len(sources)
    assert len({r['name'].casefold().strip() for r in ideas}) == 1000, 'Duplicate exact titles'
    for row in ideas:
        assert set(row['source_ids']) <= set(by_source), row['id']
    # Review cohorts reflect actual work: promising leads were researched while generation continued.
    review_pool = set()
    for lane in LANES:
        lane_rows = [r for r in ideas if r['lane'] == lane]
        review_pool.update(r['id'] for r in lane_rows if r['evidence'] == 'desk_researched')
        screened = sorted((r for r in lane_rows if r['evidence'] == 'screened'), key=lambda r: (-r['raw_score'], r['id']))
        review_pool.update(r['id'] for r in screened[:35])
    assert len(review_pool) == 300
    research_pool = [r for r in ideas if r['evidence'] == 'desk_researched']
    assert len(research_pool) == 160
    order = lambda r: (-r['priority_score'], -r['scores']['reach'], -r['scores']['pain'], r['id'])
    selected, used_families = [], set()
    # Ten intentionally exploratory positions preserve requested collector and one-time models.
    for ident in sorted(EXPLORATION):
        row = by_id[ident]
        assert row in research_pool
        assert row['decision'] != 'reject', ident
        assert row['portfolio_family'] not in used_families
        selected.append(row)
        used_families.add(row['portfolio_family'])
        row['selection_basis'] = 'exploratory'
    for row in sorted(research_pool, key=order):
        if len(selected) == 100:
            break
        if row['id'] in EXPLORATION or row['portfolio_family'] in used_families or row['decision'] == 'reject':
            continue
        if row['portfolio_family'] in FAMILY_PREFERENCES and row['id'] != FAMILY_PREFERENCES[row['portfolio_family']]:
            continue
        selected.append(row)
        used_families.add(row['portfolio_family'])
        row['selection_basis'] = 'priority'
    assert len(selected) == 100
    selected.sort(key=order)
    selected_ids = {r['id'] for r in selected}
    for row in ideas:
        row['review_pool_300'] = row['id'] in review_pool
        if row['id'] in selected_ids:
            row['selection'] = 'shortlist'
            row['selection_reason'] = ('Exploratory option retained for collector/personal or local one-time purchase learning; not an initial MRR recommendation.' if row['selection_basis'] == 'exploratory' else 'Researched candidate retained after qualitative risk review, evidence adjustment and conservative family deduplication; paid-pilot gate remains open.')
            if row['decision'] == 'reserve':
                row['selection_reason'] += ' Lane reserve remains in force: this is a conditional discovery experiment, not an advance-to-build decision.'
            if FAMILY_PREFERENCES.get(row['portfolio_family']) == row['id']:
                row['selection_reason'] += ' Explicit family preference: test editor-independent client signoff on supplied files before building subtitle revision propagation; this overrides the sibling score and is not demand evidence.'
        elif row['evidence'] == 'desk_researched':
            row['selection'] = 'researched_reserve'
            row['selection_reason'] = ('Correlated family already represented in the 100; preserve as a variant, not another launch.' if row['portfolio_family'] in used_families else 'Below the retained priority band or rejected by the lane; evidence does not support a first-wave build.')
        elif row['id'] in review_pool:
            row['selection'] = 'screened_review_pool'
            row['selection_reason'] = 'High screening score, but no individual live competitor research; return here if leading paid tests fail.'
    for rank, row in enumerate(selected, 1):
        row['rank'] = rank
    # Business ranking ties carry no statistically meaningful difference.
    write_json('selection.json', dict(date='2026-09-28', methodology='Analyst priority, not probability; 90 evidence-ranked plus 10 explicitly exploratory, one per conservative family; one explicit caption-family preference.', family_preferences=FAMILY_PREFERENCES, shortlist=[r['id'] for r in selected], review_pool_300=sorted(review_pool), ideas=ideas))
    counts = dict(total=1000, review_pool=300, desk_researched=160, shortlist=100, customer_validated=0, source_records=len(sources), unique_source_urls=len({s['url'].rstrip('/') for s in sources}), families=len({r['portfolio_family'] for r in ideas}), shortlist_lanes=dict(collections.Counter(r['lane'] for r in selected)), shortlist_models=dict(collections.Counter(r['model'] for r in selected)))
    write_json('verification.json', dict(status='passed', checks=['250 per lane', 'contiguous unique W0001–W1000', 'unique exact names', 'all required fields', 'eight bounded score dimensions', 'valid source references', '40 researched per lane', '300 review cohort', '100 shortlisted', 'one selected per conservative family', 'zero rejected ideas in shortlist', 'MRR customer arithmetic'], **counts))
    lines = ['# Distilled 100 software opportunities', '', 'Research date: 2026-09-28. These are experiments, not validated businesses. Priority scores are analyst judgments; a 1–3 point difference is not meaningful. All prices are proposed USD prices, before fees/tax. The customer column is ceil($5,000 / proposed monthly price), not a sales forecast. Lifetime receipts contribute zero MRR.', '', 'The final set retains 90 ranked candidates and 10 explicitly exploratory collector/personal/one-time options. Family limits prevent related features being counted as independent launches. No customer has validated a candidate.', '', '| Rank | ID | Candidate | Priority /100 | Proposed price | Subscription accounts for $5K MRR | Basis | Lane decision |', '|---:|---|---|---:|---|---:|---|---|']
    for row in selected:
        lines.append(f"| {row['rank']} | [{row['id']}](#{row['id'].lower()}) | {esc(row['name'])} | {row['priority_score']:g} | {price(row)} | {row['customers_for_5000_mrr'] or '—'} | {row['selection_basis']} | {row['decision']} |")
    for row in selected:
        lines += ['', f"## {row['id']}", '', f"### {row['rank']}. {row['name']}", '', f"**Buyer:** {row['buyer']}. **Family:** {row['portfolio_family']}. **Model:** {row['model']}. **Evidence:** {row['evidence_fit']} commercial/category evidence; no customer validation.", '', f"**Lane disposition:** {row['decision']}. {row['reason']}", '', f"**Job:** {row['job']}", '', f"**Proposed distinction:** {row['wedge']}", '', f"**Competition:** {row['competitors']}", '', f"**Pricing experiment:** {row['pricing_test']}", '', f"**Economics:** {price(row)} proposed. " + (f"{row['customers_for_5000_mrr']} active paying subscription accounts would reach at least $5K gross MRR at that realized price; acquisition, churn, tax, fees and labor are additional." if row['customers_for_5000_mrr'] else 'This offer produces no recurring revenue; evaluate contribution per sale separately.'), '', f"**Acquisition hypothesis:** {row['channel']}", '', f"**MVP boundary:** {row['mvp']}", '', f"**Cost and global constraints:** {row['cost_risk']} {row['global_note']}", '', f"**Failure mode:** {row['risk']}", '', f"**Validation:** {row['validation']}", '', f"**Stop condition:** {row['kill_test']}", '', f"**Evidence limit:** {row['research_note']}", '', f"**Rating:** raw {row['raw_score']:g}; central risk deduction {row['central_penalty']}; evidence deduction {row['evidence_penalty']}; priority {row['priority_score']:g}. Dimensions: " + ', '.join(f'{k} {v}/5' for k,v in row['scores'].items()) + '.', '', f"**Central review:** {row['central_review']} {row['selection_reason']}", '', '**Live source links:** ' + '; '.join(f"[{sid}: {by_source[sid]['title']}]({by_source[sid]['url']})" for sid in row['source_ids']) + '.']
    (ROOT / 'shortlist-100.md').write_text('\n'.join(lines) + '\n')
    lines = ['# Source register', '', 'Access date: 2026-09-28 unless a record states otherwise. Vendor offers establish competition and advertised prices, not revenue, active users or demand for the proposed product. Recheck checkout currency, billing, taxes, quotas and licensing before spending. Unknown prices remain unknown.', '']
    for s in sources:
        lines += [f"## {s['id']} — {s['title']}", '', f"[Primary source]({s['url']}) · Checked {s['checked']}", '', f"Observed: {s['supports']}", '', f"Price: {s['price_observed']}", '', f"Limit: {s['caveat']}", '']
    (ROOT / 'sources.md').write_text('\n'.join(lines))
    lines = ['# All 1,000 screened hypotheses', '', 'Each row is an analyst screen; 160 have live competitor research and 100 are retained. See lane JSON for the full buyer, job, proposed price, dimension ratings, MVP, channel and kill hypotheses. “Screened” never means market verified. All exact titles are unique; related jobs remain correlated.', '', '| ID | Candidate | Buyer | Raw /100 | Proposed price | Evidence | Disposition | Main failure mode |', '|---|---|---|---:|---|---|---|---|']
    for r in ideas:
        lines.append('| ' + ' | '.join(esc(v) for v in [r['id'],r['name'],r['buyer'],f"{r['raw_score']:g}",price(r),r['evidence'],r['selection'],r['risk']]) + ' |')
    (ROOT / 'catalogue-1000.md').write_text('\n'.join(lines) + '\n')
    build_browser(ideas, sources, counts)
    print(json.dumps(counts, indent=2))
    print('\nTop20:')
    for r in selected[:20]:
        print(r['rank'], r['id'], r['priority_score'], r['name'])


def build_browser(ideas, sources, counts):
    data = json.dumps(dict(ideas=ideas, sources=sources, counts=counts), ensure_ascii=False).replace('</', '<\\/')
    template = '''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>WoW2 opportunity research</title>
<style>:root{color-scheme:light;--ink:#17332f;--muted:#526b65;--line:#d4dfda;--accent:#146c58}*{box-sizing:border-box}body{margin:0;background:#f6f7f2;color:var(--ink);font:16px/1.5 system-ui,sans-serif}header,main{max-width:1440px;margin:auto;padding:28px}header{border-bottom:1px solid var(--line)}h1{font:42px/1.1 Georgia,serif;margin:10px 0}p{max-width:1000px}.eyebrow{letter-spacing:.14em;font-size:12px;color:var(--accent)}.muted{color:var(--muted)}.stats{display:flex;gap:28px;flex-wrap:wrap}.stats strong{display:block;font-size:28px}.controls{display:flex;gap:12px;flex-wrap:wrap;margin:20px 0}input,select,button{padding:11px;border:1px solid var(--line);border-radius:6px;background:white;color:var(--ink);font:inherit}input{min-width:260px;flex:1}button{cursor:pointer}button:hover{border-color:var(--accent)}.layout{display:grid;grid-template-columns:minmax(0,1.3fr) minmax(320px,1fr);gap:24px}.scroll{max-height:78vh;overflow:auto}table{border-collapse:collapse;width:100%;font-size:14px}th{text-align:left;position:sticky;top:0;background:#e7eee7}th,td{padding:12px;border-bottom:1px solid var(--line);vertical-align:top}td button{padding:0;border:0;background:none;text-align:left;font-weight:600}tr.active{background:#e0eee6}small{display:block;color:var(--muted)}article{background:white;border:1px solid var(--line);border-radius:10px;padding:24px;max-height:78vh;overflow:auto}article h2{margin-top:0;font-size:24px}article h3{margin-bottom:5px;font-size:15px}article p{margin-top:0;font-size:15px}a{color:var(--accent)}.tag{display:inline-block;padding:3px 8px;background:#e7eee7;border-radius:4px;font-size:12px;margin:0 5px 10px 0}@media(max-width:900px){.layout{grid-template-columns:1fr}article{max-height:none}.scroll{max-height:55vh}header,main{padding:18px}h1{font-size:32px}}</style>
<header><div class="eyebrow">WOW2 / RESEARCH / 28 SEPTEMBER 2026</div><h1>1,000 hypotheses. 100 experiments.</h1><p>Global software opportunities, ranked for a bootstrap portfolio. Competitor offers are evidence of competition, not proof of demand. <strong>Zero customer-validated ideas.</strong></p><div class="stats"><div><strong>1,000</strong>screened</div><div><strong>160</strong>desk researched</div><div><strong>100</strong>shortlisted</div><div><strong>$20–50</strong>initial monthly budget</div></div><p class="muted">Proposed prices and scores are analyst judgments. The $5K target is gross MRR. Lifetime sales contribute zero MRR. About $300 monthly spending becomes an option only when revenue funds it.</p></header>
<main><div class="controls"><input id="search" aria-label="Search ideas" placeholder="Search buyer, job, risk or idea…"><select id="view" aria-label="Research set"><option value="shortlist">Distilled 100</option><option value="all">All 1,000</option><option value="researched">160 researched</option><option value="pool">300 review cohort</option></select><select id="lane" aria-label="Category"><option value="">All categories</option><option>developer</option><option>business</option><option>creator</option><option>personal</option></select><select id="model" aria-label="Business model"><option value="">All models</option><option>subscription</option><option>freemium</option><option>lifetime</option><option>hybrid</option><option>usage</option><option>free</option></select><select id="sort" aria-label="Sort"><option value="priority">Priority score</option><option value="price">Proposed recurring price</option><option value="id">ID</option></select></div><p id="count" class="muted"></p><div class="layout"><div class="scroll"><table><thead><tr><th>Opportunity</th><th>Priority</th><th>Price</th></tr></thead><tbody id="rows"></tbody></table></div><article id="detail" aria-live="polite"></article></div></main>
<script id="data" type="application/json">__DATA__</script><script>
const data=JSON.parse(document.getElementById('data').textContent),sources=Object.fromEntries(data.sources.map(s=>[s.id,s]));let active='';
const el=id=>document.getElementById(id),e=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const price=r=>(r.price_monthly_usd?'$'+r.price_monthly_usd+'/mo':'')+(r.price_monthly_usd&&r.price_once_usd?' or ':'')+(r.price_once_usd?'$'+r.price_once_usd+' once':'')||'Free / unspecified';
function detail(id){active=id;const r=data.ideas.find(x=>x.id===id);if(!r)return;const part=(title,value)=>value?'<h3>'+e(title)+'</h3><p>'+e(value)+'</p>':'';el('detail').innerHTML='<span class="tag">'+e(r.id)+'</span><span class="tag">'+e(r.evidence)+'</span><span class="tag">'+e(r.selection)+'</span><span class="tag">lane: '+e(r.decision)+'</span><h2>'+e(r.name)+'</h2>'+part('Buyer',r.buyer)+part('Job and proposed distinction',r.job+'. '+r.wedge)+part('Pricing hypothesis',price(r)+'. '+(r.pricing_test||r.model))+part('$5K gross MRR arithmetic',r.customers_for_5000_mrr?r.customers_for_5000_mrr+' paying subscription accounts at the proposed realized monthly price; one-time buyers excluded. No conversion or retention forecast.':'No recurring revenue from this offer.')+part('Competition',r.competitors||'No individual live competitor research; hypothesis only.')+part('Acquisition hypothesis',r.channel)+part('MVP boundary',r.mvp)+part('Failure and cost risks',r.risk+'. '+(r.cost_risk||''))+part('Global constraints',r.global_note)+part('Validation and stop gate',r.validation+' '+(r.kill_test||''))+part('Rating', 'Raw '+r.raw_score+'; central deduction '+r.central_penalty+'; evidence deduction '+r.evidence_penalty+'; priority '+r.priority_score+'. '+r.central_review)+part('Lane disposition',r.decision+'. '+r.reason)+part('Selection',r.selection_reason)+part('Evidence limit',r.research_note)+'<h3>Sources</h3>'+r.source_ids.map(sid=>{const s=sources[sid];return '<p><a target="_blank" rel="noopener noreferrer" href="'+e(s.url)+'">'+e(s.title)+'</a><small>'+e(s.price_observed)+'</small></p>'}).join('');document.querySelectorAll('tbody tr').forEach(tr=>tr.classList.toggle('active',tr.dataset.id===id));}
function render(){const q=el('search').value.toLowerCase().trim(),view=el('view').value,lane=el('lane').value,model=el('model').value;let rows=data.ideas.filter(r=>(view==='all'||view==='shortlist'&&r.selection==='shortlist'||view==='researched'&&r.evidence==='desk_researched'||view==='pool'&&r.review_pool_300)&&(!lane||r.lane===lane)&&(!model||r.model===model)&&(!q||[r.id,r.name,r.buyer,r.job,r.wedge,r.risk].join(' ').toLowerCase().includes(q)));const sort=el('sort').value;rows.sort((a,b)=>sort==='id'?a.id.localeCompare(b.id):sort==='price'?(b.price_monthly_usd||0)-(a.price_monthly_usd||0):b.priority_score-a.priority_score||a.id.localeCompare(b.id));el('count').textContent=rows.length+' opportunities • scores rank hypotheses, not success probabilities';el('rows').innerHTML=rows.map(r=>'<tr data-id="'+r.id+'"><td><button data-open="'+r.id+'">'+e(r.name)+'</button><small>'+e(r.id+' · '+r.decision+' · '+r.buyer)+'</small></td><td>'+r.priority_score+'<small>raw '+r.raw_score+'</small></td><td>'+e(price(r))+'</td></tr>').join('');if(rows.length)detail(rows.some(r=>r.id===active)?active:rows[0].id);else el('detail').textContent='No matching ideas.';}
document.querySelectorAll('input,select').forEach(x=>x.addEventListener('input',render));el('rows').addEventListener('click',ev=>{const b=ev.target.closest('[data-open]');if(b)detail(b.dataset.open)});render();</script></html>'''
    (ROOT / 'research-browser.html').write_text(template.replace('__DATA__', data))


if __name__ == '__main__':
    main()

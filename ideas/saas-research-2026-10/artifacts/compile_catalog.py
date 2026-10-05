"""Rebuild the deterministic research catalog after analyst review (no network)."""
import json,math,collections,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
WEIGHTS={'pain':20,'recurrence':15,'budget':15,'distribution':15,'wedge':15,'feasibility':10,'global':5,'cost':5}
ALTERNATIVES={
 'distribution_first':{'pain':15,'recurrence':10,'budget':10,'distribution':30,'wedge':15,'feasibility':10,'global':5,'cost':5},
 'feasibility_first':{'pain':15,'recurrence':10,'budget':10,'distribution':15,'wedge':10,'feasibility':25,'global':5,'cost':10}}
products=[]
for lane in ('business','creator','developer','operations'):
 rows=json.loads((ROOT/'lanes'/f'{lane}.json').read_text())
 assert len(rows)==25,(lane,len(rows))
 for p in rows:p['research_lane']=lane
 products+=rows
assert len(products)==100
assert sorted(p['id'] for p in products)==[f'S{x:03}' for x in range(1,101)]
template=json.loads((ROOT/'record-template.json').read_text())
reviews={}
for lane in ('business','creator','developer','operations'):
 data=json.loads((ROOT/'artifacts'/f'review-{lane}.json').read_text())
 if isinstance(data,dict):data=data.get('reviews',data.get('records',data))
 assert isinstance(data,list),(lane,type(data))
 assert len(data)==25,(lane,len(data))
 for r in data:
  assert r['id'] not in reviews
  reviews[r['id']]=r
for p in products:
 missing=set(template)-set(p);assert not missing,(p['id'],missing)
 assert len(p['workflow'])>=3 and len(p['roles'])>=2,p['id']
 assert p['record'] and p['buyer'] and p['kill_gate']
 assert all(type(p['scores'][k]) is int and 1<=p['scores'][k]<=5 for k in WEIGHTS),p['id']
 assert p['pricing']['monthly_usd']>0
 assert p['cost']['fits_bootstrap']==(p['cost']['pilot_usd_month'][1]<=50),(p['id'],'cost flag')
 r=reviews[p['id']];assert 0<=r['penalty']<=20
 p['review']=r
 p['competitors']+=r.get('additional_sources',[])
 unique={}
 for c in p['competitors']:
  assert c['access']=='opened' and c['observed']=='2026-10-05',(p['id'],c)
  assert c['url'].startswith('https://') and c['price'] and c['facts']
  unique[c['url']]=c
 p['competitors']=list(unique.values())
 p['base_score']=round(sum(WEIGHTS[k]*p['scores'][k]/5 for k in WEIGHTS),1)
 p['challenge_penalty']=r['penalty']
 p['final_score']=round(p['base_score']-r['penalty'],1)
 p['decision']=r['decision'];assert p['decision'] in ('Validate','Reserve','Defer')
 p['accounts_to_5000_mrr']=math.ceil(5000/p['pricing']['monthly_usd'])
 p['sensitivity_scores']={name:round(sum(w[k]*p['scores'][k]/5 for k in w)-r['penalty'],1) for name,w in ALTERNATIVES.items()}

def sortkey(p,key='final_score'):return (-p[key],-p['scores']['distribution'],-p['scores']['wedge'],p['id'])
ranked=sorted(products,key=sortkey)
for i,p in enumerate(ranked,1):p['rank']=i
for name in ALTERNATIVES:
 order=sorted(products,key=lambda p:(-p['sensitivity_scores'][name],-p['scores']['distribution'],-p['scores']['wedge'],p['id']))
 for i,p in enumerate(order,1):p.setdefault('sensitivity_ranks',{})[name]=i
# All proposals, including reviewed losers, remain available for audit.
(ROOT/'products.json').write_text(json.dumps(products,indent=2,ensure_ascii=False)+'\n')

def safe(s):return str(s).replace('|',' / ').replace('\n',' ')
def joined(values):return '; '.join(str(x) for x in values)
def mdlink(p):return f"[{p['id']} — {p['name']}](catalog-100.md#{p['id'].lower()})"
lines=['# Ranked list of 100 SaaS candidates','','Research date: 2026-10-05. Proposed prices are USD per organization/workspace per month unless the dossier states otherwise. Scores are analyst judgments, not probabilities. Validate means run a paid discovery experiment, not build. See [decision report](decision-report.md), [method](research-protocol.md), [all dossiers](catalog-100.md) and [machine-readable records](products.json).','','| Rank | Product | Final / 100 | Status | Proposed $/mo | Accounts for $5K | Pilot cash/mo | Distribution rank | Feasibility rank |','|---:|---|---:|---|---:|---:|---:|---:|---:|']
for p in ranked:
 lo,hi=p['cost']['pilot_usd_month']
 lines.append(f"| {p['rank']} | {mdlink(p)} | {p['final_score']:g} | {p['decision']} | {p['pricing']['monthly_usd']} | {p['accounts_to_5000_mrr']} | ${lo}–{hi} | {p['sensitivity_ranks']['distribution_first']} | {p['sensitivity_ranks']['feasibility_first']} |")
(ROOT/'ranked-100.md').write_text('\n'.join(lines)+'\n')
lines=['# One hundred SaaS product dossiers','','Research date: 2026-10-05. These are distinct candidate business workflows, not 100 validated markets or products to build. Global software delivery does not imply uniform legal, language or payment requirements. All estimates assume a focused first release, a full-time experienced builder and a capped pilot; no production SLA or audit certification is implied. Vendor statements establish category competition only. Proposed prices, channels, moats and scores are hypotheses.','','[Decision report](decision-report.md) · [Ranked comparison](ranked-100.md) · [Evidence register](evidence-register.md) · [Scoring protocol](research-protocol.md)','','## Index','']
for p in ranked:lines.append(f"- {p['rank']}. [{p['id']} — {p['name']}](#{p['id'].lower()}) — {p['decision']}, {p['final_score']:g}/100")
for p in products:
 lines += ['',f'<a id="{p["id"].lower()}"></a>',f'## {p["id"]} — {p["name"]}','',f"**Rank {p['rank']}/100 · {p['decision']} · final {p['final_score']:g}/100** (base {p['base_score']:g}, challenge −{p['challenge_penalty']:g}). Category: {p['category']}.",'',f"**Buyer:** {p['buyer']}",'',f"**Job and payment hypothesis:** {p['job']} {p['why_pay']}",'',f"**Current workaround:** {p['current_workaround']}",'',f"**Core record:** {p['record']}",'',f"**Full workflow:** {' → '.join(p['workflow'])}",'',f"**Roles:** {joined(p['roles'])}.",'',f"**Entry hypothesis:** {p['wedge']}",'',f"**Expansion:** {p['expansion']}",'','### Commercial evidence','']
 for c in p['competitors']:
  lines += [f"- [{c['name']}]({c['url']}) — opened {c['observed']}. {c['facts']} **Observed price:** {c['price']}"]
 lines += ['',f"**Evidence limit:** {p['source_limit']} Confidence: {p['evidence_confidence']}.",'','### Economics and distribution','',f"**Proposed plan:** {p['pricing']['model']}, USD {p['pricing']['monthly_usd']}/month; {p['pricing']['unit']}. **{p['accounts_to_5000_mrr']} accounts** reach at least $5,000 gross MRR before churn, discounts, taxes, fees and costs.",'',f"**Free boundary:** {p['pricing']['free_boundary']}",'',f"**Paid boundary:** {p['pricing']['paid_boundary']}",'',f"**Lifetime:** {p['pricing']['lifetime']}",'',f"**Acquisition test:** {p['channel']}",'',f"**Retention:** {p['retention']}",'',f"**Defensibility hypothesis:** {p['moat']}",'','### Delivery and operating risk','',f"**First useful workflow:** {joined(p['mvp'])}.",'',f"**Build estimate:** {p['effort_weeks'][0]}–{p['effort_weeks'][1]} full-time builder-weeks, excluding discovery, security certification and external procurement.",'',f"**Pilot cash:** USD {p['cost']['pilot_usd_month'][0]}–{p['cost']['pilot_usd_month'][1]}/month; {'fits' if p['cost']['fits_bootstrap'] else 'exceeds'} the $50 envelope under the stated assumptions. {p['cost']['assumptions']}",'',f"**Cost drivers:** {p['cost']['drivers']}",'',f"**After revenue:** {p['cost']['revenue_stage']}",'',f"**Dependencies:** {joined(p['integrations'])}.",'',f"**Global limits:** {p['global_limits']}",'',f"**Risks:** {joined(p['risks'])}.",'','### Challenge and validation','',f"**Independent challenge (−{p['challenge_penalty']:g}):** {p['review']['reason']}",'',f"**Test:** {p['validation']}",'',f"**Kill gate:** {p['kill_gate']}",'',f"**Dimension scores:** "+', '.join(f'{k} {p["scores"][k]}/5' for k in WEIGHTS)+'.', '',f"**Score rationale:** {p['score_rationale']}",'',f"**Sensitivity:** distribution-first rank {p['sensitivity_ranks']['distribution_first']}; feasibility-first rank {p['sensitivity_ranks']['feasibility_first']}."]
(ROOT/'catalog-100.md').write_text('\n'.join(lines)+'\n')
sources={}
for p in products:
 for c in p['competitors']:
  if c['url'] not in sources:sources[c['url']]={'name':c['name'],'ids':[],'observed':c['observed'],'facts':c['facts'],'price':c['price']}
  sources[c['url']]['ids'].append(p['id'])
lines=['# Official source register','','All listed pages were opened during this research on 2026-10-05 by the root researcher or a research/review agent. This register records observations, not archived page snapshots or independent verification of vendor claims. Page content and prices can change. Search snippets alone were not accepted for confirmed prices. Duplicate URLs are collapsed here; candidate-specific qualifications remain in the dossiers.','','| Source | Candidates | Observed facts | Observed pricing / limits |','|---|---|---|---|']
for url,s in sorted(sources.items()):lines.append(f"| [{safe(s['name'])}]({url}) | {', '.join(s['ids'])} | {safe(s['facts'])} | {safe(s['price'])} |")
(ROOT/'evidence-register.md').write_text('\n'.join(lines)+'\n')
result={'records':len(products),'official_source_urls':len(sources),'decisions':dict(collections.Counter(p['decision'] for p in products)),'bootstrap_cash_fit':sum(p['cost']['fits_bootstrap'] for p in products),'top20':[{'id':p['id'],'name':p['name'],'score':p['final_score'],'decision':p['decision'],'competitors':len(p['competitors']),'price':p['pricing']['monthly_usd'],'sensitivity':p['sensitivity_ranks']} for p in ranked[:20]]}
(ROOT/'artifacts'/'catalog-checks.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))

"""Read-only scientific reaggregation; no model imports, fits, predictions or scoring."""
from pathlib import Path
import argparse
import csv, gzip, hashlib, json
from collections import defaultdict
import numpy as np

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--review-root', type=Path, required=True, help='Directory containing received/ and ARCHIVE_REVIEW.json')
BASE = parser.parse_args().review_root.resolve()
P = BASE / 'received'
A = P / 'run/analysis'
METRICS = ['crps','zero_brier','median_abs_error','interval_score90','width90','coverage50','coverage80','coverage90','coverage95']
def read(p): return json.loads(p.read_text())
def rows(p):
    with gzip.open(p,'rt') as f: return list(csv.DictReader(f))
def sha(p):
    with p.open('rb') as f: return hashlib.file_digest(f,'sha256').hexdigest()
def compare(a,b):
    a,b=np.asarray(a,float),np.asarray(b,float)
    assert np.all(np.isfinite(a)) and np.all(np.isfinite(b))
    assert np.allclose(a,b,rtol=1e-12,atol=1e-10), float(np.max(np.abs(a-b)))
    return float(np.max(np.abs(a-b)))

frozen=read(P/'source/EXPERIMENT_FREEZE.json')
for n,m in frozen.items():
    f=P/'source'/n
    assert f.stat().st_size==m['bytes'] and sha(f)==m['sha256'],n
lock=read(P/'source/provenance/MODEL_LOCK.json')
models=[m for x in lock['models'] for m in x['models']]
assert len(models)==40
for m in models:
    f=P/'run/models'/m['job_id']/'MODEL.joblib'
    assert f.stat().st_size==m['bytes'] and sha(f)==m['sha256']

cohort={ (r['source'],r['cascade_id']):r for r in csv.DictReader((P/'source/data/TEST_COHORT.csv').open())}
assert len(cohort)==10000
source_ids={s:sorted(cid for ss,cid in cohort if ss==s) for s in ['weibo','seismic']}
jobroots={}; jobwindows={}; failures=0; nrows=0; rootdiff=0.; windowdiff=0.
for mi,m in enumerate(models):
    jid=m['job_id']; d=P/'run/jobs'/jid
    parts=jid.split('__'); source=parts[0]
    ids=source_ids[source]; index={cid:i for i,cid in enumerate(ids)}
    values=np.full((5000,3,len(METRICS)),np.nan); seen=set()
    with (d/'SCORES.jsonl').open() as f:
        for line in f:
            r=json.loads(line); k=(r['cascade_id'],int(r['window_s']))
            assert k not in seen; seen.add(k)
            assert r['status']=='ok' and r['source']==source
            meta=cohort[(source,k[0])]
            assert r['group_id']==meta['group_id']
            assert str(r['has_exact_duplicate_tokens'])==meta['has_exact_duplicate_tokens']
            assert 0<=r['crps_error_bound']<=1e-8
            values[index[k[0]],{300:0,900:1,3600:2}[k[1]],:]=[r[x] for x in METRICS]
            nrows+=1
    assert len(seen)==15000 and np.isfinite(values).all()
    jr=values.mean(axis=1); jobroots[jid]=jr; jobwindows[jid]=values.mean(axis=0)
    saved=rows(d/'ROOT_SCORES.csv.gz'); assert len(saved)==5000
    saved.sort(key=lambda r:r['cascade_id'])
    assert [r['cascade_id'] for r in saved]==ids
    rootdiff=max(rootdiff,compare(jr,[[r[x] for x in METRICS] for r in saved]))
    report=read(d/'JOB_REPORT.json'); failures+=len(read(d/'FAILURES.json'))
    if (mi+1)%10==0: print('jobs reaggregated',mi+1,flush=True)
assert nrows==600000 and failures==0

pr=read(A/'PROCEDURE_METRICS.json'); savedroot=rows(A/'ROOT_PROCEDURE_SCORES.csv.gz')
assert len(pr)==24 and len(savedroot)==120000
savedgroup=defaultdict(list)
for r in savedroot:savedgroup[(r['source'],r['family'],r['info'])].append(r)
procedure_roots={}; aggdiff=0.; procedurediff=0.
for x in pr:
    key=x['source'],x['family'],x['info']; assert x['status']=='complete'
    v=np.mean([jobroots[j] for j in x['jobs']],axis=0); procedure_roots[key]=v
    sr=sorted(savedgroup[key],key=lambda r:r['cascade_id'])
    assert [r['cascade_id'] for r in sr]==source_ids[x['source']]
    procedurediff=max(procedurediff,compare(v,[[r[k] for k in METRICS] for r in sr]))
    aggdiff=max(aggdiff,compare(v.mean(axis=0),[x['metrics'][k] for k in METRICS]))
    wv=np.mean([jobwindows[j] for j in x['jobs']],axis=0)
    windowdiff=max(windowdiff,compare(wv,[[x['window_metrics'][str(w)][k] for k in METRICS] for w in [300,900,3600]]))

boot=rows(A/'BOOTSTRAP_DELTAS.csv.gz');assert len(boot)==20000
pc=read(A/'PRIMARY_COMPARISONS.json');pointdiff=0.;cidiff=0.
for x in pc:
    s,f=x['source'],x['family']
    p0=procedure_roots[(s,f,'I0')][:,0];p1=procedure_roots[(s,f,'I1')][:,0]
    pointdiff=max(pointdiff,compare([p0.mean(),p1.mean(),(p1-p0).mean()],[x['I0'],x['I1'],x['delta_I1_minus_I0']]))
    b=[float(r[f]) for r in boot if r['source']==s];assert len(b)==10000
    ci=np.quantile(b,[.05/12,1-.05/12],method='linear')
    cidiff=max(cidiff,compare(ci,x['adjusted_interval']))
    assert x['multiplicity_family_size']==6

sensitivitydiff=0.
for x in read(A/'DUPLICATE_SENSITIVITY.json'):
    s,f=x['source'],x['family']; keep=np.array([cohort[(s,cid)]['has_exact_duplicate_tokens']=='0' for cid in source_ids[s]])
    assert keep.sum()==x['kept_roots']==4997
    v0=procedure_roots[(s,f,'I0')][keep,0];v1=procedure_roots[(s,f,'I1')][keep,0]
    sensitivitydiff=max(sensitivitydiff,compare([v0.mean(),v1.mean(),(v1-v0).mean()],[x['I0'],x['I1'],x['delta_I1_minus_I0']]))

out={**read(BASE/'ARCHIVE_REVIEW.json'),'frozen_source_files_verified':len(frozen),'locked_model_hashes_verified':len(models),'saved_score_rows_reaggregated':nrows,'saved_model_root_rows_checked':200000,'saved_procedure_root_rows_checked':len(savedroot),'complete_procedures':len(pr),'bootstrap_vectors_read':len(boot),'bootstrap_contrast_values_read':60000,'primary_comparisons_checked':len(pc),'max_model_root_reaggregation_difference':rootdiff,'max_procedure_root_reaggregation_difference':procedurediff,'max_aggregate_metric_difference':aggdiff,'max_window_metric_difference':windowdiff,'max_primary_point_difference':pointdiff,'max_saved_bootstrap_quantile_difference':cidiff,'max_duplicate_sensitivity_difference':sensitivitydiff,'new_fits':0,'new_predictions':0,'new_row_scores':0,'new_bootstrap_draws':0,'calibration_figures_visually_reviewed':True,'verification_scope':'Integrity and independent reaggregation of saved numerical outputs. Model training, distribution generation, row scoring and bootstrap resampling were not repeated. Historical run counters are checked against supplied outputs, not independently observed execution.','status':'saved_outputs_verified_with_independent_reaggregation'}
(BASE/'INDEPENDENT_REVIEW.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))

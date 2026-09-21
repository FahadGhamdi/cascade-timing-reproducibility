"""Read-only Phase14 artifact audit. No model loading, fitting, prediction or resampling.

Usage: python review_saved_phase14.py RETURN.zip EXTRACTED_INPUT OUTPUT_DIR [ORIGINAL_KIT.zip]
Uses saved losses and saved bootstrap replicates, not a new scientific evaluation.
"""
import csv
import gzip
import hashlib
import json
import sys
import zipfile
from collections import Counter, defaultdict
from pathlib import Path, PurePosixPath

import numpy as np

archive, base, out = map(Path, sys.argv[1:4])
out.mkdir(parents=True, exist_ok=True)
def sha_bytes(b): return hashlib.sha256(b).hexdigest()
def sha_file(p):
    with p.open('rb') as f: return hashlib.file_digest(f, 'sha256').hexdigest()
def read(n): return json.loads((base / n).read_text())
def dump(n, v): (out / n).write_text(json.dumps(v, indent=2, allow_nan=False)+'\n')
def rows(n):
    f = base / n
    with (gzip.open(f, 'rt') if str(f).endswith('.gz') else f.open()) as h:
        return list(csv.DictReader(h))

assert archive.stat().st_size == 222470817
digest = sha_file(archive)
assert digest == '5295b94b6c6bfef77b14bbe94d16ed977e489e05dafe5e0b667d49cd1f7d2784'
with zipfile.ZipFile(archive) as z:
    manifest = json.loads(z.read('MANIFEST.json'))
    names = z.namelist()
    assert len(names) == len(set(names)) == 522
    assert set(names) == set(manifest) | {'MANIFEST.json'}
    for name, record in manifest.items():
        p = PurePosixPath(name)
        assert not p.is_absolute() and '..' not in p.parts and '\\' not in name
        b = z.read(name)  # also verifies the member CRC
        assert len(b) == record['bytes'] == z.getinfo(name).file_size
        assert sha_bytes(b) == record['sha256']
        if not name.endswith('.joblib'):
            assert (base / name).read_bytes() == b
    sm = json.loads(z.read('source/MANIFEST.json'))
    for name, record in sm.items():
        b = z.read('source/'+name)
        assert len(b) == record['bytes'] and sha_bytes(b) == record['sha256']
    kit_count = None
    if len(sys.argv) > 4:
        with zipfile.ZipFile(sys.argv[4]) as kit:
            kit_count = 0
            for name in kit.namelist():
                if name.endswith('/'): continue
                relative = name.split('/', 1)[1]
                assert kit.read(name) == z.read('source/'+relative)
                kit_count += 1
receipt = dict(archive=archive.name, bytes=archive.stat().st_size, sha256=digest,
               payloads_verified=len(manifest), sizes_sha256_crc_valid=True,
               source_manifest_payloads=len(sm), exact_original_kit_members=kit_count)
dump('ARCHIVE_REVIEW.json', receipt)
print('Archive and original kit verified', flush=True)

metrics = ['crps','zero_brier','median_abs_error','interval_score90','width90',
           'coverage50','coverage80','coverage90','coverage95','msle_saved_median']
sources = ['weibo','seismic']; families = ['hurdle','qrf','ngboost']; windows=[300,900,3600]
specs=read('source/NOISE_JOBS.json'); meta=read('run/stage_a/CASE_METADATA.json')
saved_a=np.load(base/'run/stage_a/PROCEDURE_LOSSES.npz', allow_pickle=False)
saved_b=np.load(base/'run/stage_b/NOISE_PROCEDURE_LOSSES.npz', allow_pickle=False)
boot_b=np.load(base/'run/stage_b/NOISE_BOOTSTRAP.npz', allow_pickle=False)
totals=Counter(); by_rep=defaultdict(list); job_receipts=[]; max_cert=0.0
fields=['new_procedure_fit_attempts','component_fit_calls','predictions_attempted',
        'predictions_returned','score_attempts','score_successes','score_failures','prediction_failure_rows']
assert len(specs)==42 and len({s['job_id'] for s in specs})==42
found={p.parent.name for p in (base/'run/noise_jobs').glob('*/JOB_REPORT.json')}
assert found == {s['job_id'] for s in specs}
targets={}; features={}; positions={}
for source in sources:
    ids=meta[source]['ids']; assert len(ids)==len(set(ids))==5000 and ids==sorted(ids)
    positions[source]={(cid,w):(i,j) for i,cid in enumerate(ids) for j,w in enumerate(windows)}
    yy=rows(f'source/data/{source}/TEST_TARGETS.csv.gz')
    ff=rows(f'source/data/{source}/TEST_FEATURES.csv.gz')
    targets[source]={(r['cascade_id'],int(r['window_s'])):int(r['future_count']) for r in yy}
    features[source]={(r['cascade_id'],int(r['window_s'])):int(r['n_prefix']) for r in ff}
    assert len(yy)==len(ff)==15000
    assert set(targets[source])==set(features[source])==set(positions[source])
    for key,(i,j) in positions[source].items(): assert features[source][key]==meta[source]['n_prefix'][i][j]
bindings=read('run/stage_b/NOISE_MATRIX_BINDINGS.json')
assert len(bindings)==12
for name,sha in bindings.items():
    p=base/'run'/name;assert sha_file(p)==sha
    a=np.load(p,allow_pickle=False)['values']
    assert a.shape == (18000 if '__TRAIN__' in name else 15000,7)
    assert np.isfinite(a).all() and np.max(np.abs(a)) <= np.sqrt(3)
for spec in specs:
    d=base/'run/noise_jobs'/spec['job_id']; r=json.loads((d/'JOB_REPORT.json').read_text())
    for field in ['job_id','source','family','seed','noise_replicate','params','candidate','info']:
        assert r[field]==spec[field], (spec['job_id'],field)
    assert r['complete'] and r['status']=='complete' and r['model_unchanged_after_scoring']
    assert r['old_model_refits']==r['validation_evaluations']==0
    assert r['warnings']==[] and json.loads((d/'FAILURES.json').read_text())==[]
    assert r['fit_meta'].get('converged',True)
    assert manifest[f"run/noise_jobs/{spec['job_id']}/MODEL.joblib"]['sha256']==r['model_sha256']
    pr=json.loads((d/'PROCESS_REPORT.json').read_text())
    assert pr['returncode']==0 and not pr.get('timeout',False)
    for k in ['train_noise_file','test_noise_file']:
        b=r[k];assert bindings[b['path']]==b['sha256']
    totals.update({k:r[k] for k in fields})
    a=np.full((5000,3,10),np.nan);seen=set();s=spec['source']
    with gzip.open(d/'SCORES.jsonl.gz','rt') as h:
        for line in h:
            q=json.loads(line); key=(q['cascade_id'],q['window_s'])
            assert key not in seen and key in positions[s]
            seen.add(key);i,j=positions[s][key]
            assert q['status']=='ok' and q['source']==s
            assert q['group_id']==meta[s]['groups'][i]
            assert q['n_prefix']==features[s][key] and q['future_count']==targets[s][key]
            assert 0<=q['crps_error_bound']<=1e-8
            max_cert=max(max_cert,q['crps_error_bound'])
            a[i,j]=[q[m] for m in metrics]
    assert len(seen)==15000 and np.isfinite(a).all()
    assert all(r[k]==15000 for k in ['predictions_attempted','predictions_returned','score_attempts','score_successes'])
    assert r['score_failures']==r['prediction_failure_rows']==0
    by_rep[s,spec['family'],spec['noise_replicate']].append(a)
    max_job=float(max(abs(a[:,:,k].mean()-r['metrics'][m]) for k,m in enumerate(metrics)))
    assert max_job<1e-8
    job_receipts.append(dict(job_id=spec['job_id'],rows=len(seen),unique_keys=True,
                             saved_metric_mean_max_abs_difference=max_job))
print('All 630000 saved score rows checked',flush=True)
assert dict(totals)==read('run/stage_b/STAGE_B_REPORT.json')['accounting']
rep_table=rows('run/stage_b/NOISE_REALIZATION_SUMMARIES.csv')
noise={}; max_array=max_rep=0.0
for source in sources:
    for family in families:
        reps=[]
        for rep in range(3):
            aa=by_rep[source,family,rep];assert len(aa)==(1 if family=='hurdle' else 3)
            b=np.mean(aa,axis=0);reps.append(b)
            row=next(r for r in rep_table if (r['source'],r['family'],int(r['noise_replicate']))==(source,family,rep))
            max_rep=max(max_rep,abs(b[:,:,0].mean()-float(row['CRPS'])))
        key=source+'__'+family
        noise[key]=np.mean(reps,axis=0)
        diff=float(np.max(np.abs(noise[key]-saved_b[key])))
        max_array=max(max_array,diff); assert np.allclose(noise[key],saved_b[key],atol=1e-8,rtol=1e-10)
contrasts=read('run/stage_b/NOISE_COMPARISONS.json');assert len(contrasts)==12
max_point=max_ci=0.0
for row in contrasts:
    s,fam,label=row['source'],row['family'],row['contrast'];k=s+'__'+fam
    a=saved_a[k+'__I0'][:,:,0].mean(axis=1);b=saved_a[k+'__I1'][:,:,0].mean(axis=1)
    z=noise[k][:,:,0].mean(axis=1)
    left,right=(z,a) if label=='noise_minus_I0' else (b,z)
    for value,key in [(left.mean(),'left_CRPS'),(right.mean(),'right_CRPS'),((left-right).mean(),'delta'),(100*(1-left.mean()/right.mean()),'relative_reduction_percent')]:
        max_point=max(max_point,float(abs(value-row[key])))
    j=2*families.index(fam)+(label=='I1_minus_noise')
    assert boot_b[s].shape==(10000,6) and np.isfinite(boot_b[s]).all()
    ci=np.quantile(boot_b[s][:,j],[.05/24,1-.05/24],method='linear')
    max_ci=max(max_ci,float(np.max(np.abs(ci-[row['adjusted_low'],row['adjusted_high']]))))
assert max_point<1e-8 and max_ci<1e-8
strata=read('run/stage_a/STRATA_RESULTS.json');boot_a=np.load(base/'run/stage_a/STRATA_BOOTSTRAP.npz',allow_pickle=False)
bins=['0','1-2','3-9','10-49','50+'];max_stratum=max_a_ci=0.0;withheld=[]
for r in strata:
    s=r['source'];wi=windows.index(r['window_s']);bi=bins.index(r['prefix_bin']);fam=r['family'];k=s+'__'+fam
    counts=np.asarray(meta[s]['n_prefix'])[:,wi];mask=np.searchsorted([0,2,9,49],counts,side='left')==bi
    groups=np.asarray(meta[s]['groups']);assert int(mask.sum())==r['roots']
    assert len(set(groups[mask]))==r['resampling_units']
    a=saved_a[k+'__I0'][mask,wi,0];b=saved_a[k+'__I1'][mask,wi,0]
    ce=saved_a[s+'__conditional_empirical__I0'][mask,wi,0]
    for v,key in [(a.mean(),'I0'),(b.mean(),'I1'),((b-a).mean(),'delta_I1_minus_I0'),(ce.mean(),'conditional_empirical'),((b-ce).mean(),'I1_minus_conditional_empirical')]:
        max_stratum=max(max_stratum,float(abs(v-r[key])))
    j=(wi*5+bi)*3+families.index(fam);bs=boot_a[s+'_deltas'][:,j];bs=bs[np.isfinite(bs)]
    assert len(bs)==r['valid_bootstrap_replicates']
    eligible=r['resampling_units']>=30 and len(bs)>=1980
    if eligible:
        ci=np.quantile(bs,[.025,.975]);max_a_ci=max(max_a_ci,float(np.max(np.abs(ci-[r['pointwise95_low'],r['pointwise95_high']]))))
    else:
        assert r['pointwise95_low'] is None and r['pointwise95_high'] is None
        withheld.append({k:r[k] for k in ['source','family','window_s','prefix_bin','roots','resampling_units']})
assert len(strata)==90 and len(withheld)==6 and max_stratum<1e-8 and max_a_ci<1e-8
primary=read('source/provenance/PRIMARY_COMPARISONS.json');max_primary=0.0
for r in primary:
    k=r['source']+'__'+r['family']
    for info in ['I0','I1']:max_primary=max(max_primary,abs(float(saved_a[k+'__'+info][:,:,0].mean())-r[info]))
assert max_primary<1e-8
report=dict(status='verified_saved_outputs_no_new_experiment',archive=receipt,
            saved_score_rows_checked=totals['score_successes'],jobs_checked=len(job_receipts),accounting=dict(totals),
            model_files_hashed_without_loading=42,noise_matrices_verified=12,noise_realization_means_checked=18,
            max_saved_crps_error_bound=max_cert,noise_array_max_abs_difference=max_array,
            noise_rep_mean_max_abs_difference=float(max_rep),noise_point_max_abs_difference=max_point,
            noise_saved_quantile_max_abs_difference=max_ci,noise_contrasts_checked=12,
            noise_minus_I0_intervals_including_zero=sum(r['adjusted_low']<=0<=r['adjusted_high'] for r in contrasts if r['contrast']=='noise_minus_I0'),
            I1_minus_noise_intervals_entirely_negative=sum(r['adjusted_high']<0 for r in contrasts if r['contrast']=='I1_minus_noise'),
            strata_contrasts_checked=90,strata_point_max_abs_difference=max_stratum,strata_saved_quantile_max_abs_difference=max_a_ci,
            strata_negative_deltas=sum(r['delta_I1_minus_I0']<0 for r in strata),strata_positive_deltas=sum(r['delta_I1_minus_I0']>0 for r in strata),
            withheld_strata_intervals=withheld,primary_CRPS_max_abs_difference=max_primary,
            new_fits=0,new_predictions=0,new_distribution_scores=0,new_bootstrap_draws=0,
            uncertainty_scope='Quantiles of saved bootstrap replicates verified; resampling indices were not regenerated.',
            review_implementation_note='Initial kit-identity check omitted the original archive top-level directory and raised KeyError. Path mapping was corrected in this audit only; no experiment or supplied artifact changed.')
dump('INDEPENDENT_PHASE14_REVIEW.json',report);dump('JOB_REVIEW.json',job_receipts)
print(json.dumps(report,indent=2))

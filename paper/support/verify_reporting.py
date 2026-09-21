"""Audit frozen evidence and selected published tables; no fits, predictions or resampling.
Run from any directory. Writes audit/REPORTING_CHECKS.json.
"""
from pathlib import Path
import json,hashlib,re,math
P=Path(__file__).resolve().parent.parent
checks=[]
def check(name,condition,detail=None):
 checks.append(dict(check=name,passed=bool(condition),detail=detail))
def load(n):return json.loads((P/'support/evidence'/n).read_text())
def norm(s):return re.sub(r'\s+','',s).replace('{[}','[').replace('{]}',']')
original=P/'source/initial_reviewed'
for folder in ['evidence','tables','protocols']:
 for f in (original/folder).rglob('*'):
  if f.is_file():
   new=P/'support'/f.relative_to(original)
   check('frozen:'+str(f.relative_to(original)),new.is_file() and f.read_bytes()==new.read_bytes())
primary=load('PRIMARY_COMPARISONS.json');proc=load('PROCEDURE_METRICS.json');noise=load('phase14/NOISE_COMPARISONS.json');strata=load('phase14/STRATA_RESULTS.json')
names={'hurdle':'Hurdle','qrf':'QRF','ngboost':'NGBoost','empirical_window':'Empirical by window','conditional_empirical':'Conditional empirical','poisson_glm':'Poisson GLM','nb2_glm':'NB2 GLM'}
sname=lambda s:'Weibo' if s=='weibo' else 'SEISMIC'
def get(s,f,i):return next(d for d in proc if (d['source'],d['family'],d['info'])==(s,f,i))
txt=norm((P/'tables/primary.tex').read_text())
for d in primary:
 vals=[sname(d['source']),names[d['family']],f"{d['I0']:.3f}",f"{d['I1']:.3f}",f"{d['delta_I1_minus_I0']:.3f}",f"[{d['adjusted_interval'][0]:.3f}, {d['adjusted_interval'][1]:.3f}]",f"{100*d['relative_reduction']:.2f}\\%"]
 check('primary_table:'+d['source']+'/'+d['family'],norm(' & '.join(vals)) in txt)
 check('primary_aggregate_binding:'+d['source']+'/'+d['family'],all(math.isclose(d[i],get(d['source'],d['family'],i)['metrics']['crps'],rel_tol=1e-12) for i in ['I0','I1']))
check('six_primary_intervals_below_zero',len(primary)==6 and all(d['adjusted_interval'][1]<0 for d in primary))
check('eighteen_window_directions',all(get(s,f,'I1')['window_metrics'][str(w)]['crps']<get(s,f,'I0')['window_metrics'][str(w)]['crps'] for s in ['weibo','seismic'] for f in ['hurdle','qrf','ngboost'] for w in [300,900,3600]))
txt=norm((P/'tables/noise.tex').read_text())
for d in noise:
 token=f"{d['delta']:+.3f} [{d['adjusted_low']:+.3f}, {d['adjusted_high']:+.3f}]"
 row=next((r for r in txt.split('\\\\') if norm(sname(d['source'])+'&'+names[d['family']]+'&') in r),'')
 check('noise_table:'+d['source']+'/'+d['family']+'/'+d['contrast'],norm(token) in row)
check('six_noise_I0_intervals_span_zero',sum(d['contrast']=='noise_minus_I0' and d['adjusted_low']<0<d['adjusted_high'] for d in noise)==6)
check('six_I1_noise_intervals_below_zero',sum(d['contrast']=='I1_minus_noise' and d['adjusted_high']<0 for d in noise)==6)
core=norm((P/'sections/supplement_core.tex').read_text())
for d in proc:
 m=d['metrics'];vals=[sname(d['source']),names[d['family']],d['info'],f"{m['crps']:.3f}",f"{m['zero_brier']:.6f}",f"{m['median_abs_error']:.3f}",f"{100*m['coverage90']:.2f}\\%",f"{m['width90']:.3f}",f"{m['interval_score90']:.3f}"]
 check('supplement_aggregate_row:'+d['source']+'/'+d['family']+'/'+d['info'],norm('&'.join(vals)) in core)
check('strata_counts',len(strata)==90 and sum(d['delta_I1_minus_I0']<0 for d in strata)==64 and sum(d['delta_I1_minus_I0']>0 for d in strata)==26)
st=(P/'sections/supplement_strata.tex').read_text()
for d in strata:
 section=st.split('\\subsection{'+sname(d['source'])+':')[1].split('\\subsection')[0]
 ci=f"[{d['pointwise95_low']:.3f}, {d['pointwise95_high']:.3f}]" if d['interval_status']=='exploratory_pointwise' else 'withheld'
 vals=[names[d['family']],str(d['window_s']//60),d['prefix_bin'],str(d['roots']),str(d['resampling_units']),f"{d['I0']:.3f}",f"{d['I1']:.3f}",f"{d['delta_I1_minus_I0']:.3f}",ci]
 check('strata_row:'+str((d['source'],d['family'],d['window_s'],d['prefix_bin'])),norm('&'.join(vals)) in norm(section))
check('six_withheld_strata',sum(d['interval_status']!='exploratory_pointwise' for d in strata)==6)
v=get('weibo','ngboost','I0')['window_metrics']['3600']['crps'];check('rounding_89.374',f'{v:.3f}'=='89.374' and '89.374' in core,{'unrounded':v})
cal=load('CALIBRATION.json'); primarycal=[d for d in cal if d['family'] in ['hurdle','qrf','ngboost']]
aggmax=max(max(d['calibration']['0']['nonrandomized_pit_mass']) for d in primarycal)
windowmax=max(max(d['calibration'][str(w)][k]) for d in primarycal for w in [300,900,3600] for k in ['nonrandomized_pit_mass','randomized_pit_frequency'])
check('plot_axes_do_not_truncate_PIT',aggmax<.34 and windowmax<.5,{'aggregate_max':aggmax,'window_max':windowmax})
check('strata_color_scale_not_saturated',max(abs(d['relative_reduction_percent']) for d in strata)<50)
lock=load('MODEL_LOCK.json');check('forty_locked_objects',sum(len(d['models']) for d in lock['models'])==40)
# Every literal support-relative artifact path in the new supplement must exist.
for path in re.findall(r'\\path\{([^}]+)\}',(P/'sections/supplement_core.tex').read_text()):
 if path.startswith(('protocols/','evidence/','tables/','code/')):check('artifact_path:'+path,(P/'support'/path).exists())
bibkeys=set(re.findall(r'@\w+\{([^,]+),',(P/'references.bib').read_text()))
for f in list((P/'sections').glob('*.tex'))+list((P/'config').glob('*.tex'))+[P/'main.tex',P/'supplementary.tex']:
 for group in re.findall(r'\\cite\{([^}]+)\}',f.read_text()):
  for key in group.split(','):check('citation:'+key,key in bibkeys)
result={'scope':'Reporting consistency against frozen aggregates; no raw-data, fit, prediction, score or bootstrap rerun','checks':checks,'passed':all(x['passed'] for x in checks),'count':len(checks),'bibliography_entries':len(bibkeys)}
(P/'audit/REPORTING_CHECKS.json').write_text(json.dumps(result,indent=2))
print(json.dumps({k:v for k,v in result.items() if k!='checks'}))
for x in checks:
 if not x['passed']:print(x)
raise SystemExit(0 if result['passed'] else 1)

"""Redraw publication figures from frozen aggregates only; no model evaluation."""
from pathlib import Path
import json, hashlib
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import TwoSlopeNorm
P=Path(__file__).resolve().parent; O=P.parent/'figures'; O.mkdir(exist_ok=True)
def load(n):return json.loads((P/'evidence'/n).read_text())
primary=load('PRIMARY_COMPARISONS.json'); proc=load('PROCEDURE_METRICS.json'); cal=load('CALIBRATION.json'); strata=load('phase14/STRATA_RESULTS.json'); noise=load('phase14/NOISE_COMPARISONS.json')
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':8,'axes.titlesize':9,'axes.labelsize':8,'xtick.labelsize':7,'ytick.labelsize':8,'axes.spines.top':False,'axes.spines.right':False,'axes.edgecolor':'#81909C','axes.linewidth':.5,'grid.color':'#DBE1E6','grid.linewidth':.5,'pdf.fonttype':42,'ps.fonttype':42,'savefig.facecolor':'white'})
colors={'I0':'#758595','I1':'#087F8C'}; family=['hurdle','qrf','ngboost']; names={'hurdle':'Hurdle','qrf':'QRF','ngboost':'NGBoost','empirical_window':'Empirical','conditional_empirical':'Conditional empirical','poisson_glm':'Poisson GLM','nb2_glm':'NB2 GLM'}
# Actual family keys are inspected rather than guessed.
print('families',sorted({x['family'] for x in proc}))
def get(s,f,i):return next(x for x in proc if x['source']==s and x['family']==f and x['info']==i)
def save(fig,n):
 fig.savefig(O/(n+'.pdf'),bbox_inches='tight',pad_inches=.06)
 fig.savefig(O/(n+'.png'),dpi=220,bbox_inches='tight',pad_inches=.06)
 plt.close(fig)
fig,axs=plt.subplots(1,2,figsize=(7.05,2.45),layout='constrained')
for ax,s in zip(axs,['weibo','seismic']):
 for y,f in enumerate(family):
  d=next(x for x in primary if x['source']==s and x['family']==f);v=d['delta_I1_minus_I0'];lo,hi=d['adjusted_interval'];ax.errorbar(v,y,xerr=[[v-lo],[hi-v]],fmt='o',color=colors['I1'],capsize=3,ms=5,lw=1.5)
  ax.annotate(f"{100*d['relative_reduction']:.2f}%",(hi,y),xytext=(5,0),textcoords='offset points',va='center',fontsize=7)
 ax.axvline(0,ls='--',c='#333333',lw=.8);ax.set(yticks=range(3),yticklabels=[names[f] for f in family],ylim=(2.6,-.6),xlabel=r'Mean CRPS difference ($I_1-I_0$)',title=s.upper() if s=='seismic' else 'Weibo');ax.grid(axis='x');a,b=ax.get_xlim();ax.set_xlim(a,max(b,(b-a)*.16));
 ax.text(.03,.04,'Lower favors timing',transform=ax.transAxes,fontsize=7,color='#345566')
save(fig,'primary_contrasts')
fig,axs=plt.subplots(1,2,figsize=(7.05,3.15),layout='constrained')
order=['empirical_window','conditional_empirical','poisson_glm','nb2_glm','hurdle','qrf','ngboost']
keys={x['family'] for x in proc}
for f in order:
 if f not in keys: raise RuntimeError('Unexpected family key '+f)
for ax,s in zip(axs,['weibo','seismic']):
 for y,f in enumerate(order):
  for off,i in [(-.12,'I0'),(.12,'I1')]:
   d=[x for x in proc if (x['source'],x['family'],x['info'])==(s,f,i)]
   if not d:continue
   v=d[0]['metrics']['crps'];ax.plot(v,y+off,'o' if i=='I1' else 's',ms=4.5,c=colors[i],label=i if y==2 else None)
   ax.text(v+1,y+off,f'{v:.1f}',fontsize=6.8,va='center',c=colors[i])
  if f in ['hurdle','qrf','ngboost','poisson_glm','nb2_glm']:
   ax.plot([get(s,f,'I0')['metrics']['crps'],get(s,f,'I1')['metrics']['crps']],[y-.12,y+.12],color='#BCC8D0',lw=.8,zorder=0)
 ax.set(yticks=range(7),yticklabels=[names[f] for f in order],ylim=(6.6,-.65),xlabel='Mean test CRPS (lower is better)',title='Weibo' if s=='weibo' else 'SEISMIC');ax.grid(axis='x');lo,hi=ax.get_xlim();ax.set_xlim(lo,hi+(hi-lo)*.14)
axs[0].legend(loc='lower right',frameon=False,fontsize=7)
save(fig,'all_procedures')
# Aggregate count PIT, source rows and family columns.
fig,axs=plt.subplots(2,3,figsize=(7.05,3.8),sharey=True,sharex=True,layout='constrained'); x=np.arange(10)/10+.05
for r,s in enumerate(['weibo','seismic']):
 for c,f in enumerate(family):
  ax=axs[r,c]
  for i in ['I0','I1']:
   d=next(z for z in cal if (z['source'],z['family'],z['info'])==(s,f,i))['calibration']['0']['nonrandomized_pit_mass'];ax.plot(x,d,'s--' if i=='I0' else 'o-',ms=3,lw=1,color=colors[i],label=i)
  ax.axhline(.1,c='#C18127',ls=':',lw=1);ax.set(title=('Weibo' if s=='weibo' else 'SEISMIC')+' | '+names[f],ylim=(0,.34),xticks=[0,.5,1]);ax.grid(axis='y')
  if c==0:ax.set_ylabel('PIT-bin mass')
  if r==1:ax.set_xlabel('Count PIT')
axs[0,0].legend(frameon=False,fontsize=7)
save(fig,'calibration_overview')
# All 90 exploratory slots; positive percentages mean an improvement.
fig,axs=plt.subplots(2,3,figsize=(7.05,3.6),layout='constrained');bins=['0','1-2','3-9','10-49','50+'];actual=sorted({x['prefix_bin'] for x in strata});print('bins',actual)
# Preserve labels from protocol.
bins=[next(b for b in actual if b=='0'), next(b for b in actual if '1' in b and '2' in b), next(b for b in actual if '3' in b and '9' in b),next(b for b in actual if '10' in b),next(b for b in actual if '50' in b)]
for r,s in enumerate(['weibo','seismic']):
 for c,f in enumerate(family):
  ax=axs[r,c];a=np.zeros((3,5));ds=[]
  for row,w in enumerate([300,900,3600]):
   for col,b in enumerate(bins):
    d=next(z for z in strata if (z['source'],z['family'],z['window_s'],z['prefix_bin'])==(s,f,w,b));a[row,col]=d['relative_reduction_percent'];ds.append((row,col,d))
  im=ax.imshow(a,cmap='BrBG',norm=TwoSlopeNorm(vmin=-50,vcenter=0,vmax=50),aspect='auto')
  for row,col,d in ds:
   star='*' if d['interval_status']!='exploratory_pointwise' else '';v=a[row,col];ax.text(col,row,(('0.0' if abs(v)<.05 else f'{v:.1f}')+star),ha='center',va='center',fontsize=6.6,color='white' if abs(v)>32 else '#142D33')
  ax.set(xticks=range(5),xticklabels=['0','1–2','3–9','10–49','≥50'],yticks=range(3),yticklabels=['5','15','60'],title=('Weibo' if s=='weibo' else 'SEISMIC')+' | '+names[f]);ax.tick_params(length=0)
  if c==0:ax.set_ylabel('Prefix (min)')
  if r==1:ax.set_xlabel('Recorded prefix events')
cb=fig.colorbar(im,ax=axs,shrink=.85,pad=.018);cb.set_label('CRPS reduction (%)',fontsize=8)
save(fig,'timing_strata')
# Both planned supplementary contrast types, all source/family pairs.
fig,axs=plt.subplots(1,2,figsize=(7.05,3.35),sharey=True,layout='constrained');pairs=[(s,f) for s in ['weibo','seismic'] for f in family]
for ax,ct,ttl in zip(axs,['noise_minus_I0','I1_minus_noise'],[r'Noise $-\ I_0$',r'$I_1\ -$ noise']):
 for y,(s,f) in enumerate(pairs):
  d=next(z for z in noise if (z['source'],z['family'],z['contrast'])==(s,f,ct));v=d['delta'];color=colors['I1'] if ct=='I1_minus_noise' else '#7C5C95';ax.errorbar(v,y,xerr=[[v-d['adjusted_low']],[d['adjusted_high']-v]],fmt='o',ms=4.5,c=color,capsize=3,lw=1.2)
 ax.axvline(0,c='#333333',ls='--',lw=.8);ax.axhline(2.5,c='#CFD7DE',lw=.7);ax.grid(axis='x');ax.set(title=ttl,xlabel='Mean CRPS difference',ylim=(5.6,-.6),yticks=range(6),yticklabels=[('Weibo' if s=='weibo' else 'SEISMIC')+' / '+names[f] for s,f in pairs])
save(fig,'noise_control')
# Full per-window PIT panels, both constructions.
for s in ['weibo','seismic']:
 for key,tag in [('nonrandomized_pit_mass','nonrandomized'),('randomized_pit_frequency','randomized')]:
  fig,axs=plt.subplots(3,3,figsize=(7.0,5.9),sharey=True,sharex=True,layout='constrained')
  for r,f in enumerate(family):
   for c,w in enumerate([300,900,3600]):
    ax=axs[r,c]
    for i in ['I0','I1']:
     d=next(z for z in cal if (z['source'],z['family'],z['info'])==(s,f,i))['calibration'][str(w)][key];ax.plot(x,d,'s--' if i=='I0' else 'o-',ms=3,lw=1,c=colors[i],label=i)
    ax.axhline(.1,c='#C18127',ls=':',lw=1);ax.set(title=f'{names[f]} | {w//60} min',ylim=(0,.5),xticks=[0,.5,1]);ax.grid(axis='y')
    if c==0:ax.set_ylabel('Bin mass' if tag=='nonrandomized' else 'Bin frequency')
    if r==2:ax.set_xlabel('Count PIT')
  axs[0,0].legend(frameon=False,fontsize=7);save(fig,f'pit_{s}_{tag}')
# Window-specific primary contrasts (descriptive).
fig,axs=plt.subplots(1,2,figsize=(7.05,2.8),layout='constrained')
for ax,s in zip(axs,['weibo','seismic']):
 for f,c,m in zip(family,['#758595','#087F8C','#C18127'],['s','o','^']):
  ds=[100*(1-get(s,f,'I1')['window_metrics'][str(w)]['crps']/get(s,f,'I0')['window_metrics'][str(w)]['crps']) for w in [300,900,3600]];ax.plot(range(3),ds,marker=m,c=c,lw=1.2,label=names[f])
 ax.set(xticks=range(3),xticklabels=['5','15','60'],xlabel='Prefix duration (min)',ylabel='CRPS reduction (%)',title='Weibo' if s=='weibo' else 'SEISMIC');ax.axhline(0,c='#333333',lw=.7);ax.grid(axis='y')
axs[0].legend(frameon=False,fontsize=7);save(fig,'per_window')
# No-growth reliability and the occupied-bin sample support, all families.
fig,axs=plt.subplots(2,3,figsize=(7.05,4.2),sharey=True,sharex=True,layout='constrained')
for r,s in enumerate(['weibo','seismic']):
 for c,f in enumerate(family):
  ax=axs[r,c]
  for i in ['I0','I1']:
   b=np.array(next(z for z in cal if (z['source'],z['family'],z['info'])==(s,f,i))['calibration']['0']['p0_bins_count_sumforecast_sumobserved']);sel=b[:,0]>0;b=b[sel];ax.plot(b[:,1]/b[:,0],b[:,2]/b[:,0],ls='--' if i=='I0' else '-',lw=.8,c=colors[i]);ax.scatter(b[:,1]/b[:,0],b[:,2]/b[:,0],s=9+10*np.log10(1+b[:,0]),marker='s' if i=='I0' else 'o',facecolors='none' if i=='I0' else colors[i],edgecolors=colors[i],linewidths=.6,label=i)
  ax.plot([0,1],[0,1],c='#C18127',ls=':',lw=.8);ax.set(xlim=(-.025,1.025),ylim=(-.025,1.025),xticks=[0,.5,1],yticks=[0,.5,1],title=('Weibo' if s=='weibo' else 'SEISMIC')+' | '+names[f]);ax.grid(lw=.4)
  if c==0:ax.set_ylabel('Observed no-growth fraction')
  if r==1:ax.set_xlabel('Mean forecast probability')
axs[0,0].legend(frameon=False,fontsize=7);save(fig,'no_growth_reliability')
manifest={str(x.relative_to(P)) : hashlib.sha256(x.read_bytes()).hexdigest() for x in (P/'evidence').rglob('*.json')}
(P/'FIGURE_INPUT_HASHES.json').write_text(json.dumps(manifest,indent=2))
print('Figure PDFs:',len(list(O.glob('*.pdf'))))

"""Redraw manuscript figures from the provided saved aggregate JSON; no models or scoring."""
from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
OUT=Path(__file__).resolve().parents[1]
def load(p): return json.loads(p.read_text())
primary=load(OUT/'evidence/PRIMARY_COMPARISONS.json')
metrics=load(OUT/'evidence/PROCEDURE_METRICS.json')
cal=load(OUT/'evidence/CALIBRATION.json')
M={(x['source'],x['family'],x['info']):x for x in metrics}
C={(x['source'],x['family'],x['info']):x for x in cal}
names={'weibo':'Weibo','seismic':'SEISMIC','hurdle':'Hurdle','qrf':'QRF','ngboost':'NGBoost','nb2_glm':'NB2 GLM','poisson_glm':'Poisson GLM','conditional_empirical':'Conditional empirical','empirical_window':'Empirical by window'}
families=['empirical_window','conditional_empirical','poisson_glm','nb2_glm','hurdle','qrf','ngboost']
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False,'pdf.fonttype':42,'ps.fonttype':42,'savefig.dpi':220})
colors={'I0':'#777777','I1':'#147D92'}
def save(fig,name):
 for ext in ['png','pdf']:fig.savefig(OUT/'figures'/f'{name}.{ext}',bbox_inches='tight')
 plt.close(fig)
fig,axes=plt.subplots(1,2,figsize=(10,3.5),layout='constrained')
for ax,s in zip(axes,['weibo','seismic']):
 for k,f in enumerate(['hurdle','qrf','ngboost']):
  x=next(v for v in primary if v['source']==s and v['family']==f);delta=x['delta_I1_minus_I0'];lo,hi=x['adjusted_interval']
  ax.errorbar(delta,2-k,xerr=[[delta-lo],[hi-delta]],fmt='o',color=colors['I1'],capsize=3,lw=2)
 ax.axvline(0,color='#555555',ls='--',lw=1);ax.set_yticks([2,1,0],['Hurdle','QRF','NGBoost']);ax.set_ylim(-.6,2.6);ax.set_title(names[s]);ax.set_xlabel('CRPS difference (I1 − I0)');ax.grid(axis='x',alpha=.18)
save(fig,'fig1_primary_contrasts')
fig,axes=plt.subplots(1,2,figsize=(10,4.2),layout='constrained')
for ax,s in zip(axes,['weibo','seismic']):
 for k,f in enumerate(families):
  for i in ['I0','I1']:
   if (s,f,i) not in M:continue
   ax.plot(M[(s,f,i)]['metrics']['crps'],6-k,'o',color=colors[i],ms=6,label=i if k==4 else None)
 ax.set_yticks(range(6,-1,-1),[names[f] for f in families]);ax.set_title(names[s]);ax.set_xlabel('Mean TEST CRPS');ax.grid(axis='x',alpha=.18);ax.legend(frameon=False)
save(fig,'fig2_all_procedures')
for s in ['weibo','seismic']:
 fig,axes=plt.subplots(3,3,figsize=(10,7.5),layout='constrained',sharex=True,sharey=True)
 for fi,f in enumerate(['hurdle','qrf','ngboost']):
  for wi,w in enumerate([300,900,3600]):
   ax=axes[fi,wi]
   for i in ['I0','I1']:
    v=C[(s,f,i)]['calibration'][str(w)]['nonrandomized_pit_mass']
    ax.plot(np.linspace(.05,.95,10),v,'o-',ms=3,lw=1.4,color=colors[i],label=i)
   ax.axhline(.1,color='#555555',ls=':',lw=1);ax.set_xlim(0,1);ax.set_ylim(0,.26);ax.set_xticks([0,.5,1]);ax.set_title(f'{names[f]} · {w//60} min',fontsize=10);ax.grid(alpha=.15)
   if wi==0:ax.set_ylabel('PIT bin mass')
   if fi==2:ax.set_xlabel('PIT bin center')
 axes[0,0].legend(frameon=False);fig.suptitle(f'{names[s]}: nonrandomized count PIT',fontsize=12)
 save(fig,'fig3_pit_weibo' if s=='weibo' else 'fig4_pit_seismic')
fig,axes=plt.subplots(1,2,figsize=(9,3.2),layout='constrained',sharey=True)
for ax,s in zip(axes,['weibo','seismic']):
 for f,c in zip(['hurdle','qrf','ngboost'],['#2F6575','#AE6921','#745483']):
  vals=[]
  for w in [300,900,3600]:
   a=M[(s,f,'I0')]['window_metrics'][str(w)]['crps'];b=M[(s,f,'I1')]['window_metrics'][str(w)]['crps'];vals.append(100*(1-b/a))
  ax.plot([0,1,2],vals,'o-',label=names[f],color=c,lw=1.7,ms=4)
 ax.set_xticks([0,1,2],['5','15','60']);ax.set_xlabel('Observed prefix (minutes)');ax.set_title(names[s]);ax.axhline(0,color='#777777',lw=.8);ax.grid(axis='y',alpha=.15)
axes[0].set_ylabel('Relative CRPS reduction (%)');axes[1].legend(frameon=False)
save(fig,'figS1_per_window')

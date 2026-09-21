"""Optional graphical abstract: vector PDF/SVG and publisher-size PNG from frozen results."""
from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch,FancyArrowPatch
from PIL import Image
P=Path(__file__).resolve().parent.parent
primary=json.loads((P/'support/evidence/PRIMARY_COMPARISONS.json').read_text());noise=json.loads((P/'support/evidence/phase14/NOISE_COMPARISONS.json').read_text())
low=min(d['relative_reduction']*100 for d in primary);high=max(d['relative_reduction']*100 for d in primary)
assert len(primary)==6 and all(d['adjusted_interval'][1]<0 for d in primary)
assert sum(d['contrast']=='I1_minus_noise' and d['adjusted_high']<0 for d in noise)==6
plt.rcParams.update({'font.family':'DejaVu Sans','svg.fonttype':'none','pdf.fonttype':42})
f=plt.figure(figsize=(6.6,2.95),dpi=100,facecolor='white');ax=f.add_axes([0,0,1,1]);ax.set(xlim=(0,660),ylim=(295,0));ax.axis('off')
navy='#17324D';teal='#006D77'
def text(x,y,t,size=12,color=navy,weight='normal',ha='left'):ax.text(x,y,t,fontsize=size,color=color,weight=weight,ha=ha,va='center')
text(24,28,'What does timing add to size?',17,weight='bold')
text(24,58,'Weibo + SEISMIC  |  10,000 test roots',12)
for x,w in [(24,264),(320,316)]:ax.add_patch(FancyBboxPatch((x,83),w,112,boxstyle='round,pad=0,rounding_size=9',facecolor='#F0F6F8',edgecolor='#A8BDC8'))
text(40,109,'Size + duration',14,weight='bold');text(40,143,'+ 7 timing summaries',13,color=teal);text(40,177,'Hurdle  /  QRF  /  NGBoost',11.5)
ax.add_patch(FancyArrowPatch((293,141),(315,141),arrowstyle='-|>',mutation_scale=14,color=navy,lw=1.8))
text(478,113,f'{low:.2f}–{high:.2f}%',24,color=teal,weight='bold',ha='center');text(478,149,'lower mean CRPS',14,ha='center');text(478,179,'All 6 primary contrasts',12,ha='center')
text(24,226,'Timing beats the noise control in all 6 cases',12.5,weight='bold');text(24,263,'Heterogeneous gains; calibration limits remain',12.5)
for ext in ['pdf','svg','png']:f.savefig(P/'submission'/f'gagraphic.{ext}',dpi=100)
plt.close(f)
p=P/'submission/gagraphic.png';im=Image.open(p).convert('RGB');assert im.size==(660,295);im.save(p,dpi=(300,300),optimize=True)
(P/'submission/GRAPHICAL_ABSTRACT_CAPTION.md').write_text('''# Optional graphical abstract

**Caption:** On two selected archives, adding seven timing summaries to size and duration reduces mean discrete CRPS in all six within-family comparisons (0.69–13.48%; all conditional Bonferroni-adjusted intervals exclude zero). Timing also outperforms the specified independent-noise control in six separately adjusted post-test supplementary contrasts. Benefits vary across procedures and prefix strata, and calibration limitations persist. These are fixed-model, source-specific comparisons, not evidence of causal timing effects or cross-platform transfer.

Sources: support/evidence/PRIMARY_COMPARISONS.json and support/evidence/phase14/NOISE_COMPARISONS.json. Created by support/make_graphical_abstract.py without fitting or scoring. PNG: 660×295 pixels, 300 dpi metadata; vector PDF and editable SVG are also supplied. If used, upload it with the article for peer review. Its preparation falls under the manuscript AI-assistance disclosure.\n''')
print('PNG bytes',p.stat().st_size)

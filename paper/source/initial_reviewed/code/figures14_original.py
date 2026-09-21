"""Publication-style saved-result plots; never invokes a model."""
import argparse
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from common14 import *

def make(stagea,stageb,out):
    out.mkdir(parents=True,exist_ok=True);cfg=read(KIT/'CONFIG_14.json');rows=read(stagea/'STRATA_RESULTS.json')
    plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False,'savefig.dpi':180})
    colors={'hurdle':'#2D6A8A','qrf':'#C05A35','ngboost':'#548B63'}
    for source in cfg['sources']:
        fig,axs=plt.subplots(1,3,figsize=(14,4.8),layout='constrained')
        for wi,(w,ax) in enumerate(zip(cfg['windows'],axs)):
            ax.axhline(0,color='#999999',lw=.8)
            for fi,f in enumerate(cfg['primary_families']):
                rr=[next(r for r in rows if r['source']==source and r['family']==f and r['window_s']==w and r['prefix_bin']==b) for b in cfg['bins']]
                x=np.arange(5)+(fi-1)*.15;y=[np.nan if r['delta_I1_minus_I0'] is None else r['delta_I1_minus_I0'] for r in rr]
                ax.plot(x,y,'o-',ms=4,lw=1,color=colors[f],label=f.upper() if f!='hurdle' else 'Hurdle')
                for xx,r in zip(x,rr):
                    if r['pointwise95_low'] is not None:
                        ax.vlines(xx,r['pointwise95_low'],r['pointwise95_high'],color=colors[f],lw=1,alpha=.8)
                        ax.hlines([r['pointwise95_low'],r['pointwise95_high']],xx-.035,xx+.035,color=colors[f],lw=1)
            counts=[next(r['roots'] for r in rows if r['source']==source and r['window_s']==w and r['prefix_bin']==b) for b in cfg['bins']]
            ax.set_xticks(range(5),[f'{b}\nn={n:,}' for b,n in zip(cfg['bins'],counts)])
            ax.set_title(f'{w//60}-minute prefix');ax.set_xlabel('Recorded nonroot prefix events');ax.set_ylabel('CRPS(I1) − CRPS(I0)');ax.ticklabel_format(axis='y',style='plain',useOffset=False)
        axs[0].legend(frameon=False,fontsize=9);fig.suptitle(f'{source.upper()}: timing gains within fixed prefix-size strata',fontsize=13)
        fig.get_layout_engine().set(rect=(0,.08,1,.90))
        fig.text(.5,.015,'Exploratory pointwise 95% intervals; absent below 30 sampling units. Negative favors I1. Lines connect bins for readability only.',ha='center',fontsize=9)
        for ext in ['png','pdf']:fig.savefig(out/f'strata_{source}.{ext}')
        plt.close(fig)
    if stageb is not None and (stageb/'NOISE_COMPARISONS.json').exists():
        rs=read(stageb/'NOISE_COMPARISONS.json');fig,axs=plt.subplots(2,2,figsize=(11,6),layout='constrained')
        for si,s in enumerate(cfg['sources']):
            for ci,c in enumerate(['noise_minus_I0','I1_minus_noise']):
                ax=axs[si,ci];ax.axvline(0,color='#999999',lw=.8)
                for j,f in enumerate(cfg['primary_families']):
                    r=next(x for x in rs if x['source']==s and x['family']==f and x['contrast']==c)
                    if r['status']=='available':ax.hlines(j,r['adjusted_low'],r['adjusted_high'],color=colors[f]);ax.plot(r['delta'],j,'o',color=colors[f])
                    else:ax.text(.02,j,'withheld',transform=ax.get_yaxis_transform(),va='center')
                ax.set_yticks(range(3),['Hurdle','QRF','NGBoost']);ax.set_title(s.upper()+': '+c.replace('_',' '));ax.set_xlabel('Mean CRPS difference')
        for ext in ['png','pdf']:fig.savefig(out/f'noise_contrasts.{ext}')
        plt.close(fig)
    write(out/'FIGURE_REPORT.json',{'files':[p.name for p in sorted(out.glob('*')) if p.suffix in ['.png','.pdf']],'new_predictions':0})
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--stage-a',type=Path,required=True);p.add_argument('--stage-b',type=Path);p.add_argument('--out',type=Path,required=True);a=p.parse_args();make(a.stage_a,a.stage_b,a.out)

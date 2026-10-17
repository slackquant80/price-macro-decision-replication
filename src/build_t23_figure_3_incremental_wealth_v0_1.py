"""Regenerate the one added T23 figure from exact public derived monthly returns.
Usage: python REPRODUCE_NEW_EXHIBIT.py ; requirements: pandas numpy matplotlib
Preserves source h1 net-return frequency, cost, and signal-month labels.
"""
from pathlib import Path
import hashlib
import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'data/T23_BENCHMARK_RELATIVE_MONTHLY_RETURNS_v1.0.csv'
_parser=argparse.ArgumentParser()
_parser.add_argument('--output-dir',default='reproduced')
_args=_parser.parse_args()
_OUT=Path(_args.output_dir)
if not _OUT.is_absolute(): _OUT=ROOT/_OUT
(_OUT/'figures').mkdir(parents=True,exist_ok=True)
EXPECTED='0591c2f1cc8e0616dbfaea3efbc131b08dbe6da589c442332a73fdb9b1fdc5da'
_bytes=SOURCE.read_bytes()
# Normalize only newline encoding (Git LF vs original locked Windows CRLF).
_canonical=_bytes.replace(b'\r\n',b'\n').replace(b'\r',b'\n').replace(b'\n',b'\r\n')
assert hashlib.sha256(_canonical).hexdigest()==EXPECTED,'Locked monthly derived return evidence mismatch'
monthly=pd.read_csv(SOURCE)
d=monthly[(monthly.architecture=='h1')&monthly.strategy.isin(['OWN_ONLY','MACRO_PLUS_OWN'])]
for s in ['OWN_ONLY','MACRO_PLUS_OWN']:
 x=d[d.strategy==s].sort_values('origin_signal_month')
 assert len(x)==112 and x.origin_signal_month.iloc[0]=='2017-03' and x.origin_signal_month.iloc[-1]=='2026-06'
 assert np.max(np.abs(x.gross_return-x.net_return-.001*x.turnover))<1e-12
p=d.pivot(index='origin_signal_month',columns='strategy',values='net_return').sort_index()
w=(1+p).cumprod()
rv=np.r_[1.,(w.MACRO_PLUS_OWN/w.OWN_ONLY).to_numpy()]
dd=rv/np.maximum.accumulate(rv)-1
assert abs(rv[-1]-1.0204483508663122)<1e-11
assert abs(dd.min()+0.2708482781362658)<1e-11
assert int((rv[1:]<1).sum())==72
plt.rcParams.update({'font.family':'Liberation Serif','font.size':10,'pdf.fonttype':42,'axes.linewidth':.7})
plt.rcParams['svg.hashsalt'] = 't23-v218-fig3-fixed'
fig,ax=plt.subplots(figsize=(7.4,3.55))
fig.subplots_adjust(left=.12,right=.93,top=.965,bottom=.18)
xs=np.arange(len(rv))
ax.plot(xs,rv,lw=1.85,color='#174A6E')
ax.axhline(1.,lw=.8,color='#989EA4')
ax.fill_between(xs,rv,1.,where=rv<1.,color='#9DA7B0',alpha=.14)
ax.spines[['top','right']].set_visible(False)
ax.grid(axis='y',c='#DFE3E7',lw=.55)
ax.set_axisbelow(True)
ax.set_ylim(.77,1.16);ax.set_xlim(0,118)
origins=pd.to_datetime(p.index+'-01')
years=[(i+1,str(dt.year)) for i,dt in enumerate(origins) if dt.month==1]
ax.set_xticks([1]+[i for i,y in years],['2017']+[y for i,y in years])
ax.yaxis.set_major_locator(MultipleLocator(.05))
ax.set_ylabel('Cumulative relative net wealth',fontsize=10)
ax.set_xlabel('Monthly signal origin (subsequent holding interval)',fontsize=9.2,labelpad=8)
ixdd=int(dd.argmin()); ixpeak=int(np.argmax(rv))
ax.scatter([ixdd,ixpeak],[rv[ixdd],rv[ixpeak]],s=19,color='#174A6E',zorder=3)
ax.annotate('Peak 1.126',xy=(ixpeak,rv[ixpeak]),xytext=(8,10),textcoords='offset points',fontsize=8.3,color='#174A6E')
ax.annotate('Relative drawdown -27.1%',xy=(ixdd,rv[ixdd]),xytext=(-4,-20),textcoords='offset points',ha='center',fontsize=8.5,color='#4B535B')
ax.annotate('End 1.020',xy=(112,rv[-1]),xytext=(6,8),textcoords='offset points',fontsize=8.8,color='#174A6E')
fig.savefig(_OUT/'figures/Figure_3_Incremental_Macro_Relative_Wealth_HOUSE_v0.1.pdf',bbox_inches='tight',metadata={'CreationDate':None,'ModDate':None,'Title':'T23 macro-vs-price monthly relative wealth'})
fig.savefig(_OUT/'figures/Figure_3_Incremental_Macro_Relative_Wealth_HOUSE_v0.1.svg',bbox_inches='tight',metadata={'Date':None,'Creator':'T23 monthly paper source-bound'})
fig.savefig(_OUT/'figures/Figure_3_Incremental_Macro_Relative_Wealth_HOUSE_v0.1.png',bbox_inches='tight',dpi=200)
plt.close(fig)
print('T23 v2.18 NEW FIGURE SOURCE/PARITY PASS',rv[-1],dd.min())

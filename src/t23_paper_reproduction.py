from pathlib import Path
import argparse
import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data'
_parser = argparse.ArgumentParser(description='Rebuild T23 paper-level figures and tables from included derived evidence.')
_parser.add_argument('--output-dir', default='reproduced', help='Output directory relative to package root, or an absolute path.')
_args = _parser.parse_args()
_outroot = Path(_args.output_dir)
if not _outroot.is_absolute():
    _outroot = ROOT / _outroot
OUTF = _outroot / 'figures'
OUTT = _outroot / 'tables'
OUTF.mkdir(parents=True, exist_ok=True)
OUTT.mkdir(parents=True, exist_ok=True)

# Restrained SlackQuant Investment Research figure grammar.
SQ_NAVY = '#174A6E'
SQ_SLATE = '#5E6772'
SQ_LIGHT = '#D8DDE1'
SQ_TEXT = '#16191D'
SQ_MID = '#8A9199'

plt.rcParams.update({
    'font.family': 'Liberation Serif',
    'font.size': 9.2,
    'axes.labelsize': 9.2,
    'xtick.labelsize': 8.5,
    'ytick.labelsize': 8.5,
    'legend.fontsize': 8.1,
    'axes.linewidth': 0.7,
    'pdf.fonttype': 42,
    'ps.fonttype': 42,
    'savefig.facecolor': 'white',
    'svg.hashsalt': 'slackquant-t23-v0.8',
})

def save(fig, stem):
    # Deterministic publication outputs: suppress timestamp-bearing metadata and
    # use a fixed SVG hashsalt so identical inputs/code produce identical bytes.
    for ext in ['pdf', 'svg', 'png']:
        kwargs = {'bbox_inches': 'tight'}
        if ext == 'pdf':
            kwargs['metadata'] = {
                'CreationDate': None,
                'ModDate': None,
                'Creator': 'SlackQuant T23 deterministic exhibit builder',
                'Producer': 'Matplotlib',
            }
        elif ext == 'svg':
            kwargs['metadata'] = {'Date': None, 'Creator': 'SlackQuant T23 deterministic exhibit builder'}
        else:
            kwargs['dpi'] = 220
            kwargs['metadata'] = {'Software': 'SlackQuant T23 deterministic exhibit builder'}
        fig.savefig(OUTF / f'{stem}.{ext}', **kwargs)
    plt.close(fig)

monthly = pd.read_csv(DATA / 'T23_BENCHMARK_RELATIVE_MONTHLY_RETURNS_v1.0.csv')
metrics = pd.read_csv(DATA / 'T23_BENCHMARK_RELATIVE_METRICS_v1.0.csv')
absolute = pd.read_csv(DATA / 'T23_PORTFOLIO_ABSOLUTE_SUMMARY_v1.0.csv')
random_dist = pd.read_csv(DATA / 'T23_RANDOM_TOP4_DISTRIBUTION_v1.0.csv')
random_place = pd.read_csv(DATA / 'T23_RANDOM_TOP4_OBSERVED_PLACEMENT_v1.0.csv')
ci_top = pd.read_csv(DATA / 'ROBUSTNESS_TOPN_INCREMENTAL_MACRO_CI_v1.0.csv')
ci_b8 = pd.read_csv(DATA / 'B1_BALANCED8_INCREMENTAL_MACRO_CI_v1.0.csv')
ci_ra = pd.read_csv(DATA / 'B2_RISK_ADJUSTED_INCREMENTAL_MACRO_CI_v1.0.csv')
b3_ci = pd.read_csv(DATA / 'B3_RAW_FRED_H1_SHARPE_DIFFERENCE_CI_v1.0.csv').set_index('contrast')
timing_ci = pd.read_csv(DATA / 'PMT_STAGE2_SHARPE_DIFFERENCE_CI_v1.0.csv').set_index('contrast')
timing_overlap = pd.read_csv(DATA / 'PMT_STAGE2_DECISION_OVERLAP_SUMMARY_v1.0.csv').set_index('block')
revised_ci = pd.read_csv(DATA / 'HVR_STAGE2_SHARPE_DIFFERENCE_CI_v1.0.csv').set_index('contrast')
revised_overlap = pd.read_csv(DATA / 'HVR_STAGE2_DECISION_OVERLAP_SUMMARY_v1.0.csv').set_index('block')

# ---------------------------------------------------------------------
# Figure 2. Active value relative to the same-universe EW11 benchmark.
# Panel A: cumulative relative wealth. Panel B: IR summary.
# ---------------------------------------------------------------------
h1m = monthly[monthly['architecture'].eq('h1')].copy()
piv = h1m.pivot(index='origin_signal_month', columns='strategy', values='net_return').sort_index()
piv.index = pd.to_datetime(piv.index + '-01')
strategies = [
    ('OWN_ONLY', 'Price-only ML', SQ_NAVY, '-', 1.8),
    ('MOM12', '12M momentum', SQ_SLATE, '--', 1.25),
    ('MOM12_1', '12-1M momentum', SQ_MID, '-.', 1.15),
    ('MOM6', '6M momentum', '#B0B5BB', ':', 1.35),
]
fig = plt.figure(figsize=(7.15, 6.15))
gs = fig.add_gridspec(2, 1, height_ratios=[2.1, 1.0], hspace=0.34)
ax = fig.add_subplot(gs[0, 0])
for s, label, color, ls, lw in strategies:
    rel = ((1 + piv[s]) / (1 + piv['EW11'])).cumprod()
    ax.plot(rel.index, rel.values, label=label, color=color, linestyle=ls, linewidth=lw)
    ax.annotate(f'{rel.iloc[-1]:.2f}x', (rel.index[-1], rel.iloc[-1]), xytext=(5,0), textcoords='offset points',
                va='center', fontsize=7.7, color=color)
ax.axhline(1.0, color='0.55', linewidth=0.8)
ax.set_ylabel('Wealth relative to EW11')
ax.set_ylim(0.90, 1.76)
ax.grid(axis='y', color='0.91', linewidth=0.65)
ax.spines[['top','right']].set_visible(False)
ax.legend(frameon=False, ncol=2, loc='upper left')
ax.text(0.0, 1.02, 'A. Cumulative relative wealth', transform=ax.transAxes,
        fontsize=9.2, fontweight='bold', color=SQ_TEXT)

ax2 = fig.add_subplot(gs[1, 0])
subset = metrics[(metrics['architecture'].eq('h1')) & (metrics['benchmark'].eq('EW11')) &
                 (metrics['strategy'].isin([x[0] for x in strategies]))].copy()
order = [x[0] for x in strategies]
subset['ord'] = subset['strategy'].map({s:i for i,s in enumerate(order)})
subset = subset.sort_values('ord')
labels = {s:l for s,l,_,_,_ in strategies}
colors = {s:c for s,_,c,_,_ in strategies}
y = np.arange(len(subset))[::-1]
for yy, (_, r) in zip(y, subset.iterrows()):
    s = r['strategy']
    ax2.hlines(yy, 0, r['information_ratio'], color=SQ_LIGHT, linewidth=2.0)
    ax2.scatter(r['information_ratio'], yy, s=32, color=colors[s], zorder=3)
    ax2.annotate(f"IR {r['information_ratio']:.2f}  |  active return {r['annualized_active_return']*100:.1f}%",
                 (r['information_ratio'], yy), xytext=(6,0), textcoords='offset points', va='center', fontsize=7.8)
ax2.axvline(0, color='0.55', linewidth=0.8)
ax2.set_yticks(y)
ax2.set_yticklabels([labels[s] for s in subset['strategy']])
ax2.set_xlabel('Information ratio vs EW11')
ax2.set_xlim(-0.02, 0.86)
ax2.grid(axis='x', color='0.92', linewidth=0.65)
ax2.spines[['top','right','left']].set_visible(False)
ax2.tick_params(axis='y', length=0)
ax2.text(0.0, 1.08, 'B. Benchmark-relative efficiency', transform=ax2.transAxes,
         fontsize=9.2, fontweight='bold', color=SQ_TEXT)
fig.subplots_adjust(left=0.18, right=0.91, top=0.97, bottom=0.09)
save(fig, 'Figure_2_Active_Value_vs_EW11_HOUSE_v0.5')

# ---------------------------------------------------------------------
# Figure 3. Incremental macro value, including B3 raw-FRED check.
# ---------------------------------------------------------------------
rows=[('header','11-asset universe',np.nan,np.nan,np.nan,'',False)]
for _,r in ci_top.iterrows():
    arch=str(r.architecture)
    label={'h1':'1-month forecast','h2':'2-month forecast','h3':'3-month forecast','multi':'Multi-horizon'}[arch] + f' | Top {int(r.top_n)}'
    primary_flag = (arch=='h1' and int(r.top_n)==4)
    if primary_flag:
        label += ' (primary)'
    rows.append(('data',label,float(r.point_difference),float(r.ci_2_5),float(r.ci_97_5),'macro_own',primary_flag))
rows += [('spacer','',np.nan,np.nan,np.nan,'',False),('header','Eight-asset universe',np.nan,np.nan,np.nan,'',False)]
for _,r in ci_b8.iterrows():
    arch={'h1':'1-month','h2':'2-month','h3':'3-month','multi':'Multi-horizon'}[str(r.architecture)]
    rows.append(('data',f'{arch} | Top {int(r.top_n)}',float(r.point_difference),float(r.ci_2_5),float(r.ci_97_5),'macro_own',False))
rows += [('spacer','',np.nan,np.nan,np.nan,'',False),('header','Risk-adjusted ranking',np.nan,np.nan,np.nan,'',False)]
for _,r in ci_ra.iterrows():
    arch={'h1':'1-month','h2':'2-month','h3':'3-month','multi':'Multi-horizon'}[str(r.architecture)]
    rows.append(('data',f'{arch} | Top 4',float(r.point_difference),float(r.ci_2_5),float(r.ci_97_5),'macro_own',False))
rows += [('spacer','',np.nan,np.nan,np.nan,'',False),('header','Raw FRED-MD robustness check',np.nan,np.nan,np.nan,'',False)]
for contrast,label,ctype in [
    ('RAW_REG2_MACRO_PLUS_OWN_minus_OWN_REG2','Raw Macro+Price minus Price-only','raw_own'),
    ('RAW_REG2_MACRO_PLUS_OWN_minus_PCA_REG2_MACRO_PLUS_OWN','Raw Macro+Price minus PCA Macro+Price','raw_pca')]:
    r=b3_ci.loc[contrast]
    rows.append(('data',label,float(r.point_difference),float(r.ci_2_5),float(r.ci_97_5),ctype,False))
y=np.arange(len(rows))
fig,ax=plt.subplots(figsize=(7.15,8.35))
for i,(kind,label,val,lo,hi,ctype,is_primary) in enumerate(rows):
    if kind!='data':
        continue
    xerr=np.array([[val-lo],[hi-val]])
    if is_primary:
        ax.errorbar([val],[i],xerr=xerr,fmt='D',color=SQ_NAVY,ecolor=SQ_NAVY,capsize=2.8,elinewidth=1.05,markersize=5.4,zorder=4)
    elif ctype=='raw_pca':
        ax.errorbar([val],[i],xerr=xerr,fmt='s',mfc='white',mec=SQ_SLATE,color=SQ_SLATE,ecolor=SQ_SLATE,capsize=2.5,elinewidth=0.9,markersize=4.6,zorder=3)
    else:
        ax.errorbar([val],[i],xerr=xerr,fmt='o',color=SQ_SLATE,ecolor=SQ_SLATE,capsize=2.5,elinewidth=0.9,markersize=4.4,zorder=3)
ax.axvline(0,color='0.35',linewidth=1.0,zorder=1)
ax.set_yticks(y); ax.set_yticklabels([r[1] for r in rows]); ax.invert_yaxis()
for tick,r in zip(ax.get_yticklabels(),rows):
    if r[0]=='header':
        tick.set_fontweight('bold'); tick.set_color(SQ_TEXT)
    elif r[0]=='spacer':
        tick.set_visible(False)
ax.set_xlabel('Net Sharpe difference')
ax.set_xlim(-0.75,0.32)
ax.grid(axis='x',color='0.91',linewidth=0.65)
ax.spines[['top','right','left']].set_visible(False)
ax.tick_params(axis='y',length=0)
fig.subplots_adjust(left=0.43,right=0.98,top=0.985,bottom=0.07)
save(fig, 'Figure_3_Incremental_Macro_Value_with_RAW_HOUSE_v0.7')

# ---------------------------------------------------------------------
# Figure 4. Information timing / information-design robustness.
# Panel A: incremental Sharpe difference vs Price-only.
# Panel B: Top-4 disagreement vs the historical-vintage primary.
# ---------------------------------------------------------------------
info_rows = [
    ('Historical-vintage primary',
     float(timing_ci.loc['SAME_MONTH_MACRO_PLUS_OWN_minus_OWN_ONLY','point_difference']),
     float(timing_ci.loc['SAME_MONTH_MACRO_PLUS_OWN_minus_OWN_ONLY','ci_2_5']),
     float(timing_ci.loc['SAME_MONTH_MACRO_PLUS_OWN_minus_OWN_ONLY','ci_97_5'])),
    ('Conservative previous-month timing',
     float(timing_ci.loc['PREVIOUS_MONTH_MACRO_PLUS_OWN_minus_OWN_ONLY','point_difference']),
     float(timing_ci.loc['PREVIOUS_MONTH_MACRO_PLUS_OWN_minus_OWN_ONLY','ci_2_5']),
     float(timing_ci.loc['PREVIOUS_MONTH_MACRO_PLUS_OWN_minus_OWN_ONLY','ci_97_5'])),
    ('Latest-snapshot / calendar-truncated',
     float(revised_ci.loc['REVISED_MACRO_PLUS_OWN_minus_OWN_ONLY','point_difference']),
     float(revised_ci.loc['REVISED_MACRO_PLUS_OWN_minus_OWN_ONLY','ci_2_5']),
     float(revised_ci.loc['REVISED_MACRO_PLUS_OWN_minus_OWN_ONLY','ci_97_5'])),
]
fig = plt.figure(figsize=(7.15, 5.45))
gs = fig.add_gridspec(2, 1, height_ratios=[1.6, 1.0], hspace=0.48)
ax = fig.add_subplot(gs[0,0])
y = np.arange(len(info_rows))[::-1]
for yy,(label,val,lo,hi) in zip(y,info_rows):
    xerr=np.array([[val-lo],[hi-val]])
    marker='D' if label=='Historical-vintage primary' else 'o'
    color=SQ_NAVY if label=='Historical-vintage primary' else SQ_SLATE
    ax.errorbar([val],[yy],xerr=xerr,fmt=marker,color=color,ecolor=color,capsize=2.8,elinewidth=1.0,markersize=5.0,zorder=3)
ax.axvline(0,color='0.35',linewidth=0.9)
ax.set_yticks(y); ax.set_yticklabels([r[0] for r in info_rows])
ax.set_xlabel('Macro+Price minus Price-only net Sharpe difference')
ax.set_xlim(-0.72,0.30)
ax.grid(axis='x',color='0.91',linewidth=0.65)
ax.spines[['top','right','left']].set_visible(False)
ax.tick_params(axis='y',length=0)
ax.text(0.0,1.08,'A. Incremental conclusion across information designs',transform=ax.transAxes,fontsize=9.2,fontweight='bold',color=SQ_TEXT)

ax2 = fig.add_subplot(gs[1,0])
labels=['Conservative previous-month timing','Latest-snapshot / calendar-truncated']
vals=[float(timing_overlap.loc['macro_plus_own','disagreement_fraction'])*100,
      float(revised_overlap.loc['macro_plus_own','disagreement_fraction'])*100]
y2=np.arange(len(labels))[::-1]
ax2.barh(y2,vals,color=[SQ_NAVY,SQ_SLATE],height=0.48)
for yy,v in zip(y2,vals):
    ax2.text(v+1.2,yy,f'{v:.1f}%',va='center',fontsize=8.3)
ax2.set_yticks(y2); ax2.set_yticklabels(labels)
ax2.set_xlabel('Months with a different Macro+Price Top-4 selection vs primary (%)')
ax2.set_xlim(0,62)
ax2.grid(axis='x',color='0.92',linewidth=0.65)
ax2.spines[['top','right','left']].set_visible(False)
ax2.tick_params(axis='y',length=0)
ax2.text(0.0,1.12,'B. Portfolio decisions remain information-design sensitive',transform=ax2.transAxes,fontsize=9.2,fontweight='bold',color=SQ_TEXT)
fig.subplots_adjust(left=0.36,right=0.96,top=0.96,bottom=0.10)
save(fig, 'Figure_4_Information_Timing_Robustness_HOUSE_v0.1')

# ---------------------------------------------------------------------
# Figure 5. Practitioner trade-off relative to 60/40.
# x: active return, y: MDD difference (positive = shallower drawdown).
# ---------------------------------------------------------------------
pr = metrics[(metrics['architecture'].eq('h1')) & (metrics['benchmark'].eq('SPY_AGG_60_40')) &
             (metrics['strategy'].isin(['OWN_ONLY','MACRO_PLUS_OWN','MACRO_ONLY','MOM12']))].copy()
labels4={'OWN_ONLY':'Price-only ML','MACRO_PLUS_OWN':'Macro+Price ML','MACRO_ONLY':'Macro-only ML','MOM12':'12M momentum'}
markers={'OWN_ONLY':'s','MACRO_PLUS_OWN':'o','MACRO_ONLY':'^','MOM12':'D'}
colors4={'OWN_ONLY':SQ_NAVY,'MACRO_PLUS_OWN':SQ_SLATE,'MACRO_ONLY':'#9AA0A6','MOM12':'#4A4F55'}
fig,ax=plt.subplots(figsize=(7.15,4.75))
ax.axhline(0,color='0.55',linewidth=0.8)
ax.axvline(0,color='0.55',linewidth=0.8)
offsets={'OWN_ONLY':(8,7),'MACRO_PLUS_OWN':(8,-18),'MACRO_ONLY':(8,-16),'MOM12':(8,7)}
for _,r in pr.iterrows():
    s=r['strategy']; x=r['annualized_active_return']*100; yv=r['max_drawdown_difference']*100
    ax.scatter(x,yv,s=48,marker=markers[s],color=colors4[s],zorder=3)
    ax.annotate(f"{labels4[s]}\nIR {r['information_ratio']:.2f}", (x,yv), xytext=offsets[s], textcoords='offset points', fontsize=8)
ax.set_xlabel('Annualized active return vs 60/40 (%)')
ax.set_ylabel('Maximum-drawdown difference vs 60/40 (percentage points)')
ax.set_xlim(1.8,6.5)
ax.set_ylim(-9.5,2.2)
ax.grid(color='0.92',linewidth=0.65)
ax.spines[['top','right']].set_visible(False)
ax.text(0.02,0.97,'Above zero = shallower drawdown than 60/40', transform=ax.transAxes, va='top', fontsize=7.8, color=SQ_SLATE)
fig.subplots_adjust(left=0.14,right=0.98,top=0.96,bottom=0.14)
save(fig, 'Figure_4_Practitioner_Tradeoff_vs_60_40_HOUSE_v0.6')

# ---------------------------------------------------------------------
# Figure 6. Calendar-year Macro+Price minus Price-only net return.
# Derived only from sealed monthly return series.
# ---------------------------------------------------------------------
p = piv[['MACRO_PLUS_OWN','OWN_ONLY']].copy()
p['year'] = p.index.year
rows5=[]
for yr,g in p.groupby('year'):
    m_plus=(1+g['MACRO_PLUS_OWN']).prod()-1
    own=(1+g['OWN_ONLY']).prod()-1
    rel=(1+m_plus)/(1+own)-1
    rows5.append((yr,rel,len(g)))
yr=pd.DataFrame(rows5,columns=['year','relative_return','months'])
fig,ax=plt.subplots(figsize=(7.15,4.1))
ax.bar(yr['year'],yr['relative_return']*100,color=SQ_NAVY,width=0.76)
ax.axhline(0,color='0.35',linewidth=0.9)
ax.set_ylabel('Macro+Price minus Price-only return (%)')
ax.set_xticks(yr['year'])
ax.set_xticklabels([f"{int(y)}*" if m<12 else str(int(y)) for y,m in zip(yr['year'],yr['months'])],rotation=45,ha='right')
ax.grid(axis='y',color='0.91',linewidth=0.65)
ax.spines[['top','right']].set_visible(False)
ax.text(0.01,-0.24,'* Partial calendar year in the available out-of-sample sample.',transform=ax.transAxes,fontsize=8,color=SQ_SLATE)
fig.subplots_adjust(left=0.13,right=0.98,top=0.97,bottom=0.28)
save(fig, 'Figure_5_Macro_Helps_At_Times_HOUSE_v0.6')

# ---------------------------------------------------------------------
# Appendix Figure A1. Random Top-4 IR distribution.
# Supplemental descriptive robustness only; no p-value.
# ---------------------------------------------------------------------
fig,ax=plt.subplots(figsize=(7.15,4.55))
vals=random_dist['information_ratio_vs_ew11']
ax.hist(vals,bins=48,color='#D9DDE1',edgecolor='white',linewidth=0.35)
placements={}
for s in ['OWN_ONLY','MOM12','MOM12_1']:
    row=random_place[(random_place['strategy'].eq(s)) & (random_place['random_metric'].eq('information_ratio_vs_ew11'))].iloc[0]
    placements[s]=(float(row['observed_value']),float(row['empirical_percentile_random_le_observed']))
styles=[('OWN_ONLY','Price-only ML',SQ_NAVY,'-',1.8),('MOM12','12-month momentum',SQ_SLATE,'--',1.35),('MOM12_1','12-1M momentum','#4A4F55','-.',1.25)]
for s,label,c,ls,lw in styles:
    v,pct=placements[s]
    ax.axvline(v,color=c,linestyle=ls,linewidth=lw,label=f'{label}: IR {v:.2f}, {pct*100:.1f}th percentile')
ax.set_xlabel('Information ratio vs EW11')
ax.set_ylabel('Random Top-4 simulations')
ax.grid(axis='y',color='0.93',linewidth=0.65)
ax.spines[['top','right']].set_visible(False)
ax.legend(frameon=False,loc='upper left')
fig.subplots_adjust(left=0.12,right=0.98,top=0.96,bottom=0.14)
save(fig, 'Figure_A1_Random_Top4_IR_Distribution_HOUSE_v0.7')

# ---------------------------------------------------------------------
# Table 2. Active value vs EW11.
# ---------------------------------------------------------------------
tab = metrics[(metrics['architecture'].eq('h1')) & (metrics['benchmark'].eq('EW11')) &
              (metrics['strategy'].isin(['OWN_ONLY','MOM12','MOM12_1','MOM6','MACRO_PLUS_OWN','MACRO_ONLY']))].copy()
order=['OWN_ONLY','MOM12','MOM12_1','MOM6','MACRO_PLUS_OWN','MACRO_ONLY']
tab['ord']=tab['strategy'].map({s:i for i,s in enumerate(order)}); tab=tab.sort_values('ord')
lab={'OWN_ONLY':'Price-only ML','MOM12':'12M momentum','MOM12_1':'12-1M momentum','MOM6':'6M momentum','MACRO_PLUS_OWN':'Macro+Price ML','MACRO_ONLY':'Macro-only ML'}
lines=[]
lines.append(r'\begin{tabular}{lcccccc}')
lines.append(r'\toprule')
lines.append(r'\textbf{Strategy} & \textbf{Active return} & \textbf{TE} & \textbf{IR} & \textbf{Sharpe} & \textbf{Max drawdown} & \textbf{Turnover} \\')
lines.append(r'\midrule')
for _,r in tab.iterrows():
    lines.append(f"{lab[r['strategy']]} & {r['annualized_active_return']*100:.1f}\\% & {r['tracking_error']*100:.1f}\\% & {r['information_ratio']:.2f} & {r['strategy_sharpe_excess_bil']:.3f} & {r['strategy_max_drawdown']*100:.1f}\\% & {r['strategy_annualized_turnover']:.2f} \\\\")
lines.append(r'\bottomrule')
lines.append(r'\end{tabular}')
(OUTT/'Table_2_Active_Value_vs_EW11_v1.1.tex').write_text('\n'.join(lines),encoding='utf-8',newline='\n')

# Table 3. Practitioner comparison vs 60/40.
pr2=metrics[(metrics['architecture'].eq('h1')) & (metrics['benchmark'].eq('SPY_AGG_60_40')) &
            (metrics['strategy'].isin(['OWN_ONLY','MOM12','MACRO_PLUS_OWN','MACRO_ONLY']))].copy()
order2=['OWN_ONLY','MOM12','MACRO_PLUS_OWN','MACRO_ONLY']; pr2['ord']=pr2['strategy'].map({s:i for i,s in enumerate(order2)}); pr2=pr2.sort_values('ord')
lines=[]
lines.append(r'\begin{tabular}{lcccc}')
lines.append(r'\toprule')
lines.append(r'\textbf{Strategy} & \textbf{Active return} & \textbf{IR} & \textbf{Sharpe diff.} & \textbf{Drawdown diff.} \\')
lines.append(r'\midrule')
for _,r in pr2.iterrows():
    lines.append(f"{lab[r['strategy']]} & {r['annualized_active_return']*100:.1f}\\% & {r['information_ratio']:.2f} & {r['sharpe_difference']:+.3f} & {r['max_drawdown_difference']*100:+.1f} pp \\\\")
lines.append(r'\bottomrule')
lines.append(r'\end{tabular}')
(OUTT/'Table_3_Practitioner_vs_60_40_v1.2.tex').write_text('\n'.join(lines),encoding='utf-8',newline='\n')

print(f'PASS - T23 paper-level figures/tables rebuilt from included derived evidence: {_outroot}')

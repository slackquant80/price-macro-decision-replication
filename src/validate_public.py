from pathlib import Path
import argparse, hashlib, json
import numpy as np
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data'

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def cagr(r):
    a=np.asarray(r,float); return float(np.prod(1+a)**(12/len(a))-1)
def ann_vol(r): return float(np.std(np.asarray(r,float),ddof=1)*np.sqrt(12))
def sharpe(r,bil):
    x=np.asarray(r,float)-np.asarray(bil,float); return float(np.mean(x)/np.std(x,ddof=1)*np.sqrt(12))
def max_dd(r):
    w=np.cumprod(1+np.asarray(r,float)); peak=np.maximum.accumulate(np.r_[1.0,w])[1:]; return float(np.min(w/peak-1))
def active_metrics(rs,rb):
    a=np.asarray(rs,float)-np.asarray(rb,float); ar=float(12*np.mean(a)); te=float(np.std(a,ddof=1)*np.sqrt(12)); return ar,te,float(ar/te)

def check(cond,msg):
    if not cond: raise AssertionError(msg)
    print('PASS | '+msg)

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--output-dir',default='reproduced'); ap.add_argument('--strict-output-hash',action='store_true'); args=ap.parse_args()
    out=Path(args.output_dir); out=out if out.is_absolute() else ROOT/out
    monthly=pd.read_csv(DATA/'T23_BENCHMARK_RELATIVE_MONTHLY_RETURNS_v1.0.csv')
    metrics=pd.read_csv(DATA/'T23_BENCHMARK_RELATIVE_METRICS_v1.0.csv')
    absolute=pd.read_csv(DATA/'T23_PORTFOLIO_ABSOLUTE_SUMMARY_v1.0.csv')
    check(len(monthly)==3640,'monthly derived-evidence row count = 3640')
    check(len(metrics)==50,'benchmark-relative metric row count = 50')
    h=monthly[monthly.architecture.eq('h1')]
    # Primary Price-only and Macro+Price anchors independently replayed from monthly returns.
    for s,target_sh in [('OWN_ONLY',0.820644),('MACRO_PLUS_OWN',0.797917),('MACRO_ONLY',0.680240)]:
        x=h[h.strategy.eq(s)].sort_values('origin_signal_month')
        check(len(x)==112,f'{s} monthly decisions = 112')
        calc=sharpe(x.net_return,x.bil_return)
        check(abs(calc-target_sh)<0.0015,f'{s} Sharpe matches paper anchor ({calc:.6f})')
    own=h[h.strategy.eq('OWN_ONLY')].sort_values('origin_signal_month')
    ew=h[h.strategy.eq('EW11')].sort_values('origin_signal_month')
    ar,te,ir=active_metrics(own.net_return,ew.net_return)
    check(abs(ar-0.050)<0.0015,'Price-only active return vs EW11 matches 5.0% anchor')
    check(abs(te-0.071)<0.0015,'Price-only tracking error vs EW11 matches 7.1% anchor')
    check(abs(ir-0.71)<0.015,'Price-only information ratio vs EW11 matches 0.71 anchor')
    check(abs(cagr(own.net_return)-0.153)<0.0015,'Price-only CAGR matches 15.3% anchor')
    check(abs(cagr(ew.net_return)-0.102)<0.0015,'EW11 CAGR matches 10.2% anchor')
    # Incremental-macro intervals and information-timing anchors.
    ci=pd.read_csv(DATA/'ROBUSTNESS_TOPN_INCREMENTAL_MACRO_CI_v1.0.csv')
    r=ci[(ci.architecture.eq('h1'))&(ci.top_n.eq(4))].iloc[0]
    check(abs(float(r.point_difference)+0.022727)<5e-7,'primary Macro+Price minus Price-only Sharpe difference')
    check(abs(float(r.ci_2_5)+0.350770)<5e-7 and abs(float(r.ci_97_5)-0.235339)<5e-7,'primary 95% interval')
    timing=pd.read_csv(DATA/'PMT_STAGE2_SHARPE_DIFFERENCE_CI_v1.0.csv')
    t=timing[timing.contrast.eq('PREVIOUS_MONTH_MACRO_PLUS_OWN_minus_OWN_ONLY')].iloc[0]
    check(abs(float(t.point_difference)+0.1916254677953344)<5e-12,'conservative-timing Sharpe difference')
    ov=pd.read_csv(DATA/'PMT_STAGE2_DECISION_OVERLAP_SUMMARY_v1.0.csv')
    ov=ov[ov.block.eq('macro_plus_own')].iloc[0]
    check(abs(float(ov.disagreement_fraction)-0.5267857142857143)<1e-12,'conservative-timing Top-4 disagreement = 52.7%')
    latest=pd.read_csv(DATA/'HVR_STAGE2_SHARPE_DIFFERENCE_CI_v1.0.csv')
    lr=latest[latest.contrast.eq('REVISED_MACRO_PLUS_OWN_minus_OWN_ONLY')].iloc[0]
    check(abs(float(lr.point_difference)+0.06482070376765847)<5e-12,'latest-snapshot incremental Sharpe difference')
    # Random Top-4 descriptive placement.
    pl=pd.read_csv(DATA/'T23_RANDOM_TOP4_OBSERVED_PLACEMENT_v1.0.csv')
    pr=pl[(pl.strategy.eq('OWN_ONLY'))&(pl.random_metric.eq('information_ratio_vs_ew11'))].iloc[0]
    check(abs(float(pr.empirical_percentile_random_le_observed)-0.9953)<1e-12,'Price-only IR random Top-4 percentile = 99.53%')
    # Publication outputs must be generated. Exact figure bytes can vary across OS/font/renderer
    # stacks even when the underlying data, plotting code, labels, and geometry are unchanged.
    # Therefore public replay is cross-platform by default: tables are compared after newline
    # normalization, while figures are required to exist and be non-empty. Exact figure byte
    # hashes remain available as a strict release-environment audit.
    exp=json.loads((ROOT/'reference/metadata/expected_output_hashes.json').read_text())
    figure_hash_mismatches=[]
    for rel,hx in exp.items():
        p=out/rel
        check(p.exists(),f'generated output exists: {rel}')
        check(p.stat().st_size>0,f'generated output is non-empty: {rel}')
        if rel.startswith('tables/'):
            ref=ROOT/'reference'/rel
            norm=lambda q: Path(q).read_text(encoding='utf-8').replace('\r\n','\n').replace('\r','\n')
            check(norm(p)==norm(ref),f'generated table content matches reference: {rel}')
        else:
            if sha(p)==hx:
                print('PASS | exact figure byte hash matches reference: '+rel)
            else:
                figure_hash_mismatches.append(rel)
                if args.strict_output_hash:
                    raise AssertionError('generated output hash matches reference: '+rel)
                print('NOTE | figure regenerated but exact bytes differ from release reference: '+rel)
    if figure_hash_mismatches and not args.strict_output_hash:
        print('NOTE | Exact figure-byte identity is environment-sensitive; '+str(len(figure_hash_mismatches))+' figure file(s) differed. Numerical anchors, table contents, and figure generation completed successfully.')
    print('PASS - public paper-level validation complete.')

if __name__=='__main__': main()

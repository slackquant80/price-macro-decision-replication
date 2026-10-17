from pathlib import Path
import argparse, os, shutil, subprocess, sys, hashlib

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'reproduced'

def run(cmd,**kwargs):
    print('+',' '.join(map(str,cmd))); subprocess.run(cmd,check=True,**kwargs)

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def main():
    ap=argparse.ArgumentParser(description='Rebuild T23 paper-level outputs and validate the included evidence.')
    ap.add_argument('--strict-output-hash', action='store_true',
                    help='Require exact byte hashes for publication figures. Intended for the locked release environment; cross-platform public replay does not require this.')
    args=ap.parse_args()
    if OUT.exists(): shutil.rmtree(OUT)
    run([sys.executable,str(ROOT/'src/t23_paper_reproduction.py'),'--output-dir',str(OUT)])

    # Figure 1 is conceptual TikZ rather than an empirical output. Rebuild it when xelatex is available.
    if shutil.which('xelatex'):
        fdir=OUT/'figures'; fdir.mkdir(parents=True,exist_ok=True)
        build=OUT/'_figure1_build'; build.mkdir(parents=True,exist_ok=True)
        src=ROOT/'figure_sources/Figure_1_Where_Macro_Enters_HOUSE_v1.1.tex'; shutil.copy2(src,build/src.name)
        env=os.environ.copy(); env['SOURCE_DATE_EPOCH']='1787356800'; env['FORCE_SOURCE_DATE']='1'
        run(['xelatex','-interaction=nonstopmode','-halt-on-error',src.name],cwd=build,env=env,stdout=subprocess.DEVNULL)
        built=build/'Figure_1_Where_Macro_Enters_HOUSE_v1.1.pdf'
        ref=ROOT/'reference/figures/Figure_1_Where_Macro_Enters_HOUSE_v1.1.pdf'
        if sha(built)==sha(ref):
            print('PASS | Figure 1 exact byte hash matches release reference')
        elif args.strict_output_hash:
            raise RuntimeError('Figure 1 exact byte hash mismatch in strict mode')
        else:
            print('NOTE | Figure 1 rebuilt successfully; exact PDF bytes differ from the release environment (platform/TeX rendering variation).')
        shutil.copy2(built,fdir/'Figure_1_Where_Macro_Enters_HOUSE_v1.1.pdf')
        shutil.rmtree(build)
    else:
        print('SKIP | xelatex not found; empirical figures/tables will still be validated')

    run([sys.executable,str(ROOT/'src/build_t23_figure_3_incremental_wealth_v0_1.py'),'--output-dir',str(OUT)])
    cmd=[sys.executable,str(ROOT/'src/validate_public.py'),'--output-dir',str(OUT)]
    if args.strict_output_hash: cmd.append('--strict-output-hash')
    run(cmd)
    print('PASS - T23 reproduction complete.')

if __name__=='__main__': main()

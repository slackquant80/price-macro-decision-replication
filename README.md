# The Decision Value of Price and Macro Information - Replication Materials

This package reproduces the paper-level tables and figures for **The Decision Value of Price and Macro Information: Benchmark-Relative Evidence in Multi-Asset Allocation Using Historical-Vintage FRED-MD Data**.

## Scope

The package starts from versioned derived evidence produced by the scientific analysis. It independently rebuilds the paper's benchmark-relative statistics, robustness summaries, tables, and empirical figures. It does **not** refit the forecasting models, regenerate forecasts or rankings from raw market and macro data, or maintain a second scientific backtest.

The accompanying scientific analysis used 112 monthly out-of-sample allocation decisions from March 2017 through June 2026 across 11 U.S.-listed ETFs. The primary comparison asks whether adding historical-vintage macro information improves a price-based forecasting-and-ranking process under otherwise matched portfolio rules.

## What is reproduced

- Figure 1: conceptual information-flow diagram from deterministic TikZ source;
- Figure 2: price-based active value relative to the same-universe EW11 benchmark;
- Figure 3: incremental macro value across the main robustness checks;
- Figure 4: information-timing and information-set robustness;
- Figure 5: economic trade-offs relative to SPY/AGG 60/40;
- Figure 6: calendar-year Macro+Price minus Price-only return differences;
- Figure A1: Random Top-4 information-ratio distribution;
- Table 2: primary one-month-ahead results relative to EW11; and
- Table 3: primary one-month-ahead comparison with 60/40.

The validation script also independently recomputes headline portfolio statistics and checks the primary, conservative-timing, latest-snapshot, and Random Top-4 anchors used in the paper.

## One-command reproduction

Python 3.11+ is recommended.

```bash
python -m pip install -r requirements.txt
python reproduce.py
```

The command writes regenerated outputs to `reproduced/` and performs cross-platform validation of the numerical anchors, table contents, and generated figure files. Figure 1 is additionally rebuilt if `xelatex` is installed; the empirical figures and tables require only the Python dependencies listed in `requirements.txt`.

Publication figure PDFs/SVGs/PNGs can differ byte-for-byte across operating systems because font rendering, FreeType, Matplotlib backends, and PDF/SVG serialization are environment-sensitive. This is not treated as a public-replay failure when the numerical evidence and generated outputs validate. For the locked author release environment, exact figure-byte identity can be audited with:

```bash
python reproduce.py --strict-output-hash
```


## Information-timing boundary

The primary macro design uses historical monthly FRED-MD vintages. A monthly vintage label does not by itself prove exact within-month availability before a portfolio decision, so the paper does not describe the primary design as certified point-in-time or exact real-time data.

A prespecified conservative check uses:

```text
signal month t -> FRED-MD vintage t-1 -> latest macro reference month t-2
```

while own-price information remains available through signal month `t`.

The paper's incremental-macro conclusion is unchanged under this convention, while the realized Macro+Price Top-4 selection differs from the primary design in about 52.7% of months. A separate later-snapshot/calendar-truncated comparison changes revision state and, at some historical origins, series membership; it should not be interpreted as a pure numerical-revision test.

## Scientific-source identity

The final scientific source was clean-replayed in Windows / Python 3.11.9. That replay reproduced all 14,784 primary prediction rows and 3,696 ensemble-decision rows byte-for-byte. `SOURCE_IDENTITY.md` records the version hashes and the boundary between the scientific analysis and this paper-level replication package.

## Data and rights

The repository contains author-generated code, derived evidence, publication figures/tables, source identity metadata, and reproducibility checks. It does not redistribute downloaded raw market-price or FRED/FRED-MD source files. See `DATA_AND_RIGHTS.md`.

## Citation

If you use these materials, please cite the accompanying working paper. See `CITATION.cff`.

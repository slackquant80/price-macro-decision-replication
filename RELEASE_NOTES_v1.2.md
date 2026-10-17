# T23 paper-level replication v1.2 — release candidate

This update reproduces **one newly included Figure 3** in the author-approved 15-page T23 v2.18 paper using the existing, already-distributed, derived primary monthly net-return CSV. This is not a new backtest, a new forecast, or a replacement of the scientific source.

- `python reproduce.py` now renders the new relative-wealth exhibit and validates its 112-month accounting/relative-path anchors.
- End Macro+Price / Price-only cumulative net wealth ratio: 1.0204483508663122.
- Maximum drawdown **of that cumulative relative-wealth ratio**: −27.08482781362658%. It is not a single portfolio's max drawdown.
- 72 of 112 month-end cumulative ratio observations were below 1.
- The paper's primary incremental Sharpe difference remains negative (about −0.023) with an interval including zero. No robust macro-incremental superiority is claimed.
- New deterministic figure source and PDF, PNG, SVG are provided under `src/` and `reference/figures/`. Matplotlib SVG IDs use a fixed hashsalt.
- Files of the former v1.1 paper figures remain at their historical paths for reproducibility and backwards compatibility; Figure 4 (v2.18 paper) is stored under historical filename `Figure_3_Incremental_Macro_Value_with_RAW_HOUSE_v0.7` and subsequent original file numbers likewise refer to the v2.17 filename convention. README contains the paper-to-file crosswalk.
- Existing research source snapshot, data and frozen results are not changed.

Release gate: validate complete v1.2 ZIP/checkout via clean `python reproduce.py`, verify exact branch, then publicly release only after owner signoff; check actual Zenodo integration/archive record before claiming a DOI. SSRN manuscript revision is a separate author portal action.

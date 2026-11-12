# T23 Figure 1 v1.2 — source for the revised SSRN paper

The revised **15-page** [T23 SSRN paper #7340100](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7340100) uses a **Figure 1 v1.2** conceptual information-flow diagram. Its generator is `figure_sources/build_t23_fig01_house_v1_2.py`.

## Optional reproduction

Install the optional drawing dependency `python -m pip install reportlab`, and locate your system's Liberation Serif font directory containing `LiberationSerif-Regular.ttf` and `LiberationSerif-Bold.ttf`. Font files are **not** distributed here.

From the repository root, run:

```bash
python figure_sources/build_t23_fig01_house_v1_2.py reproduced/figures/Figure_1_Where_Macro_Enters_HOUSE_v1.2.pdf --font-dir "/absolute/path/to/liberation-fonts"
```

Output is a 480 × 95 pt vector PDF. PDF serialization and system-font differences may affect byte hashes across environments.

## Reproduction boundary and historical preservation

- The original v1.1 TikZ source `figure_sources/Figure_1_Where_Macro_Enters_HOUSE_v1.1.tex` and `reference/figures/Figure_1_Where_Macro_Enters_HOUSE_v1.1.pdf` remain unchanged.
- Existing `python reproduce.py` still rebuilds the **legacy v1.1 Figure 1** along with the empirical figures and tables. Figure 1 v1.2 is an **opt-in** supplemental source, not a replacement for the scientific reproduction program.
- No change to `requirements.txt`, `reproduce.py`, historical data, paper statistics, validation checks, GitHub Release v1.2 or previous Zenodo deposits.
- The figure is conceptual. This documentation-only supplement is not a new empirical result and does not entail another SSRN paper revision or a new DOI.

## Version identity

The November 12, 2026 downloaded SSRN paper PDF (15 pages) was byte-identical to the final author-approved file archived in the Investment Papers repository, SHA256 `ce0ac46e1d7c7d03f36b3b4da7d92989394781124aa54d449a9a17a895fda28a`. Rebuilding the standalone figure does not guarantee PDF byte identity across environments.

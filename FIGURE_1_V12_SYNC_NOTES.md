# T23 revised SSRN Figure 1 v1.2 — optional reproduction

**Paper:** [The Decision Value of Price and Macro Information, SSRN #7340100](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7340100), revised 12 November 2026 (15 pages).

The revised T23 Figure 1 is a **conceptual information-flow vector diagram**, not a scientific return/forecast experiment. Its exact author-maintained drawing logic is now preserved at:
`figure_sources/build_t23_fig01_house_v1_2.py`.

## Rebuild the current paper's conceptual Figure 1

Python 3.11+, `reportlab`, and locally installed **Liberation Serif Regular/Bold** fonts are required. Do **not** commit or distribute font files.

```bash
python -m pip install reportlab
python figure_sources/build_t23_fig01_house_v1_2.py reproduced/figures/Figure_1_Where_Macro_Enters_HOUSE_v1.2.pdf --font-dir /path/to/your/liberation-serif-font-directory
```

The font directory must contain `LiberationSerif-Regular.ttf` and `LiberationSerif-Bold.ttf`. Create `reproduced/figures` first if necessary (the generator also creates the target directory). The output is one 480×95pt vector PDF. Font/rendering metadata can vary across systems; PDF byte identity is not promised across platforms.

## Keep historical v1.1 reproduction frozen

The default `python reproduce.py` **intentionally continues to reproduce the legacy Figure 1 v1.1** TikZ source and the unchanged scientific figures, tables, CSV-based evidence and checks. That legacy command must **not** be described as producing the latest Figure 1 v1.2. To regenerate the current Figure 1, run the optional command above.

Do not replace or overwrite `figure_sources/Figure_1_Where_Macro_Enters_HOUSE_v1.1.tex`, `reference/figures/Figure_1_Where_Macro_Enters_HOUSE_v1.1.pdf`, historical hashes, figures, evidence, models, or data. This is an **additive source-and-documentation update**, not a numerical replication re-release.

## Release lineage

- Existing public [GitHub replication v1.2 release](https://github.com/slackquant80/price-macro-decision-replication/releases/tag/v1.2) dates from 17 October 2026. Git tags and old release assets remain immutable; they **predate this additive v1.2 conceptual illustration source** and cannot be assumed to include it.
- The final revised SSRN PDF downloaded by the author has SHA256 `ce0ac46e1d7c7d03f36b3b4da7d92989394781124aa54d449a9a17a895fda28a`, exactly matching the source-reviewed 15-page PDF already preserved in private `research-investment-papers`.
- No new Zenodo registration or DOI is implied by adding this source. Existing historical Zenodo deposits should retain their original content and version identity.

The canonical editable paper/figure source and its original source-native visual QA remain held in the private manuscript repository.

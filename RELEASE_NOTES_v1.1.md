# Release notes v1.1

This release changes only the public replay validator and dependency lock. It does not change the scientific evidence, portfolio results, figure data, or manuscript conclusions.

- Public replay now treats exact figure byte hashes as environment-sensitive rather than a cross-platform hard gate.
- Exact figure hashes remain available through `python reproduce.py --strict-output-hash` for the locked release environment.
- Table comparisons normalize line endings across Windows/Linux.
- Python dependencies are pinned to the tested release versions.

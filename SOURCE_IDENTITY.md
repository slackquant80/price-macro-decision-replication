# Scientific Source Identity

The paper-level replication package is bound to a separately validated scientific source for the forecasting and portfolio analysis.

## Source snapshot

- scientific source project: `12_MACRO_FORECAST_ALLOCATION`
- final scientific-source snapshot artifact SHA-256: `7a82eb75e0f88b67b659edff0d0bae922f7c1cfc0959c115cb15c641f9b0eb89`
- source content-manifest SHA-256: `d19b485046a33c28f440c4faab26521e8ab83f141cc15ade0e82e7515e8e5028`

## Clean replay

The final source was independently replayed in the locked scientific environment:

- Windows
- Python 3.11.9
- numpy 2.3.5
- pandas 2.2.3
- scikit-learn 1.8.0
- xgboost 3.1.3

The clean replay reproduced:

- 14,784 primary prediction rows byte-for-byte; and
- 3,696 ensemble-decision rows byte-for-byte.

The maximum numerical difference in replayed prediction and decision payloads was 0.0.

## Boundary

This public package begins from derived paper evidence. It does not redistribute the full scientific source snapshot or raw upstream data, and it does not refit models or regenerate the scientific forecasts and rankings. This separation prevents the publication layer from becoming a second scientific implementation.

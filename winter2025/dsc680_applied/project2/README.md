# Project 2 Data Sources

This project uses locally cached CSV files in `winter2025/dsc680_applied/project2/data/` so data is not downloaded every run.

## Primary source

- `data/sp500_daily.csv`
  - Source: `yfinance` API (`yf.download("^GSPC")`)
  - Underlying market data provider: Yahoo Finance S&P 500 index historical prices (`^GSPC`)
  - Notebook cell writes cache if file does not already exist.

## Derived from primary source

- `data/sp500_annual_returns_jan_to_jan.csv`
  - Source: computed from `sp500_daily.csv` (first available close in January, year-over-year Jan-to-Jan return)
- `data/annual_returns_with_politics.csv`
  - Source: `sp500_annual_returns_jan_to_jan.csv` + presidential party labels added in notebook
- `data/election_market_dataset.csv`
  - Source: `annual_returns_with_politics.csv` + election outcomes file; includes pre-election 2-year return and underperformance indicator
- `data/model_training_dataset.csv`
  - Source: engineered modeling features from `annual_returns_with_politics.csv`

## Election outcomes file

- `data/us_presidential_elections_1952_2024.csv`
  - Source: manually curated inside the notebook as a reproducible lookup table (not downloaded from an API in this version)
  - Fields: `election_year`, `incumbent_party`, `winner_party`

## Notebook

- Data loading, caching, and transformations are implemented in:
  - `vance_project2_milestone1_stock_market_vs_elections.ipynb`

## External references

- yfinance package/docs: https://pypi.org/project/yfinance/
- Yahoo Finance S&P 500 historical page (`^GSPC`): https://finance.yahoo.com/quote/%5EGSPC/history

## Simple Q&A (Milestone 2 Findings)

1. Why use January-to-January returns?
   We used one consistent yearly window for every year. It keeps comparisons clean and lines up better with election-cycle analysis.

2. How was party assigned in transition years?
   A year was labeled by the party in power for most of that Jan-to-Jan period. In inauguration years, this effectively follows the incoming administration period.

3. What tests were used to compare party returns?
   We used a few standard comparison checks (including a non-parametric one and a bootstrap range). They all pointed to the same result: no clear, reliable party advantage.

4. How reliable is the election CSV if it was manual?
   It is consistent and reproducible for this project, but manual files can still have entry mistakes. Best practice is to cross-check against a trusted public source.

5. How was "underperformance" defined, and what if the rule changes?
   Underperformance was defined as a negative combined market return in the two years before the election. Changing the cutoff changes percentages a bit, but the overall conclusion stayed weak.

6. Is the sample size strong enough for firm conclusions on incumbent losses?
   Not really. Presidential elections are a small sample, so this supports directional insights, not strong certainty.

7. Were outliers like 2008 or 2020 tested?
   Yes. Removing those years did not materially change the main conclusions.

8. Were macro factors controlled (inflation, Fed rates, recession, valuations)?
   No. This version is mostly a politics-plus-returns study, not a full macroeconomic model.

9. How was the 2026-2027 forecast validated, and what does the interval mean?
   It used time-based out-of-sample testing. The point estimate was around -3.3%, but the range was very wide, so it should be treated as a rough scenario, not a precise prediction.

10. How should findings be interpreted, and what are the ethical limits?
    Treat this as association, not causation. Results should be communicated with uncertainty and should not be presented as guaranteed investing advice.

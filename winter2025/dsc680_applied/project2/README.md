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

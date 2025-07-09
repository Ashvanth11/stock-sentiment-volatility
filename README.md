# stock-sentiment-volatility
# Social Sentiment vs. Stock Price Volatility

This project explores whether investor sentiment—gathered from Reddit and financial news—can predict short-term stock price volatility for popular publicly traded companies.

## Problem Statement

Can online sentiment metrics explain or anticipate stock price fluctuations?  
I focus on answering:
- Does sentiment **lead, lag**, or move **concurrently** with volatility?
- Which is more predictive: **news** sentiment or **Reddit** sentiment?
- Can lagged sentiment and volume features improve **volatility forecasting**?

## Data Sources

| Source      | Description                             | Tool Used |
|-------------|-----------------------------------------|-----------|
| Reddit      | Posts from r/stocks and r/wallstreetbets | PRAW |
| Financial News | Yahoo Finance & Google News headlines | BeautifulSoup |
| Market Data | OHLCV for 9 stocks                      | yfinance |

## Features Engineered

- **Lagged sentiment scores** (`news_sentiment_lag1`, `reddit_sentiment_lag1`)
- **Sentiment change** day over day
- **Discussion volume** (z-score normalized)
- **Lagged volatility** (optional model input)

## Modeling

- **Model Used:** Ridge Regression
- **Metrics:** RMSE, R²
- **Two Variants:**
  - Without `volatility_lag1`: pure sentiment model
  - With `volatility_lag1`: includes past volatility

| Model | Test RMSE | Test R² |
|-------|-----------|---------|
| Without lag | 0.0259 | 0.0256 |
| With lag | 0.0079 | **0.91** |

## Key Insights

- Lagged sentiment from news is **negatively correlated** with volatility.
- Reddit post volume is **positively correlated** with volatility.
- Including `volatility_lag1` boosts model performance drastically.
- Certain tickers (e.g., TSLA, PLTR) are **more sentiment-sensitive**.

## Repo Structure
```
data/            # Cleaned CSV datasets
notebooks/       # Jupyter analysis
report/          # Final PDF report
README.md        # Project documentation
.gitignore       # Git exclusions
requirements.txt # Required libraries
```
## Quick Setup

1. **Clone the repo:**
```bash
  git clone https://github.com/YOUR_USERNAME/stock-sentiment-volatility.git
  cd stock-sentiment-volatility
```

2.	**Install requirements**:
  ```
   pip install -r requirements.txt
  ```
3.	**Launch the notebook**:
   ```
   jupyter notebook notebooks/ashvanth_sentiment_volatility_analysis.ipynb
  ```
**Optional**:
If you see errors about missing NLTK data, run:
  ```
  import nltk
  nltk.download('vader_lexicon')
  nltk.download('stopwords')
  ```

## Limitations

- Short time window: March–April 2025 only
- Sentiment model (VADER) is lexicon-based and simplistic
- No macroeconomic indicators or financial ratios considered

## Future Work

- Use transformer-based sentiment (e.g., FinBERT)
- Include market indicators & earnings reports
- Try non-linear models like XGBoost or Random Forest
- Explore longer time horizons and per-stock models

---

**Author:** Ashvanth Rathinavel  
**Report:** [project_report.pdf](./report/project_report.pdf)

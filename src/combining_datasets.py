import pandas as pd
import os

# === Stock symbols list ===
TICKERS = ["TSLA", "NVDA", "BAC", "INTC", "AMZN", "PLTR", "AAPL", "HOOD", "META", "UNH"]

# === Initialize combined DataFrames ===
combined_market = pd.DataFrame()
combined_news = pd.DataFrame()
combined_reddit = pd.DataFrame()

# === Process each ticker ===
for symbol in TICKERS:
    # --- Volatility ---
    vol_file = f"data/{symbol}_volatility.csv"
    if os.path.exists(vol_file):
        df_vol = pd.read_csv(vol_file)
        df_vol["ticker"] = symbol
        combined_market = pd.concat([combined_market, df_vol], ignore_index=True)

    # --- News ---
    news_file = f"data/{symbol}_google_news.csv"
    if os.path.exists(news_file):
        df_news = pd.read_csv(news_file)
        df_news["ticker"] = symbol
        combined_news = pd.concat([combined_news, df_news], ignore_index=True)

    # --- Reddit ---
    reddit_file = f"data/{symbol}_reddit_bets_stocks.csv"
    if os.path.exists(reddit_file):
        df_reddit = pd.read_csv(reddit_file)
        df_reddit["ticker"] = symbol
        combined_reddit = pd.concat([combined_reddit, df_reddit], ignore_index=True)

# The data is being sorted with respect to ticker and date
# Market data has column "Date"
combined_market["Date"] = pd.to_datetime(combined_market["Date"])
combined_market.sort_values(["ticker","Date"], inplace=True)

# News has column "date"
combined_news["date"] = pd.to_datetime(combined_news["date"])
combined_news.sort_values(["ticker","date"], inplace=True)

# Reddit has column "created"
combined_reddit["created"] = pd.to_datetime(combined_reddit["created"])
combined_reddit.sort_values(["ticker","created"], inplace=True)

# === Save to CSV ===
combined_market.to_csv("combined_data/combined_market_data.csv", index=False)
combined_news.to_csv("combined_data/combined_news_data.csv", index=False)
combined_reddit.to_csv("combined_data/combined_reddit_data.csv", index=False)

print("Combined datasets created:")
print("- combined_market_data.csv")
print("- combined_news_data.csv")
print("- combined_reddit_data.csv")
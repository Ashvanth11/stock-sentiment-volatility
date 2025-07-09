import yfinance as yf
import feedparser
import praw
import pandas as pd
from datetime import datetime, timezone

ASSETS = [
    ("INTC", "Intel Corporation"),
    ("TSLA", "Tesla"),
    ("NVDA", "Nvidia"),
    ("BAC",  "Bank of America"),
    ("AMZN", "Amazon"),
    ("PLTR", "Palantir Technologies"),
    ("AAPL", "Apple"),
    ("HOOD", "Robinhood Markets"),
    ("META", "Meta Platforms"),
    ("UNH", "UnitedHealth Group"),
]

START_DATE = "2025-03-01"
END_DATE   = "2025-04-15"

# search both r/wallstreetbets and r/stocks
REDDIT_SUBS  = ["wallstreetbets", "stocks"]
REDDIT_LIMIT = 1000

# Initialize Reddit client
reddit = praw.Reddit(
    client_id='VZVn9FDKXJaUgWg6m9IYXQ',
    client_secret='TB3B_VPyrjSZgy-YrEnvb22OnIFgrQ',
    user_agent='stock-analysis-script'
)

ASSETS = [
    ("INTC", "Intel Corporation"),
    ("TSLA", "Tesla"),
    ("NVDA", "Nvidia"),
    ("BAC",  "Bank of America"),
    ("AMZN", "Amazon"),
    ("PLTR", "Palantir Technologies"),
    ("AAPL", "Apple"),
    ("HOOD", "Robinhood Markets"),
    ("META", "Meta Platforms"),
    ("UNH", "UnitedHealth Group"),
]

START_DATE = "2025-03-01"
END_DATE   = "2025-04-15"

# search both r/wallstreetbets and r/stocks
REDDIT_SUBS  = ["wallstreetbets", "stocks"]
REDDIT_LIMIT = 1000

# Initialize Reddit client
reddit = praw.Reddit(
    client_id='VZVn9FDKXJaUgWg6m9IYXQ',
    client_secret='TB3B_VPyrjSZgy-YrEnvb22OnIFgrQ',
    user_agent='stock-analysis-script'
)

def fetch_volatility(symbol):
    df = (
        yf.Ticker(symbol)
          .history(start=START_DATE, end=END_DATE, interval="1d")
          .reset_index()[["Date","Open","High","Low","Close","Volume"]]
    )
    df.to_csv(f"data/{symbol}_volatility.csv", index=False)
    print(f"{symbol} volatility: {len(df)} rows")
    return df

def fetch_google_news(symbol, name):
    q = f"{symbol}+OR+{name.replace(' ','+')}"
    rss_url = (
        "https://news.google.com/rss/search?"
        f"q={q}+after:{START_DATE}+before:{END_DATE}"
        "&hl=en-US&gl=US&ceid=US:en"
    )
    feed = feedparser.parse(rss_url)
    recs = []
    for e in feed.entries:
        dt = datetime.strptime(e.published, "%a, %d %b %Y %H:%M:%S %Z")
        recs.append({
            "date":  dt.strftime("%Y-%m-%d"),
            "title": e.title,
            "url":   e.link
        })
    df = pd.DataFrame(recs)
    df.to_csv(f"data/{symbol}_google_news.csv", index=False)
    print(f"{symbol} news: {len(df)} headlines")
    return df

def fetch_reddit(symbol, name):
    start_dt = datetime.fromisoformat(START_DATE).replace(tzinfo=timezone.utc)
    end_dt   = datetime.fromisoformat(END_DATE).replace(tzinfo=timezone.utc)
    term = f"{symbol} OR {name}"
    recs = []
    for sub in REDDIT_SUBS:
        for subm in reddit.subreddit(sub).search(term, sort="new", limit=REDDIT_LIMIT):
            created = datetime.fromtimestamp(subm.created_utc, tz=timezone.utc)
            if start_dt <= created < end_dt:
                recs.append({
                    "subreddit": sub,
                    "title":     subm.title,
                    "score":     subm.score,
                    "created":   created.strftime("%Y-%m-%d %H:%M:%S"),
                    "url":       subm.url
                })
    df = pd.DataFrame(recs)
    df.to_csv(f"data/{symbol}_reddit_bets_stocks.csv", index=False)
    print(f"{symbol} reddit: {len(df)} posts from {REDDIT_SUBS}")
    return df

if __name__ == "__main__":
    for symbol, name in ASSETS:
        print(f"\nProcessing {symbol} ({name}) ...")
        fetch_volatility(symbol)
        fetch_google_news(symbol, name)
        fetch_reddit(symbol, name)
    print("\nAll datasets fetched and saved.")
import yfinance as yf
import pandas as pd
from datetime import datetime
import os

def download_data(tickers, start_date, end_date, filename="data/stock_prices.csv"):
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    data = yf.download(tickers, start = start_date, end = end_date, progress = False)
    
    if data is None or data.empty:
        print("❌ No data found for the given tickers or date range.")
        return

    try:
        adj_close = data["Close"]
    except (KeyError, TypeError):
        adj_close = data if isinstance(data, pd.DataFrame) else None

    if adj_close is None or adj_close.empty:
        print("❌ No adjusted close price data available.")
        return
    
    if isinstance(tickers, str):
        adj_close.columns = [tickers]
    elif len(tickers) == 1: 
        adj_close.columns = [tickers[0]]

    adj_close.dropna().to_csv(filename)
    print(f"✅ Saved data to {filename}")

if __name__ == "__main__":
    tickers = ["TSLA", "AAPL", "NVDA", "MSFT", "GOOG"]
    today = datetime.today().strftime("%Y-%m-%d")
    download_data(tickers, start_date="2022-01-01", end_date=today)
import yfinance as yf
import pandas as pd
from datetime import date, datetime

tickers = ["AAPL","THYAO.IS","GOOG","MSFT"]

# data = yf.download(tickers,start="2021-08-03",end="2026-08-03")

# data.to_csv("4_ticker_data.csv")

datas = pd.read_csv("4_ticker_data.csv")

print(datas.head())
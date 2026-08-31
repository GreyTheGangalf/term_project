import time
import pandas as pd
import yfinance as yf
import numpy as np

crypto_tickers = ["BTC-USD", "ETH-USD", "SOL-USD"]


raw_data = yf.download(crypto_tickers, period="10y")


clean_data = raw_data.stack(level=1, future_stack=True).reset_index()

clean_data.rename(columns={'level_1': 'Ticker'}, inplace=True)

final_df = clean_data[['Date', 'Ticker', 'Open', 'Close', 'High', 'Low', 'Volume']].copy()

final_df['Date'] = pd.to_datetime(final_df['Date']).dt.tz_localize(None)

final_df.insert(loc=7,column='Currency',value='USD')

crypto_ohlcv_df = final_df

crypto_ohlcv_df.to_csv('crypto_ohlcv.csv',index=False)


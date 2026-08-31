import pandas as pd
import yfinance as yf

commodity_tickers = ["GC=F", "CL=F", "HG=F", "SI=F"]

datas = []

for ticker in commodity_tickers:

    print(f'Retrieving data for {ticker}')

    commodity = yf.Ticker(ticker)

    hist = commodity.history(period="11y")

    if hist.empty:
        print(f'No data found for {ticker},skipping.')
        continue

    ticker_data = hist[["Open","Close","High","Low","Volume"]].copy()

    ticker_data = ticker_data.reset_index()

    ticker_data['Date'] = pd.to_datetime(ticker_data['Date']).dt.tz_localize(None)

    ticker_data.insert(1,column='Ticker',value=ticker)

    ticker_data.insert(7,column='Currency',value='USD')

    datas.append(ticker_data)

if datas:
    commodity_df = pd.concat(datas,ignore_index=True)
    commodity_df.to_csv('commodities_price_history.csv',index=False)
else:
    print(f'No data.')








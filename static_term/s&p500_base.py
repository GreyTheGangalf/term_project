import io
import time
from operator import index
import yfinance as yf
import pandas as pd
import requests

url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'

headers = {
    "User-Agent" : (
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        ' (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
    )
}

response = requests.get(url, headers= headers)

tmp_sp500_table = pd.read_html(io.StringIO(response.text))[0]


tickers = [
    ticker.replace('.','-') for  ticker in tmp_sp500_table['Symbol'].tolist()
]


target_metrices_whitelist = [
    "Total Revenue",
    "Gross Profit",
    "Operating Income",
    "Net Income",
    "Diluted EPS",
    "Research And Development",
    "Total Assets",
    "Total Liabilities Net Minority Interest",
    "Total Debt",
    "Stockholders Equity",
    "Cash And Cash Equivalents",
    "Ordinary Shares Number",
    "Operating Cash Flow",
    "Free Cash Flow",
    "Capital Expenditure"]

datas = []

for index,ticker in enumerate(tickers,start=1):
    try:
        print(f'Retrieving data for {ticker}')
        share = yf.Ticker(ticker)

        fin = share.financials.T
        bs = share.balance_sheet.T
        cf = share.cashflow.T

        if fin.empty and bs.empty and cf.empty:
            print(f'{ticker} has no data, skipping.')
            continue

        u_table = pd.concat([fin,bs,cf], axis=1)
        u_table = u_table.reindex(columns=target_metrices_whitelist)

        u_table = u_table.reset_index()
        u_table.rename(columns={'index' : 'Date'},inplace=True)
        u_table.insert(1,'Ticker',ticker)

        datas.append(u_table)

        time.sleep(0.2)

    except Exception as e:
        print(f'Error on retrieving {ticker} data.')
        continue

if datas:
    sp500_table = pd.concat(datas, ignore_index=True)
    sp500_table.to_csv("sp500_table.csv",index = False)
    print(sp500_table)
else:
    print(f'No data on {datas}.')


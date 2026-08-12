import time
import requests
import borsapy
import pandas as pd
import io

url = 'https://en.wikipedia.org/wiki/List_of_companies_listed_on_the_Borsa_Istanbul'

headers = {
    "User-Agent": (
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        ' (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
    )
}
response = requests.get(url, headers=headers)

wiki_tables = pd.read_html(io.StringIO(response.text))

for table in wiki_tables:
    if 'Symbol' in table.columns:
        tmp_bist_table = table

bist_tickers = tmp_bist_table['Symbol'].tolist()

clean_tickers = []

for x in bist_tickers:
    if isinstance(x,str) and '[' not in x:
        clean_tickers.append(x.split(',')[0].strip())

bist_tickers = clean_tickers

print(bist_tickers)

borsapy_to_yfinance_map = {
    "Hasılat": "Total Revenue",
    "Satış Gelirleri": "Total Revenue",
    "Brüt Kar (Zarar)": "Gross Profit",
    "Esas Faaliyet Karı (Zararı)": "Operating Income",
    "Net Dönem Karı (Zararı)": "Net Income",
    "Araştırma ve Geliştirme Giderleri (-)": "Research And Development",
    "Toplam Varlıklar": "Total Assets",
    "Toplam Yükümlülükler": "Total Liabilities Net Minority Interest",
    "Ana Ortaklığa Ait Özkaynaklar": "Stockholders Equity",
    "Toplam Özkaynaklar": "Stockholders Equity",
    "Nakit ve Nakit Benzerleri": "Cash And Cash Equivalents",
    "İşletme Faaliyetlerinden Nakit Akışları": "Operating Cash Flow",
    "Maddi ve Maddi Olmayan Duran Varlık Alımından Kaynaklanan Nakit Çıkışları": "Capital Expenditure",
    "Serbest Nakit Akışı": "Free Cash Flow"
}

bist_datas = []

for index, ticker in enumerate(bist_tickers, start=1):
    try:
        print(f'Retrieving data of {ticker}.')
        share = borsapy.Ticker(ticker)

        fin = share.get_income_stmt().T
        bs = share.get_balance_sheet().T
        cf = share.get_cashflow().T

        if fin.empty and bs.empty and cf.empty:
            print(f'{ticker} has no data, skipping.')
            continue

        u_table = pd.concat([fin, bs, cf], axis=1)

        u_table.columns = u_table.columns.str.strip()

        u_table = u_table.loc[:, ~u_table.columns.duplicated(keep='first')]

        u_table = u_table.rename(columns=borsapy_to_yfinance_map)

        target_columns = list(set(borsapy_to_yfinance_map.values()))

        for col in target_columns:
            if col not in u_table.columns:
                u_table[col] = pd.NA

        u_table = u_table.loc[:, ~u_table.columns.duplicated()][target_columns]

        u_table = u_table.reset_index()

        u_table.rename(columns={'index': 'Date'}, inplace=True)

        u_table['Date'] = pd.to_datetime(u_table['Date'].astype(str) + '-12-31')

        u_table.insert(loc=0, column='Ticker', value=ticker)

        bist_datas.append(u_table)
        print(f'{ticker} successfully processed.')

    except Exception as e:
        print(f'Error on retrieving {ticker} data. {str(e)}')
        continue

if bist_datas:
    bist_table = pd.concat(bist_datas, ignore_index=True)
    bist_table.to_csv('bist_table.csv', index=False)
    print(bist_table)
else:
    print(f'No data on {bist_datas}')
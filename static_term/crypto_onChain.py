import pandas as pd
import requests
import time

coinGecko_apiKey = 'CG-foXmhGi5JaC9sNTYCnmbwVUX'

coins = ["bitcoin","ethereum","solana"]

headers = {
    "x-cg-demo-api-key": "CG-foXmhGi5JaC9sNTYCnmbwVUX"
}

datas = []

for coin_id in coins:
    print(f'Retrieving {coin_id} data')

    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"

    params = {
        "vs_currency" : "usd",
        "days" : "365",
        "interval" : "daily"
    }

    response = requests.get(url, params=params, headers=headers)

    if  response.status_code == 200:
        data = response.json()

        prices = data.get("prices",[])
        market_caps = data.get("market_caps",[])
        total_volumes = data.get("total_volumes",[])

        df_price = pd.DataFrame(prices, columns=["Timestamp", "Price"])
        df_mc = pd.DataFrame(market_caps, columns=["Timestamp", "Market_Cap"])
        df_vol = pd.DataFrame(total_volumes, columns=["Timestamp", "Volume"])

        tmp_df = df_price.merge(df_mc, on="Timestamp").merge(df_vol, on="Timestamp")

        tmp_df['Date'] = pd.to_datetime(tmp_df['Timestamp'], unit='ms').dt.normalize()

        tmp_df['Coin'] = coin_id.upper()
        tmp_df['Currency'] = 'USD'

        tmp_df = tmp_df[['Date', 'Coin', 'Price', 'Market_Cap', 'Volume', 'Currency']]

        datas.append(tmp_df)
        print(f'{coin_id} retrieved successfully.')

        time.sleep(1.5)
    else:
        print(f'Error {response.status_code},{response.text}')

if datas:
    crypto_onChain_df = pd.concat(datas,ignore_index=True)
    crypto_onChain_df.to_csv("crypto_onChain_df.csv",index=False)
    print(crypto_onChain_df.head(10))
else:
    print('No data.')
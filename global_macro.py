#  EVDS API
import pandas as pd
from Tools.scripts.pindent import start
from evds import evdsAPI
from fredapi import Fred
import evds

#Fred
fred = Fred(api_key='6898119af8354781f2150e482fe1fbad')

series_dict = {
    'FEDFUNDS' : 'Policy_Rate',
    'CPIAUCSL' : 'Inflation_CPI',
    'M2SL' : 'M2_Money_Supply',
    'UNRATE' : 'Unemployment_Rate'
}
df_list = []

for code,name in series_dict.items():
    series = fred.get_series(code)
    df = pd.DataFrame(series,columns=[name])
    df_list.append(df)

global_macro_df = pd.concat(df_list)
print(global_macro_df)

global_macro_df.index.name = 'Date'
global_macro_df = global_macro_df.sort_index()

print(global_macro_df)

#global_macro_df.to_csv('global_macro_df.csv')

#EVDS
evdsAPI = evds.evdsAPI(key='wlFmt2HYGf')

series_list = [
    'TP.FG.J0',
    'TP_DK_USD_S_YTL',
    'TP_MB_FAIZ_KOR2',
]

local_df = evdsAPI.get_data(series_list, startdate='01-08-2021', enddate='01-08-2026')

local_df.rename(columns={
    'Tarih': 'Date',
    'TP_FG_J0': 'Inflation_CPI_TR',
    'TP_DK_USD_S_YTL': 'USD_TRY',
    'TP_MB_FAIZ_KOR2': 'Policy_Rate_TR'
}, inplace=True)

print(local_df)



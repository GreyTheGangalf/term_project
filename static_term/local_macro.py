import pandas as pd
import evds

evdsAPI = evds.evdsAPI('wlFmt2HYGf')

series_dict = {
    'TP.APIFON4': 'Policy_Rate',
    'TP.FG.J0': 'Inflation_CPI',
    'TP.TIG07': 'Unemployment_Rate',
    'TP.PBD.H09': 'M2_Money_Supply',
    'TP.DK.USD.A.YTL' : 'USD_TRY'
}

start_date = "01-01-2015"
end_date = "05-08-2026"

local_df_list = []

for code, name in series_dict.items():
    try:
        print(f"Retrieving: {name} ({code})")
        tmp_df = evdsAPI.get_data([code], startdate=start_date, enddate=end_date)

        evds_col_name = code.replace('.', '_')

        if evds_col_name not in tmp_df.columns:
            print(f"Table {code} is empty,skipping.")
            continue

        tmp_df = tmp_df[['Tarih', evds_col_name]].copy()

        tmp_df['Tarih'] = pd.to_datetime(tmp_df['Tarih'], dayfirst=True, errors='coerce')
        tmp_df = tmp_df.dropna(subset=['Tarih'])

        tmp_df.rename(columns={'Tarih': 'Date', evds_col_name: name}, inplace=True)
        tmp_df.set_index('Date', inplace=True)

        tmp_df = tmp_df[~tmp_df.index.duplicated(keep='last')]

        local_df_list.append(tmp_df)
        print(f"{name} has successfully gathered.")

    except Exception as e:
        print(f'Error - {name} ({code}): {e}')

if local_df_list:
    print("\nThe data is being aligned by daily frequency...")

    master_df = pd.concat(local_df_list, axis=1)
    master_df = master_df.sort_index()

    full_date_range = pd.date_range(start=master_df.index.min(), end=master_df.index.max(), freq='D')

    master_df = master_df.reindex(full_date_range)
    master_df.index.name = 'Date'

    master_df.ffill(inplace=True)
    master_df.bfill(inplace=True)

    print(master_df.head())

    master_df.to_csv('local_macro.csv')
else:
    print("No data has been gathered.")
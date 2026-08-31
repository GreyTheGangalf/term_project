import pandas as pd
import json
import os
import sys
from langchain_core.tools import tool

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from db_config import engine

@tool
def get_local_macro_data(target_date: str) -> str:

    """
    Retrieves the most recent available macroeconomic data for Turkey as of the date specified by the agent.
    Parameter: target_date (e.g., ‘2026-05-15’)
    Return: Text in JSON format.
    """

    query = """
        SELECT * 
        FROM local_macro
        WHERE "Date" <= %(target_date)s 
        ORDER BY "Date" DESC 
        LIMIT 1;
    """
    try:
        df = pd.read_sql(query, engine, params={"target_date": target_date})
        
        if df.empty:
            return json.dumps({"error": f"{target_date} tarihinden öncesine ait makro veri bulunamadı."})
        
        result_dict = df.iloc[0].to_dict()
        
        date_val = result_dict.get("Date")
        if pd.notnull(date_val):
            result_dict["Date"] = date_val.strftime('%Y-%m-%d') if hasattr(date_val, 'strftime') else str(date_val).split()[0]
            
        return json.dumps(result_dict, indent=2, ensure_ascii=False)
        
    except Exception as e:
        return json.dumps({"error": f"Database error: {str(e)}"})
    pass

@tool
def get_fundamental_data(ticker: str, target_date: str) -> str:
    """
    Retrieves the most recent balance sheet/fundamental analysis data for the specified stock (ticker) as of the given date.
    Parameters:
        - ticker (e.g., ‘THYAO.IS’ or ‘AAPL’)
        - target_date (e.g., ‘2026-05-15’)
    Return: Fundamental analysis data in JSON format.
    """

    table_names = ["bist_table", "sp500_table"] 
    
    for table_name in table_names:
        query = f"""
            SELECT * 
            FROM {table_name}
            WHERE "Ticker" = %(ticker)s AND "Date" <= %(target_date)s 
            ORDER BY "Date" DESC 
            LIMIT 1;
        """
        try:
            df = pd.read_sql(query, engine, params={"ticker": ticker, "target_date": target_date})
            
            if not df.empty:
                result_dict = df.iloc[0].to_dict()
                
                date_val = result_dict.get("Date")
                if pd.notnull(date_val):
                    result_dict["Date"] = date_val.strftime('%Y-%m-%d') if hasattr(date_val, 'strftime') else str(date_val).split()[0]
                    
                return json.dumps(result_dict, indent=2, ensure_ascii=False)
        except Exception:
            continue
            
    return json.dumps({"error": f"{ticker} hissesi için {target_date} tarihinden öncesine ait veri bulunamadı."})
    pass

if __name__ == "__main__":
    print(get_local_macro_data("2025-03-15"))
    print("---------------------------------")
    print(get_fundamental_data("THYAO", "2025-12-31"))
    print("---------------------------------")
    print(get_fundamental_data("AAPL", "2025-08-10"))
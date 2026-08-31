print("1. Loading libraries...")
import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

print("2. Libraries have been loaded. Reading the .env file...")
load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME")

print(f"3. Information retrieved -> Host: {DB_HOST}, Database: {DB_NAME}")
print("4. The PostgreSQL engine is being created...")

try:
    engine = create_engine(f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
    
    if __name__ == "__main__":
        print("5. A connection request is being sent to the database (If this step takes a long time, the password or port is incorrect)...")
        test_df = pd.read_sql("SELECT * FROM sp500_table LIMIT 5", engine)
        
        print("\n--- CONNECTION SUCCESSFUL! First 5 Lines ---")
        print(test_df)

except Exception as e:
    print(f"\n--- AN ERROR OCCURRED ---")
    print(e)
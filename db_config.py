import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv


load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME")


engine = create_engine(f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

if __name__ == "__main__":
    try:
        test_df = pd.read_sql("SELECT * FROM sp500_table LIMIT 5", engine)
        print("Veritabanı bağlantısı başarılı! İlk 5 satır:")
        print(test_df.head())
    except Exception as e:
        print(f"Bağlantı hatası yaşandı: {e}")
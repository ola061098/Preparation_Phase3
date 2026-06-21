import sys
sys.path.insert(0, r"C:\Users\ola06\OneDrive\Desktop\Summit_Python\Python_SQL_combined")

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from config import OUTPUT_DIR, get_engine
import seaborn as sns

def load_prices(engine):
    query = """
        SELECT datetime, price_de_lu
        FROM "Prices_NO1_DE_LU"
        ORDER BY datetime
    """
    df = pd.read_sql(query, engine)
    df["datetime"] = pd.to_datetime(df["datetime"])
    df.to_csv(r"C:\Users\ola06\OneDrive\Desktop\Summit_Python\Python_SQL_combined\price_with_generation.csv", index=False)
    return df

def calculates_peak_off_peak(df):
    df["hour"] = df["datetime"].dt.hour
    df["is_peak"] = df["hour"].apply(lambda x: 1 if 8 <= x < 20 else 0)
    average_prices_peak = df[df["is_peak"] == 1]["price_de_lu"].mean()
    average_prices_off_peak = df[df["is_peak"] == 0]["price_de_lu"].mean()
    print(f"Average price during peak hours: {average_prices_peak:.2f} EUR/MWh")
    print(f"Average price during off-peak hours: {average_prices_off_peak:.2f} EUR/MWh")

load_prices(get_engine())
calculates_peak_off_peak(load_prices(get_engine()))
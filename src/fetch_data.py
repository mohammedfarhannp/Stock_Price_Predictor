# fetch_data.py
import yfinance as yf
import pandas as pd
import os

from config import STOCK_SYMBOL, START_DATE, END_DATE, DATA_RAW_DIR
from datetime import datetime

def fetch_stock_data():
    print(f"Fetching data for {STOCK_SYMBOL}...")
    
    # Check if today is weekend
    today = datetime.now().date()
    if today.weekday() >= 5:  # Saturday or Sunday
        print("[+] Today is a weekend. Using last available trading day.")
        # Use Friday's date as end date
        end_date = today - timedelta(days=(today.weekday() - 4))
    else:
        end_date = datetime.now().strftime('%Y-%m-%d')
    
    try:
        # Download data
        stock = yf.download(STOCK_SYMBOL, 
                           start=START_DATE, 
                           end=end_date,
                           progress=False)
        
        if stock.empty:
            print("[-] No data found. Check symbol or date range.")
            return None
        
        # Reset index to make Date a column
        stock.reset_index(inplace=True)
        
        # Save to CSV
        filename = f"{STOCK_SYMBOL.replace('.', '_')}_{START_DATE}_to_{end_date}.csv"
        filepath = os.path.join(DATA_RAW_DIR, filename)
        stock.to_csv(filepath, index=False)
        
        print(f"[+] Data saved to: {filepath}")
        print(f"[+] Records downloaded: {len(stock)} days")
        print(f"[+] Date range: {stock['Date'].min()} to {stock['Date'].max()}")
        
        return filepath
        
    except Exception as e:
        print(f"[-] Error fetching data: {e}")
        return None

if __name__ == "__main__":
    # Test the function
    fetch_stock_data()
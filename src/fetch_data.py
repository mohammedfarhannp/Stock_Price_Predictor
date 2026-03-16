# fetch_data.py (fixed for proper historical data)
import pandas as pd
from datetime import datetime, timedelta
import os
import time
from config import STOCK_SYMBOL, START_DATE, END_DATE, DATA_RAW_DIR

# Remove .NS suffix for nselib
STOCK_NAME = STOCK_SYMBOL.replace('.NS', '')

def fetch_stock_data():
    """
    Download stock data from NSE India using nselib
    """
    print(f"Fetching data for {STOCK_NAME} from NSE India...")
    
    # Use a much longer historical period
    # Let's get 2 years of data to ensure enough for 60-day sequences
    end_date = datetime.now()
    start_date = end_date - timedelta(days=730)  # 2 years
    
    start_date_str = start_date.strftime('%d-%m-%Y')
    end_date_str = end_date.strftime('%d-%m-%Y')
    
    print(f"[+] Fetching from {start_date_str} to {end_date_str}...")
    
    try:
        from nselib import capital_market
        
        # Try different methods to get historical data
        methods = [
            lambda: capital_market.price_volume_and_deliverable_position_data(
                symbol=STOCK_NAME,
                from_date=start_date_str,
                to_date=end_date_str
            ),
            lambda: capital_market.historical_data(
                symbol=STOCK_NAME,
                from_date=start_date_str,
                to_date=end_date_str
            )
        ]
        
        data = None
        for i, method in enumerate(methods):
            try:
                print(f"   Attempt {i+1}...")
                data = method()
                if data is not None and not data.empty:
                    print(f"   [+] Success with method {i+1}")
                    break
            except Exception as e:
                print(f"   [-] Method {i+1} failed: {str(e)[:50]}")
                continue
        
        if data is None or data.empty:
            print("[-] No data returned from NSE.")
            return None
        
        # Rename columns
        data = data.rename(columns={
            'DATE': 'Date',
            'OPEN': 'Open',
            'HIGH': 'High', 
            'LOW': 'Low',
            'CLOSE': 'Close',
            'VOLUME': 'Volume'
        })
        
        # Convert date format
        data['Date'] = pd.to_datetime(data['Date'], format='%d-%b-%Y').dt.strftime('%d/%m/%Y')
        
        # Sort by date
        data = data.sort_values('Date')
        
        print(f"[+] Data fetched successfully!")
        print(f"[+] Records downloaded: {len(data)} days")
        print(f"[+] Date range: {data['Date'].iloc[0]} to {data['Date'].iloc[-1]}")
        
        # Save to CSV
        filename = f"{STOCK_NAME}_NSE_historical.csv"
        filepath = os.path.join(DATA_RAW_DIR, filename)
        data.to_csv(filepath, index=False)
        
        print(f"[+] Data saved to: {filepath}")
        
        return filepath
        
    except ImportError:
        print("[-] nselib not installed. Installing now...")
        os.system('pip install nselib')
        return None
    except Exception as e:
        print(f"[-] Error fetching data: {e}")
        return None

if __name__ == "__main__":
    fetch_stock_data()
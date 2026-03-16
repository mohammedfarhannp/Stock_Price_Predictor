# update_stock_data.py
import pandas as pd
from datetime import datetime, timedelta
import os
import sys
from nselib import capital_market

# Add src to path if needed
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

CSV_FILE = "data/raw/ROLEXRINGS_NS_2025-01-01_to_CURRENT.csv"
STOCK_SYMBOL = "ROLEXRINGS"

def get_last_date_from_csv():
    """Get the last date in the CSV file"""
    if not os.path.exists(CSV_FILE):
        print(f"[-] CSV file not found: {CSV_FILE}")
        return None, None
    
    df = pd.read_csv(CSV_FILE)
    df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y')
    last_date = df['Date'].max().date()
    return last_date, df

def is_trading_day(date):
    """Check if date is a weekday (Mon-Fri)"""
    return date.weekday() < 5

def generate_missing_dates(last_date, today):
    """Generate list of missing trading days between last_date and today"""
    missing_dates = []
    current = last_date + timedelta(days=1)
    
    while current <= today:
        if is_trading_day(current):
            missing_dates.append(current)
        current += timedelta(days=1)
    
    return missing_dates

def fetch_nse_data(from_date, to_date):
    """
    Fetch stock data from nselib and map to required format
    """
    try:
        # Format dates for nselib (DD-MM-YYYY)
        from_str = from_date.strftime('%d-%m-%Y')
        to_str = to_date.strftime('%d-%m-%Y')
        
        print(f"   Fetching data from {from_str} to {to_str}...")
        
        # Fetch data from nselib
        data = capital_market.price_volume_and_deliverable_position_data(
            symbol=STOCK_SYMBOL,
            from_date=from_str,
            to_date=to_str
        )
        
        if data is None or data.empty:
            print("   ❌ No data returned")
            return None
        
        # Map to required format
        mapped_data = pd.DataFrame({
            'Date': pd.to_datetime(data['Date']).dt.strftime('%d/%m/%Y'),
            'Open': data['OpenPrice'],
            'High': data['HighPrice'],
            'Low': data['LowPrice'],
            'Close': data['ClosePrice'],
            'Volume': data['TotalTradedQuantity']
        })
        
        # Sort by date
        mapped_data = mapped_data.sort_values('Date')
        
        return mapped_data
        
    except Exception as e:
        print(f"   ❌ Error fetching data: {e}")
        return None

def update_csv_with_missing_dates():
    """Main function to update CSV with missing dates using nselib"""
    print("=" * 60)
    print("STOCK DATA UPDATER - NSELIB REAL DATA MODE")
    print("=" * 60)
    
    # Check if file exists
    if not os.path.exists(CSV_FILE):
        print(f"[-] File not found: {CSV_FILE}")
        print("[+] Creating new file with complete data...")
        
        # Fetch all data from 2025-01-01 to today
        start_date = datetime(2025, 1, 1).date()
        end_date = datetime.now().date()
        
        new_data = fetch_nse_data(start_date, end_date)
        
        if new_data is not None:
            new_data.to_csv(CSV_FILE, index=False)
            print(f"[+] Created new CSV with {len(new_data)} records")
            print(f"[+] Date range: {new_data['Date'].iloc[0]} to {new_data['Date'].iloc[-1]}")
            return True
        else:
            print("[-] Failed to fetch initial data")
            return False
    
    # Get last date from CSV
    last_date, df = get_last_date_from_csv()
    today = datetime.now().date()
    
    print(f"\n[+] Last date in CSV: {last_date.strftime('%d/%m/%Y')}")
    print(f"[+] Today's date: {today.strftime('%d/%m/%Y')}")
    
    # Find missing trading days
    missing = generate_missing_dates(last_date, today)
    
    if not missing:
        print("[+] CSV is already up to date!")
        return True
    
    print(f"[+] Missing {len(missing)} trading days:")
    for date in missing:
        print(f"    - {date.strftime('%Y-%m-%d')}")
    
    # Fetch data for missing dates
    print("\n[+] Fetching REAL data from NSE via nselib...")
    
    # Fetch from day after last_date to today
    fetch_start = last_date + timedelta(days=1)
    fetch_end = today
    
    new_data = fetch_nse_data(fetch_start, fetch_end)
    
    if new_data is None or new_data.empty:
        print("[-] Failed to fetch new data")
        return False
    
    print(f"\n[+] Successfully fetched {len(new_data)} days of real data")
    
    # Append to existing CSV
    updated_df = pd.concat([df, new_data], ignore_index=True)
    
    # Remove duplicates (keep last occurrence)
    updated_df = updated_df.drop_duplicates(subset=['Date'], keep='last')
    
    # Sort by date
    updated_df['Date_dt'] = pd.to_datetime(updated_df['Date'], format='%d/%m/%Y')
    updated_df = updated_df.sort_values('Date_dt').drop('Date_dt', axis=1)
    
    # Save back to CSV
    updated_df.to_csv(CSV_FILE, index=False)
    
    print(f"\n[+] CSV updated successfully!")
    print(f"[+] Total records: {len(updated_df)}")
    print(f"[+] New last date: {updated_df['Date'].iloc[-1]}")
    
    return True

def get_price_for_date(target_date):
    """Get stock details for a specific date from CSV"""
    if not os.path.exists(CSV_FILE):
        print(f"[-] CSV file not found: {CSV_FILE}")
        return None
    
    df = pd.read_csv(CSV_FILE)
    
    # Convert target_date to string in DD/MM/YYYY format
    if isinstance(target_date, str):
        # If input is YYYY-MM-DD
        if '-' in target_date and len(target_date) == 10:
            target_date_obj = datetime.strptime(target_date, '%Y-%m-%d').date()
            target_str = target_date_obj.strftime('%d/%m/%Y')
        else:
            target_str = target_date
    else:
        # If input is date object
        target_str = target_date.strftime('%d/%m/%Y')
    
    # Find the row
    mask = df['Date'] == target_str
    if not mask.any():
        print(f"[-] No data found for {target_str}")
        return None
    
    row = df[mask].iloc[-1]
    return {
        'date': target_str,
        'open': row['Open'],
        'high': row['High'],
        'low': row['Low'],
        'close': row['Close'],
        'volume': row['Volume']
    }

def verify_march_dates():
    """Verify if March 13 and 16 data exists"""
    print("\n" + "=" * 60)
    print("VERIFYING MARCH 2026 DATES")
    print("=" * 60)
    
    if not os.path.exists(CSV_FILE):
        print("[-] CSV file not found")
        return
    
    df = pd.read_csv(CSV_FILE)
    march_data = df[df['Date'].str.contains('/03/2026')]
    
    if not march_data.empty:
        print("\n📊 MARCH 2026 DATA IN CSV:")
        print(march_data.to_string(index=False))
        
        for date in ['13/03/2026', '16/03/2026']:
            if date in march_data['Date'].values:
                row = march_data[march_data['Date'] == date].iloc[0]
                print(f"\n✅ {date}: Close = ₹{row['Close']}")
            else:
                print(f"\n❌ {date}: Not found in CSV")
    else:
        print("[-] No March 2026 data found")

if __name__ == "__main__":
    # Update the CSV with missing dates
    update_csv_with_missing_dates()
    
    # Verify March dates
    verify_march_dates()
    
    # Test get_price_for_date
    print("\n" + "=" * 60)
    print("TESTING get_price_for_date()")
    print("=" * 60)
    
    for test_date in ['2026-03-13', '2026-03-16']:
        price_data = get_price_for_date(test_date)
        if price_data:
            print(f"\n{test_date}:")
            print(f"   Open:  ₹{price_data['open']}")
            print(f"   Close: ₹{price_data['close']}")
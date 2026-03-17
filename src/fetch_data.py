# ====================================
# Import Section
# ====================================
from config import CSV_FILE, STOCK_NAME
from datetime import datetime, timedelta
from nselib import capital_market

import pandas as pd

# ====================================
# Missing Dates Return Function
# ====================================
def get_missing_dates():
    # Load CSV
    global df
    df = pd.read_csv(CSV_FILE)
    # Convert DATE column (handle mixed formats safely)
    df['DATE'] = pd.to_datetime(df['DATE'], format='mixed', dayfirst=True)

    # Get last recorded date
    last_date = df['DATE'].max().date()

    # Today's date
    today = datetime.now().date()

    missing_dates = []
    current = last_date + timedelta(days=1)

    # Exclude today
    while current < today:
        if current.weekday() < 5:  # Mon-Fri only
            missing_dates.append(current)
        current += timedelta(days=1)

    if len(missing_dates) == 1:
        missing_dates = [last_date, missing_dates[0]]

    return missing_dates

# ====================================
# Get Data for dates Function
# ====================================
def get_data_for_dates(dates):
    if not dates:
        return None
    
    try:
        dates = [date.strftime('%d-%m-%Y') for date in dates]
        
        data = capital_market.price_volume_and_deliverable_position_data(
            symbol=STOCK_NAME,
            from_date=dates[0],
            to_date=dates[-1]
        )

        if data is None or data.empty:
            return None

        # Extract required columns
        ndf = pd.DataFrame({
            'DATE': pd.to_datetime(data['Date']).dt.strftime('%Y-%m-%d'),
            'OPEN': data['OpenPrice'],
            'HIGH': data['HighPrice'],
            'LOW': data['LowPrice'],
            'CLOSE': data['ClosePrice'],
            'VOLUME': data['TotalTradedQuantity']
        })

        return ndf

    except Exception as e:
        print(f"Error fetching: {e}")
        return None

# ====================================
# Save Data for missing dates Function
# ====================================
def fix_missing_data():
    print("[*] Checking for missing data...")
    Missing_Dates = get_missing_dates()
    
    if not Missing_Dates:
        print("[+] Everything Upto Date!")
        return True
    
    print(f"[!] Data missing for Dates {Missing_Dates[0]} to {Missing_Dates[-1]}")
    print("[*] Attempting to Retrieve Data...")
    ndf = get_data_for_dates(Missing_Dates)
    if not ndf:
        print("[-] Data Retrival Failed!")
        return None
    
    ndf["DATE"] = pd.to_datetime(ndf["DATE"], format='mixed', dayfirst=True)#.dt.strftime('%d/%m/%Y')
    result_df = pd.concat([df, ndf], ignore_index=True)
    result_df.drop_duplicates()
    result_df.dropna(inplace=True)
    sorted_result_df = result_df.sort_values("DATE")
    sorted_result_df["DATE"] = sorted_result_df["DATE"].dt.strftime('%d/%m/%Y')
    sorted_result_df.to_csv(CSV_FILE, index=False)
    print("[+] New Data Acquired!")
    return True

# ===== TEST =====
if __name__ == "__main__":
    pass
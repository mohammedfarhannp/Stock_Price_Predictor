# fetch_suzlon_data.py (temporary - run once)
import pandas as pd
from nselib import capital_market
import os
from datetime import datetime

# Read existing file to match format exactly
existing_file = "data/raw/SUZLON_NS_01-01-2025_to_CURRENT.csv"
df_existing = pd.read_csv(existing_file)
print(f"[+] Detected format from existing file:")
print(f"    Columns: {list(df_existing.columns)}")
print(f"    Date format: {df_existing['DATE'].iloc[0]}")

# Settings
STOCK_NAME = "SUZLON"
START_DATE = "01-01-2025"
END_DATE = datetime.now().strftime("%d-%m-%Y")
SAVE_DIR = "data/raw"

print(f"\n[*] Fetching {STOCK_NAME} data from {START_DATE} to {END_DATE}...")

data = capital_market.price_volume_and_deliverable_position_data(
    symbol=STOCK_NAME,
    from_date=START_DATE,
    to_date=END_DATE
)

if data is None or data.empty:
    print("[-] No data returned!")
    exit()

# Match exact column structure of existing file
df = pd.DataFrame({
    'DATE': pd.to_datetime(data['Date']).dt.strftime('%d/%m/%Y'),
    'OPEN': data['OpenPrice'],
    'HIGH': data['HighPrice'],
    'LOW': data['LowPrice'],
    'CLOSE': data['ClosePrice'],
    'VOLUME': data['TotalTradedQuantity']
})

# Sort ascending
df['DATE_TMP'] = pd.to_datetime(df['DATE'], format='%d/%m/%Y')
df = df.sort_values('DATE_TMP', ascending=True)
df = df.drop(columns=['DATE_TMP'])

# Save
filename = f"SUZLON_NS_01-01-2025_to_CURRENT.csv"
filepath = os.path.join(SAVE_DIR, filename)
df.to_csv(filepath, index=False)

print(f"[+] Saved {len(df)} rows to {filepath}")
print(f"[+] Date range: {df['DATE'].iloc[0]} to {df['DATE'].iloc[-1]}")
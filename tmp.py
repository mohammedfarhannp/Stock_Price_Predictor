# fetch_suzlon_data.py (temporary - run once)
import pandas as pd
from nselib import capital_market
import os
from datetime import datetime

# Settings
STOCK_NAME = "SUZLON"
START_DATE = "01-01-2025"
END_DATE = datetime.now().strftime("%d-%m-%Y")  # Today's date
SAVE_DIR = "data/raw"

os.makedirs(SAVE_DIR, exist_ok=True)

print(f"[*] Fetching {STOCK_NAME} data from {START_DATE} to {END_DATE}...")

data = capital_market.price_volume_and_deliverable_position_data(
    symbol=STOCK_NAME,
    from_date=START_DATE,
    to_date=END_DATE
)

if data is None or data.empty:
    print("[-] No data returned!")
    exit()

# Format exactly like the existing CSV
df = pd.DataFrame({
    'DATE': pd.to_datetime(data['Date']).dt.strftime('%d/%m/%Y'),
    'OPEN': data['OpenPrice'],
    'HIGH': data['HighPrice'],
    'LOW': data['LowPrice'],
    'CLOSE': data['ClosePrice'],
    'VOLUME': data['TotalTradedQuantity']
})

# Save without index, with comma-formatted numbers (matching existing format)
filename = f"SUZLON_NS_01-01-2025_to_CURRENT.csv"
filepath = os.path.join(SAVE_DIR, filename)

df.to_csv(filepath, index=False)

print(f"[+] Saved {len(df)} rows to {filepath}")
print(f"[+] Date range: {df['DATE'].iloc[0]} to {df['DATE'].iloc[-1]}")
print("[+] Format matches existing CSV (comma-separated numbers)")
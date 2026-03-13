# main.py (updated)
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from config import STOCK_SYMBOL
from fetch_data import fetch_stock_data
from preprocess import preprocess_data
from train_model import train_models

def main():
    print("=" * 50)
    print("STOCK PREDICTOR - Testing Phase")
    print("=" * 50)
    
    # Check if raw data already exists
    raw_files = os.listdir('data/raw')
    csv_files = [f for f in raw_files if f.endswith('.csv')]
    
    if csv_files:
        print(f"\n[1] Found existing data: {csv_files[0]}")
        print("   Skipping download...")
    else:
        # Step 1: Fetch data (only if no data exists)
        print("\n[1] No existing data found. Fetching new data...")
        data_path = fetch_stock_data()
        
        if not data_path:
            print("\n[-] Data fetch failed. Exiting.")
            return
    
    # Step 2: Preprocess data
    print("\n[2] Preprocessing data...")
    result = preprocess_data()
    
    if result:
        df, X, y = result
        print(f"\n[+] Preprocessing successful!")
        print(f"   Final dataset: {len(df)} days")
        print(f"   Training sequences: {X.shape[0]}")
    else:
        print("\n[-] Preprocessing failed.")
        return
    
    # Step 3: Train models
    print("\n[3] Training models...")
    best_model, results, test_data = train_models(X, y)

if __name__ == "__main__":
    main()
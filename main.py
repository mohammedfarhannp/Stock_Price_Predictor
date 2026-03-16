# main.py
import sys
import os
import pandas as pd
from datetime import datetime, timedelta

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from config import STOCK_SYMBOL
from preprocess import preprocess_data
from train_model import train_models
from predict import predict_next_day
from update_stock_data import update_csv_with_missing_dates, get_price_for_date

CSV_FILE = "data/raw/ROLEXRINGS_NS_2025-01-01_to_CURRENT.csv"

def check_and_update_csv():
    if not os.path.exists(CSV_FILE):
        print(f"[-] CSV file not found: {CSV_FILE}")
        return False
    
    # Update CSV with any missing dates
    print("\n[1] Checking for missing dates in CSV...")
    success = update_csv_with_missing_dates()
    
    if success:
        print("[+] CSV is ready for use")
        return True
    else:
        print("[-] Failed to update CSV")
        return False

def main():
    print("=" * 50)
    print("STOCK PREDICTOR - Using Local CSV Data")
    print("=" * 50)
    
    # Step 1: Check and update CSV with missing dates
    if not check_and_update_csv():
        return
    
    # Step 2: Preprocess data from CSV
    print("\n[2] Preprocessing data from CSV...")
    result = preprocess_data()
    
    if not result:
        print("[-] Preprocessing failed. Not enough data.")
        return
    
    df, X, y = result
    print(f"[+] Preprocessing successful! {len(df)} days of data")
    
    # Step 3: Train model
    print("\n[3] Training model...")
    best_model, results, test_data = train_models(X, y)
    
    # Step 4: Make prediction for next day
    print("\n[4] Making next day prediction...")
    prediction_result = predict_next_day()
    
    if not prediction_result:
        print("[-] Prediction failed.")
        return
    
    predicted_price, next_date = prediction_result
    next_date_str = next_date.strftime('%Y-%m-%d')
    
    # Step 5: Check if we already have actual price for this date
    print(f"\n[5] Checking if {next_date_str} data exists...")
    actual_data = get_price_for_date(next_date_str)
    
    if actual_data:
        print(f"[+] Data found for {next_date_str}")
        print(f"    Actual close: ₹{actual_data['close']}")
        print(f"    Predicted: ₹{predicted_price:.2f}")
        
        # Calculate deviation
        deviation = actual_data['close'] - predicted_price
        percent_dev = (deviation / actual_data['close']) * 100
        print(f"    Deviation: ₹{deviation:+.2f} ({percent_dev:+.2f}%)")
    else:
        print(f"[-] No data yet for {next_date_str}")
        print("    Run this script again after market close to see actual vs predicted")
    
    print("\n" + "=" * 50)
    print("SESSION COMPLETE")
    print("=" * 50)

if __name__ == "__main__":
    main()
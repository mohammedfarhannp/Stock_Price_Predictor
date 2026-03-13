# main.py
import sys
import os
import pandas as pd
import time
from datetime import datetime, timedelta
import yfinance as yf

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from config import STOCK_SYMBOL, START_DATE, END_DATE
from fetch_data import fetch_stock_data
from preprocess import preprocess_data
from train_model import train_models
from predict import predict_next_day
from evaluate import evaluate_prediction

def get_last_trading_day():
    raw_files = os.listdir('data/raw')
    csv_files = [f for f in raw_files if f.endswith('.csv')]
    
    if not csv_files:
        return None
    
    latest_file = max(csv_files)
    filepath = os.path.join('data/raw', latest_file)
    df = pd.read_csv(filepath)
    
    # Parse date (handle DD/MM/YYYY format)
    if '/' in df['Date'].iloc[-1]:
        last_date = datetime.strptime(df['Date'].iloc[-1], '%d/%m/%Y')
    else:
        last_date = pd.to_datetime(df['Date'].iloc[-1])
    
    return last_date.date()

def should_update_data():
    last_date = get_last_trading_day()
    
    if last_date is None:
        print("[+] No existing data found. Fresh download needed.")
        return True
    
    today = datetime.now().date()
    
    # Calculate next expected trading day
    next_day = last_date + timedelta(days=1)
    
    # Skip weekends
    while next_day.weekday() >= 5:  # 5=Saturday, 6=Sunday
        next_day += timedelta(days=1)
    
    print(f"\n[+] Last recorded date: {last_date.strftime('%d/%m/%Y')}")
    print(f"[+] Current date: {today.strftime('%d/%m/%Y')}")
    print(f"[+] Next expected trading day: {next_day.strftime('%d/%m/%Y')}")
    
    # Check if we're missing data
    if today > next_day:
        print("[+] New data available. Downloading...")
        return True
    else:
        print("[+] Data is up to date.")
        return False

def fetch_actual_price_with_retry(date, max_retries=3):
    date_str = date.strftime('%Y-%m-%d') if isinstance(date, datetime) else date
    next_day = (datetime.strptime(date_str, '%Y-%m-%d') + timedelta(days=1)).strftime('%Y-%m-%d')
    
    print(f"[+] Fetching price for: {date_str}")
    
    for attempt in range(max_retries):
        try:
            # Method 1: Standard download with explicit session
            print(f"   Attempt {attempt + 1}/{max_retries}...")
            
            # Create a new session for each attempt
            stock = yf.Ticker(STOCK_SYMBOL)
            
            # Add delay between retries
            if attempt > 0:
                time.sleep(2)
            
            # Try to get data
            hist = stock.history(start=date_str, end=next_day)
            
            if not hist.empty:
                actual_close = hist['Close'].iloc[-1]
                print(f"[+] Fetched actual price for {date_str}: ₹{actual_close:.2f}")
                return float(actual_close)
            
            # Method 2: Try with period="1d" approach
            hist = stock.history(period="1d")
            if not hist.empty and hist.index[0].strftime('%Y-%m-%d') == date_str:
                actual_close = hist['Close'].iloc[-1]
                print(f"[+] Fetched actual price using period method: ₹{actual_close:.2f}")
                return float(actual_close)
            
            print(f"   No data available for {date_str} on attempt {attempt + 1}")
            
        except Exception as e:
            print(f"   Attempt {attempt + 1} failed: {str(e)[:100]}")
    
    # If all retries fail, prompt for manual input
    print("\n[-] Automatic fetch failed. Please enter manually.")
    try:
        manual_price = input(f"Enter actual closing price for {date_str} (or press Enter to skip): ₹")
        if manual_price.strip():
            return float(manual_price)
    except ValueError:
        print("[-] Invalid input. Skipping.")
    
    return None

def store_prediction_record(date, predicted, actual):
    records_file = os.path.join('data', 'prediction_records.csv')
    
    # Create new record
    new_record = pd.DataFrame([{
        'date': date,
        'predicted_price': predicted,
        'actual_price': actual,
        'deviation': actual - predicted,
        'deviation_percent': ((actual - predicted) / actual) * 100 if actual else None,
        'fetch_method': 'auto' if actual else 'manual',
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }])
    
    # Append or create
    if os.path.exists(records_file):
        records = pd.read_csv(records_file)
        # Check if this date already exists
        if date not in records['date'].values:
            records = pd.concat([records, new_record], ignore_index=True)
            print(f"[+] Added new prediction record for {date}")
        else:
            print(f"[+] Record for {date} already exists. Updating...")
            records = records[records['date'] != date]
            records = pd.concat([records, new_record], ignore_index=True)
    else:
        records = new_record
        print(f"[+] Created new prediction records file")
    
    records.to_csv(records_file, index=False)
    return records_file

def main():
    print("=" * 50)
    print("STOCK PREDICTOR - Automated Pipeline")
    print("=" * 50)
    
    # Step 1: Check if we need to update data
    print("\n[1] Checking data freshness...")
    needs_update = should_update_data()
    
    if needs_update:
        # Fetch new data
        print("\n[2] Downloading fresh data...")
        data_path = fetch_stock_data()
        
        if not data_path:
            print("[-] Data fetch failed. Exiting.")
            return
        
        # Preprocess and retrain
        print("\n[3] Preprocessing new data...")
        result = preprocess_data()
        
        if result:
            df, X, y = result
            print("[+] Preprocessing successful!")
            
            print("\n[4] Retraining model with new data...")
            best_model, results, test_data = train_models(X, y)
        else:
            print("[-] Preprocessing failed.")
            return
    else:
        print("\n[2] Using existing model and data...")
    
    # Step 5: Make prediction for next day
    print("\n[5] Making next day prediction...")
    prediction_result = predict_next_day()
    
    if not prediction_result:
        print("[-] Prediction failed.")
        return
    
    predicted_price, next_date = prediction_result
    next_date_str = next_date.strftime('%Y-%m-%d')
    
    # Step 6: Check if we already have actual price for this date
    records_file = os.path.join('data', 'prediction_records.csv')
    already_recorded = False
    
    if os.path.exists(records_file):
        records = pd.read_csv(records_file)
        if next_date_str in records['date'].values:
            already_recorded = True
            record = records[records['date'] == next_date_str].iloc[-1]
            actual_price = record['actual_price']
            print(f"\n[+] Prediction for {next_date_str} already recorded.")
            print(f"   Actual: ₹{actual_price:.2f}, Predicted: ₹{predicted_price:.2f}")
    
    # Step 7: If not recorded and date has passed, fetch actual price
    today = datetime.now().date()
    
    if not already_recorded and next_date.date() <= today:
        print(f"\n[6] {next_date_str} has passed. Fetching actual price...")
        actual_price = fetch_actual_price_with_retry(next_date)
        
        if actual_price:
            # Store the record
            records_file = store_prediction_record(next_date_str, predicted_price, actual_price)
            
            # Evaluate
            print("\n[7] Evaluating prediction...")
            eval_results = evaluate_prediction(
                actual_price, 
                predicted_price, 
                next_date_str
            )
        else:
            print("[-] Could not fetch actual price.")
            # Still store prediction without actual
            store_prediction_record(next_date_str, predicted_price, None)
    
    elif not already_recorded and next_date.date() > today:
        print(f"\n[6] {next_date_str} is in the future. Cannot fetch actual price yet.")
        print(f"    Run this script again after {next_date_str} to auto-evaluate.")
    
    # Step 8: Show summary
    print("\n" + "=" * 50)
    print("SESSION COMPLETE")
    print("=" * 50)
    
    # Show recent prediction records if they exist
    if os.path.exists(records_file):
        records = pd.read_csv(records_file)
        print(f"\n[+] Total prediction records: {len(records)}")
        print("\nLast 3 predictions:")
        print(records.tail(3).to_string(index=False))

if __name__ == "__main__":
    main()
    exec(open('git_commit.py').read())
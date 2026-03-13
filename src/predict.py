# predict.py
import numpy as np
import pandas as pd
import joblib
import os

from config import MODELS_DIR, DATA_PROCESSED_DIR, LOOKBACK_DAYS, FEATURES
from datetime import datetime, timedelta

def load_model():
    model_path = os.path.join(MODELS_DIR, 'best_model.pkl')
    
    if not os.path.exists(model_path):
        print("[-] No trained model found. Please run train_model.py first.")
        return None
    
    model = joblib.load(model_path)
    print("[+] Model loaded successfully")
    return model

def get_latest_sequence():
    # Load processed data
    processed_file = os.path.join(DATA_PROCESSED_DIR, 'processed_data.csv')
    
    if not os.path.exists(processed_file):
        print("[-] No processed data found.")
        return None
    
    df = pd.read_csv(processed_file)
    
    # Get last LOOKBACK_DAYS rows for features
    latest_data = df[FEATURES].values[-LOOKBACK_DAYS:]
    
    if len(latest_data) < LOOKBACK_DAYS:
        print(f"[-] Not enough data. Need {LOOKBACK_DAYS} days, have {len(latest_data)}")
        return None
    
    # Reshape for model (flatten the sequence)
    sequence = latest_data.reshape(1, -1)
    
    # Get the last date
    last_date = pd.to_datetime(df['Date'].iloc[-1])
    
    return sequence, last_date, df

def predict_next_day():
    print("\n" + "=" * 50)
    print("NEXT DAY PREDICTION")
    print("=" * 50)
    
    # Load model
    model = load_model()
    if model is None:
        return None
    
    # Get latest sequence
    result = get_latest_sequence()
    if result is None:
        return None
    
    sequence, last_date, df = result
    
    # Make prediction
    predicted_price = model.predict(sequence)[0]
    
    # Get today's actual price (last close in data)
    today_close = df['Close'].iloc[-1]
    
    # Calculate expected date (next trading day)
    next_date = last_date + timedelta(days=1)
    while next_date.weekday() >= 5:  # Skip weekends
        next_date += timedelta(days=1)
    
    print(f"\n[+] Last trading day: {last_date.strftime('%Y-%m-%d')}")
    print(f"[+] Last close price: ₹{today_close:.2f}")
    print(f"[+] Next trading day: {next_date.strftime('%Y-%m-%d')}")
    print(f"[+] Predicted close: ₹{predicted_price:.2f}")
    
    # Calculate predicted change
    change = predicted_price - today_close
    change_percent = (change / today_close) * 100
    
    if change > 0:
        print(f"[$] Predicted change: +₹{change:.2f} (+{change_percent:.2f}%)")
    else:
        print(f"[$] Predicted change: -₹{abs(change):.2f} ({change_percent:.2f}%)")
    
    return predicted_price, next_date

if __name__ == "__main__":
    # Test the function
    predict_next_day()
# preprocess.py
import pandas as pd
import numpy as np
import os
from config import DATA_RAW_DIR, DATA_PROCESSED_DIR, FEATURES, LOOKBACK_DAYS

def load_latest_data():
    files = os.listdir(DATA_RAW_DIR)
    csv_files = [f for f in files if f.endswith('.csv')]
    
    if not csv_files:
        print("[-] No CSV files found in raw data folder.")
        return None
    
    latest_file = max(csv_files)  # Gets most recent by name (dates are in filename)
    filepath = os.path.join(DATA_RAW_DIR, latest_file)
    
    print(f"[*] Loading: {latest_file}")
    df = pd.read_csv(filepath)
    df['Date'] = pd.to_datetime(df['Date'])
    return df

def create_features(df):
    df = df.copy()
    
    # Moving averages
    df['MA5'] = df['Close'].rolling(window=5).mean()
    df['MA20'] = df['Close'].rolling(window=20).mean()
    
    # Price changes
    df['Price_Change'] = df['Close'].pct_change()
    df['Volume_Change'] = df['Volume'].pct_change()
    
    # High-Low range
    df['HL_Range'] = (df['High'] - df['Low']) / df['Close']
    
    # Open-Close change
    df['OC_Change'] = (df['Close'] - df['Open']) / df['Open']
    
    return df

def create_sequences(df, lookback=LOOKBACK_DAYS):
    X, y = [], []
    data = df[FEATURES].values
    
    for i in range(lookback, len(data)):
        X.append(data[i-lookback:i])
        y.append(data[i, 3])  # 3 is index of 'Close' price
    
    return np.array(X), np.array(y)

def preprocess_data():
    print("[+] Starting data preprocessing...")
    
    # Load data
    df = load_latest_data()
    if df is None:
        return None
    
    print(f"[#] Original data shape: {df.shape}")
    
    # Create features
    df = create_features(df)
    
    # Drop NaN values from rolling calculations
    df = df.dropna()
    
    print(f"[#] After feature engineering: {df.shape}")
    
    # Save processed data
    output_file = os.path.join(DATA_PROCESSED_DIR, "processed_data.csv")
    df.to_csv(output_file, index=False)
    print(f"[+] Processed data saved to: {output_file}")
    
    # Create sequences for model
    X, y = create_sequences(df)
    print(f"[+] Created sequences: X shape {X.shape}, y shape {y.shape}")
    
    return df, X, y

if __name__ == "__main__":
    # Test the function
    df, X, y = preprocess_data()
# preprocess.py (add debug prints)
import pandas as pd
import numpy as np
import os
from config import DATA_RAW_DIR, DATA_PROCESSED_DIR, FEATURES, LOOKBACK_DAYS

def load_latest_data():
    """Load the most recent CSV file from raw data folder"""
    files = os.listdir(DATA_RAW_DIR)
    csv_files = [f for f in files if f.endswith('.csv')]
    
    if not csv_files:
        print("[-] No CSV files found in raw data folder.")
        return None
    
    latest_file = max(csv_files)
    filepath = os.path.join(DATA_RAW_DIR, latest_file)
    
    print(f"[+] Loading: {latest_file}")
    df = pd.read_csv(filepath)
    
    # Normalize column names
    df.columns = [col.upper() for col in df.columns]

    # Rename to expected format
    df = df.rename(columns={
        'DATE': 'Date',
        'OPEN': 'Open',
        'HIGH': 'High',
        'LOW': 'Low',
        'CLOSE': 'Close',
        'VOLUME': 'Volume'
    })
    
    # Drop the first column if it's unnamed (contains stock symbol)
    if 'Unnamed: 0' in df.columns:
        df = df.drop(columns=['Unnamed: 0'])
    
    # Fix date format
    df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y', dayfirst=True)
    
    # Ensure numeric columns are actually numbers
    numeric_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Drop any rows with NaN values
    df = df.dropna()
    
    print(f"[+] Loaded {len(df)} rows after cleaning")
    return df

def create_features(df):
    """Create technical indicators as features"""
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
    """Create sequences for time series prediction"""
    X, y = [], []
    data = df[FEATURES].values
    
    print(f"[+] Creating sequences from {len(data)} data points with lookback={lookback}")
    
    for i in range(lookback, len(data)):
        X.append(data[i-lookback:i])
        y.append(data[i, 3])  # 3 is index of 'Close' price
    
    X = np.array(X)
    y = np.array(y)
    
    print(f"[+] Created {len(X)} sequences")
    return X, y

def preprocess_data():
    """Main preprocessing function"""
    print("\n" + "=" * 50)
    print("DATA PREPROCESSING")
    print("=" * 50)
    
    # Load data
    df = load_latest_data()
    if df is None:
        return None
    
    print(f"[+] Original data shape: {df.shape}")
    print(f"[+] Date range: {df['Date'].min()} to {df['Date'].max()}")
    print(f"[+] Columns: {list(df.columns)}")
    
    # Create features
    df = create_features(df)
    print(f"[+] After feature creation: {df.shape}")
    
    # Drop NaN values from rolling calculations
    before_drop = len(df)
    df = df.dropna()
    after_drop = len(df)
    print(f"[+] Dropped {before_drop - after_drop} rows with NaN values")
    
    print(f"[+] Final data shape: {df.shape}")
    
    # Save processed data
    output_file = os.path.join(DATA_PROCESSED_DIR, "processed_data.csv")
    df.to_csv(output_file, index=False)
    print(f"[+] Processed data saved to: {output_file}")
    
    # Create sequences for model
    X, y = create_sequences(df)
    
    if len(X) == 0:
        print("[-] WARNING: No sequences created! Not enough data.")
        print(f"    Need at least {LOOKBACK_DAYS + 1} days of data to create one sequence.")
        print(f"    Current data points: {len(df)}")
        return None
    
    print(f"[+] Created sequences: X shape {X.shape}, y shape {y.shape}")
    
    return df, X, y

if __name__ == "__main__":
    # Test the function
    result = preprocess_data()
    if result:
        df, X, y = result
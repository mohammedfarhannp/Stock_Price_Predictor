# config.py
import os

# Stock settings
STOCK_SYMBOL = "ROLEXRINGS.NS"  # .NS for NSE stocks
STOCK_NAME = "Rolex Rings"

# Date settings
START_DATE = "2025-01-01"  # 1 year of historical data
END_DATE = "2026-03-13"     # Current date

# File paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_RAW_DIR = os.path.join(BASE_DIR, "data", "raw")
DATA_PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")
MODELS_DIR = os.path.join(BASE_DIR, "models")

# Model settings
TRAIN_TEST_SPLIT = 0.8  # 80% train, 20% test
LOOKBACK_DAYS = 60      # Use last 60 days to predict next day
FEATURES = ['Open', 'High', 'Low', 'Close', 'Volume']

# Create directories if they don't exist
for directory in [DATA_RAW_DIR, DATA_PROCESSED_DIR, MODELS_DIR]:
    os.makedirs(directory, exist_ok=True)
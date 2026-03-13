# train_model.py
import xgboost as xgb
import pandas as pd

import numpy as np

import joblib
import os

from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

from config import MODELS_DIR, TRAIN_TEST_SPLIT, LOOKBACK_DAYS

def train_models(X, y):
    print("\n" + "=" * 50)
    print("MODEL TRAINING")
    print("=" * 50)
    
    # Reshape X for sklearn (from 3D to 2D)
    n_samples = X.shape[0]
    X_reshaped = X.reshape(n_samples, -1)
    
    # Split data
    split_idx = int(len(X_reshaped) * TRAIN_TEST_SPLIT)
    X_train, X_test = X_reshaped[:split_idx], X_reshaped[split_idx:]
    y_train, y_test = y[:split_idx], y[split_idx:]
    
    print(f"\n[#] Training samples: {len(X_train)}")
    print(f"[#] Testing samples: {len(X_test)}")
    
    models = {
        'Random Forest': RandomForestRegressor(n_estimators=100, random_state=42),
        'XGBoost': xgb.XGBRegressor(n_estimators=100, random_state=42)
    }
    
    best_model = None
    best_score = float('inf')
    results = {}
    
    for name, model in models.items():
        print(f"\n[*] Training {name}...")
        
        # Train
        model.fit(X_train, y_train)
        
        # Predict
        y_pred = model.predict(X_test)
        
        # Calculate metrics
        mae = mean_absolute_error(y_test, y_pred)
        mse = mean_squared_error(y_test, y_pred)
        rmse = np.sqrt(mse)
        r2 = r2_score(y_test, y_pred)
        
        results[name] = {
            'MAE': mae,
            'RMSE': rmse,
            'R2': r2,
            'model': model
        }
        
        print(f"  [+] MAE: ₹{mae:.2f}")
        print(f"  [+] RMSE: ₹{rmse:.2f}")
        print(f"  [+] R2 Score: {r2:.4f}")
        
        # Track best model (lowest MAE)
        if mae < best_score:
            best_score = mae
            best_model = model
            best_name = name
    
    # Save best model
    model_path = os.path.join(MODELS_DIR, 'best_model.pkl')
    joblib.dump(best_model, model_path)
    
    print("\n" + "=" * 50)
    print(f"[+] Best model: {best_name} (MAE: ₹{best_score:.2f})")
    print(f"[+] Model saved to: {model_path}")
    print("=" * 50)
    
    return best_model, results, (X_test, y_test)

if __name__ == "__main__":
    # Test the function
    from preprocess import preprocess_data
    
    # Load preprocessed data
    df, X, y = preprocess_data()
    if X is not None:
        train_models(X, y)
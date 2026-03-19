# ====================================
# Imports
# ====================================
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from fetch_data import fix_missing_data
from preprocess import preprocess_data
from train_model import train_models
from predict import predict_next_day
from log_prediction import log_prediction

# ====================================
# Main Pipeline
# ====================================
def main():
    print("\n" + "=" * 60)
    print("STOCK ML PIPELINE STARTED")
    print("=" * 60)

    # Step 1: Update data
    print("\n[1/4] Updating stock data...")
    status = fix_missing_data()
    if status is None:
        print("[-] Data update failed. Exiting pipeline.")
        return
    print("[✓] Data is up-to-date and ready")

    # Step 2: Preprocess
    print("\n[2/4] Preprocessing data...")
    result = preprocess_data()
    if result is None:
        print("[-] Preprocessing failed. Exiting pipeline.")
        return
    
    df, X, y = result
    print("[+] Data preprocessing completed successfully")

    # Step 3: Train model
    print("\n[3/4] Training model...")
    model, results, test_data = train_models(X, y)
    print("[+] Model training completed and best model saved")

    # Step 4: Predict
    print("\n[4/4] Generating prediction...")
    prediction = predict_next_day()
    if prediction is None:
        print("[-] Prediction failed.")
        return
    
    predicted_price, next_date = prediction
    log_prediction(next_date, predicted_price)
    print("[+] Prediction generated successfully")

    print("\n" + "=" * 60)
    print("[+] PIPELINE COMPLETED SUCCESSFULLY")
    print("[->] Run plot_predictions.py to get visuals of predicted price vs actual price")
    print("=" * 60)

    

# ====================================
# Run
# ====================================
if __name__ == "__main__":
    main()
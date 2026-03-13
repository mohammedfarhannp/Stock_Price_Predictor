# evaluate.py
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

from config import DATA_PROCESSED_DIR, MODELS_DIR
from datetime import datetime

def evaluate_prediction(actual_price, predicted_price, prediction_date):
    print("\n" + "=" * 50)
    print("PREDICTION EVALUATION")
    print("=" * 50)
    
    # Calculate metrics
    deviation = actual_price - predicted_price
    abs_deviation = abs(deviation)
    percent_deviation = (deviation / actual_price) * 100
    abs_percent_deviation = (abs_deviation / actual_price) * 100
    
    print(f"\n[+] Date: {prediction_date}")
    print(f"[+] Predicted price: ₹{predicted_price:.2f}")
    print(f"[+] Actual price: ₹{actual_price:.2f}")
    print(f"[+] Deviation: ₹{deviation:+.2f}")
    print(f"[+] Deviation %: {percent_deviation:+.2f}%")
    
    # Accuracy assessment
    if abs_percent_deviation <= 1:
        accuracy = "Excellent"
    elif abs_percent_deviation <= 2:
        accuracy = "Good"
    elif abs_percent_deviation <= 3:
        accuracy = "Fair"
    else:
        accuracy = "Poor"
    
    print(f"[+] Accuracy: {accuracy} (off by {abs_percent_deviation:.2f}%)")
    
    # Direction prediction
    if (predicted_price > actual_price and deviation > 0) or \
       (predicted_price < actual_price and deviation < 0):
        direction_correct = True
        print("[+] Direction prediction: ✓ Correct")
    else:
        direction_correct = False
        print("[-] Direction prediction: ✗ Wrong")
    
    # Log the evaluation
    log_evaluation(prediction_date, predicted_price, actual_price, 
                   deviation, percent_deviation, direction_correct)
    
    return {
        'deviation': deviation,
        'percent_deviation': percent_deviation,
        'abs_percent_deviation': abs_percent_deviation,
        'direction_correct': direction_correct,
        'accuracy': accuracy
    }

def log_evaluation(date, predicted, actual, deviation, percent_dev, direction_correct):
    log_file = os.path.join(MODELS_DIR, 'evaluation_log.csv')
    
    # Create entry
    new_entry = pd.DataFrame([{
        'date': date,
        'predicted': predicted,
        'actual': actual,
        'deviation': deviation,
        'percent_deviation': percent_dev,
        'direction_correct': direction_correct,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }])
    
    # Append to existing log or create new one
    if os.path.exists(log_file):
        log = pd.read_csv(log_file)
        log = pd.concat([log, new_entry], ignore_index=True)
    else:
        log = new_entry
    
    log.to_csv(log_file, index=False)
    print(f"[+] Evaluation logged to: {log_file}")

def plot_prediction_history():
    log_file = os.path.join(MODELS_DIR, 'evaluation_log.csv')
    
    if not os.path.exists(log_file):
        print("[-] No prediction history found.")
        return
    
    # Load log
    df = pd.read_csv(log_file)
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date')
    
    # Create plot
    plt.figure(figsize=(12, 6))
    
    plt.plot(df['date'], df['actual'], 'b-o', label='Actual Price', markersize=4)
    plt.plot(df['date'], df['predicted'], 'r--s', label='Predicted Price', markersize=4)
    
    # Color the area between
    plt.fill_between(df['date'], df['actual'], df['predicted'], 
                     alpha=0.3, color='yellow', label='Deviation')
    
    plt.title('Stock Price Predictions vs Actual', fontsize=16)
    plt.xlabel('Date')
    plt.ylabel('Price (₹)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Add accuracy stats
    avg_error = df['percent_deviation'].abs().mean()
    correct_directions = df['direction_correct'].sum()
    total_predictions = len(df)
    direction_accuracy = (correct_directions / total_predictions) * 100
    
    plt.figtext(0.15, 0.85, f'Avg Error: {avg_error:.2f}%', 
                bbox=dict(facecolor='yellow', alpha=0.5))
    plt.figtext(0.15, 0.80, f'Direction Accuracy: {direction_accuracy:.1f}%', 
                bbox=dict(facecolor='lightblue', alpha=0.5))
    
    # Save plot
    plot_file = os.path.join(MODELS_DIR, 'prediction_history.png')
    plt.savefig(plot_file, dpi=100, bbox_inches='tight')
    plt.show()
    
    print(f"[+] Plot saved to: {plot_file}")
    
    # Summary stats
    print("\n" + "=" * 50)
    print("PERFORMANCE SUMMARY")
    print("=" * 50)
    print(f"[+] Total predictions: {total_predictions}")
    print(f"[+] Average absolute error: {avg_error:.2f}%")
    print(f"[+] Direction accuracy: {direction_accuracy:.1f}%")
    print(f"[+] Best prediction: {df['percent_deviation'].abs().min():.2f}% error")
    print(f"[+] Worst prediction: {df['percent_deviation'].abs().max():.2f}% error")

if __name__ == "__main__":
    # Test with sample data
    plot_prediction_history()
# plot_predictions.py
import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime

def plot_prediction_history():
    records_file = os.path.join('data', 'prediction_records.csv')
    
    if not os.path.exists(records_file):
        print("[-] No prediction records found.")
        return
    
    # Load data
    df = pd.read_csv(records_file)
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date')
    
    # Filter out rows without actual prices
    df = df.dropna(subset=['actual_price'])
    
    if len(df) == 0:
        print("[-] No records with actual prices found.")
        return
    
    # Create plot
    plt.figure(figsize=(14, 7))
    
    # Plot actual and predicted
    plt.plot(df['date'], df['actual_price'], 'b-o', label='Actual Price', 
             linewidth=2, markersize=6, markerfacecolor='blue')
    plt.plot(df['date'], df['predicted_price'], 'r--s', label='Predicted Price', 
             linewidth=2, markersize=6, markerfacecolor='red')
    
    # Shade the area between
    plt.fill_between(df['date'], df['actual_price'], df['predicted_price'], 
                     alpha=0.2, color='gray', label='Error Margin')
    
    # Color code by direction accuracy (green if direction correct)
    for i in range(len(df) - 1):
        pred_direction = df['predicted_price'].iloc[i+1] > df['predicted_price'].iloc[i]
        actual_direction = df['actual_price'].iloc[i+1] > df['actual_price'].iloc[i]
        
        if pred_direction == actual_direction:
            plt.axvspan(df['date'].iloc[i], df['date'].iloc[i+1], 
                       alpha=0.1, color='green')
    
    plt.title('Stock Price Predictions: Actual vs Predicted Over Time', fontsize=16, fontweight='bold')
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Price (₹)', fontsize=12)
    plt.legend(loc='best', fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    
    # Add statistics
    df['error'] = abs(df['deviation_percent'])
    avg_error = df['error'].mean()
    
    # Direction accuracy
    correct_directions = 0
    for i in range(len(df) - 1):
        pred_direction = df['predicted_price'].iloc[i+1] > df['predicted_price'].iloc[i]
        actual_direction = df['actual_price'].iloc[i+1] > df['actual_price'].iloc[i]
        if pred_direction == actual_direction:
            correct_directions += 1
    
    direction_accuracy = (correct_directions / (len(df) - 1)) * 100 if len(df) > 1 else 0
    
    stats_text = f'Avg Absolute Error: {avg_error:.2f}%\n'
    stats_text += f'Direction Accuracy: {direction_accuracy:.1f}%\n'
    stats_text += f'Total Predictions: {len(df)}'
    
    plt.figtext(0.15, 0.85, stats_text, 
                bbox=dict(facecolor='yellow', alpha=0.7, boxstyle='round,pad=0.5'),
                fontsize=10, fontweight='bold')
    
    # Tight layout
    plt.tight_layout()
    
    # Save plot
    plot_file = os.path.join('data', 'prediction_history.png')
    print(f"[+] Plot saved to: {plot_file}")
    
    plt.show()
    
    # Print summary
    print("\n" + "=" * 50)
    print("PREDICTION PERFORMANCE SUMMARY")
    print("=" * 50)
    print(f"Total predictions with actuals: {len(df)}")
    print(f"Date range: {df['date'].min().date()} to {df['date'].max().date()}")
    print(f"Average absolute error: {avg_error:.2f}%")
    print(f"Best prediction: {df['error'].min():.2f}% error")
    print(f"Worst prediction: {df['error'].max():.2f}% error")
    print(f"Direction accuracy: {direction_accuracy:.1f}%")

def plot_recent_predictions(days=30):
    records_file = os.path.join('data', 'prediction_records.csv')
    
    if not os.path.exists(records_file):
        print("[-] No prediction records found.")
        return
    
    df = pd.read_csv(records_file)
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date')
    df = df.dropna(subset=['actual_price'])
    
    if len(df) == 0:
        print("[-] No records with actual prices found.")
        return
    
    # Get last 'days' records
    recent_df = df.tail(days)
    
    plt.figure(figsize=(12, 6))
    
    plt.plot(recent_df['date'], recent_df['actual_price'], 'b-o', label='Actual', linewidth=2)
    plt.plot(recent_df['date'], recent_df['predicted_price'], 'r--s', label='Predicted', linewidth=2)
    
    plt.title(f'Recent {len(recent_df)} Predictions', fontsize=14, fontweight='bold')
    plt.xlabel('Date')
    plt.ylabel('Price (₹)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    plot_file = os.path.join('data', 'recent_predictions.png')
    print(f"[+] Recent predictions plot saved to: {plot_file}")
    plt.show()

if __name__ == "__main__":
    print("=" * 50)
    print("PREDICTION VISUALIZATION")
    print("=" * 50)
    print("\n[1] Full history plot")
    plot_prediction_history()
    
    print("\n[2] Recent predictions (last 30 days)")
    plot_recent_predictions(30)
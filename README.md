# Stock Price Predictor

A machine learning project that predicts next-day stock prices for Indian stocks using historical data. The system automatically updates data, retrains models, and evaluates predictions.

## Features

- **Automated Data Fetching**: Checks for missing trading days and fetches real data from NSE
- **ML Predictions**: Uses Random Forest and XGBoost to predict next day's closing price
- **Auto-Retraining**: Model retrains automatically when new data arrives
- **Prediction Logging**: Saves predictions and actual prices for performance tracking
- **Visualization**: Plots actual vs predicted prices over time

## Project Structure

```
stock-predictor/
│
├── data/
│   ├── raw/                     # Raw CSV data from NSE
│   └── processed/               # Processed data with features
│
├── models/
│   └── best_model.pkl           # Trained model
│
├── src/
│   ├── config.py                # Configuration settings
│   ├── fetch_data.py            # Fetches missing dates from NSE
│   ├── preprocess.py            # Feature engineering
│   ├── train_model.py           # Trains ML models
│   ├── predict.py               # Makes predictions
│   └── evaluate.py              # Evaluates predictions
│
├── main.py                      # Main pipeline
├── plot_predictions.py          # Visualization script
└── requirements.txt             # Dependencies
```

## Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd stock-predictor
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Install nselib** (for Indian stock data)
```bash
pip install nselib
```

## Usage

### 1. Update Data
```bash
python main.py
```
This will:
- Check your existing CSV for missing dates
- Fetch missing data from NSE
- Preprocess and train the model
- Make a prediction for the next trading day

### 2. View Prediction History
```bash
python plot_predictions.py
```
Shows a graph of actual vs predicted prices over time.

## CSV Format

Your data file should be in `data/raw/ROLEXRINGS_NS_2025-01-01_to_CURRENT.csv` with these columns:

| Column | Description |
|--------|-------------|
| DATE | Trading date (DD/MM/YYYY) |
| OPEN | Opening price |
| HIGH | Highest price of the day |
| LOW | Lowest price of the day |
| CLOSE | Closing price |
| VOLUME | Total traded quantity |

## Configuration

Edit `src/config.py` to change:
- Stock symbol
- Lookback days (default: 60)
- Train/test split ratio

## How It Works

1. **Data Fetch**: Checks last date in CSV → finds missing trading days → fetches from NSE
2. **Preprocessing**: Creates technical indicators (moving averages, price changes, etc.)
3. **Training**: Trains Random Forest and XGBoost models
4. **Prediction**: Uses best model to predict next day's close
5. **Evaluation**: Compares prediction with actual price when available

## Dependencies

- pandas, numpy – Data manipulation
- scikit-learn, xgboost – Machine learning
- nselib – NSE India data
- matplotlib – Visualization
- joblib – Model persistence

## Notes

- Data is fetched from NSE India using `nselib` library
- Predictions are for educational purposes only
- Model retrains automatically when new data is available
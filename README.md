# Stock Price Predictor

A machine learning project that predicts next-day stock prices for Indian stocks using historical data. The system automatically updates data, retrains models, and logs predictions.

## Project Structure

```
Stock Price Predictor ML Project/
│
├── .gitignore                      # Git ignore file
├── config.py                       # Main configuration settings
├── git_commit.py                   # Auto-commit utility
├── main.py                         # Main pipeline runner
├── plot_predictions.py             # Visualization script
├── requirements.txt                # Python dependencies
├── README.md                       # This file
│
├── data/
│   ├── raw/
│   │   └── ROLEXRINGS_NS_01-01-2025_to_CURRENT.csv   # Raw stock data
│   ├── processed/
│   │   └── processed_data.csv                         # Data with engineered features
│   └── prediction/
│       └── predictions.csv                            # Log of predictions vs actuals
│
├── models/
│   ├── best_model.pkl               # Trained ML model
│   └── evaluation_log.csv           # Model performance metrics
│
└── src/
    ├── __init__.py                  # Package initializer
    ├── fetch_data.py                # Fetches missing dates from NSE
    ├── preprocess.py                # Feature engineering
    ├── train_model.py               # Trains ML models
    ├── predict.py                   # Makes predictions
    ├── evaluate.py                  # Evaluates predictions
    └── log_prediction.py            # Logs predictions to CSV
```

## Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd "Stock Price Predictor ML Project"
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Install nselib** (for NSE India data)
```bash
pip install nselib
```

## Usage

### Run the Main Pipeline
```bash
python main.py
```
This will:
- Check for missing trading days in your CSV
- Fetch missing data from NSE
- Preprocess data and create features
- Train the model
- Make a prediction for the next trading day
- Log the prediction

### View Prediction History
```bash
python plot_predictions.py
```
Generates a graph showing actual vs predicted prices over time.

## Data Format

### Raw Data (`data/raw/ROLEXRINGS_NS_01-01-2025_to_CURRENT.csv`)
| Column | Description |
|--------|-------------|
| DATE | Trading date (DD/MM/YYYY) |
| OPEN | Opening price |
| HIGH | Highest price of the day |
| LOW | Lowest price of the day |
| CLOSE | Closing price |
| VOLUME | Total traded quantity |

### Predictions Log (`data/prediction/predictions.csv`)
| Column | Description |
|--------|-------------|
| date | Date of prediction |
| predicted_price | Model's predicted closing price |
| actual_price | Actual closing price (when available) |
| deviation | Difference between actual and predicted |
| deviation_percent | Percentage deviation |

## Configuration

Edit `config.py` to modify:
- `STOCK_SYMBOL`: Stock ticker (default: ROLEXRINGS.NS)
- `LOOKBACK_DAYS`: Days of history to use for prediction (default: 60)
- `TRAIN_TEST_SPLIT`: Train/test split ratio (default: 0.8)

## Features Engineered

The preprocessing step adds these technical indicators:
- MA5 / MA20: 5-day and 20-day moving averages
- Price_Change: Daily price percentage change
- Volume_Change: Daily volume percentage change
- HL_Range: High-Low range as percentage of close
- OC_Change: Open-Close change as percentage of open

## Models Used

- **Random Forest Regressor**: Ensemble of decision trees
- **XGBoost Regressor**: Gradient boosting optimized for performance

The best model (lowest MAE) is saved as `models/best_model.pkl`.

## How It Works

1. **Data Fetch**: Reads last date from CSV → finds missing trading days → fetches real data from NSE via nselib
2. **Preprocessing**: Adds technical indicators → cleans data → creates sequences for time series prediction
3. **Training**: Splits data → trains both models → selects best based on Mean Absolute Error
4. **Prediction**: Uses last `LOOKBACK_DAYS` of data → predicts next day's close → logs to `predictions.csv`
5. **Evaluation**: When actual price becomes available, compares with prediction → logs to `evaluation_log.csv`

## Dependencies

- `pandas`, `numpy` – Data manipulation
- `scikit-learn`, `xgboost` – Machine learning
- `nselib` – NSE India data fetching
- `matplotlib` – Visualization
- `joblib` – Model persistence
- `python-dateutil` – Date handling

## Notes

- Data is fetched from NSE India using `nselib` library
- Predictions are for educational/research purposes only
- Not financial advice or trading recommendation
- Model retrains automatically when new data is added

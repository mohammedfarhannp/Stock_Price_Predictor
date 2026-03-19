import pandas as pd

from config import PREDICTION_FILE
from datetime import datetime

def log_prediction(Date, Prediction):
    df = pd.read_csv(PREDICTION_FILE)
    
    new_row = {"DATE":Date, "PREDICTION": Prediction}
    
    ndf = pd.DataFrame([new_row])
    ndf["DATE"] = pd.to_datetime(ndf["DATE"], format='mixed', dayfirst=True)
    
    df = pd.concat([df, ndf], ignore_index=True)
    df["DATE"] = pd.to_datetime(df["DATE"], format='mixed', dayfirst=True)
    df.dropna(inplace=True)
    df = df.drop_duplicates()
    df.to_csv(PREDICTION_FILE, index=False)
    
    
# plot_predictions.py
import pandas as pd
import matplotlib.pyplot as plt
import os

from config import CSV_FILE, PREDICTION_FILE
from datetime import datetime

#

mdf = pd.read_csv(CSV_FILE)
pdf = pd.read_csv(PREDICTION_FILE)

mdf["DATE"] = pd.to_datetime(mdf["DATE"], format="mixed", dayfirst=True)
pdf["DATE"] = pd.to_datetime(pdf["DATE"], format="mixed")

mdf = mdf.drop(columns=["OPEN", "HIGH", "LOW", "VOLUME"])

for col in ["CLOSE"]:
    mdf[col] = pd.to_numeric(mdf[col].astype(str).str.replace(",", ""), errors="coerce")

pdf["PREDICTION"] = pd.to_numeric(pdf["PREDICTION"], errors="coerce")


df = pd.merge(mdf, pdf, on="DATE", how="inner")

# Rename CLOSE → ACTUAL
df = df.rename(columns={"CLOSE": "ACTUAL"})

df = df.sort_values("DATE")

# Plot
plt.figure(figsize=(12, 6))

plt.plot(df["DATE"], df["ACTUAL"], marker='o', label="Actual Price")
plt.plot(df["DATE"], df["PREDICTION"], marker='s', linestyle='--', label="Predicted Price")

# Labels & title
plt.title("Stock Price: Actual vs Predicted")
plt.xlabel("Date")
plt.ylabel("Price (₹)")

# Grid & legend
plt.grid(True, alpha=0.3)
plt.legend()

# Rotate dates for readability
plt.xticks(rotation=45)

# Layout fix
plt.tight_layout()

plt.show()


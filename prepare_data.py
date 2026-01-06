# prepare_data.py
import pandas as pd
import numpy as np

# upload the data
df = pd.read_csv("data/pollution.csv")

# fill the empty values
df = df.fillna(df.mean(numeric_only=True))

# clear the negative values
numeric_cols = df.select_dtypes(include=np.number).columns
for col in numeric_cols:
    df = df[df[col] >= 0]

# create a timestamp and add to beginning
timestamps = pd.date_range(start="2003-01-01", periods=len(df), freq="H")
df.insert(0, "timestamp", timestamps)

# save the cleaned data
df.to_csv("data/clean_air_quality.csv", index=False)

print("Data is cleaned, timestamp is added and saved.")
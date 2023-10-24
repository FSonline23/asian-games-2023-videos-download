import pandas as pd
import os

df = pd.read_csv("AsianGames2022URL_20231023.csv")
sports = df["Sport Name"].unique()
for sport in sports:
    os.mkdir(sport)

print("Sport subfolders created successfully!")
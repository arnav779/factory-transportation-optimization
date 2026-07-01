import pandas as pd

df = pd.read_csv("data.csv")

print(df.head())
print("\n")
print(df.columns.tolist())
print("\nShape:", df.shape)
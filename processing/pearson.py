import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


file_path = "gold_cleaned.csv"
df = pd.read_csv(file_path, parse_dates=["date"])

print(df.head())

corr_matrix = df.corr(method="pearson")

plt.figure(figsize=(8, 6))
cax = plt.matshow(corr_matrix, cmap="coolwarm", fignum=1)
plt.xticks(range(len(corr_matrix.columns)), corr_matrix.columns, rotation=45)
plt.yticks(range(len(corr_matrix.columns)), corr_matrix.columns)
plt.colorbar(cax)

for (i, j), val in np.ndenumerate(corr_matrix.values):
    plt.text(j, i, f"{val:.2f}", ha="center", va="center", color="black")

plt.title("Pearson Correlation Matrix", y=1.15)
plt.tight_layout()
plt.show()

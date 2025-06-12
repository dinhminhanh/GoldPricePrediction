import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid")

file_path = "../data/gold_cleaned.csv"
df = pd.read_csv(file_path, parse_dates=["date"])

print(df.head())

sns.kdeplot(df, x="gold_volume", fill=True, common_norm=False, alpha=0.5, bw_adjust=0.2)
plt.show()
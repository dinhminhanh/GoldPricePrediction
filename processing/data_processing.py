import pandas as pd
import os
from glob import glob
from functools import reduce

DATA_DIR = "data"

COLUMN_MAP = {
    "Lần cuối": "last",
    "Mở": "open",
    "Cao": "high",
    "Thấp": "low",
    "KL": "volume",
    "% Thay đổi": "change_percent"
}

def clean_numeric_column(series):
    """
    Xử lý các chuỗi số dạng '1,234.56', '204.02K', '1.5M', v.v...
    """
    return (
        series.astype(str)
              .str.replace("K", "e3", regex=False)
              .str.replace("M", "e6", regex=False)
              .str.replace(",", "", regex=False)
              .str.replace("%", "", regex=False)
              .replace("nan", None)
              .apply(pd.to_numeric, errors="coerce")
    )

def read_and_merge_csvs(file_pattern, prefix):
    files = glob(os.path.join(DATA_DIR, file_pattern))
    df_list = []

    for file in files:
        try:
            df = pd.read_csv(file)
            df = df.rename(columns={"Ngày": "Date", **COLUMN_MAP})
            df["Date"] = pd.to_datetime(df["Date"], dayfirst=True, errors="coerce")
            df = df[["Date"] + list(COLUMN_MAP.values())].dropna(subset=["Date"])

            # Làm sạch toàn bộ cột số
            for col in COLUMN_MAP.values():
                df[col] = clean_numeric_column(df[col])

            df = df.rename(columns={col: f"{prefix}_{col}" for col in COLUMN_MAP.values()})
            df_list.append(df)
        except Exception as e:
            print(f"⚠️ Lỗi khi đọc {file}: {e}")

    merged = pd.concat(df_list, ignore_index=True)
    merged = merged.drop_duplicates(subset="Date")
    merged = merged.sort_values("Date").reset_index(drop=True)
    return merged

# Đọc từng nhóm dữ liệu
gold_df = read_and_merge_csvs("gold_price*.csv", "gold")
oil_df = read_and_merge_csvs("oil_price*.csv", "oil")
dxy_df = read_and_merge_csvs("dxy*.csv", "dxy")
sp500_df = read_and_merge_csvs("sp500*.csv", "sp500")

# Merge outer toàn bộ
dfs = [gold_df, oil_df, dxy_df, sp500_df]
merged_df = reduce(lambda left, right: pd.merge(left, right, on="Date", how="outer"), dfs)

# Sắp xếp theo ngày
merged_df = merged_df.sort_values("Date").reset_index(drop=True)

# Bỏ dữ liệu trước năm 1980
merged_df = merged_df[merged_df["Date"] >= pd.Timestamp("1979-12-30")].reset_index(drop=True)

# Bỏ các cột có > 50% giá trị rỗng, nhưng giữ lại toàn bộ cột `gold_`
missing_ratio = merged_df.isnull().mean()
cols_to_keep = [col for col in merged_df.columns if (missing_ratio[col] < 0.5 or col.startswith("gold_"))]
merged_df = merged_df[cols_to_keep]

# Đảm bảo liên tục theo ngày và forward-fill
merged_df = merged_df.set_index("Date").resample("D").ffill().reset_index()

# Điền tiếp nếu còn sót giá trị rỗng
merged_df = merged_df.ffill()

# Lưu ra file
merged_df.to_csv("merged_gold_data.csv", index=False)
print("✅ Dữ liệu đã được xử lý và lưu ở 'merged_gold_data.csv'")

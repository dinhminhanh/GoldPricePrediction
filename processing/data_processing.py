import pandas as pd
import os
from glob import glob

DATA_DIR = "data"
OUTPUT_DIR = "data"
os.makedirs(OUTPUT_DIR, exist_ok=True)

COLUMN_MAP = {
    "Lần cuối": "last",
    "Mở": "open",
    "Cao": "high",
    "Thấp": "low",
    "KL": "volume",
    "% Thay đổi": "change_percent"
}

def clean_numeric_column(series):
    return (
        series.astype(str)
              .str.replace("K", "e3", regex=False)
              .str.replace("M", "e6", regex=False)
              .str.replace(",", "", regex=False)
              .str.replace("%", "", regex=False)
              .replace("nan", None)
              .apply(pd.to_numeric, errors="coerce")
    )

def process_group(file_pattern, prefix):
    files = glob(os.path.join(DATA_DIR, file_pattern))
    df_list = []

    for file in files:
        try:
            df = pd.read_csv(file)
            df = df.rename(columns={"Ngày": "Date", **COLUMN_MAP})
            df["Date"] = pd.to_datetime(df["Date"], dayfirst=True, errors="coerce")
            df = df[["Date"] + list(COLUMN_MAP.values())].dropna(subset=["Date"])

            for col in COLUMN_MAP.values():
                df[col] = clean_numeric_column(df[col])

            df = df.rename(columns={col: f"{prefix}_{col}" for col in COLUMN_MAP.values()})
            df_list.append(df)

        except Exception as e:
            print(f"⚠️ Lỗi khi xử lý {file}: {e}")

    if not df_list:
        print(f"⚠️ Không tìm thấy dữ liệu nào cho {prefix}")
        return

    # Gộp tất cả file của 1 nhóm
    merged = pd.concat(df_list, ignore_index=True)
    merged = merged.drop_duplicates(subset="Date")
    merged = merged.sort_values("Date").reset_index(drop=True)

    # 🧩 Tạo ngày liên tục từ ngày nhỏ nhất đến lớn nhất
    full_dates = pd.date_range(start=merged["Date"].min(), end=merged["Date"].max(), freq="D")
    merged = merged.set_index("Date").reindex(full_dates).rename_axis("Date").reset_index()

    # 🔁 Forward-fill dữ liệu bị thiếu
    merged = merged.ffill()

    # ✂️ Chỉ lấy từ 1993 trở đi
    merged = merged[merged["Date"] >= pd.Timestamp("1993-01-01")]

    # 🧹 Loại cột thiếu quá nhiều (sau khi ffill sẽ rất ít, nhưng vẫn để đề phòng)
    missing_ratio = merged.isnull().mean()
    keep_cols = [col for col in merged.columns if missing_ratio[col] < 0.5 or col == "Date"]
    merged = merged[keep_cols]

    # 💾 Lưu file kết quả
    out_path = os.path.join(OUTPUT_DIR, f"{prefix}_cleaned.csv")
    merged.to_csv(out_path, index=False)
    print(f"✅ Đã xử lý và lưu: {out_path}")

# Gọi cho từng nhóm
process_group("oil_price*.csv", "oil")
process_group("gold_price*.csv", "gold")
process_group("sp500*.csv", "sp500")
process_group("dxy*.csv", "dxy")

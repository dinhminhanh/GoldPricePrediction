import yfinance as yf
import pandas as pd
from functools import reduce

def download_data(ticker: str, period: str = "1mo") -> pd.DataFrame:
    print(f"📥 Downloading data for {ticker}...")
    df = yf.download(ticker, period=period, interval="1d")
    df.reset_index(inplace=True)
    return df

def calculate_change_percent(df: pd.DataFrame, name: str) -> pd.DataFrame:
    df[f"{name}_change_percent"] = (df[f"{name}_close"] - df[f"{name}_open"]) / df[f"{name}_open"] * 100
    return df

def main():
    tickers = {
        "gold": "GC=F",     # Gold Futures
        "oil": "CL=F",      # Crude Oil Futures
        "dxy": "DX-Y.NYB",  # US Dollar Index
        "sp500": "^GSPC"    # S&P 500
    }

    dfs = []

    for name, ticker in tickers.items():
        df = download_data(ticker)
        df.rename(columns={
            "Open": f"{name}_open",
            "High": f"{name}_high",
            "Low": f"{name}_low",
            "Close": f"{name}_close",
            "Volume": f"{name}_volume"
        }, inplace=True)

        # Tính last và change %
        df[f"{name}_last"] = df[f"{name}_close"]
        df = calculate_change_percent(df, name)

        dfs.append(df[[
            "Date",
            f"{name}_last",
            f"{name}_open",
            f"{name}_high",
            f"{name}_low",
            f"{name}_volume",
            f"{name}_change_percent"
        ]])

    # Gộp tất cả dataframe theo cột "Date"
    df_merged = reduce(lambda left, right: pd.merge(left, right, on="Date", how="inner"), dfs)

    # Sắp xếp theo ngày tăng dần
    df_merged.sort_values(by="Date", inplace=True)
    df_merged.columns.name = None  # quan trọng

    # ✅ Xuất file CSV
    df_merged.to_csv("realtime_input.csv", index=False)
    print("✅ Đã lưu dữ liệu mới vào realtime_input.csv với định dạng đầy đủ")

if __name__ == "__main__":
    main()

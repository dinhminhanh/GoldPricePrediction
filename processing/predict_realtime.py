import os
import pandas as pd
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lag
from pyspark.sql.window import Window
from pyspark.sql.types import DoubleType
from pyspark.ml import PipelineModel

N_LAGS = 5
MODEL_DIR = "models/linear_regression_pipeline"  
DATA_DIR = "data"
REALTIME_FILE = os.path.join("realtime_input.csv")  # File dữ liệu realtime mới

def load_pipeline_model():
    return PipelineModel.load(MODEL_DIR)

def prepare_realtime_data(spark, input_csv, n_lags):
    # Đọc file csv realtime, parse cột Date
    df_pd = pd.read_csv(input_csv, parse_dates=["Date"])
    df_pd = df_pd.sort_values("Date").ffill()  # điền giá trị thiếu nếu có

    df = spark.createDataFrame(df_pd)

    # Chọn các cột feature dùng cho model (bỏ gold_last, gold_change_percent nếu không cần)
    features = [c for c in df.columns if c.startswith("dxy_") or c.startswith("sp500_") or c.startswith("gold_") or c.startswith("oil_")]
    features = [f for f in features if f not in ["gold_last", "gold_change_percent"]]

    # Cast tất cả các cột feature sang DoubleType để model nhận diện được
    for feat in features:
        df = df.withColumn(feat, col(feat).cast(DoubleType()))

    # Tạo các cột lag cho từng feature
    window_spec = Window.orderBy("Date")
    for feat in features:
        for i in range(1, n_lags + 1):
            df = df.withColumn(f"{feat}_lag_{i}", lag(col(feat), i).over(window_spec))

    # Bỏ các dòng có null (vì lag tạo ra null ở đầu)
    df = df.orderBy("Date").dropna()

    return df

def predict_realtime():
    spark = SparkSession.builder.appName("RealtimeGoldPrediction").getOrCreate()

    pipeline_model = load_pipeline_model()

    df = prepare_realtime_data(spark, REALTIME_FILE, N_LAGS)

    prediction_df = pipeline_model.transform(df).select("Date", "prediction")
    prediction_df = prediction_df.orderBy("Date", ascending=False)

    # Lấy dự đoán ngày gần nhất
    latest_prediction = prediction_df.limit(1).collect()[0]
    print(f"📅 Dự đoán giá vàng cho ngày tiếp theo ({latest_prediction['Date']}): {latest_prediction['prediction']:.2f} USD")

    # Lưu toàn bộ kết quả dự đoán vào CSV
    output_path = os.path.join("prediction_result.csv")

    # Chuyển spark dataframe sang pandas để lưu csv (nếu data nhỏ)
    prediction_pd = prediction_df.toPandas()
    prediction_pd.to_csv(output_path, index=False)

if __name__ == "__main__":
    predict_realtime()

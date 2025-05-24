from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lag
from pyspark.sql.window import Window
from pyspark.ml.feature import VectorAssembler, StandardScaler
from pyspark.ml.regression import RandomForestRegressor, LinearRegression
from pyspark.ml.evaluation import RegressionEvaluator

import pandas as pd

# 1. Tạo Spark session
spark = SparkSession.builder.appName("GoldPricePrediction").getOrCreate()

# 2. Đọc dữ liệu bằng pandas
df_pd = pd.read_csv("data/merged_gold_data.csv")
df_pd = df_pd.dropna()
df_pd["Date"] = pd.to_datetime(df_pd["Date"])
df_pd = df_pd.sort_values("Date")

# 3. Đưa vào Spark
df = spark.createDataFrame(df_pd)

# 4. Tạo đặc trưng lag
n_lags = 5
features = [c for c in df.columns if c.startswith("dxy_") or c.startswith("sp500_") or c.startswith("gold_")]
features = [f for f in features if f not in ["gold_last", "gold_change_percent"]]

window_spec = Window.orderBy("Date")
for feat in features:
    for i in range(1, n_lags + 1):
        df = df.withColumn(f"{feat}_lag_{i}", lag(col(feat), i).over(window_spec))

# 5. Tạo cột target
df = df.withColumn("target", lag("gold_last", -1).over(window_spec)).dropna()

# 6. Chuyển về pandas để loại bỏ outlier
df_pd = df.toPandas()
for col_name in df_pd.select_dtypes(include="number").columns:
    Q1 = df_pd[col_name].quantile(0.25)
    Q3 = df_pd[col_name].quantile(0.75)
    IQR = Q3 - Q1
    lower, upper = Q1 - 1.5 * IQR, Q3 + 1.5 * IQR
    df_pd = df_pd[(df_pd[col_name] >= lower) & (df_pd[col_name] <= upper)]

# 7. Đưa lại vào Spark
df = spark.createDataFrame(df_pd)

# 8. Tách train/test
train_size = int(df.count() * 0.7)
train_df = df.limit(train_size)
test_df = df.subtract(train_df)

# 9. VectorAssembler + StandardScaler
drop_cols = ["Date", "gold_last", "gold_change_percent", "target"]
feature_cols = [c for c in df.columns if c not in drop_cols]

assembler = VectorAssembler(inputCols=feature_cols, outputCol="features_raw")
scaler = StandardScaler(inputCol="features_raw", outputCol="features")

train_vec = assembler.transform(train_df)
train_scaled = scaler.fit(train_vec).transform(train_vec)

test_vec = assembler.transform(test_df)
test_scaled = scaler.fit(train_vec).transform(test_vec)

# 10. Định nghĩa mô hình và lưu kết quả
models = {
    "Random Forest": RandomForestRegressor(labelCol="target", featuresCol="features", numTrees=100, seed=42),
    "Linear Regression": LinearRegression(labelCol="target", featuresCol="features")
}

results = []
evaluator = RegressionEvaluator(labelCol="target", predictionCol="prediction")

for name, model in models.items():
    fitted_model = model.fit(train_scaled)
    train_pred = fitted_model.transform(train_scaled)
    test_pred = fitted_model.transform(test_scaled)

    mae = evaluator.setMetricName("mae").evaluate(test_pred)
    mse = evaluator.setMetricName("mse").evaluate(test_pred)
    rmse = evaluator.setMetricName("rmse").evaluate(test_pred)
    r2 = evaluator.setMetricName("r2").evaluate(test_pred)
    r2_train = evaluator.evaluate(train_pred)
    mean_target = test_pred.select("target").rdd.map(lambda x: x[0]).mean()
    accuracy = 1 - (mae / mean_target)

    print(f"\n🔎 Mô hình: {name}")
    print(f"MAE  : {mae:.4f}")
    print(f"MSE  : {mse:.4f}")
    print(f"RMSE : {rmse:.4f}")
    print(f"R2 Test : {r2:.4f}")
    print(f"R2 Train: {r2_train:.4f}")
    print(f"Accuracy: {accuracy:.4f}")

    overfit_status = "Tốt"
    if r2_train - r2 > 0.1:
        overfit_status = "Overfit"
    elif r2 - r2_train > 0.1:
        overfit_status = "Underfit"

    results.append({
        "Model": name,
        "MAE": mae,
        "MSE": mse,
        "RMSE": rmse,
        "R2 Test": r2,
        "R2 Train": r2_train,
        "Accuracy": accuracy,
        "Fit Status": overfit_status
    })

# 11. In bảng so sánh kết quả
df_result = pd.DataFrame(results).sort_values("R2 Test", ascending=False)
print("\n📊 Bảng so sánh mô hình:")
print(df_result.to_string(index=False))

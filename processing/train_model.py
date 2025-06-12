import os
import pandas as pd
import matplotlib.pyplot as plt

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lag
from pyspark.sql.window import Window
from pyspark.sql.types import DoubleType

from pyspark.ml.feature import VectorAssembler
from pyspark.ml.regression import LinearRegression, RandomForestRegressor
from pyspark.ml import Pipeline
from pyspark.ml.evaluation import RegressionEvaluator

N_LAGS = 5
DATA_FILE = "data/merged_gold_data.csv"

def prepare_data(spark, input_csv, n_lags):
    df_pd = pd.read_csv(input_csv, parse_dates=["Date"])
    df_pd = df_pd.sort_values("Date").ffill()
    df = spark.createDataFrame(df_pd)

    features = [c for c in df.columns if c.startswith(("dxy_", "sp500_", "gold_", "oil_"))]
    features = [f for f in features if f not in ["gold_last", "gold_change_percent"]]

    for feat in features:
        df = df.withColumn(feat, col(feat).cast(DoubleType()))

    window_spec = Window.orderBy("Date")
    for feat in features:
        for i in range(1, n_lags + 1):
            df = df.withColumn(f"{feat}_lag_{i}", lag(col(feat), i).over(window_spec))

    df = df.orderBy("Date").dropna()

    # Assemble features
    lag_features = [col for col in df.columns if "_lag_" in col]
    assembler = VectorAssembler(inputCols=lag_features, outputCol="features")
    df = assembler.transform(df)

    return df

def evaluate_and_plot(model, test_df, model_name, results):
    predictions = model.transform(test_df)
    predictions_pd = predictions.select("Date", "gold_close", "prediction").toPandas()
    predictions_pd = predictions_pd.sort_values("Date")

    results[model_name] = predictions_pd

    evaluator = RegressionEvaluator(labelCol="gold_close", predictionCol="prediction", metricName="rmse")
    rmse = evaluator.evaluate(predictions)
    print(f"📊 {model_name} RMSE: {rmse:.4f}")

def plot_models(results_dict):
    plt.figure(figsize=(12, 6))

    for model_name, df in results_dict.items():
        plt.plot(df["Date"], df["prediction"], label=f"{model_name} Prediction")

    if results_dict:
        df = next(iter(results_dict.values()))
        plt.plot(df["Date"], df["gold_close"], label="Actual Gold Close", linestyle="--", color="black")

    plt.xlabel("Date")
    plt.ylabel("Gold Close Price (USD)")
    plt.title("So sánh mô hình dự đoán giá vàng")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    os.makedirs("output", exist_ok=True)
    plt.savefig("output/model_comparison.png")
    print("Đã lưu biểu đồ tại: output/model_comparison.png")

    plt.show()

def main():
    spark = SparkSession.builder.appName("TrainGoldPriceModels").getOrCreate()
    print("SparkSession started.")

    df = prepare_data(spark, DATA_FILE, N_LAGS)

    train_df, test_df = df.randomSplit([0.8, 0.2], seed=42)

    results = {}

    # Linear Regression
    lr = LinearRegression(featuresCol="features", labelCol="gold_close", predictionCol="prediction")
    lr_pipeline = Pipeline(stages=[lr])
    lr_model = lr_pipeline.fit(train_df)
    lr_model.save("models/linear_regression_pipeline")
    evaluate_and_plot(lr_model, test_df, "Linear Regression", results)

    # Random Forest
    rf = RandomForestRegressor(featuresCol="features", labelCol="gold_close", predictionCol="prediction", numTrees=100)
    rf_pipeline = Pipeline(stages=[rf])
    rf_model = rf_pipeline.fit(train_df)
    rf_model.save("models/random_forest_pipeline")
    evaluate_and_plot(rf_model, test_df, "Random Forest", results)

    # Plot comparison
    plot_models(results)

    spark.stop()

if __name__ == "__main__":
    main()
